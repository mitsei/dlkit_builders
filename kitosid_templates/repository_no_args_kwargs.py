
class AssetAdminSession:

    get_asset_content_form_for_create = """
        # Implemented from -
        # osid.repository.AssetAdminSession.get_asset_content_form_for_create
        return self._get_provider_session('asset_admin_session', 'asset').get_asset_content_form_for_create(asset_id, asset_content_record_types)"""
