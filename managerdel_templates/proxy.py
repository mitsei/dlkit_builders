
class ProxySession:

    # import_statements = [
    # ]

    init = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_id() # This will fail!
        self._id_namespace = 'type.Type'
"""

    get_proxy_condition = """
        return self._provider_session.get_proxy_condition()"""

    get_proxy = """
        return self._provider_session.get_proxy()"""
