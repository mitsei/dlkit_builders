class ResourceProfile:

    supports_visible_federation_template = """
        # Implemented from template for osid.resource.ResourceProfile.supports_visible_federation
        from . import profile
        return '${method_name}' in profile.SUPPORTS"""

    supports_resource_lookup_template = """
        # Implemented from template for osid.resource.ResourceProfile.supports_resource_lookup
        from . import profile
        return '${method_name}' in profile.SUPPORTS"""

    get_resource_record_types_template = """
        from ..primitives import Type
        from ..type.objects import TypeList
        try:
            from .records import types
            ${object_name_under}_record_types = types.${object_name_upper}_RECORD_TYPES
        except (ImportError, AttributeError):
            return TypeList([])
        record_types = []
        for rt in ${object_name_under}_record_types:
            record_types.append(Type(**${object_name_under}_record_types[rt]))
        return TypeList(record_types, count=len(record_types))"""

    supports_resource_record_type_template = """
        from ..primitives import Type
        from ..osid.osid_errors import NullArgument
        if ${arg0_name} is None:
            raise NullArgument()
        try:
            from .records import types
            ${object_name_under}_record_types = types.${object_name_upper}_RECORD_TYPES
        except (ImportError, AttributeError):
            return False
        supports = False
        for rt in ${object_name_under}_record_types:
            if (${arg0_name}.get_authority() == ${object_name_under}_records[rt]['authority'] and
                ${arg0_name}.get_identifier_namespace() == ${object_name_under}_records[rt]['namespace'] and
                ${arg0_name}.get_identifier() == ${object_name_under}_records[rt]['identifier']):
                supports = True
        return supports"""

class ResourceManager:

    import_statements_pattern = [
    'from ..osid.osid_errors import *'
    ]

    get_resource_lookup_session_template = """
        if not self.supports_${support_check}():
            raise Unimplemented()
        try:
            from . import ${return_module}
        except ImportError:
            raise #OperationFailed()
        try:
            session = ${return_module}.${return_type}()
        except AttributeError:
            raise #OperationFailed()
        return session"""

    get_resource_lookup_session_for_bin_template = """
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
            session = ${return_module}.${return_type}(${arg0_name})
#            session = ${return_module}.${return_type}(${arg0_name}.get_identifier())
        except AttributeError:
            raise #OperationFailed()
        return session"""

class ResourceProxyManager:

    get_resource_lookup_session_template = """
        if proxy is None:
            raise NullArgument()
        if not self.supports_${support_check}():
            raise Unimplemented()
        try:
            from . import ${return_module}
        except ImportError:
            raise OperationFailed()
        try:
            session = ${return_module}.${return_type}(proxy)
        except AttributeError:
            raise OperationFailed()
        return session"""

    get_resource_lookup_session_for_bin_template = """
        if not ${arg0_name} or proxy is None:
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
            session = ${return_module}.${return_type}(${arg0_name}, proxy)
#            session = ${return_module}.${return_type}(${arg0_name}.get_identifier())
        except AttributeError:
            raise #OperationFailed()
        return session"""

    old_get_resource_lookup_session_template = """
        return ${non_proxy_interface_name}().${method_name}()"""

    old_get_resource_lookup_session_for_bin_template = """
        return ${non_proxy_interface_name}().${method_name}(${arg0_name})"""

class ResourceLookupSession:

    init_template = """
    def __init__(self, catalog_id = None, proxy = None):
        from .objects import ${cat_name}
        self._catalog_class = ${cat_name}
        from ..osid.sessions import OsidSession
        self._session_name = '${interface_name}'
        self._catalog_name = '${cat_name}'
        OsidSession._init_object(self, catalog_id, proxy, db_name='${pkg_name}', cat_name='${cat_name}', cat_class=${cat_name})
        self._object_view = self.COMPARATIVE
        self._catalog_view = self.ISOLATED
"""

    old_init_template = """
    from bson.objectid import ObjectId
    _session_name = '${interface_name}'

    def __init__(self, catalog_id = None, *args, **kwargs):
        from pymongo import MongoClient
        from bson.objectid import ObjectId
        from .objects import ${cat_name}
        from ..osid.sessions import OsidSession
        from ..osid.osid_errors import NotFound
        from . import profile
        OsidSession.__init__(self, *args, **kwargs)
        collection = MongoClient()['${pkg_name}']['${cat_name}']
        if catalog_id is not None and catalog_id.get_identifier() != '000000000000000000000000':
            self._catalog_identifier = catalog_id.get_identifier()
            self._my_catalog_map = collection.find_one({'_id': ObjectId(self._catalog_identifier)})
            if self._my_catalog_map is None:
                raise NotFound('could not find catalog identifier ' + catalog_id.get_identifier())
        else:
            from ..primitives import Id, Type
            from .. import types
            self._catalog_identifier = '000000000000000000000000'
            self._my_catalog_map = {
                '_id': ObjectId(self._catalog_identifier),
                'displayName': {'text': 'Default Catalog',
                                'languageType': str(Type(**types.Language().get_type_data('DEFAULT'))),
                                'scriptType': str(Type(**types.Script().get_type_data('DEFAULT'))),
                                'formatType': str(Type(**types.Format().get_type_data('DEFAULT'))),},
                'description': {'text': 'The Default Catalog, a Phantom Root Level Catalog',
                                'languageType': str(Type(**types.Language().get_type_data('DEFAULT'))),
                                'scriptType': str(Type(**types.Script().get_type_data('DEFAULT'))),
                                'formatType': str(Type(**types.Format().get_type_data('DEFAULT'))),},
                'genusType': str(Type(**types.Genus().get_type_data('DEFAULT')))
            }
        self._catalog = ${cat_name}(self._my_catalog_map) # This may have gone in a circle
        self._catalog_id = self._catalog.get_id()
        self._object_view = self.COMPARATIVE
        self._catalog_view = self.ISOLATED
"""

    get_bin_id_template = """
        # Implemented from template for osid.resource.ResourceLookupSession.get_bin_id
        return self._catalog_id"""

    get_bin_template = """
        # Implemented from template for osid.resource.ResourceLookupSession.get_bin
        from ..osid.osid_errors import OperationFailed, PermissionDenied
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
        self._object_view = self.COMPARATIVE"""

    use_plenary_resource_view_template = """
        # Implemented from template for 
        # osid.resource.ResourceLookupSession.use_plenary_resource_view
        self._object_view = self.PLENARY"""

    use_federated_bin_view_template = """
        # Implemented from template for 
        # osid.resource.ResourceLookupSession.use_federated_bin_view
        self._catalog_view = self.FEDERATED"""

    use_isolated_bin_view_template = """
        # Implemented from template for 
        # osid.resource.ResourceLookupSession.use_isolated_bin_view
        self._catalog_view = self.ISOLATED"""

    get_resource_template = """
        # Implemented from template for 
        # osid.resource.ResourceLookupSession.get_resource
        # NOTE: This implementation currently ignores plenary view
        from bson.objectid import ObjectId
        from pymongo import MongoClient
        collection = MongoClient()['${package_name}']['${object_name}']
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import NotFound, NullArgument, OperationFailed, PermissionDenied
        if not ${arg0_name}:
            raise NullArgument()
        if self._catalog_view == self.ISOLATED:
            result = collection.find_one({'$$and': [{'_id': ObjectId(${arg0_name}.get_identifier())},
                                          {'${cat_name_mixed}Id': str(self._catalog_id)}]})
        else:
            result = collection.find_one({'_id': ObjectId(${arg0_name}.get_identifier())})
        if result is None:
            raise NotFound()
        return ${return_type}(result)"""

    get_resources_by_ids_template = """
        # Implemented from template for 
        # osid.resource.ResourceLookupSession.get_resources_by_ids
        # NOTE: This implementation currently ignores plenary view
        from bson.objectid import ObjectId
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import NotFound, NullArgument, OperationFailed, PermissionDenied
        from pymongo import MongoClient
        collection = MongoClient()['${package_name}']['${object_name}']
        if not ${arg0_name}:
            raise NullArgument()
        object_id_list = []
        for i in ${arg0_name}:
            object_id_list.append(ObjectId(i.get_identifier()))
        if self._catalog_view == self.ISOLATED:
            result = collection.find({'_id': {'$$in': object_id_list},
                                     '${cat_name_mixed}Id': str(self._catalog_id)})
            count = collection.find({'_id': {'$$in': object_id_list},
                                     '${cat_name_mixed}Id': str(self._catalog_id)}).count()
        else:
            result = collection.find({'_id': {'$$in': object_id_list}})
            count = collection.find({'_id': {'$$in': object_id_list}}).count()
        return ${return_type}(result, count)"""

    get_resources_by_genus_type_template = """
        # Implemented from template for 
        # osid.resource.ResourceLookupSession.get_resources_by_genus_type
        # NOTE: This implementation currently ignores plenary view
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import OperationFailed, PermissionDenied
        from pymongo import MongoClient
        collection = MongoClient()['${package_name}']['${object_name}']
        if self._catalog_view == self.ISOLATED:
            result = collection.find({'genusTypeId': str(${arg0_name}),
                                     '${cat_name_mixed}Id': str(self._catalog_id)})
            count = collection.find({'genusTypeId': str(${arg0_name}),
                                     '${cat_name_mixed}Id': str(self._catalog_id)}).count()
        else:
            result = collection.find({'genusTypeId': str(${arg0_name})})
            count = collection.find({'genusTypeId': str(${arg0_name})}).count()
        return ${return_type}(result, count)"""

    get_resources_by_parent_genus_type_template = """
        # Implemented from template for 
        # osid.resource.ResourceLookupSession.get_resources_by_parent_genus_type
        # WILL THIS DEPEND ON A TYPE HIERARCHY SERVICE???
        from .${return_module} import ${return_type}
        return ${return_type}([])"""

    get_resources_by_record_type_template = """
        # Implemented from template for 
        # osid.resource.ResourceLookupSession.get_resources_by_record_type
        # STILL NEED TO FIGURE OUT HOW TO DO RECORDS!!!
        from .${return_module} import ${return_type}
        return ${return_type}([])"""

    get_resources_template = """
        # Implemented from template for 
        # osid.resource.ResourceLookupSession.get_resources
        # NOTE: This implementation currently ignores plenary view
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import OperationFailed, PermissionDenied
        from pymongo import MongoClient
        collection = MongoClient()['${package_name}']['${object_name}']
        if self._catalog_view == self.ISOLATED:
            result = collection.find({'${cat_name_mixed}Id': str(self._catalog_id)})
            count = collection.find({'${cat_name_mixed}Id': str(self._catalog_id)}).count()
        else:
            result = collection.find()
            count = collection.count()
        return ${return_type}(result, count)"""

class ResourceAdminSession:

    init_template = """
    def __init__(self, catalog_id = None, proxy = None):
        from .objects import ${cat_name}
        from ..osid.sessions import OsidSession
        self._catalog_class = ${cat_name}
        self._session_name = '${interface_name}'
        self._catalog_name = '${cat_name}'
        OsidSession._init_object(self, catalog_id, proxy, db_name='${pkg_name}', cat_name='${cat_name}', cat_class=${cat_name})
        self._forms = dict()
"""

    pld_init_template = """
    _session_name = '${interface_name}'

    def __init__(self, catalog_id = None, *args, **kwargs):
        from pymongo import MongoClient
        from bson.objectid import ObjectId
        from .objects import ${cat_name}
        from ..primitives import Id, Type
        from .. import types
        from ..osid.sessions import OsidSession
        from ..osid.osid_errors import NotFound
        from . import profile
        OsidSession.__init__(self, *args, **kwargs)
        from pymongo import MongoClient
        collection = MongoClient()['${pkg_name}']['${cat_name}']
        if catalog_id is not None and catalog_id.get_identifier() != '000000000000000000000000':
            self._catalog_identifier = catalog_id.get_identifier()
            self._my_catalog_map = collection.find_one({'_id': ObjectId(self._catalog_identifier)})
            if self._my_catalog_map is None:
                # Should also check for the authority here:
                if catalog_id.get_identifier_namespace() != '${pkg_name}.${cat_name}':
                    self._my_catalog_map = {
                        '_id': ObjectId(catalog_id.get_identifier()),
                        'displayName': {'text': catalog_id.get_identifier_namespace() + ' ${cat_name}',
                                        'languageType': str(Type(**types.Language().get_type_data('DEFAULT'))),
                                        'scriptType': str(Type(**types.Script().get_type_data('DEFAULT'))),
                                        'formatType': str(Type(**types.Format().get_type_data('DEFAULT'))),},
                        'description': {'text': '${cat_name} for ' + catalog_id.get_identifier_namespace() + ' objects',
                                        'languageType': str(Type(**types.Language().get_type_data('DEFAULT'))),
                                        'scriptType': str(Type(**types.Script().get_type_data('DEFAULT'))),
                                        'formatType': str(Type(**types.Format().get_type_data('DEFAULT'))),},
                        'genusType': str(Type(**types.Genus().get_type_data('DEFAULT')))
                    }
                    collection.insert(self._my_catalog_map)
                else:
                    raise NotFound('could not find catalog identifier ' + catalog_id.get_identifier())
        else:
            self._catalog_identifier = '000000000000000000000000'
            self._my_catalog_map = {
                '_id': ObjectId(self._catalog_identifier),
                'displayName': {'text': 'Default ${cat_name}',
                                'languageType': str(Type(**types.Language().get_type_data('DEFAULT'))),
                                'scriptType': str(Type(**types.Script().get_type_data('DEFAULT'))),
                                'formatType': str(Type(**types.Format().get_type_data('DEFAULT'))),},
                'description': {'text': 'The Default ${cat_name}',
                                'languageType': str(Type(**types.Language().get_type_data('DEFAULT'))),
                                'scriptType': str(Type(**types.Script().get_type_data('DEFAULT'))),
                                'formatType': str(Type(**types.Format().get_type_data('DEFAULT'))),},
                'genusType': str(Type(**types.Genus().get_type_data('DEFAULT')))
            }
        self._catalog = ${cat_name}(self._my_catalog_map)
        self._catalog_id = self._catalog.get_id()
        self._forms = dict()
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
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import NullArgument, InvalidArgument, OperationFailed, PermissionDenied, Unsupported
        CREATED = True
        if ${arg0_name} is None:
            raise NullArgument()
        for arg in ${arg0_name}:
            if not isinstance(arg, ABC${arg0_type}):
                raise InvalidArgument('one or more argument array elements is not a valid OSID ${arg0_type}')
        if ${arg0_name} == []:
            obj_form = ${return_type}(${cat_name_under}_id = self._catalog_id)
        else:
            obj_form = ${return_type}(${cat_name_under}_id = self._catalog_id, record_types = ${arg0_name})
        #obj_form._for_update = False # This seems redundant
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form"""

    create_resource_template = """
        # Implemented from template for 
        # osid.resource.ResourceAdminSession.create_resource_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from ..osid.osid_errors import IllegalState, InvalidArgument, NullArgument, OperationFailed, PermissionDenied, Unsupported
        from pymongo import MongoClient
        collection = MongoClient()['${package_name}']['${object_name}']
        CREATED = True
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
        from .${return_module} import ${return_type}
        self._forms[${arg0_name}.get_id().get_identifier()] = CREATED
        return ${return_type}(collection.find_one({'_id': id_}))"""

    get_resource_form_for_update_template = """
        # Implemented from template for 
        # osid.resource.ResourceAdminSession.get_resource_form_for_update_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import NotFound, NullArgument, InvalidArgument, OperationFailed, PermissionDenied, Unsupported
        from bson.objectid import ObjectId
        from pymongo import MongoClient
        collection = MongoClient()['${package_name}']['${object_name}']
        UPDATED = True
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        result = collection.find_one({'_id': ObjectId(${arg0_name}.get_identifier())})
        if result == '':
            raise NotFound()
        obj_form = ${return_type}(result)
        #obj_form._for_update = True # This seems redundant
        self._forms[obj_form.get_id().get_identifier()] = not UPDATED
        return obj_form"""

    update_resource_template = """
        # Implemented from template for 
        # osid.resource.ResourceAdminSession.update_resource_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from ..osid.osid_errors import IllegalState, InvalidArgument, NullArgument, OperationFailed, PermissionDenied, Unsupported
        from pymongo import MongoClient
        collection = MongoClient()['${package_name}']['${object_name}']
        UPDATED = True
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
        try:
            result = collection.save(${arg0_name}._my_map)
        except: # what exceptions does mongodb save raise?
            raise OperationFailed()
        self._forms[${arg0_name}.get_id().get_identifier()] = UPDATED
        # Note: this is out of spec. The OSIDs don't require an object to be returned:
        from .${return_module} import ${return_type}
        return ${return_type}(${arg0_name}._my_map)
        """

    delete_resource_template = """
        # Implemented from template for 
        # osid.resource.ResourceAdminSession.delete_resource_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from ..osid.osid_errors import NotFound, NullArgument, InvalidArgument, OperationFailed, PermissionDenied, Unsupported
        from .objects import ${object_name}
        from bson.objectid import ObjectId
        from pymongo import MongoClient
        collection = MongoClient()['${package_name}']['${object_name}']
        UPDATED = True
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            return InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        ${object_name_under}_map = collection.find_one({'_id': ObjectId(${arg0_name}.get_identifier())})
        if ${object_name_under}_map is None:
            raise NotFound()
        ${object_name}(${object_name_under}_map)._delete()
        result = collection.remove({'_id': ObjectId(${arg0_name}.get_identifier())}, justOne=True)
        if 'err' in result and result['err'] is not None:
            raise OperationFailed()
#        if result['n'] == 0: This is probably redundant
#            raise NotFound()"""


    alias_resources_template = """
        # Implemented from template for 
        # osid.resource.ResourceAdminSession.alias_resources_template
        from ..osid.osid_errors import Unimplemented
        # NEED TO FIGURE OUT HOW TO IMPLEMENT THIS SOMEDAY
        raise Unimplemented()"""


class BinLookupSession:
    
    init_template = """
    _session_name = '${interface_name}'

    def __init__(self, catalog_identifier = None, *args, **kwargs):
        from pymongo import MongoClient
        from .objects import ${cat_name}
        from ..osid.sessions import OsidSession
        from ..osid.osid_errors import NotFound
        from . import profile
        OsidSession._init_catalog(self, *args, **kwargs)
        self._catalog_view = self.COMPARATIVE
"""

    use_comparative_bin_view_template = """
        # Implemented from template for 
        # osid.resource.BinLookupSession.use_comparative_bin_view
        self._catalog_view = self.COMPARATIVE"""

    use_plenary_bin_view_template = """
        # Implemented from template for 
        # osid.resource.BinLookupSession.use_plenary_bin_view
        self._catalog_view = self.PLENARY"""

    get_bin_template = """
        # Implemented from template for 
        # osid.resource.BinLookupSession.get_bin
        from bson.objectid import ObjectId
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import NotFound, NullArgument, OperationFailed, PermissionDenied
        from pymongo import MongoClient
        collection = MongoClient()['${package_name}']['${cat_name}']
        if not ${arg0_name}:
            raise NullArgument()
        result = collection.find_one({'_id': ObjectId(${arg0_name}.get_identifier())})
        if result is None:
            raise NotFound()
        return ${return_type}(result)"""

    get_bins_by_ids_template = """
        # Implemented from template for 
        # osid.resource.BinLookupSession.get_bins_by_ids_template
        # NOTE: This implementation currently ignores plenary view
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import OperationFailed, PermissionDenied
        from bson.objectid import ObjectId
        catalog_id_list = []
        for i in ${arg0_name}:
            catalog_id_list.append(ObjectId(i.get_identifier()))
        from pymongo import MongoClient
        collection = MongoClient()['${package_name}']['${cat_name}']
        result = collection.find({'_id': {'$$in': catalog_id_list}})
        count = collection.find({'_id': {'$$in': catalog_id_list}}).count()
        return ${return_type}(result, count)"""


    get_bins_template = """
        # Implemented from template for 
        # osid.resource.BinLookupSession.get_bins_template
        # NOTE: This implementation currently ignores plenary view
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import OperationFailed, PermissionDenied
        from pymongo import MongoClient
        collection = MongoClient()['${package_name}']['${cat_name}']
        result = collection.find()
        count = collection.count()
        return ${return_type}(result, count)"""

class BinAdminSession:

    init_template = """
    _session_name = '${interface_name}'

    def __init__(self, catalog_identifier = None, *args, **kwargs):
        from .objects import ${cat_name}
        from ..osid.sessions import OsidSession
        from ..osid.osid_errors import NotFound
        OsidSession._init_catalog(self, *args, **kwargs)
        self._forms = dict()
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
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import NullArgument, InvalidArgument, OperationFailed, PermissionDenied, Unsupported
        CREATED = True
        if ${arg0_name} is None:
            raise NullArgument()
        for arg in ${arg0_name}:
            if not isinstance(arg, ABC${arg0_type}):
                raise InvalidArgument('one or more argument array elements is not a valid OSID ${arg0_type}')
        if ${arg0_name} == []:
            result = ${return_type}()
        else:
            result = ${return_type}(record_types = ${arg0_name})
        result._for_update = False
        self._forms[result.get_id().get_identifier()] = not CREATED
        return result"""

    create_bin_template = """
        # Implemented from template for 
        # osid.resource.BinAdminSession.create_bin_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from ..osid.osid_errors import IllegalState, InvalidArgument, NullArgument, OperationFailed, PermissionDenied, Unsupported
        from pymongo import MongoClient
        collection = MongoClient()['${package_name}']['${cat_name}']
        CREATED = True
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
        from .${return_module} import ${return_type}
        self._forms[${arg0_name}.get_id().get_identifier()] = CREATED
        return ${return_type}(collection.find_one({'_id': id_}))"""

    get_bin_form_for_update_template = """
        # Implemented from template for 
        # osid.resource.BinAdminSession.get_bin_form_for_update_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import NotFound, NullArgument, InvalidArgument, OperationFailed, PermissionDenied, Unsupported
        from bson.objectid import ObjectId
        from pymongo import MongoClient
        collection = MongoClient()['${package_name}']['${cat_name}']
        UPDATED = True
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            return InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        result = collection.find_one({'_id': ObjectId(${arg0_name}.get_identifier())})
        if result is None:
            raise NotFound()
        cat_form = ${return_type}(result)
        cat_form._for_update = True
        self._forms[cat_form.get_id().get_identifier()] = not UPDATED
        return cat_form"""

    update_bin_template = """
        # Implemented from template for 
        # osid.resource.BinAdminSession.update_bin_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from ..osid.osid_errors import IllegalState, InvalidArgument, NullArgument, OperationFailed, PermissionDenied, Unsupported
        from pymongo import MongoClient
        collection = MongoClient()['${package_name}']['${cat_name}']
        UPDATED = True
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
        try:
            result = collection.save(${arg0_name}._my_map)
        except: # what exceptions does mongodb save raise?
            raise OperationFailed()
        self._forms[${arg0_name}.get_id().get_identifier()] = UPDATED
        # Note: this is out of spec. The OSIDs don't require an object to be returned
        from .${return_module} import ${return_type}
        return ${return_type}(${arg0_name}._my_map)"""

    delete_bin_template = """
        # Implemented from template for 
        # osid.resource.BinAdminSession.delete_bin_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from ..osid.osid_errors import NotFound, NullArgument, InvalidArgument, OperationFailed, PermissionDenied, Unsupported, IllegalState
        from bson.objectid import ObjectId
        from pymongo import MongoClient
        collection = MongoClient()['${package_name}']['${cat_name}']
        UPDATED = True
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            return InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        for object_catalog in ${cataloged_object_caps_list}:
            obj_collection = MongoClient()['${package_name}'][object_catalog]
            if obj_collection.find({'${cat_name_mixed}Id': str(${arg0_name})}).count() != 0:
                raise IllegalState('catalog is not empty')
        result = collection.remove({'_id': ObjectId(${arg0_name}.get_identifier())})
                                   # Tried using justOne above but pymongo doesn't support it
        if 'err' in result and result['err'] is not None:
            raise OperationFailed()
        if result['n'] == 0:
            raise NotFound()"""

    alias_bin_template = """
        # Implemented from template for 
        # osid.resource.BinLookupSession.alias_bin_template
        from ..osid.osid_errors import Unimplemented
        # NEED TO FIGURE OUT HOW TO IMPLEMENT THIS SOMEDAY
        raise Unimplemented()"""


class Resource:
    
    import_statements = [] # this is where you might insert one-off import statements

    import_statements_pattern = [
        'from ..osid.osid_errors import *',
        'from ..primitives import Id, Type, DisplayText',
    ]

    init_template = """
    try:
        from .records.types import ${object_name_upper}_RECORD_TYPES as _record_type_data_sets
    except ImportError, AttributeError:
        _record_type_data_sets = {}
    _namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, osid_object_map, **kwargs):
        self._my_map = osid_object_map
        self._records = dict()
        self._load_records(osid_object_map['recordTypeIds'])
${instance_initers}
    def _load_records(self, record_type_idstrs):
        for record_type_idstr in record_type_idstrs:
            self._init_record(record_type_idstr)

    def _init_record(self, record_type_idstr):
        import importlib
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
            from ..${return_implpkg_name} import managers
        except ImportError:
            raise OperationFailed('failed to import ${return_app_name}.${return_implpkg_name}.managers')
        try:
            mgr = managers.${return_pkg_title}Manager()
        except:
            raise OperationFailed('failed to instantiate ${return_pkg_title}Manager')
        if not mgr.supports_${return_type_under}_lookup():
            raise OperationFailed('${return_pkg_title} does not support ${return_type} lookup')
        try:
            osidObject = mgr.get_${return_type_under}_lookup_session().get${return_type_under}(self.get_${var_name}_id())
        except:
            raise OperationFailed()
        else:
            return osidObject"""

    get_resource_record_template = """
        if ${arg0_name} is None:
            raise NullArgument()
        if not self.has_record_type(${arg0_name}):
            raise Unsupported()
        if str(${arg0_name}) not in self._records:
            raise Unimplemented()
        return self._records[str(${arg0_name})]"""

class ResourceForm:

    import_statements_pattern = [
        'import importlib',
        'from ..osid.osid_errors import *',
        'from ..primitives import *',
        'from ..osid.objects import OsidForm',
        'from ..osid.objects import OsidObjectForm',
        'from ..osid.objects import OsidList',
        'from ..osid.metadata import Metadata',
        'from . import mdata_conf'
    ]

    init_template = """
    try:
        from .records.types import ${object_name_upper}_RECORD_TYPES as _record_type_data_sets
    except ImportError, AttributeError:
        _record_type_data_sets = {}
    _namespace = '${implpkg_name}.${object_name}'

    def __init__(self, osid_object_map=None, **kwargs):
        OsidForm.__init__(self)
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
            if 'record_types' in kwargs:
                self._init_records(kwargs['record_types'])
        self._supported_record_type_ids = self._my_map['recordTypeIds']
        self._kwargs = kwargs

    def _init_metadata(self, **kwargs):
        OsidObjectForm._init_metadata(self)
${metadata_initers}
    def _init_map(self, **kwargs):
        OsidObjectForm._init_map(self)
${persisted_initers}
    def _load_records(self, record_type_idstrs):
        for record_type_idstr in record_type_idstrs:
            self._init_record(record_type_idstr)

    def _init_records(self, record_types):
        for record_type in record_types:
            # This conditional was inserted on 7/11/14. It may prove problematic:
            if str(record_type) not in self._my_map['recordTypeIds']:
                self._init_record(str(record_type))
                self._my_map['recordTypeIds'].append(str(record_type))
  
    def _init_record(self, record_type_idstr):
        record_type_data = self._record_type_data_sets[Id(record_type_idstr).get_identifier()]
        module = importlib.import_module(record_type_data['module_path'])
        record = getattr(module, record_type_data['form_record_class_name'])
        self._records[record_type_idstr] = record(self)
"""

    get_group_metadata_template = """
        # Implemented from template for osid.resource.ResourceForm.get_group_metadata_template
        return Metadata(**self._${var_name}_metadata)"""

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
        if not self._is_valid_${arg0_type}(${arg0_name}, 
                                self.get_${var_name}_metadata()):
            raise InvalidArgument()
        self._my_map['${var_name_mixed}Id'] = str(${arg0_name})"""

    clear_avatar_template = """
        # Implemented from template for osid.resource.ResourceForm.clear_avatar_template
        if (self.get_${var_name}_metadata().is_read_only() or
            self.get_${var_name}_metadata().is_required()):
            raise NoAccess()
        self._my_map['${var_name_mixed}'] = self._${var_name}_default"""

    get_resource_form_record_template = """
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
        'from ..osid.osid_errors import *',
        'from ..primitives import *',
        'from ..osid.objects import OsidList'
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
        from .${return_module} import ${return_type} 
        try:
            next_item = OsidList.next(self)
        except:
            raise
        if isinstance(next_item, dict):
            next_item = ${return_type}(next_item)
        return next_item"""
            
    get_next_resources_template = """
    # Implemented from template for osid.resource.ResourceList.get_next_resources
        if ${arg0_name} > self.available():
            # !!! This is not quite as specified (see method docs) !!!
            raise IllegalState('not enough elements available in this list')
        else:
            next_list = []
            x = 0
            while x < ${arg0_name}:
                try:
                    next_list.append(self.next())
                except: #Need to specify exceptions here
                    raise OperationFailed()
                x = x + 1
            return next_list"""

class Bin:

    init_template = """
    _namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, osid_catalog_map):
        self._my_map = osid_catalog_map
"""

class BinForm:

    init_template = """
    _namespace = '${implpkg_name}.${object_name}'

    def __init__(self, osid_catalog_map = None, **kwargs):
        from ..osid.objects import OsidForm
        OsidForm.__init__(self)
        self._init_metadata()
        if osid_catalog_map is not None:
            self._my_map = osid_catalog_map
            self._for_update = True
        else:
            self._my_map = {}
            self._for_update = False
            self._init_map(**kwargs)

    def _init_metadata(self):
        from ..osid.objects import OsidObjectForm
        OsidObjectForm._init_metadata(self)

    def _init_map(self, **kwargs):
        from ..osid.objects import OsidObjectForm
        OsidObjectForm._init_map(self)
"""
