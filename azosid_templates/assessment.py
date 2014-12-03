# assessment templates for az_osid

class AssessmentManager:

    get_assessment_taken_query_session_for_bank = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_template
        from sessions import AssessmentTakenQuerySession
        return AssessmentTakenQuerySession(self._provider_manager.get_assessment_taken_query_session_for_bank(bank_id), self._authz_session)

    def get_assessment_taken_admin_session(self):
        from sessions import AssessmentTakenAdminSession
        return AssessmentTakenAdminSession(self._provider_manager.get_assessment_taken_admin_session(), self._authz_session)

    def get_assessment_taken_admin_session_for_bank(self, bank_id=None):
        from sessions import AssessmentTakenAdminSession
        return AssessmentTakenAdminSession(self._provider_manager.get_assessment_taken_admin_session_for_bank(bank_id), self._authz_session)
"""

class AssessmentProxyManager:

    get_assessment_taken_query_session_for_bank = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_template
        from sessions import AssessmentTakenQuerySession
        return AssessmentTakenQuerySession(self._provider_manager.get_assessment_taken_query_session_for_bank(bank_id, proxy), self._authz_session, proxy)

    def get_assessment_taken_admin_session(self, proxy=None):
        from sessions import AssessmentTakenAdminSession
        return AssessmentTakenAdminSession(self._provider_manager.get_assessment_taken_admin_session(proxy), self._authz_session, proxy)

    def get_assessment_taken_admin_session_for_bank(self, bank_id=None, proxy=None):
        from sessions import AssessmentTakenAdminSession
        return AssessmentTakenAdminSession(self._provider_manager.get_assessment_taken_admin_session_for_bank(bank_id, proxy), self._authz_session, proxy)
"""


class AssessmentSession:

    import_statements = [
        'from ..osid.osid_errors import PermissionDenied'
        ]

    init = """
    def __init__(self, provider_session, authz_session, proxy = None):
        from ..osid import sessions as osid_sessions
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_bank_id()
        self._id_namespace = 'assessment.Assessment'
"""

    can_take_assessments = """
        return self._can('take')"""

    has_assessment_begun = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.has_assessment_begun(assessment_taken_id)"""

    is_assessment_over = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.is_assessment_over(assessment_taken_id)"""

    finished_assessment = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            self._provider_session.finished_assessment(assessment_taken_id)"""

    requires_synchronous_sections = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.requires_synchronous_sections(assessment_taken_id)"""

    get_first_assessment_section = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_first_assessment_section(assessment_taken_id)"""

    has_next_assessment_section = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.has_next_assessment_section(assessment_section_id)"""

    get_next_assessment_section = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_next_assessment_section(assessment_section_id)"""

    has_previous_assessment_section = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.has_previous_assessment_section(assessment_section_id)"""

    get_previous_assessment_section = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_previous_assessment_section(assessment_section_id)"""

    get_assessment_section = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_assessment_section(assessment_section_id)"""

    get_assessment_sections = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_assessment_sections(assessment_taken_id)"""

    is_assessment_section_complete = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.is_assessment_section_complete(assessment_section_id)"""

    get_incomplete_assessment_sections = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.is_assessment_section_complete(assessment_taken_id)"""

    has_assessment_section_begun = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.has_assessment_section_begun(assessment_section_id)"""

    is_assessment_section_over = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.is_assessment_section_over(assessment_section_id)"""

    finished_assessment_section = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            self._provider_session.finished_assessment_section(assessment_section_id)"""

    requires_synchronous_responses = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.requires_synchronous_responses(assessment_section_id)"""

    get_first_question = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_first_question(assessment_section_id)"""

    has_next_question = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.has_next_question(assessment_section_id, item_id)"""

    get_next_question = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_next_question(assessment_section_id, item_id)"""

    has_previous_question = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.has_previous_question(assessment_section_id, item_id)"""

    get_previous_question = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_previous_question(assessment_section_id, item_id)"""

    get_question = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_question(assessment_section_id, item_id)"""

    get_questions = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_questions(assessment_section_id)"""

    get_response_form = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_response_form(assessment_section_id, item_id)"""

    submit_response = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.submit_response(assessment_section_id, item_id, answer)"""

    skip_item = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.skip_item(assessment_section_id, item_id)"""

    is_question_answered = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.is_question_answered(assessment_section_id, item_id)"""

    get_unanswered_questions = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_unanswered_questions(assessment_section_id)"""

    has_unanswered_questions = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.has_unanswered_questions(assessment_section_id)"""

    get_first_unanswered_question = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_first_unanswered_question(assessment_section_id)"""

    has_next_unanswered_question = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.has_next_unanswered_question(assessment_section_id, item_id)"""

    get_next_unanswered_question = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_next_unanswered_question(assessment_section_id, item_id)"""

    has_previous_unanswered_question = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.has_previous_unanswered_question(assessment_section_id, item_id)"""

    get_previous_unanswered_question = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_previous_unanswered_question(assessment_section_id, item_id)"""

    get_response = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_response(assessment_section_id, item_id)"""

    get_responses = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_responses(assessment_section_id)"""

    clear_response = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.clear_response(assessment_section_id, item_id)"""

    finish = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.finish(assessment_section_id)"""

    is_answer_available = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.is_answer_available(assessment_section_id, item_id)"""

    get_answers = """
        if not self._can('take'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_answers(assessment_section_id, item_id)"""
    


class AssessmentBasicAuthoringSession:

    init = """
    def __init__(self, provider_session, authz_session, proxy = None):
        from ..osid import sessions as osid_sessions
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_bank_id()
        self._id_namespace = 'assessment.Assessment'
"""

    can_author_assessment = """
        return self._can('author')"""

    get_items = """
        # Implemented from azosid template for -
        # osid.assessment.AssessmentBasicAuthoringSession.get_items
        if not self._can('author'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_items(assessment_id)"""

    add_item = """
        # Implemented from azosid template for -
        # osid.assessment.AssessmentBasicAuthoringSession.add_item
        if not self._can('author'):
            raise PermissionDenied()
        else:
            self._provider_session.add_item(assessment_id, item_id)"""

    remove_item = """
        # Implemented from azosid template for -
        # osid.assessment.AssessmentBasicAuthoringSession.remove_item
        if not self._can('author'):
            raise PermissionDenied()
        else:
            self._provider_session.remove_item(assessment_id, item_id)"""

    move_item = """
        # Implemented from azosid template for -
        # osid.assessment.AssessmentBasicAuthoringSession.move_item
        if not self._can('author'):
            raise PermissionDenied()
        else:
            self._provider_session.move_item(assessment_id, item_id, preceeding_item_id)"""

    order_items = """
        # Implemented from azosid template for -
        # osid.assessment.AssessmentBasicAuthoringSession.order_items
        if not self._can('author'):
            raise PermissionDenied()
        else:
            self._provider_session.order_items(item_ids, assessment_id)"""

class AssessmentTakenLookupSession:

    get_assessments_taken_for_taker_and_assessment_offered = """
        # Implemented from azosid template for -
        # osid.assessment.AssessmentTakenLookupSession.get_assessments_taken_for_taker_and_assessment_offered
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_assessments_taken_for_taker_and_assessment_offered(resource_id, assessment_offered_id)"""
