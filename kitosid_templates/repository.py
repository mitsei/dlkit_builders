
class RepositoryProfile:

    get_coordinate_types_template = """
        \"\"\"Pass through to provider ${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.repository.RepositoryProfile.get_coordinate_types
        return self._provider_manager.${method_name}(${args_kwargs_or_nothing})"""

    supports_coordinate_type_template = """
        \"\"\"Pass through to provider ${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.repository.RepositoryProfile.supports_coordinate_type
        return self._provider_manager.${method_name}(${args_kwargs_or_nothing})"""


class AssetAdminSession:

    # Why is this one not a template???
    get_asset_content_form_for_create = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from -
        # osid.repository.AssetAdminSession.get_asset_content_form_for_create
        return self._get_provider_session('asset_admin_session').get_asset_content_form_for_create(*args, **kwargs)"""

    create_asset_content_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from -
        # osid.repository.AssetAdminSession.create_asset_content_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_asset_content_form_for_update_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from -
        # osid.repository.AssetAdminSession.get_asset_content_form_for_update_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    update_asset_content_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from -
        # osid.repository.AssetAdminSession.update_asset_template
        # Note: The OSID spec does not require returning updated object
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    delete_asset_content_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from -
        # osid.repository.AssetAdminSession.delete_asset_content_template
        # Note: The OSID spec does not require returning updated object
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""


class CompositionLookupSession:

    use_active_composition_view_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._operable_views['${object_name_under}'] = ACTIVE
        self._get_provider_session('${interface_name_under}') # To make sure the session is tracked
        for session in self._provider_sessions:
            try:
                self._provider_sessions[session].${method_name}()
            except AttributeError:
                pass"""

    use_any_status_composition_view_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._operable_views['${object_name_under}'] = ANY_STATUS
        self._get_provider_session('${interface_name_under}') # To make sure the session is tracked
        for session in self._provider_sessions:
            try:
                self._provider_sessions[session].${method_name}()
            except AttributeError:
                pass"""

    use_sequestered_composition_view_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._containable_views['${object_name_under}'] = SEQUESTERED
        self._get_provider_session('${interface_name_under}') # To make sure the session is tracked
        for session in self._provider_sessions:
            try:
                self._provider_sessions[session].${method_name}()
            except AttributeError:
                pass"""

    use_unsequestered_composition_view_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._containable_views['${object_name_under}'] = UNSEQUESTERED
        self._get_provider_session('${interface_name_under}') # To make sure the session is tracked
        for session in self._provider_sessions:
            try:
                self._provider_sessions[session].${method_name}()
            except AttributeError:
                pass"""

class AssetCompositionSession:

    can_access_asset_compositions_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_composition_assets_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_compositions_by_asset_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""


class AssetCompositionDesignSession:

    can_compose_assets_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    add_asset_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    move_asset_ahead_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    move_asset_behind_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    order_assets_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    remove_asset_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""


class Repository:
    additional_methods = """
    def get_asset_content(self, *args, **kwargs):
        \"\"\"Pass through to provider AssetLookupSession.get_asset_content
            Out-of-band, non-OSID convenience method
        \"\"\"
        return self._get_provider_session('asset_lookup_session').get_asset_content(*args, **kwargs)

    def get_asset_content_query(self, *args, **kwargs):
        \"\"\"Pass through to provider AssetQuerySession.get_asset_content_query
            Out-of-band, non-OSID convenience method
        \"\"\"
        return self._get_provider_session('asset_query_session').get_asset_content_query(*args, **kwargs)

    def get_asset_contents_by_query(self, *args, **kwargs):
        \"\"\"Pass through to provider AssetQuerySession.get_asset_contents_by_query
            Out-of-band, non-OSID convenience method
        \"\"\"
        return self._get_provider_session('asset_query_session').get_asset_contents_by_query(*args, **kwargs)"""
