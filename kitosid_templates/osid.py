# osid templates for kit_osid

class OsidProfile:

    init = """
    def __init__(self):
        self._provider_manager = None"""

    get_id = """
        pass"""

    get_display_name = """
        return self._provider_manager.get_display_name()"""

    get_description = """
        return self._provider_manager.get_description()"""

    get_version = """
        return self._provider_manager.get_version()"""

    get_release_date = """
        return self._provider_manager.get_release_date()"""

    supports_osid_version = """
        return self._provider_manager.supports_osid_version(*args, **kwargs)"""

    get_locales = """
        return self._provider_manager.get_locales()"""

    supports_journal_rollback = """
        return self._provider_manager.supports_journal_rollback()"""

    supports_journal_branching = """
        return self._provider_manager.supports_journal_branching()"""

    get_branch_id = """
        return self._provider_manager.get_branch_id()"""

    get_branch = """
        return self._provider_manager.get_branch()"""

    get_proxy_record_types = """
        return self._provider_manager.get_proxy_record_types()"""

    supports_proxy_record_type = """
        return self._provider_manager.supports_proxy_record_type(*args, **kwargs)"""

class OsidManager:
    pass

class Identifiable:

    init = """
    def __init__(self, osid_object): # I will never be called :(
        self._osid_object = osid_object"""

    get_id = """
        return self._osid_object.get_id()

    id_ = property(get_id) """

    is_current = """
        return self._osid_object.is_current()

    current = property(is_current)"""


class Extensible:

    init = """
    def __init__(self, osid_object): # I will never be called :(
        self._osid_object = osid_object"""

    get_record_types = """
        return self._osid_object.get_record_types()"""

    has_record_type = """
        return self._osid_object.has_record_type(*args, **kwargs)"""


class Browsable:

    init = """
    def __init__(self, osid_object): # I will never be called :(
        self._osid_object = osid_object"""

    get_properties = """
        return self._osid_object.get_properties()"""

    get_properties_by_record_yype = """
        return self._osid_object.get_properties_by_record_yype(record_type)"""


class Sourceable:

    init = """
    def __init__(self, osid_object): # I will never be called :(
        self._osid_object = osid_object"""

    get_provider_id = """
        return self._osid_object.get_provider_id()"""

    get_provider = """
        return self._osid_object.get_provider()"""

    get_branding_ids = """
        return self._osid_object.get_branding_ids()"""

    get_branding = """
        return self._osid_object.get_branding()"""

    get_license = """
        return self._osid_object.get_license()"""


class Federateable:
    pass


class OsidSession:

    init = """

    COMPARATIVE = 0
    PLENARY = 1
    FEDERATED = 0
    ISOLATED = 1

    def __init__(self, proxy):
        self._proxy = proxy

    def _get_agent_key(self, proxy=None):
        \"\"\"Gets an agent key for session management.

        Side effect of setting a new proxy if one is sent along,
        and initializing the provider session map if agent key has
        not been seen before

        \"\"\"
        if self._proxy is None:
            self._proxy = proxy
        if self._proxy is not None and self._proxy.has_effective_agent():
            agent_key = self._proxy.get_effective_agent_id()
        else:
            agent_key = None
        if agent_key not in self._provider_sessions:
            self._provider_sessions[agent_key] = dict()
        return agent_key

    def set_proxy(self, proxy):
        \"\"\"Sets a new Proxy.\"\"\"
        self._proxy = proxy

    def clear_proxy(self):
        \"\"\"Sets proxy to None.\"\"\"
        self._proxy = None"""

    get_locale = """
        pass"""

    is_authenticated = """
        if self._proxy is None:
            return False
        elif self._proxy.has_authentication():
            return self._proxy.get_authentication().is_valid()
        else:
            return False"""

    get_authenticated_agent_id = """
        if self.is_authenticated():
            return self._proxy.get_authentication().get_agent_id()
        else:
            raise IllegalState()"""  

    get_authenticated_agent = """
        if self.is_authenticated():
            return self._proxy.get_authentication().get_agent()
        else:
            raise IllegalState()"""

    get_effective_agent_id = """
        from .primitives import Id
        if self.is_authenticated():
            if self._proxy.has_effective_agent():
                return self._proxy.get_effective_agent_id()
            else:
                return self._proxy.get_authentication().get_agent_id()
        else:
            return Id(identifier='MC3GUE$T@MIT.EDU',
                      namespace='agent.Agent',
                      authority='MIT-OEIT')"""

    get_effective_agent = """
        #from dlkit.services_impls.authentication.objects import Agent # This may want to be in Primordium?
        #effective_agent_id = self.get_effective_agent_id()
        # This may want to be extended to get the Agent directly from the Authentication
        # if available and if not effective agent is available in the proxy
        #return Agent(identifier=effective_agent_id.get_identifier(),
        #             namespace=effective_agent_id.get_identifier_namespace(),
        #             authority=effective_agent_id.get_authority())
        raise Unimplemented()"""

    supports_transactions = """
        raise Unimplemented()"""

    startTransaction = """
        raise Unimplemented()"""


class OsidObject:

    init = """
    def __init__(self, osid_object):
        self._osid_object = osid_object"""

    get_display_name = """
        return self._osid_object.get_display_name()"""

    get_description = """
        return self._osid_object.get_description()"""

    get_genus_type = """
        return self._osid_object.get_genus_type()"""

    is_of_genus_type = """
        return self._osid_object.is_of_genus_type(*args, **kwargs)"""


class OsidList:

    init = """
    def __init__(self, iter_object=None, count=None):
        if iter_object is None:
            iter_object = []
        if count != None:
            self._count = count
        elif isinstance(iter_object, dict) or isinstance(iter_object, list):
            self._count = len(iter_object)
        self._iter_object = iter(iter_object)

    def __iter__(self):
        return self

    def next(self):
        try:
            next_object = self._iter_object.next()
        except: 
            raise
        if self._count != None:
            self._count -= 1
        return next_object

    def len(self):
        return self.available()"""

    has_next = """
        if self._count != None:
            # If count is available, use it
            return bool(self._count)
        else:
            # otherwise we have no idea
            return True"""

    available = """
        if self._count != None:
            # If count is available, use it
            return self._count
        else:
            # We have no idea.
            return 0  # Don't know what to do here"""

    skip = """
        ### STILL NEED TO IMPLEMENT THIS ###
        pass"""


class Metadata:

#    init = """ """

    get_element_id_template = """
        pass"""

    get_minimum_cardinal_template = """
        pass"""

    supports_coordinate_type_template = """
        pass"""
