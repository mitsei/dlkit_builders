
class AssessmentAuthoringManager:
    """Tests for AssessmentAuthoringManager"""
    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for assessment.authoring manager tests'
        catalog = cls.svc_mgr.create_bank(create_form)
        cls.catalog_id = catalog.get_id()
        cls.mgr = Runtime().get_manager('ASSESSMENT_AUTHORING', 'TEST_MONGO_1', (3, 0, 0))

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_bank(cls.catalog_id)
"""

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

    @classmethod
    def tearDownClass(cls):
        #for obj in cls.catalog.get_assessment_parts():
        #    cls.catalog.delete_assessment_part(obj.ident)
        #for catalog in cls.catalogs:
        #    cls.svc_mgr.delete_bank(catalog.ident)
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
        self.assertEqual(self.assessment_part_list[0].get_assessment().object_map,
                         self.assessment.object_map)
"""

    get_bank_id = """
        # this should not be here...
        pass"""