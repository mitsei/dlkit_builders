from .resource import ResourceAdminSession

class RelationshipLookupSession:

    potential_import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from ..primitives import DateTime'
        'from ..osid.sessions import OsidSession',
        'from ..utilities import MongoClientValidated',
        'fro, ..utilities import overlap',
        'from . import objects',
        'from bson.objectid import ObjectId',
        'DESCENDING = -1',
        'ASCENDING = 1',
        'COMPARATIVE = 0',
        'PLENARY = 1',
        'FEDERATED = 0',
        'ISOLATED = 1',
        'CREATED = True',
        'UPDATED = True'
    ]

    get_relationships_on_date_template = """
        # Implemented from template for
        # osid.relationship.RelationshipLookupSession.get_relationships_on_date
        ${object_name_under}_list = []
        for ${object_name_under} in self.get_${object_name_plural_under}:
            if overlap(${arg0_name}, ${arg1_name}, ${object_name_under}.start_date, ${object_name_under}.end_date):
                ${object_name_under}_list.append(${object_name_under})
        return objects.${object_name}List(${object_name_under}_list, runtime=self._runtime)"""

    get_relationships_for_source_template = """
        # Implemented from template for
        # osid.relationship.RelationshipLookupSession.get_relationships_for_source
        # NOTE: This implementation currently ignores plenary and effective views
        collection = MongoClientValidated(self._db_prefix + '${package_name}', '${object_name}')
        if self._catalog_view == ISOLATED:
            result = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                      '${cat_name_mixed}Id': str(self._catalog_id)}).sort('_sort_id', ASCENDING)
        else:
            result = collection.find({'${source_name_mixed}Id': str(${arg0_name})}).sort('_sort_id', ASCENDING)
        return objects.${object_name}List(result, runtime=self._runtime)"""

    get_relationships_for_source_on_date_template = """
        # Implemented from template for
        # osid.relationship.RelationshipLookupSession.get_relationships_for_source_on_date
        ${object_name_under}_list = []
        for ${object_name_under} in self.get_${object_name_plural_under}_for_${source_name}:
            if overlap(${arg1_name}, ${arg2_name}, ${object_name_under}.start_date, ${object_name_under}.end_date):
                ${object_name_under}_list.append(${object_name_under})
        return objects.${object_name}List(${object_name_under}_list, runtime=self._runtime)"""

    get_relationships_by_genus_type_for_source_template = """
        # Implemented from template for
        # osid.relationship.RelationshipLookupSession.get_relationships_by_genus_type_for_source
        # NOTE: This implementation currently ignores plenary and effective views
        collection = MongoClientValidated(self._db_prefix + '${package_name}', '${object_name}')
        if self._catalog_view == ISOLATED:
            result = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                      'genusTypeId': str(${arg1_name}),
                                      '${cat_name_mixed}Id': str(self._catalog_id)}).sort('_sort_id', ASCENDING)
        else:
            result = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                      'genusTypeId': str(${arg1_name})}).sort('_sort_id', ASCENDING)
        return objects.${object_name}List(result, runtime=self._runtime)"""

    get_relationships_by_genus_type_for_source_on_date_template = """
        # Implemented from template for
        # osid.relationship.RelationshipLookupSession.get_relationships_by_genus_type_for_source_on_date
        ${object_name_under}_list = []
        for ${object_name_under} in self.get_${object_name_plural_under}_by_genus_type_for_${source_name}:
            if overlap(${arg2_name}, ${arg3_name}, ${object_name_under}.start_date, ${object_name_under}.end_date):
                ${object_name_under}_list.append(${object_name_under})
        return objects.${object_name}List(${object_name_under}_list, runtime=self._runtime)"""

    get_relationships_for_destination_template = """
        # Implemented from template for
        # osid.relationship.RelationshipLookupSession.get_relationships_for_destination
        # NOTE: This implementation currently ignores plenary and effective views
        collection = MongoClientValidated(self._db_prefix + '${package_name}', '${object_name}')
        if self._catalog_view == ISOLATED:
            result = collection.find({'${destination_name_mixed}Id': str(${arg0_name}),
                                      '${cat_name_mixed}Id': str(self._catalog_id)}).sort('_sort_id', ASCENDING)
        else:
            result = collection.find({'${destination_name_mixed}Id': str(${arg0_name})}).sort('_sort_id', ASCENDING)
        return objects.${object_name}List(result, runtime=self._runtime)"""

    get_relationships_for_destination_on_date_template = """
        # Implemented from template for
        # osid.relationship.RelationshipLookupSession.get_relationships_for_destination_on_date
        ${object_name_under}_list = []
        for ${object_name_under} in self.get_${object_name_plural_under}_for_${destination_name}:
            if overlap(${arg1_name}, ${arg2_name}, ${object_name_under}.start_date, ${object_name_under}.end_date):
                ${object_name_under}_list.append(${object_name_under})
        return objects.${object_name}List(${object_name_under}_list, runtime=self._runtime)"""

    get_relationships_by_genus_type_for_destination_template = """
        # Implemented from template for
        # osid.relationship.RelationshipLookupSession.get_relationships_by_genus_type_for_destination
        # NOTE: This implementation currently ignores plenary and effective views
        collection = MongoClientValidated(self._db_prefix + '${package_name}', '${object_name}')
        if self._catalog_view == ISOLATED:
            result = collection.find({'${destination_name_mixed}Id': str(${arg0_name}),
                                      'genusTypeId': str(${arg1_name}),
                                      '${cat_name_mixed}Id': str(self._catalog_id)}).sort('_sort_id', ASCENDING)
        else:
            result = collection.find({'${destination_name_mixed}Id': str(${arg0_name}),
                                      'genusTypeId': str(${arg1_name})}).sort('_sort_id', ASCENDING)
        return objects.${object_name}List(result, runtime=self._runtime)"""

    get_relationships_by_genus_type_for_destination_on_date_template = """
        # Implemented from template for
        # osid.relationship.RelationshipLookupSession.get_relationships_by_genus_type_for_destination_on_date
        ${object_name_under}_list = []
        for ${object_name_under} in self.get_${object_name_plural_under}_by_genus_type_for_${destination_name}:
            if overlap(${arg2_name}, ${arg3_name}, ${object_name_under}.start_date, ${object_name_under}.end_date):
                ${object_name_under}_list.append(${object_name_under})
        return objects.${object_name}List(${object_name_under}_list, runtime=self._runtime)"""

    get_relationships_for_peers_template = """
        # Implemented from template for
        # osid.relationship.RelationshipLookupSession.get_relationships_for_peers
        # NOTE: This implementation currently ignores plenary and effective views
        collection = MongoClientValidated(self._db_prefix + '${package_name}', '${object_name}')
        if self._catalog_view == ISOLATED:
            result = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                      '${destination_name_mixed}Id': str(${arg1_name}),
                                      '${cat_name_mixed}Id': str(self._catalog_id)}).sort('_sort_id', ASCENDING)
        else:
            result = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                      '${destination_name_mixed}Id': str(${arg1_name})}).sort('_sort_id', ASCENDING)
        return objects.${object_name}List(result, runtime=self._runtime)"""

    get_relationships_by_genus_type_for_peers_template = """
        # Implemented from template for
        # osid.relationship.RelationshipLookupSession.get_relationships_by_genus_type_for_peers
        # NOTE: This implementation currently ignores plenary and effective views
        collection = MongoClientValidated(self._db_prefix + '${package_name}', '${object_name}')
        if self._catalog_view == ISOLATED:
            result = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                      '${destination_name_mixed}Id': str(${arg1_name}),
                                      'genusTypeId': str(${arg2_name}),
                                      '${cat_name_mixed}Id': str(self._catalog_id)}).sort('_sort_id', ASCENDING)
        else:
            result = collection.find({'${source_name_mixed}Id': str(${arg0_name}),
                                      '${destination_name_mixed}Id': str(${arg1_name}),
                                      'genusTypeId': str(${arg2_name})}).sort('_sort_id', ASCENDING)
        return objects.${object_name}List(result, runtime=self._runtime)"""

class RelationshipAdminSession:

    # For when we get Relatioship based init patterns figured out:
    new_import_statements_pattern = ResourceAdminSession.import_statements_pattern

    # For when we get Relatioship based init patterns figured out:
    new_init_template = ResourceAdminSession.init_template

    import_statements_pattern = [
        'from . import objects',
        'from dlkit.abstract_osid.osid import errors',
    ]
    
    get_relationship_form_for_create_template = """
        # Implemented from template for
        # osid.relationship.RelationshipAdminSession.get_relationship_form_for_create
        # These really need to be in module imports:
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from ${arg2_abcapp_name}.${arg2_abcpkg_name}.${arg2_module} import ${arg2_type} as ABC${arg2_type}
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('argument is not a valid OSID ${arg0_type}')
        if not isinstance(${arg1_name}, ABC${arg1_type}):
            raise errors.InvalidArgument('argument is not a valid OSID ${arg1_type}')
        for arg in ${arg2_name}:
            if not isinstance(arg, ABC${arg2_type}):
                raise errors.InvalidArgument('one or more argument array elements is not a valid OSID ${arg2_type}')
        if ${arg2_name} == []:
            ## WHY are we passing ${cat_name_under}_id = self._catalog_id below, seems redundant:
            obj_form = objects.${return_type}(
                ${cat_name_under}_id=self._catalog_id,
                ${arg0_name}=${arg0_name},
                ${arg1_name}=${arg1_name},
                catalog_id=self._catalog_id,
                db_prefix=self._db_prefix,
                runtime=self._runtime)
        else:
            obj_form = objects.${return_type}(
                ${cat_name_under}_id=self._catalog_id,
                record_types=${arg2_name},
                ${arg0_name}=${arg0_name},
                ${arg1_name}=${arg1_name},
                catalog_id=self._catalog_id,
                db_prefix=self._db_prefix,
                runtime=self._runtime)
        obj_form._for_update = False
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form"""

class Relationship:

    import_statements = [
        'from ..primitives import Id'
    ]

    get_source_id_template = """
        # Implemented from template for osid.relationship.Relationship.get_source_id
        return Id(self._my_map['${var_name_mixed}Id'])"""

class RelationshipQuery:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors'
    ]
