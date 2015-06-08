
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


class CompositionLookupSession:

    use_active_composition_view = """
        self.catalog.use_active_composition_view()"""

    use_any_status_composition_view = """
        self.catalog.use_any_status_composition_view()"""

    use_sequestered_composition_view = """
        self.catalog.use_sequestered_composition_view()"""

    use_unsequestered_composition_view = """
        self.catalog.use_unsequestered_composition_view()"""


class CompositionAdminSession:

    import_statements_pattern = [
    ]

    additional_methods = """
    def test_composition_assignment(self):
        composition_list = list()
        composition_ids = list()
        for num in [0, 1, 2, 3]:
            create_form = self.catalog.get_composition_form_for_create([])
            create_form.display_name = 'Test Composition ' + str(num)
            create_form.description = 'Test Composition for CompositionLookupSession tests'
            obj = self.catalog.create_composition(create_form)
            composition_list.append(obj)
            composition_ids.append(obj.ident)
        update_form = self.catalog.get_composition_form_for_update(composition_ids[0])
        update_form.set_children(composition_ids[1:])
        self.catalog.update_composition(update_form)
        composition = self.catalog.get_composition(composition_ids[0])
        self.assertEqual(composition.get_children_ids().available(), 3)
        self.assertEqual(composition.get_child_ids().available(), 3)
        self.assertEqual(composition.get_children().available(), 3)
"""


class AssetCompositionSession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.asset_list = list()
        cls.asset_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', 'TEST_SERVICE', PROXY)
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for AssetLookupSession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)
        create_form = cls.catalog.get_composition_form_for_create([])
        create_form.display_name = 'Test Composition for AssetCompositionSession tests'
        create_form.description = 'Test Compposion for AssetCompositionSession tests'
        cls.composition = cls.catalog.create_composition(create_form)
        for num in [0, 1, 2, 3]:
            create_form = cls.catalog.get_asset_form_for_create([])
            create_form.display_name = 'Test Asset ' + str(num)
            create_form.description = 'Test Asset for AssetLookupSession tests'
            obj = cls.catalog.create_asset(create_form)
            cls.asset_list.append(obj)
            cls.asset_ids.append(obj.ident)
            cls.catalog.add_asset(obj.ident, cls.composition.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_repositories():
            for obj in catalog.get_assets():
                catalog.delete_asset(obj.ident)
            for obj in catalog.get_compositions():
                catalog.delete_composition(obj.ident)
            cls.svc_mgr.delete_repository(catalog.ident)
"""

    get_composition_assets = """
        self.assertEqual(self.catalog.get_composition_assets(self.composition.ident).available(), 4)"""

    get_compositions_by_asset = """
        self.assertEqual(self.catalog.get_compositions_by_asset(self.asset_ids[0]).available(), 1)
        self.assertEqual(self.catalog.get_compositions_by_asset(self.asset_ids[0]).next().ident, self.composition.ident)"""

class AssetCompositionDesignSession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.asset_list = list()
        cls.asset_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', 'TEST_SERVICE', PROXY)
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for AssetLookupSession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)
        for num in [0, 3]:
            create_form = cls.catalog.get_asset_form_for_create([])
            create_form.display_name = 'Test Asset ' + str(num)
            create_form.description = 'Test Asset for AssetLookupSession tests'
            obj = cls.catalog.create_asset(create_form)
            cls.asset_list.append(obj)
            cls.asset_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_repositories():
            for obj in catalog.get_compositions():
                catalog.delete_composition(obj.ident)
            for obj in catalog.get_assets():
                catalog.delete_asset(obj.ident)
            cls.svc_mgr.delete_repository(catalog.ident)
"""


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
