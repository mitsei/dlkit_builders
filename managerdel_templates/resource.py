"""resource templates for manager utils"""

class ResourceProfile:

    init_template = """
    def __init__(self):
        self._provider_manager = None

    def _initialize_provider(self, manager):
        self._provider_manager = manager
"""

    import_statements_pattern = [
    ]

    supports_visible_federation_template = """
        return self._provider_manager.${method_name}()"""

    supports_resource_lookup_template = """
        return self._provider_manager.${method_name}()"""

    get_resource_record_types_template = """
        return self._provider_manager.${method_name}()"""

    supports_resource_record_type_template = """
        return self._provider_manager.${method_name}(${arg0_name})"""

class ResourceManager:

    import_statements_pattern = [
    ]

    init_template = """
    def __init__(self):
        ${pkg_name_caps}Profile.__init__(self)

    def _initialize_provider(self, manager):
        ${pkg_name_caps}Profile._initialize_provider(self, manager)
"""

    get_resource_lookup_session_template = """
        return self._provider_manager.${method_name}()"""

    get_resource_lookup_session_for_bin_template = """
        return self._provider_manager.${method_name}(${arg0_name})"""


class ResourceProxyManager:

    import_statements_pattern = [
    ]

    init_template = """
    def __init__(self):
        ${pkg_name_caps}Profile.__init__(self)

    def _initialize_provider(self, manager):
        ${pkg_name_caps}Profile._initialize_provider(self, manager)
"""

    get_resource_lookup_session_template = """
        return self._provider_manager.${method_name}(${arg0_name})"""

    get_resource_lookup_session_for_bin_template = """
        return self._provider_manager.${method_name}(${arg0_name}, ${arg1_name})"""
