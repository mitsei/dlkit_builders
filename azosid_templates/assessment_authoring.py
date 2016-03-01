class AssessmentPartLookupSession:
    get_assessment_part = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartLookupSession.get_assessment_part
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('assessment_part_lookup_session').get_assessment_part(*args, **kwargs)"""

    get_assessment_parts = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartLookupSession.get_assessment_parts
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('assessment_part_lookup_session').get_assessment_parts(*args, **kwargs)"""

    can_lookup_assessment_parts = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartLookupSession.can_lookup_assessment_parts
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('assessment_part_lookup_session').can_lookup_assessment_parts(*args, **kwargs)"""


class AssessmentPartAdminSession:
    get_assessment_part_form_for_create_for_assessment = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.get_assessment_part_form_for_create_for_assessment
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('assessment_part_admin_session').get_assessment_part_form_for_create_for_assessment(*args, **kwargs)"""

    get_assessment_part_form_for_create_for_assessment_part = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.get_assessment_part_form_for_create_for_assessment_part
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('assessment_part_admin_session').get_assessment_part_form_for_create_for_assessment_part(*args, **kwargs)"""

    get_assessment_part_form_for_update = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.get_assessment_part_form_for_update
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('assessment_part_admin_session').get_assessment_part_form_for_update(*args, **kwargs)"""

    create_assessment_part_for_assessment = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.create_assessment_part_for_assessment
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('assessment_part_admin_session').create_assessment_part_for_assessment(*args, **kwargs)"""

    create_assessment_part_for_assessment_part = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.create_assessment_part_for_assessment_part
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('assessment_part_admin_session').create_assessment_part_for_assessment_part(*args, **kwargs)"""

    update_assessment_part = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.update_assessment_part
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('assessment_part_admin_session').update_assessment_part(*args, **kwargs)"""

    delete_assessment_part = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.delete_assessment_part
        if not self._can('delete'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('assessment_part_admin_session').delete_assessment_part(*args, **kwargs)"""

    can_create_assessment_parts = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.can_create_assessment_parts
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('assessment_part_admin_session').can_create_assessment_parts(*args, **kwargs)"""

    can_delete_assessment_parts = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.can_delete_assessment_parts
        if not self._can('delete'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('assessment_part_admin_session').can_delete_assessment_parts(*args, **kwargs)"""

    can_update_assessment_parts = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.can_update_assessment_parts
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('assessment_part_admin_session').can_update_assessment_parts(*args, **kwargs)"""


class SequenceRuleAdminSession:
    can_create_sequence_rule = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleAdminSession.can_create_sequence_rule
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('sequence_rule_admin_session').can_create_sequence_rule(*args, **kwargs)"""

    can_delete_sequence_rules = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleAdminSession.can_delete_sequence_rules
        if not self._can('delete'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('sequence_rule_admin_session').can_delete_sequence_rules(*args, **kwargs)"""

    can_update_sequence_rules = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleAdminSession.can_update_sequence_rules
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('sequence_rule_admin_session').can_update_sequence_rules(*args, **kwargs)"""

    create_sequence_rule = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleAdminSession.create_sequence_rule
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('sequence_rule_admin_session').create_sequence_rule(*args, **kwargs)"""

    delete_sequence_rule = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleAdminSession.delete_sequence_rule
        if not self._can('delete'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('sequence_rule_admin_session').delete_sequence_rule(*args, **kwargs)"""

    get_sequence_rule_form_for_create = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleAdminSession.get_sequence_rule_form_for_create
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('sequence_rule_admin_session').get_sequence_rule_form_for_create(*args, **kwargs)"""

    get_sequence_rule_form_for_update = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleAdminSession.get_sequence_rule_form_for_update
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('sequence_rule_admin_session').get_sequence_rule_form_for_update(*args, **kwargs)"""


class SequenceRuleLookupSession:
    can_lookup_sequence_rules = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleLookupSession.can_lookup_sequence_rules
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('sequence_rule_lookup_session').can_lookup_sequence_rules(*args, **kwargs)"""

    get_sequence_rule = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleLookupSession.get_sequence_rule
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('sequence_rule_lookup_session').get_sequence_rule(*args, **kwargs)"""

    get_sequence_rules = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleLookupSession.get_sequence_rules
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._get_provider_session('sequence_rule_lookup_session').get_sequence_rules(*args, **kwargs)"""


