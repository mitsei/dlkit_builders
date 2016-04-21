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
        self._provider_manager = runtime.get_manager('REPOSITORY', provider_impl)
        # need to add version argument

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
        self._provider_manager = runtime.get_proxy_manager('REPOSITORY', provider_impl)
        # need to add version argument

    def get_asset_composition_session_for_repository(self, repository_id, proxy):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        try:
            return getattr(sessions, 'AssetCompositionSession')(
                self._provider_manager.get_asset_composition_session_for_repository(repository_id, proxy),
                self._get_authz_session(),
                proxy)
        except AttributeError:
            raise OperationFailed('AssetCompositionSession not implemented in authz_adapter')

    def get_asset_composition_design_session_for_repository(self, repository_id, proxy):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        try:
            return getattr(sessions, 'AssetCompositionDesignSession')(
                self._provider_manager.get_asset_composition_design_session_for_repository(repository_id, proxy),
                self._get_authz_session(),
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

    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None, **kwargs):
        # Implemented from azosid template for -
        # osid.composition.CompositionLookupSession.__init__
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        if 'hierarchy_session' in kwargs:
            self._hierarchy_session = kwargs['hierarchy_session']
        else:
            self._hierarchy_session = None
        if 'query_session' in kwargs:
            self._query_session = kwargs['query_session']
        else:
            self._query_session = None
        self._qualifier_id = provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name_replaced}.${object_name}'
        self.use_federated_${cat_name_under}_view()
        self.use_comparative_${object_name_under}_view()

    def _get_unauth_${cat_name_under}_ids(self, ${cat_name_under}_id):
        if self._can('lookup', ${cat_name_under}_id):
            return [] # Don't go further - assumes authorizations inherited
        else:
            unauth_list = [str(${cat_name_under}_id)]
        if self._hierarchy_session.has_child_${cat_name_under_plural}(${cat_name_under}_id):
            for child_${cat_name_under}_id in self._hierarchy_session.get_child_${cat_name_under}_ids(${cat_name_under}_id):
                unauth_list = unauth_list + self._get_unauth_${cat_name_under}_ids(child_${cat_name_under}_id)
        return unauth_list

    def _try_harder(self, query):
        if self._hierarchy_session is None or self._query_session is None:
            # Should probably try to return empty result instead
            # perhaps through a query.match_any(match = None)?
            raise PermissionDenied()
        for ${cat_name_under}_id in self._get_unauth_${cat_name_under}_ids(self._qualifier_id):
            query.match_${cat_name_under}_id(${cat_name_under}_id, match=False)
        return self._query_session.get_${object_name_under_plural}_by_query(query)
"""

    use_active_composition_view_template = """
        # Implemented from azosid template for -
        # osid.composition.CompositionLookupSession.use_active_composition_view
        return self._provider_session.${method_name}()"""

    use_any_status_composition_view_template = """
        # Implemented from azosid template for -
        # osid.composition.CompositionLookupSession.use_any_status_composition_view
        return self._provider_session.${method_name}()"""

    use_sequestered_composition_view_template = """
        # Implemented from azosid template for -
        # osid.composition.CompositionLookupSession.use_sequestered_composition_view_template
        return self._provider_session.${method_name}()"""

    use_unsequestered_composition_view_template = """
        # Implemented from azosid template for -
        # osid.composition.CompositionLookupSession.use_unsequestered_composition_view_template
        return self._provider_session.${method_name}()"""

class CompositionQuerySession:
    init = """
    def __init__(self, provider_session, authz_session, proxy=None, **kwargs):
        # Implemented from azosid template for -
        # osid.composition.CompositionLookupSession.__init__
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        if 'hierarchy_session' in kwargs:
            self._hierarchy_session = kwargs['hierarchy_session']
        else:
            self._hierarchy_session = None
        if 'query_session' in kwargs:
            self._query_session = kwargs['query_session']
        else:
            self._query_session = None
        self._qualifier_id = provider_session.get_repository_id()
        self._id_namespace = 'repository.Composition'
        self.use_federated_repository_view()

    def _get_unauth_repository_ids(self, repository_id):
        if self._can('lookup', repository_id):
            return [] # Don't go further - assumes authorizations inherited
        else:
            unauth_list = [str(repository_id)]
        if self._hierarchy_session.has_child_repositories(repository_id):
            for child_repository_id in self._hierarchy_session.get_child_repository_ids(repository_id):
                unauth_list = unauth_list + self._get_unauth_repository_ids(child_repository_id)
        return unauth_list

    def _try_harder(self, query):
        if self._hierarchy_session is None or self._query_session is None:
            # Should probably try to return empty result instead
            # perhaps through a query.match_any(match = None)?
            raise PermissionDenied()
        for repository_id in self._get_unauth_repository_ids(self._qualifier_id):
            query.match_repository_id(repository_id, match=False)
        return self._query_session.get_compositions_by_query(query)

    class CompositionQueryWrapper(QueryWrapper):
        \"\"\"Wrapper for CompositionQueries to override match_repository_id method\"\"\"

        def match_repository_id(self, repository_id, match=True):
            self.cat_id_args_list.append({'repository_id': repository_id, 'match': match})

"""


class CompositionSearchSession:

    init = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_repository_id()
        self._id_namespace = 'repository.Composition'
"""

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

