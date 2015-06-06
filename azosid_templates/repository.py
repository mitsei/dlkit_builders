# repository templates for az_osid

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

    init_template = """
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

    init_template = """
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

