
class TypeProfile:

    supports_type_lookup = """
        pass"""

    supports_type_admin = """
        pass"""


class TypeManager:

    import_statements = [
    ]

    get_type_lookup_session = """
        pass"""

    get_type_admin_session = """
        pass"""


class TypeLookupSession:

    import_statements = [
    ]

    init = """
"""

    can_lookup_types = """
        pass"""

    get_type = """
        pass"""

    get_types = """
        pass"""


class TypeAdminSession:

    init = """
    """

    can_create_types = """
        pass"""

    get_type_form_for_create = """
        pass"""

    create_type = """
        pass"""

    can_update_types = """
        pass"""

    can_update_type = """
        pass"""

    get_type_form_for_update = """
        pass"""

    update_type = """
        pass"""

    can_delete_types = """
        pass"""

    can_delete_type = """
        pass"""

    delete_type = """
        pass"""


class TypeForm:

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

    get_display_label_metadata = """
        pass"""

    set_display_label = """
        pass"""

    clear_display_label = """
        pass"""

    get_description_metadata = """
        pass"""

    set_description = """
        pass"""

    clear_description = """
        pass"""

    get_domain_metadata = """
        pass"""

    set_domain = """
        pass"""

    clear_description = """
        pass"""


class TypeList:

    import_statements = [
    ]

    get_next_type = """
        pass"""

    get_next_types = """
        pass"""


class Type:

    init = """
"""

    get_authority = """
        pass"""

    get_identifier_namespace = """
        pass"""

    get_identifier = """
        pass"""

    get_display_name = """
        pass"""

    get_display_label = """
        pass"""

    get_description = """
        pass"""

    get_domain = """
        pass"""


class OldObsoleteTypeCanBeDeleted:

    init = """
"""

    get_authority = """
        pass"""

    get_identifier_namespace = """
        pass"""

    get_identifier = """
        pass"""

    get_display_name = """
        pass"""

    get_display_label = """
        pass"""

    get_description = """
        pass"""

    get_domain = """
        pass"""
