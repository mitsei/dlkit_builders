
class RelationshipAdminSession:
    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name}.${object_name}'
"""
    get_relationship_form_for_create_template = """
        # Implemented from azosid template for -
        # osid.resource.RelationshipAdminSession.get_relationship_form_for_create_template
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name}, ${arg2_name})"""


class RelationshipLookupSession:
    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name}.${object_name}'
"""
    get_relationships_for_source_template = """
        # Implemented from azosid template for -
        # osid.resource.RelationshipLookupSession.get_relationships_for_source_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_relationships_for_source_on_date_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from azosid template for -
        # osid.relationship.RelationshipLookupSession.get_relationships_for_source_on_date_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name}, ${arg2_name})"""


