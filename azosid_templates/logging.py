class LoggingProfile:
    get_priority_types = """
        # Implemented from azosid template for -
        # osid.logging.LoggingProfile.get_priority_types
        return self._provider_manager.get_priority_types()"""

    get_content_types = """
        # Implemented from azosid template for -
        # osid.logging.LoggingProfile.get_content_types
        return self._provider_manager.get_content_types()"""


class LoggingSession:
    can_log = """
        return self._provider_session.can_log()"""
