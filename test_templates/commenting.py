
class CommentLookupSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.${pkg_name_replaced_reserved} import objects as ABCObjects',
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.primordium.id.primitives import Id',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'AGENT_ID = Id(**{\'identifier\': \'jane_doe\', \'namespace\': \'osid.agent.Agent\', \'authority\': \'MIT-ODL\'})',
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/commenting.py::CommentLookupSession::init_template
    request.cls.service_config = request.param
    request.cls.${object_name_under}_list = list()
    request.cls.${object_name_under}_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_${object_name_under}_form_for_create(AGENT_ID, [])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            object = request.cls.catalog.create_${object_name_under}(create_form)
            request.cls.${object_name_under}_list.append(object)
            request.cls.${object_name_under}_ids.append(object.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_${cat_name_under_plural}():
                for obj in catalog.get_${object_name_under_plural}():
                    catalog.delete_${object_name_under}(obj.ident)
                request.cls.svc_mgr.delete_${cat_name_under}(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/commenting.py::CommentLookupSession::init_template
    request.cls.session = request.cls.catalog"""


class CommentForm:
    import_statements = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.primordium.id.primitives import Id',
        'AGENT_ID = Id(**{\'identifier\': \'jane_doe\', \'namespace\': \'osid.agent.Agent\', \'authority\': \'MIT-ODL\'})',
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'COMMENTING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_book_form_for_create([])
        create_form.display_name = 'Test Book'
        create_form.description = 'Test Book for CommentForm tests'
        request.cls.catalog = request.cls.svc_mgr.create_book(create_form)
        request.cls.form = request.cls.catalog.get_comment_form_for_create(AGENT_ID, [])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_books():
                request.cls.svc_mgr.delete_book(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""


class CommentList:
    import_statements = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.primordium.id.primitives import Id',
        'AGENT_ID = Id(**{\'identifier\': \'jane_doe\', \'namespace\': \'osid.agent.Agent\', \'authority\': \'MIT-ODL\'})',
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'COMMENTING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_book_form_for_create([])
        create_form.display_name = 'Test Book'
        create_form.description = 'Test Book for CommentForm tests'
        request.cls.catalog = request.cls.svc_mgr.create_book(create_form)
        request.cls.form = request.cls.catalog.get_comment_form_for_create(AGENT_ID, [])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_books():
                for comment in catalog.get_comments():
                    catalog.delete_comment(comment.ident)
                request.cls.svc_mgr.delete_book(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    from dlkit.json_.commenting.objects import CommentList
    request.cls.comment_list = list()
    request.cls.comment_ids = list()

    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            form = request.cls.catalog.get_comment_form_for_create(AGENT_ID, [])

            obj = request.cls.catalog.create_comment(form)

            request.cls.comment_list.append(obj)
            request.cls.comment_ids.append(obj.ident)
        request.cls.comment_list = CommentList(request.cls.comment_list)"""


class CommentQuerySession:

    import_statements_pattern = CommentLookupSession.import_statements_pattern

    init_template = """
class FakeQuery:
    _cat_id_args_list = []


@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.${object_name_under}_list = list()
    request.cls.${object_name_under}_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)
        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = request.cls.catalog.get_${object_name_under}_form_for_create(AGENT_ID, [])
            create_form.display_name = 'Test ${object_name} ' + color
            create_form.description = (
                'Test ${object_name} for ${interface_name} tests, did I mention green')
            obj = request.cls.catalog.create_${object_name_under}(create_form)
            request.cls.${object_name_under}_list.append(obj)
            request.cls.${object_name_under}_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_${cat_name_under_plural}():
                for obj in catalog.get_${object_name_under_plural}():
                    catalog.delete_${object_name_under}(obj.ident)
                request.cls.svc_mgr.delete_${cat_name_under}(catalog.ident)

    request.addfinalizer(test_tear_down)"""


class CommentAdminSession:
    import_statements = [
        'from dlkit.abstract_osid.osid.objects import OsidForm',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})',
        'NEW_TYPE_2 = Type(**{\'identifier\': \'NEW 2\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.comment_list = list()
    request.cls.comment_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'COMMENTING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_book_form_for_create([])
        create_form.display_name = 'Test Book'
        create_form.description = 'Test Book for CommentAdminSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_book(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_comment_form_for_create(AGENT_ID, [])
            create_form.display_name = 'Test Comment ' + str(num)
            create_form.description = 'Test Comment for CommentAdminSession tests'
            object = request.cls.catalog.create_comment(create_form)
            request.cls.comment_list.append(object)
            request.cls.comment_ids.append(object.ident)
        create_form = request.cls.catalog.get_comment_form_for_create(AGENT_ID, [])
        create_form.display_name = 'new Comment'
        create_form.description = 'description of Comment'
        create_form.genus_type = NEW_TYPE
        request.cls.osid_object = request.cls.catalog.create_comment(create_form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_books():
                for obj in catalog.get_comments():
                    catalog.delete_comment(obj.ident)
                request.cls.svc_mgr.delete_book(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""

    get_comment_form_for_create = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_comment_form_for_create(AGENT_ID, [])
            assert isinstance(form, OsidForm)
            assert not form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_comment_form_for_create(AGENT_ID, [])"""

    delete_comment = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_comment_form_for_create(AGENT_ID, [])
            form.display_name = 'new Comment'
            form.description = 'description of Comment'
            form.set_genus_type(NEW_TYPE)
            osid_object = self.catalog.create_comment(form)
            self.catalog.delete_comment(osid_object.ident)
            with pytest.raises(errors.NotFound):
                self.catalog.get_comment(osid_object.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.delete_comment(AGENT_ID)"""


class Comment:

    import_statements = [
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.locale.primitives import DisplayText'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'COMMENTING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_book_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_book(create_form)

        form = request.cls.catalog.get_comment_form_for_create(
            Id('resource.Resource%3A1%40ODL.MIT.EDU'),
            [])
        form.display_name = 'Test object'
        request.cls.object = request.cls.catalog.create_comment(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_comments():
                request.cls.catalog.delete_comment(obj.ident)
            request.cls.svc_mgr.delete_book(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""

    get_commenting_agent = """
        if not is_never_authz(self.service_config):
            # because the resource doesn't actually exist
            with pytest.raises(errors.OperationFailed):
                self.object.get_commenting_agent()"""

    get_commenting_agent_id = """
        if not is_never_authz(self.service_config):
            result = self.object.get_commenting_agent_id()
            assert isinstance(result, Id)
            assert str(result) == str(self.catalog._proxy.get_effective_agent_id())"""

    get_text = """
        if not is_never_authz(self.service_config):
            result = self.object.get_text()
            assert isinstance(result, DisplayText)
            assert result.text == ''"""


class CommentQuery:

    import_statements = [
    ]


class BookQuery:
    import_statements = [
        'from dlkit.json_.commenting.queries import BookQuery'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'COMMENTING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_book_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_book(create_form)
        request.cls.fake_id = Id('resource.Resource%3A1%40ODL.MIT.EDU')

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_book(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # Since the session isn't implemented, we just construct an BookQuery directly
    if not is_never_authz(request.cls.service_config):
        request.cls.query = BookQuery(runtime=request.cls.catalog._runtime)"""
