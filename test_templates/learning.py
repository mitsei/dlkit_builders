
class ObjectiveRequisiteSession:

    import_statements_pattern = [
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.requisite_list = list()
    request.cls.requisite_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ObjectiveRequisiteSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)
        create_form = request.cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for ObjectiveRequisiteSession Lookup'
        create_form.description = 'Test Objective for ObjectiveRequisiteSession tests'
        request.cls.objective = request.cls.catalog.create_objective(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveRequisiteSession tests'
            obj = request.cls.catalog.create_objective(create_form)
            request.cls.requisite_list.append(obj)
            request.cls.requisite_ids.append(obj.ident)
            request.cls.catalog.assign_objective_requisite(request.cls.objective.ident, obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj_id in request.cls.requisite_ids:
                    catalog.delete_objective(obj_id)
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    get_requisite_objectives_template = """
        # From test_templates/learning.py::ObjectiveRequsiteSession::get_requisite_objectives_template
        if not is_never_authz(self.service_config):
            requisites = self.catalog.${method_name}(self.${object_name_under}.ident)
            assert requisites.available() == len(self.requisite_ids)
            for req in requisites:
                assert req.ident in self.requisite_ids
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id)"""

    get_dependent_objectives_template = """
        # From test_templates/learning.py::ObjectiveRequsiteSession::get_dependent_objectives_template
        if not is_never_authz(self.service_config):
            dependents = self.catalog.${method_name}(self.${object_name_under}.ident)
            assert dependents.available() == 0
            dependents = self.catalog.get_dependent_objectives(self.requisite_ids[0])
            assert dependents.available() == 1
            assert dependents.next().ident == self.objective.ident
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id)"""


class ObjectiveRequisiteAssignmentSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.${pkg_name_replaced_reserved} import objects as ABCObjects',
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.requisite_list = list()
    request.cls.requisite_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ObjectiveRequisiteAssignmentSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)
        create_form = request.cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for ObjectiveRequisiteAssignmentSession Lookup'
        create_form.description = 'Test Objective for ObjectiveRequisiteAssignmentSession tests'
        request.cls.objective = request.cls.catalog.create_objective(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveRequisiteAssignmentSession tests'
            obj = request.cls.catalog.create_objective(create_form)
            request.cls.requisite_list.append(obj)
            request.cls.requisite_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj_id in request.cls.requisite_ids:
                    catalog.delete_objective(obj_id)
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    assign_objective_requisite_template = """
        # From test_templates/learning.py::ObjectiveRequsiteAssignmentSession::assign_objective_requisite_template
        if not is_never_authz(self.service_config):
            results = self.catalog.get_requisite_${object_name_plural_under}(self.${object_name_under}.ident)
            assert isinstance(results, ABCObjects.${object_name}List)
            assert results.available() == 0

            self.catalog.${method_name}(self.${object_name_under}.ident, self.requisite_ids[0])

            results = self.catalog.get_requisite_${object_name_plural_under}(self.${object_name_under}.ident)
            assert results.available() == 1
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id, self.fake_id)"""

    unassign_objective_requisite_template = """
        # From test_templates/learning.py::ObjectiveRequsiteAssignmentSession::unassign_objective_requisite_template
        if not is_never_authz(self.service_config):
            self.catalog.assign_${object_name_under}_requisite(self.${object_name_under}.ident, self.requisite_ids[0])

            results = self.catalog.get_requisite_${object_name_plural_under}(self.${object_name_under}.ident)
            assert results.available() == 1

            self.catalog.${method_name}(self.${object_name_under}.ident, self.requisite_ids[0])

            results = self.catalog.get_requisite_${object_name_plural_under}(self.${object_name_under}.ident)
            assert results.available() == 0
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id, self.fake_id)"""


class ObjectiveHierarchyDesignSession:
    import_statements = [
        'from dlkit.abstract_osid.learning.objects import ObjectiveList'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ObjectiveHierarchyDesignSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.child_list = list()
    request.cls.child_ids = list()
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for ObjectiveHierarchyDesignSession Lookup'
        create_form.description = 'Test Objective for ObjectiveHierarchyDesignSession tests'
        request.cls.objective = request.cls.catalog.create_objective(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveHierarchyDesignSession tests'
            obj = request.cls.catalog.create_objective(create_form)
            request.cls.child_list.append(obj)
            request.cls.child_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)
    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj_id in request.cls.child_ids:
                request.cls.catalog.delete_objective(obj_id)
            for obj in request.cls.catalog.get_objectives():
                request.cls.catalog.delete_objective(obj.ident)

    request.addfinalizer(test_tear_down)"""

    add_child_objective = """
        if not is_never_authz(self.service_config):
            self.catalog.add_root_objective(self.objective.ident)
    
            with pytest.raises(errors.IllegalState):
                self.catalog.get_child_objectives(self.objective.ident)
    
            self.catalog.add_child_objective(self.objective.ident, self.child_ids[0])
    
            children = self.catalog.get_child_objectives(self.objective.ident)
            assert children.available() == 1
            assert isinstance(children, ObjectiveList)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.add_child_objective(self.fake_id, self.fake_id)"""

    add_root_objective = """
        if not is_never_authz(self.service_config):
            roots = self.catalog.get_root_objectives()
            assert roots.available() == 0
            assert isinstance(roots, ObjectiveList)
    
            self.catalog.add_root_objective(self.objective.ident)
            roots = self.catalog.get_root_objectives()
            assert roots.available() == 1
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.add_root_objective(self.fake_id)"""

    can_modify_objective_hierarchy = """
        assert isinstance(self.catalog.can_modify_objective_hierarchy(), bool)"""

    remove_child_objective = """
        if not is_never_authz(self.service_config):
            self.catalog.add_root_objective(self.objective.ident)
            self.catalog.add_child_objective(self.objective.ident, self.child_ids[0])
    
            children = self.catalog.get_child_objectives(self.objective.ident)
            assert children.available() == 1
    
            self.catalog.remove_child_objective(self.objective.ident, self.child_ids[0])
    
            with pytest.raises(errors.IllegalState):
                self.catalog.get_child_objectives(self.objective.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.remove_child_objective(self.fake_id, self.fake_id)"""

    remove_child_objectives = """
        if not is_never_authz(self.service_config):
            self.catalog.add_root_objective(self.objective.ident)
            self.catalog.add_child_objective(self.objective.ident, self.child_ids[0])
            self.catalog.add_child_objective(self.objective.ident, self.child_ids[1])
    
            children = self.catalog.get_child_objectives(self.objective.ident)
            assert children.available() == 2
    
            self.catalog.remove_child_objectives(self.objective.ident)
    
            with pytest.raises(errors.IllegalState):
                self.catalog.get_child_objectives(self.objective.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.remove_child_objectives(self.fake_id)"""

    remove_root_objective = """
        if not is_never_authz(self.service_config):
            self.catalog.add_root_objective(self.objective.ident)
    
            roots = self.catalog.get_root_objectives()
            assert roots.available() == 1
    
            self.catalog.remove_root_objective(self.objective.ident)
    
            roots = self.catalog.get_root_objectives()
            assert roots.available() == 0
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.remove_root_objectives(self.fake_id)"""


class ObjectiveHierarchySession:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ObjectiveHierarchySession tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.child_list = list()
    request.cls.child_ids = list()
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for ObjectiveHierarchySession Lookup'
        create_form.description = 'Test Objective for ObjectiveHierarchySession tests'
        request.cls.objective = request.cls.catalog.create_objective(create_form)
        request.cls.catalog.add_root_objective(request.cls.objective.ident)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveHierarchySession tests'
            obj = request.cls.catalog.create_objective(create_form)
            request.cls.child_list.append(obj)
            request.cls.child_ids.append(obj.ident)
            request.cls.catalog.add_child_objective(request.cls.objective.ident, obj.ident)
    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj_id in request.cls.child_ids:
                request.cls.catalog.delete_objective(obj_id)
            for obj in self.catalog.get_objectives():
                request.cls.catalog.delete_objective(obj.ident)

    request.addfinalizer(test_tear_down)"""

    get_child_objectives = """
        if not is_never_authz(self.service_config):
            children = self.catalog.get_child_objectives(self.objective.ident)
            assert children.available() == 2
            assert isinstance(children, ObjectiveList)
            assert str(children.next().ident) == str(self.child_ids[0])
            assert str(children.next().ident) == str(self.child_ids[1])
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_child_objectives(self.fake_id)"""

    get_root_objectives = """
        if not is_never_authz(self.service_config):
            roots = self.catalog.get_root_objectives()
            assert roots.available() == 1
            assert isinstance(roots, ObjectiveList)
            assert str(roots.next().ident) == str(self.objective.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_root_objectives()"""


class ObjectiveAdminSession:

    import_statements_pattern = [
    ]

    delete_objective_template = """
        # From test_templates/learning.py::ObjectiveAdminSession::delete_objective_template
        if not is_never_authz(self.service_config):
            results = self.catalog.get_${object_name_under}s()
            assert results.available() == 1
    
            form = self.catalog.get_${object_name_under}_form_for_create([])
            form.display_name = 'new ${object_name}'
            form.description = 'description of ${object_name}'
            new_${object_name_under} = self.catalog.create_${object_name_under}(form)
    
            results = self.catalog.get_${object_name_under}s()
            assert results.available() == 2
    
            self.session.${method_name}(new_${object_name_under}.ident)
    
            results = self.catalog.get_${object_name_under}s()
            assert results.available() == 1
            assert str(results.next().ident) != str(new_${object_name_under}.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id)"""


class ObjectiveSequencingSession:
    import_statements_pattern = [
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.child_list = list()
    request.cls.child_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ObjectiveSequencingSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.objective_list = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            create_form = request.cls.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveSequencingSession tests'
            obj = request.cls.catalog.create_objective(create_form)
            request.cls.objective_list.append(obj)

    request.cls.session = request.cls.catalog

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj_id in request.cls.child_ids:
                request.cls.catalog.delete_objective(obj_id)
            for obj in request.cls.catalog.get_objectives():
                request.cls.catalog.delete_objective(obj.ident)

    request.addfinalizer(test_tear_down)"""


class ObjectiveNodeList:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ObjectiveNodeList tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)

    request.cls.objective_node_ids = list()

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_objectives():
                request.cls.catalog.delete_objective(obj.ident)
            request.cls.svc_mgr.delete_objective_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    from dlkit.json_.learning.objects import ObjectiveNodeList, ObjectiveNode
    request.cls.objective_node_list = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            create_form = request.cls.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveNodeList tests'
            obj = request.cls.catalog.create_objective(create_form)
            request.cls.objective_node_list.append(ObjectiveNode(obj.object_map))
            request.cls.objective_node_ids.append(obj.ident)
        # Not put the objectives in a hierarchy
        request.cls.catalog.add_root_objective(request.cls.objective_node_list[0].ident)
        request.cls.catalog.add_child_objective(
            request.cls.objective_node_list[0].ident,
            request.cls.objective_node_list[1].ident)
    request.cls.objective_node_list = ObjectiveNodeList(request.cls.objective_node_list)"""


class ObjectiveNode:

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ObjectiveNode tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_objectives():
                request.cls.catalog.delete_objective(obj.ident)
            request.cls.svc_mgr.delete_objective_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    from dlkit.json_.learning.objects import ObjectiveNode
    request.cls.objective_node_list = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            create_form = request.cls.catalog.get_objective_form_for_create([])
            create_form.display_name = 'Test Objective ' + str(num)
            create_form.description = 'Test Objective for ObjectiveNodeList tests'
            obj = request.cls.catalog.create_objective(create_form)
            request.cls.objective_node_list.append(ObjectiveNode(obj.object_map))
        # Now put the objectives in a hierarchy
        request.cls.catalog.add_root_objective(request.cls.objective_node_list[0].ident)
        request.cls.catalog.add_child_objective(
            request.cls.objective_node_list[0].ident,
            request.cls.objective_node_list[1].ident)
        request.cls.object = ObjectiveNode(request.cls.objective_node_list[0])"""


class ActivityLookupSession:
    import_statements = [
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.activity_list = list()
    request.cls.activity_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ActivityLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)
        create_form = request.cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for Activity Lookup'
        create_form.description = 'Test Objective for ActivityLookupSession tests'
        request.cls.objective = request.cls.catalog.create_objective(create_form)
        for num in [0, 1]:
            create_form = request.cls.catalog.get_activity_form_for_create(cls.objective.ident, [])
            create_form.display_name = 'Test Activity ' + str(num)
            create_form.description = 'Test Activity for ActivityLookupSession tests'
            obj = request.cls.catalog.create_activity(create_form)
            request.cls.activity_list.append(obj)
            request.cls.activity_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj in catalog.get_activities():
                    catalog.delete_activity(obj.ident)
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    get_activities_for_objective_template = """
        # From test_templates/learning.py::ActivityLookupSession::get_activities_for_objective_template
        if not is_never_authz(self.service_config):
            results = self.session.${method_name}(self.${arg0_object_under}.ident)
            assert results.available() == 2
            assert isinstance(results, ABCObjects.${return_type_list_object}List)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.session.${method_name}(self.fake_id)"""


class ActivityObjectiveBankSession:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.activity_list = list()
    request.cls.activity_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ActivityObjectiveBankSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)
    
        create_form = request.cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for ActivIty Lookup'
        create_form.description = 'Test Objective for ActivityLookupSession tests'
        request.cls.objective = request.cls.catalog.create_objective(create_form)
    
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank for Assignment'
        create_form.description = 'Test ObjectiveBank for ActivityObjectiveBankSession tests assignment'
        request.cls.assigned_catalog = request.cls.svc_mgr.create_objective_bank(create_form)
        for num in [0, 1, 2]:
            create_form = request.cls.catalog.get_activity_form_for_create(request.cls.objective.ident, [])
            create_form.display_name = 'Test Activity ' + str(num)
            create_form.description = 'Test Activity for ActivityObjectiveBankSession tests'
            obj = request.cls.catalog.create_activity(create_form)
            request.cls.activity_list.append(obj)
            request.cls.activity_ids.append(obj.ident)
        request.cls.svc_mgr.assign_activity_to_objective_bank(
            request.cls.activity_ids[1], request.cls.assigned_catalog.ident)
        request.cls.svc_mgr.assign_activity_to_objective_bank(
            request.cls.activity_ids[2], request.cls.assigned_catalog.ident)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.unassign_activity_from_objective_bank(
                request.cls.activity_ids[1], request.cls.assigned_catalog.ident)
            request.cls.svc_mgr.unassign_activity_from_objective_bank(
                request.cls.activity_ids[2], request.cls.assigned_catalog.ident)
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj in catalog.get_activities():
                    catalog.delete_activity(obj.ident)
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.svc_mgr"""


class ActivityObjectiveBankAssignmentSession:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.activity_list = list()
    request.cls.activity_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ActivityObjectiveBankAssignmentSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank for Assignment'
        create_form.description = 'Test ObjectiveBank for ActivityObjectiveBankAssignmentSession tests assignment'
        request.cls.assigned_catalog = request.cls.svc_mgr.create_objective_bank(create_form)
    
        create_form = request.cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for Assignment'
        create_form.description = 'Test Objective for ActivityObjectiveBankAssignmentSession tests assignment'
        request.cls.objective = request.cls.catalog.create_objective(create_form)
    
        for num in [0, 1, 2]:
            create_form = request.cls.catalog.get_activity_form_for_create(request.cls.objective.ident, [])
            create_form.display_name = 'Test Activity ' + str(num)
            create_form.description = 'Test Activity for ActivityObjectiveBankAssignmentSession tests'
            obj = request.cls.catalog.create_activity(create_form)
            request.cls.activity_list.append(obj)
            request.cls.activity_ids.append(obj.ident)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_activities():
                request.cls.catalog.delete_activity(obj.ident)
            for obj in request.cls.catalog.get_objectives():
                request.cls.catalog.delete_objective(obj.ident)
            request.cls.svc_mgr.delete_objective_bank(request.cls.assigned_catalog.ident)
            request.cls.svc_mgr.delete_objective_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.svc_mgr"""


class ActivityAdminSession:

    import_statements_pattern = [
        'from dlkit.abstract_osid.osid.objects import OsidForm',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.activity_list = list()
    request.cls.activity_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ActivityLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)
        create_form = request.cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for Activity Lookup'
        create_form.description = 'Test Objective for ActivityLookupSession tests'
        request.cls.objective = request.cls.catalog.create_objective(create_form)
        request.cls.parent_object = request.cls.objective
        for num in [0, 1]:
            create_form = request.cls.catalog.get_activity_form_for_create(request.cls.objective.ident, [])
            create_form.display_name = 'Test Activity ' + str(num)
            create_form.description = 'Test Activity for ActivityLookupSession tests'
            obj = request.cls.catalog.create_activity(create_form)
            request.cls.activity_list.append(obj)
            request.cls.activity_ids.append(obj.ident)
    
        create_form = request.cls.catalog.get_activity_form_for_create(request.cls.objective.ident, [])
        create_form.display_name = 'new Activity'
        create_form.description = 'description of Activity'
        create_form.genus_type = NEW_TYPE
        request.cls.osid_object = request.cls.catalog.create_activity(create_form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj in catalog.get_activities():
                    catalog.delete_activity(obj.ident)
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""

    get_activity_form_for_create_template = """
        # From test_templates/learning.py::ActivityAdminSession::get_activity_form_for_create_template
        if not is_never_authz(self.service_config):
            form = self.catalog.${method_name}(self.parent_object.ident, [])
            assert isinstance(form, OsidForm)
            assert not form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.${method_name}(self.fake_id, [])"""

    delete_activity = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_activity_form_for_create(self.parent_object.ident, [])
            form.display_name = 'new Activity'
            form.description = 'description of Activity'
            form.set_genus_type(NEW_TYPE)
            osid_object = self.catalog.create_activity(form)
            self.catalog.delete_activity(osid_object.ident)
            with pytest.raises(errors.NotFound):
                self.catalog.get_activity(osid_object.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.delete_activity(self.fake_id)"""


class Activity:

    import_statements_pattern = [
        'from dlkit.abstract_osid.${pkg_name_replaced_reserved} import objects as ABCObjects',
        'from dlkit.json_.id.objects import IdList',
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)

        form = request.cls.catalog.get_objective_form_for_create([])
        form.display_name = 'Objective'
        request.cls.objective = request.cls.catalog.create_objective(form)

        form = request.cls.catalog.get_activity_form_for_create(request.cls.objective.ident,
                                                                [])
        form.display_name = 'Test activity'
        request.cls.object = request.cls.catalog.create_activity(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_activities():
                request.cls.catalog.delete_activity(obj.ident)
            request.cls.catalog.delete_objective(request.cls.objective.ident)
            request.cls.svc_mgr.delete_objective_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""

    get_assessment_ids = """
        if not is_never_authz(self.service_config):
            result = self.object.get_assessment_ids()
            assert isinstance(result, IdList)
            assert result.available() == 0"""

    get_assessments = """
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.IllegalState):
                self.object.get_assessments()"""

    get_asset_ids_template = """
        # From test_templates/learning.py::Activity::get_asset_ids_template
        if not is_never_authz(self.service_config):
            result = self.object.${method_name}()
            assert isinstance(result, IdList)
            assert result.available() == 0"""

    get_assets_template = """
        # From test_templates/learning.py::Activity::get_assets_template
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.IllegalState):
                self.object.${method_name}()"""

    get_course_ids = """
        if not is_never_authz(self.service_config):
            result = self.object.get_course_ids()
            assert isinstance(result, IdList)
            assert result.available() == 0"""

    get_courses = """
        if not is_never_authz(self.service_config):
            # We don't have the course service yet
            with pytest.raises(errors.IllegalState):
                self.object.get_courses()"""

    get_objective_template = """
        # From test_templates/learning.py::Activity::get_objective_template
        if not is_never_authz(self.service_config):
            result = self.object.${method_name}()
            assert isinstance(result, ABCObjects.${return_type})
            assert str(result.ident) == str(self.${return_type_under}.ident)"""

    get_objective_id_template = """
        # From test_templates/learning.py::Activity::get_objective_id_template
        if not is_never_authz(self.service_config):
            result = self.object.${method_name}()
            assert isinstance(result, Id)
            assert str(result) == str(self.${var_name}.ident)"""


class ActivityForm:
    import_statements_pattern = [
        'from dlkit.json_.osid.metadata import Metadata',
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/learning.py::ActivityForm::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ActivityForm tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)
        create_form = request.cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for Activity Lookup'
        create_form.description = 'Test Objective for ActivityForm tests'
        request.cls.objective = request.cls.catalog.create_objective(create_form)

        request.cls.form = request.cls.catalog.get_activity_form_for_create(request.cls.objective.ident, [])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj in catalog.get_activities():
                    catalog.delete_activity(obj.ident)
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""

    get_assets_metadata_template = """
        # From test_templates/learning.py::ActivityForm::get_assets_metadata_template
        if not is_never_authz(self.service_config):
            assert isinstance(self.form.${method_name}(), Metadata)"""

    set_assets_template = """
        # From test_templates/learning.py::ActivityForm::set_assets_template
        if not is_never_authz(self.service_config):
            test_id = Id('osid.Osid%3A1%40ODL.MIT.EDU')
            self.form.${method_name}([test_id])
            assert len(self.form._my_map['${var_name_singular_mixed}Ids']) == 1
            assert self.form._my_map['${var_name_singular_mixed}Ids'][0] == str(test_id)
            with pytest.raises(errors.InvalidArgument):
                self.form.${method_name}('this is not a list')
            # reset this for other tests
            self.form._my_map['${var_name_singular_mixed}Ids'] = list()"""

    clear_assets_template = """
        # From test_templates/learning.py::ActivityForm::clear_assets_template
        if not is_never_authz(self.service_config):
            test_id = Id('osid.Osid%3A1%40ODL.MIT.EDU')
            self.form.set_${var_name}([test_id])
            assert len(self.form._my_map['${var_name_singular_mixed}Ids']) == 1
            assert self.form._my_map['${var_name_singular_mixed}Ids'][0] == str(test_id)
            self.form.${method_name}()
            assert self.form._my_map['${var_name_singular_mixed}Ids'] == []"""


class ActivityList:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ActivityList tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)
        create_form = request.cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for Activity Lookup'
        create_form.description = 'Test Objective for ActivityList tests'
        request.cls.objective = request.cls.catalog.create_objective(create_form)

        request.cls.form = request.cls.catalog.get_activity_form_for_create(request.cls.objective.ident, [])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj in catalog.get_activities():
                    catalog.delete_activity(obj.ident)
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    from dlkit.json_.learning.objects import ActivityList
    request.cls.activity_list = list()
    request.cls.activity_ids = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            form = request.cls.catalog.get_activity_form_for_create(request.cls.objective.ident, [])
            form.display_name = 'Test Activity ' + str(num)
            form.description = 'Test Activity for ActivityList tests'
            obj = request.cls.catalog.create_activity(form)

            request.cls.activity_list.append(obj)
            request.cls.activity_ids.append(obj.ident)
    request.cls.activity_list = ActivityList(request.cls.activity_list)"""


class ActivityQuery:
    import_statements = [
        'from dlkit.json_.learning.queries import ActivityQuery'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ActivityLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)
        create_form = request.cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for Activity Lookup'
        create_form.description = 'Test Objective for ActivityLookupSession tests'
        request.cls.objective = request.cls.catalog.create_objective(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj in catalog.get_activities():
                    catalog.delete_activity(obj.ident)
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # Since the session isn't implemented, we just construct an ActivityQuery directly
    if not is_never_authz(request.cls.service_config):
        request.cls.query = ActivityQuery(runtime=request.cls.catalog._runtime)"""


class ProficiencyQuerySession:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.proficiency_list = list()
    request.cls.proficiency_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ProficiencyQuerySession tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)
    
        form = request.cls.catalog.get_objective_form_for_create([])
        form.display_name = "Test LO"
        objective = request.cls.catalog.create_objective(form)
    
        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = request.cls.catalog.get_proficiency_form_for_create(objective.ident, AGENT_ID, [])
            create_form.display_name = 'Test Proficiency ' + color
            create_form.description = (
                'Test Proficiency for ProficiencyQuerySession tests, did I mention green')
            obj = request.cls.catalog.create_proficiency(create_form)
            request.cls.proficiency_list.append(obj)
            request.cls.proficiency_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj in catalog.get_proficiencies():
                    catalog.delete_proficiency(obj.ident)
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""


class ProficiencyLookupSession:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.proficiency_list = list()
    request.cls.proficiency_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ProficiencyLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)
    
        form = request.cls.catalog.get_objective_form_for_create([])
        form.display_name = "Test LO"
        objective = request.cls.catalog.create_objective(form)
    
        for color in ['Orange', 'Blue']:
            create_form = request.cls.catalog.get_proficiency_form_for_create(objective.ident, AGENT_ID, [])
            create_form.display_name = 'Test Proficiency ' + color
            create_form.description = (
                'Test Proficiency for ProficiencyLookupSession tests, did I mention green')
            obj = request.cls.catalog.create_proficiency(create_form)
            request.cls.proficiency_list.append(obj)
            request.cls.proficiency_ids.append(obj.ident)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj in catalog.get_proficiencies():
                    catalog.delete_proficiency(obj.ident)
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""


class ProficiencyForm:
    import_statements = [
        'from dlkit.primordium.id.primitives import Id'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ProficiencyForm tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)

        form = request.cls.catalog.get_objective_form_for_create([])
        form.display_name = "Test LO"
        request.cls.objective = request.cls.catalog.create_objective(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj in catalog.get_proficiencies():
                    catalog.delete_proficiency(obj.ident)
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    if not is_never_authz(request.cls.service_config):
        request.cls.form = request.cls.catalog.get_proficiency_form_for_create(request.cls.objective.ident, AGENT_ID, [])
        request.cls.object = request.cls.form"""

    clear_completion = """
        if not is_never_authz(self.service_config):
            self.form.set_completion(50.0)
            assert self.form._my_map['completion'] is not None
            self.form.clear_completion()
            assert self.form._my_map['completion'] is None"""

    set_completion = """
        if not is_never_authz(self.service_config):
            assert self.form._my_map['completion'] is None
            self.form.set_completion(50.0)
            assert self.form._my_map['completion'] is not None"""

    clear_level = """
        if not is_never_authz(self.service_config):
            self.form.set_level(Id('grading.Grade%3Afake%40ODL.MIT.EDU'))
            assert self.form._my_map['level'] is not None
            self.form.clear_level()
            assert self.form._my_map['level'] == ''"""

    set_level = """
        # This is a slightly hokey test, because the spec seems to have a typo
        if not is_never_authz(self.service_config):
            assert self.form._my_map['levelId'] == ''
            self.form.set_level(Id('grading.Grade%3Afake%40ODL.MIT.EDU'))
            assert self.form._my_map['level'] is not None"""


class ProficiencyList:
    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ProficiencyList tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)

        form = request.cls.catalog.get_objective_form_for_create([])
        form.display_name = "Test LO"
        request.cls.objective = request.cls.catalog.create_objective(form)

        request.cls.form = request.cls.catalog.get_proficiency_form_for_create(request.cls.objective.ident, AGENT_ID, [])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj in catalog.get_proficiencies():
                    catalog.delete_proficiency(obj.ident)
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    from dlkit.json_.learning.objects import ProficiencyList
    request.cls.proficiency_list = list()
    request.cls.proficiency_ids = list()
    if not is_never_authz(request.cls.service_config):
        for num in [0, 1]:
            form = request.cls.catalog.get_proficiency_form_for_create(request.cls.objective.ident, AGENT_ID, [])
            form.display_name = 'Test Proficiency ' + str(num)
            form.description = 'Test Proficiency for ProficiencyList tests'
            obj = request.cls.catalog.create_proficiency(form)

            request.cls.proficiency_list.append(obj)
            request.cls.proficiency_ids.append(obj.ident)
    request.cls.proficiency_list = ProficiencyList(request.cls.proficiency_list)"""


class Proficiency:
    import_statements = [
        'from dlkit.abstract_osid.learning.objects import Objective',
        'from dlkit.runtime import PROXY_SESSION, proxy_example',
        'from dlkit.runtime.managers import Runtime',
        'REQUEST = proxy_example.SimpleRequest()',
        'CONDITION = PROXY_SESSION.get_proxy_condition()',
        'CONDITION.set_http_request(REQUEST)',
        'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
        'from dlkit.primordium.type.primitives import Type',
        'from dlkit.primordium.id.primitives import Id',
        'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
        'AGENT_ID = Id(**{\'identifier\': \'jane_doe\', \'namespace\': \'osid.agent.Agent\', \'authority\': \'MIT-ODL\'})',
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)

        form = request.cls.catalog.get_objective_form_for_create([])
        form.display_name = 'Objective'
        request.cls.objective = request.cls.catalog.create_objective(form)

        form = request.cls.catalog.get_proficiency_form_for_create(request.cls.objective.ident,
                                                                   AGENT_ID,
                                                                   [])
        form.display_name = 'Test proficiency'
        request.cls.object = request.cls.catalog.create_proficiency(form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for obj in request.cls.catalog.get_proficiencies():
                request.cls.catalog.delete_proficiency(obj.ident)
            request.cls.catalog.delete_objective(request.cls.objective.ident)
            request.cls.svc_mgr.delete_objective_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""

    get_completion = """
        if not is_never_authz(self.service_config):
            score = self.object.get_completion()
            assert score is None

            # if this is set, should be a Decimal
            form = self.catalog.get_proficiency_form_for_create(self.objective.ident,
                                                                AGENT_ID,
                                                                [])
            form.set_completion(0.0)
            new_proficiency = self.catalog.create_proficiency(form)

            assert new_proficiency.get_completion() == 0.0"""

    get_objective = """
        if not is_never_authz(self.service_config):
            result = self.object.get_objective()
            assert isinstance(result, Objective)
            assert str(result.ident) == str(self.objective.ident)"""


class ProficiencyQuery:
    match_completion = """
        if not is_never_authz(self.service_config):
            start = float(0.0)
            end = float(100.0)
            if is_no_authz(self.service_config):
                assert 'completion' not in self.query._query_terms
            self.query.match_completion(start, end, True)
            if is_no_authz(self.service_config):
                assert self.query._query_terms['completion'] == {
                    '$gte': start,
                    '$lte': end
                }"""

    match_minimum_completion = """
        if not is_never_authz(self.service_config):
            with pytest.raises(errors.Unimplemented):
                self.query.match_minimum_completion(float(50.0), True)"""


class ProficiencyAdminSession:
    import_statements_pattern = [
        'from dlkit.abstract_osid.osid.objects import OsidForm',
        'NEW_TYPE = Type(**{\'identifier\': \'NEW\', \'namespace\': \'MINE\', \'authority\': \'YOURS\'})'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.proficiency_list = list()
    request.cls.proficiency_ids = list()
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    request.cls.fake_id = Id('resource.Resource%3Afake%40DLKIT.MIT.EDU')
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ProficiencyLookupSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)
    
        form = request.cls.catalog.get_objective_form_for_create([])
        form.display_name = "Test LO"
        request.cls.objective = request.cls.catalog.create_objective(form)

        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = request.cls.catalog.get_proficiency_form_for_create(request.cls.objective.ident, AGENT_ID, [])
            create_form.display_name = 'Test Proficiency ' + color
            create_form.description = (
                'Test Proficiency for ProficiencyLookupSession tests, did I mention green')
            obj = request.cls.catalog.create_proficiency(create_form)
            request.cls.proficiency_list.append(obj)
            request.cls.proficiency_ids.append(obj.ident)
    
        create_form = request.cls.catalog.get_proficiency_form_for_create(request.cls.objective.ident, AGENT_ID, [])
        create_form.display_name = 'new Proficiency'
        create_form.description = 'description of Proficiency'
        create_form.genus_type = NEW_TYPE
        request.cls.osid_object = request.cls.catalog.create_proficiency(create_form)
    else:
        request.cls.catalog = request.cls.svc_mgr.get_${interface_name_under}(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_objective_banks():
                for obj in catalog.get_proficiencies():
                    catalog.delete_proficiency(obj.ident)
                for obj in catalog.get_objectives():
                    catalog.delete_objective(obj.ident)
                request.cls.svc_mgr.delete_objective_bank(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.catalog"""

    get_proficiency_form_for_create = """
        if not is_never_authz(self.service_config):
            form = self.catalog.get_proficiency_form_for_create(self.objective.ident, AGENT_ID, [])
            assert isinstance(form, OsidForm)
            assert not form.is_for_update()
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.get_proficiency_form_for_create(self.fake_id, AGENT_ID, [])"""

    delete_proficiency = """
        if not is_never_authz(self.service_config):
            create_form = self.catalog.get_proficiency_form_for_create(self.objective.ident, AGENT_ID, [])
            create_form.display_name = 'new Proficiency'
            create_form.description = 'description of Proficiency'
            create_form.genus_type = NEW_TYPE
            osid_object = self.catalog.create_proficiency(create_form)
            self.catalog.delete_proficiency(osid_object.ident)
            with pytest.raises(errors.NotFound):
                self.catalog.get_proficiency(osid_object.ident)
        else:
            with pytest.raises(errors.PermissionDenied):
                self.catalog.delete_proficiency(self.fake_id)"""


class ObjectiveBankQuery:
    import_statements = [
        'from dlkit.json_.learning.queries import ObjectiveBankQuery'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LEARNING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    create_form = request.cls.svc_mgr.get_objective_bank_form_for_create([])
    create_form.display_name = 'Test catalog'
    create_form.description = 'Test catalog description'
    request.cls.catalog = request.cls.svc_mgr.create_objective_bank(create_form)
    request.cls.fake_id = Id('resource.Resource%3A1%40ODL.MIT.EDU')

    def class_tear_down():
        request.cls.svc_mgr.delete_objective_bank(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # Since the session isn't implemented, we just construct an ObjectiveBankQuery directly
    request.cls.query = ObjectiveBankQuery(runtime=request.cls.catalog._runtime)"""
