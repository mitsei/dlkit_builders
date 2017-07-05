# learning templates for az_osid


class ObjectiveAdminSession:

    delete_objective_template = """
        # Implemented from azosid template for -
        # osid.learning.ObjectiveAdminSession.delete_objective_template
        if not self._can_for_${object_name_under}('delete', ${object_name_under}_id):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""


class ActivityLookupSession:

    get_activities_for_objective_template = """
        # Implemented from azosid template for -
        # osid.learning.ActivityLookupSession.get_activities_for_objective_template
        if self._can('lookup'):
            return self._provider_session.${method_name}(${arg0_name})
        self._check_lookup_conditions()  # raises PermissionDenied
        query = self._query_session.get_${object_name_under}_query()
        query.match_${arg0_object_under}_id(${arg0_name}, match=True)
        return self._try_harder(query)"""

    get_activities_for_objectives_template = """
        # Implemented from azosid template for -
        # osid.learning.ActivityLookupSession.get_activities_for_objectives_template
        if self._can('lookup'):
            return self._provider_session.${method_name}(${arg0_name})
        self._check_lookup_conditions()  # raises PermissionDenied
        query = self._query_session.get_${object_name_under}_query()
        for ${object_name_under}_id in (${arg0_name}):
            query.match_${arg0_object_under}_id(${object_name_under}_id, match=True)
        return self._try_harder(query)"""


class ActivityAdminSession:

    get_activity_form_for_create_template = """
        # Implemented from azosid template for -
        # osid.learning.ActivityAdminSession.get_activity_form_for_create_template
        if not self._can('create'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""


class ObjectiveRequisiteAssignmentSession:
    init = """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        self._qualifier_id = self._provider_session.get_objective_bank_id()
        self._id_namespace = 'learning.Objective'
        self._auth_objective_bank_ids = None
        self._unauth_objective_bank_ids = None"""

    unassign_objective_requisite = """
        if not self._can('modify'):
            raise PermissionDenied()
        return self._provider_session.unassign_objective_requisite(objective_id, requisite_objective_id)"""

    assign_objective_requisite = """
        if not self._can('modify'):
            raise PermissionDenied()
        return self._provider_session.assign_objective_requisite(objective_id, requisite_objective_id)"""


class ObjectiveRequisiteSession:
    init = """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        self._qualifier_id = self._provider_session.get_objective_bank_id()
        self._id_namespace = 'learning.Objective'
        self._auth_objective_bank_ids = None
        self._unauth_objective_bank_ids = None"""

    get_requisite_objectives = """
        if self._can('lookup'):
            return self._provider_session.get_requisite_objectives(objective_id)
        self._check_lookup_conditions()  # raises PermissionDenied
        query = self._query_session.get_objective_query()
        query.match_requisite_objective_id(objective_id, match=True)
        return self._try_harder(query)"""

    get_dependent_objectives = """
        if self._can('lookup'):
            return self._provider_session.get_dependent_objectives(objective_id)
        self._check_lookup_conditions()  # raises PermissionDenied
        query = self._query_session.get_objective_query()
        query.match_dependent_objective_id(objective_id, match=True)
        return self._try_harder(query)"""
