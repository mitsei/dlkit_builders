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
    def __init__(self, provider_session, authz_session, proxy=None, **kwargs):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        if 'hierarchy_session' in kwargs:
            self._hierarchy_session = kwargs['hierarchy_session']
        else:
            self._hierarchy_session = None
        if 'query_session' in kwargs:
            self._query_session = kwargs['query_session']
        else:
            self._query_session = None

        self._qualifier_id = provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name}.${object_name}'
        self.use_federated_${cat_name_under}_view()
        self.use_comparative_${object_name_under}_view()
        self._unauth_${cat_name_under}_ids = None

    def _get_unauth_${cat_name_under}_ids(self, ${cat_name_under}_id):
        if self._can('lookup', ${cat_name_under}_id):
            return [] # Don't go further - assumes authorizations inherited
        else:
            unauth_list = [str(${cat_name_under}_id)]
        if self._hierarchy_session.has_child_${cat_name_under_plural}(${cat_name_under}_id):
            for child_${cat_name_under}_id in self._hierarchy_session.get_child_${cat_name_under}_ids(${cat_name_under}_id):
                unauth_list = unauth_list + self._get_unauth_${cat_name_under}_ids(child_${cat_name_under}_id)
        return unauth_list

    def _try_harder(self, query):
        if self._hierarchy_session is None or self._query_session is None:
            # Should probably try to return empty result instead
            # perhaps through a query.match_any(match = None)?
            raise PermissionDenied()
        if self._unauth_${cat_name_under}_ids is None:
            self._unauth_${cat_name_under}_ids = self._get_unauth_${cat_name_under}_ids(self._qualifier_id)
        for ${cat_name_under}_id in self._unauth_${cat_name_under}_ids:
            query.match_${cat_name_under}_id(${cat_name_under}_id, match=False)
        return self._query_session.get_${object_name_under_plural}_by_query(query)"""

class CommentQuerySession:
    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None, **kwargs):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        if 'hierarchy_session' in kwargs:
            self._hierarchy_session = kwargs['hierarchy_session']
        else:
            self._hierarchy_session = None
        if 'query_session' in kwargs:
            self._query_session = kwargs['query_session']
        else:
            self._query_session = None

        self._qualifier_id = provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name}.${object_name}'
        self.use_federated_${cat_name_under}_view()
        self._unauth_${cat_name_under}_ids = None

    def _get_unauth_${cat_name_under}_ids(self, ${cat_name_under}_id):
        if self._can('search', ${cat_name_under}_id):
            return [] # Don't go further - assumes authorizations inherited
        else:
            unauth_list = [str(${cat_name_under}_id)]
        if self._hierarchy_session.has_child_${cat_name_under_plural}(${cat_name_under}_id):
            for child_${cat_name_under}_id in self._hierarchy_session.get_child_${cat_name_under}_ids(${cat_name_under}_id):
                unauth_list = unauth_list + self._get_unauth_${cat_name_under}_ids(child_${cat_name_under}_id)
        return unauth_list

    def _try_harder(self, query):
        if self._hierarchy_session is None:
            # Should probably try to return empty result instead
            # perhaps through a query.match_any(match = None)?
            raise PermissionDenied()
        if self._unauth_${cat_name_under}_ids is None:
            self._unauth_${cat_name_under}_ids = self._get_unauth_${cat_name_under}_ids(self._qualifier_id)
        for ${cat_name_under}_id in self._unauth_${cat_name_under}_ids:
            query.match_${cat_name_under}_id(${cat_name_under}_id, match=False)
        return self._query_session.get_${object_name_under_plural}_by_query(query)

    class ${object_name}QueryWrapper(QueryWrapper):
        \"\"\"Wrapper for ${object_name}Queries to override match_${cat_name_under}_id method\"\"\"

        def match_${cat_name_under}_id(self, ${cat_name_under}_id, match=True):
            self.cat_id_args_list.append({'${cat_name_under}_id': ${cat_name_under}_id, 'match': match})"""