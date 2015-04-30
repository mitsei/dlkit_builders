
from .error_lists import session_errors

class ResourceProfile:

    import_statements_pattern = [
        '# pylint: disable=no-member',
        'from ..primitives import Type',
        'from ..type.objects import TypeList',
        'from . import sessions',
        'from ..osid.osid_errors import NullArgument',
        'from . import profile',
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
        try:
            from .records import types
            record_type_maps = types.${object_name_upper}_RECORD_TYPES
        except (ImportError, AttributeError):
            return TypeList([])
        record_types = []
        for record_type_map in record_type_maps:
            record_types.append(Type(**record_type_maps[record_type_map]))
        return TypeList(record_types, count=len(record_types))"""

    supports_resource_record_type_template = """
        # Implemented from template for
        # osid.resource.ResourceProfile.supports_resource_record_type_template
        if ${arg0_name} is None:
            raise NullArgument()
        try:
            from .records import types
            record_type_maps = types.${object_name_upper}_RECORD_TYPES
        except (ImportError, AttributeError):
            return False
        supports = False
        for record_type_map in record_type_maps:
            if (${arg0_name}.get_authority() == record_type_maps[record_type_map]['authority'] and
                    ${arg0_name}.get_identifier_namespace() == record_type_maps[record_type_map]['namespace'] and
                    ${arg0_name}.get_identifier() == record_type_maps[record_type_map]['identifier']):
                supports = True
        return supports"""

class ResourceManager:

    import_statements_pattern = [
    'from ..osid.osid_errors import Unimplemented',
    'from ..osid.osid_errors import NullArgument',
    'from ..osid.osid_errors import NotFound # pylint: disable=unused-import',
    'from ..osid.osid_errors import OperationFailed # pylint: disable=unused-import',
    ]

    get_resource_lookup_session_template = """
        if not self.supports_${support_check}():
            raise Unimplemented()
        return ${return_module}.${return_type}(runtime=self._runtime)"""

    get_resource_lookup_session_for_bin_template = """
        if not ${arg0_name}:
            raise NullArgument
        if not self.supports_${support_check}():
            raise Unimplemented()
        ##
        # Also include check to see if the catalog Id is found otherwise raise NotFound
        ##
        return ${return_module}.${return_type}(${arg0_name}, runtime=self._runtime)"""

    old_get_resource_lookup_session_template = """
        if not self.supports_${support_check}():
            raise Unimplemented()
        try:
            from . import ${return_module}
        except ImportError:
            raise #OperationFailed()
        try:
            session = ${return_module}.${return_type}(runtime=self._runtime)
        except AttributeError:
            raise #OperationFailed()
        return session"""

    old_get_resource_lookup_session_for_bin_template = """
        if not ${arg0_name}:
            raise NullArgument
        if not self.supports_${support_check}():
            raise Unimplemented()
        ##
        # Also include check to see if the catalog Id is found otherwise raise NotFound
        ##
        try:
            from . import ${return_module}
        except ImportError:
            raise #OperationFailed()
        try:
            session = ${return_module}.${return_type}(${arg0_name}, runtime=self._runtime)
#            session = ${return_module}.${return_type}(${arg0_name}.get_identifier())
        except AttributeError:
            raise #OperationFailed()
        return session"""

class ResourceProxyManager:

    import_statements_pattern = [
    'from ..osid.osid_errors import Unimplemented',
    'from ..osid.osid_errors import NullArgument',
    'from ..osid.osid_errors import NotFound # pylint: disable=unused-import',
    'from ..osid.osid_errors import OperationFailed # pylint: disable=unused-import',
    ]

    get_resource_lookup_session_template = """
        if proxy is None:
            raise NullArgument()
        if not self.supports_${support_check}():
            raise Unimplemented()
        return ${return_module}.${return_type}(proxy=proxy, runtime=self._runtime) # pylint: disable=no-member"""

    get_resource_lookup_session_for_bin_template = """
        if ${arg0_name} is None or proxy is None:
            raise NullArgument
        if not self.supports_${support_check}():
            raise Unimplemented()
        ##
        # Also include check to see if the catalog Id is found otherwise raise NotFound
        ##
        return ${return_module}.${return_type}(${arg0_name}, proxy=proxy, runtime=self._runtime) # pylint: disable=no-member"""

    old_get_resource_lookup_session_template = """
        if proxy is None:
            raise NullArgument()
        if not self.supports_${support_check}():
            raise Unimplemented()
        try:
            from . import ${return_module}
        except ImportError:
            raise OperationFailed()
        try:
            session = ${return_module}.${return_type}(proxy=proxy, runtime=self._runtime)
        except AttributeError:
            raise OperationFailed()
        return session"""

    old_get_resource_lookup_session_for_bin_template = """
        if ${arg0_name} is None or proxy is None:
            raise NullArgument
        if not self.supports_${support_check}():
            raise Unimplemented()
        ##
        # Also include check to see if the catalog Id is found otherwise raise NotFound
        ##
        try:
            from . import ${return_module}
        except ImportError:
            raise OperationFailed()
        try:
            session = ${return_module}.${return_type}(${arg0_name}, proxy=proxy, runtime=self._runtime)
#            session = ${return_module}.${return_type}(${arg0_name}.get_identifier())
        except AttributeError:
            raise #OperationFailed()
        return session"""


class ResourceLookupSession:

    import_statements_pattern = [
        '# pylint: disable=protected-access',
        'from ..osid.osid_errors import ' + session_errors,
        'from ..primitives import Id',
        'from ..osid.sessions import OsidSession',
        'from .. import mongo_client',
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

    init_template = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        self._catalog_class = objects.${cat_name}
        self._session_name = '${interface_name}'
        self._catalog_name = '${cat_name}'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='${pkg_name}',
            cat_name='${cat_name}',
            cat_class=objects.${cat_name})
        self._object_view = COMPARATIVE
        self._catalog_view = ISOLATED
        self._kwargs = kwargs

    def _catalog_view_idstrs(self):
        \"\"\"Implement me soon? \"\"\"
        pass
        #if self._catalog_view == ISOLATED:
        #    return [str(self._catalog_id)]
        #try:
        #    ${pkg_name}_manager = self._get_provider_manager('pkg_name_upper')
        #    hs = ${pkg_name}_manager.get_${cat_name_under}_hierarchy_session() # What about proxy?
        #except:
        #    return [str(self._catalog_id)]
"""

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
        self._object_view = COMPARATIVE"""

    use_plenary_resource_view_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.use_plenary_resource_view
        self._object_view = PLENARY"""

    use_federated_bin_view_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.use_federated_bin_view
        self._catalog_view = FEDERATED"""

    use_isolated_bin_view_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.use_isolated_bin_view
        self._catalog_view = ISOLATED"""

    get_resource_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.get_resource
        # NOTE: This implementation currently ignores plenary view
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        if not ${arg0_name}:
            raise NullArgument()
        if self._catalog_view == ISOLATED:
            result = collection.find_one({'_id': ObjectId(${arg0_name}.get_identifier()),
                                          '${cat_name_mixed}Id': str(self._catalog_id)})
        else:
            # This should really look in the underlying hierarchy (when hierarchy is implemented)
            result = collection.find_one({'_id': ObjectId(${arg0_name}.get_identifier())})
        if result is None:
            raise NotFound()
        mongo_client.close()
        return objects.${return_type}(result, db_prefix=self._db_prefix, runtime=self._runtime)"""

    get_resources_by_ids_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.get_resources_by_ids
        # NOTE: This implementation currently ignores plenary view
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        if not ${arg0_name}:
            raise NullArgument()
        object_id_list = []
        for i in ${arg0_name}:
            object_id_list.append(ObjectId(i.get_identifier()))
        if self._catalog_view == ISOLATED:
            result = collection.find({'_id': {'$$in': object_id_list},
                                      '${cat_name_mixed}Id': str(self._catalog_id)}).sort('_id', DESCENDING)
            count = collection.find({'_id': {'$$in': object_id_list},
                                     '${cat_name_mixed}Id': str(self._catalog_id)}).count()
        else:
            result = collection.find({'_id': {'$$in': object_id_list}}).sort('_id', DESCENDING)
            count = collection.find({'_id': {'$$in': object_id_list}}).count()
        mongo_client.close()
        return objects.${return_type}(result, count=count, runtime=self._runtime)"""

    get_resources_by_genus_type_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.get_resources_by_genus_type
        # NOTE: This implementation currently ignores plenary view
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        if self._catalog_view == ISOLATED:
            result = collection.find({'genusTypeId': str(${arg0_name}),
                                      '${cat_name_mixed}Id': str(self._catalog_id)}).sort('_id', DESCENDING)
            count = collection.find({'genusTypeId': str(${arg0_name}),
                                     '${cat_name_mixed}Id': str(self._catalog_id)}).count()
        else:
            result = collection.find({'genusTypeId': str(${arg0_name})}).sort('_id', DESCENDING)
            count = collection.find({'genusTypeId': str(${arg0_name})}).count()
        mongo_client.close()
        return objects.${return_type}(result, count=count, runtime=self._runtime)"""

    get_resources_by_parent_genus_type_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.get_resources_by_parent_genus_type
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
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        if self._catalog_view == ISOLATED:
            result = collection.find({'${cat_name_mixed}Id': str(self._catalog_id)}).sort('_id', DESCENDING)
            count = collection.find({'${cat_name_mixed}Id': str(self._catalog_id)}).count()
        else:
            result = collection.find().sort('_id', DESCENDING)
            count = collection.count()
        mongo_client.close()
        return objects.${return_type}(result, count=count, runtime=self._runtime)"""

class ResourceQuerySession:

    import_statements_pattern = [
        'from ..osid.osid_errors import ' + session_errors,
        'from ..osid.sessions import OsidSession',
        'from .. import mongo_client',
        'from . import queries',
        'DESCENDING = -1',
        'ASCENDING = 1'
    ]

    init_template = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        self._catalog_class = objects.${cat_name}
        self._session_name = '${interface_name}'
        self._catalog_name = '${cat_name}'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='${pkg_name}',
            cat_name='${cat_name}',
            cat_class=objects.${cat_name})
        self._catalog_view = ISOLATED
        self._kwargs = kwargs
"""

    can_query_resources_template = """
        # Implemented from template for
        # osid.resource.ResourceQuerySession.can_query_resources
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    get_resource_query_template = """
        # Implemented from template for
        # osid.resource.ResourceQuerySession.get_resource_query_template
        return queries.${return_type}()"""

    get_resources_by_query_template = """
        # Implemented from template for
        # osid.resource.ResourceQuerySession.get_resources_by_query
        if not ${arg0_name}:
            raise NullArgument()
        query_terms = dict(${arg0_name}._query_terms)
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        if self._catalog_view == ISOLATED:
            query_terms['${cat_name_mixed}Id'] = str(self._catalog_id)
        result = collection.find(query_terms).sort('_id', DESCENDING)
        count = collection.find(query_terms).count()
        mongo_client.close()
        return objects.${return_type}(result, count=count, runtime=self._runtime)"""


class ResourceAdminSession:

    import_statements_pattern = [
        'from ..osid.osid_errors import ' + session_errors,
        'from ..osid.sessions import OsidSession',
        'from ..primitives import Id',
        'from .. import mongo_client',
        'from . import objects',
        'from bson.objectid import ObjectId'
    ]

    init_template = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        self._catalog_class = objects.${cat_name}
        self._session_name = '${interface_name}'
        self._catalog_name = '${cat_name}'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='${pkg_name}',
            cat_name='${cat_name}',
            cat_class=objects.${cat_name})
        self._forms = dict()
        self._kwargs = kwargs
"""

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

    get_resource_form_for_create_template = """
        # Implemented from template for
        # osid.resource.ResourceAdminSession.get_resource_form_for_create_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        if ${arg0_name} is None:
            raise NullArgument()
        for arg in ${arg0_name}:
            if not isinstance(arg, ABC${arg0_type}):
                raise InvalidArgument('one or more argument array elements is not a valid OSID ${arg0_type}')
        if ${arg0_name} == []:
            obj_form = objects.${return_type}(
                ${cat_name_under}_id=self._catalog_id,
                db_prefix=self._db_prefix,
                runtime=self._runtime,
                effective_agent_id=self.get_effective_agent_id())
        else:
            obj_form = objects.${return_type}(
                ${cat_name_under}_id=self._catalog_id,
                record_types=${arg0_name},
                db_prefix=self._db_prefix,
                runtime=self._runtime,
                effective_agent_id=self.get_effective_agent_id())
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form"""

    create_resource_template = """
        # Implemented from template for
        # osid.resource.ResourceAdminSession.create_resource_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise InvalidArgument('argument type is not an ${arg0_type}')
        if ${arg0_name}.is_for_update():
            raise InvalidArgument('the ${arg0_type} is for update only, not create')
        try:
            if self._forms[${arg0_name}.get_id().get_identifier()] == CREATED:
                raise IllegalState('${arg0_name} already used in a create transaction')
        except KeyError:
            raise Unsupported('${arg0_name} did not originate from this session')
        if not ${arg0_name}.is_valid():
            raise InvalidArgument('one or more of the form elements is invalid')
        try:
            id_ = collection.insert(${arg0_name}._my_map)
        except: # what exceptions does mongodb insert raise?
            raise OperationFailed()
        self._forms[${arg0_name}.get_id().get_identifier()] = CREATED
        result = objects.${return_type}(
            collection.find_one({'_id': id_}),
            db_prefix=self._db_prefix,
            runtime=self._runtime)
        mongo_client.close()
        return result"""

    get_resource_form_for_update_template = """
        # Implemented from template for
        # osid.resource.ResourceAdminSession.get_resource_form_for_update_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        result = collection.find_one({'_id': ObjectId(${arg0_name}.get_identifier())})
        if result == '':
            raise NotFound()
        obj_form = objects.${return_type}(result, db_prefix=self._db_prefix, runtime=self._runtime)
        self._forms[obj_form.get_id().get_identifier()] = not UPDATED
        mongo_client.close()
        return obj_form"""

    update_resource_template = """
        # Implemented from template for
        # osid.resource.ResourceAdminSession.update_resource_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise InvalidArgument('argument type is not an ${arg0_type}')
        if not ${arg0_name}.is_for_update():
            raise InvalidArgument('the ${arg0_type} is for update only, not create')
        try:
            if self._forms[${arg0_name}.get_id().get_identifier()] == UPDATED:
                raise IllegalState('${arg0_name} already used in an update transaction')
        except KeyError:
            raise Unsupported('${arg0_name} did not originate from this session')
        if not ${arg0_name}.is_valid():
            raise InvalidArgument('one or more of the form elements is invalid')
        result = collection.save(${arg0_name}._my_map)
        if result == "What to look for here???":
            pass # Need to figure out what writeConcernErrors to catch and deal with?
        self._forms[${arg0_name}.get_id().get_identifier()] = UPDATED
        mongo_client.close()
        # Note: this is out of spec. The OSIDs don't require an object to be returned:
        return objects.${return_type}(
            ${arg0_name}._my_map,
            db_prefix=self._db_prefix,
            runtime=self._runtime)"""

    delete_resource_template = """
        # Implemented from template for
        # osid.resource.ResourceAdminSession.delete_resource_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            return InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        ${object_name_under}_map = collection.find_one({'_id': ObjectId(${arg0_name}.get_identifier())})
        if ${object_name_under}_map is None:
            raise NotFound()
        objects.${object_name}(${object_name_under}_map, db_prefix=self._db_prefix, runtime=self._runtime)._delete()
        result = collection.remove({'_id': ObjectId(${arg0_name}.get_identifier())}, justOne=True)
        if 'err' in result and result['err'] is not None:
            raise OperationFailed()
        mongo_client.close()
#        if result['n'] == 0: This is probably redundant
#            raise NotFound()"""


    alias_resources_template = """
        # Implemented from template for
        # osid.resource.ResourceAdminSession.alias_resources_template
        raise Unimplemented()"""


class BinLookupSession:

    import_statements_pattern = [
        'from ..osid.osid_errors import ' + session_errors,
        'from ..primitives import Id',
        'from ..osid.sessions import OsidSession',
        'from . import objects',
        'from .. import mongo_client',
        'from bson.objectid import ObjectId',
        'DESCENDING = -1',
        'ASCENDING = 1',
        'COMPARATIVE = 0',
        'PLENARY = 1',
        'CREATED = True',
        'UPDATED = True'
    ]

    init_template = """
    _session_name = '${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession._init_catalog(self, proxy, runtime)
        self._catalog_view = COMPARATIVE
        self._kwargs = kwargs
"""

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
        collection = mongo_client[self._db_prefix + '${package_name}']['${cat_name}']
        if not ${arg0_name}:
            raise NullArgument()
        # Need to consider how to best deal with the "phantom root" catalog issue
        if ${arg0_name}.get_identifier() == '000000000000000000000000':
            return self._get_phantom_root_catalog(cat_class=objects.${cat_name}, cat_name='${cat_name}')
        result = collection.find_one({'_id': ObjectId(${arg0_name}.get_identifier())})
        if result is None:
            # Try creating an orchestrated ${cat_name}.  Let it raise NotFound()
            result = self._create_orchestrated_catalog_map(${arg0_name}, '${package_name}', '${cat_name}')
        mongo_client.close()
        return objects.${return_type}(result, db_prefix=self._db_prefix, runtime=self._runtime)"""

    get_bins_by_ids_template = """
        # Implemented from template for
        # osid.resource.BinLookupSession.get_bins_by_ids_template
        # NOTE: This implementation currently ignores plenary view
        # Also, this should be implemeted to use get_${cat_name}() instead of direct to database
        catalog_id_list = []
        for i in ${arg0_name}:
            catalog_id_list.append(ObjectId(i.get_identifier()))
        collection = mongo_client[self._db_prefix + '${package_name}']['${cat_name}']
        result = collection.find({'_id': {'$$in': catalog_id_list}}).sort('_id', DESCENDING)
        count = collection.find({'_id': {'$$in': catalog_id_list}}).count()
        mongo_client.close()
        return objects.${return_type}(result, count=count, db_prefix=self._db_prefix, runtime=self._runtime)"""


    get_bins_template = """
        # Implemented from template for
        # osid.resource.BinLookupSession.get_bins_template
        # NOTE: This implementation currently ignores plenary view
        collection = mongo_client[self._db_prefix + '${package_name}']['${cat_name}']
        result = collection.find().sort('_id', DESCENDING)
        count = collection.count()
        mongo_client.close()
        return objects.${return_type}(result, count=count, db_prefix=self._db_prefix, runtime=self._runtime)"""

class BinAdminSession:

    import_statements_pattern = [
        'from ..osid.osid_errors import ' + session_errors,
        'from ..primitives import Id',
        'from ..osid.sessions import OsidSession',
        'from .. import mongo_client',
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
        self._kwargs = kwargs
"""

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

    get_bin_form_for_create_template = """
        # Implemented from template for
        # osid.resource.BinAdminSession.get_bin_form_for_create_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        if ${arg0_name} is None:
            raise NullArgument()
        for arg in ${arg0_name}:
            if not isinstance(arg, ABC${arg0_type}):
                raise InvalidArgument('one or more argument array elements is not a valid OSID ${arg0_type}')
        if ${arg0_name} == []:
            result = objects.${return_type}(
                db_prefix=self._db_prefix,
                runtime=self._runtime)
        else:
            result = objects.${return_type}(
                record_types=${arg0_name},
                db_prefix=self._db_prefix,
                runtime=self._runtime)
        self._forms[result.get_id().get_identifier()] = not CREATED
        return result"""

    create_bin_template = """
        # Implemented from template for
        # osid.resource.BinAdminSession.create_bin_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        collection = mongo_client[self._db_prefix + '${package_name}']['${cat_name}']
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise InvalidArgument('argument type is not an ${arg0_type}')
        if ${arg0_name}.is_for_update():
            raise InvalidArgument('the ${arg0_type} is for update only, not create')
        try:
            if self._forms[${arg0_name}.get_id().get_identifier()] == CREATED:
                raise IllegalState('${arg0_name} already used in a create transaction')
        except KeyError:
            raise Unsupported('${arg0_name} did not originate from this session')
        if not ${arg0_name}.is_valid():
            raise InvalidArgument('one or more of the form elements is invalid')
        try:
            id_ = collection.insert(${arg0_name}._my_map)
        except: # what exceptions does mongodb insert raise?
            raise OperationFailed()
        self._forms[${arg0_name}.get_id().get_identifier()] = CREATED
        result = objects.${return_type}(
            collection.find_one({'_id': id_}),
            db_prefix=self._db_prefix,
            runtime=self._runtime)
        mongo_client.close()
        return result"""

    get_bin_form_for_update_template = """
        # Implemented from template for
        # osid.resource.BinAdminSession.get_bin_form_for_update_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        collection = mongo_client[self._db_prefix + '${package_name}']['${cat_name}']
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            return InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        result = collection.find_one({'_id': ObjectId(${arg0_name}.get_identifier())})
        if result is None:
            raise NotFound()
        cat_form = objects.${return_type}(result, db_prefix=self._db_prefix, runtime=self._runtime)
        self._forms[cat_form.get_id().get_identifier()] = not UPDATED
        mongo_client.close()
        return cat_form"""

    update_bin_template = """
        # Implemented from template for
        # osid.resource.BinAdminSession.update_bin_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        collection = mongo_client[self._db_prefix + '${package_name}']['${cat_name}']
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise InvalidArgument('argument type is not an ${arg0_type}')
        if not ${arg0_name}.is_for_update():
            raise InvalidArgument('the ${arg0_type} is for update only, not create')
        try:
            if self._forms[${arg0_name}.get_id().get_identifier()] == UPDATED:
                raise IllegalState('${arg0_name} already used in an update transaction')
        except KeyError:
            raise Unsupported('${arg0_name} did not originate from this session')
        if not ${arg0_name}.is_valid():
            raise InvalidArgument('one or more of the form elements is invalid')
        result = collection.save(${arg0_name}._my_map)
        if result == "What to look for here???":
            pass # Need to figure out what writeConcernErrors to catch and deal with?
        self._forms[${arg0_name}.get_id().get_identifier()] = UPDATED
        mongo_client.close()
        # Note: this is out of spec. The OSIDs don't require an object to be returned
        return objects.${return_type}(${arg0_name}._my_map, db_prefix=self._db_prefix, runtime=self._runtime)"""

    delete_bin_template = """
        # Implemented from template for
        # osid.resource.BinAdminSession.delete_bin_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        collection = mongo_client[self._db_prefix + '${package_name}']['${cat_name}']
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            return InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        for object_catalog in ${cataloged_object_caps_list}:
            obj_collection = mongo_client[self._db_prefix + '${package_name}'][object_catalog]
            if obj_collection.find({'${cat_name_mixed}Id': str(${arg0_name})}).count() != 0:
                raise IllegalState('catalog is not empty')
        result = collection.remove({'_id': ObjectId(${arg0_name}.get_identifier())})
                                   # Tried using justOne above but pymongo doesn't support it
        if 'err' in result and result['err'] is not None:
            raise OperationFailed()
        if result['n'] == 0:
            raise NotFound()
        mongo_client.close()"""

    alias_bin_template = """
        # Implemented from template for
        # osid.resource.BinLookupSession.alias_bin_template
        # NEED TO FIGURE OUT HOW TO IMPLEMENT THIS SOMEDAY
        raise Unimplemented()"""

class BinHierarchySession:

    import_statements_pattern = [
        'from ..osid.osid_errors import ' + session_errors,
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
        self._catalog_view = ISOLATED
        self._kwargs = kwargs
        hierarchy_mgr = self._get_provider_manager('HIERARCHY')
        self._hierarchy_session = hierarchy_mgr.get_hierarchy_traversal_session_for_hierarchy(
            Id(authority='${pkg_name_upper}',
               namespace='CATALOG',
               identifier='${cat_name_upper}')
        )
"""

    can_access_objective_bank_hierarchy_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchySession.can_access_objective_bank_hierarchy
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
        return self._hierarchy_session.is_parent(id_=${arg0_name}, parent_id=${arg1_name})"""

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
        return self._hierarchy_session.is_child(id_=${arg0_name}, child_id=${arg1_name})"""

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
        raise Unimplemented()"""

class BinHierarchyDesignSession:

    import_statements_pattern = [
        'from ..osid.osid_errors import ' + session_errors,
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
               identifier='${cat_name_upper}')
        )
"""

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


class Resource:

    import_statements_pattern = [
        '# pylint: disable=protected-access',
        'from ..osid.osid_errors import * # pylint: disable=wildcard-import,unused-wildcard-import',
        'from ..primitives import Id',
        'from ..id.objects import IdList',
        'import importlib',
    ]

    init_template = """
    try:
        from .records.types import ${object_name_upper}_RECORD_TYPES as _record_type_data_sets
    except (ImportError, AttributeError):
        _record_type_data_sets = {}
    _namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, osid_object_map, db_prefix='', runtime=None):
        self._my_map = osid_object_map
        self._db_prefix = db_prefix
        self._runtime = runtime
        self._records = dict()
        self._load_records(osid_object_map['recordTypeIds'])
${instance_initers}
    # These next two private methods should be moved to osid.Extensible??? (I thought they were already)
    def _load_records(self, record_type_idstrs):
        \"\"\"Load all records of record type for this object.\"\"\"
        for record_type_idstr in record_type_idstrs:
            self._init_record(record_type_idstr)

    def _init_record(self, record_type_idstr):
        \"\"\"Initialize all records for this object.\"\"\"
        record_type_data = self._record_type_data_sets[Id(record_type_idstr).get_identifier()]
        module = importlib.import_module(record_type_data['module_path'])
        record = getattr(module, record_type_data['object_record_class_name'])
        self._records[record_type_idstr] = record(self)
"""

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
            raise IllegalState('this ${object_name} has no ${var_name}')
        else:
            return Id(self._my_map['${var_name_mixed}Id'])"""

    get_avatar_template = """
        # Implemented from template for osid.resource.Resource.get_avatar_template
        if not self._my_map['${var_name_mixed}Id']:
            raise IllegalState('this ${object_name} has no ${var_name}')
        try:
            mgr = self._get_provider_manager('${return_pkg_caps}')
        except:
            raise OperationFailed('failed to instantiate ${return_pkg_title}Manager')
        if not mgr.supports_${return_type_under}_lookup():
            raise OperationFailed('${return_pkg_title} does not support ${return_type} lookup')
        try:
            osid_object = mgr.get_${return_type_under}_lookup_session().get_${return_type_under}(self.get_${var_name}_id())
        except:
            raise OperationFailed()
        else:
            return osid_object"""

    get_resource_record_template = """
        # This is now in Extensible and can be replaces with:
        # return self._get_record(${arg0_name}):
        if ${arg0_name} is None:
            raise NullArgument()
        if not self.has_record_type(${arg0_name}):
            raise Unsupported()
        if str(${arg0_name}) not in self._records:
            raise Unimplemented()
        return self._records[str(${arg0_name})]"""

class ResourceQuery:

    import_statements_pattern = [
        'from ..osid.osid_errors import * # pylint: disable=wildcard-import,unused-wildcard-import',
        'from ..primitives import Id'
    ]

    init_template = """
    def __init__(self):
        try:
            from .records.types import ${object_name_upper}_RECORD_TYPES as record_type_data_sets
        except (ImportError, AttributeError):
            record_type_data_sets = {}
        self._all_supported_record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_ids = []
        for data_set in record_type_data_sets:
            self._all_supported_record_type_ids.append(str(Id(**record_type_data_sets[data_set])))
        osid_queries.OsidQuery.__init__(self)
"""

    clear_group_terms_template = """
        self._clear_terms('${var_name_mixed}')"""

class ResourceForm:

    import_statements_pattern = [
        'import importlib',
        'from ..osid.osid_errors import * # pylint: disable=wildcard-import,unused-wildcard-import',
        'from ..primitives import Id',
        'from ..osid.metadata import Metadata',
        'from . import mdata_conf'
    ]

    init_template = """
    try:
        from .records.types import ${object_name_upper}_RECORD_TYPES as _record_type_data_sets
    except (ImportError, AttributeError):
        _record_type_data_sets = dict()
    _namespace = '${implpkg_name}.${object_name}'

    def __init__(self, osid_object_map=None, record_types=None, db_prefix='', runtime=None, **kwargs):
        osid_objects.OsidForm.__init__(self)
        self._runtime = runtime
        self._db_prefix = db_prefix
        self._kwargs = kwargs
        if 'catalog_id' in kwargs:
            self._catalog_id = kwargs['catalog_id']
        self._init_metadata(**kwargs)
        self._records = dict()
        self._supported_record_type_ids = []
        if osid_object_map is not None:
            self._for_update = True
            self._my_map = osid_object_map
            self._load_records(osid_object_map['recordTypeIds'])
        else:
            self._my_map = {}
            self._for_update = False
            self._init_map(**kwargs)
            if record_types is not None:
                self._init_records(record_types)
        self._supported_record_type_ids = self._my_map['recordTypeIds']

    def _init_metadata(self, **kwargs):
        ${init_object}._init_metadata(self, **kwargs)
${metadata_initers}
    def _init_map(self, **kwargs):
        ${init_object}._init_map(self)
${persisted_initers}
    # These next three private methods should be moved to osid.Extensible??? (I thought they were already)
    def _load_records(self, record_type_idstrs):
        \"\"\"Load all records of record type for this form.\"\"\"
        for record_type_idstr in record_type_idstrs:
            self._init_record(record_type_idstr)

    def _init_records(self, record_types):
        \"\"\"Initalize all records for this form.\"\"\"
        for record_type in record_types:
            # This conditional was inserted on 7/11/14. It may prove problematic:
            if str(record_type) not in self._my_map['recordTypeIds']:
                self._init_record(str(record_type))
                self._my_map['recordTypeIds'].append(str(record_type))

    def _init_record(self, record_type_idstr):
        \"\"\"Initalize a record of record type.\"\"\"
        record_type_data = self._record_type_data_sets[Id(record_type_idstr).get_identifier()]
        module = importlib.import_module(record_type_data['module_path'])
        record = getattr(module, record_type_data['form_record_class_name'])
        self._records[record_type_idstr] = record(self)
"""

    get_group_metadata_template = """
        # Implemented from template for osid.resource.ResourceForm.get_group_metadata_template
        metadata = dict(self._${var_name}_metadata)
        metadata.update({'existing_${var_name}_values': self._my_map['${var_name_mixed}']})
        return Metadata(**metadata)"""

    get_avatar_metadata_template = """
        # Implemented from template for osid.resource.ResourceForm.get_group_metadata_template
        metadata = dict(self._${var_name}_metadata)
        metadata.update({'existing_${var_name}_values': self._my_map['${var_name_mixed}Id']})
        return Metadata(**metadata)"""

    set_group_template = """
        # Implemented from template for osid.resource.ResourceForm.set_group_template
        if ${arg0_name} is None:
            raise NullArgument()
        if self.get_${var_name}_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_${arg0_type}(${arg0_name}):
            raise InvalidArgument()
        self._my_map['${var_name_mixed}'] = ${arg0_name}"""

    clear_group_template = """
        # Implemented from template for osid.resource.ResourceForm.clear_group_template
        if (self.get_${var_name}_metadata().is_read_only() or
            self.get_${var_name}_metadata().is_required()):
            raise NoAccess()
        self._my_map['${var_name_mixed}'] = self._${var_name}_default"""

    set_avatar_template = """
        # Implemented from template for osid.resource.ResourceForm.set_avatar_template
        if ${arg0_name} is None:
            raise NullArgument()
        if self.get_${var_name}_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_id(${arg0_name}):
            raise InvalidArgument()
        self._my_map['${var_name_mixed}Id'] = str(${arg0_name})"""

    clear_avatar_template = """
        # Implemented from template for osid.resource.ResourceForm.clear_avatar_template
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise NoAccess()
        self._my_map['${var_name_mixed}Id'] = self._${var_name}_default"""

    get_resource_form_record_template = """
        # This is now in OsidExtensibleForm and can be replaces with:
        # return self._get_record(${arg0_name}):
        if ${arg0_name} is None:
            raise NullArgument()
        if not self.has_record_type(${arg0_name}):
            raise Unsupported()
        if str(${arg0_name}) not in self._records: # Currently this should never be True
            self._init_record(str(${arg0_name}))
            if str(${arg0_name}) not in self._my_map['recordTypeIds']: # nor this
                self._my_map['recordTypeIds'].append(str(${arg0_name}))
        return self._records[str(${arg0_name})]"""



class ResourceList:

    import_statements_pattern = [
        'from ..osid.osid_errors import * # pylint: disable=wildcard-import,unused-wildcard-import',
        'from ..primitives import Id',
    ]

    get_next_resource_template = """
        # Implemented from template for osid.resource.ResourceList.get_next_resource
        try:
            next_item = self.next()
        except StopIteration:
            raise IllegalState('no more elements available in this list')
        except: #Need to specify exceptions here
            raise OperationFailed()
        else:
            return next_item

    def next(self):
        try:
            next_item = osid_objects.OsidList.next(self)
        except:
            raise
        if isinstance(next_item, dict):
            next_item = ${return_type}(next_item, db_prefix=self._db_prefix, runtime=self._runtime)
        return next_item"""

    get_next_resources_template = """
    # Implemented from template for osid.resource.ResourceList.get_next_resources
        if ${arg0_name} > self.available():
            # !!! This is not quite as specified (see method docs) !!!
            raise IllegalState('not enough elements available in this list')
        else:
            next_list = []
            i = 0
            while i < ${arg0_name}:
                try:
                    next_list.append(self.next())
                except: #Need to specify exceptions here
                    raise OperationFailed()
                i = i + 1
            return next_list"""

class Bin:

    import_statements_pattern = [
        'import importlib',
    ]

    init_template = """
    try:
        from .records.types import ${object_name_upper}_RECORD_TYPES as _record_type_data_sets
    except (ImportError, AttributeError):
        _record_type_data_sets = dict()
    _namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, osid_catalog_map, db_prefix='', runtime=None):
        self._my_map = osid_catalog_map
        self._runtime = runtime
        self._db_prefix = db_prefix
        self._records = dict()
        # This check is here for transition purposes:
        try:
            self._load_records(osid_catalog_map['recordTypeIds'])
        except KeyError:
            print 'KeyError: recordTypeIds key not found in ', self._my_map['displayName']['text']
            self._load_records([]) # In place for transition purposes

    # These next two private methods should be moved to osid.Extensible??? (I thought they were already)
    def _load_records(self, record_type_idstrs):
        for record_type_idstr in record_type_idstrs:
            self._init_record(record_type_idstr)

    def _init_record(self, record_type_idstr):
        record_type_data = self._record_type_data_sets[Id(record_type_idstr).get_identifier()]
        module = importlib.import_module(record_type_data['module_path'])
        record = getattr(module, record_type_data['object_record_class_name'])
        self._records[record_type_idstr] = record(self)
"""

class BinForm:

    import_statements_pattern = [
        '#from ..osid.objects import OsidForm',
        '#from ..osid.objects import OsidObjectForm',
    ]

    init_template = """
    try:
        from .records.types import ${object_name_upper}_RECORD_TYPES as _record_type_data_sets
    except (ImportError, AttributeError):
        _record_type_data_sets = dict()
    _namespace = '${implpkg_name}.${object_name}'

    def __init__(self, osid_catalog_map=None, record_types=None, db_prefix='', runtime=None, **kwargs):
        #from ..osid.objects import OsidForm
        osid_objects.OsidForm.__init__(self)
        self._runtime = runtime
        self._db_prefix = db_prefix
        self._kwargs = kwargs
        self._init_metadata(**kwargs)
        self._records = dict()
        if osid_catalog_map is not None:
            self._for_update = True
            self._my_map = osid_catalog_map
            self._load_records(osid_catalog_map['recordTypeIds'])
        else:
            self._my_map = {}
            self._for_update = False
            self._init_map(**kwargs)
            if record_types is not None:
                self._init_records(record_types)
        self._supported_record_type_ids = self._my_map['recordTypeIds']

    def _init_metadata(self, **kwargs):
        osid_objects.OsidObjectForm._init_metadata(self)

    def _init_map(self):
        #from ..osid.objects import OsidObjectForm
        osid_objects.OsidObjectForm._init_map(self)

    # These next three private methods should be moved to osid.Extensible??? (I thought they were already)
    def _load_records(self, record_type_idstrs):
        \"\"\"Load all records of record type for this catalog.\"\"\"
        for record_type_idstr in record_type_idstrs:
            self._init_record(record_type_idstr)

    def _init_records(self, record_types):
        \"\"\"Initalize all records for this catalog.\"\"\"
        for record_type in record_types:
            # This conditional was inserted on 7/11/14. It may prove problematic:
            if str(record_type) not in self._my_map['recordTypeIds']:
                self._init_record(str(record_type))
                self._my_map['recordTypeIds'].append(str(record_type))

    def _init_record(self, record_type_idstr):
        \"\"\"Initalize a record of record type.\"\"\"
        record_type_data = self._record_type_data_sets[Id(record_type_idstr).get_identifier()]
        module = importlib.import_module(record_type_data['module_path'])
        record = getattr(module, record_type_data['form_record_class_name'])
        self._records[record_type_idstr] = record(self)

"""
