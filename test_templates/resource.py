"""Test templates for resource interfaces"""

class ResourceProfile:

    import_statements_pattern = [
        'from dlkit_django import RUNTIME, PROXY_SESSION, proxy_example',
        'from dlkit_django.managers import Runtime',
        'REQUEST = proxy_example.TestRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\',})\n',
        'from dlkit.abstract_osid.type.objects import TypeList as abc_type_list',
    ]

    init_template = """
    @classmethod
    def setUpClass(cls):
        cls.mgr = Runtime().get_service_manager('${pkg_name_upper}', 'TEST_SERVICE', PROXY)
"""

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
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', 'TEST_SERVICE', PROXY)
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${pkg_name} manager tests'
        catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
        cls.catalog_id = catalog.get_id()
        cls.mgr = RUNTIME.get_manager('${pkg_name_upper}', 'MONGO_1', (3, 0, 0))

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog_id)
"""

    get_resource_lookup_session_template = """
        if self.mgr.supports_${support_check}():
            self.mgr.${method_name}()"""

    get_resource_lookup_session_for_bin_template = """
        if self.mgr.supports_${support_check}():
            self.mgr.${method_name}(self.catalog_id)
        with self.assertRaises(errors.NullArgument):
            self.mgr.${method_name}()"""

    get_resource_batch_manager_template = """
        if self.mgr.supports_${support_check}():
            self.mgr.${method_name}()"""


class ResourceProxyManager:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
    ]

    init_template = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', 'TEST_SERVICE', PROXY)
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${pkg_name} proxy manager tests'
        catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
        cls.catalog_id = catalog.get_id()
        cls.mgr = RUNTIME.get_proxy_manager('${pkg_name_upper}', 'MONGO_1', (3, 0, 0))

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog_id)
"""

    get_resource_lookup_session_template = """
        if self.mgr.supports_${support_check}():
            self.mgr.${method_name}(PROXY)
        with self.assertRaises(errors.NullArgument):
            self.mgr.${method_name}()"""

    get_resource_lookup_session_for_bin_template = """
        if self.mgr.supports_${support_check}():
            self.mgr.${method_name}(self.catalog_id, PROXY)
        with self.assertRaises(errors.NullArgument):
            self.mgr.${method_name}()"""

    get_resource_batch_proxy_manager_template = """
        if self.mgr.supports_${support_check}():
            self.mgr.${method_name}()"""


class ResourceLookupSession:

    import_statements_pattern = [
        'from dlkit_django import RUNTIME, PROXY_SESSION, proxy_example',
        'from dlkit_django.managers import Runtime',
        'REQUEST = proxy_example.TestRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\',})\n',
    ]

    init_template = """
    @classmethod
    def setUpClass(cls):
        cls.${object_name_under}_list = list()
        cls.${object_name_under}_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', 'TEST_SERVICE', PROXY)
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
        #for obj in cls.catalog.get_${object_name_under_plural}():
        #    cls.catalog.delete_${object_name_under}(obj.ident)
        #for catalog in cls.catalogs:
        #    cls.svc_mgr.delete_${cat_name_under}(catalog.ident)
        for catalog in cls.svc_mgr.get_${cat_name_under_plural}():
            for obj in catalog.get_${object_name_under_plural}():
                catalog.delete_${object_name_under}(obj.ident)
            cls.svc_mgr.delete_${cat_name_under}(catalog.ident)
"""

    get_bin_id_template = """
        self.assertEqual(self.catalog.${method_name}(), self.catalog.ident)"""

    get_bin_template = """
        pass"""

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
        obj = self.catalog.${method_name}(self.${object_name_under}_list[0].ident)
        self.assertEqual(obj.ident, self.${object_name_under}_list[0].ident)"""

    get_resources_by_ids_template = """
        from dlkit.abstract_osid.${package_name}.objects import ${return_type}
        objects = self.catalog.${method_name}(self.${object_name_under}_ids)
        self.assertTrue(isinstance(objects, ${return_type}))
        self.catalog.use_federated_${cat_name_under}_view()
        objects = self.catalog.${method_name}(self.${object_name_under}_ids)"""

    get_resources_by_genus_type_template = """
        from dlkit.abstract_osid.${package_name}.objects import ${return_type}
        objects = self.catalog.${method_name}(DEFAULT_TYPE)
        self.assertTrue(isinstance(objects, ${return_type}))
        self.catalog.use_federated_${cat_name_under}_view()
        objects = self.catalog.${method_name}(DEFAULT_TYPE)"""

    get_resources_by_parent_genus_type_template = """
        from dlkit.abstract_osid.${package_name}.objects import ${return_type}
        objects = self.catalog.${method_name}(DEFAULT_TYPE)
        self.assertTrue(isinstance(objects, ${return_type}))
        self.catalog.use_federated_${cat_name_under}_view()
        objects = self.catalog.${method_name}(DEFAULT_TYPE)"""

    get_resources_by_record_type_template = """
        from dlkit.abstract_osid.${package_name}.objects import ${return_type}
        objects = self.catalog.${method_name}(DEFAULT_TYPE)
        self.assertTrue(isinstance(objects, ${return_type}))
        self.catalog.use_federated_${cat_name_under}_view()
        objects = self.catalog.${method_name}(DEFAULT_TYPE)"""

    get_resources_template = """
        from dlkit.abstract_osid.${package_name}.objects import ${return_type}
        objects = self.catalog.${method_name}()
        self.assertTrue(isinstance(objects, ${return_type}))
        self.catalog.use_federated_${cat_name_under}_view()
        objects = self.catalog.${method_name}()"""

class ResourceQuerySession:

    import_statements_pattern = [
    ]

    init_template = """
"""

    can_query_resources_template = """
        pass"""

    get_resource_query_template = """
        pass"""

    get_resources_by_query_template = """
        pass"""


class ResourceAdminSession:

    import_statements_pattern = [
        'from dlkit_django import RUNTIME, PROXY_SESSION, proxy_example',
        'from dlkit_django.managers import Runtime',
        'REQUEST = proxy_example.TestRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\',})\n',
    ]

    init_template = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', 'TEST_SERVICE', PROXY)
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_${object_name_under_plural}():
            cls.catalog.delete_${object_name_under}(obj.ident)
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog.ident)
"""

    can_create_resources_template = """
        self.assertTrue(isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool))"""

    can_create_resource_with_record_types_template = """
        self.assertTrue(isinstance(self.${svc_mgr_or_catalog}.${method_name}(DEFAULT_TYPE), bool))"""

    get_resource_form_for_create_template = """
        pass"""

    create_resource_template = """
        pass"""

    get_resource_form_for_update_template = """
        pass"""

    update_resource_template = """
        pass"""

    delete_resource_template = """
        pass"""

    alias_resources_template = """
        pass"""

class ResourceAgentSession:

    import_statements = [
        'from dlkit_django import RUNTIME, PROXY_SESSION, proxy_example',
        'from dlkit_django.managers import Runtime',
        'REQUEST = proxy_example.TestRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.primordium.id.primitives import Id',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\',})\n',
        'AGENT_ID_0 = Id(**{\'identifier\': \'jane_doe\', \'namespace\': \'authentication.Agent\', \'authority\': \'odl.mit.edu\',})\n',
        'AGENT_ID_1 = Id(**{\'identifier\': \'john_doe\', \'namespace\': \'authentication.Agent\', \'authority\': \'odl.mit.edu\',})\n',
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.resource_list = list()
        cls.resource_ids = list()
        cls.svc_mgr = Runtime('TEST_SERVICE').get_service_manager('RESOURCE', PROXY)
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
        #for obj in cls.catalog.get_resources():
        #    cls.catalog.delete_resource(obj.ident)
        #for catalog in cls.catalogs:
        #    cls.svc_mgr.delete_bin(catalog.ident)
        for catalog in cls.svc_mgr.get_bins():
            for obj in catalog.get_resources():
                catalog.delete_resource(obj.ident)
            cls.svc_mgr.delete_bin(catalog.ident)
"""

    get_resource_id_by_agent = """
        resource_id = self.catalog.get_resource_id_by_agent(AGENT_ID_0)"""

    get_resource_by_agent = """
        resource = self.catalog.get_resource_by_agent(AGENT_ID_1)
        self.assertEqual(resource.display_name.text, 'Test Resource 1')"""

    get_agent_ids_by_resource = """
        id_list = self.catalog.get_agent_ids_by_resource(self.resource_ids[0])
        self.assertEqual(id_list.next(), AGENT_ID_0)"""

    get_agents_by_resource = """
        """


class ResourceAgentAssignmentSession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.resource_list = list()
        cls.resource_ids = list()
        cls.svc_mgr = Runtime('TEST_SERVICE').get_service_manager('RESOURCE', PROXY)
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
        #for obj in cls.catalog.get_resources():
        #    cls.catalog.delete_resource(obj.ident)
        #for catalog in cls.catalogs:
        #    cls.svc_mgr.delete_bin(catalog.ident)
        for catalog in cls.svc_mgr.get_bins():
            for obj in catalog.get_resources():
                catalog.delete_resource(obj.ident)
            cls.svc_mgr.delete_bin(catalog.ident)
"""

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
        'from dlkit_django import RUNTIME, PROXY_SESSION, proxy_example',
        'from dlkit_django.managers import Runtime',
        'REQUEST = proxy_example.TestRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\',})\n',
    ]

    init_template = """
    @classmethod
    def setUpClass(cls):
        cls.catalogs = list()
        cls.catalog_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', 'TEST_SERVICE', PROXY)
        for num in [0, 1]:
            create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
            create_form.display_name = 'Test ${cat_name} ' + str(num)
            create_form.description = 'Test ${cat_name} for ${pkg_name} proxy manager tests'
            catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
            cls.catalogs.append(catalog)
            cls.catalog_ids.append(catalog.ident)

    @classmethod
    def tearDownClass(cls):
        #for catalog in cls.catalogs:
        #    cls.svc_mgr.delete_${cat_name_under}(catalog.ident)
        for catalog in cls.svc_mgr.get_${cat_name_under_plural}():
            cls.svc_mgr.delete_${cat_name_under}(catalog.ident)
"""

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
        'from dlkit_django import RUNTIME, PROXY_SESSION, proxy_example',
        'from dlkit_django.managers import Runtime',
        'REQUEST = proxy_example.TestRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\',})\n',
        'from dlkit.abstract_osid.osid import errors',
    ]

    init_template = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', 'TEST_SERVICE', PROXY)
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
        #for catalog in cls.catalogs:
        #    cls.svc_mgr.delete_${cat_name_under}(catalog.ident)
        for catalog in cls.svc_mgr.get_${cat_name_under_plural}():
            cls.svc_mgr.delete_${cat_name_under}(catalog.ident)
"""

    can_create_bins_template = """
        self.assertTrue(isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool))"""

    can_create_bin_with_record_types_template = """
        self.assertTrue(isinstance(self.${svc_mgr_or_catalog}.${method_name}(DEFAULT_TYPE), bool))"""

    get_bin_form_for_create_template = """
        from dlkit.abstract_osid.${package_name}.objects import ${return_type}
        catalog_form = self.svc_mgr.${method_name}([])
        self.assertTrue(isinstance(catalog_form, ${return_type}))
        self.assertFalse(catalog_form.is_for_update())"""

    create_bin_template = """
        from dlkit.abstract_osid.${package_name}.objects import ${return_type}
        catalog_form = self.svc_mgr.get_${cat_name_under}_form_for_create([])
        catalog_form.display_name = 'Test ${cat_name}'
        catalog_form.description = 'Test ${cat_name} for ${interface_name}.${method_name} tests'
        new_catalog = self.svc_mgr.${method_name}(catalog_form)
        self.assertTrue(isinstance(new_catalog, ${return_type}))"""

    get_bin_form_for_update_template = """
        from dlkit.abstract_osid.${package_name}.objects import ${return_type}
        catalog_form = self.svc_mgr.${method_name}(self.catalog.ident)
        self.assertTrue(isinstance(catalog_form, ${return_type}))
        self.assertTrue(catalog_form.is_for_update())"""

    update_bin_template = """
        catalog_form = self.svc_mgr.get_${cat_name_under}_form_for_update(self.catalog.ident)
        # Update some elements here?
        self.svc_mgr.${method_name}(catalog_form)"""

    delete_bin_template = """
        cat_id = self.catalog_to_delete.ident
        self.svc_mgr.${method_name}(cat_id)
        with self.assertRaises(errors.NotFound):
            self.svc_mgr.get_${cat_name_under}(cat_id)"""

    alias_bin_template = """
        pass"""

class BinHierarchySession:

    import_statements_pattern = [
    ]

    init_template = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', 'TEST_SERVICE', PROXY)
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
            cls.svc_mgr.delete_${cat_name_under}(cls.catalogs[cat_name].ident)
"""

    can_access_objective_bank_hierarchy_template = """
        self.assertTrue(isinstance(self.${svc_mgr_or_catalog}.${method_name}(), bool))"""

    get_bin_hierarchy_id_template = """
        hierarchy_id = self.svc_mgr.${method_name}()"""

    get_bin_hierarchy_template = """
        hierarchy = self.svc_mgr.${method_name}()"""

    get_root_bin_ids_template = """
        root_ids = self.svc_mgr.${method_name}()"""

    get_root_bins_template = """
        roots = self.svc_mgr.${method_name}()"""

    has_parent_bins_template = """
        self.assertTrue(isinstance(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident), bool))
        self.assertTrue(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident))
        self.assertTrue(self.svc_mgr.${method_name}(self.catalogs['Child 2'].ident))
        self.assertTrue(self.svc_mgr.${method_name}(self.catalogs['Grandchild 1'].ident))
        self.assertFalse(self.svc_mgr.${method_name}(self.catalogs['Root'].ident))"""

    is_parent_of_bin_template = """
        self.assertTrue(isinstance(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, self.catalogs['Root'].ident), bool))
        self.assertTrue(self.svc_mgr.${method_name}(self.catalogs['Root'].ident, self.catalogs['Child 1'].ident))
        self.assertTrue(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, self.catalogs['Grandchild 1'].ident))
        self.assertFalse(self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, self.catalogs['Root'].ident))"""

    get_parent_bin_ids_template = """
        from dlkit.abstract_osid.id.objects import ${return_type}
        catalog_list = self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident)
        self.assertTrue(isinstance(catalog_list, ${return_type}))
        self.assertEqual(catalog_list.available(), 1)"""

    get_parent_bins_template = """
        from dlkit.abstract_osid.${package_name}.objects import ${return_type}
        catalog_list = self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident)
        self.assertTrue(isinstance(catalog_list, ${return_type}))
        self.assertEqual(catalog_list.available(), 1)
        self.assertEqual(catalog_list.next().display_name.text, 'Root')"""

    is_ancestor_of_bin_template = """
        pass"""

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
        from dlkit.abstract_osid.${package_name}.objects import ${return_type}
        catalog_list = self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident)
        self.assertTrue(isinstance(catalog_list, ${return_type}))
        self.assertEqual(catalog_list.available(), 1)
        self.assertEqual(catalog_list.next().display_name.text, 'Grandchild 1')"""

    is_descendant_of_bin_template = """
        pass"""

    get_bin_node_ids_template = """
        node_ids = self.svc_mgr.${method_name}(self.catalogs['Child 1'].ident, 1, 1, False)
        # add some tests on the returned node"""

    get_bin_nodes_template = """
        pass"""

class BinHierarchyDesignSession:

    import_statements_pattern = [
    ]

    init_template = """
"""

    can_modify_bin_hierarchy_template = """
        pass"""

    add_root_bin_template = """
        pass"""

    remove_root_bin_template = """
        pass"""

    add_child_bin_template = """
        pass"""

    remove_child_bin_template = """
        pass"""

    remove_child_bins_template = """
        pass"""


class Resource:

    import_statements_pattern = [
    ]

    init_template = """
"""

    is_group_template = """
        pass"""

    is_demographic = """
        pass"""

    has_avatar_template = """
        pass"""

    get_avatar_id_template = """
        pass"""

    get_avatar_template = """
        pass"""

    get_resource_record_template = """
        pass"""

class ResourceQuery:

    import_statements_pattern = [
    ]

    init_template = """
"""

    clear_group_terms_template = """
        pass"""

class ResourceForm:

    import_statements_pattern = [
    ]

    init_template = """
"""

    get_group_metadata_template = """
        pass"""

    get_avatar_metadata_template = """
        pass"""

    set_group_template = """
        pass"""

    clear_group_template = """
        pass"""

    set_avatar_template = """
        pass"""

    clear_avatar_template = """
        pass"""

    get_resource_form_record_template = """
        pass"""


class ResourceList:

    import_statements_pattern = [
    ]

    get_next_resource_template = """
        pass"""

    get_next_resources_template = """
        pass"""

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
