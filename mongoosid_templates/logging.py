
class LoggingSession:

    import_statements = [
        'from ..primitives import *',
        'from ..osid.osid_errors import *',
        'from ..osid.sessions import OsidSession'
        ]

    init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None):
        self._catalog_class = LogBook
        self._session_name = 'LoggingSession'
        self._catalog_name = 'LogBook'
        OsidSession._init_object(self, catalog_id, proxy, runtime, db_name='logging', cat_name='LogBook', cat_class=LogBook)
        self._forms = dict()
        lm = self._get_provider_manager('LOGGING')
        self._leas = lm.get_log_entry_admin_session_for_log_book(self._catalog_id)
        self._lels = lm.get_log_entry_lookup_session_for_log_book(self._catalog_id)
        self._content_types = lm.get_content_types()
"""

    can_log = """
        # NOTE: It is expected that real authentication hints will be 
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    log = """
        if content is None or contentType is None:
            raise NullArgument()
        if not contentType in self._content_types:
            raise Unsupported()
        lefc = self._leas.get_content_form_for_create([])
        lefc.set_timestamp(DateTime.now())"""
    
class LogEntry:

    import_statements_pattern = [
        'from ..primitives import *',
        'from ..osid.osid_errors import *',
    ]
    
    get_priority_template = """
        # Implemented from template for osid.logging.LogEntry.get_priority
        if not self._my_map['${var_name_mixed}']:
            raise IllegalState('this ${object_name} has no ${var_name}')
        else:
            return Id(self._my_map['${var_name_mixed}'])"""


class LogEntryForm:

    import_statements_pattern = [
        'from ..primitives import *',
        'from ..osid.osid_errors import *',
    ]
    
    set_priority_template = """
        # Implemented from template for osid.logging.LogEntryForm.set_priority
        if ${arg0_name} is None:
            raise NullArgument()
        if self.get_${var_name}_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_type(${arg0_name}, 
                                self.get_${var_name}_metadata()):
            raise InvalidArgument()
        self._my_map['${var_name_mixed}'] = str(${arg0_name})"""
