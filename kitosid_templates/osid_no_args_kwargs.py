# osid templates for kit_osid


class OsidProfile:

    get_id = """
        pass"""

    get_display_name = """
        pass"""

    get_description = """
        pass"""

    get_version = """
        pass"""

    get_release_date = """
        pass"""

    supports_osid_version = """
        pass"""

    get_locales = """
        pass"""

    supports_journal_rollback = """
        pass"""

    supports_journal_branching = """
        pass"""

    get_branch_id = """
        pass"""

    get_branch = """
        pass"""

    get_proxy_record_types = """
        pass"""

    supports_proxy_record_type = """
        pass"""


class Identifiable:

    init = """
    def __init__(self, osid_object): # I will never be called :(
        self._osid_object = osid_object
"""

    get_id = """
        return self._osid_object.get_id()

    id_ = property(get_id) """

    is_current = """
        return self._osid_object.is_current()

    current = property(is_current)"""


class Extensible:

    init = """
    def __init__(self, osid_object): # I will never be called :(
        self._osid_object = osid_object
"""

    get_record_types = """
        return self._osid_object.get_record_types()"""

    has_record_type = """
        return self._osid_object.has_record_type(*args, **kwargs)"""


class Browsable:

    init = """
    def __init__(self, osid_object): # I will never be called :(
        self._osid_object = osid_object
"""

    get_properties = """
        return self._osid_object.get_properties()"""

    get_properties_by_record_yype = """
        return self._osid_object.get_properties_by_record_yype(*args, **kwargs)"""


class Sourceable:

    init = """
    def __init__(self, osid_object): # I will never be called :(
        self._osid_object = osid_object
"""

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

    def __init__(self, provider_session):
        self._provider_session = provider_session
"""

    get_locale = """
        pass"""

    is_authenticated = """
        pass"""

    get_authenticated_agent_id = """
        pass"""

    get_authenticated_agent = """
        pass"""

    get_effective_agent_id = """
        pass"""

    get_effective_agent = """
        pass"""

    supports_transactions = """
        pass"""

    startTransaction = """
        pass"""


class OsidObject:

    init = """
    def __init__(self, osid_object): # I will never be called :(
        self._osid_object = osid_object
"""

    get_display_name = """
        return self._osid_object.get_display_name()

    display_name = property(get_display_name)"""

    get_description = """
        return self._osid_object.get_description()

    description = property(get_description)"""

    get_genus_type = """
        return self._osid_object.get_genus_type()

    genus_type = property(get_genus_type)"""

    is_of_genus_type = """
        return self._osid_object.is_of_genus_type(*args, **kwargs)"""


class OsidList:

    init = """
    def __init__(self, iter_object = [], count = None):
        if count != None:
            self._count = count
        elif isinstance(iter_object, dict) or isinstance(iter_object, list):
            self._count = len(iter_object)
        self._iter_object = iter(iter_object)

    def __iter__(self):
        return self

    def next(self):
        next_object = self._iter_object.next()
        if self._count != None:
            self._count -= 1
        return next_object

    def len(self):
        return self.available()
"""

    has_next = """
        if self._count != None:
            # If count is available, use it
            return bool(self._count)
        else:
            # otherwise we have no idea
            return true"""

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

    get_element_id_template = """
        pass"""

    get_minimum_cardinal_template = """
        pass"""

    supports_coordinate_type_template = """
        pass"""
