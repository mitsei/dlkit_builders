
class AssessmentManager:

    get_assessment_taken_query_session_for_bank = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_catalog_template
        session = self._provider_manager.get_assessment_taken_query_session_for_bank(*args, **kwargs)
        return Bank(self._provider_manager, session.get_bank(), self._proxy, assessment_taken_query_session = session)

    def get_assessment_taken_admin_session(self, *args, **kwargs):
        session = self._provider_manager.get_assessment_taken_admin_session(*args, **kwargs)
        return Bank(self._provider_manager, session.get_bank(), self._proxy, assessment_taken_admin_session = session)

    assessment_taken_admin_session = property(fget=get_assessment_taken_admin_session)

    def get_assessment_taken_admin_session_for_bank(self, *args, **kwargs):
        session = self._provider_manager.get_assessment_taken_admin_session_for_bank(*args, **kwargs)
        return Bank(self._provider_manager, session.get_bank(), self._proxy, assessment_taken_admin_session = session)
    """

class AssessmentSession:

    can_take_assessments = """
        return self._get_provider_session('assessment_session').can_take_assessments(*args, **kwargs)"""

    has_assessment_begun = """
        return self._get_provider_session('assessment_session').has_assessment_begun(*args, **kwargs)"""

    is_assessment_over = """
        return self._get_provider_session('assessment_session').is_assessment_over(*args, **kwargs)"""

    finished_assessment = """
        self._get_provider_session('assessment_session').finished_assessment(*args, **kwargs)"""

    requires_synchronous_sections = """
        return self._get_provider_session('assessment_session').requires_synchronous_sections(*args, **kwargs)"""

    get_first_assessment_section = """
        return self._get_provider_session('assessment_session').get_first_assessment_section(*args, **kwargs)"""

    has_next_assessment_section = """
        return self._get_provider_session('assessment_session').has_next_assessment_section(*args, **kwargs)"""

    get_next_assessment_section = """
        return self._get_provider_session('assessment_session').get_next_assessment_section(*args, **kwargs)"""

    has_previous_assessment_section = """
        return self._get_provider_session('assessment_session').has_previous_assessment_section(*args, **kwargs)"""

    get_previous_assessment_section = """
        return self._get_provider_session('assessment_session').get_previous_assessment_section(*args, **kwargs)"""

    get_assessment_section = """
        return self._get_provider_session('assessment_session').get_assessment_section(*args, **kwargs)"""

    get_assessment_sections = """
        return self._get_provider_session('assessment_session').get_assessment_sections(*args, **kwargs)"""

    is_assessment_section_complete = """
        return self._get_provider_session('assessment_session').is_assessment_section_complete(*args, **kwargs)"""

    get_incomplete_assessment_sections = """
        return self._get_provider_session('assessment_session').get_incomplete_assessment_sections(*args, **kwargs)"""

    has_assessment_section_begun = """
        return self._get_provider_session('assessment_session').has_assessment_section_begun(*args, **kwargs)"""

    is_assessment_section_over = """
        return self._get_provider_session('assessment_session').is_assessment_section_over(*args, **kwargs)"""

    finished_assessment_section = """
        self._get_provider_session('assessment_session').finished_assessment_section(*args, **kwargs)"""

    requires_synchronous_responses = """
        return self._get_provider_session('assessment_session').requires_synchronous_responses(*args, **kwargs)"""

    get_first_question = """
        return self._get_provider_session('assessment_session').get_first_question(*args, **kwargs)"""

    has_next_question = """
        return self._get_provider_session('assessment_session').has_next_question(*args, **kwargs)"""

    get_next_question = """
        return self._get_provider_session('assessment_session').get_next_question(*args, **kwargs)"""

    has_previous_question = """
        return self._get_provider_session('assessment_session').has_previous_question(*args, **kwargs)"""

    get_previous_question = """
        return self._get_provider_session('assessment_session').get_previous_question(*args, **kwargs)"""

    get_question = """
        return self._get_provider_session('assessment_session').get_question(*args, **kwargs)"""

    get_questions = """
        return self._get_provider_session('assessment_session').get_questions(*args, **kwargs)"""

    get_response_form = """
        return self._get_provider_session('assessment_session').get_response_form(*args, **kwargs)"""

    submit_response = """
        self._get_provider_session('assessment_session').submit_response(*args, **kwargs)"""

    skip_item = """
        return self._get_provider_session('assessment_session').skip_item(*args, **kwargs)"""

    is_question_answered = """
        return self._get_provider_session('assessment_session').is_question_answered(*args, **kwargs)"""

    get_unanswered_questions = """
        return self._get_provider_session('assessment_session').get_unanswered_questions(*args, **kwargs)"""

    has_unanswered_questions = """
        return self._get_provider_session('assessment_session').has_unanswered_questions(*args, **kwargs)"""

    get_first_unanswered_question = """
        return self._get_provider_session('assessment_session').get_first_unanswered_question(*args, **kwargs)"""

    has_next_unanswered_question = """
        return self._get_provider_session('assessment_session').has_next_unanswered_question(*args, **kwargs)"""

    get_next_unanswered_question = """
        return self._get_provider_session('assessment_session').get_next_unanswered_question(*args, **kwargs)"""

    has_previous_unanswered_question = """
        return self._get_provider_session('assessment_session').has_previous_unanswered_question(*args, **kwargs)"""

    get_previous_unanswered_question = """
        return self._get_provider_session('assessment_session').get_previous_unanswered_question(*args, **kwargs)"""

    get_response = """
        return self._get_provider_session('assessment_session').get_response(*args, **kwargs)"""

    get_responses = """
        return self._get_provider_session('assessment_session').get_responses(*args, **kwargs)"""

    clear_response = """
        self._get_provider_session('assessment_session').clear_response(*args, **kwargs)"""

    finish = """
        self._get_provider_session('assessment_session').finish(*args, **kwargs)"""

    is_answer_available = """
        return self._get_provider_session('assessment_session').is_answer_available(*args, **kwargs)"""

    get_answers = """
        return self._get_provider_session('assessment_session').get_answers(*args, **kwargs)"""
    


class AssessmentBasicAuthoringSession:

    can_author_assessment = """
        return self._get_provider_session('assessment_basic_authoring_session').can_author_assessment(*args, **kwargs)"""

    get_assessment_items = """
        # Note: this method is differenct from the underlying signature
        return self._get_provider_session('assessment_basic_authoring_session').get_items(*args, **kwargs)"""

    add_item = """
        self._get_provider_session('assessment_basic_authoring_session').add_item(*args, **kwargs)"""

    remove_item = """
        self._get_provider_session('assessment_basic_authoring_session').remove_item(*args, **kwargs)"""

    move_item = """
        self._get_provider_session('assessment_basic_authoring_session').move_item(*args, **kwargs)"""

    order_items = """
        self._get_provider_session('assessment_basic_authoring_session').order_items(*args, **kwargs)"""

class AssessmentTakenLookupSession:

    get_assessments_taken_for_taker_and_assessment_offered = """
        return self._get_provider_session('assessment_taken_lookup_session').get_assessments_taken_for_taker_and_assessment_offered(*args, **kwargs)"""
