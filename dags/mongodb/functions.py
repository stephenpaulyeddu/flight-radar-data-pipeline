from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from mongodb.schema import flight_summary
from datetime import datetime


def get_collection():
    client = MongoClient("mongodb://mongo:27017/?replicaSet=rs0",
                        serverSelectionTimeoutMS=5000)
    db = client['flight_db']
    return db['flight_summaries']


def update_collection(data):

    record = flight_summary.get_records(data)
    record['_id'] = record.pop('fr24_id')
    collection = get_collection()

    try:
        collection.insert_one(record)
        print(f"Inserted: _id: {record['_id']}")

    except DuplicateKeyError:
        # _id already exists, update the document
        print(f"_id: {record['_id']} already exists!")
        update_fields = {k: v for k, v in record.items() if k != '_id'}
        collection.update_one({'_id': record['_id']}, {'$set': update_fields})
        print(f"Updated: {record['_id']} document")

    except Exception as e:
        print(f"Failed to insert/update _id: {record['_id']}: {e}")


def delete_record_by_id(doc_id):
    try:
        collection = get_collection()
        result = collection.delete_one({'_id': doc_id})
        if result.deleted_count == 1:
            print(f"Deleted: _id: {doc_id}")
        else:
            print(f"No document found with _id: {doc_id}")
    except Exception as e:
        print(f"Failed to delete _id: {doc_id}: {e}")


def create_collection():

    collection = get_collection()
    # Check if collection exists and is empty
    if collection.estimated_document_count() == 0:

        dummy_data = [{
            'fr24_id': 'test_1',
            'flight': 'EY237',
            'callsign': 'ETD237',
            'operating_as': 'ETD',
            'painted_as': 'ETD',
            'type': 'A21N',
            'reg': 'A6-AES',
            'orig_icao': 'VOBL',
            'orig_iata': 'BLR',
            'datetime_takeoff': '2025-07-12T10:54:34Z',
            'runway_takeoff': '27R',
            'dest_icao': 'OMAA',
            'dest_iata': 'AUH',
            'dest_icao_actual': 'OMAA',
            'dest_iata_actual': 'AUH',
            'datetime_landed': '2025-07-12T14:07:38Z',
            'runway_landed': '31R',
            'flight_time': 11584,
            'actual_distance': 2736.7,
            'circle_distance': 2726.33,
            'category': 'Passenger',
            'hex': '896678',
            'first_seen': '2025-07-12T10:42:16Z',
            'last_seen': '2025-07-12T14:08:47Z',
            'flight_ended': True
        }]

        record = flight_summary.get_records(dummy_data[0])
        record['_id'] = record.pop('fr24_id')

        try:
            collection.insert_one(record)
            print(f"Inserted dummy record: _id: {record['_id']}")
        except Exception as e:
            print(f"Failed to insert dummy record _id: {record['_id']}: {e}")


        # Create indexes
        try:
            collection.create_index([("first_seen", -1)])
            collection.create_index([("updated_at", -1)])
            collection.create_index([("flight_ended", -1)])
            collection.create_index([("datetime_takeoff",-1)])
            print("Indexes created on: first_seen, updated_at, flight_ended, datetime_takeoff")

        except Exception as index_err:
            print(f"Failed to create indexes: {index_err}")

    else:
        print("Collection already exists and is not empty. Skipping dummy insert.")



def get_non_ended_flight_records(last_updated: datetime):

    collection = get_collection()

    query = {
        "first_seen": {"$lte": last_updated},
        "updated_at": {"$lte": last_updated},
        "flight_ended": False
    }

    # Run the query
    results = collection.find(query)

    flight_list = []

    for data in results:
        flight_list.append(data)

    return flight_list


def get_non_started_flight_records(last_updated: datetime):

    collection = get_collection()
    
    query = {
        "first_seen": {"$lte": last_updated},
        "updated_at": {"$lte": last_updated},
        "datetime_takeoff": None
    }

    # Run the query
    results = collection.find(query)

    flight_list = []

    for data in results:
        flight_list.append(data)

    return flight_list
