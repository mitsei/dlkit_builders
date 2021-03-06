
class AssessmentManager:

    old_get_assessment_taken_query_session_for_bank_for_deletion = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_catalog_template
        session = self._provider_manager.get_assessment_taken_query_session_for_bank(*args, **kwargs)
        return Bank(self._provider_manager, session.get_bank(), self._runtime, self._proxy, assessment_taken_query_session = session)

    def get_assessment_taken_admin_session(self, *args, **kwargs):
        \"\"\"Pass through to provider method\"\"\"
        session = self._provider_manager.get_assessment_taken_admin_session(*args, **kwargs)
        return Bank(self._provider_manager, session.get_bank(), self._runtime, self._proxy, assessment_taken_admin_session = session)

    assessment_taken_admin_session = property(fget=get_assessment_taken_admin_session)

    def get_assessment_taken_admin_session_for_bank(self, *args, **kwargs):
        \"\"\"Pass through to provider method\"\"\"
        session = self._provider_manager.get_assessment_taken_admin_session_for_bank(*args, **kwargs)
        return Bank(self._provider_manager, session.get_bank(), self._runtime, self._proxy, assessment_taken_admin_session = session)"""


# Ideally we would figure out a way to do this in the builder, for all subpackages...
class AssessmentProfile:
    import_statements = [
        'from dlkit.manager_impls.assessment_authoring import managers as assessment_authoring_managers'
    ]

    inheritance = ['assessment_authoring_managers.AssessmentAuthoringProfile']


class AssessmentAuthoringManager:
    get_sequence_rule_lookup_session = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_sequence_rule_lookup_session(*args, **kwargs)"""

    get_sequence_rule_lookup_session_for_bank = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_sequence_rule_lookup_session_for_bank(*args, **kwargs)"""

    get_assessment_part_lookup_session = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_assessment_part_lookup_session(*args, **kwargs)"""

    get_assessment_part_lookup_session_for_bank = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_assessment_part_lookup_session_for_bank(*args, **kwargs)"""

    get_assessment_part_query_session = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_assessment_part_query_session(*args, **kwargs)"""

    get_assessment_part_query_session_for_bank = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_assessment_part_query_session_for_bank(*args, **kwargs)"""

    get_assessment_part_admin_session = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_assessment_part_admin_session(*args, **kwargs)"""

    get_assessment_part_admin_session_for_bank = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_assessment_part_admin_session_for_bank(*args, **kwargs)"""

    get_assessment_part_bank_session = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_assessment_part_bank_session(*args, **kwargs)"""

    get_assessment_part_bank_assignment_session = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_assessment_part_bank_assignment_session(*args, **kwargs)"""

    get_sequence_rule_admin_session = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_sequence_rule_admin_session(*args, **kwargs)"""

    get_sequence_rule_admin_session_for_bank = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_sequence_rule_admin_session_for_bank(*args, **kwargs)

    def get_assessment_part_item_session(self, *args, **kwargs):
        \"\"\"Pass through to provider method\"\"\"
        # Missing in the spec
        return self._get_sub_package_provider_manager('assessment_authoring').get_assessment_part_item_session(*args, **kwargs)

    def get_assessment_part_item_session_for_bank(self, *args, **kwargs):
        \"\"\"Pass through to provider method\"\"\"
        # Missing in the spec
        return self._get_sub_package_provider_manager('assessment_authoring').get_assessment_part_item_session_for_bank(*args, **kwargs)

    def get_assessment_part_item_design_session(self, *args, **kwargs):
        \"\"\"Pass through to provider method\"\"\"
        # Missing in the spec
        return self._get_sub_package_provider_manager('assessment_authoring').get_assessment_part_item_design_session(*args, **kwargs)

    def get_assessment_part_item_design_session_for_bank(self, *args, **kwargs):
        \"\"\"Pass through to provider method\"\"\"
        # Missing in the spec
        return self._get_sub_package_provider_manager('assessment_authoring').get_assessment_part_item_design_session_for_bank(*args, **kwargs)"""


class AssessmentAuthoringProxyManager:
    get_sequence_rule_lookup_session = """
        \"\"\"Pass through to provider method\"\"\"
        return AssessmentManager.get_sequence_rule_lookup_session(*args, **kwargs)"""

    get_sequence_rule_lookup_session_for_bank = """
        \"\"\"Pass through to provider method\"\"\"
        return AssessmentManager.get_sequence_rule_lookup_session_for_bank(*args, **kwargs)"""

    get_assessment_part_lookup_session = """
        \"\"\"Pass through to provider method\"\"\"
        return AssessmentManager.get_assessment_part_lookup_session(*args, **kwargs)"""

    get_assessment_part_lookup_session_for_bank = """
        \"\"\"Pass through to provider method\"\"\"
        return AssessmentManager.get_assessment_part_lookup_session_for_bank(*args, **kwargs)"""

    get_assessment_part_query_session = """
        \"\"\"Pass through to provider method\"\"\"
        return AssessmentManager.get_assessment_part_query_session(*args, **kwargs)"""

    get_assessment_part_query_session_for_bank = """
        \"\"\"Pass through to provider method\"\"\"
        return AssessmentManager.get_assessment_part_query_session_for_bank(*args, **kwargs)"""

    get_assessment_part_admin_session = """
        \"\"\"Pass through to provider method\"\"\"
        return AssessmentManager.get_assessment_part_admin_session(*args, **kwargs)"""

    get_assessment_part_admin_session_for_bank = """
        \"\"\"Pass through to provider method\"\"\"
        return AssessmentManager.get_assessment_part_admin_session_for_bank(*args, **kwargs)"""

    get_assessment_part_bank_session = """
        \"\"\"Pass through to provider method\"\"\"
        return AssessmentManager.get_assessment_part_bank_session(*args, **kwargs)"""

    get_assessment_part_bank_assignment_session = """
        \"\"\"Pass through to provider method\"\"\"
        return AssessmentManager.get_assessment_part_bank_assignment_session(*args, **kwargs)"""

    get_sequence_rule_admin_session = """
        \"\"\"Pass through to provider method\"\"\"
        return AssessmentManager.get_sequence_rule_admin_session(*args, **kwargs)"""

    get_sequence_rule_admin_session_for_bank = """
        \"\"\"Pass through to provider method\"\"\"
        return AssessmentManager.get_sequence_rule_admin_session_for_bank(*args, **kwargs)

    def get_assessment_part_item_session(self, *args, **kwargs):
        \"\"\"Pass through to provider method\"\"\"
        return AssessmentManager.get_assessment_part_item_session(*args, **kwargs)

    def get_assessment_part_item_session_for_bank(self, *args, **kwargs):
        \"\"\"Pass through to provider method\"\"\"
        return AssessmentManager.get_assessment_part_item_session_for_bank(*args, **kwargs)

    def get_assessment_part_item_design_session(self, *args, **kwargs):
        \"\"\"Pass through to provider method\"\"\"
        return AssessmentManager.get_assessment_part_item_design_session(*args, **kwargs)

    def get_assessment_part_item_design_session_for_bank(self, *args, **kwargs):
        \"\"\"Pass through to provider method\"\"\"
        return AssessmentManager.get_assessment_part_item_design_session_for_bank(*args, **kwargs)"""


class AssessmentAuthoringProfile:
    get_assessment_part_record_types = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_assessment_part_record_types()"""

    get_assessment_part_search_record_types = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_assessment_part_search_record_types()"""

    get_sequence_rule_enabler_record_types = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_sequence_rule_enabler_record_types()"""

    get_sequence_rule_enabler_search_record_types = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_sequence_rule_enabler_search_record_types()"""

    get_sequence_rule_record_types = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_sequence_rule_record_types()"""

    get_sequence_rule_search_record_types = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').get_sequence_rule_search_record_types()"""

    supports_assessment_part_admin = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').supports_assessment_part_admin()"""

    supports_assessment_part_lookup = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').supports_assessment_part_lookup()"""

    supports_assessment_part_item = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').supports_assessment_part_item()"""

    supports_assessment_part_item_design = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').supports_assessment_part_item_design()"""

    supports_sequence_rule_admin = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').supports_sequence_rule_admin()"""

    supports_sequence_rule_lookup = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').supports_sequence_rule_lookup()"""

    supports_assessment_part_query = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_manager('assessment_authoring').supports_assessment_part_query()"""

    supports_assessment_part_bank = """
        return self._get_sub_package_provider_manager('assessment_authoring').supports_assessment_part_bank()"""

    supports_assessment_part_bank_assignment = """
        return self._get_sub_package_provider_manager('assessment_authoring').supports_assessment_part_bank_assignment()"""


class MyAssessmentTakenSession:

    can_get_my_taken_assessments = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('my_assessment_taken_session').can_get_my_taken_assessments()"""

    get_assessments_started_during = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('my_assessment_taken_session').get_assessments_started_during(*args, **kwargs)"""

    get_assessments_started = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('my_assessment_taken_session').get_assessments_started()"""

    get_assessments_in_progress_during = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('my_assessment_taken_session').get_assessments_in_progress_during(*args, **kwargs)"""

    get_assessments_in_progress = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('my_assessment_taken_session').get_assessments_in_progress()"""

    get_assessments_completed = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('my_assessment_taken_session').get_assessments_completed()"""


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


class AssessmentResultsSession:

    can_access_assessment_results = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_results_session').can_access_assessment_results()"""

    get_assessment_taken_items = """
        \"\"\"Pass through to provider method\"\"\"
        # Note: this method is differenct from the underlying signature
        return self._get_provider_session('assessment_results_session').get_items(*args, **kwargs)"""

    get_assessment_taken_responses = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_results_session').get_responses(*args, **kwargs)"""

    are_results_available = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_results_session').are_results_available(*args, **kwargs)"""

    get_grade_entries = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_results_session').get_grade_entries(*args, **kwargs)"""


class AssessmentBasicAuthoringSession:
    import_statements = [
        'from .osid_errors import InvalidArgument'
    ]

    can_author_assessments = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_basic_authoring_session').can_author_assessments()"""

    get_assessment_items = """
        \"\"\"Pass through to provider method\"\"\"
        # Note: this method is differenct from the underlying signature
        return self._get_provider_session('assessment_basic_authoring_session').get_items(*args, **kwargs)"""

    add_item = """
        \"\"\"Pass through to provider methods.\"\"\"
        try:
            self._get_provider_session('assessment_basic_authoring_session').add_item(*args, **kwargs)
        except InvalidArgument:
            self._get_sub_package_provider_session(
                'assessment_authoring', 'assessment_part_item_design_session').add_item(*args, **kwargs)"""

    remove_item = """
        \"\"\"Pass through to provider methods.\"\"\"
        try:
            self._get_provider_session('assessment_basic_authoring_session').remove_item(*args, **kwargs)
        except InvalidArgument:
            self._get_sub_package_provider_session(
                'assessment_authoring', 'assessment_part_item_design_session').remove_item(*args, **kwargs)"""

    move_item = """
        \"\"\"Pass through to provider method\"\"\"
        self._get_provider_session('assessment_basic_authoring_session').move_item(*args, **kwargs)"""

    order_items = """
        \"\"\"Pass through to provider methods.\"\"\"
        try:
            self._get_provider_session('assessment_basic_authoring_session').order_items(*args, **kwargs)
        except InvalidArgument:
            self._get_sub_package_provider_session(
                'assessment_authoring', 'assessment_part_item_design_session').order_items(*args, **kwargs)"""


class AssessmentTakenLookupSession:

    get_assessments_taken_for_taker_and_assessment_offered = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_provider_session('assessment_taken_lookup_session').get_assessments_taken_for_taker_and_assessment_offered(*args, **kwargs)"""


class AssessmentPartAdminSession:
    get_assessment_part_form_for_create_for_assessment = """
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_admin_session').get_assessment_part_form_for_create_for_assessment(*args, **kwargs)"""

    get_assessment_part_form_for_update = """
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_admin_session').get_assessment_part_form_for_update(*args, **kwargs)

    def get_assessment_part_form(self, *args, **kwargs):
        \"\"\"Pass through to provider AssessmentPartAdminSession.get_assessment_part_form_for_update\"\"\"
        # This method might be a bit sketchy. Time will tell.
        if isinstance(args[-1], list) or 'assessment_part_record_types' in kwargs:
            return self.get_assessment_part_form_for_create(*args, **kwargs)
        else:
            return self.get_assessment_part_form_for_update(*args, **kwargs)

    def duplicate_assessment_part(self, assessment_part_id):
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_admin_session').duplicate_assessment_part(assessment_part_id)"""

    delete_assessment_part = """
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_admin_session').delete_assessment_part(*args, **kwargs)"""

    can_create_assessment_parts = """
        \"\"\"Pass through to provider AssessmentPartAdminSession.can_create_assessment_parts\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_admin_session').can_create_assessment_parts()"""

    can_create_assessment_part_with_record_types = """
        \"\"\"Pass through to provider AssessmentPartAdminSession.can_create_assessment_part_with_record_types\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_admin_session').can_create_assessment_part_with_record_types(*args, **kwargs)"""


class AssessmentPartBankSession:
    can_lookup_assessment_part_bank_mappings = """
        \"\"\"Pass through to provider AssessmentPartBankSession.can_lookup_assessment_part_bank_mappings\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_bank_session').can_lookup_assessment_part_bank_mappings()"""

    get_assessment_part_ids_by_bank = """
        \"\"\"Pass through to provider AssessmentPartBankSession.get_assessment_part_ids_by_bank\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_bank_session').get_assessment_part_ids_by_bank(*args, **kwargs)"""


class AssessmentPartBankAssignmentSession:
    assign_assessment_part_to_bank = """
        \"\"\"Pass through to provider AssessmentPartBankAssignmentSession.assign_assessment_part_to_bank\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_bank_assignment_session').assign_assessment_part_to_bank(*args, **kwargs)"""

    can_assign_assessment_parts = """
        \"\"\"Pass through to provider AssessmentPartBankAssignmentSession.can_assign_assessment_parts\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_bank_assignment_session').can_assign_assessment_parts()"""


class AssessmentPartItemSession:
    get_assessment_part_items = """
        \"\"\"Pass through to provider method\"\"\"
        # Note: this method is different from the underlying signature
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_item_session').get_assessment_part_items(*args, **kwargs)"""

    get_assessment_parts_by_item = """
        \"\"\"Pass through to provider method\"\"\"
        # Note: this method is different from the underlying signature
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_item_session').get_assessment_parts_by_item(*args, **kwargs)"""

    can_access_assessment_part_items = """
        \"\"\"Pass through to provider method\"\"\"
        # Note: this method is different from the underlying signature
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_item_session').can_access_assessment_part_items()"""


class AssessmentPartItemDesignSession:
    import_statements = [
        'from .osid_errors import InvalidArgument'
    ]

    can_design_assessment_parts = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_item_design_session').can_design_assessment_parts()"""

    get_assessment_part_items = """
        \"\"\"Pass through to provider method\"\"\"
        # Note: this method is differenct from the underlying signature
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_item_design_session').get_items(*args, **kwargs)"""

    add_item = None

    move_item_ahead = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_item_design_session').move_item_ahead(*args, **kwargs)"""

    move_item_behind = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_item_design_session').move_item_behind(*args, **kwargs)"""

    remove_items = None

    order_items = None


class AssessmentPartLookupSession:
    get_assessment_part = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_lookup_session').get_assessment_part(*args, **kwargs)"""

    get_assessment_parts = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_lookup_session').get_assessment_parts()"""

    get_assessment_parts_for_assessment = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_lookup_session').get_assessment_parts_for_assessment(*args, **kwargs)"""

    get_assessment_parts_by_genus_type = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_lookup_session').get_assessment_parts_by_genus_type(*args, **kwargs)"""

    get_assessment_parts_by_parent_genus_type = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_lookup_session').get_assessment_parts_by_parent_genus_type(*args, **kwargs)"""

    get_assessment_parts_by_record_type = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_lookup_session').get_assessment_parts_by_record_type(*args, **kwargs)"""

    get_assessment_parts_by_ids = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_lookup_session').get_assessment_parts_by_ids(*args, **kwargs)"""

    can_lookup_assessment_parts = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_lookup_session').can_lookup_assessment_parts()"""

    use_sequestered_assessment_part_view = """
        \"\"\"Pass through to provider AssessmentPartLookupSession.use_sequestered_assessment_part_view\"\"\"
        # Does this need to be re-implemented to match the other non-sub-package view setters?
        self._containable_views['assessment_part'] = SEQUESTERED
        self._get_sub_package_provider_session('assessment_authoring',
                                               'assessment_part_lookup_session')
        for session in self._provider_sessions:
            for provider_session_name, provider_session in self._provider_sessions[session].items():
                try:
                    provider_session.use_sequestered_assessment_part_view()
                except AttributeError:
                    pass"""

    use_unsequestered_assessment_part_view = """
        \"\"\"Pass through to provider AssessmentPartLookupSession.use_unsequestered_assessment_part_view\"\"\"
        # Does this need to be re-implemented to match the other non-sub-package view setters?
        self._containable_views['assessment_part'] = UNSEQUESTERED
        self._get_sub_package_provider_session('assessment_authoring',
                                               'assessment_part_lookup_session')
        for session in self._provider_sessions:
            for provider_session_name, provider_session in self._provider_sessions[session].items():
                try:
                    provider_session.use_unsequestered_assessment_part_view()
                except AttributeError:
                    pass"""


class AssessmentPartQuerySession:
    get_assessment_part_query = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_query_session').get_assessment_part_query()"""

    can_search_assessment_parts = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_query_session').can_search_assessment_parts()"""


class SequenceRuleAdminSession:
    can_create_sequence_rule = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'sequence_rule_admin_session').can_create_sequence_rule()"""

    can_delete_sequence_rules = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'sequence_rule_admin_session').can_delete_sequence_rules()"""

    can_update_sequence_rules = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'sequence_rule_admin_session').can_update_sequence_rules()"""

    create_sequence_rule = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'sequence_rule_admin_session').create_sequence_rule(*args, **kwargs)"""

    delete_sequence_rule = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'sequence_rule_admin_session').delete_sequence_rule(*args, **kwargs)"""

    get_sequence_rule_form_for_create = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'sequence_rule_admin_session').get_sequence_rule_form_for_create(*args, **kwargs)"""

    get_sequence_rule_form_for_update = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'sequence_rule_admin_session').get_sequence_rule_form_for_update(*args, **kwargs)"""


class SequenceRuleLookupSession:
    can_lookup_sequence_rules = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'sequence_rule_lookup_session').can_lookup_sequence_rules()"""

    get_sequence_rule = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'sequence_rule_lookup_session').get_sequence_rule(*args, **kwargs)"""

    get_sequence_rules = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'sequence_rule_lookup_session').get_sequence_rules()"""

    get_sequence_rules_for_assessment = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'sequence_rule_lookup_session').get_sequence_rules_for_assessment(*args, **kwargs)"""


class Bank:
    import_statements = [
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
    def __init__(self, provider_manager, catalog, runtime, proxy, **kwargs):
        self._provider_manager = provider_manager
        self._catalog = catalog
        self._runtime = runtime
        osid.OsidObject.__init__(self, self._catalog)  # This is to initialize self._object
        osid.OsidSession.__init__(self, proxy)  # This is to initialize self._proxy
        self._catalog_id = catalog.get_id()
        self._provider_sessions = kwargs
        self._session_management = AUTOMATIC
        self._bank_view = DEFAULT
        self._object_views = dict()
        self._operable_views = dict()
        self._containable_views = dict()
        self._sub_package_provider_managers = dict()

    def _set_bank_view(self, session):
        \"\"\"Sets the underlying bank view to match current view\"\"\"
        if self._bank_view == FEDERATED:
            try:
                session.use_federated_bank_view()
            except AttributeError:
                pass
        else:
            try:
                session.use_isolated_bank_view()
            except AttributeError:
                pass

    def _set_object_view(self, session):
        \"\"\"Sets the underlying object views to match current view\"\"\"
        for obj_name in self._object_views:
            if self._object_views[obj_name] == PLENARY:
                try:
                    getattr(session, 'use_plenary_' + obj_name + '_view')()
                except AttributeError:
                    pass
            else:
                try:
                    getattr(session, 'use_comparative_' + obj_name + '_view')()
                except AttributeError:
                    pass

    def _set_containable_view(self, session):
        \"\"\"Sets the underlying containable views to match current view\"\"\"
        for obj_name in self._containable_views:
            if self._containable_views[obj_name] == SEQUESTERED:
                try:
                    getattr(session, 'use_sequestered_' + obj_name + '_view')()
                except AttributeError:
                    pass
            else:
                try:
                    getattr(session, 'use_unsequestered_' + obj_name + '_view')()
                except AttributeError:
                    pass

    def _set_operable_view(self, session):
        \"\"\"Sets the underlying operable views to match current view\"\"\"
        # for obj_name in self._operable_views:
        #     if self._operable_views[obj_name] == ???:
        #         try:
        #             getattr(session, 'use_???_' + obj_name + '_view')()
        #         except AttributeError:
        #             pass
        #     else:
        #         try:
        #             getattr(session, 'use_???_' + obj_name + '_view')()
        #         except AttributeError:
        #             pass
        pass

    def _get_provider_session(self, session_name):
        \"\"\"Returns the requested provider session.\"\"\"
        agent_key = self._get_agent_key()
        if session_name in self._provider_sessions[agent_key]:
            return self._provider_sessions[agent_key][session_name]
        else:
            session_class = getattr(self._provider_manager, 'get_' + session_name + '_for_bank')
            if self._proxy is None:
                if 'notification_session' in session_name:
                    # Is there something else we should do about the receiver field?
                    session = session_class('fake receiver', self._catalog.get_id())
                else:
                    session = session_class(self._catalog.get_id())
            else:
                if 'notification_session' in session_name:
                    # Is there something else we should do about the receiver field?
                    session = session_class('fake receiver', self._catalog.get_id(), self._proxy)
                else:
                    session = session_class(self._catalog.get_id(), self._proxy)
            self._set_bank_view(session)
            self._set_object_view(session)
            self._set_operable_view(session)
            self._set_containable_view(session)
            if self._session_management != DISABLED:
                self._provider_sessions[agent_key][session_name] = session
            return session

    def _get_sub_package_provider_manager(self, sub_package_name):
        if sub_package_name in self._sub_package_provider_managers:
            return self._sub_package_provider_managers[sub_package_name]
        config = self._runtime.get_configuration()
        parameter_id = Id('parameter:{0}ProviderImpl@dlkit_service'.format(sub_package_name))
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        if self._proxy is None:
            # need to add version argument
            sub_package = self._runtime.get_manager(sub_package_name.upper(), provider_impl)
        else:
            # need to add version argument
            sub_package = self._runtime.get_proxy_manager(sub_package_name.upper(), provider_impl)
        self._sub_package_provider_managers[sub_package_name] = sub_package
        return sub_package

    def _get_sub_package_provider_session(self, sub_package, session_name, proxy=None):
        \"\"\"Gets the session from a sub-package\"\"\"
        agent_key = self._get_agent_key()
        if session_name in self._provider_sessions[agent_key]:
            return self._provider_sessions[agent_key][session_name]
        else:
            manager = self._get_sub_package_provider_manager(sub_package)
            session = self._instantiate_session('get_' + session_name + '_for_bank',
                                                proxy=self._proxy,
                                                manager=manager)
            self._set_bank_view(session)
            self._set_object_view(session)
            self._set_operable_view(session)
            self._set_containable_view(session)
            if self._session_management != DISABLED:
                self._provider_sessions[agent_key][session_name] = session
            return session

    def _instantiate_session(self, method_name, proxy=None, manager=None, *args, **kwargs):
        \"\"\"Instantiates a provider session\"\"\"
        if manager is None:
            manager = self._provider_manager

        session_class = getattr(manager, method_name)
        if proxy is None:
            try:
                return session_class(bank_id=self._catalog_id, *args, **kwargs)
            except AttributeError:
                return session_class(*args, **kwargs)
        else:
            try:
                return session_class(bank_id=self._catalog_id, proxy=proxy, *args, **kwargs)
            except AttributeError:
                return session_class(proxy=proxy, *args, **kwargs)

    def get_bank_id(self):
        \"\"\"Gets the Id of this bank."\"\"
        return self._catalog_id

    def get_bank(self):
        \"\"\"Strange little method to assure conformance for inherited Sessions."\"\"
        return self

    def get_objective_hierarchy_id(self):
        \"\"\"WHAT am I doing here?\"\"\"
        return self._catalog_id

    def get_objective_hierarchy(self):
        \"\"\"WHAT am I doing here?\"\"\"
        return self

    def __getattr__(self, name):
        if '_catalog' in self.__dict__:
            try:
                return self._catalog[name]
            except AttributeError:
                pass
        raise AttributeError

    def close_sessions(self):
        \"\"\"Close all sessions currently being managed by this Manager to save memory."\"\"
        if self._session_management != MANDATORY:
            self._provider_sessions = dict()
        else:
            raise IllegalState()

    def use_automatic_session_management(self):
        \"\"\"Session state will be saved until closed by consumers."\"\"
        self._session_management = AUTOMATIC

    def use_mandatory_session_management(self):
        \"\"\"Session state will always be saved and can not be closed by consumers."\"\"
        # Session state will be saved and can not be closed by consumers
        self._session_management = MANDATORY

    def disable_session_management(self):
        \"\"\"Session state will never be saved."\"\"
        self._session_management = DISABLED
        self.close_sessions()"""
