
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
        cls.mgr = Runtime().get_manager('ASSESSMENT_AUTHORING', 'TEST_JSON_1', (3, 0, 0))

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
        cls.mgr = Runtime().get_manager('ASSESSMENT_AUTHORING', 'TEST_JSON_1', (3, 0, 0))

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_bank(cls.catalog_id)"""


class AssessmentPartLookupSession:

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


class AssessmentPartItemDesignSession:

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

        cls.assessment = cls.catalog.get_assessment(cls.assessment.ident)

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


class SequenceRuleLookupSession:
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
        assessment_part_1 = cls.catalog.create_assessment_part_for_assessment(create_form)

        create_form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 2'
        create_form.description = 'Test Assessment Part for SequenceRuleLookupSession tests'
        assessment_part_2 = cls.catalog.create_assessment_part_for_assessment(create_form)

        for num in [0, 1]:
            create_form = cls.catalog.get_sequence_rule_form_for_create(assessment_part_1.ident,
                                                                        assessment_part_2.ident,
                                                                        [])
            create_form.display_name = 'Test Sequence Rule ' + str(num)
            create_form.description = 'Test Sequence Rule for SequenceRuleLookupSession tests'
            obj = cls.catalog.create_sequence_rule(create_form)
            cls.sequence_rule_list.append(obj)
            cls.sequence_rule_ids.append(obj.ident)

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


class SequenceRuleForm:
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

        cls.form = cls.catalog.get_sequence_rule_form_for_create(cls.assessment_part_1.ident,
                                                                 cls.assessment_part_2.ident,
                                                                 [])

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_banks():
            for obj in catalog.get_assessment_parts():
                catalog.delete_assessment_part(obj.ident)
            for obj in catalog.get_assessments():
                catalog.delete_assessment(obj.ident)
            cls.svc_mgr.delete_bank(catalog.ident)"""

    set_cumulative = """
        create_form = self.catalog.get_sequence_rule_form_for_create(self.assessment_part_1.ident,
                                                                     self.assessment_part_2.ident,
                                                                     [])
        create_form.set_cumulative(True)
        self.assertTrue(create_form._my_map['cumulative'])"""


    get_applied_assessment_parts_metadata = """"""


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
    init = """"""

    is_section = """"""


class AssessmentPartForm:
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

        cls.form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident,
                                                                                  [])

        cls.assessment = cls.catalog.get_assessment(cls.assessment.ident)

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

        # cls.query = cls.catalog.get_assessment_part_query()

    @classmethod
    def tearDownClass(cls):
        cls.catalog.use_unsequestered_assessment_part_view()
        cls.catalog.delete_assessment(cls.assessment.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""


class AssessmentPartAdminSession:
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

        form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident, [])
        form.display_name = 'new AssessmentPart'
        form.description = 'description of AssessmentPart'
        form.set_genus_type(NEW_TYPE)
        cls.osid_object = cls.catalog.create_assessment_part_for_assessment(form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessment_parts():
            cls.catalog.delete_assessment_part(obj.ident)
        for obj in cls.catalog.get_assessments():
            cls.catalog.delete_assessment(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    get_assessment_part_form_for_create_for_assessment = """"""

    get_assessment_part_form_for_create_for_assessment_part = """"""

    create_assessment_part_for_assessment = """"""

    create_assessment_part_for_assessment_part = """"""

    delete_assessment_part = """"""

    update_assessment_part = """"""


class SequenceRule:
    init = """"""

    is_cumulative = """"""
