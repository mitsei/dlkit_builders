
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

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_logs():
            cls.svc_mgr.delete_log(catalog.ident)"""

    can_log = """
        pass"""

    log = """
        pass"""

    get_log_id = """
        pass"""


class LogEntry:

    import_statements_pattern = [
    ]

    get_priority_template = """
        pass"""

    get_agent = """"""

    get_agent_id = """"""

    get_resource = """"""

    get_resource_id = """"""


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
        pass"""

    get_priority_metadata_template = """
        # From test_templates/logging.py::LogEntryForm::get_priority_metadata_template
        self.assertTrue(isinstance(self.form.${method_name}(), Metadata))"""

    set_timestamp = """
        test_time = DateTime.utcnow()
        # By default log entries have this set, so can't use the templated test
        self.assertIsNotNone(self.form._my_map['timestamp'])
        self.form.set_timestamp(test_time)
        self.assertEqual(self.form._my_map['timestamp'],
                         test_time)"""


class LogNodeList:
    init = """"""

    get_next_log_node = """"""

    get_next_log_nodes = """"""


class LogNode:
    init = """"""

    get_log = """"""

    get_parent_log_nodes = """"""

    get_child_log_nodes = """"""
