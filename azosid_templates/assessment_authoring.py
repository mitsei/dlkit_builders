
# Some of these should now be templated through resource
class AssessmentPartLookupSession:
# 
#     get_assessment_part = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartLookupSession.get_assessment_part
#         if not self._can('lookup'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.get_assessment_part(assessment_part_id)"""
# 
#     get_assessment_parts = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartLookupSession.get_assessment_parts
#         if not self._can('lookup'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.get_assessment_parts()"""
# 
#     get_assessment_parts_by_genus_type = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartLookupSession.get_assessment_parts_by_genus_type
#         if not self._can('lookup'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.get_assessment_parts_by_genus_type(assessment_part_genus_type)"""
# 
#     get_assessment_parts_by_ids = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartLookupSession.get_assessment_parts_by_ids
#         if not self._can('lookup'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.get_assessment_parts_by_ids(assessment_part_ids)"""
# 
#     get_assessment_parts_by_parent_genus_type = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartLookupSession.get_assessment_parts_by_parent_genus_type
#         if not self._can('lookup'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.get_assessment_parts_by_parent_genus_type(assessment_genus_type)"""
# 
#     get_assessment_parts_by_record_type = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartLookupSession.get_assessment_parts_by_record_type
#         if not self._can('lookup'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.get_assessment_parts_by_record_type(assessment_part_record_type)"""
# 
#     can_lookup_assessment_parts = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartLookupSession.can_lookup_assessment_parts
#         if not self._can('lookup'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.can_lookup_assessment_parts()"""
# 
#     use_comparative_assessment_part_view = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartLookupSession.use_comparative_assessment_part_view
#         if not self._can('lookup'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.use_comparative_assessment_part_view()"""
# 
#     use_plenary_assessment_part_view = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartLookupSession.use_plenary_assessment_part_view
#         if not self._can('lookup'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.use_plenary_assessment_part_view()"""
# 
#     use_unsequestered_assessment_part_view = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartLookupSession.use_unsequestered_assessment_part_view
#         if not self._can('lookup'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.use_unsequestered_assessment_part_view()"""

    additional_methods = """
    def get_assessment_parts_for_assessment_part(self, assessment_part_id):
        # NOT CURRENTLY IN SPEC - Implemented from
        # osid.assessment_authoring.AssessmentPartLookupSession.additional_methods
        if self._can('lookup'):
            return self._provider_session.get_assessment_parts_for_assessment_part(assessment_part_id)
        self._check_lookup_conditions() # raises PermissionDenied
        query = self._query_session.get_assessment_part_query()
        query.match_assessment_part_id(assessment_part_id, match=True)
        return self._try_harder(query)"""


# Some of these should now be templated through resource
# class AssessmentPartAdminSession:
#     alias_assessment_part = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartAdminSession.alias_assessment_part
#         if not self._can('update'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.alias_assessment_part(assessment_part_id,
#                                                                 alias_id)"""
# 
#     get_assessment_part_form_for_create_for_assessment = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartAdminSession.get_assessment_part_form_for_create_for_assessment
#         if not self._can('create'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.get_assessment_part_form_for_create_for_assessment(assessment_id,
#                                                                                              assessment_part_record_types)"""
# 
#     get_assessment_part_form_for_create_for_assessment_part = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartAdminSession.get_assessment_part_form_for_create_for_assessment_part
#         if not self._can('create'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.get_assessment_part_form_for_create_for_assessment_part(assessment_part_id,
#                                                                                                   assessment_part_record_types)"""
# 
#     get_assessment_part_form_for_update = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartAdminSession.get_assessment_part_form_for_update
#         if not self._can('update'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.get_assessment_part_form_for_update(assessment_part_id)"""
# 
#     create_assessment_part_for_assessment = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartAdminSession.create_assessment_part_for_assessment
#         if not self._can('create'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.create_assessment_part_for_assessment(assessment_part_form)"""
# 
#     create_assessment_part_for_assessment_part = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartAdminSession.create_assessment_part_for_assessment_part
#         if not self._can('create'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.create_assessment_part_for_assessment_part(assessment_part_form)"""
# 
#     update_assessment_part = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartAdminSession.update_assessment_part
#         if not self._can('update'):
#             raise PermissionDenied()
#         else:
#             # because there is a bug in the spec
#             return self._provider_session.update_assessment_part(assessment_part_id, assessment_part_form)"""
# 
#     delete_assessment_part = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartAdminSession.delete_assessment_part
#         if not self._can('delete'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.delete_assessment_part(assessment_part_id)"""
# 
#     can_create_assessment_parts = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartAdminSession.can_create_assessment_parts
#         if not self._can('create'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.can_create_assessment_parts()"""
# 
#     can_delete_assessment_parts = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartAdminSession.can_delete_assessment_parts
#         if not self._can('delete'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.can_delete_assessment_parts()"""
# 
#     can_update_assessment_parts = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.AssessmentPartAdminSession.can_update_assessment_parts
#         if not self._can('update'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.can_update_assessment_parts()"""

# These should now be templated throug resource
# class SequenceRuleAdminSession:
#     can_create_sequence_rule = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.SequenceRuleAdminSession.can_create_sequence_rule
#         if not self._can('create'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.can_create_sequence_rule()"""
# 
#     can_delete_sequence_rules = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.SequenceRuleAdminSession.can_delete_sequence_rules
#         if not self._can('delete'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.can_delete_sequence_rules()"""
# 
#     can_update_sequence_rules = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.SequenceRuleAdminSession.can_update_sequence_rules
#         if not self._can('update'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.can_update_sequence_rules()"""
# 
#     create_sequence_rule = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.SequenceRuleAdminSession.create_sequence_rule
#         if not self._can('create'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.create_sequence_rule(sequence_rule_form)"""
# 
#     delete_sequence_rule = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.SequenceRuleAdminSession.delete_sequence_rule
#         if not self._can('delete'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.delete_sequence_rule(sequence_rule_id)"""
# 
#     get_sequence_rule_form_for_create = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.SequenceRuleAdminSession.get_sequence_rule_form_for_create
#         if not self._can('create'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.get_sequence_rule_form_for_create(assessment_part_id,
#                                                                             next_assessment_part_id,
#                                                                             sequence_rule_record_types)"""
# 
#     get_sequence_rule_form_for_update = """
#         # Implemented from azosid template for -
#         # osid.assessment_authoring.SequenceRuleAdminSession.get_sequence_rule_form_for_update
#         if not self._can('update'):
#             raise PermissionDenied()
#         else:
#             return self._provider_session.get_sequence_rule_form_for_update(sequence_rule_id)"""

# These should be templated through resource
# class SequenceRuleLookupSession:
    # can_lookup_sequence_rules = """
    #     # Implemented from azosid template for -
    #     # osid.assessment_authoring.SequenceRuleLookupSession.can_lookup_sequence_rules
    #     if not self._can('lookup'):
    #         raise PermissionDenied()
    #     else:
    #         return self._provider_session.can_lookup_sequence_rules()"""
    # 
    # get_sequence_rule = """
    #     # Implemented from azosid template for -
    #     # osid.assessment_authoring.SequenceRuleLookupSession.get_sequence_rule
    #     if not self._can('lookup'):
    #         raise PermissionDenied()
    #     else:
    #         return self._provider_session.get_sequence_rule(sequence_rule_id)"""
    # 
    # get_sequence_rules = """
    #     # Implemented from azosid template for -
    #     # osid.assessment_authoring.SequenceRuleLookupSession.get_sequence_rules
    #     if not self._can('lookup'):
    #         raise PermissionDenied()
    #     else:
    #         return self._provider_session.get_sequence_rules()"""

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
    def __init__(self, interface_name):
        osid_managers.OsidProfile.__init__(self)

    def _get_hierarchy_session(self, proxy=None):
        # currently proxy not used, even if it's passed in...
        try:
            base_package_mgr = self._get_base_package_provider_manager('assessment')
            return base_package_mgr.get_bank_hierarchy_session(proxy)
        except Unsupported:
            return None

    def _get_base_package_provider_manager(self, base_package):
        config = self._my_runtime.get_configuration()
        parameter_id = Id('parameter:{0}ProviderImpl@dlkit_service'.format(base_package))
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        try:
            # need to add version argument
            return self._my_runtime.get_proxy_manager(base_package.upper(), provider_impl)
        except AttributeError:
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