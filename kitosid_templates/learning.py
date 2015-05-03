
class ObjectiveSequencingSession:

    can_sequence_objectives = """
        pass"""

    move_objective_ahead = """
        pass"""

    move_objective_behind = """
        pass"""

    sequence_objectives = """
        pass"""


class ActivityLookupSession:

    get_activities_for_objective_template = """
        # Implemented from kitosid template for -
        # osid.resource.ActivityLookupSession.get_activities_for_objective
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_activities_for_objectives_template = """
        # Implemented from kitosid template for -
        # osid.resource.ActivityLookupSession.get_activities_for_objectives
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

class ActivityAdminSession:

    get_activity_form_for_create_template = """
        # Implemented from -
        # osid.learning.ActivityAdminSession.get_activity_form_for_create_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

class ObjectiveAdminSession:

    delete_objective_template = """
        # Implemented from kitosid template for -
        # osid.learning.ObjectiveAdminSession.delete_objective
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

class ObjectiveRequisiteSession:
    
    can_lookup_objective_prerequisites_template = """
        # Implemented from kitosid template for -
        # osid.learning.ObjectiveRequisiteSession.can_lookup_objective_prerequisites
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_requisite_objectives_template = """
        # Implemented from kitosid template for -
        # osid.learning.ObjectiveRequisiteSession.get_requisite_objectives
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_all_requisite_objectives_template = """
        # Implemented from kitosid template for -
        # osid.learning.ObjectiveRequisiteSession.get_all_requisite_objectives
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_dependent_objectives_template = """
        # Implemented from kitosid template for -
        # osid.learning.ObjectiveRequisiteSession.get_dependent_objectives
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    is_objective_required_template = """
        # Implemented from kitosid template for -
        # osid.learning.ObjectiveRequisiteSession.is_objective_required
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_equivalent_objectives_template = """
        # Implemented from kitosid template for -
        # osid.learning.ObjectiveRequisiteSession.get_equivalent_objectives
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""


class ObjectiveRequisiteAssignmentSession:

    can_assign_requisites_template = """
        # Implemented from kitosid template for -
        # osid.learning.ObjectiveRequisiteAssignmentSession.can_assign_requisites
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    assign_objective_requisite_template = """
        # Implemented from kitosid template for -
        # osid.learning.ObjectiveRequisiteAssignmentSession.assign_objective_requisite
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    unassign_objective_requisite_template = """
        # Implemented from kitosid template for -
        # osid.learning.ObjectiveRequisiteAssignmentSession.unassign_objective_requisite
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    assign_equivalent_objective_template = """
        # Implemented from kitosid template for -
        # osid.learning.ObjectiveRequisiteAssignmentSession.assign_equivalent_objective
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    unassign_equivalent_objective_template = """
        # Implemented from kitosid template for -
        # osid.learning.ObjectiveRequisiteAssignmentSession.unassign_equivalent_objective
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""


