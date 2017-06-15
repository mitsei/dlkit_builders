
class ObjectiveRequisiteSession:

    import_statements_pattern = [
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.requisite_list = list()
        cls.requisite_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ObjectiveRequisiteSession tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)
        create_form = cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for ObjectiveRequisiteSession Lookup'
        create_form.description = 'Test Objective for ObjectiveRequisiteSession tests'
        cls.objective = cls.catalog.create_objective(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveRequisiteSession tests'
            obj = cls.catalog.create_objective(create_form)
            cls.requisite_list.append(obj)
            cls.requisite_ids.append(obj.ident)
            cls.catalog.assign_objective_requisite(cls.objective.ident, obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj_id in cls.requisite_ids:
                catalog.delete_objective(obj_id)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""

    get_requisite_objectives_template = """
        requisites = self.catalog.get_requisite_objectives(self.objective.ident)
        self.assertEqual(
            requisites.available(),
            len(self.requisite_ids)
        )
        for req in requisites:
            self.assertIn(
                req.ident,
                self.requisite_ids
            )"""

    get_dependent_objectives_template = """
        dependents = self.catalog.get_dependent_objectives(self.objective.ident)
        self.assertEqual(
            dependents.available(),
            0
        )
        dependents = self.catalog.get_dependent_objectives(self.requisite_ids[0])
        self.assertEqual(
            dependents.available(),
            1
        )
        self.assertEqual(
            dependents.next().ident,
            self.objective.ident
        )"""


class ObjectiveRequisiteAssignmentSession:

    import_statements_pattern = [
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.requisite_list = list()
        cls.requisite_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ObjectiveRequisiteAssignmentSession tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)
        create_form = cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for ObjectiveRequisiteAssignmentSession Lookup'
        create_form.description = 'Test Objective for ObjectiveRequisiteAssignmentSession tests'
        cls.objective = cls.catalog.create_objective(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveRequisiteAssignmentSession tests'
            obj = cls.catalog.create_objective(create_form)
            cls.requisite_list.append(obj)
            cls.requisite_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj_id in cls.requisite_ids:
                catalog.delete_objective(obj_id)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""

    assign_objective_requisite_template = """
        self.catalog.assign_objective_requisite(self.objective.ident, self.requisite_ids[0])"""


class ObjectiveHierarchyDesignSession:
    init = """
    def setUp(cls):
        cls.child_list = list()
        cls.child_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ObjectiveHierarchyDesignSession tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)
        create_form = cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for ObjectiveHierarchyDesignSession Lookup'
        create_form.description = 'Test Objective for ObjectiveHierarchyDesignSession tests'
        cls.objective = cls.catalog.create_objective(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveHierarchyDesignSession tests'
            obj = cls.catalog.create_objective(create_form)
            cls.child_list.append(obj)
            cls.child_ids.append(obj.ident)

    def tearDown(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj_id in cls.child_ids:
                catalog.delete_objective(obj_id)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""

    add_child_objective = """
        self.catalog.add_root_objective(self.objective.ident)
        self.catalog.add_child_objective(self.objective.ident, self.child_ids[0])"""

    add_root_objective = """
        self.catalog.add_root_objective(self.objective.ident)"""

    can_modify_objective_hierarchy = """
        self.assertTrue(self.catalog.can_modify_objective_hierarchy())"""

    remove_child_objective = """
        self.catalog.add_root_objective(self.objective.ident)
        self.catalog.add_child_objective(self.objective.ident, self.child_ids[0])
        self.catalog.remove_child_objective(self.objective.ident, self.child_ids[0])"""

    remove_child_objectives = """
        self.catalog.add_root_objective(self.objective.ident)
        self.catalog.add_child_objective(self.objective.ident, self.child_ids[0])
        self.catalog.add_child_objective(self.objective.ident, self.child_ids[1])
        self.catalog.remove_child_objectives(self.objective.ident)"""

    remove_root_objective = """
        self.catalog.add_root_objective(self.objective.ident)
        self.catalog.remove_root_objective(self.objective.ident)"""


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
        create_form = cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for ObjectiveHierarchySession Lookup'
        create_form.description = 'Test Objective for ObjectiveHierarchySession tests'
        cls.objective = cls.catalog.create_objective(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveHierarchySession tests'
            obj = cls.catalog.create_objective(create_form)
            cls.child_list.append(obj)
            cls.child_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj_id in cls.child_ids:
                catalog.delete_objective(obj_id)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""


class ObjectiveAdminSession:

    import_statements_pattern = [
    ]

    delete_objective_template = """"""


class ObjectiveSequencingSession:
    import_statements_pattern = [
    ]


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


class ActivityLookupSession:

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

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_activities():
                catalog.delete_activity(obj.ident)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""

    get_activities_for_objective_template = """"""


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

    get_activity_form_for_create = """
        form = self.catalog.get_activity_form_for_create(self.objective.ident, [])
        self.assertTrue(isinstance(form, OsidForm))
        self.assertFalse(form.is_for_update())"""

    delete_activity = """
        form = self.catalog.get_activity_form_for_create(self.objective.ident, [])
        form.display_name = 'new Activity'
        form.description = 'description of Activity'
        form.set_genus_type(NEW_TYPE)
        osid_object = self.catalog.create_activity(form)
        self.catalog.delete_activity(osid_object.ident)
        with self.assertRaises(errors.NotFound):
            self.catalog.get_activity(osid_object.ident)"""


class Activity:

    import_statements_pattern = [
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

    get_objective_id_template = """"""

    get_objective_template = """"""

    is_asset_based_activity_template = """"""

    get_asset_ids_template = """"""

    get_assets_template = """"""

    is_assessment_based_activity = """"""

    is_asset_based_activity = """"""

    is_course_based_activity = """"""


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
        self.assertTrue(isinstance(self.form.${method_name}(), Metadata))"""

    set_assets_template = """
        # From test_templates/learning.py::ActivityForm::set_assets_template
        test_id = Id('osid.Osid%3A1%40ODL.MIT.EDU')
        self.form.${method_name}([test_id])
        self.assertTrue(len(self.form._my_map['${var_name_singular_mixed}Ids']), 1)
        self.assertEqual(self.form._my_map['${var_name_singular_mixed}Ids'][0],
                         str(test_id))
        with self.assertRaises(errors.InvalidArgument):
            self.form.${method_name}('this is not a list')
        # reset this for other tests
        self.form._my_map['${var_name_singular_mixed}Ids'] = list()"""

    clear_assets_template = """
        # From test_templates/learning.py::ActivityForm::clear_assets_template
        test_id = Id('osid.Osid%3A1%40ODL.MIT.EDU')
        self.form.set_${var_name}([test_id])
        self.assertTrue(len(self.form._my_map['${var_name_singular_mixed}Ids']), 1)
        self.assertEqual(self.form._my_map['${var_name_singular_mixed}Ids'][0],
                         str(test_id))
        self.form.${method_name}()
        self.assertEqual(self.form._my_map['${var_name_singular_mixed}Ids'], [])"""


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

        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = cls.catalog.get_proficiency_form_for_create(objective.ident, AGENT_ID, [])
            create_form.display_name = 'Test Proficiency ' + color
            create_form.description = (
                'Test Proficiency for ProficiencyLookupSession tests, did I mention green')
            obj = cls.catalog.create_proficiency(create_form)
            cls.proficiency_list.append(obj)
            cls.proficiency_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_proficiencies():
                catalog.delete_proficiency(obj.ident)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""


class ProficiencyForm:
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
        objective = cls.catalog.create_objective(form)

        cls.form = cls.catalog.get_proficiency_form_for_create(objective.ident, AGENT_ID, [])

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_proficiencies():
                catalog.delete_proficiency(obj.ident)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)"""


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
        with self.assertRaises(errors.Unimplemented):
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
        with self.assertRaises(errors.NotFound):
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
