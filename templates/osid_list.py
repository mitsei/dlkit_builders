class GenericObjectList(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
            ]
        }
    }

    init_template = {
        'python': {
            'tests': """
${pattern_name}
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_${object_name_under_plural}():
                request.cls.catalog.delete_${object_name_under}(obj.ident)
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    from dlkit.json_.${pkg_name_replaced_reserved}.objects import ${interface_name}
    request.cls.${object_name_under}_list = list()
    request.cls.${object_name_under}_ids = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            create_form = request.cls.catalog.get_${object_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            obj = request.cls.catalog.create_${object_name_under}(create_form)
            request.cls.${object_name_under}_list.append(obj)
            request.cls.${object_name_under}_ids.append(obj.ident)
    request.cls.${object_name_under}_list = ${interface_name}(request.cls.${object_name_under}_list)
    request.cls.object = request.cls.${object_name_under}_list"""
        }
    }

    get_next_object_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return next(self)

    def next(self):
        return self._get_next_object(${return_type})

    __next__ = next""",
            'services': """
    def ${method_name}(self):
        \"\"\"Gets next object\"\"\"
        ${pattern_name}
        return next(self)

    def next(self):
        \"\"\"next method for enumerator\"\"\"
        return self._get_next_object(${return_type})

    __next__ = next""",
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}
        if not is_never_authz(self.service_config):
            assert isinstance(self.${return_type_under}_list.${method_name}(), ${return_type})"""
        }
    }

    get_next_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        return self._get_next_n(${return_type}List, number=${arg0_name})""",
            'services': """
    def ${method_name}(self, ${arg0_name}):
        ${pattern_name}
        return self._get_next_n(${return_type}List, number=${arg0_name})""",
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        from dlkit.abstract_osid.${package_name_replace_reserved}.objects import ${return_type}List, ${return_type}
        if not is_never_authz(self.service_config):
            new_list = self.${return_type_under}_list.${method_name}(2)
            assert isinstance(new_list, ${return_type}List)
            for item in new_list:
                assert isinstance(item, ${return_type})"""
        }
    }


class GenericCatalogList(object):
    init_template = {
        'python': {
            'tests': """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    ${pattern_name}
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        request.cls.${object_name_under}_ids = list()

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.${object_name_under}_ids:
                request.cls.svc_mgr.delete_${cat_name_under}(obj)
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    ${pattern_name}
    from dlkit.json_.${pkg_name_replaced_reserved}.objects import ${interface_name}
    request.cls.${object_name_under}_list = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            create_form = request.cls.svc_mgr.get_${object_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            obj = request.cls.svc_mgr.create_${object_name_under}(create_form)
            request.cls.${object_name_under}_list.append(obj)
            request.cls.${object_name_under}_ids.append(obj.ident)
    request.cls.${object_name_under}_list = ${interface_name}(request.cls.${object_name_under}_list)"""
        }
    }


class GenericCatalogNodeList(object):
    init_template = {
        'python': {
            'tests': """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    ${pattern_name}
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}Node'
        create_form.description = 'Test ${cat_name}Node for ${interface_name} tests'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        request.cls.${object_name_under}_node_ids = list()

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.${object_name_under}_node_ids:
                request.cls.svc_mgr.delete_${cat_name_under}(obj)
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    ${pattern_name}
    from dlkit.json_.${pkg_name_replaced_reserved}.objects import ${interface_name}, ${object_name}Node
    request.cls.${object_name_under}_node_list = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
            create_form.display_name = 'Test ${object_name}Node ' + str(num)
            create_form.description = 'Test ${object_name}Node for ${interface_name} tests'
            obj = request.cls.svc_mgr.create_${cat_name_under}(create_form)
            request.cls.${object_name_under}_node_list.append(${object_name}Node(obj.object_map))
            request.cls.${object_name_under}_node_ids.append(obj.ident)
        # Not put the catalogs in a hierarchy
        request.cls.svc_mgr.add_root_${cat_name_under}(request.cls.${object_name_under}_node_list[0].ident)
        request.cls.svc_mgr.add_child_${cat_name_under}(
            request.cls.${object_name_under}_node_list[0].ident,
            request.cls.${object_name_under}_node_list[1].ident)
    request.cls.${object_name_under}_node_list = ${interface_name}(request.cls.${object_name_under}_node_list)"""
        }
    }
