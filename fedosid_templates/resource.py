# resource templates for osid_federator implementations


class ResourceProfile:

    supports_visible_federation_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceProfile.supports_visible_federation
        for pm in self._provider_managers:
            if pm.${method_name}() == True:
                return True
        return False"""

    supports_resource_lookup_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceProfile.supports_resource_lookup
        for pm in self._provider_managers:
            if pm.${method_name}() == True:
                return True
        return False"""


class ResourceManager:

    init_template = """
    def __init__(self):
        import settings
        import importlib
        self._provider_managers = []
        for module_path in settings.PROVIDER_MANAGER_MODULE_PATHS:
            provider_module = importlib.import_module(module_path)
            Provider${interface_name} = getattr(provider_module, '${interface_name}')
            self._provider_managers.append(Provider${interface_name}())
"""

    get_resource_lookup_session_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session
        from ${return_module} import ${return_type}
        provider_sessions = []
        for pm in self._provider_managers:
            if pm.supports_${support_check}:
                provider_sessions.append(pm.${method_name}())
        return ${return_type}(provider_sessions)"""

    get_resource_lookup_session_for_bin_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin
        from ${return_module} import ${return_type}
        provider_sessions = []
        for pm in self._provider_managers:
            try:
                if pm.supports_${support_check}:
                    provider_sessions.append(pm.${method_name}(${arg0_name}))
            except NOT_FOUND:
                pass
        if not provider_sessions:
            raise NOT_FOUND
        return ${return_type}(provider_sessions)"""


class ResourceLookupSession:

    init_template = """
    def __init__(self, provider_sessions):
        self._provider_sessions = provider_sessions
        self._id_namespace = '${pkg_name}.${object_name}'
        self._object_view = self.COMPARATIVE
        self._catalog_view = self.FEDERATED
        for ps in self._provider_sessions:
            ps.use_comparative_${object_name_under}_view()
            ps.use_federated_${cat_name_under}_view()
"""

    get_bin_id_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceLookupSession.get_bin_id
        # get default bin Id from first session in provider session list
        return self._provider_sessions[0].${method_name}()"""

    get_bin_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceLookupSession.get_bin
        # get default bin Id from first session in provider session list
        return self._provider_sessions[0].${method_name}()"""

    can_lookup_resources_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceLookupSession.can_lookup_resources
        if self._catalog_view == self.FEDERATED:
            for ps in _provider_sessions:
                if ps.${method_name}() == True:
                    return True
        else:
            return self._provider_sessions[0].${method_name}()"""

    use_comparative_resource_view_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceLookupSession.use_comparative_resource_view
        self._object_view = self.COMPARATIVE
        for ps in self._provider_sessions:
            ps.${method_name}()"""

    use_plenary_resource_view_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceLookupSession.use_plenary_resource_view
        self._object_view = self.PLENARY
        for ps in self._provider_sessions:
            ps.${method_name}()"""

    use_federated_bin_view_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceLookupSession.use_federated_bin_view
        self._catalog_view = self.FEDERATED
        for ps in self._provider_sessions:
            ps.${method_name}()"""

    use_isolated_bin_view_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceLookupSession.use_isolated_bin_view
        self._catalog_view = self.ISOLATED
        for ps in self._provider_sessions:
            ps.${method_name}()"""

    get_resource_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceLookupSession.get_resource
        from osid_kit.osid_errors import NOT_FOUND, NULL_ARGUMENT, OPERATION_FAILED, PERMISSION_DENIED
        if ${arg0_name} is None:
            return NULL_ARGUMENT()
        if self._catalog_view == self.ISOLATED:
            return self._provider_sessions[0].${method_name}(${arg0_name})
        else:
            result = None
            for ps in self._provider_sessions:
                if ps.can_lookup_${object_name_under_plural}():
                    try:
                        result = ps.${method_name}(${arg0_name})
                    except NOT_FOUND:
                        pass # This implementation will raise its own.
                    except OPERATION_FAILED:
                        pass # What to do with OPERATION_FAILED? Plenary vs Comparative?
                    except:
                        raise
                if result:
                    break
        if result:
            return result
        else:
            raise NOT_FOUND()"""

    get_resources_by_ids_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_ids
        pass"""

    get_resources_by_genus_type_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_genus_type
        pass"""

    get_resources_by_parent_genus_type_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_parent_genus_type
        pass"""

    get_resources_by_record_type_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_record_type
        pass"""

    get_resources_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceLookupSession.get_resources
        from objects import ${return_type}
        if self._catalog_view == self.ISOLATED:
            if self._provider_sessions[0].can_lookup_${object_name}():
                return self._provider_sessions[0].${method_name}()
        else:
            results = []
            for ps in self._provider_sessions:
                if ps.can_lookup_${object_name_under_plural}():
                    # What to do with OPERATION_FAILED? Plenary vs Comparative?
                    results.append(ps.${method_name}())
        return ${return_type}(results)"""


class ResourceAdminSession:

    init_template = """
    def __init__(self, provider_sessions):
        # This implementation assumes that the first session in the
        # provider_sessions list is the one for the requested catalog,
        # or is the default catalog if no catalog was specified
        self._provider_session = provider_sessions[0]
        self._id_namespace = '${pkg_name}.${object_name}'
"""

    can_create_resources_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceAdminSession.can_create_resources
        return self._provider_session.${method_name}()"""

    can_create_resource_with_record_types_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceAdminSession.can_create_resource_with_record_types
        return self._provider_session.${method_name}(${arg0_name})"""

    get_resource_form_for_create_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_create
        return self._provider_session.${method_name}(${arg0_name})"""

    create_resource_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceAdminSession.create_resource
        return self._provider_session.${method_name}(${arg0_name})"""

    get_resource_form_for_update_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_update
        return self._provider_session.${method_name}(${arg0_name})"""

    update_resource_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceAdminSession.update_resource
        return self._provider_session.${method_name}(${arg0_name})"""

    delete_resource_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceAdminSession.delete_resource
        return self._provider_session.${method_name}(${arg0_name})"""

    can_manage_resource_aliases_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceAdminSession.can_manage_resource_aliases
        return self._provider_session.${method_name}()"""

    alias_resource_template = """
        # Implemented from fedosid template for -
        # osid.resource.ResourceAdminSession.alias_resources_template
        from osid_kit.osid_errors import PERMISSION_DENIED
        self._provider_session.${method_name}(${arg0_name}=${arg0_name}, ${arg1_name}=${arg1_name})"""


class ResourceList:

    get_next_resource_template = """
        # Implemented from template for osid.resource.ResourceList.get_next_resource
        from osid_kit.osid_errors import ILLEGAL_STATE, OPERATION_FAILED
        next_object = self.next()
        return next_object"""

    get_next_resources_template = """
        # Implemented from template for osid.resource.ResourceList.get_next_resources
        import sys
        from osid_kit.osid_errors import ILLEGAL_STATE, OPERATION_FAILED
        if ${arg0_name} > self.available():
            # This is not quite as specified (see method docs)!
            raise ILLEGAL_STATE('not enough elements available in this list')
        else:
            next_objects = []
            n = 0
            while n < ${arg0_name}:
                try:
                    next_objects.append(self.next())
                except:  # Need to specify exceptions here?
                    raise OPERATION_FAILED()
                n += 1
            return next_objects"""
