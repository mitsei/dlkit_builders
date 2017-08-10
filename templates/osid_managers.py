from copy import deepcopy


class GenericAdapterProfileAndManager(object):
    method_no_args = {
        'python': {
            'services': """
    def ${method_name}(self):
        \"\"\"Pass through to provider ${method_name}\"\"\"
        ${pattern_name}
        return self._provider_manager.${method_name}()"""
        }
    }

    # Need to do this separately because in services, we might pass
    #  ``proxy``, but the pattern doesn't know this
    method_with_args = {
        'python': {
            'services': """
    def ${method_name}(self, *args, **kwargs):
        \"\"\"Pass through to provider ${method_name}\"\"\"
        ${pattern_name}
        return self._provider_manager.${method_name}(*args, **kwargs)"""
        }
    }

    sub_package_method = {
        'python': {
            'services': """
    def ${method_name}(self, *args, **kwargs):
        \"\"\"Pass through to sub package provider method\"\"\"
        ${pattern_name}
        return self._get_sub_package_provider_manager(
            '${package_name_replace_reserved}').${method_original_name}(*args, **kwargs)"""
        }
    }

    sub_package_method_no_args = {
        'python': {
            'services': """
    def ${method_name}(self):
        \"\"\"Pass through to sub package provider method\"\"\"
        ${pattern_name}
        return self._get_sub_package_provider_manager(
            '${package_name_replace_reserved}').${method_original_name}()"""
        }
    }

    unimplemented_no_args = {
        'python': {
            'manager': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        raise Unimplemented()"""
        }
    }

    unimplemented_one_arg = {
        'python': {
            'manager': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        if ${arg0_name} is None:
            raise NullArgument('${arg0_name} cannot be None')
        raise Unimplemented()"""
        }
    }

    unimplemented_two_args = {
        'python': {
            'manager': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        ${pattern_name}
        if ${arg0_name} is None:
            raise NullArgument('${arg0_name} cannot be None')
        if ${arg1_name} is None:
            raise NullArgument('${arg1_name} cannot be None')
        raise Unimplemented()"""
        }
    }

    return_false = {
        'python': {
            'manager': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return False"""
        }
    }

    return_false_one_arg = {
        'python': {
            'manager': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        if ${arg0_name} is None:
            raise NullArgument('${arg0_name} cannot be None')
        return False"""
        }
    }

    return_typelist = {
        'python': {
            'manager': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return TypeList([])"""
        }
    }

    assert_bool = {
        'python': {
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        assert isinstance(self.mgr.${method_name}(), bool)"""
        }
    }

    assert_type_list = {
        'python': {
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        assert isinstance(self.mgr.${method_name}(), abc_type_list)"""
        }
    }

    get_session_no_proxy = {
        'python': {
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}()"""
        }
    }

    get_session_with_proxy = {
        'python': {
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(PROXY)
        with pytest.raises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""
        }
    }

    get_session_with_receiver_no_proxy = {
        'python': {
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.receiver)
        with pytest.raises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""
        }
    }

    get_session_with_receiver_proxy = {
        'python': {
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.receiver, proxy=PROXY)
        with pytest.raises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""
        }
    }

    get_session_with_catalog_no_proxy = {
        'python': {
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.catalog_id)
        with pytest.raises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""
        }
    }

    get_session_with_catalog_proxy = {
        'python': {
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.catalog_id, PROXY)
        with pytest.raises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""
        }
    }

    get_session_with_catalog_and_receiver_no_proxy = {
        'python': {
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.receiver, self.catalog_id)
        with pytest.raises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""
        }
    }

    get_session_with_catalog_receiver_proxy = {
        'python': {
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.receiver, self.catalog_id, proxy=PROXY)
        with pytest.raises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""
        }
    }


class GenericProfile(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from ..primitives import Type',
                'from ..type.objects import TypeList',
                'from . import sessions',
                'from dlkit.abstract_osid.osid import errors',
                'from . import profile',
                'from ..utilities import get_registry',
            ],
            'manager': [
                'from ..type.objects import TypeList',
                'from ..osid.osid_errors import NullArgument',
            ],
            'tests': [
                'from dlkit.runtime import PROXY_SESSION, proxy_example',
                'from dlkit.runtime.managers import Runtime',
                'REQUEST = proxy_example.SimpleRequest()',
                'CONDITION = PROXY_SESSION.get_proxy_condition()',
                'CONDITION.set_http_request(REQUEST)',
                'PROXY = PROXY_SESSION.get_proxy(CONDITION)',
                'from dlkit.primordium.type.primitives import Type',
                'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
                'from dlkit.abstract_osid.type.objects import TypeList as abc_type_list'
            ]
        }
    }

    init_template = {
        'python': {
            'services': """
    def __init__(self):
        self._provider_manager = None""",
            'authz': """
    def __init__(self):
        osid_managers.OsidProfile.__init__(self)

    def _get_hierarchy_session(self, proxy=None):
        if proxy is not None:
            try:
                return self._provider_manager.get_${cat_name_under}_hierarchy_session(proxy)
            except Unimplemented:
                return None
        try:
            return self._provider_manager.get_${cat_name_under}_hierarchy_session()
        except Unimplemented:
            return None""",
            'tests': """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""
        }
    }

    supports_visible_federation_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return '${method_name}' in profile.SUPPORTS""",
            'services': GenericAdapterProfileAndManager.method_no_args['python']['services'],
            'authz': GenericAdapterProfileAndManager.method_no_args['python']['services'],
            'manager': GenericAdapterProfileAndManager.return_false['python']['manager'],
            'tests': GenericAdapterProfileAndManager.assert_bool['python']['tests']
        }
    }

    supports_object_lookup_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return '${method_name}' in profile.SUPPORTS""",
            'services': GenericAdapterProfileAndManager.method_no_args['python']['services'],
            'authz': GenericAdapterProfileAndManager.method_no_args['python']['services'],
            'manager': GenericAdapterProfileAndManager.return_false['python']['manager'],
            'tests': GenericAdapterProfileAndManager.assert_bool['python']['tests']
        }
    }

    get_object_record_types_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        record_type_maps = get_registry('${object_name_upper}_RECORD_TYPES', self._runtime)
        record_types = []
        for record_type_map in record_type_maps:
            record_types.append(Type(**record_type_maps[record_type_map]))
        return TypeList(record_types)""",
            'services': GenericAdapterProfileAndManager.method_no_args['python']['services'],
            'authz': GenericAdapterProfileAndManager.method_no_args['python']['services'],
            'manager': GenericAdapterProfileAndManager.return_typelist['python']['manager'],
            'tests': GenericAdapterProfileAndManager.assert_type_list['python']['tests']
        }
    }

    supports_object_record_type_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        record_type_maps = get_registry('${object_name_upper}_RECORD_TYPES', self._runtime)
        supports = False
        for record_type_map in record_type_maps:
            if (${arg0_name}.get_authority() == record_type_maps[record_type_map]['authority'] and
                    ${arg0_name}.get_identifier_namespace() == record_type_maps[record_type_map]['namespace'] and
                    ${arg0_name}.get_identifier() == record_type_maps[record_type_map]['identifier']):
                supports = True
        return supports""",
            'services': GenericAdapterProfileAndManager.method_no_args['python']['services'],
            'manager': GenericAdapterProfileAndManager.return_false_one_arg['python']['manager'],
            'tests': GenericAdapterProfileAndManager.assert_bool['python']['tests']
        }
    }

    get_type_list_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return TypeList([])""",
            'services': GenericAdapterProfileAndManager.method_no_args['python']['services'],
            'manager': GenericAdapterProfileAndManager.return_typelist['python']['manager'],
            'tests': GenericAdapterProfileAndManager.assert_type_list['python']['tests']
        }
    }

    supports_type_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return False""",
            'services': GenericAdapterProfileAndManager.method_no_args['python']['services'],
            'manager': GenericAdapterProfileAndManager.return_false_one_arg['python']['manager'],
            'tests': GenericAdapterProfileAndManager.assert_bool['python']['tests']
        }
    }


class GenericManager(object):

    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
            ],
            'manager': [
                'from ..osid.osid_errors import Unimplemented',
                'from ..osid.osid_errors import NullArgument',
            ],
            'tests': [
                'from dlkit.abstract_osid.osid import errors'
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    def __init__(self):
        osid_managers.OsidManager.__init__(self)""",
            'services': """
    def __init__(self, proxy=None):
        self._runtime = None
        self._provider_manager = None
        self._provider_sessions = dict()
        self._session_management = AUTOMATIC
        self._${cat_name_under}_view = DEFAULT
        # This is to initialize self._proxy
        osid.OsidSession.__init__(self, proxy)
        self._sub_package_provider_managers = dict()

    def _set_${cat_name_under}_view(self, session):
        \"\"\"Sets the underlying ${cat_name_under} view to match current view\"\"\"
        if self._${cat_name_under}_view == COMPARATIVE:
            try:
                session.use_comparative_${cat_name_under}_view()
            except AttributeError:
                pass
        else:
            try:
                session.use_plenary_${cat_name_under}_view()
            except AttributeError:
                pass

    def _get_provider_session(self, session_name, proxy=None):
        \"\"\"Gets the session for the provider\"\"\"
        agent_key = self._get_agent_key(proxy)
        if session_name in self._provider_sessions[agent_key]:
            return self._provider_sessions[agent_key][session_name]
        else:
            session = self._instantiate_session('get_' + session_name, self._proxy)
            self._set_${cat_name_under}_view(session)
            if self._session_management != DISABLED:
                self._provider_sessions[agent_key][session_name] = session
            return session

    def _get_sub_package_provider_manager(self, sub_package_name):
        if sub_package_name in self._sub_package_provider_managers:
            return self._sub_package_provider_managers[sub_package_name]
        config = self._runtime.get_configuration()
        parameter_id = Id('parameter:{0}ProviderImpl@dlkit_service'.format(sub_package_name))
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        if self._proxy is None:
            # need to add version argument
            sub_package = self._runtime.get_manager(sub_package_name.upper(), provider_impl)
        else:
            # need to add version argument
            sub_package = self._runtime.get_proxy_manager(sub_package_name.upper(), provider_impl)
        self._sub_package_provider_managers[sub_package_name] = sub_package
        return sub_package

    def _get_sub_package_provider_session(self, sub_package, session_name, proxy=None):
        \"\"\"Gets the session from a sub-package\"\"\"
        agent_key = self._get_agent_key(proxy)
        if session_name in self._provider_sessions[agent_key]:
            return self._provider_sessions[agent_key][session_name]
        else:
            manager = self._get_sub_package_provider_manager(sub_package)
            session = self._instantiate_session('get_' + session_name + '_for_bank',
                                                proxy=self._proxy,
                                                manager=manager)
            self._set_bank_view(session)
            if self._session_management != DISABLED:
                self._provider_sessions[agent_key][session_name] = session
            return session

    def _instantiate_session(self, method_name, proxy=None, *args, **kwargs):
        \"\"\"Instantiates a provider session\"\"\"
        session_class = getattr(self._provider_manager, method_name)
        if proxy is None:
            try:
                return session_class(bank_id=self._catalog_id, *args, **kwargs)
            except AttributeError:
                return session_class(*args, **kwargs)
        else:
            try:
                return session_class(bank_id=self._catalog_id, proxy=proxy, *args, **kwargs)
            except AttributeError:
                return session_class(proxy=proxy, *args, **kwargs)

    def initialize(self, runtime):
        \"\"\"OSID Manager initialize\"\"\"
        from .primitives import Id
        if self._runtime is not None:
            raise IllegalState('Manager has already been initialized')
        self._runtime = runtime
        config = runtime.get_configuration()
        parameter_id = Id('parameter:${pkg_name_replaced}ProviderImpl@dlkit_service')
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        if self._proxy is None:
            # need to add version argument
            self._provider_manager = runtime.get_manager('${pkg_name_upper}', provider_impl)
        else:
            # need to add version argument
            self._provider_manager = runtime.get_proxy_manager('${pkg_name_upper}', provider_impl)

    def close_sessions(self):
        \"\"\"Close all sessions, unless session management is set to MANDATORY\"\"\"
        if self._session_management != MANDATORY:
            self._provider_sessions = dict()

    def use_automatic_session_management(self):
        \"\"\"Session state will be saved unless closed by consumers\"\"\"
        self._session_management = AUTOMATIC

    def use_mandatory_session_management(self):
        \"\"\"Session state will be saved and can not be closed by consumers\"\"\"
        self._session_management = MANDATORY

    def disable_session_management(self):
        \"\"\"Session state will never be saved\"\"\"
        self._session_management = DISABLED
        self.close_sessions()""",
            'authz': """
    def __init__(self):
        ${pkg_name_replaced_caps}Profile.__init__(self)

    def initialize(self, runtime):
        osid_managers.OsidManager.initialize(self, runtime)
        config = self._my_runtime.get_configuration()
        parameter_id = Id('parameter:${pkg_name_replaced}ProviderImpl@authz_adapter')
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        self._provider_manager = runtime.get_manager('${pkg_name_replaced_upper}', provider_impl)
        # need to add version argument""",
            'tests': """
class NotificationReceiver(object):
    # Implemented from resource.ResourceManager
    pass


@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # Implemented from resource.ResourceManager
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${pkg_name} manager tests'
        catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        request.cls.catalog_id = catalog.get_id()
        request.cls.receiver = NotificationReceiver()
    else:
        request.cls.catalog_id = Id('resource.Resource%3A000000000000000000000000%40DLKIT.MIT.EDU')

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog_id)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # Implemented from resource.ResourceManager
    pass"""
        }
    }

    get_object_lookup_session_template = {
        'python': {
            'json': """
    def ${method_name}(self, **kwargs):
        ${doc_string}
        ${pattern_name}
        if not self.supports_${support_check}():
            raise errors.Unimplemented()
        if 'proxy' in kwargs:
            return ${return_module}.${return_type}(proxy=kwargs['proxy'], runtime=self._runtime)
        return ${return_module}.${return_type}(runtime=self._runtime)""",
            'services': GenericAdapterProfileAndManager.method_with_args['python']['services'],
            'authz': """
    def ${method_name}(self):
        ${pattern_name}
        try:
            query_session = self._provider_manager.get_${object_name_under}_query_session()
            query_session.use_federated_${cat_name_under}_view()
        except Unimplemented:
            query_session = None
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            hierarchy_session=self._get_hierarchy_session(),
            query_session=query_session)""",
            'manager': GenericAdapterProfileAndManager.unimplemented_no_args['python']['manager'],
            'tests': GenericAdapterProfileAndManager.get_session_no_proxy['python']['tests']
        }
    }

    get_object_admin_session_template = deepcopy(get_object_lookup_session_template)
    get_object_admin_session_template['python']['authz'] = """
    def ${method_name}(self):
        ${pattern_name}
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            provider_manager=self._provider_manager)"""

    get_object_lookup_session_for_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, **kwargs):
        ${doc_string}
        ${pattern_name}
        if not self.supports_${support_check}():
            raise errors.Unimplemented()
        ##
        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        ##
        # pylint: disable=no-member
        if 'proxy' in kwargs:
            return ${return_module}.${return_type}(
                ${arg0_name},
                proxy=kwargs['proxy'],
                runtime=self._runtime)
        return ${return_module}.${return_type}(${arg0_name}, runtime=self._runtime)""",
            'services': GenericAdapterProfileAndManager.method_with_args['python']['services'],
            'authz': """
    def ${method_name}(self, ${arg0_name}):
        ${pattern_name}
        try:
            query_session = self._provider_manager.get_${object_name_under}_query_session_for_${cat_name_under}(${arg0_name})
            query_session.use_federated_${cat_name_under}_view()
        except Unimplemented:
            query_session = None
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(${arg0_name}),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            hierarchy_session=self._get_hierarchy_session(),
            query_session=query_session)""",
            'manager': GenericAdapterProfileAndManager.unimplemented_one_arg['python']['manager'],
            'tests': GenericAdapterProfileAndManager.get_session_with_catalog_no_proxy['python']['tests']
        }
    }

    get_object_admin_session_for_catalog_template = deepcopy(get_object_lookup_session_for_catalog_template)
    get_object_admin_session_for_catalog_template['python']['authz'] = """
    def ${method_name}(self, ${arg0_name}):
        ${pattern_name}
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(${arg0_name}),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            provider_manager=self._provider_manager)"""

    get_object_notification_session_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, **kwargs):
        ${doc_string}
        ${pattern_name}
        if not self.supports_${support_check}():
            raise errors.Unimplemented()
        # pylint: disable=no-member
        if 'proxy' in kwargs:
            return ${return_module}.${return_type}(
                proxy=kwargs['proxy'],
                runtime=self._runtime,
                receiver=${arg0_name})
        return ${return_module}.${return_type}(runtime=self._runtime, receiver=${arg0_name})""",
            'services': GenericAdapterProfileAndManager.method_with_args['python']['services'],
            'authz': """
    def ${method_name}(self, ${arg0_name}):
        ${pattern_name}
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(${arg0_name}),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            provider_manager=self._provider_manager)""",
            'manager': GenericAdapterProfileAndManager.unimplemented_one_arg['python']['manager'],
            'tests': GenericAdapterProfileAndManager.get_session_with_receiver_no_proxy['python']['tests']
        }
    }

    get_object_notification_session_for_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}, **kwargs):
        ${doc_string}
        ${pattern_name}
        if not self.supports_${support_check}():
            raise errors.Unimplemented()
        ##
        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        ##
        # pylint: disable=no-member
        if 'proxy' in kwargs:
            return ${return_module}.${return_type}(
                catalog_id=${arg1_name},
                proxy=kwargs['proxy'],
                runtime=self._runtime,
                receiver=${arg0_name})
        return ${return_module}.${return_type}(
            catalog_id=${arg1_name},
            runtime=self._runtime,
            receiver=${arg0_name})""",
            'services': GenericAdapterProfileAndManager.method_with_args['python']['services'],
            'authz': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${pattern_name}
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(${arg0_name}, ${arg1_name}),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            provider_manager=self._provider_manager)""",
            'manager': GenericAdapterProfileAndManager.unimplemented_two_args['python']['manager'],
            'tests': GenericAdapterProfileAndManager.get_session_with_catalog_and_receiver_no_proxy['python']['tests']
        }
    }

    get_object_smart_catalog_session_template = {
        'python': {
            'manager': GenericAdapterProfileAndManager.unimplemented_one_arg['python']['manager'],
            'tests': GenericAdapterProfileAndManager.get_session_no_proxy['python']['tests']
        }
    }

    get_object_batch_manager_template = {
        'python': {
            'manager': GenericAdapterProfileAndManager.unimplemented_no_args['python']['manager'],
            'tests': GenericAdapterProfileAndManager.get_session_no_proxy['python']['tests']
        }
    }


class GenericProxyManager(object):
    import_statements_template = {
        'python': {
            'tests': [
                'from dlkit.abstract_osid.osid import errors',
                'from dlkit.primordium.id.primitives import Id'
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    ${pattern_name}
    def __init__(self):
        osid_managers.OsidProxyManager.__init__(self)""",
            'authz': """
    def __init__(self):
        ${pkg_name_replaced_caps}Profile.__init__(self)

    def initialize(self, runtime):
        osid_managers.OsidProxyManager.initialize(self, runtime)
        config = self._my_runtime.get_configuration()
        parameter_id = Id('parameter:${pkg_name_replaced}ProviderImpl@authz_adapter')
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        self._provider_manager = runtime.get_proxy_manager('${pkg_name_replaced_upper}', provider_impl)
        # need to add version argument""",
            'tests': """
class NotificationReceiver(object):
    # Implemented from resource.ResourceProxyManager
    pass


@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # Implemented from resource.ResourceProxyManager
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)

    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${pkg_name} proxy manager tests'
        catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        request.cls.catalog_id = catalog.get_id()
    else:
        request.cls.catalog_id = Id('resource.Resource%3A000000000000000000000000%40DLKIT.MIT.EDU')
    request.cls.receiver = NotificationReceiver()

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog_id)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # Implemented from resource.ResourceProxyManager
    pass"""
        }
    }

    get_object_lookup_session_template = {
        'python': {
            'tests': GenericAdapterProfileAndManager.get_session_with_proxy['python']['tests']
        }
    }

    get_object_admin_session_template = deepcopy(get_object_lookup_session_template)

    get_object_lookup_session_for_catalog_template = {
        'python': {
            'tests': GenericAdapterProfileAndManager.get_session_with_catalog_proxy['python']['tests']
        }
    }

    get_object_admin_session_for_catalog_template = deepcopy(get_object_lookup_session_for_catalog_template)

    get_object_notification_session_template = {
        'python': {
            'tests': GenericAdapterProfileAndManager.get_session_with_receiver_proxy['python']['tests']
        }
    }

    get_object_notification_session_for_catalog_template = {
        'python': {
            'tests': GenericAdapterProfileAndManager.get_session_with_catalog_receiver_proxy['python']['tests']
        }
    }

    get_object_smart_catalog_session_template = {
        'python': {
            'tests': GenericAdapterProfileAndManager.get_session_with_proxy['python']['tests']
        }
    }

    get_object_batch_proxy_manager_template = {
        'python': {
            'tests': GenericAdapterProfileAndManager.get_session_with_proxy['python']['tests']
        }
    }