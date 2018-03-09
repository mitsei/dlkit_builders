
class LoggingSession:

    import_statements = [
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LOGGING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        # Initialize test catalog:
        create_form = request.cls.svc_mgr.get_log_form_for_create([])
        create_form.display_name = 'Test Log'
        create_form.description = 'Test Log for LogAdminSession tests'
        request.cls.catalog = request.cls.svc_mgr.create_log(create_form)
        # Initialize catalog to be deleted:
        create_form = request.cls.svc_mgr.get_log_form_for_create([])
        create_form.display_name = 'Test Log For Deletion'
        create_form.description = 'Test Log for LogAdminSession deletion test'
        request.cls.catalog_to_delete = request.cls.svc_mgr.create_log(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.svc_mgr.get_logs():
                request.cls.svc_mgr.delete_log(catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    request.cls.session = request.cls.svc_mgr"""

    can_log = """
        assert isinstance(self.session.can_log(), bool)"""


class LogEntry:

    import_statements = [
    ]

    get_priority_template = """
        pass"""

    get_agent = """
        # because we don't have Agency implemented in authentication
        with pytest.raises(AttributeError):
            self.object.get_agent()"""

    get_agent_id = """
        result = self.object.get_agent_id()
        assert isinstance(result, Id)
        assert str(result) == str(self.catalog._proxy.get_effective_agent_id())"""

    get_resource = """
        with pytest.raises(errors.Unimplemented):
            self.object.get_resource()"""

    get_resource_id = """
        with pytest.raises(errors.Unimplemented):
            self.object.get_resource_id()"""


class LogEntryForm:

    import_statements_pattern = [
        'from dlkit.json_.osid.metadata import Metadata'
    ]

    init_template = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)

        request.cls.form = request.cls.catalog.get_${object_name_under}_form_for_create([])

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)

@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    pass"""

    set_priority_template = """
        # From test_templates/logging.py::LogEntryForm::set_priority_template
        if not is_never_authz(self.service_config):
            self.form.set_${var_name}(Type('type.Type%3Afake-type-id%40ODL.MIT.EDU'))
            assert self.form._my_map['${var_name_mixed}'] == 'type.Type%3Afake-type-id%40ODL.MIT.EDU'
            with pytest.raises(errors.InvalidArgument):
                self.form.${method_name}(True)"""

    clear_priority_template = """
        # From test_templates/logging.py::LogEntryForm::clear_priority_template
        if not is_never_authz(self.service_config):
            self.form.set_${var_name}(Type('type.Type%3Afake-type-id%40ODL.MIT.EDU'))
            assert self.form._my_map['${var_name_mixed}'] == 'type.Type%3Afake-type-id%40ODL.MIT.EDU'
            self.form.${method_name}()
            assert self.form._my_map['${var_name_mixed}Id'] == self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0]"""

    get_priority_metadata_template = """
        # From test_templates/logging.py::LogEntryForm::get_priority_metadata_template
        if not is_never_authz(self.service_config):
            mdata = self.form.${method_name}()
            assert isinstance(mdata, Metadata)
            assert isinstance(mdata.get_element_id(), ABC_Id)
            assert isinstance(mdata.get_element_label(), ABC_DisplayText)
            assert isinstance(mdata.get_instructions(), ABC_DisplayText)
            assert mdata.get_syntax() == '${syntax}'
            assert not mdata.is_array()
            assert isinstance(mdata.is_required(), bool)
            assert isinstance(mdata.is_read_only(), bool)
            assert isinstance(mdata.is_linked(), bool)"""

    set_timestamp = """
        if not is_never_authz(self.service_config):
            test_time = DateTime.utcnow()
            # By default log entries have this set, so can't use the templated test
            assert self.form._my_map['timestamp'] is not None
            self.form.set_timestamp(test_time)
            assert self.form._my_map['timestamp'] == test_time
            with pytest.raises(errors.InvalidArgument):
                self.form.set_timestamp(True)"""


class LogEntryQuery:
    import_statements = [
        'from dlkit.primordium.calendaring.primitives import DateTime'
    ]

    match_priority = """
        with pytest.raises(errors.Unimplemented):
            self.query.match_priority('foo', match=True)"""

    match_minimum_priority = """
        with pytest.raises(errors.Unimplemented):
            self.query.match_minimum_priority('foo', match=True)"""

    match_timestamp = """
        start_date = DateTime.utcnow()
        end_date = DateTime.utcnow()
        assert 'timestamp' not in self.query._query_terms
        self.query.match_timestamp(start_date, end_date, True)
        assert self.query._query_terms['timestamp'] == {
            '$gte': start_date,
            '$lte': end_date
        }"""

    match_any_priority = """
        with pytest.raises(errors.Unimplemented):
            self.query.match_any_priority(match=True)"""

    clear_minimum_priority_terms = """
        with pytest.raises(errors.Unimplemented):
            self.query.clear_minimum_priority_terms()"""

    clear_resource_terms = """
        with pytest.raises(errors.Unimplemented):
            self.query.clear_resource_terms()"""

    supports_resource_query = """
        with pytest.raises(errors.Unimplemented):
            self.query.supports_resource_query()"""

    supports_agent_query = """
        with pytest.raises(errors.Unimplemented):
            self.query.supports_agent_query()"""

    supports_log_query = """
        with pytest.raises(errors.Unimplemented):
            self.query.supports_log_query()"""

    get_resource_query = """
        with pytest.raises(errors.Unimplemented):
            self.query.get_resource_query()"""

    get_agent_query = """
        with pytest.raises(errors.Unimplemented):
            self.query.get_agent_query()"""

    get_log_query = """
        with pytest.raises(errors.Unimplemented):
            self.query.get_log_query()"""


class LogNodeList:
    init = """"""

    get_next_log_node = """"""

    get_next_log_nodes = """"""


class LogNode:
    init = """"""

    get_log = """"""

    get_parent_log_nodes = """"""

    get_child_log_nodes = """"""


class LogQuery:
    import_statements = [
        'from dlkit.json_.logging_.queries import LogQuery'
    ]

    init = """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        'LOGGING',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_log_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_log(create_form)
        request.cls.fake_id = Id('resource.Resource%3A1%40ODL.MIT.EDU')

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_log(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # Since the session isn't implemented, we just construct a LogQuery directly
    request.cls.query = LogQuery(runtime=request.cls.catalog._runtime)"""


class LogEntryLookupSession:
    # override this -- typically templated from ResourceLookupSession::get_resource
    # Now that we have the QuerySession, will throw NotFound instead of PermissionDenied
    get_log_entry = """
        if not is_never_authz(self.service_config):
            self.catalog.use_isolated_log_view()
            obj = self.catalog.get_log_entry(self.log_entry_list[0].ident)
            assert obj.ident == self.log_entry_list[0].ident
            self.catalog.use_federated_log_view()
            obj = self.catalog.get_log_entry(self.log_entry_list[0].ident)
            assert obj.ident == self.log_entry_list[0].ident
        else:
            with pytest.raises(errors.NotFound):
                self.catalog.get_log_entry(self.fake_id)"""

    # override this -- typically templated from ResourceLookupSession::get_resources_by_ids
    # Now that we have the QuerySession, will return empty list
    get_log_entries_by_ids = """
        from dlkit.abstract_osid.logging_.objects import LogEntryList
        objects = self.catalog.get_log_entries_by_ids(self.log_entry_ids)
        assert isinstance(objects, LogEntryList)
        self.catalog.use_federated_log_view()
        objects = self.catalog.get_log_entries_by_ids(self.log_entry_ids)
        assert isinstance(objects, LogEntryList)
        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0"""

    # override this -- typically templated from ResourceLookupSession::get_resources_by_genus_type
    # Now that we have the QuerySession, will return empty list
    get_log_entries_by_genus_type = """
        from dlkit.abstract_osid.logging_.objects import LogEntryList
        objects = self.catalog.get_log_entries_by_genus_type(DEFAULT_GENUS_TYPE)
        assert isinstance(objects, LogEntryList)
        self.catalog.use_federated_log_view()
        objects = self.catalog.get_log_entries_by_genus_type(DEFAULT_GENUS_TYPE)
        assert isinstance(objects, LogEntryList)
        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0"""

    # override this -- typically templated from ResourceLookupSession::get_resources_by_parent_genus_type
    # Now that we have the QuerySession, will throw Unimplemented instead of PermissionDenied
    get_log_entries_by_parent_genus_type = """
        from dlkit.abstract_osid.logging_.objects import LogEntryList
        if not is_never_authz(self.service_config):
            objects = self.catalog.get_log_entries_by_parent_genus_type(DEFAULT_GENUS_TYPE)
            assert isinstance(objects, LogEntryList)
            self.catalog.use_federated_log_view()
            objects = self.catalog.get_log_entries_by_parent_genus_type(DEFAULT_GENUS_TYPE)
            assert objects.available() == 0
            assert isinstance(objects, LogEntryList)
        else:
            with pytest.raises(errors.Unimplemented):
                # because the never_authz "tries harder" and runs the actual query...
                #    whereas above the method itself in JSON returns an empty list
                self.catalog.get_log_entries_by_parent_genus_type(DEFAULT_GENUS_TYPE)"""

    # override this -- typically templated from ResourceLookupSession::get_resources_by_record_type
    # Now that we have the QuerySession, will return empty list
    get_log_entries_by_record_type = """
        from dlkit.abstract_osid.logging_.objects import LogEntryList
        objects = self.catalog.get_log_entries_by_record_type(DEFAULT_TYPE)
        assert isinstance(objects, LogEntryList)
        self.catalog.use_federated_log_view()
        objects = self.catalog.get_log_entries_by_record_type(DEFAULT_TYPE)
        assert objects.available() == 0
        assert isinstance(objects, LogEntryList)"""

    # override this -- typically templated from ResourceLookupSession::get_resources
    # Now that we have the QuerySession, will return empty list
    get_log_entries = """
        from dlkit.abstract_osid.logging_.objects import LogEntryList
        objects = self.catalog.get_log_entries()
        assert isinstance(objects, LogEntryList)
        self.catalog.use_federated_log_view()
        objects = self.catalog.get_log_entries()
        assert isinstance(objects, LogEntryList)

        if not is_never_authz(self.service_config):
            assert objects.available() > 0
        else:
            assert objects.available() == 0

    def test_get_log_entry_with_alias(self):
        if not is_never_authz(self.service_config):
            self.catalog.alias_log_entry(self.log_entry_ids[0], ALIAS_ID)
            obj = self.catalog.get_log_entry(ALIAS_ID)
            assert obj.get_id() == self.log_entry_ids[0]"""
