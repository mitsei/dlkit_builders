
class AuthorizationSession:

    import_statements = [
        'from dlkit_runtime import PROXY_SESSION, proxy_example',
        'from dlkit_runtime.managers import Runtime',
        'REQUEST = proxy_example.TestRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.id.primitives import Id',
        'LOOKUP_RESOURCE_FUNCTION_ID = Id(**{\'identifier\': \'lookup\', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\',})',
        'SEARCH_RESOURCE_FUNCTION_ID = Id(**{\'identifier\': \'search\', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\',})',
        'CREATE_RESOURCE_FUNCTION_ID = Id(**{\'identifier\': \'create\', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\',})',
        'DELETE_RESOURCE_FUNCTION_ID = Id(**{\'identifier\': \'delete\', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\',})',
        'CREATE_BIN_FUNCTION_ID = Id(**{\'identifier\': \'create\', \'namespace\': \'resource.Bin\', \'authority\': \'ODL.MIT.EDU\',})',
        'DELETE_BIN_FUNCTION_ID = Id(**{\'identifier\': \'delete\', \'namespace\': \'resource.Bin\', \'authority\': \'ODL.MIT.EDU\',})',
        'LOOKUP_BIN_FUNCTION_ID = Id(**{\'identifier\': \'lookup\', \'namespace\': \'resource.Bin\', \'authority\': \'ODL.MIT.EDU\',})',
        'ACCESS_BIN_HIERARCHY_FUNCTION_ID = Id(**{\'identifier\': \'access\', \'namespace\': \'resource.Bin\', \'authority\': \'ODL.MIT.EDU\',})',
        'MODIFY_BIN_HIERARCHY_FUNCTION_ID = Id(**{\'identifier\': \'modify\', \'namespace\': \'resource.Bin\', \'authority\': \'ODL.MIT.EDU\',})',
        'ROOT_QUALIFIER_ID = Id(\'resource.Bin%3AROOT%40ODL.MIT.EDU\')'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.authz_mgr = Runtime().get_manager('AUTHORIZATION', implementation='MONGO_1')
        cls.vault_admin_session = cls.authz_mgr.get_vault_admin_session()
        cls.vault_lookup_session = cls.authz_mgr.get_vault_lookup_session()
        create_form = cls.vault_admin_session.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationLookupSession tests'
        cls.vault = cls.vault_admin_session.create_vault(create_form)
        cls.authz_admin_session = cls.authz_mgr.get_authorization_admin_session_for_vault(cls.vault.ident)
        cls.authz_lookup_session = cls.authz_mgr.get_authorization_lookup_session_for_vault(cls.vault.ident)

        # Set up Bin create authorization for current user
        create_form = cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            CREATE_BIN_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Bin Create for Test Authorizations'
        create_form.description = 'Bin Create Authorization for AuthorizationLookupSession tests'
        bin_create_authz = cls.authz_admin_session.create_authorization(create_form)

        # Set up Bin delete authorization for current user
        create_form = cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            DELETE_BIN_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Bin Delete for Test Authorizations'
        create_form.description = 'Bin Delete Authorization for AuthorizationLookupSession tests'
        bin_delete_authz = cls.authz_admin_session.create_authorization(create_form)

        # Set up Bin lookup authorization for current user
        create_form = cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            LOOKUP_BIN_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Bin Lookup for Test Authorizations'
        create_form.description = 'Bin Lookup Authorization for AuthorizationLookupSession tests'
        bin_lookup_authz = cls.authz_admin_session.create_authorization(create_form)

        # Set up Bin hierarchy access authorization for current user
        create_form = cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            ACCESS_BIN_HIERARCHY_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Bin Hierarchy Access for Test Authorizations'
        create_form.description = 'Bin Hierarchy Access Authorization for AuthorizationLookupSession tests'
        bin_hierarchy_modify_authz = cls.authz_admin_session.create_authorization(create_form)

        # Set up Bin hierarchy modify authorization for current user
        create_form = cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            MODIFY_BIN_HIERARCHY_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Bin Hierarchy Modify for Test Authorizations'
        create_form.description = 'Bin Hierarchy Modify Authorization for AuthorizationLookupSession tests'
        bin_hierarchy_modify_authz = cls.authz_admin_session.create_authorization(create_form)

        # Set up Resource create authorization for current user
        create_form = cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            CREATE_RESOURCE_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Resource create for Test Authorizations'
        create_form.description = 'Resource create Authorization for AuthorizationLookupSession tests'
        resource_create_authz = cls.authz_admin_session.create_authorization(create_form)

        # Set up Resource delete authorization for current user
        create_form = cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            DELETE_RESOURCE_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Resource Delete for Test Authorizations'
        create_form.description = 'Resource Delete Authorization for AuthorizationLookupSession tests'
        resource_delete_authz = cls.authz_admin_session.create_authorization(create_form)

        # Set up Resource lookup authorization for current user
        create_form = cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            LOOKUP_RESOURCE_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Resource Lookup for Test Authorizations'
        create_form.description = 'Resource Lookup Authorization for AuthorizationLookupSession tests'
        resource_lookup_authz = cls.authz_admin_session.create_authorization(create_form)

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
        cls.catalog = cls.svc_mgr.get_vault(cls.vault.ident)

        # Set up Bin lookup authorization for Jane
        create_form = cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            AGENT_ID,
            LOOKUP_BIN_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Jane Lookup Authorization'
        create_form.description = 'Test Authorization for AuthorizationLookupSession tests'
        jane_lookup_authz = cls.authz_admin_session.create_authorization(create_form)
        
        # Set up Resource lookup authorizations for Jane
        for num in [1, 5]:
            create_form = cls.authz_admin_session.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                LOOKUP_RESOURCE_FUNCTION_ID,
                cls.bin_id_list[num],
                [])
            create_form.display_name = 'Test Authorization ' + str(num)
            create_form.description = 'Test Authorization for AuthorizationLookupSession tests'
            authz = cls.authz_admin_session.create_authorization(create_form)
            cls.authz_list.append(authz)
            cls.authz_id_list.append(authz.ident)

        # Set up Resource search authorizations for Jane
        for num in [1, 5]:
            create_form = cls.authz_admin_session.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                SEARCH_RESOURCE_FUNCTION_ID,
                cls.bin_id_list[num],
                [])
            create_form.display_name = 'Test Authorization ' + str(num)
            create_form.description = 'Test Authorization for AuthorizationLookupSession tests'
            authz = cls.authz_admin_session.create_authorization(create_form)
            cls.authz_list.append(authz)
            cls.authz_id_list.append(authz.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.resource_mgr.get_bins():
            for obj in catalog.get_resources():
                catalog.delete_resource(obj.ident)
            cls.resource_mgr.delete_bin(catalog.ident)
        for vault in cls.vault_lookup_session.get_vaults():
            lookup_session = cls.authz_mgr.get_authorization_lookup_session_for_vault(vault.ident)
            admin_session = cls.authz_mgr.get_authorization_admin_session_for_vault(vault.ident)
            for authz in lookup_session.get_authorizations():
                admin_session.delete_authorization(authz.ident)
            cls.vault_admin_session.delete_vault(vault.ident)
            
        # The hierarchy should look like this. (t) indicates where lookup is
        # explicitely authorized:
        #
        #            _____ 0 _____
        #           |             |
        #        _ 1(t) _         2 
        #       |        |        |
        #       3        4       5(t)
"""

    is_authorized = """
        self.assertFalse(self.catalog.is_authorized(AGENT_ID, LOOKUP_RESOURCE_FUNCTION_ID, self.bin_id_list[0]))

    def test_is_authorized_1(self):
        \"\"\"Tests is_authorized 1\"\"\"
        self.assertTrue(self.catalog.is_authorized(AGENT_ID, LOOKUP_RESOURCE_FUNCTION_ID, self.bin_id_list[1]))

    def test_is_authorized_3(self):
        \"\"\"Tests is_authorized 3\"\"\"
        self.assertTrue(self.catalog.is_authorized(AGENT_ID, LOOKUP_RESOURCE_FUNCTION_ID, self.bin_id_list[3]))

    def test_is_authorized_4(self):
        \"\"\"Tests is_authorized 4\"\"\"
        self.assertTrue(self.catalog.is_authorized(AGENT_ID, LOOKUP_RESOURCE_FUNCTION_ID, self.bin_id_list[4]))

    def test_is_authorized_2(self):
        \"\"\"Tests is_authorized 2\"\"\"
        self.assertFalse(self.catalog.is_authorized(AGENT_ID, LOOKUP_RESOURCE_FUNCTION_ID, self.bin_id_list[2]))

    def test_is_authorized_5(self):
        \"\"\"Tests is_authorized 5\"\"\"
        self.assertTrue(self.catalog.is_authorized(AGENT_ID, LOOKUP_RESOURCE_FUNCTION_ID, self.bin_id_list[5]))
"""

class AuthorizationLookupSession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.authorization_list = list()
        cls.authorization_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('AUTHORIZATION', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationLookupSession tests'
        cls.catalog = cls.svc_mgr.create_vault(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                LOOKUP_RESOURCE_FUNCTION_ID,
                Id(**{\'identifier\': str(num), \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\',}),
                [])
            create_form.display_name = 'Test Authorization ' + str(num)
            create_form.description = 'Test Authorization for AuthorizationLookupSession tests'
            object = cls.catalog.create_authorization(create_form)
            cls.authorization_list.append(object)
            cls.authorization_ids.append(object.ident)

    @classmethod
    def tearDownClass(cls):
        #for obj in cls.catalog.get_authorizations():
        #    cls.catalog.delete_authorization(obj.ident)
        #for catalog in cls.catalogs:
        #    cls.svc_mgr.delete_vault(catalog.ident)
        for catalog in cls.svc_mgr.get_vaults():
            for obj in catalog.get_authorizations():
                catalog.delete_authorization(obj.ident)
            cls.svc_mgr.delete_vault(catalog.ident)
"""

class Authorization:
    pass