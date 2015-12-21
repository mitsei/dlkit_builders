
class ProxyManager:

    init = """

    def __init__(self):
        import settings
        import importlib
        provider_module = importlib.import_module(settings.PROXY_PROVIDER_MANAGER_PATH, settings.ANCHOR_PATH)
        provider_manager_class = getattr(provider_module, 'ProxyManager')
        self._provider_manager = provider_manager_class()
        self._provider_sessions = dict()

    def _get_provider_session(self, session):
        if session in self._provider_sessions:
            return self._provider_sessions[session]
        else:
            try:
                get_session = getattr(self._provider_manager, 'get_' + session)
            except:
                raise # Unimplemented???
            else: 
                self._provider_sessions[session] = get_session()
            return self._provider_sessions[session]"""

class ProxySession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session"""

    get_proxy_condition = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from 
        # osid.proxy.ProxySession.get_proxy_condition
        return self._get_provider_session('proxy_session').get_proxy_condition()"""

    get_proxy = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from 
        # osid.proxy.ProxySession.get_proxy
        return self._get_provider_session('proxy_session').get_proxy(*args, **kwargs)"""
