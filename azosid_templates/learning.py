# learning templates for az_osid

class ObjectiveAdminSession:

    delete_objective_template = """
        # Implemented from azosid template for -
        # osid.learning.ObjectiveAdminSession.delete_objective_template
        if not self._can('delete'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

class ActivityLookupSession:

    get_activities_for_objective_template = """
        # Implemented from azosid template for -
        # osid.learning.ActivityLookupSession.get_activities_for_objective_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_activities_for_objectives_template = """
        # Implemented from azosid template for -
        # osid.learning.ActivityLookupSession.get_activities_for_objectives_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""


class ActivityAdminSession:

    get_activity_form_for_create_template = """
        # Implemented from azosid template for -
        # osid.learning.ActivityAdminSession.get_activity_form_for_create_template
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

