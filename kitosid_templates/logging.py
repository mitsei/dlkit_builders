class LoggingSession:
    get_log_id = """
        return self._get_provider_session('logging_session').get_log_id()"""

    can_log = """
        return self._get_provider_session('logging_session').can_log()"""


class LogEntryLookupSession:

    can_read_log = """
        return self.can_lookup_log_entries()

    def can_lookup_log_entries(self):
        \"\"\"Pass through to provider LogEntryLookupSession.can_lookup_log_entries\"\"\"
        return self._get_provider_session('log_entry_lookup_session').can_lookup_log_entries()"""
