class CatalogAdminSession:
    delete_catalog = """
        self._get_provider_session('catalog_admin_session').delete_catalog(*args, **kwargs)"""
