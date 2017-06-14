
class CommentLookupSession:

    import_statements_pattern = [
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
    @classmethod
    def setUpClass(cls):
        cls.${object_name_under}_list = list()
        cls.${object_name_under}_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test ${cat_name}'
        create_form.description = 'Test ${cat_name} for ${interface_name} tests'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_${object_name_under}_form_for_create(AGENT_ID, [])
            create_form.display_name = 'Test ${object_name} ' + str(num)
            create_form.description = 'Test ${object_name} for ${interface_name} tests'
            object = cls.catalog.create_${object_name_under}(create_form)
            cls.${object_name_under}_list.append(object)
            cls.${object_name_under}_ids.append(object.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_${cat_name_under_plural}():
            for obj in catalog.get_${object_name_under_plural}():
                catalog.delete_${object_name_under}(obj.ident)
            cls.svc_mgr.delete_${cat_name_under}(catalog.ident)"""


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
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('COMMENTING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_book_form_for_create([])
        create_form.display_name = 'Test Book'
        create_form.description = 'Test Book for CommentForm tests'
        cls.catalog = cls.svc_mgr.create_book(create_form)
        cls.form = cls.catalog.get_comment_form_for_create(AGENT_ID, [])

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_books():
            cls.svc_mgr.delete_book(catalog.ident)"""


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
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('COMMENTING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_book_form_for_create([])
        create_form.display_name = 'Test Book'
        create_form.description = 'Test Book for CommentForm tests'
        cls.catalog = cls.svc_mgr.create_book(create_form)
        cls.form = cls.catalog.get_comment_form_for_create(AGENT_ID, [])

    def setUp(self):
        from dlkit.json_.commenting.objects import CommentList
        self.comment_list = list()
        self.comment_ids = list()

        for num in [0, 1]:
            form = self.catalog.get_comment_form_for_create(AGENT_ID, [])

            obj = self.catalog.create_comment(form)

            self.comment_list.append(obj)
            self.comment_ids.append(obj.ident)
        self.comment_list = CommentList(self.comment_list)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_books():
            for comment in catalog.get_comments():
                catalog.delete_comment(comment.ident)
            cls.svc_mgr.delete_book(catalog.ident)"""


class CommentQuerySession:

    import_statements_pattern = CommentLookupSession.import_statements_pattern

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
        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = cls.catalog.get_${object_name_under}_form_for_create(AGENT_ID, [])
            create_form.display_name = 'Test ${object_name} ' + color
            create_form.description = (
                'Test ${object_name} for ${interface_name} tests, did I mention green')
            obj = cls.catalog.create_${object_name_under}(create_form)
            cls.${object_name_under}_list.append(obj)
            cls.${object_name_under}_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_${cat_name_under_plural}():
            for obj in catalog.get_${object_name_under_plural}():
                catalog.delete_${object_name_under}(obj.ident)
            cls.svc_mgr.delete_${cat_name_under}(catalog.ident)"""


class CommentAdminSession:
    import_statements = [
        'from dlkit.abstract_osid.osid.objects import OsidForm',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})',
        'NEW_TYPE_2 = Type(**{\'identifier\': \'NEW 2\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.comment_list = list()
        cls.comment_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('COMMENTING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_book_form_for_create([])
        create_form.display_name = 'Test Book'
        create_form.description = 'Test Book for CommentAdminSession tests'
        cls.catalog = cls.svc_mgr.create_book(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_comment_form_for_create(AGENT_ID, [])
            create_form.display_name = 'Test Comment ' + str(num)
            create_form.description = 'Test Comment for CommentAdminSession tests'
            object = cls.catalog.create_comment(create_form)
            cls.comment_list.append(object)
            cls.comment_ids.append(object.ident)
        create_form = cls.catalog.get_comment_form_for_create(AGENT_ID, [])
        create_form.display_name = 'new Comment'
        create_form.description = 'description of Comment'
        create_form.genus_type = NEW_TYPE
        cls.osid_object = cls.catalog.create_comment(create_form)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_books():
            for obj in catalog.get_comments():
                catalog.delete_comment(obj.ident)
            cls.svc_mgr.delete_book(catalog.ident)"""

    get_comment_form_for_create = """
        form = self.catalog.get_comment_form_for_create(AGENT_ID, [])
        self.assertTrue(isinstance(form, OsidForm))
        self.assertFalse(form.is_for_update())"""

    delete_comment = """
        form = self.catalog.get_comment_form_for_create(AGENT_ID, [])
        form.display_name = 'new Comment'
        form.description = 'description of Comment'
        form.set_genus_type(NEW_TYPE)
        osid_object = self.catalog.create_comment(form)
        self.catalog.delete_comment(osid_object.ident)
        with self.assertRaises(errors.NotFound):
            self.catalog.get_comment(osid_object.ident)"""


class Comment:

    import_statements = [
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('COMMENTING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_book_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_book(create_form)

        form = cls.catalog.get_comment_form_for_create(
            Id('resource.Resource%3A1%40ODL.MIT.EDU'),
            [])
        form.display_name = 'Test object'
        cls.object = cls.catalog.create_comment(form)

    @classmethod
    def tearDownClass(cls):
        for obj in cls.catalog.get_comments():
            cls.catalog.delete_comment(obj.ident)
        cls.svc_mgr.delete_book(cls.catalog.ident)"""

    get_commenting_agent_id = """"""

    get_commenting_agent = """"""

    get_comment_record = """"""

    get_rating = """"""

    get_rating_id = """"""

    has_rating = """"""


class CommentQuery:

    import_statements = [
    ]


class BookQuery:
    init = """"""

    clear_comment_id_terms = """"""

    clear_comment_terms = """"""

    clear_ancestor_book_id_terms = """"""

    clear_ancestor_book_terms = """"""

    clear_descendant_book_id_terms = """"""

    clear_descendant_book_terms = """"""
