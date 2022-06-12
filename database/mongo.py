from typing import Dict
from flask_pymongo import PyMongo, ObjectId

from .provider import DatabaseProvider


class MongoDbProvider(DatabaseProvider):
    def __init__(self, app, config):
        app.config["MONGO_URI"] = config.database_uri

        app.config["MONGO_AUTH_SOURCE"] = "admin"

        self.mongo = PyMongo(app)
        self.db = self.mongo.db[config.contacts_database_name]

    def get_object_id(self, _id: object):
        return ObjectId(_id)

    def attach_doc_id(self, _id: object, doc: Dict[str, object]):
        doc["_id"] = _id
        return doc

    def insert(self, doc: Dict[str, object]):
        id = self.db.insert_one(doc)
        return id

    def find_many(self, query: Dict[str, object]):
        objects = []
        for doc in self.db.find(query):
            objects.append(doc)
        return objects

    def find_all(self):
        return self.find_many({})

    def find_one(self, query: Dict[str, object]):
        return self.db.find_one(query)

    def delete_one(self, query: Dict[str, object]):
        return self.db.delete_one(query)

    def update_one(self, query: Dict[str, object], doc: Dict[str, object]):
        return self.db.update_one(query, doc)
