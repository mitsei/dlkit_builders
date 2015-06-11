
class ObjectiveRequisiteSession:

    import_statements_pattern = [
    ]

    get_requisite_objectives_template = """
        pass"""


class ObjectiveRequisiteAssignmentSession:

    import_statements_pattern = [
    ]


    assign_objective_requisite_template= """
        pass"""

class ObjectiveAdminSession:

    import_statements_pattern = [
    ]

    delete_objective_template = """
        pass"""


class ActivityLookupSession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.activity_list = list()
        cls.activity_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ActivityLookupSession tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)
        create_form = cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for ActivIty Lookup'
        create_form.description = 'Test Objective for ActivityLookupSession tests'
        cls.objective = cls.catalog.create_objective(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_activity_form_for_create(cls.objective.ident, [])
            create_form.display_name = 'Test Activity ' + str(num)
            create_form.description = 'Test Activity for ActivityLookupSession tests'
            obj = cls.catalog.create_activity(create_form)
            cls.activity_list.append(obj)
            cls.activity_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        #for obj in cls.catalog.get_activities():
        #    cls.catalog.delete_activity(obj.ident)
        #for catalog in cls.catalogs:
        #    cls.svc_mgr.delete_objective_bank(catalog.ident)
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_activities():
                catalog.delete_activity(obj.ident)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)
"""

    get_activities_for_objective_template = """
        pass"""


class ActivityAdminSession:

    import_statements_pattern = [
    ]

    get_activity_form_for_create_template = """
        pass"""



class Activity:

    import_statements_pattern = [
    ]

    import_statements = [
    ]


    get_objective_id_template = """
        pass"""

    get_objective_template = """
        pass"""

    is_asset_based_activity_template = """
        pass"""

    get_asset_ids_template = """
        pass"""

    get_assets_template = """
        pass"""


class ActivityForm:

    get_assets_metadata_template = """
        pass"""

    set_assets_template = """
        pass"""

    clear_assets_template = """
        pass"""

