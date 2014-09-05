
class AssetAdminSession:

    get_asset_content_form_for_create = """
        # Implemented from -
        # osid.repository.AssetAdminSession.get_asset_content_form_for_create
        return self._get_provider_session('asset_admin_session').get_asset_content_form_for_create(*args, **kwargs)"""

    create_asset_content_template = """
        # Implemented from -
        # osid.repository.AssetAdminSession.create_asset_content_template
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_asset_content_form_for_update_template = """
        # Implemented from -
        # osid.repository.AssetAdminSession.get_asset_content_form_for_update_template
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    update_asset_content_template = """
        # Implemented from -
        # osid.repository.AssetAdminSession.update_asset_template
        # Note: The OSID spec does not require returning updated object
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    delete_asset_content_template = """
        # Implemented from -
        # osid.repository.AssetAdminSession.delete_asset_content_template
        # Note: The OSID spec does not require returning updated object
        self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""
