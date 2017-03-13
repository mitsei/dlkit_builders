
from .error_lists import session_errors

class ProxyManager:

    init = """
    def __init__(self):
        osid_managers.OsidManager.__init__(self)"""

class ProxyProxyManager:

    init = """
    def __init__(self):
        osid_managers.OsidProxyManager.__init__(self)"""

class ProxySession:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from . import rules',
        'from ..authentication_process.objects import Authentication'
    ]

    init = """
    def __init__(self, proxy=None, runtime=None):
        self._proxy = proxy
        self._runtime = runtime"""

    get_proxy_condition = """
        return rules.ProxyCondition()"""

    get_proxy = """
        if input_._http_request is not None:
            authentication = Authentication()
            authentication.set_django_user(input_._http_request.user)
        else:
            authentication = None
        effective_agent_id = input_._effective_agent_id
        # Also need to deal with effective dates and Local
        return rules.Proxy(authentication=authentication,
                           effective_agent_id=effective_agent_id)"""

class Proxy:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id'
    ]

    init = """
    def __init__(self,
                 authentication=None,
                 effective_agent_id=None,
                 effective_date=None,
                 effective_clock_rate=None,
                 locale=None,
                 format_type=None):
        self._authentication = authentication
        self._effective_agent_id = effective_agent_id
        self._effective_date = effective_date
        self._effective_clock_rate = effective_clock_rate
        self._locale = locale
        self._format_type = format_type"""

    has_authentication = """
        return bool(self._authentication)"""

    get_authentication = """
        if self.has_authentication():
            return self._authentication
        else:
            raise errors.IllegalState()"""

    has_effective_agent = """
        return bool(self._effective_agent_id)"""

    get_effective_agent_id = """
        if self.has_effective_agent():
            return self._effective_agent_id
        else:
            raise errors.IllegalState()"""

    get_effective_agent = """
        raise errors.Unimplemented"""

    has_effective_date = """
        return bool(self._authentication)"""

    get_effective_date = """
        if self.has_effective_date():
            return self._effective_date
        else:
            raise errors.IllegalState()"""

    get_effective_clock_rate = """
        if self.has_effective_date():
            return self._effective_clock_rate
        else:
            raise errors.IllegalState()"""

    get_locale = """
        return self._locale"""

    has_format_type = """
        return bool(self._format_type)"""

    get_format_type = """
        if self.has_format_type():
            return self._format_type
        else:
            raise errors.IllegalState()"""

class ProxyCondition:

    init = """
    def __init__(self):
        self._effective_agent_id = None
        self._language_type = None
        self._script_type = None
        self._calendar_type = None
        self._time_type = None
        self._currency_type = None
        self._unit_system_type = None
        self._format_type = None
        self._http_request = None"""

    set_effective_agent_id = """
        self._effective_agent_id = agent_id"""

    set_effective_date = """
        raise errors.Unimplemented()"""

    set_language_type = """
        self._language_type = language_type"""

    set_script_type = """
        self._script_type = script_type"""

    set_calendar_type = """
        self._calendar_type = calendar_type"""

    set_time_type = """
        self._time_type = time_type"""

    set_currency_type = """
        self._currency_type = currency_type"""

    set_unit_system_type = """
        self._unit_system_type = unit_system_type"""

    set_format_type = """
        self._format_type = format_type"""

    get_proxy_condition_record = """
        if self.has_record_type(proxy_condition_type):
            return self
        else:
            raise errors.Unsupported()

    def set_http_request(self, http_request):
        \"\"\"Support the HTTPRequest ProxyConditionRecordType and checks for special effective agent ids\"\"\"
        self._http_request = http_request
        if 'HTTP_LTI_USER_ID' in http_request.META:
            try:
                authority = http_request.META['HTTP_LTI_TOOL_CONSUMER_INSTANCE_GUID']
            except (AttributeError, KeyError):
                authority = 'unknown_lti_consumer_instance'
            self.set_effective_agent_id(Id(
                authority=authority,
                namespace='agent.Agent',
                identifier=http_request.META['HTTP_LTI_USER_ID']))

    http_request = property(fset=set_http_request)"""