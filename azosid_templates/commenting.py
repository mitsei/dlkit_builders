# commenting templates for az_osid

class CommentAdminSession:

    get_comment_form_for_create_template = """
        # Implemented from azosid template for -
        # osid.repository.CommentAdminSession.get_comment_form_for_create
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""
