class GradeSystem:
    import_statements = [
        'from dlkit.abstract_osid.grading.objects import GradeList',
        'from dlkit.json_.id.objects import IdList'
    ]

    get_grade_ids = """
        if not is_never_authz(self.service_config):
            grade_ids = self.object.get_grade_ids()
            assert isinstance(grade_ids, IdList)
            assert grade_ids.available() == 0"""

    get_grades = """
        if not is_never_authz(self.service_config):
            grades = self.object.get_grades()
            assert isinstance(grades, GradeList)
            assert grades.available() == 0"""

    get_highest_numeric_score = """
        if not is_never_authz(self.service_config):
            score = self.object.get_highest_numeric_score()
            assert score is None

            # if this is set, should be a Decimal
            form = self.catalog.get_grade_system_form_for_create([])
            form.set_highest_numeric_score(100.0)
            new_grade_system = self.catalog.create_grade_system(form)

            assert new_grade_system.get_highest_numeric_score() == 100.0"""

    get_lowest_numeric_score = """
        if not is_never_authz(self.service_config):
            score = self.object.get_lowest_numeric_score()
            assert score is None

            # if this is set, should be a Decimal
            form = self.catalog.get_grade_system_form_for_create([])
            form.set_lowest_numeric_score(0.0)
            new_grade_system = self.catalog.create_grade_system(form)

            assert new_grade_system.get_lowest_numeric_score() == 0.0"""

    get_numeric_score_increment = """
        if not is_never_authz(self.service_config):
            score = self.object.get_numeric_score_increment()
            assert score is None

            # if this is set, should be a Decimal
            form = self.catalog.get_grade_system_form_for_create([])
            form.set_numeric_score_increment(1.0)
            new_grade_system = self.catalog.create_grade_system(form)

            assert new_grade_system.get_numeric_score_increment() == 1.0"""

    is_based_on_grades = """
        if not is_never_authz(self.service_config):
            # when not set on create, returns None
            assert self.object.is_based_on_grades() is None

            form = self.catalog.get_grade_system_form_for_create([])
            form.set_based_on_grades(True)
            new_grade_system = self.catalog.create_grade_system(form)

            assert new_grade_system.is_based_on_grades()"""


class GradeSystemForm:
    import_statements = [
        'from dlkit.abstract_osid.grading.objects import GradeList',
        'from dlkit.json_.id.objects import IdList'
    ]

    clear_highest_numeric_score = """
        if not is_never_authz(self.service_config):
            self.form.set_highest_numeric_score(100.0)
            assert self.form._my_map['highestNumericScore'] is not None
            self.form.clear_highest_numeric_score()
            assert self.form._my_map['highestNumericScore'] is None"""

    clear_lowest_numeric_score = """
        if not is_never_authz(self.service_config):
            self.form.set_lowest_numeric_score(100.0)
            assert self.form._my_map['lowestNumericScore'] is not None
            self.form.clear_lowest_numeric_score()
            assert self.form._my_map['lowestNumericScore'] is None"""

    clear_numeric_score_increment = """
        if not is_never_authz(self.service_config):
            self.form.set_numeric_score_increment(100.0)
            assert self.form._my_map['numericScoreIncrement'] is not None
            self.form.clear_numeric_score_increment()
            assert self.form._my_map['numericScoreIncrement'] is None"""

    clear_based_on_grades = """
        if not is_never_authz(self.service_config):
            self.form.set_based_on_grades(True)
            assert self.form._my_map['basedOnGrades'] is not None
            self.form.clear_based_on_grades()
            assert self.form._my_map['basedOnGrades'] is None"""

    set_highest_numeric_score = """
        if not is_never_authz(self.service_config):
            assert self.form._my_map['highestNumericScore'] is None
            self.form.set_highest_numeric_score(100.0)
            assert self.form._my_map['highestNumericScore'] is not None"""

    set_lowest_numeric_score = """
        if not is_never_authz(self.service_config):
            assert self.form._my_map['lowestNumericScore'] is None
            self.form.set_lowest_numeric_score(100.0)
            assert self.form._my_map['lowestNumericScore'] is not None"""

    set_numeric_score_increment = """
        if not is_never_authz(self.service_config):
            assert self.form._my_map['numericScoreIncrement'] is None
            self.form.set_numeric_score_increment(100.0)
            assert self.form._my_map['numericScoreIncrement'] is not None"""

    set_based_on_grades = """
        if not is_never_authz(self.service_config):
            assert self.form._my_map['basedOnGrades'] is None
            self.form.set_based_on_grades(True)
            assert self.form._my_map['basedOnGrades'] is not None"""


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
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'GRADING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_gradebook(create_form)

        form = request.cls.catalog.get_grade_system_form_for_create([])
        form.display_name = 'Grade system'
        request.cls.grade_system = request.cls.catalog.create_grade_system(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_grade_entries():
                request.cls.catalog.delete_grade_entry(obj.ident)
            for obj in request.cls.catalog.get_gradebook_columns():
                request.cls.catalog.delete_gradebook_column(obj.ident)
            request.cls.catalog.delete_grade_system(request.cls.grade_system.ident)
            request.cls.svc_mgr.delete_gradebook(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        form = request.cls.catalog.get_gradebook_column_form_for_create([])
        form.display_name = 'Gradebook Column'
        form.set_grade_system(request.cls.grade_system.ident)
        request.cls.object = request.cls.catalog.create_gradebook_column(form)

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for gradebook_column in request.cls.catalog.get_gradebook_columns():
                request.cls.catalog.delete_gradebook_column(gradebook_column.ident)

    request.addfinalizer(test_tear_down)"""

    get_grade_system = """
        if not is_never_authz(self.service_config):
            grade_system = self.object.get_grade_system()
            assert isinstance(grade_system, GradeSystem)
            assert str(grade_system.ident) == str(self.grade_system.ident)"""

    get_grade_system_id = """
        if not is_never_authz(self.service_config):
            grade_system_id = self.object.get_grade_system_id()
            assert isinstance(grade_system_id, Id)
            assert str(grade_system_id) == str(self.grade_system.ident)"""


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
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'GRADING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3A000000000000000000000000%40DLKIT.MIT.EDU')


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.grade_entry_list = list()
    request.cls.grade_entry_ids = list()
    request.cls.gradebook_column_list = list()
    request.cls.gradebook_column_ids = list()

    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test Gradebook'
        create_form.description = 'Test Gradebook for GradebookColumnLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_gradebook(create_form)
        create_form = request.cls.catalog.get_grade_system_form_for_create([])
        create_form.display_name = 'Test Grade System'
        create_form.description = 'Test Grade System for GradebookColumnLookupSession tests'
        create_form.based_on_grades = False
        create_form.lowest_numeric_score = 0
        create_form.highest_numeric_score = 100
        create_form.numeric_score_increment = 1
        request.cls.grade_system = request.cls.catalog.create_grade_system(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_gradebook_column_form_for_create([])
            create_form.display_name = 'Test GradebookColumn ' + str(num)
            create_form.description = 'Test GradebookColumn for GradebookColumnLookupSession tests'
            create_form.grade_system = request.cls.grade_system.ident
            obj = request.cls.catalog.create_gradebook_column(create_form)
            request.cls.gradebook_column_list.append(obj)
            request.cls.gradebook_column_ids.append(obj.ident)
        for num in range(0, 100):
            create_form = request.cls.catalog.get_grade_entry_form_for_create(request.cls.gradebook_column_ids[0], AGENT_ID, [])
            create_form.display_name = 'Test GradeEntry ' + str(num)
            create_form.description = 'Test GradeEntry for GradebookColumnLookupSession tests'
            create_form.set_score(float(num))
            object = request.cls.catalog.create_grade_entry(create_form)
            request.cls.grade_entry_list.append(object)
            request.cls.grade_entry_ids.append(object.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_gradebooks():
                for obj in catalog.get_grade_entries():
                    catalog.delete_grade_entry(obj.ident)
                for obj in catalog.get_gradebook_columns():
                    catalog.delete_gradebook_column(obj.ident)
                for obj in catalog.get_grade_systems():
                    catalog.delete_grade_system(obj.ident)
                request.cls.svc_mgr.delete_gradebook(catalog.ident)

    request.addfinalizer(test_tear_down)"""

    # skip this one until gradebook column summary is supported
    get_gradebook_column_summary = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.catalog.get_gradebook_column_summary(self.gradebook_column_ids[0]),
                              GradebookColumnSummary)
        else:
            with pytest.raises(errors.NotFound):
                self.catalog.get_gradebook_column_summary(self.fake_id)"""


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
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'GRADING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3A000000000000000000000000%40DLKIT.MIT.EDU')


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.grade_entry_list = list()
    request.cls.grade_entry_ids = list()
    request.cls.gradebook_column_list = list()
    request.cls.gradebook_column_ids = list()

    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test Gradebook'
        create_form.description = 'Test Gradebook for GradeEntryLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_gradebook(create_form)
        create_form = request.cls.catalog.get_grade_system_form_for_create([])
        create_form.display_name = 'Test Grade System'
        create_form.description = 'Test Grade System for GradeEntryLookupSession tests'
        create_form.based_on_grades = False
        create_form.lowest_numeric_score = 0
        create_form.highest_numeric_score = 5
        create_form.numeric_score_increment = 0.25
        request.cls.grade_system = request.cls.catalog.create_grade_system(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_gradebook_column_form_for_create([])
            create_form.display_name = 'Test GradebookColumn ' + str(num)
            create_form.description = 'Test GradebookColumn for GradeEntryLookupSession tests'
            create_form.grade_system = request.cls.grade_system.ident
            obj = request.cls.catalog.create_gradebook_column(create_form)
            request.cls.gradebook_column_list.append(obj)
            request.cls.gradebook_column_ids.append(obj.ident)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_grade_entry_form_for_create(request.cls.gradebook_column_ids[num], AGENT_ID, [])
            create_form.display_name = 'Test GradeEntry ' + str(num)
            create_form.description = 'Test GradeEntry for GradeEntryLookupSession tests'
            object = request.cls.catalog.create_grade_entry(create_form)
            request.cls.grade_entry_list.append(object)
            request.cls.grade_entry_ids.append(object.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_gradebooks():
                for obj in catalog.get_grade_entries():
                    catalog.delete_grade_entry(obj.ident)
                for obj in catalog.get_gradebook_columns():
                    catalog.delete_gradebook_column(obj.ident)
                for obj in catalog.get_grade_systems():
                    catalog.delete_grade_system(obj.ident)
                request.cls.svc_mgr.delete_gradebook(catalog.ident)

    request.addfinalizer(test_tear_down)"""

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
        if not is_never_authz(self.service_config):
            results = self.session.get_grade_entries_for_gradebook_column_on_date(self.gradebook_column_ids[0],
                                                                                  DateTime.utcnow(),
                                                                                  end_date)
            assert isinstance(results, ABCObjects.GradeEntryList)
            assert results.available() == 1
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_grade_entries_for_gradebook_column_on_date(self.fake_id,
                                                                            DateTime.utcnow(),
                                                                            end_date)"""


class GradeEntryQuerySession:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.grade_entry_list = list()
    request.cls.grade_entry_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'GRADING',
        proxy=PROXY,
        implementation=request.cls.service_config)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test Gradebook'
        create_form.description = 'Test Gradebook for GradeEntryQuerySession tests'
        request.cls.catalog = request.cls.svc_mgr.create_gradebook(create_form)

        form = request.cls.catalog.get_grade_system_form_for_create([])
        form.display_name = 'Test grade system'
        grade_system = request.cls.catalog.create_grade_system(form)

        form = request.cls.catalog.get_gradebook_column_form_for_create([])
        form.display_name = 'Test gradebook column'
        form.set_grade_system(grade_system.ident)
        gradebook_column = request.cls.catalog.create_gradebook_column(form)

        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = request.cls.catalog.get_grade_entry_form_for_create(gradebook_column.ident, AGENT_ID, [])
            create_form.display_name = 'Test GradeEntry ' + color
            create_form.description = (
                'Test GradeEntry for GradeEntryQuerySession tests, did I mention green')
            obj = request.cls.catalog.create_grade_entry(create_form)
            request.cls.grade_entry_list.append(obj)
            request.cls.grade_entry_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_gradebooks():
                for obj in catalog.get_grade_entries():
                    catalog.delete_grade_entry(obj.ident)
                for obj in catalog.get_gradebook_columns():
                    catalog.delete_gradebook_column(obj.ident)
                for obj in catalog.get_grade_systems():
                    catalog.delete_grade_system(obj.ident)
                request.cls.svc_mgr.delete_gradebook(catalog.ident)

    request.addfinalizer(test_tear_down)"""


class Grade:
    import_statements = [
        'from dlkit.abstract_osid.grading import objects as ABCObjects',
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'GRADING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_gradebook(create_form)

        form = request.cls.catalog.get_grade_system_form_for_create([])
        form.display_name = 'Grade system'
        request.cls.grade_system = request.cls.catalog.create_grade_system(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_grade_entries():
                request.cls.catalog.delete_grade_entry(obj.ident)
            for obj in request.cls.catalog.get_gradebook_columns():
                request.cls.catalog.delete_gradebook_column(obj.ident)
            request.cls.catalog.delete_grade_system(request.cls.grade_system.ident)
            request.cls.svc_mgr.delete_gradebook(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        form = request.cls.catalog.get_grade_form_for_create(
            request.cls.grade_system.ident,
            [])
        form.display_name = 'Test object'
        request.cls.object = request.cls.catalog.create_grade(form)

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for grade in request.cls.grade_system.get_grades():
                request.cls.catalog.delete_grade(grade.ident)

    request.addfinalizer(test_tear_down)"""

    get_grade_system = """
        if not is_never_authz(self.service_config):
            grade_system = self.object.get_grade_system()
            assert isinstance(grade_system, ABCObjects.GradeSystem)
            assert str(grade_system.ident) == str(self.grade_system.ident)"""

    get_grade_system_id = """
        if not is_never_authz(self.service_config):
            grade_system_id = self.object.get_grade_system_id()
            assert isinstance(grade_system_id, Id)
            assert str(grade_system_id) == str(self.grade_system.ident)"""

    get_input_score_end_range = """
        if not is_never_authz(self.service_config):
            end_range = self.object.get_input_score_end_range()
            assert end_range is None

            # if this is set, should be a Decimal
            form = self.catalog.get_grade_form_for_create(
                self.grade_system.ident,
                [])
            form.set_input_score_end_range(50.0)
            new_grade = self.catalog.create_grade(form)

            assert new_grade.get_input_score_end_range() == 50.0"""

    get_input_score_start_range = """
        if not is_never_authz(self.service_config):
            start_range = self.object.get_input_score_end_range()
            assert start_range is None

            # if this is set, should be a Decimal
            form = self.catalog.get_grade_form_for_create(
                self.grade_system.ident,
                [])
            form.set_input_score_start_range(50.0)
            new_grade = self.catalog.create_grade(form)

            assert new_grade.get_input_score_start_range() == 50.0"""

    get_output_score = """
        if not is_never_authz(self.service_config):
            score = self.object.get_output_score()
            assert score is None

            # if this is set, should be a Decimal
            form = self.catalog.get_grade_form_for_create(
                self.grade_system.ident,
                [])
            form.set_output_score(50.0)
            new_grade = self.catalog.create_grade(form)

            assert new_grade.get_output_score() == 50.0"""


class GradeForm:
    import_statements = [
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'GRADING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_gradebook(create_form)

        form = request.cls.catalog.get_grade_system_form_for_create([])
        form.display_name = 'Grade system'
        request.cls.grade_system = request.cls.catalog.create_grade_system(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_grade_entries():
                request.cls.catalog.delete_grade_entry(obj.ident)
            for obj in request.cls.catalog.get_gradebook_columns():
                request.cls.catalog.delete_gradebook_column(obj.ident)
            request.cls.catalog.delete_grade_system(request.cls.grade_system.ident)
            request.cls.svc_mgr.delete_gradebook(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        request.cls.form = request.cls.catalog.get_grade_form_for_create(
            request.cls.grade_system.ident,
            [])

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for grade in request.cls.grade_system.get_grades():
                request.cls.catalog.delete_grade(grade.ident)

    request.addfinalizer(test_tear_down)"""

    clear_input_score_end_range = """
        if not is_never_authz(self.service_config):
            self.form.set_input_score_end_range(50.0)
            assert self.form._my_map['inputScoreEndRange'] is not None
            self.form.clear_input_score_end_range()
            assert self.form._my_map['inputScoreEndRange'] is None"""

    clear_input_score_start_range = """
        if not is_never_authz(self.service_config):
            self.form.set_input_score_start_range(50.0)
            assert self.form._my_map['inputScoreStartRange'] is not None
            self.form.clear_input_score_start_range()
            assert self.form._my_map['inputScoreStartRange'] is None"""

    clear_output_score = """
        if not is_never_authz(self.service_config):
            self.form.set_output_score(50.0)
            assert self.form._my_map['outputScore'] is not None
            self.form.clear_output_score()
            assert self.form._my_map['outputScore'] is None"""

    set_input_score_end_range = """
        if not is_never_authz(self.service_config):
            assert self.form._my_map['inputScoreEndRange'] is None
            self.form.set_input_score_end_range(50.0)
            assert self.form._my_map['inputScoreEndRange'] == 50.0"""

    set_input_score_start_range = """
        if not is_never_authz(self.service_config):
            assert self.form._my_map['inputScoreStartRange'] is None
            self.form.set_input_score_start_range(50.0)
            assert self.form._my_map['inputScoreStartRange'] == 50.0"""

    set_output_score = """
        if not is_never_authz(self.service_config):
            assert self.form._my_map['outputScore'] is None
            self.form.set_output_score(50.0)
            assert self.form._my_map['outputScore'] == 50.0"""


class GradeList:
    import_statements = [
        'from dlkit.json_.grading.objects import GradeList',
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'GRADING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_gradebook(create_form)

        form = request.cls.catalog.get_grade_system_form_for_create([])
        form.display_name = 'Grade system'
        request.cls.grade_system = request.cls.catalog.create_grade_system(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_grade_entries():
                request.cls.catalog.delete_grade_entry(obj.ident)
            for obj in request.cls.catalog.get_gradebook_columns():
                request.cls.catalog.delete_gradebook_column(obj.ident)
            request.cls.catalog.delete_grade_system(request.cls.grade_system.ident)
            request.cls.svc_mgr.delete_gradebook(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.grade_list = []
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            form = request.cls.catalog.get_grade_form_for_create(
                request.cls.grade_system.ident,
                [])
            new_grade = request.cls.catalog.create_grade(form)
            request.cls.grade_list.append(new_grade)
        request.cls.grade_list = GradeList(request.cls.grade_list,
                                           runtime=request.cls.catalog._runtime,
                                           proxy=request.cls.catalog._proxy)

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for grade in request.cls.grade_system.get_grades():
                request.cls.catalog.delete_grade(grade.ident)

    request.addfinalizer(test_tear_down)"""

    get_next_grade = """
        from dlkit.abstract_osid.grading.objects import Grade
        if not is_never_authz(self.service_config):
            assert isinstance(self.grade_list.get_next_grade(), Grade)"""

    get_next_grades = """
        from dlkit.abstract_osid.grading.objects import Grade, GradeList
        if not is_never_authz(self.service_config):
            new_list = self.grade_list.get_next_grades(2)
            assert isinstance(new_list, GradeList)
            for item in new_list:
                assert isinstance(item, Grade)"""


class GradeQuery:
    import_statements = [
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.json_.grading.queries import GradeQuery'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'GRADING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_gradebook(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_gradebook(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # Since the session isn't implemented, we just construct an ActivityQuery directly
    if not is_never_authz(request.cls.service_config):
        request.cls.query = GradeQuery(runtime=request.cls.catalog._runtime)"""


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
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'GRADING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_gradebook(create_form)

        form = request.cls.catalog.get_grade_system_form_for_create([])
        form.display_name = 'Grade system'
        request.cls.grade_system = request.cls.catalog.create_grade_system(form)

        form = request.cls.catalog.get_gradebook_column_form_for_create([])
        form.display_name = 'Gradebook Column'
        form.set_grade_system(request.cls.grade_system.ident)
        request.cls.column = request.cls.catalog.create_gradebook_column(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_grade_entries():
                request.cls.catalog.delete_grade_entry(obj.ident)
            for obj in request.cls.catalog.get_gradebook_columns():
                request.cls.catalog.delete_gradebook_column(obj.ident)
            request.cls.catalog.delete_grade_system(request.cls.grade_system.ident)
            request.cls.svc_mgr.delete_gradebook(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        form = request.cls.catalog.get_grade_entry_form_for_create(
            request.cls.column.ident,
            AGENT_ID,
            [])
        form.display_name = 'Test object'
        request.cls.object = request.cls.catalog.create_grade_entry(form)

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for grade_entry in request.cls.catalog.get_grade_entries():
                request.cls.catalog.delete_grade_entry(grade_entry.ident)

    request.addfinalizer(test_tear_down)"""

    get_grade = """
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.IllegalState):
                self.object.get_grade()"""

    get_grade_id = """
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.IllegalState):
                self.object.get_grade()"""

    get_gradebook_column = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.get_gradebook_column(), GradebookColumn)
            assert str(self.object.get_gradebook_column().ident) == str(self.column.ident)"""

    get_gradebook_column_id = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.get_gradebook_column_id(), Id)
            assert str(self.object.get_gradebook_column_id()) == str(self.column.ident)"""

    get_grading_agent = """
        if not is_never_authz(self.service_config):
            agent = self.object.get_grading_agent()
            assert isinstance(agent, Agent)"""

    get_grading_agent_id = """
        if not is_never_authz(self.service_config):
            agent_id = self.object.get_grading_agent_id()
            assert isinstance(agent_id, Id)"""

    get_key_resource = """
        if not is_never_authz(self.service_config):
            agent = self.object.get_key_resource()
            assert isinstance(agent, Agent)"""

    get_key_resource_id = """
        if not is_never_authz(self.service_config):
            agent_id = self.object.get_key_resource_id()
            assert isinstance(agent_id, Id)"""

    get_score = """
        if not is_never_authz(self.service_config):
            score = self.object.get_score()
            assert score is None

            # if this is set, should be a Decimal
            form = self.catalog.get_grade_entry_form_for_create(
                self.column.ident,
                AGENT_ID,
                [])
            form.set_score(50.0)
            new_grade_entry = self.catalog.create_grade_entry(form)

            assert new_grade_entry.get_score() == 50.0"""

    get_time_graded = """
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.IllegalState):
                self.object.get_time_graded()"""

    is_graded = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.is_graded(), bool)"""

    overrides_calculated_entry = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.overrides_calculated_entry(), bool)"""


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
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'GRADING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_gradebook(create_form)

        form = request.cls.catalog.get_grade_system_form_for_create([])
        form.display_name = 'Grade system'
        form.set_based_on_grades(True)
        request.cls.grade_system = request.cls.catalog.create_grade_system(form)

        form = request.cls.catalog.get_gradebook_column_form_for_create([])
        form.display_name = 'Gradebook Column'
        form.set_grade_system(request.cls.grade_system.ident)
        request.cls.column = request.cls.catalog.create_gradebook_column(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_grade_entries():
                request.cls.catalog.delete_grade_entry(obj.ident)
            for obj in request.cls.catalog.get_gradebook_columns():
                request.cls.catalog.delete_gradebook_column(obj.ident)
            request.cls.catalog.delete_grade_system(request.cls.grade_system.ident)
            request.cls.svc_mgr.delete_gradebook(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        request.cls.form = request.cls.catalog.get_grade_entry_form_for_create(
            request.cls.column.ident,
            AGENT_ID,
            [])"""

    set_ignored_for_calculations = """
        self.form.set_ignored_for_calculations(True)
        assert self.form._my_map['ignoredForCalculations']
        with pytest.raises(errors.InvalidArgument):
            self.form.set_ignored_for_calculations('false')"""

    clear_grade = """
        # Normally this would follow ResourceForm.clear_avatar_template
        # Except we need a valid ``grade`` for the initial ``set_grade`` to
        #   work, so we provide a hand-written impl here.
        self.form._my_map['gradeId'] = 'repository.Asset%3Afake-id%40ODL.MIT.EDU'
        assert self.form._my_map['gradeId'] == 'repository.Asset%3Afake-id%40ODL.MIT.EDU'
        self.form.clear_grade()
        assert self.form._my_map['gradeId'] == ''"""

    clear_score = """
        # because this GradeSystem is basedOnGrades, cannot use form.set_score()
        #   to set the initial data
        self.form._my_map['score'] = 50.0
        assert self.form._my_map['score'] is not None
        self.form.clear_score()

        # Also, because this is basedOnGrades, no exception thrown
        #  AND this method also does nothing...how confusing
        assert self.form._my_map['score'] is not None"""

    set_score = """
        # because this GradeSystem is basedOnGrades, set_score() throws
        #   an exception
        with pytest.raises(errors.InvalidArgument):
            self.form.set_score(50.0)"""

    set_grade = """
        # This should come from ResourceForm.set_avatar_template,
        #   but we override because in this case, there is no acceptable
        #   gradeId set, so we get an exception.
        with pytest.raises(errors.InvalidArgument):
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
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'GRADING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_gradebook(create_form)

        form = request.cls.catalog.get_grade_system_form_for_create([])
        form.display_name = 'Grade system'
        form.set_based_on_grades(True)
        request.cls.grade_system = request.cls.catalog.create_grade_system(form)

        form = request.cls.catalog.get_gradebook_column_form_for_create([])
        form.display_name = 'Gradebook Column'
        form.set_grade_system(request.cls.grade_system.ident)
        request.cls.column = request.cls.catalog.create_gradebook_column(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_grade_entries():
                request.cls.catalog.delete_grade_entry(obj.ident)
            for obj in request.cls.catalog.get_gradebook_columns():
                request.cls.catalog.delete_gradebook_column(obj.ident)
            request.cls.catalog.delete_grade_system(request.cls.grade_system.ident)
            request.cls.svc_mgr.delete_gradebook(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    from dlkit.json_.grading.objects import GradeEntryList
    request.cls.grade_entry_list = list()
    request.cls.grade_entry_ids = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            form = request.cls.catalog.get_grade_entry_form_for_create(
                request.cls.column.ident,
                AGENT_ID,
                [])

            obj = request.cls.catalog.create_grade_entry(form)

            request.cls.grade_entry_list.append(obj)
            request.cls.grade_entry_ids.append(obj.ident)
        request.cls.grade_entry_list = GradeEntryList(request.cls.grade_entry_list)"""


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
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.grade_entry_list = list()
    request.cls.grade_entry_ids = list()
    request.cls.gradebook_column_list = list()
    request.cls.gradebook_column_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'GRADING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test Gradebook'
        create_form.description = 'Test Gradebook for GradebookColumnLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_gradebook(create_form)
        create_form = request.cls.catalog.get_grade_system_form_for_create([])
        create_form.display_name = 'Test Grade System'
        create_form.description = 'Test Grade System for GradebookColumnLookupSession tests'
        create_form.based_on_grades = False
        create_form.lowest_numeric_score = 0
        create_form.highest_numeric_score = 100
        create_form.numeric_score_increment = 1
        request.cls.grade_system = request.cls.catalog.create_grade_system(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_gradebook_column_form_for_create([])
            create_form.display_name = 'Test GradebookColumn ' + str(num)
            create_form.description = 'Test GradebookColumn for GradebookColumnLookupSession tests'
            create_form.grade_system = request.cls.grade_system.ident
            obj = request.cls.catalog.create_gradebook_column(create_form)
            request.cls.gradebook_column_list.append(obj)
            request.cls.gradebook_column_ids.append(obj.ident)
        for num in range(0, 100):
            create_form = request.cls.catalog.get_grade_entry_form_for_create(request.cls.gradebook_column_ids[0], AGENT_ID, [])
            create_form.display_name = 'Test GradeEntry ' + str(num)
            create_form.description = 'Test GradeEntry for GradebookColumnLookupSession tests'
            create_form.set_score(float(num))
            object = request.cls.catalog.create_grade_entry(create_form)
            request.cls.grade_entry_list.append(object)
            request.cls.grade_entry_ids.append(object.ident)
        request.cls.object = request.cls.catalog.get_gradebook_column_summary(request.cls.gradebook_column_ids[0])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_gradebooks():
                for obj in catalog.get_grade_entries():
                    catalog.delete_grade_entry(obj.ident)
                for obj in catalog.get_gradebook_columns():
                    catalog.delete_gradebook_column(obj.ident)
                for obj in catalog.get_grade_systems():
                    catalog.delete_grade_system(obj.ident)
                request.cls.svc_mgr.delete_gradebook(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""

    get_gradebook_column_id = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.get_gradebook_column_id(), Id)
            assert str(self.object.get_gradebook_column_id()) == str(self.gradebook_column_ids[0])"""

    get_gradebook_column = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.get_gradebook_column(), GradebookColumn)
            assert str(self.object.get_gradebook_column().ident) == str(self.gradebook_column_ids[0])"""

    get_mean = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.get_mean(), Decimal)
            assert self.object.get_mean() == Decimal(49.5)"""

    get_median = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.get_median(), Decimal)
            assert self.object.get_median() == Decimal(49.5)"""

    get_rms = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.get_rms(), Decimal)
            assert self.object.get_rms() == Decimal('57.30183243143276652887614453')"""

    get_standard_deviation = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.get_standard_deviation(), Decimal)
            assert self.object.get_standard_deviation() == Decimal('28.86607004772211800433171979')"""

    get_sum = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.get_sum(), Decimal)
            assert self.object.get_sum() == Decimal('4950')"""


class GradebookColumnSummaryQuery:
    import_statements = [
        'from dlkit.json_.grading.queries import GradebookColumnSummaryQuery'
    ]

    # Until we figure out how to do Relationship init patterns properly:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.grade_entry_list = list()
    request.cls.grade_entry_ids = list()
    request.cls.gradebook_column_list = list()
    request.cls.gradebook_column_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'GRADING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test Gradebook'
        create_form.description = 'Test Gradebook for GradebookColumnLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_gradebook(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_grade_entries():
                request.cls.catalog.delete_grade_entry(obj.ident)
            for obj in request.cls.catalog.get_gradebook_columns():
                request.cls.catalog.delete_gradebook_column(obj.ident)
            for obj in request.cls.catalog.get_grade_systems():
                request.cls.catalog.delete_grade_system(obj.ident)
            request.cls.svc_mgr.delete_gradebook(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # Since the session isn't implemented, we just construct a GradebookColumnSummaryQuery directly
    if not is_never_authz(request.cls.service_config):
        request.cls.query = GradebookColumnSummaryQuery(runtime=request.cls.catalog._runtime)"""


class GradeEntryAdminSession:
    import_statements_pattern = [
        'from dlkit.abstract_osid.osid.objects import OsidForm',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.grade_entry_list = list()
    request.cls.grade_entry_ids = list()
    request.cls.gradebook_column_list = list()
    request.cls.gradebook_column_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'GRADING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test Gradebook'
        create_form.description = 'Test Gradebook for GradeEntryAdminSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_gradebook(create_form)
        create_form = request.cls.catalog.get_grade_system_form_for_create([])
        create_form.display_name = 'Test Grade System'
        create_form.description = 'Test Grade System for GradeEntryAdminSession tests'
        create_form.based_on_grades = False
        create_form.lowest_numeric_score = 0
        create_form.highest_numeric_score = 5
        create_form.numeric_score_increment = 0.25
        request.cls.grade_system = request.cls.catalog.create_grade_system(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_gradebook_column_form_for_create([])
            create_form.display_name = 'Test GradebookColumn ' + str(num)
            create_form.description = 'Test GradebookColumn for GradeEntryAdminSession tests'
            create_form.grade_system = request.cls.grade_system.ident
            obj = request.cls.catalog.create_gradebook_column(create_form)
            request.cls.gradebook_column_list.append(obj)
            request.cls.gradebook_column_ids.append(obj.ident)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_grade_entry_form_for_create(request.cls.gradebook_column_ids[num], AGENT_ID, [])
            create_form.display_name = 'Test GradeEntry ' + str(num)
            create_form.description = 'Test GradeEntry for GradeEntryAdminSession tests'
            object = request.cls.catalog.create_grade_entry(create_form)
            request.cls.grade_entry_list.append(object)
            request.cls.grade_entry_ids.append(object.ident)

        request.cls.form = request.cls.catalog.get_grade_entry_form_for_create(request.cls.gradebook_column_ids[0], AGENT_ID, [])
        request.cls.form.display_name = 'new GradeEntry'
        request.cls.form.description = 'description of GradeEntry'
        request.cls.form.genus_type = NEW_TYPE
        request.cls.osid_object = request.cls.catalog.create_grade_entry(request.cls.form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_grade_entries():
                request.cls.catalog.delete_grade_entry(obj.ident)
            for obj in request.cls.catalog.get_gradebook_columns():
                request.cls.catalog.delete_gradebook_column(obj.ident)
            for obj in request.cls.catalog.get_grade_systems():
                request.cls.catalog.delete_grade_system(obj.ident)
            request.cls.svc_mgr.delete_gradebook(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    get_grade_entry_form_for_create = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_grade_entry_form_for_create(self.gradebook_column_ids[0], AGENT_ID, [])
            assert isinstance(form, OsidForm)
            assert not form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_grade_entry_form_for_create(self.fake_id, AGENT_ID, [])"""

    delete_grade_entry = """
        if not is_never_authz(self.service_config):
            create_form = self.catalog.get_grade_entry_form_for_create(self.gradebook_column_ids[0], AGENT_ID, [])
            create_form.display_name = 'new GradeEntry'
            create_form.description = 'description of GradeEntry'
            create_form.genus_type = NEW_TYPE
            osid_object = self.catalog.create_grade_entry(create_form)
            self.catalog.delete_grade_entry(osid_object.ident)
            with pytest.raises(errors.NotFound):
                self.catalog.get_grade_entry(osid_object.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.delete_grade_entry(self.fake_id)"""


class GradebookQuery:
    import_statements = [
        'from dlkit.json_.grading.queries import GradebookQuery'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'GRADING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_gradebook_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_gradebook(create_form)
        request.cls.fake_id = Id('resource.Resource%3A1%40ODL.MIT.EDU')

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_gradebook(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # Since the session isn't implemented, we just construct a GradebookQuery directly
    if not is_never_authz(request.cls.service_config):
        request.cls.query = GradebookQuery(runtime=request.cls.catalog._runtime)"""


class GradebookHierarchySession:
    init = """
# Override this because spec doesn't have a method ``remove_child_gradebooks``
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'GRADING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.catalogs = dict()
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        for name in ['Root', 'Child 1', 'Child 2', 'Grandchild 1']:
            create_form = request.cls.svc_mgr.get_gradebook_form_for_create([])
            create_form.display_name = name
            create_form.description = 'Test Gradebook ' + name
            request.cls.catalogs[name] = request.cls.svc_mgr.create_gradebook(create_form)
        request.cls.svc_mgr.add_root_gradebook(request.cls.catalogs['Root'].ident)
        request.cls.svc_mgr.add_child_gradebook(request.cls.catalogs['Root'].ident, request.cls.catalogs['Child 1'].ident)
        request.cls.svc_mgr.add_child_gradebook(request.cls.catalogs['Root'].ident, request.cls.catalogs['Child 2'].ident)
        request.cls.svc_mgr.add_child_gradebook(request.cls.catalogs['Child 1'].ident, request.cls.catalogs['Grandchild 1'].ident)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.remove_child_gradebook(request.cls.catalogs['Child 1'].ident, request.cls.catalogs['Grandchild 1'].ident)
            request.cls.svc_mgr.remove_child_gradebook(request.cls.catalogs['Root'].ident, request.cls.catalogs['Child 1'].ident)
            request.cls.svc_mgr.remove_child_gradebook(request.cls.catalogs['Root'].ident, request.cls.catalogs['Child 2'].ident)
            request.cls.svc_mgr.remove_root_gradebook(request.cls.catalogs['Root'].ident)
            for cat_name in request.cls.catalogs:
                request.cls.svc_mgr.delete_gradebook(request.cls.catalogs[cat_name].ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.svc_mgr"""


class GradebookHierarchyDesignSession:
    init = """
# Override this because spec doesn't have a method ``remove_child_gradebooks``
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'GRADING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.catalogs = dict()
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        for name in ['Root', 'Child 1', 'Child 2', 'Grandchild 1']:
            create_form = request.cls.svc_mgr.get_gradebook_form_for_create([])
            create_form.display_name = name
            create_form.description = 'Test Gradebook ' + name
            request.cls.catalogs[name] = request.cls.svc_mgr.create_gradebook(create_form)
        request.cls.svc_mgr.add_root_gradebook(request.cls.catalogs['Root'].ident)
        request.cls.svc_mgr.add_child_gradebook(request.cls.catalogs['Root'].ident, request.cls.catalogs['Child 1'].ident)
        request.cls.svc_mgr.add_child_gradebook(request.cls.catalogs['Root'].ident, request.cls.catalogs['Child 2'].ident)
        request.cls.svc_mgr.add_child_gradebook(request.cls.catalogs['Child 1'].ident, request.cls.catalogs['Grandchild 1'].ident)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.remove_child_gradebook(request.cls.catalogs['Child 1'].ident, request.cls.catalogs['Grandchild 1'].ident)
            request.cls.svc_mgr.remove_child_gradebook(request.cls.catalogs['Root'].ident, request.cls.catalogs['Child 1'].ident)
            request.cls.svc_mgr.remove_child_gradebook(request.cls.catalogs['Root'].ident, request.cls.catalogs['Child 2'].ident)
            request.cls.svc_mgr.remove_root_gradebook(request.cls.catalogs['Root'].ident)
            for cat_name in request.cls.catalogs:
                request.cls.svc_mgr.delete_gradebook(request.cls.catalogs[cat_name].ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.svc_mgr"""


class GradeSystemLookupSession:
    # Override these locally for GradeSystem because with GradeSystemQuerySession implemented,
    #   the authz adapter will return an empty List instead of throwing PermissionDenied
    get_grade_system = """
        if not is_never_authz(self.service_config):
            self.catalog.use_isolated_gradebook_view()
            obj = self.catalog.get_grade_system(self.grade_system_list[0].ident)
            assert obj.ident == self.grade_system_list[0].ident
            self.catalog.use_federated_gradebook_view()
            obj = self.catalog.get_grade_system(self.grade_system_list[0].ident)
            assert obj.ident == self.grade_system_list[0].ident
        else:
            with pytest.raises(errors.NotFound):
                self.catalog.get_grade_system(self.fake_id)"""

    get_grade_systems_by_ids = """
        from dlkit.abstract_osid.grading.objects import GradeSystemList
        objects = self.catalog.get_grade_systems_by_ids(self.grade_system_ids)
        assert isinstance(objects, GradeSystemList)
        self.catalog.use_federated_gradebook_view()
        objects = self.catalog.get_grade_systems_by_ids(self.grade_system_ids)
        assert isinstance(objects, GradeSystemList)
        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0"""

    get_grade_systems_by_genus_type = """
        from dlkit.abstract_osid.grading.objects import GradeSystemList
        objects = self.catalog.get_grade_systems_by_genus_type(DEFAULT_GENUS_TYPE)
        assert isinstance(objects, GradeSystemList)
        self.catalog.use_federated_gradebook_view()
        objects = self.catalog.get_grade_systems_by_genus_type(DEFAULT_GENUS_TYPE)
        assert isinstance(objects, GradeSystemList)
        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0"""

    get_grade_systems_by_parent_genus_type = """
        from dlkit.abstract_osid.grading.objects import GradeSystemList
        if not is_never_authz(self.service_config):
            objects = self.catalog.get_grade_systems_by_parent_genus_type(DEFAULT_GENUS_TYPE)
            assert isinstance(objects, GradeSystemList)
            self.catalog.use_federated_gradebook_view()
            objects = self.catalog.get_grade_systems_by_parent_genus_type(DEFAULT_GENUS_TYPE)
            assert objects.available() == 0
            assert isinstance(objects, GradeSystemList)
        else:
            with pytest.raises(errors.Unimplemented):
                # because the never_authz "tries harder" and runs the actual query...
                #    whereas above the method itself in JSON returns an empty list
                self.catalog.get_grade_systems_by_parent_genus_type(DEFAULT_GENUS_TYPE)"""

    get_grade_systems_by_record_type = """
        from dlkit.abstract_osid.grading.objects import GradeSystemList
        objects = self.catalog.get_grade_systems_by_record_type(DEFAULT_TYPE)
        assert isinstance(objects, GradeSystemList)
        self.catalog.use_federated_gradebook_view()
        objects = self.catalog.get_grade_systems_by_record_type(DEFAULT_TYPE)
        assert objects.available() == 0
        assert isinstance(objects, GradeSystemList)"""

    get_grade_systems = """
        from dlkit.abstract_osid.grading.objects import GradeSystemList
        objects = self.catalog.get_grade_systems()
        assert isinstance(objects, GradeSystemList)
        self.catalog.use_federated_gradebook_view()
        objects = self.catalog.get_grade_systems()
        assert isinstance(objects, GradeSystemList)

        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0

    def test_get_grade_system_with_alias(self):
        if not is_never_authz(self.service_config):
            self.catalog.alias_grade_system(self.grade_system_ids[0], ALIAS_ID)
            obj = self.catalog.get_grade_system(ALIAS_ID)
            assert obj.get_id() == self.grade_system_ids[0]"""


class GradeSystemAdminSession:
    import_statements = [
        'from dlkit.abstract_osid.grading.objects import Grade',
        'from dlkit.abstract_osid.osid.objects import OsidForm'
    ]

    can_create_grade_with_record_types = """
        assert isinstance(self.session.can_create_grade_with_record_types(self.osid_object.ident,
                                                                          DEFAULT_TYPE),
                          bool)"""

    can_create_grades = """
        assert isinstance(self.session.can_create_grades(self.osid_object.ident),
                          bool)"""

    can_delete_grades = """
        assert isinstance(self.session.can_delete_grades(self.osid_object.ident),
                          bool)"""

    create_grade = """
        if not is_never_authz(self.service_config):
            assert self.osid_object.get_grades().available() == 0
            form = self.session.get_grade_form_for_create(
                self.osid_object.ident,
                [])
            form.display_name = 'Test object'
            grade = self.session.create_grade(form)
            assert isinstance(grade, Grade)
            assert grade.display_name.text == 'Test object'

            updated_grade_system = self.catalog.get_grade_system(self.osid_object.ident)
            assert updated_grade_system.get_grades().available() == 1
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.create_grade('foo')"""

    delete_grade = """
        if not is_never_authz(self.service_config):
            form = self.session.get_grade_form_for_create(
                self.osid_object.ident,
                [])
            form.display_name = 'Test object'
            grade = self.session.create_grade(form)
            assert isinstance(grade, Grade)
            assert grade.display_name.text == 'Test object'

            updated_grade_system = self.catalog.get_grade_system(self.osid_object.ident)
            assert updated_grade_system.get_grades().available() == 1

            self.session.delete_grade(grade.ident)

            updated_grade_system = self.catalog.get_grade_system(self.osid_object.ident)
            assert updated_grade_system.get_grades().available() == 0
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.delete_grade(self.fake_id)"""

    get_grade_form_for_create = """
        if not is_never_authz(self.service_config):
            form = self.session.get_grade_form_for_create(
                self.osid_object.ident,
                [])
            assert isinstance(form, OsidForm)
            assert not form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_grade_form_for_create(self.fake_id, [])"""

    get_grade_form_for_update = """
        if not is_never_authz(self.service_config):
            form = self.session.get_grade_form_for_create(
                self.osid_object.ident,
                [])
            grade = self.session.create_grade(form)
            form = self.session.get_grade_form_for_update(grade.ident)
            assert isinstance(form, OsidForm)
            assert form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_grade_form_for_update(self.fake_id)"""

    update_grade = """
        if not is_never_authz(self.service_config):
            assert self.osid_object.get_grades().available() == 0
            form = self.session.get_grade_form_for_create(
                self.osid_object.ident,
                [])
            form.display_name = 'Test object'
            grade = self.session.create_grade(form)
            assert isinstance(grade, Grade)
            assert grade.display_name.text == 'Test object'

            form = self.session.get_grade_form_for_update(grade.ident)
            form.display_name = 'new name'
            grade = self.session.update_grade(form)

            assert isinstance(grade, Grade)
            assert grade.display_name.text == 'new name'

            updated_grade_system = self.catalog.get_grade_system(self.osid_object.ident)
            assert updated_grade_system.get_grades().available() == 1
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.update_grade('foo')"""
