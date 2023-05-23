/*
 * Copyright (c) 2023 Airbyte, Inc., all rights reserved.
 */

package io.airbyte.integrations.destination_async.state;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.google.common.collect.ImmutableMap;
import com.google.common.collect.Lists;
import io.airbyte.commons.json.Jsons;
import io.airbyte.integrations.destination_async.buffers.BufferManager;
import io.airbyte.integrations.destination_async.buffers.StreamAwareQueue;
import io.airbyte.protocol.models.v0.AirbyteMessage;
import io.airbyte.protocol.models.v0.AirbyteMessage.Type;
import io.airbyte.protocol.models.v0.AirbyteRecordMessage;
import io.airbyte.protocol.models.v0.AirbyteStateMessage;
import io.airbyte.protocol.models.v0.AirbyteStateMessage.AirbyteStateType;
import io.airbyte.protocol.models.v0.AirbyteStreamState;
import io.airbyte.protocol.models.v0.StreamDescriptor;
import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import org.apache.commons.lang.RandomStringUtils;
import org.junit.jupiter.api.Test;

class AsyncStateManagerTest {

  private static final String STREAM_NAME = "id_and_name";
  private static final String STREAM_NAME2 = STREAM_NAME + 2;
  private static final StreamDescriptor STREAM1_DESC = new StreamDescriptor()
      .withName(STREAM_NAME);
  private static final StreamDescriptor STREAM2_DESC = new StreamDescriptor()
      .withName(STREAM_NAME2);

  private static final AirbyteMessage GLOBAL_MESSAGE1 = new AirbyteMessage()
      .withType(Type.STATE)
      .withState(new AirbyteStateMessage()
          .withType(AirbyteStateType.GLOBAL));
  private static final AirbyteMessage STREAM_STATE_MESSAGE1 = new AirbyteMessage()
      .withType(Type.STATE)
      .withState(new AirbyteStateMessage()
          .withType(AirbyteStateType.STREAM)
          .withStream(new AirbyteStreamState().withStreamDescriptor(STREAM1_DESC).withStreamState(Jsons.jsonNode(1))));
  private static final AirbyteMessage STREAM_STATE_MESSAGE2 = new AirbyteMessage()
      .withType(Type.STATE)
      .withState(new AirbyteStateMessage()
          .withType(AirbyteStateType.STREAM)
          .withStream(new AirbyteStreamState().withStreamDescriptor(STREAM1_DESC).withStreamState(Jsons.jsonNode(2))));

  @Test
  void testEmptyQueues() {
    final ConcurrentMap<StreamDescriptor, StreamAwareQueue> buffers = new ConcurrentHashMap<>();
    final AsyncStateManager stateManager = new AsyncStateManager(buffers);
    stateManager.trackState(GLOBAL_MESSAGE1, 100);
    final List<AirbyteMessage> flush = stateManager.flush();

    assertEquals(GLOBAL_MESSAGE1, flush.get(0));
  }

  @Test
  void testStateAcrossMultipleStreams() throws InterruptedException {
    final ConcurrentMap<StreamDescriptor, StreamAwareQueue> buffers = new ConcurrentHashMap<>();
    buffers.put(STREAM1_DESC, new StreamAwareQueue(BufferManager.TOTAL_QUEUES_MAX_SIZE_LIMIT_BYTES));
    buffers.put(STREAM2_DESC, new StreamAwareQueue(BufferManager.TOTAL_QUEUES_MAX_SIZE_LIMIT_BYTES));
    final AsyncStateManager stateManager = new AsyncStateManager(buffers);

    final List<AirbyteMessage> stream1Records = generateRecords(1000, STREAM_NAME);
    long count = 0;
    for (final AirbyteMessage r : stream1Records) {
      buffers.get(STREAM1_DESC).offer(r, count++, 160);
    }

    final List<AirbyteMessage> stream2Records = generateRecords(1000, STREAM_NAME2);
    for (final AirbyteMessage r : stream2Records) {
      if (count % 1120 == 0) {
        stateManager.trackState(GLOBAL_MESSAGE1, count++);
      }
      buffers.get(STREAM2_DESC).offer(r, count++, 160);
    }

    stateManager.claim(STREAM2_DESC, 1500);
    // todo (cgardens) - the fact that i have to do this shows something is leaking.
    for (int i = 0; i < 500; i++) {
      buffers.get(STREAM2_DESC).take();
    }
    assertEquals(Optional.empty(), stateManager.fulfill(STREAM2_DESC, 1500));

    stateManager.claim(STREAM1_DESC, 900);
    for (int i = 0; i < 900; i++) {
      buffers.get(STREAM1_DESC).take();
    }
    assertEquals(Optional.empty(), stateManager.fulfill(STREAM1_DESC, 900));

    stateManager.claim(STREAM1_DESC, 1000);
    for (int i = 0; i < 100; i++) {
      buffers.get(STREAM1_DESC).take();
    }
    assertEquals(Optional.of(GLOBAL_MESSAGE1), stateManager.fulfill(STREAM1_DESC, 1000));
  }

  private static List<AirbyteMessage> generateRecords(final long numRecords, final String streamName) {
    final List<AirbyteMessage> output = Lists.newArrayList();
    for (int i = 0; i < numRecords; i++) {
      final JsonNode payload =
          Jsons.jsonNode(ImmutableMap.of("id", RandomStringUtils.randomAlphabetic(7), "name", "human " + String.format("%8d", i)));
      final AirbyteMessage airbyteMessage = new AirbyteMessage()
          .withType(Type.RECORD)
          .withRecord(new AirbyteRecordMessage()
              .withStream(streamName)
              .withEmittedAt(Instant.now().toEpochMilli())
              .withData(payload));
      output.add(airbyteMessage);
    }
    return output;
  }

}
