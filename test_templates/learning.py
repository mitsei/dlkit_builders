
class ObjectiveRequisiteSession:

    import_statements_pattern = [
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.requisite_list = list()
    request.cls.requisite_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ObjectiveRequisiteSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)
        create_form = request.cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for ObjectiveRequisiteSession Lookup'
        create_form.description = 'Test Objective for ObjectiveRequisiteSession tests'
        request.cls.objective = request.cls.catalog.create_objective(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveRequisiteSession tests'
            obj = request.cls.catalog.create_objective(create_form)
            request.cls.requisite_list.append(obj)
            request.cls.requisite_ids.append(obj.ident)
            request.cls.catalog.assign_objective_requisite(request.cls.objective.ident, obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj_id in request.cls.requisite_ids:
                    catalog.delete_objective(obj_id)
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    get_requisite_objectives_template = """
        # From test_templates/learning.py::ObjectiveRequsiteSession::get_requisite_objectives_template
        if not is_never_authz(self.service_config):
            requisites = self.catalog.${method_name}(self.${object_name_under}.ident)
            assert requisites.available() == len(self.requisite_ids))
            for req in requisites:
                assert req.ident in self.requisite_ids
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id)"""

    get_dependent_objectives_template = """
        # From test_templates/learning.py::ObjectiveRequsiteSession::get_dependent_objectives_template
        if not is_never_authz(self.service_config):
            dependents = self.catalog.${method_name}(self.${object_name_under}.ident)
            assert dependents.available() == 0
            dependents = self.catalog.get_dependent_objectives(self.requisite_ids[0])
            assert dependents.available() == 1
            assert dependents.next().ident == self.objective.ident
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id)"""


class ObjectiveRequisiteAssignmentSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.${pkg_name_replaced_reserved} import objects as ABCObjects',
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.requisite_list = list()
    request.cls.requisite_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ObjectiveRequisiteAssignmentSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)
        create_form = request.cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for ObjectiveRequisiteAssignmentSession Lookup'
        create_form.description = 'Test Objective for ObjectiveRequisiteAssignmentSession tests'
        request.cls.objective = request.cls.catalog.create_objective(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveRequisiteAssignmentSession tests'
            obj = request.cls.catalog.create_objective(create_form)
            request.cls.requisite_list.append(obj)
            request.cls.requisite_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj_id in request.cls.requisite_ids:
                    catalog.delete_objective(obj_id)
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    assign_objective_requisite_template = """
        # From test_templates/learning.py::ObjectiveRequsiteAssignmentSession::assign_objective_requisite_template
        if not is_never_authz(self.service_config):
            results = self.catalog.get_requisite_${object_name_plural_under}(self.${object_name_under}.ident)
            assert isinstance(results, ABCObjects.${return_type})
            assert results.available() == 0

            self.catalog.${method_name}(self.${object_name_under}.ident, self.requisite_ids[0])

            results = self.catalog.get_requisite_${object_name_plural_under}(self.${object_name_under}.ident)
            assert results.available() == 1
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id, self.fake_id)"""

    unassign_objective_requisite_template = """
        # From test_templates/learning.py::ObjectiveRequsiteAssignmentSession::unassign_objective_requisite_template
        if not is_never_authz(self.service_config):
            self.catalog.assign_${object_name_under}_requisite(self.${object_name_under}.ident, self.requisite_ids[0])

            results = self.catalog.get_requisite_${object_name_plural_under}(self.${object_name_under}.ident)
            assert results.available() == 1

            self.catalog.${method_name}(self.${object_name_under}.ident, self.requisite_ids[0])

            results = self.catalog.get_requisite_${object_name_plural_under}(self.${object_name_under}.ident)
            assert results.available() == 0
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id, self.fake_id)"""


class ObjectiveHierarchyDesignSession:
    import_statements = [
        'from dlkit.abstract_osid.learning.objects import ObjectiveList'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ObjectiveHierarchyDesignSession tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)

    def setUp(self):
        self.child_list = list()
        self.child_ids = list()
        create_form = self.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for ObjectiveHierarchyDesignSession Lookup'
        create_form.description = 'Test Objective for ObjectiveHierarchyDesignSession tests'
        self.objective = self.catalog.create_objective(create_form)
        for num in [0, 1]:
            create_form = self.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveHierarchyDesignSession tests'
            obj = self.catalog.create_objective(create_form)
            self.child_list.append(obj)
            self.child_ids.append(obj.ident)
        self.session = self.catalog

    def tearDown(self):
        for obj_id in self.child_ids:
            self.catalog.delete_objective(obj_id)
        for obj in self.catalog.get_objectives():
            self.catalog.delete_objective(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""

    add_child_objective = """
        self.catalog.add_root_objective(self.objective.ident)

        with pytest.raises(errors.IllegalState):
            self.catalog.get_child_objectives(self.objective.ident)

        self.catalog.add_child_objective(self.objective.ident, self.child_ids[0])

        children = self.catalog.get_child_objectives(self.objective.ident)
        self.assertEqual(children.available(), 1)
        self.assertTrue(isinstance(children, ObjectiveList))"""

    add_root_objective = """
        roots = self.catalog.get_root_objectives()
        self.assertEqual(roots.available(), 0)
        self.assertTrue(isinstance(roots, ObjectiveList))

        self.catalog.add_root_objective(self.objective.ident)
        roots = self.catalog.get_root_objectives()
        self.assertEqual(roots.available(), 1)"""

    can_modify_objective_hierarchy = """
        self.assertTrue(isinstance(self.catalog.can_modify_objective_hierarchy(), bool))"""

    remove_child_objective = """
        self.catalog.add_root_objective(self.objective.ident)
        self.catalog.add_child_objective(self.objective.ident, self.child_ids[0])

        children = self.catalog.get_child_objectives(self.objective.ident)
        self.assertEqual(children.available(), 1)

        self.catalog.remove_child_objective(self.objective.ident, self.child_ids[0])

        with pytest.raises(errors.IllegalState):
            self.catalog.get_child_objectives(self.objective.ident)"""

    remove_child_objectives = """
        self.catalog.add_root_objective(self.objective.ident)
        self.catalog.add_child_objective(self.objective.ident, self.child_ids[0])
        self.catalog.add_child_objective(self.objective.ident, self.child_ids[1])

        children = self.catalog.get_child_objectives(self.objective.ident)
        self.assertEqual(children.available(), 2)

        self.catalog.remove_child_objectives(self.objective.ident)

        with pytest.raises(errors.IllegalState):
            self.catalog.get_child_objectives(self.objective.ident)"""

    remove_root_objective = """
        self.catalog.add_root_objective(self.objective.ident)

        roots = self.catalog.get_root_objectives()
        self.assertEqual(roots.available(), 1)

        self.catalog.remove_root_objective(self.objective.ident)

        roots = self.catalog.get_root_objectives()
        self.assertEqual(roots.available(), 0)"""


class ObjectiveHierarchySession:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.child_list = list()
        cls.child_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ObjectiveHierarchySession tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)

    def setUp(self):
        self.child_list = list()
        self.child_ids = list()
        create_form = self.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for ObjectiveHierarchySession Lookup'
        create_form.description = 'Test Objective for ObjectiveHierarchySession tests'
        self.objective = self.catalog.create_objective(create_form)
        self.catalog.add_root_objective(self.objective.ident)
        for num in [0, 1]:
            create_form = self.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveHierarchySession tests'
            obj = self.catalog.create_objective(create_form)
            self.child_list.append(obj)
            self.child_ids.append(obj.ident)
            self.catalog.add_child_objective(self.objective.ident, obj.ident)
        self.session = self.catalog

    def tearDown(self):
        for obj_id in self.child_ids:
            self.catalog.delete_objective(obj_id)
        for obj in self.catalog.get_objectives():
            self.catalog.delete_objective(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""

    get_child_objectives = """
        children = self.catalog.get_child_objectives(self.objective.ident)
        self.assertEqual(children.available(), 2)
        self.assertTrue(isinstance(children, ObjectiveList))
        self.assertEqual(str(children.next().ident),
                         str(self.child_ids[0]))
        self.assertEqual(str(children.next().ident),
                         str(self.child_ids[1]))"""

    get_root_objectives = """
        roots = self.catalog.get_root_objectives()
        self.assertEqual(roots.available(), 1)
        self.assertTrue(isinstance(roots, ObjectiveList))
        self.assertEqual(str(roots.next().ident),
                         str(self.objective.ident))"""


class ObjectiveAdminSession:

    import_statements_pattern = [
    ]

    delete_objective_template = """
        # From test_templates/learning.py::ObjectiveAdminSession::delete_objective_template
        results = self.catalog.get_${object_name_under}s()
        self.assertEqual(results.available(), 1)

        form = self.catalog.get_${object_name_under}_form_for_create([])
        form.display_name = 'new ${object_name}'
        form.description = 'description of ${object_name}'
        new_${object_name_under} = self.catalog.create_${object_name_under}(form)

        results = self.catalog.get_${object_name_under}s()
        self.assertEqual(results.available(), 2)

        self.session.${method_name}(new_${object_name_under}.ident)

        results = self.catalog.get_${object_name_under}s()
        self.assertEqual(results.available(), 1)
        self.assertNotEqual(str(results.next().ident),
                            str(new_${object_name_under}.ident))"""


class ObjectiveSequencingSession:
    import_statements_pattern = [
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.child_list = list()
        cls.child_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ObjectiveSequencingSession tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)

    def setUp(self):
        self.objective_list = list()
        for num in [0, 1]:
            create_form = self.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveSequencingSession tests'
            obj = self.catalog.create_objective(create_form)
            self.objective_list.append(obj)

        self.session = self.catalog

    def tearDown(self):
        for obj_id in self.child_ids:
            self.catalog.delete_objective(obj_id)
        for obj in self.catalog.get_objectives():
            self.catalog.delete_objective(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""


class ObjectiveNodeList:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ObjectiveNodeList tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)

        cls.objective_node_ids = list()

    def setUp(self):
        from dlkit.json_.learning.objects import ObjectiveNodeList, ObjectiveNode
        self.objective_node_list = list()
        for num in [0, 1]:
            create_form = self.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveNodeList tests'
            obj = self.catalog.create_objective(create_form)
            self.objective_node_list.append(ObjectiveNode(obj.object_map))
            self.objective_node_ids.append(obj.ident)
        # Not put the objectives in a hierarchy
        self.catalog.add_root_objective(self.objective_node_list[0].ident)
        self.catalog.add_child_objective(
            self.objective_node_list[0].ident,
            self.objective_node_list[1].ident)
        self.objective_node_list = ObjectiveNodeList(self.objective_node_list)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_objectives():
            cls.catalog.delete_objective(obj.ident)
        cls.svc_mgr.delete_objective_bank(cls.catalog.ident)"""


class ObjectiveNode:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ObjectiveNode tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)

    def setUp(self):
        from dlkit.json_.learning.objects import ObjectiveNode
        self.objective_node_list = list()
        for num in [0, 1]:
            create_form = self.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveNodeList tests'
            obj = self.catalog.create_objective(create_form)
            self.objective_node_list.append(ObjectiveNode(obj.object_map))
        # Now put the objectives in a hierarchy
        self.catalog.add_root_objective(self.objective_node_list[0].ident)
        self.catalog.add_child_objective(
            self.objective_node_list[0].ident,
            self.objective_node_list[1].ident)
        self.object = ObjectiveNode(self.objective_node_list[0])

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_objectives():
            cls.catalog.delete_objective(obj.ident)
        cls.svc_mgr.delete_objective_bank(cls.catalog.ident)"""


class ActivityLookupSession:
    import_statements = [
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.activity_list = list()
        cls.activity_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ActivityLookupSession tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)
        create_form = cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for Activity Lookup'
        create_form.description = 'Test Objective for ActivityLookupSession tests'
        cls.objective = cls.catalog.create_objective(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_activity_form_for_create(cls.objective.ident, [])
            create_form.display_name = 'Test Activity ' + str(num)
            create_form.description = 'Test Activity for ActivityLookupSession tests'
            obj = cls.catalog.create_activity(create_form)
            cls.activity_list.append(obj)
            cls.activity_ids.append(obj.ident)

    def setUp(self):
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_activities():
                catalog.delete_activity(obj.ident)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""

    get_activities_for_objective_template = """
        # From test_templates/learning.py::ActivityLookupSession::get_activities_for_objective_template
        results = self.session.${method_name}(self.${arg0_object_under}.ident)
        self.assertEqual(results.available(), 2)
        self.assertTrue(isinstance(results, ABCObjects.${return_type_list_object}List))"""


class ActivityObjectiveBankSession:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.activity_list = list()
        cls.activity_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ActivityObjectiveBankSession tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)

        create_form = cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for ActivIty Lookup'
        create_form.description = 'Test Objective for ActivityLookupSession tests'
        cls.objective = cls.catalog.create_objective(create_form)

        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank for Assignment'
        create_form.description = 'Test ObjectiveBank for ActivityObjectiveBankSession tests assignment'
        cls.assigned_catalog = cls.svc_mgr.create_objective_bank(create_form)
        for num in [0, 1, 2]:
            create_form = cls.catalog.get_activity_form_for_create(cls.objective.ident, [])
            create_form.display_name = 'Test Activity ' + str(num)
            create_form.description = 'Test Activity for ActivityObjectiveBankSession tests'
            obj = cls.catalog.create_activity(create_form)
            cls.activity_list.append(obj)
            cls.activity_ids.append(obj.ident)
        cls.svc_mgr.assign_activity_to_objective_bank(
            cls.activity_ids[1], cls.assigned_catalog.ident)
        cls.svc_mgr.assign_activity_to_objective_bank(
            cls.activity_ids[2], cls.assigned_catalog.ident)

    def setUp(self):
        self.session = self.svc_mgr

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.unassign_activity_from_objective_bank(
            cls.activity_ids[1], cls.assigned_catalog.ident)
        cls.svc_mgr.unassign_activity_from_objective_bank(
            cls.activity_ids[2], cls.assigned_catalog.ident)
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_activities():
                catalog.delete_activity(obj.ident)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""


class ActivityObjectiveBankAssignmentSession:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.activity_list = list()
        cls.activity_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ActivityObjectiveBankAssignmentSession tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank for Assignment'
        create_form.description = 'Test ObjectiveBank for ActivityObjectiveBankAssignmentSession tests assignment'
        cls.assigned_catalog = cls.svc_mgr.create_objective_bank(create_form)

        create_form = cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for Assignment'
        create_form.description = 'Test Objective for ActivityObjectiveBankAssignmentSession tests assignment'
        cls.objective = cls.catalog.create_objective(create_form)

        for num in [0, 1, 2]:
            create_form = cls.catalog.get_activity_form_for_create(cls.objective.ident, [])
            create_form.display_name = 'Test Activity ' + str(num)
            create_form.description = 'Test Activity for ActivityObjectiveBankAssignmentSession tests'
            obj = cls.catalog.create_activity(create_form)
            cls.activity_list.append(obj)
            cls.activity_ids.append(obj.ident)

    def setUp(self):
        self.session = self.svc_mgr

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_activities():
            cls.catalog.delete_activity(obj.ident)
        for obj in cls.catalog.get_objectives():
            cls.catalog.delete_objective(obj.ident)
        cls.svc_mgr.delete_objective_bank(cls.assigned_catalog.ident)
        cls.svc_mgr.delete_objective_bank(cls.catalog.ident)"""


class ActivityAdminSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid.objects import OsidForm',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.activity_list = list()
        cls.activity_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ActivityLookupSession tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)
        create_form = cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for Activity Lookup'
        create_form.description = 'Test Objective for ActivityLookupSession tests'
        cls.objective = cls.catalog.create_objective(create_form)
        cls.parent_object = cls.objective
        for num in [0, 1]:
            create_form = cls.catalog.get_activity_form_for_create(cls.objective.ident, [])
            create_form.display_name = 'Test Activity ' + str(num)
            create_form.description = 'Test Activity for ActivityLookupSession tests'
            obj = cls.catalog.create_activity(create_form)
            cls.activity_list.append(obj)
            cls.activity_ids.append(obj.ident)

        create_form = cls.catalog.get_activity_form_for_create(cls.objective.ident, [])
        create_form.display_name = 'new Activity'
        create_form.description = 'description of Activity'
        create_form.genus_type = NEW_TYPE
        cls.osid_object = cls.catalog.create_activity(create_form)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_activities():
                catalog.delete_activity(obj.ident)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""

    get_activity_form_for_create_template = """
        # From test_templates/learning.py::ActivityAdminSession::get_activity_form_for_create_template
        if not is_never_authz(self.service_config):
            form = self.catalog.${method_name}(self.parent_object.ident, [])
            assert isinstance(form, OsidForm)
            assert not form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id, [])"""

    delete_activity = """
        form = self.catalog.get_activity_form_for_create(self.parent_object.ident, [])
        form.display_name = 'new Activity'
        form.description = 'description of Activity'
        form.set_genus_type(NEW_TYPE)
        osid_object = self.catalog.create_activity(form)
        self.catalog.delete_activity(osid_object.ident)
        with pytest.raises(errors.NotFound):
            self.catalog.get_activity(osid_object.ident)"""


class Activity:

    import_statements_pattern = [
        'from dlkit.abstract_osid.${pkg_name_replaced_reserved} import objects as ABCObjects',
        'from dlkit.json_.id.objects import IdList',
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)

        form = cls.catalog.get_objective_form_for_create([])
        form.display_name = 'Objective'
        cls.objective = cls.catalog.create_objective(form)

        form = cls.catalog.get_activity_form_for_create(cls.objective.ident,
                                                        [])
        form.display_name = 'Test activity'
        cls.object = cls.catalog.create_activity(form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_activities():
            cls.catalog.delete_activity(obj.ident)
        cls.catalog.delete_objective(cls.objective.ident)
        cls.svc_mgr.delete_objective_bank(cls.catalog.ident)"""

    get_assessment_ids = """
        result = self.object.get_assessment_ids()
        self.assertTrue(isinstance(result, IdList))
        self.assertEqual(result.available(), 0)"""

    get_assessments = """
        with pytest.raises(errors.IllegalState):
            self.object.get_assessments()"""

    get_asset_ids_template = """
        # From test_templates/learning.py::Activity::get_asset_ids_template
        if not is_never_authz(self.service_config):
            result = self.object.${method_name}()
            assert isinstance(result, IdList)
            assert result.available() == 0"""

    get_assets_template = """
        # From test_templates/learning.py::Activity::get_assets_template
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.IllegalState):
                self.object.${method_name}()"""

    get_course_ids = """
        result = self.object.get_course_ids()
        self.assertTrue(isinstance(result, IdList))
        self.assertEqual(result.available(), 0)"""

    get_courses = """
        # We don't have the course service yet
        with pytest.raises(errors.IllegalState):
            self.object.get_courses()"""

    get_objective_template = """
        # From test_templates/learning.py::Activity::get_objective_template
        if not is_never_authz(self.service_config):
            result = self.object.${method_name}()
            assert isinstance(result, ABCObjects.${return_type})
            assert str(result.ident) == str(self.${return_type_under}.ident)"""

    get_objective_id_template = """
        # From test_templates/learning.py::Activity::get_objective_id_template
        if not is_never_authz(self.service_config):
            result = self.object.${method_name}()
            assert isinstance(result, Id)
            assert str(result) == str(self.${var_name}.ident)"""


class ActivityForm:
    import_statements_pattern = [
        'from dlkit.json_.osid.metadata import Metadata',
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        # From test_templates/learning.py::ActivityForm::init_template
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ActivityForm tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)
        create_form = cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for Activity Lookup'
        create_form.description = 'Test Objective for ActivityForm tests'
        cls.objective = cls.catalog.create_objective(create_form)

        cls.form = cls.catalog.get_activity_form_for_create(cls.objective.ident, [])

    @classmethod
    def tearDownClass(cls):
        # From test_templates/learning.py::ActivityForm::init_template
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_activities():
                catalog.delete_activity(obj.ident)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""

    get_assets_metadata_template = """
        # From test_templates/learning.py::ActivityForm::get_assets_metadata_template
        assert isinstance(self.form.${method_name}(), Metadata)"""

    set_assets_template = """
        # From test_templates/learning.py::ActivityForm::set_assets_template
        test_id = Id('osid.Osid%3A1%40ODL.MIT.EDU')
        self.form.${method_name}([test_id])
        assert len(self.form._my_map['${var_name_singular_mixed}Ids']) == 1
        assert self.form._my_map['${var_name_singular_mixed}Ids'][0] == str(test_id)
        with pytest.raises(errors.InvalidArgument):
            self.form.${method_name}('this is not a list')
        # reset this for other tests
        self.form._my_map['${var_name_singular_mixed}Ids'] = list()"""

    clear_assets_template = """
        # From test_templates/learning.py::ActivityForm::clear_assets_template
        test_id = Id('osid.Osid%3A1%40ODL.MIT.EDU')
        self.form.set_${var_name}([test_id])
        assert len(self.form._my_map['${var_name_singular_mixed}Ids']) == 1
        assert self.form._my_map['${var_name_singular_mixed}Ids'][0] == str(test_id)
        self.form.${method_name}()
        assert self.form._my_map['${var_name_singular_mixed}Ids'] == []"""


class ActivityList:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ActivityList tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)
        create_form = cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for Activity Lookup'
        create_form.description = 'Test Objective for ActivityList tests'
        cls.objective = cls.catalog.create_objective(create_form)

        cls.form = cls.catalog.get_activity_form_for_create(cls.objective.ident, [])

    def setUp(self):
        from dlkit.json_.learning.objects import ActivityList
        self.activity_list = list()
        self.activity_ids = list()
        for num in [0, 1]:
            form = self.catalog.get_activity_form_for_create(self.objective.ident, [])
            form.display_name = 'Test Activity ' + str(num)
            form.description = 'Test Activity for ActivityList tests'
            obj = self.catalog.create_activity(form)

            self.activity_list.append(obj)
            self.activity_ids.append(obj.ident)
        self.activity_list = ActivityList(self.activity_list)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_activities():
                catalog.delete_activity(obj.ident)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""


class ActivityQuery:
    import_statements = [
        'from dlkit.json_.learning.queries import ActivityQuery'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ActivityLookupSession tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)
        create_form = cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for Activity Lookup'
        create_form.description = 'Test Objective for ActivityLookupSession tests'
        cls.objective = cls.catalog.create_objective(create_form)

    def setUp(self):
        # Since the session isn't implemented, we just construct an ActivityQuery directly
        self.query = ActivityQuery(runtime=self.catalog._runtime)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_activities():
                catalog.delete_activity(obj.ident)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""


class ProficiencyQuerySession:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.proficiency_list = list()
        cls.proficiency_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ProficiencyQuerySession tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)

        form = cls.catalog.get_objective_form_for_create([])
        form.display_name = "Test LO"
        objective = cls.catalog.create_objective(form)

        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = cls.catalog.get_proficiency_form_for_create(objective.ident, AGENT_ID, [])
            create_form.display_name = 'Test Proficiency ' + color
            create_form.description = (
                'Test Proficiency for ProficiencyQuerySession tests, did I mention green')
            obj = cls.catalog.create_proficiency(create_form)
            cls.proficiency_list.append(obj)
            cls.proficiency_ids.append(obj.ident)

    def setUp(self):
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_proficiencies():
                catalog.delete_proficiency(obj.ident)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""


class ProficiencyLookupSession:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.proficiency_list = list()
        cls.proficiency_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ProficiencyLookupSession tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)

        form = cls.catalog.get_objective_form_for_create([])
        form.display_name = "Test LO"
        objective = cls.catalog.create_objective(form)

        for color in ['Orange', 'Blue']:
            create_form = cls.catalog.get_proficiency_form_for_create(objective.ident, AGENT_ID, [])
            create_form.display_name = 'Test Proficiency ' + color
            create_form.description = (
                'Test Proficiency for ProficiencyLookupSession tests, did I mention green')
            obj = cls.catalog.create_proficiency(create_form)
            cls.proficiency_list.append(obj)
            cls.proficiency_ids.append(obj.ident)

    def setUp(self):
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_proficiencies():
                catalog.delete_proficiency(obj.ident)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""


class ProficiencyForm:
    import_statements = [
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ProficiencyForm tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)

        form = cls.catalog.get_objective_form_for_create([])
        form.display_name = "Test LO"
        cls.objective = cls.catalog.create_objective(form)

    def setUp(self):
        self.form = self.catalog.get_proficiency_form_for_create(self.objective.ident, AGENT_ID, [])
        self.object = self.form

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_proficiencies():
                catalog.delete_proficiency(obj.ident)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""

    clear_completion = """
        self.form.set_completion(50.0)
        self.assertIsNotNone(self.form._my_map['completion'])
        self.form.clear_completion()
        self.assertIsNone(self.form._my_map['completion'])"""

    set_completion = """
        self.assertIsNone(self.form._my_map['completion'])
        self.form.set_completion(50.0)
        self.assertIsNotNone(self.form._my_map['completion'])"""

    clear_level = """
        self.form.set_level(Id('grading.Grade%3Afake%40ODL.MIT.EDU'))
        self.assertIsNotNone(self.form._my_map['level'])
        self.form.clear_level()
        self.assertEqual(self.form._my_map['level'], '')"""

    set_level = """
        # This is a slightly hokey test, because the spec seems to have a typo
        self.assertEqual(self.form._my_map['levelId'], '')
        self.form.set_level(Id('grading.Grade%3Afake%40ODL.MIT.EDU'))
        self.assertIsNotNone(self.form._my_map['level'])"""


class ProficiencyList:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ProficiencyList tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)

        form = cls.catalog.get_objective_form_for_create([])
        form.display_name = "Test LO"
        cls.objective = cls.catalog.create_objective(form)

        cls.form = cls.catalog.get_proficiency_form_for_create(cls.objective.ident, AGENT_ID, [])

    def setUp(self):
        from dlkit.json_.learning.objects import ProficiencyList
        self.proficiency_list = list()
        self.proficiency_ids = list()
        for num in [0, 1]:
            form = self.catalog.get_proficiency_form_for_create(self.objective.ident, AGENT_ID, [])
            form.display_name = 'Test Proficiency ' + str(num)
            form.description = 'Test Proficiency for ProficiencyList tests'
            obj = self.catalog.create_proficiency(form)

            self.proficiency_list.append(obj)
            self.proficiency_ids.append(obj.ident)
        self.proficiency_list = ProficiencyList(self.proficiency_list)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_proficiencies():
                catalog.delete_proficiency(obj.ident)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""


class Proficiency:
    import_statements = [
        'from dlkit.abstract_osid.learning.objects import Objective',
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.primordium.id.primitives import Id',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'AGENT_ID = Id(**{\'identifier\': \'jane_doe\', \'namespace\': \'osid.agent.Agent\', \'authority\': \'MIT-ODL\'})',
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)

        form = cls.catalog.get_objective_form_for_create([])
        form.display_name = 'Objective'
        cls.objective = cls.catalog.create_objective(form)

        form = cls.catalog.get_proficiency_form_for_create(cls.objective.ident,
                                                           AGENT_ID,
                                                           [])
        form.display_name = 'Test proficiency'
        cls.object = cls.catalog.create_proficiency(form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_proficiencies():
            cls.catalog.delete_proficiency(obj.ident)
        cls.catalog.delete_objective(cls.objective.ident)
        cls.svc_mgr.delete_objective_bank(cls.catalog.ident)"""

    get_completion = """
        score = self.object.get_completion()
        self.assertIsNone(score)

        # if this is set, should be a Decimal
        form = self.catalog.get_proficiency_form_for_create(self.objective.ident,
                                                            AGENT_ID,
                                                            [])
        form.set_completion(0.0)
        new_proficiency = self.catalog.create_proficiency(form)

        self.assertEqual(new_proficiency.get_completion(), 0.0)"""

    get_objective = """
        result = self.object.get_objective()
        self.assertTrue(isinstance(result, Objective))
        self.assertEqual(str(result.ident),
                         str(self.objective.ident))"""


class ProficiencyQuery:
    match_completion = """
        start = float(0.0)
        end = float(100.0)
        self.assertNotIn('completion', self.query._query_terms)
        self.query.match_completion(start, end, True)
        self.assertEqual(self.query._query_terms['completion'], {
            '$gte': start,
            '$lte': end
        })"""

    match_minimum_completion = """
        with pytest.raises(errors.Unimplemented):
            self.query.match_minimum_completion(float(50.0), True)"""


class ProficiencyAdminSession:
    import_statements_pattern = [
        'from dlkit.abstract_osid.osid.objects import OsidForm',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.proficiency_list = list()
        cls.proficiency_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ProficiencyLookupSession tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)

        form = cls.catalog.get_objective_form_for_create([])
        form.display_name = "Test LO"
        cls.objective = cls.catalog.create_objective(form)

        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = cls.catalog.get_proficiency_form_for_create(cls.objective.ident, AGENT_ID, [])
            create_form.display_name = 'Test Proficiency ' + color
            create_form.description = (
                'Test Proficiency for ProficiencyLookupSession tests, did I mention green')
            obj = cls.catalog.create_proficiency(create_form)
            cls.proficiency_list.append(obj)
            cls.proficiency_ids.append(obj.ident)

        create_form = cls.catalog.get_proficiency_form_for_create(cls.objective.ident, AGENT_ID, [])
        create_form.display_name = 'new Proficiency'
        create_form.description = 'description of Proficiency'
        create_form.genus_type = NEW_TYPE
        cls.osid_object = cls.catalog.create_proficiency(create_form)

    def setUp(self):
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_proficiencies():
                catalog.delete_proficiency(obj.ident)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""

    get_proficiency_form_for_create = """
        form = self.catalog.get_proficiency_form_for_create(self.objective.ident, AGENT_ID, [])
        self.assertTrue(isinstance(form, OsidForm))
        self.assertFalse(form.is_for_update())"""

    delete_proficiency = """
        create_form = self.catalog.get_proficiency_form_for_create(self.objective.ident, AGENT_ID, [])
        create_form.display_name = 'new Proficiency'
        create_form.description = 'description of Proficiency'
        create_form.genus_type = NEW_TYPE
        osid_object = self.catalog.create_proficiency(create_form)
        self.catalog.delete_proficiency(osid_object.ident)
        with pytest.raises(errors.NotFound):
            self.catalog.get_proficiency(osid_object.ident)"""


class ObjectiveBankQuery:
    import_statements = [
        'from dlkit.json_.learning.queries import ObjectiveBankQuery'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)
        cls.fake_id = Id('resource.Resource%3A1%40ODL.MIT.EDU')

    def setUp(self):
        # Since the session isn't implemented, we just construct an ObjectiveBankQuery directly
        self.query = ObjectiveBankQuery(runtime=self.catalog._runtime)

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_objective_bank(cls.catalog.ident)"""
