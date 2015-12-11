"""mongo utilities.py"""
import time
import datetime
from threading import Thread
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import OperationFailure as PyMongoOperationFailed
from bson import ObjectId
from bson.timestamp import Timestamp

from .osid.osid_errors import NullArgument, NotFound, OperationFailed
from dlkit.primordium.calendaring.primitives import DateTime
from dlkit.primordium.id.primitives import Id
from importlib import import_module

from . import MONGO_CLIENT

# VMAP = {
#     'i': 'new',
#     'u': 'changed',
#     'd': 'deleted'
# }

class Filler(object):
    pass


def set_mongo_client(runtime):
    try:
        mongo_host_param_id = Id('parameter:mongoHostURI@mongo')
        mongo_host = runtime.get_configuration().get_value_by_parameter(mongo_host_param_id).get_string_value()
    except (AttributeError, KeyError, NotFound):
        MONGO_CLIENT.set_mongo_client(MongoClient())
    else:
        MONGO_CLIENT.set_mongo_client(MongoClient(mongo_host))

class MongoClientValidated(object):
    """automatically validates the insert_one, find_one, and delete_one methods"""
    def __init__(self, db, collection=None, runtime=None):
        if not MONGO_CLIENT.is_mongo_client_set() and runtime is not None:
            set_mongo_client(runtime)
        db_prefix = ''
        try:
            db_prefix_param_id = Id('parameter:mongoDBNamePrefix@mongo')
            db_prefix = runtime.get_configuration().get_value_by_parameter(db_prefix_param_id).get_string_value()
        except (AttributeError, KeyError, NotFound):
            pass

        if collection is None:
            self._mc = MONGO_CLIENT.mongo_client[db_prefix + db]
        else:
            self._mc = MONGO_CLIENT.mongo_client[db_prefix + db][collection]
            # add the collection index, if available in the configs
            try:
                mongo_indexes_param_id = Id('parameter:indexes@mongo')
                mongo_indexes = runtime.get_configuration().get_value_by_parameter(mongo_indexes_param_id).get_object_value()
                namespace = '{0}.{1}'.format(db, collection)
                if namespace in mongo_indexes:
                    for field in mongo_indexes[namespace]:
                        self._mc.create_index(field)
            except (AttributeError, KeyError, NotFound):
                pass

    def _validate_write(self, result):
        try:
            if not result.acknowledged or result.inserted_id is None:
            # if (('writeErrors' in result and len(result['writeErrors']) > 0) or
            #         ('writeConcernErrors' in result and len(result['writeConcernErrors']) > 0)):
                raise OperationFailed(str(result))
        except AttributeError:
            # account for deprecated save() method
            if result is None:
                raise OperationFailed('Nothing saved to database.')

    def count(self):
        return self._mc.count()

    def delete_one(self, query):
        try:
            result = self._mc.delete_one(query)
        except TypeError:
            result = self._mc.remove(query)
            if result is not None:
                returned_object = result
                result = Filler()
                result.deleted_count = returned_object['n']
        if result is None or result.deleted_count == 0:
            raise NotFound(str(query) + ' returned None.')
        return result

    def find(self, query=None):
        if query is None:
            return self._mc.find()
        else:
            return self._mc.find(query)

    def find_one(self, query):
        result = self._mc.find_one(query)
        if result is None:
            raise NotFound(str(query) + ' returned None.')
        return result

    def insert_one(self, doc):
        try:
            result = self._mc.insert_one(doc)
        except TypeError:
            # pymongo 2.8.1
            result = self._mc.insert(doc)
            if result is not None:
                returned_object_id = result
                result = Filler()
                result.inserted_id = returned_object_id
        self._validate_write(result)
        return result

    def raw(self):
        """ return the raw mongo client object...used for GridFS
        """
        return self._mc

    def save(self, doc):
        result = self._mc.save(doc)
        self._validate_write(result)
        return result

def arguments_not_none(func):
    """decorator, to check if any arguments are None; raise exception if so"""
    def wrapper(*args, **kwargs):
        for arg in args:
            if arg is None:
                raise NullArgument()
        for arg, val in kwargs.iteritems():
            if val is None:
                raise NullArgument()
        try:
            return func(*args, **kwargs)
        except TypeError as ex:
            if 'takes exactly' in ex.args[0]:
                raise NullArgument('Wrong number of arguments provided: ' + str(ex.args[0]))
            else:
                raise

    return wrapper

def overlap(start1, end1, start2, end2):
    """
    Does the range (start1, end1) overlap with (start2, end2)?
    
    From Ned Batchelder
    http://nedbatchelder.com/blog/201310/range_overlap_in_two_compares.html
    
    """
    return not (end1 < start2 or end2 < start1)

def now_map():
    now = DateTime.utcnow()
    return {
        'year': now.year,
        'month': now.month,
        'day': now.day,
        'hour': now.hour,
        'minute': now.minute,
        'second': now.second,
        'microsecond': now.microsecond,
    }

def get_provider_manager(osid, runtime=None, proxy=None, local=False):
    """
    Gets the most appropriate provider manager depending on config.
    
    If local is True, then don't bother with the runtime/config and
    try to get the requested service manager directly from the local
    service implementations known to this mongodb implementation.
    
    """
    if runtime is not None and not local:
        try:
            # Try to get the manager from the runtime, if available:
            config = runtime.get_configuration()
            parameter_id = Id('parameter:' + osid.lower() + 'ProviderImpl@mongo')
            impl_name = config.get_value_by_parameter(parameter_id).get_string_value()
            return runtime.get_manager(osid, impl_name) # What about ProxyManagers?
        except (AttributeError, KeyError, NotFound):
            pass
    # Try to return a Manager from this implementation, or raise OperationFailed:
    try:
        module = import_module('dlkit.mongo.' + osid.lower() + '.managers')
        manager = getattr(module, osid.title() + 'Manager')()
    except (ImportError, AttributeError):
        raise OperationFailed()
    if runtime is not None:
        manager.initialize(runtime)
    return manager


# class OLDMongoListener(Thread):
#     """A utility thread that listens for database changes for notification sessions"""
#     def __init__(self, ns, receiver, runtime, authority, obj_name_plural):
#         """Constructor"""
#         Thread.__init__(self)
#         self.setDaemon(True)
#         self.reliable = False
#         self._ns = ns
#         self._obj_name_plural = obj_name_plural
#         self._receiver = receiver
#         self._authority = authority
#         self._registry = {
#             'i': False,
#             'u': False,
#             'd': False
#             }
#         if not MONGO_CLIENT.is_mongo_client_set() and runtime is not None:
#             set_mongo_client(runtime)
#         cursor = MONGO_CLIENT.mongo_client['local']['oplog.rs'].find().sort('ts', DESCENDING).limit(-1)
#         try:
#             self.last_timestamp = cursor.next()['ts']
#         except StopIteration:
#             self.last_timestamp = Timestamp(0, 0)
#         self._notification_list = list()
# 
#     def _callback(self, doc):
#         """process the notification"""
#         if self._registry[doc['op']]:
#             if self._registry[doc['op']] is True or str(doc['o']['_id']) in self._registry[doc['op']]:
#                 verb = VMAP[doc['op']]
#                 object_id = Id(self._ns + ':' + str(doc['o']['_id']) + '@' + self._authority)
#                 notification_id = Id(self._ns + 'Notification:' + str(ObjectId()) + '@' + self._authority)
#                 getattr(self._receiver, '_'.join([verb, self._obj_name_plural]))(notification_id, [object_id])
#                 if self.reliable:
#                     self._notification_list.append(notification_id)
# 
#     def acknowledge_notification(self, notification_id):
#         """receipt of notification has been acknowledged"""
#         if self.reliable:
#             try:
#                 self._notification_list.remove(notification_id)
#             except ValueError:
#                 pass
#             
#     def run(self):
#         """main control loop for thread"""
#         while True:
#             cursor = MONGO_CLIENT.mongo_client['local']['oplog.rs'].find(
#                 {'ts':{'$gt': self.last_timestamp}})
#             # http://stackoverflow.com/questions/30401063/pymongo-tailing-oplog
#             cursor.add_option(2)  # tailable
#             cursor.add_option(8)  # oplog_replay
#             cursor.add_option(32)  # await data
#             for doc in cursor:
#                 self.last_timestamp = doc['ts']
#                 if doc['ns'] == self._ns:
#                     self._callback(doc)
#             time.sleep(1)
