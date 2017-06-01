
class GradeSystemAdminSession:

    import_statements_pattern = [
    ]

    # override this until we create a more rigorous test that can send the gradesystem id arg

    can_create_grades = """"""

    can_create_grade_with_record_types = """"""

    can_update_grades = """"""

    can_delete_grades = """"""


class GradebookColumnLookupSession:
    # Until we figure out how to do Relationship init patterns properly:
    import_statements = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.json_.grading.objects import GradebookColumnSummary',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.primordium.id.primitives import Id',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'AGENT_ID = Id(**{\'identifier\': \'jane_doe\', \'namespace\': \'osid.agent.Agent\', \'authority\': \'MIT-ODL\'})',
    ]

    # Until we figure out how to do Relationship init patterns properly:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.grade_entry_list = list()
        cls.grade_entry_ids = list()
        cls.gradebook_column_list = list()
        cls.gradebook_column_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('GRADING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test Gradebook'
        create_form.description = 'Test Gradebook for GradebookColumnLookupSession tests'
        cls.catalog = cls.svc_mgr.create_gradebook(create_form)
        create_form = cls.catalog.get_grade_system_form_for_create([])
        create_form.display_name = 'Test Grade System'
        create_form.description = 'Test Grade System for GradebookColumnLookupSession tests'
        create_form.based_on_grades = False
        create_form.lowest_numeric_score = 0
        create_form.highest_numeric_score = 100
        create_form.numeric_score_increment = 1
        cls.grade_system = cls.catalog.create_grade_system(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_gradebook_column_form_for_create([])
            create_form.display_name = 'Test GradebookColumn ' + str(num)
            create_form.description = 'Test GradebookColumn for GradebookColumnLookupSession tests'
            create_form.grade_system = cls.grade_system.ident
            obj = cls.catalog.create_gradebook_column(create_form)
            cls.gradebook_column_list.append(obj)
            cls.gradebook_column_ids.append(obj.ident)
        for num in range(0, 100):
            create_form = cls.catalog.get_grade_entry_form_for_create(cls.gradebook_column_ids[0], AGENT_ID, [])
            create_form.display_name = 'Test GradeEntry ' + str(num)
            create_form.description = 'Test GradeEntry for GradebookColumnLookupSession tests'
            create_form.set_score(float(num))
            object = cls.catalog.create_grade_entry(create_form)
            cls.grade_entry_list.append(object)
            cls.grade_entry_ids.append(object.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_gradebooks():
            for obj in catalog.get_grade_entries():
                catalog.delete_grade_entry(obj.ident)
            for obj in catalog.get_gradebook_columns():
                catalog.delete_gradebook_column(obj.ident)
            for obj in catalog.get_grade_systems():
                catalog.delete_grade_system(obj.ident)
            cls.svc_mgr.delete_gradebook(catalog.ident)"""

    # skip this one until gradebook column summary is supported
    get_gradebook_column_summary = """
        self.assertTrue(isinstance(self.catalog.get_gradebook_column_summary(self.gradebook_column_ids[0]),
                                   GradebookColumnSummary))"""


class GradeEntryLookupSession:
    # Until we figure out how to do Relationship init patterns properly:
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

    # Until we figure out how to do Relationship init patterns properly:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.grade_entry_list = list()
        cls.grade_entry_ids = list()
        cls.gradebook_column_list = list()
        cls.gradebook_column_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('GRADING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test Gradebook'
        create_form.description = 'Test Gradebook for GradeEntryLookupSession tests'
        cls.catalog = cls.svc_mgr.create_gradebook(create_form)
        create_form = cls.catalog.get_grade_system_form_for_create([])
        create_form.display_name = 'Test Grade System'
        create_form.description = 'Test Grade System for GradeEntryLookupSession tests'
        create_form.based_on_grades = False
        create_form.lowest_numeric_score = 0
        create_form.highest_numeric_score = 5
        create_form.numeric_score_increment = 0.25
        cls.grade_system = cls.catalog.create_grade_system(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_gradebook_column_form_for_create([])
            create_form.display_name = 'Test GradebookColumn ' + str(num)
            create_form.description = 'Test GradebookColumn for GradeEntryLookupSession tests'
            create_form.grade_system = cls.grade_system.ident
            obj = cls.catalog.create_gradebook_column(create_form)
            cls.gradebook_column_list.append(obj)
            cls.gradebook_column_ids.append(obj.ident)
        for num in [0, 1]:
            create_form = cls.catalog.get_grade_entry_form_for_create(cls.gradebook_column_ids[num], AGENT_ID, [])
            create_form.display_name = 'Test GradeEntry ' + str(num)
            create_form.description = 'Test GradeEntry for GradeEntryLookupSession tests'
            object = cls.catalog.create_grade_entry(create_form)
            cls.grade_entry_list.append(object)
            cls.grade_entry_ids.append(object.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_gradebooks():
            for obj in catalog.get_grade_entries():
                catalog.delete_grade_entry(obj.ident)
            for obj in catalog.get_gradebook_columns():
                catalog.delete_gradebook_column(obj.ident)
            for obj in catalog.get_grade_systems():
                catalog.delete_grade_system(obj.ident)
            cls.svc_mgr.delete_gradebook(catalog.ident)"""


class GradeEntryQuerySession:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.grade_entry_list = list()
        cls.grade_entry_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('GRADING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test Gradebook'
        create_form.description = 'Test Gradebook for GradeEntryQuerySession tests'
        cls.catalog = cls.svc_mgr.create_gradebook(create_form)

        form = cls.catalog.get_grade_system_form_for_create([])
        form.display_name = 'Test grade system'
        grade_system = cls.catalog.create_grade_system(form)

        form = cls.catalog.get_gradebook_column_form_for_create([])
        form.display_name = 'Test gradebook column'
        form.set_grade_system(grade_system.ident)
        gradebook_column = cls.catalog.create_gradebook_column(form)

        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = cls.catalog.get_grade_entry_form_for_create(gradebook_column.ident, AGENT_ID, [])
            create_form.display_name = 'Test GradeEntry ' + color
            create_form.description = (
                'Test GradeEntry for GradeEntryQuerySession tests, did I mention green')
            obj = cls.catalog.create_grade_entry(create_form)
            cls.grade_entry_list.append(obj)
            cls.grade_entry_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_gradebooks():
            for obj in catalog.get_grade_entries():
                catalog.delete_grade_entry(obj.ident)
            for obj in catalog.get_gradebook_columns():
                catalog.delete_gradebook_column(obj.ident)
            for obj in catalog.get_grade_systems():
                catalog.delete_grade_system(obj.ident)
            cls.svc_mgr.delete_gradebook(catalog.ident)"""


class Grade:
    import_statements = [
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
    # This really shouldn't be generated...should be GradeEntry??
    @classmethod
    def setUpClass(cls):
        cls.object = None

    @classmethod
    def tearDownClass(cls):
        pass"""


class GradeForm:
    import_statements = [
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
    # This really shouldn't be generated...should be GradeEntryForm??
    @classmethod
    def setUpClass(cls):
        cls.object = None

    @classmethod
    def tearDownClass(cls):
        pass"""

    get_grade_form_record = """"""

    get_input_score_end_range_metadata = """"""

    get_input_score_start_range_metadata = """"""

    get_output_score_metadata = """"""


class GradeList:
    import_statements = [
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
    # This really shouldn't be generated...should be GradeEntryList??
    @classmethod
    def setUpClass(cls):
        cls.object = None

    @classmethod
    def tearDownClass(cls):
        pass"""

    get_next_grade = """"""

    get_next_grades = """"""


class GradeQuery:
    import_statements = [
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
    # This really shouldn't be generated...should be GradeEntryQuery??
    @classmethod
    def setUpClass(cls):
        cls.object = None

    @classmethod
    def tearDownClass(cls):
        pass"""

    match_grade_system_id = """"""

    clear_grade_system_id_terms = """"""

    clear_grade_system_terms = """"""

    clear_input_score_start_range_terms = """"""

    clear_input_score_end_range_terms = """"""

    clear_output_score_terms = """"""

    match_grade_entry_id = """"""

    clear_grade_entry_id_terms = """"""

    match_gradebook_id = """"""

    clear_gradebook_id_terms = """"""

    clear_gradebook_terms = """"""


class GradeEntry:
    import_statements = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.id.primitives import Id',
        'AGENT_ID = Id(**{\'identifier\': \'jane_doe\', \'namespace\': \'osid.agent.Agent\', \'authority\': \'MIT-ODL\'})',
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('GRADING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_gradebook(create_form)

        form = cls.catalog.get_grade_system_form_for_create([])
        form.display_name = 'Grade system'
        cls.grade_system = cls.catalog.create_grade_system(form)

        form = cls.catalog.get_gradebook_column_form_for_create([])
        form.display_name = 'Gradebook Column'
        form.set_grade_system(cls.grade_system.ident)
        cls.column = cls.catalog.create_gradebook_column(form)

        form = cls.catalog.get_grade_entry_form_for_create(
            cls.column.ident,
            AGENT_ID,
            [])
        form.display_name = 'Test object'
        cls.object = cls.catalog.create_grade_entry(form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_grade_entries():
            cls.catalog.delete_grade_entry(obj.ident)
        for obj in cls.catalog.get_gradebook_columns():
            cls.catalog.delete_gradebook_column(obj.ident)
        cls.catalog.delete_grade_system(cls.grade_system.ident)
        cls.svc_mgr.delete_gradebook(cls.catalog.ident)"""

    get_grading_agent = """"""

    get_grading_agent_id = """"""

    get_key_resource_id = """"""

    get_key_resource = """"""

    get_overridden_calculated_entry_id = """"""

    get_overridden_calculated_entry = """"""


class GradeEntryForm:
    import_statements = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.id.primitives import Id',
        'AGENT_ID = Id(**{\'identifier\': \'jane_doe\', \'namespace\': \'osid.agent.Agent\', \'authority\': \'MIT-ODL\'})',
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('GRADING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_gradebook(create_form)

        form = cls.catalog.get_grade_system_form_for_create([])
        form.display_name = 'Grade system'
        form.set_based_on_grades(True)
        cls.grade_system = cls.catalog.create_grade_system(form)

        form = cls.catalog.get_gradebook_column_form_for_create([])
        form.display_name = 'Gradebook Column'
        form.set_grade_system(cls.grade_system.ident)
        cls.column = cls.catalog.create_gradebook_column(form)

    def setUp(self):
        self.form = self.catalog.get_grade_entry_form_for_create(
            self.column.ident,
            AGENT_ID,
            [])

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_grade_entries():
            cls.catalog.delete_grade_entry(obj.ident)
        for obj in cls.catalog.get_gradebook_columns():
            cls.catalog.delete_gradebook_column(obj.ident)
        cls.catalog.delete_grade_system(cls.grade_system.ident)
        cls.svc_mgr.delete_gradebook(cls.catalog.ident)"""

    set_ignored_for_calculations = """
        self.form.set_ignored_for_calculations(True)
        self.assertTrue(self.form._my_map['ignoredForCalculations'])"""

    clear_grade = """
        # Normally this would follow ResourceForm.clear_avatar_template
        # Except we need a valid ``grade`` for the initial ``set_grade`` to
        #   work, so we provide a hand-written impl here.
        self.form._my_map['gradeId'] = 'repository.Asset%3Afake-id%40ODL.MIT.EDU'
        self.assertEqual(self.form._my_map['gradeId'],
                         'repository.Asset%3Afake-id%40ODL.MIT.EDU')
        self.form.clear_grade()
        self.assertEqual(self.form._my_map['gradeId'], '')"""

    set_grade = """"""  # Need to figure out how to set valid grades in the grade system


class GradeEntryList:
    import_statements = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.id.primitives import Id',
        'AGENT_ID = Id(**{\'identifier\': \'jane_doe\', \'namespace\': \'osid.agent.Agent\', \'authority\': \'MIT-ODL\'})',
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('GRADING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_gradebook(create_form)

        form = cls.catalog.get_grade_system_form_for_create([])
        form.display_name = 'Grade system'
        form.set_based_on_grades(True)
        cls.grade_system = cls.catalog.create_grade_system(form)

        form = cls.catalog.get_gradebook_column_form_for_create([])
        form.display_name = 'Gradebook Column'
        form.set_grade_system(cls.grade_system.ident)
        cls.column = cls.catalog.create_gradebook_column(form)

    def setUp(self):
        from dlkit.json_.grading.objects import GradeEntryList
        self.grade_entry_list = list()
        self.grade_entry_ids = list()

        for num in [0, 1]:
            form = self.catalog.get_grade_entry_form_for_create(
                self.column.ident,
                AGENT_ID,
                [])

            obj = self.catalog.create_grade_entry(form)

            self.grade_entry_list.append(obj)
            self.grade_entry_ids.append(obj.ident)
        self.grade_entry_list = GradeEntryList(self.grade_entry_list)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_grade_entries():
            cls.catalog.delete_grade_entry(obj.ident)
        for obj in cls.catalog.get_gradebook_columns():
            cls.catalog.delete_gradebook_column(obj.ident)
        cls.catalog.delete_grade_system(cls.grade_system.ident)
        cls.svc_mgr.delete_gradebook(cls.catalog.ident)"""


class GradebookColumnSummary:
    import_statements = [
        'from dlkit.json_.grading.objects import GradebookColumn',
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.id.primitives import Id',
        'AGENT_ID = Id(**{\'identifier\': \'jane_doe\', \'namespace\': \'osid.agent.Agent\', \'authority\': \'MIT-ODL\'})',
    ]

    # Until we figure out how to do Relationship init patterns properly:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.grade_entry_list = list()
        cls.grade_entry_ids = list()
        cls.gradebook_column_list = list()
        cls.gradebook_column_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('GRADING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test Gradebook'
        create_form.description = 'Test Gradebook for GradebookColumnLookupSession tests'
        cls.catalog = cls.svc_mgr.create_gradebook(create_form)
        create_form = cls.catalog.get_grade_system_form_for_create([])
        create_form.display_name = 'Test Grade System'
        create_form.description = 'Test Grade System for GradebookColumnLookupSession tests'
        create_form.based_on_grades = False
        create_form.lowest_numeric_score = 0
        create_form.highest_numeric_score = 100
        create_form.numeric_score_increment = 1
        cls.grade_system = cls.catalog.create_grade_system(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_gradebook_column_form_for_create([])
            create_form.display_name = 'Test GradebookColumn ' + str(num)
            create_form.description = 'Test GradebookColumn for GradebookColumnLookupSession tests'
            create_form.grade_system = cls.grade_system.ident
            obj = cls.catalog.create_gradebook_column(create_form)
            cls.gradebook_column_list.append(obj)
            cls.gradebook_column_ids.append(obj.ident)
        for num in range(0, 100):
            create_form = cls.catalog.get_grade_entry_form_for_create(cls.gradebook_column_ids[0], AGENT_ID, [])
            create_form.display_name = 'Test GradeEntry ' + str(num)
            create_form.description = 'Test GradeEntry for GradebookColumnLookupSession tests'
            create_form.set_score(float(num))
            object = cls.catalog.create_grade_entry(create_form)
            cls.grade_entry_list.append(object)
            cls.grade_entry_ids.append(object.ident)
        cls.object = cls.catalog.get_gradebook_column_summary(cls.gradebook_column_ids[0])

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_gradebooks():
            for obj in catalog.get_grade_entries():
                catalog.delete_grade_entry(obj.ident)
            for obj in catalog.get_gradebook_columns():
                catalog.delete_gradebook_column(obj.ident)
            for obj in catalog.get_grade_systems():
                catalog.delete_grade_system(obj.ident)
            cls.svc_mgr.delete_gradebook(catalog.ident)"""

    get_gradebook_column_id = """
        self.assertTrue(isinstance(self.object.get_gradebook_column_id(), Id))
        self.assertEqual(str(self.object.get_gradebook_column_id()),
                         str(self.gradebook_column_ids[0]))"""

    get_gradebook_column = """
        self.assertTrue(isinstance(self.object.get_gradebook_column(), GradebookColumn))
        self.assertEqual(str(self.object.get_gradebook_column().ident),
                         str(self.gradebook_column_ids[0]))"""

    get_mean = """
        self.assertTrue(isinstance(self.object.get_mean(), Decimal))
        self.assertEqual(self.object.get_mean(), Decimal(49.5))"""

    get_median = """
        self.assertTrue(isinstance(self.object.get_median(), Decimal))
        self.assertEqual(self.object.get_median(), Decimal(49.5))"""

    get_rms = """
        self.assertTrue(isinstance(self.object.get_rms(), Decimal))
        self.assertEqual(self.object.get_rms(), Decimal('57.30183243143276652887614453'))"""

    get_standard_deviation = """
        self.assertTrue(isinstance(self.object.get_standard_deviation(), Decimal))
        self.assertEqual(self.object.get_standard_deviation(), Decimal('28.86607004772211800433171979'))"""

    get_sum = """
        self.assertTrue(isinstance(self.object.get_sum(), Decimal))
        self.assertEqual(self.object.get_sum(), Decimal('4950'))"""


class GradeEntryAdminSession:
    import_statements_pattern = [
        'from dlkit.abstract_osid.osid.objects import OsidForm',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.grade_entry_list = list()
        cls.grade_entry_ids = list()
        cls.gradebook_column_list = list()
        cls.gradebook_column_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('GRADING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test Gradebook'
        create_form.description = 'Test Gradebook for GradeEntryLookupSession tests'
        cls.catalog = cls.svc_mgr.create_gradebook(create_form)
        create_form = cls.catalog.get_grade_system_form_for_create([])
        create_form.display_name = 'Test Grade System'
        create_form.description = 'Test Grade System for GradeEntryLookupSession tests'
        create_form.based_on_grades = False
        create_form.lowest_numeric_score = 0
        create_form.highest_numeric_score = 5
        create_form.numeric_score_increment = 0.25
        cls.grade_system = cls.catalog.create_grade_system(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_gradebook_column_form_for_create([])
            create_form.display_name = 'Test GradebookColumn ' + str(num)
            create_form.description = 'Test GradebookColumn for GradeEntryLookupSession tests'
            create_form.grade_system = cls.grade_system.ident
            obj = cls.catalog.create_gradebook_column(create_form)
            cls.gradebook_column_list.append(obj)
            cls.gradebook_column_ids.append(obj.ident)
        for num in [0, 1]:
            create_form = cls.catalog.get_grade_entry_form_for_create(cls.gradebook_column_ids[num], AGENT_ID, [])
            create_form.display_name = 'Test GradeEntry ' + str(num)
            create_form.description = 'Test GradeEntry for GradeEntryLookupSession tests'
            object = cls.catalog.create_grade_entry(create_form)
            cls.grade_entry_list.append(object)
            cls.grade_entry_ids.append(object.ident)

        create_form = cls.catalog.get_grade_entry_form_for_create(cls.gradebook_column_ids[0], AGENT_ID, [])
        create_form.display_name = 'new GradeEntry'
        create_form.description = 'description of GradeEntry'
        create_form.genus_type = NEW_TYPE
        cls.osid_object = cls.catalog.create_grade_entry(create_form)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_gradebooks():
            for obj in catalog.get_grade_entries():
                catalog.delete_grade_entry(obj.ident)
            for obj in catalog.get_gradebook_columns():
                catalog.delete_gradebook_column(obj.ident)
            for obj in catalog.get_grade_systems():
                catalog.delete_grade_system(obj.ident)
            cls.svc_mgr.delete_gradebook(catalog.ident)"""

    get_grade_entry_form_for_create = """
        form = self.catalog.get_grade_entry_form_for_create(self.gradebook_column_ids[0], AGENT_ID, [])
        self.assertTrue(isinstance(form, OsidForm))
        self.assertFalse(form.is_for_update())"""

    delete_grade_entry = """
        create_form = self.catalog.get_grade_entry_form_for_create(self.gradebook_column_ids[0], AGENT_ID, [])
        create_form.display_name = 'new GradeEntry'
        create_form.description = 'description of GradeEntry'
        create_form.genus_type = NEW_TYPE
        osid_object = self.catalog.create_grade_entry(create_form)
        self.catalog.delete_grade_entry(osid_object.ident)
        with self.assertRaises(errors.NotFound):
            self.catalog.get_grade_entry(osid_object.ident)"""


class GradebookNodeList:

    import_statements_pattern = [
    ]

    init_template = """"""

    get_next_gradebook_node = """"""

    get_next_gradebook_nodes = """"""


class GradebookNode:
    init = """"""

    get_gradebook = """"""

    get_parent_gradebook_nodes = """"""

    get_child_gradebook_nodes = """"""
