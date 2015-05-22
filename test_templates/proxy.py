
class ProxyManager:

    init = """
"""

class ProxyProxyManager:

    init = """
"""

class ProxySession:

    import_statements = [
    ]

    init = """
"""

    get_proxy_condition = """
        pass"""

    get_proxy = """
        pass"""

class Proxy:

    import_statements = [
    ]

    init = """
"""

    has_authentication = """
        pass"""

    get_authentication = """
        pass"""

    has_effective_agent = """
        pass"""

    get_effective_agent_id = """
        pass"""

    get_effective_agent = """
        pass"""

    has_effective_date = """
        pass"""

    get_effective_date = """
        pass"""

    get_effective_clock_rate = """
        pass"""

    get_locale = """
        pass"""

    has_format_type = """
        pass"""

    get_format_type = """
        pass"""

class ProxyCondition:

    init = """
"""

    set_effective_agent_id = """
        pass"""

    set_effective_date = """
        pass"""

    set_language_type = """
        pass"""

    set_script_type = """
        pass"""

    set_calendar_type = """
        pass"""

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