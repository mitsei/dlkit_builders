

# Some of these should now be templated through resource
class AssessmentPartLookupSession:

    additional_methods = """
    def get_assessment_parts_for_assessment_part(self, assessment_part_id):
        # NOT CURRENTLY IN SPEC - Implemented from
        # osid.assessment_authoring.AssessmentPartLookupSession.additional_methods
        if self._can('lookup'):
            return self._provider_session.get_assessment_parts_for_assessment_part(assessment_part_id)
        self._check_lookup_conditions()  # raises PermissionDenied
        query = self._query_session.get_assessment_part_query()
        query.match_assessment_part_id(assessment_part_id, match=True)
        return self._try_harder(query)"""


class AssessmentAuthoringManager:
    # The following is here only until Tom fixes spec and adds these methods
    additional_methods = """
    def get_assessment_part_item_session(self):
        return self._provider_manager.get_assessment_part_item_session()

    assessment_part_item_session = property(fget=get_assessment_part_item_session)

    def get_assessment_part_item_session_for_bank(self, bank_id):
        return self._provider_manager.get_assessment_part_item_session_for_bank(bank_id)

    def get_assessment_part_item_design_session(self):
        return self._provider_manager.get_assessment_part_item_design_session()

    assessment_part_item_design_session = property(fget=get_assessment_part_item_design_session)

    def get_assessment_part_item_design_session_for_bank(self, bank_id):
        return self._provider_manager.get_assessment_part_item_design_session_for_bank(bank_id)"""


class AssessmentAuthoringProxyManager:
    # The following is here only until Tom fixes spec and adds these methods
    additional_methods = """
    def get_assessment_part_item_session(self, proxy):
        return self._provider_manager.get_assessment_part_item_session(proxy)

    assessment_part_item_session = property(fget=get_assessment_part_item_session)

    def get_assessment_part_item_session_for_bank(self, bank_id, proxy):
        return self._provider_manager.get_assessment_part_item_session_for_bank(bank_id, proxy)

    def get_assessment_part_item_design_session(self, proxy):
        return self._provider_manager.get_assessment_part_item_design_session(proxy)

    assessment_part_item_design_session = property(fget=get_assessment_part_item_design_session)

    def get_assessment_part_item_design_session_for_bank(self, bank_id, proxy):
        return self._provider_manager.get_assessment_part_item_design_session_for_bank(bank_id, proxy)"""


class AssessmentAuthoringProfile:
    import_statements_pattern = [
        "from ..osid.osid_errors import Unsupported"
    ]

    init = """
    def __init__(self):
        osid_managers.OsidProfile.__init__(self)

    def _get_hierarchy_session(self, proxy=None):
        base_package_mgr = self._get_base_package_provider_manager('assessment', proxy)
        if proxy is not None:
            try:
                return base_package_mgr.get_bank_hierarchy_session(proxy)
            except Unimplemented:
                return None
        try:
            return base_package_mgr.get_bank_hierarchy_session()
        except Unimplemented:
            return None

    def _get_base_package_provider_manager(self, base_package, proxy=None):
        config = self._my_runtime.get_configuration()
        parameter_id = Id('parameter:{0}ProviderImpl@dlkit_service'.format(base_package))
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        # try:
        #     # need to add version argument
        #     return self._my_runtime.get_proxy_manager(base_package.upper(), provider_impl)
        # except AttributeError:
        #     # need to add version argument
        #     return self._my_runtime.get_manager(base_package.upper(), provider_impl)
        if proxy is not None:
            # need to add version argument
            return self._my_runtime.get_proxy_manager(base_package.upper(), provider_impl)
        else:
            # need to add version argument
            return self._my_runtime.get_manager(base_package.upper(), provider_impl)
"""

    get_assessment_part_record_types = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentAuthoringProfile.get_assessment_part_record_types
        return self._provider_manager.get_assessment_part_record_types()

    assessment_part_record_types = property(fget=get_assessment_part_record_types)"""

    get_assessment_part_search_record_types = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentAuthoringProfile.get_assessment_part_search_record_types
        return self._provider_manager.get_assessment_part_search_record_types()

    assessment_part_search_record_types = property(fget=get_assessment_part_search_record_types)"""

    get_sequence_rule_enabler_record_types = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentAuthoringProfile.get_sequence_rule_enabler_record_types
        return self._provider_manager.get_sequence_rule_enabler_record_types()

    sequence_rule_enabler_record_types = property(fget=get_sequence_rule_enabler_record_types)"""

    get_sequence_rule_enabler_search_record_types = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentAuthoringProfile.get_sequence_rule_enabler_search_record_types
        return self._provider_manager.get_sequence_rule_enabler_search_record_types()

    sequence_rule_enabler_search_record_types = property(fget=get_sequence_rule_enabler_search_record_types)"""

    get_sequence_rule_record_types = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentAuthoringProfile.get_sequence_rule_record_types
        return self._provider_manager.get_sequence_rule_record_types()

    sequence_rule_record_types = property(fget=get_sequence_rule_record_types)"""

    get_sequence_rule_search_record_types = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentAuthoringProfile.get_sequence_rule_search_record_types
        return self._provider_manager.get_sequence_rule_search_record_types()

    sequence_rule_search_record_types = property(fget=get_sequence_rule_search_record_types)"""

    supports_assessment_part_admin = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentAuthoringProfile.supports_assessment_part_admin
        return self._provider_manager.supports_assessment_part_admin()"""

    supports_assessment_part_lookup = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentAuthoringProfile.supports_assessment_part_lookup
        return self._provider_manager.supports_assessment_part_lookup()"""

    supports_assessment_part_item_design = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentAuthoringProfile.supports_assessment_part_item_design
        return self._provider_manager.supports_assessment_part_item_design()"""

    supports_assessment_part_item = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentAuthoringProfile.supports_assessment_part_item
        return self._provider_manager.supports_assessment_part_item()"""

    supports_sequence_rule_admin = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentAuthoringProfile.supports_sequence_rule_admin
        return self._provider_manager.supports_sequence_rule_admin()"""

    supports_sequence_rule_lookup = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentAuthoringProfile.supports_sequence_rule_lookup
        return self._provider_manager.supports_sequence_rule_lookup()"""


class AssessmentPartAdminSession:

    update_assessment_part = """
        if not self._can('update'):
            raise PermissionDenied()
        return self._provider_session.update_assessment_part(assessment_part_id, assessment_part_form)"""

class SequenceRuleAdminSession:

    get_sequence_rule_form_for_create = """
        if not self._can('create'):
            raise PermissionDenied()
        return self._provider_session.get_sequence_rule_form_for_create(assessment_part_id, next_assessment_part_id, sequence_rule_record_types)"""
