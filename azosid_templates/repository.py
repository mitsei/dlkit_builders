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
