
class ObjectiveRequisiteSession:

    get_requisite_objectives_template = """
        # Implemented from template for 
        # osid.learning.ObjectiveRequisiteSession.get_requisite_objectives_template
        # NOTE: This implementation currently ignores plenary view
        from . import types
        from ..primitives import Id
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import OperationFailed, PermissionDenied
        collection = MongoClient()['relationship']['Relationship'] ## Really! No we should use OSIDs
        requisite_type = str(Id(**types.Relationship().get_type_data('REQUISITE')))
        result = collection.find({'$$and': {'sourceId': str(objective_id)}, 'genusType': str(requisite_type)},
                                  {'destinationId': 1, '_id': 0})

        from bson.objectid import ObjectId
        catalog_id_list = []
        for i in ${arg0_name}:
            catalog_id_list.append(ObjectId(i.get_identifier()))
        collection = self._db['Relationship']
        ## I LEFT OFF HERE - THERE'S A WAY TO RETURN ONLY DEST IDS I THINK
        result = collection.find({'_id': {'$$in': catalog_id_list}})
        count = collection.find({'_id': {'$$in': catalog_id_list}}).count()
        return ${return_type}(result, count)"""


class ObjectiveRequisiteAssignmentSession:

    assign_objective_requisite_template= """
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from ${arg1_abcapp_name}.${arg1_abcpkg_name}.${arg1_module} import ${arg1_type} as ABC${arg1_type}
        from ..osid.osid_errors import AlreadyExists, NotFound, NullArgument, OperationFailed, PermissionDenied
        if ${arg0_name} is None or ${arg1_name} is None:
            raise NullArgument()
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
            raise NullArgument()
        requisite_type = str(Id(**types.Relationship().get_type_data('REQUISITE')))
        rls = RelationshipManager().get_relationship_admin_session_for_objective_bank(self.get_objective_bank_id())
        ras = RelationshipManager().get_relationship_admin_session_for_objective_bank(self.get_objective_bank_id())
    """

class ObjectiveAdminSession:

    delete_objective_template = """
        # Implemented from template for 
        # osid.learning.ObjectiveAdminSession.delete_activity_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from ..osid.osid_errors import NotFound, NullArgument, InvalidArgument, IllegalState, OperationFailed, PermissionDenied, Unsupported
        from bson.objectid import ObjectId
        from pymongo import MongoClient
        UPDATED = True
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            return InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        collection = MongoClient()['${package_name}']['${dependent_object_name}']
        if collection.find({'${object_name_mixed}Id': str(${arg0_name})}).count() != 0:
            raise IllegalState('there are still ${dependent_object_name}s associated with this ${object_name}')
        collection = MongoClient()['${package_name}']['${object_name}']
        result = collection.remove({'_id': ObjectId(${arg0_name}.get_identifier())}, justOne=True)
        if 'err' in result and result['err'] is not None:
            raise OperationFailed()
        if result['n'] == 0:
            raise NotFound()"""


class ActivityLookupSession:

    get_activities_for_objective_template = """
        # Implemented from template for 
        # osid.learning.ActivityLookupSession.get_activities_for_objective_template
        # NOTE: This implementation currently ignores plenary view
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import OperationFailed, PermissionDenied
        from pymongo import MongoClient
        collection = MongoClient()['${package_name}']['${object_name}']
        if self._catalog_view == self.ISOLATED:
            result = collection.find({'${arg0_object_mixed}Id': str(${arg0_name}),
                                     '${cat_name_mixed}Id': str(self._catalog_id)})
            count = collection.find({'${arg0_object_mixed}Id': str(${arg0_name}),
                                     '${cat_name_mixed}Id': str(self._catalog_id)}).count()
        else:
            result = collection.find({'${arg0_object_mixed}Id': str(${arg0_name})})
            count = collection.find({'${arg0_object_mixed}Id': str(${arg0_name})}).count()
        return ${return_type}(result, count)"""

class ActivityAdminSession:

    get_activity_form_for_create_template = """
        # Implemented from template for 
        # osid.learning.ActivityAdminSession.get_activity_form_for_create_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from ${arg1_abcapp_name}.${arg1_abcpkg_name}.${arg1_module} import ${arg1_type} as ABC${arg1_type}
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import NullArgument, InvalidArgument, OperationFailed, PermissionDenied, Unsupported
        CREATED = True
        if ${arg0_name} is None or ${arg1_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise InvalidArgument('argument is not a valid OSID ${arg0_type}')
        for arg in ${arg1_name}:
            if not isinstance(arg, ABC${arg1_type}):
                raise InvalidArgument('one or more argument array elements is not a valid OSID ${arg1_type}')
        if ${arg1_name} == []:
            ## WHY are we passing ${cat_name_under}_id = self._catalog_id below, seems redundant:
            obj_form = ${return_type}(${cat_name_under}_id = self._catalog_id, ${arg0_name} = ${arg0_name}, catalog_id = self._catalog_id)
        else:
            obj_form = ${return_type}(${cat_name_under}_id = self._catalog_id, record_types = ${arg1_name}, ${arg0_name} = ${arg0_name}, catalog_id = self._catalog_id)
        obj_form._for_update = False
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form"""


class Activity:

    get_objective_id_template = """
        # Implemented from template for osid.learning.Activity.get_objective_id
        from ..primitives import Id
        return Id(self._my_map['${var_name_mixed}Id'])"""

    get_objective_template = """
        # Implemented from template for osid.learning.Activity.get_objective_id
        from ..osid.osid_errors import OperationFailed
        try:
            from . import managers
        except ImportError:
            raise OperationFailed('failed to import ${return_app_name}.${return_implpkg_name}.managers')
${import_str}        try:
            mgr = managers.${return_pkg_title}Manager()
        except:
            raise OperationFailed('failed to instantiate ${return_pkg_title}Manager')
        if not mgr.supports_${return_type_under}_lookup():
            raise OperationFailed('${return_pkg_title} does not support ${return_type} lookup')
        try:
            lookup_session = mgr.get_${return_type_under}_lookup_session()
            lookup_session.use_federated_${cat_name_under}_view()
            return_object = lookup_session.get_${return_type_under}(self.get_${var_name}_id())
        except:
            raise OperationFailed()
        else:
            return return_object"""

    is_asset_based_activity_template = """
        # Implemented from template for osid.learning.Activity.is_asset_based_activity_template
        return self.my_model.${var_name}"""

    get_asset_ids = """
        pass # IMPLEMENT ME NEXT!"""

    get_assets = """
        pass # IMPLEMENT ME NEXT!"""

