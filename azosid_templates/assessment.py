# assessment templates for az_osid


class AssessmentManager:

    old_get_assessment_taken_query_session_for_bank_to_delete = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_template
        return sessions.AssessmentTakenQuerySession(
            provider_session=self._provider_manager.get_assessment_taken_query_session_for_bank(bank_id),
            authz_session=sself._authz_session)

    def get_assessment_taken_admin_session(self):
        return sessions.AssessmentTakenAdminSession(
            provider_session=self._provider_manager.get_assessment_taken_admin_session(),
            authz_session=self._authz_session)

    def get_assessment_taken_admin_session_for_bank(self, bank_id=None):
        return sessions.AssessmentTakenAdminSession(
            provider_session=self._provider_manager.get_assessment_taken_admin_session_for_bank(bank_id),
            authz_session=sself._authz_session)
"""


class AssessmentProxyManager:

    old_get_assessment_taken_query_session_for_bank_to_delete = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_template
        return sessions.AssessmentTakenQuerySession(
            provider_session=self._provider_manager.get_assessment_taken_query_session_for_bank(bank_id, proxy),
            authz_session=sself._authz_session,
            proxy=proxy)

    def get_assessment_taken_admin_session(self, proxy=None):
        return sessions.AssessmentTakenAdminSession(
            provider_session=self._provider_manager.get_assessment_taken_admin_session(proxy),
            authz_session=sself._authz_session,
            proxy=proxy)

    def get_assessment_taken_admin_session_for_bank(self, bank_id=None, proxy=None):
        return sessions.AssessmentTakenAdminSession(
            provider_session=self._provider_manager.get_assessment_taken_admin_session_for_bank(bank_id, proxy),
            authz_session=sself._authz_session,
            proxy=proxy)
"""


class MyAssessmentTakenSession:

    import_statements = [
        'from ..osid.osid_errors import PermissionDenied'
    ]

    init = """
    def __init__(self, **kwargs):
        osid_sessions.OsidSession.__init__(self, **kwargs)
        self._qualifier_id = self._provider_session.get_bank_id()
        self._id_namespace = 'assessment.AssessmentTaken'
"""

    can_get_my_taken_assessments = """
        return self._can('get_my')"""

    get_assessments_started_during = """
        if not self._can('get_my'):
            raise PermissionDenied()
        return self._provider_session.get_assessments_started_during(start, end)"""

    get_assessments_started = """
        if not self._can('get_my'):
            raise PermissionDenied()
        return self._provider_session.get_assessments_started_during()"""

    get_assessments_in_progress_during = """
        if not self._can('get_my'):
            raise PermissionDenied()
        return self._provider_session.get_assessments_in_progress_during(start, end)"""

    get_assessments_in_progress = """
        if not self._can('get_my'):
            raise PermissionDenied()
        return self._provider_session.get_assessments_in_progress()"""

    get_assessments_completed = """
        if not self._can('get_my'):
            raise PermissionDenied()
        return self._provider_session.get_assessments_completed()"""


class AssessmentSession:

    import_statements = [
        'from ..osid.osid_errors import PermissionDenied'
    ]

    init = """
    def __init__(self, **kwargs):
        osid_sessions.OsidSession.__init__(self, **kwargs)
        self._qualifier_id = self._provider_session.get_bank_id()
        self._id_namespace = 'assessment.Assessment'
"""

    can_take_assessments = """
        return self._can('take')"""

    has_assessment_begun = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.has_assessment_begun(assessment_taken_id)"""

    is_assessment_over = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.is_assessment_over(assessment_taken_id)"""

    finished_assessment = """
        if not self._can('take'):
            raise PermissionDenied()
        self._provider_session.finished_assessment(assessment_taken_id)"""

    requires_synchronous_sections = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.requires_synchronous_sections(assessment_taken_id)"""

    get_first_assessment_section = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_first_assessment_section(assessment_taken_id)"""

    has_next_assessment_section = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.has_next_assessment_section(assessment_section_id)"""

    get_next_assessment_section = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_next_assessment_section(assessment_section_id)"""

    has_previous_assessment_section = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.has_previous_assessment_section(assessment_section_id)"""

    get_previous_assessment_section = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_previous_assessment_section(assessment_section_id)"""

    get_assessment_section = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_assessment_section(assessment_section_id)"""

    get_assessment_sections = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_assessment_sections(assessment_taken_id)"""

    is_assessment_section_complete = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.is_assessment_section_complete(assessment_section_id)"""

    get_incomplete_assessment_sections = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.is_assessment_section_complete(assessment_taken_id)"""

    has_assessment_section_begun = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.has_assessment_section_begun(assessment_section_id)"""

    is_assessment_section_over = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.is_assessment_section_over(assessment_section_id)"""

    requires_synchronous_responses = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.requires_synchronous_responses(assessment_section_id)"""

    get_first_question = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_first_question(assessment_section_id)"""

    has_next_question = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.has_next_question(assessment_section_id, item_id)"""

    get_next_question = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_next_question(assessment_section_id, item_id)"""

    has_previous_question = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.has_previous_question(assessment_section_id, item_id)"""

    get_previous_question = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_previous_question(assessment_section_id, item_id)"""

    get_question = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_question(assessment_section_id, item_id)"""

    get_questions = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_questions(assessment_section_id)"""

    get_response_form = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_response_form(assessment_section_id, item_id)"""

    submit_response = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.submit_response(assessment_section_id, item_id, answer_form)"""

    skip_item = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.skip_item(assessment_section_id, item_id)"""

    is_question_answered = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.is_question_answered(assessment_section_id, item_id)"""

    get_unanswered_questions = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_unanswered_questions(assessment_section_id)"""

    has_unanswered_questions = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.has_unanswered_questions(assessment_section_id)"""

    get_first_unanswered_question = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_first_unanswered_question(assessment_section_id)"""

    has_next_unanswered_question = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.has_next_unanswered_question(assessment_section_id, item_id)"""

    get_next_unanswered_question = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_next_unanswered_question(assessment_section_id, item_id)"""

    has_previous_unanswered_question = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.has_previous_unanswered_question(assessment_section_id, item_id)"""

    get_previous_unanswered_question = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_previous_unanswered_question(assessment_section_id, item_id)"""

    get_response = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_response(assessment_section_id, item_id)"""

    get_responses = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_responses(assessment_section_id)"""

    clear_response = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.clear_response(assessment_section_id, item_id)"""

    finish_assessment_section = """
        if not self._can('take'):
            raise PermissionDenied()
        self._provider_session.finish_assessment_section(assessment_section_id)"""

    is_answer_available = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.is_answer_available(assessment_section_id, item_id)"""

    get_answers = """
        if not self._can('take'):
            raise PermissionDenied()
        return self._provider_session.get_answers(assessment_section_id, item_id)"""

    finish_assessment = """
        if not self._can('take'):
            raise PermissionDenied()
        self._provider_session.finish_assessment(assessment_taken_id)"""


class AssessmentResultsSession:

    import_statements = [
        'from ..osid.osid_errors import PermissionDenied'
    ]

    init = """
    def __init__(self, **kwargs):
        osid_sessions.OsidSession.__init__(self, **kwargs)
        self._qualifier_id = self._provider_session.get_bank_id()
        self._id_namespace = 'assessment.AssessmentResults'
"""

    can_access_assessment_results = """
        return self._can('access')"""

    get_items = """
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.get_items(assessment_taken_id)"""

    get_responses = """
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.get_responses(assessment_taken_id)"""

    are_results_available = """
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.are_results_available(assessment_taken_id)"""

    get_grade_entries = """
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.get_grade_entries(assessment_taken_id)"""


class AssessmentBasicAuthoringSession:

    init = """
    def __init__(self, **kwargs):
        osid_sessions.OsidSession.__init__(self, **kwargs)
        self._qualifier_id = self._provider_session.get_bank_id()
        self._id_namespace = 'assessment.Assessment'
"""

    can_author_assessments = """
        return self._can('author')"""

    get_items = """
        # Implemented from azosid template for -
        # osid.assessment.AssessmentBasicAuthoringSession.get_items
        if not self._can('author'):
            raise PermissionDenied()
        return self._provider_session.get_items(assessment_id)"""

    add_item = """
        # Implemented from azosid template for -
        # osid.assessment.AssessmentBasicAuthoringSession.add_item
        if not self._can('author'):
            raise PermissionDenied()
        self._provider_session.add_item(assessment_id, item_id)"""

    remove_item = """
        # Implemented from azosid template for -
        # osid.assessment.AssessmentBasicAuthoringSession.remove_item
        if not self._can('author'):
            raise PermissionDenied()
        self._provider_session.remove_item(assessment_id, item_id)"""

    move_item = """
        # Implemented from azosid template for -
        # osid.assessment.AssessmentBasicAuthoringSession.move_item
        if not self._can('author'):
            raise PermissionDenied()
        self._provider_session.move_item(assessment_id, item_id, preceeding_item_id)"""

    order_items = """
        # Implemented from azosid template for -
        # osid.assessment.AssessmentBasicAuthoringSession.order_items
        if not self._can('author'):
            raise PermissionDenied()
        self._provider_session.order_items(item_ids, assessment_id)"""


class AssessmentTakenLookupSession:

    old_get_assessments_taken_for_taker_and_assessment_offered = """
        if not self._can('lookup'):
            raise PermissionDenied()
        return self._provider_session.get_assessments_taken_for_taker_and_assessment_offered(resource_id, assessment_offered_id)"""

    get_assessments_taken_for_taker_and_assessment_offered = """
        if self._can('lookup'):
            return self._provider_session.get_assessments_taken_for_taker_and_assessment_offered(resource_id, assessment_offered_id)
        self._check_lookup_conditions()  # raises PermissionDenied
        query = self._query_session.get_assessment_taken_query()
        query.match_taking_agent_id(resource_id, match=True)
        query.match_assessment_offered_id(assessment_offered_id, match=True)
        return self._try_harder(query)"""
