

class AssetAdminSession:

    create_asset_content_template = """
        # Implemented from template for 
        # osid.repository.AssetAdminSession.create_asset_content_template
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from bson.objectid import ObjectId
        from ..primitives import Id
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
        ${arg0_name}._my_map['_id'] = ObjectId()
        ${object_name_under}_id = Id(${arg0_name}._my_map['${object_name_under}Id']).get_identifier()
        ${object_name_under} = collection.find_one({'$$and': [{'_id': ObjectId(${object_name_under}_id)},
                                      {'${cat_name_mixed}Id': str(self._catalog_id)}]})
        ${object_name_under}['${aggregated_objects_name_mixed}'].append(${arg0_name}._my_map)
        try:
            id_ = collection.save(${object_name_under})
        except: # what exceptions does mongodb insert raise?
            raise OperationFailed()
        self._forms[${arg0_name}.get_id().get_identifier()] = CREATED
        from .${return_module} import ${aggregated_object_name}
        return ${return_type}(${arg0_name}._my_map)"""

    get_asset_content_form_for_update_template = """
        # Implemented from template for 
        # osid.repository.AssetAdminSession.get_asset_content_form_for_update_template
        from bson.objectid import ObjectId
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
            return InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        document = collection.find_one({'${aggregated_objects_name_mixed}._id': ObjectId(${arg0_name}.get_identifier())})
        if document is None:
            raise NotFound()
        for sub_doc in document['${aggregated_objects_name_mixed}']: # There may be a MongoDB shortcut for this
            if sub_doc['_id'] == ObjectId(${arg0_name}.get_identifier()):
                result = sub_doc
        obj_form = ${return_type}(result)
        obj_form._for_update = True
        self._forms[obj_form.get_id().get_identifier()] = not UPDATED
        return obj_form"""

    update_asset_content_template = """
        # Implemented from template for 
        # osid.repository.AssetAdminSession.update_asset_content_template
        from bson.objectid import ObjectId
        from ..primitives import Id
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
        ${object_name_under}_id = Id(${arg0_name}._my_map['${object_name_under}Id']).get_identifier()
        ${object_name_under} = collection.find_one({'$$and': [{'_id': ObjectId(${object_name_under}_id)},
                                      {'${cat_name_mixed}Id': str(self._catalog_id)}]})
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
            raise NotFound()
        try:
            collection.save(${object_name_under})
        except: # what exceptions does mongodb save raise?
            raise OperationFailed()
        self._forms[${arg0_name}.get_id().get_identifier()] = UPDATED
        # Note: this is out of spec. The OSIDs don't require an object to be returned:
        from .objects import ${aggregated_object_name}
        return ${aggregated_object_name}(${arg0_name}._my_map)"""

    delete_asset_content_template = """
        # Implemented from template for 
        # osid.repository.AssetAdminSession.delete_asset_content_template
        from bson.objectid import ObjectId
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from ..osid.osid_errors import NotFound, NullArgument, InvalidArgument, OperationFailed, PermissionDenied, Unsupported
        from .objects import ${aggregated_object_name}
        from bson.objectid import ObjectId
        from pymongo import MongoClient
        collection = MongoClient()['${package_name}']['${object_name}']
        UPDATED = True
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            return InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        ${object_name_under} = collection.find_one({'${aggregated_objects_name_mixed}._id': ObjectId(${arg0_name}.get_identifier())})
        if ${object_name_under} is None:
            raise NotFound()
        index = 0
        found = False
        for i in ${object_name_under}['${aggregated_objects_name_mixed}']:
            if i['_id'] == ObjectId(${arg0_name}.get_identifier()):
                ${aggregated_object_name_under}_map = ${object_name_under}['${aggregated_objects_name_mixed}'].pop(index)
            index += 1
            found = True
        if not found:
            raise OperationFailed()
        ${aggregated_object_name}(${aggregated_object_name_under}_map)._delete()
        try:
            collection.save(${object_name_under})
        except: # what exceptions does mongodb save raise?
            raise OperationFailed()"""


class Asset:

    import_statements_pattern = [
        'from ..primitives import *'
        ]

    get_title_template = """
        # Implemented from template for osid.repository.Asset.get_title_template
        return DisplayText(self._my_map['${var_name_mixed}'])"""

    can_distribute_verbatim_template = """
        # Implemented from template for osid.repository.AssetForm.can_distribute_verbatim
        from .osid_errors import IllegalState
        if self._my_map['${var_name_mixed}'] is None:
            raise IllegalState()
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
        return ${aggregated_object_name}List(self._my_map['${var_name_plural_mixed}'])
        
    def _delete(self):
        for ${aggregated_object_name_under} in self.get_${aggregated_objects_name_under}():
            ${aggregated_object_name_under}._delete()
        osid_objects.OsidObject._delete(self)"""

class AssetForm:

    set_title_template = """
        # Implemented from template for osid.repository.AssetForm.set_title_template
        from ..osid.osid_errors import InvalidArgument, NullArgument, NoAccess
        if ${arg0_name} is None:
            raise NullArgument()
        if self.get_${var_name}_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_${arg0_type}(${arg0_name}, 
                                     self.get_${arg0_name}_metadata()):
            raise InvalidArgument()
        self._my_map['${var_name_mixed}']['text'] = ${arg0_name}"""

    clear_title_template = """
        # Implemented from template for osid.repository.AssetForm.clear_title_template
        from ..osid.osid_errors import NoAccess
        if (self.get_${var_name}_metadata().is_read_only() or
            self.get_${var_name}_metadata().is_required()):
            raise NoAccess()
        self._my_map['${var_name_mixed}'] = dict(self._${var_name}_default)"""


class AssetContent:

    import_statements = [
        'from pymongo import MongoClient',
        'import gridfs',
        'from ..primitives import DataInputStream',
        'from ..osid.osid_errors import *']

    has_url_template = """
        # Implemented from template for osid.repository.AssetContent.has_url_template
        return bool(self._my_map['${var_name_mixed}'])"""

    get_url_template = """
        # Implemented from template for osid.repository.AssetContent.get_url_template
        if not bool(self._my_map['${var_name_mixed}']):
            raise IllegalState()
        return self._my_map['${var_name_mixed}']"""

    get_data = """
        db = MongoClient()['repository']
        fs = gridfs.GridFS(db)
        return DataInputStream(fs.get(self._my_map['data']))""" 

    additional_methods = """
    def _delete(self):
        db = MongoClient()['repository']
        fs = gridfs.GridFS(db)
        if self._my_map['data'] and fs.exists(self._my_map['data']):
            fs.delete(self._my_map['data'])
        osid_objects.OsidObject._delete(self)"""

class AssetContentForm:

    import_statements = [
        'from pymongo import MongoClient',
        'import gridfs',
        'from ..primitives import DataInputStream']

    set_url_template = """
        # Implemented from template for osid.repository.AssetContentForm.set_url_template
        from ..osid.osid_errors import InvalidArgument, NullArgument, NoAccess
        if ${arg0_name} is None:
            raise NullArgument()
        if self.get_${var_name}_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_${arg0_type}(${arg0_name}, 
                                     self.get_${var_name}_metadata()):
            raise InvalidArgument()
        self._my_map['${var_name_mixed}'] = ${arg0_name}"""

    set_data = """
        if data is None:
            raise NullArgument()
        db = MongoClient()['repository']
        fs = gridfs.GridFS(db)
        self._my_map['data'] = fs.put(data._my_data)"""

    clear_data = """
        from ..osid.osid_errors import NoAccess
        if (self.get_data_metadata().is_read_only() or
            self.get_data_metadata().is_required()):
            raise NoAccess()
        db = MongoClient()['repository']
        fs = gridfs.GridFS(db)
        fs.delete(self._my_map['data'])
        self._my_map['data'] = self._data_default"""
