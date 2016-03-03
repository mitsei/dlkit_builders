class LoggingSession:
    get_log_id = """
        return self._get_provider_session('logging_session').get_log_id()"""