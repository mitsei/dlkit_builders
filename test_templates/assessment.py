
class AssessmentSession:
    import_statements = [
        'import datetime',
        'from dlkit.abstract_osid.assessment.objects import Bank, Answer, AnswerList, AnswerForm',
        'from dlkit.abstract_osid.assessment.objects import Question, QuestionList',
        'from dlkit.abstract_osid.assessment.objects import ResponseList',
        'from dlkit.abstract_osid.assessment.objects import AssessmentSection, AssessmentSectionList',
        'from dlkit.abstract_osid.assessment.rules import Response',
        'from dlkit.primordium.calendaring.primitives import DateTime',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.records import registry',
        'SEQUENCE_ASSESSMENT = Type(**registry.ASSESSMENT_RECORD_TYPES["simple-child-sequencing"])'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([SEQUENCE_ASSESSMENT])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)

        for number in ['One', 'Two', 'Three', 'Four']:
            ifc = request.cls.catalog.get_item_form_for_create([])
            ifc.set_display_name('Test Assessment Item ' + number)
            ifc.set_description('This is a Test Item Called Number ' + number)
            test_item = request.cls.catalog.create_item(ifc)
            form = request.cls.catalog.get_question_form_for_create(test_item.ident, [])
            request.cls.catalog.create_question(form)

            if number == 'One':
                form = request.cls.catalog.get_answer_form_for_create(test_item.ident, [])
                request.cls.catalog.create_answer(form)

            request.cls.catalog.add_item(request.cls.assessment.ident, test_item.ident)

        form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
        request.cls.assessment_offered = request.cls.catalog.create_assessment_offered(form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    request.cls.session = request.cls.catalog

    if not is_never_authz(request.cls.service_config):
        form = request.cls.catalog.get_assessment_taken_form_for_create(request.cls.assessment_offered.ident, [])
        request.cls.taken = request.cls.catalog.create_assessment_taken(form)

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments():
                for offered in request.cls.catalog.get_assessments_offered_for_assessment(obj.ident):
                    for taken in request.cls.catalog.get_assessments_taken_for_assessment_offered(offered.ident):
                        request.cls.catalog.delete_assessment_taken(taken.ident)
                    request.cls.catalog.delete_assessment_offered(offered.ident)
                request.cls.catalog.delete_assessment(obj.ident)
            for item in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(item.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(test_tear_down)"""

    get_bank = """
        # this test should not be needed....
        if not is_never_authz(self.service_config):
            assert isinstance(self.catalog, Bank)"""

    can_take_assessments = """
        assert isinstance(self.session.can_take_assessments(), bool)"""

    get_assessment_section = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            test_section = self.session.get_assessment_section(section.ident)
            assert isinstance(test_section, AssessmentSection)
            assert str(test_section.ident) == str(section.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_assessment_section(self.fake_id)"""

    get_assessment_sections = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            test_sections = self.session.get_assessment_sections(self.taken.ident)
            assert isinstance(test_sections, AssessmentSectionList)
            assert test_sections.available() == 1
            first_section = test_sections.next()
            assert isinstance(first_section, AssessmentSection)
            assert str(first_section.ident) == str(section.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_assessment_sections(self.fake_id)"""

    get_first_assessment_section = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            assert isinstance(section, AssessmentSection)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_first_assessment_section(self.fake_id)"""

    submit_response = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()

            assert 'missingResponse' in section._my_map['questions'][0]['responses'][0]
            assert 0 == section._my_map['questions'][0]['responses'][0]['missingResponse']

            form = self.session.get_response_form(section.ident, first_question.ident)
            self.session.submit_response(section.ident, first_question.ident, form)
            section = self.catalog.get_assessment_section(section.ident)

            assert 'missingResponse' not in section._my_map['questions'][0]['responses'][0]
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.submit_response(self.fake_id, self.fake_id, 'foo')"""

    clear_response = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()

            assert 'missingResponse' in section._my_map['questions'][0]['responses'][0]
            assert 0 == section._my_map['questions'][0]['responses'][0]['missingResponse']

            form = self.session.get_response_form(section.ident, first_question.ident)
            self.session.submit_response(section.ident, first_question.ident, form)
            section = self.catalog.get_assessment_section(section.ident)

            assert 'missingResponse' not in section._my_map['questions'][0]['responses'][0]

            self.session.clear_response(section.ident, first_question.ident)
            section = self.catalog.get_assessment_section(section.ident)

            assert 'missingResponse' in section._my_map['questions'][0]['responses'][0]
            assert 1 == section._my_map['questions'][0]['responses'][0]['missingResponse']
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.clear_response(self.fake_id, self.fake_id)"""

    skip_item = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()

            assert 'missingResponse' in section._my_map['questions'][0]['responses'][0]
            assert 0 == section._my_map['questions'][0]['responses'][0]['missingResponse']

            self.session.skip_item(section.ident, first_question.ident)
            section = self.catalog.get_assessment_section(section.ident)

            assert 'missingResponse' in section._my_map['questions'][0]['responses'][0]
            assert 1 == section._my_map['questions'][0]['responses'][0]['missingResponse']
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.skip_item(self.fake_id, self.fake_id)"""

    finish_assessment = """
        if not is_never_authz(self.service_config):
            future_start = DateTime.utcnow() + datetime.timedelta(days=1)
            form = self.catalog.get_assessment_offered_form_for_create(self.assessment.ident, [])
            form.set_start_time(DateTime(**{
                'year': future_start.year,
                'month': future_start.month,
                'day': future_start.day,
                'hour': future_start.hour,
                'minute': future_start.minute,
                'second': future_start.second
            }))
            future_offered = self.catalog.create_assessment_offered(form)
            form = self.catalog.get_assessment_taken_form_for_create(future_offered.ident, [])
            future_taken = self.catalog.create_assessment_taken(form)
            with pytest.raises(errors.IllegalState):
                self.session.finish_assessment(future_taken.ident)

            assert self.taken._my_map['completionTime'] is None
            self.session.finish_assessment(self.taken.ident)
            taken = self.catalog.get_assessment_taken(self.taken.ident)
            assert taken._my_map['completionTime'] is not None
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.finish_assessment(self.fake_id)"""

    finish_assessment_section = """
        if not is_never_authz(self.service_config):
            future_start = DateTime.utcnow() + datetime.timedelta(days=1)
            form = self.catalog.get_assessment_offered_form_for_create(self.assessment.ident, [])
            form.set_start_time(DateTime(**{
                'year': future_start.year,
                'month': future_start.month,
                'day': future_start.day,
                'hour': future_start.hour,
                'minute': future_start.minute,
                'second': future_start.second
            }))
            future_offered = self.catalog.create_assessment_offered(form)
            form = self.catalog.get_assessment_taken_form_for_create(future_offered.ident, [])
            future_taken = self.catalog.create_assessment_taken(form)
            with pytest.raises(errors.IllegalState):
                self.catalog.get_first_assessment_section(future_taken.ident)

            first_section = self.catalog.get_first_assessment_section(self.taken.ident)
            assert 'completionTime' not in first_section._my_map
            self.session.finish_assessment_section(first_section.ident)

            with pytest.raises(errors.IllegalState):
                # it is over, so can't GET the section now
                self.catalog.get_assessment_section(first_section.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.finish_assessment_section(self.fake_id)"""

    has_assessment_begun = """
        if not is_never_authz(self.service_config):
            future_start = DateTime.utcnow() + datetime.timedelta(days=1)
            form = self.catalog.get_assessment_offered_form_for_create(self.assessment.ident, [])
            form.set_start_time(DateTime(**{
                'year': future_start.year,
                'month': future_start.month,
                'day': future_start.day,
                'hour': future_start.hour,
                'minute': future_start.minute,
                'second': future_start.second
            }))
            future_offered = self.catalog.create_assessment_offered(form)
            form = self.catalog.get_assessment_taken_form_for_create(future_offered.ident, [])
            future_taken = self.catalog.create_assessment_taken(form)
            assert not self.session.has_assessment_begun(future_taken.ident)

            assert self.session.has_assessment_begun(self.taken.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.has_assessment_begun(self.fake_id)"""

    has_assessment_section_begun = """
        if not is_never_authz(self.service_config):
            future_start = DateTime.utcnow() + datetime.timedelta(days=1)
            form = self.catalog.get_assessment_offered_form_for_create(self.assessment.ident, [])
            form.set_start_time(DateTime(**{
                'year': future_start.year,
                'month': future_start.month,
                'day': future_start.day,
                'hour': future_start.hour,
                'minute': future_start.minute,
                'second': future_start.second
            }))
            future_offered = self.catalog.create_assessment_offered(form)
            form = self.catalog.get_assessment_taken_form_for_create(future_offered.ident, [])
            future_taken = self.catalog.create_assessment_taken(form)

            with pytest.raises(errors.IllegalState):
                # cannot even get the sectionId to call the method
                self.catalog.get_first_assessment_section(future_taken.ident)

            section = self.catalog.get_first_assessment_section(self.taken.ident)
            assert self.session.has_assessment_section_begun(section.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.has_assessment_section_begun(self.fake_id)"""

    is_assessment_over = """
        # There are also other conditions that flag "over", but are not
        # tested here. Like if the offered goes past the deadline...so we
        # would have to do a time.sleep(). TODO: add those tests in.

        if not is_never_authz(self.service_config):
            assert not self.session.is_assessment_over(self.taken.ident)
            self.session.finish_assessment(self.taken.ident)
            assert self.session.is_assessment_over(self.taken.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.is_assessment_over(self.fake_id)"""

    is_assessment_section_over = """
        # There are also other conditions that flag "over", but are not
        # tested here. Like if the offered goes past the deadline...so we
        # would have to do a time.sleep(). TODO: add those tests in.

        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)

            assert not self.session.is_assessment_section_over(section.ident)
            self.session.finish_assessment_section(section.ident)
            assert self.session.is_assessment_section_over(section.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.is_assessment_section_over(self.fake_id)"""

    get_answers = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()
            second_question = questions.next()

            with pytest.raises(errors.IllegalState):
                self.session.get_answers(section.ident, second_question.ident)

            form = self.session.get_response_form(section.ident, first_question.ident)
            self.session.submit_response(section.ident, first_question.ident, form)

            answers = self.session.get_answers(section.ident, first_question.ident)
            assert isinstance(answers, AnswerList)
            assert answers.available() == 1
            assert isinstance(answers.next(), Answer)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_answers(self.fake_id, self.fake_id)"""

    is_answer_available = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()
            second_question = questions.next()

            assert not self.session.is_answer_available(section.ident,
                                                        second_question.ident)

            form = self.session.get_response_form(section.ident, first_question.ident)
            self.session.submit_response(section.ident, first_question.ident, form)

            answers = self.session.get_answers(section.ident, first_question.ident)
            assert isinstance(answers, AnswerList)
            assert self.session.is_answer_available(section.ident,
                                                    first_question.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.is_answer_available(self.fake_id, self.fake_id)"""

    get_first_question = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()

            test_question = self.session.get_first_question(section.ident)
            assert isinstance(test_question, Question)
            assert str(first_question.ident) == str(test_question.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_first_question(self.fake_id)"""

    get_first_unanswered_question = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()
            second_question = questions.next()

            unanswered_question = self.session.get_first_unanswered_question(section.ident)
            assert isinstance(unanswered_question, Question)
            assert str(unanswered_question.ident) == str(first_question.ident)

            form = self.session.get_response_form(section.ident, first_question.ident)
            self.session.submit_response(section.ident, first_question.ident, form)

            unanswered_question = self.session.get_first_unanswered_question(section.ident)
            assert isinstance(unanswered_question, Question)
            assert str(unanswered_question.ident) == str(second_question.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_first_unanswered_question(self.fake_id)"""

    is_question_answered = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()

            assert not self.session.is_question_answered(section.ident,
                                                         first_question.ident)

            form = self.session.get_response_form(section.ident, first_question.ident)
            self.session.submit_response(section.ident, first_question.ident, form)

            assert self.session.is_question_answered(section.ident,
                                                     first_question.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.is_question_answered(self.fake_id, self.fake_id)"""

    get_incomplete_assessment_sections = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()

            test_sections = self.session.get_incomplete_assessment_sections(self.taken.ident)
            assert isinstance(test_sections, AssessmentSectionList)
            assert test_sections.available() == 1
            first_section = test_sections.next()
            assert isinstance(first_section, AssessmentSection)
            assert str(first_section.ident) == str(section.ident)

            for question in questions:
                form = self.session.get_response_form(section.ident, question.ident)
                self.session.submit_response(section.ident, question.ident, form)

            self.session._provider_sessions = {}  # need to get rid of the cached taken
            test_sections = self.session.get_incomplete_assessment_sections(self.taken.ident)
            assert isinstance(test_sections, AssessmentSectionList)
            assert test_sections.available() == 0
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_incomplete_assessment_sections(self.fake_id)"""

    is_assessment_section_complete = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            total_questions = questions.available()

            assert not self.session.is_assessment_section_complete(section.ident)

            for index, question in enumerate(questions):
                form = self.session.get_response_form(section.ident, question.ident)
                self.session.submit_response(section.ident, question.ident, form)
                if index < (total_questions - 1):
                    assert not self.session.is_assessment_section_complete(section.ident)
                else:
                    assert self.session.is_assessment_section_complete(section.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.is_assessment_section_complete(self.fake_id)"""

    get_next_assessment_section = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            with pytest.raises(errors.IllegalState):
                self.session.get_next_assessment_section(section.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_next_assessment_section(self.fake_id)"""

    get_previous_assessment_section = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            with pytest.raises(errors.IllegalState):
                self.session.get_previous_assessment_section(section.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_previous_assessment_section(self.fake_id)"""

    has_next_assessment_section = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            assert not self.session.has_next_assessment_section(section.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.has_next_assessment_section(self.fake_id)"""

    has_previous_assessment_section = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            assert not self.session.has_previous_assessment_section(section.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.has_previous_assessment_section(self.fake_id)"""

    get_next_question = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()
            second_question = questions.next()
            third_question = questions.next()
            fourth_question = questions.next()

            test_question = self.session.get_next_question(section.ident,
                                                           first_question.ident)
            assert isinstance(test_question, Question)
            assert str(second_question.ident) == str(test_question.ident)

            with pytest.raises(errors.IllegalState):
                self.session.get_next_question(section.ident, fourth_question.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_next_question(self.fake_id, self.fake_id)"""

    has_next_question = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()
            second_question = questions.next()
            third_question = questions.next()
            fourth_question = questions.next()

            assert self.session.has_next_question(section.ident,
                                                  first_question.ident)
            assert not self.session.has_next_question(section.ident,
                                                      fourth_question.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.has_next_question(self.fake_id, self.fake_id)"""

    get_previous_question = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()
            second_question = questions.next()
            third_question = questions.next()
            fourth_question = questions.next()

            test_question = self.session.get_previous_question(section.ident,
                                                               fourth_question.ident)
            assert isinstance(test_question, Question)
            assert str(third_question.ident) == str(test_question.ident)

            with pytest.raises(errors.IllegalState):
                self.session.get_previous_question(section.ident, first_question.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_previous_question(self.fake_id, self.fake_id)"""

    has_previous_question = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()
            second_question = questions.next()
            third_question = questions.next()
            fourth_question = questions.next()

            assert self.session.has_previous_question(section.ident,
                                                      fourth_question.ident)
            assert not self.session.has_previous_question(section.ident,
                                                          first_question.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.has_previous_question(self.fake_id, self.fake_id)"""

    get_next_unanswered_question = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()
            second_question = questions.next()
            third_question = questions.next()
            fourth_question = questions.next()

            test_question = self.session.get_next_unanswered_question(section.ident,
                                                                      first_question.ident)
            assert isinstance(test_question, Question)
            assert str(second_question.ident) == str(test_question.ident)

            form = self.session.get_response_form(section.ident, second_question.ident)
            self.session.submit_response(section.ident, second_question.ident, form)

            test_question = self.session.get_next_unanswered_question(section.ident,
                                                                      first_question.ident)
            assert isinstance(test_question, Question)
            assert str(third_question.ident) == str(test_question.ident)

            with pytest.raises(errors.IllegalState):
                self.session.get_next_unanswered_question(section.ident,
                                                          fourth_question.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_next_unanswered_question(self.fake_id, self.fake_id)"""

    has_next_unanswered_question = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()
            second_question = questions.next()
            third_question = questions.next()
            fourth_question = questions.next()

            assert self.session.has_next_unanswered_question(section.ident,
                                                             first_question.ident)

            form = self.session.get_response_form(section.ident, second_question.ident)
            self.session.submit_response(section.ident, second_question.ident, form)

            assert self.session.has_next_unanswered_question(section.ident,
                                                             first_question.ident)
            assert not self.session.has_next_unanswered_question(section.ident,
                                                                 fourth_question.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.has_next_unanswered_question(self.fake_id, self.fake_id)"""

    get_previous_unanswered_question = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()
            second_question = questions.next()
            third_question = questions.next()
            fourth_question = questions.next()

            test_question = self.session.get_previous_unanswered_question(section.ident,
                                                                          fourth_question.ident)
            assert isinstance(test_question, Question)
            assert str(third_question.ident) == str(test_question.ident)

            form = self.session.get_response_form(section.ident, third_question.ident)
            self.session.submit_response(section.ident, third_question.ident, form)

            test_question = self.session.get_previous_unanswered_question(section.ident,
                                                                          fourth_question.ident)
            assert isinstance(test_question, Question)
            assert str(second_question.ident) == str(test_question.ident)

            with pytest.raises(errors.IllegalState):
                self.session.get_previous_unanswered_question(section.ident,
                                                              first_question.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_previous_unanswered_question(self.fake_id, self.fake_id)"""

    has_previous_unanswered_question = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()
            second_question = questions.next()
            third_question = questions.next()
            fourth_question = questions.next()

            assert self.session.has_previous_unanswered_question(section.ident,
                                                                 fourth_question.ident)

            form = self.session.get_response_form(section.ident, third_question.ident)
            self.session.submit_response(section.ident, third_question.ident, form)

            assert self.session.has_previous_unanswered_question(section.ident,
                                                                 fourth_question.ident)
            assert not self.session.has_previous_unanswered_question(section.ident,
                                                                     first_question.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.has_previous_unanswered_question(self.fake_id, self.fake_id)"""

    get_question = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()

            test_question = self.session.get_question(section.ident, first_question.ident)
            assert isinstance(test_question, Question)
            assert str(test_question.ident) == str(first_question.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_question(self.fake_id, self.fake_id)"""

    get_questions = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()

            test_questions = self.session.get_questions(section.ident)
            assert isinstance(test_questions, QuestionList)
            assert test_questions.available() == 4
            first_test_question = test_questions.next()
            assert isinstance(first_test_question, Question)
            assert str(first_test_question.ident) == str(first_question.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_questions(self.fake_id)"""

    get_unanswered_questions = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            question_ids = [q.ident for q in questions]

            test_questions = self.session.get_unanswered_questions(section.ident)
            assert isinstance(test_questions, QuestionList)
            assert test_questions.available() == 4
            test_question_ids = [q.ident for q in test_questions]
            assert question_ids == test_question_ids

            form = self.session.get_response_form(section.ident, question_ids[1])
            self.session.submit_response(section.ident, question_ids[1], form)

            test_questions = self.session.get_unanswered_questions(section.ident)
            assert isinstance(test_questions, QuestionList)
            assert test_questions.available() == 3
            test_question_ids = [q.ident for q in test_questions]
            assert question_ids[1] not in test_question_ids
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_unanswered_questions(self.fake_id)"""

    get_response = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()

            test_response = self.session.get_response(section.ident, first_question.ident)
            assert isinstance(test_response, Response)

            with pytest.raises(errors.IllegalState):
                test_response.object_map

            form = self.session.get_response_form(section.ident, first_question.ident)
            self.session.submit_response(section.ident, first_question.ident, form)

            test_response = self.session.get_response(section.ident, first_question.ident)
            assert isinstance(test_response, Response)

            test_response.object_map
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_response(self.fake_id, self.fake_id)"""

    get_responses = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()

            test_responses = self.session.get_responses(section.ident)
            assert isinstance(test_responses, ResponseList)
            assert test_responses.available() == 4
            first_response = test_responses.next()
            assert isinstance(first_response, Response)

            with pytest.raises(errors.IllegalState):
                first_response.object_map
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_responses(self.fake_id)"""

    get_response_form = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            first_question = questions.next()

            form = self.session.get_response_form(section.ident, first_question.ident)
            assert isinstance(form, AnswerForm)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_response_form(self.fake_id, self.fake_id)"""

    has_unanswered_questions = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()
            total_questions = questions.available()

            assert self.session.has_unanswered_questions(section.ident)

            for index, question in enumerate(questions):
                form = self.session.get_response_form(section.ident, question.ident)
                self.session.submit_response(section.ident, question.ident, form)
                if index < (total_questions - 1):
                    assert self.session.has_unanswered_questions(section.ident)
                else:
                    assert not self.session.has_unanswered_questions(section.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.has_unanswered_questions(self.fake_id)"""

    requires_synchronous_responses = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            assert not self.session.requires_synchronous_responses(section.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.requires_synchronous_responses(self.fake_id)"""

    requires_synchronous_sections = """
        if not is_never_authz(self.service_config):
            assert not self.session.requires_synchronous_sections(self.taken.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.requires_synchronous_sections(self.fake_id)"""


class AssessmentResultsSession:
    import_statements = [
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.records import registry',
        'SEQUENCE_ASSESSMENT = Type(**registry.ASSESSMENT_RECORD_TYPES["simple-child-sequencing"])'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentResultsSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([SEQUENCE_ASSESSMENT])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentResultsSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)

        for number in ['One', 'Two', 'Three', 'Four']:
            ifc = request.cls.catalog.get_item_form_for_create([])
            ifc.set_display_name('Test Assessment Item ' + number)
            ifc.set_description('This is a Test Item Called Number ' + number)
            test_item = request.cls.catalog.create_item(ifc)

            form = request.cls.catalog.get_question_form_for_create(test_item.ident, [])
            request.cls.catalog.create_question(form)

            request.cls.catalog.add_item(request.cls.assessment.ident, test_item.ident)

        form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
        request.cls.assessment_offered = request.cls.catalog.create_assessment_offered(form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments():
                for offered in request.cls.catalog.get_assessments_offered_for_assessment(obj.ident):
                    for taken in request.cls.catalog.get_assessments_taken_for_assessment_offered(offered.ident):
                        request.cls.catalog.delete_assessment_taken(taken.ident)
                    request.cls.catalog.delete_assessment_offered(offered.ident)
                request.cls.catalog.delete_assessment(obj.ident)
            for item in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(item.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.svc_mgr.get_assessment_results_session(proxy=request.cls.catalog._proxy)
    if not is_never_authz(request.cls.service_config):
        form = request.cls.catalog.get_assessment_taken_form_for_create(request.cls.assessment_offered.ident, [])
        request.cls.taken = request.cls.catalog.create_assessment_taken(form)"""

    are_results_available = """
        if not is_never_authz(self.service_config):
            assert not self.session.are_results_available(self.assessment.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.are_results_available(self.fake_id)"""

    can_access_assessment_results = """
        assert isinstance(self.session.can_access_assessment_results(), bool)"""

    get_grade_entries = """
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.IllegalState):
                self.session.get_grade_entries(self.assessment.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_grade_entries(self.fake_id)"""

    get_items = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            section.get_questions()
            assert self.session.get_items(self.taken.ident).available() == 4
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_items(self.fake_id)"""

    get_responses = """
        if not is_never_authz(self.service_config):
            section = self.catalog.get_first_assessment_section(self.taken.ident)
            questions = section.get_questions()

            test_responses = self.session.get_responses(self.taken.ident)
            assert isinstance(test_responses, ResponseList)
            assert test_responses.available() == 4
            first_response = test_responses.next()
            assert isinstance(first_response, Response)

            with pytest.raises(errors.IllegalState):
                first_response.object_map
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_responses(self.fake_id)"""


class ItemAdminSession:

    import_statements = [
        'from dlkit.abstract_osid.assessment import objects',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})',
        'NEW_TYPE_2 = Type(**{\'identifier\': \'NEW 2\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})',
        'from dlkit.primordium.id.primitives import Id',
        'ALIAS_ID = Id(**{\'identifier\': \'ALIAS\', \'namespace\': \'ALIAS\', \'authority\': \'ALIAS\'})',
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for ItemAdminSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments():
                for offered in request.cls.catalog.get_assessments_offered_for_assessment(obj.ident):
                    for taken in request.cls.catalog.get_assessments_taken_for_assessment_offered(offered.ident):
                        request.cls.catalog.delete_assessment_taken(taken.ident)
                    request.cls.catalog.delete_assessment_offered(offered.ident)
                request.cls.catalog.delete_assessment(obj.ident)
            for item in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(item.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.catalog.get_item_form_for_create([])
        create_form.display_name = 'new Item'
        create_form.description = 'description of Item'
        create_form.set_genus_type(NEW_TYPE)
        request.cls.osid_object = request.cls.catalog.create_item(create_form)
    request.cls.session = request.cls.catalog"""

    create_answer = """
        if not is_never_authz(self.service_config):
            assert self.osid_object.get_answers().available() == 0
            form = self.session.get_answer_form_for_create(self.osid_object.ident, [])
            self.session.create_answer(form)
            updated_item = self.catalog.get_item(self.osid_object.ident)
            assert updated_item.get_answers().available() == 1
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.create_answer('foo')"""

    create_question = """
        if not is_never_authz(self.service_config):
            with pytest.raises(TypeError):
                # question_map = dict(self._my_map['question'])
                # TypeError: 'NoneType' object is not iterable
                self.osid_object.get_question()

            form = self.session.get_question_form_for_create(self.osid_object.ident, [])
            self.session.create_question(form)
            updated_item = self.catalog.get_item(self.osid_object.ident)
            assert isinstance(updated_item.get_question(), Question)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.create_question('foo')"""

    delete_answer = """
        if not is_never_authz(self.service_config):
            assert self.osid_object.get_answers().available() == 0
            form = self.session.get_answer_form_for_create(self.osid_object.ident, [])
            answer = self.session.create_answer(form)
            updated_item = self.catalog.get_item(self.osid_object.ident)
            assert updated_item.get_answers().available() == 1

            with pytest.raises(errors.NotFound):
                self.session.delete_answer(Id('fake.Package%3A000000000000000000000000%40ODL.MIT.EDU'))

            self.session.delete_answer(answer.ident)
            updated_item = self.catalog.get_item(self.osid_object.ident)
            assert updated_item.get_answers().available() == 0
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.delete_answer(self.fake_id)"""

    delete_question = """
        if not is_never_authz(self.service_config):
            with pytest.raises(TypeError):
                # question_map = dict(self._my_map['question'])
                # TypeError: 'NoneType' object is not iterable
                self.osid_object.get_question()

            form = self.session.get_question_form_for_create(self.osid_object.ident, [])
            question = self.session.create_question(form)
            updated_item = self.catalog.get_item(self.osid_object.ident)
            assert isinstance(updated_item.get_question(), Question)

            with pytest.raises(errors.NotFound):
                self.session.delete_question(Id('fake.Package%3A000000000000000000000000%40ODL.MIT.EDU'))

            self.session.delete_question(question.ident)
            updated_item = self.catalog.get_item(self.osid_object.ident)

            with pytest.raises(TypeError):
                updated_item.get_question()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.delete_question(self.fake_id)"""

    get_answer_form_for_create = """
        if not is_never_authz(self.service_config):
            form = self.session.get_answer_form_for_create(self.osid_object.ident, [])
            assert isinstance(form, objects.AnswerForm)
            assert not form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_answer_form_for_create(self.fake_id, [])"""

    get_question_form_for_create = """
        if not is_never_authz(self.service_config):
            form = self.session.get_question_form_for_create(self.osid_object.ident, [])
            assert isinstance(form, objects.QuestionForm)
            assert not form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_question_form_for_create(self.fake_id, [])"""

    get_answer_form_for_update = """
        if not is_never_authz(self.service_config):
            form = self.session.get_answer_form_for_create(self.osid_object.ident, [])
            answer = self.session.create_answer(form)

            form = self.session.get_answer_form_for_update(answer.ident)
            assert isinstance(form, objects.AnswerForm)
            assert form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_answer_form_for_update(self.fake_id)"""

    get_question_form_for_update = """
        if not is_never_authz(self.service_config):
            form = self.session.get_question_form_for_create(self.osid_object.ident, [])
            question = self.session.create_question(form)

            form = self.session.get_question_form_for_update(question.ident)
            assert isinstance(form, objects.QuestionForm)
            assert form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_question_form_for_update(self.fake_id)"""

    update_answer = """
        if not is_never_authz(self.service_config):
            form = self.session.get_answer_form_for_create(self.osid_object.ident, [])
            form.display_name = 'first name'
            answer = self.session.create_answer(form)
            assert answer.display_name.text == 'first name'

            form = self.session.get_answer_form_for_update(answer.ident)
            form.display_name = 'second name'
            answer = self.session.update_answer(form)
            assert isinstance(answer, objects.Answer)
            assert answer.display_name.text == 'second name'
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.update_answer('foo')"""

    update_question = """
        if not is_never_authz(self.service_config):
            form = self.session.get_question_form_for_create(self.osid_object.ident, [])
            question = self.session.create_question(form)
            assert question.display_name.text == 'new Item'

            form = self.session.get_question_form_for_update(question.ident)
            form.display_name = 'second name'
            question = self.session.update_question(form)
            assert isinstance(question, objects.Question)
            assert question.display_name.text == 'second name'
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.update_question('foo')"""


class ItemBankSession:

    import_statements = [
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})',
        'NEW_TYPE_2 = Type(**{\'identifier\': \'NEW 2\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})',
        'from dlkit.primordium.id.primitives import Id',
        'ALIAS_ID = Id(**{\'identifier\': \'ALIAS\', \'namespace\': \'ALIAS\', \'authority\': \'ALIAS\'})',
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.item_list = list()
    request.cls.item_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for ItemBankSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank for Assignment'
        create_form.description = 'Test Bank for ItemBankSession tests assignment'
        request.cls.assigned_catalog = request.cls.svc_mgr.create_bank(create_form)
        for num in [0, 1, 2]:
            create_form = request.cls.catalog.get_item_form_for_create([])
            create_form.display_name = 'Test Item ' + str(num)
            create_form.description = 'Test Item for ItemBankSession tests'
            obj = request.cls.catalog.create_item(create_form)
            request.cls.item_list.append(obj)
            request.cls.item_ids.append(obj.ident)
        request.cls.svc_mgr.assign_item_to_bank(
            request.cls.item_ids[1], request.cls.assigned_catalog.ident)
        request.cls.svc_mgr.assign_item_to_bank(
            request.cls.item_ids[2], request.cls.assigned_catalog.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.unassign_item_from_bank(
                request.cls.item_ids[1], request.cls.assigned_catalog.ident)
            request.cls.svc_mgr.unassign_item_from_bank(
                request.cls.item_ids[2], request.cls.assigned_catalog.ident)
            for obj in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.assigned_catalog.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.svc_mgr"""


class AssessmentAdminSession:

    import_statements = [
    ]


class AssessmentOfferedLookupSession:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.assessment_offered_list = list()
    request.cls.assessment_offered_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentOfferedLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedLookupSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
            create_form.display_name = 'Test AssessmentOffered ' + str(num)
            create_form.description = 'Test AssessmentOffered for AssessmentOfferedLookupSession tests'
            obj = request.cls.catalog.create_assessment_offered(create_form)
            request.cls.assessment_offered_list.append(obj)
            request.cls.assessment_offered_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments_offered():
                request.cls.catalog.delete_assessment_offered(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""


class AssessmentTakenLookupSession:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.assessment_taken_list = list()
    request.cls.assessment_taken_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentTakenLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentTakenLookupSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        create_form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
        create_form.display_name = 'Test AssessmentOffered'
        create_form.description = 'Test AssessmentOffered for AssessmentTakenLookupSession tests'
        request.cls.assessment_offered = request.cls.catalog.create_assessment_offered(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_assessment_taken_form_for_create(request.cls.assessment_offered.ident, [])
            create_form.display_name = 'Test AssessmentTaken ' + str(num)
            create_form.description = 'Test AssessmentTaken for AssessmentTakenLookupSession tests'
            obj = request.cls.catalog.create_assessment_taken(create_form)
            request.cls.assessment_taken_list.append(obj)
            request.cls.assessment_taken_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_banks():
                for obj in catalog.get_assessments():
                    for offered in catalog.get_assessments_offered_for_assessment(obj.ident):
                        for taken in catalog.get_assessments_taken_for_assessment_offered(offered.ident):
                            catalog.delete_assessment_taken(taken.ident)
                        catalog.delete_assessment_offered(offered.ident)
                    catalog.delete_assessment(obj.ident)
                for obj in catalog.get_items():
                    catalog.delete_item(obj.ident)
                request.cls.svc_mgr.delete_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    # This is hand built, but there may be a pattern to try to map, specifically
    # getting objects for another package object and a persisted id thingy
    get_assessments_taken_for_taker_and_assessment_offered = """
        from dlkit.abstract_osid.assessment.objects import AssessmentTakenList
        if not is_never_authz(self.service_config):
            takens = self.session.get_assessments_taken_for_taker_and_assessment_offered(
                self.catalog._proxy.get_effective_agent_id(),
                self.assessment_offered.ident)
            assert isinstance(takens, AssessmentTakenList)
            assert takens.available() == 2
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_assessments_taken_for_taker_and_assessment_offered(
                    self.fake_id,
                    self.fake_id)"""

    get_assessments_taken_for_assessment = """
        from dlkit.abstract_osid.assessment.objects import AssessmentTakenList
        if not is_never_authz(self.service_config):
            takens = self.session.get_assessments_taken_for_assessment(self.assessment.ident)
            assert isinstance(takens, AssessmentTakenList)
            assert takens.available() == 2
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_assessments_taken_for_assessment(self.fake_id)"""


class AssessmentTakenAdminSession:

    import_statements = [
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.abstract_osid.assessment.objects import AssessmentTaken',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})',
        'NEW_TYPE_2 = Type(**{\'identifier\': \'NEW 2\', \'namespace\': \'MINE 2\', \'authority\': \'YOURS 2\'})'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentTakenAdminSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentTakenAdminSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        create_form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
        create_form.display_name = 'Test AssessmentOffered'
        create_form.description = 'Test AssessmentOffered for AssessmentTakenAdminSession tests'
        obj = request.cls.catalog.create_assessment_offered(create_form)
        request.cls.assessment_offered = obj
        form = request.cls.catalog.get_assessment_taken_form_for_create(request.cls.assessment_offered.ident, [])
        form.display_name = 'new AssessmentTaken'
        form.description = 'description of AssessmentTaken'
        form.set_genus_type(NEW_TYPE)
        request.cls.osid_object = request.cls.catalog.create_assessment_taken(form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments_taken():
                request.cls.catalog.delete_assessment_taken(obj.ident)
            for obj in request.cls.catalog.get_assessments_offered():
                request.cls.catalog.delete_assessment_offered(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            for obj in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""

    get_assessment_taken_form_for_create = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_assessment_taken_form_for_create(self.assessment_offered.ident, [])
            assert isinstance(form, OsidForm)
            assert not form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_assessment_taken_form_for_create(self.fake_id, [])"""

    delete_assessment_taken = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_assessment_taken_form_for_create(self.assessment_offered.ident, [])
            form.display_name = 'new Assessment Taken'
            form.set_genus_type(NEW_TYPE)
            osid_object = self.catalog.create_assessment_taken(form)
            self.catalog.delete_assessment_taken(osid_object.ident)
            with pytest.raises(errors.NotFound):
                self.catalog.get_assessment_taken(osid_object.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.delete_assessment_taken(self.fake_id)"""

    ##
    # This impl may differ from the usual create_osid_object method in that it
    # deals with agent id and default display name based on the underlying Assessment
    # and checks for exceeding max attempts...
    proposed_create_assessment_taken = """
        pass"""


class AssessmentOfferedBankSession:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.assessment_offered_list = list()
    request.cls.assessment_offered_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentOfferedBankSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank Assigned'
        create_form.description = 'Test Bank for AssessmentOfferedBankSession tests'
        request.cls.assigned_catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedBankSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        for num in [0, 1, 2]:
            create_form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
            create_form.display_name = 'Test AssessmentOffered ' + str(num)
            create_form.description = 'Test AssessmentOffered for AssessmentOfferedBankSession tests'
            obj = request.cls.catalog.create_assessment_offered(create_form)
            request.cls.assessment_offered_list.append(obj)
            request.cls.assessment_offered_ids.append(obj.ident)
        request.cls.svc_mgr.assign_assessment_offered_to_bank(
            request.cls.assessment_offered_ids[1], request.cls.assigned_catalog.ident)
        request.cls.svc_mgr.assign_assessment_offered_to_bank(
            request.cls.assessment_offered_ids[2], request.cls.assigned_catalog.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.unassign_assessment_offered_from_bank(
                request.cls.assessment_offered_ids[1], request.cls.assigned_catalog.ident)
            request.cls.svc_mgr.unassign_assessment_offered_from_bank(
                request.cls.assessment_offered_ids[2], request.cls.assigned_catalog.ident)
            for obj in request.cls.catalog.get_assessments_offered():
                request.cls.catalog.delete_assessment_offered(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.svc_mgr"""


class AssessmentOfferedBankAssignmentSession:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.assessment_offered_list = list()
    request.cls.assessment_offered_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentOfferedBankAssignmentSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank Assigned'
        create_form.description = 'Test Bank for AssessmentOfferedBankAssignmentSession tests'
        request.cls.assigned_catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedBankAssignmentSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        for num in [0, 1, 2]:
            create_form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
            create_form.display_name = 'Test AssessmentOffered ' + str(num)
            create_form.description = 'Test AssessmentOffered for AssessmentOfferedBankAssignmentSession tests'
            obj = request.cls.catalog.create_assessment_offered(create_form)
            request.cls.assessment_offered_list.append(obj)
            request.cls.assessment_offered_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments_offered():
                request.cls.catalog.delete_assessment_offered(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.svc_mgr"""


class AssessmentTakenBankSession:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.assessment_taken_list = list()
    request.cls.assessment_taken_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentTakenBankSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank Assigned'
        create_form.description = 'Test Bank for AssessmentTakenBankSession tests'
        request.cls.assigned_catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentTakenBankSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        create_form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
        create_form.display_name = 'Test AssessmentOffered'
        create_form.description = 'Test AssessmentOffered for AssessmentTakenLBankSession tests'
        request.cls.assessment_offered = request.cls.catalog.create_assessment_offered(create_form)
        for num in [0, 1, 2]:
            create_form = request.cls.catalog.get_assessment_taken_form_for_create(request.cls.assessment_offered.ident, [])
            create_form.display_name = 'Test AssessmentTaken ' + str(num)
            create_form.description = 'Test AssessmentTaken for AssessmentTakenLookupSession tests'
            obj = request.cls.catalog.create_assessment_taken(create_form)
            request.cls.assessment_taken_list.append(obj)
            request.cls.assessment_taken_ids.append(obj.ident)
        request.cls.svc_mgr.assign_assessment_taken_to_bank(
            request.cls.assessment_taken_ids[1], request.cls.assigned_catalog.ident)
        request.cls.svc_mgr.assign_assessment_taken_to_bank(
            request.cls.assessment_taken_ids[2], request.cls.assigned_catalog.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.unassign_assessment_taken_from_bank(
                request.cls.assessment_taken_ids[1], request.cls.assigned_catalog.ident)
            request.cls.svc_mgr.unassign_assessment_taken_from_bank(
                request.cls.assessment_taken_ids[2], request.cls.assigned_catalog.ident)
            for obj in request.cls.catalog.get_assessments_taken():
                request.cls.catalog.delete_assessment_taken(obj.ident)
            for obj in request.cls.catalog.get_assessments_offered():
                request.cls.catalog.delete_assessment_offered(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.svc_mgr"""


class AssessmentTakenBankAssignmentSession:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.assessment_taken_list = list()
    request.cls.assessment_taken_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentTakenBankAssignmentSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank Assigned'
        create_form.description = 'Test Bank for AssessmentTakenBankAssignmentSession tests'
        request.cls.assigned_catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentTakenBankAssignmentSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        create_form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
        create_form.display_name = 'Test AssessmentOffered'
        create_form.description = 'Test AssessmentOffered for AssessmentTakenBankAssignmentSession tests'
        request.cls.assessment_offered = request.cls.catalog.create_assessment_offered(create_form)
        for num in [0, 1, 2]:
            create_form = request.cls.catalog.get_assessment_taken_form_for_create(request.cls.assessment_offered.ident, [])
            create_form.display_name = 'Test AssessmentTaken ' + str(num)
            create_form.description = 'Test AssessmentTaken for AssessmentTakenBankAssignmentSession tests'
            obj = request.cls.catalog.create_assessment_taken(create_form)
            request.cls.assessment_taken_list.append(obj)
            request.cls.assessment_taken_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments_taken():
                request.cls.catalog.delete_assessment_taken(obj.ident)
            for obj in request.cls.catalog.get_assessments_offered():
                request.cls.catalog.delete_assessment_offered(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.svc_mgr"""


class AssessmentBasicAuthoringSession:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.assessment_offered_list = list()
    request.cls.assessment_offered_ids = list()
    simple_sequence_record_type = Type(**{
        'authority': 'ODL.MIT.EDU',
        'namespace': 'osid-object',
        'identifier': 'simple-child-sequencing'})
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentBasicAuthoringSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([simple_sequence_record_type])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentBasicAuthoringSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        request.cls.test_items = list()
        request.cls.test_item_ids = list()
        for number in ['One', 'Two', 'Three', 'Four']:
            ifc = request.cls.catalog.get_item_form_for_create([])
            ifc.set_display_name('Test Assessment Item ' + number)
            ifc.set_description('This is a Test Item Called Number ' + number)
            test_item = request.cls.catalog.create_item(ifc)
            request.cls.test_items.append(test_item)
            request.cls.test_item_ids.append(test_item.ident)
            request.cls.catalog.add_item(request.cls.assessment.ident, test_item.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            for obj in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""

    can_author_assessments = """
        assert isinstance(self.catalog.can_author_assessments(), bool)"""

    get_items = """
        if not is_never_authz(self.service_config):
            assert self.catalog.get_assessment_items(self.assessment.ident).available() == 4
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_items(self.fake_id)"""

    add_item = """
        if not is_never_authz(self.service_config):
            self._reorder_items()
            ifc = self.catalog.get_item_form_for_create([])
            ifc.set_display_name('Test Assessment Additional Item')
            ifc.set_description('This is an addtional Test Item')
            additional_item = self.catalog.create_item(ifc)
            self.catalog.add_item(self.assessment.ident, additional_item.ident)
            assert self.catalog.get_assessment_items(self.assessment.ident).available() == 5
            self.catalog.remove_item(self.assessment.ident, additional_item.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.add_item(self.fake_id, self.fake_id)"""

    remove_item = """
        if not is_never_authz(self.service_config):
            self._reorder_items()
            self.catalog.remove_item(self.assessment.ident, self.test_item_ids[1])
            assert self.catalog.get_assessment_items(self.assessment.ident).available() == 3
            self.catalog.add_item(self.assessment.ident, self.test_item_ids[1])
            items = self.catalog.get_assessment_items(self.assessment.ident)
            assert items.next().ident == self.test_item_ids[0]
            assert items.next().ident == self.test_item_ids[2]
            assert items.next().ident == self.test_item_ids[3]
            assert items.next().ident == self.test_item_ids[1]
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.remove_item(self.fake_id, self.fake_id)"""

    move_item = """
        if not is_never_authz(self.service_config):
            self._reorder_items()
            self.catalog.move_item(self.assessment.ident, self.test_item_ids[0], self.test_item_ids[3])
            items = self.catalog.get_assessment_items(self.assessment.ident)
            assert items.next().ident == self.test_item_ids[1]
            assert items.next().ident == self.test_item_ids[2]
            assert items.next().ident == self.test_item_ids[3]
            assert items.next().ident == self.test_item_ids[0]
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.move_item(self.fake_id, self.fake_id, self.fake_id)"""

    order_items = """
        if not is_never_authz(self.service_config):
            self.catalog.order_items([
                self.test_item_ids[3],
                self.test_item_ids[2],
                self.test_item_ids[1],
                self.test_item_ids[0]],
                self.assessment.ident)
            assert self.catalog.get_assessment_items(self.assessment.ident).next().ident == self.test_item_ids[3]
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.order_items([self.fake_id, self.fake_id], self.fake_id)

    def _reorder_items(self):
        self.catalog.order_items([
            self.test_item_ids[0],
            self.test_item_ids[1],
            self.test_item_ids[2],
            self.test_item_ids[3]],
            self.assessment.ident)"""


class Question:

    import_statements = [
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        item_form = request.cls.catalog.get_item_form_for_create([])
        item_form.display_name = 'Item'
        request.cls.item = request.cls.catalog.create_item(item_form)

        form = request.cls.catalog.get_question_form_for_create(request.cls.item.ident, [])
        form.display_name = 'Test question'
        request.cls.question = request.cls.catalog.create_question(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.object = request.cls.question"""


class QuestionForm:

    import_statements = [
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        item_form = request.cls.catalog.get_item_form_for_create([])
        item_form.display_name = 'Item'
        request.cls.item = request.cls.catalog.create_item(item_form)

        request.cls.form = request.cls.catalog.get_question_form_for_create(request.cls.item.ident, [])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""


class QuestionQuery:

    import_statements = [
        'from dlkit.json_.assessment.queries import QuestionQuery'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # Since the session isn't implemented, we just construct a QuestionQuery directly
    if not is_never_authz(request.cls.service_config):
        request.cls.query = QuestionQuery(runtime=request.cls.catalog._runtime)"""


class QuestionList:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for QuestionList tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    from dlkit.json_.assessment.objects import QuestionList
    request.cls.question_list = list()
    request.cls.question_ids = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            item_form = request.cls.catalog.get_item_form_for_create([])
            item_form.display_name = 'Item'
            item = request.cls.catalog.create_item(item_form)

            create_form = request.cls.catalog.get_question_form_for_create(item.ident, [])
            create_form.display_name = 'Test Question ' + str(num)
            create_form.description = 'Test Question for QuestionList tests'
            obj = request.cls.catalog.create_question(create_form)
            request.cls.question_list.append(obj)
            request.cls.question_ids.append(obj.ident)
    request.cls.question_list = QuestionList(request.cls.question_list)"""


class Answer:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        item_form = request.cls.catalog.get_item_form_for_create([])
        item_form.display_name = 'Item'
        request.cls.item = request.cls.catalog.create_item(item_form)

        form = request.cls.catalog.get_answer_form_for_create(request.cls.item.ident, [])
        form.display_name = 'Test answer'
        request.cls.answer = request.cls.catalog.create_answer(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        request.cls.object = request.cls.answer"""


class AnswerForm:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        item_form = request.cls.catalog.get_item_form_for_create([])
        item_form.display_name = 'Item'
        request.cls.item = request.cls.catalog.create_item(item_form)

        request.cls.form = request.cls.catalog.get_answer_form_for_create(request.cls.item.ident, [])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""


class AnswerQuery:

    import_statements = [
        'from dlkit.json_.assessment.queries import AnswerQuery'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # Since the session isn't implemented, we just construct a AnswerQuery directly
    if not is_never_authz(request.cls.service_config):
        request.cls.query = AnswerQuery(runtime=request.cls.catalog._runtime)"""


class AnswerList:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AnswerList tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    from dlkit.json_.assessment.objects import AnswerList
    request.cls.answer_list = list()
    request.cls.answer_ids = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            item_form = request.cls.catalog.get_item_form_for_create([])
            item_form.display_name = 'Item'
            item = request.cls.catalog.create_item(item_form)

            create_form = request.cls.catalog.get_answer_form_for_create(item.ident, [])
            create_form.display_name = 'Test Answer ' + str(num)
            create_form.description = 'Test Answer for AnswerList tests'
            obj = request.cls.catalog.create_answer(create_form)
            request.cls.answer_list.append(obj)
            request.cls.answer_ids.append(obj.ident)
    request.cls.answer_list = AnswerList(request.cls.answer_list)"""


class Item:
    import_statements = [
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.json_.assessment.objects import Question, AnswerList',
        'from dlkit.json_.id.objects import IdList',
        'from dlkit.json_.learning.objects import ObjectiveList'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.lsvc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)

    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        create_form = request.cls.lsvc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test objective bank'
        create_form.description = 'Test objective bank description'
        request.cls.bank = request.cls.lsvc_mgr.create_objective_bank(create_form)
        request.cls.objectives = list()
        for _ in range(2):
            form = request.cls.bank.get_objective_form_for_create([])
            objective = request.cls.bank.create_objective(form)
            request.cls.objectives.append(objective)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

            for obj in request.cls.bank.get_objectives():
                request.cls.bank.delete_objective(obj.ident)
            request.cls.lsvc_mgr.delete_objective_bank(request.cls.bank.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        form = request.cls.catalog.get_item_form_for_create([])
        form.display_name = 'Test object'
        form.set_learning_objectives([request.cls.objectives[0].ident,
                                      request.cls.objectives[1].ident])
        request.cls.item = request.cls.catalog.create_item(form)

        form = request.cls.catalog.get_question_form_for_create(request.cls.item.ident, [])
        request.cls.catalog.create_question(form)

        form = request.cls.catalog.get_answer_form_for_create(request.cls.item.ident, [])
        form.set_genus_type(Type('answer-genus%3Aright-answer%40ODL.MIT.EDU'))
        request.cls.catalog.create_answer(form)

        request.cls.item = request.cls.catalog.get_item(request.cls.item.ident)
        request.cls.object = request.cls.item"""

    get_learning_objective_ids = """
        if not is_never_authz(self.service_config):
            lo_ids = self.item.get_learning_objective_ids()
            assert isinstance(lo_ids, IdList)
            assert lo_ids.available() == 2
            assert str(next(lo_ids)) == str(self.objectives[0].ident)
            assert str(next(lo_ids)) == str(self.objectives[1].ident)"""

    get_learning_objectives = """
        if not is_never_authz(self.service_config):
            los = self.item.get_learning_objectives()
            assert isinstance(los, ObjectiveList)
            assert los.available() == 2
            assert str(next(los).ident) == str(self.objectives[0].ident)
            assert str(next(los).ident) == str(self.objectives[1].ident)"""

    get_answer_ids = """
        if not is_never_authz(self.service_config):
            answer_ids = self.item.get_answer_ids()
            assert isinstance(answer_ids, IdList)
            assert answer_ids.available() == 1"""

    get_answers = """
        if not is_never_authz(self.service_config):
            answers = self.item.get_answers()
            assert isinstance(answers, AnswerList)
            assert answers.available() == 1
            assert str(next(answers).genus_type) == 'answer-genus%3Aright-answer%40ODL.MIT.EDU'"""

    get_question_id = """
        if not is_never_authz(self.service_config):
            question_id = self.item.get_question_id()
            assert isinstance(question_id, Id)
            assert str(question_id) == str(self.item.ident)"""

    get_question = """
        if not is_never_authz(self.service_config):
            question = self.item.get_question()
            assert isinstance(question, Question)
            assert str(question.ident) == str(self.item.ident)"""


class ItemQuery:
    import_statement = [
        'from dlkit.primordium.id.primitives import Id'
    ]

    match_assessment_assessment_id = """
        if not is_never_authz(self.service_config):
            test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
            if is_no_authz(self.service_config):
                assert 'assessmentObjectiveIds' not in self.query._query_terms

            self.query.match_assessment_assessment_id(test_id, match=True)

            if is_no_authz(self.service_config):
                assert self.query._query_terms['assessmentObjectiveIds'] == {
                    '$in': [str(test_id)]
                }"""

    match_learning_objective_id = """
        if not is_never_authz(self.service_config):
            test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
            if is_no_authz(self.service_config):
                assert 'learningObjectiveIds' not in self.query._query_terms

            self.query.match_learning_objective_id(test_id, match=True)

            if is_no_authz(self.service_config):
                assert self.query._query_terms['learningObjectiveIds'] == {
                    '$in': [str(test_id)]
                }"""

    clear_assessment_assessment_id_terms = """
        if not is_never_authz(self.service_config):
            test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
            self.query.match_assessment_assessment_id(test_id, match=True)

            if is_no_authz(self.service_config):
                assert 'assessmentObjectiveIds' in self.query._query_terms

            self.query.clear_assessment_assessment_id_terms()

            if is_no_authz(self.service_config):
                assert 'assessmentObjectiveIds' not in self.query._query_terms"""

    clear_learning_objective_id_terms = """
        if not is_never_authz(self.service_config):
            test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
            self.query.match_learning_objective_id(test_id, match=True)

            if is_no_authz(self.service_config):
                assert 'learningObjectiveIds' in self.query._query_terms

            self.query.clear_learning_objective_id_terms()

            if is_no_authz(self.service_config):
                assert 'learningObjectiveIds' not in self.query._query_terms"""

    clear_assessment_assessment_terms = """
        if not is_never_authz(self.service_config):
            self.query.match_any_assessment_assessment(match=True)

            if is_no_authz(self.service_config):
                assert 'assessmentObjectiveIds' in self.query._query_terms

            self.query.clear_assessment_assessment_terms()

            if is_no_authz(self.service_config):
                assert 'assessmentObjectiveIds' not in self.query._query_terms"""

    clear_learning_objective_terms = """
        if not is_never_authz(self.service_config):
            self.query.match_any_learning_objective(match=True)

            if is_no_authz(self.service_config):
                assert 'learningObjectiveIds' in self.query._query_terms

            self.query.clear_learning_objective_terms()

            if is_no_authz(self.service_config):
                assert 'learningObjectiveIds' not in self.query._query_terms"""

    match_any_assessment_assessment = """
        if not is_never_authz(self.service_config):
            if is_no_authz(self.service_config):
                assert 'assessmentObjectiveIds' not in self.query._query_terms

            self.query.match_any_assessment_assessment(match=True)

            if is_no_authz(self.service_config):
                assert self.query._query_terms['assessmentObjectiveIds'] == {
                    '$exists': 'true',
                    '$nin': [[], ['']]
                }"""

    match_any_learning_objective = """
        if not is_never_authz(self.service_config):
            if is_no_authz(self.service_config):
                assert 'learningObjectiveIds' not in self.query._query_terms

            self.query.match_any_learning_objective(match=True)

            if is_no_authz(self.service_config):
                assert self.query._query_terms['learningObjectiveIds'] == {
                    '$exists': 'true',
                    '$nin': [[], ['']]
                }"""


class ItemSearch:
    import_statements = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'from dlkit.abstract_osid.osid import errors',
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.search = request.cls.catalog.get_item_search()"""

    search_among_items = """
        if not is_never_authz(self.service_config):
            assert self.search._id_list is None
            fake_list = [self.catalog.ident]
            self.search.search_among_items(fake_list)
            assert self.search._id_list == fake_list"""


class ItemSearchResults:
    import_statements = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'from dlkit.abstract_osid.osid import errors',
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        request.cls.query = request.cls.catalog.get_item_query()
        request.cls.search_obj = request.cls.catalog.get_item_search()
        request.cls.search = request.cls.catalog.get_items_by_search(request.cls.query, request.cls.search_obj)"""

    get_items = """
        from dlkit.abstract_osid.assessment.objects import ItemList
        if not is_never_authz(self.service_config):
            items = self.search.get_items()
            assert isinstance(items, ItemList)
            assert items.available() == 0"""


class ItemQuerySession:
    import_statements = [
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for ItemQuerySession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = request.cls.catalog.get_item_form_for_create([])
            create_form.display_name = 'Test Item ' + color
            create_form.description = (
                'Test Item for ItemQuerySession tests, did I mention green')
            obj = request.cls.catalog.create_item(create_form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments():
                for offered in request.cls.catalog.get_assessments_offered_for_assessment(obj.ident):
                    for taken in request.cls.catalog.get_assessments_taken_for_assessment_offered(offered.ident):
                        request.cls.catalog.delete_assessment_taken(taken.ident)
                    request.cls.catalog.delete_assessment_offered(offered.ident)
                request.cls.catalog.delete_assessment(obj.ident)
            for item in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(item.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(test_tear_down)"""

    can_search_items = """
        assert isinstance(self.session.can_search_items(), bool)"""


class ItemSearchSession:
    import_statements = [
        'from dlkit.json_.assessment import searches',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.abstract_osid.osid import errors',
        'from dlkit.primordium.locale.types.string import get_type_data as get_string_type_data',
        'DEFAULT_STRING_MATCH_TYPE = Type(**get_string_type_data("WORDIGNORECASE"))'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for ItemSearchSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = request.cls.catalog.get_item_form_for_create([])
            create_form.display_name = 'Test Item ' + color
            create_form.description = (
                'Test Item for ItemSearchSession tests, did I mention green')
            obj = request.cls.catalog.create_item(create_form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments():
                for offered in request.cls.catalog.get_assessments_offered_for_assessment(obj.ident):
                    for taken in request.cls.catalog.get_assessments_taken_for_assessment_offered(offered.ident):
                        request.cls.catalog.delete_assessment_taken(taken.ident)
                    request.cls.catalog.delete_assessment_offered(offered.ident)
                request.cls.catalog.delete_assessment(obj.ident)
            for item in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(item.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    get_item_search = """
        if not is_never_authz(self.service_config):
            search = self.session.get_item_search()
            assert isinstance(search, searches.ItemSearch)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_item_search()"""

    get_items_by_search = """
        if not is_never_authz(self.service_config):
            query = self.session.get_item_query()
            query.match_display_name('zxy', DEFAULT_STRING_MATCH_TYPE, True)
            search = self.session.get_item_search()
            results = self.session.get_items_by_search(query, search)
            assert isinstance(results, searches.ItemSearchResults)
            assert results.get_result_size() == 0
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_items_by_search('foo', 'foo')"""


class AssessmentOffered:

    import_statements = [
        'import datetime',
        'from dlkit.primordium.calendaring.primitives import DateTime, Duration',
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.json_.assessment.objects import Assessment'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        form = request.cls.catalog.get_assessment_form_for_create([])
        form.display_name = 'Assessment'
        request.cls.assessment = request.cls.catalog.create_assessment(form)

        form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
        form.display_name = 'Test assessment offered'
        form.set_start_time(DateTime.utcnow())
        form.set_duration(Duration(hours=1))
        deadline = DateTime.utcnow() + datetime.timedelta(days=4)
        form.set_deadline(DateTime(year=deadline.year,
                                   month=deadline.month,
                                   day=deadline.day,
                                   hour=deadline.hour,
                                   minute=deadline.minute,
                                   second=deadline.second,
                                   microsecond=deadline.microsecond))
        request.cls.object = request.cls.catalog.create_assessment_offered(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments():
                for offered in request.cls.catalog.get_assessments_offered_for_assessment(obj.ident):
                    request.cls.catalog.delete_assessment_offered(offered.ident)
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""

    get_assessment_id = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.get_assessment_id(), Id)
            assert str(self.object.get_assessment_id()) == str(self.assessment.ident)"""

    get_assessment = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.get_assessment(), Assessment)
            assert str(self.object.get_assessment().ident) == str(self.assessment.ident)"""

    get_start_time_template = """
        # From test_templates/assessment.py::AssessmentOffered::get_start_time_template
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.get_start_time(), DateTime)"""

    get_duration_template = """
        # From test_templates/assessment.py::AssessmentOffered::get_duration_template
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.get_duration(), Duration)"""

    has_rubric = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set rubricId?
        if not is_never_authz(self.service_config):
            pytest.raises(KeyError,
                          self.object.has_rubric)"""

    get_rubric = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set rubricId?
        if not is_never_authz(self.service_config):
            pytest.raises(KeyError,
                          self.object.get_rubric)"""

    get_rubric_id = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set rubricId?
        if not is_never_authz(self.service_config):
            pytest.raises(KeyError,
                          self.object.get_rubric_id)"""

    is_graded = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set graded?
        if not is_never_authz(self.service_config):
            pytest.raises(KeyError,
                          self.object.is_graded)"""

    is_scored = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set scored?
        if not is_never_authz(self.service_config):
            pytest.raises(KeyError,
                          self.object.is_scored)"""


class AssessmentOfferedAdminSession:
    import_statements = [
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.abstract_osid.assessment.objects import AssessmentOffered',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})',
        'NEW_TYPE_2 = Type(**{\'identifier\': \'NEW 2\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.assessment_offered_list = list()
    request.cls.assessment_offered_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentOfferedAdminSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedAdminSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
            create_form.display_name = 'Test AssessmentOffered ' + str(num)
            create_form.description = 'Test AssessmentOffered for AssessmentOfferedAdminSession tests'
            obj = request.cls.catalog.create_assessment_offered(create_form)
            request.cls.assessment_offered_list.append(obj)
            request.cls.assessment_offered_ids.append(obj.ident)
        create_form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
        create_form.display_name = 'new AssessmentOffered'
        create_form.description = 'description of AssessmentOffered'
        create_form.genus_type = NEW_TYPE
        request.cls.osid_object = request.cls.catalog.create_assessment_offered(create_form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments_taken():
                request.cls.catalog.delete_assessment_taken(obj.ident)
            for obj in request.cls.catalog.get_assessments_offered():
                request.cls.catalog.delete_assessment_offered(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            for obj in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""

    get_assessment_offered_form_for_create = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_assessment_offered_form_for_create(self.assessment.ident, [])
            assert isinstance(form, OsidForm)
            assert not form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_assessment_offered_form_for_create(self.fake_id, [])"""

    delete_assessment_offered = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_assessment_offered_form_for_create(self.assessment.ident, [])
            form.display_name = 'new Assessment Offered'
            form.set_genus_type(NEW_TYPE)
            osid_object = self.catalog.create_assessment_offered(form)
            self.catalog.delete_assessment_offered(osid_object.ident)
            with pytest.raises(errors.NotFound):
                self.catalog.get_assessment_offered(osid_object.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.delete_assessment_offered(self.fake_id)"""


class AssessmentOfferedForm:
    import_statements_pattern = [
        'from dlkit.primordium.calendaring.primitives import DateTime, Duration'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentOfferedLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedLookupSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)

        request.cls.form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident,
                                                                                      [])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments_offered():
                request.cls.catalog.delete_assessment_offered(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        request.cls.form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident,
                                                                                      [])"""

    set_start_time_template = """
        # From test_templates/assessment.py::AssessmentOfferedForm::set_start_time_template
        if not is_never_authz(self.service_config):
            test_time = DateTime.utcnow()
            assert self.form._my_map['${var_name_mixed}'] is None
            self.form.${method_name}(test_time)
            assert self.form._my_map['${var_name_mixed}'] == test_time
            with pytest.raises(errors.InvalidArgument):
                self.form.${method_name}(True)
            # reset this for other tests
            self.form._my_map['${var_name_mixed}'] = None"""

    # This looks just like the generic one. Need to find in the pattern?
    clear_start_time_template = """
        # From test_templates/assessment.py::AssessmentOfferedForm::clear_start_time_template
        if not is_never_authz(self.service_config):
            test_time = DateTime.utcnow()
            assert self.form._my_map['${var_name_mixed}'] is None
            self.form.set_${var_name}(test_time)
            assert self.form._my_map['${var_name_mixed}'] == test_time
            self.form.${method_name}()
            assert self.form._my_map['${var_name_mixed}'] == self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0]"""

    set_duration_template = """
        # From test_templates/assessment.py::AssessmentOfferedForm::set_duration_template
        if not is_never_authz(self.service_config):
            test_duration = Duration(hours=1)
            assert self.form._my_map['${var_name_mixed}'] is None
            self.form.${method_name}(test_duration)
            assert self.form._my_map['${var_name_mixed}']['seconds'] == 3600
            assert self.form._my_map['${var_name_mixed}']['days'] == 0
            assert self.form._my_map['${var_name_mixed}']['microseconds'] == 0
            with pytest.raises(errors.InvalidArgument):
                self.form.${method_name}(1.05)
            # reset this for other tests
            self.form._my_map['${var_name_mixed}'] = None"""

    clear_duration_template = """
        # From test_templates/assessment.py::AssessmentOfferedForm::clear_duration_template
        if not is_never_authz(self.service_config):
            test_duration = Duration(hours=1)
            assert self.form._my_map['${var_name_mixed}'] is None
            self.form.set_${var_name}(test_duration)
            assert self.form._my_map['${var_name_mixed}']['seconds'] == 3600
            assert self.form._my_map['${var_name_mixed}']['days'] == 0
            assert self.form._my_map['${var_name_mixed}']['microseconds'] == 0
            self.form.${method_name}()
            assert self.form._my_map['${var_name_mixed}'] == self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0]"""


class AssessmentOfferedList:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentOfferedList tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedList tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)

        request.cls.form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident,
                                                                                      [])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments_offered():
                request.cls.catalog.delete_assessment_offered(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    from dlkit.json_.assessment.objects import AssessmentOfferedList
    request.cls.assessment_offered_list = list()
    request.cls.assessment_offered_ids = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident,
                                                                              [])
            form.display_name = 'Test AssessmentOffered ' + str(num)
            form.description = 'Test AssessmentOffered for AssessmentOfferedList tests'
            obj = request.cls.catalog.create_assessment_offered(form)
            request.cls.assessment_offered_list.append(obj)
            request.cls.assessment_offered_ids.append(obj.ident)
    request.cls.assessment_offered_list = AssessmentOfferedList(request.cls.assessment_offered_list)"""

    # These seem misplaced:
    # set_start_time_template = """"""
    #
    # # This looks just like the generic one. Need to find in the pattern?
    # clear_start_time_template = """
    #     pass"""
    #
    # set_duration_template = """
    #     pass"""


class AssessmentOfferedQuery:
    import_statements = [
        'from dlkit.primordium.calendaring.primitives import DateTime'
    ]

    match_start_time_template = """
        if not is_never_authz(self.service_config):
            start_time = DateTime.utcnow()
            end_time = DateTime.utcnow()
            self.query.${method_name}(start_time, end_time, match=True)
            assert self.query._query_terms['${var_name_mixed}'] == {
                '$$gte': start_time,
                '$$lte': end_time
            }"""


class AssessmentQuery:

    match_item_id = """
        if not is_never_authz(self.service_config):
            test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
            self.query.match_item_id(test_id, match=True)
            assert self.query._query_terms['itemIds'] == {
                '$in': [str(test_id)]
            }"""

    clear_item_id_terms = """
        if not is_never_authz(self.service_config):
            test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
            self.query.match_item_id(test_id, match=True)
            assert 'itemIds' in self.query._query_terms
            self.query.clear_item_id_terms()
            assert 'itemIds' not in self.query._query_terms"""


class AssessmentOfferedQuerySession:

    import_statements_pattern = [
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.assessment_offered_list = list()
    request.cls.assessment_offered_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentOfferedQuerySession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedQuerySession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
            create_form.display_name = 'Test AssessmentOffered ' + color
            create_form.description = (
                'Test AssessmentOffered for AssessmentOfferedQuerySession tests, did I mention green')
            obj = request.cls.catalog.create_assessment_offered(create_form)
            request.cls.assessment_offered_list.append(obj)
            request.cls.assessment_offered_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    request.cls.session = request.cls.catalog

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments_offered():
                request.cls.catalog.delete_assessment_offered(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)"""


class AssessmentTakenQuerySession:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.assessment_taken_list = list()
    request.cls.assessment_taken_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentTakenLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentTakenLookupSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        create_form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
        create_form.display_name = 'Test AssessmentOffered'
        create_form.description = 'Test AssessmentOffered for AssessmentTakenLookupSession tests'
        request.cls.assessment_offered = request.cls.catalog.create_assessment_offered(create_form)
        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = request.cls.catalog.get_assessment_taken_form_for_create(request.cls.assessment_offered.ident, [])
            create_form.display_name = 'Test AssessmentTaken ' + color
            create_form.description = (
                'Test AssessmentTaken for AssessmentTakenQuerySession tests, did I mention green')
            obj = request.cls.catalog.create_assessment_taken(create_form)
            request.cls.assessment_taken_list.append(obj)
            request.cls.assessment_taken_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_banks():
                for obj in catalog.get_assessments_taken():
                    catalog.delete_assessment_taken(obj.ident)
                for obj in catalog.get_assessments_offered():
                    catalog.delete_assessment_offered(obj.ident)
                for obj in catalog.get_assessments():
                    catalog.delete_assessment(obj.ident)
                request.cls.svc_mgr.delete_bank(catalog.ident)

    request.addfinalizer(test_tear_down)"""


class AssessmentTaken:

    import_statements_pattern = [
        'from decimal import Decimal',
        'from dlkit.abstract_osid.osid import errors',
        'from dlkit.json_.assessment.objects import AssessmentOffered',
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.records import registry',
        'SEQUENCE_ASSESSMENT = Type(**registry.ASSESSMENT_RECORD_TYPES["simple-child-sequencing"])'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        form = request.cls.catalog.get_assessment_form_for_create([SEQUENCE_ASSESSMENT])
        form.display_name = 'Assessment'
        request.cls.assessment = request.cls.catalog.create_assessment(form)

        form = request.cls.catalog.get_item_form_for_create([])
        form.display_name = 'Test item'
        request.cls.item = request.cls.catalog.create_item(form)

        form = request.cls.catalog.get_question_form_for_create(request.cls.item.ident, [])
        request.cls.catalog.create_question(form)
        request.cls.item = request.cls.catalog.get_item(request.cls.item.ident)

        request.cls.catalog.add_item(request.cls.assessment.ident, request.cls.item.ident)
        request.cls.assessment = request.cls.catalog.get_assessment(request.cls.assessment.ident)

        form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
        form.display_name = 'Test assessment offered'
        request.cls.offered = request.cls.catalog.create_assessment_offered(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments():
                for offered in request.cls.catalog.get_assessments_offered_for_assessment(obj.ident):
                    for taken in request.cls.catalog.get_assessments_taken_for_assessment_offered(offered.ident):
                        request.cls.catalog.delete_assessment_taken(taken.ident)
                    request.cls.catalog.delete_assessment_offered(offered.ident)
                request.cls.catalog.delete_assessment(obj.ident)
            for obj in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        form = request.cls.catalog.get_assessment_taken_form_for_create(request.cls.offered.ident,
                                                                        [])
        request.cls.object = request.cls.catalog.create_assessment_taken(form)

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.catalog.delete_assessment_taken(request.cls.object.ident)

    request.addfinalizer(test_tear_down)"""

    get_assessment_offered_id = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.get_assessment_offered_id(), Id)
            assert str(self.object.get_assessment_offered_id()) == str(self.offered.ident)"""

    get_assessment_offered = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.get_assessment_offered(), AssessmentOffered)
            assert str(self.object.get_assessment_offered().ident) == str(self.offered.ident)"""

    get_taker_id = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.get_taker_id(), Id)
            assert str(self.object.get_taker_id()) == str(self.catalog._proxy.get_effective_agent_id())"""

    get_taker = """
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.Unimplemented):
                self.object.get_taker()"""

    get_taking_agent_id = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.get_taking_agent_id(), Id)
            assert str(self.object.get_taking_agent_id()) == str(self.catalog._proxy.get_effective_agent_id())"""

    get_taking_agent = """
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.Unimplemented):
                self.object.get_taking_agent()"""

    has_started = """
        # tests if the assessment has begun
        if not is_never_authz(self.service_config):
            assert self.object.has_started()"""

    get_actual_start_time = """
        # tests if the taker has started the assessment
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.IllegalState):
                self.object.actual_start_time
            # Also test the other branches of this method
            form = self.catalog.get_assessment_taken_form_for_create(self.offered.ident,
                                                                     [])
            taken = self.catalog.create_assessment_taken(form)
            section = self.catalog.get_first_assessment_section(taken.ident)
            section.get_questions()
            taken = self.catalog.get_assessment_taken(taken.ident)
            assert isinstance(taken.actual_start_time, DateTime)
            self.catalog.delete_assessment_taken(taken.ident)"""

    has_ended = """
        # tests if the assessment is over
        if not is_never_authz(self.service_config):
            assert not self.object.has_ended()"""

    get_completion_time = """
        # tests if the taker has "finished" the assessment
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.IllegalState):
                self.object.completion_time
            # Also test the other branches of this method
            form = self.catalog.get_assessment_taken_form_for_create(self.offered.ident,
                                                                     [])
            taken = self.catalog.create_assessment_taken(form)
            section = self.catalog.get_first_assessment_section(taken.ident)
            section.get_questions()

            self.catalog.finish_assessment(taken.ident)

            taken = self.catalog.get_assessment_taken(taken.ident)
            assert isinstance(taken.completion_time, DateTime)
            self.catalog.delete_assessment_taken(taken.ident)"""

    get_time_spent = """
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.IllegalState):
                self.object.time_spent
            # Also test the other branches of this method
            form = self.catalog.get_assessment_taken_form_for_create(self.offered.ident,
                                                                     [])
            taken = self.catalog.create_assessment_taken(form)
            section = self.catalog.get_first_assessment_section(taken.ident)
            section.get_questions()

            self.catalog.finish_assessment(taken.ident)
            taken = self.catalog.get_assessment_taken(taken.ident)
            assert isinstance(taken.time_spent, datetime.timedelta)
            self.catalog.delete_assessment_taken(taken.ident)"""

    get_completion_template = """
        # From test_templates/assessment.py::AssessmentTaken::get_completion_template
        # Our implementation is probably wrong -- there is no "completion" setter
        # in the form / spec...so unclear how the value gets here.
        if not is_never_authz(self.service_config):
            pytest.raises(KeyError,
                          self.object.${method_name})"""

    get_score_template = """
        # From test_templates/assessment.py::AssessmentTaken::get_score_template
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.${method_name}(), Decimal)
            assert self.object.${method_name}() == Decimal(0.0)"""

    has_rubric = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set rubricId?
        if not is_never_authz(self.service_config):
            pytest.raises(KeyError,
                          self.object.has_rubric)"""

    get_rubric = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set rubricId?
        if not is_never_authz(self.service_config):
            pytest.raises(KeyError,
                          self.object.get_rubric)"""

    get_rubric_id = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set rubricId?
        if not is_never_authz(self.service_config):
            pytest.raises(KeyError,
                          self.object.get_rubric_id)"""

    is_graded = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set graded?
        if not is_never_authz(self.service_config):
            pytest.raises(KeyError,
                          self.object.is_graded)"""

    is_scored = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set scored?
        if not is_never_authz(self.service_config):
            pytest.raises(KeyError,
                          self.object.is_scored)"""

    get_score_system = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set scoreSystemId?
        if not is_never_authz(self.service_config):
            pytest.raises(KeyError,
                          self.object.get_score_system)"""

    get_score_system_id = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set scoreSystemId?
        if not is_never_authz(self.service_config):
            pytest.raises(KeyError,
                          self.object.get_score_system_id)"""

    get_feedback = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set feedback?
        if not is_never_authz(self.service_config):
            pytest.raises(KeyError,
                          self.object.get_feedback)"""


class AssessmentTakenForm:

    import_statements = [
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentTakenForm tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentTakenForm tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        create_form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
        create_form.display_name = 'Test AssessmentOffered'
        create_form.description = 'Test AssessmentOffered for AssessmentTakenForm tests'
        request.cls.assessment_offered = request.cls.catalog.create_assessment_offered(create_form)

        request.cls.form = request.cls.catalog.get_assessment_taken_form_for_create(request.cls.assessment_offered.ident, [])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments_offered():
                request.cls.catalog.delete_assessment_offered(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""


class AssessmentTakenList:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentTakenList tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentTakenList tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)

        form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident,
                                                                          [])
        request.cls.assessment_offered = request.cls.catalog.create_assessment_offered(form)

        request.cls.form = request.cls.catalog.get_assessment_taken_form_for_create(request.cls.assessment_offered.ident,
                                                                                    [])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments_taken():
                request.cls.catalog.delete_assessment_taken(obj.ident)
            for obj in request.cls.catalog.get_assessments_offered():
                request.cls.catalog.delete_assessment_offered(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    from dlkit.json_.assessment.objects import AssessmentTakenList
    request.cls.assessment_taken_list = list()
    request.cls.assessment_taken_ids = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident,
                                                                              [])
            form.display_name = 'Test AssessmentOffered ' + str(num)
            form.description = 'Test AssessmentOffered for AssessmentTakenList tests'
            obj = request.cls.catalog.create_assessment_offered(form)

            form = request.cls.catalog.get_assessment_taken_form_for_create(obj.ident, [])
            obj = request.cls.catalog.create_assessment_taken(form)
            request.cls.assessment_taken_list.append(obj)
            request.cls.assessment_taken_ids.append(obj.ident)
    request.cls.assessment_taken_list = AssessmentTakenList(request.cls.assessment_taken_list)"""


class AssessmentSection:
    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from dlkit.json_.assessment.objects import AssessmentTaken',
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.records import registry',
        'SEQUENCE_ASSESSMENT = Type(**registry.ASSESSMENT_RECORD_TYPES["simple-child-sequencing"])'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        form = request.cls.catalog.get_assessment_form_for_create([SEQUENCE_ASSESSMENT])
        form.display_name = 'Assessment'
        request.cls.assessment = request.cls.catalog.create_assessment(form)

        form = request.cls.catalog.get_item_form_for_create([])
        form.display_name = 'Test item'
        request.cls.item = request.cls.catalog.create_item(form)

        form = request.cls.catalog.get_question_form_for_create(request.cls.item.ident, [])
        request.cls.catalog.create_question(form)
        request.cls.item = request.cls.catalog.get_item(request.cls.item.ident)

        request.cls.catalog.add_item(request.cls.assessment.ident, request.cls.item.ident)
        request.cls.assessment = request.cls.catalog.get_assessment(request.cls.assessment.ident)

        form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
        form.display_name = 'Test assessment offered'
        request.cls.offered = request.cls.catalog.create_assessment_offered(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments():
                for offered in request.cls.catalog.get_assessments_offered_for_assessment(obj.ident):
                    for taken in request.cls.catalog.get_assessments_taken_for_assessment_offered(offered.ident):
                        request.cls.catalog.delete_assessment_taken(taken.ident)
                    request.cls.catalog.delete_assessment_offered(offered.ident)
                request.cls.catalog.delete_assessment(obj.ident)
            for obj in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        form = request.cls.catalog.get_assessment_taken_form_for_create(request.cls.offered.ident,
                                                                        [])
        request.cls.taken = request.cls.catalog.create_assessment_taken(form)
        request.cls.section = request.cls.catalog.get_first_assessment_section(request.cls.taken.ident)
        request.cls.object = request.cls.section

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.catalog.delete_assessment_taken(request.cls.taken.ident)

    request.addfinalizer(test_tear_down)"""

    get_assessment_taken_id = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.section.get_assessment_taken_id(), Id)
            assert str(self.section.get_assessment_taken_id()) == str(self.taken.ident)"""

    get_assessment_taken = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.section.get_assessment_taken(), AssessmentTaken)
            assert str(self.section.get_assessment_taken().ident) == str(self.taken.ident)"""

    has_allocated_time = """
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.Unimplemented):
                self.section.has_allocated_time()"""

    get_allocated_time = """
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.Unimplemented):
                self.section.get_allocated_time()"""

    are_items_sequential = """
        # This does not throw an exception because of the SIMPLE_SEQUENCE record
        if not is_never_authz(self.service_config):
            assert not self.section.are_items_sequential()"""

    are_items_shuffled = """
        # This does not throw an exception because of the SIMPLE_SEQUENCE record
        if not is_never_authz(self.service_config):
            assert not self.section.are_items_shuffled()"""


class AssessmentSectionList:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentSectionList tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentSectionList tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)

        request.cls.form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident,
                                                                                                  [])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    from dlkit.json_.assessment.objects import AssessmentSectionList
    request.cls.assessment_section_list = list()
    request.cls.assessment_section_ids = list()

    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident, [])

            obj = request.cls.catalog.create_assessment_part_for_assessment(form)

            request.cls.assessment_section_list.append(obj)
            request.cls.assessment_section_ids.append(obj.ident)
    request.cls.assessment_section_list = AssessmentSectionList(request.cls.assessment_section_list)"""

    get_next_assessment_section = """
        from dlkit.abstract_osid.assessment_authoring.objects import AssessmentPart
        if not is_never_authz(self.service_config):
            assert isinstance(self.assessment_section_list.get_next_assessment_section(), AssessmentPart)"""

    get_next_assessment_sections = """
        from dlkit.abstract_osid.assessment.objects import AssessmentSectionList
        from dlkit.abstract_osid.assessment_authoring.objects import AssessmentPart
        if not is_never_authz(self.service_config):
            new_list = self.assessment_section_list.get_next_assessment_sections(2)
            assert isinstance(new_list, AssessmentSectionList)
            for item in new_list:
                assert isinstance(item, AssessmentPart)"""


class Response:

    import_statements = [
    ]

    init = """
"""

    get_item_id = """
        pass"""

    get_item = """
        pass"""

    get_response_record = """
        pass"""


class ResponseList:

    import_statements = [
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for ResponseList tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        create_form = request.cls.catalog.get_assessment_form_for_create([SEQUENCE_ASSESSMENT])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)

        for number in ['One', 'Two', 'Three', 'Four']:
            ifc = request.cls.catalog.get_item_form_for_create([])
            ifc.set_display_name('Test Assessment Item ' + number)
            ifc.set_description('This is a Test Item Called Number ' + number)
            test_item = request.cls.catalog.create_item(ifc)
            form = request.cls.catalog.get_question_form_for_create(test_item.ident, [])
            request.cls.catalog.create_question(form)

            if number == 'One':
                form = request.cls.catalog.get_answer_form_for_create(test_item.ident, [])
                request.cls.catalog.create_answer(form)

            request.cls.catalog.add_item(request.cls.assessment.ident, test_item.ident)

        form = request.cls.catalog.get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
        request.cls.assessment_offered = request.cls.catalog.create_assessment_offered(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessments():
                for offered in request.cls.catalog.get_assessments_offered_for_assessment(obj.ident):
                    for taken in request.cls.catalog.get_assessments_taken_for_assessment_offered(offered.ident):
                        request.cls.catalog.delete_assessment_taken(taken.ident)
                    request.cls.catalog.delete_assessment_offered(offered.ident)
                request.cls.catalog.delete_assessment(obj.ident)
            for obj in request.cls.catalog.get_items():
                request.cls.catalog.delete_item(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        form = request.cls.catalog.get_assessment_taken_form_for_create(request.cls.assessment_offered.ident, [])
        request.cls.taken = request.cls.catalog.create_assessment_taken(form)

        section = request.cls.catalog.get_first_assessment_section(request.cls.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()

        for num in [0, 1]:
            create_form = request.cls.catalog.get_response_form(section.ident, first_question.ident)
            request.cls.catalog.submit_response(section.ident, first_question.ident, create_form)

        request.cls.response_list = request.cls.catalog.get_responses(section.ident)
        request.cls.object = request.cls.response_list"""

    get_next_response = """
        from dlkit.abstract_osid.assessment.rules import Response
        if not is_never_authz(self.service_config):
            assert isinstance(self.response_list.get_next_response(), Response)"""

    get_next_responses = """
        from dlkit.abstract_osid.assessment.objects import ResponseList
        from dlkit.abstract_osid.assessment.rules import Response
        if not is_never_authz(self.service_config):
            new_list = self.response_list.get_next_responses(2)
            assert isinstance(new_list, ResponseList)
            for item in new_list:
                assert isinstance(item, Response)"""


class BankQuery:
    match_ancestor_bank_id = """
        if not is_never_authz(self.service_config):
            assert '_id' not in self.query._query_terms
            self.query.match_ancestor_bank_id(self.fake_id, True)
            assert self.query._query_terms['_id'] == {
                '$in': []
            }"""


class BankForm:
    get_bank_form_record = """
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.Unsupported):
                self.object.get_bank_form_record(DEFAULT_TYPE)"""


class AssessmentLookupSession:
    # Override these locally for Assessment because with AssessmentQuerySession implemented,
    #   the authz adapter will return an empty List instead of throwing PermissionDenied
    get_assessment = """
        if not is_never_authz(self.service_config):
            self.catalog.use_isolated_bank_view()
            obj = self.catalog.get_assessment(self.assessment_list[0].ident)
            assert obj.ident == self.assessment_list[0].ident
            self.catalog.use_federated_bank_view()
            obj = self.catalog.get_assessment(self.assessment_list[0].ident)
            assert obj.ident == self.assessment_list[0].ident
        else:
            with pytest.raises(errors.NotFound):
                self.catalog.get_assessment(self.fake_id)"""

    get_assessments_by_ids = """
        from dlkit.abstract_osid.assessment.objects import AssessmentList
        objects = self.catalog.get_assessments_by_ids(self.assessment_ids)
        assert isinstance(objects, AssessmentList)
        self.catalog.use_federated_bank_view()
        objects = self.catalog.get_assessments_by_ids(self.assessment_ids)
        assert isinstance(objects, AssessmentList)
        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0"""

    get_assessments_by_genus_type = """
        from dlkit.abstract_osid.assessment.objects import AssessmentList
        objects = self.catalog.get_assessments_by_genus_type(DEFAULT_GENUS_TYPE)
        assert isinstance(objects, AssessmentList)
        self.catalog.use_federated_bank_view()
        objects = self.catalog.get_assessments_by_genus_type(DEFAULT_GENUS_TYPE)
        assert isinstance(objects, AssessmentList)
        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0"""

    get_assessments_by_parent_genus_type = """
        from dlkit.abstract_osid.assessment.objects import AssessmentList
        if not is_never_authz(self.service_config):
            objects = self.catalog.get_assessments_by_parent_genus_type(DEFAULT_GENUS_TYPE)
            assert isinstance(objects, AssessmentList)
            self.catalog.use_federated_bank_view()
            objects = self.catalog.get_assessments_by_parent_genus_type(DEFAULT_GENUS_TYPE)
            assert objects.available() == 0
            assert isinstance(objects, AssessmentList)
        else:
            with pytest.raises(errors.Unimplemented):
                # because the never_authz "tries harder" and runs the actual query...
                #    whereas above the method itself in JSON returns an empty list
                self.catalog.get_assessments_by_parent_genus_type(DEFAULT_GENUS_TYPE)"""

    get_assessments_by_record_type = """
        from dlkit.abstract_osid.assessment.objects import AssessmentList
        objects = self.catalog.get_assessments_by_record_type(DEFAULT_TYPE)
        assert isinstance(objects, AssessmentList)
        self.catalog.use_federated_bank_view()
        objects = self.catalog.get_assessments_by_record_type(DEFAULT_TYPE)
        assert objects.available() == 0
        assert isinstance(objects, AssessmentList)"""

    get_assessments = """
        from dlkit.abstract_osid.assessment.objects import AssessmentList
        objects = self.catalog.get_assessments()
        assert isinstance(objects, AssessmentList)
        self.catalog.use_federated_bank_view()
        objects = self.catalog.get_assessments()
        assert isinstance(objects, AssessmentList)

        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0

    def test_get_assessment_with_alias(self):
        if not is_never_authz(self.service_config):
            self.catalog.alias_assessment(self.assessment_ids[0], ALIAS_ID)
            obj = self.catalog.get_assessment(ALIAS_ID)
            assert obj.get_id() == self.assessment_ids[0]"""


class ItemLookupSession:
    # Override these locally for Item because with ItemQuerySession implemented,
    #   the authz adapter will return an empty List instead of throwing PermissionDenied
    get_item = """
        if not is_never_authz(self.service_config):
            self.catalog.use_isolated_bank_view()
            obj = self.catalog.get_item(self.item_list[0].ident)
            assert obj.ident == self.item_list[0].ident
            self.catalog.use_federated_bank_view()
            obj = self.catalog.get_item(self.item_list[0].ident)
            assert obj.ident == self.item_list[0].ident
        else:
            with pytest.raises(errors.NotFound):
                self.catalog.get_item(self.fake_id)"""

    get_items_by_ids = """
        from dlkit.abstract_osid.assessment.objects import ItemList
        objects = self.catalog.get_items_by_ids(self.item_ids)
        assert isinstance(objects, ItemList)
        self.catalog.use_federated_bank_view()
        objects = self.catalog.get_items_by_ids(self.item_ids)
        assert isinstance(objects, ItemList)
        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0"""

    get_items_by_genus_type = """
        from dlkit.abstract_osid.assessment.objects import ItemList
        objects = self.catalog.get_items_by_genus_type(DEFAULT_GENUS_TYPE)
        assert isinstance(objects, ItemList)
        self.catalog.use_federated_bank_view()
        objects = self.catalog.get_items_by_genus_type(DEFAULT_GENUS_TYPE)
        assert isinstance(objects, ItemList)
        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0"""

    get_items_by_parent_genus_type = """
        from dlkit.abstract_osid.assessment.objects import ItemList
        if not is_never_authz(self.service_config):
            objects = self.catalog.get_items_by_parent_genus_type(DEFAULT_GENUS_TYPE)
            assert isinstance(objects, ItemList)
            self.catalog.use_federated_bank_view()
            objects = self.catalog.get_items_by_parent_genus_type(DEFAULT_GENUS_TYPE)
            assert objects.available() == 0
            assert isinstance(objects, ItemList)
        else:
            with pytest.raises(errors.Unimplemented):
                # because the never_authz "tries harder" and runs the actual query...
                #    whereas above the method itself in JSON returns an empty list
                self.catalog.get_items_by_parent_genus_type(DEFAULT_GENUS_TYPE)"""

    get_items_by_record_type = """
        from dlkit.abstract_osid.assessment.objects import ItemList
        objects = self.catalog.get_items_by_record_type(DEFAULT_TYPE)
        assert isinstance(objects, ItemList)
        self.catalog.use_federated_bank_view()
        objects = self.catalog.get_items_by_record_type(DEFAULT_TYPE)
        assert objects.available() == 0
        assert isinstance(objects, ItemList)"""

    get_items = """
        from dlkit.abstract_osid.assessment.objects import ItemList
        objects = self.catalog.get_items()
        assert isinstance(objects, ItemList)
        self.catalog.use_federated_bank_view()
        objects = self.catalog.get_items()
        assert isinstance(objects, ItemList)

        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0

    def test_get_item_with_alias(self):
        if not is_never_authz(self.service_config):
            self.catalog.alias_item(self.item_ids[0], ALIAS_ID)
            obj = self.catalog.get_item(ALIAS_ID)
            assert obj.get_id() == self.item_ids[0]"""
