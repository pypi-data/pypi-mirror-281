import uuid
from pymongo import MongoClient
from bson.objectid import ObjectId

class BatchProcessor:
    def __init__(self, connection_string, database_name, collection_name):
        """
        Initializes the BatchProcessor with a connection to MongoDB.
        
        Args:
        - connection_string (str): The connection string for MongoDB.
        - database_name (str): The name of the database.
        - collection_name (str): The name of the collection.
        """
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name][collection_name]
        print(f"Connected to MongoDB database: {database_name}, collection: {collection_name}")

    def read_and_lock(self, size):
        """
        Reads and locks a specified number of records from the collection.
        
        Args:
        - size (int): The number of records to read and lock.
        
        Returns:
        - tuple: A batch ID and a list of locked records.
        """
        print(f"Attempting to read and lock {size} records...")
        records = self.db.find({
            '$or': [{'locked': False}, {'locked': {'$exists': False}}]
        }).limit(size)
        
        locked_records = []
        batch_id = str(uuid.uuid4())
        for record in records:
            print(f"Fetched record: {record}")
            update_fields = {'locked': True}
            if 'batch_identifier' not in record:
                update_fields['batch_identifier'] = batch_id
            self.db.update_one({'_id': record['_id']}, {'$set': update_fields})
            locked_records.append(record)
        
        print(f"Locked {len(locked_records)} records with batch ID: {batch_id}")
        return batch_id, locked_records

    def unlock_record(self, record_id):
        """
        Unlocks a single record by its ID.
        
        Args:
        - record_id (str): The ID of the record to unlock.
        """
        record_object_id = ObjectId(record_id)
        print(f"Unlocking record with ID: {record_object_id}")
        result = self.db.update_one({'_id': record_object_id}, {'$set': {'locked': False}})
        print(f"Unlocked record result: {result.raw_result}")

    def unlock_records(self, record_ids):
        """
        Unlocks multiple records by their IDs.
        
        Args:
        - record_ids (list): A list of record IDs to unlock.
        """
        for record_id in record_ids:
            self.unlock_record(record_id)

    def process_batches(self, size, total_records):
        """
        Processes batches of records by locking, processing, and unlocking them.
        
        Args:
        - size (int): The number of records per batch.
        - total_records (int): The total number of records to process.
        
        Yields:
        - tuple: A batch ID and a list of locked records for each batch.
        """
        batches = []
        for _ in range(0, total_records, size):
            batch_id, locked_records = self.read_and_lock(size)
            if not locked_records:
                print("No more records to lock and process.")
                break
            batches.append((batch_id, locked_records))
            yield batch_id, locked_records
