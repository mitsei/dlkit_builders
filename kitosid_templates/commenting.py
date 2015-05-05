
class CommentAdminSession:

    get_comment_form_for_create_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from -
        # osid.commenting.CommentAdminSession.get_comment_form_for_create
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""
