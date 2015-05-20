
from error_lists import session_errors

class ObjectiveRequisiteSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from . import objects',
        'from .. import mongo_client',
        'from . import types',
        'from bson.objectid import ObjectId',
        'UPDATED = True',
        'CREATED = True'
    ]

    get_requisite_objectives_template = """
        # Implemented from template for
        # osid.learning.ObjectiveRequisiteSession.get_requisite_objectives_template
        # NOTE: This implementation currently ignores plenary view
        pass
        collection = mongo_client[self._db_prefix + 'relationship']['Relationship'] ## Really! No we should use OSIDs
        requisite_type = str(Id(**types.Relationship().get_type_data('REQUISITE')))
        result = collection.find({'$$and': {'sourceId': str(objective_id)}, 'genusType': str(requisite_type)},
                                  {'destinationId': 1, '_id': 0})
        catalog_id_list = []
        for i in ${arg0_name}:
            catalog_id_list.append(ObjectId(i.get_identifier()))
        collection = self._db['Relationship']
        ## I LEFT OFF HERE - THERE'S A WAY TO RETURN ONLY DEST IDS I THINK
        result = collection.find({'_id': {'$$in': catalog_id_list}})
        count = collection.find({'_id': {'$$in': catalog_id_list}}).count()
        #mongo_client.close()
        return objects.${return_type}(result, count)"""


class ObjectiveRequisiteAssignmentSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from .. import mongo_client',
    ]


    assign_objective_requisite_template= """
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from ${arg1_abcapp_name}.${arg1_abcpkg_name}.${arg1_module} import ${arg1_type} as ABC${arg1_type}
        if ${arg0_name} is None or ${arg1_name} is None:
            raise errors.NullArgument()
        requisite_type = str(Id(**types.Relationship().get_type_data('REQUISITE')))


        ras = RelationshipManager().get_relationship_admin_session_for_objective_bank(self.get_objective_bank_id())
        rfc = ras.get_relationship_form_for_create(${arg0_name}, ${arg1_name})
        rfc.set_display_name('Objective Requisite')
        rfc.set_description('An Objective Requisite created by the ObjectiveRequisiteAssignmentSession')
        rfc.set_genus_type(requisite_type)
        ras.create_relationship(rfc)"""

    unassign_objective_requisite_template = """
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from ${arg1_abcapp_name}.${arg1_abcpkg_name}.${arg1_module} import ${arg1_type} as ABC${arg1_type}
        from ..relationship.managers import RelationshipManager
        from ..osid.osid_errors import NotFound, NullArgument, OperationFailed, PermissionDenied
        if ${arg0_name} is None or ${arg1_name} is None:
            raise errors.NullArgument()
        requisite_type = str(Id(**types.Relationship().get_type_data('REQUISITE')))
        rls = RelationshipManager().get_relationship_admin_session_for_objective_bank(self.get_objective_bank_id())
        ras = RelationshipManager().get_relationship_admin_session_for_objective_bank(self.get_objective_bank_id())
    """

class ObjectiveAdminSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from .. import mongo_client',
    ]

    delete_objective_template = """
        # Implemented from template for
        # osid.learning.ObjectiveAdminSession.delete_activity_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        if ${arg0_name} is None:
            raise errors.NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            return InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        collection = mongo_client[self._db_prefix + '${package_name}']['${dependent_object_name}']
        if collection.find({'${object_name_mixed}Id': str(${arg0_name})}).count() != 0:
            raise errors.IllegalState('there are still ${dependent_object_name}s associated with this ${object_name}')
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        delete_result = collection.delete_one({'_id': ObjectId(${arg0_name}.get_identifier())})
        if delete_result.delete_count == 0:
            raise errors.NotFound
        # any reason to raise:
            #raise errors.OperationFailed()
        #if 'err' in result and result['err'] is not None:
        #    raise errors.OperationFailed()
        #if result['n'] == 0:
        #    raise errors.NotFound()
        #mongo_client.close()"""


class ActivityLookupSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from . import objects',
        'from .. import mongo_client',
    ]

    get_activities_for_objective_template = """
        # Implemented from template for
        # osid.learning.ActivityLookupSession.get_activities_for_objective_template
        # NOTE: This implementation currently ignores plenary view
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        if self._catalog_view == ISOLATED:
            result = collection.find({'${arg0_object_mixed}Id': str(${arg0_name}),
                                      '${cat_name_mixed}Id': str(self._catalog_id)})
            count = collection.find({'${arg0_object_mixed}Id': str(${arg0_name}),
                                     '${cat_name_mixed}Id': str(self._catalog_id)}).count()
        else:
            result = collection.find({'${arg0_object_mixed}Id': str(${arg0_name})})
            count = collection.find({'${arg0_object_mixed}Id': str(${arg0_name})}).count()
        #mongo_client.close()
        return objects.${return_type}(result, count=count, runtime=self._runtime)"""


class ActivityAdminSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from . import objects',
        'from .. import mongo_client',
    ]

    get_activity_form_for_create_template = """
        # Implemented from template for
        # osid.learning.ActivityAdminSession.get_activity_form_for_create_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from ${arg1_abcapp_name}.${arg1_abcpkg_name}.${arg1_module} import ${arg1_type} as ABC${arg1_type}
        if ${arg0_name} is None or ${arg1_name} is None:
            raise errors.NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('argument is not a valid OSID ${arg0_type}')
        for arg in ${arg1_name}:
            if not isinstance(arg, ABC${arg1_type}):
                raise errors.InvalidArgument('one or more argument array elements is not a valid OSID ${arg1_type}')
        if ${arg1_name} == []:
            ## WHY are we passing ${cat_name_under}_id = self._catalog_id below, seems redundant:
            obj_form = objects.${return_type}(
                ${cat_name_under}_id=self._catalog_id,
                ${arg0_name}=${arg0_name},
                catalog_id=self._catalog_id,
                db_prefix=self._db_prefix,
                runtime=self._runtime)
        else:
            obj_form = objects.${return_type}(
                ${cat_name_under}_id=self._catalog_id,
                record_types=${arg1_name},
                ${arg0_name}=${arg0_name},
                catalog_id=self._catalog_id,
                db_prefix=self._db_prefix,
                runtime=self._runtime)
        obj_form._for_update = False
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form"""



class Activity:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from ..id.objects import IdList',
    ]

    import_statements = [
        'from ..id.objects import IdList',
    ]


    get_objective_id_template = """
        # Implemented from template for osid.learning.Activity.get_objective_id
        return Id(self._my_map['${var_name_mixed}Id'])"""

    get_objective_template = """
        # Implemented from template for osid.learning.Activity.get_objective
        try:
            mgr = self._get_provider_manager('${return_pkg_caps}')
        except ImportError:
            raise errors.OperationFailed('failed to instantiate ${return_pkg_title}Manager')
        if not mgr.supports_${return_type_under}_lookup():
            raise errors.OperationFailed('${return_pkg_title} does not support ${return_type} lookup')
        try:
            lookup_session = mgr.get_${return_type_under}_lookup_session()
            lookup_session.use_federated_${cat_name_under}_view()
            result = lookup_session.get_${return_type_under}(self.get_${var_name}_id())
        except:
            raise errors.OperationFailed()
        else:
            return result"""

    is_asset_based_activity_template = """
        # Implemented from template for osid.learning.Activity.is_asset_based_activity_template
        return self.my_model.${var_name}"""

    get_asset_ids_template = """
        # Implemented from template for osid.learning.Activity.get_asset_ids_template
        return IdList(self._my_map['${var_name_mixed}Ids'])"""

    get_assets_template = """
        # Implemented from template for osid.learning.Activity.get_assets_template
        try:
            mgr = self._get_provider_manager('${return_pkg_caps}')
        except ImportError:
            raise errors.OperationFailed('failed to instantiate ${return_pkg_title}Manager')
        if not mgr.supports_${return_type_list_object_under}_lookup():
            raise errors.OperationFailed('${return_pkg_title} does not support ${return_type_list_object} lookup')
        try:
            lookup_session = mgr.get_${return_type_list_object_under}_lookup_session()
            lookup_session.use_federated_${return_cat_name_under}_view()
            result = lookup_session.get_${return_type_list_object_plural_under}_by_ids(self.get_${var_name_singular}_ids())
        except:
            raise errors.OperationFailed()
        else:
            return result"""


class ActivityForm:

    get_assets_metadata_template = """
        # Implemented from template for osid.learning.ActivityForm.get_assets_metadata_template
        metadata = dict(self._${var_name}_metadata)
        metadata.update({'existing_${var_name}_values': self._my_map['${var_name_singular_mixed}Ids']})
        return Metadata(**metadata)"""

    set_assets_template = """
        # Implemented from template for osid.learning.ActivityForm.set_assets_template
        if ${arg0_name} is None:
            raise errors.NullArgument()
        if not isinstance(${arg0_name}, list):
            raise errors.InvalidArgument()
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        idstr_list = []
        for object_id in ${arg0_name}:
            if not self._is_valid_id(object_id):
                raise errors.InvalidArgument()
            idstr_list.append(str(object_id))
        self._my_map['${var_name_singular_mixed}Ids'] = idstr_list"""

    clear_assets_template = """
        # Implemented from template for osid.learning.ActivityForm.clear_assets_template
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['${var_name_singular_mixed}Ids'] = self._${var_name}_default"""

