#
# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
#

import copy
import json
import logging
from functools import cache
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Union

from airbyte_cdk.models import AirbyteLogMessage, AirbyteMessage, AirbyteStream, Level, SyncMode, Type
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.file_based.availability_strategy import AbstractFileBasedAvailabilityStrategy
from airbyte_cdk.sources.file_based.config.file_based_stream_config import FileBasedStreamConfig
from airbyte_cdk.sources.file_based.file_types.file_type_parser import FileTypeParser
from airbyte_cdk.sources.file_based.remote_file import RemoteFile
from airbyte_cdk.sources.file_based.schema_validation_policies import AbstractSchemaValidationPolicy
from airbyte_cdk.sources.file_based.stream import AbstractFileBasedStream
from airbyte_cdk.sources.file_based.stream.concurrent.cursor import FileBasedNoopCursor
from airbyte_cdk.sources.message import MessageRepository
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.concurrent.default_stream import FileBasedDefaultStream
from airbyte_cdk.sources.streams.concurrent.exceptions import ExceptionWithDisplayMessage
from airbyte_cdk.sources.streams.concurrent.partitions.partition import Partition
from airbyte_cdk.sources.streams.concurrent.partitions.partition_generator import PartitionGenerator
from airbyte_cdk.sources.streams.concurrent.partitions.record import Record
from airbyte_cdk.sources.streams.core import StreamData
from airbyte_cdk.sources.utils.slice_logger import SliceLogger
from deprecated.classic import deprecated

"""
This module contains adapters to help enabling concurrency on File-based Stream objects without needing to migrate to AbstractStream
"""


@deprecated("This class is experimental. Use at your own risk.")
class FileBasedStreamFacade(Stream):
    @classmethod
    def create_from_stream(
        cls,
        stream: AbstractFileBasedStream,
        source: AbstractSource,
        logger: logging.Logger,
        state: Optional[MutableMapping[str, Any]],
        cursor: FileBasedNoopCursor,
    ) -> "FileBasedStreamFacade":
        """
        Create a ConcurrentStream from a FileBasedStream object.
        """
        pk = cls._get_primary_key_from_stream(stream.primary_key)
        cursor_field = cls._get_cursor_field_from_stream(stream)

        if not source.message_repository:
            raise ValueError(
                "A message repository is required to emit non-record messages. Please set the message repository on the source."
            )

        message_repository = source.message_repository
        return FileBasedStreamFacade(
            FileBasedDefaultStream(  # type: ignore
                stream,
                partition_generator=FileBasedStreamPartitionGenerator(
                    stream,
                    message_repository,
                    SyncMode.full_refresh if isinstance(cursor, FileBasedNoopCursor) else SyncMode.incremental,
                    [cursor_field] if cursor_field is not None else None,
                    state,
                    cursor,
                ),
                name=stream.name,
                namespace=stream.namespace,
                json_schema=stream.get_json_schema(),
                primary_key=pk,
                cursor_field=cursor_field,
                logger=logger,
            ),
            stream,
            cursor,
            logger=logger,
            slice_logger=source._slice_logger,
        )

    def __init__(
        self,
        stream: FileBasedDefaultStream,
        legacy_stream: AbstractFileBasedStream,
        cursor: FileBasedNoopCursor,
        slice_logger: SliceLogger,
        logger: logging.Logger,
    ):
        """
        :param stream: The underlying AbstractStream
        """
        self._abstract_stream = stream
        self._legacy_stream = legacy_stream
        self._cursor = cursor
        self._slice_logger = slice_logger
        self._logger = logger

    @property
    def availability_strategy(self) -> AbstractFileBasedAvailabilityStrategy:
        return self._legacy_stream.availability_strategy

    def get_parser(self) -> FileTypeParser:
        return self._legacy_stream.get_parser()

    @property
    def config(self) -> FileBasedStreamConfig:
        return self._legacy_stream.config

    def get_files(self) -> Iterable[RemoteFile]:
        return self._legacy_stream.get_files()

    @property
    def catalog_schema(self) -> Optional[Mapping[str, Any]]:
        return self._legacy_stream.catalog_schema

    @property
    def validation_policy(self) -> AbstractSchemaValidationPolicy:
        return self._legacy_stream.validation_policy

    @cache
    def get_json_schema(self) -> Mapping[str, Any]:
        return self._legacy_stream.get_json_schema()

    @property
    def supports_incremental(self) -> bool:
        return self._legacy_stream.supports_incremental

    def read_records(
        self,
        sync_mode: SyncMode,
        cursor_field: Optional[List[str]] = None,
        stream_slice: Optional[Mapping[str, Any]] = None,
        stream_state: Optional[Mapping[str, Any]] = None,
    ) -> Iterable[StreamData]:
        try:
            yield from self._read_records()
        except Exception as exc:
            if hasattr(self._cursor, "state"):
                state = str(self._cursor.state)
            else:
                # This shouldn't happen if the ConcurrentCursor was used
                state = "unknown; no state attribute was available on the cursor"
            yield AirbyteMessage(
                type=Type.LOG, log=AirbyteLogMessage(level=Level.ERROR, message=f"Cursor State at time of exception: {state}")
            )
            raise exc

    def _read_records(self) -> Iterable[StreamData]:
        for partition in self._abstract_stream.generate_partitions():
            if self._slice_logger.should_log_slice_message(self._logger):
                yield self._slice_logger.create_slice_log_message(partition.to_slice())
            for record in partition.read():
                yield record.data

    @property
    def name(self) -> str:
        return self._abstract_stream.name

    @property
    def primary_key(self) -> Optional[Union[str, List[str], List[List[str]]]]:
        return self._legacy_stream.config.primary_key or self.get_parser().get_parser_defined_primary_key(self._legacy_stream.config)

    @classmethod
    def _get_primary_key_from_stream(cls, stream_primary_key: Optional[Union[str, List[str], List[List[str]]]]) -> List[str]:
        if stream_primary_key is None:
            return []
        elif isinstance(stream_primary_key, str):
            return [stream_primary_key]
        elif isinstance(stream_primary_key, list):
            if len(stream_primary_key) > 0 and all(isinstance(k, str) for k in stream_primary_key):
                return stream_primary_key  # type: ignore # We verified all items in the list are strings
            else:
                raise ValueError(f"Nested primary keys are not supported. Found {stream_primary_key}")
        else:
            raise ValueError(f"Invalid type for primary key: {stream_primary_key}")

    @classmethod
    def _get_cursor_field_from_stream(cls, stream: AbstractFileBasedStream) -> Optional[str]:
        if isinstance(stream.cursor_field, list):
            if len(stream.cursor_field) > 1:
                raise ValueError(f"Nested cursor fields are not supported. Got {stream.cursor_field} for {stream.name}")
            elif len(stream.cursor_field) == 0:
                return None
            else:
                return stream.cursor_field[0]
        else:
            return stream.cursor_field

    def as_airbyte_stream(self) -> AirbyteStream:
        return self._abstract_stream.as_airbyte_stream()


class FileBasedStreamPartition(Partition):
    def __init__(
        self,
        stream: AbstractFileBasedStream,
        _slice: Optional[Mapping[str, Any]],
        message_repository: MessageRepository,
        sync_mode: SyncMode,
        cursor_field: Optional[List[str]],
        state: Optional[MutableMapping[str, Any]],
        cursor: FileBasedNoopCursor,
    ):
        self._stream = stream
        self._slice = _slice
        self._message_repository = message_repository
        self._sync_mode = sync_mode
        self._cursor_field = cursor_field
        self._state = state
        self._cursor = cursor
        self._is_closed = False

    def read(self) -> Iterable[Record]:
        if self._slice is None:
            raise RuntimeError(f"Empty slice for stream {self.stream_name()}. This is unexpected. Please contact Support.")
        try:
            for record_data in self._stream.read_records_from_slice(
                stream_slice=copy.deepcopy(self._slice),
            ):
                if isinstance(record_data, Mapping):
                    data_to_return = dict(record_data)
                    self._stream.transformer.transform(data_to_return, self._stream.get_json_schema())
                    yield Record(data_to_return, self.stream_name())
                else:
                    self._message_repository.emit_message(record_data)
        except Exception as e:
            display_message = self._stream.get_error_display_message(e)
            if display_message:
                raise ExceptionWithDisplayMessage(display_message) from e
            else:
                raise e

    def to_slice(self) -> Optional[Mapping[str, Any]]:
        if self._slice is None:
            return None
        assert (
            len(self._slice["files"]) == 1
        ), f"Expected 1 file per partition but got {len(self._slice['files'])} for stream {self.stream_name()}"
        file = self._slice["files"][0]
        return {file.uri: file}

    def close(self) -> None:
        self._cursor.close_partition(self)
        self._is_closed = True

    def is_closed(self) -> bool:
        return self._is_closed

    def __hash__(self) -> int:
        if self._slice:
            # Convert the slice to a string so that it can be hashed
            if len(self._slice["files"]) != 1:
                raise ValueError(f"THIS SHOULDN'T BE != 1!! {self._slice['files']}")
            else:
                s = json.dumps(f"{self._slice['files'][0].last_modified}_{self._slice['files'][0].uri}")
            return hash((self._stream.name, s))
        else:
            return hash(self._stream.name)

    def stream_name(self) -> str:
        return self._stream.name

    def __repr__(self) -> str:
        return f"FileBasedStreamPartition({self._stream.name}, {self._slice})"


class FileBasedStreamPartitionGenerator(PartitionGenerator):
    def __init__(
        self,
        stream: AbstractFileBasedStream,
        message_repository: MessageRepository,
        sync_mode: SyncMode,
        cursor_field: Optional[List[str]],
        state: Optional[MutableMapping[str, Any]],
        cursor: FileBasedNoopCursor,
    ):
        self._stream = stream
        self._message_repository = message_repository
        self._sync_mode = sync_mode
        self._cursor_field = cursor_field
        self._state = state
        self._cursor = cursor

    def generate(self) -> Iterable[FileBasedStreamPartition]:
        pending_partitions = []
        for _slice in self._stream.stream_slices(sync_mode=self._sync_mode, cursor_field=self._cursor_field, stream_state=self._state):
            if _slice is not None:
                pending_partitions.extend(
                    [
                        FileBasedStreamPartition(
                            self._stream,
                            {"files": [copy.deepcopy(f)]},
                            self._message_repository,
                            self._sync_mode,
                            self._cursor_field,
                            self._state,
                            self._cursor,
                        )
                        for f in _slice.get("files", [])
                    ]
                )
        self._cursor.set_pending_partitions(pending_partitions)
        yield from pending_partitions
