class LoggingSession:
    get_log_id = """
        return self._get_provider_session('logging_session').get_log_id()"""

    can_log = """
        return self._get_provider_session('logging_session').can_log()"""
