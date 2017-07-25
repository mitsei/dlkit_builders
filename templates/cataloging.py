class CatalogSession:

    get_ids_by_catalog = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        raise errors.Unimplemented()"""
        }
    }

    get_ids_by_catalogs = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        raise errors.Unimplemented()"""
        }
    }

    get_catalog_ids_by_id = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        raise errors.Unimplemented()"""
        }
    }

    get_catalogs_by_id = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        raise errors.Unimplemented()"""
        }
    }


class CatalogAssignmentSession:

    assign_id_to_catalog = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        raise errors.Unimplemented()"""
        }
    }

    unassign_id_from_catalog = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        raise errors.Unimplemented()"""
        }
    }

    reassign_id_to_catalog = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        raise errors.Unimplemented()"""
        }
    }


class CatalogAdminSession:
    delete_catalog = {
        'python': {
            'json': """
    def ${method_name}(self, catalog_id):
        ${doc_string}
        if self._catalog_session is not None:
            return self._catalog_session.delete_catalog(catalog_id=catalog_id)
        collection = JSONClientValidated('cataloging',
                                         collection='Catalog',
                                         runtime=self._runtime)
        if not isinstance(catalog_id, ABCId):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        collection.delete_one({'_id': ObjectId(catalog_id.get_identifier())})"""
        }
    }


class CatalogQuerySession:
    import_statements = {
        'python': {
            'json': [
                'from . import queries'
            ]
        }
    }


class CatalogQuery:
    import_statements = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors'
            ]
        }
    }
