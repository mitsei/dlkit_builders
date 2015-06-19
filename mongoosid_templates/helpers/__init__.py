#from pymongo import MongoClient
#mongo_client = MongoClient()

from dlkit.abstract_osid.osid.errors import OperationFailed

class MongoClientContainer:

    def __init__(self):
        self._mongo_client = None

    def is_mongo_client_set(self):
        return bool(self._mongo_client)

    def set_mongo_client(self, mongo_client):
        if self.is_mongo_client_set():
            raise OperationFailed('MongoClient already set')
        self._mongo_client = mongo_client

    def get_mongo_client(self):
        if not self.is_mongo_client_set():
            raise OperationFailed('MongoClient not set')
        return self._mongo_client

    mongo_client = property(fget=get_mongo_client, fset=set_mongo_client)

MONGO_CLIENT = MongoClientContainer()
