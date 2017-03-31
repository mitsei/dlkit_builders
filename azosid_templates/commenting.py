# commenting templates for az_osid

from . import resource


class CommentAdminSession:

    get_comment_form_for_create_template = """
        # Implemented from azosid template for -
        # osid.repository.CommentAdminSession.get_comment_form_for_create
        if not self._can('create'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""


class CommentLookupSession:

    init_template = resource.ResourceLookupSession.init_template


class CommentQuerySession:

    init_template = resource.ResourceQuerySession.init_template
