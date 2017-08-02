"""TestAuthZ templates for assessment interfaces"""

class AssessmentOfferedLookupSession:

    additional_methods = """
@pytest.fixture(scope="function")
def authz_adapter_test_fixture(request):
    request.cls.${object_name_under}_id_lists = []
    count = 0
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.bank_list[0].get_assessment_form_for_create([])
        create_form.display_name = 'Assessment for AssessmentOffered Tests'
        create_form.description = 'Assessment for authz adapter tests for AssessmentOffered'
        request.cls.assessment = request.cls.bank_list[0].create_assessment(create_form)
        for ${cat_name_under}_ in request.cls.${cat_name_under}_list:
            request.cls.${object_name_under}_id_lists.append([])
            for color in ['Red', 'Blue', 'Red']:
                create_form = ${cat_name_under}_.get_${object_name_under}_form_for_create(request.cls.assessment.ident, [])
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
            request.cls.bank_list[0].delete_assessment(request.cls.assessment.ident)

    request.addfinalizer(test_tear_down)"""

class AssessmentTakenLookupSession:

    additional_methods = """
@pytest.fixture(scope="function")
def authz_adapter_test_fixture(request):
    request.cls.${object_name_under}_id_lists = []
    count = 0
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.bank_list[0].get_assessment_form_for_create([])
        create_form.display_name = 'Assessment for AssessmentOffered Tests'
        create_form.description = 'Assessment for authz adapter tests for AssessmentOffered'
        request.cls.assessment = request.cls.bank_list[0].create_assessment(create_form)
        create_form = request.cls.bank_list[0].get_assessment_offered_form_for_create(request.cls.assessment.ident, [])
        create_form.display_name = 'AssessmentOffered for AssessmentTaken Tests'
        create_form.description = 'AssessmentOffered for authz adapter tests for AssessmentTaken'
        request.cls.assessment_offered = request.cls.bank_list[0].create_assessment_offered(create_form)
        for ${cat_name_under}_ in request.cls.${cat_name_under}_list:
            request.cls.${object_name_under}_id_lists.append([])
            for color in ['Red', 'Blue', 'Red']:
                create_form = ${cat_name_under}_.get_${object_name_under}_form_for_create(request.cls.assessment_offered.ident, [])
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
            request.cls.bank_list[0].delete_assessment_offered(request.cls.assessment_offered.ident)
            request.cls.bank_list[0].delete_assessment(request.cls.assessment.ident)

    request.addfinalizer(test_tear_down)"""
