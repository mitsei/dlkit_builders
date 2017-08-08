class ObjectiveRequisiteSession:

    import_statements = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
                'from . import objects',
                'from ..utilities import JSONClientValidated',
                'from bson.objectid import ObjectId',
                'from ..types import Relationship',
                'UPDATED = True',
                'CREATED = True'
            ]
        }
    }

    init = {
        'python': {
            'json': """
    def __init__(self, catalog_id=None, proxy=None, runtime=None):
        self._catalog_class = objects.Objective
        self._catalog_name = 'ObjectiveBank'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='learning',
            cat_name='ObjectiveBank',
            cat_class=objects.ObjectiveBank)
        self._forms = dict()""",
            'authz': """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        self._qualifier_id = self._provider_session.get_objective_bank_id()
        self._id_namespace = 'learning.Objective'
        self._auth_objective_bank_ids = None
        self._unauth_objective_bank_ids = None"""
        }
    }

    # get_requisite_objectives_template = """
    #     # Implemented from template for
    #     # osid.learning.ObjectiveRequisiteSession.get_requisite_objectives_template
    #     # NOTE: This implementation currently ignores plenary view
    #     requisite_type = Type(**Relationship().get_type_data('OBJECTIVE.REQUISITE'))
    #     relm = self._get_provider_manager('RELATIONSHIP')
    #     rls = relm.get_relationship_lookup_session(proxy=self._proxy)
    #     rls.use_federated_family_view()
    #     requisite_relationships = rls.get_relationships_by_genus_type_for_source(${arg0_name},
    #                                                                              requisite_type)
    #     destination_ids = [ObjectId(r.get_destination_id().identifier)
    #                        for r in requisite_relationships]
    #     collection = JSONClientValidated('learning',
    #                                      collection='Objective',
    #                                      runtime=self._runtime)
    #     result = collection.find({'_id': {'$$in': destination_ids}})
    #     return objects.${return_type}(result, runtime=self._runtime)"""
    #
    # can_lookup_objective_prerequisites = """
    #     return True"""
    #
    # get_dependent_objectives_template = """
    #     # Implemented from template for
    #     # osid.learning.ObjectiveRequisiteSession.get_dependent_objectives_template
    #     # NOTE: This implementation currently ignores plenary view
    #     requisite_type = Type(**Relationship().get_type_data('OBJECTIVE.REQUISITE'))
    #     relm = self._get_provider_manager('RELATIONSHIP')
    #     rls = relm.get_relationship_lookup_session(proxy=self._proxy)
    #     rls.use_federated_family_view()
    #     requisite_relationships = rls.get_relationships_by_genus_type_for_destination(${arg0_name},
    #                                                                                   requisite_type)
    #     source_ids = [ObjectId(r.get_source_id().identifier)
    #                   for r in requisite_relationships]
    #     collection = JSONClientValidated('learning',
    #                                      collection='Objective',
    #                                      runtime=self._runtime)
    #     result = collection.find({'_id': {'$$in': source_ids}})
    #     return objects.${return_type}(result, runtime=self._runtime)"""


class ObjectiveRequisiteAssignmentSession:

    import_statements = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
                'from ..types import Relationship'
            ]
        }
    }

    init = {
        'python': {
            'json': """
    def __init__(self, catalog_id=None, proxy=None, runtime=None):
        self._catalog_class = objects.Objective
        self._catalog_name = 'ObjectiveBank'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='learning',
            cat_name='ObjectiveBank',
            cat_class=objects.ObjectiveBank)
        self._forms = dict()""",
            'authz': """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        self._qualifier_id = self._provider_session.get_objective_bank_id()
        self._id_namespace = 'learning.Objective'
        self._auth_objective_bank_ids = None
        self._unauth_objective_bank_ids = None"""
        }
    }

    # assign_objective_requisite_import_templates = [
    #     'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}',
    #     'from ${arg1_abcapp_name}.${arg1_abcpkg_name}.${arg1_module} import ${arg1_type} as ABC${arg1_type}'
    # ]
    #
    # assign_objective_requisite_template = """
    #     requisite_type = Type(**Relationship().get_type_data('${object_name_upper}.REQUISITE'))
    #
    #     ras = self._get_provider_manager(
    #         'RELATIONSHIP').get_relationship_admin_session_for_family(
    #         self.get_${cat_name_under}_id(), proxy=self._proxy)
    #     rfc = ras.get_relationship_form_for_create(${arg0_name}, ${arg1_name}, [])
    #     rfc.set_display_name('${object_name} Requisite')
    #     rfc.set_description('An ${object_name} Requisite created by the ${object_name}RequisiteAssignmentSession')
    #     rfc.set_genus_type(requisite_type)
    #     ras.create_relationship(rfc)"""
    #
    # unassign_objective_requisite_import_templates = [
    #     'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}',
    #     'from ${arg1_abcapp_name}.${arg1_abcpkg_name}.${arg1_module} import ${arg1_type} as ABC${arg1_type}',
    # ]
    #
    # unassign_objective_requisite_template = """
    #     requisite_type = Type(**Relationship().get_type_data('${object_name_upper}.REQUISITE'))
    #     rls = self._get_provider_manager(
    #         'RELATIONSHIP').get_relationship_lookup_session_for_family(
    #         self.get_${cat_name_under}_id(), proxy=self._proxy)
    #     ras = self._get_provider_manager(
    #         'RELATIONSHIP').get_relationship_admin_session_for_family(
    #         self.get_${cat_name_under}_id(), proxy=self._proxy)
    #     rls.use_federated_family_view()
    #     relationships = rls.get_relationships_by_genus_type_for_source(${arg0_name}, requisite_type)
    #     if relationships.available() == 0:
    #         raise errors.IllegalState('no ${object_name} found')
    #     for relationship in relationships:
    #         if str(relationship.get_destination_id()) == str(${arg1_name}):
    #             ras.delete_relationship(relationship.ident)"""


# class ObjectiveAdminSession:
#
#     import_statements_pattern = [
#         'from dlkit.abstract_osid.osid import errors',
#         'from ..primitives import Id',
#         'from ..utilities import JSONClientValidated',
#     ]
#
#     delete_objective_import_templates = [
#         'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
#     ]
#
#     delete_objective_template = """
#         # Implemented from template for
#         # osid.learning.ObjectiveAdminSession.delete_objective_template
#
#         if not isinstance(${arg0_name}, ABC${arg0_type}):
#             raise errors.InvalidArgument('the argument is not a valid OSID ${arg0_type}')
#         collection = JSONClientValidated('${package_name_replace}',
#                                          collection='${dependent_object_name}',
#                                          runtime=self._runtime)
#         if collection.find({'${object_name_mixed}Id': str(${arg0_name})}).count() != 0:
#             raise errors.IllegalState('there are still ${dependent_object_name}s associated with this ${object_name}')
#
#         collection = JSONClientValidated('${package_name_replace}',
#                                          collection='${object_name}',
#                                          runtime=self._runtime)
#         collection.delete_one({'_id': ObjectId(${arg0_name}.get_identifier())})"""


# class ActivityLookupSession:
#
#     import_statements_pattern = [
#         'from dlkit.abstract_osid.osid import errors',
#         'from ..primitives import Id',
#         'from . import objects',
#         'from ..utilities import JSONClientValidated',
#     ]
#
#     get_activities_for_objective_template = """
#         # Implemented from template for
#         # osid.learning.ActivityLookupSession.get_activities_for_objective_template
#         # NOTE: This implementation currently ignores plenary view
#         collection = JSONClientValidated('${package_name_replace}',
#                                          collection='${object_name}',
#                                          runtime=self._runtime)
#         result = collection.find(
#             dict({'${arg0_object_mixed}Id': str(${arg0_name})},
#                  **self._view_filter()))
#         return objects.${return_type}(result, runtime=self._runtime)"""


# class ActivityAdminSession:
#
#     import_statements_pattern = [
#         'from dlkit.abstract_osid.osid import errors',
#         'from ..primitives import Id',
#         'from . import objects',
#     ]

    # get_activity_form_for_create_import_templates = [
    #     'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}',
    #     'from ${arg1_abcapp_name}.${arg1_abcpkg_name}.${arg1_module} import ${arg1_type} as ABC${arg1_type}'
    # ]
    #
    # get_activity_form_for_create_template = """
    #     # Implemented from template for
    #     # osid.learning.ActivityAdminSession.get_activity_form_for_create_template
    #
    #     if not isinstance(${arg0_name}, ABC${arg0_type}):
    #         raise errors.InvalidArgument('argument is not a valid OSID ${arg0_type}')
    #     for arg in ${arg1_name}:
    #         if not isinstance(arg, ABC${arg1_type}):
    #             raise errors.InvalidArgument('one or more argument array elements is not a valid OSID ${arg1_type}')
    #     if ${arg1_name} == []:
    #         # WHY are we passing ${cat_name_under}_id = self._catalog_id below, seems redundant:
    #         obj_form = objects.${return_type}(
    #             ${cat_name_under}_id=self._catalog_id,
    #             ${arg0_name}=${arg0_name},
    #             catalog_id=self._catalog_id,
    #             runtime=self._runtime,
    #             proxy=self._proxy)
    #     else:
    #         obj_form = objects.${return_type}(
    #             ${cat_name_under}_id=self._catalog_id,
    #             record_types=${arg1_name},
    #             ${arg0_name}=${arg0_name},
    #             catalog_id=self._catalog_id,
    #             runtime=self._runtime,
    #             proxy=self._proxy)
    #     obj_form._for_update = False
    #     self._forms[obj_form.get_id().get_identifier()] = not CREATED
    #     return obj_form"""


class Activity:

    # import_statements = [
    #     # 'from dlkit.abstract_osid.osid import errors',
    #     # 'from ..primitives import Id',
    #     'from ..id.objects import IdList',
    # ]
    #
    # import_statements = [
    #     'from ..id.objects import IdList',
    # ]

    # get_objective_id_template = """
    #     # Implemented from template for osid.learning.Activity.get_objective_id
    #     if not bool(self._my_map['${var_name_mixed}Id']):
    #         raise errors.IllegalState('${var_name} empty')
    #     return Id(self._my_map['${var_name_mixed}Id'])"""

    # get_objective_template = """
    #     # Implemented from template for osid.learning.Activity.get_objective
    #     if not bool(self._my_map['${var_name_mixed}Id']):
    #         raise errors.IllegalState('${var_name} empty')
    #     mgr = self._get_provider_manager('${return_pkg_replace_caps}')
    #     if not mgr.supports_${return_type_under}_lookup():
    #         raise errors.OperationFailed('${return_pkg_replace_title} does not support ${return_type} lookup')
    #     lookup_session = mgr.get_${return_type_under}_lookup_session(proxy=getattr(self, "_proxy", None))
    #     lookup_session.use_federated_${return_cat_name_under}_view()
    #     return lookup_session.get_${return_type_under}(self.get_${var_name}_id())"""

    is_course_based_activity = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        return bool(self._my_map['courseIds'])"""
        }
    }

    is_assessment_based_activity = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        return bool(self._my_map['assessmentIds'])"""
        }
    }

    is_asset_based_activity = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        return bool(self._my_map['assetIds'])"""
        }
    }

    # This is actually used by Grading.GradeSystem.is_based_on_grades
    # Something wrong with our patterns, if it isn't going to the source pattern of
    # Resource.Resource.is_group_template...
    # is_asset_based_activity_template = """
    #     # Implemented from template for osid.learning.Activity.is_asset_based_activity_template
    #     return self._my_map['${var_name_mixed}']"""

    # get_asset_ids_template = """
    #     # Implemented from template for osid.learning.Activity.get_asset_ids_template
    #     return IdList(self._my_map['${var_name_mixed}Ids'])"""

    # get_assets_template = """
    #     # Implemented from template for osid.learning.Activity.get_assets_template
    #     if not bool(self._my_map['${var_name_singular_mixed}Ids']):
    #         raise errors.IllegalState('no ${var_name_singular_mixed}Ids')
    #     mgr = self._get_provider_manager('${return_pkg_caps}')
    #     if not mgr.supports_${return_type_list_object_under}_lookup():
    #         raise errors.OperationFailed('${return_pkg_title} does not support ${return_type_list_object} lookup')
    #
    #     # What about the Proxy?
    #     lookup_session = mgr.get_${return_type_list_object_under}_lookup_session(proxy=getattr(self, "_proxy", None))
    #     lookup_session.use_federated_${return_cat_name_under}_view()
    #     return lookup_session.get_${return_type_list_object_plural_under}_by_ids(self.get_${var_name_singular}_ids())"""


class ObjectiveHierarchySession:
    init = {
        'python': {
            'json': """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, *args, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.Objective
        self._catalog_name = 'ObjectiveBank'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='learning',
            cat_name='ObjectiveBank',
            cat_class=objects.ObjectiveBank)
        self._forms = dict()
        self._kwargs = kwargs
        hierarchy_mgr = self._get_provider_manager('HIERARCHY')
        self._hierarchy_session = hierarchy_mgr.get_hierarchy_traversal_session_for_hierarchy(
            Id(authority='LEARNING',
               namespace='CATALOG',
               identifier='OBJECTIVE'),
            proxy=self._proxy
        )"""
        }
    }


class ObjectiveHierarchyDesignSession:
    init = {
        'python': {
            'json': """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, *args, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.Objective
        self._catalog_name = 'ObjectiveBank'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='learning',
            cat_name='ObjectiveBank',
            cat_class=objects.ObjectiveBank)
        self._forms = dict()
        self._kwargs = kwargs
        hierarchy_mgr = self._get_provider_manager('HIERARCHY')
        self._hierarchy_session = hierarchy_mgr.get_hierarchy_design_session_for_hierarchy(
            Id(authority='LEARNING',
               namespace='CATALOG',
               identifier='OBJECTIVE'),
            proxy=self._proxy
        )"""
        }
    }


class ObjectiveSequencingSession:
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
                'from ..types import Relationship'
            ]
        }
    }

    init = {
        'python': {
            'json': """
    def __init__(self, catalog_id=None, proxy=None, runtime=None):
        self._catalog_class = objects.Objective
        self._catalog_name = 'ObjectiveBank'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='learning',
            cat_name='ObjectiveBank',
            cat_class=objects.ObjectiveBank)
        self._forms = dict()"""
        }
    }


class ProficiencyForm:

    set_level = {
        'python': {
            'json': """
    def ${method_name}(self, grade):
        ${doc_string}
        if self.get_level_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_id(grade):
            raise errors.InvalidArgument()
        self._my_map['level'] = str(grade)

    def set_level_id(self, grade_id):
        if self.get_level_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_id(grade_id):
            raise errors.InvalidArgument()
        self._my_map['levelId'] = str(grade_id)"""
        }
    }

    clear_level = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        if (self.get_level_metadata().is_read_only() or
                self.get_level_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['levelId'] = self._level_default
        self._my_map['level'] = self._level_default"""
        }
    }


class ProficiencyQuery:
    init = {
        'python': {
            'json': """
    def __init__(self, runtime):
        self._namespace = '${pkg_name}.${object_name}'
        self._runtime = runtime
        record_type_data_sets = get_registry('${object_name_upper}_RECORD_TYPES', runtime)
        self._all_supported_record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_ids = []
        for data_set in record_type_data_sets:
            self._all_supported_record_type_ids.append(str(Id(**record_type_data_sets[data_set])))
        osid_queries.OsidObjectQuery.__init__(self, runtime)"""
        }
    }

    match_level_id = {
        'python': {
            'json': """
    def ${method_name}(self, grade_id, match):
        ${doc_string}
        if not isinstance(grade_id, Id):
            raise errors.InvalidArgument()
        self._add_match('levelId', str(grade_id), match)"""
        }
    }

    match_completion = {
        'python': {
            'json': """
    def ${method_name}(self, start, end, match):
        ${doc_string}
        try:
            start = float(start)
        except ValueError:
            raise errors.InvalidArgument('Invalid start value')
        try:
            end = float(end)
        except ValueError:
            raise errors.InvalidArgument('Invalid end value')
        if match:
            if end < start:
                raise errors.InvalidArgument('end value must be >= start value when match = True')
            self._query_terms['completion'] = {
                '$$gte': start,
                '$$lte': end
            }
        else:
            raise errors.InvalidArgument('match = False not currently supported')"""
        }
    }

    match_resource_id = {
        'python': {
            'json': """
    def ${method_name}(self, resource_id):
        ${doc_string}
        if not isinstance(resource_id, Id):
            raise errors.InvalidArgument()
        self._add_match('resourceId', str(resource_id), match)"""
        }
    }

    match_objective_id = {
        'python': {
            'json': """
    def ${method_name}(self, objective_id):
        ${doc_string}
        if not isinstance(objective_id, Id):
            raise errors.InvalidArgument()
        self._add_match('objectiveId', str(objective_id), match)"""
        }
    }


class Proficiency:
    additional_methods = {
        'python': {
            'json': """
    def get_object_map(self):
        obj_map = dict(self._my_map)
        if obj_map['startDate'] is not None:
            actual_start_date = obj_map['startDate']
            obj_map['startDate'] = dict()
            obj_map['startDate']['year'] = actual_start_date.year
            obj_map['startDate']['month'] = actual_start_date.month
            obj_map['startDate']['day'] = actual_start_date.day
            obj_map['startDate']['hour'] = actual_start_date.hour
            obj_map['startDate']['minute'] = actual_start_date.minute
            obj_map['startDate']['second'] = actual_start_date.second
            obj_map['startDate']['microsecond'] = actual_start_date.microsecond
        if obj_map['endDate'] is not None:
            actual_end_date = obj_map['endDate']
            obj_map['endDate'] = dict()
            obj_map['endDate']['year'] = actual_end_date.year
            obj_map['endDate']['month'] = actual_end_date.month
            obj_map['endDate']['day'] = actual_end_date.day
            obj_map['endDate']['hour'] = actual_end_date.hour
            obj_map['endDate']['minute'] = actual_end_date.minute
            obj_map['endDate']['second'] = actual_end_date.second
            obj_map['endDate']['microsecond'] = actual_end_date.microsecond

        return osid_objects.OsidObject.get_object_map(self, obj_map)

    object_map = property(fget=get_object_map)"""
        }
    }
