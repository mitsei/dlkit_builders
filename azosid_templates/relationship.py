
from . import resource

class RelationshipAdminSession:

    init_template = resource.ResourceAdminSession.init_template

#     old_init_template = """
#     def __init__(self, provider_session, authz_session, proxy=None):
#         osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
#         self._qualifier_id = provider_session.get_${cat_name_under}_id()
#         self._id_namespace = '${pkg_name}.${object_name}'
# """

    get_relationship_form_for_create_template = """
        # Implemented from azosid template for -
        # osid.resource.RelationshipAdminSession.get_relationship_form_for_create_template
        if not self._can('create'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name}, ${arg1_name}, ${arg2_name})"""


class RelationshipLookupSession:

    init_template = resource.ResourceLookupSession.init_template

#     init_template = """
#     def __init__(self, provider_session, authz_session, proxy=None):
#         osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
#         self._qualifier_id = provider_session.get_${cat_name_under}_id()
#         self._id_namespace = '${pkg_name}.${object_name}'
# """

    get_relationships_for_source_template = """
        # Implemented from azosid template for -
        # osid.resource.RelationshipLookupSession.get_relationships_for_source_template
        if self._can('lookup'):
            return self._provider_session.${method_name}(${arg0_name})
        self._check_lookup_conditions() # raises PermissionDenied
        query = self._query_session.get_${object_name_under}_query()
        query.match_source_id(${arg0_name}, match=True)
        return self._try_harder(query)"""

    get_relationships_for_source_on_date_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from azosid template for -
        # osid.relationship.RelationshipLookupSession.get_relationships_for_source_on_date_template
        if self._can('lookup'):
            return self._provider_session.${method_name}(${arg0_name})
        self._check_lookup_conditions() # raises PermissionDenied
        query = self._query_session.get_${object_name_under}_query()
        query.match_source_id(${arg0_name}, match=True)
        query.match_date(${arg1_name}, ${arg2_name}, match=True)
        return self._try_harder(query)"""


