# osid templates for az_osid


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

    get_id = """
        pass"""

    is_current = """
        pass"""


class Extensible:

    has_record_type = """
        pass"""

    get_record_types = """
        pass"""


class Operable:

    is_active = """
        pass"""

    is_enabled = """
        pass"""

    is_disabled = """
        pass"""

    is_operational = """
        pass"""


class OsidSession:

    init = """

    COMPARATIVE = 0
    PLENARY = 1
    ISOLATED = 0
    FEDERATED = 1

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

    get_display_name = """
        pass"""

    get_description = """
        pass"""


class OsidRule:

    has_rule = """
        pass"""

    get_rule_id = """
        pass"""

    get_rule = """
        pass"""


class OsidForm:

    is_for_update = """
        pass"""

    get_default_locale = """
        pass"""

    get_locales = """
        pass"""

    set_locale = """
        pass"""

    get_comment_metadata = """
        pass"""

    set_comment = """
        pass"""

    is_valid = """
        pass"""

    get_validation_messages = """
        pass"""

    get_invalid_metadata = """
        pass"""


class OsidObjectForm:

    get_display_name_metadata = """
        pass"""

    set_display_name = """
        pass"""

    clear_display_name = """
        pass"""

    get_description_metadata = """
        pass"""

    set_description = """
        pass"""

    clear_description = """
        pass"""


class OsidList:

    # Initially we will create a federated OsidList that is initialized with
    # one or more iterators (other object lists).  Eventually we might replace
    # this with an implmentation that deals with threads.

    init = """
    def __init__(self, osid_lists = []):
        # This implementation expects to be called with a list of OsidList
        # objects.
        self._osid_lists = osid_lists  # A list of OsidList objects
        self._index = 0  # The index of the OsidList currently being worked on

    def __iter__(self):
        return self

    def next(self):
        try:
            next_object = self._osid_lists[self._index].next()
        except StopIteration:
            self._index += 1 # Try to switch to the next OsidList
            if self._index < len(self._osid_lists):
                return self.next()
            else:
                raise
        return next_object

    def len(self):
        return self.available()
"""

    has_next = """
        has_next = False
        n = self._index
        while n < len(self._osid_lists):
            has_next = has_next or self._osid_lists[n].has_next()
            n += 1
        return has_next"""

    available = """
        available = 0
        n = self._index
        while n < len(self._osid_lists):
            available = available + self._osid_lists[n].available()
            n += 1
        return available"""


class Metadata:

    get_element_id_template = """
        pass"""

    get_minimum_cardinal_template = """
        pass"""

    supports_coordinate_type_template = """
        pass"""
