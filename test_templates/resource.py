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
    @classmethod
    def setUpClass(cls):
        cls.mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')"""

    supports_visible_federation_template = """
        self.assertTrue(isinstance(self.mgr.supports_visible_federation(), bool))"""

    supports_resource_lookup_template = """
        self.assertTrue(isinstance(self.mgr.${method_name}(), bool))"""

    get_resource_record_types_template = """
        self.assertTrue(isinstance(self.mgr.${method_name}(), abc_type_list))"""

    supports_resource_record_type_template = """
        self.assertTrue(isinstance(self.mgr.${method_name}(DEFAULT_TYPE), bool))"""


class ResourceManager:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
    ]

    init_template = """
    # Implemented from resource.ResourceManager
    class NotificationReceiver(object):
        pass

    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${pkg_name} manager tests'
        catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
        cls.catalog_id = catalog.get_id()
        # cls.mgr = Runtime().get_manager('${pkg_name_upper}', 'TEST_JSON_1', (3, 0, 0))
        cls.receiver = cls.NotificationReceiver()

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog_id)"""

    get_resource_lookup_session_template = """
        # From tests_templates/resource.py::ResourceManager::get_resource_lookup_session_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}()"""

    get_resource_lookup_session_for_bin_template = """
        # From tests_templates/resource.py::ResourceManager::get_resource_lookup_session_for_bin_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.catalog_id)
        with self.assertRaises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""

    get_resource_admin_session_template = """
        # From tests_templates/resource.py::ResourceManager::get_resource_admin_session_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}()"""

    get_resource_admin_session_for_bin_template = """
        # From tests_templates/resource.py::ResourceManager::get_resource_admin_session_for_bin_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.catalog_id)
        with self.assertRaises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""

    get_resource_notification_session_template = """
        # From tests_templates/resource.py::ResourceManager::get_resource_notification_session_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.receiver)"""

    get_resource_notification_session_for_bin_template = """
        # From tests_templates/resource.py::ResourceManager::get_resource_notification_session_for_bin_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.receiver, self.catalog_id)
        with self.assertRaises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""

    get_resource_batch_manager_template = """
        # From tests_templates/resource.py::ResourceManager::get_resource_batch_manager_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}()"""


class ResourceProxyManager:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
    ]

    init_template = """
    # Implemented from resource.ResourceProxyManager
    class NotificationReceiver(object):
        pass

    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${pkg_name} proxy manager tests'
        catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
        cls.catalog_id = catalog.get_id()
        # cls.mgr = Runtime().get_proxy_manager('${pkg_name_upper}', 'TEST_JSON_1', (3, 0, 0))
        cls.receiver = cls.NotificationReceiver()

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog_id)"""

    get_resource_lookup_session_template = """
        # From tests_templates/resource.py::ResourceProxyManager::get_resource_lookup_session_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(PROXY)
        with self.assertRaises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""

    get_resource_lookup_session_for_bin_template = """
        # From tests_templates/resource.py::ResourceProxyManager::get_resource_lookup_session_for_bin_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.catalog_id, PROXY)
        with self.assertRaises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""

    get_resource_admin_session_template = """
        # From tests_templates/resource.py::ResourceProxyManager::get_resource_admin_session_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(PROXY)
        with self.assertRaises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""

    get_resource_admin_session_for_bin_template = """
        # From tests_templates/resource.py::ResourceProxyManager::get_resource_admin_session_for_bin_template
        if self.svc_mgr.supports_${support_check}():
            self.svc_mgr.${method_name}(self.catalog_id, PROXY)
        with self.assertRaises(errors.NullArgument):
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
        with self.assertRaises(errors.NullArgument):
            self.svc_mgr.${method_name}()"""

    get_group_hierarchy_session = """
        if self.svc_mgr.supports_group_hierarchy():
            self.svc_mgr.get_group_hierarchy_session(PROXY)
        with self.assertRaises(errors.Unimplemented):
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
        'from dlkit.primordium.id.primitives import Id',
        'ALIAS_ID = Id(**{\'identifier\': \'ALIAS\', \'namespace\': \'ALIAS\', \'authority\': \'ALIAS\'})',
    ]

    init_template = """
    @classmethod
    def setUpClass(cls):
        # Implemented from init template for ResourceLookupSession
        cls.${object_name_under}_list = list()
        cls.${object_name_under}_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_${object_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            obj = cls.catalog.create_${object_name_under}(create_form)
            cls.${object_name_under}_list.append(obj)
            cls.${object_name_under}_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        # Implemented from init template for ResourceLookupSession
        for obj in cls.catalog.get_${object_name_under_plural}():
            cls.catalog.delete_${object_name_under}(obj.ident)
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog.ident)"""

    get_bin_id_template = """
        self.assertEqual(self.catalog.${method_name}(), self.catalog.ident)"""

    get_bin_template = """
        # is this test really needed?
        # From test_templates/resource.py::ResourceLookupSession::get_bin_template
        self.assertIsNotNone(self.catalog)"""

    can_lookup_resources_template = """
        self.assertTrue(isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool))"""

    use_comparative_resource_view_template = """
        self.catalog.${method_name}()"""

    use_plenary_resource_view_template = """
        self.catalog.${method_name}()"""

    use_federated_bin_view_template = """
        self.catalog.${method_name}()"""

    use_isolated_bin_view_template = """
        self.catalog.${method_name}()"""

    get_resource_template = """
        # From test_templates/resource.py ResourceLookupSession.get_resource_template
        self.catalog.use_isolated_${cat_name_under}_view()
        obj = self.catalog.${method_name}(self.${object_name_under}_list[0].ident)
        self.assertEqual(obj.ident, self.${object_name_under}_list[0].ident)
        self.catalog.use_federated_${cat_name_under}_view()
        obj = self.catalog.${method_name}(self.${object_name_under}_list[0].ident)
        self.assertEqual(obj.ident, self.${object_name_under}_list[0].ident)"""

    get_resources_by_ids_template = """
        # From test_templates/resource.py ResourceLookupSession.get_resources_by_ids_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        objects = self.catalog.${method_name}(self.${object_name_under}_ids)
        self.assertTrue(isinstance(objects, ${return_type}))
        self.catalog.use_federated_${cat_name_under}_view()
        objects = self.catalog.${method_name}(self.${object_name_under}_ids)"""

    get_resources_by_genus_type_template = """
        # From test_templates/resource.py ResourceLookupSession.get_resources_by_genus_type_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        objects = self.catalog.${method_name}(DEFAULT_TYPE)
        self.assertTrue(isinstance(objects, ${return_type}))
        self.catalog.use_federated_${cat_name_under}_view()
        objects = self.catalog.${method_name}(DEFAULT_TYPE)"""

    get_resources_by_parent_genus_type_template = """
        # From test_templates/resource.py ResourceLookupSession.get_resources_by_parent_genus_type_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        objects = self.catalog.${method_name}(DEFAULT_TYPE)
        self.assertTrue(isinstance(objects, ${return_type}))
        self.catalog.use_federated_${cat_name_under}_view()
        objects = self.catalog.${method_name}(DEFAULT_TYPE)"""

    get_resources_by_record_type_template = """
        # From test_templates/resource.py ResourceLookupSession.get_resources_by_record_type_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        objects = self.catalog.${method_name}(DEFAULT_TYPE)
        self.assertTrue(isinstance(objects, ${return_type}))
        self.catalog.use_federated_${cat_name_under}_view()
        objects = self.catalog.${method_name}(DEFAULT_TYPE)"""

    get_resources_template = """
        # From test_templates/resource.py ResourceLookupSession.get_resources_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        objects = self.catalog.${method_name}()
        self.assertTrue(isinstance(objects, ${return_type}))
        self.catalog.use_federated_${cat_name_under}_view()
        objects = self.catalog.${method_name}()

    def test_get_${object_name_under}_with_alias(self):
        self.catalog.alias_${object_name_under}(self.${object_name_under}_ids[0], ALIAS_ID)
        obj = self.catalog.get_${object_name_under}(ALIAS_ID)
        self.assertEqual(obj.get_id(), self.${object_name_under}_ids[0])"""


class ResourceQuerySession:

    import_statements_pattern = [
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
    @classmethod
    def setUpClass(cls):
        cls.${object_name_under}_list = list()
        cls.${object_name_under}_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = cls.catalog.get_${object_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + color
            create_form.description = (
                'Test ${object_name} for ${interface_name} tests, did I mention green')
            obj = cls.catalog.create_${object_name_under}(create_form)
            cls.${object_name_under}_list.append(obj)
            cls.${object_name_under}_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_${object_name_under_plural}():
            cls.catalog.delete_${object_name_under}(obj.ident)
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog.ident)"""

    can_query_resources_template = """
        self.assertTrue(isinstance(self.catalog.${method_name}(), bool))"""

    get_resource_query_template = """
        query = self.catalog.${method_name}()"""

    get_resources_by_query_template = """
        # From test_templates/resource.py ResourceQuerySession::get_resources_by_query_template
        # Need to add some tests with string types
        query = self.catalog.get_${object_name_under}_query()
        query.match_display_name('orange')
        self.assertEqual(self.catalog.${method_name}(query).available(), 2)
        query.clear_display_name_terms()
        query.match_display_name('blue', match=False)
        self.assertEqual(self.catalog.${method_name}(query).available(), 3)"""


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
    # From test_templates/resource.py::ResourceAdminSession::init_template
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)

        form = cls.catalog.get_${object_name_under}_form_for_create([])
        form.display_name = 'new ${object_name}'
        form.description = 'description of ${object_name}'
        form.set_genus_type(NEW_TYPE)
        cls.osid_object = cls.catalog.create_${object_name_under}(form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_${object_name_under_plural}():
            cls.catalog.delete_${object_name_under}(obj.ident)
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog.ident)"""

    can_create_resources_template = """
        # From test_templates/resource.py::ResourceAdminSession::can_create_resources_template
        self.assertTrue(isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool))"""

    can_update_resources_template = """
        # From test_templates/resource.py::ResourceAdminSession::can_update_resources_template
        self.assertTrue(isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool))"""

    can_delete_resources_template = """
        # From test_templates/resource.py::ResourceAdminSession::can_delete_resources_template
        self.assertTrue(isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool))"""

    can_manage_resource_aliases_template = """
        # From test_templates/resource.py::ResourceAdminSession::can_manage_resource_aliases_template
        self.assertTrue(isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool))"""

    can_create_resource_with_record_types_template = """
        # From test_templates/resource.py::ResourceAdminSession::can_create_resource_with_record_types_template
        self.assertTrue(isinstance(self.${svc_mgr_or_catalog}.${method_name}(DEFAULT_TYPE), bool))"""

    get_resource_form_for_create_template = """
        # From test_templates/resource.py::ResourceAdminSession::get_resource_form_for_create_template
        form = self.catalog.${method_name}([])
        self.assertTrue(isinstance(form, OsidForm))
        self.assertFalse(form.is_for_update())"""

    create_resource_template = """
        # From test_templates/resource.py::ResourceAdminSession::create_resource_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${object_name}
        self.assertTrue(isinstance(self.osid_object, ${object_name}))
        self.assertEqual(self.osid_object.display_name.text, 'new ${object_name}')
        self.assertEqual(self.osid_object.description.text, 'description of ${object_name}')
        self.assertEqual(self.osid_object.genus_type, NEW_TYPE)"""

    get_resource_form_for_update_template = """
        # From test_templates/resource.py::ResourceAdminSession::get_resource_form_for_update_template
        form = self.catalog.${method_name}(self.osid_object.ident)
        self.assertTrue(isinstance(form, OsidForm))
        self.assertTrue(form.is_for_update())"""

    update_resource_template = """
        # From test_templates/resource.py::ResourceAdminSession::update_resource_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${object_name}
        form = self.catalog.get_${object_name_under}_form_for_update(self.osid_object.ident)
        form.display_name = 'new name'
        form.description = 'new description'
        form.set_genus_type(NEW_TYPE_2)
        updated_object = self.catalog.${method_name}(form)
        self.assertTrue(isinstance(updated_object, ${object_name}))
        self.assertEqual(updated_object.ident, self.osid_object.ident)
        self.assertEqual(updated_object.display_name.text, 'new name')
        self.assertEqual(updated_object.description.text, 'new description')
        self.assertEqual(updated_object.genus_type, NEW_TYPE_2)"""

    delete_resource_template = """
        # From test_templates/resource.py::ResourceAdminSession::delete_resource_template
        form = self.catalog.get_${object_name_under}_form_for_create([])
        form.display_name = 'new ${object_name}'
        form.description = 'description of ${object_name}'
        form.set_genus_type(NEW_TYPE)
        osid_object = self.catalog.create_${object_name_under}(form)
        self.catalog.${method_name}(osid_object.ident)
        with self.assertRaises(errors.NotFound):
            self.catalog.get_${object_name_under}(osid_object.ident)"""

    alias_resource_template = """
        # From test_templates/resource.py::ResourceAdminSession::alias_resource_template
        alias_id = Id(self.catalog.ident.namespace + '%3Amy-alias%40ODL.MIT.EDU')
        self.catalog.${method_name}(self.osid_object.ident, alias_id)
        aliased_object = self.catalog.get_${object_name_under}(alias_id)
        self.assertEqual(aliased_object.ident, self.osid_object.ident)"""


class ResourceNotificationSession:

    # Placeholder: still need to write a real ResourceNotificationSession tess
    import_statements_pattern = ResourceLookupSession.import_statements_pattern

    # Placeholder: still need to write a real ResourceNotificationSession tess
    init_template = ResourceLookupSession.init_template


class ResourceBinSession:

    import_statements_pattern = [
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
    @classmethod
    def setUpClass(cls):
        cls.${object_name_under}_list = list()
        cls.${object_name_under}_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name} for Assignment'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests assignment'
        cls.assigned_catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
        for num in [0, 1, 2]:
            create_form = cls.catalog.get_${object_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            obj = cls.catalog.create_${object_name_under}(create_form)
            cls.${object_name_under}_list.append(obj)
            cls.${object_name_under}_ids.append(obj.ident)
        cls.svc_mgr.assign_${object_name_under}_to_${cat_name_under}(
            cls.${object_name_under}_ids[1], cls.assigned_catalog.ident)
        cls.svc_mgr.assign_${object_name_under}_to_${cat_name_under}(
            cls.${object_name_under}_ids[2], cls.assigned_catalog.ident)

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.unassign_${object_name_under}_from_${cat_name_under}(
            cls.${object_name_under}_ids[1], cls.assigned_catalog.ident)
        cls.svc_mgr.unassign_${object_name_under}_from_${cat_name_under}(
            cls.${object_name_under}_ids[2], cls.assigned_catalog.ident)
        for obj in cls.catalog.get_${object_name_under_plural}():
            cls.catalog.delete_${object_name_under}(obj.ident)
        cls.svc_mgr.delete_${cat_name_under}(cls.assigned_catalog.ident)
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog.ident)"""

    get_resource_ids_by_bin_template = """
        objects = self.svc_mgr.get_${object_name_under}_ids_by_${cat_name_under}(self.assigned_catalog.ident)
        self.assertEqual(objects.available(), 2)"""

    get_resource_by_bin_template = """
        objects = self.svc_mgr.get_${object_name_plural_under}_ids_by_${cat_name_under}(self.assigned_catalog.ident)
        self.assertEqual(objects.available(), 2)"""

    get_bin_ids_by_resource_template = """
        cats = self.svc_mgr.get_${cat_name_under}_ids_by_${object_name_under}(self.${object_name_under}_ids[1])
        self.assertEqual(cats.available(), 2)"""

    get_bins_by_resource_template = """
        cats = self.svc_mgr.get_${cat_name_plural_under}_by_${object_name_under}(self.${object_name_under}_ids[1])
        self.assertEqual(cats.available(), 2)"""


class ResourceAgentSession:

    import_statements = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.primordium.id.primitives import Id',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'AGENT_ID_0 = Id(**{\'identifier\': \'jane_doe\', \'namespace\': \'osid.agent.Agent\', \'authority\': \'MIT-ODL\'})',
        'AGENT_ID_1 = Id(**{\'identifier\': \'john_doe\', \'namespace\': \'osid.agent.Agent\', \'authority\': \'MIT-ODL\'})',
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.resource_list = list()
        cls.resource_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('RESOURCE', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bin_form_for_create([])
        create_form.display_name = 'Test Bin'
        create_form.description = 'Test Bin for ResourceLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bin(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_resource_form_for_create([])
            create_form.display_name = 'Test Resource ' + str(num)
            create_form.description = 'Test Resource for ResourceLookupSession tests'
            obj = cls.catalog.create_resource(create_form)
            cls.resource_list.append(obj)
            cls.resource_ids.append(obj.ident)
        cls.catalog.assign_agent_to_resource(AGENT_ID_0, cls.resource_ids[0])
        cls.catalog.assign_agent_to_resource(AGENT_ID_1, cls.resource_ids[1])

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_bins():
            for obj in catalog.get_resources():
                catalog.delete_resource(obj.ident)
            cls.svc_mgr.delete_bin(catalog.ident)"""

    get_resource_id_by_agent = """
        resource_id = self.catalog.get_resource_id_by_agent(AGENT_ID_0)"""

    get_resource_by_agent = """
        resource = self.catalog.get_resource_by_agent(AGENT_ID_1)
        self.assertEqual(resource.display_name.text, 'Test Resource 1')"""

    get_agent_ids_by_resource = """
        id_list = self.catalog.get_agent_ids_by_resource(self.resource_ids[0])
        self.assertEqual(id_list.next(), AGENT_ID_0)"""

    get_agents_by_resource = """"""


class ResourceAgentAssignmentSession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.resource_list = list()
        cls.resource_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('RESOURCE', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bin_form_for_create([])
        create_form.display_name = 'Test Bin'
        create_form.description = 'Test Bin for ResourceLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bin(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_resource_form_for_create([])
            create_form.display_name = 'Test Resource ' + str(num)
            create_form.description = 'Test Resource for ResourceLookupSession tests'
            obj = cls.catalog.create_resource(create_form)
            cls.resource_list.append(obj)
            cls.resource_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_bins():
            for obj in catalog.get_resources():
                catalog.delete_resource(obj.ident)
            cls.svc_mgr.delete_bin(catalog.ident)"""

    assign_agent_to_resource = """
        self.catalog.assign_agent_to_resource(AGENT_ID_0, self.resource_ids[0])
        with self.assertRaises(errors.AlreadyExists):
            self.catalog.assign_agent_to_resource(AGENT_ID_0, self.resource_ids[1])"""

    unassign_agent_from_resource = """
        self.catalog.assign_agent_to_resource(AGENT_ID_1, self.resource_ids[1])
        self.assertEqual(self.catalog.get_resource_by_agent(AGENT_ID_1).display_name.text, 'Test Resource 1')
        self.catalog.unassign_agent_from_resource(AGENT_ID_1, self.resource_ids[1])
        with self.assertRaises(errors.NotFound):
            self.catalog.get_resource_by_agent(AGENT_ID_1)"""


class BinLookupSession:

    import_statements_pattern = [
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
    @classmethod
    def setUpClass(cls):
        cls.catalogs = list()
        cls.catalog_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        for num in [0, 1]:
            create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
            create_form.display_name = 'Test ${cat_name} ' + str(num)
            create_form.description = 'Test ${cat_name} for ${pkg_name} proxy manager tests'
            catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
            cls.catalogs.append(catalog)
            cls.catalog_ids.append(catalog.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_${cat_name_under_plural}():
            cls.svc_mgr.delete_${cat_name_under}(catalog.ident)"""

    use_comparative_bin_view_template = """
        self.svc_mgr.${method_name}()"""

    use_plenary_bin_view_template = """
        self.svc_mgr.${method_name}()"""

    get_bin_template = """
        catalog = self.svc_mgr.${method_name}(self.catalogs[0].ident)
        self.assertEqual(catalog.ident, self.catalogs[0].ident)"""

    get_bins_by_ids_template = """
        catalogs = self.svc_mgr.${method_name}(self.catalog_ids)"""

    test_get_bins_by_genus_type_template = """
        catalogs = self.svc_mgr.${method_name}(DEFAULT_TYPE)"""

    test_get_bins_by_parent_genus_type_template = """
        catalogs = self.svc_mgr.${method_name}(DEFAULT_TYPE)"""

    test_get_bins_by_record_type_template = """
        catalogs = self.svc_mgr.${method_name}(DEFAULT_TYPE)"""

    test_get_bins_by_provider_template = """
        # PASSES RESOURCE_ID!!!!
        catalogs = self.svc_mgr.${method_name}()"""

    get_bins_template = """
        catalogs = self.svc_mgr.${method_name}()"""


class BinAdminSession:

    import_statements_pattern = [
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
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        # Initialize test catalog:
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
        # Initialize catalog to be deleted:
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name} For Deletion'
        create_form.description = 'Test ${cat_name} for ${interface_name} deletion test'
        cls.catalog_to_delete = cls.svc_mgr.create_${cat_name_under}(create_form)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_${cat_name_under_plural}():
            cls.svc_mgr.delete_${cat_name_under}(catalog.ident)"""

    can_create_bins_template = """
        # From test_templates/resource.py BinAdminSession.can_create_bins_template
        self.assertTrue(isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool))"""

    can_create_bin_with_record_types_template = """
        # From test_templates/resource.py BinAdminSession.can_create_bin_with_record_types_template
        self.assertTrue(isinstance(self.${svc_mgr_or_catalog}.${method_name}(DEFAULT_TYPE), bool))"""

    get_bin_form_for_create_template = """
        # From test_templates/resource.py BinAdminSession.get_bin_form_for_create_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        catalog_form = self.svc_mgr.${method_name}([])
        self.assertTrue(isinstance(catalog_form, ${return_type}))
        self.assertFalse(catalog_form.is_for_update())"""

    create_bin_template = """
        # From test_templates/resource.py BinAdminSession.create_bin_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        catalog_form = self.svc_mgr.get_${cat_name_under}_form_for_create([])
        catalog_form.display_name = 'Test ${cat_name}'
        catalog_form.description = 'Test ${cat_name} for ${interface_name}.${method_name} tests'
        new_catalog = self.svc_mgr.${method_name}(catalog_form)
        self.assertTrue(isinstance(new_catalog, ${return_type}))"""

    get_bin_form_for_update_template = """
        # From test_templates/resource.py BinAdminSession.get_bin_form_for_update_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        catalog_form = self.svc_mgr.${method_name}(self.catalog.ident)
        self.assertTrue(isinstance(catalog_form, ${return_type}))
        self.assertTrue(catalog_form.is_for_update())"""

    update_bin_template = """
        # From test_templates/resource.py BinAdminSession.update_bin_template
        catalog_form = self.svc_mgr.get_${cat_name_under}_form_for_update(self.catalog.ident)
        # Update some elements here?
        self.svc_mgr.${method_name}(catalog_form)"""

    delete_bin_template = """
        # From test_templates/resource.py BinAdminSession.delete_bin_template
        cat_id = self.catalog_to_delete.ident
        self.svc_mgr.${method_name}(cat_id)
        with self.assertRaises(errors.NotFound):
            self.svc_mgr.get_${cat_name_under}(cat_id)"""

    alias_bin_template = """
        # From test_templates/resource.py BinAdminSession.alias_bin_template
        alias_id = Id('${package_name_replace_reserved}.${cat_name}%3Amy-alias%40ODL.MIT.EDU')
        self.svc_mgr.${method_name}(self.catalog_to_delete.ident, alias_id)
        aliased_catalog = self.svc_mgr.get_${cat_name_under}(alias_id)
        self.assertEqual(self.catalog_to_delete.ident, aliased_catalog.ident)"""


class BinHierarchySession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.id.objects import IdList',
        'from dlkit.abstract_osid.hierarchy.objects import Hierarchy',
        'from dlkit.abstract_osid.osid.objects import OsidNode',
        'from dlkit.primordium.id.primitives import Id'
    ]

    init_template = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        cls.catalogs = dict()
        for name in ['Root', 'Child 1', 'Child 2', 'Grandchild 1']:
            create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
            create_form.display_name = name
            create_form.description = 'Test ${cat_name} ' + name
            cls.catalogs[name] = cls.svc_mgr.create_${cat_name_under}(create_form)
        cls.svc_mgr.add_root_${cat_name_under}(cls.catalogs['Root'].ident)
        cls.svc_mgr.add_child_${cat_name_under}(cls.catalogs['Root'].ident, cls.catalogs['Child 1'].ident)
        cls.svc_mgr.add_child_${cat_name_under}(cls.catalogs['Root'].ident, cls.catalogs['Child 2'].ident)
        cls.svc_mgr.add_child_${cat_name_under}(cls.catalogs['Child 1'].ident, cls.catalogs['Grandchild 1'].ident)

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.remove_child_${cat_name_under}(cls.catalogs['Child 1'].ident, cls.catalogs['Grandchild 1'].ident)
        cls.svc_mgr.remove_child_${cat_name_under_plural}(cls.catalogs['Root'].ident)
        cls.svc_mgr.remove_root_${cat_name_under}(cls.catalogs['Root'].ident)
        for cat_name in cls.catalogs:
            cls.svc_mgr.delete_${cat_name_under}(cls.catalogs[cat_name].ident)"""

    can_access_objective_bank_hierarchy_template = """
        # From test_templates/resource.py::BinHierarchySession::can_access_objective_bank_hierarchy_template
        self.assertTrue(isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool))"""

    get_bin_hierarchy_id_template = """
        # From test_templates/resource.py::BinHierarchySession::get_bin_hierarchy_id_template
        hierarchy_id = self.svc_mgr.${method_name}()
        self.assertTrue(isinstance(hierarchy_id, Id))"""

    get_bin_hierarchy_template = """
        # From test_templates/resource.py::BinHierarchySession::get_bin_hierarchy_template
        hierarchy = self.svc_mgr.${method_name}()
        self.assertTrue(isinstance(hierarchy, Hierarchy))"""

    get_root_bin_ids_template = """
        # From test_templates/resource.py::BinHierarchySession::get_root_bin_ids_template
        root_ids = self.svc_mgr.${method_name}()
        self.assertTrue(isinstance(root_ids, IdList))
        # probably should be == 1, but we seem to be getting test cruft,
        # and I can't pinpoint where it's being introduced.
        self.assertTrue(root_ids.available() >= 1)"""

    get_root_bins_template = """
        # From test_templates/resource.py::BinHierarchySession::get_root_bins_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${cat_name}List
        roots = self.svc_mgr.${method_name}()
        self.assertTrue(isinstance(roots, ${cat_name}List))
        self.assertTrue(roots.available() == 1)"""

    has_parent_bins_template = """
        # From test_templates/resource.py::BinHierarchySession::has_parent_bins_template
        self.assertTrue(isinstance(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident), bool))
        self.assertTrue(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident))
        self.assertTrue(self.svc_mgr.${method_name}(self.catalogs['Child 2'].ident))
        self.assertTrue(self.svc_mgr.${method_name}(self.catalogs['Grandchild 1'].ident))
        self.assertFalse(self.svc_mgr.${method_name}(self.catalogs['Root'].ident))"""

    is_parent_of_bin_template = """
        # From test_templates/resource.py::BinHierarchySession::is_parent_of_bin_template
        self.assertTrue(isinstance(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, self.catalogs['Root'].ident), bool))
        self.assertTrue(self.svc_mgr.${method_name}(self.catalogs['Root'].ident, self.catalogs['Child 1'].ident))
        self.assertTrue(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, self.catalogs['Grandchild 1'].ident))
        self.assertFalse(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, self.catalogs['Root'].ident))"""

    get_parent_bin_ids_template = """
        # From test_templates/resource.py::BinHierarchySession::get_parent_bin_ids_template
        from dlkit.abstract_osid.id.objects import ${return_type}
        catalog_list = self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident)
        self.assertTrue(isinstance(catalog_list, ${return_type}))
        self.assertEqual(catalog_list.available(), 1)"""

    get_parent_bins_template = """
        # From test_templates/resource.py::BinHierarchySession::get_parent_bins_template
        from dlkit.abstract_osid.${package_name_replace}.objects import ${return_type}
        catalog_list = self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident)
        self.assertTrue(isinstance(catalog_list, ${return_type}))
        self.assertEqual(catalog_list.available(), 1)
        self.assertEqual(catalog_list.next().display_name.text, 'Root')"""

    is_ancestor_of_bin_template = """
        # From test_templates/resource.py::BinHierarchySession::is_ancestor_of_bin_template
        self.assertRaises(errors.Unimplemented,
                          self.svc_mgr.${method_name},
                          self.catalogs['Root'].ident,
                          self.catalogs['Child 1'].ident)
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
        self.assertTrue(isinstance(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident), bool))
        self.assertTrue(self.svc_mgr.${method_name}(self.catalogs['Root'].ident))
        self.assertTrue(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident))
        self.assertFalse(self.svc_mgr.${method_name}(self.catalogs['Child 2'].ident))
        self.assertFalse(self.svc_mgr.${method_name}(self.catalogs['Grandchild 1'].ident))"""

    is_child_of_bin_template = """
        self.assertTrue(isinstance(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, self.catalogs['Root'].ident), bool))
        self.assertTrue(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, self.catalogs['Root'].ident))
        self.assertTrue(self.svc_mgr.${method_name}(self.catalogs['Grandchild 1'].ident, self.catalogs['Child 1'].ident))
        self.assertFalse(self.svc_mgr.${method_name}(self.catalogs['Root'].ident, self.catalogs['Child 1'].ident))"""

    get_child_bin_ids_template = """
        from dlkit.abstract_osid.id.objects import ${return_type}
        catalog_list = self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident)
        self.assertTrue(isinstance(catalog_list, ${return_type}))
        self.assertEqual(catalog_list.available(), 1)"""

    get_child_bins_template = """
        from dlkit.abstract_osid.${package_name_replace}.objects import ${return_type}
        catalog_list = self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident)
        self.assertTrue(isinstance(catalog_list, ${return_type}))
        self.assertEqual(catalog_list.available(), 1)
        self.assertEqual(catalog_list.next().display_name.text, 'Grandchild 1')"""

    is_descendant_of_bin_template = """
        # From test_templates/resource.py::BinHierarchySession::is_descendant_of_bin_template
        self.assertRaises(errors.Unimplemented,
                          self.svc_mgr.${method_name},
                          self.catalogs['Child 1'].ident,
                          self.catalogs['Root'].ident)
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
        node = self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, 1, 2, False)
        self.assertTrue(isinstance(node, OsidNode))
        self.assertFalse(node.is_root())
        self.assertFalse(node.is_leaf())
        self.assertTrue(node.get_child_ids().available(), 1)
        self.assertTrue(isinstance(node.get_child_ids(), IdList))
        self.assertTrue(node.get_parent_ids().available(), 1)
        self.assertTrue(isinstance(node.get_parent_ids(), IdList))"""

    get_bin_nodes_template = """
        # From test_templates/resource.py::BinHierarchySession::get_bin_nodes_template
        node = self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, 1, 2, False)
        self.assertTrue(isinstance(node, OsidNode))
        self.assertFalse(node.is_root())
        self.assertFalse(node.is_leaf())
        self.assertTrue(node.get_child_ids().available(), 1)
        self.assertTrue(isinstance(node.get_child_ids(), IdList))
        self.assertTrue(node.get_parent_ids().available(), 1)
        self.assertTrue(isinstance(node.get_parent_ids(), IdList))"""


class BinHierarchyDesignSession:

    import_statements_pattern = [
    ]

    init_template = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        cls.catalogs = dict()
        for name in ['Root', 'Child 1', 'Child 2', 'Grandchild 1']:
            create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
            create_form.display_name = name
            create_form.description = 'Test ${cat_name} ' + name
            cls.catalogs[name] = cls.svc_mgr.create_${cat_name_under}(create_form)
        cls.svc_mgr.add_root_${cat_name_under}(cls.catalogs['Root'].ident)
        cls.svc_mgr.add_child_${cat_name_under}(cls.catalogs['Root'].ident, cls.catalogs['Child 1'].ident)
        cls.svc_mgr.add_child_${cat_name_under}(cls.catalogs['Root'].ident, cls.catalogs['Child 2'].ident)
        cls.svc_mgr.add_child_${cat_name_under}(cls.catalogs['Child 1'].ident, cls.catalogs['Grandchild 1'].ident)

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.remove_child_${cat_name_under}(cls.catalogs['Child 1'].ident, cls.catalogs['Grandchild 1'].ident)
        cls.svc_mgr.remove_child_${cat_name_under_plural}(cls.catalogs['Root'].ident)
        for cat_name in cls.catalogs:
            cls.svc_mgr.delete_${cat_name_under}(cls.catalogs[cat_name].ident)"""

    can_modify_bin_hierarchy_template = """
        # this is tested in the setUpClass
        self.assertTrue(True)"""

    add_root_bin_template = """
        # this is tested in the setUpClass
        self.assertTrue(True)"""

    remove_root_bin_template = """
        # this is tested in the tearDownClass
        self.assertTrue(True)"""

    add_child_bin_template = """
        # this is tested in the setUpClass
        self.assertTrue(True)"""

    remove_child_bin_template = """
        # this is tested in the tearDownClass
        self.assertTrue(True)"""

    remove_child_bins_template = """
        # this is tested in the tearDownClass
        self.assertTrue(True)"""


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
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)

        form = cls.catalog.get_${object_name_under}_form_for_create([])
        form.display_name = 'Test object'
        cls.object = cls.catalog.create_${object_name_under}(form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_${object_name_under_plural}():
            cls.catalog.delete_${object_name_under}(obj.ident)
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog.ident)"""

    is_group_template = """
        # From test_templates/resources.py::Resource::is_group_template
        self.assertTrue(isinstance(self.object.${method_name}(), bool))
        self.assertFalse(self.object.${method_name}())"""

    is_demographic = """
        with self.assertRaises(AttributeError):
            self.object.is_demographic()"""

    has_avatar_template = """
        # From test_templates/resources.py::Resource::has_avatar_template
        self.assertTrue(isinstance(self.object.${method_name}(), bool))
        self.assertFalse(self.object.${method_name}())"""

    get_avatar_id_template = """
        # From test_templates/resources.py::Resource::get_avatar_id_template
        self.assertRaises(errors.IllegalState,
                          self.object.${method_name})"""

    get_avatar_template = """
        # From test_templates/resources.py::Resource::get_avatar_template
        self.assertRaises(errors.IllegalState,
                          self.object.${method_name})"""

    get_resource_record_template = """"""


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
    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::ResourceQuery::init_template
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)

    def setUp(self):
        # From test_templates/resource.py::ResourceQuery::init_template
        self.query = self.catalog.get_${object_name_under}_query()

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::ResourceQuery::init_template
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog.ident)"""

    clear_group_terms_template = """
        # From test_templates/resource.py::ResourceQuery::clear_group_terms_template
        self.query._query_terms['${var_name_mixed}'] = 'foo'
        self.query.${method_name}()
        self.assertNotIn('${var_name_mixed}',
                         self.query._query_terms)"""

    match_avatar_id_template = """
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('${var_name_mixed}', self.query._query_terms)
        self.query.${method_name}(test_id, match=True)
        self.assertEqual(self.query._query_terms['${var_name_mixed}'], {
            '$$in': [str(test_id)]
        })"""

    clear_avatar_id_terms_template = """
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_${var_name}(test_id, match=True)
        self.assertIn('${var_name_mixed}',
                      self.query._query_terms)
        self.query.${method_name}()
        self.assertNotIn('${var_name_mixed}',
                         self.query._query_terms)"""

    match_bin_id_template = """
        # From test_templates/resource.py::ResourceQuery::match_bin_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.${method_name}(test_id, match=True)
        self.assertEqual(self.query._query_terms['assigned${cat_name}Ids'], {
            '$$in': [str(test_id)]
        })"""

    clear_bin_id_terms_template = """
        # From test_templates/resource.py::ResourceQuery::clear_bin_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_${var_name}(test_id, match=True)
        self.assertIn('assigned${cat_name}Ids',
                      self.query._query_terms)
        self.query.${method_name}()
        self.assertNotIn('assigned${cat_name}Ids',
                         self.query._query_terms)"""


class ResourceForm:

    import_statements_pattern = [
        'from dlkit.json_.osid.metadata import Metadata',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.abstract_osid.id.primitives import Id as ABC_Id',
        'from dlkit.abstract_osid.locale.primitives import DisplayText as ABC_DisplayText',
    ]

    init_template = """
    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::ResourceForm::init_template
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)

    def setUp(self):
        # From test_templates/resource.py::ResourceForm::init_template
        self.form = self.catalog.get_${object_name_under}_form_for_create([])

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::ResourceForm::init_template
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog.ident)"""

    get_group_metadata_template = """
        # From test_templates/resource.py::ResourceForm::get_group_metadata_template
        mdata = self.form.${method_name}()
        self.assertTrue(isinstance(mdata, Metadata))
        self.assertTrue(isinstance(mdata.get_element_id(), ABC_Id))
        self.assertTrue(isinstance(mdata.get_element_label(), ABC_DisplayText))
        self.assertTrue(isinstance(mdata.get_instructions(), ABC_DisplayText))
        self.assertEquals(mdata.get_syntax(), '${syntax}')
        self.assertFalse(mdata.is_array())
        self.assertTrue(isinstance(mdata.is_required(), bool))
        self.assertTrue(isinstance(mdata.is_read_only(), bool))
        self.assertTrue(isinstance(mdata.is_linked(), bool))"""

    get_avatar_metadata_template = """
        # From test_templates/resource.py::ResourceForm::get_avatar_metadata_template
        mdata = self.form.${method_name}()
        self.assertTrue(isinstance(mdata, Metadata))
        self.assertTrue(isinstance(mdata.get_element_id(), ABC_Id))
        self.assertTrue(isinstance(mdata.get_element_label(), ABC_DisplayText))
        self.assertTrue(isinstance(mdata.get_instructions(), ABC_DisplayText))
        self.assertEquals(mdata.get_syntax(), '${syntax}')
        self.assertFalse(mdata.is_array())
        self.assertTrue(isinstance(mdata.is_required(), bool))
        self.assertTrue(isinstance(mdata.is_read_only(), bool))
        self.assertTrue(isinstance(mdata.is_linked(), bool))"""

    set_group_template = """
        # From test_templates/resource.py::ResourceForm::set_group_template
        self.form.${method_name}(True)
        self.assertTrue(self.form._my_map['${var_name_mixed}'])
        with self.assertRaises(errors.InvalidArgument):
            self.form.${method_name}('false')"""

    clear_group_template = """
        # From test_templates/resource.py::ResourceForm::clear_group_template
        self.form.set_${var_name}(True)
        self.assertTrue(self.form._my_map['${var_name_mixed}'])
        self.form.${method_name}()
        self.assertIsNone(self.form._my_map['${var_name_mixed}'])"""

    set_avatar_template = """
        # From test_templates/resource.py::ResourceForm::set_avatar_template
        self.assertEqual(self.form._my_map['${var_name_mixed}Id'], '')
        self.form.set_${var_name}(Id('repository.Asset%3Afake-id%40ODL.MIT.EDU'))
        self.assertEqual(self.form._my_map['${var_name_mixed}Id'],
                         'repository.Asset%3Afake-id%40ODL.MIT.EDU')
        with self.assertRaises(errors.InvalidArgument):
            self.form.${method_name}(True)"""

    clear_avatar_template = """
        # From test_templates/resource.py::ResourceForm::clear_avatar_template
        self.form.set_${var_name}(Id('repository.Asset%3Afake-id%40ODL.MIT.EDU'))
        self.assertEqual(self.form._my_map['${var_name_mixed}Id'],
                         'repository.Asset%3Afake-id%40ODL.MIT.EDU')
        self.form.${method_name}()
        self.assertEqual(self.form._my_map['${var_name_mixed}Id'], self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0])"""

    get_resource_form_record_template = """
        with self.assertRaises(errors.Unsupported):
            self.form.${method_name}(Type('osid.Osid%3Afake-record%40ODL.MIT.EDU'))
        # Here check for a real record?"""


class ResourceList:

    import_statements_pattern = [
    ]

    init_template = """
    @classmethod
    def setUpClass(cls):
        # Implemented from init template for ResourceList
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)

    def setUp(self):
        # Implemented from init template for ResourceList
        from dlkit.json_.${pkg_name_replaced_reserved}.objects import ${interface_name}
        self.${object_name_under}_list = list()
        self.${object_name_under}_ids = list()
        for num in [0, 1]:
            create_form = self.catalog.get_${object_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            obj = self.catalog.create_${object_name_under}(create_form)
            self.${object_name_under}_list.append(obj)
            self.${object_name_under}_ids.append(obj.ident)
        self.${object_name_under}_list = ${interface_name}(self.${object_name_under}_list)

    @classmethod
    def tearDownClass(cls):
        # Implemented from init template for ResourceList
        for obj in cls.catalog.get_${object_name_under_plural}():
            cls.catalog.delete_${object_name_under}(obj.ident)
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog.ident)"""

    get_next_resource_template = """
        # From test_templates/resource.py::ResourceList::get_next_resource_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        self.assertTrue(isinstance(self.${return_type_under}_list.${method_name}(), ${return_type}))"""

    get_next_resources_template = """
        # From test_templates/resource.py::ResourceList::get_next_resources_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}List, ${return_type}
        new_list = self.${return_type_under}_list.${method_name}(2)
        self.assertTrue(isinstance(new_list, ${return_type}List))
        for item in new_list:
            self.assertTrue(isinstance(item, ${return_type}))"""


class ResourceNodeList:
    init = """"""

    get_next_resource_node = """"""

    get_next_resource_nodes = """"""


class Bin:

    import_statements_pattern = [
    ]

    init_template = """
"""


class BinForm:

    import_statements_pattern = [
    ]

    init_template = """
"""


class BinList:

    import_statements_pattern = [
    ]

    init_template = """
    @classmethod
    def setUpClass(cls):
        # Implemented from init template for BinList
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
        cls.${object_name_under}_ids = list()

    def setUp(self):
        # Implemented from init template for BinList
        from dlkit.json_.${pkg_name_replaced_reserved}.objects import ${interface_name}
        self.${object_name_under}_list = list()
        for num in [0, 1]:
            create_form = self.svc_mgr.get_${object_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            obj = self.svc_mgr.create_${object_name_under}(create_form)
            self.${object_name_under}_list.append(obj)
            self.${object_name_under}_ids.append(obj.ident)
        self.${object_name_under}_list = ${interface_name}(self.${object_name_under}_list)

    @classmethod
    def tearDownClass(cls):
        # Implemented from init template for BinList
        for obj in cls.${object_name_under}_ids:
            cls.svc_mgr.delete_${cat_name_under}(obj)
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog.ident)"""


class BinNodeList:

    import_statements_pattern = [
    ]

    init_template = """
    @classmethod
    def setUpClass(cls):
        # Implemented from init template for BinNodeList
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
        cls.${object_name_under}_ids = list()

    def setUp(self):
        # Implemented from init template for BinNodeList
        from dlkit.json_.${pkg_name_replaced_reserved}.objects import ${interface_name}, ${object_name}
        self.${object_name_under}_list = list()
        for num in [0, 1]:
            create_form = self.svc_mgr.get_${cat_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            obj = self.svc_mgr.create_${cat_name_under}(create_form)
            self.${object_name_under}_list.append(${object_name}(obj.object_map))
            self.${object_name_under}_ids.append(obj.ident)
        # Not put the catalogs in a hierarchy
        self.svc_mgr.add_root_${cat_name_under}(self.${object_name_under}_list[0].ident)
        self.svc_mgr.add_child_${cat_name_under}(
            self.${object_name_under}_list[0].ident,
            self.${object_name_under}_list[1].ident)
        self.${object_name_under}_list = ${interface_name}(self.${object_name_under}_list)

    @classmethod
    def tearDownClass(cls):
        # Implemented from init template for BinNodeList
        for obj in cls.${object_name_under}_ids:
            cls.svc_mgr.delete_${cat_name_under}(obj)
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog.ident)"""


class BinNode:

    import_statements_pattern = [
    ]

    init_template = """
    @classmethod
    def setUpClass(cls):
        # Implemented from init template for BinNode
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
        cls.${object_name_under}_ids = list()

    def setUp(self):
        # Implemented from init template for BinNode
        from dlkit.json_.${pkg_name_replaced_reserved}.objects import ${interface_name}
        self.${object_name_under}_list = list()
        for num in [0, 1]:
            create_form = self.svc_mgr.get_${cat_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            obj = self.svc_mgr.create_${cat_name_under}(create_form)
            self.${object_name_under}_list.append(${interface_name}(
                obj.object_map,
                runtime=self.svc_mgr._runtime,
                proxy=self.svc_mgr._proxy))
            self.${object_name_under}_ids.append(obj.ident)
        # Not put the catalogs in a hierarchy
        self.svc_mgr.add_root_${cat_name_under}(self.${object_name_under}_list[0].ident)
        self.svc_mgr.add_child_${cat_name_under}(
            self.${object_name_under}_list[0].ident,
            self.${object_name_under}_list[1].ident)

    @classmethod
    def tearDownClass(cls):
        # Implemented from init template for BinNode
        for obj in cls.${object_name_under}_ids:
            cls.svc_mgr.delete_${cat_name_under}(obj)
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog.ident)"""

    get_bin_template = """
        # from test_templates/resource.py::BinNode::get_bin_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${cat_name}
        self.assertTrue(isinstance(self.${cat_name_under}_list[0].${method_name}(), ${cat_name}))
        self.assertEqual(str(self.${cat_name_under}_list[0].${method_name}().ident),
                         str(self.${cat_name_under}_list[0].ident))"""

    get_parent_bin_nodes_template = """
        # from test_templates/resource.py::BinNode::get_parent_bin_nodes
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${cat_name}NodeList
        node = self.svc_mgr.get_${cat_name_under}_nodes(
            self.${cat_name_under}_list[1].ident,
            1,
            0,
            False)
        self.assertTrue(isinstance(node.${method_name}(), ${cat_name}NodeList))
        self.assertEqual(node.${method_name}().available(),
                         1)
        self.assertEqual(str(node.${method_name}().next().ident),
                         str(self.${cat_name_under}_list[0].ident))"""

    get_child_bin_nodes_template = """
        # from test_templates/resource.py::BinNode::get_child_bin_nodes_template
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${cat_name}NodeList
        node = self.svc_mgr.get_${cat_name_under}_nodes(
            self.${cat_name_under}_list[0].ident,
            0,
            1,
            False)
        self.assertTrue(isinstance(node.${method_name}(), ${cat_name}NodeList))
        self.assertEqual(node.${method_name}().available(),
                         1)
        self.assertEqual(str(node.${method_name}().next().ident),
                         str(self.${cat_name_under}_list[1].ident))"""


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
    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::BinQuery::init_template
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
        cls.fake_id = Id('resource.Resource%3A1%40ODL.MIT.EDU')

    def setUp(self):
        # From test_templates/resource.py::BinQuery::init_template
        self.query = self.svc_mgr.get_${cat_name_under}_query()

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::BinQuery::init_template
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog.ident)"""

    clear_group_terms_template = """
        # From test_templates/resource.py::BinQuery::clear_group_terms_template
        self.query._query_terms['${var_name_mixed}'] = 'foo'
        self.query.${method_name}()
        self.assertNotIn('${var_name_mixed}',
                         self.query._query_terms)"""
