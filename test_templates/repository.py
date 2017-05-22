from .resource import ResourceLookupSession, ResourceQuerySession


class RepositoryProfile:

    get_coordinate_types_template = """
        self.assertTrue(isinstance(self.mgr.${method_name}(), abc_type_list))"""

    supports_coordinate_type_template = """
        self.assertTrue(isinstance(self.mgr.${method_name}(DEFAULT_TYPE), bool))"""


class AssetAdminSession:

    import_statements_pattern = [
    ]

    create_asset_content_template = """"""

    get_asset_content_form_for_update_template = """"""

    update_asset_content_template = """"""

    delete_asset_content_template = """"""


class CompositionLookupSession:

    import_statements_pattern = ResourceLookupSession.import_statements_pattern

    init_template = """
    @classmethod
    def setUpClass(cls):
        cls.${object_name_under}_list = list()
        cls.${object_name_under}_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
        for num in [0, 1, 2, 3]:
            create_form = cls.catalog.get_${object_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            if num > 1:
                create_form.sequestered = True
            obj = cls.catalog.create_${object_name_under}(create_form)
            cls.${object_name_under}_list.append(obj)
            cls.${object_name_under}_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_${cat_name_under_plural}():
            catalog.use_unsequestered_${object_name_under}_view()
            for obj in catalog.get_${object_name_under_plural}():
                catalog.delete_${object_name_under}(obj.ident)
            cls.svc_mgr.delete_${cat_name_under}(catalog.ident)"""

    use_active_composition_view = """
        self.catalog.use_active_composition_view()"""

    use_any_status_composition_view = """
        self.catalog.use_any_status_composition_view()"""

    use_sequestered_composition_view = """
        self.catalog.use_sequestered_composition_view()"""

    use_unsequestered_composition_view = """
        self.catalog.use_unsequestered_composition_view()"""

    get_composition = """
        self.catalog.use_isolated_repository_view()
        obj = self.catalog.get_composition(self.composition_list[0].ident)
        self.assertEqual(obj.ident, self.composition_list[0].ident)
        self.catalog.use_federated_repository_view()
        obj = self.catalog.get_composition(self.composition_list[0].ident)
        self.assertEqual(obj.ident, self.composition_list[0].ident)
        self.catalog.use_sequestered_composition_view()
        obj = self.catalog.get_composition(self.composition_list[1].ident)
        with self.assertRaises(errors.NotFound):
            obj = self.catalog.get_composition(self.composition_list[3].ident)
"""

    get_compositions = """
        from dlkit.abstract_osid.repository.objects import CompositionList
        objects = self.catalog.get_compositions()
        self.assertTrue(isinstance(objects, CompositionList))
        self.catalog.use_federated_repository_view()
        self.catalog.use_unsequestered_composition_view()
        self.assertEqual(self.catalog.get_compositions().available(), 4)
        self.catalog.use_sequestered_composition_view()
        self.assertEqual(self.catalog.get_compositions().available(), 2)"""


class CompositionQuerySession:

    init_template = ResourceQuerySession.init_template

    get_compositions_by_query = """
        cfu = self.catalog.get_composition_form_for_update(self.composition_list[3].ident)
        cfu.set_sequestered(True)
        self.catalog.update_composition(cfu)
        query = self.catalog.get_composition_query()
        query.match_display_name('orange')
        self.assertEqual(self.catalog.get_compositions_by_query(query).available(), 1)
        query.clear_display_name_terms()
        query.match_display_name('blue', match=False)
        self.assertEqual(self.catalog.get_compositions_by_query(query).available(), 2)
        cfu = self.catalog.get_composition_form_for_update(self.composition_list[3].ident)
        cfu.set_sequestered(False)
        self.catalog.update_composition(cfu)"""


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
        self.assertEqual(composition.get_children().available(), 3)"""


class AssetCompositionSession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.asset_list = list()
        cls.asset_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
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
            cls.svc_mgr.delete_repository(catalog.ident)"""

    get_composition_assets_template = """
        self.assertEqual(self.catalog.get_${containable_object_name_under}_${object_name_plural_under}(self.${containable_object_name_under}.ident).available(), 4)"""

    get_compositions_by_asset_template = """
        self.assertEqual(self.catalog.get_${containable_object_name_plural_under}_by_${object_name_under}(self.${object_name_under}_ids[0]).available(), 1)
        self.assertEqual(self.catalog.get_${containable_object_name_plural_under}_by_${object_name_under}(self.${object_name_under}_ids[0]).next().ident, self.${containable_object_name_under}.ident)"""


class AssetCompositionDesignSession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.asset_list = list()
        cls.asset_ids = list()
        cls.composition_list = list()
        cls.composition_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for AssetLookupSession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)
        for num in [0, 1, 2, 3]:
            create_form = cls.catalog.get_asset_form_for_create([])
            create_form.display_name = 'Test Asset ' + str(num)
            create_form.description = 'Test Asset for AssetLookupSession tests' + str(num)
            asset = cls.catalog.create_asset(create_form)
            cls.asset_list.append(asset)
            cls.asset_ids.append(asset.ident)
        for num in [0, 1, 2, 3, 4]:
            create_form = cls.catalog.get_composition_form_for_create([])
            create_form.display_name = 'Test Composition ' + str(num)
            create_form.description = 'Test Compposion for AssetCompositionSession tests ' + str(num)
            composition = cls.catalog.create_composition(create_form)
            cls.composition_list.append(composition)
            cls.composition_ids.append(composition.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_repositories():
            for obj in catalog.get_compositions():
                catalog.delete_composition(obj.ident)
            for obj in catalog.get_assets():
                catalog.delete_asset(obj.ident)
            cls.svc_mgr.delete_repository(catalog.ident)"""

    add_asset = """
        for asset_id in self.asset_ids:
            self.catalog.add_asset(asset_id, self.composition_ids[0])
        self.assertEqual(self.catalog.get_composition_assets(self.composition_ids[0]).available(), 4)
        self.assertEqual(self.catalog.get_composition_assets(self.composition_ids[0]).next().display_name.text, 'Test Asset 0')"""

    move_asset_ahead = """
        for asset_id in self.asset_ids:
            self.catalog.add_asset(asset_id, self.composition_ids[1])
        self.catalog.move_asset_ahead(self.asset_ids[2], self.composition_ids[1], self.asset_ids[0])
        first_asset = self.catalog.get_composition_assets(self.composition_ids[1]).next()
        self.assertEqual(first_asset.ident, self.asset_ids[2])"""

    move_asset_behind = """
        for asset_id in self.asset_ids:
            self.catalog.add_asset(asset_id, self.composition_ids[2])
        self.catalog.move_asset_behind(self.asset_ids[0], self.composition_ids[2], self.asset_ids[3])
        last_asset = list(self.catalog.get_composition_assets(self.composition_ids[2]))[-1]
        self.assertEqual(last_asset.ident, self.asset_ids[0])"""

    order_assets = """
        for asset_id in self.asset_ids:
            self.catalog.add_asset(asset_id, self.composition_ids[3])
        new_order = [self.asset_ids[2], self.asset_ids[3], self.asset_ids[1], self.asset_ids[0]]
        self.catalog.order_assets(new_order, self.composition_ids[3])
        asset_list = list(self.catalog.get_composition_assets(self.composition_ids[3]))
        for num in [0, 1, 2, 3]:
            self.assertEqual(new_order[num], asset_list[num].ident)"""

    remove_asset = """
        for asset_id in self.asset_ids:
            self.catalog.add_asset(asset_id, self.composition_ids[4])
        self.catalog.remove_asset(self.asset_ids[1], self.composition_ids[4])
        self.assertEqual(self.catalog.get_composition_assets(self.composition_ids[4]).available(), 3)"""


class Asset:

    import_statements = [
    ]

    get_title_template = """"""

    can_distribute_verbatim_template = """"""

    get_asset_content_ids_template = """"""

    get_asset_contents_template = """"""


class AssetForm:

    set_title_template = """"""

    clear_title_template = """"""


class AssetContent:

    import_statements = [
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_repository(create_form)

        form = cls.catalog.get_asset_form_for_create([])
        form.display_name = 'Asset'
        cls.asset = cls.catalog.create_asset(form)

        form = cls.catalog.get_asset_content_form_for_create(cls.asset.ident,
                                                             [])
        form.display_name = 'Test asset content'
        cls.object = cls.catalog.create_asset_content(form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assets():
            cls.catalog.delete_asset(obj.ident)
        cls.svc_mgr.delete_repository(cls.catalog.ident)"""

    has_url_template = """"""

    get_url_template = """"""

    get_data = """"""


class AssetContentForm:

    import_statements = [
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_repository(create_form)

        form = cls.catalog.get_asset_form_for_create([])
        form.display_name = 'Asset'
        cls.asset = cls.catalog.create_asset(form)

        cls.form = cls.catalog.get_asset_content_form_for_create(cls.asset.ident,
                                                                 [])

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assets():
            cls.catalog.delete_asset(obj.ident)
        cls.svc_mgr.delete_repository(cls.catalog.ident)"""

    set_url_template = """"""

    set_data = """"""

    clear_data = """"""


class AssetContentList:

    import_statements = [
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_repository(create_form)

        form = cls.catalog.get_asset_form_for_create([])
        form.display_name = 'Asset'
        cls.asset = cls.catalog.create_asset(form)

        cls.form = cls.catalog.get_asset_content_form_for_create(cls.asset.ident,
                                                                 [])

    def setUp(self):
        from dlkit.json_.repository.objects import AssetContentList
        self.asset_content_list = list()
        self.asset_content_ids = list()
        for num in [0, 1]:
            form = self.catalog.get_asset_content_form_for_create(self.asset.ident,
                                                                  [])
            form.display_name = 'Test AssetContent ' + str(num)
            form.description = 'Test AssetContent for AssetContentList tests'
            obj = self.catalog.create_asset_content(form)

            self.asset_content_list.append(obj)
            self.asset_content_ids.append(obj.ident)
        self.asset_content_list = AssetContentList(self.asset_content_list)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assets():
            cls.catalog.delete_asset(obj.ident)
        cls.svc_mgr.delete_repository(cls.catalog.ident)"""
