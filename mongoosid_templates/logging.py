
from .error_lists import session_errors

class LoggingSession:

    import_statements = [
        'from ..primitives import *',
        'from dlkit.abstract_osid.osid import errors',
        'from . import objects',
        'from ..osid.sessions import OsidSession'
        ]

    init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None):
        OsidSession.__init__(self)
        self._catalog_class = objects.Log
        self._session_name = 'LoggingSession'
        self._catalog_name = 'Log'
        OsidSession._init_object(self, catalog_id, proxy, runtime, db_name='logging', cat_name='Log', cat_class=objects.Log)
        self._forms = dict()
        lm = self._get_provider_manager('LOGGING')
        self._leas = lm.get_log_entry_admin_session_for_log(self._catalog_id)
        self._lels = lm.get_log_entry_lookup_session_for_log(self._catalog_id)
        self._content_types = lm.get_content_types()"""

    can_log = """
        # NOTE: It is expected that real authentication hints will be 
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    log = """
        if not content_type in self._content_types:
            raise errors.Unsupported()
        lefc = self._leas.get_content_form_for_create([])
        lefc.set_timestamp(DateTime.now())"""

class LogEntryAdminSession:
    import_statements_pattern = [
        'from ..primitives import DateTime'
    ]

    create_log_entry = """
        collection = MongoClientValidated('logging',
                                          collection='LogEntry',
                                          runtime=self._runtime)
        if not isinstance(log_entry_form, ABCLogEntryForm):
            raise errors.InvalidArgument('argument type is not an LogEntryForm')
        if log_entry_form.is_for_update():
            raise errors.InvalidArgument('the LogEntryForm is for update only, not create')
        try:
            if self._forms[log_entry_form.get_id().get_identifier()] == CREATED:
                raise errors.IllegalState('log_entry_form already used in a create transaction')
        except KeyError:
            raise errors.Unsupported('log_entry_form did not originate from this session')
        if not log_entry_form.is_valid():
            raise errors.InvalidArgument('one or more of the form elements is invalid')

        if 'timestamp' not in log_entry_form._my_map or log_entry_form._my_map['timestamp'] is None:
            log_entry_form._my_map['timestamp'] = DateTime.now()
        log_entry_form._my_map['agentId'] = str(self.get_effective_agent_id())

        insert_result = collection.insert_one(log_entry_form._my_map)

        self._forms[log_entry_form.get_id().get_identifier()] = CREATED
        result = objects.LogEntry(
            collection.find_one({'_id': insert_result.inserted_id}),
            runtime=self._runtime)

        return result"""

class LogEntry:

    import_statements_pattern = [
        'from ..primitives import *',
        'from ..osid.osid_errors import *',
    ]
    
    get_priority_template = """
        # Implemented from template for osid.logging.LogEntry.get_priority
        if not self._my_map['${var_name_mixed}']:
            raise errors.IllegalState('this ${object_name} has no ${var_name}')
        else:
            return Id(self._my_map['${var_name_mixed}'])"""

    additional_methods = """
    def get_object_map(self):
        obj_map = dict(self._my_map)
        if obj_map['timestamp'] is not None:
            timestamp = obj_map['timestamp']
            obj_map['timestamp'] = dict()
            obj_map['timestamp']['year'] = timestamp.year
            obj_map['timestamp']['month'] = timestamp.month
            obj_map['timestamp']['day'] = timestamp.day
            obj_map['timestamp']['hour'] = timestamp.hour
            obj_map['timestamp']['minute'] = timestamp.minute
            obj_map['timestamp']['second'] = timestamp.second
            obj_map['timestamp']['microsecond'] = timestamp.microsecond

        obj_map = osid_objects.OsidObject.get_object_map(self, obj_map)

        return obj_map

    object_map = property(fget=get_object_map)"""

class LogEntryForm:

    import_statements_pattern = [
        'from ..primitives import *',
        'from ..osid.osid_errors import *',
        'import datetime'
    ]

    init = """
    def __init__(self, osid_object_map=None, record_types=None, runtime=None, **kwargs):
        self._record_type_data_sets = get_registry('LOG_ENTRY_RECORD_TYPES', runtime)
        osid_objects.OsidObjectForm.__init__(
            self, osid_object_map=osid_object_map, record_types=record_types, runtime=runtime, **kwargs)
        self._mdata = dict(default_mdata.LOG_ENTRY)
        self._init_metadata(**kwargs)

        if not self.is_for_update():
            self._init_map(record_types, **kwargs)

    def _init_metadata(self, **kwargs):
        osid_objects.OsidObjectForm._init_metadata(self, **kwargs)
        self._priority_default = self._mdata['priority']['default_type_values'][0]
        self._timestamp_default = datetime.datetime.now()
        self._agent_default = self._mdata['agent']['default_id_values'][0]

    def _init_map(self, record_types=None, **kwargs):
        osid_objects.OsidObjectForm._init_map(self, record_types=record_types)
        self._my_map['priorityId'] = self._priority_default
        self._my_map['timestamp'] = self._timestamp_default
        self._my_map['assignedLogIds'] = [str(kwargs['log_id'])]
        self._my_map['agentId'] = self._agent_default
"""
    
    set_priority_template = """
        # Implemented from template for osid.logging.LogEntryForm.set_priority
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_type(${arg0_name}, 
                                self.get_${var_name}_metadata()):
            raise errors.InvalidArgument()
        self._my_map['${var_name_mixed}'] = str(${arg0_name})"""

class LogEntryQuery:
    match_agent_id = """
        self._add_match("agentId", str(agent_id), match)"""

