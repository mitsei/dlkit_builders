class GenericContainableObjectLookupSession(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'ACTIVE = 0',
                'ANY_STATUS = 1',
                'SEQUESTERED = 0',
                'UNSEQUESTERED = 1',
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    # From: templates/osid_session.py::GenericContainableObjectLookupSession::init_template
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.${cat_name}
        self._catalog_name = '${cat_name}'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='${pkg_name_replaced}',
            cat_name='${cat_name}',
            cat_class=objects.${cat_name})
        self._kwargs = kwargs
        self._status_view = ACTIVE
        self._sequestered_view = SEQUESTERED

    def _view_filter(self):
        \"\"\"
        Overrides OsidSession._view_filter to add sequestering filter.

        \"\"\"
        view_filter = OsidSession._view_filter(self)
        if self._sequestered_view == SEQUESTERED:
            view_filter['sequestered'] = False
        return view_filter"""
        }
    }

    use_active_containable_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericContainableObjectLookupSession::use_active_containable_view_template
        self._status_view = ACTIVE"""
        }
    }

    use_any_status_containable_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericContainableObjectLookupSession::use_any_status_containable_view_template
        self._status_view = ANY_STATUS"""
        }
    }

    use_sequestered_containable_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericContainableObjectLookupSession::use_sequestered_containable_view_template
        self._sequestered_view = SEQUESTERED"""
        }
    }

    use_unsequestered_containable_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericContainableObjectLookupSession::use_unsequestered_containable_view_template
        self._sequestered_view = UNSEQUESTERED"""
        }
    }


class GenericContainableObjectQuerySession(object):
    import_statements_pattern = GenericContainableObjectLookupSession.import_statements_pattern

    init_template = GenericContainableObjectLookupSession.init_template


class GenericObjectLookupSession(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
                'from ..osid.sessions import OsidSession',
                'from ..utilities import JSONClientValidated',
                'from . import objects',
                'from bson.objectid import ObjectId',
                'DESCENDING = -1',
                'ASCENDING = 1',
                'CREATED = True',
                'UPDATED = True'
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    # From: templates/osid_session.py::GenericObjectLookupSession::init_template
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.${cat_name}
        self._catalog_name = '${cat_name}'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='${pkg_name_replaced}',
            cat_name='${cat_name}',
            cat_class=objects.${cat_name})
        self._kwargs = kwargs"""
        }
    }

    get_catalog_id_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::get_catalog_id_template
        return self._catalog_id"""
        }
    }

    get_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::get_catalog_template
        return self._catalog"""
        }
    }

    can_lookup_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::can_lookup_objects_template
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
        }
    }

    use_comparative_object_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::use_comparative_object_view_template
        self._use_comparative_object_view()"""
        }
    }

    use_plenary_object_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::use_plenary_object_view_template
        self._use_plenary_object_view()"""
        }
    }

    use_federated_catalog_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::use_federated_catalog_view_template
        self._use_federated_catalog_view()"""
        }
    }

    use_isolated_catalog_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::use_isolated_catalog_view_template
        self._use_isolated_catalog_view()"""
        }
    }

    get_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::get_object_template
        # NOTE: This implementation currently ignores plenary view
        collection = JSONClientValidated('${package_name_replace}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        result = collection.find_one(
            dict({'_id': ObjectId(self._get_id(${arg0_name}, '${package_name_replace}').get_identifier())},
                 **self._view_filter()))
        return objects.${return_type}(osid_object_map=result, runtime=self._runtime, proxy=self._proxy)"""
        }
    }

    get_objects_by_ids_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::get_objects_by_ids_template
        # NOTE: This implementation currently ignores plenary view
        collection = JSONClientValidated('${package_name_replace}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        object_id_list = []
        for i in ${arg0_name}:
            object_id_list.append(ObjectId(self._get_id(i, '${package_name_replace}').get_identifier()))
        result = collection.find(
            dict({'_id': {'$$in': object_id_list}},
                 **self._view_filter()))
        result = list(result)
        sorted_result = []
        for object_id in object_id_list:
            for object_map in result:
                if object_map['_id'] == object_id:
                    sorted_result.append(object_map)
                    break
        return objects.${return_type}(sorted_result, runtime=self._runtime, proxy=self._proxy)"""
        }
    }

    get_objects_by_genus_type_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::get_objects_by_genus_type_template
        # NOTE: This implementation currently ignores plenary view
        collection = JSONClientValidated('${package_name_replace}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        result = collection.find(
            dict({'genusTypeId': str(${arg0_name})},
                 **self._view_filter())).sort('_id', DESCENDING)
        return objects.${return_type}(result, runtime=self._runtime, proxy=self._proxy)"""
        }
    }

    get_objects_by_parent_genus_type_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::get_objects_by_parent_genus_type_template
        # STILL NEED TO IMPLEMENT!!!
        return objects.${return_type}([])"""
        }
    }

    get_objects_by_record_type_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::get_objects_by_record_type_template
        # STILL NEED TO IMPLEMENT!!!
        return objects.${return_type}([])"""
        }
    }

    get_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::get_objects_template
        # NOTE: This implementation currently ignores plenary view
        collection = JSONClientValidated('${package_name_replace}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        result = collection.find(self._view_filter()).sort('_id', DESCENDING)
        return objects.${return_type}(result, runtime=self._runtime, proxy=self._proxy)"""
        }
    }

    get_subjugated_objects_for_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::get_subjugated_objects_for_object_template
        # NOTE: This implementation currently ignores plenary view
        collection = JSONClientValidated('${package_name_replace}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        result = collection.find(
            dict({'${arg0_object_mixed}Id': str(${arg0_name})},
                 **self._view_filter()))
        return objects.${return_type}(result, runtime=self._runtime)"""
        }
    }

    get_subjugated_objects_for_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::get_subjugated_objects_for_objects_template
        # NOTE: This implementation currently ignores plenary view
        collection = JSONClientValidated('${package_name_replace}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        id_str_list = [str(id_) for id_ in ${arg0_name}]
        result = collection.find(
            dict({'${arg0_object_mixed}Id': {$$in: id_str_list}},
                 **self._view_filter()))
        return objects.${return_type}(result, runtime=self._runtime)"""
        }
    }


class GenericObjectAdminSession(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..osid.sessions import OsidSession',
                'from ..primitives import Id',
                'from ..primitives import Type',
                'from ..utilities import JSONClientValidated',
                'from . import objects',
                'from bson.objectid import ObjectId',
                """ENCLOSURE_RECORD_TYPE = Type(
    identifier=\'enclosure\',
    namespace=\'osid-object\',
    authority=\'ODL.MIT.EDU\')""",
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    # From: templates/osid_session.py::GenericObjectAdminSession::init_template
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.${cat_name}
        self._catalog_name = '${cat_name}'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='${pkg_name_replaced}',
            cat_name='${cat_name}',
            cat_class=objects.${cat_name})
        self._forms = dict()
        self._kwargs = kwargs"""
        }
    }


class GenericObjectNotificationSession(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..osid.sessions import OsidSession',
                'from ..utilities import JSONClientValidated',
                'from .. import MONGO_LISTENER'
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    # From: templates/osid_session.py::GenericObjectNotificationSession::init_template
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.${cat_name}
        self._catalog_name = '${cat_name}'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='${pkg_name_replaced}',
            cat_name='${cat_name}',
            cat_class=objects.${cat_name})

        if not MONGO_LISTENER.is_alive():
            MONGO_LISTENER.initialize(runtime)
            MONGO_LISTENER.start()

        self._receiver = kwargs['receiver']
        db_prefix = ''
        try:
            db_prefix_param_id = Id('parameter:mongoDBNamePrefix@mongo')
            db_prefix = runtime.get_configuration().get_value_by_parameter(db_prefix_param_id).get_string_value()
        except (AttributeError, KeyError, errors.NotFound):
            pass
        self._ns = '{0}${pkg_name_replaced}.${object_name}'.format(db_prefix)

        if self._ns not in MONGO_LISTENER.receivers:
            MONGO_LISTENER.receivers[self._ns] = dict()
        MONGO_LISTENER.receivers[self._ns][self._receiver] = {
            'authority': self._authority,
            'obj_name_plural': '${object_name_under_plural}',
            'i': False,
            'u': False,
            'd': False,
            'reliable': False,
        }

    def __del__(self):
        \"\"\"Make sure the receiver is removed from the listener\"\"\"
        del MONGO_LISTENER.receivers[self._ns][self._receiver]
        super(${interface_name}, self).__del__()"""
        }
    }


class GenericRelationshipLookupSession(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
                'from ..primitives import DateTime',
                'from ..osid.sessions import OsidSession',
                'from ..utilities import JSONClientValidated',
                'from ..utilities import overlap',
                'from . import objects',
                'from bson.objectid import ObjectId',
                'DESCENDING = -1',
                'ASCENDING = 1',
                'CREATED = True',
                'UPDATED = True'
            ]
        }
    }

    init_template = GenericObjectLookupSession.init_template

    use_effective_relationship_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericRelationshipLookupSession::use_effective_relationship_view_template
        self._use_effective_view()"""
        }
    }

    use_any_effective_relationship_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericRelationshipLookupSession::use_any_effective_relationship_view_template
        self._use_any_effective_view()"""
        }
    }

    get_relationships_on_date_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericRelationshipLookupSession::get_relationships_on_date_template
        ${object_name_under}_list = []
        for ${object_name_under} in self.get_${object_name_plural_under}():
            if overlap(${arg0_name}, ${arg1_name}, ${object_name_under}.start_date, ${object_name_under}.end_date):
                ${object_name_under}_list.append(${object_name_under})
        return objects.${object_name}List(${object_name_under}_list, runtime=self._runtime)"""
        }
    }

    get_relationships_for_source_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericRelationshipLookupSession::get_relationships_for_source_template
        # NOTE: This implementation currently ignores plenary and effective views
        collection = JSONClientValidated('${package_name}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        result = collection.find(
            dict({'${source_name_mixed}Id': str(${arg0_name})},
                 **self._view_filter())).sort('_sort_id', ASCENDING)
        return objects.${object_name}List(result, runtime=self._runtime)"""
        }
    }

    get_relationships_for_source_on_date_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}, ${arg2_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericRelationshipLookupSession::get_relationships_for_source_on_date_template
        ${object_name_under}_list = []
        for ${object_name_under} in self.get_${object_name_plural_under}_for_${source_name}(${arg0_name}):
            if overlap(${arg1_name}, ${arg2_name}, ${object_name_under}.start_date, ${object_name_under}.end_date):
                ${object_name_under}_list.append(${object_name_under})
        return objects.${object_name}List(${object_name_under}_list, runtime=self._runtime)"""
        }
    }

    get_relationships_by_genus_type_for_source_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericRelationshipLookupSession::get_relationships_by_genus_type_for_source_template
        # NOTE: This implementation currently ignores plenary and effective views
        collection = JSONClientValidated('${package_name}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        result = collection.find(
            dict({'${source_name_mixed}Id': str(${arg0_name}),
                  'genusTypeId': str(${arg1_name})},
                 **self._view_filter())).sort('_sort_id', ASCENDING)
        return objects.${object_name}List(result, runtime=self._runtime)"""
        }
    }

    get_relationships_by_genus_type_for_source_on_date_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}, ${arg2_name}, ${arg3_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericRelationshipLookupSession::get_relationships_by_genus_type_for_source_on_date_template
        ${object_name_under}_list = []
        for ${object_name_under} in self.get_${object_name_plural_under}_by_genus_type_for_${source_name}():
            if overlap(${arg2_name}, ${arg3_name}, ${object_name_under}.start_date, ${object_name_under}.end_date):
                ${object_name_under}_list.append(${object_name_under})
        return objects.${object_name}List(${object_name_under}_list, runtime=self._runtime)"""
        }
    }

    get_relationships_for_destination_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericRelationshipLookupSession::get_relationships_for_destination_template
        # NOTE: This implementation currently ignores plenary and effective views
        collection = JSONClientValidated('${package_name}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        result = collection.find(
            dict({'${destination_name_mixed}Id': str(${arg0_name})},
                 **self._view_filter())).sort('_sort_id', ASCENDING)
        return objects.${object_name}List(result, runtime=self._runtime)"""
        }
    }

    get_relationships_for_destination_on_date_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}, ${arg2_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericRelationshipLookupSession::get_relationships_for_destination_on_date_template
        ${object_name_under}_list = []
        for ${object_name_under} in self.get_${object_name_plural_under}_for_${destination_name}():
            if overlap(${arg1_name}, ${arg2_name}, ${object_name_under}.start_date, ${object_name_under}.end_date):
                ${object_name_under}_list.append(${object_name_under})
        return objects.${object_name}List(${object_name_under}_list, runtime=self._runtime)"""
        }
    }

    get_relationships_by_genus_type_for_destination_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericRelationshipLookupSession::get_relationships_by_genus_type_for_destination_template
        # NOTE: This implementation currently ignores plenary and effective views
        collection = JSONClientValidated('${package_name}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        result = collection.find(
            dict({'${destination_name_mixed}Id': str(${arg0_name}),
                  'genusTypeId': str(${arg1_name})},
                 **self._view_filter())).sort('_sort_id', ASCENDING)
        return objects.${object_name}List(result, runtime=self._runtime)"""
        }
    }

    get_relationships_by_genus_type_for_destination_on_date_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}, ${arg2_name}, ${arg3_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericRelationshipLookupSession::get_relationships_by_genus_type_for_destination_on_date_template
        ${object_name_under}_list = []
        for ${object_name_under} in self.get_${object_name_plural_under}_by_genus_type_for_${destination_name}():
            if overlap(${arg2_name}, ${arg3_name}, ${object_name_under}.start_date, ${object_name_under}.end_date):
                ${object_name_under}_list.append(${object_name_under})
        return objects.${object_name}List(${object_name_under}_list, runtime=self._runtime)"""
        }
    }

    get_relationships_for_peers_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericRelationshipLookupSession::get_relationships_for_peers_template
        # NOTE: This implementation currently ignores plenary and effective views
        collection = JSONClientValidated('${package_name}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        result = collection.find(
            dict({'${source_name_mixed}Id': str(${arg0_name}),
                  '${destination_name_mixed}Id': str(${arg1_name})},
                 **self._view_filter())).sort('_sort_id', ASCENDING)
        return objects.${object_name}List(result, runtime=self._runtime)"""
        }
    }

    get_relationships_by_genus_type_for_peers_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}, ${arg2_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericRelationshipLookupSession::get_relationships_by_genus_type_for_peers_template
        # NOTE: This implementation currently ignores plenary and effective views
        collection = JSONClientValidated('${package_name}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        result = collection.find(
            dict({'${source_name_mixed}Id': str(${arg0_name}),
                  '${destination_name_mixed}Id': str(${arg1_name}),
                  'genusTypeId': str(${arg2_name})},
                 **self._view_filter())).sort('_sort_id', ASCENDING)
        return objects.${object_name}List(result, runtime=self._runtime)"""
        }
    }


class GenericObjectCatalogSession(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from ..id.objects import IdList',
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    # From: templates/osid_session.py::GenericObjectCatalogSession::init_template
    _session_namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession._init_catalog(self, proxy, runtime)
        self._catalog_view = COMPARATIVE
        self._kwargs = kwargs"""
        }
    }


class GenericObjectCatalogAssignmentSession(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from ..id.objects import IdList',
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    # From: templates/osid_session.py::GenericObjectCatalogAssignmentSession::init_template
    _session_namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession._init_catalog(self, proxy, runtime)
        self._catalog_name = '${cat_name}'
        self._forms = dict()
        self._kwargs = kwargs"""
        }
    }


class GenericObjectQuerySession(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..osid.sessions import OsidSession',
                'from ..utilities import JSONClientValidated',
                'from . import queries',
                'DESCENDING = -1',
                'ASCENDING = 1'
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    # From: templates/osid_session.py::GenericObjectQuerySession::init_template
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.${cat_name}
        self._catalog_name = '${cat_name}'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='${pkg_name_replaced}',
            cat_name='${cat_name}',
            cat_class=objects.${cat_name})
        self._kwargs = kwargs"""
        }
    }


class GenericRelationshipQuerySession(object):
    import_statements_pattern = GenericObjectQuerySession.import_statements_pattern

    init_template = GenericObjectQuerySession.init_template


class GenericCatalogLookupSession(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
                'from ..osid.sessions import OsidSession',
                'from . import objects',
                'from ..utilities import JSONClientValidated',
                'from ..utilities import PHANTOM_ROOT_IDENTIFIER',
                'from bson.objectid import ObjectId',
                'DESCENDING = -1',
                'ASCENDING = 1',
                'COMPARATIVE = 0',
                'PLENARY = 1'
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    # From: templates/osid_session.py::GenericCatalogLookupSession::init_template
    _session_namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        OsidSession._init_catalog(self, proxy, runtime)
        if self._cataloging_manager is not None:
            self._catalog_session = self._cataloging_manager.get_catalog_lookup_session()
            self._catalog_session.use_comparative_catalog_view()
        self._catalog_view = COMPARATIVE
        self._kwargs = kwargs"""
        }
    }

    use_comparative_catalog_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::use_comparative_catalog_view_template
        self._catalog_view = COMPARATIVE
        if self._catalog_session is not None:
            self._catalog_session.use_comparative_catalog_view()"""
        }
    }

    use_plenary_catalog_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::use_plenary_catalog_view_template
        self._catalog_view = PLENARY
        if self._catalog_session is not None:
            self._catalog_session.use_plenary_catalog_view()"""
        }
    }

    get_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::get_catalog_template
        if self._catalog_session is not None:
            return self._catalog_session.get_catalog(catalog_id=${arg0_name})
        collection = JSONClientValidated('${package_name}',
                                         collection='${cat_name}',
                                         runtime=self._runtime)
        # Need to consider how to best deal with the "phantom root" catalog issue
        if ${arg0_name}.get_identifier() == PHANTOM_ROOT_IDENTIFIER:
            return self._get_phantom_root_catalog(cat_class=objects.${cat_name}, cat_name='${cat_name}')
        try:
            result = collection.find_one({'_id': ObjectId(self._get_id(${arg0_name},
                                                                       '${package_name_replace}').get_identifier())})
        except errors.NotFound:
            # Try creating an orchestrated ${cat_name}.  Let it raise errors.NotFound()
            result = self._create_orchestrated_cat(${arg0_name}, '${package_name}', '${cat_name}')

        return objects.${return_type}(osid_object_map=result, runtime=self._runtime, proxy=self._proxy)"""
        }
    }

    get_catalogs_by_ids_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::get_catalogs_by_ids_template
        # NOTE: This implementation currently ignores plenary view
        # Also, this should be implemented to use get_${cat_name}() instead of direct to database
        if self._catalog_session is not None:
            return self._catalog_session.get_catalogs_by_ids(catalog_ids=${arg0_name})
        catalog_id_list = []
        for i in ${arg0_name}:
            catalog_id_list.append(ObjectId(i.get_identifier()))
        collection = JSONClientValidated('${package_name}',
                                         collection='${cat_name}',
                                         runtime=self._runtime)
        result = collection.find({'_id': {'$$in': catalog_id_list}}).sort('_id', DESCENDING)

        return objects.${return_type}(result, runtime=self._runtime, proxy=self._proxy)"""
        }
    }

    get_catalogs_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::get_catalogs_template
        # NOTE: This implementation currently ignores plenary view
        if self._catalog_session is not None:
            return self._catalog_session.get_catalogs()
        collection = JSONClientValidated('${package_name}',
                                         collection='${cat_name}',
                                         runtime=self._runtime)
        result = collection.find().sort('_id', DESCENDING)

        return objects.${return_type}(result, runtime=self._runtime, proxy=self._proxy)"""
        }
    }

    get_catalogs_by_genus_type_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::get_catalogs_by_genus_type_template
        # NOTE: This implementation currently ignores plenary view
        if self._catalog_session is not None:
            return self._catalog_session.get_catalogs_by_genus_type(catalog_genus_type=${arg0_name})
        collection = JSONClientValidated('${package_name}',
                                         collection='${cat_name}',
                                         runtime=self._runtime)
        result = collection.find({"genusTypeId": str(${arg0_name})}).sort('_id', DESCENDING)

        return objects.${return_type}(result, runtime=self._runtime, proxy=self._proxy)"""
        }
    }

    can_lookup_catalogs_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogLookupSession::can_lookup_catalogs_template
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        if self._catalog_session is not None:
            return self._catalog_session.can_lookup_catalogs()
        return True"""
        }
    }


class GenericCatalogQuerySession(object):
    import_statements_pattern = {
        'python': {
            'json': [
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    # From: templates/osid_session.py::GenericCatalogQuerySession::init_template
    _session_namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        OsidSession._init_catalog(self, proxy, runtime)
        if self._cataloging_manager is not None:
            self._catalog_session = self._cataloging_manager.get_catalog_query_session()
        self._forms = dict()
        self._kwargs = kwargs"""
        }
    }

    can_query_catalogs_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogQuerySession::can_query_catalogs_template
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
        }
    }

    can_search_catalogs_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogQuerySession::can_search_catalogs_template
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
        }
    }

    get_catalog_query_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogQuerySession::get_catalog_query_template
        return queries.${return_type}(runtime=self._runtime)"""
        }
    }

    get_catalogs_by_query_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogQuerySession::get_catalogs_by_query_template
        if self._catalog_session is not None:
            return self._catalog_session.get_catalogs_by_query(${arg0_name})
        query_terms = dict(${arg0_name}._query_terms)
        collection = JSONClientValidated('${package_name}',
                                         collection='${cat_name}',
                                         runtime=self._runtime)
        result = collection.find(query_terms).sort('_id', DESCENDING)

        return objects.${return_type}(result, runtime=self._runtime)"""
        }
    }


class GenericCatalogAdminSession(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
                'from ..osid.sessions import OsidSession',
                'from ..utilities import JSONClientValidated',
                'from . import objects',
                'from bson.objectid import ObjectId',
                'CREATED = True',
                'UPDATED = True'
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    # From: templates/osid_session.py::GenericCatalogAdminSession::init_template
    _session_namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        OsidSession._init_catalog(self, proxy, runtime)
        if self._cataloging_manager is not None:
            self._catalog_session = self._cataloging_manager.get_catalog_admin_session()
        self._forms = dict()
        self._kwargs = kwargs"""
        }
    }

    can_create_catalogs_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::can_create_catalogs_template
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        if self._catalog_session is not None:
            return self._catalog_session.can_create_catalogs()
        return True"""
        }
    }

    can_create_catalog_with_record_types_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::can_create_catalog_with_record_types_template
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        if self._catalog_session is not None:
            return self._catalog_session.can_create_catalog_with_record_types(catalog_record_types=${arg0_name})
        return True"""
        }
    }

    get_catalog_form_for_create_import_templates = {
        'python': {
            'json': [
                'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
            ]
        }
    }

    get_catalog_form_for_create_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::get_catalog_form_for_create_template
        if self._catalog_session is not None:
            return self._catalog_session.get_catalog_form_for_create(catalog_record_types=${arg0_name})
        for arg in ${arg0_name}:
            if not isinstance(arg, ABC${arg0_type}):
                raise errors.InvalidArgument('one or more argument array elements is not a valid OSID ${arg0_type}')
        if ${arg0_name} == []:
            result = objects.${return_type}(
                runtime=self._runtime,
                effective_agent_id=self.get_effective_agent_id(),
                proxy=self._proxy)  # Probably don't need effective agent id now that we have proxy in form.
        else:
            result = objects.${return_type}(
                record_types=${arg0_name},
                runtime=self._runtime,
                effective_agent_id=self.get_effective_agent_id(),
                proxy=self._proxy)  # Probably don't need effective agent id now that we have proxy in form.
        self._forms[result.get_id().get_identifier()] = not CREATED
        return result"""
        }
    }

    create_catalog_import_templates = {
        'python': {
            'json': [
                'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
            ]
        }
    }

    create_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::get_catalog_form_for_create_template
        if self._catalog_session is not None:
            return self._catalog_session.create_catalog(catalog_form=${arg0_name})
        collection = JSONClientValidated('${package_name}',
                                         collection='${cat_name}',
                                         runtime=self._runtime)
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('argument type is not an ${arg0_type}')
        if ${arg0_name}.is_for_update():
            raise errors.InvalidArgument('the ${arg0_type} is for update only, not create')
        try:
            if self._forms[${arg0_name}.get_id().get_identifier()] == CREATED:
                raise errors.IllegalState('${arg0_name} already used in a create transaction')
        except KeyError:
            raise errors.Unsupported('${arg0_name} did not originate from this session')
        if not ${arg0_name}.is_valid():
            raise errors.InvalidArgument('one or more of the form elements is invalid')
        insert_result = collection.insert_one(${arg0_name}._my_map)

        self._forms[${arg0_name}.get_id().get_identifier()] = CREATED
        result = objects.${return_type}(
            osid_object_map=collection.find_one({'_id': insert_result.inserted_id}),
            runtime=self._runtime,
            proxy=self._proxy)

        return result"""
        }
    }

    get_catalog_form_for_update_import_templates = {
        'python': {
            'json': [
                'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
            ]
        }
    }

    get_catalog_form_for_update_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::get_catalog_form_for_update_template
        if self._catalog_session is not None:
            return self._catalog_session.get_catalog_form_for_update(catalog_id=${arg0_name})
        collection = JSONClientValidated('${package_name}',
                                         collection='${cat_name}',
                                         runtime=self._runtime)
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        result = collection.find_one({'_id': ObjectId(${arg0_name}.get_identifier())})

        cat_form = objects.${return_type}(osid_object_map=result, runtime=self._runtime, proxy=self._proxy)
        self._forms[cat_form.get_id().get_identifier()] = not UPDATED

        return cat_form"""
        }
    }

    can_update_catalogs_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::can_update_catalogs_template
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        if self._catalog_session is not None:
            return self._catalog_session.can_update_catalogs()
        return True"""
        }
    }

    update_catalog_import_templates = {
        'python': {
            'json': [
                'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
            ]
        }
    }

    update_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::update_catalog_template
        if self._catalog_session is not None:
            return self._catalog_session.update_catalog(catalog_form=${arg0_name})
        collection = JSONClientValidated('${package_name}',
                                         collection='${cat_name}',
                                         runtime=self._runtime)
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('argument type is not an ${arg0_type}')
        if not ${arg0_name}.is_for_update():
            raise errors.InvalidArgument('the ${arg0_type} is for update only, not create')
        try:
            if self._forms[${arg0_name}.get_id().get_identifier()] == UPDATED:
                raise errors.IllegalState('${arg0_name} already used in an update transaction')
        except KeyError:
            raise errors.Unsupported('${arg0_name} did not originate from this session')
        if not ${arg0_name}.is_valid():
            raise errors.InvalidArgument('one or more of the form elements is invalid')
        collection.save(${arg0_name}._my_map)  # save is deprecated - change to replace_one

        self._forms[${arg0_name}.get_id().get_identifier()] = UPDATED

        # Note: this is out of spec. The OSIDs don't require an object to be returned
        return objects.${return_type}(osid_object_map=${arg0_name}._my_map, runtime=self._runtime, proxy=self._proxy)"""
        }
    }

    can_delete_catalogs_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::can_delete_catalogs_template
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        if self._catalog_session is not None:
            return self._catalog_session.can_delete_catalogs()
        return True"""
        }
    }

    delete_catalog_import_templates = {
        'python': {
            'json': [
                'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
            ]
        }
    }

    delete_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::delete_catalog_template
        # Implemented from template for
        # osid.resource.BinAdminSession.delete_bin_template
        if self._catalog_session is not None:
            return self._catalog_session.delete_catalog(catalog_id=${arg0_name})
        collection = JSONClientValidated('${package_name}',
                                         collection='${cat_name}',
                                         runtime=self._runtime)
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        for object_catalog in ${cataloged_object_caps_list}:
            obj_collection = JSONClientValidated('${package_name}',
                                                 collection=object_catalog,
                                                 runtime=self._runtime)
            if obj_collection.find({'assigned${cat_name}Ids': {'$$in': [str(${arg0_name})]}}).count() != 0:
                raise errors.IllegalState('catalog is not empty')
        collection.delete_one({'_id': ObjectId(${arg0_name}.get_identifier())})"""
        }
    }

    alias_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, alias_id):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::alias_catalog_template
        if self._catalog_session is not None:
            return self._catalog_session.alias_catalog(catalog_id=${arg0_name}, alias_id=alias_id)
        self._alias_id(primary_id=${arg0_name}, equivalent_id=alias_id)"""
        }
    }


class GenericCatalogNotificationSession(object):

    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..osid.sessions import OsidSession',
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    # From: templates/osid_session.py::GenericCatalogNotificationSession::init_template
    _session_namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        OsidSession._init_catalog(self, proxy, runtime)
        self._kwargs = kwargs"""
        }
    }


class GenericCatalogHierarchySession(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
                'from ..osid.sessions import OsidSession',
                'from . import objects',
                'COMPARATIVE = 0',
                'PLENARY = 1',
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    # From: templates/osid_session.py::GenericCatalogHierarchySession::init_template
    _session_namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        # Implemented from template for
        # osid.resource.BinHierarchySession.init_template
        OsidSession.__init__(self)
        OsidSession._init_catalog(self, proxy, runtime)
        self._forms = dict()
        self._kwargs = kwargs
        if self._cataloging_manager is not None:
            self._catalog_session = self._cataloging_manager.get_catalog_hierarchy_session()
        else:
            hierarchy_mgr = self._get_provider_manager('HIERARCHY')
            self._hierarchy_session = hierarchy_mgr.get_hierarchy_traversal_session_for_hierarchy(
                Id(authority='${pkg_name_upper}',
                   namespace='CATALOG',
                   identifier='${cat_name_upper}'),
                proxy=self._proxy)"""
        }
    }

    can_access_catalog_hierarchy_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::can_access_catalog_hierarchy_template
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        if self._catalog_session is not None:
            return self._catalog_session.can_access_catalog_hierarchy()
        return True"""
        }
    }

    get_catalog_hierarchy_id_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::get_catalog_hierarchy_id_template
        if self._catalog_session is not None:
            return self._catalog_session.get_catalog_hierarchy_id()
        return self._hierarchy_session.get_hierarchy_id()"""
        }
    }

    get_catalog_hierarchy_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::get_catalog_hierarchy_template
        if self._catalog_session is not None:
            return self._catalog_session.get_catalog_hierarchy()
        return self._hierarchy_session.get_hierarchy()"""
        }
    }

    get_root_catalog_ids_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::get_root_catalog_ids_template
        if self._catalog_session is not None:
            return self._catalog_session.get_root_catalog_ids()
        return self._hierarchy_session.get_roots()"""
        }
    }

    get_root_catalogs_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::get_root_catalogs_template
        if self._catalog_session is not None:
            return self._catalog_session.get_root_catalogs()
        return ${cat_name}LookupSession(
            self._proxy,
            self._runtime).get_${cat_name_plural_under}_by_ids(list(self.get_root_${cat_name_under}_ids()))"""
        }
    }

    has_parent_catalogs_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::has_parent_catalogs_template
        if self._catalog_session is not None:
            return self._catalog_session.has_parent_catalogs(catalog_id=${arg0_name})
        return self._hierarchy_session.has_parents(id_=${arg0_name})"""
        }
    }

    is_parent_of_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::is_parent_of_catalog_template
        if self._catalog_session is not None:
            return self._catalog_session.is_parent_of_catalog(id_=${arg0_name}, catalog_id=${arg1_name})
        return self._hierarchy_session.is_parent(id_=${arg1_name}, parent_id=${arg0_name})"""
        }
    }

    get_parent_catalog_ids_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::get_parent_catalog_ids_template
        if self._catalog_session is not None:
            return self._catalog_session.get_parent_catalog_ids(catalog_id=${arg0_name})
        return self._hierarchy_session.get_parents(id_=${arg0_name})"""
        }
    }

    get_parent_catalogs_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::get_parent_catalogs_template
        if self._catalog_session is not None:
            return self._catalog_session.get_parent_catalogs(catalog_id=${arg0_name})
        return ${cat_name}LookupSession(
            self._proxy,
            self._runtime).get_${cat_name_plural_under}_by_ids(
                list(self.get_parent_${cat_name_under}_ids(${arg0_name})))"""
        }
    }

    is_ancestor_of_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::is_ancestor_of_catalog_template
        if self._catalog_session is not None:
            return self._catalog_session.is_ancestor_of_catalog(id_=${arg0_name}, catalog_id=${arg1_name})
        return self._hierarchy_session.is_ancestor(id_=${arg0_name}, ancestor_id=${arg1_name})"""
        }
    }

    has_child_catalogs_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::has_child_catalogs_template
        if self._catalog_session is not None:
            return self._catalog_session.has_child_catalogs(catalog_id=${arg0_name})
        return self._hierarchy_session.has_children(id_=${arg0_name})"""
        }
    }

    is_child_of_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::is_child_of_catalog_template
        if self._catalog_session is not None:
            return self._catalog_session.is_child_of_catalog(id_=${arg0_name}, catalog_id=${arg1_name})
        return self._hierarchy_session.is_child(id_=${arg1_name}, child_id=${arg0_name})"""
        }
    }

    get_child_catalog_ids_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::get_child_catalog_ids_template
        if self._catalog_session is not None:
            return self._catalog_session.get_child_catalog_ids(catalog_id=${arg0_name})
        return self._hierarchy_session.get_children(id_=${arg0_name})"""
        }
    }

    get_child_catalogs_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::get_child_catalogs_template
        if self._catalog_session is not None:
            return self._catalog_session.get_child_catalogs(catalog_id=${arg0_name})
        return ${cat_name}LookupSession(
            self._proxy,
            self._runtime).get_${cat_name_plural_under}_by_ids(
                list(self.get_child_${cat_name_under}_ids(${arg0_name})))"""
        }
    }

    is_descendant_of_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::is_descendant_of_catalog_template
        if self._catalog_session is not None:
            return self._catalog_session.is_descendant_of_catalog(id_=${arg0_name}, catalog_id=${arg1_name})
        return self._hierarchy_session.is_descendant(id_=${arg0_name}, descendant_id=${arg1_name})"""
        }
    }

    get_catalog_node_ids_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}, ${arg2_name}, ${arg3_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::get_catalog_node_ids_template
        if self._catalog_session is not None:
            return self._catalog_session.get_catalog_node_ids(
                catalog_id=${arg0_name},
                ancestor_levels=${arg1_name},
                descendant_levels=${arg2_name},
                include_siblings=${arg3_name})
        return self._hierarchy_session.get_nodes(
            id_=${arg0_name},
            ancestor_levels=${arg1_name},
            descendant_levels=${arg2_name},
            include_siblings=${arg3_name})"""
        }
    }

    get_catalog_nodes_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}, ${arg2_name}, ${arg3_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::get_catalog_node_ids_template
        return objects.${return_type}(self.get_${cat_name_under}_node_ids(
            ${arg0_name}=${arg0_name},
            ${arg1_name}=${arg1_name},
            ${arg2_name}=${arg2_name},
            ${arg3_name}=${arg3_name})._my_map, runtime=self._runtime, proxy=self._proxy)"""
        }
    }


class GenericCatalogHierarchyDesignSession(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
                'from ..osid.sessions import OsidSession',
                'from . import objects',
                'COMPARATIVE = 0',
                'PLENARY = 1',
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    # From: templates/osid_session.py::GenericCatalogHierarchyDesignSession::init_template
    _session_namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        OsidSession._init_catalog(self, proxy, runtime)
        self._forms = dict()
        self._kwargs = kwargs
        if self._cataloging_manager is not None:
            self._catalog_session = self._cataloging_manager.get_catalog_hierarchy_design_session()
        else:
            hierarchy_mgr = self._get_provider_manager('HIERARCHY')
            self._hierarchy_session = hierarchy_mgr.get_hierarchy_design_session_for_hierarchy(
                Id(authority='${pkg_name_upper}',
                   namespace='CATALOG',
                   identifier='${cat_name_upper}'),
                proxy=self._proxy)"""
        }
    }

    can_modify_catalog_hierarchy_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::can_modify_catalog_hierarchy_template
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        if self._catalog_session is not None:
            return self._catalog_session.can_modify_catalog_hierarchy()
        return True"""
        }
    }

    add_root_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::add_root_catalog_template
        if self._catalog_session is not None:
            return self._catalog_session.add_root_catalog(catalog_id=${arg0_name})
        return self._hierarchy_session.add_root(id_=${arg0_name})"""
        }
    }

    remove_root_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::remove_root_catalog_template
        if self._catalog_session is not None:
            return self._catalog_session.remove_root_catalog(catalog_id=${arg0_name})
        return self._hierarchy_session.remove_root(id_=${arg0_name})"""
        }
    }

    add_child_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::add_child_catalog_template
        if self._catalog_session is not None:
            return self._catalog_session.add_child_catalog(catalog_id=${arg0_name}, child_id=${arg1_name})
        return self._hierarchy_session.add_child(id_=${arg0_name}, child_id=${arg1_name})"""
        }
    }

    remove_child_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::remove_child_catalog_template
        if self._catalog_session is not None:
            return self._catalog_session.remove_child_catalog(catalog_id=${arg0_name}, child_id=${arg1_name})
        return self._hierarchy_session.remove_child(id_=${arg0_name}, child_id=${arg1_name})"""
        }
    }

    remove_child_catalogs_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_session.py::GenericCatalogAdminSession::remove_child_catalogs_template
        if self._catalog_session is not None:
            return self._catalog_session.remove_child_catalogs(catalog_id=${arg0_name})
        return self._hierarchy_session.remove_children(id_=${arg0_name})"""
        }
    }


class GenericObjectContainableSession(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.primordium.id.primitives import Id'
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    # From: templates/osid_session.py::GenericObjectContainableSession::init_template
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.${cat_name}
        self._catalog_name = '${cat_name}'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='${pkg_name_replaced}',
            cat_name='${cat_name}',
            cat_class=objects.${cat_name})
        self._kwargs = kwargs"""
        }
    }


class GenericObjectContainableDesignSession(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from ..list_utilities import move_id_ahead, move_id_behind, order_ids',
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    # From: templates/osid_session.py::GenericObjectContainableDesignSession::init_template
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.${cat_name}
        self._catalog_name = '${cat_name}'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='${pkg_name_replaced}',
            cat_name='${cat_name}',
            cat_class=objects.${cat_name})
        self._kwargs = kwargs"""
        }
    }
