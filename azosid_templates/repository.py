# repository templates for az_osid

class RepositoryManager:
    # This is here temporarily until Tom adds missing methods to RepositoryManager
    
    init = """
    def __init__(self):
        RepositoryProfile.__init__(self, 'RepositoryManager')


    def initialize(self, runtime):
        osid_managers.OsidManager.initialize(self, runtime)
        config = self._my_runtime.get_configuration()
        parameter_id = Id('parameter:repositoryProviderImpl@authz_adapter')
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        self._provider_manager = runtime.get_manager('REPOSITORY', provider_impl) # need to add version argument

    def get_asset_composition_session_for_repository(self, repository_id, proxy):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        try:
            return getattr(sessions, 'AssetCompositionSession')(
                self._provider_manager.get_asset_composition_session_for_repository(repository_id),
                self._authz_session)
        except AttributeError:
            raise OperationFailed('AssetCompositionSession not implemented in authz_adapter')

    def get_asset_composition_design_session_for_repository(self, repository_id, proxy):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        try:
            return getattr(sessions, 'AssetCompositionDesignSession')(
                self._provider_manager.get_asset_composition_design_session_for_repository(repository_id),
                self._authz_session)
        except AttributeError:
            raise OperationFailed('AssetCompositionDesignSession not implemented in authz_adapter')
"""


class RepositoryProxyManager:
    # This is here temporarily until Tom adds missing methods to RepositoryProxyManager

    init = """
    def __init__(self):
        RepositoryProfile.__init__(self, 'RepositoryProxyManager')

    def initialize(self, runtime):
        osid_managers.OsidProxyManager.initialize(self, runtime)
        config = self._my_runtime.get_configuration()
        parameter_id = Id('parameter:repositoryProviderImpl@authz_adapter')
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        self._provider_manager = runtime.get_proxy_manager('REPOSITORY', provider_impl) # need to add version argument

    def get_asset_composition_session_for_repository(self, repository_id, proxy):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        try:
            return getattr(sessions, 'AssetCompositionSession')(
                self._provider_manager.get_asset_composition_session_for_repository(repository_id, proxy),
                self._authz_session,
                proxy)
        except AttributeError:
            raise OperationFailed('AssetCompositionSession not implemented in authz_adapter')

    def get_asset_composition_design_session_for_repository(self, repository_id, proxy):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        try:
            return getattr(sessions, 'AssetCompositionDesignSession')(
                self._provider_manager.get_asset_composition_design_session_for_repository(repository_id, proxy),
                self._authz_session,
                proxy)
        except AttributeError:
            raise OperationFailed('AssetCompositionDesignSession not implemented in authz_adapter')
"""


class AssetAdminSession:

    create_asset_content_template = """
        # Implemented from azosid template for -
        # osid.repository.AssetAdminSession.create_asset_content_template
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_asset_content_form_for_update_template = """
        # Implemented from azosid template for -
        # osid.repository.AssetAdminSession.get_asset_content_form_for_update_template
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    update_asset_content_template = """
        # Implemented from azosid template for -
        # osid.repository.AssetAdminSession.update_asset_content_template
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    delete_asset_content_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.delete_asset_content_template
        if not self._can('delete'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

class CompositionLookupSession:

    # Note: These should be templated some day. But first add to pattern mappers

    use_active_composition_view = """
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.use_active_composition_view()"""

    use_any_status_composition_view = """
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.use_any_status_composition_view()"""

    use_sequestered_composition_view = """
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.use_sequestered_composition_view()"""

    use_unsequestered_composition_view = """
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.use_unsequestered_composition_view()"""

class AssetCompositionSession:

    init = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_repository_id()
        self._id_namespace = 'repository.AssetComposition'
"""

    can_access_asset_compositions = """
        return self._can('access')"""

    get_composition_assets = """
        if not self._can('access'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_composition_assets(composition_id)"""

    get_compositions_by_asset = """
        if not self._can('access'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_compositions_by_asset(asset_id)"""


class AssetCompositionDesignSession:

    init = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_repository_id()
        self._id_namespace = 'repository.AssetComposition'
"""

    can_compose_assets = """
        return self._can('compose')"""

    add_asset = """
        if not self._can('compose'):
            raise PermissionDenied()
        else:
            return self._provider_session.add_asset(asset_id, composition_id)"""

    move_asset_ahead = """
        if not self._can('compose'):
            raise PermissionDenied()
        else:
            return self._provider_session.move_asset_ahead(asset_id, composition_id, reference_id)"""

    move_asset_behind = """
        if not self._can('compose'):
            raise PermissionDenied()
        else:
            return self._provider_session.move_asset_behind(asset_id, composition_id, reference_id)"""

    order_assets = """
        if not self._can('compose'):
            raise PermissionDenied()
        else:
            return self._provider_session.order_assets(asset_ids, composition_id)"""

    remove_asset = """
        if not self._can('compose'):
            raise PermissionDenied()
        else:
            return self._provider_session.remove_asset(asset_id, composition_id)"""

