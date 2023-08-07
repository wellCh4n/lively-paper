from typing import Dict, Optional

from pymongo import MongoClient
from pymongo.collection import Collection


class Store:
    client: MongoClient
    connection: str
    collection_dict: Dict[str, Collection] = dict()

    def __init__(self, connection: str) -> None:
        self.connection = connection
        self.client = MongoClient(connection)
        self.db = self.client['chat_history']

        history = self.db['history']
        history.create_index('SessionId')
        self.collection_dict['history'] = history

        message_store = self.db['message_store']
        message_store.create_index('SessionId')
        self.collection_dict['message_store'] = message_store

        super().__init__()

    def insert(self, collection_name: str, data: Dict):
        collection = self.collection_dict[collection_name]
        collection.insert_one(data)

    def delete(self, collection_name: str, data: Dict):
        collection = self.collection_dict[collection_name]
        collection.delete_one(data)

    def list(self, collection_name: str, data: Optional[Dict] = None) -> list:
        collection = self.collection_dict[collection_name]
        result = []
        if data:
            cursor = collection.find(data)
        else:
            cursor = collection.find({})
        for document in cursor:
            document['_id'] = str(document['_id'])
            result.append(document)
        return result


connection_string = 'mongodb://127.0.0.1:27017'
scalar_store: Store = Store(connection_string)
