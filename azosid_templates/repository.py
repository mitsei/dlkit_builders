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

    def get_asset_content_lookup_session(self, proxy):
        \"\"\"Pass through to provider get_asset_content_lookup_session\"\"\"
        try:
            return getattr(sessions, 'AssetContentLookupSession')(
                self._provider_manager.get_asset_content_lookup_session(),
                self._authz_session)
        except AttributeError:
            raise OperationFailed('AssetContentLookupSession not implemented in authz_adapter')

    def get_asset_content_lookup_session_for_repository(self, repository_id, proxy):
        \"\"\"Pass through to provider get_asset_content_lookup_session_for_repository\"\"\"
        try:
            return getattr(sessions, 'AssetContentLookupSession')(
                self._provider_manager.get_asset_content_lookup_session_for_repository(repository_id),
                self._authz_session)
        except AttributeError:
            raise OperationFailed('AssetContentLookupSession not implemented in authz_adapter')"""


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

    def get_asset_content_lookup_session(self, proxy):
        \"\"\"Pass through to provider get_asset_content_lookup_session\"\"\"
        try:
            return getattr(sessions, 'AssetContentLookupSession')(
                self._provider_manager.get_asset_content_lookup_session(proxy),
                self._get_authz_session(),
                proxy)
        except AttributeError:
            raise OperationFailed('AssetContentLookupSession not implemented in authz_adapter')

    def get_asset_content_lookup_session_for_repository(self, repository_id, proxy):
        \"\"\"Pass through to provider get_asset_content_lookup_session_for_repository\"\"\"
        try:
            return getattr(sessions, 'AssetContentLookupSession')(
                self._provider_manager.get_asset_content_lookup_session_for_repository(repository_id, proxy),
                self._get_authz_session(),
                proxy)
        except AttributeError:
            raise OperationFailed('AssetContentLookupSession not implemented in authz_adapter')"""


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
        self._unauth_${cat_name_under}_ids = None

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
        if self._unauth_${cat_name_under}_ids is None:
            self._unauth_${cat_name_under}_ids = self._get_unauth_${cat_name_under}_ids(self._qualifier_id)
        for ${cat_name_under}_id in self._unauth_${cat_name_under}_ids:
            query.match_${cat_name_under}_id(${cat_name_under}_id, match=False)
        return self._query_session.get_${object_name_under_plural}_by_query(query)"""

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
    
    # This should be an init_template:
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
        self._unauth_repository_ids = None

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
        if self._unauth_repository_ids is None:
            self._unauth_repository_ids = self._get_unauth_repository_ids(self._qualifier_id)
        for repository_id in self._unauth_repository_ids:
            query.match_repository_id(repository_id, match=False)
        return self._query_session.get_compositions_by_query(query)

    class CompositionQueryWrapper(QueryWrapper):
        \"\"\"Wrapper for CompositionQueries to override match_repository_id method\"\"\"

        def match_repository_id(self, repository_id, match=True):
            self.cat_id_args_list.append({'repository_id': repository_id, 'match': match})"""


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

    get_composition_assets_template = """
        if not self._can('access'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_compositions_by_asset_template = """
        if not self._can('access'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""


class AssetCompositionDesignSession:

    init = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_repository_id()
        self._id_namespace = 'repository.AssetComposition'
"""

    can_compose_assets = """
        return self._can('compose')"""

    add_asset_template = """
        if not self._can('compose'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

    move_asset_ahead_template = """
        if not self._can('compose'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name}, ${arg2_name})"""

    move_asset_behind_template = """
        if not self._can('compose'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name}, ${arg2_name})"""

    order_assets_template = """
        if not self._can('compose'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

    remove_asset_template = """
        if not self._can('compose'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

class AssetLookupSession:
    additional_methods = """
    # def get_asset_content(self, asset_content_id):
    #     if not self._can('lookup'):
    #         raise PermissionDenied()
    #     else:
    #         return self._provider_session.get_asset_content(asset_content_id)


class AssetContentLookupSession(abc_repository_sessions.AssetContentLookupSession, osid_sessions.OsidSession):
    \"\"\"Adapts underlying AssetContentLookupSession methods with authorization checks
    For now uses the "Asset" namespace authz -- assumes if you can lookup an asset, you can
     lookup the contents. That could change in the future.
    \"\"\"

    def __init__(self, provider_session, authz_session, proxy=None, **kwargs):
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
        self._id_namespace = 'repository.Asset'
        self.use_federated_repository_view()
        self.use_comparative_asset_content_view()
        self._unauth_repository_ids = None

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
        if self._unauth_repository_ids is None:
            self._unauth_repository_ids = self._get_unauth_repository_ids(self._qualifier_id)
        for repository_id in self._unauth_repository_ids:
            query.match_repository_id(repository_id, match=False)
        return self._query_session.get_assets_by_query(query)

    def get_repository_id(self):
        return self._provider_session.get_repository_id()

    repository_id = property(fget=get_repository_id)

    def get_repository(self):
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_repository()

    repository = property(fget=get_repository)

    def can_lookup_asset_contents(self):
        return self._can('lookup')

    def use_comparative_asset_content_view(self):
        self._use_comparative_object_view()
        self._provider_session.use_comparative_asset_content_view()

    def use_plenary_asset_content_view(self):
        self._use_plenary_object_view()
        self._provider_session.use_plenary_asset_content_view()

    def use_federated_repository_view(self):
        self._use_federated_catalog_view()
        self._provider_session.use_federated_repository_view()

    def use_isolated_repository_view(self):
        self._use_isolated_catalog_view()
        self._provider_session.use_isolated_repository_view()

    def get_asset_content(self, asset_content_id):
        if self._can('lookup'):
            return self._provider_session.get_asset_content(asset_content_id)
        elif self._is_isolated_catalog_view() or self._is_plenary_object_view():
            raise PermissionDenied()
        else:
            query = self._query_session.get_asset_content_query()
            query.match_id(asset_content_id, match=True)
            results = self._try_harder(query)
            if results.available() > 0:
                return results.next()
            else:
                raise NotFound()

    def get_asset_contents_by_ids(self, asset_content_ids):
        if self._can('lookup'):
            return self._provider_session.get_asset_contents_by_ids(asset_content_ids)
        elif self._is_isolated_catalog_view() or self._is_plenary_object_view():
            raise PermissionDenied()
        else:
            query = self._query_session.get_asset_content_query()
            for asset_content_id in (asset_content_ids):
                query.match_id(asset_content_id, match=True)
            return self._try_harder(query)

    def get_asset_contents_by_genus_type(self, asset_content_genus_type):
        if self._can('lookup'):
            return self._provider_session.get_asset_contents_by_genus_type(asset_content_genus_type)
        elif self._is_isolated_catalog_view() or self._is_plenary_object_view():
            raise PermissionDenied()
        else:
            query = self._query_session.get_asset_content_query()
            query.match_genus_type(asset_content_genus_type, match=True)
            return self._try_harder(query)

    def get_asset_contents_by_parent_genus_type(self, asset_content_genus_type):
        if self._can('lookup'):
            return self._provider_session.get_asset_contents_by_parent_genus_type(asset_content_genus_type)
        elif self._is_isolated_catalog_view() or self._is_plenary_object_view():
            raise PermissionDenied()
        else:
            query = self._query_session.get_asset_content_query()
            query.match_parent_genus_type(asset_content_genus_type, match=True)
            return self._try_harder(query)

    def get_asset_contents_by_record_type(self, asset_content_record_type):
        if self._can('lookup'):
            return self._provider_session.get_asset_contents_by_record_type(asset_content_record_type)
        elif self._is_isolated_catalog_view() or self._is_plenary_object_view():
            raise PermissionDenied()
        else:
            query = self._query_session.get_asset_content_query()
            query.match_record_type(asset_content_record_type, match=True)
            return self._try_harder(query)

    def get_asset_contents_for_asset(self, asset_id):
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_asset_contents_for_asset(asset_id)

    def get_asset_contents_by_genus_type_for_asset(self, asset_content_genus_type, asset_id):
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_asset_contents_by_genus_type_for_asset(asset_content_genus_type,
                                                                                     asset_id)"""

class AssetQuerySession:
    additional_methods = """
    def get_asset_content_query(self):
        if not self._can('search'):
            raise PermissionDenied()
        else:
            return self.AssetQueryWrapper(self._provider_session.get_asset_content_query())

    def get_asset_contents_by_query(self, asset_content_query):
        if not hasattr(asset_content_query, 'cat_id_args_list'):
            raise Unsupported('asset_content_query not from this session')
        for kwargs in asset_content_query.cat_id_args_list:
            if self._can('search', kwargs['repository_id']):
                asset_content_query._provider_query.match_repository_id(**kwargs)
        if self._can('search'):
            return self._provider_session.get_asset_contents_by_query(asset_content_query)
        elif self._is_isolated_catalog_view():
            raise PermissionDenied()
        else:
            result = self._try_harder(asset_content_query)
            asset_content_query._provider_query.clear_repository_terms()
            return result"""
