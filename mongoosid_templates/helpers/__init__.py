"""Supporting objects to be instantiated at runtime"""

from dlkit.abstract_osid.osid.errors import OperationFailed
#from bson import ObjectId
#from bson.timestamp import Timestamp
#import datetime


class MongoClientContainer:

    def __init__(self):
        self._mongo_client = None

    def is_mongo_client_set(self):
        """Check to see if the mongo client has been set."""
        return bool(self._mongo_client)

    def set_mongo_client(self, mongo_client):
        """Set the mongo client. Raises error if already set."""
        if self.is_mongo_client_set():
            raise OperationFailed('MongoClient already set')
        self._mongo_client = mongo_client

    def get_mongo_client(self):
        """Gets the mongo client. Raises error if no mongo client set."""
        if not self.is_mongo_client_set():
            raise OperationFailed('MongoClient not set')
        return self._mongo_client

    mongo_client = property(fget=get_mongo_client, fset=set_mongo_client)


MONGO_CLIENT = MongoClientContainer()


from .utilities import MongoListener
MONGO_LISTENER = MongoListener()