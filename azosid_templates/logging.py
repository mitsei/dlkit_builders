class LoggingProfile:

    get_priority_types = """
        # Implemented from azosid template for -
        # osid.logging.LoggingProfile.get_priority_types
        return self._provider_manager.get_priority_types()"""

    get_content_types = """
        # Implemented from azosid template for -
        # osid.logging.LoggingProfile.get_content_types
        return self._provider_manager.get_content_types()"""


class LogEntryLookupSession:

    can_read_log = """
        return self.can_lookup_log_entries()

    def can_lookup_log_entries(self):
        \"\"\"Tests if the user can lookup log entries\"\"\"
        return (self._can('lookup') or
                bool(self._get_overriding_catalog_ids('lookup')))"""


class LoggingSession:
    init = """
    def __init__(self, provider_manager, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        self._qualifier_id = self._provider_session.get_log_id()
        self._id_namespace = 'logging.LogEntry'
        self._overriding_log_ids = None
        if self._proxy is not None:
            try:
                self._object_catalog_session = provider_manager.get_log_entry_log_session(self._proxy)
            except (Unimplemented, AttributeError):
                pass
        else:
            try:
                self._object_catalog_session = provider_manager.get_log_entry_log_session()
                self.get_log_ids_by_log_entry = self._object_catalog_session.get_log_ids_by_log_entry
            except (Unimplemented, AttributeError):
                pass

    def _get_overriding_log_ids(self):
        if self._overriding_log_ids is None:
            self._overriding_log_ids = self._get_overriding_catalog_ids('lookup')
        return self._overriding_log_ids"""

    can_log = """
        return self._can('create')"""
