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
        self._catalog_name = 'Log'
        OsidSession._init_object(self, catalog_id, proxy, runtime, db_name='logging', cat_name='Log', cat_class=objects.Log)
        self._forms = dict()
        lm = self._get_provider_manager('LOGGING')
        self._leas = lm.get_log_entry_admin_session_for_log(self._catalog_id, proxy=self._proxy)
        self._lels = lm.get_log_entry_lookup_session_for_log(self._catalog_id, proxy=self._proxy)
        self._content_types = lm.get_content_types()"""

    can_log = """
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    log = """
        if content_type not in self._content_types:
            raise errors.Unsupported()
        lefc = self._leas.get_content_form_for_create([])
        lefc.set_timestamp(DateTime.utcnow())"""


class LogEntryLookupSession:

    can_read_log = """
        \"\"\"Tests if this user can read the log.

        A return of true does not guarantee successful authorization. A
        return of false indicates that it is known all methods in this
        session will result in a ``PermissionDenied``. This is intended
        as a hint to an application that may opt not to offer reading
        operations.

        return: (boolean) - ``false`` if reading methods are not
                authorized, ``true`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        return self.can_lookup_log_entries()

    def can_lookup_log_entries(self):
        \"\"\"Tests if a user can read logs :)\"\"\"
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""


class LogEntryAdminSession:
    import_statements_pattern = [
        'from ..primitives import DateTime'
    ]

    create_log_entry = """
        collection = JSONClientValidated('logging',
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
            log_entry_form._my_map['timestamp'] = DateTime.utcnow()
        log_entry_form._my_map['agentId'] = str(self.get_effective_agent_id())

        insert_result = collection.insert_one(log_entry_form._my_map)

        self._forms[log_entry_form.get_id().get_identifier()] = CREATED
        result = objects.LogEntry(
            osid_object_map=collection.find_one({'_id': insert_result.inserted_id}),
            runtime=self._runtime,
            proxy=self._proxy)

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

    get_resource_id = """
        raise errors.Unimplemented()"""

    get_resource = """
        raise errors.Unimplemented()"""

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
    _namespace = 'logging.LogEntry'

    def __init__(self, **kwargs):
        osid_objects.OsidObjectForm.__init__(self, **kwargs)
        self._mdata = default_mdata.get_log_entry_mdata()

    def _init_metadata(self, **kwargs):
        osid_objects.OsidObjectForm._init_metadata(self, **kwargs)
        self._priority_default = self._mdata['priority']['default_type_values'][0]
        self._timestamp_default = datetime.datetime.utcnow()
        self._agent_default = self._mdata['agent']['default_id_values'][0]

    def _init_map(self, record_types=None, **kwargs):
        osid_objects.OsidObjectForm._init_map(self, record_types=record_types)
        self._my_map['priorityId'] = self._priority_default
        self._my_map['timestamp'] = self._timestamp_default
        self._my_map['assignedLogIds'] = [str(kwargs['log_id'])]
        self._my_map['agentId'] = self._agent_default"""

    set_priority_template = """
        # Implemented from template for osid.logging.LogEntryForm.set_priority
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_type(${arg0_name}):
            raise errors.InvalidArgument()
        self._my_map['${var_name_mixed}'] = str(${arg0_name})"""

    clear_priority_template = """
        # Implemented from template for osid.logging.LogEntryForm.clear_priority_template
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['${var_name_mixed}'] = self._${var_name}_default"""

    get_priority_metadata_template = """
        # Implemented from template for osid.logging.LogEntryForm.get_priority_metadata
        metadata = dict(self._mdata['${var_name}'])
        metadata.update({'existing_type_values': self._my_map['${var_name_mixed}Id']})
        return Metadata(**metadata)"""


class LogEntryQuery:
    match_agent_id = """
        self._add_match("agentId", str(agent_id), match)"""
