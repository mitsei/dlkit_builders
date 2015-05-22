
class OsidProfile:

    import_statements = [
    ]

    init = """
"""
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
       """

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

class OsidManager:

    import_statements = [
    ]  

    init = """
"""
    
    initialize = """
        pass"""

class OsidProxyManager:

    import_statements = [
    ]  

    init = """
"""
    
    initialize = """
        pass"""


class OsidRuntimeManager:

    import_statements = [
    ]  

    init = """
"""


class Identifiable:

    import_statements = [
    ]  

    init = """
"""

    get_id = """
        pass"""

    is_current = """
        pass"""


class Extensible:

    import_statements = [
    ]  

    init = """
"""

    has_record_type = """
        pass"""

    get_record_types = """
        pass"""

class Temporal:

    import_statements = [
    ]

    init = """
"""

    is_effective = """
        pass"""

    get_start_date = """
        pass"""

    get_end_date = """
        pass"""

class Containable:

    init = """
"""

    is_sequestered = """
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

    import_statements = [
    ]

    init = """
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

    import_statements = [
        ]

    init = """
"""

    get_display_name = """
        pass"""

    get_description = """
        pass"""

    get_genus_type = """
        pass"""

    is_of_genus_type = """
        pass"""

class OsidRule:

    has_rule = """
        pass"""

    get_rule_id = """
        pass"""
    
    get_rule= """
        pass"""

class OsidForm:

    import_statements = [
        ]

    init = """
"""

    is_for_update = """
        pass"""

    get_default_locale = """
        pass"""

    get_locales = """
        pass"""

    set_locale = """
        pass"""

    get_journal_comment_metadata = """
        pass"""

    set_journal_comment = """
        pass"""

    is_valid = """
        pass"""

    get_validation_messages = """
        pass"""

    get_invalid_metadata = """
        pass"""

class OsidExtensibleForm:

    init = """
"""

class OsidTemporalForm:

    import_statements = [
        ]

    init = """
"""

    get_start_date_metadata = """
        pass"""

    set_start_date = """
        pass"""

    clear_start_date = """
        pass"""

    get_end_date_metadata = """
        pass"""

    set_end_date = """
        pass"""

    clear_end_date = """
        pass"""


class OsidObjectForm:

    import_statements = [
        ]

    init = """
"""

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

    get_genus_type_metadata = """
        pass"""

    set_genus_type = """
        pass"""

    clear_genus_type = """
        pass"""

class OsidRelationshipForm:

    init = """
"""

class OsidList:

    init = """
"""

    has_next = """
        pass"""

    available = """
        pass"""

    skip = """
        pass"""

class OsidQuery:

    import_statements = [
    ]

    init = """
"""

class OsidIdentifiableQuery:

    import_statements = [
    ]

    match_id = """
        pass"""
    
    clear_id_terms = """
        pass"""

class OsidExtensibleQuery:

    import_statements = [
    ]

    init = """
"""

class OsidObjectQuery:

    import_statements = [
    ]

    match_display_name = """
        pass"""

    match_any_display_name = """
        pass"""

    clear_display_name_terms = """
        pass"""
    
    match_description = """
        pass"""

    match_any_description = """
        pass"""

    clear_description_terms = """
        pass"""

class OsidQueryInspector:

    import_statements = [
    ]

class OsidRecord:


    implements_record_type = """
        pass"""
    

class Metadata:

    import_statements = [
    ]

    init = """
"""

    get_element_id_template = """
        pass"""

    get_minimum_cardinal_template = """
        pass"""

    supports_coordinate_type_template = """
        pass"""

    get_existing_cardinal_values_template = """
        pass"""


class OsidNode:

    init = """
"""

    is_root = """
        pass"""

    has_parents = """
        pass"""

    get_parent_ids = """
        pass"""

    is_leaf = """
        pass"""

    has_children = """
        pass"""

    get_child_ids = """
        pass"""


class Property:

    import_statements = [
    ]


class OsidReceiver:

    import_statements = [
    ]


class OsidSearchOrder:

    import_statements = [
    ]

class OsidSearch:

    import_statements = [
    ]
