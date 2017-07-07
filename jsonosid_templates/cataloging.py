class CatalogSession:

    get_ids_by_catalog = """
        raise errors.Unimplemented()"""

    get_ids_by_catalogs = """
        raise errors.Unimplemented()"""

    get_catalog_ids_by_id = """
        raise errors.Unimplemented()"""

    get_catalogs_by_id = """
        raise errors.Unimplemented()"""


class CatalogAssignmentSession:

    assign_id_to_catalog = """
        raise errors.Unimplemented()"""

    unassign_id_from_catalog = """
        raise errors.Unimplemented()"""

    reassign_id_to_catalog = """
        raise errors.Unimplemented()"""


class CatalogAdminSession:
    delete_catalog = """
        if self._catalog_session is not None:
            return self._catalog_session.delete_catalog(catalog_id=bin_id)
        collection = JSONClientValidated('cataloging',
                                         collection='Catalog',
                                         runtime=self._runtime)
        if not isinstance(catalog_id, ABCId):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        collection.delete_one({'_id': ObjectId(catalog_id.get_identifier())})"""


class CatalogQuerySession:
    import_statements = [
        'from . import queries'
    ]


class CatalogQuery:
    import_statements = [
        'from dlkit.abstract_osid.osid import errors'
    ]
