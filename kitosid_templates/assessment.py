
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


class AssessmentPartLookupSession:
    get_assessment_part = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_lookup_session').get_assessment_part(*args, **kwargs)"""

    get_assessment_parts = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_lookup_session').get_assessment_parts()"""

    can_lookup_assessment_parts = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_lookup_session').can_lookup_assessment_parts()"""


class AssessmentPartAdminSession:
    get_assessment_part_form_for_create_for_assessment = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_admin_session').get_assessment_part_form_for_create_for_assessment(*args, **kwargs)"""

    get_assessment_part_form_for_create_for_assessment_part = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_admin_session').get_assessment_part_form_for_create_for_assessment_part(*args, **kwargs)"""

    get_assessment_part_form_for_update = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_admin_session').get_assessment_part_form_for_update(*args, **kwargs)"""

    create_assessment_part_for_assessment = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_admin_session').create_assessment_part_for_assessment(*args, **kwargs)"""

    create_assessment_part_for_assessment_part = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_admin_session').create_assessment_part_for_assessment_part(*args, **kwargs)"""

    update_assessment_part = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_admin_session').update_assessment_part(*args, **kwargs)"""

    delete_assessment_part = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_admin_session').delete_assessment_part(*args, **kwargs)"""

    can_create_assessment_parts = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_admin_session').can_create_assessment_parts()"""

    can_delete_assessment_parts = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_admin_session').can_delete_assessment_parts()"""

    can_update_assessment_parts = """
        \"\"\"Pass through to provider method\"\"\"
        return self._get_sub_package_provider_session('assessment_authoring',
                                                      'assessment_part_admin_session').can_update_assessment_parts()"""


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


class Bank:
    import_statements = [
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
    def __init__(self, provider_manager, catalog, proxy, **kwargs):
        self._provider_manager = provider_manager
        self._catalog = catalog
        osid.OsidObject.__init__(self, self._catalog) # This is to initialize self._object
        osid.OsidSession.__init__(self, proxy) # This is to initialize self._proxy
        self._catalog_id = catalog.get_id()
        self._provider_sessions = kwargs
        self._session_management = AUTOMATIC
        self._bank_view = DEFAULT
        self._object_views = dict()

        # for the sub-package impls
        if 'runtime' in kwargs:
            self._runtime = kwargs['runtime']

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


    def _get_provider_session(self, session_name):
        \"\"\"Returns the requested provider session.\"\"\"
        if session_name in self._provider_sessions:
            return self._provider_sessions[session_name]
        else:
            session_class = getattr(self._provider_manager, 'get_' + session_name + '_for_bank')
            if self._proxy is None:
                session = session_class(self._catalog.get_id())
            else:
                session = session_class(self._catalog.get_id(), self._proxy)
            self._set_bank_view(session)
            self._set_object_view(session)
            if self._session_management != DISABLED:
                self._provider_sessions[session_name] = session
            return session

    def _get_sub_package_provider_manager(self, sub_package):
        config = self._runtime.get_configuration()
        parameter_id = Id('parameter:{0}ProviderImpl@dlkit_service'.format(sub_package))
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        if self._proxy is None:
            # need to add version argument
            return self._runtime.get_manager(sub_package.upper(), provider_impl)
        else:
            # need to add version argument
            return self._runtime.get_proxy_manager(sub_package.upper(), provider_impl)

    def _get_sub_package_provider_session(self, sub_package, session_name, proxy=None):
        \"\"\"Gets the session from a sub-package\"\"\"
        if self._proxy is None:
            self._proxy = proxy
        if session_name in self._provider_sessions:
            return self._provider_sessions[session_name]
        else:
            manager = self._get_sub_package_provider_manager(sub_package)
            session = self._instantiate_session('get_' + session_name,
                                                proxy=self._proxy,
                                                manager=manager)
            self._set_bank_view(session)
            if self._session_management != DISABLED:
                self._provider_sessions[session_name] = session
            return session

    def _instantiate_session(self, method_name, proxy=None, manager=None, *args, **kwargs):
        \"\"\"Instantiates a provider session\"\"\"
        if manager is None:
            manager = self._provider_manager

        session_class = getattr(manager, method_name)
        if proxy is None:
            return session_class(*args, **kwargs)
        else:
            return session_class(proxy=proxy, *args, **kwargs)"""

