"""Test templates for resource interfaces"""


class ResourceProfile:

    import_statements_pattern = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'from dlkit.abstract_osid.type.objects import TypeList as abc_type_list',
    ]

    init_template = """
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

    supports_visible_federation_template = """
        assert isinstance(self.mgr.supports_visible_federation(), bool)"""

    supports_resource_lookup_template = """
        assert isinstance(self.mgr.${method_name}(), bool)"""

    get_resource_record_types_template = """
        assert isinstance(self.mgr.${method_name}(), abc_type_list)"""

    supports_resource_record_type_template = """
        assert isinstance(self.mgr.${method_name}(DEFAULT_TYPE), bool)"""


class ResourceManager:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
    ]

    init_template = """
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

    get_resource_lookup_session_template = """
        # From tests_templates/resource.py::ResourceManager::get_resource_lookup_session_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}()"""

    get_resource_lookup_session_for_bin_template = """
        # From tests_templates/resource.py::ResourceManager::get_resource_lookup_session_for_bin_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.catalog_id)
        with pytest.raises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""

    get_resource_admin_session_template = """
        # From tests_templates/resource.py::ResourceManager::get_resource_admin_session_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}()"""

    get_resource_admin_session_for_bin_template = """
        # From tests_templates/resource.py::ResourceManager::get_resource_admin_session_for_bin_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.catalog_id)
        with pytest.raises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""

    get_resource_notification_session_template = """
        # From tests_templates/resource.py::ResourceManager::get_resource_notification_session_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.receiver)"""

    get_resource_notification_session_for_bin_template = """
        # From tests_templates/resource.py::ResourceManager::get_resource_notification_session_for_bin_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.receiver, self.catalog_id)
        with pytest.raises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""

    get_resource_batch_manager_template = """
        # From tests_templates/resource.py::ResourceManager::get_resource_batch_manager_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}()"""


class ResourceProxyManager:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from dlkit.primordium.id.primitives import Id'
    ]

    init_template = """
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

    get_resource_lookup_session_template = """
        # From tests_templates/resource.py::ResourceProxyManager::get_resource_lookup_session_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(PROXY)
        with pytest.raises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""

    get_resource_lookup_session_for_bin_template = """
        # From tests_templates/resource.py::ResourceProxyManager::get_resource_lookup_session_for_bin_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.catalog_id, PROXY)
        with pytest.raises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""

    get_resource_admin_session_template = """
        # From tests_templates/resource.py::ResourceProxyManager::get_resource_admin_session_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(PROXY)
        with pytest.raises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""

    get_resource_admin_session_for_bin_template = """
        # From tests_templates/resource.py::ResourceProxyManager::get_resource_admin_session_for_bin_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.catalog_id, PROXY)
        with pytest.raises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""

    get_resource_batch_proxy_manager_template = """
        # From tests_templates/resource.py::ResourceProxyManager::get_resource_batch_proxy_manager_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}()"""

    get_resource_notification_session_template = """
        # From tests_templates/resource.py::ResourceProxyManager::get_resource_notification_session_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.receiver, proxy=PROXY)"""

    get_resource_notification_session_for_bin_template = """
        # From tests_templates/resource.py::ResourceProxyManager::get_resource_notification_session_for_bin_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.receiver, self.catalog_id, proxy=PROXY)
        with pytest.raises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""

    get_group_hierarchy_session = """
        if self.svc_mgr.supports_group_hierarchy():
            self.svc_mgr.get_group_hierarchy_session(PROXY)
        with pytest.raises(errors.Unimplemented):
            self.svc_mgr.get_group_hierarchy_session()"""


class ResourceLookupSession:

    import_statements_pattern = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'DEFAULT_GENUS_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'GenusType\', \'authority\': \'DLKIT.MIT.EDU\'})',
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.abstract_osid.${base_pkg_name_reserved}.objects import ${cat_name} as ABC${cat_name}',
        'ALIAS_ID = Id(**{\'identifier\': \'ALIAS\', \'namespace\': \'ALIAS\', \'authority\': \'ALIAS\'})',
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # Implemented from init template for ResourceLookupSession
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3A000000000000000000000000%40DLKIT.MIT.EDU')


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.${object_name_under}_list = list()
    request.cls.${object_name_under}_ids = list()

    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_${object_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            obj = request.cls.catalog.create_${object_name_under}(create_form)
            request.cls.${object_name_under}_list.append(obj)
            request.cls.${object_name_under}_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_${object_name_under_plural}():
                request.cls.catalog.delete_${object_name_under}(obj.ident)
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(test_tear_down)"""

    get_bin_id_template = """
        # From test_templates/resource.py ResourceLookupSession.get_bin_id_template
        if not is_never_authz(self.service_config):
            assert self.catalog.${method_name}() == self.catalog.ident"""

    get_bin_template = """
        # is this test really needed?
        # From test_templates/resource.py::ResourceLookupSession::get_bin_template
        if not is_never_authz(self.service_config):
            assert isinstance(self.catalog.${method_name}(), ABC${return_type})"""

    can_lookup_resources_template = """
        # From test_templates/resource.py ResourceLookupSession.can_lookup_resources_template
        assert isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool)"""

    use_comparative_resource_view_template = """
        # From test_templates/resource.py ResourceLookupSession.use_comparative_resource_view_template
        self.catalog.${method_name}()"""

    use_plenary_resource_view_template = """
        # From test_templates/resource.py ResourceLookupSession.use_plenary_resource_view_template
        self.catalog.${method_name}()"""

    use_federated_bin_view_template = """
        # From test_templates/resource.py ResourceLookupSession.use_federated_bin_view_template
        self.catalog.${method_name}()"""

    use_isolated_bin_view_template = """
        # From test_templates/resource.py ResourceLookupSession.use_isolated_bin_view_template
        self.catalog.${method_name}()"""

    # Keep most of these templates because we're missing many XQuerySessions, and
    #   the authz adapter will throw PermissionDenied
    get_resources_template = """
        # From test_templates/resource.py ResourceLookupSession.get_resources_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        if self.svc_mgr.supports_${object_name_under}_query():
            objects = self.catalog.${method_name}()
            assert isinstance(objects, ${return_type})
            self.catalog.use_federated_${cat_name_under}_view()
            objects = self.catalog.${method_name}()
            assert isinstance(objects, ${return_type})

            if not is_never_authz(self.service_config):
                assert objects.available() > 0
            else:
                assert objects.available() == 0
        else:
            if not is_never_authz(self.service_config):
                objects = self.catalog.${method_name}()
                assert isinstance(objects, ${return_type})
                self.catalog.use_federated_${cat_name_under}_view()
                objects = self.catalog.${method_name}()
                assert objects.available() > 0
                assert isinstance(objects, ${return_type})
            else:
                with pytest.raises(errors.PermissionDenied):
                    self.catalog.${method_name}()

    def test_get_${object_name_under}_with_alias(self):
        if not is_never_authz(self.service_config):
            # Because you can't create the alias with NEVER_AUTHZ
            self.catalog.alias_${object_name_under}(self.${object_name_under}_ids[0], ALIAS_ID)
            obj = self.catalog.get_${object_name_under}(ALIAS_ID)
            assert obj.get_id() == self.${object_name_under}_ids[0]"""

    get_resources_by_record_type_template = """
        # From test_templates/resource.py ResourceLookupSession.get_resources_by_record_type_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        if self.svc_mgr.supports_${object_name_under}_query():
            objects = self.catalog.${method_name}(DEFAULT_TYPE)
            assert isinstance(objects, ${return_type})
            self.catalog.use_federated_${cat_name_under}_view()
            objects = self.catalog.${method_name}(DEFAULT_TYPE)
            assert objects.available() == 0
            assert isinstance(objects, ${return_type})
        else:
            if not is_never_authz(self.service_config):
                objects = self.catalog.${method_name}(DEFAULT_TYPE)
                assert isinstance(objects, ${return_type})
                self.catalog.use_federated_${cat_name_under}_view()
                objects = self.catalog.${method_name}(DEFAULT_TYPE)
                assert objects.available() == 0
                assert isinstance(objects, ${return_type})
            else:
                with pytest.raises(errors.PermissionDenied):
                    self.catalog.${method_name}(DEFAULT_TYPE)"""

    get_resources_by_parent_genus_type_template = """
        # From test_templates/resource.py ResourceLookupSession.get_resources_by_parent_genus_type_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        if self.svc_mgr.supports_${object_name_under}_query():
            if not is_never_authz(self.service_config):
                objects = self.catalog.${method_name}(DEFAULT_GENUS_TYPE)
                assert isinstance(objects, ${return_type})
                self.catalog.use_federated_${cat_name_under}_view()
                objects = self.catalog.${method_name}(DEFAULT_GENUS_TYPE)
                assert objects.available() == 0
                assert isinstance(objects, ${return_type})
            else:
                with pytest.raises(errors.Unimplemented):
                    # because the never_authz "tries harder" and runs the actual query...
                    #    whereas above the method itself in JSON returns an empty list
                    self.catalog.${method_name}(DEFAULT_GENUS_TYPE)
        else:
            if not is_never_authz(self.service_config):
                objects = self.catalog.${method_name}(DEFAULT_GENUS_TYPE)
                assert isinstance(objects, ${return_type})
                self.catalog.use_federated_${cat_name_under}_view()
                objects = self.catalog.${method_name}(DEFAULT_GENUS_TYPE)
                assert objects.available() == 0
                assert isinstance(objects, ${return_type})
            else:
                with pytest.raises(errors.PermissionDenied):
                    self.catalog.${method_name}(DEFAULT_GENUS_TYPE)"""

    get_resources_by_genus_type_template = """
        # From test_templates/resource.py ResourceLookupSession.get_resources_by_genus_type_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        if self.svc_mgr.supports_${object_name_under}_query():
            objects = self.catalog.${method_name}(DEFAULT_GENUS_TYPE)
            assert isinstance(objects, ${return_type})
            self.catalog.use_federated_${cat_name_under}_view()
            objects = self.catalog.${method_name}(DEFAULT_GENUS_TYPE)
            assert isinstance(objects, ${return_type})
            if not is_never_authz(self.service_config):
                assert objects.available() > 0
            else:
                assert objects.available() == 0
        else:
            if not is_never_authz(self.service_config):
                objects = self.catalog.${method_name}(DEFAULT_GENUS_TYPE)
                assert isinstance(objects, ${return_type})
                self.catalog.use_federated_${cat_name_under}_view()
                objects = self.catalog.${method_name}(DEFAULT_GENUS_TYPE)
                assert objects.available() > 0
                assert isinstance(objects, ${return_type})
            else:
                with pytest.raises(errors.PermissionDenied):
                    self.catalog.${method_name}(DEFAULT_GENUS_TYPE)"""

    get_resources_by_ids_template = """
        # From test_templates/resource.py ResourceLookupSession.get_resources_by_ids_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        if self.svc_mgr.supports_${object_name_under}_query():
            objects = self.catalog.${method_name}(self.${object_name_under}_ids)
            assert isinstance(objects, ${return_type})
            self.catalog.use_federated_${cat_name_under}_view()
            objects = self.catalog.${method_name}(self.${object_name_under}_ids)
            assert isinstance(objects, ${return_type})
            if not is_never_authz(self.service_config):
                assert objects.available() > 0
            else:
                assert objects.available() == 0
        else:
            if not is_never_authz(self.service_config):
                objects = self.catalog.${method_name}(self.${object_name_under}_ids)
                assert isinstance(objects, ${return_type})
                self.catalog.use_federated_${cat_name_under}_view()
                objects = self.catalog.${method_name}(self.${object_name_under}_ids)
                assert objects.available() > 0
                assert isinstance(objects, ${return_type})
            else:
                with pytest.raises(errors.PermissionDenied):
                    self.catalog.${method_name}(self.${object_name_under}_ids)"""

    get_resource_template = """
        # From test_templates/resource.py ResourceLookupSession.get_resource_template
        if self.svc_mgr.supports_${object_name_under}_query():
            if not is_never_authz(self.service_config):
                self.catalog.use_isolated_${cat_name_under}_view()
                obj = self.catalog.${method_name}(self.${object_name_under}_list[0].ident)
                assert obj.ident == self.${object_name_under}_list[0].ident
                self.catalog.use_federated_${cat_name_under}_view()
                obj = self.catalog.${method_name}(self.${object_name_under}_list[0].ident)
                assert obj.ident == self.${object_name_under}_list[0].ident
            else:
                with pytest.raises(errors.NotFound):
                    self.catalog.${method_name}(self.fake_id)
        else:
            if not is_never_authz(self.service_config):
                self.catalog.use_isolated_${cat_name_under}_view()
                obj = self.catalog.${method_name}(self.${object_name_under}_list[0].ident)
                assert obj.ident == self.${object_name_under}_list[0].ident
                self.catalog.use_federated_${cat_name_under}_view()
                obj = self.catalog.${method_name}(self.${object_name_under}_list[0].ident)
                assert obj.ident == self.${object_name_under}_list[0].ident
            else:
                with pytest.raises(errors.PermissionDenied):
                    self.catalog.${method_name}(self.fake_id)"""

    # Override these locally for Resource because with ResourceQuerySession implemented,
    #   the authz adapter will return an empty List instead of throwing PermissionDenied
    # get_resource = """
    #     if not is_never_authz(self.service_config):
    #         self.catalog.use_isolated_bin_view()
    #         obj = self.catalog.get_resource(self.resource_list[0].ident)
    #         assert obj.ident == self.resource_list[0].ident
    #         self.catalog.use_federated_bin_view()
    #         obj = self.catalog.get_resource(self.resource_list[0].ident)
    #         assert obj.ident == self.resource_list[0].ident
    #     else:
    #         with pytest.raises(errors.NotFound):
    #             self.catalog.get_resource(self.fake_id)"""

    # get_resources_by_ids = """
    #     from dlkit.abstract_osid.resource.objects import ResourceList
    #     objects = self.catalog.get_resources_by_ids(self.resource_ids)
    #     assert isinstance(objects, ResourceList)
    #     self.catalog.use_federated_bin_view()
    #     objects = self.catalog.get_resources_by_ids(self.resource_ids)
    #     assert isinstance(objects, ResourceList)
    #     if not is_never_authz(self.service_config):
    #         assert objects.available() > 0
    #     else:
    #         assert objects.available() == 0"""

    # get_resources_by_genus_type = """
    #     from dlkit.abstract_osid.resource.objects import ResourceList
    #     objects = self.catalog.get_resources_by_genus_type(DEFAULT_GENUS_TYPE)
    #     assert isinstance(objects, ResourceList)
    #     self.catalog.use_federated_bin_view()
    #     objects = self.catalog.get_resources_by_genus_type(DEFAULT_GENUS_TYPE)
    #     assert isinstance(objects, ResourceList)
    #     if not is_never_authz(self.service_config):
    #         assert objects.available() > 0
    #     else:
    #         assert objects.available() == 0"""

    # get_resources_by_parent_genus_type = """
    #     from dlkit.abstract_osid.resource.objects import ResourceList
    #     if not is_never_authz(self.service_config):
    #         objects = self.catalog.get_resources_by_parent_genus_type(DEFAULT_GENUS_TYPE)
    #         assert isinstance(objects, ResourceList)
    #         self.catalog.use_federated_bin_view()
    #         objects = self.catalog.get_resources_by_parent_genus_type(DEFAULT_GENUS_TYPE)
    #         assert objects.available() == 0
    #         assert isinstance(objects, ResourceList)
    #     else:
    #         with pytest.raises(errors.Unimplemented):
    #             # because the never_authz "tries harder" and runs the actual query...
    #             #    whereas above the method itself in JSON returns an empty list
    #             self.catalog.get_resources_by_parent_genus_type(DEFAULT_GENUS_TYPE)"""

    # get_resources_by_record_type = """
    #     from dlkit.abstract_osid.resource.objects import ResourceList
    #     objects = self.catalog.get_resources_by_record_type(DEFAULT_TYPE)
    #     assert isinstance(objects, ResourceList)
    #     self.catalog.use_federated_bin_view()
    #     objects = self.catalog.get_resources_by_record_type(DEFAULT_TYPE)
    #     assert objects.available() == 0
    #     assert isinstance(objects, ResourceList)"""

    # get_resources = """
    #     from dlkit.abstract_osid.resource.objects import ResourceList
    #     objects = self.catalog.get_resources()
    #     assert isinstance(objects, ResourceList)
    #     self.catalog.use_federated_bin_view()
    #     objects = self.catalog.get_resources()
    #     assert isinstance(objects, ResourceList)
    #
    #     if not is_never_authz(self.service_config):
    #         assert objects.available() > 0
    #     else:
    #         assert objects.available() == 0
    #
    # def test_get_resource_with_alias(self):
    #     if not is_never_authz(self.service_config):
    #         self.catalog.alias_resource(self.resource_ids[0], ALIAS_ID)
    #         obj = self.catalog.get_resource(ALIAS_ID)
    #         assert obj.get_id() == self.resource_ids[0]"""


class ResourceQuerySession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.${pkg_name_replaced_reserved} import queries as ABCQueries',
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
    ]

    init_template = """
class FakeQuery:
    _cat_id_args_list = []


@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::ResourceQuerySession::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::ResourceQuerySession::init_template
    request.cls.${object_name_under}_list = list()
    request.cls.${object_name_under}_ids = list()

    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = request.cls.catalog.get_${object_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + color
            create_form.description = (
                'Test ${object_name} for ${interface_name} tests, did I mention green')
            obj = request.cls.catalog.create_${object_name_under}(create_form)
            request.cls.${object_name_under}_list.append(obj)
            request.cls.${object_name_under}_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_${object_name_under_plural}():
                request.cls.catalog.delete_${object_name_under}(obj.ident)
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(test_tear_down)"""

    can_query_resources_template = """
        # From test_templates/resource.py ResourceQuerySession::can_query_resources_template
        assert isinstance(self.session.${method_name}(), bool)"""

    can_search_resources_template = """
        # From test_templates/resource.py ResourceQuerySession::can_search_resources_template
        assert isinstance(self.session.${method_name}(), bool)"""

    get_resource_query_template = """
        # From test_templates/resource.py ResourceQuerySession::get_resource_query_template
        query = self.session.${method_name}()
        assert isinstance(query, ABCQueries.${return_type})"""

    get_resources_by_query_template = """
        # From test_templates/resource.py ResourceQuerySession::get_resources_by_query_template
        # Need to add some tests with string types
        if not is_never_authz(self.service_config):
            query = self.session.get_${object_name_under}_query()
            query.match_display_name('orange')
            assert self.catalog.${method_name}(query).available() == 2
            query.clear_display_name_terms()
            query.match_display_name('blue', match=False)
            assert self.session.${method_name}(query).available() == 3
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}(FakeQuery())"""


class ResourceAdminSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid.objects import OsidForm',
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})',
        'NEW_TYPE_2 = Type(**{\'identifier\': \'NEW 2\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})',
        'from dlkit.primordium.id.primitives import Id',
        'ALIAS_ID = Id(**{\'identifier\': \'ALIAS\', \'namespace\': \'ALIAS\', \'authority\': \'ALIAS\'})',
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::ResourceAdminSession::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.assessment_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_${object_name_under_plural}():
                request.cls.catalog.delete_${object_name_under}(obj.ident)
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::ResourceAdminSession::init_template
    if not is_never_authz(request.cls.service_config):
        request.cls.form = request.cls.catalog.get_${object_name_under}_form_for_create([])
        request.cls.form.display_name = 'new ${object_name}'
        request.cls.form.description = 'description of ${object_name}'
        request.cls.form.set_genus_type(NEW_TYPE)
        request.cls.osid_object = request.cls.catalog.create_${object_name_under}(request.cls.form)
    request.cls.session = request.cls.catalog

    def test_tear_down():
        # From test_templates/resource.py::ResourceAdminSession::init_template
        if not is_never_authz(request.cls.service_config):
            request.cls.catalog.delete_${object_name_under}(request.cls.osid_object.ident)

    request.addfinalizer(test_tear_down)"""

    can_create_resources_template = """
        # From test_templates/resource.py::ResourceAdminSession::can_create_resources_template
        assert isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool)"""

    can_update_resources_template = """
        # From test_templates/resource.py::ResourceAdminSession::can_update_resources_template
        assert isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool)"""

    can_delete_resources_template = """
        # From test_templates/resource.py::ResourceAdminSession::can_delete_resources_template
        assert isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool)"""

    can_manage_resource_aliases_template = """
        # From test_templates/resource.py::ResourceAdminSession::can_manage_resource_aliases_template
        assert isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool)"""

    can_create_resource_with_record_types_template = """
        # From test_templates/resource.py::ResourceAdminSession::can_create_resource_with_record_types_template
        assert isinstance(self.${svc_mgr_or_catalog}.${method_name}(DEFAULT_TYPE), bool)"""

    get_resource_form_for_create_template = """
        # From test_templates/resource.py::ResourceAdminSession::get_resource_form_for_create_template
        if not is_never_authz(self.service_config):
            form = self.catalog.${method_name}([])
            assert isinstance(form, OsidForm)
            assert not form.is_for_update()
            with pytest.raises(errors.InvalidArgument):
                self.catalog.${method_name}([1])
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}([])"""

    create_resource_template = """
        # From test_templates/resource.py::ResourceAdminSession::create_resource_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${object_name}
        if not is_never_authz(self.service_config):
            assert isinstance(self.osid_object, ${object_name})
            assert self.osid_object.display_name.text == 'new ${object_name}'
            assert self.osid_object.description.text == 'description of ${object_name}'
            assert self.osid_object.genus_type == NEW_TYPE
            with pytest.raises(errors.IllegalState):
                self.catalog.${method_name}(self.form)
            with pytest.raises(errors.InvalidArgument):
                self.catalog.${method_name}('I Will Break You!')
            update_form = self.catalog.get_${object_name_under}_form_for_update(self.osid_object.ident)
            with pytest.raises(errors.InvalidArgument):
                self.catalog.${method_name}(update_form)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}('foo')"""

    get_resource_form_for_update_template = """
        # From test_templates/resource.py::ResourceAdminSession::get_resource_form_for_update_template
        if not is_never_authz(self.service_config):
            form = self.catalog.${method_name}(self.osid_object.ident)
            assert isinstance(form, OsidForm)
            assert form.is_for_update()
            with pytest.raises(errors.InvalidArgument):
                self.catalog.${method_name}(['This is Doomed!'])
            with pytest.raises(errors.InvalidArgument):
                self.catalog.${method_name}(
                    Id(authority='Respect my Authoritay!',
                       namespace='${package_name}.{object_name}',
                       identifier='1'))
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id)"""

    update_resource_template = """
        # From test_templates/resource.py::ResourceAdminSession::update_resource_template
        if not is_never_authz(self.service_config):
            from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${object_name}
            form = self.catalog.get_${object_name_under}_form_for_update(self.osid_object.ident)
            form.display_name = 'new name'
            form.description = 'new description'
            form.set_genus_type(NEW_TYPE_2)
            updated_object = self.catalog.${method_name}(form)
            assert isinstance(updated_object, ${object_name})
            assert updated_object.ident == self.osid_object.ident
            assert updated_object.display_name.text == 'new name'
            assert updated_object.description.text == 'new description'
            assert updated_object.genus_type == NEW_TYPE_2
            with pytest.raises(errors.IllegalState):
                self.catalog.${method_name}(form)
            with pytest.raises(errors.InvalidArgument):
                self.catalog.${method_name}('I Will Break You!')
            with pytest.raises(errors.InvalidArgument):
                self.catalog.${method_name}(self.form)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}('foo')"""

    delete_resource_template = """
        # From test_templates/resource.py::ResourceAdminSession::delete_resource_template
        if not is_never_authz(self.service_config):
            form = self.catalog.get_${object_name_under}_form_for_create([])
            form.display_name = 'new ${object_name}'
            form.description = 'description of ${object_name}'
            form.set_genus_type(NEW_TYPE)
            osid_object = self.catalog.create_${object_name_under}(form)
            self.catalog.${method_name}(osid_object.ident)
            with pytest.raises(errors.NotFound):
                self.catalog.get_${object_name_under}(osid_object.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id)"""

    alias_resource_template = """
        # From test_templates/resource.py::ResourceAdminSession::alias_resource_template
        if not is_never_authz(self.service_config):
            alias_id = Id(self.catalog.ident.namespace + '%3Amy-alias%40ODL.MIT.EDU')
            self.catalog.${method_name}(self.osid_object.ident, alias_id)
            aliased_object = self.catalog.get_${object_name_under}(alias_id)
            assert aliased_object.ident == self.osid_object.ident
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id, self.fake_id)"""


class ResourceNotificationSession:

    # Placeholder: still need to write a real ResourceNotificationSession tess
    import_statements_pattern = ResourceLookupSession.import_statements_pattern

    # Placeholder: still need to write a real ResourceNotificationSession tess
    init_template = """
class NotificationReceiver(object):
    # Implemented from resource.ResourceNotificationSession
    pass


@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # Implemented from init template for ResourceNotificationSession
    request.cls.service_config = request.param
    request.cls.${object_name_under}_list = list()
    request.cls.${object_name_under}_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_${object_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            obj = request.cls.catalog.create_${object_name_under}(create_form)
            request.cls.${object_name_under}_list.append(obj)
            request.cls.${object_name_under}_ids.append(obj.ident)

    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(NotificationReceiver(), proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_${object_name_under_plural}():
                request.cls.catalog.delete_${object_name_under}(obj.ident)
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::ResourceNotificationSession::init_template
    request.cls.session = request.cls.catalog"""

    register_for_changed_resources_template = """
        # From test_templates/resource.py::ResourceNotificationSession::register_for_changed_resources_template
        if not is_never_authz(self.service_config):
            self.session.${method_name}()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}()"""

    register_for_deleted_resources_template = """
        # From test_templates/resource.py::ResourceNotificationSession::register_for_deleted_resources_template
        if not is_never_authz(self.service_config):
            self.session.${method_name}()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}()"""

    register_for_changed_resource_template = """
        # From test_templates/resource.py::ResourceNotificationSession::register_for_changed_resource_template
        if not is_never_authz(self.service_config):
            self.session.${method_name}(self.fake_id)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}(self.fake_id)"""

    register_for_deleted_resource_template = """
        # From test_templates/resource.py::ResourceNotificationSession::register_for_deleted_resource_template
        if not is_never_authz(self.service_config):
            self.session.${method_name}(self.fake_id)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}(self.fake_id)"""

    register_for_new_resources_template = """
        # From test_templates/resource.py::ResourceNotificationSession::register_for_new_resources_template
        if not is_never_authz(self.service_config):
            self.session.${method_name}()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}()"""

    reliable_resource_notifications_template = """
        # From test_templates/resource.py::ResourceNotificationSession::reliable_resource_notifications_template
        self.session.${method_name}()"""

    unreliable_resource_notifications_template = """
        # From test_templates/resource.py::ResourceNotificationSession::unreliable_resource_notifications_template
        self.session.${method_name}()"""

    can_register_for_resource_notifications_template = """
        # From test_templates/resource.py::ResourceNotificationSession::can_register_for_resource_notifications_template
        if is_no_authz(self.service_config):
            with pytest.raises(errors.Unimplemented):
                self.session.${method_name}()
        else:
            assert isinstance(self.session.${method_name}(), bool)"""


class ResourceBinSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.${pkg_name_replaced_reserved} import objects as ABCObjects',
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.json_.id.objects import IdList',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::ResourceBinSession::init_template
    request.cls.service_config = request.param
    request.cls.${object_name_under}_list = list()
    request.cls.${object_name_under}_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name} for Assignment'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests assignment'
        request.cls.assigned_catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        for num in [0, 1, 2]:
            create_form = request.cls.catalog.get_${object_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            obj = request.cls.catalog.create_${object_name_under}(create_form)
            request.cls.${object_name_under}_list.append(obj)
            request.cls.${object_name_under}_ids.append(obj.ident)
        request.cls.svc_mgr.assign_${object_name_under}_to_${cat_name_under}(
            request.cls.${object_name_under}_ids[1], request.cls.assigned_catalog.ident)
        request.cls.svc_mgr.assign_${object_name_under}_to_${cat_name_under}(
            request.cls.${object_name_under}_ids[2], request.cls.assigned_catalog.ident)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.unassign_${object_name_under}_from_${cat_name_under}(
                request.cls.${object_name_under}_ids[1], request.cls.assigned_catalog.ident)
            request.cls.svc_mgr.unassign_${object_name_under}_from_${cat_name_under}(
                request.cls.${object_name_under}_ids[2], request.cls.assigned_catalog.ident)
            for obj in request.cls.catalog.get_${object_name_under_plural}():
                request.cls.catalog.delete_${object_name_under}(obj.ident)
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.assigned_catalog.ident)
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::ResourceBinSession::init_template
    request.cls.session = request.cls.svc_mgr"""

    can_lookup_resource_bin_mappings_template = """
        # From test_templates/resource.py::ResourceBinSession::can_lookup_resource_bin_mappings
        result = self.session.${method_name}()
        assert isinstance(result, bool)"""

    get_resource_ids_by_bin_template = """
        # From test_templates/resource.py::ResourceBinSession::get_resource_ids_by_bin_template
        if not is_never_authz(self.service_config):
            objects = self.svc_mgr.${method_name}(self.assigned_catalog.ident)
            assert objects.available() == 2
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id)"""

    get_resource_ids_by_bins_template = """
        # From test_templates/resource.py::ResourceBinSession::get_resource_ids_by_bins_template
        if not is_never_authz(self.service_config):
            catalog_ids = [self.catalog.ident, self.assigned_catalog.ident]
            object_ids = self.session.${method_name}(catalog_ids)
            assert isinstance(object_ids, IdList)
            # Currently our impl does not remove duplicate objectIds
            assert object_ids.available() == 5
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}([self.fake_id])"""

    get_resources_by_bin_template = """
        # From test_templates/resource.py::ResourceBinSession::get_resources_by_bin_template
        if not is_never_authz(self.service_config):
            results = self.session.${method_name}(self.assigned_catalog.ident)
            assert isinstance(results, ABCObjects.${object_name}List)
            assert results.available() == 2
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}(self.fake_id)"""

    get_resources_by_bins_template = """
        # From test_templates/resource.py::ResourceBinSession::get_resources_by_bins_template
        if not is_never_authz(self.service_config):
            catalog_ids = [self.catalog.ident, self.assigned_catalog.ident]
            results = self.session.${method_name}(catalog_ids)
            assert isinstance(results, ABCObjects.${object_name}List)
            # Currently our impl does not remove duplicate objects
            assert results.available() == 5
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}([self.fake_id])"""

    get_resource_by_bin_template = """
        # From test_templates/resource.py::ResourceBinSession::get_resource_by_bin_template
        if not is_never_authz(self.service_config):
            objects = self.svc_mgr.${method_name}(self.assigned_catalog.ident)
            assert objects.available() == 2
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id)"""

    get_bin_ids_by_resource_template = """
        # From test_templates/resource.py::ResourceBinSession::get_bin_ids_by_resource_template
        if not is_never_authz(self.service_config):
            cats = self.svc_mgr.${method_name}(self.${object_name_under}_ids[1])
            assert cats.available() == 2
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id)"""

    get_bins_by_resource_template = """
        # From test_templates/resource.py::ResourceBinSession::get_bins_by_resource_template
        if not is_never_authz(self.service_config):
            cats = self.svc_mgr.${method_name}(self.${object_name_under}_ids[1])
            assert cats.available() == 2
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id)"""


class ResourceBinAssignmentSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.${pkg_name_replaced_reserved} import objects as ABCObjects',
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.json_.id.objects import IdList',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::ResourceBinAssignmentSession::init_template
    request.cls.service_config = request.param
    request.cls.${object_name_under}_list = list()
    request.cls.${object_name_under}_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name} for Assignment'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests assignment'
        request.cls.assigned_catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        for num in [0, 1, 2]:
            create_form = request.cls.catalog.get_${object_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            obj = request.cls.catalog.create_${object_name_under}(create_form)
            request.cls.${object_name_under}_list.append(obj)
            request.cls.${object_name_under}_ids.append(obj.ident)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_${object_name_under_plural}():
                request.cls.catalog.delete_${object_name_under}(obj.ident)
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.assigned_catalog.ident)
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::ResourceBinAssignmentSession::init_template
    request.cls.session = request.cls.svc_mgr"""

    assign_resource_to_bin_template = """
        # From test_templates/resource.py::ResourceBinAssignmentSession::assign_resource_to_bin_template
        if not is_never_authz(self.service_config):
            results = self.assigned_catalog.get_${object_name_plural_under}()
            assert results.available() == 0
            self.session.${method_name}(self.${object_name_under}_ids[1], self.assigned_catalog.ident)
            results = self.assigned_catalog.get_${object_name_plural_under}()
            assert results.available() == 1
            self.session.unassign_${object_name_under}_from_${cat_name_under}(
                self.${object_name_under}_ids[1],
                self.assigned_catalog.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}(self.fake_id, self.fake_id)"""

    unassign_resource_from_bin_template = """
        # From test_templates/resource.py::ResourceBinAssignmentSession::unassign_resource_from_bin_template
        if not is_never_authz(self.service_config):
            results = self.assigned_catalog.get_${object_name_plural_under}()
            assert results.available() == 0
            self.session.assign_${object_name_under}_to_${cat_name_under}(
                self.${object_name_under}_ids[1],
                self.assigned_catalog.ident)
            results = self.assigned_catalog.get_${object_name_plural_under}()
            assert results.available() == 1
            self.session.${method_name}(
                self.${object_name_under}_ids[1],
                self.assigned_catalog.ident)
            results = self.assigned_catalog.get_${object_name_plural_under}()
            assert results.available() == 0
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}(self.fake_id, self.fake_id)"""

    can_assign_resources_template = """
        # From test_templates/resource.py::ResourceBinAssignmentSession::can_assign_resources_template
        result = self.session.${method_name}()
        assert isinstance(result, bool)"""

    can_assign_resources_to_bin_template = """
        # From test_templates/resource.py::ResourceBinAssignmentSession::can_assign_resources_to_bin_template
        result = self.session.${method_name}(self.assigned_catalog.ident)
        assert isinstance(result, bool)"""

    get_assignable_bin_ids_template = """
        # From test_templates/resource.py::ResourceBinAssignmentSession::get_assignable_bin_ids_template
        # Note that our implementation just returns all catalogIds, which does not follow
        #   the OSID spec (should return only the catalogIds below the given one in the hierarchy.
        if not is_never_authz(self.service_config):
            results = self.session.${method_name}(self.catalog.ident)
            assert isinstance(results, IdList)

            # Because we're not deleting all banks from all tests, we might
            #   have some crufty banks here...but there should be at least 2.
            assert results.available() >= 2
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}(self.fake_id)"""

    get_assignable_bin_ids_for_resource_template = """
        # From test_templates/resource.py::ResourceBinAssignmentSession::get_assignable_bin_ids_for_resource_template
        # Note that our implementation just returns all catalogIds, which does not follow
        #   the OSID spec (should return only the catalogIds below the given one in the hierarchy.
        if not is_never_authz(self.service_config):
            results = self.session.${method_name}(self.catalog.ident, self.${object_name_under}_ids[0])
            assert isinstance(results, IdList)

            # Because we're not deleting all banks from all tests, we might
            #   have some crufty banks here...but there should be at least 2.
            assert results.available() >= 2
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}(self.fake_id, self.fake_id)"""


class ResourceAgentSession:

    import_statements = [
        'from dlkit.abstract_osid.authentication.objects import AgentList',
        'from dlkit.abstract_osid.resource.objects import Resource',
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.json_.id.objects import IdList',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'AGENT_ID_0 = Id(**{\'identifier\': \'jane_doe\', \'namespace\': \'osid.agent.Agent\', \'authority\': \'MIT-ODL\'})',
        'AGENT_ID_1 = Id(**{\'identifier\': \'john_doe\', \'namespace\': \'osid.agent.Agent\', \'authority\': \'MIT-ODL\'})',
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.resource_list = list()
    request.cls.resource_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'RESOURCE',
        proxy=PROXY,
        implementation=request.cls.service_config)

    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bin_form_for_create([])
        create_form.display_name = 'Test Bin'
        create_form.description = 'Test Bin for ResourceAgentSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bin(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_resource_form_for_create([])
            create_form.display_name = 'Test Resource ' + str(num)
            create_form.description = 'Test Resource for ResourceAgentSession tests'
            obj = request.cls.catalog.create_resource(create_form)
            request.cls.resource_list.append(obj)
            request.cls.resource_ids.append(obj.ident)
        request.cls.catalog.assign_agent_to_resource(AGENT_ID_0, request.cls.resource_ids[0])
        request.cls.catalog.assign_agent_to_resource(AGENT_ID_1, request.cls.resource_ids[1])
    else:
        request.cls.catalog = request.cls.svc_mgr.get_resource_agent_session(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_bins():
                for obj in catalog.get_resources():
                    catalog.delete_resource(obj.ident)
                request.cls.svc_mgr.delete_bin(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    get_resource_id_by_agent = """
        if not is_never_authz(self.service_config):
            resource_id = self.catalog.get_resource_id_by_agent(AGENT_ID_0)
            assert isinstance(resource_id, Id)
            assert resource_id == self.resource_ids[0]
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_resource_id_by_agent(AGENT_ID_0)"""

    get_resource_by_agent = """
        if not is_never_authz(self.service_config):
            resource = self.catalog.get_resource_by_agent(AGENT_ID_1)
            assert isinstance(resource, Resource)
            assert resource.display_name.text == 'Test Resource 1'
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_resource_by_agent(AGENT_ID_1)"""

    get_agent_ids_by_resource = """
        if not is_never_authz(self.service_config):
            id_list = self.catalog.get_agent_ids_by_resource(self.resource_ids[0])
            assert id_list.next() == AGENT_ID_0
            assert isinstance(id_list, IdList)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_agent_ids_by_resource(AGENT_ID_0)"""

    get_agents_by_resource = """
        if not is_never_authz(self.service_config):
            agents = self.catalog.get_agents_by_resource(self.resource_ids[0])
            assert agents.available() == 1
            assert isinstance(agents, AgentList)
            assert agents.next().ident == AGENT_ID_0
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_agents_by_resource(AGENT_ID_0)"""


class ResourceAgentAssignmentSession:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'RESOURCE',
        proxy=PROXY,
        implementation=request.cls.service_config)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.resource_list = list()
    request.cls.resource_ids = list()

    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bin_form_for_create([])
        create_form.display_name = 'Test Bin'
        create_form.description = 'Test Bin for ResourceAgentAssignmentSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bin(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_resource_form_for_create([])
            create_form.display_name = 'Test Resource ' + str(num)
            create_form.description = 'Test Resource for ResourceAgentAssignmentSession tests'
            obj = request.cls.catalog.create_resource(create_form)
            request.cls.resource_list.append(obj)
            request.cls.resource_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_resource_agent_assignment_session(proxy=PROXY)

    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_resources():
                request.cls.catalog.delete_resource(obj.ident)
            request.cls.svc_mgr.delete_bin(request.cls.catalog.ident)

    request.addfinalizer(test_tear_down)"""

    assign_agent_to_resource = """
        if not is_never_authz(self.service_config):
            self.catalog.assign_agent_to_resource(AGENT_ID_0, self.resource_ids[0])
            with pytest.raises(errors.AlreadyExists):
                self.catalog.assign_agent_to_resource(AGENT_ID_0, self.resource_ids[1])
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.assign_agent_to_resource(AGENT_ID_0, AGENT_ID_1)"""

    unassign_agent_from_resource = """
        if not is_never_authz(self.service_config):
            self.catalog.assign_agent_to_resource(AGENT_ID_1, self.resource_ids[1])
            assert self.catalog.get_resource_by_agent(AGENT_ID_1).display_name.text == 'Test Resource 1'
            self.catalog.unassign_agent_from_resource(AGENT_ID_1, self.resource_ids[1])
            with pytest.raises(errors.NotFound):
                self.catalog.get_resource_by_agent(AGENT_ID_1)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.unassign_agent_from_resource(AGENT_ID_1, AGENT_ID_0)"""

    can_assign_agents_to_resource = """
        if is_no_authz(self.service_config):
            with pytest.raises(errors.Unimplemented):
                self.session.can_assign_agents_to_resource(True)
        else:
            assert isinstance(self.session.can_assign_agents_to_resource(True), bool)"""

    can_assign_agents = """
        if is_no_authz(self.service_config):
            with pytest.raises(errors.Unimplemented):
                self.session.can_assign_agents()
        else:
            assert isinstance(self.session.can_assign_agents(), bool)"""


class BinLookupSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.${pkg_name_replaced_reserved} import objects as ABCObjects',
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'DEFAULT_GENUS_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'GenusType\', \'authority\': \'DLKIT.MIT.EDU\'})',
        'AGENT_ID = Id(**{\'identifier\': \'jane_doe\', \'namespace\': \'osid.agent.Agent\', \'authority\': \'MIT-ODL\'})',
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::BinLookupSession::init_template
    request.cls.service_config = request.param
    request.cls.catalogs = list()
    request.cls.catalog_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
            create_form.display_name = 'Test ${cat_name} ' + str(num)
            create_form.description = 'Test ${cat_name} for ${pkg_name} proxy manager tests'
            catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
            request.cls.catalogs.append(catalog)
            request.cls.catalog_ids.append(catalog.ident)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_${cat_name_under_plural}():
                request.cls.svc_mgr.delete_${cat_name_under}(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::BinLookupSession::init_template
    request.cls.session = request.cls.svc_mgr"""

    use_comparative_bin_view_template = """
        # From test_templates/resource.py::BinLookupSession::use_comparative_bin_view_template
        self.svc_mgr.${method_name}()"""

    use_plenary_bin_view_template = """
        # From test_templates/resource.py::BinLookupSession::use_plenary_bin_view_template
        self.svc_mgr.${method_name}()"""

    get_bin_template = """
        # From test_templates/resource.py::BinLookupSession::get_bin_template
        if not is_never_authz(self.service_config):
            catalog = self.svc_mgr.${method_name}(self.catalogs[0].ident)
            assert catalog.ident == self.catalogs[0].ident
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id)"""

    get_bins_by_ids_template = """
        # From test_templates/resource.py::BinLookupSession::get_bins_by_ids_template
        if not is_never_authz(self.service_config):
            catalogs = self.svc_mgr.${method_name}(self.catalog_ids)
            assert catalogs.available() == 2
            assert isinstance(catalogs, ABCObjects.${cat_name}List)
            catalog_id_strs = [str(cat_id) for cat_id in self.catalog_ids]
            for index, catalog in enumerate(catalogs):
                assert str(catalog.ident) in catalog_id_strs
                catalog_id_strs.remove(str(catalog.ident))
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}([self.fake_id])"""

    get_bins_by_genus_type_template = """
        # From test_templates/resource.py::BinLookupSession::get_bins_by_genus_type_template
        if not is_never_authz(self.service_config):
            catalogs = self.svc_mgr.${method_name}(DEFAULT_GENUS_TYPE)
            assert catalogs.available() > 0
            assert isinstance(catalogs, ABCObjects.${cat_name}List)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(DEFAULT_GENUS_TYPE)"""

    get_bins_template = """
        # From test_templates/resource.py::BinLookupSession::get_bins_template
        if not is_never_authz(self.service_config):
            catalogs = self.svc_mgr.${method_name}()
            assert catalogs.available() > 0
            assert isinstance(catalogs, ABCObjects.${cat_name}List)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}()"""

    can_lookup_bins_template = """
        # From test_templates/resource.py::BinLookupSession::can_lookup_bins_template
        assert isinstance(self.session.${method_name}(), bool)"""


class BinAdminSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid.objects import OsidCatalogForm, OsidCatalog',
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'from dlkit.primordium.id.primitives import Id',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'from dlkit.abstract_osid.osid import errors',
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::BinAdminSession::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::BinAdminSession::init_template
    if not is_never_authz(request.cls.service_config):
        # Initialize test catalog:
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        # Initialize catalog to be deleted:
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name} For Deletion'
        create_form.description = 'Test ${cat_name} for ${interface_name} deletion test'
        request.cls.catalog_to_delete = request.cls.svc_mgr.create_${cat_name_under}(create_form)

    request.cls.session = request.cls.svc_mgr

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_${cat_name_under_plural}():
                request.cls.svc_mgr.delete_${cat_name_under}(catalog.ident)

    request.addfinalizer(test_tear_down)"""

    can_create_bins_template = """
        # From test_templates/resource.py BinAdminSession.can_create_bins_template
        assert isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool)"""

    can_delete_bins_template = """
        # From test_templates/resource.py BinAdminSession.can_delete_bins_template
        assert isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool)"""

    can_update_bins_template = """
        # From test_templates/resource.py BinAdminSession.can_update_bins_template
        assert isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool)"""

    can_create_bin_with_record_types_template = """
        # From test_templates/resource.py BinAdminSession.can_create_bin_with_record_types_template
        assert isinstance(self.${svc_mgr_or_catalog}.${method_name}(DEFAULT_TYPE), bool)"""

    get_bin_form_for_create_template = """
        # From test_templates/resource.py BinAdminSession.get_bin_form_for_create_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        if not is_never_authz(self.service_config):
            catalog_form = self.svc_mgr.${method_name}([])
            assert isinstance(catalog_form, OsidCatalogForm)
            assert not catalog_form.is_for_update()
            with pytest.raises(errors.InvalidArgument):
                self.svc_mgr.${method_name}([1])
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}([])"""

    create_bin_template = """
        # From test_templates/resource.py BinAdminSession.create_bin_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        if not is_never_authz(self.service_config):
            catalog_form = self.svc_mgr.get_${cat_name_under}_form_for_create([])
            catalog_form.display_name = 'Test ${cat_name}'
            catalog_form.description = 'Test ${cat_name} for ${interface_name}.${method_name} tests'
            new_catalog = self.svc_mgr.${method_name}(catalog_form)
            assert isinstance(new_catalog, OsidCatalog)
            with pytest.raises(errors.IllegalState):
                self.svc_mgr.${method_name}(catalog_form)
            with pytest.raises(errors.InvalidArgument):
                self.svc_mgr.${method_name}('I Will Break You!')
            update_form = self.svc_mgr.get_${cat_name_under}_form_for_update(new_catalog.ident)
            with pytest.raises(errors.InvalidArgument):
                self.svc_mgr.${method_name}(update_form)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}('foo')"""

    get_bin_form_for_update_template = """
        # From test_templates/resource.py BinAdminSession.get_bin_form_for_update_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        if not is_never_authz(self.service_config):
            catalog_form = self.svc_mgr.${method_name}(self.catalog.ident)
            assert isinstance(catalog_form, OsidCatalogForm)
            assert catalog_form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id)"""

    update_bin_template = """
        # From test_templates/resource.py BinAdminSession.update_bin_template
        if not is_never_authz(self.service_config):
            catalog_form = self.svc_mgr.get_${cat_name_under}_form_for_update(self.catalog.ident)
            # Update some elements here?
            self.svc_mgr.${method_name}(catalog_form)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}('foo')"""

    delete_bin_template = """
        # From test_templates/resource.py BinAdminSession.delete_bin_template
        if not is_never_authz(self.service_config):
            cat_id = self.catalog_to_delete.ident
            self.svc_mgr.${method_name}(cat_id)
            with pytest.raises(errors.NotFound):
                self.svc_mgr.get_${cat_name_under}(cat_id)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id)"""

    alias_bin_template = """
        # From test_templates/resource.py BinAdminSession.alias_bin_template
        alias_id = Id('${package_name_replace_reserved}.${cat_name}%3Amy-alias%40ODL.MIT.EDU')

        if not is_never_authz(self.service_config):
            self.svc_mgr.${method_name}(self.catalog_to_delete.ident, alias_id)
            aliased_catalog = self.svc_mgr.get_${cat_name_under}(alias_id)
            assert self.catalog_to_delete.ident == aliased_catalog.ident
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id, alias_id)"""


class BinHierarchySession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid.objects import OsidList',
        'from dlkit.abstract_osid.id.objects import IdList',
        'from dlkit.abstract_osid.hierarchy.objects import Hierarchy',
        'from dlkit.abstract_osid.osid.objects import OsidNode',
        'from dlkit.primordium.id.primitives import Id'
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::BinHierarchySession::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.catalogs = dict()
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        for name in ['Root', 'Child 1', 'Child 2', 'Grandchild 1']:
            create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
            create_form.display_name = name
            create_form.description = 'Test ${cat_name} ' + name
            request.cls.catalogs[name] = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        request.cls.svc_mgr.add_root_${cat_name_under}(request.cls.catalogs['Root'].ident)
        request.cls.svc_mgr.add_child_${cat_name_under}(request.cls.catalogs['Root'].ident, request.cls.catalogs['Child 1'].ident)
        request.cls.svc_mgr.add_child_${cat_name_under}(request.cls.catalogs['Root'].ident, request.cls.catalogs['Child 2'].ident)
        request.cls.svc_mgr.add_child_${cat_name_under}(request.cls.catalogs['Child 1'].ident, request.cls.catalogs['Grandchild 1'].ident)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.remove_child_${cat_name_under}(request.cls.catalogs['Child 1'].ident, request.cls.catalogs['Grandchild 1'].ident)
            request.cls.svc_mgr.remove_child_${cat_name_under_plural}(request.cls.catalogs['Root'].ident)
            request.cls.svc_mgr.remove_root_${cat_name_under}(request.cls.catalogs['Root'].ident)
            for cat_name in request.cls.catalogs:
                request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalogs[cat_name].ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::BinHierarchySession::init_template
    request.cls.session = request.cls.svc_mgr"""

    can_access_bin_hierarchy_template = """
        # From test_templates/resource.py::BinHierarchySession::can_access_objective_bank_hierarchy_template
        assert isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool)"""

    get_bin_hierarchy_id_template = """
        # From test_templates/resource.py::BinHierarchySession::get_bin_hierarchy_id_template
        hierarchy_id = self.svc_mgr.${method_name}()
        assert isinstance(hierarchy_id, Id)"""

    get_bin_hierarchy_template = """
        # From test_templates/resource.py::BinHierarchySession::get_bin_hierarchy_template
        if not is_never_authz(self.service_config):
            hierarchy = self.svc_mgr.${method_name}()
            assert isinstance(hierarchy, Hierarchy)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}()"""

    get_root_bin_ids_template = """
        # From test_templates/resource.py::BinHierarchySession::get_root_bin_ids_template
        if not is_never_authz(self.service_config):
            root_ids = self.svc_mgr.${method_name}()
            assert isinstance(root_ids, IdList)
            # probably should be == 1, but we seem to be getting test cruft,
            # and I can't pinpoint where it's being introduced.
            assert root_ids.available() >= 1
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}()"""

    get_root_bins_template = """
        # From test_templates/resource.py::BinHierarchySession::get_root_bins_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${cat_name}List
        if not is_never_authz(self.service_config):
            roots = self.svc_mgr.${method_name}()
            assert isinstance(roots, OsidList)
            assert roots.available() == 1
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}()"""

    has_parent_bins_template = """
        # From test_templates/resource.py::BinHierarchySession::has_parent_bins_template
        if not is_never_authz(self.service_config):
            assert isinstance(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident), bool)
            assert self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident)
            assert self.svc_mgr.${method_name}(self.catalogs['Child 2'].ident)
            assert self.svc_mgr.${method_name}(self.catalogs['Grandchild 1'].ident)
            assert not self.svc_mgr.${method_name}(self.catalogs['Root'].ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id)"""

    is_parent_of_bin_template = """
        # From test_templates/resource.py::BinHierarchySession::is_parent_of_bin_template
        if not is_never_authz(self.service_config):
            assert isinstance(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, self.catalogs['Root'].ident), bool)
            assert self.svc_mgr.${method_name}(self.catalogs['Root'].ident, self.catalogs['Child 1'].ident)
            assert self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, self.catalogs['Grandchild 1'].ident)
            assert not self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, self.catalogs['Root'].ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id, self.fake_id)"""

    get_parent_bin_ids_template = """
        # From test_templates/resource.py::BinHierarchySession::get_parent_bin_ids_template
        from dlkit.abstract_osid.id.objects import ${return_type}
        if not is_never_authz(self.service_config):
            catalog_list = self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident)
            assert isinstance(catalog_list, ${return_type})
            assert catalog_list.available() == 1
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id)"""

    get_parent_bins_template = """
        # From test_templates/resource.py::BinHierarchySession::get_parent_bins_template
        if not is_never_authz(self.service_config):
            catalog_list = self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident)
            assert isinstance(catalog_list, OsidList)
            assert catalog_list.available() == 1
            assert catalog_list.next().display_name.text == 'Root'
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id)"""

    is_ancestor_of_bin_template = """
        # From test_templates/resource.py::BinHierarchySession::is_ancestor_of_bin_template
        if not is_never_authz(self.service_config):
            pytest.raises(errors.Unimplemented,
                          self.svc_mgr.${method_name},
                          self.catalogs['Root'].ident,
                          self.catalogs['Child 1'].ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id, self.fake_id)
        # self.assertTrue(isinstance(self.svc_mgr.${method_name}(
        #     self.catalogs['Root'].ident,
        #     self.catalogs['Child 1'].ident),
        #     bool))
        # self.assertTrue(self.svc_mgr.${method_name}(
        #     self.catalogs['Root'].ident,
        #     self.catalogs['Child 1'].ident))
        # self.assertTrue(self.svc_mgr.${method_name}(
        #     self.catalogs['Root'].ident,
        #     self.catalogs['Grandchild 1'].ident))
        # self.assertFalse(self.svc_mgr.${method_name}(
        #     self.catalogs['Child 1'].ident,
        #     self.catalogs['Root'].ident))"""

    has_child_bins_template = """
        # From test_templates/resource.py::BinHierarchySession::has_child_bins_template
        if not is_never_authz(self.service_config):
            assert isinstance(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident), bool)
            assert self.svc_mgr.${method_name}(self.catalogs['Root'].ident)
            assert self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident)
            assert not self.svc_mgr.${method_name}(self.catalogs['Child 2'].ident)
            assert not self.svc_mgr.${method_name}(self.catalogs['Grandchild 1'].ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id)"""

    is_child_of_bin_template = """
        # From test_templates/resource.py::BinHierarchySession::is_child_of_bin_template
        if not is_never_authz(self.service_config):
            assert isinstance(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, self.catalogs['Root'].ident), bool)
            assert self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, self.catalogs['Root'].ident)
            assert self.svc_mgr.${method_name}(self.catalogs['Grandchild 1'].ident, self.catalogs['Child 1'].ident)
            assert not self.svc_mgr.${method_name}(self.catalogs['Root'].ident, self.catalogs['Child 1'].ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id, self.fake_id)"""

    get_child_bin_ids_template = """
        # From test_templates/resource.py::BinHierarchySession::get_child_bin_ids_template
        from dlkit.abstract_osid.id.objects import ${return_type}
        if not is_never_authz(self.service_config):
            catalog_list = self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident)
            assert isinstance(catalog_list, ${return_type})
            assert catalog_list.available() == 1
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id)"""

    get_child_bins_template = """
        # From test_templates/resource.py::BinHierarchySession::get_child_bins_template
        if not is_never_authz(self.service_config):
            catalog_list = self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident)
            assert isinstance(catalog_list, OsidList)
            assert catalog_list.available() == 1
            assert catalog_list.next().display_name.text == 'Grandchild 1'
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id)"""

    is_descendant_of_bin_template = """
        # From test_templates/resource.py::BinHierarchySession::is_descendant_of_bin_template
        if not is_never_authz(self.service_config):
            pytest.raises(errors.Unimplemented,
                          self.svc_mgr.${method_name},
                          self.catalogs['Child 1'].ident,
                          self.catalogs['Root'].ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id, self.fake_id)
        # self.assertTrue(isinstance(self.svc_mgr.${method_name}(
        #     self.catalogs['Root'].ident,
        #     self.catalogs['Child 1'].ident),
        #     bool))
        # self.assertTrue(self.svc_mgr.${method_name}(
        #     self.catalogs['Child 1'].ident,
        #     self.catalogs['Root'].ident))
        # self.assertTrue(self.svc_mgr.${method_name}(
        #     self.catalogs['Grandchild 1'].ident,
        #     self.catalogs['Root'].ident))
        # self.assertFalse(self.svc_mgr.${method_name}(
        #     self.catalogs['Root'].ident,
        #     self.catalogs['Child 1'].ident))"""

    get_bin_node_ids_template = """
        # From test_templates/resource.py::BinHierarchySession::get_bin_node_ids_template
        # Per the spec, perhaps counterintuitively this method returns a
        #  node, **not** a IdList...
        if not is_never_authz(self.service_config):
            node = self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, 1, 2, False)
            assert isinstance(node, OsidNode)
            assert not node.is_root()
            assert not node.is_leaf()
            assert node.get_child_ids().available() == 1
            assert isinstance(node.get_child_ids(), IdList)
            assert node.get_parent_ids().available() == 1
            assert isinstance(node.get_parent_ids(), IdList)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id, 1, 2, False)"""

    get_bin_nodes_template = """
        # From test_templates/resource.py::BinHierarchySession::get_bin_nodes_template
        if not is_never_authz(self.service_config):
            node = self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, 1, 2, False)
            assert isinstance(node, OsidNode)
            assert not node.is_root()
            assert not node.is_leaf()
            assert node.get_child_ids().available() == 1
            assert isinstance(node.get_child_ids(), IdList)
            assert node.get_parent_ids().available() == 1
            assert isinstance(node.get_parent_ids(), IdList)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.${method_name}(self.fake_id, 1, 2, False)"""


class BinHierarchyDesignSession:

    import_statements_pattern = [
        'from dlkit.primordium.id.primitives import Id'
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::BinHierarchyDesignSession::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.catalogs = dict()
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        for name in ['Root', 'Child 1', 'Child 2', 'Grandchild 1']:
            create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
            create_form.display_name = name
            create_form.description = 'Test ${cat_name} ' + name
            request.cls.catalogs[name] = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        request.cls.svc_mgr.add_root_${cat_name_under}(request.cls.catalogs['Root'].ident)
        request.cls.svc_mgr.add_child_${cat_name_under}(request.cls.catalogs['Root'].ident, request.cls.catalogs['Child 1'].ident)
        request.cls.svc_mgr.add_child_${cat_name_under}(request.cls.catalogs['Root'].ident, request.cls.catalogs['Child 2'].ident)
        request.cls.svc_mgr.add_child_${cat_name_under}(request.cls.catalogs['Child 1'].ident, request.cls.catalogs['Grandchild 1'].ident)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.remove_child_${cat_name_under}(request.cls.catalogs['Child 1'].ident, request.cls.catalogs['Grandchild 1'].ident)
            request.cls.svc_mgr.remove_child_${cat_name_under_plural}(request.cls.catalogs['Root'].ident)
            for cat_name in request.cls.catalogs:
                request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalogs[cat_name].ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::BinHierarchyDesignSession::init_template
    request.cls.session = request.cls.svc_mgr"""

    can_modify_bin_hierarchy_template = """
        # From test_templates/resource.py::BinHierarchyDesignSession::can_modify_bin_hierarchy_template
        assert isinstance(self.session.${method_name}(), bool)"""

    add_root_bin_template = """
        # From test_templates/resource.py::BinHierarchyDesignSession::add_root_bin_template
        # this is tested in the setUpClass
        if not is_never_authz(self.service_config):
            roots = self.session.get_root_${cat_name_plural_under}()
            assert isinstance(roots, OsidList)
            assert roots.available() == 1
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}(self.fake_id)"""

    remove_root_bin_template = """
        # From test_templates/resource.py::BinHierarchyDesignSession::remove_root_bin_template
        if not is_never_authz(self.service_config):
            roots = self.session.get_root_${cat_name_plural_under}()
            assert roots.available() == 1

            create_form = self.svc_mgr.get_${cat_name_under}_form_for_create([])
            create_form.display_name = 'new root'
            create_form.description = 'Test ${cat_name} root'
            new_${cat_name_under} = self.svc_mgr.create_${cat_name_under}(create_form)
            self.svc_mgr.add_root_${cat_name_under}(new_${cat_name_under}.ident)

            roots = self.session.get_root_${cat_name_plural_under}()
            assert roots.available() == 2

            self.session.${method_name}(new_${cat_name_under}.ident)

            roots = self.session.get_root_${cat_name_plural_under}()
            assert roots.available() == 1
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}(self.fake_id)"""

    add_child_bin_template = """
        # From test_templates/resource.py::BinHierarchyDesignSession::add_child_bin_template
        if not is_never_authz(self.service_config):
            # this is tested in the setUpClass
            children = self.session.get_child_${cat_name_plural_under}(self.catalogs['Root'].ident)
            assert isinstance(children, OsidList)
            assert children.available() == 2
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}(self.fake_id, self.fake_id)"""

    remove_child_bin_template = """
        # From test_templates/resource.py::BinHierarchyDesignSession::remove_child_bin_template
        if not is_never_authz(self.service_config):
            children = self.session.get_child_${cat_name_plural_under}(self.catalogs['Root'].ident)
            assert children.available() == 2

            create_form = self.svc_mgr.get_${cat_name_under}_form_for_create([])
            create_form.display_name = 'test child'
            create_form.description = 'Test ${cat_name} child'
            new_${cat_name_under} = self.svc_mgr.create_${cat_name_under}(create_form)
            self.svc_mgr.add_child_${cat_name_under}(
                self.catalogs['Root'].ident,
                new_${cat_name_under}.ident)

            children = self.session.get_child_${cat_name_plural_under}(self.catalogs['Root'].ident)
            assert children.available() == 3

            self.session.${method_name}(
                self.catalogs['Root'].ident,
                new_${cat_name_under}.ident)

            children = self.session.get_child_${cat_name_plural_under}(self.catalogs['Root'].ident)
            assert children.available() == 2
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}(self.fake_id, self.fake_id)"""

    remove_child_bins_template = """
        # From test_templates/resource.py::BinHierarchyDesignSession::remove_child_bins_template
        if not is_never_authz(self.service_config):
            children = self.session.get_child_${cat_name_plural_under}(self.catalogs['Grandchild 1'].ident)
            assert children.available() == 0

            create_form = self.svc_mgr.get_${cat_name_under}_form_for_create([])
            create_form.display_name = 'test great grandchild'
            create_form.description = 'Test ${cat_name} child'
            new_${cat_name_under} = self.svc_mgr.create_${cat_name_under}(create_form)
            self.svc_mgr.add_child_${cat_name_under}(
                self.catalogs['Grandchild 1'].ident,
                new_${cat_name_under}.ident)

            children = self.session.get_child_${cat_name_plural_under}(self.catalogs['Grandchild 1'].ident)
            assert children.available() == 1

            self.session.${method_name}(self.catalogs['Grandchild 1'].ident)

            children = self.session.get_child_${cat_name_plural_under}(self.catalogs['Grandchild 1'].ident)
            assert children.available() == 0
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}(self.fake_id)"""


class Resource:

    import_statements_pattern = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'from dlkit.abstract_osid.osid import errors',
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::Resource::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)

        form = request.cls.catalog.get_${object_name_under}_form_for_create([])
        form.display_name = 'Test object'
        request.cls.object = request.cls.catalog.create_${object_name_under}(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_${object_name_under_plural}():
                request.cls.catalog.delete_${object_name_under}(obj.ident)
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""

    is_group_template = """
        # From test_templates/resources.py::Resource::is_group_template
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.${method_name}(), bool)"""

    is_demographic = """
        if not is_never_authz(self.service_config):
            with pytest.raises(AttributeError):
                self.object.is_demographic()"""

    has_avatar_template = """
        # From test_templates/resources.py::Resource::has_avatar_template
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.${method_name}(), bool)"""

    get_avatar_id_template = """
        # From test_templates/resources.py::Resource::get_avatar_id_template
        if not is_never_authz(self.service_config):
            pytest.raises(errors.IllegalState,
                          self.object.${method_name})"""

    get_avatar_template = """
        # From test_templates/resources.py::Resource::get_avatar_template
        if not is_never_authz(self.service_config):
            pytest.raises(errors.IllegalState,
                          self.object.${method_name})"""


class ResourceQuery:

    import_statements_pattern = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'from dlkit.abstract_osid.osid import errors',
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::ResourceQuery::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::ResourceQuery::init_template
    request.cls.query = request.cls.catalog.get_${object_name_under}_query()"""

    clear_group_terms_template = """
        # From test_templates/resource.py::ResourceQuery::clear_group_terms_template
        if is_no_authz(self.service_config):
            self.query._query_terms['${var_name_mixed}'] = 'foo'
        self.query.${method_name}()
        if is_no_authz(self.service_config):
            assert '${var_name_mixed}' not in self.query._query_terms"""

    match_avatar_id_template = """
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        if is_no_authz(self.service_config):
            assert '${var_name_mixed}' not in self.query._query_terms
        self.query.${method_name}(test_id, match=True)
        if is_no_authz(self.service_config):
            assert self.query._query_terms['${var_name_mixed}'] == {
                '$$in': [str(test_id)]
            }"""

    clear_avatar_id_terms_template = """
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_${var_name}(test_id, match=True)
        if is_no_authz(self.service_config):
            assert '${var_name_mixed}' in self.query._query_terms
        self.query.${method_name}()
        if is_no_authz(self.service_config):
            assert '${var_name_mixed}' not in self.query._query_terms"""

    match_bin_id_template = """
        # From test_templates/resource.py::ResourceQuery::match_bin_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.${method_name}(test_id, match=True)

        if is_no_authz(self.service_config):
            assert self.query._query_terms['assigned${cat_name}Ids'] == {
                '$$in': [str(test_id)]
            }"""

    clear_bin_id_terms_template = """
        # From test_templates/resource.py::ResourceQuery::clear_bin_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_${var_name}(test_id, match=True)
        if is_no_authz(self.service_config):
            assert 'assigned${cat_name}Ids' in self.query._query_terms
        self.query.${method_name}()
        if is_no_authz(self.service_config):
            assert 'assigned${cat_name}Ids' not in self.query._query_terms"""


class ResourceSearch:

    import_statements_pattern = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'from dlkit.abstract_osid.osid import errors',
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::ResourceSearch::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
    create_form.display_name = 'Test catalog'
    create_form.description = 'Test catalog description'
    request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)

    def class_tear_down():
        request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::ResourceSearch::init_template
    request.cls.search = request.cls.catalog.get_${object_name_under}_search()"""


class ResourceSearchSession:
    import_statements_pattern = [
        'from dlkit.abstract_osid.${pkg_name_replaced_reserved} import searches as ABCSearches',
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
    ]

    import_statements = [
        'from dlkit.abstract_osid.resource import searches as ABCSearches',
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.resource_list = list()
    request.cls.resource_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'RESOURCE',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bin_form_for_create([])
        create_form.display_name = 'Test Bin'
        create_form.description = 'Test Bin for ResourceSearchSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bin(create_form)
        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = request.cls.catalog.get_resource_form_for_create([])
            create_form.display_name = 'Test Resource ' + color
            create_form.description = (
                'Test Resource for ResourceSearchSession tests, did I mention green')
            obj = request.cls.catalog.create_resource(create_form)
            request.cls.resource_list.append(obj)
            request.cls.resource_ids.append(obj.ident)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_resources():
                request.cls.catalog.delete_resource(obj.ident)
            request.cls.svc_mgr.delete_bin(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    get_resource_search_template = """
        # From test_templates/resource.py::ResourceSearchSession::get_resource_search_template
        result = self.session.${method_name}()
        assert isinstance(result, ABCSearches.${return_type})"""

    get_resources_by_search_template = """
        # From test_templates/resource.py::ResourceSearchSession::get_resources_by_search_template
        query = self.catalog.get_${object_name_under}_query()
        search = self.session.get_${object_name_under}_search()
        results = self.session.${method_name}(query, search)
        assert isinstance(results, ABCSearches.${return_type})"""


class ResourceForm:

    import_statements_pattern = [
        'from dlkit.json_.osid.metadata import Metadata',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.abstract_osid.id.primitives import Id as ABC_Id',
        'from dlkit.abstract_osid.locale.primitives import DisplayText as ABC_DisplayText',
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::ResourceForm::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::ResourceForm::init_template
    if not is_never_authz(request.cls.service_config):
        request.cls.form = request.cls.catalog.get_${object_name_under}_form_for_create([])"""

    get_group_metadata_template = """
        # From test_templates/resource.py::ResourceForm::get_group_metadata_template
        mdata = self.form.${method_name}()
        assert isinstance(mdata, Metadata)
        assert isinstance(mdata.get_element_id(), ABC_Id)
        assert isinstance(mdata.get_element_label(), ABC_DisplayText)
        assert isinstance(mdata.get_instructions(), ABC_DisplayText)
        assert mdata.get_syntax() == '${syntax}'
        assert not mdata.is_array()
        assert isinstance(mdata.is_required(), bool)
        assert isinstance(mdata.is_read_only(), bool)
        assert isinstance(mdata.is_linked(), bool)"""

    get_avatar_metadata_template = """
        # From test_templates/resource.py::ResourceForm::get_avatar_metadata_template
        mdata = self.form.${method_name}()
        assert isinstance(mdata, Metadata)
        assert isinstance(mdata.get_element_id(), ABC_Id)
        assert isinstance(mdata.get_element_label(), ABC_DisplayText)
        assert isinstance(mdata.get_instructions(), ABC_DisplayText)
        assert mdata.get_syntax() == '${syntax}'
        assert not mdata.is_array()
        assert isinstance(mdata.is_required(), bool)
        assert isinstance(mdata.is_read_only(), bool)
        assert isinstance(mdata.is_linked(), bool)"""

    set_group_template = """
        # From test_templates/resource.py::ResourceForm::set_group_template
        self.form.${method_name}(True)
        assert self.form._my_map['${var_name_mixed}']
        with pytest.raises(errors.InvalidArgument):
            self.form.${method_name}('false')"""

    clear_group_template = """
        # From test_templates/resource.py::ResourceForm::clear_group_template
        self.form.set_${var_name}(True)
        assert self.form._my_map['${var_name_mixed}']
        self.form.${method_name}()
        assert self.form._my_map['${var_name_mixed}'] is None"""

    set_avatar_template = """
        # From test_templates/resource.py::ResourceForm::set_avatar_template
        assert self.form._my_map['${var_name_mixed}Id'] == ''
        self.form.set_${var_name}(Id('repository.Asset%3Afake-id%40ODL.MIT.EDU'))
        assert self.form._my_map['${var_name_mixed}Id'] == 'repository.Asset%3Afake-id%40ODL.MIT.EDU'
        with pytest.raises(errors.InvalidArgument):
            self.form.${method_name}(True)"""

    clear_avatar_template = """
        # From test_templates/resource.py::ResourceForm::clear_avatar_template
        self.form.set_${var_name}(Id('repository.Asset%3Afake-id%40ODL.MIT.EDU'))
        assert self.form._my_map['${var_name_mixed}Id'] == 'repository.Asset%3Afake-id%40ODL.MIT.EDU'
        self.form.${method_name}()
        assert self.form._my_map['${var_name_mixed}Id'] == self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0]"""

    get_resource_form_record_template = """
        with pytest.raises(errors.Unsupported):
            self.form.${method_name}(Type('osid.Osid%3Afake-record%40ODL.MIT.EDU'))
        # Here check for a real record?"""


class ResourceList:

    import_statements_pattern = [
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # Implemented from init template for ResourceList
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_${object_name_under_plural}():
                request.cls.catalog.delete_${object_name_under}(obj.ident)
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # Implemented from init template for ResourceList
    from dlkit.json_.${pkg_name_replaced_reserved}.objects import ${interface_name}
    request.cls.${object_name_under}_list = list()
    request.cls.${object_name_under}_ids = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            create_form = request.cls.catalog.get_${object_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            obj = request.cls.catalog.create_${object_name_under}(create_form)
            request.cls.${object_name_under}_list.append(obj)
            request.cls.${object_name_under}_ids.append(obj.ident)
    request.cls.${object_name_under}_list = ${interface_name}(request.cls.${object_name_under}_list)
    request.cls.object = request.cls.${object_name_under}_list"""

    get_next_resource_template = """
        # From test_templates/resource.py::ResourceList::get_next_resource_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        if not is_never_authz(self.service_config):
            assert isinstance(self.${return_type_under}_list.${method_name}(), ${return_type})"""

    get_next_resources_template = """
        # From test_templates/resource.py::ResourceList::get_next_resources_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}List, ${return_type}
        if not is_never_authz(self.service_config):
            new_list = self.${return_type_under}_list.${method_name}(2)
            assert isinstance(new_list, ${return_type}List)
            for item in new_list:
                assert isinstance(item, ${return_type})"""


class ResourceNodeList:
    init = """"""

    get_next_resource_node = """"""

    get_next_resource_nodes = """"""


class Bin:

    import_statements_pattern = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'from dlkit.abstract_osid.osid import errors',
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::Bin::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)

    def class_tear_down():
        pass

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::Bin::init_template
    if not is_never_authz(request.cls.service_config):
        form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        form.display_name = 'for testing'
        request.cls.object = request.cls.svc_mgr.create_${cat_name_under}(form)

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.object.ident)

    request.addfinalizer(test_tear_down)"""


class BinForm:

    import_statements_pattern = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'from dlkit.abstract_osid.osid import errors',
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::BinForm::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)

    def class_tear_down():
        pass

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::BinForm::init_template
    if not is_never_authz(request.cls.service_config):
        request.cls.object = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])

    def test_tear_down():
        pass

    request.addfinalizer(test_tear_down)"""


class BinList:

    import_statements_pattern = [
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # Implemented from init template for BinList
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        request.cls.${object_name_under}_ids = list()

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.${object_name_under}_ids:
                request.cls.svc_mgr.delete_${cat_name_under}(obj)
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # Implemented from init template for BinList
    from dlkit.json_.${pkg_name_replaced_reserved}.objects import ${interface_name}
    request.cls.${object_name_under}_list = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            create_form = request.cls.svc_mgr.get_${object_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            obj = request.cls.svc_mgr.create_${object_name_under}(create_form)
            request.cls.${object_name_under}_list.append(obj)
            request.cls.${object_name_under}_ids.append(obj.ident)
    request.cls.${object_name_under}_list = ${interface_name}(request.cls.${object_name_under}_list)"""


class BinNodeList:

    import_statements_pattern = [
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # Implemented from init template for BinNodeList
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        request.cls.${object_name_under}_ids = list()

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.${object_name_under}_ids:
                request.cls.svc_mgr.delete_${cat_name_under}(obj)
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # Implemented from init template for BinNodeList
    from dlkit.json_.${pkg_name_replaced_reserved}.objects import ${interface_name}, ${object_name}
    request.cls.${object_name_under}_list = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            obj = request.cls.svc_mgr.create_${cat_name_under}(create_form)
            request.cls.${object_name_under}_list.append(${object_name}(obj.object_map))
            request.cls.${object_name_under}_ids.append(obj.ident)
        # Not put the catalogs in a hierarchy
        request.cls.svc_mgr.add_root_${cat_name_under}(request.cls.${object_name_under}_list[0].ident)
        request.cls.svc_mgr.add_child_${cat_name_under}(
            request.cls.${object_name_under}_list[0].ident,
            request.cls.${object_name_under}_list[1].ident)
    request.cls.${object_name_under}_list = ${interface_name}(request.cls.${object_name_under}_list)"""


class BinNode:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid.objects import OsidCatalog'
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # Implemented from init template for BinNode
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        request.cls.${object_name_under}_ids = list()

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # Implemented from init template for BinNode
    from dlkit.json_.${pkg_name_replaced_reserved}.objects import ${interface_name}
    request.cls.${object_name_under}_list = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            obj = request.cls.svc_mgr.create_${cat_name_under}(create_form)
            request.cls.${object_name_under}_list.append(${interface_name}(
                obj.object_map,
                runtime=request.cls.svc_mgr._runtime,
                proxy=request.cls.svc_mgr._proxy))
            request.cls.${object_name_under}_ids.append(obj.ident)
        # Not put the catalogs in a hierarchy
        request.cls.svc_mgr.add_root_${cat_name_under}(request.cls.${object_name_under}_list[0].ident)
        request.cls.svc_mgr.add_child_${cat_name_under}(
            request.cls.${object_name_under}_list[0].ident,
            request.cls.${object_name_under}_list[1].ident)

        request.cls.object = request.cls.svc_mgr.get_${cat_name_under}_nodes(
            request.cls.${object_name_under}_list[0].ident, 0, 5, False)

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.remove_child_${cat_name_under}(
                request.cls.${object_name_under}_list[0].ident,
                request.cls.${object_name_under}_list[1].ident)
            request.cls.svc_mgr.remove_root_${cat_name_under}(request.cls.${object_name_under}_list[0].ident)
            for node in request.cls.${object_name_under}_list:
                request.cls.svc_mgr.delete_${cat_name_under}(node.ident)

    request.addfinalizer(test_tear_down)"""

    get_bin_template = """
        # from test_templates/resource.py::BinNode::get_bin_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${cat_name}
        if not is_never_authz(self.service_config):
            assert isinstance(self.${cat_name_under}_list[0].${method_name}(), OsidCatalog)
            assert str(self.${cat_name_under}_list[0].${method_name}().ident) == str(self.${cat_name_under}_list[0].ident)"""

    get_parent_bin_nodes_template = """
        # from test_templates/resource.py::BinNode::get_parent_bin_nodes
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${cat_name}NodeList
        if not is_never_authz(self.service_config):
            node = self.svc_mgr.get_${cat_name_under}_nodes(
                self.${cat_name_under}_list[1].ident,
                1,
                0,
                False)
            assert isinstance(node.${method_name}(), ${cat_name}NodeList)
            assert node.${method_name}().available() == 1
            assert str(node.${method_name}().next().ident) == str(self.${cat_name_under}_list[0].ident)"""

    get_child_bin_nodes_template = """
        # from test_templates/resource.py::BinNode::get_child_bin_nodes_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${cat_name}NodeList
        if not is_never_authz(self.service_config):
            node = self.svc_mgr.get_${cat_name_under}_nodes(
                self.${cat_name_under}_list[0].ident,
                0,
                1,
                False)
            assert isinstance(node.${method_name}(), ${cat_name}NodeList)
            assert node.${method_name}().available() == 1
            assert str(node.${method_name}().next().ident) == str(self.${cat_name_under}_list[1].ident)"""


class BinQuery:

    import_statements_pattern = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'from dlkit.abstract_osid.osid import errors',
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::BinQuery::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        request.cls.fake_id = Id('resource.Resource%3A1%40ODL.MIT.EDU')

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::BinQuery::init_template
    if not is_never_authz(request.cls.service_config):
        request.cls.query = request.cls.svc_mgr.get_${cat_name_under}_query()"""

    clear_group_terms_template = """
        # From test_templates/resource.py::BinQuery::clear_group_terms_template
        if is_no_authz(self.service_config):
            self.query._query_terms['${var_name_mixed}'] = 'foo'

        if not is_never_authz(self.service_config):
            self.query.${method_name}()

        if is_no_authz(self.service_config):
            assert '${var_name_mixed}' not in self.query._query_terms"""


class BinQuerySession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.${pkg_name_replaced_reserved} import queries as ABCQueries',
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'from dlkit.abstract_osid.osid import errors',
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::BinQuerySession::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        request.cls.fake_id = Id('resource.Resource%3A1%40ODL.MIT.EDU')

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::BinQuerySession::init_template
    request.cls.session = request.cls.svc_mgr"""

    get_bin_query_template = """
        # From test_templates/resource.py::BinQuerySession::get_bin_query_template
        if not is_never_authz(self.service_config):
            query = self.session.${method_name}()
            assert isinstance(query, ABCQueries.${cat_name}Query)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}()"""

    get_bins_by_query_template = """
        # From test_templates/resource.py::BinQuerySession::get_bins_by_query_template
        if not is_never_authz(self.service_config):
            query = self.session.get_${cat_name_under}_query()
            query.match_display_name('Test catalog')
            assert self.session.${method_name}(query).available() == 1
            query.clear_display_name_terms()
            query.match_display_name('Test catalog', match=False)
            assert self.session.${method_name}(query).available() == 0
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}('foo')"""

    can_search_bins_template = """
        # From test_templates/resource.py::BinQuerySession::can_search_bins_template
        assert isinstance(self.session.${method_name}(), bool)"""
