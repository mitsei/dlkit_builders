
class AssessmentAuthoringManager:
    """Tests for AssessmentAuthoringManager"""
    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for assessment.authoring manager tests'
        catalog = cls.svc_mgr.create_bank(create_form)
        cls.catalog_id = catalog.get_id()
        # cls.mgr = Runtime().get_manager('ASSESSMENT_AUTHORING', 'TEST_JSON_1', (3, 0, 0))

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_bank(cls.catalog_id)"""


class AssessmentAuthoringProxyManager:
    """Tests for AssessmentAuthoringProxyManager"""
    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for assessment.authoring manager tests'
        catalog = cls.svc_mgr.create_bank(create_form)
        cls.catalog_id = catalog.get_id()
        # cls.mgr = Runtime().get_manager('ASSESSMENT_AUTHORING', 'TEST_JSON_1', (3, 0, 0))

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_bank(cls.catalog_id)"""


class AssessmentPartLookupSession:
    import_statements = [
        'from dlkit.abstract_osid.assessment_authoring import objects as ABCObjects'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.assessment_part_list = list()
        cls.assessment_part_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPartLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        assessment_form = cls.catalog.get_assessment_form_for_create([])
        assessment_form.display_name = 'Test Assessment'
        assessment_form.description = 'Test Assessment for AssessmentPartLookupSession tests'
        cls.assessment = cls.catalog.create_assessment(assessment_form)

        for num in [0, 1, 2, 3]:
            create_form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident,
                                                                                         [])
            create_form.display_name = 'Test AssessmentPart ' + str(num)
            create_form.description = 'Test AssessmentPart for AssessmentPartLookupSession tests'
            if num > 1:
                create_form.sequestered = True
            obj = cls.catalog.create_assessment_part_for_assessment(create_form)
            cls.assessment_part_list.append(obj)
            cls.assessment_part_ids.append(obj.ident)

        cls.assessment = cls.catalog.get_assessment(cls.assessment.ident)

    def setUp(self):
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        cls.catalog.use_unsequestered_assessment_part_view()
        for obj in cls.catalog.get_assessment_parts():
            cls.catalog.delete_assessment_part(obj.ident)
        cls.catalog.delete_assessment(cls.assessment.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)

    def test_get_assessment_id(self):
        \"\"\"tests get_assessment_id\"\"\"
        self.assertEqual(str(self.assessment_part_list[0].get_assessment_id()),
                         str(self.assessment.ident))

    def test_get_assessment(self):
        \"\"\"tests get_assessment\"\"\"
        def check_equal(val1, val2):
            self.assertEqual(val1, val2)

        def check_dict_equal(dict1, dict2):
            for item in dict1.items():
                key = item[0]
                value = item[1]
                if isinstance(value, dict):
                    check_dict_equal(value, dict2[key])
                else:
                    check_equal(value, dict2[key])

        check_dict_equal(self.assessment_part_list[0].get_assessment().object_map,
                         self.assessment.object_map)"""

    get_bank_id = """
        # this should not be here...
        pass"""


class AssessmentPartQuerySession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.assessment_part_list = list()
        cls.assessment_part_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPartLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        assessment_form = cls.catalog.get_assessment_form_for_create([])
        assessment_form.display_name = 'Test Assessment'
        assessment_form.description = 'Test Assessment for AssessmentPartLookupSession tests'
        cls.assessment = cls.catalog.create_assessment(assessment_form)

        colors = ['Orange', 'Blue', 'Green', 'orange']

        for num in [0, 1, 2, 3]:
            create_form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident,
                                                                                         [])
            create_form.display_name = 'Test AssessmentPart ' + str(num) + colors[num]
            create_form.description = 'Test AssessmentPart for AssessmentPartLookupSession tests'
            obj = cls.catalog.create_assessment_part_for_assessment(create_form)
            cls.assessment_part_list.append(obj)
            cls.assessment_part_ids.append(obj.ident)

        cls.assessment = cls.catalog.get_assessment(cls.assessment.ident)

    def setUp(self):
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        cls.catalog.use_unsequestered_assessment_part_view()
        for obj in cls.catalog.get_assessment_parts():
            cls.catalog.delete_assessment_part(obj.ident)
        cls.catalog.delete_assessment(cls.assessment.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""


class AssessmentPartItemSession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.item_list = list()
        cls.item_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT_AUTHORING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPartItemSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssetCompositionSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        create_form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part'
        create_form.description = 'Test Assessment Part for AssetCompositionSession tests'
        cls.assessment_part = cls.catalog.create_assessment_part_for_assessment(create_form)
        for num in [0, 1, 2, 3]:
            create_form = cls.catalog.get_item_form_for_create([])
            create_form.display_name = 'Test Item ' + str(num)
            create_form.description = 'Test Item for AssessmentPartItemSession tests'
            obj = cls.catalog.create_item(create_form)
            cls.item_list.append(obj)
            cls.item_ids.append(obj.ident)
            cls.catalog.add_item(obj.ident, cls.assessment_part.ident)

    def setUp(self):
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_banks():
            for obj in catalog.get_assessment_parts():
                if obj.has_children():
                    for child_id in obj.get_child_assessment_part_ids():
                        catalog.delete_assessment_part(child_id)
                catalog.delete_assessment_part(obj.ident)
            for obj in catalog.get_assessments():
                catalog.delete_assessment(obj.ident)
            for obj in catalog.get_items():
                catalog.delete_item(obj.ident)
            cls.svc_mgr.delete_bank(catalog.ident)"""

    can_access_assessment_part_items = """
        self.assertTrue(isinstance(self.session.can_access_assessment_part_items(), bool))"""


class AssessmentPartItemDesignSession:
    import_statements = [
        'from random import shuffle'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.item_list = list()
        cls.item_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT_AUTHORING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPartItemDesignSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentPartItemDesignSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        create_form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part'
        create_form.description = 'Test Assessment Part for AssessmentPartItemDesignSession tests'
        cls.assessment_part = cls.catalog.create_assessment_part_for_assessment(create_form)
        for num in [0, 1, 2, 3]:
            create_form = cls.catalog.get_item_form_for_create([])
            create_form.display_name = 'Test Item ' + str(num)
            create_form.description = 'Test Item for AssessmentPartItemDesignSession tests'
            obj = cls.catalog.create_item(create_form)
            cls.item_list.append(obj)
            cls.item_ids.append(obj.ident)
            cls.catalog.add_item(obj.ident, cls.assessment_part.ident)

        cls.assessment = cls.catalog.get_assessment(cls.assessment.ident)

    def setUp(self):
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_banks():
            for obj in catalog.get_assessment_parts():
                catalog.delete_assessment_part(obj.ident)
            for obj in catalog.get_assessments():
                catalog.delete_assessment(obj.ident)
            for obj in catalog.get_items():
                catalog.delete_item(obj.ident)
            cls.svc_mgr.delete_bank(catalog.ident)"""

    add_item = """
        self.assertEqual(self.catalog.get_assessment_part_items(self.assessment_part.ident).available(), 4)

        create_form = self.catalog.get_item_form_for_create([])
        create_form.display_name = 'Test Item 5'
        create_form.description = 'Test Item for AssessmentPartItemDesignSession tests'
        obj = self.catalog.create_item(create_form)
        self.session.add_item(obj.ident, self.assessment_part.ident)

        self.assertEqual(self.catalog.get_assessment_part_items(self.assessment_part.ident).available(), 5)"""

    can_design_assessment_parts = """
        self.assertTrue(isinstance(self.session.can_design_assessment_parts(), bool))"""

    move_item_ahead = """
        original_item_order = list(self.catalog.get_assessment_part_items(self.assessment_part.ident))
        original_ids = [item.ident for item in original_item_order]
        self.session.move_item_ahead(original_ids[-1],
                                     self.assessment_part.ident,
                                     original_ids[0])
        expected_order = [original_ids[-1]] + original_ids[0:-1]
        new_order = [item.ident for item in self.catalog.get_assessment_part_items(self.assessment_part.ident)]
        self.assertEqual(new_order, expected_order)"""

    move_item_behind = """
        original_item_order = list(self.catalog.get_assessment_part_items(self.assessment_part.ident))
        original_ids = [item.ident for item in original_item_order]
        self.session.move_item_behind(original_ids[0],
                                      self.assessment_part.ident,
                                      original_ids[-1])
        expected_order = original_ids[1::] + [original_ids[0]]
        new_order = [item.ident for item in self.catalog.get_assessment_part_items(self.assessment_part.ident)]
        self.assertEqual(new_order, expected_order)"""

    order_items = """
        original_item_order = list(self.catalog.get_assessment_part_items(self.assessment_part.ident))
        original_ids = [item.ident for item in original_item_order]
        shuffle(original_ids)
        self.session.order_items(original_ids,
                                 self.assessment_part.ident)
        new_order = [item.ident for item in self.catalog.get_assessment_part_items(self.assessment_part.ident)]
        self.assertEqual(new_order, original_ids)"""

    remove_item = """
        original_item_order = list(self.catalog.get_assessment_part_items(self.assessment_part.ident))
        original_ids = [item.ident for item in original_item_order]
        self.session.remove_item(original_ids[0],
                                 self.assessment_part.ident)
        new_order = [item.ident for item in self.catalog.get_assessment_part_items(self.assessment_part.ident)]
        self.assertEqual(new_order, original_ids[1::])"""


class SequenceRuleLookupSession:
    import_statements = [
        'from dlkit.primordium.type.primitives import Type',
        'SIMPLE_SEQUENCE_RECORD_TYPE = Type(**{"authority": "ODL.MIT.EDU", "namespace": "osid-object", "identifier": "simple-child-sequencing"})'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.sequence_rule_list = list()
        cls.sequence_rule_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for SequenceRuleLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        create_form = cls.catalog.get_assessment_form_for_create([SIMPLE_SEQUENCE_RECORD_TYPE])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for SequenceRuleLookupSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        create_form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 1'
        create_form.description = 'Test Assessment Part for SequenceRuleLookupSession tests'
        cls.assessment_part_1 = cls.catalog.create_assessment_part_for_assessment(create_form)

        create_form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 2'
        create_form.description = 'Test Assessment Part for SequenceRuleLookupSession tests'
        assessment_part_2 = cls.catalog.create_assessment_part_for_assessment(create_form)

        for num in [0, 1]:
            create_form = cls.catalog.get_sequence_rule_form_for_create(cls.assessment_part_1.ident,
                                                                        assessment_part_2.ident,
                                                                        [])
            create_form.display_name = 'Test Sequence Rule ' + str(num)
            create_form.description = 'Test Sequence Rule for SequenceRuleLookupSession tests'
            obj = cls.catalog.create_sequence_rule(create_form)
            cls.sequence_rule_list.append(obj)
            cls.sequence_rule_ids.append(obj.ident)

    def setUp(self):
        self.session = self.catalog
        self.assessment_part = self.assessment_part_1

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_banks():
            for obj in catalog.get_sequence_rules():
                catalog.delete_sequence_rule(obj.ident)
            for obj in catalog.get_assessment_parts():
                catalog.delete_assessment_part(obj.ident)
            for obj in catalog.get_assessments():
                catalog.delete_assessment(obj.ident)
            cls.svc_mgr.delete_bank(catalog.ident)"""


class SequenceRule:
    import_statements = [
        'from dlkit.abstract_osid.assessment_authoring.objects import AssessmentPart',
        'from dlkit.json_.id.objects import IdList',
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.sequence_rule_list = list()
        cls.sequence_rule_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for SequenceRule tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for SequenceRule tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        create_form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 1'
        create_form.description = 'Test Assessment Part for SequenceRule tests'
        cls.assessment_part_1 = cls.catalog.create_assessment_part_for_assessment(create_form)

        create_form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 2'
        create_form.description = 'Test Assessment Part for SequenceRule tests'
        cls.assessment_part_2 = cls.catalog.create_assessment_part_for_assessment(create_form)

    def setUp(self):
        form = self.catalog.get_sequence_rule_form_for_create(self.assessment_part_1.ident,
                                                              self.assessment_part_2.ident,
                                                              [])
        self.object = self.catalog.create_sequence_rule(form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessment_parts():
            cls.catalog.delete_assessment_part(obj.ident)
        for obj in cls.catalog.get_assessments():
            cls.catalog.delete_assessment(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    get_applied_assessment_part_ids = """
        result = self.object.get_applied_assessment_part_ids()
        self.assertTrue(isinstance(result, IdList))
        self.assertEqual(result.available(), 0)"""

    get_assessment_part = """
        part = self.object.get_assessment_part()
        self.assertTrue(isinstance(part, AssessmentPart))
        self.assertEqual(str(part.ident),
                         str(self.assessment_part_1.ident))"""

    get_assessment_part_id = """
        part_id = self.object.get_assessment_part_id()
        self.assertTrue(isinstance(part_id, Id))
        self.assertEqual(str(part_id),
                         str(self.assessment_part_1.ident))"""


class SequenceRuleForm:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.sequence_rule_list = list()
        cls.sequence_rule_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for SequenceRuleForm tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for SequenceRuleForm tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        create_form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 1'
        create_form.description = 'Test Assessment Part for SequenceRuleForm tests'
        cls.assessment_part_1 = cls.catalog.create_assessment_part_for_assessment(create_form)

        create_form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 2'
        create_form.description = 'Test Assessment Part for SequenceRuleForm tests'
        cls.assessment_part_2 = cls.catalog.create_assessment_part_for_assessment(create_form)

    def setUp(self):
        self.form = self.catalog.get_sequence_rule_form_for_create(self.assessment_part_1.ident,
                                                                   self.assessment_part_2.ident,
                                                                   [])
        self.object = self.form

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessment_parts():
            cls.catalog.delete_assessment_part(obj.ident)
        for obj in cls.catalog.get_assessments():
            cls.catalog.delete_assessment(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    set_cumulative = """
        create_form = self.catalog.get_sequence_rule_form_for_create(self.assessment_part_1.ident,
                                                                     self.assessment_part_2.ident,
                                                                     [])
        create_form.set_cumulative(True)
        self.assertTrue(create_form._my_map['cumulative'])"""

    get_applied_assessment_parts_metadata = """"""


class SequenceRuleList:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.sequence_rule_list = list()
        cls.sequence_rule_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for SequenceRuleList tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for SequenceRuleList tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        create_form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 1'
        create_form.description = 'Test Assessment Part for SequenceRuleList tests'
        cls.assessment_part_1 = cls.catalog.create_assessment_part_for_assessment(create_form)

        create_form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 2'
        create_form.description = 'Test Assessment Part for SequenceRuleList tests'
        cls.assessment_part_2 = cls.catalog.create_assessment_part_for_assessment(create_form)

        cls.form = cls.catalog.get_sequence_rule_form_for_create(cls.assessment_part_1.ident,
                                                                 cls.assessment_part_2.ident,
                                                                 [])

    def setUp(self):
        from dlkit.json_.assessment_authoring.objects import SequenceRuleList
        self.sequence_rule_list = list()
        self.sequence_rule_ids = list()

        for num in [0, 1]:
            form = self.catalog.get_sequence_rule_form_for_create(self.assessment_part_1.ident,
                                                                  self.assessment_part_2.ident,
                                                                  [])
            obj = self.catalog.create_sequence_rule(form)

            self.sequence_rule_list.append(obj)
            self.sequence_rule_ids.append(obj.ident)
        self.sequence_rule_list = SequenceRuleList(self.sequence_rule_list)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_sequence_rules():
            cls.catalog.delete_sequence_rule(obj.ident)
        for obj in cls.catalog.get_assessments():
            cls.catalog.delete_assessment(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""


class SequenceRuleQuery:
    import_statements = [
        'from dlkit.json_.assessment_authoring.queries import SequenceRuleQuery'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for SequenceRuleQuery tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

    def setUp(self):
        # Since the session isn't implemented, we just construct an SequenceRuleQuery directly
        self.query = SequenceRuleQuery(runtime=self.catalog._runtime)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_sequence_rules():
            cls.catalog.delete_sequence_rule(obj.ident)
        for obj in cls.catalog.get_assessments():
            cls.catalog.delete_assessment(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""


class SequenceRuleAdminSession:
    import_statements = [
        'from dlkit.abstract_osid.osid.objects import OsidForm',
        'from dlkit.abstract_osid.osid import errors',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})',
        'NEW_TYPE_2 = Type(**{\'identifier\': \'NEW 2\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.sequence_rule_list = list()
        cls.sequence_rule_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for SequenceRuleLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for SequenceRuleLookupSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        create_form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 1'
        create_form.description = 'Test Assessment Part for SequenceRuleLookupSession tests'
        cls.assessment_part_1 = cls.catalog.create_assessment_part_for_assessment(create_form)

        create_form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 2'
        create_form.description = 'Test Assessment Part for SequenceRuleLookupSession tests'
        cls.assessment_part_2 = cls.catalog.create_assessment_part_for_assessment(create_form)

        for num in [0, 1]:
            create_form = cls.catalog.get_sequence_rule_form_for_create(cls.assessment_part_1.ident,
                                                                        cls.assessment_part_2.ident,
                                                                        [])
            create_form.display_name = 'Test Sequence Rule ' + str(num)
            create_form.description = 'Test Sequence Rule for SequenceRuleLookupSession tests'
            obj = cls.catalog.create_sequence_rule(create_form)
            cls.sequence_rule_list.append(obj)
            cls.sequence_rule_ids.append(obj.ident)

        create_form = cls.catalog.get_sequence_rule_form_for_create(cls.assessment_part_1.ident,
                                                                    cls.assessment_part_2.ident,
                                                                    [])
        create_form.display_name = 'new SequenceRule'
        create_form.description = 'description of SequenceRule'
        create_form.genus_type = NEW_TYPE
        cls.osid_object = cls.catalog.create_sequence_rule(create_form)

    def setUp(self):
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_sequence_rules():
            cls.catalog.delete_sequence_rule(obj.ident)
        for obj in cls.catalog.get_assessment_parts():
            cls.catalog.delete_assessment_part(obj.ident)
        for obj in cls.catalog.get_assessments():
            cls.catalog.delete_assessment(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    get_sequence_rule_form_for_create = """
        form = self.catalog.get_sequence_rule_form_for_create(self.assessment_part_1.ident,
                                                              self.assessment_part_2.ident,
                                                              [])
        self.assertTrue(isinstance(form, OsidForm))
        self.assertFalse(form.is_for_update())"""

    delete_sequence_rule = """
        create_form = self.catalog.get_sequence_rule_form_for_create(self.assessment_part_1.ident,
                                                                     self.assessment_part_2.ident,
                                                                     [])
        create_form.display_name = 'new SequenceRule'
        create_form.description = 'description of SequenceRule'
        create_form.genus_type = NEW_TYPE
        osid_object = self.catalog.create_sequence_rule(create_form)
        self.catalog.delete_sequence_rule(osid_object.ident)
        with self.assertRaises(errors.NotFound):
            self.catalog.get_sequence_rule(osid_object.ident)"""


class AssessmentPart:
    import_statements = [
        'from dlkit.abstract_osid.assessment.objects import Assessment',
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.json_.id.objects import IdList',
        'SIMPLE_SEQUENCE_RECORD_TYPE = Type(**{"authority": "ODL.MIT.EDU", "namespace": "osid-object", "identifier": "simple-child-sequencing"})'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.assessment_part_list = list()
        cls.assessment_part_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPart tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        assessment_form = cls.catalog.get_assessment_form_for_create([])
        assessment_form.display_name = 'Test Assessment'
        assessment_form.description = 'Test Assessment for AssessmentPart tests'
        cls.assessment = cls.catalog.create_assessment(assessment_form)

    def setUp(self):
        form = self.catalog.get_assessment_part_form_for_create_for_assessment(self.assessment.ident,
                                                                               [])
        self.object = self.catalog.create_assessment_part_for_assessment(form)
        self.assessment = self.catalog.get_assessment(self.assessment.ident)

    def tearDown(self):
        for assessment_part in self.catalog.get_assessment_parts_for_assessment(self.assessment.ident):
            if assessment_part.has_children():
                for child_id in assessment_part.get_child_ids():
                    try:
                        self.catalog.delete_assessment_part(child_id)
                    except errors.NotFound:
                        pass
            self.catalog.delete_assessment_part(assessment_part.ident)

    @classmethod
    def tearDownClass(cls):
        cls.catalog.use_unsequestered_assessment_part_view()
        cls.catalog.delete_assessment(cls.assessment.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    get_assessment = """
        result = self.object.get_assessment()
        self.assertTrue(isinstance(result, Assessment))
        self.assertEqual(str(result.ident),
                         str(self.assessment.ident))"""

    get_assessment_id = """
        result_id = self.object.get_assessment_id()
        self.assertTrue(isinstance(result_id, Id))
        self.assertEqual(str(result_id),
                         str(self.assessment.ident))"""

    get_assessment_part = """
        with self.assertRaises(errors.IllegalState):
            self.object.get_assessment_part()"""

    get_assessment_part_id = """
        with self.assertRaises(errors.IllegalState):
            self.object.get_assessment_part_id()"""

    get_child_assessment_part_ids = """
        with self.assertRaises(errors.IllegalState):
            self.object.get_child_assessment_part_ids()

        # to get these back, need to have a simple sequencing part as the parent
        form = self.catalog.get_assessment_part_form_for_create_for_assessment(self.assessment.ident,
                                                                               [SIMPLE_SEQUENCE_RECORD_TYPE])
        form.set_children([Id('assessment.Part%3A000000000000000000000000%40ODL.MIT.EDU')])
        parent_part = self.catalog.create_assessment_part_for_assessment(form)

        results = parent_part.get_child_assessment_part_ids()
        self.assertTrue(isinstance(results, IdList))
        self.assertEqual(results.available(), 1)
        self.assertEqual(str(results.next()),
                         'assessment.Part%3A000000000000000000000000%40ODL.MIT.EDU')"""

    get_child_assessment_parts = """
        with self.assertRaises(errors.IllegalState):
            self.object.get_child_assessment_parts()

        # to get these back, need to have a simple sequencing part as the parent

        form = self.catalog.get_assessment_part_form_for_create_for_assessment(self.assessment.ident,
                                                                               [SIMPLE_SEQUENCE_RECORD_TYPE])
        parent_part = self.catalog.create_assessment_part_for_assessment(form)

        form = self.catalog.get_assessment_part_form_for_create_for_assessment_part(parent_part.ident,
                                                                                    [])
        child_part = self.catalog.create_assessment_part_for_assessment(form)

        parent_part = self.catalog.get_assessment_part(parent_part.ident)

        results = parent_part.get_child_assessment_part_ids()
        self.assertTrue(isinstance(results, IdList))
        self.assertEqual(results.available(), 1)
        self.assertEqual(str(results.next()),
                         str(child_part.ident))"""

    has_parent_part = """
        self.assertTrue(isinstance(self.object.has_parent_part(), bool))"""


class AssessmentPartForm:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.assessment_part_list = list()
        cls.assessment_part_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPartForm tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        assessment_form = cls.catalog.get_assessment_form_for_create([])
        assessment_form.display_name = 'Test Assessment'
        assessment_form.description = 'Test Assessment for AssessmentPartForm tests'
        cls.assessment = cls.catalog.create_assessment(assessment_form)

    def setUp(self):
        self.form = self.catalog.get_assessment_part_form_for_create_for_assessment(self.assessment.ident,
                                                                                    [])
        self.object = self.form
        self.assessment = self.catalog.get_assessment(self.assessment.ident)

    @classmethod
    def tearDownClass(cls):
        cls.catalog.use_unsequestered_assessment_part_view()
        cls.catalog.delete_assessment(cls.assessment.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""


class AssessmentPartList:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.assessment_part_list = list()
        cls.assessment_part_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPartList tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        assessment_form = cls.catalog.get_assessment_form_for_create([])
        assessment_form.display_name = 'Test Assessment'
        assessment_form.description = 'Test Assessment for AssessmentPartList tests'
        cls.assessment = cls.catalog.create_assessment(assessment_form)

        cls.form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident,
                                                                                  [])

    def setUp(self):
        from dlkit.json_.assessment_authoring.objects import AssessmentPartList
        self.assessment_part_list = list()
        self.assessment_part_ids = list()

        for num in [0, 1]:
            form = self.catalog.get_assessment_part_form_for_create_for_assessment(self.assessment.ident, [])

            obj = self.catalog.create_assessment_part_for_assessment(form)

            self.assessment_part_list.append(obj)
            self.assessment_part_ids.append(obj.ident)
        self.assessment_part_list = AssessmentPartList(self.assessment_part_list)

    @classmethod
    def tearDownClass(cls):
        cls.catalog.use_unsequestered_assessment_part_view()
        cls.catalog.delete_assessment(cls.assessment.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""


class AssessmentPartQuery:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.assessment_part_list = list()
        cls.assessment_part_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPartLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        assessment_form = cls.catalog.get_assessment_form_for_create([])
        assessment_form.display_name = 'Test Assessment'
        assessment_form.description = 'Test Assessment for AssessmentPartLookupSession tests'
        cls.assessment = cls.catalog.create_assessment(assessment_form)

    def setUp(self):
        self.query = self.catalog.get_assessment_part_query()

    @classmethod
    def tearDownClass(cls):
        cls.catalog.use_unsequestered_assessment_part_view()
        cls.catalog.delete_assessment(cls.assessment.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""


class AssessmentPartAdminSession:
    import_statements = [
        'from dlkit.abstract_osid.assessment_authoring import objects as ABCObjects',
        'from dlkit.primordium.type.primitives import Type',
        'SIMPLE_SEQUENCE_RECORD_TYPE = Type(**{"authority": "ODL.MIT.EDU", "namespace": "osid-object", "identifier": "simple-child-sequencing"})'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPartAdminSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        assessment_form = cls.catalog.get_assessment_form_for_create([])
        assessment_form.display_name = 'Test Assessment'
        assessment_form.description = 'Test Assessment for AssessmentPartAdminSession tests'
        cls.assessment = cls.catalog.create_assessment(assessment_form)

    def setUp(self):
        form = self.catalog.get_assessment_part_form_for_create_for_assessment(self.assessment.ident,
                                                                               [SIMPLE_SEQUENCE_RECORD_TYPE])
        form.display_name = 'new AssessmentPart'
        form.description = 'description of AssessmentPart'
        form.set_genus_type(NEW_TYPE)
        self.osid_object = self.catalog.create_assessment_part_for_assessment(form)
        self.session = self.catalog

    def tearDown(self):
        self.osid_object = self.catalog.get_assessment_part(self.osid_object.ident)
        if self.osid_object.has_children():
            for child_id in self.osid_object.get_child_assessment_part_ids():
                self.catalog.delete_assessment_part(child_id)
        self.catalog.delete_assessment_part(self.osid_object.ident)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessment_parts():
            cls.catalog.delete_assessment_part(obj.ident)
        for obj in cls.catalog.get_assessments():
            cls.catalog.delete_assessment(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    delete_assessment_part = """
        results = self.catalog.get_assessment_parts()
        self.assertEqual(results.available(), 1)

        form = self.catalog.get_assessment_part_form_for_create_for_assessment(self.assessment.ident,
                                                                               [])
        form.display_name = 'new AssessmentPart'
        form.description = 'description of AssessmentPart'
        new_assessment_part = self.catalog.create_assessment_part_for_assessment(form)

        results = self.catalog.get_assessment_parts()
        self.assertEqual(results.available(), 2)

        self.session.delete_assessment_part(new_assessment_part.ident)

        results = self.catalog.get_assessment_parts()
        self.assertEqual(results.available(), 1)
        self.assertNotEqual(str(results.next().ident),
                            str(new_assessment_part.ident))"""

    get_assessment_part_form_for_create_for_assessment = """
        form = self.session.get_assessment_part_form_for_create_for_assessment(self.assessment.ident, [])
        self.assertTrue(isinstance(form, ABCObjects.AssessmentPartForm))
        self.assertFalse(form.is_for_update())"""

    get_assessment_part_form_for_create_for_assessment_part = """
        form = self.session.get_assessment_part_form_for_create_for_assessment_part(self.osid_object.ident, [])
        self.assertTrue(isinstance(form, ABCObjects.AssessmentPartForm))
        self.assertFalse(form.is_for_update())"""

    update_assessment_part = """
        form = self.catalog.get_assessment_part_form_for_update(self.osid_object.ident)
        form.display_name = 'new name'
        form.description = 'new description'
        form.set_genus_type(NEW_TYPE_2)
        updated_object = self.catalog.update_assessment_part(self.osid_object.ident, form)
        self.assertTrue(isinstance(updated_object, ABCObjects.AssessmentPart))
        self.assertEqual(updated_object.ident, self.osid_object.ident)
        self.assertEqual(updated_object.display_name.text, 'new name')
        self.assertEqual(updated_object.description.text, 'new description')
        self.assertEqual(updated_object.genus_type, NEW_TYPE_2)"""

    create_assessment_part_for_assessment = """
        from dlkit.abstract_osid.assessment_authoring.objects import AssessmentPart
        self.assertTrue(isinstance(self.osid_object, AssessmentPart))
        self.assertEqual(self.osid_object.display_name.text, 'new AssessmentPart')
        self.assertEqual(self.osid_object.description.text, 'description of AssessmentPart')
        self.assertEqual(self.osid_object.genus_type, NEW_TYPE)

        form = self.catalog.get_assessment_part_form_for_create_for_assessment_part(self.osid_object.ident, [])
        form.display_name = 'new AssessmentPart child'
        form.description = 'description of AssessmentPart child'
        child_part = self.catalog.create_assessment_part_for_assessment_part(form)

        parent_part = self.catalog.get_assessment_part(self.osid_object.ident)
        self.assertTrue(parent_part.has_children())
        self.assertEqual(parent_part.get_child_assessment_part_ids().available(), 1)
        self.assertEqual(str(parent_part.get_child_assessment_part_ids().next()),
                         str(child_part.ident))"""
