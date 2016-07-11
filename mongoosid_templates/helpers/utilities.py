"""mongo utilities.py"""
import time
import datetime
from threading import Thread
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import OperationFailure as PyMongoOperationFailed
from bson import ObjectId
from bson.timestamp import Timestamp

from .osid.osid_errors import NullArgument, NotFound,\
    OperationFailed, Unimplemented, IllegalState, InvalidArgument
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

def remove_null_proxy_kwarg(func):
    """decorator, to remove a 'proxy' keyword argument. For wrapping certain Manager methods"""
    def wrapper(*args, **kwargs):
        if 'proxy' in kwargs:
            if kwargs['proxy'] is None:
                del kwargs['proxy']
            else:
                raise InvalidArgument('Manager sessions cannot be called with Proxies. Use ProxyManager instead')
        return func(*args, **kwargs)
    return wrapper

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

def handle_simple_sequencing(func):
    """decorator, deal with simple sequencing cases"""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if 'create_assessment_part' in func.__name__:
            update_parent_sequence_map(result)
        elif func.__name__ == 'delete_assessment_part':
            remove_from_parent_sequence_map(*args, **kwargs)
        return result
    return wrapper

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
            if proxy is None:
                return runtime.get_manager(osid, impl_name)
            else:
                return runtime.get_proxy_manager(osid, impl_name)
        except (AttributeError, KeyError, NotFound):
            pass
    # Try to return a Manager from this implementation, or raise OperationFailed:
    try:
        if proxy is None:
            mgr_str = 'Manager'
        else:
            mgr_str = 'ProxyManager'
        module = import_module('dlkit.mongo.' + osid.lower() + '.managers')
        manager_name = ''.join((osid.title()).split('_')) + mgr_str
        manager = getattr(module, manager_name)()
    except (ImportError, AttributeError):
        raise OperationFailed()
    if runtime is not None:
        manager.initialize(runtime)
    return manager

def get_provider_session(provider_manager, session_method, proxy=None, *args, **kwargs):
    if proxy is None:
        return getattr(provider_manager, session_method)(*args, **kwargs)
    else:
        return getattr(provider_manager, session_method)(proxy, *args, **kwargs)

def format_catalog(catalog_name):
    return catalog_name.replace('_', '').title()

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

def overlap(start1, end1, start2, end2):
    """
    Does the range (start1, end1) overlap with (start2, end2)?

    From Ned Batchelder
    http://nedbatchelder.com/blog/201310/range_overlap_in_two_compares.html

    """
    return not (end1 < start2 or end2 < start1)


class OsidListList(list):
    """
    A morker class for initializing OsidLists with a list of other OsidLists
    
    To use, load up this list with OsidLists of the same object type, and pass
    it as the argument to an OsidList of that same object type. The OsidList
    should exhaust all the contained OsidLists in order on iteration to return
    all the underlying objects as if they are part of one list.
    
    """
    pass


def get_registry(entry, runtime):
    """Returns a record registry given an entry and runtime"""
    try:
        records_location_param_id = Id('parameter:recordsRegistry@mongo')
        registry = runtime.get_configuration().get_value_by_parameter(
            records_location_param_id).get_string_value()
        return import_module(registry).__dict__.get(entry, {})
    except (ImportError, AttributeError, KeyError, NotFound):
        return {}

def is_authenticated_with_proxy(proxy):
    """Given a Proxy, checks whether a user is authenticated"""
    if proxy is None:
        return False
    elif proxy.has_authentication():
        return proxy.get_authentication().is_valid()
    else:
        return False

def get_authenticated_agent_id_with_proxy(proxy):
    """Given a Proxy, returns the Id of the authenticated Agent"""
    if is_authenticated_with_proxy(proxy):
        return proxy.get_authentication().get_agent_id()
    else:
        raise IllegalState()

def get_authenticated_agent_with_proxy(proxy):
    """Given a Proxy, returns the authenticated Agent"""
    if is_authenticated_with_proxy(proxy):
        return proxy.get_authentication().get_agent()
    else:
        raise IllegalState()

def get_effective_agent_id_with_proxy(proxy):
    """Given a Proxy, returns the Id of the effective Agent"""
    if is_authenticated_with_proxy(proxy):
        if proxy.has_effective_agent():
            return proxy.get_effective_agent_id()
        else:
            return proxy.get_authentication().get_agent_id()
    else:
        return Id(
            identifier='MC3GUE$T@MIT.EDU',
            namespace='authentication.Agent',
            authority='MIT-ODL')

def get_effective_agent_with_proxy(proxy):
    """Given a Proxy, returns the effective Agent"""
    #effective_agent_id = self.get_effective_agent_id()
    # This may want to be extended to get the Agent directly from the Authentication
    # if available and if not effective agent is available in the proxy
    #return Agent(
    #    identifier=effective_agent_id.get_identifier(),
    #    namespace=effective_agent_id.get_namespace(),
    #    authority=effective_agent_id.get_authority())
    raise Unimplemented()

def get_locale_with_proxy(proxy):
    """Given a Proxy, returns the Locale

    This assumes that instantiating a dlkit.mongo.locale.objects.Locale
    without constructor arguments wlll return the default Locale.
    
    """
    from .locale.objects import Locale
    if proxy is not None:
            locale = proxy.get_locale()
            if locale is not None:
                return locale
    return Locale()

def update_display_text_defaults(mdata, locale_map):
    for default_display_text in mdata['default_string_values']:
        default_display_text.update(locale_map)

def update_parent_sequence_map(self, child_part, delete=False):
    """Updates the child map of a simple sequence assessment assessment part"""
    if child_part.has_assessment_part():
        object_map = child_part.get_assessment_part()._my_map
        database = 'assessment_authoring'
        collection_type = 'AssessmentPart'
    else:
        object_map = child_part.get_assessment_part()._my_map
        database = 'assessment'
        collection_type = 'Assessment'
    collection = MongoClientValidated(database,
                                      collection=collection_type,
                                      runtime=self._runtime)
    if delete:
        object_map['childIds'].remove(str(child_part.get_id()))
    else:
        object_map['childIds'].append(str(child_part.get_id()))
    collection.save(object_map)

def remove_from_parent_sequence_map(assessment_part_id):
    """Updates the child map of a simple sequence assessment assessment part to remove child part"""
    mgr = get_provider_manager('ASSESSMENT_AUTHORING', runtime=None, proxy=None, local=True)
    child_part = mgr.get_assessment_part_lookup_session().get_assessment_part(assessment_part_id)
    update_parent_sequence_map(child_part, delete=True)

# This may not be needed anymore, Time will tell
def simple_sequencing_error_check(assessment_part_id, next_assessment_part_id, *args, **kwargs):
    """This may not be needed anymore. Time will tell"""
    mgr = get_provider_manager('ASSESSMENT_AUTHORING', runtime=None, proxy=None, local=True)
    for child_part_id in [assessment_part_id, next_assessment_part_id]:
        child_part = mgr.get_assessment_part_lookup_session().get_assessment_part(child_part_id)
        if child_part.has_assessment_part() and child_part.get_assessment_part().supports_simple_child_sequencing():
            raise IllegalState('AssessmentPart only supports simple sequencing')
        elif child_part.get_assessment().supports_simple_child_sequencing():
            raise IllegalState('Assessment only supports simple sequencing')