"""TestAuthZ templates for authorization interfaces"""


class AuthorizationLookupSession:

    additional_methods = """
@pytest.fixture(scope="function")
def authz_adapter_test_fixture(request):
    request.cls.authorization_id_lists = []
    count = 0
    if not is_never_authz(request.cls.service_config):
        agent_id = Id(authority='TEST', namespace='authentication.Agent', identifier='A_USER')
        for vault_ in request.cls.vault_list:
            request.cls.authorization_id_lists.append([])
            for color in ['Red', 'Blue', 'Another Red']:
                # Note that the json authorization service seems picky about ids.  Need to review.
                func_namespace = 'resource.Resource'
                func_authority = 'TEST'
                if color == 'Red':
                    func_identifier = 'lookup'
                elif color == 'Blue':
                    func_identifier = 'query'
                else:
                    func_identifier = 'admin'
                function_id = Id(authority=func_authority, namespace=func_namespace, identifier=func_identifier)
                qualifier_id = Id(authority='TEST', namespace='authorization.Qualifier', identifier='TEST' + str(count) + color)
                create_form = vault_.get_authorization_form_for_create_for_agent(agent_id, function_id, qualifier_id, [])
                create_form.display_name = color + ' ' + str(count) + ' Authorization'
                create_form.description = color + ' authorization for authz adapter tests from Vault number ' + str(count)
                if color == 'Blue':
                    create_form.genus_type = BLUE_TYPE
                authorization = vault_.create_authorization(create_form)
                if count == 2 and color == 'Blue':
                    request.cls.authorization_mgr.assign_authorization_to_vault(
                        authorization.ident,
                        request.cls.vault_id_list[7])
                request.cls.authorization_id_lists[count].append(authorization.ident)
            count += 1

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for index, vault_ in enumerate(request.cls.vault_list):
                for authorization_id in request.cls.authorization_id_lists[index]:
                    vault_.delete_authorization(authorization_id)

    request.addfinalizer(test_tear_down)"""
