
class LoggingSession:

    import_statements = [
    ]

    init = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('LOGGING', proxy=PROXY, implementation='TEST_SERVICE')
        # Initialize test catalog:
        create_form = cls.svc_mgr.get_log_form_for_create([])
        create_form.display_name = 'Test Log'
        create_form.description = 'Test Log for LogAdminSession tests'
        cls.catalog = cls.svc_mgr.create_log(create_form)
        # Initialize catalog to be deleted:
        create_form = cls.svc_mgr.get_log_form_for_create([])
        create_form.display_name = 'Test Log For Deletion'
        create_form.description = 'Test Log for LogAdminSession deletion test'
        cls.catalog_to_delete = cls.svc_mgr.create_log(create_form)

    def setUp(self):
        self.session = self.svc_mgr

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_logs():
            cls.svc_mgr.delete_log(catalog.ident)"""

    can_log = """
        self.assertTrue(isinstance(self.session.can_log(), bool))"""


class LogEntry:

    import_statements = [
    ]

    get_priority_template = """
        pass"""

    get_agent = """
        # because we don't have Agency implemented in authentication
        with self.assertRaises(AttributeError):
            self.object.get_agent()"""

    get_agent_id = """
        result = self.object.get_agent_id()
        self.assertTrue(isinstance(result, Id))
        self.assertEqual(str(result),
                         str(self.catalog._proxy.get_effective_agent_id()))"""

    get_resource = """
        with self.assertRaises(errors.Unimplemented):
            self.object.get_resource()"""

    get_resource_id = """
        with self.assertRaises(errors.Unimplemented):
            self.object.get_resource_id()"""


class LogEntryForm:

    import_statements_pattern = [
        'from dlkit.json_.osid.metadata import Metadata'
    ]

    init_template = """
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('${pkg_name_upper}', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_${cat_name_under}(create_form)

        cls.form = cls.catalog.get_${object_name_under}_form_for_create([])

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_${cat_name_under}(cls.catalog.ident)"""

    set_priority_template = """
        # From test_templates/logging.py::LogEntryForm::set_priority_template
        self.form.set_${var_name}(Type('type.Type%3Afake-type-id%40ODL.MIT.EDU'))
        self.assertEqual(self.form._my_map['${var_name_mixed}'],
                         'type.Type%3Afake-type-id%40ODL.MIT.EDU')
        with self.assertRaises(errors.InvalidArgument):
            self.form.${method_name}(True)"""

    clear_priority_template = """
        # From test_templates/logging.py::LogEntryForm::clear_priority_template
        self.form.set_${var_name}(Type('type.Type%3Afake-type-id%40ODL.MIT.EDU'))
        self.assertEqual(self.form._my_map['${var_name_mixed}'],
                         'type.Type%3Afake-type-id%40ODL.MIT.EDU')
        self.form.${method_name}()
        self.assertEqual(self.form._my_map['${var_name_mixed}Id'], self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0])"""

    get_priority_metadata_template = """
        # From test_templates/logging.py::LogEntryForm::get_priority_metadata_template
        mdata = self.form.${method_name}()
        self.assertTrue(isinstance(mdata, Metadata))
        self.assertTrue(isinstance(mdata.get_element_id(), ABC_Id))
        self.assertTrue(isinstance(mdata.get_element_label(), ABC_DisplayText))
        self.assertTrue(isinstance(mdata.get_instructions(), ABC_DisplayText))
        self.assertEquals(mdata.get_syntax(), '${syntax}')
        self.assertFalse(mdata.is_array())
        self.assertTrue(isinstance(mdata.is_required(), bool))
        self.assertTrue(isinstance(mdata.is_read_only(), bool))
        self.assertTrue(isinstance(mdata.is_linked(), bool))"""

    set_timestamp = """
        test_time = DateTime.utcnow()
        # By default log entries have this set, so can't use the templated test
        self.assertIsNotNone(self.form._my_map['timestamp'])
        self.form.set_timestamp(test_time)
        self.assertEqual(self.form._my_map['timestamp'],
                         test_time)
        with self.assertRaises(errors.InvalidArgument):
            self.form.set_timestamp(True)"""


class LogEntryQuery:
    import_statements = [
        'from dlkit.primordium.calendaring.primitives import DateTime'
    ]

    match_priority = """
        with self.assertRaises(errors.Unimplemented):
            self.query.match_priority('foo', match=True)"""

    match_minimum_priority = """
        with self.assertRaises(errors.Unimplemented):
            self.query.match_minimum_priority('foo', match=True)"""

    match_timestamp = """
        start_date = DateTime.utcnow()
        end_date = DateTime.utcnow()
        self.assertNotIn('timestamp', self.query._query_terms)
        self.query.match_timestamp(start_date, end_date, True)
        self.assertEqual(self.query._query_terms['timestamp'], {
            '$gte': start_date,
            '$lte': end_date
        })"""

    match_any_priority = """
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_priority(match=True)"""

    clear_minimum_priority_terms = """
        with self.assertRaises(errors.Unimplemented):
            self.query.clear_minimum_priority_terms()"""

    clear_resource_terms = """
        with self.assertRaises(errors.Unimplemented):
            self.query.clear_resource_terms()"""

    supports_resource_query = """
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_resource_query()"""

    supports_agent_query = """
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_agent_query()"""

    supports_log_query = """
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_log_query()"""

    get_resource_query = """
        with self.assertRaises(errors.Unimplemented):
            self.query.get_resource_query()"""

    get_agent_query = """
        with self.assertRaises(errors.Unimplemented):
            self.query.get_agent_query()"""

    get_log_query = """
        with self.assertRaises(errors.Unimplemented):
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
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('LOGGING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_log_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_log(create_form)
        cls.fake_id = Id('resource.Resource%3A1%40ODL.MIT.EDU')

    def setUp(self):
        # Since the session isn't implemented, we just construct a LogQuery directly
        self.query = LogQuery(runtime=self.catalog._runtime)

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_log(cls.catalog.ident)"""
