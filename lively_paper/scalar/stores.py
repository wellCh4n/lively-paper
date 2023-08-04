from typing import Dict, Optional

from pymongo import MongoClient


class Store:
    client: MongoClient
    connection: str

    def __init__(self, connection: str) -> None:
        self.connection = connection
        self.client = MongoClient(connection)
        self.db = self.client['chat_history']
        self.collection = self.db['history']
        self.collection.create_index('SessionId')
        super().__init__()

    def insert(self, data: Dict):
        self.collection.insert_one(data)

    def list(self, data: Optional[Dict] = None):
        result = []
        if data:
            cursor = self.collection.find(data)
        else:
            cursor = self.collection.find({})
        for document in cursor:
            document['_id'] = str(document['_id'])
            result.append(document)
        return result


connection_string = 'mongodb://127.0.0.1:27017'
scalar_store: Store = Store(connection_string)
