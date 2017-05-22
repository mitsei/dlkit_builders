
class AuthorizationSession:

    import_statements = [
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.type.primitives import Type',
        'LOOKUP_RESOURCE_FUNCTION_ID = Id(**{\'identifier\': \'lookup\', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'})',
        'SEARCH_RESOURCE_FUNCTION_ID = Id(**{\'identifier\': \'search\', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'})',
        'CREATE_RESOURCE_FUNCTION_ID = Id(**{\'identifier\': \'create\', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'})',
        'DELETE_RESOURCE_FUNCTION_ID = Id(**{\'identifier\': \'delete\', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'})',
        'ASSIGN_RESOURCE_FUNCTION_ID = Id(**{\'identifier\': \'assign\', \'namespace\': \'resource.ResourceBin\', \'authority\': \'ODL.MIT.EDU\'})',
        'CREATE_BIN_FUNCTION_ID = Id(**{\'identifier\': \'create\', \'namespace\': \'resource.Bin\', \'authority\': \'ODL.MIT.EDU\'})',
        'DELETE_BIN_FUNCTION_ID = Id(**{\'identifier\': \'delete\', \'namespace\': \'resource.Bin\', \'authority\': \'ODL.MIT.EDU\'})',
        'LOOKUP_BIN_FUNCTION_ID = Id(**{\'identifier\': \'lookup\', \'namespace\': \'resource.Bin\', \'authority\': \'ODL.MIT.EDU\'})',
        'ACCESS_BIN_HIERARCHY_FUNCTION_ID = Id(**{\'identifier\': \'access\', \'namespace\': \'resource.Bin\', \'authority\': \'ODL.MIT.EDU\'})',
        'MODIFY_BIN_HIERARCHY_FUNCTION_ID = Id(**{\'identifier\': \'modify\', \'namespace\': \'resource.Bin\', \'authority\': \'ODL.MIT.EDU\'})',
        'ROOT_QUALIFIER_ID = Id(\'resource.Bin%3AROOT%40ODL.MIT.EDU\')',
        'BOOTSTRAP_VAULT_TYPE = Type(authority=\'ODL.MIT.EDU\', namespace=\'authorization.Vault\', identifier=\'bootstrap_vault\')',
        'OVERRIDE_VAULT_TYPE = Type(authority=\'ODL.MIT.EDU\', namespace=\'authorization.Vault\', identifier=\'override_vault\')',
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.authz_mgr = Runtime().get_manager('AUTHORIZATION', implementation='JSON_1')
        cls.vault_admin_session = cls.authz_mgr.get_vault_admin_session()
        cls.vault_lookup_session = cls.authz_mgr.get_vault_lookup_session()

        create_form = cls.vault_admin_session.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationLookupSession tests'
        create_form.genus_type = BOOTSTRAP_VAULT_TYPE
        cls.vault = cls.vault_admin_session.create_vault(create_form)

        create_form = cls.vault_admin_session.get_vault_form_for_create([])
        create_form.display_name = 'Test Override Vault'
        create_form.description = 'Test Override Vault for AuthorizationLookupSession tests'
        create_form.genus_type = OVERRIDE_VAULT_TYPE
        cls.override_vault = cls.vault_admin_session.create_vault(create_form)

        cls.authz_admin_session = cls.authz_mgr.get_authorization_admin_session_for_vault(cls.vault.ident)
        cls.override_authz_admin_session = cls.authz_mgr.get_authorization_admin_session_for_vault(cls.override_vault.ident)
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

        # Set up Resource - Bin assignment authorization for current user
        create_form = cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            ASSIGN_RESOURCE_FUNCTION_ID,
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
        for num in [0, 1, 2, 3, 4, 5, 6, 7]:
            create_form = cls.resource_mgr.get_bin_form_for_create([])
            create_form.display_name = 'Test Bin ' + str(num)
            create_form.description = 'Test Bin for Testing Authorization Number: ' + str(num)
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
        cls.authz_list.append(jane_lookup_authz)
        cls.authz_id_list.append(jane_lookup_authz.ident)

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

        # Set up Resource lookup override authorizations for Jane
        for num in [7]:
            create_form = cls.override_authz_admin_session.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                LOOKUP_RESOURCE_FUNCTION_ID,
                cls.bin_id_list[num],
                [])
            create_form.display_name = 'Test Authorization ' + str(num) + ' (override)'
            create_form.description = 'Test Authorization for AuthorizationLookupSession tests'
            authz = cls.override_authz_admin_session.create_authorization(create_form)
            cls.authz_list.append(authz)
            cls.authz_id_list.append(authz.ident)

        # Set up Resource search override authorizations for Jane
        for num in [7]:
            create_form = cls.override_authz_admin_session.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                SEARCH_RESOURCE_FUNCTION_ID,
                cls.bin_id_list[num],
                [])
            create_form.display_name = 'Test Authorization ' + str(num) + ' (override)'
            create_form.description = 'Test Authorization for AuthorizationLookupSession tests'
            authz = cls.override_authz_admin_session.create_authorization(create_form)
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
        #        _ 1(t) _         2     not in hierarchy
        #       |        |        |
        #       3        4       5(t)      6     7(t)   (the 'blue' resource in bin 2 is also assigned to bin 7)"""

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

    def test_is_authorized_6(self):
        \"\"\"Tests is_authorized 5\"\"\"
        self.assertFalse(self.catalog.is_authorized(AGENT_ID, LOOKUP_RESOURCE_FUNCTION_ID, self.bin_id_list[6]))

    def test_is_authorized_7(self):
        \"\"\"Tests is_authorized 5\"\"\"
        self.assertTrue(self.catalog.is_authorized(AGENT_ID, LOOKUP_RESOURCE_FUNCTION_ID, self.bin_id_list[7]))
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
                Id(**{\'identifier\': str(num), \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
                [])
            create_form.display_name = 'Test Authorization ' + str(num)
            create_form.description = 'Test Authorization for AuthorizationLookupSession tests'
            object = cls.catalog.create_authorization(create_form)
            cls.authorization_list.append(object)
            cls.authorization_ids.append(object.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_vaults():
            for obj in catalog.get_authorizations():
                catalog.delete_authorization(obj.ident)
            cls.svc_mgr.delete_vault(catalog.ident)"""


class AuthorizationForm:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('AUTHORIZATION', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationLookupSession tests'
        cls.catalog = cls.svc_mgr.create_vault(create_form)
        cls.form = cls.catalog.get_authorization_form_for_create_for_agent(
            AGENT_ID,
            LOOKUP_RESOURCE_FUNCTION_ID,
            Id(**{\'identifier\': '1', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
            [])

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_vaults():
            cls.svc_mgr.delete_vault(catalog.ident)"""


class AuthorizationList:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('AUTHORIZATION', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationLookupSession tests'
        cls.catalog = cls.svc_mgr.create_vault(create_form)
        cls.form = cls.catalog.get_authorization_form_for_create_for_agent(
            AGENT_ID,
            LOOKUP_RESOURCE_FUNCTION_ID,
            Id(**{\'identifier\': '1', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
            [])

    def setUp(self):
        from dlkit.json_.authorization.objects import AuthorizationList
        self.authorization_list = list()
        self.authorization_ids = list()

        for num in [0, 1]:
            form = self.catalog.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                LOOKUP_RESOURCE_FUNCTION_ID,
                Id(**{\'identifier\': str(num), \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
                [])
            obj = self.catalog.create_authorization(form)

            self.authorization_list.append(obj)
            self.authorization_ids.append(obj.ident)
        self.authorization_list = AuthorizationList(self.authorization_list)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_vaults():
            for authz in catalog.get_authorizations():
                catalog.delete_authorization(authz.ident)
            cls.svc_mgr.delete_vault(catalog.ident)"""


class Authorization:
    import_statements = [
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)',
        "LOOKUP_RESOURCE_FUNCTION_ID = Id(**{'identifier': 'lookup', 'namespace': 'resource.Resource', 'authority': 'ODL.MIT.EDU'})",
        "AGENT_ID = Id(**{'identifier': 'jane_doe', 'namespace': 'osid.agent.Agent', 'authority': 'MIT-ODL'})"
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.authorization_list = list()
        cls.authorization_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('AUTHORIZATION', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationQuerySession tests'
        cls.catalog = cls.svc_mgr.create_vault(create_form)
        create_form = cls.catalog.get_authorization_form_for_create_for_agent(
            AGENT_ID,
            LOOKUP_RESOURCE_FUNCTION_ID,
            Id(**{\'identifier\': str('foo'), \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
            [])
        create_form.display_name = 'Test Authorization'
        create_form.description = (
            'Test Authorization for Authorization tests')
        obj = cls.catalog.create_authorization(create_form)
        cls.object = obj

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_vaults():
            for obj in catalog.get_authorizations():
                catalog.delete_authorization(obj.ident)
            cls.svc_mgr.delete_vault(catalog.ident)"""

    get_agent = """"""

    get_agent_id = """"""

    has_agent = """"""

    get_trust = """"""

    get_trust_id = """"""

    has_trust = """"""

    get_resource = """"""

    get_resource_id = """"""

    has_resource = """"""

    is_implicit = """"""


class AuthorizationQuerySession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.authorization_list = list()
        cls.authorization_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('AUTHORIZATION', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationQuerySession tests'
        cls.catalog = cls.svc_mgr.create_vault(create_form)
        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = cls.catalog.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                LOOKUP_RESOURCE_FUNCTION_ID,
                Id(**{\'identifier\': str(color), \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
                [])
            create_form.display_name = 'Test Authorization ' + color
            create_form.description = (
                'Test Authorization for AuthorizationQuerySession tests, did I mention green')
            obj = cls.catalog.create_authorization(create_form)
            cls.authorization_list.append(obj)
            cls.authorization_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_vaults():
            for obj in catalog.get_authorizations():
                catalog.delete_authorization(obj.ident)
            cls.svc_mgr.delete_vault(catalog.ident)"""


class AuthorizationAdminSession:
    import_statements = [
        'from dlkit.abstract_osid.osid.objects import OsidForm',
        'from dlkit.abstract_osid.osid import errors',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})',
        'NEW_TYPE_2 = Type(**{\'identifier\': \'NEW 2\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})'
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.authorization_list = list()
        cls.authorization_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('AUTHORIZATION', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationAdminSession tests'
        cls.catalog = cls.svc_mgr.create_vault(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                LOOKUP_RESOURCE_FUNCTION_ID,
                Id(**{\'identifier\': str(num), \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
                [])
            create_form.display_name = 'Test Authorization ' + str(num)
            create_form.description = 'Test Authorization for AuthorizationLookupSession tests'
            object = cls.catalog.create_authorization(create_form)
            cls.authorization_list.append(object)
            cls.authorization_ids.append(object.ident)

        form = cls.catalog.get_authorization_form_for_create_for_agent(
            AGENT_ID,
            LOOKUP_RESOURCE_FUNCTION_ID,
            Id(**{\'identifier\': \'foo\', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
            [])
        form.display_name = 'new Authorization'
        form.description = 'description of Authorization'
        form.genus_type = NEW_TYPE
        cls.osid_object = cls.catalog.create_authorization(form)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_vaults():
            for obj in catalog.get_authorizations():
                catalog.delete_authorization(obj.ident)
            cls.svc_mgr.delete_vault(catalog.ident)"""

    get_authorization_form_for_create = """
        form = self.catalog.get_authorization_form_for_create_for_agent(
            AGENT_ID,
            LOOKUP_RESOURCE_FUNCTION_ID,
            Id(**{\'identifier\': str(num), \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
            [])
        self.assertTrue(isinstance(form, OsidForm))
        self.assertFalse(form.is_for_update())"""

    update_authorization = """
        from dlkit.abstract_osid.authorization.objects import Authorization
        form = self.catalog.get_authorization_form_for_update(self.osid_object.ident)
        form.display_name = 'new name'
        form.description = 'new description'
        form.set_genus_type(NEW_TYPE_2)
        updated_object = self.catalog.update_authorization(form)
        self.assertTrue(isinstance(updated_object, Authorization))
        self.assertEqual(updated_object.ident, self.osid_object.ident)
        self.assertEqual(updated_object.display_name.text, 'new name')
        self.assertEqual(updated_object.description.text, 'new description')
        self.assertEqual(updated_object.genus_type, NEW_TYPE_2)"""

    delete_authorization = """
        form = self.catalog.get_authorization_form_for_create_for_agent(
            AGENT_ID,
            LOOKUP_RESOURCE_FUNCTION_ID,
            Id(**{\'identifier\': \'foo2\', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
            [])
        form.display_name = 'new Authorization'
        form.description = 'description of Authorization'
        form.genus_type = NEW_TYPE
        osid_object = self.catalog.create_authorization(form)
        self.catalog.delete_authorization(osid_object.ident)
        with self.assertRaises(errors.NotFound):
            self.catalog.get_authorization(osid_object.ident)"""


class VaultNodeList:
    init = """"""
    get_next_vault_node = """"""

    get_next_vault_nodes = """"""
