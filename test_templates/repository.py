
class RepositoryProfile:

    get_coordinate_types_template = """
        self.assertTrue(isinstance(self.mgr.${method_name}(), abc_type_list))"""

    supports_coordinate_type_template = """
        self.assertTrue(isinstance(self.mgr.${method_name}(DEFAULT_TYPE), bool))"""


class AssetAdminSession:

    import_statements_pattern = [
    ]

    create_asset_content_template = """
        pass"""

    get_asset_content_form_for_update_template = """
        pass"""

    update_asset_content_template = """
        pass"""

    delete_asset_content_template = """
        pass"""


class Asset:

    import_statements = [
    ]

    get_title_template = """
        pass"""

    can_distribute_verbatim_template = """
        pass"""

    get_asset_content_ids_template = """
        pass"""

    get_asset_contents_template = """
        pass"""

class AssetForm:

    set_title_template = """
        pass"""

    clear_title_template = """
        pass"""


class AssetContent:

    import_statements = [
    ]

    has_url_template = """
        pass"""

    get_url_template = """
        pass"""

    get_data = """
        pass""" 


class AssetContentForm:

    import_statements = [
        ]

    set_url_template = """
        pass"""

    set_data = """
        pass"""

    clear_data = """
        pass"""
