"""repository templates for manager utils"""

class RepositoryProfile:

    import_statements_pattern = [
        'from ..type.objects import TypeList',
        'from ..osid.osid_errors import NullArgument',
    ]

    get_coordinate_types_template = """
        return TypeList([])"""

    supports_coordinate_type_template = """
        if ${arg0_name} is None:
            raise NullArgument()
        return False"""
