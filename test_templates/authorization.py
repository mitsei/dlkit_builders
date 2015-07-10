
class AuthorizationSession:

    init = """
"""

    is_authorized = """
        pass"""

class AuthorizationLookupSession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.authorization_list = list()
        cls.authorization_ids = list()
        cls.repo_mgr = Runtime().get_service_manager('AUTHORIZATION', proxy=PROXY, implementation='TEST_SERVICE')

        create_form = cls.repo_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository 1'
        create_form.description = 'Test Repository for AuthorizationLookupSession tests'
        cls.repo_one = cls.repo_mgr.create_repository(create_form)

        create_form = cls.repo_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository 2'
        create_form.description = 'Test Repository for AuthorizationLookupSession tests'
        cls.repo_two = cls.repo_mgr.create_repository(create_form)

        cls.svc_mgr = Runtime().get_service_manager('AUTHORIZATION', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationLookupSession tests'
        cls.catalog = cls.svc_mgr.create_vault(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_authorization_form_for_create(AGENT_ID, [])
            create_form.display_name = 'Test Authorization ' + str(num)
            create_form.description = 'Test Authorization for AuthorizationLookupSession tests'
            object = cls.catalog.create_authorization(create_form)
            cls.authorization_list.append(object)
            cls.authorization_ids.append(object.ident)
"""

class Authorization:
    pass