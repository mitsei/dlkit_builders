class CatalogAdminSession:
    delete_catalog = """
        if not self._can('delete'):
            raise PermissionDenied()
        return self._provider_session.delete_catalog(catalog_id)"""


class CatalogAssignmentSession:
    init = """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        # This needs to be done right
        # Build from authority in config
        self._qualifier_id = Id('cataloging.Catalog%3AROOT%40ODL.MIT.EDU')
        self._id_namespace = 'cataloging.Catalog'"""


class CatalogSession:
    init = """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        # This needs to be done right
        # Build from authority in config
        self._qualifier_id = Id('cataloging.Catalog%3AROOT%40ODL.MIT.EDU')
        self._id_namespace = 'cataloging.Catalog'"""
