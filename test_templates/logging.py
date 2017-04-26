
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
    ]

    set_priority_template = """
        pass"""
