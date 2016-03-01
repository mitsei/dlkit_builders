class AssessmentPartLookupSession:
    get_assessment_part = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartLookupSession.get_assessment_part
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_assessment_part(assessment_part_id)"""

    get_assessment_parts = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartLookupSession.get_assessment_parts
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_assessment_parts()"""

    can_lookup_assessment_parts = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartLookupSession.can_lookup_assessment_parts
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.can_lookup_assessment_parts()"""

    use_unsequestered_assessment_part_view = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartLookupSession.use_unsequestered_assessment_part_view
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.use_unsequestered_assessment_part_view()"""


class AssessmentPartAdminSession:
    get_assessment_part_form_for_create_for_assessment = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.get_assessment_part_form_for_create_for_assessment
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_assessment_part_form_for_create_for_assessment(assessment_id,
                                                                                             assessment_part_record_types)"""

    get_assessment_part_form_for_create_for_assessment_part = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.get_assessment_part_form_for_create_for_assessment_part
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_assessment_part_form_for_create_for_assessment_part(assessment_part_id,
                                                                                                  assessment_part_record_types)"""

    get_assessment_part_form_for_update = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.get_assessment_part_form_for_update
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_assessment_part_form_for_update(assessment_part_id)"""

    create_assessment_part_for_assessment = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.create_assessment_part_for_assessment
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.create_assessment_part_for_assessment(assessment_part_form)"""

    create_assessment_part_for_assessment_part = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.create_assessment_part_for_assessment_part
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.create_assessment_part_for_assessment_part(assessment_part_form)"""

    update_assessment_part = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.update_assessment_part
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.update_assessment_part(assessment_part_form)"""

    delete_assessment_part = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.delete_assessment_part
        if not self._can('delete'):
            raise PermissionDenied()
        else:
            return self._provider_session.delete_assessment_part(assessment_part_id)"""

    can_create_assessment_parts = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.can_create_assessment_parts
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.can_create_assessment_parts()"""

    can_delete_assessment_parts = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.can_delete_assessment_parts
        if not self._can('delete'):
            raise PermissionDenied()
        else:
            return self._provider_session.can_delete_assessment_parts()"""

    can_update_assessment_parts = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.AssessmentPartAdminSession.can_update_assessment_parts
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.can_update_assessment_parts()"""


class SequenceRuleAdminSession:
    can_create_sequence_rule = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleAdminSession.can_create_sequence_rule
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.can_create_sequence_rule()"""

    can_delete_sequence_rules = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleAdminSession.can_delete_sequence_rules
        if not self._can('delete'):
            raise PermissionDenied()
        else:
            return self._provider_session.can_delete_sequence_rules()"""

    can_update_sequence_rules = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleAdminSession.can_update_sequence_rules
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.can_update_sequence_rules()"""

    create_sequence_rule = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleAdminSession.create_sequence_rule
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.create_sequence_rule(sequence_rule_form)"""

    delete_sequence_rule = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleAdminSession.delete_sequence_rule
        if not self._can('delete'):
            raise PermissionDenied()
        else:
            return self._provider_session.delete_sequence_rule(sequence_rule_id)"""

    get_sequence_rule_form_for_create = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleAdminSession.get_sequence_rule_form_for_create
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_sequence_rule_form_for_create(assessment_part_id,
                                                                            next_assessment_part_id,
                                                                            sequence_rule_record_types)"""

    get_sequence_rule_form_for_update = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleAdminSession.get_sequence_rule_form_for_update
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_sequence_rule_form_for_update(sequence_rule_id)"""


class SequenceRuleLookupSession:
    can_lookup_sequence_rules = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleLookupSession.can_lookup_sequence_rules
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.can_lookup_sequence_rules()"""

    get_sequence_rule = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleLookupSession.get_sequence_rule
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_sequence_rule(sequence_rule_id)"""

    get_sequence_rules = """
        # Implemented from azosid template for -
        # osid.assessment_authoring.SequenceRuleLookupSession.get_sequence_rules
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_sequence_rules()"""


