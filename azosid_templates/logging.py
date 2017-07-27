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
