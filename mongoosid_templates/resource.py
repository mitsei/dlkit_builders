
class ResourceProfile:

    import_statements_pattern = [
        'from ..primitives import Type',
        'from ..type.objects import TypeList',
        'from . import sessions',
        'from dlkit.abstract_osid.osid import errors',
        'from . import profile',
		'from ..utilities import get_registry',
    ]

    supports_visible_federation_template = """
        # Implemented from template for
        # osid.resource.ResourceProfile.supports_visible_federation
        return '${method_name}' in profile.SUPPORTS"""

    supports_resource_lookup_template = """
        # Implemented from template for
        # osid.resource.ResourceProfile.supports_resource_lookup
        return '${method_name}' in profile.SUPPORTS"""

    get_resource_record_types_template = """
        # Implemented from template for
        # osid.resource.ResourceProfile.get_resource_record_types_template
        record_type_maps = get_registry('${object_name_upper}_RECORD_TYPES', self._runtime)
        record_types = []
        for record_type_map in record_type_maps:
            record_types.append(Type(**record_type_maps[record_type_map]))
        return TypeList(record_types)"""

    supports_resource_record_type_template = """
        # Implemented from template for
        # osid.resource.ResourceProfile.supports_resource_record_type_template
        record_type_maps = get_registry('${object_name_upper}_RECORD_TYPES', self._runtime)
        supports = False
        for record_type_map in record_type_maps:
            if (${arg0_name}.get_authority() == record_type_maps[record_type_map]['authority'] and
                    ${arg0_name}.get_identifier_namespace() == record_type_maps[record_type_map]['namespace'] and
                    ${arg0_name}.get_identifier() == record_type_maps[record_type_map]['identifier']):
                supports = True
        return supports"""

class ResourceManager:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
    #'from ..osid.osid_errors import Unimplemented',
    #'from ..osid.osid_errors import NullArgument',
    #'from ..osid.osid_errors import NotFound # pylint: disable=unused-import',
    #'from ..osid.osid_errors import OperationFailed # pylint: disable=unused-import',
    ]

    init_template = """
    def __init__(self):
        osid_managers.OsidManager.__init__(self)"""

    get_resource_lookup_session_template = """
        if not self.supports_${support_check}():
            raise errors.Unimplemented()
        # pylint: disable=no-member
        return ${return_module}.${return_type}(runtime=self._runtime)"""

    get_resource_lookup_session_for_bin_template = """
        if not self.supports_${support_check}():
            raise errors.Unimplemented()
        ##
        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        ##
        # pylint: disable=no-member
        return ${return_module}.${return_type}(${arg0_name}, runtime=self._runtime)"""
        
    get_resource_admin_session_template = get_resource_lookup_session_template

    get_resource_admin_session_for_bin_template = get_resource_lookup_session_for_bin_template

    get_resource_notification_session_template = """
        if not self.supports_${support_check}():
            raise errors.Unimplemented()
        # pylint: disable=no-member
        return ${return_module}.${return_type}(runtime=self._runtime, receiver=${arg0_name})"""

    get_resource_notification_session_for_bin_template = """
        if not self.supports_${support_check}():
            raise errors.Unimplemented()
        ##
        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        ##
        # pylint: disable=no-member
        return ${return_module}.${return_type}(${arg1_name}, runtime=self._runtime, receiver=${arg0_name})"""

class ResourceProxyManager:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
    #'from ..osid.osid_errors import Unimplemented',
    #'from ..osid.osid_errors import NullArgument',
    #'from ..osid.osid_errors import NotFound # pylint: disable=unused-import',
    #'from ..osid.osid_errors import OperationFailed # pylint: disable=unused-import',
    ]

    init_template = """
    def __init__(self):
        osid_managers.OsidProxyManager.__init__(self)"""

    get_resource_lookup_session_template = """
        if not self.supports_${support_check}():
            raise errors.Unimplemented()
        # pylint: disable=no-member
        return ${return_module}.${return_type}(proxy=proxy, runtime=self._runtime)"""

    get_resource_lookup_session_for_bin_template = """
        if not self.supports_${support_check}():
            raise errors.Unimplemented()
        ##
        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        ##
        # pylint: disable=no-member
        return ${return_module}.${return_type}(${arg0_name}, proxy, self._runtime)"""

    get_resource_admin_session_template = get_resource_lookup_session_template

    get_resource_admin_session_for_bin_template = get_resource_lookup_session_for_bin_template

    get_resource_notification_session_template = """
        if not self.supports_${support_check}():
            raise errors.Unimplemented()
        # pylint: disable=no-member
        return ${return_module}.${return_type}(proxy=proxy, runtime=self._runtime, receiver=${arg0_name})"""

    get_resource_notification_session_for_bin_template = """
        if not self.supports_${support_check}():
            raise errors.Unimplemented()
        ##
        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        ##
        # pylint: disable=no-member
        return ${return_module}.${return_type}(catalog_id=${arg1_name}, proxy=proxy, runtime=self._runtime, receiver=${arg0_name})"""


class ResourceLookupSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from ..osid.sessions import OsidSession',
        'from ..utilities import MongoClientValidated',
        'from . import objects',
        'from bson.objectid import ObjectId',
        'DESCENDING = -1',
        'ASCENDING = 1',
        'CREATED = True',
        'UPDATED = True'
    ]

    init_template = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.${cat_name}
        self._session_name = '${interface_name}'
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

    get_bin_id_template = """
        # Implemented from template for osid.resource.ResourceLookupSession.get_bin_id
        return self._catalog_id"""

    get_bin_template = """
        # Implemented from template for osid.resource.ResourceLookupSession.get_bin
        return self._catalog"""

    can_lookup_resources_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.can_lookup_resources
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    use_comparative_resource_view_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.use_comparative_resource_view
        self._use_comparative_object_view()"""

    use_plenary_resource_view_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.use_plenary_resource_view
        self._use_plenary_object_view()"""

    use_federated_bin_view_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.use_federated_bin_view
        self._use_federated_catalog_view()"""

    use_isolated_bin_view_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.use_isolated_bin_view
        self._use_isolated_catalog_view()"""

    get_resource_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.get_resource
        # NOTE: This implementation currently ignores plenary view
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${object_name}',
                                          runtime=self._runtime)
        result = collection.find_one(
            dict({'_id': ObjectId(self._get_id(${arg0_name}, '${package_name_replace}').get_identifier())},
                 **self._view_filter()))
        return objects.${return_type}(osid_object_map=result, runtime=self._runtime, proxy=self._proxy)"""

    get_resources_by_ids_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.get_resources_by_ids
        # NOTE: This implementation currently ignores plenary view
        collection = MongoClientValidated('${package_name_replace}',
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

    get_resources_by_genus_type_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.get_resources_by_genus_type
        # NOTE: This implementation currently ignores plenary view
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${object_name}',
                                          runtime=self._runtime)
        result = collection.find(
            dict({'genusTypeId': str(${arg0_name})},
                 **self._view_filter())).sort('_id', DESCENDING)
        return objects.${return_type}(result, runtime=self._runtime, proxy=self._proxy)"""

    get_resources_by_parent_genus_type_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.get_resources_by_parent_genus_type
        # STILL NEED TO IMPLEMENT!!!
        return objects.${return_type}([])"""

    get_resources_by_record_type_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.get_resources_by_record_type
        # STILL NEED TO IMPLEMENT!!!
        return objects.${return_type}([])"""

    get_resources_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.get_resources
        # NOTE: This implementation currently ignores plenary view
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${object_name}',
                                          runtime=self._runtime)
        result = collection.find(self._view_filter()).sort('_id', DESCENDING)
        return objects.${return_type}(result, runtime=self._runtime, proxy=self._proxy)"""

class ResourceQuerySession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..osid.sessions import OsidSession',
        'from ..utilities import MongoClientValidated',
        'from . import queries',
        'DESCENDING = -1',
        'ASCENDING = 1'
    ]

    init_template = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.${cat_name}
        self._session_name = '${interface_name}'
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

    can_query_resources_template = """
        # Implemented from template for
        # osid.resource.ResourceQuerySession.can_query_resources
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    can_search_resources_template = """
        # Implemented from template for
        # osid.resource.ResourceQuerySession.can_search_resources
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    get_resource_query_template = """
        # Implemented from template for
        # osid.resource.ResourceQuerySession.get_resource_query_template
        return queries.${return_type}(runtime=self._runtime)"""

    get_resources_by_query_template = """
        # Implemented from template for
        # osid.resource.ResourceQuerySession.get_resources_by_query
        and_list = list()
        or_list = list()
        for term in ${arg0_name}._query_terms:
            and_list.append({term: ${arg0_name}._query_terms[term]})
        for term in ${arg0_name}._keyword_terms:
            or_list.append({term: ${arg0_name}._keyword_terms[term]})
        if or_list:
            and_list.append({'$$or': or_list})
        view_filter = self._view_filter()
        if view_filter:
            and_list.append(view_filter)
        if and_list:
            query_terms = {'$$and': and_list}
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${object_name}',
                                          runtime=self._runtime)
        result = collection.find(query_terms).sort('_id', DESCENDING)
        return objects.${return_type}(result, runtime=self._runtime, proxy=self._proxy)"""


class ResourceSearchSession:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..osid.sessions import OsidSession',
        'from ..utilities import MongoClientValidated',
        'from . import queries',
        'from . import searches',
        'from bson.objectid import ObjectId',
        'DESCENDING = -1',
        'ASCENDING = 1'
    ]

    init_template = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.${cat_name}
        self._session_name = '${interface_name}'
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

    get_resource_search_template = """
        # Implemented from template for
        # osid.resource.ResourceSearchSession.get_resource_search_template
        return searches.${return_type}(runtime=self._runtime)"""

    get_resources_by_search_template = """
        # Implemented from template for
        # osid.resource.ResourceSearchSession.get_resources_by_search_template
        # Copied from osid.resource.ResourceQuerySession.get_resources_by_query_template
        and_list = list()
        or_list = list()
        for term in ${arg0_name}._query_terms:
            and_list.append({term: ${arg0_name}._query_terms[term]})
        for term in ${arg0_name}._keyword_terms:
            or_list.append({term: ${arg0_name}._keyword_terms[term]})
        if ${arg1_name}._id_list is not None:
            identifiers = [ObjectId(i.identifier) for i in ${arg1_name}._id_list]
            and_list.append({'_id': {'$$in': identifiers}})
        if or_list:
            and_list.append({'$$or': or_list})
        view_filter = self._view_filter()
        if view_filter:
            and_list.append(view_filter)
        if and_list:
            query_terms = {'$$and': and_list}
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${object_name}',
                                          runtime=self._runtime)
        if ${arg1_name}.start is not None and ${arg1_name}.end is not None:
            result = collection.find(query_terms)[${arg1_name}.start:${arg1_name}.end]
        else:
            result = collection.find(query_terms)
        return searches.${return_type}(result, runtime=self._runtime)"""


class ResourceAdminSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..osid.sessions import OsidSession',
        'from ..primitives import Id',
        'from ..primitives import Type',
        'from ..utilities import MongoClientValidated',
        'from . import objects',
        'from bson.objectid import ObjectId',
        """ENCLOSURE_RECORD_TYPE = Type(
    identifier=\'enclosure\',
    namespace=\'osid-object\',
    authority=\'ODL.MIT.EDU\')""",
    ]

    init_template = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.${cat_name}
        self._session_name = '${interface_name}'
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

    can_create_resources_template = """
        # Implemented from template for
        # osid.resource.ResourceAdminSession.can_create_resources
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    can_create_resource_with_record_types_template = """
        # Implemented from template for
        # osid.resource.ResourceAdminSession.can_create_resource_with_record_types
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    get_resource_form_for_create_import_templates = [
        'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
    ]

    get_resource_form_for_create_template = """
        # Implemented from template for
        # osid.resource.ResourceAdminSession.get_resource_form_for_create_template
        for arg in ${arg0_name}:
            if not isinstance(arg, ABC${arg0_type}):
                raise errors.InvalidArgument('one or more argument array elements is not a valid OSID ${arg0_type}')
        if ${arg0_name} == []:
            obj_form = objects.${return_type}(
                ${cat_name_under}_id=self._catalog_id,
                runtime=self._runtime,
                effective_agent_id=self.get_effective_agent_id(),
                proxy=self._proxy)
        else:
            obj_form = objects.${return_type}(
                ${cat_name_under}_id=self._catalog_id,
                record_types=${arg0_name},
                runtime=self._runtime,
                effective_agent_id=self.get_effective_agent_id(),
                proxy=self._proxy)
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form"""

    create_resource_import_templates = [
        'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
    ]

    create_resource_template = """
        # Implemented from template for
        # osid.resource.ResourceAdminSession.create_resource_template
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${object_name}',
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

    get_resource_form_for_update_import_templates = [
        'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
    ]

    get_resource_form_for_update_template = """
        # Implemented from template for
        # osid.resource.ResourceAdminSession.get_resource_form_for_update_template
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${object_name}',
                                          runtime=self._runtime)
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        if ${arg0_name}.get_identifier_namespace() != '${package_name_replace}.${object_name}':
            if ${arg0_name}.get_authority() != self._authority:
                raise errors.InvalidArgument()
            else:
                ${arg0_name} = self._get_${object_name_under}_id_with_enclosure(${arg0_name})
        result = collection.find_one({'_id': ObjectId(${arg0_name}.get_identifier())})

        obj_form = objects.${return_type}(osid_object_map=result, runtime=self._runtime, proxy=self._proxy)
        self._forms[obj_form.get_id().get_identifier()] = not UPDATED

        return obj_form
    
    def _get_${object_name_under}_id_with_enclosure(self, enclosure_id):
        \"\"\"Create an ${object_name} with an enclosed foreign object.
        
        return: (osid.id.Id) - the id of the new ${object_name}
        
        \"\"\"
        mgr = self._get_provider_manager('REPOSITORY')
        query_session = mgr.get_${object_name_under}_query_session_for_${cat_name_under}(self._catalog_id, proxy=self._proxy)
        query_form = query_session.get_${object_name_under}_query()
        query_form.match_enclosed_object_id(enclosure_id)
        query_result = query_session.get_${object_name_plural_under}_by_query(query_form)
        if query_result.available() > 0:
            ${object_name_under}_id = query_result.next().get_id()
        else:
            create_form = self.get_${object_name_under}_form_for_create([ENCLOSURE_RECORD_TYPE])
            create_form.set_enclosed_object(enclosure_id)
            ${object_name_under}_id = self.create_${object_name_under}(create_form).get_id()
        return ${object_name_under}_id

    @utilities.arguments_not_none
    def duplicate_${object_name_under}(self, ${object_name_under}_id):
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${object_name}',
                                          runtime=self._runtime)
        mgr = self._get_provider_manager('${package_name_replace_upper}')
        lookup_session = mgr.get_${object_name_under}_lookup_session(proxy=self._proxy)
        lookup_session.use_federated_${cat_name_under}_view()
        try:
            lookup_session.use_unsequestered_${object_name_under}_view()
        except AttributeError:
            pass
        ${object_name_under}_map = dict(lookup_session.get_${object_name_under}(${object_name_under}_id)._my_map)
        del ${object_name_under}_map['_id']
        if '${cat_name_lower}Id' in ${object_name_under}_map:
            ${object_name_under}_map['${cat_name_lower}Id'] = str(self._catalog_id)
        if 'assigned${cat_name}Ids' in ${object_name_under}_map:
            ${object_name_under}_map['assigned${cat_name}Ids'] = [str(self._catalog_id)]
        insert_result = collection.insert_one(${object_name_under}_map)
        result = objects.${object_name}(
            osid_object_map=collection.find_one({'_id': insert_result.inserted_id}),
            runtime=self._runtime,
            proxy=self._proxy)
        return result"""

    update_resource_import_templates = [
        'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
    ]

    update_resource_template = """
        # Implemented from template for
        # osid.resource.ResourceAdminSession.update_resource_template
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${object_name}',
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
        collection.save(${arg0_name}._my_map)

        self._forms[${arg0_name}.get_id().get_identifier()] = UPDATED

        # Note: this is out of spec. The OSIDs don't require an object to be returned:
        return objects.${return_type}(
            osid_object_map=${arg0_name}._my_map,
            runtime=self._runtime,
            proxy=self._proxy)"""

    delete_resource_import_templates = [
        'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
    ]

    delete_resource_template = """
        # Implemented from template for
        # osid.resource.ResourceAdminSession.delete_resource_template
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${object_name}',
                                          runtime=self._runtime)
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        ${object_name_under}_map = collection.find_one(
            dict({'_id': ObjectId(${arg0_name}.get_identifier())},
                 **self._view_filter()))

        objects.${object_name}(osid_object_map=${object_name_under}_map, runtime=self._runtime, proxy=self._proxy)._delete()
        collection.delete_one({'_id': ObjectId(${arg0_name}.get_identifier())})"""

    can_manage_asset_aliases_template = """
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    alias_resource_template = """
        # Implemented from template for
        # osid.resource.ResourceAdminSession.alias_resources_template
        self._alias_id(primary_id=${arg0_name}, equivalent_id=${arg1_name})"""

class ResourceNotificationSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..osid.sessions import OsidSession',
        #'from ..primitives import Id',
        #'from ..primitives import Type',
        'from ..utilities import MongoClientValidated',
        #'from ..utilities import MongoListener',
        'from .. import MONGO_LISTENER'
        #'from . import objects',
    ]

    init_template = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.${cat_name}
        self._session_name = '${interface_name}'
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
        self._ns='{0}${pkg_name_replaced}.${object_name}'.format(db_prefix)

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

    reliable_resource_notifications_template = """
        # Implemented from template for
        # osid.resource.ResourceNotificationSession.reliable_resource_notifications
        MONGO_LISTENER.receivers[self._ns][self._receiver]['reliable'] = True"""

    unreliable_resource_notifications_template = """
        # Implemented from template for
        # osid.resource.ResourceNotificationSession.unreliable_resource_notifications
        MONGO_LISTENER.receivers[self._ns][self._receiver]['reliable'] = False"""

    acknowledge_notification_template = """
        # Implemented from template for
        # osid.resource.ResourceNotificationSession.acknowledge_notification
        try:
            del MONGO_LISTENER.notifications[notification_id]
        except KeyError:
            pass"""

    register_for_new_resources_template = """
        # Implemented from template for
        # osid.resource.ResourceNotificationSession.register_for_new_resources
        MONGO_LISTENER.receivers[self._ns][self._receiver]['i'] = True"""

    register_for_changed_resources_template = """
        # Implemented from template for
        # osid.resource.ResourceNotificationSession.register_for_changed_resources
        MONGO_LISTENER.receivers[self._ns][self._receiver]['u'] = True"""

    register_for_changed_resource_template = """
        # Implemented from template for
        # osid.resource.ResourceNotificationSession.register_for_changed_resource
        if MONGO_LISTENER.receivers[self._ns][self._receiver]['u'] == False:
            MONGO_LISTENER.receivers[self._ns][self._receiver]['u'] = []
        if isinstance(MONGO_LISTENER.receivers[self._ns][self._receiver]['u'], list):
            MONGO_LISTENER.receivers[self._ns][self._receiver]['u'].append(${arg0_name}.get_identifier())"""

    register_for_deleted_resources_template = """
        # Implemented from template for
        # osid.resource.ResourceNotificationSession.register_for_deleted_resources
        MONGO_LISTENER.receivers[self._ns][self._receiver]['d'] = True"""

    register_for_deleted_resource_template = """
        # Implemented from template for
        # osid.resource.ResourceNotificationSession.register_for_deleted_resource
        if MONGO_LISTENER.receivers[self._ns][self._receiver]['d'] == False:
            MONGO_LISTENER.receivers[self._ns][self._receiver]['d'] = []
        if isinstance(MONGO_LISTENER.receivers[self._ns][self._receiver]['d'], list):
            self.MONGO_LISTENER.receivers[self._ns][self._receiver]['d'].append(${arg0_name}.get_identifier())"""

class ResourceBinSession:

    import_statements_pattern = [
        'from ..id.objects import IdList',
    ]

    init_template = """
    _session_name = '${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession._init_catalog(self, proxy, runtime)
        self._catalog_view = COMPARATIVE
        self._kwargs = kwargs"""

    can_lookup_resource_bin_mappings_template = """
        # Implemented from template for
        # osid.resource.ResourceBinSession.can_lookup_resource_bin_mappings
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    get_resource_ids_by_bin_template = """
        # Implemented from template for
        # osid.resource.ResourceBinSession.get_resource_ids_by_bin
        id_list = []
        for ${object_name_under} in self.get_${object_name_plural_under}_by_${cat_name_under}(${arg0_name}):
            id_list.append(${object_name_under}.get_id())
        return IdList(id_list)"""

    get_resources_by_bin_template = """
        # Implemented from template for
        # osid.resource.ResourceBinSession.get_resources_by_bin
        mgr = self._get_provider_manager('${package_name_replace_upper}')
        lookup_session = mgr.get_${object_name_under}_lookup_session_for_${cat_name_under}(${arg0_name}, proxy=self._proxy)
        lookup_session.use_isolated_${cat_name_under}_view()
        return lookup_session.get_${object_name_plural_under}()"""

    get_resource_ids_by_bins_template = """
        # Implemented from template for
        # osid.resource.ResourceBinSession.get_resource_ids_by_bins
        id_list = []
        for ${object_name_under} in self.get_${object_name_plural_under}_by_${cat_name_plural_under}(${arg0_name}):
            id_list.append(${object_name_under}.get_id())
        return IdList(id_list)"""

    get_resources_by_bins_template = """
        # Implemented from template for
        # osid.resource.ResourceBinSession.get_resources_by_bins
        ${object_name_under}_list = []
        for ${cat_name_under}_id in ${arg0_name}:
            ${object_name_under}_list += list(
                self.get_${object_name_plural_under}_by_${cat_name_under}(${cat_name_under}_id))
        return objects.${return_type}(${object_name_under}_list)"""

    get_bin_ids_by_resource_template = """
        # Implemented from template for
        # osid.resource.ResourceBinSession.get_bin_ids_by_resource
        mgr = self._get_provider_manager('${package_name_replace_upper}', local=True)
        lookup_session = mgr.get_${object_name_under}_lookup_session(proxy=self._proxy)
        lookup_session.use_federated_${cat_name_under}_view()
        ${object_name_under} = lookup_session.get_${object_name_under}(${arg0_name})
        id_list = []
        for idstr in ${object_name_under}._my_map['assigned${cat_name}Ids']:
            id_list.append(Id(idstr))
        return IdList(id_list)"""

    get_bins_by_resource_template = """
        # Implemented from template for
        # osid.resource.ResourceBinSession.get_bins_by_resource
        mgr = self._get_provider_manager('${package_name_replace_upper}')
        lookup_session = mgr.get_${cat_name_under}_lookup_session(proxy=self._proxy)
        return lookup_session.get_${cat_name_plural_under}_by_ids(
            self.get_${cat_name_under}_ids_by_${object_name_under}(${arg0_name}))"""


class ResourceBinAssignmentSession:

    import_statements_pattern = [
        'from ..id.objects import IdList',
    ]

    init_template = """
    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession._init_catalog(self, proxy, runtime)
        self._session_name = '${interface_name}'
        self._catalog_name = '${cat_name}'
        self._forms = dict()
        self._kwargs = kwargs"""

    can_assign_resources_template = """
        # Implemented from template for
        # osid.resource.ResourceBinAssignmentSession.can_assign_resources
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    can_assign_resources_to_bin_template = """
        # Implemented from template for
        # osid.resource.ResourceBinAssignmentSession.can_assign_resources_to_bin
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        if ${arg0_name}.get_identifier() == '000000000000000000000000':
            return False
        return True"""

    get_assignable_bin_ids_template = """
        # Implemented from template for
        # osid.resource.ResourceBinAssignmentSession.get_assignable_bin_ids
        # This will likely be overridden by an authorization adapter
        mgr = self._get_provider_manager('${package_name_replace_upper}', local=True)
        lookup_session = mgr.get_${cat_name_under}_lookup_session(proxy=self._proxy)
        ${object_name_plural_under} = lookup_session.get_${cat_name_plural_under}()
        id_list = []
        for ${object_name_under} in ${object_name_plural_under}:
            id_list.append(${object_name_plural_under}.get_id())
        return IdList(id_list)"""

    get_assignable_bin_ids_for_resource_template = """
        # Implemented from template for
        # osid.resource.ResourceBinAssignmentSession.get_assignable_bin_ids_for_resource
        # This will likely be overridden by an authorization adapter
        return self.get_assignable_bin_ids()"""

    assign_resource_to_bin_template = """
        # Implemented from template for
        # osid.resource.ResourceBinAssignmentSession.assign_resource_to_bin
        mgr = self._get_provider_manager('${package_name_replace_upper}', local=True)
        lookup_session = mgr.get_${cat_name_under}_lookup_session(proxy=self._proxy)
        lookup_session.get_${cat_name_under}(${arg1_name}) # to raise NotFound
        self._assign_object_to_catalog(${arg0_name}, ${arg1_name})"""

    unassign_resource_from_bin_template = """
        # Implemented from template for
        # osid.resource.ResourceBinAssignmentSession.unassign_resource_from_bin
        mgr = self._get_provider_manager('${package_name_replace_upper}', local=True)
        lookup_session = mgr.get_${cat_name_under}_lookup_session(proxy=self._proxy)
        cat = lookup_session.get_${cat_name_under}(${arg1_name}) # to raise NotFound
        self._unassign_object_from_catalog(${arg0_name}, ${arg1_name})"""


class ResourceAgentSession:

    import_statements = [
        'from .simple_agent import Agent',
        'from ..id.objects import IdList'
    ]

    init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None):
        OsidSession.__init__(self)
        self._catalog_class = objects.Bin
        self._session_name = 'ResourceAgentSession'
        self._catalog_name = 'Bin'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='assessment',
            cat_name='Bin',
            cat_class=objects.Bin)
        self._forms = dict()"""

    get_resource_id_by_agent = """
        return self.get_resource_by_agent(agent_id).get_id()"""

    get_resource_by_agent = """
        collection = MongoClientValidated('resource',
                                          collection='Resource',
                                          runtime=self._runtime)
        result = collection.find_one(
            dict({'agentIds': {'$in': [str(agent_id)]}},
                 **self._view_filter()))
        return objects.Resource(
            osid_object_map=result,
            runtime=self._runtime,
            proxy=self._proxy)"""

    get_agent_ids_by_resource = """
        collection = MongoClientValidated('resource',
                                          collection='Resource',
                                          runtime=self._runtime)
        resource = collection.find_one(
            dict({'_id': ObjectId(resource_id.get_identifier())},
                 **self._view_filter()))
        if 'agentIds' not in resource:
            result = IdList([])
        else:
            result = IdList(resource['agentIds'])
        return result"""

    get_agents_by_resource = """
        agent_list = []
        for agent_id in self.get_agent_ids_by_resource(resource_id):
            agent_list.append(Agent(agent_id))
        return AgentList(agent_list)"""


class ResourceAgentAssignmentSession:

    init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None):
        OsidSession.__init__(self)
        self._catalog_class = objects.Bin
        self._session_name = 'ResourceAgentAssignmentSession'
        self._catalog_name = 'Bin'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='assessment',
            cat_name='Bin',
            cat_class=objects.Bin)
        self._forms = dict()"""

    assign_agent_to_resource = """
        # Should check for existence of Agent? We may mever manage them.
        collection = MongoClientValidated('resource',
                                          collection='Resource',
                                          runtime=self._runtime)
        resource = collection.find_one({'_id': ObjectId(resource_id.get_identifier())})

        try:
            ResourceAgentSession(
                self._catalog_id, self._proxy, self._runtime).get_resource_by_agent(agent_id)
        except errors.NotFound:
            pass
        else:
            raise errors.AlreadyExists()
        if 'agentIds' not in resource:
            resource['agentIds'] = [str(agent_id)]
        else:
            resource['agentIds'].append(str(agent_id))
        collection.save(resource)"""

    unassign_agent_from_resource = """
        collection = MongoClientValidated('resource',
                                          collection='Resource',
                                          runtime=self._runtime)
        resource = collection.find_one({'_id': ObjectId(resource_id.get_identifier())})

        try:
            resource['agentIds'].remove(str(agent_id))
        except (KeyError, ValueError):
            raise errors.NotFound('agent_id not assigned to resource')
        collection.save(resource)"""


class BinLookupSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from ..osid.sessions import OsidSession',
        'from . import objects',
        'from ..utilities import MongoClientValidated',
        'from bson.objectid import ObjectId',
        'DESCENDING = -1',
        'ASCENDING = 1',
        'COMPARATIVE = 0',
        'PLENARY = 1',
        #'CREATED = True',
        #'UPDATED = True'
    ]

    init_template = """
    _session_name = '${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession._init_catalog(self, proxy, runtime)
        self._catalog_view = COMPARATIVE
        self._kwargs = kwargs"""

    use_comparative_bin_view_template = """
        # Implemented from template for
        # osid.resource.BinLookupSession.use_comparative_bin_view
        self._catalog_view = COMPARATIVE"""

    use_plenary_bin_view_template = """
        # Implemented from template for
        # osid.resource.BinLookupSession.use_plenary_bin_view
        self._catalog_view = PLENARY"""

    get_bin_template = """
        # Implemented from template for
        # osid.resource.BinLookupSession.get_bin
        collection = MongoClientValidated('${package_name}',
                                          collection='${cat_name}',
                                          runtime=self._runtime)
        # Need to consider how to best deal with the "phantom root" catalog issue
        if ${arg0_name}.get_identifier() == '000000000000000000000000':
            return self._get_phantom_root_catalog(cat_class=objects.${cat_name}, cat_name='${cat_name}')
        try:
            result = collection.find_one({'_id': ObjectId(${arg0_name}.get_identifier())})
        except errors.NotFound:
            # Try creating an orchestrated ${cat_name}.  Let it raise errors.NotFound()
            result = self._create_orchestrated_cat(${arg0_name}, '${package_name}', '${cat_name}')

        return objects.${return_type}(osid_object_map=result, runtime=self._runtime, proxy=self._proxy)"""

    get_bins_by_ids_template = """
        # Implemented from template for
        # osid.resource.BinLookupSession.get_bins_by_ids_template
        # NOTE: This implementation currently ignores plenary view
        # Also, this should be implemented to use get_${cat_name}() instead of direct to database
        catalog_id_list = []
        for i in ${arg0_name}:
            catalog_id_list.append(ObjectId(i.get_identifier()))
        collection = MongoClientValidated('${package_name}',
                                          collection='${cat_name}',
                                          runtime=self._runtime)
        result = collection.find({'_id': {'$$in': catalog_id_list}}).sort('_id', DESCENDING)

        return objects.${return_type}(result, runtime=self._runtime, proxy=self._proxy)"""


    get_bins_template = """
        # Implemented from template for
        # osid.resource.BinLookupSession.get_bins_template
        # NOTE: This implementation currently ignores plenary view
        collection = MongoClientValidated('${package_name}',
                                          collection='${cat_name}',
                                          runtime=self._runtime)
        result = collection.find().sort('_id', DESCENDING)

        return objects.${return_type}(result, runtime=self._runtime, proxy=self._proxy)"""

    get_bins_by_genus_type_template = """
        # Implemented from template for
        # osid.resource.BinLookupSession.get_bins_by_genus_type_template
        # NOTE: This implementation currently ignores plenary view
        collection = MongoClientValidated('${package_name}',
                                          collection='${cat_name}',
                                          runtime=self._runtime)
        result = collection.find({"genusTypeId": str(${arg0_name})}).sort('_id', DESCENDING)

        return objects.${return_type}(result, runtime=self._runtime, proxy=self._proxy)"""


class BinAdminSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from ..osid.sessions import OsidSession',
        'from ..utilities import MongoClientValidated',
        'from . import objects',
        'from bson.objectid import ObjectId',
        'CREATED = True',
        'UPDATED = True'
    ]

    init_template = """
    _session_name = '${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession._init_catalog(self, proxy, runtime)
        self._forms = dict()
        self._kwargs = kwargs"""

    can_create_bins_template = """
        # Implemented from template for
        # osid.resource.BinAdminSession.can_create_bins
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    can_create_bin_with_record_types_template = """
        # Implemented from template for
        # osid.resource.BinAdminSession.can_create_bin_with_record_types
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    get_bin_form_for_create_import_templates = [
        'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
    ]

    get_bin_form_for_create_template = """
        # Implemented from template for
        # osid.resource.BinAdminSession.get_bin_form_for_create_template
        for arg in ${arg0_name}:
            if not isinstance(arg, ABC${arg0_type}):
                raise errors.InvalidArgument('one or more argument array elements is not a valid OSID ${arg0_type}')
        if ${arg0_name} == []:
            result = objects.${return_type}(
                runtime=self._runtime,
                effective_agent_id=self.get_effective_agent_id(),
                proxy=self._proxy) ## Probably don't need effective agent id now that we have proxy in form.
        else:
            result = objects.${return_type}(
                record_types=${arg0_name},
                runtime=self._runtime,
                effective_agent_id=self.get_effective_agent_id(),
                proxy=self._proxy) ## Probably don't need effective agent id now that we have proxy in form.
        self._forms[result.get_id().get_identifier()] = not CREATED
        return result"""

    create_bin_import_templates = [
        'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
    ]

    create_bin_template = """
        # Implemented from template for
        # osid.resource.BinAdminSession.create_bin_template
        collection = MongoClientValidated('${package_name}',
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

    get_bin_form_for_update_import_templates = [
        'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
    ]

    get_bin_form_for_update_template = """
        # Implemented from template for
        # osid.resource.BinAdminSession.get_bin_form_for_update_template
        collection = MongoClientValidated('${package_name}',
                                          collection='${cat_name}',
                                          runtime=self._runtime)
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        result = collection.find_one({'_id': ObjectId(${arg0_name}.get_identifier())})

        cat_form = objects.${return_type}(osid_object_map=result, runtime=self._runtime, proxy=self._proxy)
        self._forms[cat_form.get_id().get_identifier()] = not UPDATED

        return cat_form"""

    update_bin_import_templates = [
        'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
    ]

    update_bin_template = """
        # Implemented from template for
        # osid.resource.BinAdminSession.update_bin_template
        collection = MongoClientValidated('${package_name}',
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
        collection.save(${arg0_name}._my_map) # save is deprecated - change to replace_one

        self._forms[${arg0_name}.get_id().get_identifier()] = UPDATED

        # Note: this is out of spec. The OSIDs don't require an object to be returned
        return objects.${return_type}(osid_object_map=${arg0_name}._my_map, runtime=self._runtime, proxy=self._proxy)"""

    delete_bin_import_templates = [
        'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
    ]

    delete_bin_template = """
        # Implemented from template for
        # osid.resource.BinAdminSession.delete_bin_template
        collection = MongoClientValidated('${package_name}',
                                          collection='${cat_name}',
                                          runtime=self._runtime)
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        for object_catalog in ${cataloged_object_caps_list}:
            obj_collection = MongoClientValidated('${package_name}',
                                                  collection=object_catalog,
                                                  runtime=self._runtime)
            if obj_collection.find({'assigned${cat_name}Ids': {'$$in': [str(${arg0_name})]}}).count() != 0:
                raise errors.IllegalState('catalog is not empty')
        collection.delete_one({'_id': ObjectId(${arg0_name}.get_identifier())})"""

    alias_bin_template = """
        # Implemented from template for
        # osid.resource.BinLookupSession.alias_bin_template
        # NEED TO FIGURE OUT HOW TO IMPLEMENT THIS SOMEDAY
        raise errors.Unimplemented()"""

class BinNotificationSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..osid.sessions import OsidSession',
        #'from ..primitives import Id',
        #'from ..utilities import MongoClientValidated',
        #'from . import objects',
        #'from bson.objectid import ObjectId',
    ]

    init_template = """
    _session_name = '${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession._init_catalog(self, proxy, runtime)
        self._kwargs = kwargs"""


class BinHierarchySession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from ..osid.sessions import OsidSession',
        'from . import objects',
        'COMPARATIVE = 0',
        'PLENARY = 1',
    ]

    init_template = """
    _session_name = '${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        OsidSession._init_catalog(self, proxy, runtime)
        self._forms = dict()
        self._kwargs = kwargs
        hierarchy_mgr = self._get_provider_manager('HIERARCHY')
        self._hierarchy_session = hierarchy_mgr.get_hierarchy_traversal_session_for_hierarchy(
            Id(authority='${pkg_name_upper}',
               namespace='CATALOG',
               identifier='${cat_name_upper}'),
             proxy=self._proxy
        )"""

    can_access_bin_hierarchy_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.can_access_bin_hierarchy
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    get_bin_hierarchy_id_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.get_bin_hierarchy_id
        return self._hierarchy_session.get_hierarchy_id()"""

    get_bin_hierarchy_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.get_bin_hierarchy
        return self._hierarchy_session.get_hierarchy()"""

    get_root_bin_ids_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.get_root_bin_ids
        return self._hierarchy_session.get_roots()"""

    get_root_bins_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.get_root_bins
        return ${cat_name}LookupSession(
            self._proxy,
            self._runtime).get_${cat_name_plural_under}_by_ids(list(self.get_root_${cat_name_under}_ids()))"""

    has_parent_bins_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.has_parent_bins
        return self._hierarchy_session.has_parents(id_=${arg0_name})"""

    is_parent_of_bin_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.is_parent_of_bin
        return self._hierarchy_session.is_parent(id_=${arg1_name}, parent_id=${arg0_name})"""

    get_parent_bin_ids_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.get_parent_bin_ids
        return self._hierarchy_session.get_parents(id_=${arg0_name})"""

    get_parent_bins_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.get_parent_bins
        return ${cat_name}LookupSession(
            self._proxy,
            self._runtime).get_${cat_name_plural_under}_by_ids(
                list(self.get_parent_${cat_name_under}_ids(${arg0_name})))"""

    is_ancestor_of_bin_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.is_ancestor_of_bin
        return self._hierarchy_session.is_ancestor(id_=${arg0_name}, ancestor_id=${arg1_name})"""

    has_child_bins_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.has_child_bins
        return self._hierarchy_session.has_children(id_=${arg0_name})"""

    is_child_of_bin_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.is_child_of_bin
        return self._hierarchy_session.is_child(id_=${arg1_name}, child_id=${arg0_name})"""

    get_child_bin_ids_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.get_child_bin_ids
        return self._hierarchy_session.get_children(id_=${arg0_name})"""

    get_child_bins_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.get_child_bins
        return ${cat_name}LookupSession(
            self._proxy,
            self._runtime).get_${cat_name_plural_under}_by_ids(
                list(self.get_child_${cat_name_under}_ids(${arg0_name})))"""

    is_descendant_of_bin_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.is_descendant_of_bin
        return self._hierarchy_session.is_descendant(id_=${arg0_name}, descendant_id=${arg1_name})"""

    get_bin_node_ids_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.get_bin_node_ids
        return self._hierarchy_session.get_nodes(
            id_=${arg0_name},
            ancestor_levels=${arg1_name},
            descendant_levels=${arg2_name},
            include_siblings=${arg3_name})"""

    get_bin_nodes_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.get_bin_nodes
        return objects.${return_type}(self.get_${cat_name_under}_node_ids(
            ${arg0_name}=${arg0_name},
            ${arg1_name}=${arg1_name},
            ${arg2_name}=${arg2_name},
            ${arg3_name}=${arg3_name})._my_map, runtime=self._runtime, proxy=self._proxy)"""

class BinHierarchyDesignSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from ..osid.sessions import OsidSession',
        'from . import objects',
        'COMPARATIVE = 0',
        'PLENARY = 1',
    ]

    init_template = """
    _session_name = '${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession._init_catalog(self, proxy, runtime)
        self._forms = dict()
        self._kwargs = kwargs
        hierarchy_mgr = self._get_provider_manager('HIERARCHY')
        self._hierarchy_session = hierarchy_mgr.get_hierarchy_design_session_for_hierarchy(
            Id(authority='${pkg_name_upper}',
               namespace='CATALOG',
               identifier='${cat_name_upper}'),
            proxy=self._proxy
        )"""

    can_modify_bin_hierarchy_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchyDesignSession.can_modify_objective_bank_hierarchy
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    add_root_bin_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchyDesignSession.add_root_bin_template
        return self._hierarchy_session.add_root(id_=${arg0_name})"""

    remove_root_bin_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchyDesignSession.remove_root_bin_template
        return self._hierarchy_session.remove_root(id_=${arg0_name})"""

    add_child_bin_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchyDesignSession.add_child_bin_template
        return self._hierarchy_session.add_child(id_=${arg0_name}, child_id=${arg1_name})"""

    remove_child_bin_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchyDesignSession.remove_child_bin_template
        return self._hierarchy_session.remove_child(id_=${arg0_name}, child_id=${arg1_name})"""

    remove_child_bins_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchyDesignSession.remove_child_bin_template
        return self._hierarchy_session.remove_children(id_=${arg0_name})"""


class BinQuerySession:

    import_statements_pattern = [
    ]

    init_template = """
    _session_name = '${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession._init_catalog(self, proxy, runtime)
        self._forms = dict()
        self._kwargs = kwargs"""

    can_query_bins_template = """
        # Implemented from template for
        # osid.resource.BinQuerySession.can_query_bins
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    get_bin_query_template = """
        # Implemented from template for
        # osid.resource.BinQuerySession.get_bin_query_template
        return queries.${return_type}(runtime=self._runtime)"""

    get_bins_by_query_template = """
        # Implemented from template for
        # osid.resource.BinQuerySession.get_bins_by_query_template
        query_terms = dict(${arg0_name}._query_terms)
        collection = MongoClientValidated('${package_name}',
                                          collection='${cat_name}',
                                          runtime=self._runtime)
        result = collection.find(query_terms).sort('_id', DESCENDING)

        return objects.${return_type}(result, runtime=self._runtime)"""

class Resource:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        '#from ..id.objects import IdList',
        '#import importlib',
		'from ..utilities import get_registry',
    ]

    # Note: self._catalog_name = '${cat_name_under}' below is currently 
    # only for osid.OsidObject.get_object_map() setting the now deprecated
    # ${cat_name}Id element and may be removed someday
    init_template = """
    _namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, **kwargs): # removed osid_object_map, runtime=None
        # self._record_type_data_sets = get_registry('${object_name_upper}_RECORD_TYPES', runtime)
        osid_objects.OsidObject.__init__(self, object_name='${object_name_upper}', **kwargs)
        # self._records = dict() # Now in Extensible
        # self._load_records(osid_object_map['recordTypeIds']) # Now in OsidObject
        self._catalog_name = '${cat_name_under}'
${instance_initers}"""

    is_group_template = """
        # Implemented from template for osid.resource.Resource.is_group_template
        return self._my_map['${var_name_mixed}']"""

    is_demographic = """
        return self._demographic"""

    has_avatar_template = """
        # Implemented from template for osid.resource.Resource.has_avatar_template
        return bool(self._my_map['${var_name_mixed}Id'])"""

    get_avatar_id_template = """
        # Implemented from template for osid.resource.Resource.get_avatar_id_template
        if not self._my_map['${var_name_mixed}Id']:
            raise errors.IllegalState('this ${object_name} has no ${var_name}')
        else:
            return Id(self._my_map['${var_name_mixed}Id'])"""

    get_avatar_template = """
        # Implemented from template for osid.resource.Resource.get_avatar_template
        if not self._my_map['${var_name_mixed}Id']:
            raise errors.IllegalState('this ${object_name} has no ${var_name}')
        mgr = self._get_provider_manager('${return_pkg_caps}')
        if not mgr.supports_${return_type_under}_lookup():
            raise errors.OperationFailed('${return_pkg_title} does not support ${return_type} lookup')
        lookup_session = mgr.get_${return_type_under}_lookup_session() # What about the Proxy
        lookup_session.use_federated_${return_cat_name_under}_view()
        osid_object = lookup_session.get_${return_type_under}(self.get_${var_name}_id())
        return osid_object"""

    get_resource_record_template = """
        return self._get_record(${arg0_name})"""

    additional_methods = """
    def get_object_map(self):
        obj_map = dict(self._my_map)
        if 'agentIds' in obj_map:
            del obj_map['agentIds']
        return osid_objects.OsidObject.get_object_map(self, obj_map)

    object_map = property(fget=get_object_map)"""

class ResourceQuery:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
		'from ..utilities import get_registry',
    ]

    init_template = """
    def __init__(self, runtime):
        self._namespace = '${pkg_name_replaced}.${object_name}'
        self._runtime = runtime
        record_type_data_sets = get_registry('${object_name_upper}_RECORD_TYPES', runtime)
        self._all_supported_record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_ids = []
        for data_set in record_type_data_sets:
            self._all_supported_record_type_ids.append(str(Id(**record_type_data_sets[data_set])))
        osid_queries.OsidObjectQuery.__init__(self, runtime)
"""

    clear_group_terms_template = """
        self._clear_terms('${var_name_mixed}')"""

    match_bin_id_template = """
        self._add_match('assigned${cat_name}Ids', str(${arg0_name}), ${arg1_name})"""

    clear_bin_id_terms_template = """
        self._clear_terms('assigned${cat_name}Ids')"""


class ResourceSearch:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from dlkit.mongo.osid import searches as osid_searches',
		'from ..utilities import get_registry',
    ]

    init = """
    def __init__(self, runtime):
        self._namespace = 'resource.Resource'
        self._runtime = runtime
        record_type_data_sets = get_registry('RESOURCE_RECORD_TYPES', runtime)
        self._record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_ids = []
        self._id_list = None
        for data_set in record_type_data_sets:
            self._all_supported_record_type_ids.append(str(Id(**record_type_data_sets[data_set])))
        osid_searches.OsidSearch.__init__(self, runtime)"""

    search_among_resources = """
        self._id_list = resource_ids"""

class ResourceSearchResults:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from . import objects',
    ]

    init = """
    def __init__(self, results, runtime):
        # if you don't iterate, then .count() on the cursor is an inaccurate representation of limit / skip
        # self._results = [r for r in results]
        self._results = results
        self._runtime = runtime
        self.retrieved = False"""

    get_resources = """
        if self.retrieved:
            raise errors.IllegalState('List has already been retrieved.')
        self.retrieved = True
        return objects.ResourceList(self._results, runtime=self._runtime)"""


class ResourceForm:

    import_statements_pattern = [
        'import importlib',
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from ..osid.metadata import Metadata',
        'from . import default_mdata',
		'from ..utilities import get_registry',
		'from ..utilities import update_display_text_defaults',
    ]

    init_template = """
    _namespace = '${implpkg_name}.${object_name}'

    def __init__(self, **kwargs):
        ${init_object}.__init__(self, object_name='${object_name_upper}', **kwargs)
        self._mdata = dict(default_mdata.${object_name_caps_under})
        self._init_metadata(**kwargs)
        if not self.is_for_update():
            self._init_map(**kwargs)

    def _init_metadata(self, **kwargs):
        \"\"\"Initialize form metadata\"\"\"
${metadata_super_initers}        ${init_object}._init_metadata(self, **kwargs)
${metadata_initers}    def _init_map(self, record_types=None, **kwargs):
        \"\"\"Initialize form map\"\"\"
${map_super_initers}        ${init_object}._init_map(self, record_types=record_types)
${persisted_initers}"""

    get_group_metadata_template = """
        # Implemented from template for osid.resource.ResourceForm.get_group_metadata_template
        metadata = dict(self._mdata['${var_name}'])
        metadata.update({'existing_${var_name}_values': self._my_map['${var_name_mixed}']})
        return Metadata(**metadata)"""

    get_avatar_metadata_template = """
        # Implemented from template for osid.resource.ResourceForm.get_group_metadata_template
        metadata = dict(self._mdata['${var_name}'])
        metadata.update({'existing_${var_name}_values': self._my_map['${var_name_mixed}Id']})
        return Metadata(**metadata)"""

    set_group_template = """
        # Implemented from template for osid.resource.ResourceForm.set_group_template
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_${arg0_type}(${arg0_name}):
            raise errors.InvalidArgument()
        self._my_map['${var_name_mixed}'] = ${arg0_name}"""

    clear_group_template = """
        # Implemented from template for osid.resource.ResourceForm.clear_group_template
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['${var_name_mixed}'] = self._${var_name}_default"""

    set_avatar_template = """
        # Implemented from template for osid.resource.ResourceForm.set_avatar_template
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_id(${arg0_name}):
            raise errors.InvalidArgument()
        self._my_map['${var_name_mixed}Id'] = str(${arg0_name})"""

    clear_avatar_template = """
        # Implemented from template for osid.resource.ResourceForm.clear_avatar_template
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['${var_name_mixed}Id'] = self._${var_name}_default"""

    get_resource_form_record_template = """
        return self._get_record(${arg0_name})"""



class ResourceList:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
    ]

    get_next_resource_template = """
        # Implemented from template for osid.resource.ResourceList.get_next_resource
        return self.next()

    def next(self):
        return self._get_next_object(${return_type})"""

    get_next_resources_template = """
        # Implemented from template for osid.resource.ResourceList.get_next_resources
        return self._get_next_n(${arg0_name})"""

class Bin:

    import_statements_pattern = [
        'import importlib',
    ]

    init_template = """
    _namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, **kwargs):
        # self._record_type_data_sets = get_registry('${object_name_upper}_RECORD_TYPES', runtime)
        osid_objects.OsidCatalog.__init__(self, object_name='${object_name_upper}', **kwargs)
        # self._records = dict() # Now set in Extensible, including transition stuff below. Let's hope we've transitioned:
        # This check is here for transition purposes:
        # try:
        #     self._load_records(osid_object_map['recordTypeIds'])
        # except KeyError:
        #     #print 'KeyError: recordTypeIds key not found in ', self._my_map['displayName']['text']
        #     self._load_records([]) # In place for transition purposes"""

class BinForm:

    import_statements_pattern = [
        'from . import default_mdata',
        '#from ..osid.objects import OsidForm',
        '#from ..osid.objects import OsidObjectForm',
		'#from ..utilities import get_registry',
    ]

    init_template = """
    _namespace = '${implpkg_name}.${object_name}'

    def __init__(self, **kwargs):
        osid_objects.OsidCatalogForm.__init__(self, object_name='${object_name_upper}', **kwargs)
        self._mdata = dict(default_mdata.${object_name_caps_under})
        self._init_metadata(**kwargs)
        if not self.is_for_update():
            self._init_map(**kwargs)

    def _init_metadata(self, **kwargs):
        \"\"\"Initialize form metadata\"\"\"
        osid_objects.OsidCatalogForm._init_metadata(self, **kwargs)

    def _init_map(self, record_types=None, **kwargs):
        \"\"\"Initialize form map\"\"\"
        osid_objects.OsidCatalogForm._init_map(self, record_types, **kwargs)
"""


class BinQuery:

    import_statements_pattern = [
        'from ..primitives import Id',
        'from ..id.objects import IdList',
		'from ..utilities import get_registry',
    ]

    init_template = """
    def __init__(self, runtime):
        self._runtime = runtime
        record_type_data_sets = get_registry('${cat_name_upper}_RECORD_TYPES', runtime)
        self._all_supported_record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_ids = []
        for data_set in record_type_data_sets:
            self._all_supported_record_type_ids.append(str(Id(**record_type_data_sets[data_set])))
        osid_queries.OsidCatalogQuery.__init__(self, runtime)

    def _get_descendant_catalog_ids(self, catalog_id):
        hm = self._get_provider_manager('HIERARCHY')
        hts = hm.get_hierarchy_traversal_session_for_hierarchy(
            Id(authority='${pkg_name_upper}',
               namespace='CATALOG',
               identifier='${cat_name_upper}')
        ) # What about the Proxy?
        descendants = []
        if hts.has_children(catalog_id):
            for child_id in hts.get_children(catalog_id):
                descendants += list(self._get_descendant_catalog_ids(child_id))
                descendants.append(child_id)
        return IdList(descendants)
"""

    clear_group_terms_template = """
        self._clear_terms('${var_name_mixed}')"""


class BinNode:

    import_statements_pattern = [
        'from ..utilities import get_provider_manager',
        'from dlkit.primordium.id.primitives import Id',
    ]

    init_template = """
    def __init__(self, node_map, runtime=None, proxy=None, lookup_session=None):
        osid_objects.OsidNode.__init__(self, node_map)
        self._lookup_session = lookup_session
        self._runtime = runtime
        self._proxy = proxy

    def get_object_node_map(self):
        node_map = dict(self.get_${object_name_under}().get_object_map())
        node_map['type'] = '${object_name}Node'
        node_map['parentNodes'] = []
        node_map['childNodes'] = []
        for ${object_name_under}_node in self.get_parent_${object_name_under}_nodes():
            node_map['parentNodes'].append(${object_name_under}_node.get_object_node_map())
        for ${object_name_under}_node in self.get_child_${object_name_under}_nodes():
            node_map['childNodes'].append(${object_name_under}_node.get_object_node_map())
        return node_map"""

    get_bin_template = """
        if self._lookup_session is None:
            mgr = get_provider_manager('${package_name_upper}', runtime=self._runtime, proxy=self._proxy)
            self._lookup_session = mgr.get_${object_name_under}_lookup_session()
        return self._lookup_session.get_${object_name_under}(Id(self._my_map['id']))"""

    get_parent_bin_nodes_template = """
        parent_${object_name_under}_nodes = []
        for node in self._my_map['parentNodes']:
            parent_${object_name_under}_nodes.append(${object_name}Node(
                node._my_map,
                runtime=self._runtime,
                proxy=self._proxy,
                lookup_session=self._lookup_session))
        return ${return_type}(parent_${object_name_under}_nodes)"""

    get_child_bin_nodes_template = """
        parent_${object_name_under}_nodes = []
        for node in self._my_map['childNodes']:
            parent_${object_name_under}_nodes.append(${object_name}Node(
                node._my_map,
                runtime=self._runtime,
                proxy=self._proxy,
                lookup_session=self._lookup_session))
        return ${return_type}(parent_${object_name_under}_nodes)"""
