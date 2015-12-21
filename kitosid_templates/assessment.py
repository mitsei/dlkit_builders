
class AssessmentManager:

    old_get_assessment_taken_query_session_for_bank_for_deletion = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_catalog_template
        session = self._provider_manager.get_assessment_taken_query_session_for_bank(*args, **kwargs)
        return Bank(self._provider_manager, session.get_bank(), self._proxy, assessment_taken_query_session = session)

    def get_assessment_taken_admin_session(self, *args, **kwargs):
        \"\"\"Pass through to provider method\"\"\"
        session = self._provider_manager.get_assessment_taken_admin_session(*args, **kwargs)
        return Bank(self._provider_manager, session.get_bank(), self._proxy, assessment_taken_admin_session = session)

    assessment_taken_admin_session = property(fget=get_assessment_taken_admin_session)

    def get_assessment_taken_admin_session_for_bank(self, *args, **kwargs):
        \"\"\"Pass through to provider method\"\"\"
        session = self._provider_manager.get_assessment_taken_admin_session_for_bank(*args, **kwargs)
        return Bank(self._provider_manager, session.get_bank(), self._proxy, assessment_taken_admin_session = session)"""

class AssessmentSession:

    can_take_assessments = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').can_take_assessments()"""

    has_assessment_begun = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').has_assessment_begun(*args, **kwargs)"""

    is_assessment_over = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').is_assessment_over(*args, **kwargs)"""

    finished_assessment = """
        \"\"\"Pass through to provider method\"\"\"
        self._get_provider_session('assessment_session').finished_assessment(*args, **kwargs)"""

    requires_synchronous_sections = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').requires_synchronous_sections(*args, **kwargs)"""

    get_first_assessment_section = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_first_assessment_section(*args, **kwargs)"""

    has_next_assessment_section = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').has_next_assessment_section(*args, **kwargs)"""

    get_next_assessment_section = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_next_assessment_section(*args, **kwargs)"""

    has_previous_assessment_section = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').has_previous_assessment_section(*args, **kwargs)"""

    get_previous_assessment_section = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_previous_assessment_section(*args, **kwargs)"""

    get_assessment_section = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_assessment_section(*args, **kwargs)"""

    get_assessment_sections = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_assessment_sections(*args, **kwargs)"""

    is_assessment_section_complete = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').is_assessment_section_complete(*args, **kwargs)"""

    get_incomplete_assessment_sections = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_incomplete_assessment_sections(*args, **kwargs)"""

    has_assessment_section_begun = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').has_assessment_section_begun(*args, **kwargs)"""

    is_assessment_section_over = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').is_assessment_section_over(*args, **kwargs)"""

    requires_synchronous_responses = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').requires_synchronous_responses(*args, **kwargs)"""

    get_first_question = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_first_question(*args, **kwargs)"""

    has_next_question = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').has_next_question(*args, **kwargs)"""

    get_next_question = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_next_question(*args, **kwargs)"""

    has_previous_question = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').has_previous_question(*args, **kwargs)"""

    get_previous_question = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_previous_question(*args, **kwargs)"""

    get_question = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_question(*args, **kwargs)"""

    get_questions = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_questions(*args, **kwargs)"""

    get_response_form = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_response_form(*args, **kwargs)"""

    submit_response = """
        \"\"\"Pass through to provider method\"\"\"
        self._get_provider_session('assessment_session').submit_response(*args, **kwargs)"""

    skip_item = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').skip_item(*args, **kwargs)"""

    is_question_answered = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').is_question_answered(*args, **kwargs)"""

    get_unanswered_questions = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_unanswered_questions(*args, **kwargs)"""

    has_unanswered_questions = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').has_unanswered_questions(*args, **kwargs)"""

    get_first_unanswered_question = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_first_unanswered_question(*args, **kwargs)"""

    has_next_unanswered_question = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').has_next_unanswered_question(*args, **kwargs)"""

    get_next_unanswered_question = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_next_unanswered_question(*args, **kwargs)"""

    has_previous_unanswered_question = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').has_previous_unanswered_question(*args, **kwargs)"""

    get_previous_unanswered_question = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_previous_unanswered_question(*args, **kwargs)"""

    get_response = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_response(*args, **kwargs)"""

    get_responses = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_responses(*args, **kwargs)"""

    clear_response = """
        \"\"\"Pass through to provider method\"\"\"
        self._get_provider_session('assessment_session').clear_response(*args, **kwargs)"""

    finish_assessment_section = """
        \"\"\"Pass through to provider method\"\"\"
        self._get_provider_session('assessment_session').finish_assessment_section(*args, **kwargs)"""

    is_answer_available = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').is_answer_available(*args, **kwargs)"""

    get_answers = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_session').get_answers(*args, **kwargs)"""
 
    finish_assessment = """
        \"\"\"Pass through to provider method\"\"\"
        self._get_provider_session('assessment_session').finish_assessment(*args, **kwargs)"""
 


class AssessmentBasicAuthoringSession:

    can_author_assessments = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_basic_authoring_session').can_author_assessments()"""

    get_assessment_items = """
        \"\"\"Pass through to provider method\"\"\"
        # Note: this method is differenct from the underlying signature
        return self._get_provider_session('assessment_basic_authoring_session').get_items(*args, **kwargs)"""

    add_item = """
        \"\"\"Pass through to provider method\"\"\"
        self._get_provider_session('assessment_basic_authoring_session').add_item(*args, **kwargs)"""

    remove_item = """
        \"\"\"Pass through to provider method\"\"\"
        self._get_provider_session('assessment_basic_authoring_session').remove_item(*args, **kwargs)"""

    move_item = """
        \"\"\"Pass through to provider method\"\"\"
        self._get_provider_session('assessment_basic_authoring_session').move_item(*args, **kwargs)"""

    order_items = """
        \"\"\"Pass through to provider method\"\"\"
        self._get_provider_session('assessment_basic_authoring_session').order_items(*args, **kwargs)"""

class AssessmentTakenLookupSession:

    get_assessments_taken_for_taker_and_assessment_offered = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_taken_lookup_session').get_assessments_taken_for_taker_and_assessment_offered(*args, **kwargs)"""
