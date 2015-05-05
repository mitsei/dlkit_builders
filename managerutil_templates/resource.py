"""resource templates for manager utils"""

class ResourceProfile:

    import_statements_pattern = [
        'from ..type.objects import TypeList',
        'from ..osid.osid_errors import NullArgument',
    ]

    supports_visible_federation_template = """
        return False"""

    supports_resource_lookup_template = """
        return False"""

    get_resource_record_types_template = """
        return TypeList([])"""

    supports_resource_record_type_template = """
        if ${arg0_name} is None:
            raise NullArgument()
        return False"""

class ResourceManager:

    import_statements_pattern = [
    'from ..osid.osid_errors import Unsupported',
    'from ..osid.osid_errors import Unimplemented',
    'from ..osid.osid_errors import NullArgument',
    ]


    get_resource_lookup_session_template = """
        raise Unsupported()"""

    get_resource_lookup_session_for_bin_template = """
        if ${arg0_name} is None:
            raise NullArgument
        raise Unsupported()"""


class ResourceProxyManager:

    import_statements_pattern = [
    'from ..osid.osid_errors import Unsupported',
    'from ..osid.osid_errors import Unimplemented',
    'from ..osid.osid_errors import NullArgument',
    ]


    get_resource_lookup_session_template = """
        if proxy is None:
            raise NullArgument()
        raise Unsupported()"""

    get_resource_lookup_session_for_bin_template = """
        if ${arg0_name} is None or proxy is None:
            raise NullArgument
        raise Unsupported()"""
