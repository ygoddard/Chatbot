from typing import Dict

class DatabaseProvider(object):
    def insert(self, doc: Dict[str, object]):
        raise NotImplementedError

    def find_many(self, query: Dict[str, object]):
        raise NotImplementedError

    def find_one(self, query: Dict[str, object]):
        raise NotImplementedError

    def delete_one(self, query: Dict[str, object]):
        raise NotImplementedError

    def update_one(self, query: Dict[str, object], doc: Dict[str, object]):
        raise NotImplementedError

    def get_object_id(self, id: object):
        raise NotImplementedError

    def attach_doc_id(self, _id: object, doc: Dict[str, object]):
        raise NotImplementedError