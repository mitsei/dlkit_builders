# resource templates for az_osid

class ResourceProfile:

    supports_visible_federation_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceProfile.supports_visible_federation
        return self._provider_manager.${method_name}()"""

    supports_resource_lookup_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceProfile.supports_resource_lookup
        return self._provider_manager.${method_name}()"""

#    get_resource_record_types = """
        # Implemented from azosid template for -
        # osid.resource.ResourceProfile.get_resource_record_types
#        return self._provider_manager.${method_name}()"""

class ResourceManager:

    init_template = """
    def __init__(self):
        from . import settings
        import importlib
        provider_module = importlib.import_module(settings.PROVIDER_MANAGER_MODULE_PATH, settings.ANCHOR_PATH)
        authz_module = importlib.import_module(settings.AUTHZ_MANAGER_MODULE_PATH, settings.ANCHOR_PATH)
        Provider${interface_name} = getattr(provider_module, '${interface_name}')
        MyAuthorizationManager = getattr(authz_module, 'AuthorizationManager')
        self._provider_manager = Provider${interface_name}()
        self._authz_session = MyAuthorizationManager().get_authorization_session()
"""

    get_resource_lookup_session_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_template
        from ${return_module} import ${return_type}
        return ${return_type}(self._provider_manager.${method_name}(), self._authz_session)"""

    get_resource_lookup_session_for_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_template
        from ${return_module} import ${return_type}
        return ${return_type}(self._provider_manager.${method_name}(${arg0_name}), self._authz_session)"""


class ResourceProxyManager:

    init_template = """
    def __init__(self):
        from . import settings
        import importlib
        provider_module = importlib.import_module(settings.PROVIDER_MANAGER_MODULE_PATH, settings.ANCHOR_PATH)
        authz_module = importlib.import_module(settings.AUTHZ_MANAGER_MODULE_PATH, settings.ANCHOR_PATH)
        Provider${interface_name} = getattr(provider_module, '${interface_name}')
        MyAuthorizationManager = getattr(authz_module, 'AuthorizationManager')
        self._provider_manager = Provider${interface_name}()
        self._authz_session = MyAuthorizationManager().get_authorization_session()
"""

    get_resource_lookup_session_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_template
        from ${return_module} import ${return_type}
        return ${return_type}(self._provider_manager.${method_name}(proxy), self._authz_session, proxy)"""

    get_resource_lookup_session_for_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_template
        from ${return_module} import ${return_type}
        return ${return_type}(self._provider_manager.${method_name}(${arg0_name}, proxy), self._authz_session, proxy)"""


class ResourceLookupSession:

    init_template = """
    def __init__(self, provider_session, authz_session, proxy = None):
        from ..osid import sessions as osid_sessions
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name}.${object_name}'
"""

    get_bin_id_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_bin_id_template
        return self._provider_session.${method_name}()"""

    get_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_bin_template
        return self._provider_session.${method_name}()"""

    can_lookup_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.can_lookup_resources_template
        return self._can('${func_name}')"""

    use_comparative_resource_view_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.use_comparative_resource_view_template
        self._provider_session.${method_name}()"""

    use_plenary_resource_view_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.use_plenary_resource_view_template
        self._provider_session.${method_name}()"""

    use_federated_bin_view_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.use_federated_bin_view_template
        self._provider_session.${method_name}()"""

    use_isolated_bin_view_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.use_isolated_bin_view_template
        self._provider_session.${method_name}()"""

    get_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resource_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_resources_by_ids_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_ids_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_resources_by_genus_type_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_genus_type_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_resources_by_parent_genus_type_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_parent_genus_type_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_resources_by_record_type_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_record_type_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}()"""

class ResourceQuerySession:

    can_search_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceQuerySession.can_search_resources_template
        return self._can('${func_name}')"""

    get_resource_query_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceQuerySession.get_resource_query_template
        if not self._can('search'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}()"""

    get_resources_by_query_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceQuerySession.get_resources_by_query_template
        if not self._can('search'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}()"""

class ResourceAdminSession:

    init_template = """
    def __init__(self, provider_session, authz_session, proxy = None):
        from ..osid import sessions as osid_sessions
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name}.${object_name}'
"""

    can_create_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.can_create_resources_template
        return self._can('${func_name}')"""

    can_create_resource_with_record_types_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.can_create_resource_with_record_types_template
        # This would like to be a real implementation someday:
        from ..osid.osid_errors import NullArgument, PermissionDenied
        if ${arg0_name} == None:
            raise NullArgument() # Just 'cause the spec says to :)
        else:
            return self._can('admin')"""

    get_resource_form_for_create_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_create_template
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    create_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.create_resource_template
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_resource_form_for_update_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_update_template
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    update_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.update_resource_template
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    delete_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.delete_resource_template
        if not self._can('delete'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    alias_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.alias_resources_template
        if not self._can('alias'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

class BinLookupSession:
    
    init_template = """
    def __init__(self, provider_session, authz_session, proxy = None):
        from ..osid import sessions as osid_sessions
        from ..primitives import Id
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = Id('authorization.Qualifier%3AROOT%40dlkit.mit.edu') # This needs to be done right
        self._id_namespace = '${pkg_name}.${cat_name}'
"""

    use_comparative_bin_view_template = """
        # Implemented from azosid template for -
        # osid.resource.BinLookupSession.use_comparative_bin_view_template
        self._provider_session.${method_name}()"""

    use_plenary_bin_view_template = """
        # Implemented from azosid template for -
        # osid.resource.BinLookupSession.use_plenary_bin_view_template
        self._provider_session.${method_name}()"""

    get_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinLookupSession.get_bin_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_bins_by_ids_template = """
        # Implemented from azosid template for -
        # osid.resource.BinLookupSession.get_bins_by_ids_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinLookupSession.get_bins_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}()"""

class BinAdminSession:

    init_template = """
    def __init__(self, provider_session, authz_session, proxy = None):
        from ..osid import sessions as osid_sessions
        from ..primitives import Id
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = Id('authorization.Qualifier%3AROOT%40dlkit.mit.edu') # This needs to be done right
        self._id_namespace = '${pkg_name}.${cat_name}'
"""

    can_create_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinLookupSession.can_create_bins_template
        return self._can('${func_name}')"""

    can_create_bin_with_record_types_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.can_create_bin_with_record_types_template
        # This would like to be a real implementation someday:
        from ..osid.osid_errors import NullArgument, PermissionDenied
        if ${arg0_name} == None:
            raise NullArgument() # Just 'cause the spec says to :)
        else:
            return self._can('admin')"""

    get_bin_form_for_create_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.get_bin_form_for_create_template
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    create_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.create_bin_template
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_bin_form_for_update_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.get_bin_form_for_update_template
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    update_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.update_bin_template
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    delete_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.delete_bin_template
        if not self._can('delete'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    alias_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.alias_bin_template
        if not self._can('alias'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

