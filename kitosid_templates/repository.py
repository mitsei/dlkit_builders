
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
