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
            ]
        }
    }

    init_template = {
        'python': {
            'services': """
    def __init__(self):
        self._provider_manager = None"""
        }
    }

    supports_visible_federation_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return '${method_name}' in profile.SUPPORTS""",
            'services': GenericAdapterProfileAndManager.method_no_args['python']['services']
        }
    }

    supports_object_lookup_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return '${method_name}' in profile.SUPPORTS""",
            'services': GenericAdapterProfileAndManager.method_no_args['python']['services']
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
            'services': GenericAdapterProfileAndManager.method_no_args['python']['services']
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
            'services': GenericAdapterProfileAndManager.method_no_args['python']['services']
        }
    }

    get_type_list_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return TypeList([])""",
            'services': GenericAdapterProfileAndManager.method_no_args['python']['services']
        }
    }

    supports_type_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return False""",
            'services': GenericAdapterProfileAndManager.method_no_args['python']['services']
        }
    }


class GenericManager(object):

    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
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
        self.close_sessions()"""
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
            'services': GenericAdapterProfileAndManager.method_with_args['python']['services']
        }
    }

    get_object_admin_session_template = get_object_lookup_session_template

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
            'services': GenericAdapterProfileAndManager.method_with_args['python']['services']
        }
    }

    get_object_admin_session_for_catalog_template = get_object_lookup_session_for_catalog_template

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
            'services': GenericAdapterProfileAndManager.method_with_args['python']['services']
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
            'services': GenericAdapterProfileAndManager.method_with_args['python']['services']
        }
    }


class GenericProxyManager(object):
    init_template = {
        'python': {
            'json': """
    ${pattern_name}
    def __init__(self):
        osid_managers.OsidProxyManager.__init__(self)"""
        }
    }
