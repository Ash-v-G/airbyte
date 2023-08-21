/*
 * Copyright (c) 2023 Airbyte, Inc., all rights reserved.
 */

package io.airbyte.integrations.debezium.internals.mongodb;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.fasterxml.jackson.databind.JsonNode;
import com.mongodb.client.ChangeStreamIterable;
import com.mongodb.client.MongoChangeStreamCursor;
import com.mongodb.client.MongoClient;
import com.mongodb.client.model.changestream.ChangeStreamDocument;
import io.debezium.connector.mongodb.ResumeTokens;
import org.bson.BsonDocument;
import org.bson.BsonString;
import org.bson.BsonTimestamp;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class MongodbDebeziumStateUtilTest {

  private MongodbDebeziumStateUtil mongodbDebeziumStateUtil;

  @BeforeEach
  void setup() {
    mongodbDebeziumStateUtil = new MongodbDebeziumStateUtil();
  }

  @Test
  void testConstructInitialDebeziumState() {
    final String database = "test";
    final String replicaSet = "test_rs";
    final String resumeToken = "8264BEB9F3000000012B0229296E04";
    final BsonDocument resumeTokenDocument = mock(BsonDocument.class);
    final ChangeStreamIterable changeStreamIterable = mock(ChangeStreamIterable.class);
    final MongoChangeStreamCursor<ChangeStreamDocument<BsonDocument>> mongoChangeStreamCursor =
        mock(MongoChangeStreamCursor.class);
    final MongoClient mongoClient = mock(MongoClient.class);

    when(resumeTokenDocument.containsKey("_data")).thenReturn(true);
    when(resumeTokenDocument.get("_data")).thenReturn(new BsonString(resumeToken));
    when(mongoChangeStreamCursor.getResumeToken()).thenReturn(resumeTokenDocument);
    when(changeStreamIterable.cursor()).thenReturn(mongoChangeStreamCursor);
    when(mongoClient.watch(BsonDocument.class)).thenReturn(changeStreamIterable);

    final JsonNode initialState = mongodbDebeziumStateUtil.constructInitialDebeziumState(mongoClient,
        database, replicaSet);

    assertNotNull(initialState);
    assertEquals(1, initialState.size());
    final BsonTimestamp timestamp = ResumeTokens.getTimestamp(resumeTokenDocument);
    final JsonNode offsetState = initialState.fields().next().getValue();
    assertEquals(resumeToken, offsetState.get(MongodbDebeziumConstants.OffsetState.VALUE_RESUME_TOKEN).asText());
    assertEquals(timestamp.getTime(), offsetState.get(MongodbDebeziumConstants.OffsetState.VALUE_SECONDS).asInt());
    assertEquals(timestamp.getInc(), offsetState.get(MongodbDebeziumConstants.OffsetState.VALUE_INCREMENT).asInt());
    assertEquals("null", offsetState.get(MongodbDebeziumConstants.OffsetState.VALUE_TRANSACTION_ID).asText());
  }

}
