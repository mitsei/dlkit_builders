
class CommentLookupSession:

    import_statements_pattern = [
        'from dlkit_django import PROXY_SESSION, proxy_example',
        'from dlkit_django.managers import Runtime',
        'REQUEST = proxy_example.TestRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.primordium.id.primitives import Id',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\',})\n',
        'AGENT_ID = Id(**{\'identifier\': \'jane_doe\', \'namespace\': \'authentication.Agent\', \'authority\': \'odl.mit.edu\',})\n',
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
        #for obj in cls.catalog.get_${object_name_under_plural}():
        #    cls.catalog.delete_${object_name_under}(obj.ident)
        #for catalog in cls.catalogs:
        #    cls.svc_mgr.delete_${cat_name_under}(catalog.ident)
        for catalog in cls.svc_mgr.get_${cat_name_under_plural}():
            for obj in catalog.get_${object_name_under_plural}():
                catalog.delete_${object_name_under}(obj.ident)
            cls.svc_mgr.delete_${cat_name_under}(catalog.ident)
"""


class CommentQuerySession:

    import_statements_pattern = CommentLookupSession.import_statements_pattern

    init_template = CommentLookupSession.init_template


class CommentAdminSession:

    get_comment_form_for_create_template = """
        pass"""

class Comment:

    import_statements = [
    ]

    get_commenting_agent_id = """
        pass"""

    get_commenting_agent = """
        pass"""

class CommentQuery:

    import_statements = [
    ]
