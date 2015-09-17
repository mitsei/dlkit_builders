
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
        return sessions.AssetCompositionDesignSession(repository_id, runtime=self._runtime) # pylint: disable=no-member
"""

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
        return sessions.AssetCompositionDesignSession(repository_id, proxy, runtime=self._runtime) # pylint: disable=no-member
"""

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
            {'$$and': [{'_id': ObjectId(${object_name_under}_id)}, {'${cat_name_mixed}Id': str(self._catalog_id)}]})
        ${object_name_under}['${aggregated_objects_name_mixed}'].append(${arg0_name}._my_map)
        result = collection.save(${object_name_under})

        self._forms[${arg0_name}.get_id().get_identifier()] = CREATED
        from .${return_module} import ${aggregated_object_name}
        return ${return_type}(${arg0_name}._my_map, runtime=self._runtime)"""

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
        obj_form = ${return_type}(result, runtime=self._runtime)
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
            {'$$and': [{'_id': ObjectId(${object_name_under}_id)}, {'${cat_name_mixed}Id': str(self._catalog_id)}]})
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

        return ${aggregated_object_name}(${arg0_name}._my_map, runtime=self._runtime)"""

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
        ${aggregated_object_name}(${aggregated_object_name_under}_map, runtime=self._runtime)._delete()
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
            db_name='${pkg_name}',
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

    use_active_composition_view = """
        self._status_view = ACTIVE"""

    use_any_status_composition_view = """
        self._status_view = ANY_STATUS"""

    use_sequestered_composition_view = """
        self._sequestered_view = SEQUESTERED"""

    use_unsequestered_composition_view = """
        self._sequestered_view = UNSEQUESTERED"""


class CompositionQuerySession:

    import_statements = [
        'ACTIVE = 0',
        'ANY_STATUS = 1',
        'SEQUESTERED = 0',
        'UNSEQUESTERED = 1',
    ]

    init = """
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
        return view_filter
"""


class AssetCompositionSession:

    import_statements = [
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
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
        self._kwargs = kwargs
"""

    get_composition_assets = """
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
        als = mgr.get_asset_lookup_session()
        als.use_federated_repository_view()
        return als.get_assets_by_ids(asset_ids)"""

    get_compositions_by_asset = """
        collection = MongoClientValidated('repository',
                                          collection='Composition',
                                          runtime=self._runtime)
        result = collection.find(
            dict({'assetIds': {'$in': [str(asset_id)]}},
                 **self._view_filter())).sort('_id', DESCENDING)
        return objects.CompositionList(result, runtime=self._runtime)"""


class AssetCompositionDesignSession:

    import_statements = [
        'from ..list_utilities import move_id_ahead, move_id_behind, order_ids',
    ]

    init = """
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
        self._kwargs = kwargs
"""

    can_compose_assets = """
        return True"""

    add_asset = """
        # This asset found check may want to be run through _get_provider_manager
        # so as to ensure assess control:
        from ...abstract_osid.id.primitives import Id as ABCId
        if not isinstance(asset_id, ABCId):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        if asset_id.get_identifier_namespace() != 'repository.Asset':
            if asset_id.get_authority() != self._authority:
                raise errors.InvalidArgument()
            else:
                mgr = self._get_provider_manager('REPOSITORY')
                admin_session = mgr.get_asset_admin_session_for_repository(self._catalog_id)
                asset_id = admin_session._get_asset_id_with_enclosure(asset_id)
        collection = MongoClientValidated('repository',
                                          collection='Asset',
                                          runtime=self._runtime)
        asset = collection.find_one({'_id': ObjectId(asset_id.get_identifier())})
        collection = MongoClientValidated('repository',
                                          collection='Composition',
                                          runtime=self._runtime)
        composition = collection.find_one({'_id': ObjectId(composition_id.get_identifier())})
        if 'assetIds' in composition:
            if str(asset_id) not in composition['assetIds']:
                composition['assetIds'].append(str(asset_id))
        else:
            composition['assetIds'] = [str(asset_id)]
        collection.save(composition)"""

    move_asset_ahead = """
        collection = MongoClientValidated('repository',
                                          collection='Composition',
                                          runtime=self._runtime)
        composition = collection.find_one({'_id': ObjectId(composition_id.get_identifier())})
        if 'assetIds' not in composition:
            raise errors.NotFound('no Assets are assigned to this Composition')
        composition['assetIds'] = move_id_ahead(asset_id, reference_id, composition['assetIds'])
        collection.save(composition)"""

    move_asset_behind = """
        collection = MongoClientValidated('repository',
                                          collection='Composition',
                                          runtime=self._runtime)
        composition = collection.find_one({'_id': ObjectId(composition_id.get_identifier())})
        if 'assetIds' not in composition:
            raise errors.NotFound('no Assets are assigned to this Composition')
        composition['assetIds'] = move_id_behind(asset_id, reference_id, composition['assetIds'])
        collection.save(composition)"""

    order_assets = """
        collection = MongoClientValidated('repository',
                                          collection='Composition',
                                          runtime=self._runtime)
        composition = collection.find_one({'_id': ObjectId(composition_id.get_identifier())})
        collection = MongoClientValidated('repository',
                                          collection='Composition',
                                          runtime=self._runtime)
        if 'assetIds' not in composition:
            raise errors.NotFound('no Assets are assigned to this Composition')
        composition['assetIds'] = order_ids(asset_ids, composition['assetIds'])
        collection.save(composition)"""

    remove_asset = """
        collection = MongoClientValidated('repository',
                                          collection='Composition',
                                          runtime=self._runtime)
        composition = collection.find_one({'_id': ObjectId(composition_id.get_identifier())})
        try:
            composition['assetIds'].remove(str(asset_id))
        except (KeyError, ValueError):
            raise errors.NotFound()
        collection.save(composition)"""


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
    try:
        from ..records.types import ASSET_RECORD_TYPES as _record_type_data_sets #pylint: disable=no-name-in-module
    except (ImportError, AttributeError):
        _record_type_data_sets = {}
    _namespace = 'repository.Asset'

    def __init__(self, osid_object_map, runtime=None):
        osid_objects.OsidObject.__init__(self, osid_object_map, runtime)
        self._records = dict()
        self._load_records(osid_object_map['recordTypeIds'])
        self._catalog_name = 'Repository'
        if self.is_composition():
            self._composition = self.get_composition()

    def __getattr__(self, name):
        if self.is_composition():
            try:
                return self._composition[name]
            except AttributeError:
                raise AttributeError()
        #HOW TO PASS TO EXTENSIBLE!!!!
"""


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
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_${arg0_type}(${arg0_name}, self.get_${arg0_name}_metadata()):
            raise errors.InvalidArgument()
        self._my_map['${var_name_mixed}']['text'] = ${arg0_name}"""

    clear_title_template = """
        # Implemented from template for osid.repository.AssetForm.clear_title_template
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['${var_name_mixed}'] = dict(self._${var_name}_default)"""


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
        metadata = dict(self._children_metadata)
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

    children = property(fset=set_children, fdel=clear_children)
"""

class CompositionQuery:
    match_containing_composition_id = """
        self._add_match('_id', composition_id.identifier, match)
    """

    match_contained_composition_id = """
        self._add_match('childIds', str(composition_id), match)
    """

    match_asset_id = """
        self._add_match('assetIds', str(asset_id), match)
    """