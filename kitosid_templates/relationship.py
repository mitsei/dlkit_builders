
class RelationshipAdminSession:

    get_relationship_form_for_create_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.relationship.RelationshipAdminSession.get_relationship_form_for_create_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""


class RelationshipLookupSession:

    get_relationships_for_source_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.relationship.RelationshipLookupSession.get_relationships_for_source_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_relationships_for_source_on_date_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.relationship.RelationshipLookupSession.get_relationships_for_source_on_date_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""
