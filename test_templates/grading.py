class GradeSystem:
    import_statements = [
        'from dlkit.abstract_osid.grading.objects import GradeList',
        'from dlkit.json_.id.objects import IdList'
    ]

    get_grade_ids = """
        grade_ids = self.object.get_grade_ids()
        self.assertTrue(isinstance(grade_ids, IdList))
        self.assertEqual(grade_ids.available(), 0)"""

    get_grades = """
        grades = self.object.get_grades()
        self.assertTrue(isinstance(grades, GradeList))
        self.assertEqual(grades.available(), 0)"""

    get_highest_numeric_score = """
        score = self.object.get_highest_numeric_score()
        self.assertIsNone(score)

        # if this is set, should be a Decimal
        form = self.catalog.get_grade_system_form_for_create([])
        form.set_highest_numeric_score(100.0)
        new_grade_system = self.catalog.create_grade_system(form)

        self.assertEqual(new_grade_system.get_highest_numeric_score(), 100.0)"""

    get_lowest_numeric_score = """
        score = self.object.get_lowest_numeric_score()
        self.assertIsNone(score)

        # if this is set, should be a Decimal
        form = self.catalog.get_grade_system_form_for_create([])
        form.set_lowest_numeric_score(0.0)
        new_grade_system = self.catalog.create_grade_system(form)

        self.assertEqual(new_grade_system.get_lowest_numeric_score(), 0.0)"""

    get_numeric_score_increment = """
        score = self.object.get_numeric_score_increment()
        self.assertIsNone(score)

        # if this is set, should be a Decimal
        form = self.catalog.get_grade_system_form_for_create([])
        form.set_numeric_score_increment(1.0)
        new_grade_system = self.catalog.create_grade_system(form)

        self.assertEqual(new_grade_system.get_numeric_score_increment(), 1.0)"""

    is_based_on_grades = """
        # when not set on create, returns None
        self.assertIsNone(self.object.is_based_on_grades())

        form = self.catalog.get_grade_system_form_for_create([])
        form.set_based_on_grades(True)
        new_grade_system = self.catalog.create_grade_system(form)

        self.assertTrue(new_grade_system.is_based_on_grades())"""


class GradeSystemForm:
    import_statements = [
        'from dlkit.abstract_osid.grading.objects import GradeList',
        'from dlkit.json_.id.objects import IdList'
    ]

    clear_highest_numeric_score = """
        self.form.set_highest_numeric_score(100.0)
        self.assertIsNotNone(self.form._my_map['highestNumericScore'])
        self.form.clear_highest_numeric_score()
        self.assertIsNone(self.form._my_map['highestNumericScore'])"""

    clear_lowest_numeric_score = """
        self.form.set_lowest_numeric_score(100.0)
        self.assertIsNotNone(self.form._my_map['lowestNumericScore'])
        self.form.clear_lowest_numeric_score()
        self.assertIsNone(self.form._my_map['lowestNumericScore'])"""

    clear_numeric_score_increment = """
        self.form.set_numeric_score_increment(100.0)
        self.assertIsNotNone(self.form._my_map['numericScoreIncrement'])
        self.form.clear_numeric_score_increment()
        self.assertIsNone(self.form._my_map['numericScoreIncrement'])"""

    clear_based_on_grades = """
        self.form.set_based_on_grades(True)
        self.assertIsNotNone(self.form._my_map['basedOnGrades'])
        self.form.clear_based_on_grades()
        self.assertIsNone(self.form._my_map['basedOnGrades'])"""

    set_highest_numeric_score = """
        self.assertIsNone(self.form._my_map['highestNumericScore'])
        self.form.set_highest_numeric_score(100.0)
        self.assertIsNotNone(self.form._my_map['highestNumericScore'])"""

    set_lowest_numeric_score = """
        self.assertIsNone(self.form._my_map['lowestNumericScore'])
        self.form.set_lowest_numeric_score(100.0)
        self.assertIsNotNone(self.form._my_map['lowestNumericScore'])"""

    set_numeric_score_increment = """
        self.assertIsNone(self.form._my_map['numericScoreIncrement'])
        self.form.set_numeric_score_increment(100.0)
        self.assertIsNotNone(self.form._my_map['numericScoreIncrement'])"""

    set_based_on_grades = """
        self.assertIsNone(self.form._my_map['basedOnGrades'])
        self.form.set_based_on_grades(True)
        self.assertIsNotNone(self.form._my_map['basedOnGrades'])"""


class GradebookColumn:
    import_statements = [
        'from dlkit.abstract_osid.grading.objects import GradeSystem',
        'from dlkit.abstract_osid.authentication.objects import Agent',
        'from dlkit.primordium.calendaring.primitives import DateTime',
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

    def setUp(self):
        form = self.catalog.get_gradebook_column_form_for_create([])
        form.display_name = 'Gradebook Column'
        form.set_grade_system(self.grade_system.ident)
        self.object = self.catalog.create_gradebook_column(form)

    def tearDown(self):
        for gradebook_column in self.catalog.get_gradebook_columns():
            self.catalog.delete_gradebook_column(gradebook_column.ident)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_grade_entries():
            cls.catalog.delete_grade_entry(obj.ident)
        for obj in cls.catalog.get_gradebook_columns():
            cls.catalog.delete_gradebook_column(obj.ident)
        cls.catalog.delete_grade_system(cls.grade_system.ident)
        cls.svc_mgr.delete_gradebook(cls.catalog.ident)"""

    get_grade_system = """
        grade_system = self.object.get_grade_system()
        self.assertTrue(isinstance(grade_system, GradeSystem))
        self.assertTrue(str(grade_system.ident),
                        str(self.grade_system.ident))"""

    get_grade_system_id = """
        grade_system_id = self.object.get_grade_system_id()
        self.assertTrue(isinstance(grade_system_id, Id))
        self.assertTrue(str(grade_system_id),
                        str(self.grade_system.ident))"""


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

    def setUp(self):
        self.session = self.catalog

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

    def setUp(self):
        self.session = self.catalog

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

    get_grade_entries_for_gradebook_column_on_date = """
        end_date = DateTime.utcnow() + datetime.timedelta(days=5)
        end_date = DateTime(**{
            'year': end_date.year,
            'month': end_date.month,
            'day': end_date.day,
            'hour': end_date.hour,
            'minute': end_date.minute,
            'second': end_date.second,
            'microsecond': end_date.microsecond
        })
        results = self.session.get_grade_entries_for_gradebook_column_on_date(self.gradebook_column_ids[0],
                                                                              DateTime.utcnow(),
                                                                              end_date)
        self.assertTrue(isinstance(results, ABCObjects.GradeEntryList))
        self.assertEqual(results.available(), 1)"""


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

    def setUp(self):
        self.session = self.catalog

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
        'from dlkit.abstract_osid.grading import objects as ABCObjects',
        'from dlkit.primordium.id.primitives import Id'
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

    def setUp(self):
        form = self.catalog.get_grade_form_for_create(
            self.grade_system.ident,
            [])
        form.display_name = 'Test object'
        self.object = self.catalog.create_grade(form)

    def tearDown(self):
        for grade in self.grade_system.get_grades():
            self.catalog.delete_grade(grade.ident)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_grade_entries():
            cls.catalog.delete_grade_entry(obj.ident)
        for obj in cls.catalog.get_gradebook_columns():
            cls.catalog.delete_gradebook_column(obj.ident)
        cls.catalog.delete_grade_system(cls.grade_system.ident)
        cls.svc_mgr.delete_gradebook(cls.catalog.ident)"""

    get_grade_system = """
        grade_system = self.object.get_grade_system()
        self.assertTrue(isinstance(grade_system, ABCObjects.GradeSystem))
        self.assertEqual(str(grade_system.ident),
                         str(self.grade_system.ident))"""

    get_grade_system_id = """
        grade_system_id = self.object.get_grade_system_id()
        self.assertTrue(isinstance(grade_system_id, Id))
        self.assertEqual(str(grade_system_id),
                         str(self.grade_system.ident))"""

    get_input_score_end_range = """
        end_range = self.object.get_input_score_end_range()
        self.assertIsNone(end_range)

        # if this is set, should be a Decimal
        form = self.catalog.get_grade_form_for_create(
            self.grade_system.ident,
            [])
        form.set_input_score_end_range(50.0)
        new_grade = self.catalog.create_grade(form)

        self.assertEqual(new_grade.get_input_score_end_range(), 50.0)"""

    get_input_score_start_range = """
        start_range = self.object.get_input_score_end_range()
        self.assertIsNone(start_range)

        # if this is set, should be a Decimal
        form = self.catalog.get_grade_form_for_create(
            self.grade_system.ident,
            [])
        form.set_input_score_start_range(50.0)
        new_grade = self.catalog.create_grade(form)

        self.assertEqual(new_grade.get_input_score_start_range(), 50.0)"""

    get_output_score = """
        score = self.object.get_output_score()
        self.assertIsNone(score)

        # if this is set, should be a Decimal
        form = self.catalog.get_grade_form_for_create(
            self.grade_system.ident,
            [])
        form.set_output_score(50.0)
        new_grade = self.catalog.create_grade(form)

        self.assertEqual(new_grade.get_output_score(), 50.0)"""


class GradeForm:
    import_statements = [
        'from dlkit.primordium.id.primitives import Id'
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

    def setUp(self):
        self.form = self.catalog.get_grade_form_for_create(
            self.grade_system.ident,
            [])

    def tearDown(self):
        for grade in self.grade_system.get_grades():
            self.catalog.delete_grade(grade.ident)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_grade_entries():
            cls.catalog.delete_grade_entry(obj.ident)
        for obj in cls.catalog.get_gradebook_columns():
            cls.catalog.delete_gradebook_column(obj.ident)
        cls.catalog.delete_grade_system(cls.grade_system.ident)
        cls.svc_mgr.delete_gradebook(cls.catalog.ident)"""

    clear_input_score_end_range = """
        self.form.set_input_score_end_range(50.0)
        self.assertIsNotNone(self.form._my_map['inputScoreEndRange'])
        self.form.clear_input_score_end_range()
        self.assertIsNone(self.form._my_map['inputScoreEndRange'])"""

    clear_input_score_start_range = """
        self.form.set_input_score_start_range(50.0)
        self.assertIsNotNone(self.form._my_map['inputScoreStartRange'])
        self.form.clear_input_score_start_range()
        self.assertIsNone(self.form._my_map['inputScoreStartRange'])"""

    clear_output_score = """
        self.form.set_output_score(50.0)
        self.assertIsNotNone(self.form._my_map['outputScore'])
        self.form.clear_output_score()
        self.assertIsNone(self.form._my_map['outputScore'])"""

    set_input_score_end_range = """
        self.assertIsNone(self.form._my_map['inputScoreEndRange'])
        self.form.set_input_score_end_range(50.0)
        self.assertEqual(self.form._my_map['inputScoreEndRange'], 50.0)"""

    set_input_score_start_range = """
        self.assertIsNone(self.form._my_map['inputScoreStartRange'])
        self.form.set_input_score_start_range(50.0)
        self.assertEqual(self.form._my_map['inputScoreStartRange'], 50.0)"""

    set_output_score = """
        self.assertIsNone(self.form._my_map['outputScore'])
        self.form.set_output_score(50.0)
        self.assertEqual(self.form._my_map['outputScore'], 50.0)"""


class GradeList:
    import_statements = [
        'from dlkit.json_.grading.objects import GradeList',
        'from dlkit.primordium.id.primitives import Id'
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

    def setUp(self):
        self.grade_list = []
        for num in [0, 1]:
            form = self.catalog.get_grade_form_for_create(
                self.grade_system.ident,
                [])
            new_grade = self.catalog.create_grade(form)
            self.grade_list.append(new_grade)
        self.grade_list = GradeList(self.grade_list,
                                    runtime=self.catalog._runtime,
                                    proxy=self.catalog._proxy)

    def tearDown(self):
        for grade in self.grade_system.get_grades():
            self.catalog.delete_grade(grade.ident)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_grade_entries():
            cls.catalog.delete_grade_entry(obj.ident)
        for obj in cls.catalog.get_gradebook_columns():
            cls.catalog.delete_gradebook_column(obj.ident)
        cls.catalog.delete_grade_system(cls.grade_system.ident)
        cls.svc_mgr.delete_gradebook(cls.catalog.ident)"""

    get_next_grade = """
        from dlkit.abstract_osid.grading.objects import Grade
        self.assertTrue(isinstance(self.grade_list.get_next_grade(), Grade))"""

    get_next_grades = """
        from dlkit.abstract_osid.grading.objects import Grade, GradeList
        new_list = self.grade_list.get_next_grades(2)
        self.assertTrue(isinstance(new_list, GradeList))
        for item in new_list:
            self.assertTrue(isinstance(item, Grade))"""


class GradeQuery:
    import_statements = [
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.json_.grading.queries import GradeQuery'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('GRADING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_gradebook(create_form)

    def setUp(self):
        # Since the session isn't implemented, we just construct an ActivityQuery directly
        self.query = GradeQuery(runtime=self.catalog._runtime)

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_gradebook(cls.catalog.ident)"""


class GradeEntry:
    import_statements = [
        'from dlkit.abstract_osid.grading.objects import GradebookColumn',
        'from dlkit.abstract_osid.authentication.objects import Agent',
        'from dlkit.primordium.calendaring.primitives import DateTime',
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

    def setUp(self):
        form = self.catalog.get_grade_entry_form_for_create(
            self.column.ident,
            AGENT_ID,
            [])
        form.display_name = 'Test object'
        self.object = self.catalog.create_grade_entry(form)

    def tearDown(self):
        for grade_entry in self.catalog.get_grade_entries():
            self.catalog.delete_grade_entry(grade_entry.ident)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_grade_entries():
            cls.catalog.delete_grade_entry(obj.ident)
        for obj in cls.catalog.get_gradebook_columns():
            cls.catalog.delete_gradebook_column(obj.ident)
        cls.catalog.delete_grade_system(cls.grade_system.ident)
        cls.svc_mgr.delete_gradebook(cls.catalog.ident)"""

    get_grade = """
        with self.assertRaises(errors.IllegalState):
            self.object.get_grade()"""

    get_grade_id = """
        self.assertTrue(isinstance(self.object.get_grade_id(), Id))"""

    get_gradebook_column = """
        self.assertTrue(isinstance(self.object.get_gradebook_column(), GradebookColumn))
        self.assertEqual(str(self.object.get_gradebook_column().ident),
                         str(self.column.ident))"""

    get_gradebook_column_id = """
        self.assertTrue(isinstance(self.object.get_gradebook_column_id(), Id))
        self.assertEqual(str(self.object.get_gradebook_column_id()),
                         str(self.column.ident))"""

    get_grading_agent = """
        agent = self.object.get_grading_agent()
        self.assertTrue(isinstance(agent, Agent))"""

    get_grading_agent_id = """
        agent_id = self.object.get_grading_agent_id()
        self.assertTrue(isinstance(agent_id, Id))"""

    get_key_resource = """
        agent = self.object.get_key_resource()
        self.assertTrue(isinstance(agent, Agent))"""

    get_key_resource_id = """
        agent_id = self.object.get_key_resource_id()
        self.assertTrue(isinstance(agent_id, Id))"""

    get_score = """
        score = self.object.get_score()
        self.assertIsNone(score)

        # if this is set, should be a Decimal
        form = self.catalog.get_grade_entry_form_for_create(
            self.column.ident,
            AGENT_ID,
            [])
        form.set_score(50.0)
        new_grade_entry = self.catalog.create_grade_entry(form)

        self.assertEqual(new_grade_entry.get_score(), 50.0)"""

    get_time_graded = """
        with self.assertRaises(errors.IllegalState):
            self.object.get_time_graded()"""

    is_graded = """
        self.assertTrue(isinstance(self.object.is_graded(), bool))"""

    overrides_calculated_entry = """
        self.assertTrue(isinstance(self.object.overrides_calculated_entry(), bool))"""


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
        self.assertTrue(self.form._my_map['ignoredForCalculations'])
        with self.assertRaises(errors.InvalidArgument):
            self.form.set_ignored_for_calculations('false')"""

    clear_grade = """
        # Normally this would follow ResourceForm.clear_avatar_template
        # Except we need a valid ``grade`` for the initial ``set_grade`` to
        #   work, so we provide a hand-written impl here.
        self.form._my_map['gradeId'] = 'repository.Asset%3Afake-id%40ODL.MIT.EDU'
        self.assertEqual(self.form._my_map['gradeId'],
                         'repository.Asset%3Afake-id%40ODL.MIT.EDU')
        self.form.clear_grade()
        self.assertEqual(self.form._my_map['gradeId'], '')"""

    clear_score = """
        # because this GradeSystem is basedOnGrades, cannot use form.set_score()
        #   to set the initial data
        self.form._my_map['score'] = 50.0
        self.assertIsNotNone(self.form._my_map['score'])
        self.form.clear_score()

        # Also, because this is basedOnGrades, no exception thrown
        #  AND this method also does nothing...how confusing
        self.assertIsNotNone(self.form._my_map['score'])"""

    set_score = """
        # because this GradeSystem is basedOnGrades, set_score() throws
        #   an exception
        with self.assertRaises(errors.InvalidArgument):
            self.form.set_score(50.0)"""

    set_grade = """
        # This should come from ResourceForm.set_avatar_template,
        #   but we override because in this case, there is no acceptable
        #   gradeId set, so we get an exception.
        with self.assertRaises(errors.InvalidArgument):
            self.form.set_grade(Id('repository.Asset%3Afake-id%40ODL.MIT.EDU'))"""


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


class GradebookColumnSummaryQuery:
    import_statements = [
        'from dlkit.json_.grading.queries import GradebookColumnSummaryQuery'
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

    def setUp(self):
        # Since the session isn't implemented, we just construct a GradebookColumnSummaryQuery directly
        self.query = GradebookColumnSummaryQuery(runtime=self.catalog._runtime)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_grade_entries():
            cls.catalog.delete_grade_entry(obj.ident)
        for obj in cls.catalog.get_gradebook_columns():
            cls.catalog.delete_gradebook_column(obj.ident)
        for obj in cls.catalog.get_grade_systems():
            cls.catalog.delete_grade_system(obj.ident)
        cls.svc_mgr.delete_gradebook(cls.catalog.ident)"""


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

    def setUp(self):
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_grade_entries():
            cls.catalog.delete_grade_entry(obj.ident)
        for obj in cls.catalog.get_gradebook_columns():
            cls.catalog.delete_gradebook_column(obj.ident)
        for obj in cls.catalog.get_grade_systems():
            cls.catalog.delete_grade_system(obj.ident)
        cls.svc_mgr.delete_gradebook(cls.catalog.ident)"""

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


class GradebookQuery:
    import_statements = [
        'from dlkit.json_.grading.queries import GradebookQuery'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('GRADING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_gradebook(create_form)
        cls.fake_id = Id('resource.Resource%3A1%40ODL.MIT.EDU')

    def setUp(self):
        # Since the session isn't implemented, we just construct a GradebookQuery directly
        self.query = GradebookQuery(runtime=self.catalog._runtime)

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_gradebook(cls.catalog.ident)"""


class GradebookHierarchySession:
    init = """
    # Override this because spec doesn't have a method ``remove_child_gradebooks``
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('GRADING', proxy=PROXY, implementation='TEST_SERVICE')
        cls.catalogs = dict()
        for name in ['Root', 'Child 1', 'Child 2', 'Grandchild 1']:
            create_form = cls.svc_mgr.get_gradebook_form_for_create([])
            create_form.display_name = name
            create_form.description = 'Test Gradebook ' + name
            cls.catalogs[name] = cls.svc_mgr.create_gradebook(create_form)
        cls.svc_mgr.add_root_gradebook(cls.catalogs['Root'].ident)
        cls.svc_mgr.add_child_gradebook(cls.catalogs['Root'].ident, cls.catalogs['Child 1'].ident)
        cls.svc_mgr.add_child_gradebook(cls.catalogs['Root'].ident, cls.catalogs['Child 2'].ident)
        cls.svc_mgr.add_child_gradebook(cls.catalogs['Child 1'].ident, cls.catalogs['Grandchild 1'].ident)

    def setUp(self):
        self.session = self.svc_mgr

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.remove_child_gradebook(cls.catalogs['Child 1'].ident, cls.catalogs['Grandchild 1'].ident)
        cls.svc_mgr.remove_child_gradebook(cls.catalogs['Root'].ident, cls.catalogs['Child 1'].ident)
        cls.svc_mgr.remove_child_gradebook(cls.catalogs['Root'].ident, cls.catalogs['Child 2'].ident)
        cls.svc_mgr.remove_root_gradebook(cls.catalogs['Root'].ident)
        for cat_name in cls.catalogs:
            cls.svc_mgr.delete_gradebook(cls.catalogs[cat_name].ident)"""


class GradebookHierarchyDesignSession:
    init = """
    # Override this because spec doesn't have a method ``remove_child_gradebooks``
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('GRADING', proxy=PROXY, implementation='TEST_SERVICE')
        cls.catalogs = dict()
        for name in ['Root', 'Child 1', 'Child 2', 'Grandchild 1']:
            create_form = cls.svc_mgr.get_gradebook_form_for_create([])
            create_form.display_name = name
            create_form.description = 'Test Gradebook ' + name
            cls.catalogs[name] = cls.svc_mgr.create_gradebook(create_form)
        cls.svc_mgr.add_root_gradebook(cls.catalogs['Root'].ident)
        cls.svc_mgr.add_child_gradebook(cls.catalogs['Root'].ident, cls.catalogs['Child 1'].ident)
        cls.svc_mgr.add_child_gradebook(cls.catalogs['Root'].ident, cls.catalogs['Child 2'].ident)
        cls.svc_mgr.add_child_gradebook(cls.catalogs['Child 1'].ident, cls.catalogs['Grandchild 1'].ident)

    def setUp(self):
        self.session = self.svc_mgr

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.remove_child_gradebook(cls.catalogs['Child 1'].ident, cls.catalogs['Grandchild 1'].ident)
        cls.svc_mgr.remove_child_gradebook(cls.catalogs['Root'].ident, cls.catalogs['Child 1'].ident)
        cls.svc_mgr.remove_child_gradebook(cls.catalogs['Root'].ident, cls.catalogs['Child 2'].ident)
        cls.svc_mgr.remove_root_gradebook(cls.catalogs['Root'].ident)
        for cat_name in cls.catalogs:
            cls.svc_mgr.delete_gradebook(cls.catalogs[cat_name].ident)"""


class GradeSystemAdminSession:
    import_statements = [
        'from dlkit.abstract_osid.grading.objects import Grade',
        'from dlkit.abstract_osid.osid.objects import OsidForm'
    ]

    can_create_grade_with_record_types = """
        self.assertTrue(
            isinstance(self.session.can_create_grade_with_record_types(self.osid_object.ident,
                                                                       DEFAULT_TYPE),
                       bool))"""

    can_create_grades = """
        self.assertTrue(
            isinstance(self.session.can_create_grades(self.osid_object.ident),
                       bool))"""

    can_delete_grades = """
        self.assertTrue(
            isinstance(self.session.can_delete_grades(self.osid_object.ident),
                       bool))"""

    create_grade = """
        self.assertEqual(self.osid_object.get_grades().available(), 0)
        form = self.session.get_grade_form_for_create(
            self.osid_object.ident,
            [])
        form.display_name = 'Test object'
        grade = self.session.create_grade(form)
        self.assertTrue(isinstance(grade, Grade))
        self.assertEqual(grade.display_name.text, 'Test object')

        updated_grade_system = self.catalog.get_grade_system(self.osid_object.ident)
        self.assertEqual(updated_grade_system.get_grades().available(), 1)"""

    delete_grade = """
        form = self.session.get_grade_form_for_create(
            self.osid_object.ident,
            [])
        form.display_name = 'Test object'
        grade = self.session.create_grade(form)
        self.assertTrue(isinstance(grade, Grade))
        self.assertEqual(grade.display_name.text, 'Test object')

        updated_grade_system = self.catalog.get_grade_system(self.osid_object.ident)
        self.assertEqual(updated_grade_system.get_grades().available(), 1)

        self.session.delete_grade(grade.ident)

        updated_grade_system = self.catalog.get_grade_system(self.osid_object.ident)
        self.assertEqual(updated_grade_system.get_grades().available(), 0)"""

    get_grade_form_for_create = """
        form = self.session.get_grade_form_for_create(
            self.osid_object.ident,
            [])
        self.assertTrue(isinstance(form, OsidForm))
        self.assertFalse(form.is_for_update())"""

    get_grade_form_for_update = """
        form = self.session.get_grade_form_for_create(
            self.osid_object.ident,
            [])
        grade = self.session.create_grade(form)
        form = self.session.get_grade_form_for_update(grade.ident)
        self.assertTrue(isinstance(form, OsidForm))
        self.assertTrue(form.is_for_update())"""

    update_grade = """
        self.assertEqual(self.osid_object.get_grades().available(), 0)
        form = self.session.get_grade_form_for_create(
            self.osid_object.ident,
            [])
        form.display_name = 'Test object'
        grade = self.session.create_grade(form)
        self.assertTrue(isinstance(grade, Grade))
        self.assertEqual(grade.display_name.text, 'Test object')

        form = self.session.get_grade_form_for_update(grade.ident)
        form.display_name = 'new name'
        grade = self.session.update_grade(form)

        self.assertTrue(isinstance(grade, Grade))
        self.assertEqual(grade.display_name.text, 'new name')

        updated_grade_system = self.catalog.get_grade_system(self.osid_object.ident)
        self.assertEqual(updated_grade_system.get_grades().available(), 1)"""
