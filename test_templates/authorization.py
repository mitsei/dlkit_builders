
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
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.authz_mgr = Runtime().get_manager(
        'AUTHORIZATION',
        implementation='JSON_1')
    if not is_never_authz(request.cls.service_config):
        request.cls.vault_admin_session = request.cls.authz_mgr.get_vault_admin_session()
        request.cls.vault_lookup_session = request.cls.authz_mgr.get_vault_lookup_session()

        create_form = request.cls.vault_admin_session.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationSession tests'
        create_form.genus_type = BOOTSTRAP_VAULT_TYPE
        request.cls.vault = request.cls.vault_admin_session.create_vault(create_form)

        create_form = request.cls.vault_admin_session.get_vault_form_for_create([])
        create_form.display_name = 'Test Override Vault'
        create_form.description = 'Test Override Vault for AuthorizationSession tests'
        create_form.genus_type = OVERRIDE_VAULT_TYPE
        request.cls.override_vault = request.cls.vault_admin_session.create_vault(create_form)

        request.cls.authz_admin_session = request.cls.authz_mgr.get_authorization_admin_session_for_vault(request.cls.vault.ident)
        request.cls.override_authz_admin_session = request.cls.authz_mgr.get_authorization_admin_session_for_vault(request.cls.override_vault.ident)
        request.cls.authz_lookup_session = request.cls.authz_mgr.get_authorization_lookup_session_for_vault(request.cls.vault.ident)

        # Set up Bin create authorization for current user
        create_form = request.cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            CREATE_BIN_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Bin Create for Test Authorizations'
        create_form.description = 'Bin Create Authorization for AuthorizationSession tests'
        bin_create_authz = request.cls.authz_admin_session.create_authorization(create_form)

        # Set up Bin delete authorization for current user
        create_form = request.cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            DELETE_BIN_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Bin Delete for Test Authorizations'
        create_form.description = 'Bin Delete Authorization for AuthorizationSession tests'
        bin_delete_authz = request.cls.authz_admin_session.create_authorization(create_form)

        # Set up Bin lookup authorization for current user
        create_form = request.cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            LOOKUP_BIN_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Bin Lookup for Test Authorizations'
        create_form.description = 'Bin Lookup Authorization for AuthorizationSession tests'
        bin_lookup_authz = request.cls.authz_admin_session.create_authorization(create_form)

        # Set up Bin hierarchy access authorization for current user
        create_form = request.cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            ACCESS_BIN_HIERARCHY_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Bin Hierarchy Access for Test Authorizations'
        create_form.description = 'Bin Hierarchy Access Authorization for AuthorizationSession tests'
        bin_hierarchy_modify_authz = request.cls.authz_admin_session.create_authorization(create_form)

        # Set up Bin hierarchy modify authorization for current user
        create_form = request.cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            MODIFY_BIN_HIERARCHY_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Bin Hierarchy Modify for Test Authorizations'
        create_form.description = 'Bin Hierarchy Modify Authorization for AuthorizationSession tests'
        bin_hierarchy_modify_authz = request.cls.authz_admin_session.create_authorization(create_form)

        # Set up Resource create authorization for current user
        create_form = request.cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            CREATE_RESOURCE_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Resource create for Test Authorizations'
        create_form.description = 'Resource create Authorization for AuthorizationSession tests'
        resource_create_authz = request.cls.authz_admin_session.create_authorization(create_form)

        # Set up Resource delete authorization for current user
        create_form = request.cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            DELETE_RESOURCE_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Resource Delete for Test Authorizations'
        create_form.description = 'Resource Delete Authorization for AuthorizationSession tests'
        resource_delete_authz = request.cls.authz_admin_session.create_authorization(create_form)

        # Set up Resource - Bin assignment authorization for current user
        create_form = request.cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            ASSIGN_RESOURCE_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Resource Delete for Test Authorizations'
        create_form.description = 'Resource Delete Authorization for AuthorizationSession tests'
        resource_delete_authz = request.cls.authz_admin_session.create_authorization(create_form)

        # Set up Resource lookup authorization for current user
        create_form = request.cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            PROXY.get_authentication().get_agent_id(),
            LOOKUP_RESOURCE_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Resource Lookup for Test Authorizations'
        create_form.description = 'Resource Lookup Authorization for AuthorizationSession tests'
        resource_lookup_authz = request.cls.authz_admin_session.create_authorization(create_form)

        request.cls.bin_list = list()
        request.cls.bin_id_list = list()
        request.cls.authz_list = list()
        request.cls.authz_id_list = list()
        request.cls.resource_mgr = Runtime().get_service_manager(
            'RESOURCE',
            proxy=PROXY,
            implementation='TEST_SERVICE')
        for num in [0, 1, 2, 3, 4, 5, 6, 7]:
            create_form = request.cls.resource_mgr.get_bin_form_for_create([])
            create_form.display_name = 'Test Bin ' + str(num)
            create_form.description = 'Test Bin for Testing Authorization Number: ' + str(num)
            bin = request.cls.resource_mgr.create_bin(create_form)
            request.cls.bin_list.append(bin)
            request.cls.bin_id_list.append(bin.ident)

        request.cls.resource_mgr.add_root_bin(request.cls.bin_id_list[0])
        request.cls.resource_mgr.add_child_bin(request.cls.bin_id_list[0], request.cls.bin_id_list[1])
        request.cls.resource_mgr.add_child_bin(request.cls.bin_id_list[0], request.cls.bin_id_list[2])
        request.cls.resource_mgr.add_child_bin(request.cls.bin_id_list[1], request.cls.bin_id_list[3])
        request.cls.resource_mgr.add_child_bin(request.cls.bin_id_list[1], request.cls.bin_id_list[4])
        request.cls.resource_mgr.add_child_bin(request.cls.bin_id_list[2], request.cls.bin_id_list[5])

        request.cls.svc_mgr = Runtime().get_service_manager(
            'AUTHORIZATION',
            proxy=PROXY,
            implementation=request.cls.service_config)
        request.cls.catalog = request.cls.svc_mgr.get_vault(request.cls.vault.ident)

        # Set up Bin lookup authorization for Jane
        create_form = request.cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            AGENT_ID,
            LOOKUP_BIN_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Jane Lookup Authorization'
        create_form.description = 'Test Authorization for AuthorizationSession tests'
        jane_lookup_authz = request.cls.authz_admin_session.create_authorization(create_form)
        request.cls.authz_list.append(jane_lookup_authz)
        request.cls.authz_id_list.append(jane_lookup_authz.ident)

        # Set up Resource lookup authorizations for Jane
        for num in [1, 5]:
            create_form = request.cls.authz_admin_session.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                LOOKUP_RESOURCE_FUNCTION_ID,
                request.cls.bin_id_list[num],
                [])
            create_form.display_name = 'Test Authorization ' + str(num)
            create_form.description = 'Test Authorization for AuthorizationSession tests'
            authz = request.cls.authz_admin_session.create_authorization(create_form)
            request.cls.authz_list.append(authz)
            request.cls.authz_id_list.append(authz.ident)

        # Set up Resource lookup override authorizations for Jane
        for num in [7]:
            create_form = request.cls.override_authz_admin_session.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                LOOKUP_RESOURCE_FUNCTION_ID,
                request.cls.bin_id_list[num],
                [])
            create_form.display_name = 'Test Authorization ' + str(num) + ' (override)'
            create_form.description = 'Test Authorization for AuthorizationSession tests'
            authz = request.cls.override_authz_admin_session.create_authorization(create_form)
            request.cls.authz_list.append(authz)
            request.cls.authz_id_list.append(authz.ident)

        # Set up Resource search override authorizations for Jane
        for num in [7]:
            create_form = request.cls.override_authz_admin_session.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                SEARCH_RESOURCE_FUNCTION_ID,
                request.cls.bin_id_list[num],
                [])
            create_form.display_name = 'Test Authorization ' + str(num) + ' (override)'
            create_form.description = 'Test Authorization for AuthorizationSession tests'
            authz = request.cls.override_authz_admin_session.create_authorization(create_form)
            request.cls.authz_list.append(authz)
            request.cls.authz_id_list.append(authz.ident)

        # Set up Resource search authorizations for Jane
        for num in [1, 5]:
            create_form = request.cls.authz_admin_session.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                SEARCH_RESOURCE_FUNCTION_ID,
                request.cls.bin_id_list[num],
                [])
            create_form.display_name = 'Test Authorization ' + str(num)
            create_form.description = 'Test Authorization for AuthorizationSession tests'
            authz = request.cls.authz_admin_session.create_authorization(create_form)
            request.cls.authz_list.append(authz)
            request.cls.authz_id_list.append(authz.ident)

    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.resource_mgr.get_bins():
                for obj in catalog.get_resources():
                    catalog.delete_resource(obj.ident)
                request.cls.resource_mgr.delete_bin(catalog.ident)
            for vault in request.cls.vault_lookup_session.get_vaults():
                lookup_session = request.cls.authz_mgr.get_authorization_lookup_session_for_vault(vault.ident)
                admin_session = request.cls.authz_mgr.get_authorization_admin_session_for_vault(vault.ident)
                for authz in lookup_session.get_authorizations():
                    admin_session.delete_authorization(authz.ident)
                request.cls.vault_admin_session.delete_vault(vault.ident)

        # The hierarchy should look like this. (t) indicates where lookup is
        # explicitely authorized:
        #
        #            _____ 0 _____
        #           |             |
        #        _ 1(t) _         2     not in hierarchy
        #       |        |        |
        #       3        4       5(t)      6     7(t)   (the 'blue' resource in bin 2 is also assigned to bin 7)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    is_authorized = """
        if not is_never_authz(self.service_config):
            assert not self.catalog.is_authorized(AGENT_ID, LOOKUP_RESOURCE_FUNCTION_ID, self.bin_id_list[0])

    def test_is_authorized_1(self):
        \"\"\"Tests is_authorized 1\"\"\"
        if not is_never_authz(self.service_config):
            assert self.catalog.is_authorized(AGENT_ID, LOOKUP_RESOURCE_FUNCTION_ID, self.bin_id_list[1])

    def test_is_authorized_3(self):
        \"\"\"Tests is_authorized 3\"\"\"
        if not is_never_authz(self.service_config):
            assert self.catalog.is_authorized(AGENT_ID, LOOKUP_RESOURCE_FUNCTION_ID, self.bin_id_list[3])

    def test_is_authorized_4(self):
        \"\"\"Tests is_authorized 4\"\"\"
        if not is_never_authz(self.service_config):
            assert self.catalog.is_authorized(AGENT_ID, LOOKUP_RESOURCE_FUNCTION_ID, self.bin_id_list[4])

    def test_is_authorized_2(self):
        \"\"\"Tests is_authorized 2\"\"\"
        if not is_never_authz(self.service_config):
            assert not self.catalog.is_authorized(AGENT_ID, LOOKUP_RESOURCE_FUNCTION_ID, self.bin_id_list[2])

    def test_is_authorized_5(self):
        \"\"\"Tests is_authorized 5\"\"\"
        if not is_never_authz(self.service_config):
            assert self.catalog.is_authorized(AGENT_ID, LOOKUP_RESOURCE_FUNCTION_ID, self.bin_id_list[5])

    def test_is_authorized_6(self):
        \"\"\"Tests is_authorized 5\"\"\"
        if not is_never_authz(self.service_config):
            assert not self.catalog.is_authorized(AGENT_ID, LOOKUP_RESOURCE_FUNCTION_ID, self.bin_id_list[6])

    def test_is_authorized_7(self):
        \"\"\"Tests is_authorized 5\"\"\"
        if not is_never_authz(self.service_config):
            assert self.catalog.is_authorized(AGENT_ID, LOOKUP_RESOURCE_FUNCTION_ID, self.bin_id_list[7])
"""


class AuthorizationLookupSession:
    import_statements = [
        'from dlkit.abstract_osid.authorization.objects import AuthorizationList'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.authorization_list = list()
    request.cls.authorization_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'AUTHORIZATION',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_vault(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                LOOKUP_RESOURCE_FUNCTION_ID,
                Id(**{\'identifier\': str(num), \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
                [])
            create_form.display_name = 'Test Authorization ' + str(num)
            create_form.description = 'Test Authorization for AuthorizationLookupSession tests'
            object = request.cls.catalog.create_authorization(create_form)
            request.cls.authorization_list.append(object)
            request.cls.authorization_ids.append(object.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_vaults():
                for obj in catalog.get_authorizations():
                    catalog.delete_authorization(obj.ident)
                request.cls.svc_mgr.delete_vault(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    get_authorizations_for_function = """
        if not is_never_authz(self.service_config):
            results = self.session.get_authorizations_for_function(LOOKUP_RESOURCE_FUNCTION_ID)
            assert results.available() == 2
            assert isinstance(results, AuthorizationList)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_authorizations_for_function(LOOKUP_RESOURCE_FUNCTION_ID)"""


class AuthorizationForm:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'AUTHORIZATION',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_vault(create_form)
        request.cls.form = request.cls.catalog.get_authorization_form_for_create_for_agent(
            AGENT_ID,
            LOOKUP_RESOURCE_FUNCTION_ID,
            Id(**{\'identifier\': '1', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
            [])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_vaults():
                request.cls.svc_mgr.delete_vault(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""


class AuthorizationList:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'AUTHORIZATION',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_vault(create_form)
        request.cls.form = request.cls.catalog.get_authorization_form_for_create_for_agent(
            AGENT_ID,
            LOOKUP_RESOURCE_FUNCTION_ID,
            Id(**{\'identifier\': '1', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
            [])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_vaults():
                for authz in catalog.get_authorizations():
                    catalog.delete_authorization(authz.ident)
                request.cls.svc_mgr.delete_vault(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    from dlkit.json_.authorization.objects import AuthorizationList
    request.cls.authorization_list = list()
    request.cls.authorization_ids = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            form = request.cls.catalog.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                LOOKUP_RESOURCE_FUNCTION_ID,
                Id(**{\'identifier\': str(num), \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
                [])
            obj = request.cls.catalog.create_authorization(form)

            request.cls.authorization_list.append(obj)
            request.cls.authorization_ids.append(obj.ident)
        request.cls.authorization_list = AuthorizationList(request.cls.authorization_list)"""


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
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.authorization_list = list()
    request.cls.authorization_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'AUTHORIZATION',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationQuerySession tests'
        request.cls.catalog = request.cls.svc_mgr.create_vault(create_form)
        create_form = request.cls.catalog.get_authorization_form_for_create_for_agent(
            AGENT_ID,
            LOOKUP_RESOURCE_FUNCTION_ID,
            Id(**{\'identifier\': str('foo'), \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
            [])
        create_form.display_name = 'Test Authorization'
        create_form.description = (
            'Test Authorization for Authorization tests')
        obj = request.cls.catalog.create_authorization(create_form)
        request.cls.object = obj

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_vaults():
                for obj in catalog.get_authorizations():
                    catalog.delete_authorization(obj.ident)
                request.cls.svc_mgr.delete_vault(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""

    get_agent = """
        if not is_never_authz(self.service_config):
            # because we don't have Agency implemented in authentication
            with pytest.raises(AttributeError):
                self.object.get_agent()"""

    get_agent_id = """
        if not is_never_authz(self.service_config):
            result = self.object.get_agent_id()
            assert isinstance(result, Id)
            assert str(result) == str(AGENT_ID)"""

    get_function = """
        if not is_never_authz(self.service_config):
            # not supported
            with pytest.raises(errors.OperationFailed):
                self.object.get_function()"""

    get_function_id = """
        if not is_never_authz(self.service_config):
            result = self.object.get_function_id()
            assert isinstance(result, Id)
            assert str(result) == str(LOOKUP_RESOURCE_FUNCTION_ID)"""

    get_qualifier = """
        if not is_never_authz(self.service_config):
            # not supported
            with pytest.raises(errors.OperationFailed):
                self.object.get_qualifier()"""

    get_qualifier_id = """
        if not is_never_authz(self.service_config):
            result = self.object.get_qualifier_id()
            assert isinstance(result, Id)
            assert str(result) == 'resource.Resource%3Afoo%40ODL.MIT.EDU'"""

    has_agent = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.has_agent(), bool)"""

    get_trust = """
        if not is_never_authz(self.service_config):
            # no trust, so throws IllegalState
            with pytest.raises(errors.IllegalState):
                self.object.get_trust()"""

    get_trust_id = """
        if not is_never_authz(self.service_config):
            # no trust, so throws IllegalState
            with pytest.raises(errors.IllegalState):
                self.object.get_trust_id()"""

    has_trust = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.has_trust(), bool)"""

    get_resource = """
        if not is_never_authz(self.service_config):
            # no resource, so throws IllegalState
            with pytest.raises(errors.IllegalState):
                self.object.get_resource()"""

    get_resource_id = """
        if not is_never_authz(self.service_config):
            # no resource, so throws IllegalState
            with pytest.raises(errors.IllegalState):
                self.object.get_resource_id()"""

    has_resource = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.has_resource(), bool)"""

    is_implicit = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.is_implicit(), bool)"""


class AuthorizationQuerySession:

    init = """
class FakeQuery:
    _cat_id_args_list = []


@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.authorization_list = list()
    request.cls.authorization_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'AUTHORIZATION',
        proxy=PROXY,
        implementation=request.cls.service_config)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationQuerySession tests'
        request.cls.catalog = request.cls.svc_mgr.create_vault(create_form)
        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = request.cls.catalog.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                LOOKUP_RESOURCE_FUNCTION_ID,
                Id(**{\'identifier\': str(color), \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
                [])
            create_form.display_name = 'Test Authorization ' + color
            create_form.description = (
                'Test Authorization for AuthorizationQuerySession tests, did I mention green')
            obj = request.cls.catalog.create_authorization(create_form)
            request.cls.authorization_list.append(obj)
            request.cls.authorization_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_vaults():
                for obj in catalog.get_authorizations():
                    catalog.delete_authorization(obj.ident)
                request.cls.svc_mgr.delete_vault(catalog.ident)

    request.addfinalizer(test_tear_down)"""


class AuthorizationAdminSession:
    import_statements = [
        'from dlkit.abstract_osid.authorization.objects import Authorization',
        'from dlkit.abstract_osid.osid.objects import OsidForm',
        'from dlkit.abstract_osid.osid import errors',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})',
        'NEW_TYPE_2 = Type(**{\'identifier\': \'NEW 2\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.authorization_list = list()
    request.cls.authorization_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'AUTHORIZATION',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationAdminSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_vault(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                LOOKUP_RESOURCE_FUNCTION_ID,
                Id(**{\'identifier\': str(num), \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
                [])
            create_form.display_name = 'Test Authorization ' + str(num)
            create_form.description = 'Test Authorization for AuthorizationLookupSession tests'
            object = request.cls.catalog.create_authorization(create_form)
            request.cls.authorization_list.append(object)
            request.cls.authorization_ids.append(object.ident)

        request.cls.form = request.cls.catalog.get_authorization_form_for_create_for_agent(
            AGENT_ID,
            LOOKUP_RESOURCE_FUNCTION_ID,
            Id(**{\'identifier\': \'foo\', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
            [])
        request.cls.form.display_name = 'new Authorization'
        request.cls.form.description = 'description of Authorization'
        request.cls.form.genus_type = NEW_TYPE
        request.cls.osid_object = request.cls.catalog.create_authorization(request.cls.form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_vaults():
                for obj in catalog.get_authorizations():
                    catalog.delete_authorization(obj.ident)
                request.cls.svc_mgr.delete_vault(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    get_authorization_form_for_create = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                LOOKUP_RESOURCE_FUNCTION_ID,
                Id(**{\'identifier\': str(num), \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
                [])
            assert isinstance(form, OsidForm)
            assert not form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_authorization_form_for_create_for_agent(
                    AGENT_ID,
                    LOOKUP_RESOURCE_FUNCTION_ID,
                    Id(**{\'identifier\': str(num), \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
                    [])"""

    update_authorization = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_authorization_form_for_update(self.osid_object.ident)
            form.display_name = 'new name'
            form.description = 'new description'
            form.set_genus_type(NEW_TYPE_2)
            updated_object = self.catalog.update_authorization(form)
            assert isinstance(updated_object, Authorization)
            assert updated_object.ident == self.osid_object.ident
            assert updated_object.display_name.text == 'new name'
            assert updated_object.description.text == 'new description'
            assert updated_object.genus_type == NEW_TYPE_2
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.update_authorization('foo')"""

    delete_authorization = """
        if not is_never_authz(self.service_config):
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
            with pytest.raises(errors.NotFound):
                self.catalog.get_authorization(osid_object.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.delete_authorization(self.fake_id)"""

    get_authorization_form_for_create_for_agent = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                LOOKUP_RESOURCE_FUNCTION_ID,
                Id(**{\'identifier\': \'foo\', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
                [])
            assert isinstance(form, OsidForm)
            assert not form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_authorization_form_for_create_for_agent(
                    AGENT_ID,
                    LOOKUP_RESOURCE_FUNCTION_ID,
                    Id(**{\'identifier\': \'foo\', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
                    [])"""

    get_authorization_form_for_create_for_resource = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_authorization_form_for_create_for_resource(
                AGENT_ID,
                LOOKUP_RESOURCE_FUNCTION_ID,
                Id(**{\'identifier\': \'foo\', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
                [])
            assert isinstance(form, OsidForm)
            assert not form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_authorization_form_for_create_for_resource(
                    AGENT_ID,
                    LOOKUP_RESOURCE_FUNCTION_ID,
                    Id(**{\'identifier\': \'foo\', \'namespace\': \'resource.Resource\', \'authority\': \'ODL.MIT.EDU\'}),
                    [])"""


class AuthorizationVaultSession:

    init = """
@pytest.fixture(scope="class",
                params=['TEST_SERVICE', 'TEST_SERVICE_ALWAYS_AUTHZ', 'TEST_SERVICE_NEVER_AUTHZ', 'TEST_SERVICE_CATALOGING'])
def authorization_vault_session_class_fixture(request):
    # From test_templates/resource.py::ResourceBinSession::init_template
    request.cls.service_config = request.param
    request.cls.authorization_list = list()
    request.cls.authorization_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'AUTHORIZATION',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationVaultSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_vault(create_form)
        create_form = request.cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault for Assignment'
        create_form.description = 'Test Vault for AuthorizationVaultSession tests assignment'
        request.cls.assigned_catalog = request.cls.svc_mgr.create_vault(create_form)
        agent_id = Id(authority='TEST', namespace='authentication.Agent', identifier='A_USER')
        for num in [0, 1, 2]:
            # Note that the json authorization service seems picky about ids.  Need to review.
            func_namespace = 'resource.Resource'
            func_authority = 'TEST'
            if num == 1:
                func_identifier = 'lookup'
            elif num == 2:
                func_identifier = 'query'
            else:
                func_identifier = 'admin'
            function_id = Id(authority=func_authority, namespace=func_namespace, identifier=func_identifier)
            qualifier_id = Id(authority='TEST', namespace='authorization.Qualifier', identifier='TEST_' + str(num))
            create_form = request.cls.catalog.get_authorization_form_for_create_for_agent(agent_id, function_id, qualifier_id, [])
            create_form.display_name = 'Test Authorization ' + str(num)
            create_form.description = 'Test Authorization for AuthorizationVaultSession tests'
            obj = request.cls.catalog.create_authorization(create_form)
            request.cls.authorization_list.append(obj)
            request.cls.authorization_ids.append(obj.ident)
        request.cls.svc_mgr.assign_authorization_to_vault(
            request.cls.authorization_ids[1], request.cls.assigned_catalog.ident)
        request.cls.svc_mgr.assign_authorization_to_vault(
            request.cls.authorization_ids[2], request.cls.assigned_catalog.ident)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.unassign_authorization_from_vault(
                request.cls.authorization_ids[1], request.cls.assigned_catalog.ident)
            request.cls.svc_mgr.unassign_authorization_from_vault(
                request.cls.authorization_ids[2], request.cls.assigned_catalog.ident)
            for obj in request.cls.catalog.get_authorizations():
                request.cls.catalog.delete_authorization(obj.ident)
            request.cls.svc_mgr.delete_vault(request.cls.assigned_catalog.ident)
            request.cls.svc_mgr.delete_vault(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def authorization_vault_session_test_fixture(request):
    # From test_templates/resource.py::ResourceBinSession::init_template
    request.cls.session = request.cls.svc_mgr"""


class AuthorizationVaultAssignmentSession:

    init = """
@pytest.fixture(scope="class",
                params=['TEST_SERVICE', 'TEST_SERVICE_ALWAYS_AUTHZ', 'TEST_SERVICE_NEVER_AUTHZ', 'TEST_SERVICE_CATALOGING'])
def authorization_vault_assignment_session_class_fixture(request):
    # From test_templates/resource.py::ResourceBinAssignmentSession::init_template
    request.cls.service_config = request.param
    request.cls.authorization_list = list()
    request.cls.authorization_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'AUTHORIZATION',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationVaultAssignmentSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_vault(create_form)
        create_form = request.cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault for Assignment'
        create_form.description = 'Test Vault for AuthorizationVaultAssignmentSession tests assignment'
        request.cls.assigned_catalog = request.cls.svc_mgr.create_vault(create_form)
        agent_id = Id(authority='TEST', namespace='authentication.Agent', identifier='A_USER')
        for num in [0, 1, 2]:
            # Note that the json authorization service seems picky about ids.  Need to review.
            func_namespace = 'resource.Resource'
            func_authority = 'TEST'
            if num == 1:
                func_identifier = 'lookup'
            elif num == 2:
                func_identifier = 'query'
            else:
                func_identifier = 'admin'
            function_id = Id(authority=func_authority, namespace=func_namespace, identifier=func_identifier)
            qualifier_id = Id(authority='TEST', namespace='authorization.Qualifier', identifier='TEST_' + str(num))
            create_form = request.cls.catalog.get_authorization_form_for_create_for_agent(agent_id, function_id, qualifier_id, [])
            create_form.display_name = 'Test Authorization ' + str(num)
            create_form.description = 'Test Authorization for AuthorizationVaultAssignmentSession tests'
            obj = request.cls.catalog.create_authorization(create_form)
            request.cls.authorization_list.append(obj)
            request.cls.authorization_ids.append(obj.ident)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_authorizations():
                request.cls.catalog.delete_authorization(obj.ident)
            request.cls.svc_mgr.delete_vault(request.cls.assigned_catalog.ident)
            request.cls.svc_mgr.delete_vault(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def authorization_vault_assignment_session_test_fixture(request):
    # From test_templates/resource.py::ResourceBinAssignmentSession::init_template
    request.cls.session = request.cls.svc_mgr"""


class VaultNodeList:
    init = """"""
    get_next_vault_node = """"""

    get_next_vault_nodes = """"""


class VaultNode:
    init = """"""

    get_vault = """"""

    get_parent_vault_nodes = """"""

    get_child_vault_nodes = """"""
