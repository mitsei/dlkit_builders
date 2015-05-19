"""Test templates for resource interfaces"""

class ResourceProfile:

    import_statements_pattern = [
        'from dlkit_django import RUNTIME, PROXY_SESSION, proxy_example',
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
        cls.mgr = RUNTIME.get_service_manager('${pkg_name_upper}', PROXY)
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
        cls.svc_mgr = RUNTIME.get_service_manager('${pkg_name_upper}', PROXY)
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
        cls.svc_mgr = RUNTIME.get_service_manager('${pkg_name_upper}', PROXY)
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
        cls.svc_mgr = RUNTIME.get_service_manager('${pkg_name_upper}', PROXY)
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_${object_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            object = cls.catalog.create_${object_name_under}(create_form)
            cls.${object_name_under}_list.append(object)
            cls.${object_name_under}_ids.append(object.ident)

    @classmethod
    def tearDownClass(cls):
        for object in cls.catalog.get_${object_name_under_plural}():
            cls.catalog.delete_${object_name_under}(object.ident)
        #for catalog in cls.catalogs:
        #    cls.svc_mgr.delete_${cat_name_under}(catalog.ident)
        for catalog in cls.svc_mgr.get_${cat_name_under_plural}():
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
        'from dlkit.abstract_osid.osid import errors',
        'from ..osid.sessions import OsidSession',
        'from .. import mongo_client',
        'from . import queries',
        'DESCENDING = -1',
        'ASCENDING = 1'
    ]

    init_template = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
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
        self._catalog_view = ISOLATED
        self._kwargs = kwargs
"""

    can_query_resources_template = """
        # Implemented from template for
        # osid.resource.ResourceQuerySession.can_query_resources
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    get_resource_query_template = """
        # Implemented from template for
        # osid.resource.ResourceQuerySession.get_resource_query_template
        return queries.${return_type}()"""

    get_resources_by_query_template = """
        # Implemented from template for
        # osid.resource.ResourceQuerySession.get_resources_by_query
        if not ${arg0_name}:
            raise errors.NullArgument()
        query_terms = dict(${arg0_name}._query_terms)
        collection = mongo_client[self._db_prefix + '${package_name}']['${object_name}']
        if self._catalog_view == ISOLATED:
            query_terms['${cat_name_mixed}Id'] = str(self._catalog_id)
        result = collection.find(query_terms).sort('_id', DESCENDING)
        count = collection.find(query_terms).count()
        mongo_client.close()
        return objects.${return_type}(result, count=count, db_prefix=self._db_prefix, runtime=self._runtime)"""


class ResourceAdminSession:

    import_statements_pattern = [
        'from dlkit_django import RUNTIME, PROXY_SESSION, proxy_example',
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
        cls.svc_mgr = RUNTIME.get_service_manager('${pkg_name_upper}', PROXY)
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
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

    init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None):
        self._catalog_class = objects.Bin
        self._session_name = 'ResourceAgentSession'
        self._catalog_name = 'Bin'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='assessment',
            cat_name='Bin',
            cat_class=objects.Bin)
        self._forms = dict()
"""

    get_resource_id_by_agent = """
        # NOT DONE YET
        if agent_id is None:
            raise errors.NullArgument()
        collection = mongo_client[self._db_prefix + 'resource']['Resource']

        if self._catalog_view == ISOLATED:
            result = collection.find_one({'$in': {'agentIds': str(agent_id)},
                                          '${cat_name_mixed}Id': str(self._catalog_id)})
        else:
            # This should really look in the underlying hierarchy (when hierarchy is implemented)
            result = collection.find_one('SOMETHING HERE')
        if result is None:
            raise errors.NotFound()
        mongo_client.close()"""

    get_resource_by_agent = """
        # NOT DONE YET
        if agent_id is None:
            raise errors.NullArgument()
        collection = mongo_client[self._db_prefix + 'resource']['Resource']"""

    get_agent_ids_by_resource = """
        if resource_id is None:
            raise errors.NullArgument()
        collection = mongo_client[self._db_prefix + 'resource']['Resource']
        resource = collection.find_one({'_id': ObjectId(resource_id.get_identifier())})
        if resource is None:
            raise errors.NotFound()
        if 'agentIds' not in resource:
            result = IdList([])
        else:
            result = IdList(resource['agentIds'])
        mongo_client.close()
        return result"""

    get_agents_by_resource = """
        agent_list = []
        for agent_id in self.get_agent_ids_by_resource(resource_id):
            agent_list.append(Agent(agent_id))
        return AgentList(agent_list)"""


class ResourceAgentAssignmentSession:

    init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None):
        self._catalog_class = objects.Bin
        self._session_name = 'ResourceAgentAssignmentSession'
        self._catalog_name = 'Bin'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='assessment',
            cat_name='Bin',
            cat_class=objects.Bin)
        self._forms = dict()
"""

    assign_agent_to_resource = """
        if agent_id is None or resource_id is None:
            raise errors.NullArgument()
        # Should check for existence of Agent? We may mever manage them.
        collection = mongo_client[self._db_prefix + 'resource']['Resource']
        resource = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})
        if not resource:
            raise errors.NotFound()
        if 'agentIds' not in resource:
            resource['agentIds'] = [str(agent_id)]
        else:
            resource['agentIds'].append(str(agent_id))
        collection.save(resource)
        mongo_client.close()"""

    unassign_agent_from_resource = """
        if agent_id is None or resource_id is None:
            raise errors.NullArgument()
        collection = mongo_client[self._db_prefix + 'resource']['Resource']
        resource = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})
        if not resource:
            raise errors.NotFound()
        try:
            resource['agentIds'].remove(str(agent_id))
        except (KeyError, ValueError):
            raise errors.NotFound('agent_id not assigned to resource')
        collection.save(resource)
        mongo_client.close()"""


class BinLookupSession:

    import_statements_pattern = [
        'from dlkit_django import RUNTIME, PROXY_SESSION, proxy_example',
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
        cls.svc_mgr = RUNTIME.get_service_manager('${pkg_name_upper}', PROXY)
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
        cls.svc_mgr = RUNTIME.get_service_manager('${pkg_name_upper}', PROXY)
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
        cls.svc_mgr = RUNTIME.get_service_manager('${pkg_name_upper}', PROXY)
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
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from ..osid.sessions import OsidSession',
        'from . import objects',
        'COMPARATIVE = 0',
        'PLENARY = 1',
    ]

    init_template = """
    _session_name = '${interface_name}'

    def __init__(self, proxy=None, runtime=None, **kwargs):
        OsidSession._init_catalog(self, proxy, runtime)
        self._forms = dict()
        self._kwargs = kwargs
        hierarchy_mgr = self._get_provider_manager('HIERARCHY')
        self._hierarchy_session = hierarchy_mgr.get_hierarchy_design_session_for_hierarchy(
            Id(authority='${pkg_name_upper}',
               namespace='CATALOG',
               identifier='${cat_name_upper}')
        )
"""

    can_modify_bin_hierarchy_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchyDesignSession.can_modify_objective_bank_hierarchy
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    add_root_bin_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchyDesignSession.add_root_bin_template
        return self._hierarchy_session.add_root(id_=${arg0_name})"""

    remove_root_bin_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchyDesignSession.remove_root_bin_template
        return self._hierarchy_session.remove_root(id_=${arg0_name})"""

    add_child_bin_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchyDesignSession.add_child_bin_template
        return self._hierarchy_session.add_child(id_=${arg0_name}, child_id=${arg1_name})"""

    remove_child_bin_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchyDesignSession.remove_child_bin_template
        return self._hierarchy_session.remove_child(id_=${arg0_name}, child_id=${arg1_name})"""

    remove_child_bins_template = """
        # Implemented from template for
        # osid.resource.ResourceHierarchyDesignSession.remove_child_bin_template
        return self._hierarchy_session.remove_children(id_=${arg0_name})"""


class Resource:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        '#from ..id.objects import IdList',
        '#import importlib',
    ]

    init_template = """
    try:
        from ..records.types import ${object_name_upper}_RECORD_TYPES as _record_type_data_sets #pylint: disable=no-name-in-module
    except (ImportError, AttributeError):
        _record_type_data_sets = {}
    _namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, osid_object_map, db_prefix='', runtime=None):
        self._my_map = osid_object_map
        self._db_prefix = db_prefix
        self._runtime = runtime
        self._records = dict()
        self._load_records(osid_object_map['recordTypeIds'])
${instance_initers}
    # These next two private methods should be moved to osid.Extensible??? (I thought they were already)
    def _load_records(self, record_type_idstrs):
        \"\"\"Load all records of record type for this object.\"\"\"
        for record_type_idstr in record_type_idstrs:
            self._init_record(record_type_idstr)

    def _init_record(self, record_type_idstr):
        \"\"\"Initialize all records for this object.\"\"\"
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
            raise errors.IllegalState('this ${object_name} has no ${var_name}')
        else:
            return Id(self._my_map['${var_name_mixed}Id'])"""

    get_avatar_template = """
        # Implemented from template for osid.resource.Resource.get_avatar_template
        if not self._my_map['${var_name_mixed}Id']:
            raise errors.IllegalState('this ${object_name} has no ${var_name}')
        mgr = self._get_provider_manager('${return_pkg_caps}')
        if not mgr.supports_${return_type_under}_lookup():
            raise errors.OperationFailed('${return_pkg_title} does not support ${return_type} lookup')
        osid_object = mgr.get_${return_type_under}_lookup_session().get_${return_type_under}(self.get_${var_name}_id())
        return osid_object"""

    get_resource_record_template = """
        # This is now in Extensible and can be replaces with:
        # return self._get_record(${arg0_name}):
        if ${arg0_name} is None:
            raise errors.NullArgument()
        if not self.has_record_type(${arg0_name}):
            raise errors.Unsupported()
        if str(${arg0_name}) not in self._records:
            raise errors.Unimplemented()
        return self._records[str(${arg0_name})]"""

class ResourceQuery:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id'
    ]

    init_template = """
    def __init__(self):
        try:
            from ..records.types import ${object_name_upper}_RECORD_TYPES as record_type_data_sets #pylint: disable=no-name-in-module
        except (ImportError, AttributeError):
            record_type_data_sets = {}
        self._all_supported_record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_ids = []
        for data_set in record_type_data_sets:
            self._all_supported_record_type_ids.append(str(Id(**record_type_data_sets[data_set])))
        osid_queries.OsidQuery.__init__(self)
"""

    clear_group_terms_template = """
        self._clear_terms('${var_name_mixed}')"""

class ResourceForm:

    import_statements_pattern = [
        'import importlib',
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from ..osid.metadata import Metadata',
        'from . import mdata_conf'
    ]

    init_template = """
    try:
        from ..records.types import ${object_name_upper}_RECORD_TYPES as _record_type_data_sets #pylint: disable=no-name-in-module
    except (ImportError, AttributeError):
        _record_type_data_sets = dict()
    _namespace = '${implpkg_name}.${object_name}'

    def __init__(self, osid_object_map=None, record_types=None, db_prefix='', runtime=None, **kwargs):
        osid_objects.OsidForm.__init__(self)
        self._runtime = runtime
        self._db_prefix = db_prefix
        self._kwargs = kwargs
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
            if record_types is not None:
                self._init_records(record_types)
        self._supported_record_type_ids = self._my_map['recordTypeIds']

    def _init_metadata(self, **kwargs):
        ${init_object}._init_metadata(self, **kwargs)
${metadata_initers}
    def _init_map(self, **kwargs):
        ${init_object}._init_map(self)
${persisted_initers}
    # These next three private methods should be moved to osid.Extensible??? (I thought they were already)
    def _load_records(self, record_type_idstrs):
        \"\"\"Load all records of record type for this form.\"\"\"
        for record_type_idstr in record_type_idstrs:
            self._init_record(record_type_idstr)

    def _init_records(self, record_types):
        \"\"\"Initalize all records for this form.\"\"\"
        for record_type in record_types:
            # This conditional was inserted on 7/11/14. It may prove problematic:
            if str(record_type) not in self._my_map['recordTypeIds']:
                self._init_record(str(record_type))
                self._my_map['recordTypeIds'].append(str(record_type))

    def _init_record(self, record_type_idstr):
        \"\"\"Initalize a record of record type.\"\"\"
        record_type_data = self._record_type_data_sets[Id(record_type_idstr).get_identifier()]
        module = importlib.import_module(record_type_data['module_path'])
        record = getattr(module, record_type_data['form_record_class_name'])
        self._records[record_type_idstr] = record(self)
"""

    get_group_metadata_template = """
        # Implemented from template for osid.resource.ResourceForm.get_group_metadata_template
        metadata = dict(self._${var_name}_metadata)
        metadata.update({'existing_${var_name}_values': self._my_map['${var_name_mixed}']})
        return Metadata(**metadata)"""

    get_avatar_metadata_template = """
        # Implemented from template for osid.resource.ResourceForm.get_group_metadata_template
        metadata = dict(self._${var_name}_metadata)
        metadata.update({'existing_${var_name}_values': self._my_map['${var_name_mixed}Id']})
        return Metadata(**metadata)"""

    set_group_template = """
        # Implemented from template for osid.resource.ResourceForm.set_group_template
        if ${arg0_name} is None:
            raise errors.NullArgument()
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_${arg0_type}(${arg0_name}):
            raise errors.InvalidArgument()
        self._my_map['${var_name_mixed}'] = ${arg0_name}"""

    clear_group_template = """
        # Implemented from template for osid.resource.ResourceForm.clear_group_template
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['${var_name_mixed}'] = self._${var_name}_default"""

    set_avatar_template = """
        # Implemented from template for osid.resource.ResourceForm.set_avatar_template
        if ${arg0_name} is None:
            raise errors.NullArgument()
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_id(${arg0_name}):
            raise errors.InvalidArgument()
        self._my_map['${var_name_mixed}Id'] = str(${arg0_name})"""

    clear_avatar_template = """
        # Implemented from template for osid.resource.ResourceForm.clear_avatar_template
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['${var_name_mixed}Id'] = self._${var_name}_default"""

    get_resource_form_record_template = """
        # This is now in OsidExtensibleForm and can be replaces with:
        # return self._get_record(${arg0_name}):
        if ${arg0_name} is None:
            raise errors.NullArgument()
        if not self.has_record_type(${arg0_name}):
            raise errors.Unsupported()
        if str(${arg0_name}) not in self._records: # Currently this should never be True
            self._init_record(str(${arg0_name}))
            if str(${arg0_name}) not in self._my_map['recordTypeIds']: # nor this
                self._my_map['recordTypeIds'].append(str(${arg0_name}))
        return self._records[str(${arg0_name})]"""



class ResourceList:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
    ]

    get_next_resource_template = """
        # Implemented from template for osid.resource.ResourceList.get_next_resource
        try:
            next_item = self.next()
        except StopIteration:
            raise errors.IllegalState('no more elements available in this list')
        #except: #Need to specify exceptions here
        #    raise errors.OperationFailed()
        else:
            return next_item

    def next(self):
        next_item = osid_objects.OsidList.next(self)
        if isinstance(next_item, dict):
            next_item = ${return_type}(next_item, db_prefix=self._db_prefix, runtime=self._runtime)
        return next_item"""

    get_next_resources_template = """
    # Implemented from template for osid.resource.ResourceList.get_next_resources
        if ${arg0_name} > self.available():
            # !!! This is not quite as specified (see method docs) !!!
            raise errors.IllegalState('not enough elements available in this list')
        else:
            next_list = []
            i = 0
            while i < ${arg0_name}:
                try:
                    next_list.append(self.next())
                except StopIteration:
                    break
                i += 1
            return next_list"""

class Bin:

    import_statements_pattern = [
        'import importlib',
    ]

    init_template = """
    try:
        from ..records.types import ${object_name_upper}_RECORD_TYPES as _record_type_data_sets #pylint: disable=no-name-in-module
    except (ImportError, AttributeError):
        _record_type_data_sets = dict()
    _namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, osid_catalog_map, db_prefix='', runtime=None):
        self._my_map = osid_catalog_map
        self._runtime = runtime
        self._db_prefix = db_prefix
        self._records = dict()
        # This check is here for transition purposes:
        try:
            self._load_records(osid_catalog_map['recordTypeIds'])
        except KeyError:
            print 'KeyError: recordTypeIds key not found in ', self._my_map['displayName']['text']
            self._load_records([]) # In place for transition purposes

    # These next two private methods should be moved to osid.Extensible??? (I thought they were already)
    def _load_records(self, record_type_idstrs):
        for record_type_idstr in record_type_idstrs:
            self._init_record(record_type_idstr)

    def _init_record(self, record_type_idstr):
        record_type_data = self._record_type_data_sets[Id(record_type_idstr).get_identifier()]
        module = importlib.import_module(record_type_data['module_path'])
        record = getattr(module, record_type_data['object_record_class_name'])
        self._records[record_type_idstr] = record(self)
"""

class BinForm:

    import_statements_pattern = [
        '#from ..osid.objects import OsidForm',
        '#from ..osid.objects import OsidObjectForm',
    ]

    init_template = """
    try:
        from ..records.types import ${object_name_upper}_RECORD_TYPES as _record_type_data_sets #pylint: disable=no-name-in-module
    except (ImportError, AttributeError):
        _record_type_data_sets = dict()
    _namespace = '${implpkg_name}.${object_name}'

    def __init__(self, osid_catalog_map=None, record_types=None, db_prefix='', runtime=None, **kwargs):
        #from ..osid.objects import OsidForm
        osid_objects.OsidForm.__init__(self)
        self._runtime = runtime
        self._db_prefix = db_prefix
        self._kwargs = kwargs
        self._init_metadata(**kwargs)
        self._records = dict()
        if osid_catalog_map is not None:
            self._for_update = True
            self._my_map = osid_catalog_map
            self._load_records(osid_catalog_map['recordTypeIds'])
        else:
            self._my_map = {}
            self._for_update = False
            self._init_map(**kwargs)
            if record_types is not None:
                self._init_records(record_types)
        self._supported_record_type_ids = self._my_map['recordTypeIds']

    def _init_metadata(self, **kwargs):
        osid_objects.OsidObjectForm._init_metadata(self)

    def _init_map(self):
        #from ..osid.objects import OsidObjectForm
        osid_objects.OsidObjectForm._init_map(self)

    # These next three private methods should be moved to osid.Extensible??? (I thought they were already)
    def _load_records(self, record_type_idstrs):
        \"\"\"Load all records of record type for this catalog.\"\"\"
        for record_type_idstr in record_type_idstrs:
            self._init_record(record_type_idstr)

    def _init_records(self, record_types):
        \"\"\"Initalize all records for this catalog.\"\"\"
        for record_type in record_types:
            # This conditional was inserted on 7/11/14. It may prove problematic:
            if str(record_type) not in self._my_map['recordTypeIds']:
                self._init_record(str(record_type))
                self._my_map['recordTypeIds'].append(str(record_type))

    def _init_record(self, record_type_idstr):
        \"\"\"Initalize a record of record type.\"\"\"
        record_type_data = self._record_type_data_sets[Id(record_type_idstr).get_identifier()]
        module = importlib.import_module(record_type_data['module_path'])
        record = getattr(module, record_type_data['form_record_class_name'])
        self._records[record_type_idstr] = record(self)

"""
