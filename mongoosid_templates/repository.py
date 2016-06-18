
class RepositoryProfile:

    get_coordinate_types_template = """
        # Implemented from template for
        # osid.repository.RepositoryProfile.get_coordinate_types
        return TypeList([])"""

    supports_coordinate_type_template = """
        # Implemented from template for
        # osid.repository.RepositoryProfile.supports_coordinate_type
        return False"""

class RepositoryManager:
    # This is here temporarily until Tom adds missing methods to RepositoryManager
    
    additional_methods = """
    @utilities.arguments_not_none
    def get_asset_composition_session_for_repository(self, repository_id):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        if not self.supports_asset_composition():
            raise errors.Unimplemented()
        ##
        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        ##
        return sessions.AssetCompositionSession(repository_id, runtime=self._runtime) # pylint: disable=no-member

    @utilities.arguments_not_none
    def get_asset_composition_design_session_for_repository(self, repository_id):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        if not self.supports_asset_composition():
            raise errors.Unimplemented()
        ##
        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        ##
        return sessions.AssetCompositionDesignSession(repository_id, runtime=self._runtime) # pylint: disable=no-member"""

class RepositoryProxyManager:
    # This is here temporarily until Tom adds missing methods to RepositoryProxyManager

    additional_methods = """
    @utilities.arguments_not_none
    def get_asset_composition_session_for_repository(self, repository_id, proxy):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        if not self.supports_asset_composition():
            raise errors.Unimplemented()
        ##
        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        ##
        return sessions.AssetCompositionSession(repository_id, proxy, runtime=self._runtime) # pylint: disable=no-member

    @utilities.arguments_not_none
    def get_asset_composition_design_session_for_repository(self, repository_id, proxy):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        if not self.supports_asset_composition():
            raise errors.Unimplemented()
        ##
        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        ##
        return sessions.AssetCompositionDesignSession(repository_id, proxy, runtime=self._runtime) # pylint: disable=no-member"""

class AssetAdminSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from bson.objectid import ObjectId',
        'from ..utilities import MongoClientValidated',
        'CREATED = True'
        'UPDATED = True',
    ]

    create_asset_content_template = """
        # Implemented from template for
        # osid.repository.AssetAdminSession.create_asset_content_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        collection = MongoClientValidated('${package_name}',
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
        ${arg0_name}._my_map['_id'] = ObjectId()
        ${object_name_under}_id = Id(${arg0_name}._my_map['${object_name_mixed}Id']).get_identifier()
        ${object_name_under} = collection.find_one(
            {'$$and': [{'_id': ObjectId(${object_name_under}_id)},
                       {'assigned' + self._catalog_name + 'Ids': {'$$in': [str(self._catalog_id)]}}]})
        ${object_name_under}['${aggregated_objects_name_mixed}'].append(${arg0_name}._my_map)
        result = collection.save(${object_name_under})

        self._forms[${arg0_name}.get_id().get_identifier()] = CREATED
        from .${return_module} import ${aggregated_object_name}
        return ${return_type}(osid_object_map=${arg0_name}._my_map,
                              runtime=self._runtime,
                              proxy=self._proxy)"""

    get_asset_content_form_for_update_template = """
        # Implemented from template for
        # osid.repository.AssetAdminSession.get_asset_content_form_for_update_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from .${return_module} import ${return_type}
        collection = MongoClientValidated('${package_name}',
                                          collection='${object_name}',
                                          runtime=self._runtime)
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        document = collection.find_one({'${aggregated_objects_name_mixed}._id': ObjectId(${arg0_name}.get_identifier())})
        for sub_doc in document['${aggregated_objects_name_mixed}']: # There may be a MongoDB shortcut for this
            if sub_doc['_id'] == ObjectId(${arg0_name}.get_identifier()):
                result = sub_doc
        obj_form = ${return_type}(osid_object_map=result,
                                  runtime=self._runtime,
                                  proxy=self._proxy)
        obj_form._for_update = True
        self._forms[obj_form.get_id().get_identifier()] = not UPDATED
        return obj_form"""

    update_asset_content_template = """
        # Implemented from template for
        # osid.repository.AssetAdminSession.update_asset_content_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        collection = MongoClientValidated('${package_name}',
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
        ${object_name_under}_id = Id(${arg0_name}._my_map['${object_name_under}Id']).get_identifier()
        ${object_name_under} = collection.find_one(
            {'$$and': [{'_id': ObjectId(${object_name_under}_id)},
                       {'assigned' + self._catalog_name + 'Ids': {'$$in': [str(self._catalog_id)]}}]})
        index = 0
        found = False
        for i in ${object_name_under}['${aggregated_objects_name_mixed}']:
            if i['_id'] == ObjectId(${arg0_name}._my_map['_id']):
                ${object_name_under}['${aggregated_objects_name_mixed}'].pop(index)
                ${object_name_under}['${aggregated_objects_name_mixed}'].insert(index, ${arg0_name}._my_map)
                found = True
                break
            index += 1
        if not found:
            raise errors.NotFound()
        try:
            collection.save(${object_name_under})
        except: # what exceptions does mongodb save raise?
            raise errors.OperationFailed()
        self._forms[${arg0_name}.get_id().get_identifier()] = UPDATED
        # Note: this is out of spec. The OSIDs don't require an object to be returned:
        from .objects import ${aggregated_object_name}

        return ${aggregated_object_name}(osid_object_map=${arg0_name}._my_map,
                                         runtime=self._runtime,
                                         proxy=self._proxy)"""

    delete_asset_content_template = """
        # Implemented from template for
        # osid.repository.AssetAdminSession.delete_asset_content_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from .objects import ${aggregated_object_name}
        collection = MongoClientValidated('${package_name}',
                                          collection='${object_name}',
                                          runtime=self._runtime)
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        ${object_name_under} = collection.find_one({'${aggregated_objects_name_mixed}._id': ObjectId(${arg0_name}.get_identifier())})

        index = 0
        found = False
        for i in ${object_name_under}['${aggregated_objects_name_mixed}']:
            if i['_id'] == ObjectId(${arg0_name}.get_identifier()):
                ${aggregated_object_name_under}_map = ${object_name_under}['${aggregated_objects_name_mixed}'].pop(index)
            index += 1
            found = True
        if not found:
            raise errors.OperationFailed()
        ${aggregated_object_name}(osid_object_map=${aggregated_object_name_under}_map,
                                  runtime=self._runtime,
                                  proxy=self._proxy)._delete()
        collection.save(${object_name_under})"""


class CompositionLookupSession:

    import_statements = [
        'ACTIVE = 0',
        'ANY_STATUS = 1',
        'SEQUESTERED = 0',
        'UNSEQUESTERED = 1',
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
        return view_filter
"""

    use_active_composition_view_template = """
        # Implemented from template for
        # osid.repository.CompositionLookupSession.use_active_composition_view_template
        self._status_view = ACTIVE"""

    use_any_status_composition_view_template = """
        # Implemented from template for
        # osid.repository.CompositionLookupSession.use_any_status_composition_view_template
        self._status_view = ANY_STATUS"""

    use_sequestered_composition_view_template = """
        # Implemented from template for
        # osid.repository.CompositionLookupSession.use_sequestered_composition_view_template
        self._sequestered_view = SEQUESTERED"""

    use_unsequestered_composition_view_template = """
        # Implemented from template for
        # osid.repository.CompositionLookupSession.use_unsequestered_composition_view_template
        self._sequestered_view = UNSEQUESTERED"""


class CompositionQuerySession:

    import_statements = [
        'ACTIVE = 0',
        'ANY_STATUS = 1',
        'SEQUESTERED = 0',
        'UNSEQUESTERED = 1',
    ]

    init_template = CompositionLookupSession.init_template

    old_init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.Repository
        self._session_name = 'CompositionQuerySession'
        self._catalog_name = 'Repository'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='repository',
            cat_name='Repository',
            cat_class=objects.Repository)
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

    old_use_sequestered_composition_view = """ #NOW TEMPLATED FROM LOOKUP SESSION
        self._sequestered_view = SEQUESTERED"""

    old_use_unsequestered_composition_view = """ #NOW TEMPLATED LOOKUP SESSION
        self._sequestered_view = UNSEQUESTERED"""


class CompositionSearchSession:

    import_statements = [
        'from . import searches',
    ]


class AssetCompositionSession:

    import_statements = [
        'from dlkit.primordium.id.primitives import Id'
    ]

    import_statements_pattern = [
        'from dlkit.primordium.id.primitives import Id'
    ]

    old_init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.Repository
        self._session_name = 'AssetCompositionSession'
        self._catalog_name = 'Repository'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='repository',
            cat_name='Repository',
            cat_class=objects.Repository)
        self._kwargs = kwargs"""

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

    can_access_asset_compositions_template = """
        # Implemented from template for
        # osid.repository.AssetCompositionSession.can_access_asset_compositions
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    old_get_composition_assets = """
        collection = MongoClientValidated('repository',
                                          collection='Composition',
                                          runtime=self._runtime)
        composition = collection.find_one(
            dict({'_id': ObjectId(composition_id.get_identifier())},
                 **self._view_filter()))
        if 'assetIds' not in composition:
            raise errors.NotFound('no Assets are assigned to this Composition')
        asset_ids = []
        for idstr in composition['assetIds']:
            asset_ids.append(Id(idstr))
        mgr = self._get_provider_manager('REPOSITORY')
        als = mgr.get_asset_lookup_session(proxy=self._proxy)
        als.use_federated_repository_view()
        return als.get_assets_by_ids(asset_ids)"""

    get_composition_assets_template = """
        # Implemented from template for
        # osid.repository.AssetCompositionSession.get_composition_assets
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${containable_object_name}',
                                          runtime=self._runtime)
        ${containable_object_name_under} = collection.find_one(
            dict({'_id': ObjectId(${containable_object_name_under}_id.get_identifier())},
                 **self._view_filter()))
        if '${object_name_mixed}Ids' not in ${containable_object_name_under}:
            raise errors.NotFound('no ${object_name_plural} are assigned to this ${containable_object_name}')
        ${object_name_under}_ids = []
        for idstr in ${containable_object_name_under}['${object_name_mixed}Ids']:
            ${object_name_under}_ids.append(Id(idstr))
        mgr = self._get_provider_manager('${package_name_replace_upper}')
        lookup_session = mgr.get_${object_name_under}_lookup_session(proxy=self._proxy)
        lookup_session.use_federated_${cat_name_under}_view()
        return lookup_session.get_${object_name_plural_under}_by_ids(${object_name_under}_ids)"""

    old_get_compositions_by_asset = """
        collection = MongoClientValidated('repository',
                                          collection='Composition',
                                          runtime=self._runtime)
        result = collection.find(
            dict({'assetIds': {'$in': [str(asset_id)]}},
                 **self._view_filter())).sort('_id', DESCENDING)
        return objects.CompositionList(result, runtime=self._runtime)"""

    get_compositions_by_asset_template = """
        # Implemented from template for
        # osid.repository.AssetCompositionSession.get_compositions_by_asset
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${containable_object_name}',
                                          runtime=self._runtime)
        result = collection.find(
            dict({'${object_name_mixed}Ids': {'$$in': [str(${object_name_under}_id)]}},
                 **self._view_filter())).sort('_id', DESCENDING)
        return objects.${return_type}(result, runtime=self._runtime)"""


class AssetCompositionDesignSession:

    import_statements_pattern = [
        'from ..list_utilities import move_id_ahead, move_id_behind, order_ids',
    ]

    old_init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.Repository
        self._session_name = 'AssetCompositionDesignSession'
        self._catalog_name = 'Repository'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='repository',
            cat_name='Repository',
            cat_class=objects.Repository)
        self._kwargs = kwargs"""

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


    old_can_compose_assets = """
        return True"""

    can_compose_assets_template = """
        # Implemented from template for
        # osid.repository.AssetCompositionDesignSession.can_compose_assets_template
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    add_asset_template = """
        # The ${object_name_under} found check may want to be run through _get_provider_manager
        # so as to ensure access control:
        from ...abstract_osid.id.primitives import Id as ABCId
        if not isinstance(${object_name_under}_id, ABCId):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        if (not isinstance(${containable_object_name_under}_id, ABCId) and 
                ${containable_object_name_under}_id.get_identifier_namespace() != '${package_name_replace}.${containable_object_name}'):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        if ${object_name_under}_id.get_identifier_namespace() != '${object_namespace}':
            if ${object_name_under}_id.get_authority() != self._authority:
                raise errors.InvalidArgument()
            else:
                mgr = self._get_provider_manager('${object_package_name_replace_upper}')
                admin_session = mgr.get_${object_name_under}_admin_session_for_${cat_name_under}(self._catalog_id, proxy=self._proxy)
                ${object_name_under}_id = admin_session._get_${object_name_under}_id_with_enclosure(${object_name_under}_id)
        collection = MongoClientValidated('${object_package_name_replace}',
                                          collection='${object_name}',
                                          runtime=self._runtime)
        ${object_name_under} = collection.find_one({'_id': ObjectId(${object_name_under}_id.get_identifier())})
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${containable_object_name}',
                                          runtime=self._runtime)
        ${containable_object_name_under} = collection.find_one({'_id': ObjectId(${containable_object_name_under}_id.get_identifier())})
        if '${object_name_mixed}Ids' in ${containable_object_name_under}:
            if str(${object_name_under}_id) not in ${containable_object_name_under}['${object_name_mixed}Ids']:
                ${containable_object_name_under}['${object_name_mixed}Ids'].append(str(${object_name_under}_id))
        else:
            ${containable_object_name_under}['${object_name_mixed}Ids'] = [str(${object_name_under}_id)]
        collection.save(${containable_object_name_under})"""

    older_move_asset_ahead_template = """
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${containable_object_name}',
                                          runtime=self._runtime)
        ${containable_object_name_under} = collection.find_one({'_id': ObjectId(${containable_object_name_under}_id.get_identifier())})
        if '${object_name_mixed}Ids' not in ${containable_object_name_under}:
            raise errors.NotFound('no ${object_name_plural} are assigned to this ${containable_object_name}')
        ${containable_object_name_under}['${object_name_mixed}Ids'] = move_id_ahead(${object_name_under}_id, reference_id, ${containable_object_name_under}['${object_name_mixed}Ids'])
        collection.save(${containable_object_name_under})"""

    move_asset_ahead_template = """
        if (not isinstance(${containable_object_name_under}_id, ABCId) and 
                ${containable_object_name_under}_id.get_identifier_namespace() != '${package_name_replace}.${containable_object_name}'):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        ${containable_object_name_under}_map, collection = self._get_${containable_object_name_under}_collection(${containable_object_name_under}_id)
        ${containable_object_name_under}_map['${object_name_mixed}Ids'] = move_id_ahead(${object_name_under}_id, reference_id, ${containable_object_name_under}_map['${object_name_mixed}Ids'])
        collection.save(${containable_object_name_under}_map)"""

    older_move_asset_behind_template = """
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${containable_object_name}',
                                          runtime=self._runtime)
        ${containable_object_name_under} = collection.find_one({'_id': ObjectId(${containable_object_name_under}_id.get_identifier())})
        if '${object_name_mixed}Ids' not in ${containable_object_name_under}:
            raise errors.NotFound('no ${object_name_plural} are assigned to this ${containable_object_name}')
        ${containable_object_name_under}['${object_name_mixed}Ids'] = move_id_behind(${object_name_under}_id, reference_id, ${containable_object_name_under}['${object_name_mixed}Ids'])
        collection.save(${containable_object_name_under})"""

    move_asset_behind_template = """
        if (not isinstance(${containable_object_name_under}_id, ABCId) and 
                ${containable_object_name_under}_id.get_identifier_namespace() != '${package_name_replace}.${containable_object_name}'):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        ${containable_object_name_under}_map, collection = self._get_${containable_object_name_under}_collection(${containable_object_name_under}_id)
        ${containable_object_name_under}_map['${object_name_mixed}Ids'] = move_id_behind(${object_name_under}_id, reference_id, ${containable_object_name_under}_map['${object_name_mixed}Ids'])
        collection.save(${containable_object_name_under}_map)"""

    older_order_assets_template = """
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${containable_object_name}',
                                          runtime=self._runtime)
        ${containable_object_name_under} = collection.find_one({'_id': ObjectId(${containable_object_name_under}_id.get_identifier())})
        if '${object_name_mixed}Ids' not in ${containable_object_name_under}:
            raise errors.NotFound('no ${object_name_plural} are assigned to this ${containable_object_name}')
        ${containable_object_name_under}['${object_name_mixed}Ids'] = order_ids(${object_name_under}_ids, ${containable_object_name_under}['${object_name_mixed}Ids'])
        collection.save(${containable_object_name_under})"""

    order_assets_template = """
        if (not isinstance(${containable_object_name_under}_id, ABCId) and 
                ${containable_object_name_under}_id.get_identifier_namespace() != '${package_name_replace}.${containable_object_name}'):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        ${containable_object_name_under}_map, collection = self._get_${containable_object_name_under}_collection(${containable_object_name_under}_id)
        ${containable_object_name_under}_map['${object_name_mixed}Ids'] = order_ids(${object_name_under}_ids, ${containable_object_name_under}_map['${object_name_mixed}Ids'])
        collection.save(${containable_object_name_under}_map)"""

    older_remove_asset_template = """
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${containable_object_name}',
                                          runtime=self._runtime)
        ${containable_object_name_under} = collection.find_one({'_id': ObjectId(${containable_object_name_under}_id.get_identifier())})
        try:
            ${containable_object_name_under}['${object_name_mixed}Ids'].remove(str(${object_name_under}_id))
        except (KeyError, ValueError):
            raise errors.NotFound()
        collection.save(${containable_object_name_under})"""

    remove_asset_template = """
        if (not isinstance(${containable_object_name_under}_id, ABCId) and 
                ${containable_object_name_under}_id.get_identifier_namespace() != '${package_name_replace}.${containable_object_name}'):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        ${containable_object_name_under}_map, collection = self._get_${containable_object_name_under}_collection(${containable_object_name_under}_id)
        try:
            ${containable_object_name_under}_map['${object_name_mixed}Ids'].remove(str(${object_name_under}_id))
        except (KeyError, ValueError):
            raise errors.NotFound()
        collection.save(${containable_object_name_under}_map)

    def _get_${containable_object_name_under}_collection(self, ${containable_object_name_under}_id):
        \"\"\"Returns a Mongo Collection and ${containable_object_name} given a ${containable_object_name} Id\"\"\"
        collection = MongoClientValidated('${package_name_replace}',
                                          collection='${containable_object_name}',
                                          runtime=self._runtime)
        ${containable_object_name_under}_map = collection.find_one({'_id': ObjectId(${containable_object_name_under}_id.get_identifier())})
        if '${object_name_mixed}Ids' not in ${containable_object_name_under}_map:
            raise errors.NotFound('no ${object_name_plural} are assigned to this ${containable_object_name}')
        return ${containable_object_name_under}_map, collection
"""


class Asset:

    import_statements = [
        'from ..primitives import DisplayText',
        'from ..id.objects import IdList',
        'from ..osid.markers import Extensible'
    ]

    # Note: self._catalog_name = 'Repository' below is currently 
    # only for osid.OsidObject.get_object_map() setting the now deprecated
    # repositoryId element and may be removed someday
    init = """
    _namespace = 'repository.Asset'

    def __init__(self, **kwargs):
        osid_objects.OsidObject.__init__(self, object_name='ASSET', **kwargs)
        self._catalog_name = 'Repository'
        if self.is_composition():
            self._composition = self.get_composition()

    def __getattr__(self, name):
        if self.is_composition():
            try:
                return self._composition[name]
            except AttributeError:
                raise AttributeError()
        #HOW TO PASS TO EXTENSIBLE!!!!"""

    get_title_template = """
        # Implemented from template for osid.repository.Asset.get_title_template
        return DisplayText(self._my_map['${var_name_mixed}'])"""

    can_distribute_verbatim_template = """
        # Implemented from template for osid.repository.AssetForm.can_distribute_verbatim
        if self._my_map['${var_name_mixed}'] is None:
            raise errors.IllegalState()
        else:
            return self._my_map['${var_name_mixed}']"""

    get_asset_content_ids_template = """
        # Implemented from template for osid.repository.Asset.get_asset_content_ids_template
        id_list = []
        for ${var_name} in self.get_${var_name_plural}():
            id_list.append(${var_name}.get_id())
        return ${aggregated_object_name}List(id_list)"""

    get_asset_contents_template = """
        # Implemented from template for osid.repository.Asset.get_asset_contents_template
        return ${aggregated_object_name}List(self._my_map['${var_name_plural_mixed}'], runtime=self._runtime)

    def _delete(self):
        for ${aggregated_object_name_under} in self.get_${aggregated_objects_name_under}():
            ${aggregated_object_name_under}._delete()
        osid_objects.OsidObject._delete(self)"""

    is_composition = """
        return bool(self._my_map['compositionId'])"""

    additional_methods = """
    def get_object_map(self):
        obj_map = dict(self._my_map)
        obj_map['assetContent'] = obj_map['assetContents'] = [ac.object_map
                                                              for ac in self.get_asset_contents()]
        # note: assetContent is deprecated
        return osid_objects.OsidObject.get_object_map(self, obj_map)

    object_map = property(fget=get_object_map)"""

class AssetForm:

    set_title_template = """
        # Implemented from template for osid.repository.AssetForm.set_title_template
        self._my_map['${var_name_mixed}'] = self._get_display_text(${arg0_name}, self.get_${var_name}_metadata())"""

    clear_title_template = """
        # Implemented from template for osid.repository.AssetForm.clear_title_template
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['${var_name_mixed}'] = dict(self._${var_name}_default)"""


class AssetSearch:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from ..utilities import get_registry',
        'from dlkit.mongo.osid import searches as osid_searches',
    ]

    init = """
    def __init__(self, runtime):
        self._namespace = 'repository.Asset'
        record_type_data_sets = get_registry('ASSET_RECORD_TYPES', runtime)
        self._record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_ids = []
        self._id_list = None
        for data_set in record_type_data_sets:
            self._all_supported_record_type_ids.append(str(Id(**record_type_data_sets[data_set])))
        osid_searches.OsidSearch.__init__(self, runtime)"""

    search_among_assets = """
        self._id_list = asset_ids"""

class AssetSearchResults:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from . import objects',
    ]

    init = """
    def __init__(self, results, runtime):
        # if you don't iterate, then .count() on the cursor is an inaccurate representation of limit / skip
        self._results = results
        self._runtime = runtime
        self.retrieved = False"""

    get_assets = """
        if self.retrieved:
            raise errors.IllegalState('List has already been retrieved.')
        self.retrieved = True
        return objects.AssetList(self._results, runtime=self._runtime)"""

class AssetSearchSession:

    import_statements = [
        'from . import searches',
    ]


class AssetContent:

    import_statements = [
        'import gridfs',
        'from ..primitives import DataInputStream',
        'from ..utilities import MongoClientValidated'
    ]

    has_url_template = """
        # Implemented from template for osid.repository.AssetContent.has_url_template
        try:
            return bool(self._my_map['${var_name_mixed}'])
        except KeyError:
            return False"""

    get_url_template = """
        # Implemented from template for osid.repository.AssetContent.get_url_template
        if not bool(self._my_map['${var_name_mixed}']):
            raise errors.IllegalState()
        return self._my_map['${var_name_mixed}']"""

    get_data = """
        dbase = MongoClientValidated('repository',
                                     runtime=self._runtime).raw()
        filesys = gridfs.GridFS(dbase)
        return DataInputStream(filesys.get(self._my_map['data']))""" 

    additional_methods = """
    def _delete(self):
        dbase = MongoClientValidated('repository',
                                     runtime=self._runtime).raw()
        filesys = gridfs.GridFS(dbase)
        if self._my_map['data'] and filesys.exists(self._my_map['data']):
            filesys.delete(self._my_map['data'])
        osid_objects.OsidObject._delete(self)"""

class AssetContentForm:

    import_statements = [
        'import base64',
        'import gridfs',
        'from ..primitives import DataInputStream',
        'from dlkit.abstract_osid.osid import errors',
        'from ..utilities import MongoClientValidated'
    ]

    set_url_template = """
        # Implemented from template for osid.repository.AssetContentForm.set_url_template
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_${arg0_type}(
                ${arg0_name},
                self.get_${var_name}_metadata()):
            raise errors.InvalidArgument()
        self._my_map['${var_name_mixed}'] = ${arg0_name}"""

    set_data = """
        if data is None:
            raise errors.NullArgument()
        dbase = MongoClientValidated('repository',
                                     runtime=self._runtime)
        filesys = gridfs.GridFS(dbase)
        self._my_map['data'] = filesys.put(data._my_data)
        data._my_data.seek(0)
        self._my_map['base64'] = base64.b64encode(data._my_data.read())"""

    clear_data = """
        if (self.get_data_metadata().is_read_only() or
                self.get_data_metadata().is_required()):
            raise errors.NoAccess()
        if self._my_map['data'] == self._data_default:
            pass
        dbase = MongoClientValidated('repository',
                                     runtime=self._runtime)
        filesys = gridfs.GridFS(dbase)
        filesys.delete(self._my_map['data'])
        self._my_map['data'] = self._data_default
        del self._my_map['base64']"""

class Composition:
    
    ## This two methods are defined here because of an inconsistency with
    # Naming conventions.  The pattern mapper expected get_child_ids.  The second
    # should otherwise come from the template for learning.Activity.get_asset_ids
    get_children_ids = """
        return IdList(self._my_map['childIds'])

    def get_child_ids(self):
        return self.get_children_ids()"""

    additional_methods = """
    def get_object_map(self):
        obj_map = dict(self._my_map)
        if 'assetIds' in obj_map:
            del obj_map['assetIds']
        return osid_objects.OsidObject.get_object_map(self, obj_map)

    object_map = property(fget=get_object_map)"""

class CompositionForm:
    # per Tom Coppeto. We are moving composition design to the CompositionForm
    additional_methods = """
    def get_children_metadata(self):
        \"\"\"Gets the metadata for children.

        return: (osid.Metadata) - metadata for the children
        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        metadata = dict(self._mdata['children'])
        metadata.update({'existing_children_values': self._my_map['childIds']})
        return Metadata(**metadata)

    children_metadata = property(fget=get_children_metadata)

    @utilities.arguments_not_none
    def set_children(self, child_ids):
        \"\"\"Sets the children.

        arg:    child_ids (osid.id.Id[]): the children``Ids``
        raise:  InvalidArgument - ``child_ids`` is invalid
        raise:  NoAccess - ``Metadata.isReadOnly()`` is ``true``
        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        if not isinstance(child_ids, list):
            raise errors.InvalidArgument()
        if self.get_children_metadata().is_read_only():
            raise errors.NoAccess()
        idstr_list = []
        for object_id in child_ids:
            if not self._is_valid_id(object_id):
                raise errors.InvalidArgument()
            if str(object_id) not in idstr_list:
                idstr_list.append(str(object_id))
        self._my_map['childIds'] = idstr_list

    def clear_children(self):
        \"\"\"Clears the children.

        raise:  NoAccess - ``Metadata.isRequired()`` or
                ``Metadata.isReadOnly()`` is ``true``
        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        if (self.get_children_metadata().is_read_only() or
                self.get_children_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['childIds'] = self._children_default

    children = property(fset=set_children, fdel=clear_children)"""

class CompositionQuery:
    match_containing_composition_id = """
        self._add_match('_id', composition_id.identifier, match)"""

    match_contained_composition_id = """
        self._add_match('childIds', str(composition_id), match)"""

    match_asset_id = """
        self._add_match('assetIds', str(asset_id), match)"""


class CompositionSearch:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from ..utilities import get_registry',
        'from dlkit.mongo.osid import searches as osid_searches',
    ]

    init = """
    def __init__(self, runtime):
        self._namespace = 'repository.Composition'
        record_type_data_sets = get_registry('COMPOSITION_RECORD_TYPES', runtime)
        self._record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_ids = []
        self._id_list = None
        for data_set in record_type_data_sets:
            self._all_supported_record_type_ids.append(str(Id(**record_type_data_sets[data_set])))
        osid_searches.OsidSearch.__init__(self, runtime)"""

    search_among_compositions = """
        self._id_list = composition_ids"""

class CompositionSearchResults:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from . import objects',
    ]

    init = """
    def __init__(self, results, runtime):
        # if you don't iterate, then .count() on the cursor is an inaccurate representation of limit / skip
        self._results = results
        self._runtime = runtime
        self.retrieved = False"""

    get_compositions = """
        if self.retrieved:
            raise errors.IllegalState('List has already been retrieved.')
        self.retrieved = True
        return objects.CompositionList(self._results, runtime=self._runtime)"""

class CompositionRepositorySession:
    get_repository_ids_by_composition = """
        mgr = self._get_provider_manager('REPOSITORY', local=True)
        lookup_session = mgr.get_composition_lookup_session(proxy=self._proxy)
        lookup_session.use_federated_repository_view()
        lookup_session.use_unsequestered_composition_view()
        composition = lookup_session.get_composition(composition_id)
        id_list = []
        if 'assignedRepositoryIds' in composition._my_map:
            for idstr in composition._my_map['assignedRepositoryIds']:
                id_list.append(Id(idstr))
        return IdList(id_list)"""

