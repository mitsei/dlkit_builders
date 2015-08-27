
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

    # Note: These should be templates.  But first add to pattern mappers

    use_active_composition_view = """
        \"\"\"Pass through to provider CompositionLookupSession.use_active_composition_view\"\"\"
        self._get_provider_session('composition_lookup_session').use_active_composition_view()"""

    use_any_status_composition_view = """
        \"\"\"Pass through to provider CompositionLookupSession.use_any_status_composition_view\"\"\"
        self._get_provider_session('composition_lookup_session').use_any_status_composition_view()"""

    use_sequestered_composition_view = """
        \"\"\"Pass through to provider CompositionLookupSession.use_sequestered_composition_view\"\"\"
        self._get_provider_session('composition_lookup_session').use_sequestered_composition_view()"""

    use_unsequestered_composition_view = """
        \"\"\"Pass through to provider CompositionLookupSession.use_unsequestered_composition_view\"\"\"
        self._get_provider_session('composition_lookup_session').use_unsequestered_composition_view()"""

class AssetCompositionSession:

    can_access_asset_compositions = """
        \"\"\"Pass through to provider AssetCompositionSession.can_access_asset_compositions\"\"\"
        self._get_provider_session('asset_composition_session').can_access_asset_compositions()"""

    get_composition_assets = """
        \"\"\"Pass through to provider AssetCompositionSession.get_composition_assets\"\"\"
        return self._get_provider_session('asset_composition_session').get_composition_assets(*args, **kwargs)"""

    get_compositions_by_asset = """
        \"\"\"Pass through to provider AssetCompositionSession.get_compositions_by_asset\"\"\"
        return self._get_provider_session('asset_composition_session').get_compositions_by_asset(*args, **kwargs)"""


class AssetCompositionDesignSession:

    can_compose_assets = """
        \"\"\"Pass through to provider AssetCompositionDesignSession.can_compose_assets\"\"\"
        self._get_provider_session('asset_composition_design_session').can_compose_assets()"""

    add_asset = """
        \"\"\"Pass through to provider AssetCompositionDesignSession.add_asset\"\"\"
        self._get_provider_session('asset_composition_design_session').add_asset(*args, **kwargs)"""

    move_asset_ahead = """
        \"\"\"Pass through to provider AssetCompositionDesignSession.move_asset_ahead\"\"\"
        self._get_provider_session('asset_composition_design_session').move_asset_ahead(*args, **kwargs)"""

    move_asset_behind = """
        \"\"\"Pass through to provider AssetCompositionDesignSession.move_asset_behind\"\"\"
        self._get_provider_session('asset_composition_design_session').move_asset_behind(*args, **kwargs)"""

    order_assets = """
        \"\"\"Pass through to provider AssetCompositionDesignSession.order_assets\"\"\"
        self._get_provider_session('asset_composition_design_session').order_assets(*args, **kwargs)"""

    remove_asset = """
        \"\"\"Pass through to provider AssetCompositionDesignSession.remove_asset\"\"\"
        self._get_provider_session('asset_composition_design_session').remove_asset(*args, **kwargs)"""
