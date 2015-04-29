
class RelationshipLookupSession:

    import_statements_pattern = [
        'from . import objects'
    ]

    get_relationships_for_source_template = """
        # Implemented from template for 
        # osid.relationship.RelationshipLookupSession.get_relationships_for_source
        # NOTE: This implementation currently ignores plenary and effective views
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        if self._catalog_view == ISOLATED:
            result = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                      '${cat_name_mixed}Id': str(self._catalog_id)}).sort('_sort_id', ASCENDING)
            count = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                     '${cat_name_mixed}Id': str(self._catalog_id)}).count()
        else:
            result = collection.find({'${source_name_mixed}Id': str(${arg0_name})}).sort('_sort_id', ASCENDING)
            count = collection.find({'${source_name_mixed}Id': str(${arg0_name})}).count()
        mongo_client.close()
        return objects.${object_name}List(result, count=count, runtime=self._runtime)"""

    get_relationships_by_genus_type_for_source_template = """
        # Implemented from template for 
        # osid.relationship.RelationshipLookupSession.get_relationships_by_genus_type_for_source
        # NOTE: This implementation currently ignores plenary and effective views
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        if self._catalog_view == ISOLATED:
            result = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                      'genusTypeId': str(${arg1_name}),
                                      '${cat_name_mixed}Id': str(self._catalog_id)}).sort('_sort_id', ASCENDING)
            count = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                     'genusTypeId': str(${arg1_name}),
                                     '${cat_name_mixed}Id': str(self._catalog_id)}).count()
        else:
            result = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                      'genusTypeId': str(${arg1_name})}).sort('_sort_id', ASCENDING)
            count = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                     'genusTypeId': str(${arg1_name})}).count()
        mongo_client.close()
        return objects.${object_name}List(result, count=count, runtime=self._runtime)"""

    get_relationships_for_destination_template = """
        # Implemented from template for 
        # osid.relationship.RelationshipLookupSession.get_relationships_for_destination
        # NOTE: This implementation currently ignores plenary and effective views
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        if self._catalog_view == ISOLATED:
            result = collection.find({'${destination_name_mixed}Id': str(${arg0_name}),
                                      '${cat_name_mixed}Id': str(self._catalog_id)}).sort('_sort_id', ASCENDING)
            count = collection.find({'${destination_name_mixed}Id': str(${arg0_name}),
                                     '${cat_name_mixed}Id': str(self._catalog_id)}).count()
        else:
            result = collection.find({'${destination_name_mixed}Id': str(${arg0_name})}).sort('_sort_id', ASCENDING)
            count = collection.find({'${destination_name_mixed}Id': str(${arg0_name})}).count()
        mongo_client.close()
        return objects.${object_name}List(result, count=count, runtime=self._runtime)"""

    get_relationships_by_genus_type_for_destination_template = """
        # Implemented from template for 
        # osid.relationship.RelationshipLookupSession.get_relationships_by_genus_type_for_destination
        # NOTE: This implementation currently ignores plenary and effective views
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        if self._catalog_view == ISOLATED:
            result = collection.find({'${destination_name_mixed}Id': str(${arg0_name}),
                                      'genusTypeId': str(${arg1_name}),
                                      '${cat_name_mixed}Id': str(self._catalog_id)}).sort('_sort_id', ASCENDING)
            count = collection.find({'${destination_name_mixed}Id': str(${arg0_name}),
                                     'genusTypeId': str(${arg1_name}),
                                     '${cat_name_mixed}Id': str(self._catalog_id)}).count()
        else:
            result = collection.find({'${destination_name_mixed}Id': str(${arg0_name}),
                                      'genusTypeId': str(${arg1_name})}).sort('_sort_id', ASCENDING)
            count = collection.find({'${destination_name_mixed}Id': str(${arg0_name}),
                                     'genusTypeId': str(${arg1_name})}).count()
        mongo_client.close()
        return objects.${object_name}List(result, count=count, runtime=self._runtime)"""

    get_relationships_for_peers_template = """
        # Implemented from template for 
        # osid.relationship.RelationshipLookupSession.get_relationships_for_peers
        # NOTE: This implementation currently ignores plenary and effective views
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        if self._catalog_view == ISOLATED:
            result = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                      '${destination_name_mixed}Id': str(${arg1_name}),
                                      '${cat_name_mixed}Id': str(self._catalog_id)}).sort('_sort_id', ASCENDING)
            count = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                     '${destination_name_mixed}Id': str(${arg1_name}),
                                     '${cat_name_mixed}Id': str(self._catalog_id)}).count()
        else:
            result = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                      '${destination_name_mixed}Id': str(${arg1_name})}).sort('_sort_id', ASCENDING)
            count = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                     '${destination_name_mixed}Id': str(${arg1_name})}).count()
        mongo_client.close()
        return objects.${object_name}List(result, count=count, runtime=self._runtime)"""

    get_relationships_by_genus_type_for_peers_template = """
        # Implemented from template for 
        # osid.relationship.RelationshipLookupSession.get_relationships_by_genus_type_for_peers
        # NOTE: This implementation currently ignores plenary and effective views
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        if self._catalog_view == ISOLATED:
            result = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                      '${destination_name_mixed}Id': str(${arg1_name}),
                                      'genusTypeId': str(${arg2_name}),
                                      '${cat_name_mixed}Id': str(self._catalog_id)}).sort('_sort_id', ASCENDING)
            count = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                     '${destination_name_mixed}Id': str(${arg1_name}),
                                     'genusTypeId': str(${arg2_name}),
                                     '${cat_name_mixed}Id': str(self._catalog_id)}).count()
        else:
            result = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                      '${destination_name_mixed}Id': str(${arg1_name}),
                                      'genusTypeId': str(${arg2_name})}).sort('_sort_id', ASCENDING)
            count = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                     '${destination_name_mixed}Id': str(${arg1_name}),
                                     'genusTypeId': str(${arg2_name})}).count()
        mongo_client.close()
        return objects.${object_name}List(result, count=count, runtime=self._runtime)"""

class RelationshipAdminSession:

    
    import_statements_pattern = [
        'from . import objects'
    ]
    
    get_relationship_form_for_create_template = """
        # Implemented from template for 
        # osid.relationship.RelationshipAdminSession.get_relationship_form_for_create
        # These really need to be in module imports:
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from ${arg2_abcapp_name}.${arg2_abcpkg_name}.${arg2_module} import ${arg2_type} as ABC${arg2_type}
        if ${arg0_name} is None or ${arg1_name} is None or ${arg2_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise InvalidArgument('argument is not a valid OSID ${arg0_type}')
        if not isinstance(${arg1_name}, ABC${arg1_type}):
            raise InvalidArgument('argument is not a valid OSID ${arg1_type}')
        for arg in ${arg2_name}:
            if not isinstance(arg, ABC${arg2_type}):
                raise InvalidArgument('one or more argument array elements is not a valid OSID ${arg2_type}')
        if ${arg2_name} == []:
            ## WHY are we passing ${cat_name_under}_id = self._catalog_id below, seems redundant:
            obj_form = objects.${return_type}(${cat_name_under}_id=self._catalog_id, ${arg0_name}=${arg0_name}, ${arg1_name}=${arg1_name}, catalog_id=self._catalog_id, db_prefix=self._db_prefix, runtime=self._runtime)
        else:
            obj_form = objects.${return_type}(${cat_name_under}_id=self._catalog_id, record_types=${arg2_name}, ${arg0_name}=${arg0_name}, ${arg1_name}=${arg1_name}, catalog_id=self._catalog_id, db_prefix=self._db_prefix, runtime=self._runtime)
        obj_form._for_update = False
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form"""

class Relationship:

    import_statements = [
        'from ..primitives import *'
    ]

    get_source_id_template = """
        # Implemented from template for osid.relationship.Relationship.get_source_id
        return Id(self._my_map['${var_name_mixed}Id'])"""

