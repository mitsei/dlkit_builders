"""TestAuthZ templates for learning interfaces"""


class ActivityLookupSession:

    additional_methods = """
@pytest.fixture(scope="function")
def authz_adapter_test_fixture(request):
    request.cls.${object_name_under}_id_lists = []
    count = 0
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.objective_bank_list[0].get_objective_form_for_create([])
        create_form.display_name = 'Objective for Activity Tests'
        create_form.description = 'Objective for authz adapter tests for Activity'
        request.cls.objective = request.cls.objective_bank_list[0].create_objective(create_form)
        for ${cat_name_under}_ in request.cls.${cat_name_under}_list:
            request.cls.${object_name_under}_id_lists.append([])
            for color in ['Red', 'Blue', 'Red']:
                create_form = ${cat_name_under}_.get_${object_name_under}_form_for_create(request.cls.objective.ident, [])
                create_form.display_name = color + ' ' + str(count) + ' ${object_name}'
                create_form.description = color + ' ${object_name_under} for authz adapter tests from ${cat_name} number ' + str(count)
                if color == 'Blue':
                    create_form.genus_type = BLUE_TYPE
                ${object_name_under} = ${cat_name_under}_.create_${object_name_under}(create_form)
                if count == 2 and color == 'Blue':
                    request.cls.${pkg_name}_mgr.assign_${object_name_under}_to_${cat_name_under}(
                        ${object_name_under}.ident,
                        request.cls.${cat_name_under}_id_list[7])
                request.cls.${object_name_under}_id_lists[count].append(${object_name_under}.ident)
            count += 1

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for index, ${cat_name_under}_ in enumerate(request.cls.${cat_name_under}_list):
                for ${object_name_under}_id in request.cls.${object_name_under}_id_lists[index]:
                    ${cat_name_under}_.delete_${object_name_under}(${object_name_under}_id)
            request.cls.objective_bank_list[0].delete_objective(request.cls.objective.ident)

    request.addfinalizer(test_tear_down)"""
