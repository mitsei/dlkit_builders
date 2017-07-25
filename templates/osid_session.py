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
    ${pattern_name}
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
        ${pattern_name}
        self._status_view = ACTIVE"""
        }
    }

    use_any_status_containable_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        self._status_view = ANY_STATUS"""
        }
    }

    use_sequestered_containable_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        self._sequestered_view = SEQUESTERED"""
        }
    }

    use_unsequestered_containable_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
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
        ${pattern_name}
        return self._catalog_id"""
        }
    }

    get_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return self._catalog"""
        }
    }

    can_lookup_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
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
        ${pattern_name}
        self._use_comparative_object_view()"""
        }
    }

    use_plenary_object_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        self._use_plenary_object_view()"""
        }
    }

    use_federated_catalog_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        self._use_federated_catalog_view()"""
        }
    }

    use_isolated_catalog_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        self._use_isolated_catalog_view()"""
        }
    }

    get_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
        # STILL NEED TO IMPLEMENT!!!
        return objects.${return_type}([])"""
        }
    }

    get_objects_by_record_type_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        # STILL NEED TO IMPLEMENT!!!
        return objects.${return_type}([])"""
        }
    }

    get_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        # NOTE: This implementation currently ignores plenary view
        collection = JSONClientValidated('${package_name_replace}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        result = collection.find(self._view_filter()).sort('_id', DESCENDING)
        return objects.${return_type}(result, runtime=self._runtime, proxy=self._proxy)"""
        }
    }

    # Could probably move these two method templates to a GenericSubjugateableObjectLookupSession class...
    get_subjugated_objects_for_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
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
        ${pattern_name}
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
    ${pattern_name}
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

    can_create_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
        }
    }

    can_create_object_with_record_types_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
        }
    }

    get_object_form_for_create_import_templates = {
        'python': {
            'json': [
                'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
            ]
        }
    }

    get_object_form_for_create_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
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
        }
    }

    create_object_import_templates = {
        'python': {
            'json': [
                'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
            ]
        }
    }

    create_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        collection = JSONClientValidated('${package_name_replace}',
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
        }
    }

    can_update_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
        }
    }

    get_object_form_for_update_import_templates = {
        'python': {
            'json': [
                'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
            ]
        }
    }

    get_object_form_for_update_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        collection = JSONClientValidated('${package_name_replace}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        if (${arg0_name}.get_identifier_namespace() != '${package_name_replace}.${object_name}' or
                ${arg0_name}.get_authority() != self._authority):
            raise errors.InvalidArgument()
        result = collection.find_one({'_id': ObjectId(${arg0_name}.get_identifier())})

        obj_form = objects.${return_type}(osid_object_map=result, runtime=self._runtime, proxy=self._proxy)
        self._forms[obj_form.get_id().get_identifier()] = not UPDATED

        return obj_form"""
        }
    }

    # This is out of spec, but used by the EdX / LORE record extensions for assets / compositions
    # So put it in additional methods there only.
    # @utilities.arguments_not_none
    # def duplicate_${object_name_under}(self, ${object_name_under}_id):
    #     collection = JSONClientValidated('${package_name_replace}',
    #                                      collection='${object_name}',
    #                                      runtime=self._runtime)
    #     mgr = self._get_provider_manager('${package_name_replace_upper}')
    #     lookup_session = mgr.get_${object_name_under}_lookup_session(proxy=self._proxy)
    #     lookup_session.use_federated_${cat_name_under}_view()
    #     try:
    #         lookup_session.use_unsequestered_${object_name_under}_view()
    #     except AttributeError:
    #         pass
    #     ${object_name_under}_map = dict(lookup_session.get_${object_name_under}(${object_name_under}_id)._my_map)
    #     del ${object_name_under}_map['_id']
    #     if '${cat_name_lower}Id' in ${object_name_under}_map:
    #         ${object_name_under}_map['${cat_name_lower}Id'] = str(self._catalog_id)
    #     if 'assigned${cat_name}Ids' in ${object_name_under}_map:
    #         ${object_name_under}_map['assigned${cat_name}Ids'] = [str(self._catalog_id)]
    #     insert_result = collection.insert_one(${object_name_under}_map)
    #     result = objects.${object_name}(
    #         osid_object_map=collection.find_one({'_id': insert_result.inserted_id}),
    #         runtime=self._runtime,
    #         proxy=self._proxy)
    #     return result"""

    update_object_import_templates = {
        'python': {
            'json': [
                'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
            ]
        }
    }

    update_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        collection = JSONClientValidated('${package_name_replace}',
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
        }
    }

    can_delete_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
        }
    }

    delete_object_import_templates = {
        'python': {
            'json': [
                'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
            ]
        }
    }

    delete_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        collection = JSONClientValidated('${package_name_replace}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        ${object_name_under}_map = collection.find_one(
            dict({'_id': ObjectId(${arg0_name}.get_identifier())},
                 **self._view_filter()))

        objects.${object_name}(osid_object_map=${object_name_under}_map, runtime=self._runtime, proxy=self._proxy)._delete()
        collection.delete_one({'_id': ObjectId(${arg0_name}.get_identifier())})"""
        }
    }

    can_manage_object_aliases_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
        }
    }

    alias_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        ${pattern_name}
        self._alias_id(primary_id=${arg0_name}, equivalent_id=${arg1_name})"""
        }
    }

    # Could probably move these two method templates to a GenericSubjugateableObjectAdminSession class...
    get_subjugated_object_form_for_create_import_templates = {
        'python': {
            'json': [
                'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}',
                'from ${arg1_abcapp_name}.${arg1_abcpkg_name}.${arg1_module} import ${arg1_type} as ABC${arg1_type}'
            ]
        }
    }

    get_subjugated_object_form_for_create_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        ${pattern_name}

        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('argument is not a valid OSID ${arg0_type}')
        for arg in ${arg1_name}:
            if not isinstance(arg, ABC${arg1_type}):
                raise errors.InvalidArgument('one or more argument array elements is not a valid OSID ${arg1_type}')
        if ${arg1_name} == []:
            # WHY are we passing ${cat_name_under}_id = self._catalog_id below, seems redundant:
            obj_form = objects.${return_type}(
                ${cat_name_under}_id=self._catalog_id,
                ${arg0_name}=${arg0_name},
                catalog_id=self._catalog_id,
                runtime=self._runtime,
                proxy=self._proxy)
        else:
            obj_form = objects.${return_type}(
                ${cat_name_under}_id=self._catalog_id,
                record_types=${arg1_name},
                ${arg0_name}=${arg0_name},
                catalog_id=self._catalog_id,
                runtime=self._runtime,
                proxy=self._proxy)
        obj_form._for_update = False
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form"""
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
    ${pattern_name}
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

    reliable_object_notifications_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        MONGO_LISTENER.receivers[self._ns][self._receiver]['reliable'] = True"""
        }
    }

    unreliable_object_notifications_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        MONGO_LISTENER.receivers[self._ns][self._receiver]['reliable'] = False"""
        }
    }

    acknowledge_notification_template = {
        'python': {
            'json': """
    def ${method_name}(self, notification_id):
        ${doc_string}
        ${pattern_name}
        try:
            del MONGO_LISTENER.notifications[notification_id]
        except KeyError:
            pass"""
        }
    }

    register_for_new_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        MONGO_LISTENER.receivers[self._ns][self._receiver]['i'] = True"""
        }
    }

    register_for_changed_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        MONGO_LISTENER.receivers[self._ns][self._receiver]['u'] = True"""
        }
    }

    register_for_changed_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        if not MONGO_LISTENER.receivers[self._ns][self._receiver]['u']:
            MONGO_LISTENER.receivers[self._ns][self._receiver]['u'] = []
        if isinstance(MONGO_LISTENER.receivers[self._ns][self._receiver]['u'], list):
            MONGO_LISTENER.receivers[self._ns][self._receiver]['u'].append(${arg0_name}.get_identifier())"""
        }
    }

    register_for_deleted_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        MONGO_LISTENER.receivers[self._ns][self._receiver]['d'] = True"""
        }
    }

    register_for_deleted_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        if not MONGO_LISTENER.receivers[self._ns][self._receiver]['d']:
            MONGO_LISTENER.receivers[self._ns][self._receiver]['d'] = []
        if isinstance(MONGO_LISTENER.receivers[self._ns][self._receiver]['d'], list):
            MONGO_LISTENER.receivers[self._ns][self._receiver]['d'].append(${arg0_name}.get_identifier())"""
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
        ${pattern_name}
        self._use_effective_view()"""
        }
    }

    use_any_effective_relationship_view_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        self._use_any_effective_view()"""
        }
    }

    get_relationships_on_date_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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

    # Should the following three methods be in a "GenericObjectRequisiteSession" class?
    get_requisite_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        # NOTE: This implementation currently ignores plenary view
        requisite_type = Type(**Relationship().get_type_data('${object_name_upper}.REQUISITE'))
        relm = self._get_provider_manager('RELATIONSHIP')
        rls = relm.get_relationship_lookup_session(proxy=self._proxy)
        rls.use_federated_family_view()
        requisite_relationships = rls.get_relationships_by_genus_type_for_source(${arg0_name},
                                                                                 requisite_type)
        destination_ids = [ObjectId(r.get_destination_id().identifier)
                           for r in requisite_relationships]
        collection = JSONClientValidated('${package_name}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        result = collection.find({'_id': {'$$in': destination_ids}})
        return objects.${return_type}(result, runtime=self._runtime)"""
        }
    }

    can_lookup_object_prerequisites_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return True"""
        }
    }

    get_dependent_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        # NOTE: This implementation currently ignores plenary view
        requisite_type = Type(**Relationship().get_type_data('${object_name_upper}.REQUISITE'))
        relm = self._get_provider_manager('RELATIONSHIP')
        rls = relm.get_relationship_lookup_session(proxy=self._proxy)
        rls.use_federated_family_view()
        requisite_relationships = rls.get_relationships_by_genus_type_for_destination(${arg0_name},
                                                                                      requisite_type)
        source_ids = [ObjectId(r.get_source_id().identifier)
                      for r in requisite_relationships]
        collection = JSONClientValidated('${package_name}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        result = collection.find({'_id': {'$$in': source_ids}})
        return objects.${return_type}(result, runtime=self._runtime)"""
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
    ${pattern_name}
    _session_namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession._init_catalog(self, proxy, runtime)
        self._catalog_view = COMPARATIVE
        self._kwargs = kwargs"""
        }
    }

    can_lookup_object_catalog_mappings_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
        }
    }

    get_object_ids_by_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        id_list = []
        for ${object_name_under} in self.get_${object_name_plural_under}_by_${cat_name_under}(${arg0_name}):
            id_list.append(${object_name_under}.get_id())
        return IdList(id_list)"""
        }
    }

    get_objects_by_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        mgr = self._get_provider_manager('${package_name_replace_upper}', local=True)
        lookup_session = mgr.get_${object_name_under}_lookup_session_for_${cat_name_under}(${arg0_name}, proxy=self._proxy)
        lookup_session.use_isolated_${cat_name_under}_view()
        return lookup_session.get_${object_name_plural_under}()"""
        }
    }

    get_object_ids_by_catalogs_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        id_list = []
        for ${object_name_under} in self.get_${object_name_plural_under}_by_${cat_name_plural_under}(${arg0_name}):
            id_list.append(${object_name_under}.get_id())
        return IdList(id_list)"""
        }
    }

    get_objects_by_catalogs_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        ${object_name_under}_list = []
        for ${cat_name_under}_id in ${arg0_name}:
            ${object_name_under}_list += list(
                self.get_${object_name_plural_under}_by_${cat_name_under}(${cat_name_under}_id))
        return objects.${return_type}(${object_name_under}_list)"""
        }
    }

    get_catalog_ids_by_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        mgr = self._get_provider_manager('${package_name_replace_upper}', local=True)
        lookup_session = mgr.get_${object_name_under}_lookup_session(proxy=self._proxy)
        lookup_session.use_federated_${cat_name_under}_view()
        ${object_name_under} = lookup_session.get_${object_name_under}(${arg0_name})
        id_list = []
        for idstr in ${object_name_under}._my_map['assigned${cat_name}Ids']:
            id_list.append(Id(idstr))
        return IdList(id_list)"""
        }
    }

    get_catalogs_by_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        mgr = self._get_provider_manager('${package_name_replace_upper}', local=True)
        lookup_session = mgr.get_${cat_name_under}_lookup_session(proxy=self._proxy)
        return lookup_session.get_${cat_name_plural_under}_by_ids(
            self.get_${cat_name_under}_ids_by_${object_name_under}(${arg0_name}))"""
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
    ${pattern_name}
    _session_namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession._init_catalog(self, proxy, runtime)
        self._catalog_name = '${cat_name}'
        self._forms = dict()
        self._kwargs = kwargs"""
        }
    }

    can_assign_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
        }
    }

    can_assign_objects_to_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        if ${arg0_name}.get_identifier() == '000000000000000000000000':
            return False
        return True"""
        }
    }

    get_assignable_catalog_ids_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        # This will likely be overridden by an authorization adapter
        mgr = self._get_provider_manager('${package_name_replace_upper}', local=True)
        lookup_session = mgr.get_${cat_name_under}_lookup_session(proxy=self._proxy)
        ${cat_name_plural_under} = lookup_session.get_${cat_name_plural_under}()
        id_list = []
        for ${cat_name_under} in ${cat_name_plural_under}:
            id_list.append(${cat_name_under}.get_id())
        return IdList(id_list)"""
        }
    }

    get_assignable_catalog_ids_for_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        # This will likely be overridden by an authorization adapter
        return self.get_assignable_${cat_name_under}_ids(${arg0_name})"""
        }
    }

    assign_object_to_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        ${pattern_name}
        mgr = self._get_provider_manager('${package_name_replace_upper}', local=True)
        lookup_session = mgr.get_${cat_name_under}_lookup_session(proxy=self._proxy)
        lookup_session.get_${cat_name_under}(${arg1_name})  # to raise NotFound
        self._assign_object_to_catalog(${arg0_name}, ${arg1_name})"""
        }
    }

    unassign_object_from_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        ${pattern_name}
        mgr = self._get_provider_manager('${package_name_replace_upper}', local=True)
        lookup_session = mgr.get_${cat_name_under}_lookup_session(proxy=self._proxy)
        lookup_session.get_${cat_name_under}(${arg1_name})  # to raise NotFound
        self._unassign_object_from_catalog(${arg0_name}, ${arg1_name})"""
        }
    }

    reassign_object_to_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}, ${arg2_name}):
        ${doc_string}
        ${pattern_name}
        self.assign_${object_name_under}_to_${cat_name_under}(${arg0_name}, ${arg2_name})
        try:
            self.unassign_${object_name_under}_from_${cat_name_under}(${arg0_name}, ${arg1_name})
        except:  # something went wrong, roll back assignment to ${arg2_name}
            self.unassign_${object_name_under}_from_${cat_name_under}(${arg0_name}, ${arg2_name})
            raise"""
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
    ${pattern_name}
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

    can_query_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
        }
    }

    can_search_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
        }
    }

    get_object_query_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return queries.${return_type}(runtime=self._runtime)"""
        }
    }

    get_objects_by_query_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        and_list = list()
        or_list = list()
        for term in ${arg0_name}._query_terms:
            if '$$in' in ${arg0_name}._query_terms[term] and '$$nin' in ${arg0_name}._query_terms[term]:
                and_list.append(
                    {'$$or': [{term: {'$$in': ${arg0_name}._query_terms[term]['$$in']}},
                             {term: {'$$nin': ${arg0_name}._query_terms[term]['$$nin']}}]})
            else:
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
            collection = JSONClientValidated('${package_name_replace}',
                                             collection='${object_name}',
                                             runtime=self._runtime)
            result = collection.find(query_terms).sort('_id', DESCENDING)
        else:
            result = []
        return objects.${return_type}(result, runtime=self._runtime, proxy=self._proxy)"""
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
    ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
    ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
        return queries.${return_type}(runtime=self._runtime)"""
        }
    }

    get_catalogs_by_query_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
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
    ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
    ${pattern_name}
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
    ${pattern_name}
    _session_namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
    ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
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
        ${pattern_name}
        if self._catalog_session is not None:
            return self._catalog_session.remove_child_catalogs(catalog_id=${arg0_name})
        return self._hierarchy_session.remove_children(id_=${arg0_name})"""
        }
    }


class GenericObjectContainableSession(object):
    # AssetCompositionSession
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
    ${pattern_name}
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

    can_access_object_containables_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
        }
    }

    get_containable_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        collection = JSONClientValidated('${package_name_replace}',
                                         collection='${containable_object_name}',
                                         runtime=self._runtime)
        ${containable_object_name_under} = collection.find_one(
            dict({'_id': ObjectId(${arg0_name}.get_identifier())},
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
        }
    }

    get_containables_by_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        collection = JSONClientValidated('${package_name_replace}',
                                         collection='${containable_object_name}',
                                         runtime=self._runtime)
        result = collection.find(
            dict({'${object_name_mixed}Ids': {'$$in': [str(${arg0_name})]}},
                 **self._view_filter())).sort('_id', DESCENDING)
        return objects.${return_type}(result, runtime=self._runtime)"""
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
    ${pattern_name}
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

    can_compose_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
        }
    }

    add_object_to_containable_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        ${pattern_name}
        # The ${object_name_under} found check may want to be run through _get_provider_manager
        # so as to ensure access control:
        from dlkit.abstract_osid.id.primitives import Id as ABCId
        if not isinstance(${arg0_name}, ABCId):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        if (not isinstance(${arg1_name}, ABCId) and
                ${arg1_name}.get_identifier_namespace() != '${package_name_replace}.${containable_object_name}'):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        if ${arg0_name}.get_identifier_namespace() != '${object_namespace}':
            if ${arg0_name}.get_authority() != self._authority:
                raise errors.InvalidArgument()
            else:
                mgr = self._get_provider_manager('${object_package_name_replace_upper}')
                admin_session = mgr.get_${object_name_under}_admin_session_for_${cat_name_under}(self._catalog_id, proxy=self._proxy)
                ${arg0_name} = admin_session._get_${object_name_under}_id_with_enclosure(${arg0_name})
        collection = JSONClientValidated('${object_package_name_replace}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        ${object_name_under} = collection.find_one({'_id': ObjectId(${arg0_name}.get_identifier())})
        collection = JSONClientValidated('${package_name_replace}',
                                         collection='${containable_object_name}',
                                         runtime=self._runtime)
        ${containable_object_name_under} = collection.find_one({'_id': ObjectId(${arg1_name}.get_identifier())})
        if '${object_name_mixed}Ids' in ${containable_object_name_under}:
            if str(${arg0_name}) not in ${containable_object_name_under}['${object_name_mixed}Ids']:
                ${containable_object_name_under}['${object_name_mixed}Ids'].append(str(${arg0_name}))
        else:
            ${containable_object_name_under}['${object_name_mixed}Ids'] = [str(${arg0_name})]
        collection.save(${containable_object_name_under})"""
        }
    }

    move_object_ahead_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}, ${arg2_name}):
        ${doc_string}
        ${pattern_name}
        if (not isinstance(${arg1_name}, ABCId) and
                ${arg1_name}.get_identifier_namespace() != '${package_name_replace}.${containable_object_name}'):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        ${containable_object_name_under}_map, collection = self._get_${containable_object_name_under}_collection(${arg1_name})
        ${containable_object_name_under}_map['${object_name_mixed}Ids'] = move_id_ahead(${arg0_name}, ${arg2_name}, ${containable_object_name_under}_map['${object_name_mixed}Ids'])
        collection.save(${containable_object_name_under}_map)"""
        }
    }

    move_object_behind_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}, ${arg2_name}):
        ${doc_string}
        ${pattern_name}
        if (not isinstance(${arg1_name}, ABCId) and
                ${arg1_name}.get_identifier_namespace() != '${package_name_replace}.${containable_object_name}'):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        ${containable_object_name_under}_map, collection = self._get_${containable_object_name_under}_collection(${arg1_name})
        ${containable_object_name_under}_map['${object_name_mixed}Ids'] = move_id_behind(${arg0_name}, ${arg2_name}, ${containable_object_name_under}_map['${object_name_mixed}Ids'])
        collection.save(${containable_object_name_under}_map)"""
        }
    }

    order_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        ${pattern_name}
        if (not isinstance(${arg1_name}, ABCId) and
                ${arg1_name}.get_identifier_namespace() != '${package_name_replace}.${containable_object_name}'):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        ${containable_object_name_under}_map, collection = self._get_${containable_object_name_under}_collection(${arg1_name})
        ${containable_object_name_under}_map['${object_name_mixed}Ids'] = order_ids(${arg0_name}, ${containable_object_name_under}_map['${object_name_mixed}Ids'])
        collection.save(${containable_object_name_under}_map)"""
        }
    }

    remove_object_from_containable_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        ${pattern_name}
        if (not isinstance(${arg1_name}, ABCId) and
                ${arg1_name}.get_identifier_namespace() != '${package_name_replace}.${containable_object_name}'):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        ${containable_object_name_under}_map, collection = self._get_${containable_object_name_under}_collection(${arg1_name})
        try:
            ${containable_object_name_under}_map['${object_name_mixed}Ids'].remove(str(${arg0_name}))
        except (KeyError, ValueError):
            raise errors.NotFound()
        collection.save(${containable_object_name_under}_map)

    def _get_${containable_object_name_under}_collection(self, ${containable_object_name_under}_id):
        \"\"\"Returns a Mongo Collection and ${containable_object_name} given a ${containable_object_name} Id\"\"\"
        collection = JSONClientValidated('${package_name_replace}',
                                         collection='${containable_object_name}',
                                         runtime=self._runtime)
        ${containable_object_name_under}_map = collection.find_one({'_id': ObjectId(${containable_object_name_under}_id.get_identifier())})
        if '${object_name_mixed}Ids' not in ${containable_object_name_under}_map:
            raise errors.NotFound('no ${object_name_plural} are assigned to this ${containable_object_name}')
        return ${containable_object_name_under}_map, collection"""
        }
    }


class GenericObjectSearchSession:

    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..osid.sessions import OsidSession',
                'from ..utilities import JSONClientValidated',
                'from . import queries',
                'from . import searches',
                'from bson.objectid import ObjectId',
                'DESCENDING = -1',
                'ASCENDING = 1'
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    ${pattern_name}
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

    get_object_search_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return searches.${return_type}(runtime=self._runtime)"""
        }
    }

    get_objects_by_search_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        ${pattern_name}
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
        collection = JSONClientValidated('${package_name_replace}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        if ${arg1_name}.start is not None and ${arg1_name}.end is not None:
            result = collection.find(query_terms)[${arg1_name}.start:${arg1_name}.end]
        else:
            result = collection.find(query_terms)
        return searches.${return_type}(result, dict(${arg0_name}._query_terms), runtime=self._runtime)"""
        }
    }


class GenericRelationshipAdminSession(object):
    get_relationship_form_for_create_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}, ${arg2_name}):
        ${doc_string}
        ${pattern_name}
        # These really need to be in module imports:
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from ${arg2_abcapp_name}.${arg2_abcpkg_name}.${arg2_module} import ${arg2_type} as ABC${arg2_type}
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('argument is not a valid OSID ${arg0_type}')
        if not isinstance(${arg1_name}, ABC${arg1_type}):
            raise errors.InvalidArgument('argument is not a valid OSID ${arg1_type}')
        for arg in ${arg2_name}:
            if not isinstance(arg, ABC${arg2_type}):
                raise errors.InvalidArgument('one or more argument array elements is not a valid OSID ${arg2_type}')
        if ${arg2_name} == []:
            # WHY are we passing ${cat_name_under}_id = self._catalog_id below, seems redundant:
            obj_form = objects.${return_type}(
                ${cat_name_under}_id=self._catalog_id,
                ${arg0_name}=${arg0_name},
                ${arg1_name}=${arg1_name},
                catalog_id=self._catalog_id,
                runtime=self._runtime,
                proxy=self._proxy)
        else:
            obj_form = objects.${return_type}(
                ${cat_name_under}_id=self._catalog_id,
                record_types=${arg2_name},
                ${arg0_name}=${arg0_name},
                ${arg1_name}=${arg1_name},
                catalog_id=self._catalog_id,
                runtime=self._runtime,
                proxy=self._proxy)
        obj_form._for_update = False
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form"""
        }
    }

    get_relationship_form_for_create_for_agent_import_templates = {
        'python': {
            'json': [
                'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}',
                'from ${arg1_abcapp_name}.${arg1_abcpkg_name}.${arg1_module} import ${arg1_type} as ABC${arg1_type}'
            ]
        }
    }

    get_relationship_form_for_create_for_agent_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        ${pattern_name}
        # These really need to be in module imports:
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('argument is not a valid OSID ${arg0_type}')
        for arg in ${arg1_name}:
            if not isinstance(arg, ABC${arg1_type}):
                raise errors.InvalidArgument('one or more argument array elements is not a valid OSID ${arg1_type}')
        if ${arg1_name} == []:
            # WHY are we passing ${cat_name_under}_id = self._catalog_id below, seems redundant:
            # Probably don't need to send effective_agent_id, since the form can get that from proxy.
            obj_form = objects.${return_type}(
                ${cat_name_under}_id=self._catalog_id,
                ${arg0_name}=${arg0_name},
                effective_agent_id=str(self.get_effective_agent_id()),
                catalog_id=self._catalog_id,
                runtime=self._runtime,
                proxy=self._proxy)
        else:
            obj_form = objects.${return_type}(
                ${cat_name_under}_id=self._catalog_id,
                record_types=${arg1_name},
                ${arg0_name}=${arg0_name},
                effective_agent_id=self.get_effective_agent_id(),
                catalog_id=self._catalog_id,
                runtime=self._runtime,
                proxy=self._proxy)
        obj_form._for_update = False
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form"""
        }
    }

    # Should the following methods be in a "GenericObjectRequisiteAssignmentSession" class?
    assign_object_requisite_import_templates = {
        'python': {
            'json': [
                'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}',
                'from ${arg1_abcapp_name}.${arg1_abcpkg_name}.${arg1_module} import ${arg1_type} as ABC${arg1_type}'
            ]
        }
    }

    assign_object_requisite_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        ${pattern_name}
        requisite_type = Type(**Relationship().get_type_data('${object_name_upper}.REQUISITE'))

        ras = self._get_provider_manager(
            'RELATIONSHIP').get_relationship_admin_session_for_family(
            self.get_${cat_name_under}_id(), proxy=self._proxy)
        rfc = ras.get_relationship_form_for_create(${arg0_name}, ${arg1_name}, [])
        rfc.set_display_name('${object_name} Requisite')
        rfc.set_description('An ${object_name} Requisite created by the ${object_name}RequisiteAssignmentSession')
        rfc.set_genus_type(requisite_type)
        ras.create_relationship(rfc)"""
        }
    }

    unassign_object_requisite_import_templates = {
        'python': {
            'json': [
                'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}',
                'from ${arg1_abcapp_name}.${arg1_abcpkg_name}.${arg1_module} import ${arg1_type} as ABC${arg1_type}',
            ]
        }
    }

    unassign_object_requisite_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        ${pattern_name}
        requisite_type = Type(**Relationship().get_type_data('${object_name_upper}.REQUISITE'))
        rls = self._get_provider_manager(
            'RELATIONSHIP').get_relationship_lookup_session_for_family(
            self.get_${cat_name_under}_id(), proxy=self._proxy)
        ras = self._get_provider_manager(
            'RELATIONSHIP').get_relationship_admin_session_for_family(
            self.get_${cat_name_under}_id(), proxy=self._proxy)
        rls.use_federated_family_view()
        relationships = rls.get_relationships_by_genus_type_for_source(${arg0_name}, requisite_type)
        if relationships.available() == 0:
            raise errors.IllegalState('no ${object_name} found')
        for relationship in relationships:
            if str(relationship.get_destination_id()) == str(${arg1_name}):
                ras.delete_relationship(relationship.ident)"""
        }
    }


class GenericDependentObjectAdminSession(object):
    # Dependent is a non-OSID term. Here it means things which are administered through a "parent" object
    #   AdminSession. For example, AssetContents are administered through an AssetAdminSession, Questions / Answers
    #   are administered through ItemAdminSession.
    # Furthermore, in general you cannot GET any of the "dependent" objects without going through the parent object, i.e.
    #   Asset.get_asset_contents()
    #   Item.get_answers()
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from bson.objectid import ObjectId',
                'from ..utilities import JSONClientValidated',
                'CREATED = True',
                'UPDATED = True',
            ]
        }
    }

    create_dependent_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        collection = JSONClientValidated('${package_name}',
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
        return ${return_type}(
            osid_object_map=${arg0_name}._my_map,
            runtime=self._runtime,
            proxy=self._proxy)"""
        }
    }

    get_dependent_object_form_for_update_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from .${return_module} import ${return_type}
        collection = JSONClientValidated('${package_name}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        document = collection.find_one({'${aggregated_objects_name_mixed}._id': ObjectId(${arg0_name}.get_identifier())})
        for sub_doc in document['${aggregated_objects_name_mixed}']:  # There may be a MongoDB shortcut for this
            if sub_doc['_id'] == ObjectId(${arg0_name}.get_identifier()):
                result = sub_doc
        obj_form = ${return_type}(
            osid_object_map=result,
            runtime=self._runtime,
            proxy=self._proxy)
        obj_form._for_update = True
        self._forms[obj_form.get_id().get_identifier()] = not UPDATED
        return obj_form"""
        }
    }

    update_dependent_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        collection = JSONClientValidated('${package_name}',
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
        ${object_name_under}_id = Id(${arg0_name}._my_map['${object_name_mixed}Id']).get_identifier()
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
        except:  # what exceptions does mongodb save raise?
            raise errors.OperationFailed()
        self._forms[${arg0_name}.get_id().get_identifier()] = UPDATED
        # Note: this is out of spec. The OSIDs don't require an object to be returned:
        from .objects import ${aggregated_object_name}

        return ${aggregated_object_name}(
            osid_object_map=${arg0_name}._my_map,
            runtime=self._runtime,
            proxy=self._proxy)"""
        }
    }

    delete_dependent_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from .objects import ${aggregated_object_name}
        collection = JSONClientValidated('${package_name}',
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
        ${aggregated_object_name}(
            osid_object_map=${aggregated_object_name_under}_map,
            runtime=self._runtime,
            proxy=self._proxy)._delete()
        collection.save(${object_name_under})"""
        }
    }


class GenericRequisiteObjectAdminSession:
    # For Objectives right now -- because when they get deleted, have to remove them from Activity as wel

    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
                'from ..utilities import JSONClientValidated',
            ]
        }
    }

    delete_requisite_object_import_templates = {
        'python': {
            'json': [
                'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}'
            ]
        }
    }

    delete_requisite_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}

        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        collection = JSONClientValidated('${package_name_replace}',
                                         collection='${dependent_object_name}',
                                         runtime=self._runtime)
        if collection.find({'${object_name_mixed}Id': str(${arg0_name})}).count() != 0:
            raise errors.IllegalState('there are still ${dependent_object_name}s associated with this ${object_name}')

        collection = JSONClientValidated('${package_name_replace}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        collection.delete_one({'_id': ObjectId(${arg0_name}.get_identifier())})"""
        }
    }


class GenericObjectHierarchySession(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..utilities import JSONClientValidated',
            ]
        }
    }

    get_root_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        root_ids = self._hierarchy_session.get_roots()
        collection = JSONClientValidated('${package_name_replace}',
                                         collection='${object_name}',
                                         runtime=self._runtime)
        result = collection.find(
            dict({'_id': {'$$in': [ObjectId(root_id.get_identifier()) for root_id in root_ids]}},
                 **self._view_filter()))
        return objects.${return_type}(
            result,
            runtime=self._runtime,
            proxy=self._proxy)"""
        }
    }

    get_child_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        if self._hierarchy_session.has_children(${arg0_name}):
            child_ids = self._hierarchy_session.get_children(${arg0_name})
            collection = JSONClientValidated('${package_name_replace}',
                                             collection='${object_name}',
                                             runtime=self._runtime)
            result = collection.find(
                dict({'_id': {'$$in': [ObjectId(child_id.get_identifier()) for child_id in child_ids]}},
                     **self._view_filter()))
            return objects.${return_type}(
                result,
                runtime=self._runtime,
                proxy=self._proxy)
        raise errors.IllegalState('no children')"""
        }
    }


class GenericObjectHierarchyDesignSession(object):
    add_root_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        return self._hierarchy_session.add_root(id_=${arg0_name})"""
        }
    }

    add_child_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        ${pattern_name}
        return self._hierarchy_session.add_child(id_=${arg0_name}, child_id=${arg1_name})"""
        }
    }

    remove_root_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        return self._hierarchy_session.remove_root(id_=${arg0_name})"""
        }
    }

    can_modify_object_hierarchy_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return True"""
        }
    }

    remove_child_object_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        ${pattern_name}
        return self._hierarchy_session.remove_child(id_=${arg0_name}, child_id=${arg1_name})"""
        }
    }

    remove_child_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        return self._hierarchy_session.remove_children(id_=${arg0_name})"""
        }
    }
