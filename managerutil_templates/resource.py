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
    'from ..osid.osid_errors import Unimplemented',
    'from ..osid.osid_errors import NullArgument',
    ]


    get_resource_lookup_session_template = """
        raise Unimplemented()"""

    get_resource_lookup_session_for_bin_template = """
        if ${arg0_name} is None:
            raise NullArgument
        raise Unimplemented()"""

    get_resource_admin_session_template = get_resource_lookup_session_template

    get_resource_admin_session_for_bin_template = get_resource_lookup_session_for_bin_template

    get_resource_notification_session_template = get_resource_lookup_session_template

    get_resource_notification_session_for_bin_template = """
        if ${arg0_name} is None:
            raise NullArgument
        if ${arg1_name} is None:
            raise NullArgument
        raise Unimplemented()"""

    get_bin_lookup_session_template = get_resource_lookup_session_template

    get_resource_smart_bin_session_template = get_resource_lookup_session_for_bin_template

    get_resource_batch_manager_template = get_resource_lookup_session_template


class ResourceProxyManager:

    import_statements_pattern = [
    'from ..osid.osid_errors import Unimplemented',
    'from ..osid.osid_errors import NullArgument',
    ]


    get_resource_lookup_session_template = """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()"""

    get_resource_lookup_session_for_bin_template = """
        if ${arg0_name} is None or proxy is None:
            raise NullArgument
        raise Unimplemented()"""

    get_resource_admin_session_template = get_resource_lookup_session_template

    get_resource_admin_session_for_bin_template = get_resource_lookup_session_for_bin_template

    get_resource_notification_session_template = get_resource_lookup_session_template

    get_resource_notification_session_for_bin_template = get_resource_lookup_session_for_bin_template

    get_resource_batch_proxy_manager_template = get_resource_lookup_session_template
