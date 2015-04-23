
class CommentAdminSession:

    get_comment_form_for_create_template = """
        # Implemented from -
        # osid.commenting.CommentAdminSession.get_comment_form_for_create
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""
