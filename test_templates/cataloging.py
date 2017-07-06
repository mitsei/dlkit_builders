class CatalogAssignmentSession:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def catalog_assignment_session_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.catalogs = list()
    request.cls.catalog_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'CATALOGING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')


@pytest.fixture(scope="function")
def catalog_assignment_session_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_catalog_form_for_create([])
        create_form.display_name = 'Test Catalog'
        create_form.description = 'Test Catalog for CatalogAssignmentSession tests'
        request.cls.assigned_catalog = request.cls.svc_mgr.create_catalog(create_form)
        for num in [0, 1]:
            create_form = request.cls.svc_mgr.get_catalog_form_for_create([])
            create_form.display_name = 'Test Catalog ' + str(num)
            create_form.description = 'Test Catalog for CatalogAssignmentSession tests'
            catalog = request.cls.svc_mgr.create_catalog(create_form)
            request.cls.catalogs.append(catalog)
            request.cls.catalog_ids.append(catalog.ident)

    request.cls.session = request.cls.svc_mgr

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_catalogs():
                request.cls.svc_mgr.delete_catalog(catalog.ident)

    request.addfinalizer(test_tear_down)"""

    assign_id_to_catalog = """
        if not is_never_authz(self.service_config):
            results = self.svc_mgr.get_catalogs_by_id(self.fake_id)
            assert results.available() == 0
            self.session.assign_id_to_catalog(self.fake_id, self.assigned_catalog.ident)
            results = self.assigned_catalog.get_catalogs_by_id(self.fake_id)
            assert results.available() == 1
            self.session.assign_id_to_catalog(self.fake_id, self.catalog_ids[0])
            results = self.assigned_catalog.get_catalogs_by_id(self.fake_id)
            assert results.available() == 2
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.assign_id_to_catalog(self.fake_id, self.fake_id)"""

    unassign_id_from_catalog = """
        if not is_never_authz(self.service_config):
            self.session.assign_id_to_catalog(self.fake_id, self.assigned_catalog.ident)
            results = self.assigned_catalog.get_catalogs_by_id(self.fake_id)
            assert results.available() == 1
            self.session.unassign_id_from_catalog(self.fake_id, self.assigned_catalog.ident)
            results = self.assigned_catalog.get_catalogs_by_id(self.fake_id)
            assert results.available() == 0
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.assign_id_to_catalog(self.fake_id, self.fake_id)"""


class CatalogSession:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def catalog_session_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'CATALOGING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_catalog_form_for_create([])
        create_form.display_name = 'Test Catalog'
        create_form.description = 'Test Catalog for CatalogSession tests'
        request.cls.assigned_catalog = request.cls.svc_mgr.create_catalog(create_form)

        request.cls.id_ids = [request.cls.assigned_catalog.ident, request.cls.assigned_catalog.ident]
    request.cls.catalog = request.cls.svc_mgr

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_catalogs():
                request.cls.svc_mgr.delete_catalog(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def catalog_session_test_fixture(request):
    request.cls.session = request.cls.svc_mgr"""


class CatalogAdminSession:
    delete_catalog = """
        if not is_never_authz(self.service_config):
            cat_id = self.catalog_to_delete.ident
            self.svc_mgr.delete_catalog(cat_id)
            with pytest.raises(errors.NotFound):
                self.svc_mgr.get_catalog(cat_id)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.svc_mgr.delete_catalog(self.fake_id)"""
