from .resource import ResourceLookupSession, ResourceQuerySession


class RepositoryProfile:

    get_coordinate_types_template = """
        assert isinstance(self.mgr.${method_name}(), abc_type_list)"""

    supports_coordinate_type_template = """
        assert isinstance(self.mgr.${method_name}(DEFAULT_TYPE), bool)"""


class AssetAdminSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.${pkg_name_replaced_reserved} import objects as ABCObjects',
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'REPOSITORY',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for AssetAdminSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_repository(create_form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assets():
                request.cls.catalog.delete_asset(obj.ident)
            request.cls.svc_mgr.delete_repository(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        request.cls.form = request.cls.catalog.get_asset_form_for_create([])
        request.cls.form.display_name = 'new Asset'
        request.cls.form.description = 'description of Asset'
        request.cls.form.set_genus_type(NEW_TYPE)
        request.cls.osid_object = request.cls.catalog.create_asset(request.cls.form)
        request.cls.parent_object = request.cls.osid_object
    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.catalog.delete_asset(request.cls.osid_object.ident)

    request.addfinalizer(test_tear_down)"""

    create_asset_content_template = """
        if not is_never_authz(self.service_config):
            results = self.parent_object.get_${aggregated_objects_name_under}()
            assert isinstance(results, ABCObjects.${aggregated_object_name}List)
            assert results.available() == 0

            form = self.catalog.get_${aggregated_object_name_under}_form_for_create(self.parent_object.ident, [])
            result = self.catalog.${method_name}(form)
            assert isinstance(result, ABCObjects.${aggregated_object_name})

            updated_parent = self.catalog.get_${object_name_under}(self.parent_object.ident)
            results = updated_parent.get_${aggregated_objects_name_under}()
            assert results.available() == 1
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}('foo')"""

    get_asset_content_form_for_update_template = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_${aggregated_object_name_under}_form_for_create(self.parent_object.ident, [])
            new_aggregated_object = self.catalog.create_${aggregated_object_name_under}(form)

            form = self.catalog.${method_name}(new_aggregated_object.ident)
            assert isinstance(form, OsidForm)
            assert form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id)"""

    update_asset_content_template = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_${aggregated_object_name_under}_form_for_create(self.parent_object.ident, [])
            form.display_name = 'old name'
            new_aggregated_object = self.catalog.create_${aggregated_object_name_under}(form)

            assert new_aggregated_object.display_name.text == 'old name'

            form = self.catalog.get_${aggregated_object_name_under}_form_for_update(new_aggregated_object.ident)
            form.display_name = 'new name'
            result = self.catalog.${method_name}(form)
            assert isinstance(result, ABCObjects.${aggregated_object_name})
            assert result.display_name.text == 'new name'
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}('foo')"""

    delete_asset_content_template = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_${aggregated_object_name_under}_form_for_create(self.parent_object.ident, [])
            result = self.catalog.create_${aggregated_object_name_under}(form)

            updated_parent = self.catalog.get_${object_name_under}(self.parent_object.ident)
            results = updated_parent.get_${aggregated_objects_name_under}()
            assert results.available() == 1

            self.catalog.${method_name}(result.ident)

            results = self.parent_object.get_${aggregated_objects_name_under}()
            assert results.available() == 0
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id)"""


class AssetLookupSession:
    # Override these locally for Asset because with AssetQuerySession implemented,
    #   the authz adapter will return an empty List instead of throwing PermissionDenied
    get_asset = """
        if not is_never_authz(self.service_config):
            self.catalog.use_isolated_repository_view()
            obj = self.catalog.get_asset(self.asset_list[0].ident)
            assert obj.ident == self.asset_list[0].ident
            self.catalog.use_federated_repository_view()
            obj = self.catalog.get_asset(self.asset_list[0].ident)
            assert obj.ident == self.asset_list[0].ident
        else:
            with pytest.raises(errors.NotFound):
                self.catalog.get_asset(self.fake_id)"""

    get_assets_by_ids = """
        from dlkit.abstract_osid.repository.objects import AssetList
        objects = self.catalog.get_assets_by_ids(self.asset_ids)
        assert isinstance(objects, AssetList)
        self.catalog.use_federated_repository_view()
        objects = self.catalog.get_assets_by_ids(self.asset_ids)
        assert isinstance(objects, AssetList)
        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0"""

    get_assets_by_genus_type = """
        from dlkit.abstract_osid.repository.objects import AssetList
        objects = self.catalog.get_assets_by_genus_type(DEFAULT_GENUS_TYPE)
        assert isinstance(objects, AssetList)
        self.catalog.use_federated_repository_view()
        objects = self.catalog.get_assets_by_genus_type(DEFAULT_GENUS_TYPE)
        assert isinstance(objects, AssetList)
        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0"""

    get_assets_by_parent_genus_type = """
        from dlkit.abstract_osid.repository.objects import AssetList
        if not is_never_authz(self.service_config):
            objects = self.catalog.get_assets_by_parent_genus_type(DEFAULT_GENUS_TYPE)
            assert isinstance(objects, AssetList)
            self.catalog.use_federated_repository_view()
            objects = self.catalog.get_assets_by_parent_genus_type(DEFAULT_GENUS_TYPE)
            assert objects.available() == 0
            assert isinstance(objects, AssetList)
        else:
            with pytest.raises(errors.Unimplemented):
                # because the never_authz "tries harder" and runs the actual query...
                #    whereas above the method itself in JSON returns an empty list
                self.catalog.get_assets_by_parent_genus_type(DEFAULT_GENUS_TYPE)"""

    get_assets_by_record_type = """
        from dlkit.abstract_osid.repository.objects import AssetList
        objects = self.catalog.get_assets_by_record_type(DEFAULT_TYPE)
        assert isinstance(objects, AssetList)
        self.catalog.use_federated_repository_view()
        objects = self.catalog.get_assets_by_record_type(DEFAULT_TYPE)
        assert objects.available() == 0
        assert isinstance(objects, AssetList)"""

    get_assets = """
        from dlkit.abstract_osid.repository.objects import AssetList
        objects = self.catalog.get_assets()
        assert isinstance(objects, AssetList)
        self.catalog.use_federated_repository_view()
        objects = self.catalog.get_assets()
        assert isinstance(objects, AssetList)

        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0

    def test_get_asset_with_alias(self):
        if not is_never_authz(self.service_config):
            self.catalog.alias_asset(self.asset_ids[0], ALIAS_ID)
            obj = self.catalog.get_asset(ALIAS_ID)
            assert obj.get_id() == self.asset_ids[0]"""


class CompositionLookupSession:

    import_statements_pattern = ResourceLookupSession.import_statements_pattern

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/repository.py::CompositionLookupSession::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3A000000000000000000000000%40DLKIT.MIT.EDU')


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/repository.py::CompositionLookupSession::init_template
    request.cls.${object_name_under}_list = list()
    request.cls.${object_name_under}_ids = list()

    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        for num in [0, 1, 2, 3]:
            create_form = request.cls.catalog.get_${object_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            if num > 1:
                create_form.sequestered = True
            obj = request.cls.catalog.create_${object_name_under}(create_form)
            request.cls.${object_name_under}_list.append(obj)
            request.cls.${object_name_under}_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_${cat_name_under_plural}():
                catalog.use_unsequestered_${object_name_under}_view()
                for obj in catalog.get_${object_name_under_plural}():
                    catalog.delete_${object_name_under}(obj.ident)
                request.cls.svc_mgr.delete_${cat_name_under}(catalog.ident)

    request.addfinalizer(test_tear_down)"""

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


class CompositionQuerySession:

    init_template = ResourceQuerySession.init_template

    get_compositions_by_query = """
        if not is_never_authz(self.service_config):
            cfu = self.catalog.get_composition_form_for_update(self.composition_list[3].ident)
            cfu.set_sequestered(True)
            self.catalog.update_composition(cfu)
            query = self.catalog.get_composition_query()
            query.match_display_name('orange')
            assert self.catalog.get_compositions_by_query(query).available() == 1
            query.clear_display_name_terms()
            query.match_display_name('blue', match=False)
            assert self.catalog.get_compositions_by_query(query).available() == 2
            cfu = self.catalog.get_composition_form_for_update(self.composition_list[3].ident)
            cfu.set_sequestered(False)
            self.catalog.update_composition(cfu)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_compositions_by_query(FakeQuery())"""


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
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'REPOSITORY',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for CompositionSearchSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_repository(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_repository(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""


class Composition:
    get_children = """
        with pytest.raises(errors.IllegalState):
            self.object.get_children()"""


class CompositionQuery:
    match_asset_id = """
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_asset_id(test_id, match=True)
        assert self.query._query_terms['assetIds'] == {
            '$in': [str(test_id)]
        }"""

    clear_asset_id_terms = """
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_asset_id(test_id, match=True)
        assert 'assetIds' in self.query._query_terms
        self.query.clear_asset_id_terms()
        assert 'assetIds' not in self.query._query_terms"""

    match_contained_composition_id = """
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_contained_composition_id(test_id, match=True)
        assert self.query._query_terms['childIds'] == {
            '$in': [str(test_id)]
        }"""

    clear_contained_composition_id_terms = """
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_contained_composition_id(test_id, match=True)
        assert 'childIds' in self.query._query_terms
        self.query.clear_contained_composition_id_terms()
        assert 'childIds' not in self.query._query_terms"""

    match_containing_composition_id = """
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_containing_composition_id(test_id, match=True)
        assert self.query._query_terms['_id'] == {
            '$in': [test_id.identifier]
        }"""

    clear_containing_composition_id_terms = """
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_containing_composition_id(test_id, match=True)
        assert '_id' in self.query._query_terms
        self.query.clear_containing_composition_id_terms()
        assert '_id' not in self.query._query_terms"""


class CompositionAdminSession:

    import_statements_pattern = [
    ]

    additional_methods = """
    def test_composition_assignment(self):
        if not is_never_authz(self.service_config):
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
            assert composition.get_children_ids().available() == 3
            assert composition.get_child_ids().available() == 3
            assert composition.get_children().available() == 3"""


class AssetCompositionSession:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.asset_list = list()
    request.cls.asset_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'REPOSITORY',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for AssetLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_repository(create_form)
        create_form = request.cls.catalog.get_composition_form_for_create([])
        create_form.display_name = 'Test Composition for AssetCompositionSession tests'
        create_form.description = 'Test Compposion for AssetCompositionSession tests'
        request.cls.composition = request.cls.catalog.create_composition(create_form)
        for num in [0, 1, 2, 3]:
            create_form = request.cls.catalog.get_asset_form_for_create([])
            create_form.display_name = 'Test Asset ' + str(num)
            create_form.description = 'Test Asset for AssetLookupSession tests'
            obj = request.cls.catalog.create_asset(create_form)
            request.cls.asset_list.append(obj)
            request.cls.asset_ids.append(obj.ident)
            request.cls.catalog.add_asset(obj.ident, request.cls.composition.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_asset_composition_session(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_repositories():
                catalog.use_unsequestered_composition_view()
                for obj in catalog.get_assets():
                    catalog.delete_asset(obj.ident)
                for obj in catalog.get_compositions():
                    catalog.delete_composition(obj.ident)
                request.cls.svc_mgr.delete_repository(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    can_access_asset_compositions_template = """
        # From test_templates/repository.py::AssetCompositionSession::can_access_asset_compositions_template
        assert isinstance(self.session.${method_name}(), bool)"""

    get_composition_assets_template = """
        # From test_templates/repository.py::AssetCompositionSession::get_composition_assets_template
        if not is_never_authz(self.service_config):
            assert self.catalog.${method_name}(self.${containable_object_name_under}.ident).available() == 4
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id)"""

    get_compositions_by_asset_template = """
        # From test_templates/repository.py::AssetCompositionSession::get_compositions_by_asset_template
        if not is_never_authz(self.service_config):
            assert self.catalog.${method_name}(self.${object_name_under}_ids[0]).available() == 1
            assert self.catalog.${method_name}(self.${object_name_under}_ids[0]).next().ident == self.${containable_object_name_under}.ident
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id)"""


class AssetCompositionDesignSession:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.asset_list = list()
    request.cls.asset_ids = list()
    request.cls.composition_list = list()
    request.cls.composition_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'REPOSITORY',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for AssetCompositionDesignSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_repository(create_form)
        for num in [0, 1, 2, 3]:
            create_form = request.cls.catalog.get_asset_form_for_create([])
            create_form.display_name = 'Test Asset ' + str(num)
            create_form.description = 'Test Asset for AssetCompositionDesignSession tests' + str(num)
            asset = request.cls.catalog.create_asset(create_form)
            request.cls.asset_list.append(asset)
            request.cls.asset_ids.append(asset.ident)
        for num in [0, 1, 2, 3, 4]:
            create_form = request.cls.catalog.get_composition_form_for_create([])
            create_form.display_name = 'Test Composition ' + str(num)
            create_form.description = 'Test Compposion for AssetCompositionDesignSession tests ' + str(num)
            composition = request.cls.catalog.create_composition(create_form)
            request.cls.composition_list.append(composition)
            request.cls.composition_ids.append(composition.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_asset_composition_design_session(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_repositories():
                for obj in catalog.get_compositions():
                    catalog.delete_composition(obj.ident)
                for obj in catalog.get_assets():
                    catalog.delete_asset(obj.ident)
                request.cls.svc_mgr.delete_repository(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    add_asset = """
        if not is_never_authz(self.service_config):
            for asset_id in self.asset_ids:
                self.catalog.add_asset(asset_id, self.composition_ids[0])
            assert self.catalog.get_composition_assets(self.composition_ids[0]).available() == 4
            assert self.catalog.get_composition_assets(self.composition_ids[0]).next().display_name.text == 'Test Asset 0'
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.add_asset(self.fake_id, self.fake_id)"""

    move_asset_ahead = """
        if not is_never_authz(self.service_config):
            for asset_id in self.asset_ids:
                self.catalog.add_asset(asset_id, self.composition_ids[1])
            self.catalog.move_asset_ahead(self.asset_ids[2], self.composition_ids[1], self.asset_ids[0])
            first_asset = self.catalog.get_composition_assets(self.composition_ids[1]).next()
            assert first_asset.ident == self.asset_ids[2]
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.move_asset_ahead(self.fake_id, self.fake_id, self.fake_id)"""

    move_asset_behind = """
        if not is_never_authz(self.service_config):
            for asset_id in self.asset_ids:
                self.catalog.add_asset(asset_id, self.composition_ids[2])
            self.catalog.move_asset_behind(self.asset_ids[0], self.composition_ids[2], self.asset_ids[3])
            last_asset = list(self.catalog.get_composition_assets(self.composition_ids[2]))[-1]
            assert last_asset.ident == self.asset_ids[0]
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.move_asset_behind(self.fake_id, self.fake_id, self.fake_id)"""

    order_assets = """
        if not is_never_authz(self.service_config):
            for asset_id in self.asset_ids:
                self.catalog.add_asset(asset_id, self.composition_ids[3])
            new_order = [self.asset_ids[2], self.asset_ids[3], self.asset_ids[1], self.asset_ids[0]]
            self.catalog.order_assets(new_order, self.composition_ids[3])
            asset_list = list(self.catalog.get_composition_assets(self.composition_ids[3]))
            for num in [0, 1, 2, 3]:
                assert new_order[num] == asset_list[num].ident
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.order_assets([self.fake_id], self.fake_id)"""

    remove_asset = """
        if not is_never_authz(self.service_config):
            for asset_id in self.asset_ids:
                self.catalog.add_asset(asset_id, self.composition_ids[4])
            self.catalog.remove_asset(self.asset_ids[1], self.composition_ids[4])
            assert self.catalog.get_composition_assets(self.composition_ids[4]).available() == 3
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.remove_asset(self.fake_id, self.fake_id)"""

    can_compose_assets_template = """
        # From test_templates/repository.py::AssetCompositionDesignSession::can_compose_assets_template
        assert isinstance(self.session.${method_name}(), bool)"""


class Asset:

    import_statements_pattern = [
        'from dlkit.json_.id.objects import IdList',
        'from dlkit.abstract_osid.${pkg_name_replaced_reserved} import objects as ABCObjects',
        'from dlkit.primordium.locale.primitives import DisplayText'
    ]

    can_distribute_alterations = """
        with pytest.raises(errors.IllegalState):
            self.object.can_distribute_alterations()"""

    can_distribute_compositions = """
        with pytest.raises(errors.IllegalState):
            self.object.can_distribute_compositions()"""

    can_distribute_verbatim = """
        with pytest.raises(errors.IllegalState):
            self.object.can_distribute_verbatim()"""

    get_asset_content_ids_template = """
        results = self.object.${method_name}()
        assert isinstance(results, IdList)"""

    get_asset_contents_template = """
        results = self.object.${method_name}()
        assert isinstance(results, ABCObjects.${return_type})"""

    get_composition = """
        with pytest.raises(errors.IllegalState):
            self.object.get_composition()"""

    get_composition_id = """
        with pytest.raises(errors.IllegalState):
            self.object.get_composition_id()"""

    get_title_template = """
        # From test_templates/repository.py::Asset::get_title_template
        result = self.object.${method_name}()
        assert isinstance(result, DisplayText)
        assert result.text == ''"""

    is_composition = """
        result = self.object.is_composition()
        assert isinstance(result, bool)"""

    get_provider_links = """
        # Override because no providerLinkIds
        with pytest.raises(errors.IllegalState):
            self.object.get_provider_links()"""


class AssetForm:

    set_title_template = """
        # From test_templates/repository.py::AssetForm::set_title_template
        default_value = self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0]
        assert self.form._my_map['${var_name_mixed}'] == default_value
        self.form.set_${var_name}('String')
        assert self.form._my_map['${var_name_mixed}']['text'] == 'String'
        with pytest.raises(errors.InvalidArgument):
            self.form.${method_name}(42)"""

    clear_title_template = """
        # From test_templates/repository.py::AssetForm::clear_title_template
        self.form.set_${var_name}('A String to Clear')
        assert self.form._my_map['${var_name_mixed}']['text'] == 'A String to Clear'
        self.form.${method_name}()
        assert self.form._my_map['${var_name_mixed}'] == self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0]"""


class AssetQuery:
    import_statements = [
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.primordium.calendaring.primitives import DateTime',
        'from dlkit.primordium.locale.types.string import get_type_data as get_string_type_data',
        'DEFAULT_STRING_MATCH_TYPE = Type(**get_string_type_data("WORDIGNORECASE"))'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'REPOSITORY',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_repository(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_repository(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.query = request.cls.catalog.get_asset_query()
    request.cls.start_date = DateTime.utcnow()
    request.cls.end_date = DateTime.utcnow()"""

    match_created_date = """
        if is_no_authz(self.service_config):
            assert 'createdDate' not in self.query._query_terms
        self.query.match_created_date(self.start_date, self.end_date, True)
        if is_no_authz(self.service_config):
            assert self.query._query_terms['createdDate'] == {
                '$gte': self.start_date,
                '$lte': self.end_date
            }"""

    match_published_date = """
        if is_no_authz(self.service_config):
            assert 'publishedDate' not in self.query._query_terms
        self.query.match_published_date(self.start_date, self.end_date, True)
        if is_no_authz(self.service_config):
            assert self.query._query_terms['publishedDate'] == {
                '$gte': self.start_date,
                '$lte': self.end_date
            }"""


class AssetSearchSession:
    import_statements = [
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.abstract_osid.repository import searches',
        'from dlkit.primordium.locale.types.string import get_type_data as get_string_type_data',
        'DEFAULT_STRING_MATCH_TYPE = Type(**get_string_type_data("WORDIGNORECASE"))'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'REPOSITORY',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_repository(create_form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_asset_search_session(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_repository(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    get_asset_search = """
        if not is_never_authz(self.service_config):
            search = self.session.get_asset_search()
            assert isinstance(search, searches.AssetSearch)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_asset_search()"""

    get_assets_by_search = """
        if not is_never_authz(self.service_config):
            query = self.session.get_asset_query()
            query.match_display_name('zxy', DEFAULT_STRING_MATCH_TYPE, True)
            search = self.session.get_asset_search()
            results = self.session.get_assets_by_search(query, search)
            assert isinstance(results, searches.AssetSearchResults)
            assert results.get_result_size() == 0
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_assets_by_search(FakeQuery(), 'foo')"""


class AssetNotificationSession:
    register_for_new_assets_by_genus_type = """
        if not is_never_authz(self.service_config):
            self.session.register_for_new_assets_by_genus_type(Id('package.Catalog%3Afake%40DLKIT.MIT.EDU'))
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.register_for_new_assets_by_genus_type(Id('package.Catalog%3Afake%40DLKIT.MIT.EDU'))"""


class AssetContent:

    import_statements = [
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'REPOSITORY',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_repository(create_form)

        form = request.cls.catalog.get_asset_form_for_create([])
        form.display_name = 'Asset'
        request.cls.asset = request.cls.catalog.create_asset(form)

        form = request.cls.catalog.get_asset_content_form_for_create(request.cls.asset.ident,
                                                                     [])
        form.display_name = 'Test asset content'
        form.set_url('https://www.google.com')
        request.cls.object = request.cls.catalog.create_asset_content(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assets():
                request.cls.catalog.delete_asset(obj.ident)
            request.cls.svc_mgr.delete_repository(request.cls.catalog.ident)
        request.cls.object = None
        request.cls.catalog = None

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""

    has_url_template = """
        # From test_templates/repository.py::AssetContent::has_url_template
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.${method_name}(), bool)"""

    get_url_template = """
        # From test_templates/repository.py::AssetContent::get_url_template
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.IllegalState):
                self.object.${method_name}()"""

    get_url = """
        if not is_never_authz(self.service_config):
            result = self.object.get_url()
            assert result == 'https://www.google.com'"""

    get_data = """
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.IllegalState):
                self.object.get_data()"""


class AssetContentForm:

    import_statements = [
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'REPOSITORY',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_repository(create_form)

        form = request.cls.catalog.get_asset_form_for_create([])
        form.display_name = 'Asset'
        request.cls.asset = request.cls.catalog.create_asset(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assets():
                request.cls.catalog.delete_asset(obj.ident)
            request.cls.svc_mgr.delete_repository(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        request.cls.form = request.cls.catalog.get_asset_content_form_for_create(request.cls.asset.ident,
                                                                                 [])
    request.cls.object = request.cls.form"""

    set_url_template = """
        # From test_templates/repository.py::AssetContentForm::set_url_template
        default_value = self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0]
        assert self.form._my_map['${var_name_mixed}'] == default_value
        self.form.set_${var_name}('String')
        assert self.form._my_map['${var_name_mixed}'] == 'String'
        with pytest.raises(errors.InvalidArgument):
            self.form.${method_name}(42)"""

    clear_url_template = """
        # From test_templates/repository.py::AssetContentForm::clear_url_template
        self.form.set_${var_name}('A String to Clear')
        assert self.form._my_map['${var_name_mixed}'] == 'A String to Clear'
        self.form.${method_name}()
        assert self.form._my_map['${var_name_mixed}'] == self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0]"""

    set_data = """
        with pytest.raises(errors.InvalidArgument):
            self.form.set_data('foo')
        # TODO: should test setting actual data..."""

    clear_data = """
        self.form.clear_data()"""


class AssetContentList:

    import_statements = [
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'REPOSITORY',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_repository(create_form)

        form = request.cls.catalog.get_asset_form_for_create([])
        form.display_name = 'Asset'
        request.cls.asset = request.cls.catalog.create_asset(form)

        request.cls.form = request.cls.catalog.get_asset_content_form_for_create(request.cls.asset.ident,
                                                                                 [])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assets():
                request.cls.catalog.delete_asset(obj.ident)
            request.cls.svc_mgr.delete_repository(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    from dlkit.json_.repository.objects import AssetContentList
    request.cls.asset_content_list = list()
    request.cls.asset_content_ids = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            form = request.cls.catalog.get_asset_content_form_for_create(request.cls.asset.ident,
                                                                         [])
            form.display_name = 'Test AssetContent ' + str(num)
            form.description = 'Test AssetContent for AssetContentList tests'
            obj = request.cls.catalog.create_asset_content(form)

            request.cls.asset_content_list.append(obj)
            request.cls.asset_content_ids.append(obj.ident)
    request.cls.asset_content_list = AssetContentList(request.cls.asset_content_list)"""
