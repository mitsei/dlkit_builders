
class Relationship:

    get_source_id_template = """
        # Implemented from template for osid.relationship.Relationship.get_source_id
        from ..primitives import Id
        return Id(self._my_map['${var_name_mixed}Id'])"""
