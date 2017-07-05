
class AssessmentAuthoringManager:
    """Tests for AssessmentAuthoringManager"""
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for assessment.authoring manager tests'
        catalog = request.cls.svc_mgr.create_bank(create_form)
        request.cls.catalog_id = catalog.get_id()
        request.cls.mgr = Runtime().get_manager('ASSESSMENT_AUTHORING', 'TEST_JSON_1', (3, 0, 0))
    else:
        request.cls.catalog_id = Id('resource.Resource%3A000000000000000000000000%40DLKIT.MIT.EDU')

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_bank(request.cls.catalog_id)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""


class AssessmentAuthoringProxyManager:
    """Tests for AssessmentAuthoringProxyManager"""
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for assessment.authoring manager tests'
        catalog = request.cls.svc_mgr.create_bank(create_form)
        request.cls.catalog_id = catalog.get_id()
        request.cls.mgr = Runtime().get_manager('ASSESSMENT_AUTHORING', 'TEST_JSON_1', (3, 0, 0))
    else:
        request.cls.catalog_id = Id('resource.Resource%3A000000000000000000000000%40DLKIT.MIT.EDU')

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_bank(request.cls.catalog_id)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""


class AssessmentPartLookupSession:
    import_statements = [
        'from dlkit.abstract_osid.assessment_authoring import objects as ABCObjects'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3A000000000000000000000000%40DLKIT.MIT.EDU')


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.assessment_part_list = list()
    request.cls.assessment_part_ids = list()

    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPartLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        assessment_form = request.cls.catalog.get_assessment_form_for_create([])
        assessment_form.display_name = 'Test Assessment'
        assessment_form.description = 'Test Assessment for AssessmentPartLookupSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(assessment_form)

        for num in [0, 1, 2, 3]:
            create_form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident,
                                                                                                 [])
            create_form.display_name = 'Test AssessmentPart ' + str(num)
            create_form.description = 'Test AssessmentPart for AssessmentPartLookupSession tests'
            if num > 1:
                create_form.sequestered = True
            obj = request.cls.catalog.create_assessment_part_for_assessment(create_form)
            request.cls.assessment_part_list.append(obj)
            request.cls.assessment_part_ids.append(obj.ident)

        request.cls.assessment = request.cls.catalog.get_assessment(request.cls.assessment.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.catalog.use_unsequestered_assessment_part_view()
            for obj in request.cls.catalog.get_assessment_parts():
                request.cls.catalog.delete_assessment_part(obj.ident)
            request.cls.catalog.delete_assessment(request.cls.assessment.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(test_tear_down)"""

    get_assessment_parts_for_assessment = """
        # Override this because we do have AssessmentPartQuerySession implemented,
        #   so with NEVER_AUTHZ it returns an empty result set
        results = self.session.get_assessment_parts_for_assessment(self.assessment.ident)
        assert isinstance(results, ABCObjects.AssessmentPartList)
        if not is_never_authz(self.service_config):
            assert results.available() == 2
        else:
            assert results.available() == 0"""

    additional_methods = """
    def test_get_assessment_id(self):
        \"\"\"tests get_assessment_id\"\"\"
        if not is_never_authz(self.service_config):
            assert str(self.assessment_part_list[0].get_assessment_id()) == str(self.assessment.ident)

    def test_get_assessment(self):
        \"\"\"tests get_assessment\"\"\"
        def check_equal(val1, val2):
            assert val1 == val2

        def check_dict_equal(dict1, dict2):
            for item in dict1.items():
                key = item[0]
                value = item[1]
                if isinstance(value, dict):
                    check_dict_equal(value, dict2[key])
                else:
                    check_equal(value, dict2[key])

        if not is_never_authz(self.service_config):
            check_dict_equal(self.assessment_part_list[0].get_assessment().object_map,
                             self.assessment.object_map)"""

    get_bank_id = """
        # this should not be here...
        pass"""

    # Override these locally for AssessmentPart because with AssessmentPartQuerySession implemented,
    #   the authz adapter will return an empty List instead of throwing PermissionDenied
    get_assessment_part = """
        if not is_never_authz(self.service_config):
            self.catalog.use_isolated_bank_view()
            obj = self.catalog.get_assessment_part(self.assessment_part_list[0].ident)
            assert obj.ident == self.assessment_part_list[0].ident
            self.catalog.use_federated_bank_view()
            obj = self.catalog.get_assessment_part(self.assessment_part_list[0].ident)
            assert obj.ident == self.assessment_part_list[0].ident
        else:
            with pytest.raises(errors.NotFound):
                self.catalog.get_assessment_part(self.fake_id)"""

    get_assessment_parts_by_ids = """
        from dlkit.abstract_osid.assessment_authoring.objects import AssessmentPartList
        objects = self.catalog.get_assessment_parts_by_ids(self.assessment_part_ids)
        assert isinstance(objects, AssessmentPartList)
        self.catalog.use_federated_bank_view()
        objects = self.catalog.get_assessment_parts_by_ids(self.assessment_part_ids)
        assert isinstance(objects, AssessmentPartList)
        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0"""

    get_assessment_parts_by_genus_type = """
        from dlkit.abstract_osid.assessment_authoring.objects import AssessmentPartList
        objects = self.catalog.get_assessment_parts_by_genus_type(DEFAULT_GENUS_TYPE)
        assert isinstance(objects, AssessmentPartList)
        self.catalog.use_federated_bank_view()
        objects = self.catalog.get_assessment_parts_by_genus_type(DEFAULT_GENUS_TYPE)
        assert isinstance(objects, AssessmentPartList)
        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0"""

    get_assessment_parts_by_parent_genus_type = """
        from dlkit.abstract_osid.assessment_authoring.objects import AssessmentPartList
        if not is_never_authz(self.service_config):
            objects = self.catalog.get_assessment_parts_by_parent_genus_type(DEFAULT_GENUS_TYPE)
            assert isinstance(objects, AssessmentPartList)
            self.catalog.use_federated_bank_view()
            objects = self.catalog.get_assessment_parts_by_parent_genus_type(DEFAULT_GENUS_TYPE)
            assert objects.available() == 0
            assert isinstance(objects, AssessmentPartList)
        else:
            with pytest.raises(errors.Unimplemented):
                # because the never_authz "tries harder" and runs the actual query...
                #    whereas above the method itself in JSON returns an empty list
                self.catalog.get_assessment_parts_by_parent_genus_type(DEFAULT_GENUS_TYPE)"""

    get_assessment_parts_by_record_type = """
        from dlkit.abstract_osid.assessment_authoring.objects import AssessmentPartList
        objects = self.catalog.get_assessment_parts_by_record_type(DEFAULT_TYPE)
        assert isinstance(objects, AssessmentPartList)
        self.catalog.use_federated_bank_view()
        objects = self.catalog.get_assessment_parts_by_record_type(DEFAULT_TYPE)
        assert objects.available() == 0
        assert isinstance(objects, AssessmentPartList)"""

    get_assessment_parts = """
        from dlkit.abstract_osid.assessment_authoring.objects import AssessmentPartList
        objects = self.catalog.get_assessment_parts()
        assert isinstance(objects, AssessmentPartList)
        self.catalog.use_federated_bank_view()
        objects = self.catalog.get_assessment_parts()
        assert isinstance(objects, AssessmentPartList)

        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0

    def test_get_assessment_part_with_alias(self):
        if not is_never_authz(self.service_config):
            self.catalog.alias_assessment_part(self.assessment_part_ids[0], ALIAS_ID)
            obj = self.catalog.get_assessment_part(ALIAS_ID)
            assert obj.get_id() == self.assessment_part_ids[0]"""


class AssessmentPartQuerySession:

    init = """
class FakeQuery:
    _cat_id_args_list = []


@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.assessment_part_list = list()
    request.cls.assessment_part_ids = list()

    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPartQuerySession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        assessment_form = request.cls.catalog.get_assessment_form_for_create([])
        assessment_form.display_name = 'Test Assessment'
        assessment_form.description = 'Test Assessment for AssessmentPartQuerySession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(assessment_form)

        colors = ['Orange', 'Blue', 'Green', 'orange']

        for num in [0, 1, 2, 3]:
            create_form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident,
                                                                                                 [])
            create_form.display_name = 'Test AssessmentPart ' + str(num) + colors[num]
            create_form.description = 'Test AssessmentPart for AssessmentPartQuerySession tests'
            obj = request.cls.catalog.create_assessment_part_for_assessment(create_form)
            request.cls.assessment_part_list.append(obj)
            request.cls.assessment_part_ids.append(obj.ident)

        request.cls.assessment = request.cls.catalog.get_assessment(request.cls.assessment.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.catalog.use_unsequestered_assessment_part_view()
            for obj in request.cls.catalog.get_assessment_parts():
                request.cls.catalog.delete_assessment_part(obj.ident)
            request.cls.catalog.delete_assessment(request.cls.assessment.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(test_tear_down)"""


class AssessmentPartItemSession:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT_AUTHORING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.item_list = list()
    request.cls.item_ids = list()
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPartItemSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentPartItemSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        create_form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part'
        create_form.description = 'Test Assessment Part for AssessmentPartItemSession tests'
        request.cls.assessment_part = request.cls.catalog.create_assessment_part_for_assessment(create_form)
        for num in [0, 1, 2, 3]:
            create_form = request.cls.catalog.get_item_form_for_create([])
            create_form.display_name = 'Test Item ' + str(num)
            create_form.description = 'Test Item for AssessmentPartItemSession tests'
            obj = request.cls.catalog.create_item(create_form)
            request.cls.item_list.append(obj)
            request.cls.item_ids.append(obj.ident)
            request.cls.catalog.add_item(obj.ident, request.cls.assessment_part.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_banks():
                for obj in catalog.get_assessment_parts():
                    if obj.has_children():
                        for child_id in obj.get_child_assessment_part_ids():
                            catalog.delete_assessment_part(child_id)
                    catalog.delete_assessment_part(obj.ident)
                for obj in catalog.get_assessments():
                    catalog.delete_assessment(obj.ident)
                for obj in catalog.get_items():
                    catalog.delete_item(obj.ident)
                request.cls.svc_mgr.delete_bank(catalog.ident)

    request.addfinalizer(test_tear_down)"""

    can_access_assessment_part_items = """
        assert isinstance(self.session.can_access_assessment_part_items(), bool)"""


class AssessmentPartItemDesignSession:
    import_statements = [
        'from random import shuffle'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.item_list = list()
    request.cls.item_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT_AUTHORING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPartItemDesignSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)
        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentPartItemDesignSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        create_form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part'
        create_form.description = 'Test Assessment Part for AssessmentPartItemDesignSession tests'
        request.cls.assessment_part = request.cls.catalog.create_assessment_part_for_assessment(create_form)
        for num in [0, 1, 2, 3]:
            create_form = request.cls.catalog.get_item_form_for_create([])
            create_form.display_name = 'Test Item ' + str(num)
            create_form.description = 'Test Item for AssessmentPartItemDesignSession tests'
            obj = request.cls.catalog.create_item(create_form)
            request.cls.item_list.append(obj)
            request.cls.item_ids.append(obj.ident)
            request.cls.catalog.add_item(obj.ident, request.cls.assessment_part.ident)

        request.cls.assessment = request.cls.catalog.get_assessment(request.cls.assessment.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_banks():
                for obj in catalog.get_assessment_parts():
                    catalog.delete_assessment_part(obj.ident)
                for obj in catalog.get_assessments():
                    catalog.delete_assessment(obj.ident)
                for obj in catalog.get_items():
                    catalog.delete_item(obj.ident)
                request.cls.svc_mgr.delete_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    add_item = """
        if not is_never_authz(self.service_config):
            assert self.catalog.get_assessment_part_items(self.assessment_part.ident).available() == 4

            create_form = self.catalog.get_item_form_for_create([])
            create_form.display_name = 'Test Item 5'
            create_form.description = 'Test Item for AssessmentPartItemDesignSession tests'
            obj = self.catalog.create_item(create_form)
            self.session.add_item(obj.ident, self.assessment_part.ident)

            assert self.catalog.get_assessment_part_items(self.assessment_part.ident).available() == 5
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.add_item(self.fake_id, self.fake_id)"""

    can_design_assessment_parts = """
        assert isinstance(self.session.can_design_assessment_parts(), bool)"""

    move_item_ahead = """
        if not is_never_authz(self.service_config):
            original_item_order = list(self.catalog.get_assessment_part_items(self.assessment_part.ident))
            original_ids = [item.ident for item in original_item_order]
            self.session.move_item_ahead(original_ids[-1],
                                         self.assessment_part.ident,
                                         original_ids[0])
            expected_order = [original_ids[-1]] + original_ids[0:-1]
            new_order = [item.ident for item in self.catalog.get_assessment_part_items(self.assessment_part.ident)]
            assert new_order == expected_order
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.move_item_ahead(self.fake_id, self.fake_id, self.fake_id)"""

    move_item_behind = """
        if not is_never_authz(self.service_config):
            original_item_order = list(self.catalog.get_assessment_part_items(self.assessment_part.ident))
            original_ids = [item.ident for item in original_item_order]
            self.session.move_item_behind(original_ids[0],
                                          self.assessment_part.ident,
                                          original_ids[-1])
            expected_order = original_ids[1::] + [original_ids[0]]
            new_order = [item.ident for item in self.catalog.get_assessment_part_items(self.assessment_part.ident)]
            assert new_order == expected_order
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.move_item_behind(self.fake_id, self.fake_id, self.fake_id)"""

    order_items = """
        if not is_never_authz(self.service_config):
            original_item_order = list(self.catalog.get_assessment_part_items(self.assessment_part.ident))
            original_ids = [item.ident for item in original_item_order]
            shuffle(original_ids)
            self.session.order_items(original_ids,
                                     self.assessment_part.ident)
            new_order = [item.ident for item in self.catalog.get_assessment_part_items(self.assessment_part.ident)]
            assert new_order == original_ids
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.order_items(self.fake_id, self.fake_id)"""

    remove_item = """
        if not is_never_authz(self.service_config):
            original_item_order = list(self.catalog.get_assessment_part_items(self.assessment_part.ident))
            original_ids = [item.ident for item in original_item_order]
            self.session.remove_item(original_ids[0],
                                     self.assessment_part.ident)
            new_order = [item.ident for item in self.catalog.get_assessment_part_items(self.assessment_part.ident)]
            assert new_order == original_ids[1::]
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.remove_item(self.fake_id, self.fake_id)"""


class SequenceRuleLookupSession:
    import_statements = [
        'from dlkit.primordium.type.primitives import Type',
        'SIMPLE_SEQUENCE_RECORD_TYPE = Type(**{"authority": "ODL.MIT.EDU", "namespace": "osid-object", "identifier": "simple-child-sequencing"})'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.sequence_rule_list = list()
    request.cls.sequence_rule_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for SequenceRuleLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        create_form = request.cls.catalog.get_assessment_form_for_create([SIMPLE_SEQUENCE_RECORD_TYPE])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for SequenceRuleLookupSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        create_form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 1'
        create_form.description = 'Test Assessment Part for SequenceRuleLookupSession tests'
        request.cls.assessment_part_1 = request.cls.catalog.create_assessment_part_for_assessment(create_form)

        create_form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 2'
        create_form.description = 'Test Assessment Part for SequenceRuleLookupSession tests'
        assessment_part_2 = request.cls.catalog.create_assessment_part_for_assessment(create_form)

        for num in [0, 1]:
            create_form = request.cls.catalog.get_sequence_rule_form_for_create(request.cls.assessment_part_1.ident,
                                                                                assessment_part_2.ident,
                                                                                [])
            create_form.display_name = 'Test Sequence Rule ' + str(num)
            create_form.description = 'Test Sequence Rule for SequenceRuleLookupSession tests'
            obj = request.cls.catalog.create_sequence_rule(create_form)
            request.cls.sequence_rule_list.append(obj)
            request.cls.sequence_rule_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_banks():
                for obj in catalog.get_sequence_rules():
                    catalog.delete_sequence_rule(obj.ident)
                for obj in catalog.get_assessment_parts():
                    catalog.delete_assessment_part(obj.ident)
                for obj in catalog.get_assessments():
                    catalog.delete_assessment(obj.ident)
                request.cls.svc_mgr.delete_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog
    request.cls.assessment_part = request.cls.assessment_part_1"""

    get_sequence_rules = """
        # Override this because we haven't implemented SequenceRuleQuerySession, so will
        #   throw PermissionDenied with NEVER_AUTHZ
        from dlkit.abstract_osid.assessment_authoring.objects import SequenceRuleList
        if not is_never_authz(self.service_config):
            objects = self.catalog.get_sequence_rules()
            assert isinstance(objects, SequenceRuleList)
            self.catalog.use_federated_bank_view()
            objects = self.catalog.get_sequence_rules()
            assert isinstance(objects, SequenceRuleList)
            assert objects.available() > 0
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_sequence_rules()"""

    get_sequence_rules_by_record_type = """
        # Override this because we haven't implemented SequenceRuleQuerySession, so will
        #   throw PermissionDenied with NEVER_AUTHZ
        from dlkit.abstract_osid.assessment_authoring.objects import SequenceRuleList
        if not is_never_authz(self.service_config):
            objects = self.catalog.get_sequence_rules_by_record_type(DEFAULT_TYPE)
            assert isinstance(objects, SequenceRuleList)
            self.catalog.use_federated_bank_view()
            objects = self.catalog.get_sequence_rules_by_record_type(DEFAULT_TYPE)
            assert objects.available() == 0
            assert isinstance(objects, SequenceRuleList)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_sequence_rules_by_record_type(DEFAULT_TYPE)"""

    get_sequence_rules_by_parent_genus_type = """
        # Override this because we haven't implemented SequenceRuleQuerySession, so will
        #   throw PermissionDenied with NEVER_AUTHZ
        from dlkit.abstract_osid.assessment_authoring.objects import SequenceRuleList
        if not is_never_authz(self.service_config):
            objects = self.catalog.get_sequence_rules_by_parent_genus_type(DEFAULT_GENUS_TYPE)
            assert isinstance(objects, SequenceRuleList)
            self.catalog.use_federated_bank_view()
            objects = self.catalog.get_sequence_rules_by_parent_genus_type(DEFAULT_GENUS_TYPE)
            assert objects.available() == 0
            assert isinstance(objects, SequenceRuleList)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_sequence_rules_by_parent_genus_type(DEFAULT_GENUS_TYPE)"""

    get_sequence_rules_by_genus_type = """
        # Override this because we haven't implemented SequenceRuleQuerySession, so will
        #   throw PermissionDenied with NEVER_AUTHZ
        from dlkit.abstract_osid.assessment_authoring.objects import SequenceRuleList
        if not is_never_authz(self.service_config):
            objects = self.catalog.get_sequence_rules_by_genus_type(DEFAULT_GENUS_TYPE)
            assert isinstance(objects, SequenceRuleList)
            self.catalog.use_federated_bank_view()
            objects = self.catalog.get_sequence_rules_by_genus_type(DEFAULT_GENUS_TYPE)
            assert isinstance(objects, SequenceRuleList)
            assert objects.available() > 0
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_sequence_rules_by_genus_type(DEFAULT_GENUS_TYPE)"""

    get_sequence_rules_by_ids = """
        # Override this because we haven't implemented SequenceRuleQuerySession, so will
        #   throw PermissionDenied with NEVER_AUTHZ
        from dlkit.abstract_osid.assessment_authoring.objects import SequenceRuleList
        if not is_never_authz(self.service_config):
            objects = self.catalog.get_sequence_rules_by_ids(self.sequence_rule_ids)
            assert isinstance(objects, SequenceRuleList)
            self.catalog.use_federated_bank_view()
            objects = self.catalog.get_sequence_rules_by_ids(self.sequence_rule_ids)
            assert isinstance(objects, SequenceRuleList)
            assert objects.available() > 0
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_sequence_rules_by_ids(self.sequence_rule_ids)"""

    get_sequence_rule = """
        # Override this because we haven't implemented SequenceRuleQuerySession, so will
        #   throw PermissionDenied with NEVER_AUTHZ
        if not is_never_authz(self.service_config):
            self.catalog.use_isolated_bank_view()
            obj = self.catalog.get_sequence_rule(self.sequence_rule_list[0].ident)
            assert obj.ident == self.sequence_rule_list[0].ident
            self.catalog.use_federated_bank_view()
            obj = self.catalog.get_sequence_rule(self.sequence_rule_list[0].ident)
            assert obj.ident == self.sequence_rule_list[0].ident
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_sequence_rule(self.fake_id)"""


class SequenceRule:
    import_statements = [
        'from dlkit.abstract_osid.assessment_authoring.objects import AssessmentPart',
        'from dlkit.json_.id.objects import IdList',
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.sequence_rule_list = list()
    request.cls.sequence_rule_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for SequenceRule tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for SequenceRule tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        create_form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 1'
        create_form.description = 'Test Assessment Part for SequenceRule tests'
        request.cls.assessment_part_1 = request.cls.catalog.create_assessment_part_for_assessment(create_form)

        create_form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 2'
        create_form.description = 'Test Assessment Part for SequenceRule tests'
        request.cls.assessment_part_2 = request.cls.catalog.create_assessment_part_for_assessment(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessment_parts():
                request.cls.catalog.delete_assessment_part(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        form = request.cls.catalog.get_sequence_rule_form_for_create(request.cls.assessment_part_1.ident,
                                                                     request.cls.assessment_part_2.ident,
                                                                     [])
        request.cls.object = request.cls.catalog.create_sequence_rule(form)"""

    get_applied_assessment_part_ids = """
        if not is_never_authz(self.service_config):
            result = self.object.get_applied_assessment_part_ids()
            assert isinstance(result, IdList)
            assert result.available() == 0"""

    get_assessment_part = """
        if not is_never_authz(self.service_config):
            part = self.object.get_assessment_part()
            assert isinstance(part, AssessmentPart)
            assert str(part.ident) == str(self.assessment_part_1.ident)"""

    get_assessment_part_id = """
        if not is_never_authz(self.service_config):
            part_id = self.object.get_assessment_part_id()
            assert isinstance(part_id, Id)
            assert str(part_id) == str(self.assessment_part_1.ident)"""


class SequenceRuleForm:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.sequence_rule_list = list()
    request.cls.sequence_rule_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for SequenceRuleForm tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for SequenceRuleForm tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        create_form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 1'
        create_form.description = 'Test Assessment Part for SequenceRuleForm tests'
        request.cls.assessment_part_1 = request.cls.catalog.create_assessment_part_for_assessment(create_form)

        create_form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 2'
        create_form.description = 'Test Assessment Part for SequenceRuleForm tests'
        request.cls.assessment_part_2 = request.cls.catalog.create_assessment_part_for_assessment(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessment_parts():
                request.cls.catalog.delete_assessment_part(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        request.cls.form = request.cls.catalog.get_sequence_rule_form_for_create(request.cls.assessment_part_1.ident,
                                                                                 request.cls.assessment_part_2.ident,
                                                                                 [])
        request.cls.object = request.cls.form"""

    set_cumulative = """
        if not is_never_authz(self.service_config):
            create_form = self.catalog.get_sequence_rule_form_for_create(self.assessment_part_1.ident,
                                                                         self.assessment_part_2.ident,
                                                                         [])
            create_form.set_cumulative(True)
            assert create_form._my_map['cumulative']"""

    get_applied_assessment_parts_metadata = """"""  # so this doesn't build from the template


class SequenceRuleList:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.sequence_rule_list = list()
    request.cls.sequence_rule_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for SequenceRuleList tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for SequenceRuleList tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        create_form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 1'
        create_form.description = 'Test Assessment Part for SequenceRuleList tests'
        request.cls.assessment_part_1 = request.cls.catalog.create_assessment_part_for_assessment(create_form)

        create_form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 2'
        create_form.description = 'Test Assessment Part for SequenceRuleList tests'
        request.cls.assessment_part_2 = request.cls.catalog.create_assessment_part_for_assessment(create_form)

        request.cls.form = request.cls.catalog.get_sequence_rule_form_for_create(request.cls.assessment_part_1.ident,
                                                                                 request.cls.assessment_part_2.ident,
                                                                                 [])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_sequence_rules():
                request.cls.catalog.delete_sequence_rule(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    from dlkit.json_.assessment_authoring.objects import SequenceRuleList
    request.cls.sequence_rule_list = list()
    request.cls.sequence_rule_ids = list()

    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            form = request.cls.catalog.get_sequence_rule_form_for_create(request.cls.assessment_part_1.ident,
                                                                         request.cls.assessment_part_2.ident,
                                                                         [])
            obj = request.cls.catalog.create_sequence_rule(form)

            request.cls.sequence_rule_list.append(obj)
            request.cls.sequence_rule_ids.append(obj.ident)
        request.cls.sequence_rule_list = SequenceRuleList(request.cls.sequence_rule_list)"""


class SequenceRuleQuery:
    import_statements = [
        'from dlkit.json_.assessment_authoring.queries import SequenceRuleQuery'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for SequenceRuleQuery tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_sequence_rules():
                request.cls.catalog.delete_sequence_rule(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # Since the session isn't implemented, we just construct an SequenceRuleQuery directly
    if not is_never_authz(request.cls.service_config):
        request.cls.query = SequenceRuleQuery(runtime=request.cls.catalog._runtime)"""


class SequenceRuleAdminSession:
    import_statements = [
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
    request.cls.sequence_rule_list = list()
    request.cls.sequence_rule_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for SequenceRuleAdminSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        create_form = request.cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for SequenceRuleAdminSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(create_form)
        create_form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 1'
        create_form.description = 'Test Assessment Part for SequenceRuleAdminSession tests'
        request.cls.assessment_part_1 = request.cls.catalog.create_assessment_part_for_assessment(create_form)

        create_form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident, [])
        create_form.display_name = 'Test Assessment Part 2'
        create_form.description = 'Test Assessment Part for SequenceRuleAdminSession tests'
        request.cls.assessment_part_2 = request.cls.catalog.create_assessment_part_for_assessment(create_form)

        for num in [0, 1]:
            create_form = request.cls.catalog.get_sequence_rule_form_for_create(request.cls.assessment_part_1.ident,
                                                                                request.cls.assessment_part_2.ident,
                                                                                [])
            create_form.display_name = 'Test Sequence Rule ' + str(num)
            create_form.description = 'Test Sequence Rule for SequenceRuleAdminSession tests'
            obj = request.cls.catalog.create_sequence_rule(create_form)
            request.cls.sequence_rule_list.append(obj)
            request.cls.sequence_rule_ids.append(obj.ident)

        create_form = request.cls.catalog.get_sequence_rule_form_for_create(request.cls.assessment_part_1.ident,
                                                                            request.cls.assessment_part_2.ident,
                                                                            [])
        create_form.display_name = 'new SequenceRule'
        create_form.description = 'description of SequenceRule'
        create_form.genus_type = NEW_TYPE
        request.cls.osid_object = request.cls.catalog.create_sequence_rule(create_form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_sequence_rules():
                request.cls.catalog.delete_sequence_rule(obj.ident)
            for obj in request.cls.catalog.get_assessment_parts():
                request.cls.catalog.delete_assessment_part(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    get_sequence_rule_form_for_create = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_sequence_rule_form_for_create(self.assessment_part_1.ident,
                                                                  self.assessment_part_2.ident,
                                                                  [])
            assert isinstance(form, OsidForm)
            assert not form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_sequence_rule_form_for_create(self.fake_id, self.fake_id, [])"""

    delete_sequence_rule = """
        if not is_never_authz(self.service_config):
            create_form = self.catalog.get_sequence_rule_form_for_create(self.assessment_part_1.ident,
                                                                         self.assessment_part_2.ident,
                                                                         [])
            create_form.display_name = 'new SequenceRule'
            create_form.description = 'description of SequenceRule'
            create_form.genus_type = NEW_TYPE
            osid_object = self.catalog.create_sequence_rule(create_form)
            self.catalog.delete_sequence_rule(osid_object.ident)
            with pytest.raises(errors.NotFound):
                self.catalog.get_sequence_rule(osid_object.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.delete_sequence_rule(self.fake_id)"""


class AssessmentPart:
    import_statements = [
        'from dlkit.abstract_osid.assessment.objects import Assessment',
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.json_.id.objects import IdList',
        'SIMPLE_SEQUENCE_RECORD_TYPE = Type(**{"authority": "ODL.MIT.EDU", "namespace": "osid-object", "identifier": "simple-child-sequencing"})'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.assessment_part_list = list()
    request.cls.assessment_part_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPart tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        assessment_form = request.cls.catalog.get_assessment_form_for_create([])
        assessment_form.display_name = 'Test Assessment'
        assessment_form.description = 'Test Assessment for AssessmentPart tests'
        request.cls.assessment = request.cls.catalog.create_assessment(assessment_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.catalog.use_unsequestered_assessment_part_view()
            request.cls.catalog.delete_assessment(request.cls.assessment.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident,
                                                                                      [])
        request.cls.object = request.cls.catalog.create_assessment_part_for_assessment(form)
        request.cls.assessment = request.cls.catalog.get_assessment(request.cls.assessment.ident)

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for assessment_part in request.cls.catalog.get_assessment_parts_for_assessment(request.cls.assessment.ident):
                if assessment_part.has_children():
                    for child_id in assessment_part.get_child_ids():
                        try:
                            request.cls.catalog.delete_assessment_part(child_id)
                        except errors.NotFound:
                            pass
                request.cls.catalog.delete_assessment_part(assessment_part.ident)

    request.addfinalizer(test_tear_down)"""

    get_assessment = """
        if not is_never_authz(self.service_config):
            result = self.object.get_assessment()
            assert isinstance(result, Assessment)
            assert str(result.ident) == str(self.assessment.ident)"""

    get_assessment_id = """
        if not is_never_authz(self.service_config):
            result_id = self.object.get_assessment_id()
            assert isinstance(result_id, Id)
            assert str(result_id) == str(self.assessment.ident)"""

    get_assessment_part = """
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.IllegalState):
                self.object.get_assessment_part()"""

    get_assessment_part_id = """
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.IllegalState):
                self.object.get_assessment_part_id()"""

    get_child_assessment_part_ids = """
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.IllegalState):
                self.object.get_child_assessment_part_ids()

            # to get these back, need to have a simple sequencing part as the parent
            form = self.catalog.get_assessment_part_form_for_create_for_assessment(self.assessment.ident,
                                                                                   [SIMPLE_SEQUENCE_RECORD_TYPE])
            form.set_children([Id('assessment.Part%3A000000000000000000000000%40ODL.MIT.EDU')])
            parent_part = self.catalog.create_assessment_part_for_assessment(form)

            results = parent_part.get_child_assessment_part_ids()
            assert isinstance(results, IdList)
            assert results.available() == 1
            assert str(results.next()) == 'assessment.Part%3A000000000000000000000000%40ODL.MIT.EDU'"""

    get_child_assessment_parts = """
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.IllegalState):
                self.object.get_child_assessment_parts()

            # to get these back, need to have a simple sequencing part as the parent

            form = self.catalog.get_assessment_part_form_for_create_for_assessment(self.assessment.ident,
                                                                                   [SIMPLE_SEQUENCE_RECORD_TYPE])
            parent_part = self.catalog.create_assessment_part_for_assessment(form)

            form = self.catalog.get_assessment_part_form_for_create_for_assessment_part(parent_part.ident,
                                                                                        [])
            child_part = self.catalog.create_assessment_part_for_assessment(form)

            parent_part = self.catalog.get_assessment_part(parent_part.ident)

            results = parent_part.get_child_assessment_part_ids()
            assert isinstance(results, IdList)
            assert results.available() == 1
            assert str(results.next()) == str(child_part.ident)"""

    has_parent_part = """
        if not is_never_authz(self.service_config):
            assert isinstance(self.object.has_parent_part(), bool)"""


class AssessmentPartForm:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.assessment_part_list = list()
    request.cls.assessment_part_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPartForm tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        assessment_form = request.cls.catalog.get_assessment_form_for_create([])
        assessment_form.display_name = 'Test Assessment'
        assessment_form.description = 'Test Assessment for AssessmentPartForm tests'
        request.cls.assessment = request.cls.catalog.create_assessment(assessment_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.catalog.use_unsequestered_assessment_part_view()
            request.cls.catalog.delete_assessment(request.cls.assessment.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        request.cls.form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident,
                                                                                                  [])
        request.cls.object = request.cls.form
        request.cls.assessment = request.cls.catalog.get_assessment(request.cls.assessment.ident)"""


class AssessmentPartList:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.assessment_part_list = list()
    request.cls.assessment_part_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPartList tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        assessment_form = request.cls.catalog.get_assessment_form_for_create([])
        assessment_form.display_name = 'Test Assessment'
        assessment_form.description = 'Test Assessment for AssessmentPartList tests'
        request.cls.assessment = request.cls.catalog.create_assessment(assessment_form)

        request.cls.form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident,
                                                                                                  [])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.catalog.use_unsequestered_assessment_part_view()
            request.cls.catalog.delete_assessment(request.cls.assessment.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    from dlkit.json_.assessment_authoring.objects import AssessmentPartList
    request.cls.assessment_part_list = list()
    request.cls.assessment_part_ids = list()

    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident, [])

            obj = request.cls.catalog.create_assessment_part_for_assessment(form)

            request.cls.assessment_part_list.append(obj)
            request.cls.assessment_part_ids.append(obj.ident)
        request.cls.assessment_part_list = AssessmentPartList(request.cls.assessment_part_list)"""


class AssessmentPartQuery:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.assessment_part_list = list()
    request.cls.assessment_part_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPartQuery tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        assessment_form = request.cls.catalog.get_assessment_form_for_create([])
        assessment_form.display_name = 'Test Assessment'
        assessment_form.description = 'Test Assessment for AssessmentPartQuery tests'
        request.cls.assessment = request.cls.catalog.create_assessment(assessment_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.catalog.use_unsequestered_assessment_part_view()
            request.cls.catalog.delete_assessment(request.cls.assessment.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        request.cls.query = request.cls.catalog.get_assessment_part_query()"""


class AssessmentPartAdminSession:
    import_statements = [
        'from dlkit.abstract_osid.assessment_authoring import objects as ABCObjects',
        'from dlkit.primordium.type.primitives import Type',
        'SIMPLE_SEQUENCE_RECORD_TYPE = Type(**{"authority": "ODL.MIT.EDU", "namespace": "osid-object", "identifier": "simple-child-sequencing"})'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'ASSESSMENT',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentPartAdminSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_bank(create_form)

        assessment_form = request.cls.catalog.get_assessment_form_for_create([])
        assessment_form.display_name = 'Test Assessment'
        assessment_form.description = 'Test Assessment for AssessmentPartAdminSession tests'
        request.cls.assessment = request.cls.catalog.create_assessment(assessment_form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_assessment_parts():
                request.cls.catalog.delete_assessment_part(obj.ident)
            for obj in request.cls.catalog.get_assessments():
                request.cls.catalog.delete_assessment(obj.ident)
            request.cls.svc_mgr.delete_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        form = request.cls.catalog.get_assessment_part_form_for_create_for_assessment(request.cls.assessment.ident,
                                                                                      [SIMPLE_SEQUENCE_RECORD_TYPE])
        form.display_name = 'new AssessmentPart'
        form.description = 'description of AssessmentPart'
        form.set_genus_type(NEW_TYPE)
        request.cls.osid_object = request.cls.catalog.create_assessment_part_for_assessment(form)
    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.osid_object = request.cls.catalog.get_assessment_part(request.cls.osid_object.ident)
            if request.cls.osid_object.has_children():
                for child_id in request.cls.osid_object.get_child_assessment_part_ids():
                    request.cls.catalog.delete_assessment_part(child_id)
            request.cls.catalog.delete_assessment_part(request.cls.osid_object.ident)

    request.addfinalizer(test_tear_down)"""

    delete_assessment_part = """
        if not is_never_authz(self.service_config):
            results = self.catalog.get_assessment_parts()
            assert results.available() == 1

            form = self.catalog.get_assessment_part_form_for_create_for_assessment(self.assessment.ident,
                                                                                   [])
            form.display_name = 'new AssessmentPart'
            form.description = 'description of AssessmentPart'
            new_assessment_part = self.catalog.create_assessment_part_for_assessment(form)

            results = self.catalog.get_assessment_parts()
            assert results.available() == 2

            self.session.delete_assessment_part(new_assessment_part.ident)

            results = self.catalog.get_assessment_parts()
            assert results.available() == 1
            assert str(results.next().ident) != str(new_assessment_part.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.delete_assessment_part(self.fake_id)"""

    get_assessment_part_form_for_create_for_assessment = """
        if not is_never_authz(self.service_config):
            form = self.session.get_assessment_part_form_for_create_for_assessment(self.assessment.ident, [])
            assert isinstance(form, ABCObjects.AssessmentPartForm)
            assert not form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_assessment_part_form_for_create_for_assessment(self.fake_id, [])"""

    get_assessment_part_form_for_create_for_assessment_part = """
        if not is_never_authz(self.service_config):
            form = self.session.get_assessment_part_form_for_create_for_assessment_part(self.osid_object.ident, [])
            assert isinstance(form, ABCObjects.AssessmentPartForm)
            assert not form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.get_assessment_part_form_for_create_for_assessment_part(self.fake_id, [])"""

    update_assessment_part = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_assessment_part_form_for_update(self.osid_object.ident)
            form.display_name = 'new name'
            form.description = 'new description'
            form.set_genus_type(NEW_TYPE_2)
            updated_object = self.catalog.update_assessment_part(self.osid_object.ident, form)
            assert isinstance(updated_object, ABCObjects.AssessmentPart)
            assert updated_object.ident == self.osid_object.ident
            assert updated_object.display_name.text == 'new name'
            assert updated_object.description.text == 'new description'
            assert updated_object.genus_type == NEW_TYPE_2
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.update_assessment_part(self.fake_id, 'foo')"""

    create_assessment_part_for_assessment = """
        from dlkit.abstract_osid.assessment_authoring.objects import AssessmentPart
        if not is_never_authz(self.service_config):
            assert isinstance(self.osid_object, AssessmentPart)
            assert self.osid_object.display_name.text == 'new AssessmentPart'
            assert self.osid_object.description.text == 'description of AssessmentPart'
            assert self.osid_object.genus_type == NEW_TYPE

            form = self.catalog.get_assessment_part_form_for_create_for_assessment_part(self.osid_object.ident, [])
            form.display_name = 'new AssessmentPart child'
            form.description = 'description of AssessmentPart child'
            child_part = self.catalog.create_assessment_part_for_assessment_part(form)

            parent_part = self.catalog.get_assessment_part(self.osid_object.ident)
            assert parent_part.has_children()
            assert parent_part.get_child_assessment_part_ids().available() == 1
            assert str(parent_part.get_child_assessment_part_ids().next()) == str(child_part.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.create_assessment_part_for_assessment_part('foo')"""
