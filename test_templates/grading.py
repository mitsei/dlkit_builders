
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
    # This really shouldn't be generated...should be GradeBook??
    @classmethod
    def setUpClass(cls):
        cls.object = None

    @classmethod
    def tearDownClass(cls):
        pass"""


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


class GradebookColumnSummary:
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

    init = """"""


class GradeEntryAdminSession:
    create_grade_entry = """"""
