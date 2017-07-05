
class RelationshipLookupSession:

    import_statements_pattern = [
        'import datetime',
        'from dlkit.abstract_osid.${pkg_name_replaced_reserved} import objects as ABCObjects',
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.calendaring.primitives import DateTime',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.primordium.id.primitives import Id',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'AGENT_ID = Id(**{\'identifier\': \'jane_doe\', \'namespace\': \'osid.agent.Agent\', \'authority\': \'MIT-ODL\'})',
    ]

    get_relationships_for_source_template = """
        pass"""

    get_relationships_by_genus_type_for_source_template = """
        pass"""

    get_relationships_for_destination_template = """
        pass"""

    get_relationships_by_genus_type_for_destination_template = """
        pass"""

    get_relationships_for_peers_template = """
        pass"""

    get_relationships_by_genus_type_for_peers_template = """
        pass"""

    get_relationships_for_source_on_date_template = """
        # From test_templates/relationship.py::RelationshipLookupSession::get_relationships_for_source_on_date_template
        if not is_never_authz(self.service_config):
            end_date = DateTime.utcnow() + datetime.timedelta(days=5)
            end_date = DateTime(**{
                'year': end_date.year,
                'month': end_date.month,
                'day': end_date.day,
                'hour': end_date.hour,
                'minute': end_date.minute,
                'second': end_date.second,
                'microsecond': end_date.microsecond
            })

            # NOTE: this first argument will probably break in many of the other methods,
            #   since it's not clear they always use something like AGENT_ID
            # i.e. in get_grade_entries_for_gradebook_column_on_date it needs to be
            #   a gradebookColumnId.
            results = self.session.${method_name}(AGENT_ID, DateTime.utcnow(), end_date)
            assert isinstance(results, ABCObjects.${return_type})
            assert results.available() == 2"""


class RelationshipAdminSession:

    import_statements_pattern = [
    ]

    get_relationship_form_for_create_template = """
        pass"""


class Relationship:

    import_statements = [
    ]

    get_source_id_template = """
        pass"""


class RelationshipQuery:

    import_statements = [
    ]
