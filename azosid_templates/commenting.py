# commenting templates for az_osid

class CommentAdminSession:

    get_comment_form_for_create_template = """
        # Implemented from azosid template for -
        # osid.repository.CommentAdminSession.get_comment_form_for_create
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""


class CommentLookupSession:

    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name}.${object_name}'
"""