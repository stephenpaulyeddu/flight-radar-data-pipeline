#!/bin/bash

echo "⏳ Waiting for services..."
sleep 60

echo "🔍 Checking Mongo replica set..."

docker exec mongo mongosh --eval '
try {
  var status = rs.status();
  print("Replica set already initialized");
} catch (e) {
  print("Initializing replica set...");
  rs.initiate();
}
'

# echo "🔧 Ensuring correct replica host..."

# docker exec mongo mongosh --eval '
# cfg = rs.conf();
# if (cfg.members[0].host != "mongo:27017") {
#   cfg.members[0].host = "mongo:27017";
#   rs.reconfig(cfg, { force: true });
#   print("Replica host updated");
# } else {
#   print("Replica host already correct");
# }
# '

echo "🔁 Restarting Kafka Connect..."
docker restart kafka-connect

echo "⏳ Waiting for Kafka Connect..."
sleep 15

echo "🔍 Checking Kafka Connect..."
curl -s http://localhost:8083 || exit 1

echo "🚀 Creating/updating Debezium connector..."

curl -X PUT http://localhost:8083/connectors/mongo-flight-connector/config \
-H "Content-Type: application/json" \
-d '{
  "connector.class": "io.debezium.connector.mongodb.MongoDbConnector",
  "mongodb.connection.string": "mongodb://mongo:27017/?replicaSet=rs0",
  "mongodb.name": "mongo-flight-cluster",
  "database.include.list": "flight_db",
  "collection.include.list": "flight_db.flight_summaries",
  "topic.prefix": "mongo",
  "tasks.max": "1"
}'

echo "✅ Setup complete"