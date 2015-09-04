
class AuthorizationSession:

    import_statements = [
        'from dlkit_django import PROXY_SESSION, proxy_example',
        'from dlkit_django.managers import Runtime',
        'REQUEST = proxy_example.TestRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.id.primitives import Id',
        'FUNCTION_ID = Id(**{\'identifier\': \'lookup\', \'namespace\': \'resource.Resource\', \'authority\': \'odl.mit.edu\',})\n',
        'AGENT_ID = Id(**{\'identifier\': \'birdland\', \'namespace\': \'authentication.Agent\', \'authority\': \'mit.edu\',})\n',
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.bin_list = list()
        cls.bin_id_list = list()
        cls.authz_list = list()
        cls.authz_id_list = list()
        cls.resource_mgr = Runtime().get_service_manager('RESOURCE', proxy=PROXY, implementation='TEST_SERVICE')
        for num in [0, 1, 2, 3, 4, 5]:
            create_form = cls.resource_mgr.get_bin_form_for_create([])
            create_form.display_name = 'Test Resource'
            create_form.description = 'Test Resource for Testing Authorization Number: ' + str(num)
            bin = cls.resource_mgr.create_bin(create_form)
            cls.bin_list.append(bin)
            cls.bin_id_list.append(bin.ident)

        cls.resource_mgr.add_root_bin(cls.bin_id_list[0])
        cls.resource_mgr.add_child_bin(cls.bin_id_list[0], cls.bin_id_list[1])
        cls.resource_mgr.add_child_bin(cls.bin_id_list[0], cls.bin_id_list[2])
        cls.resource_mgr.add_child_bin(cls.bin_id_list[1], cls.bin_id_list[3])
        cls.resource_mgr.add_child_bin(cls.bin_id_list[1], cls.bin_id_list[4])
        cls.resource_mgr.add_child_bin(cls.bin_id_list[2], cls.bin_id_list[5])
        
        cls.svc_mgr = Runtime().get_service_manager('AUTHORIZATION', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationLookupSession tests'
        cls.catalog = cls.svc_mgr.create_vault(create_form)
        for num in [1, 5]:
            create_form = cls.catalog.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                FUNCTION_ID,
                cls.bin_id_list[num],
                [])
            create_form.display_name = 'Test Authorization ' + str(num)
            create_form.description = 'Test Authorization for AuthorizationLookupSession tests'
            authz = cls.catalog.create_authorization(create_form)
            cls.authz_list.append(authz)
            cls.authz_id_list.append(authz.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.resource_mgr.get_bins():
            for obj in catalog.get_resources():
                catalog.delete_resource(obj.ident)
            cls.svc_mgr.delete_bin(catalog.ident)
        for catalog in cls.svc_mgr.get_vaults():
            for obj in catalog.get_authorizations():
                catalog.delete_authorization(obj.ident)
            cls.svc_mgr.delete_vault(catalog.ident)
"""

    is_authorized = """
        self.assertFalse(self.catalog.is_authorized(AGENT_ID, FUNCTION_ID, cls.bin_id_list[0]))
        self.assertTrue(self.catalog.is_authorized(AGENT_ID, FUNCTION_ID, cls.bin_id_list[1]))
        self.assertTrue(self.catalog.is_authorized(AGENT_ID, FUNCTION_ID, cls.bin_id_list[3]))
        self.assertFalse(self.catalog.is_authorized(AGENT_ID, FUNCTION_ID, cls.bin_id_list[2]))
        self.assertTrue(self.catalog.is_authorized(AGENT_ID, FUNCTION_ID, cls.bin_id_list[5]))
"""

class Authorization:
    pass