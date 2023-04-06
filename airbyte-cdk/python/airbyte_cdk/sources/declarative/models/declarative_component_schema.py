#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

# generated by datamodel-codegen:
#   filename:  declarative_component_schema.yaml

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Extra, Field
from typing_extensions import Literal


class AddedFieldDefinition(BaseModel):
    type: Literal["AddedFieldDefinition"]
    path: List[str]
    value: str
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class AddFields(BaseModel):
    type: Literal["AddFields"]
    fields: List[AddedFieldDefinition]
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class ApiKeyAuthenticator(BaseModel):
    type: Literal["ApiKeyAuthenticator"]
    api_token: str
    header: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class BasicHttpAuthenticator(BaseModel):
    type: Literal["BasicHttpAuthenticator"]
    username: str = Field(
        ...,
        description="The username that will be combined with the password, base64 encoded and used to make requests",
    )
    password: Optional[str] = Field(
        "",
        description="The password that will be combined with the username, base64 encoded and used to make requests",
    )
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class BearerAuthenticator(BaseModel):
    type: Literal["BearerAuthenticator"]
    api_token: str
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class CheckStream(BaseModel):
    type: Literal["CheckStream"]
    stream_names: List[str]


class ConstantBackoffStrategy(BaseModel):
    type: Literal["ConstantBackoffStrategy"]
    backoff_time_in_seconds: Union[float, str]
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class CustomAuthenticator(BaseModel):
    class Config:
        extra = Extra.allow

    type: Literal["CustomAuthenticator"]
    class_name: str
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class CustomBackoffStrategy(BaseModel):
    class Config:
        extra = Extra.allow

    type: Literal["CustomBackoffStrategy"]
    class_name: str
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class CustomErrorHandler(BaseModel):
    class Config:
        extra = Extra.allow

    type: Literal["CustomErrorHandler"]
    class_name: str
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class CustomIncrementalSync(BaseModel):
    class Config:
        extra = Extra.allow

    type: Literal["CustomIncrementalSync"]
    class_name: str = Field(
        ...,
        description="The class that will be implementing the custom incremental sync. The format is `source_<name>.<package>.<class_name>`",
    )
    cursor_field: str = Field(
        ...,
        description="The location of the value on a record that will be used as a bookmark during sync",
    )
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class CustomPaginationStrategy(BaseModel):
    class Config:
        extra = Extra.allow

    type: Literal["CustomPaginationStrategy"]
    class_name: str
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class CustomRecordExtractor(BaseModel):
    class Config:
        extra = Extra.allow

    type: Literal["CustomRecordExtractor"]
    class_name: str
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class CustomRequester(BaseModel):
    class Config:
        extra = Extra.allow

    type: Literal["CustomRequester"]
    class_name: str
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class CustomRetriever(BaseModel):
    class Config:
        extra = Extra.allow

    type: Literal["CustomRetriever"]
    class_name: str
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class CustomPartitionRouter(BaseModel):
    class Config:
        extra = Extra.allow

    type: Literal["CustomPartitionRouter"]
    class_name: str
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class CustomTransformation(BaseModel):
    class Config:
        extra = Extra.allow

    type: Literal["CustomTransformation"]
    class_name: str
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class OAuthAuthenticator(BaseModel):
    type: Literal["OAuthAuthenticator"]
    client_id: str
    client_secret: str
    refresh_token: str
    token_refresh_endpoint: str
    access_token_name: Optional[str] = "access_token"
    expires_in_name: Optional[str] = "expires_in"
    grant_type: Optional[str] = "refresh_token"
    refresh_request_body: Optional[Dict[str, Any]] = None
    scopes: Optional[List[str]] = None
    token_expiry_date: Optional[str] = None
    token_expiry_date_format: Optional[str] = Field(
        None,
        description="The format of the datetime; provide it if expires_in is returned in datetime instead of seconds",
    )
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class SingleUseRefreshTokenOAuthAuthenticator(BaseModel):
    type: Literal["SingleUseRefreshTokenOAuthAuthenticator"]
    token_refresh_endpoint: str
    client_id_config_path: Optional[List[str]] = ["credentials", "client_id"]
    client_secret_config_path: Optional[List[str]] = ["credentials", "client_secret"]
    access_token_config_path: Optional[List[str]] = ["credentials", "access_token"]
    refresh_token_config_path: Optional[List[str]] = ["credentials", "refresh_token"]
    token_expiry_date_config_path: Optional[List[str]] = [
        "credentials",
        "token_expiry_date",
    ]
    access_token_name: Optional[str] = "access_token"
    refresh_token_name: Optional[str] = "refresh_token"
    expires_in_name: Optional[str] = "expires_in"
    grant_type: Optional[str] = "refresh_token"
    refresh_request_body: Optional[Dict[str, Any]] = None
    scopes: Optional[List[str]] = None
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class ExponentialBackoffStrategy(BaseModel):
    type: Literal["ExponentialBackoffStrategy"]
    factor: Optional[Union[float, str]] = 5
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class HttpMethodEnum(Enum):
    GET = "GET"
    POST = "POST"


class Action(Enum):
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    RETRY = "RETRY"
    IGNORE = "IGNORE"


class HttpResponseFilter(BaseModel):
    type: Literal["HttpResponseFilter"]
    action: Action
    error_message: Optional[str] = None
    error_message_contains: Optional[str] = None
    http_codes: Optional[List[int]] = None
    predicate: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class InlineSchemaLoader(BaseModel):
    type: Literal["InlineSchemaLoader"]
    schema_: Optional[Dict[str, Any]] = Field(None, alias="schema")


class JsonFileSchemaLoader(BaseModel):
    type: Literal["JsonFileSchemaLoader"]
    file_path: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class JsonDecoder(BaseModel):
    type: Literal["JsonDecoder"]


class MinMaxDatetime(BaseModel):
    type: Literal["MinMaxDatetime"]
    datetime: str
    datetime_format: Optional[str] = ""
    max_datetime: Optional[str] = None
    min_datetime: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class NoPagination(BaseModel):
    type: Literal["NoPagination"]


class OffsetIncrement(BaseModel):
    type: Literal["OffsetIncrement"]
    page_size: Union[int, str] = Field(..., description="The number of records to request")
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class PageIncrement(BaseModel):
    type: Literal["PageIncrement"]
    page_size: int = Field(..., description="The number of records to request")
    start_from_page: Optional[int] = 0
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class PrimaryKey(BaseModel):
    __root__: Union[str, List[str], List[List[str]]] = Field(..., description="The stream field to be used to distinguish unique rows")


class RecordFilter(BaseModel):
    type: Literal["RecordFilter"]
    condition: Optional[str] = Field(
        "",
        description="The predicate to filter a record. Records will be removed if evaluated to False",
    )
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class RemoveFields(BaseModel):
    type: Literal["RemoveFields"]
    field_pointers: List[List[str]]


class RequestPath(BaseModel):
    type: Literal["RequestPath"]


class InjectInto(Enum):
    request_parameter = "request_parameter"
    header = "header"
    body_data = "body_data"
    body_json = "body_json"


class RequestOption(BaseModel):
    type: Literal["RequestOption"]
    field_name: str
    inject_into: InjectInto


class Schemas(BaseModel):
    pass

    class Config:
        extra = Extra.allow


class SessionTokenAuthenticator(BaseModel):
    type: Literal["SessionTokenAuthenticator"]
    api_url: str
    header: str
    login_url: str
    session_token: str
    session_token_response_key: str
    username: str
    validate_session_url: str
    password: Optional[str] = ""
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class AuthFlowType(Enum):
    oauth2_0 = "oauth2.0"
    oauth1_0 = "oauth1.0"


class OAuthConfigSpecification(BaseModel):
    class Config:
        extra = Extra.allow

    oauth_user_input_from_connector_config_specification: Optional[Dict[str, Any]] = Field(
        None,
        description="OAuth specific blob. This is a Json Schema used to validate Json configurations used as input to OAuth.\nMust be a valid non-nested JSON that refers to properties from ConnectorSpecification.connectionSpecification\nusing special annotation 'path_in_connector_config'.\nThese are input values the user is entering through the UI to authenticate to the connector, that might also shared\nas inputs for syncing data via the connector.\nExamples:\nif no connector values is shared during oauth flow, oauth_user_input_from_connector_config_specification=[]\nif connector values such as 'app_id' inside the top level are used to generate the API url for the oauth flow,\n  oauth_user_input_from_connector_config_specification={\n    app_id: {\n      type: string\n      path_in_connector_config: ['app_id']\n    }\n  }\nif connector values such as 'info.app_id' nested inside another object are used to generate the API url for the oauth flow,\n  oauth_user_input_from_connector_config_specification={\n    app_id: {\n      type: string\n      path_in_connector_config: ['info', 'app_id']\n    }\n  }",
        examples=[
            {"app_id": {"type": "string", "path_in_connector_config": ["app_id"]}},
            {
                "app_id": {
                    "type": "string",
                    "path_in_connector_config": ["info", "app_id"],
                }
            },
        ],
        title="OAuth user input",
    )
    complete_oauth_output_specification: Optional[Dict[str, Any]] = Field(
        None,
        description="OAuth specific blob. This is a Json Schema used to validate Json configurations produced by the OAuth flows as they are\nreturned by the distant OAuth APIs.\nMust be a valid JSON describing the fields to merge back to `ConnectorSpecification.connectionSpecification`.\nFor each field, a special annotation `path_in_connector_config` can be specified to determine where to merge it,\nExamples:\n    complete_oauth_output_specification={\n      refresh_token: {\n        type: string,\n        path_in_connector_config: ['credentials', 'refresh_token']\n      }\n    }",
        examples=[
            {
                "refresh_token": {
                    "type": "string,",
                    "path_in_connector_config": ["credentials", "refresh_token"],
                }
            }
        ],
        title="OAuth output specification",
    )
    complete_oauth_server_input_specification: Optional[Dict[str, Any]] = Field(
        None,
        description="OAuth specific blob. This is a Json Schema used to validate Json configurations persisted as Airbyte Server configurations.\nMust be a valid non-nested JSON describing additional fields configured by the Airbyte Instance or Workspace Admins to be used by the\nserver when completing an OAuth flow (typically exchanging an auth code for refresh token).\nExamples:\n    complete_oauth_server_input_specification={\n      client_id: {\n        type: string\n      },\n      client_secret: {\n        type: string\n      }\n    }",
        examples=[{"client_id": {"type": "string"}, "client_secret": {"type": "string"}}],
        title="OAuth input specification",
    )
    complete_oauth_server_output_specification: Optional[Dict[str, Any]] = Field(
        None,
        description="OAuth specific blob. This is a Json Schema used to validate Json configurations persisted as Airbyte Server configurations that\nalso need to be merged back into the connector configuration at runtime.\nThis is a subset configuration of `complete_oauth_server_input_specification` that filters fields out to retain only the ones that\nare necessary for the connector to function with OAuth. (some fields could be used during oauth flows but not needed afterwards, therefore\nthey would be listed in the `complete_oauth_server_input_specification` but not `complete_oauth_server_output_specification`)\nMust be a valid non-nested JSON describing additional fields configured by the Airbyte Instance or Workspace Admins to be used by the\nconnector when using OAuth flow APIs.\nThese fields are to be merged back to `ConnectorSpecification.connectionSpecification`.\nFor each field, a special annotation `path_in_connector_config` can be specified to determine where to merge it,\nExamples:\n      complete_oauth_server_output_specification={\n        client_id: {\n          type: string,\n          path_in_connector_config: ['credentials', 'client_id']\n        },\n        client_secret: {\n          type: string,\n          path_in_connector_config: ['credentials', 'client_secret']\n        }\n      }",
        examples=[
            {
                "client_id": {
                    "type": "string,",
                    "path_in_connector_config": ["credentials", "client_id"],
                },
                "client_secret": {
                    "type": "string,",
                    "path_in_connector_config": ["credentials", "client_secret"],
                },
            }
        ],
        title="OAuth server output specification",
    )


class WaitTimeFromHeader(BaseModel):
    type: Literal["WaitTimeFromHeader"]
    header: str
    regex: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class WaitUntilTimeFromHeader(BaseModel):
    type: Literal["WaitUntilTimeFromHeader"]
    header: str
    min_wait: Optional[Union[float, str]] = None
    regex: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class CursorPagination(BaseModel):
    type: Literal["CursorPagination"]
    cursor_value: str
    page_size: Optional[int] = None
    stop_condition: Optional[str] = None
    decoder: Optional[JsonDecoder] = None
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class DatetimeBasedCursor(BaseModel):
    type: Literal["DatetimeBasedCursor"]
    cursor_field: str = Field(
        ...,
        description="The location of the value on a record that will be used as a bookmark during sync",
    )
    datetime_format: str = Field(..., description="The format of the datetime")
    cursor_granularity: str = Field(
        ...,
        description="Smallest increment the datetime_format has (ISO 8601 duration) that is used to ensure the start of a slice does not overlap with the end of the previous one",
    )
    end_datetime: Union[str, MinMaxDatetime] = Field(
        ...,
        description="The datetime that determines the last record that should be synced",
    )
    start_datetime: Union[str, MinMaxDatetime] = Field(
        ...,
        description="The datetime that determines the earliest record that should be synced",
    )
    step: str = Field(..., description="The size of the time window (ISO8601 duration)")
    end_time_option: Optional[RequestOption] = Field(None, description="Request option for end time")
    lookback_window: Optional[str] = Field(
        None,
        description="How many days before start_datetime to read data for (ISO8601 duration)",
    )
    partition_field_end: Optional[str] = Field(None, description="Partition start time field")
    partition_field_start: Optional[str] = Field(None, description="Partition end time field")
    start_time_option: Optional[RequestOption] = Field(None, description="Request option for start time")
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class DefaultErrorHandler(BaseModel):
    type: Literal["DefaultErrorHandler"]
    backoff_strategies: Optional[
        List[
            Union[
                ConstantBackoffStrategy,
                CustomBackoffStrategy,
                ExponentialBackoffStrategy,
                WaitTimeFromHeader,
                WaitUntilTimeFromHeader,
            ]
        ]
    ] = None
    max_retries: Optional[int] = 5
    response_filters: Optional[List[HttpResponseFilter]] = None
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class DefaultPaginator(BaseModel):
    type: Literal["DefaultPaginator"]
    pagination_strategy: Union[CursorPagination, CustomPaginationStrategy, OffsetIncrement, PageIncrement]
    decoder: Optional[JsonDecoder] = None
    page_size_option: Optional[RequestOption] = None
    page_token_option: Optional[Union[RequestOption, RequestPath]] = None
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class DpathExtractor(BaseModel):
    type: Literal["DpathExtractor"]
    field_path: List[str]
    decoder: Optional[JsonDecoder] = None
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class ListPartitionRouter(BaseModel):
    type: Literal["ListPartitionRouter"]
    cursor_field: str
    values: Union[str, List[str]]
    request_option: Optional[RequestOption] = None
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class RecordSelector(BaseModel):
    type: Literal["RecordSelector"]
    extractor: Union[CustomRecordExtractor, DpathExtractor]
    record_filter: Optional[RecordFilter] = None
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class AuthFlow(BaseModel):
    auth_flow_type: Optional[AuthFlowType] = Field(None, description="The type of auth to use", title="Auth flow type")
    predicate_key: Optional[List[str]] = Field(
        None,
        description="Json Path to a field in the connectorSpecification that should exist for the advanced auth to be applicable.",
        examples=[["credentials", "auth_type"]],
        title="Predicate key",
    )
    predicate_value: Optional[str] = Field(
        None,
        description="Value of the predicate_key fields for the advanced auth to be applicable.",
        examples=["Oauth"],
        title="Predicate value",
    )
    oauth_config_specification: Optional[OAuthConfigSpecification] = None


class CompositeErrorHandler(BaseModel):
    type: Literal["CompositeErrorHandler"]
    error_handlers: List[Union[CompositeErrorHandler, DefaultErrorHandler]]
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class HttpRequester(BaseModel):
    type: Literal["HttpRequester"]
    path: str = Field(..., description="The specific endpoint to fetch data from for a resource.")
    url_base: str = Field(..., description="The root of the API source.")
    authenticator: Optional[
        Union[
            ApiKeyAuthenticator,
            BasicHttpAuthenticator,
            BearerAuthenticator,
            CustomAuthenticator,
            OAuthAuthenticator,
            SingleUseRefreshTokenOAuthAuthenticator,
            SessionTokenAuthenticator,
        ]
    ] = Field(
        None,
        description="Authenticator component that defines how to authenticate to the source.",
    )
    error_handler: Optional[Union[DefaultErrorHandler, CustomErrorHandler, CompositeErrorHandler]] = Field(
        None, description="Error handler component that defines how to handle errors."
    )
    http_method: Optional[Union[str, HttpMethodEnum]] = Field(
        "GET",
        description="The HTTP method used to fetch data from the source (can be GET or POST).",
    )
    request_body_data: Optional[Union[str, Dict[str, str]]] = Field(
        None,
        description="Specifies how to populate the body of the request with a non-JSON payload. If returns a ready text that it will be sent as is. If returns a dict that it will be converted to a urlencoded form.",
    )
    request_body_json: Optional[Union[str, Dict[str, str]]] = Field(
        None,
        description="Specifies how to populate the body of the request with a JSON payload.",
    )
    request_headers: Optional[Union[str, Dict[str, str]]] = Field(
        None,
        description="Return any non-auth headers. Authentication headers will overwrite any overlapping headers returned from this method.",
    )
    request_parameters: Optional[Union[str, Dict[str, str]]] = Field(
        None,
        description="Specifies the query parameters that should be set on an outgoing HTTP request given the inputs.",
    )
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class Spec(BaseModel):
    type: Literal["Spec"]
    connection_specification: Dict[str, Any]
    documentation_url: Optional[str] = None
    advanced_auth: Optional[AuthFlow] = None


class DeclarativeSource(BaseModel):
    class Config:
        extra = Extra.forbid

    type: Literal["DeclarativeSource"]
    check: CheckStream
    streams: List[DeclarativeStream]
    version: str
    schemas: Optional[Schemas] = None
    definitions: Optional[Dict[str, Any]] = None
    spec: Optional[Spec] = None


class DeclarativeStream(BaseModel):
    class Config:
        extra = Extra.allow

    type: Literal["DeclarativeStream"]
    retriever: Union[CustomRetriever, SimpleRetriever]
    incremental_sync: Optional[Union[CustomIncrementalSync, DatetimeBasedCursor]] = None
    name: Optional[str] = ""
    primary_key: Optional[PrimaryKey] = ""
    schema_loader: Optional[Union[InlineSchemaLoader, JsonFileSchemaLoader]] = None
    transformations: Optional[List[Union[AddFields, CustomTransformation, RemoveFields]]] = None
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class ParentStreamConfig(BaseModel):
    type: Literal["ParentStreamConfig"]
    parent_key: str
    stream: DeclarativeStream
    partition_field: str
    request_option: Optional[RequestOption] = None
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class SimpleRetriever(BaseModel):
    type: Literal["SimpleRetriever"]
    record_selector: RecordSelector = Field(
        ...,
        description="Component that describes how to extract records from a HTTP response.",
    )
    requester: Union[CustomRequester, HttpRequester] = Field(
        ...,
        description="Requester component that describes how to prepare HTTP requests to send to the source API.",
    )
    paginator: Optional[Union[DefaultPaginator, NoPagination]] = Field(
        None,
        description="Paginator component that describes how to navigate through the API's pages.",
    )
    partition_router: Optional[
        Union[
            CustomPartitionRouter,
            ListPartitionRouter,
            SubstreamPartitionRouter,
            List[Union[CustomPartitionRouter, ListPartitionRouter, SubstreamPartitionRouter]],
        ]
    ] = Field(
        [],
        description="StreamSlicer component that describes how to partition the stream, enabling incremental syncs and checkpointing.",
    )
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


class SubstreamPartitionRouter(BaseModel):
    type: Literal["SubstreamPartitionRouter"]
    parent_stream_configs: List[ParentStreamConfig]
    parameters: Optional[Dict[str, Any]] = Field(None, alias="$parameters")


CompositeErrorHandler.update_forward_refs()
DeclarativeSource.update_forward_refs()
DeclarativeStream.update_forward_refs()
SimpleRetriever.update_forward_refs()
