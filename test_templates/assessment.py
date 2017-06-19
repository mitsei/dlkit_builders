
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
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([SEQUENCE_ASSESSMENT])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)

        for number in ['One', 'Two', 'Three', 'Four']:
            ifc = cls.catalog.get_item_form_for_create([])
            ifc.set_display_name('Test Assessment Item ' + number)
            ifc.set_description('This is a Test Item Called Number ' + number)
            test_item = cls.catalog.create_item(ifc)
            form = cls.catalog.get_question_form_for_create(test_item.ident, [])
            cls.catalog.create_question(form)

            if number == 'One':
                form = cls.catalog.get_answer_form_for_create(test_item.ident, [])
                cls.catalog.create_answer(form)

            cls.catalog.add_item(cls.assessment.ident, test_item.ident)

        form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident, [])
        cls.assessment_offered = cls.catalog.create_assessment_offered(form)

    def setUp(self):
        self.session = self.catalog
        form = self.catalog.get_assessment_taken_form_for_create(self.assessment_offered.ident, [])
        self.taken = self.catalog.create_assessment_taken(form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessments():
            for offered in cls.catalog.get_assessments_offered_for_assessment(obj.ident):
                for taken in cls.catalog.get_assessments_taken_for_assessment_offered(offered.ident):
                    cls.catalog.delete_assessment_taken(taken.ident)
                cls.catalog.delete_assessment_offered(offered.ident)
            cls.catalog.delete_assessment(obj.ident)
        for item in cls.catalog.get_items():
            cls.catalog.delete_item(item.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    get_bank = """
        # this test should not be needed....
        self.assertTrue(isinstance(self.catalog, Bank))"""

    can_take_assessments = """
        self.assertTrue(self.session.can_take_assessments())"""

    get_assessment_section = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        test_section = self.session.get_assessment_section(section.ident)
        self.assertTrue(isinstance(test_section, AssessmentSection))
        self.assertEqual(str(test_section.ident),
                         str(section.ident))"""

    get_assessment_sections = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        test_sections = self.session.get_assessment_sections(self.taken.ident)
        self.assertTrue(isinstance(test_sections, AssessmentSectionList))
        self.assertEqual(test_sections.available(), 1)
        first_section = test_sections.next()
        self.assertTrue(isinstance(first_section, AssessmentSection))
        self.assertEqual(str(first_section.ident),
                         str(section.ident))"""

    get_first_assessment_section = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        self.assertTrue(isinstance(section, AssessmentSection))"""

    submit_response = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()

        self.assertIn('missingResponse',
                      section._my_map['questions'][0]['responses'][0])
        self.assertEqual(0, section._my_map['questions'][0]['responses'][0]['missingResponse'])

        form = self.session.get_response_form(section.ident, first_question.ident)
        self.session.submit_response(section.ident, first_question.ident, form)
        section = self.catalog.get_assessment_section(section.ident)

        self.assertNotIn('missingResponse',
                         section._my_map['questions'][0]['responses'][0])"""

    clear_response = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()

        self.assertIn('missingResponse',
                      section._my_map['questions'][0]['responses'][0])
        self.assertEqual(0, section._my_map['questions'][0]['responses'][0]['missingResponse'])

        form = self.session.get_response_form(section.ident, first_question.ident)
        self.session.submit_response(section.ident, first_question.ident, form)
        section = self.catalog.get_assessment_section(section.ident)

        self.assertNotIn('missingResponse',
                         section._my_map['questions'][0]['responses'][0])

        self.session.clear_response(section.ident, first_question.ident)
        section = self.catalog.get_assessment_section(section.ident)

        self.assertIn('missingResponse',
                      section._my_map['questions'][0]['responses'][0])
        self.assertEqual(1, section._my_map['questions'][0]['responses'][0]['missingResponse'])"""

    skip_item = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()

        self.assertIn('missingResponse',
                      section._my_map['questions'][0]['responses'][0])
        self.assertEqual(0, section._my_map['questions'][0]['responses'][0]['missingResponse'])

        self.session.skip_item(section.ident, first_question.ident)
        section = self.catalog.get_assessment_section(section.ident)

        self.assertIn('missingResponse',
                      section._my_map['questions'][0]['responses'][0])
        self.assertEqual(1, section._my_map['questions'][0]['responses'][0]['missingResponse'])"""

    finish_assessment = """
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
        with self.assertRaises(errors.IllegalState):
            self.session.finish_assessment(future_taken.ident)

        self.assertIsNone(self.taken._my_map['completionTime'])
        self.session.finish_assessment(self.taken.ident)
        taken = self.catalog.get_assessment_taken(self.taken.ident)
        self.assertIsNotNone(taken._my_map['completionTime'])"""

    finish_assessment_section = """
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
        with self.assertRaises(errors.IllegalState):
            self.catalog.get_first_assessment_section(future_taken.ident)

        first_section = self.catalog.get_first_assessment_section(self.taken.ident)
        self.assertNotIn('completionTime', first_section._my_map)
        self.session.finish_assessment_section(first_section.ident)

        with self.assertRaises(errors.IllegalState):
            # it is over, so can't GET the section now
            self.catalog.get_assessment_section(first_section.ident)"""

    has_assessment_begun = """
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
        self.assertFalse(self.session.has_assessment_begun(future_taken.ident))

        self.assertTrue(self.session.has_assessment_begun(self.taken.ident))"""

    has_assessment_section_begun = """
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

        with self.assertRaises(errors.IllegalState):
            # cannot even get the sectionId to call the method
            self.catalog.get_first_assessment_section(future_taken.ident)

        section = self.catalog.get_first_assessment_section(self.taken.ident)
        self.assertTrue(self.session.has_assessment_section_begun(section.ident))"""

    is_assessment_over = """
        # There are also other conditions that flag "over", but are not
        # tested here. Like if the offered goes past the deadline...so we
        # would have to do a time.sleep(). TODO: add those tests in.

        self.assertFalse(self.session.is_assessment_over(self.taken.ident))
        self.session.finish_assessment(self.taken.ident)
        self.assertTrue(self.session.is_assessment_over(self.taken.ident))"""

    is_assessment_section_over = """
        # There are also other conditions that flag "over", but are not
        # tested here. Like if the offered goes past the deadline...so we
        # would have to do a time.sleep(). TODO: add those tests in.

        section = self.catalog.get_first_assessment_section(self.taken.ident)

        self.assertFalse(self.session.is_assessment_section_over(section.ident))
        self.session.finish_assessment_section(section.ident)
        self.assertTrue(self.session.is_assessment_section_over(section.ident))"""

    get_answers = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()
        second_question = questions.next()

        with self.assertRaises(errors.IllegalState):
            self.session.get_answers(section.ident, second_question.ident)

        form = self.session.get_response_form(section.ident, first_question.ident)
        self.session.submit_response(section.ident, first_question.ident, form)

        answers = self.session.get_answers(section.ident, first_question.ident)
        self.assertTrue(isinstance(answers, AnswerList))
        self.assertEqual(answers.available(), 1)
        self.assertTrue(isinstance(answers.next(), Answer))"""

    is_answer_available = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()
        second_question = questions.next()

        self.assertFalse(self.session.is_answer_available(section.ident,
                                                          second_question.ident))

        form = self.session.get_response_form(section.ident, first_question.ident)
        self.session.submit_response(section.ident, first_question.ident, form)

        answers = self.session.get_answers(section.ident, first_question.ident)
        self.assertTrue(isinstance(answers, AnswerList))
        self.assertTrue(self.session.is_answer_available(section.ident,
                                                         first_question.ident))"""

    get_first_question = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()

        test_question = self.session.get_first_question(section.ident)
        self.assertTrue(isinstance(test_question, Question))
        self.assertEqual(str(first_question.ident),
                         str(test_question.ident))"""

    get_first_unanswered_question = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()
        second_question = questions.next()

        unanswered_question = self.session.get_first_unanswered_question(section.ident)
        self.assertTrue(isinstance(unanswered_question, Question))
        self.assertEqual(str(unanswered_question.ident),
                         str(first_question.ident))

        form = self.session.get_response_form(section.ident, first_question.ident)
        self.session.submit_response(section.ident, first_question.ident, form)

        unanswered_question = self.session.get_first_unanswered_question(section.ident)
        self.assertTrue(isinstance(unanswered_question, Question))
        self.assertEqual(str(unanswered_question.ident),
                         str(second_question.ident))"""

    is_question_answered = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()

        self.assertFalse(self.session.is_question_answered(section.ident,
                                                           first_question.ident))

        form = self.session.get_response_form(section.ident, first_question.ident)
        self.session.submit_response(section.ident, first_question.ident, form)

        self.assertTrue(self.session.is_question_answered(section.ident,
                                                          first_question.ident))"""

    get_incomplete_assessment_sections = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()

        test_sections = self.session.get_incomplete_assessment_sections(self.taken.ident)
        self.assertTrue(isinstance(test_sections, AssessmentSectionList))
        self.assertEqual(test_sections.available(), 1)
        first_section = test_sections.next()
        self.assertTrue(isinstance(first_section, AssessmentSection))
        self.assertEqual(str(first_section.ident),
                         str(section.ident))

        for question in questions:
            form = self.session.get_response_form(section.ident, question.ident)
            self.session.submit_response(section.ident, question.ident, form)

        self.session._provider_sessions = {}  # need to get rid of the cached taken
        test_sections = self.session.get_incomplete_assessment_sections(self.taken.ident)
        self.assertTrue(isinstance(test_sections, AssessmentSectionList))
        self.assertEqual(test_sections.available(), 0)"""

    is_assessment_section_complete = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        total_questions = questions.available()

        self.assertFalse(self.session.is_assessment_section_complete(section.ident))

        for index, question in enumerate(questions):
            form = self.session.get_response_form(section.ident, question.ident)
            self.session.submit_response(section.ident, question.ident, form)
            if index < (total_questions - 1):
                self.assertFalse(self.session.is_assessment_section_complete(section.ident))
            else:
                self.assertTrue(self.session.is_assessment_section_complete(section.ident))"""

    get_next_assessment_section = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        with self.assertRaises(errors.IllegalState):
            self.session.get_next_assessment_section(section.ident)"""

    get_previous_assessment_section = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        with self.assertRaises(errors.IllegalState):
            self.session.get_previous_assessment_section(section.ident)"""

    has_next_assessment_section = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        self.assertFalse(self.session.has_next_assessment_section(section.ident))"""

    has_previous_assessment_section = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        self.assertFalse(self.session.has_previous_assessment_section(section.ident))"""

    get_next_question = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()
        second_question = questions.next()
        third_question = questions.next()
        fourth_question = questions.next()

        test_question = self.session.get_next_question(section.ident,
                                                       first_question.ident)
        self.assertTrue(isinstance(test_question, Question))
        self.assertEqual(str(second_question.ident),
                         str(test_question.ident))

        with self.assertRaises(errors.IllegalState):
            self.session.get_next_question(section.ident, fourth_question.ident)"""

    has_next_question = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()
        second_question = questions.next()
        third_question = questions.next()
        fourth_question = questions.next()

        self.assertTrue(self.session.has_next_question(section.ident,
                                                       first_question.ident))
        self.assertFalse(self.session.has_next_question(section.ident,
                                                        fourth_question.ident))"""

    get_previous_question = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()
        second_question = questions.next()
        third_question = questions.next()
        fourth_question = questions.next()

        test_question = self.session.get_previous_question(section.ident,
                                                           fourth_question.ident)
        self.assertTrue(isinstance(test_question, Question))
        self.assertEqual(str(third_question.ident),
                         str(test_question.ident))

        with self.assertRaises(errors.IllegalState):
            self.session.get_previous_question(section.ident, first_question.ident)"""

    has_previous_question = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()
        second_question = questions.next()
        third_question = questions.next()
        fourth_question = questions.next()

        self.assertTrue(self.session.has_previous_question(section.ident,
                                                           fourth_question.ident))
        self.assertFalse(self.session.has_previous_question(section.ident,
                                                            first_question.ident))"""

    get_next_unanswered_question = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()
        second_question = questions.next()
        third_question = questions.next()
        fourth_question = questions.next()

        test_question = self.session.get_next_unanswered_question(section.ident,
                                                                  first_question.ident)
        self.assertTrue(isinstance(test_question, Question))
        self.assertEqual(str(second_question.ident),
                         str(test_question.ident))

        form = self.session.get_response_form(section.ident, second_question.ident)
        self.session.submit_response(section.ident, second_question.ident, form)

        test_question = self.session.get_next_unanswered_question(section.ident,
                                                                  first_question.ident)
        self.assertTrue(isinstance(test_question, Question))
        self.assertEqual(str(third_question.ident),
                         str(test_question.ident))

        with self.assertRaises(errors.IllegalState):
            self.session.get_next_unanswered_question(section.ident,
                                                      fourth_question.ident)"""

    has_next_unanswered_question = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()
        second_question = questions.next()
        third_question = questions.next()
        fourth_question = questions.next()

        self.assertTrue(self.session.has_next_unanswered_question(section.ident,
                                                                  first_question.ident))

        form = self.session.get_response_form(section.ident, second_question.ident)
        self.session.submit_response(section.ident, second_question.ident, form)

        self.assertTrue(self.session.has_next_unanswered_question(section.ident,
                                                                  first_question.ident))
        self.assertFalse(self.session.has_next_unanswered_question(section.ident,
                                                                   fourth_question.ident))"""

    get_previous_unanswered_question = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()
        second_question = questions.next()
        third_question = questions.next()
        fourth_question = questions.next()

        test_question = self.session.get_previous_unanswered_question(section.ident,
                                                                      fourth_question.ident)
        self.assertTrue(isinstance(test_question, Question))
        self.assertEqual(str(third_question.ident),
                         str(test_question.ident))

        form = self.session.get_response_form(section.ident, third_question.ident)
        self.session.submit_response(section.ident, third_question.ident, form)

        test_question = self.session.get_previous_unanswered_question(section.ident,
                                                                      fourth_question.ident)
        self.assertTrue(isinstance(test_question, Question))
        self.assertEqual(str(second_question.ident),
                         str(test_question.ident))

        with self.assertRaises(errors.IllegalState):
            self.session.get_previous_unanswered_question(section.ident,
                                                          first_question.ident)"""

    has_previous_unanswered_question = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()
        second_question = questions.next()
        third_question = questions.next()
        fourth_question = questions.next()

        self.assertTrue(self.session.has_previous_unanswered_question(section.ident,
                                                                      fourth_question.ident))

        form = self.session.get_response_form(section.ident, third_question.ident)
        self.session.submit_response(section.ident, third_question.ident, form)

        self.assertTrue(self.session.has_previous_unanswered_question(section.ident,
                                                                      fourth_question.ident))
        self.assertFalse(self.session.has_previous_unanswered_question(section.ident,
                                                                       first_question.ident))"""

    get_question = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()

        test_question = self.session.get_question(section.ident, first_question.ident)
        self.assertTrue(isinstance(test_question, Question))
        self.assertEqual(str(test_question.ident),
                         str(first_question.ident))"""

    get_questions = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()

        test_questions = self.session.get_questions(section.ident)
        self.assertTrue(isinstance(test_questions, QuestionList))
        self.assertEqual(test_questions.available(), 4)
        first_test_question = test_questions.next()
        self.assertTrue(isinstance(first_test_question, Question)),
        self.assertEqual(str(first_test_question.ident),
                         str(first_question.ident))"""

    get_unanswered_questions = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        question_ids = [q.ident for q in questions]

        test_questions = self.session.get_unanswered_questions(section.ident)
        self.assertTrue(isinstance(test_questions, QuestionList))
        self.assertEqual(test_questions.available(), 4)
        test_question_ids = [q.ident for q in test_questions]
        self.assertEqual(question_ids, test_question_ids)

        form = self.session.get_response_form(section.ident, question_ids[1])
        self.session.submit_response(section.ident, question_ids[1], form)

        test_questions = self.session.get_unanswered_questions(section.ident)
        self.assertTrue(isinstance(test_questions, QuestionList))
        self.assertEqual(test_questions.available(), 3)
        test_question_ids = [q.ident for q in test_questions]
        self.assertNotIn(question_ids[1], test_question_ids)"""

    get_response = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()

        test_response = self.session.get_response(section.ident, first_question.ident)
        self.assertTrue(isinstance(test_response, Response))

        with self.assertRaises(errors.IllegalState):
            test_response.object_map

        form = self.session.get_response_form(section.ident, first_question.ident)
        self.session.submit_response(section.ident, first_question.ident, form)

        test_response = self.session.get_response(section.ident, first_question.ident)
        self.assertTrue(isinstance(test_response, Response))

        test_response.object_map"""

    get_responses = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()

        test_responses = self.session.get_responses(section.ident)
        self.assertTrue(isinstance(test_responses, ResponseList))
        self.assertEqual(test_responses.available(), 4)
        first_response = test_responses.next()
        self.assertTrue(isinstance(first_response, Response))

        with self.assertRaises(errors.IllegalState):
            first_response.object_map"""

    get_response_form = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        first_question = questions.next()

        form = self.session.get_response_form(section.ident, first_question.ident)
        self.assertTrue(isinstance(form, AnswerForm))"""

    has_unanswered_questions = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()
        total_questions = questions.available()

        self.assertTrue(self.session.has_unanswered_questions(section.ident))

        for index, question in enumerate(questions):
            form = self.session.get_response_form(section.ident, question.ident)
            self.session.submit_response(section.ident, question.ident, form)
            if index < (total_questions - 1):
                self.assertTrue(self.session.has_unanswered_questions(section.ident))
            else:
                self.assertFalse(self.session.has_unanswered_questions(section.ident))"""

    requires_synchronous_responses = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        self.assertFalse(self.session.requires_synchronous_responses(section.ident))"""

    requires_synchronous_sections = """
        self.assertFalse(self.session.requires_synchronous_sections(self.taken.ident))"""


class AssessmentResultsSession:
    import_statements = [
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.records import registry',
        'SEQUENCE_ASSESSMENT = Type(**registry.ASSESSMENT_RECORD_TYPES["simple-child-sequencing"])'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentResultsSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([SEQUENCE_ASSESSMENT])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentResultsSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)

        for number in ['One', 'Two', 'Three', 'Four']:
            ifc = cls.catalog.get_item_form_for_create([])
            ifc.set_display_name('Test Assessment Item ' + number)
            ifc.set_description('This is a Test Item Called Number ' + number)
            test_item = cls.catalog.create_item(ifc)

            form = cls.catalog.get_question_form_for_create(test_item.ident, [])
            cls.catalog.create_question(form)

            cls.catalog.add_item(cls.assessment.ident, test_item.ident)

        form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident, [])
        cls.assessment_offered = cls.catalog.create_assessment_offered(form)

    def setUp(self):
        self.session = self.svc_mgr.get_assessment_results_session(proxy=self.catalog._proxy)
        form = self.catalog.get_assessment_taken_form_for_create(self.assessment_offered.ident, [])
        self.taken = self.catalog.create_assessment_taken(form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessments():
            for offered in cls.catalog.get_assessments_offered_for_assessment(obj.ident):
                for taken in cls.catalog.get_assessments_taken_for_assessment_offered(offered.ident):
                    cls.catalog.delete_assessment_taken(taken.ident)
                cls.catalog.delete_assessment_offered(offered.ident)
            cls.catalog.delete_assessment(obj.ident)
        for item in cls.catalog.get_items():
            cls.catalog.delete_item(item.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    are_results_available = """
        self.assertFalse(self.session.are_results_available(self.assessment.ident))"""

    can_access_assessment_results = """
        self.assertTrue(self.session.can_access_assessment_results())"""

    get_grade_entries = """
        with self.assertRaises(errors.IllegalState):
            self.session.get_grade_entries(self.assessment.ident)"""

    get_items = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        section.get_questions()
        self.assertEqual(self.session.get_items(self.taken.ident).available(), 4)"""

    get_responses = """
        section = self.catalog.get_first_assessment_section(self.taken.ident)
        questions = section.get_questions()

        test_responses = self.session.get_responses(self.taken.ident)
        self.assertTrue(isinstance(test_responses, ResponseList))
        self.assertEqual(test_responses.available(), 4)
        first_response = test_responses.next()
        self.assertTrue(isinstance(first_response, Response))

        with self.assertRaises(errors.IllegalState):
            first_response.object_map"""


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
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for ItemAdminSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

    def setUp(self):
        create_form = self.catalog.get_item_form_for_create([])
        create_form.display_name = 'new Item'
        create_form.description = 'description of Item'
        create_form.set_genus_type(NEW_TYPE)
        self.osid_object = self.catalog.create_item(create_form)
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessments():
            for offered in cls.catalog.get_assessments_offered_for_assessment(obj.ident):
                for taken in cls.catalog.get_assessments_taken_for_assessment_offered(offered.ident):
                    cls.catalog.delete_assessment_taken(taken.ident)
                cls.catalog.delete_assessment_offered(offered.ident)
            cls.catalog.delete_assessment(obj.ident)
        for item in cls.catalog.get_items():
            cls.catalog.delete_item(item.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    create_answer = """
        self.assertEqual(self.osid_object.get_answers().available(), 0)
        form = self.session.get_answer_form_for_create(self.osid_object.ident, [])
        self.session.create_answer(form)
        updated_item = self.catalog.get_item(self.osid_object.ident)
        self.assertEqual(updated_item.get_answers().available(), 1)"""

    create_question = """
        with self.assertRaises(TypeError):
            # question_map = dict(self._my_map['question'])
            # TypeError: 'NoneType' object is not iterable
            self.osid_object.get_question()

        form = self.session.get_question_form_for_create(self.osid_object.ident, [])
        self.session.create_question(form)
        updated_item = self.catalog.get_item(self.osid_object.ident)
        self.assertTrue(isinstance(updated_item.get_question(), Question))"""

    delete_answer = """
        self.assertEqual(self.osid_object.get_answers().available(), 0)
        form = self.session.get_answer_form_for_create(self.osid_object.ident, [])
        answer = self.session.create_answer(form)
        updated_item = self.catalog.get_item(self.osid_object.ident)
        self.assertEqual(updated_item.get_answers().available(), 1)

        with self.assertRaises(errors.NotFound):
            self.session.delete_answer(Id('fake.Package%3A000000000000000000000000%40ODL.MIT.EDU'))

        self.session.delete_answer(answer.ident)
        updated_item = self.catalog.get_item(self.osid_object.ident)
        self.assertEqual(updated_item.get_answers().available(), 0)"""

    delete_question = """
        with self.assertRaises(TypeError):
            # question_map = dict(self._my_map['question'])
            # TypeError: 'NoneType' object is not iterable
            self.osid_object.get_question()

        form = self.session.get_question_form_for_create(self.osid_object.ident, [])
        question = self.session.create_question(form)
        updated_item = self.catalog.get_item(self.osid_object.ident)
        self.assertTrue(isinstance(updated_item.get_question(), Question))

        with self.assertRaises(errors.NotFound):
            self.session.delete_question(Id('fake.Package%3A000000000000000000000000%40ODL.MIT.EDU'))

        self.session.delete_question(question.ident)
        updated_item = self.catalog.get_item(self.osid_object.ident)

        with self.assertRaises(TypeError):
            updated_item.get_question()"""

    get_answer_form_for_create = """
        form = self.session.get_answer_form_for_create(self.osid_object.ident, [])
        self.assertTrue(isinstance(form, objects.AnswerForm))
        self.assertFalse(form.is_for_update())"""

    get_question_form_for_create = """
        form = self.session.get_question_form_for_create(self.osid_object.ident, [])
        self.assertTrue(isinstance(form, objects.QuestionForm))
        self.assertFalse(form.is_for_update())"""

    get_answer_form_for_update = """
        form = self.session.get_answer_form_for_create(self.osid_object.ident, [])
        answer = self.session.create_answer(form)

        form = self.session.get_answer_form_for_update(answer.ident)
        self.assertTrue(isinstance(form, objects.AnswerForm))
        self.assertTrue(form.is_for_update())"""

    get_question_form_for_update = """
        form = self.session.get_question_form_for_create(self.osid_object.ident, [])
        question = self.session.create_question(form)

        form = self.session.get_question_form_for_update(question.ident)
        self.assertTrue(isinstance(form, objects.QuestionForm))
        self.assertTrue(form.is_for_update())"""

    update_answer = """
        form = self.session.get_answer_form_for_create(self.osid_object.ident, [])
        form.display_name = 'first name'
        answer = self.session.create_answer(form)
        self.assertEqual(answer.display_name.text, 'first name')

        form = self.session.get_answer_form_for_update(answer.ident)
        form.display_name = 'second name'
        answer = self.session.update_answer(form)
        self.assertTrue(isinstance(answer, objects.Answer))
        self.assertEqual(answer.display_name.text, 'second name')"""

    update_question = """
        form = self.session.get_question_form_for_create(self.osid_object.ident, [])
        question = self.session.create_question(form)
        self.assertEqual(question.display_name.text, 'new Item')

        form = self.session.get_question_form_for_update(question.ident)
        form.display_name = 'second name'
        question = self.session.update_question(form)
        self.assertTrue(isinstance(question, objects.Question))
        self.assertEqual(question.display_name.text, 'second name')"""


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
    @classmethod
    def setUpClass(cls):
        cls.item_list = list()
        cls.item_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for ItemBankSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank for Assignment'
        create_form.description = 'Test Bank for ItemBankSession tests assignment'
        cls.assigned_catalog = cls.svc_mgr.create_bank(create_form)
        for num in [0, 1, 2]:
            create_form = cls.catalog.get_item_form_for_create([])
            create_form.display_name = 'Test Item ' + str(num)
            create_form.description = 'Test Item for ItemBankSession tests'
            obj = cls.catalog.create_item(create_form)
            cls.item_list.append(obj)
            cls.item_ids.append(obj.ident)
        cls.svc_mgr.assign_item_to_bank(
            cls.item_ids[1], cls.assigned_catalog.ident)
        cls.svc_mgr.assign_item_to_bank(
            cls.item_ids[2], cls.assigned_catalog.ident)

    def setUp(self):
        self.session = self.svc_mgr

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.unassign_item_from_bank(
            cls.item_ids[1], cls.assigned_catalog.ident)
        cls.svc_mgr.unassign_item_from_bank(
            cls.item_ids[2], cls.assigned_catalog.ident)
        for obj in cls.catalog.get_items():
            cls.catalog.delete_item(obj.ident)
        cls.svc_mgr.delete_bank(cls.assigned_catalog.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    can_lookup_item_bank_mappings = """
        result = self.session.can_lookup_item_bank_mappings()
        self.assertTrue(result)"""


class AssessmentAdminSession:

    import_statements = [
    ]


class AssessmentOfferedLookupSession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.assessment_offered_list = list()
        cls.assessment_offered_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentOfferedLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedLookupSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident, [])
            create_form.display_name = 'Test AssessmentOffered ' + str(num)
            create_form.description = 'Test AssessmentOffered for AssessmentOfferedLookupSession tests'
            obj = cls.catalog.create_assessment_offered(create_form)
            cls.assessment_offered_list.append(obj)
            cls.assessment_offered_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_banks():
            for obj in catalog.get_assessments_offered():
                catalog.delete_assessment_offered(obj.ident)
            for obj in catalog.get_assessments():
                catalog.delete_assessment(obj.ident)
            cls.svc_mgr.delete_bank(catalog.ident)"""


class AssessmentTakenLookupSession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.assessment_taken_list = list()
        cls.assessment_taken_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentTakenLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedLookupSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        create_form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident, [])
        create_form.display_name = 'Test AssessmentOffered'
        create_form.description = 'Test AssessmentOffered for AssessmentOfferedLookupSession tests'
        cls.assessment_offered = cls.catalog.create_assessment_offered(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_assessment_taken_form_for_create(cls.assessment_offered.ident, [])
            create_form.display_name = 'Test AssessmentTaken ' + str(num)
            create_form.description = 'Test AssessmentTaken for AssessmentTakenLookupSession tests'
            obj = cls.catalog.create_assessment_taken(create_form)
            cls.assessment_taken_list.append(obj)
            cls.assessment_taken_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_banks():
            for obj in catalog.get_assessments_taken():
                catalog.delete_assessment_taken(obj.ident)
            for obj in catalog.get_assessments_offered():
                catalog.delete_assessment_offered(obj.ident)
            for obj in catalog.get_assessments():
                catalog.delete_assessment(obj.ident)
            cls.svc_mgr.delete_bank(catalog.ident)"""

    # This is hand built, but there may be a pattern to try to map, specifically
    # getting objects for another package object and a persisted id thingy
    get_assessments_taken_for_taker_and_assessment_offered = """
        pass"""

    get_assessments_taken_for_assessment = """
        pass"""


class AssessmentTakenAdminSession:

    import_statements = [
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.abstract_osid.assessment.objects import AssessmentTaken',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})',
        'NEW_TYPE_2 = Type(**{\'identifier\': \'NEW 2\', \'namespace\': \'MINE 2\', \'authority\': \'YOURS 2\'})'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentOfferedLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedLookupSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        create_form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident, [])
        create_form.display_name = 'Test AssessmentOffered'
        create_form.description = 'Test AssessmentOffered for AssessmentTakenAdminSession tests'
        obj = cls.catalog.create_assessment_offered(create_form)
        cls.assessment_offered = obj
        form = cls.catalog.get_assessment_taken_form_for_create(cls.assessment_offered.ident, [])
        form.display_name = 'new AssessmentTaken'
        form.description = 'description of AssessmentTaken'
        form.set_genus_type(NEW_TYPE)
        cls.osid_object = cls.catalog.create_assessment_taken(form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessments_taken():
            cls.catalog.delete_assessment_taken(obj.ident)
        for obj in cls.catalog.get_assessments_offered():
            cls.catalog.delete_assessment_offered(obj.ident)
        for obj in cls.catalog.get_assessments():
            cls.catalog.delete_assessment(obj.ident)
        for obj in cls.catalog.get_items():
            cls.catalog.delete_item(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    get_assessment_taken_form_for_create = """
        form = self.catalog.get_assessment_taken_form_for_create(self.assessment_offered.ident, [])
        self.assertTrue(isinstance(form, OsidForm))
        self.assertFalse(form.is_for_update())"""

    delete_assessment_taken = """
        form = self.catalog.get_assessment_taken_form_for_create(self.assessment_offered.ident, [])
        form.display_name = 'new Assessment Taken'
        form.set_genus_type(NEW_TYPE)
        osid_object = self.catalog.create_assessment_taken(form)
        self.catalog.delete_assessment_taken(osid_object.ident)
        with self.assertRaises(errors.NotFound):
            self.catalog.get_assessment_taken(osid_object.ident)"""

    ##
    # This impl may differ from the usual create_osid_object method in that it
    # deals with agent id and default display name based on the underlying Assessment
    # and checks for exceeding max attempts...
    proposed_create_assessment_taken = """
        pass"""


class AssessmentOfferedBankSession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.assessment_offered_list = list()
        cls.assessment_offered_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentOfferedLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank Assigned'
        create_form.description = 'Test Bank for AssessmentOfferedBankSession tests'
        cls.assigned_catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedBankSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        for num in [0, 1, 2]:
            create_form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident, [])
            create_form.display_name = 'Test AssessmentOffered ' + str(num)
            create_form.description = 'Test AssessmentOffered for AssessmentOfferedBankSession tests'
            obj = cls.catalog.create_assessment_offered(create_form)
            cls.assessment_offered_list.append(obj)
            cls.assessment_offered_ids.append(obj.ident)
        cls.svc_mgr.assign_assessment_offered_to_bank(
            cls.assessment_offered_ids[1], cls.assigned_catalog.ident)
        cls.svc_mgr.assign_assessment_offered_to_bank(
            cls.assessment_offered_ids[2], cls.assigned_catalog.ident)

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.unassign_assessment_offered_from_bank(
            cls.assessment_offered_ids[1], cls.assigned_catalog.ident)
        cls.svc_mgr.unassign_assessment_offered_from_bank(
            cls.assessment_offered_ids[2], cls.assigned_catalog.ident)
        for catalog in cls.svc_mgr.get_banks():
            for obj in catalog.get_assessments_offered():
                catalog.delete_assessment_offered(obj.ident)
            for obj in catalog.get_assessments():
                catalog.delete_assessment(obj.ident)
            cls.svc_mgr.delete_bank(catalog.ident)"""


class AssessmentTakenBankSession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.assessment_taken_list = list()
        cls.assessment_taken_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentTakenBankSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank Assigned'
        create_form.description = 'Test Bank for AssessmentTakenBankSession tests'
        cls.assigned_catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentTakenBankSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        create_form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident, [])
        create_form.display_name = 'Test AssessmentOffered'
        create_form.description = 'Test AssessmentOffered for AssessmentTakenLBankSession tests'
        cls.assessment_offered = cls.catalog.create_assessment_offered(create_form)
        for num in [0, 1, 2]:
            create_form = cls.catalog.get_assessment_taken_form_for_create(cls.assessment_offered.ident, [])
            create_form.display_name = 'Test AssessmentTaken ' + str(num)
            create_form.description = 'Test AssessmentTaken for AssessmentTakenLookupSession tests'
            obj = cls.catalog.create_assessment_taken(create_form)
            cls.assessment_taken_list.append(obj)
            cls.assessment_taken_ids.append(obj.ident)
        cls.svc_mgr.assign_assessment_taken_to_bank(
            cls.assessment_taken_ids[1], cls.assigned_catalog.ident)
        cls.svc_mgr.assign_assessment_taken_to_bank(
            cls.assessment_taken_ids[2], cls.assigned_catalog.ident)

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.unassign_assessment_taken_from_bank(
            cls.assessment_taken_ids[1], cls.assigned_catalog.ident)
        cls.svc_mgr.unassign_assessment_taken_from_bank(
            cls.assessment_taken_ids[2], cls.assigned_catalog.ident)
        for catalog in cls.svc_mgr.get_banks():
            for obj in catalog.get_assessments_taken():
                catalog.delete_assessment_taken(obj.ident)
            for obj in catalog.get_assessments_offered():
                catalog.delete_assessment_offered(obj.ident)
            for obj in catalog.get_assessments():
                catalog.delete_assessment(obj.ident)
            cls.svc_mgr.delete_bank(catalog.ident)"""


class AssessmentBasicAuthoringSession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.assessment_offered_list = list()
        cls.assessment_offered_ids = list()
        simple_sequence_record_type = Type(**{
            'authority': 'ODL.MIT.EDU',
            'namespace': 'osid-object',
            'identifier': 'simple-child-sequencing'})
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        # cls.auth_svc_mgr = Runtime().get_service_manager('ASSESSMENT_AUTHORING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentBasicAuthoringSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([simple_sequence_record_type])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentBasicAuthoringSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        cls.test_items = list()
        cls.test_item_ids = list()
        for number in ['One', 'Two', 'Three', 'Four']:
            ifc = cls.catalog.get_item_form_for_create([])
            ifc.set_display_name('Test Assessment Item ' + number)
            ifc.set_description('This is a Test Item Called Number ' + number)
            test_item = cls.catalog.create_item(ifc)
            cls.test_items.append(test_item)
            cls.test_item_ids.append(test_item.ident)
            cls.catalog.add_item(cls.assessment.ident, test_item.ident)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessments():
            cls.catalog.delete_assessment(obj.ident)
        for obj in cls.catalog.get_items():
            cls.catalog.delete_item(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    can_author_assessments = """
        pass"""

    get_items = """
        self.assertEqual(self.catalog.get_assessment_items(self.assessment.ident).available(), 4)"""

    add_item = """
        self._reorder_items()
        ifc = self.catalog.get_item_form_for_create([])
        ifc.set_display_name('Test Assessment Additional Item')
        ifc.set_description('This is an addtional Test Item')
        additional_item = self.catalog.create_item(ifc)
        self.catalog.add_item(self.assessment.ident, additional_item.ident)
        self.assertEqual(self.catalog.get_assessment_items(self.assessment.ident).available(), 5)
        self.catalog.remove_item(self.assessment.ident, additional_item.ident)"""

    remove_item = """
        self._reorder_items()
        self.catalog.remove_item(self.assessment.ident, self.test_item_ids[1])
        self.assertEqual(self.catalog.get_assessment_items(self.assessment.ident).available(), 3)
        self.catalog.add_item(self.assessment.ident, self.test_item_ids[1])
        items = self.catalog.get_assessment_items(self.assessment.ident)
        self.assertEqual(items.next().ident, self.test_item_ids[0])
        self.assertEqual(items.next().ident, self.test_item_ids[2])
        self.assertEqual(items.next().ident, self.test_item_ids[3])
        self.assertEqual(items.next().ident, self.test_item_ids[1])"""

    move_item = """
        self._reorder_items()
        self.catalog.move_item(self.assessment.ident, self.test_item_ids[0], self.test_item_ids[3])
        items = self.catalog.get_assessment_items(self.assessment.ident)
        self.assertEqual(items.next().ident, self.test_item_ids[1])
        self.assertEqual(items.next().ident, self.test_item_ids[2])
        self.assertEqual(items.next().ident, self.test_item_ids[3])
        self.assertEqual(items.next().ident, self.test_item_ids[0])"""

    order_items = """
        self.catalog.order_items([
            self.test_item_ids[3],
            self.test_item_ids[2],
            self.test_item_ids[1],
            self.test_item_ids[0]],
            self.assessment.ident)
        self.assertEqual(self.catalog.get_assessment_items(self.assessment.ident).next().ident, self.test_item_ids[3])

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
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        item_form = cls.catalog.get_item_form_for_create([])
        item_form.display_name = 'Item'
        cls.item = cls.catalog.create_item(item_form)

        form = cls.catalog.get_question_form_for_create(cls.item.ident, [])
        form.display_name = 'Test question'
        cls.question = cls.catalog.create_question(form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_items():
            cls.catalog.delete_item(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""


class QuestionForm:

    import_statements = [
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        item_form = cls.catalog.get_item_form_for_create([])
        item_form.display_name = 'Item'
        cls.item = cls.catalog.create_item(item_form)

        cls.form = cls.catalog.get_question_form_for_create(cls.item.ident, [])

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_items():
            cls.catalog.delete_item(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""


class QuestionQuery:

    import_statements = [
        'from dlkit.json_.assessment.queries import QuestionQuery'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

    def setUp(self):
        # Since the session isn't implemented, we just construct a QuestionQuery directly
        self.query = QuestionQuery(runtime=self.catalog._runtime)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_items():
            cls.catalog.delete_item(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""


class QuestionList:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for QuestionList tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

    def setUp(self):
        from dlkit.json_.assessment.objects import QuestionList
        self.question_list = list()
        self.question_ids = list()
        for num in [0, 1]:
            item_form = self.catalog.get_item_form_for_create([])
            item_form.display_name = 'Item'
            item = self.catalog.create_item(item_form)

            create_form = self.catalog.get_question_form_for_create(item.ident, [])
            create_form.display_name = 'Test Question ' + str(num)
            create_form.description = 'Test Question for QuestionList tests'
            obj = self.catalog.create_question(create_form)
            self.question_list.append(obj)
            self.question_ids.append(obj.ident)
        self.question_list = QuestionList(self.question_list)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_items():
            cls.catalog.delete_item(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""


class Answer:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        item_form = cls.catalog.get_item_form_for_create([])
        item_form.display_name = 'Item'
        cls.item = cls.catalog.create_item(item_form)

        form = cls.catalog.get_answer_form_for_create(cls.item.ident, [])
        form.display_name = 'Test answer'
        cls.answer = cls.catalog.create_answer(form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_items():
            cls.catalog.delete_item(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""


class AnswerForm:
    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        item_form = cls.catalog.get_item_form_for_create([])
        item_form.display_name = 'Item'
        cls.item = cls.catalog.create_item(item_form)

        cls.form = cls.catalog.get_answer_form_for_create(cls.item.ident, [])

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_items():
            cls.catalog.delete_item(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""


class AnswerQuery:

    import_statements = [
        'from dlkit.json_.assessment.queries import AnswerQuery'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

    def setUp(self):
        # Since the session isn't implemented, we just construct a AnswerQuery directly
        self.query = AnswerQuery(runtime=self.catalog._runtime)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_items():
            cls.catalog.delete_item(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""


class AnswerList:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AnswerList tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

    def setUp(self):
        from dlkit.json_.assessment.objects import AnswerList
        self.answer_list = list()
        self.answer_ids = list()
        for num in [0, 1]:
            item_form = self.catalog.get_item_form_for_create([])
            item_form.display_name = 'Item'
            item = self.catalog.create_item(item_form)

            create_form = self.catalog.get_answer_form_for_create(item.ident, [])
            create_form.display_name = 'Test Answer ' + str(num)
            create_form.description = 'Test Answer for AnswerList tests'
            obj = self.catalog.create_answer(create_form)
            self.answer_list.append(obj)
            self.answer_ids.append(obj.ident)
        self.answer_list = AnswerList(self.answer_list)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_items():
            cls.catalog.delete_item(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""


class Item:
    import_statements = [
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.json_.assessment.objects import Question, AnswerList',
        'from dlkit.json_.id.objects import IdList',
        'from dlkit.json_.learning.objects import ObjectiveList'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        cls.lsvc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.lsvc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test objective bank'
        create_form.description = 'Test objective bank description'
        cls.objective_bank = cls.lsvc_mgr.create_objective_bank(create_form)
        cls.objectives = list()
        for _ in range(2):
            form = cls.objective_bank.get_objective_form_for_create([])
            objective = cls.objective_bank.create_objective(form)
            cls.objectives.append(objective)

    def setUp(self):
        form = self.catalog.get_item_form_for_create([])
        form.display_name = 'Test object'
        form.set_learning_objectives([self.objectives[0].ident,
                                      self.objectives[1].ident])
        self.item = self.catalog.create_item(form)

        form = self.catalog.get_question_form_for_create(self.item.ident, [])
        self.catalog.create_question(form)

        form = self.catalog.get_answer_form_for_create(self.item.ident, [])
        form.set_genus_type(Type('answer-genus%3Aright-answer%40ODL.MIT.EDU'))
        self.catalog.create_answer(form)

        self.item = self.catalog.get_item(self.item.ident)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_items():
            cls.catalog.delete_item(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)

        for obj in cls.objective_bank.get_objectives():
            cls.objective_bank.delete_objective(obj.ident)
        cls.lsvc_mgr.delete_objective_bank(cls.objective_bank.ident)"""

    get_learning_objective_ids = """
        lo_ids = self.item.get_learning_objective_ids()
        self.assertTrue(isinstance(lo_ids, IdList))
        self.assertEqual(lo_ids.available(), 2)
        self.assertEqual(str(next(lo_ids)), str(self.objectives[0].ident))
        self.assertEqual(str(next(lo_ids)), str(self.objectives[1].ident))"""

    get_learning_objectives = """
        los = self.item.get_learning_objectives()
        self.assertTrue(isinstance(los, ObjectiveList))
        self.assertEqual(los.available(), 2)
        self.assertEqual(str(next(los).ident), str(self.objectives[0].ident))
        self.assertEqual(str(next(los).ident), str(self.objectives[1].ident))"""

    get_answer_ids = """
        answer_ids = self.item.get_answer_ids()
        self.assertTrue(isinstance(answer_ids, IdList))
        self.assertEqual(answer_ids.available(), 1)"""

    get_answers = """
        answers = self.item.get_answers()
        self.assertTrue(isinstance(answers, AnswerList))
        self.assertEqual(answers.available(), 1)
        self.assertEqual(str(next(answers).genus_type),
                         'answer-genus%3Aright-answer%40ODL.MIT.EDU')"""

    get_question_id = """
        question_id = self.item.get_question_id()
        self.assertTrue(isinstance(question_id, Id))
        self.assertEqual(str(question_id), str(self.item.ident))"""

    get_question = """
        question = self.item.get_question()
        self.assertTrue(isinstance(question, Question))
        self.assertEqual(str(question.ident),
                         str(self.item.ident))"""


class ItemQuery:
    import_statement = [
        'from dlkit.primordium.id.primitives import Id'
    ]

    match_learning_objective_id = """
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('learningObjectiveIds', self.query._query_terms)
        self.query.match_learning_objective_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['learningObjectiveIds'], {
            '$in': [str(test_id)]
        })"""

    clear_learning_objective_id_terms = """
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_learning_objective_id(test_id, match=True)
        self.assertIn('learningObjectiveIds',
                      self.query._query_terms)
        self.query.clear_learning_objective_id_terms()
        self.assertNotIn('learningObjectiveIds',
                         self.query._query_terms)"""

    clear_learning_objective_terms = """
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_any_learning_objective(match=True)
        self.assertIn('learningObjectiveIds',
                      self.query._query_terms)
        self.query.clear_learning_objective_terms()
        self.assertNotIn('learningObjectiveIds',
                         self.query._query_terms)"""

    match_any_learning_objective = """
        self.assertNotIn('learningObjectiveIds', self.query._query_terms)
        self.query.match_any_learning_objective(match=True)
        self.assertEqual(self.query._query_terms['learningObjectiveIds'], {
            '$exists': 'true',
            '$nin': [[], ['']]
        })"""


class ItemQuerySession:
    import_statements = [
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for ItemQuerySession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = cls.catalog.get_item_form_for_create([])
            create_form.display_name = 'Test Item ' + color
            create_form.description = (
                'Test Item for ItemQuerySession tests, did I mention green')
            obj = cls.catalog.create_item(create_form)

    def setUp(self):
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessments():
            for offered in cls.catalog.get_assessments_offered_for_assessment(obj.ident):
                for taken in cls.catalog.get_assessments_taken_for_assessment_offered(offered.ident):
                    cls.catalog.delete_assessment_taken(taken.ident)
                cls.catalog.delete_assessment_offered(offered.ident)
            cls.catalog.delete_assessment(obj.ident)
        for item in cls.catalog.get_items():
            cls.catalog.delete_item(item.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    can_search_items = """
        self.assertTrue(self.session.can_search_items())"""


class ItemSearchSession:
    import_statements = [
        'from dlkit.json_.assessment import searches',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.primordium.locale.types.string import get_type_data as get_string_type_data',
        'DEFAULT_STRING_MATCH_TYPE = Type(**get_string_type_data("WORDIGNORECASE"))'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for ItemSearchSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = cls.catalog.get_item_form_for_create([])
            create_form.display_name = 'Test Item ' + color
            create_form.description = (
                'Test Item for ItemSearchSession tests, did I mention green')
            obj = cls.catalog.create_item(create_form)

    def setUp(self):
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessments():
            for offered in cls.catalog.get_assessments_offered_for_assessment(obj.ident):
                for taken in cls.catalog.get_assessments_taken_for_assessment_offered(offered.ident):
                    cls.catalog.delete_assessment_taken(taken.ident)
                cls.catalog.delete_assessment_offered(offered.ident)
            cls.catalog.delete_assessment(obj.ident)
        for item in cls.catalog.get_items():
            cls.catalog.delete_item(item.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    get_item_search = """
        search = self.session.get_item_search()
        self.assertTrue(isinstance(search, searches.ItemSearch))"""

    get_items_by_search = """
        query = self.session.get_item_query()
        query.match_display_name('zxy', DEFAULT_STRING_MATCH_TYPE, True)
        search = self.session.get_item_search()
        results = self.session.get_items_by_search(query, search)
        self.assertTrue(isinstance(results, searches.ItemSearchResults))
        self.assertEqual(results.get_result_size(), 0)"""


class AssessmentOffered:

    import_statements = [
        'import datetime',
        'from dlkit.primordium.calendaring.primitives import DateTime, Duration',
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.json_.assessment.objects import Assessment'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        form = cls.catalog.get_assessment_form_for_create([])
        form.display_name = 'Assessment'
        cls.assessment = cls.catalog.create_assessment(form)

        form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident, [])
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
        cls.object = cls.catalog.create_assessment_offered(form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessments():
            for offered in cls.catalog.get_assessments_offered_for_assessment(obj.ident):
                cls.catalog.delete_assessment_offered(offered.ident)
            cls.catalog.delete_assessment(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    get_assessment_id = """
        self.assertTrue(isinstance(self.object.get_assessment_id(), Id))
        self.assertEqual(str(self.object.get_assessment_id()),
                         str(self.assessment.ident))"""

    get_assessment = """
        self.assertTrue(isinstance(self.object.get_assessment(), Assessment))
        self.assertEqual(str(self.object.get_assessment().ident),
                         str(self.assessment.ident))"""

    get_start_time_template = """
        # From test_templates/assessment.py::AssessmentOffered::get_start_time_template
        self.assertTrue(isinstance(self.object.get_start_time(), DateTime))"""

    get_duration_template = """
        # From test_templates/assessment.py::AssessmentOffered::get_duration_template
        self.assertTrue(isinstance(self.object.get_duration(), Duration))"""

    has_rubric = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set rubricId?
        self.assertRaises(KeyError,
                          self.object.has_rubric)"""

    get_rubric = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set rubricId?
        self.assertRaises(KeyError,
                          self.object.get_rubric)"""

    get_rubric_id = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set rubricId?
        self.assertRaises(KeyError,
                          self.object.get_rubric_id)"""

    is_graded = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set graded?
        self.assertRaises(KeyError,
                          self.object.is_graded)"""

    is_scored = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set scored?
        self.assertRaises(KeyError,
                          self.object.is_scored)"""


class AssessmentOfferedAdminSession:
    import_statements = [
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.abstract_osid.assessment.objects import AssessmentOffered',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})',
        'NEW_TYPE_2 = Type(**{\'identifier\': \'NEW 2\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.assessment_offered_list = list()
        cls.assessment_offered_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentOfferedLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedLookupSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident, [])
            create_form.display_name = 'Test AssessmentOffered ' + str(num)
            create_form.description = 'Test AssessmentOffered for AssessmentOfferedAdminSession tests'
            obj = cls.catalog.create_assessment_offered(create_form)
            cls.assessment_offered_list.append(obj)
            cls.assessment_offered_ids.append(obj.ident)
        create_form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident, [])
        create_form.display_name = 'new AssessmentOffered'
        create_form.description = 'description of AssessmentOffered'
        create_form.genus_type = NEW_TYPE
        cls.osid_object = cls.catalog.create_assessment_offered(create_form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessments_taken():
            cls.catalog.delete_assessment_taken(obj.ident)
        for obj in cls.catalog.get_assessments_offered():
            cls.catalog.delete_assessment_offered(obj.ident)
        for obj in cls.catalog.get_assessments():
            cls.catalog.delete_assessment(obj.ident)
        for obj in cls.catalog.get_items():
            cls.catalog.delete_item(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    get_assessment_offered_form_for_create = """
        form = self.catalog.get_assessment_offered_form_for_create(self.assessment.ident, [])
        self.assertTrue(isinstance(form, OsidForm))
        self.assertFalse(form.is_for_update())"""

    delete_assessment_offered = """
        form = self.catalog.get_assessment_offered_form_for_create(self.assessment.ident, [])
        form.display_name = 'new Assessment Offered'
        form.set_genus_type(NEW_TYPE)
        osid_object = self.catalog.create_assessment_offered(form)
        self.catalog.delete_assessment_offered(osid_object.ident)
        with self.assertRaises(errors.NotFound):
            self.catalog.get_assessment_offered(osid_object.ident)"""


class AssessmentOfferedForm:
    import_statements_pattern = [
        'from dlkit.primordium.calendaring.primitives import DateTime, Duration'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentOfferedLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedLookupSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)

        cls.form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident,
                                                                      [])

    def setUp(self):
        self.form = self.catalog.get_assessment_offered_form_for_create(self.assessment.ident,
                                                                        [])

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessments_offered():
            cls.catalog.delete_assessment_offered(obj.ident)
        for obj in cls.catalog.get_assessments():
            cls.catalog.delete_assessment(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    set_start_time_template = """
        # From test_templates/assessment.py::AssessmentOfferedForm::set_start_time_template
        test_time = DateTime.utcnow()
        self.assertIsNone(self.form._my_map['${var_name_mixed}'])
        self.form.${method_name}(test_time)
        self.assertEqual(self.form._my_map['${var_name_mixed}'],
                         test_time)
        with self.assertRaises(errors.InvalidArgument):
            self.form.${method_name}(True)
        # reset this for other tests
        self.form._my_map['${var_name_mixed}'] = None"""

    # This looks just like the generic one. Need to find in the pattern?
    clear_start_time_template = """
        # From test_templates/assessment.py::AssessmentOfferedForm::clear_start_time_template
        test_time = DateTime.utcnow()
        self.assertIsNone(self.form._my_map['${var_name_mixed}'])
        self.form.set_${var_name}(test_time)
        self.assertEqual(self.form._my_map['${var_name_mixed}'],
                         test_time)
        self.form.${method_name}()
        self.assertEqual(self.form._my_map['${var_name_mixed}'], self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0])"""

    set_duration_template = """
        # From test_templates/assessment.py::AssessmentOfferedForm::set_duration_template
        test_duration = Duration(hours=1)
        self.assertIsNone(self.form._my_map['${var_name_mixed}'])
        self.form.${method_name}(test_duration)
        self.assertEqual(self.form._my_map['${var_name_mixed}']['seconds'], 3600)
        self.assertEqual(self.form._my_map['${var_name_mixed}']['days'], 0)
        self.assertEqual(self.form._my_map['${var_name_mixed}']['microseconds'], 0)
        with self.assertRaises(errors.InvalidArgument):
            self.form.${method_name}(1.05)
        # reset this for other tests
        self.form._my_map['${var_name_mixed}'] = None"""

    clear_duration_template = """
        # From test_templates/assessment.py::AssessmentOfferedForm::clear_duration_template
        test_duration = Duration(hours=1)
        self.assertIsNone(self.form._my_map['${var_name_mixed}'])
        self.form.set_${var_name}(test_duration)
        self.assertEqual(self.form._my_map['${var_name_mixed}']['seconds'], 3600)
        self.assertEqual(self.form._my_map['${var_name_mixed}']['days'], 0)
        self.assertEqual(self.form._my_map['${var_name_mixed}']['microseconds'], 0)
        self.form.${method_name}()
        self.assertEqual(self.form._my_map['${var_name_mixed}'], self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0])"""


class AssessmentOfferedList:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentOfferedList tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedList tests'
        cls.assessment = cls.catalog.create_assessment(create_form)

        cls.form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident,
                                                                      [])

    def setUp(self):
        from dlkit.json_.assessment.objects import AssessmentOfferedList
        self.assessment_offered_list = list()
        self.assessment_offered_ids = list()
        for num in [0, 1]:
            form = self.catalog.get_assessment_offered_form_for_create(self.assessment.ident,
                                                                       [])
            form.display_name = 'Test AssessmentOffered ' + str(num)
            form.description = 'Test AssessmentOffered for AssessmentOfferedList tests'
            obj = self.catalog.create_assessment_offered(form)
            self.assessment_offered_list.append(obj)
            self.assessment_offered_ids.append(obj.ident)
        self.assessment_offered_list = AssessmentOfferedList(self.assessment_offered_list)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessments_offered():
            cls.catalog.delete_assessment_offered(obj.ident)
        for obj in cls.catalog.get_assessments():
            cls.catalog.delete_assessment(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

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

    match_start_time_template = """
        pass"""


class AssessmentQuery:
    match_item_id = """
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_item_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['itemIds'], {
            '$in': [str(test_id)]
        })"""

    clear_item_id_terms = """
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_item_id(test_id, match=True)
        self.assertIn('itemIds',
                      self.query._query_terms)
        self.query.clear_item_id_terms()
        self.assertNotIn('itemIds',
                         self.query._query_terms)"""


class AssessmentOfferedQuerySession:

    import_statements_pattern = [
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.assessment_offered_list = list()
        cls.assessment_offered_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentOfferedLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedLookupSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident, [])
            create_form.display_name = 'Test AssessmentOffered ' + color
            create_form.description = (
                'Test AssessmentOffered for AssessmentOfferedQuerySession tests, did I mention green')
            obj = cls.catalog.create_assessment_offered(create_form)
            cls.assessment_offered_list.append(obj)
            cls.assessment_offered_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_banks():
            for obj in catalog.get_assessments_offered():
                catalog.delete_assessment_offered(obj.ident)
            for obj in catalog.get_assessments():
                catalog.delete_assessment(obj.ident)
            cls.svc_mgr.delete_bank(catalog.ident)"""


class AssessmentTakenQuerySession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.assessment_taken_list = list()
        cls.assessment_taken_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentTakenLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedLookupSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        create_form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident, [])
        create_form.display_name = 'Test AssessmentOffered'
        create_form.description = 'Test AssessmentOffered for AssessmentOfferedLookupSession tests'
        cls.assessment_offered = cls.catalog.create_assessment_offered(create_form)
        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = cls.catalog.get_assessment_taken_form_for_create(cls.assessment_offered.ident, [])
            create_form.display_name = 'Test AssessmentTaken ' + color
            create_form.description = (
                'Test AssessmentTaken for AssessmentTakenQuerySession tests, did I mention green')
            obj = cls.catalog.create_assessment_taken(create_form)
            cls.assessment_taken_list.append(obj)
            cls.assessment_taken_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_banks():
            for obj in catalog.get_assessments_taken():
                catalog.delete_assessment_taken(obj.ident)
            for obj in catalog.get_assessments_offered():
                catalog.delete_assessment_offered(obj.ident)
            for obj in catalog.get_assessments():
                catalog.delete_assessment(obj.ident)
            cls.svc_mgr.delete_bank(catalog.ident)"""


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
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        form = cls.catalog.get_assessment_form_for_create([SEQUENCE_ASSESSMENT])
        form.display_name = 'Assessment'
        cls.assessment = cls.catalog.create_assessment(form)

        form = cls.catalog.get_item_form_for_create([])
        form.display_name = 'Test item'
        cls.item = cls.catalog.create_item(form)

        form = cls.catalog.get_question_form_for_create(cls.item.ident, [])
        cls.catalog.create_question(form)
        cls.item = cls.catalog.get_item(cls.item.ident)

        cls.catalog.add_item(cls.assessment.ident, cls.item.ident)
        cls.assessment = cls.catalog.get_assessment(cls.assessment.ident)

        form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident, [])
        form.display_name = 'Test assessment offered'
        cls.offered = cls.catalog.create_assessment_offered(form)

    def setUp(self):
        form = self.catalog.get_assessment_taken_form_for_create(self.offered.ident,
                                                                 [])
        self.object = self.catalog.create_assessment_taken(form)

    def tearDown(self):
        self.catalog.delete_assessment_taken(self.object.ident)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessments():
            for offered in cls.catalog.get_assessments_offered_for_assessment(obj.ident):
                for taken in cls.catalog.get_assessments_taken_for_assessment_offered(offered.ident):
                    cls.catalog.delete_assessment_taken(taken.ident)
                cls.catalog.delete_assessment_offered(offered.ident)
            cls.catalog.delete_assessment(obj.ident)
        for obj in cls.catalog.get_items():
            cls.catalog.delete_item(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    get_assessment_offered_id = """
        self.assertTrue(isinstance(self.object.get_assessment_offered_id(), Id))
        self.assertEqual(str(self.object.get_assessment_offered_id()),
                         str(self.offered.ident))"""

    get_assessment_offered = """
        self.assertTrue(isinstance(self.object.get_assessment_offered(), AssessmentOffered))
        self.assertEqual(str(self.object.get_assessment_offered().ident),
                         str(self.offered.ident))"""

    get_taker_id = """
        self.assertTrue(isinstance(self.object.get_taker_id(), Id))
        self.assertEqual(str(self.object.get_taker_id()),
                         str(self.catalog._proxy.get_effective_agent_id()))"""

    get_taker = """
        with self.assertRaises(errors.Unimplemented):
            self.object.get_taker()"""

    get_taking_agent_id = """
        self.assertTrue(isinstance(self.object.get_taking_agent_id(), Id))
        self.assertEqual(str(self.object.get_taking_agent_id()),
                         str(self.catalog._proxy.get_effective_agent_id()))"""

    get_taking_agent = """
        with self.assertRaises(errors.Unimplemented):
            self.object.get_taking_agent()"""

    has_started = """
        # tests if the assessment has begun
        self.assertTrue(self.object.has_started())"""

    get_actual_start_time = """
        # tests if the taker has started the assessment
        with self.assertRaises(errors.IllegalState):
            self.object.actual_start_time
        # Also test the other branches of this method
        form = self.catalog.get_assessment_taken_form_for_create(self.offered.ident,
                                                                 [])
        taken = self.catalog.create_assessment_taken(form)
        section = self.catalog.get_first_assessment_section(taken.ident)
        section.get_questions()
        taken = self.catalog.get_assessment_taken(taken.ident)
        self.assertTrue(isinstance(taken.actual_start_time, DateTime))
        self.catalog.delete_assessment_taken(taken.ident)"""

    has_ended = """
        # tests if the assessment is over
        self.assertFalse(self.object.has_ended())"""

    get_completion_time = """
        # tests if the taker has "finished" the assessment
        with self.assertRaises(errors.IllegalState):
            self.object.completion_time
        # Also test the other branches of this method
        form = self.catalog.get_assessment_taken_form_for_create(self.offered.ident,
                                                                 [])
        taken = self.catalog.create_assessment_taken(form)
        section = self.catalog.get_first_assessment_section(taken.ident)
        section.get_questions()

        self.catalog.finish_assessment(taken.ident)

        taken = self.catalog.get_assessment_taken(taken.ident)
        self.assertTrue(isinstance(taken.completion_time, DateTime))
        self.catalog.delete_assessment_taken(taken.ident)"""

    get_time_spent = """
        with self.assertRaises(errors.IllegalState):
            self.object.time_spent
        # Also test the other branches of this method
        form = self.catalog.get_assessment_taken_form_for_create(self.offered.ident,
                                                                 [])
        taken = self.catalog.create_assessment_taken(form)
        section = self.catalog.get_first_assessment_section(taken.ident)
        section.get_questions()

        self.catalog.finish_assessment(taken.ident)
        taken = self.catalog.get_assessment_taken(taken.ident)
        self.assertTrue(isinstance(taken.time_spent, datetime.timedelta))
        self.catalog.delete_assessment_taken(taken.ident)"""

    get_completion_template = """
        # From test_templates/assessment.py::AssessmentTaken::get_completion_template
        # Our implementation is probably wrong -- there is no "completion" setter
        # in the form / spec...so unclear how the value gets here.
        self.assertRaises(KeyError,
                          self.object.${method_name})"""

    get_score_template = """
        # From test_templates/assessment.py::AssessmentTaken::get_score_template
        self.assertTrue(isinstance(self.object.${method_name}(), Decimal))
        self.assertEqual(self.object.${method_name}(), Decimal(0.0))"""

    has_rubric = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set rubricId?
        self.assertRaises(KeyError,
                          self.object.has_rubric)"""

    get_rubric = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set rubricId?
        self.assertRaises(KeyError,
                          self.object.get_rubric)"""

    get_rubric_id = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set rubricId?
        self.assertRaises(KeyError,
                          self.object.get_rubric_id)"""

    is_graded = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set graded?
        self.assertRaises(KeyError,
                          self.object.is_graded)"""

    is_scored = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set scored?
        self.assertRaises(KeyError,
                          self.object.is_scored)"""

    get_score_system = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set scoreSystemId?
        self.assertRaises(KeyError,
                          self.object.get_score_system)"""

    get_score_system_id = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set scoreSystemId?
        self.assertRaises(KeyError,
                          self.object.get_score_system_id)"""

    get_feedback = """
        # This may be an error in the spec -- not in _my_map
        # since there are no form methods to set feedback?
        self.assertRaises(KeyError,
                          self.object.get_feedback)"""


class AssessmentTakenForm:

    import_statements = [
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentTakenLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedLookupSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        create_form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident, [])
        create_form.display_name = 'Test AssessmentOffered'
        create_form.description = 'Test AssessmentOffered for AssessmentOfferedLookupSession tests'
        cls.assessment_offered = cls.catalog.create_assessment_offered(create_form)

        cls.form = cls.catalog.get_assessment_taken_form_for_create(cls.assessment_offered.ident, [])

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessments_offered():
            cls.catalog.delete_assessment_offered(obj.ident)
        for obj in cls.catalog.get_assessments():
            cls.catalog.delete_assessment(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""


class AssessmentTakenList:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentTakenList tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentTakenList tests'
        cls.assessment = cls.catalog.create_assessment(create_form)

        form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident,
                                                                  [])
        cls.assessment_offered = cls.catalog.create_assessment_offered(form)

        cls.form = cls.catalog.get_assessment_taken_form_for_create(cls.assessment_offered.ident,
                                                                    [])

    def setUp(self):
        from dlkit.json_.assessment.objects import AssessmentTakenList
        self.assessment_taken_list = list()
        self.assessment_taken_ids = list()
        for num in [0, 1]:
            form = self.catalog.get_assessment_offered_form_for_create(self.assessment.ident,
                                                                       [])
            form.display_name = 'Test AssessmentOffered ' + str(num)
            form.description = 'Test AssessmentOffered for AssessmentTakenList tests'
            obj = self.catalog.create_assessment_offered(form)

            form = self.catalog.get_assessment_taken_form_for_create(obj.ident, [])
            obj = self.catalog.create_assessment_taken(form)
            self.assessment_taken_list.append(obj)
            self.assessment_taken_ids.append(obj.ident)
        self.assessment_taken_list = AssessmentTakenList(self.assessment_taken_list)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessments_taken():
            cls.catalog.delete_assessment_taken(obj.ident)
        for obj in cls.catalog.get_assessments_offered():
            cls.catalog.delete_assessment_offered(obj.ident)
        for obj in cls.catalog.get_assessments():
            cls.catalog.delete_assessment(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""


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
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        form = cls.catalog.get_assessment_form_for_create([SEQUENCE_ASSESSMENT])
        form.display_name = 'Assessment'
        cls.assessment = cls.catalog.create_assessment(form)

        form = cls.catalog.get_item_form_for_create([])
        form.display_name = 'Test item'
        cls.item = cls.catalog.create_item(form)

        form = cls.catalog.get_question_form_for_create(cls.item.ident, [])
        cls.catalog.create_question(form)
        cls.item = cls.catalog.get_item(cls.item.ident)

        cls.catalog.add_item(cls.assessment.ident, cls.item.ident)
        cls.assessment = cls.catalog.get_assessment(cls.assessment.ident)

        form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident, [])
        form.display_name = 'Test assessment offered'
        cls.offered = cls.catalog.create_assessment_offered(form)

    def setUp(self):
        form = self.catalog.get_assessment_taken_form_for_create(self.offered.ident,
                                                                 [])
        self.taken = self.catalog.create_assessment_taken(form)
        self.section = self.catalog.get_first_assessment_section(self.taken.ident)

    def tearDown(self):
        self.catalog.delete_assessment_taken(self.taken.ident)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessments():
            for offered in cls.catalog.get_assessments_offered_for_assessment(obj.ident):
                for taken in cls.catalog.get_assessments_taken_for_assessment_offered(offered.ident):
                    cls.catalog.delete_assessment_taken(taken.ident)
                cls.catalog.delete_assessment_offered(offered.ident)
            cls.catalog.delete_assessment(obj.ident)
        for obj in cls.catalog.get_items():
            cls.catalog.delete_item(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    get_assessment_taken_id = """
        self.assertTrue(isinstance(self.section.get_assessment_taken_id(), Id))
        self.assertEqual(str(self.section.get_assessment_taken_id()),
                         str(self.taken.ident))"""

    get_assessment_taken = """
        self.assertTrue(isinstance(self.section.get_assessment_taken(), AssessmentTaken))
        self.assertEqual(str(self.section.get_assessment_taken().ident),
                         str(self.taken.ident))"""

    has_allocated_time = """
        with self.assertRaises(errors.Unimplemented):
            self.section.has_allocated_time()"""

    get_allocated_time = """
        with self.assertRaises(errors.Unimplemented):
            self.section.get_allocated_time()"""

    are_items_sequential = """
        # This does not throw an exception because of the SIMPLE_SEQUENCE record
        self.assertFalse(self.section.are_items_sequential())"""

    are_items_shuffled = """
        # This does not throw an exception because of the SIMPLE_SEQUENCE record
        self.assertFalse(self.section.are_items_shuffled())"""


class AssessmentSectionList:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentSectionList tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentSectionList tests'
        cls.assessment = cls.catalog.create_assessment(create_form)

        cls.form = cls.catalog.get_assessment_part_form_for_create_for_assessment(cls.assessment.ident,
                                                                                  [])

    def setUp(self):
        from dlkit.json_.assessment.objects import AssessmentSectionList
        self.assessment_section_list = list()
        self.assessment_section_ids = list()

        for num in [0, 1]:
            form = self.catalog.get_assessment_part_form_for_create_for_assessment(self.assessment.ident, [])

            obj = self.catalog.create_assessment_part_for_assessment(form)

            self.assessment_section_list.append(obj)
            self.assessment_section_ids.append(obj.ident)
        self.assessment_section_list = AssessmentSectionList(self.assessment_section_list)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assessments():
            cls.catalog.delete_assessment(obj.ident)
        cls.svc_mgr.delete_bank(cls.catalog.ident)"""

    get_next_assessment_section = """
        from dlkit.abstract_osid.assessment_authoring.objects import AssessmentPart
        self.assertTrue(isinstance(self.assessment_section_list.get_next_assessment_section(), AssessmentPart))"""

    get_next_assessment_sections = """
        from dlkit.abstract_osid.assessment.objects import AssessmentSectionList
        from dlkit.abstract_osid.assessment_authoring.objects import AssessmentPart
        new_list = self.assessment_section_list.get_next_assessment_sections(2)
        self.assertTrue(isinstance(new_list, AssessmentSectionList))
        for item in new_list:
            self.assertTrue(isinstance(item, AssessmentPart))"""


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
"""

    get_next_response = """"""

    get_next_responses = """"""


class BankQuery:
    match_ancestor_bank_id = """
        self.assertNotIn('_id', self.query._query_terms)
        self.query.match_ancestor_bank_id(self.fake_id, True)
        self.assertEqual(self.query._query_terms['_id'], {
            '$in': []
        })"""
