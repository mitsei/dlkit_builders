from .resource import ResourceLookupSession, ResourceQuerySession


class RepositoryProfile:

    get_coordinate_types_template = """
        self.assertTrue(isinstance(self.mgr.${method_name}(), abc_type_list))"""

    supports_coordinate_type_template = """
        self.assertTrue(isinstance(self.mgr.${method_name}(DEFAULT_TYPE), bool))"""


class AssetAdminSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.${pkg_name_replaced_reserved} import objects as ABCObjects',
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for AssetAdminSession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)

    def setUp(self):
        form = self.catalog.get_asset_form_for_create([])
        form.display_name = 'new Asset'
        form.description = 'description of Asset'
        form.set_genus_type(NEW_TYPE)
        self.osid_object = self.catalog.create_asset(form)
        self.parent_object = self.osid_object
        self.session = self.catalog

    def tearDown(self):
        self.catalog.delete_asset(self.osid_object.ident)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assets():
            cls.catalog.delete_asset(obj.ident)
        cls.svc_mgr.delete_repository(cls.catalog.ident)"""

    create_asset_content_template = """
        results = self.parent_object.get_${aggregated_objects_name_under}()
        self.assertTrue(isinstance(results, ABCObjects.${aggregated_object_name}List))
        self.assertEqual(results.available(), 0)

        form = self.catalog.get_${aggregated_object_name_under}_form_for_create(self.parent_object.ident, [])
        result = self.catalog.${method_name}(form)
        self.assertTrue(isinstance(result, ABCObjects.${aggregated_object_name}))

        updated_parent = self.catalog.get_${object_name_under}(self.parent_object.ident)
        results = updated_parent.get_${aggregated_objects_name_under}()
        self.assertEqual(results.available(), 1)"""

    get_asset_content_form_for_update_template = """
        form = self.catalog.get_${aggregated_object_name_under}_form_for_create(self.parent_object.ident, [])
        new_aggregated_object = self.catalog.create_${aggregated_object_name_under}(form)

        form = self.catalog.${method_name}(new_aggregated_object.ident)
        self.assertTrue(isinstance(form, OsidForm))
        self.assertTrue(form.is_for_update())"""

    update_asset_content_template = """
        form = self.catalog.get_${aggregated_object_name_under}_form_for_create(self.parent_object.ident, [])
        form.display_name = 'old name'
        new_aggregated_object = self.catalog.create_${aggregated_object_name_under}(form)

        self.assertEqual(new_aggregated_object.display_name.text, 'old name')

        form = self.catalog.get_${aggregated_object_name_under}_form_for_update(new_aggregated_object.ident)
        form.display_name = 'new name'
        result = self.catalog.${method_name}(form)
        self.assertTrue(isinstance(result, ABCObjects.${aggregated_object_name}))
        self.assertEqual(result.display_name.text, 'new name')"""

    delete_asset_content_template = """
        form = self.catalog.get_${aggregated_object_name_under}_form_for_create(self.parent_object.ident, [])
        result = self.catalog.create_${aggregated_object_name_under}(form)

        updated_parent = self.catalog.get_${object_name_under}(self.parent_object.ident)
        results = updated_parent.get_${aggregated_objects_name_under}()
        self.assertEqual(results.available(), 1)

        self.catalog.${method_name}(result.ident)

        results = self.parent_object.get_${aggregated_objects_name_under}()
        self.assertEqual(results.available(), 0)"""


class CompositionLookupSession:

    import_statements_pattern = ResourceLookupSession.import_statements_pattern

    init_template = """
    @classmethod
    def setUpClass(cls):
        # From test_templates/repository.py::CompositionLookupSession::init_template
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

    def setUp(self):
        # From test_templates/repository.py::CompositionLookupSession::init_template
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        # From test_templates/repository.py::CompositionLookupSession::init_template
        for catalog in cls.svc_mgr.get_${cat_name_under_plural}():
            catalog.use_unsequestered_${object_name_under}_view()
            for obj in catalog.get_${object_name_under_plural}():
                catalog.delete_${object_name_under}(obj.ident)
            cls.svc_mgr.delete_${cat_name_under}(catalog.ident)"""

    use_active_composition_view_template = """
        # From test_templates/repository.py::CompositionLookupSession::use_active_composition_view_template
        # Ideally also verify the value is set...
        self.catalog.${method_name}()"""

    use_any_status_composition_view_template = """
        # From test_templates/repository.py::CompositionLookupSession::use_any_status_composition_view_template
        # Ideally also verify the value is set...
        self.catalog.${method_name}()"""

    use_sequestered_composition_view_template = """
        # From test_templates/repository.py::CompositionLookupSession::use_sequestered_composition_view
        # Ideally also verify the value is set...
        self.catalog.${method_name}()"""

    use_unsequestered_composition_view_template = """
        # From test_templates/repository.py::CompositionLookupSession::use_unsequestered_composition_view
        # Ideally also verify the value is set...
        self.catalog.${method_name}()"""

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
            obj = self.catalog.get_composition(self.composition_list[3].ident)"""

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


class CompositionSearchSession:

    import_statements = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for CompositionSearchSession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)

    def setUp(self):
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_repository(cls.catalog.ident)"""


class Composition:
    get_children = """
        with self.assertRaises(errors.IllegalState):
            self.object.get_children()"""


class CompositionQuery:
    match_asset_id = """
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_asset_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['assetIds'], {
            '$in': [str(test_id)]
        })"""

    clear_asset_id_terms = """
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_asset_id(test_id, match=True)
        self.assertIn('assetIds',
                      self.query._query_terms)
        self.query.clear_asset_id_terms()
        self.assertNotIn('assetIds',
                         self.query._query_terms)"""

    match_contained_composition_id = """
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_contained_composition_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['childIds'], {
            '$in': [str(test_id)]
        })"""

    clear_contained_composition_id_terms = """
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_contained_composition_id(test_id, match=True)
        self.assertIn('childIds',
                      self.query._query_terms)
        self.query.clear_contained_composition_id_terms()
        self.assertNotIn('childIds',
                         self.query._query_terms)"""

    match_containing_composition_id = """
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_containing_composition_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['_id'], {
            '$in': [test_id.identifier]
        })"""

    clear_containing_composition_id_terms = """
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_containing_composition_id(test_id, match=True)
        self.assertIn('_id',
                      self.query._query_terms)
        self.query.clear_containing_composition_id_terms()
        self.assertNotIn('_id',
                         self.query._query_terms)"""


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

    def setUp(self):
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_repositories():
            for obj in catalog.get_assets():
                catalog.delete_asset(obj.ident)
            for obj in catalog.get_compositions():
                catalog.delete_composition(obj.ident)
            cls.svc_mgr.delete_repository(catalog.ident)"""

    can_access_asset_compositions_template = """
        # From test_templates/repository.py::AssetCompositionSession::can_access_asset_compositions_template
        self.assertTrue(isinstance(self.session.${method_name}(), bool))"""

    get_composition_assets_template = """
        # From test_templates/repository.py::AssetCompositionSession::get_composition_assets_template
        self.assertEqual(self.catalog.get_${containable_object_name_under}_${object_name_plural_under}(self.${containable_object_name_under}.ident).available(), 4)"""

    get_compositions_by_asset_template = """
        # From test_templates/repository.py::AssetCompositionSession::get_compositions_by_asset_template
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

    def setUp(self):
        self.session = self.catalog

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

    can_compose_assets_template = """
        # From test_templates/repository.py::AssetCompositionDesignSession::can_compose_assets_template
        self.assertTrue(isinstance(self.session.${method_name}(), bool))"""


class Asset:

    import_statements_pattern = [
        'from dlkit.json_.id.objects import IdList',
        'from dlkit.abstract_osid.${pkg_name_replaced_reserved} import objects as ABCObjects',
        'from dlkit.primordium.locale.primitives import DisplayText'
    ]

    can_distribute_alterations = """
        with self.assertRaises(errors.IllegalState):
            self.object.can_distribute_alterations()"""

    can_distribute_compositions = """
        with self.assertRaises(errors.IllegalState):
            self.object.can_distribute_compositions()"""

    can_distribute_verbatim = """
        with self.assertRaises(errors.IllegalState):
            self.object.can_distribute_verbatim()"""

    get_asset_content_ids_template = """
        results = self.object.${method_name}()
        self.assertTrue(isinstance(results, IdList))"""

    get_asset_contents_template = """
        results = self.object.${method_name}()
        self.assertTrue(isinstance(results, ABCObjects.${return_type}))"""

    get_composition = """
        with self.assertRaises(errors.IllegalState):
            self.object.get_composition()"""

    get_composition_id = """
        with self.assertRaises(errors.IllegalState):
            self.object.get_composition_id()"""

    get_title_template = """
        # From test_templates/repository.py::Asset::get_title_template
        result = self.object.${method_name}()
        self.assertTrue(isinstance(result, DisplayText))
        self.assertEqual(result.text, '')"""

    is_composition = """
        result = self.object.is_composition()
        self.assertTrue(isinstance(result, bool))"""

    get_provider_links = """
        # Override because no providerLinkIds
        with self.assertRaises(errors.IllegalState):
            self.object.get_provider_links()"""


class AssetForm:

    set_title_template = """
        # From test_templates/repository.py::AssetForm::set_title_template
        default_value = self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0]
        self.assertEqual(self.form._my_map['${var_name_mixed}'], default_value)
        self.form.set_${var_name}('String')
        self.assertEqual(self.form._my_map['${var_name_mixed}']['text'], 'String')
        with self.assertRaises(errors.InvalidArgument):
            self.form.${method_name}(42)"""

    clear_title_template = """
        # From test_templates/repository.py::AssetForm::clear_title_template
        self.form.set_${var_name}('A String to Clear')
        self.assertEqual(self.form._my_map['${var_name_mixed}']['text'], 'A String to Clear')
        self.form.${method_name}()
        self.assertEqual(self.form._my_map['${var_name_mixed}'], self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0])"""


class AssetQuery:
    import_statements = [
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.primordium.calendaring.primitives import DateTime',
        'from dlkit.primordium.locale.types.string import get_type_data as get_string_type_data',
        'DEFAULT_STRING_MATCH_TYPE = Type(**get_string_type_data("WORDIGNORECASE"))'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_repository(create_form)

    def setUp(self):
        self.query = self.catalog.get_asset_query()
        self.start_date = DateTime.utcnow()
        self.end_date = DateTime.utcnow()

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_repository(cls.catalog.ident)"""

    match_created_date = """
        self.assertNotIn('createdDate', self.query._query_terms)
        self.query.match_created_date(self.start_date, self.end_date, True)
        self.assertEqual(self.query._query_terms['createdDate'], {
            '$gte': self.start_date,
            '$lte': self.end_date
        })"""

    match_published_date = """
        self.assertNotIn('publishedDate', self.query._query_terms)
        self.query.match_published_date(self.start_date, self.end_date, True)
        self.assertEqual(self.query._query_terms['publishedDate'], {
            '$gte': self.start_date,
            '$lte': self.end_date
        })"""


class AssetSearchSession:
    import_statements = [
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.abstract_osid.repository import searches',
        'from dlkit.primordium.locale.types.string import get_type_data as get_string_type_data',
        'DEFAULT_STRING_MATCH_TYPE = Type(**get_string_type_data("WORDIGNORECASE"))'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_repository(create_form)

    def setUp(self):
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_repository(cls.catalog.ident)"""

    get_asset_search = """
        search = self.session.get_asset_search()
        self.assertTrue(isinstance(search, searches.AssetSearch))"""

    get_assets_by_search = """
        query = self.session.get_asset_query()
        query.match_display_name('zxy', DEFAULT_STRING_MATCH_TYPE, True)
        search = self.session.get_asset_search()
        results = self.session.get_assets_by_search(query, search)
        self.assertTrue(isinstance(results, searches.AssetSearchResults))
        self.assertEqual(results.get_result_size(), 0)"""


class AssetNotificationSession:
    register_for_new_assets_by_genus_type = """
        self.session.register_for_new_assets_by_genus_type(Id('package.Catalog%3Afake%40DLKIT.MIT.EDU'))"""


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
        form.set_url('https://www.google.com')
        cls.object = cls.catalog.create_asset_content(form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assets():
            cls.catalog.delete_asset(obj.ident)
        cls.svc_mgr.delete_repository(cls.catalog.ident)"""

    has_url_template = """
        # From test_templates/repository.py::AssetContent::has_url_template
        self.assertTrue(isinstance(self.object.${method_name}(), bool))"""

    get_url_template = """
        # From test_templates/repository.py::AssetContent::get_url_template
        with self.assertRaises(errors.IllegalState):
            self.object.${method_name}()"""

    get_url = """
        result = self.object.get_url()
        self.assertEqual(result, 'https://www.google.com')"""

    get_data = """
        with self.assertRaises(errors.IllegalState):
            self.object.get_data()"""


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

    def setUp(self):
        self.form = self.catalog.get_asset_content_form_for_create(self.asset.ident,
                                                                   [])
        self.object = self.form

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_assets():
            cls.catalog.delete_asset(obj.ident)
        cls.svc_mgr.delete_repository(cls.catalog.ident)"""

    set_url_template = """
        # From test_templates/repository.py::AssetContentForm::set_url_template
        default_value = self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0]
        self.assertEqual(self.form._my_map['${var_name_mixed}'], default_value)
        self.form.set_${var_name}('String')
        self.assertEqual(self.form._my_map['${var_name_mixed}'], 'String')
        with self.assertRaises(errors.InvalidArgument):
            self.form.${method_name}(42)"""

    clear_url_template = """
        # From test_templates/repository.py::AssetContentForm::clear_url_template
        self.form.set_${var_name}('A String to Clear')
        self.assertEqual(self.form._my_map['${var_name_mixed}'], 'A String to Clear')
        self.form.${method_name}()
        self.assertEqual(self.form._my_map['${var_name_mixed}'], self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0])"""

    set_data = """
        with self.assertRaises(errors.InvalidArgument):
            self.form.set_data('foo')
        # TODO: should test setting actual data..."""

    clear_data = """
        self.form.clear_data()"""


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
