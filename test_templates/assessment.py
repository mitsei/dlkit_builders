
class AssessmentSession:
    
    import_statements = [
        ]
    
    init = """
"""
    
    can_take_assessments = """
        pass"""
    
    has_assessment_begun = """
        pass"""
    
    is_assessment_over = """
        pass"""
    
    ## This method has been deprecated:
    finished_assessment = """
        pass"""
    
    requires_synchronous_sections = """
        pass"""
    
    get_first_assessment_section = """
        pass"""
    
    has_next_assessment_section = """
        pass"""
    
    get_next_assessment_section = """
        pass"""
    
    has_previous_assessment_section = """
        pass"""
    
    get_previous_assessment_section = """
        pass"""
    
    get_assessment_section = """
        pass"""
    
    get_assessment_sections = """
        pass"""
    
    is_assessment_section_complete = """
        pass"""
    
    get_incomplete_assessment_sections = """
        pass"""
    
    has_assessment_section_begun = """
        pass"""
    
    is_assessment_section_over = """
        pass"""
    
    ## This method has been deprecated:
    finished_assessment_section = """
        pass"""
    
    requires_synchronous_responses = """
        pass"""
    
    get_first_question = """
        pass"""
    
    has_next_question = """
        pass"""
    
    get_next_question = """
        pass"""
    
    has_previous_question = """
        pass"""
    
    get_previous_question = """
        pass"""
    
    get_question = """
        pass"""
    
    get_questions = """
        pass"""
    
    get_response_form = """
        pass"""
    
    submit_response = """
        pass"""
    
    skip_item = """
        pass"""
    
    is_question_answered = """
        pass"""
    
    get_unanswered_questions = """
        pass"""
    
    has_unanswered_questions = """
        pass"""
    
    get_first_unanswered_question = """
        pass"""
    
    has_next_unanswered_question = """
        pass"""
    
    get_next_unanswered_question = """
        pass"""
    
    has_previous_unanswered_question = """
        pass"""
    
    get_previous_unanswered_question = """
        pass"""
    
    get_response = """
        pass"""
    
    get_responses = """
        pass"""
    
    clear_response = """
        pass"""
    
    finish_assessment_section = """
        pass"""
    
    ## This is no longer needed?
    finish = """
        pass"""
    
    finish_assessment = """
        pass"""

    
    is_answer_available = """
        pass"""
    
    get_answers = """
        pass"""


class ItemAdminSession:
    
    import_statements = [
        ]
    
    # This method may need to be hand implemented to deal with error if the item
    # is found to be associated with an assessment
    proposed_delete_item = """
"""    

    # These methods overwrite the canonical aggregate object admin methods to
    # deal with authoring Questions whitch are special: ie. there is only one per
    # Item.  Perhaps we will see this pattern again and can make templates.
    create_question = """
        pass"""
    
    get_question_form_for_update = """
        pass"""
    
    update_question = """
        pass"""


class AssessmentAdminSession:
    
    import_statements = [
        ]
    
    # This method may need to be hand implemented to deal with error if the assessment
    # is found to be associated with an assessment offered
    proposed_delete_assessment = """
        pass"""

class AssessmentOfferedLookupSession:

    init = """
    @classmethod
    def setUpClass(cls):
        cls.assessment_offered_list = list()
        cls.assessment_offered_ids = list()
        cls.svc_mgr = RUNTIME.get_service_manager('ASSESSMENT', PROXY)
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentOfferedLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedLookupSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident, [])
            create_form.display_name = 'Test AssessmentOffered ' + str(num)
            create_form.description = 'Test AssessmentOffered for AssessmentOfferedLookupSession tests'
            obj = cls.catalog.create_assessment_offered(create_form)
            cls.assessment_offered_list.append(obj)
            cls.assessment_offered_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        #for obj in cls.catalog.get_assessments_offered():
        #    cls.catalog.delete_assessment_offered(obj.ident)
        #for catalog in cls.catalogs:
        #    cls.svc_mgr.delete_bank(catalog.ident)
        for catalog in cls.svc_mgr.get_banks():
            for obj in catalog.get_assessments_offered():
                catalog.delete_assessment_offered(obj.ident)
            for obj in catalog.get_assessments():
                catalog.delete_assessment(obj.ident)
            cls.svc_mgr.delete_bank(catalog.ident)
"""

class AssessmentTakenLookupSession:
    
    init = """
    @classmethod
    def setUpClass(cls):
        cls.assessment_taken_list = list()
        cls.assessment_taken_ids = list()
        cls.svc_mgr = RUNTIME.get_service_manager('ASSESSMENT', PROXY)
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test Bank'
        create_form.description = 'Test Bank for AssessmentTakenLookupSession tests'
        cls.catalog = cls.svc_mgr.create_bank(create_form)
        create_form = cls.catalog.get_assessment_form_for_create([])
        create_form.display_name = 'Test Assessment'
        create_form.description = 'Test Assessment for AssessmentOfferedLookupSession tests'
        cls.assessment = cls.catalog.create_assessment(create_form)
        create_form = cls.catalog.get_assessment_offered_form_for_create(cls.assessment.ident, [])
        create_form.display_name = 'Test AssessmentOffered'
        create_form.description = 'Test AssessmentOffered for AssessmentOfferedLookupSession tests'
        cls.assessment_offered = cls.catalog.create_assessment_offered(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_assessment_taken_form_for_create(cls.assessment_offered.ident, [])
            create_form.display_name = 'Test AssessmentTaken ' + str(num)
            create_form.description = 'Test AssessmentTaken for AssessmentTakenLookupSession tests'
            obj = cls.catalog.create_assessment_taken(create_form)
            cls.assessment_taken_list.append(obj)
            cls.assessment_taken_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        #for obj in cls.catalog.get_assessments_taken():
        #    cls.catalog.delete_assessment_taken(obj.ident)
        #for catalog in cls.catalogs:
        #    cls.svc_mgr.delete_bank(catalog.ident)
        for catalog in cls.svc_mgr.get_banks():
            for obj in catalog.get_assessments_taken():
                catalog.delete_assessment_taken(obj.ident)
            for obj in catalog.get_assessments_offered():
                catalog.delete_assessment_offered(obj.ident)
            for obj in catalog.get_assessments():
                catalog.delete_assessment(obj.ident)
            cls.svc_mgr.delete_bank(catalog.ident)

"""
    
    # This is hand built, but there may be a pattern to try to map, specifically
    # getting objects for another package object and a persisted id thingy
    get_assessments_taken_for_taker_and_assessment_offered = """
        pass"""
    
    get_assessments_taken_for_assessment = """
        pass"""


class AssessmentTakenAdminSession:
    
    import_statements = [
    ]

    
    ##
    # This impl may differ from the usual create_osid_object method in that it
    # deals with agent id and default display name based on the underlying Assessment
    # and checks for exceeding max attempts...
    proposed_create_assessment_taken = """
        pass"""

class AssessmentBasicAuthoringSession:
    
    import_statements = [
    ]
    
    init = """
"""
    
    can_author_assessments = """
        pass"""
    
    get_items = """
        pass"""
    
    add_item = """
        pass"""
    
    remove_item = """
        pass"""
    
    move_item = """
        pass"""
    
    order_items = """
        pass"""


class Question:
    
    import_statements = [
    ]
    
    additional_methods = """
"""

class Item:
    
    get_question_id = """
        pass"""
    
    get_question = """
        pass"""
    
    additional_methods = """
        pass"""

class AssessmentOffered:
    
    import_statements = [
        ]
    
    additional_methods = """
        pass"""
    
    has_start_time_template = """
        pass"""
    
    get_start_time_template = """
        pass"""
    
    has_duration_template = """
        pass"""
    
    get_duration_template = """
        pass"""

class AssessmentOfferedForm:
    
    set_start_time_template = """
"""
    
    # This looks just like the generic one. Need to find in the pattern?
    clear_start_time_template = """
        pass"""
    
    set_duration_template = """
       """

class AssessmentOfferedQuery:
    
    match_start_time_template = """
        pass"""

class AssessmentTaken:
    
    import_statements = [
    ]
    
    additional_methods = """
"""
    
    get_taker_id = """
        pass"""
    
    get_taker = """
        pass"""
    
    get_taking_agent_id = """
        pass"""
    
    get_taking_agent = """
        pass"""
    
    has_started = """
        pass"""
    
    get_actual_start_time = """
        pass"""
    
    has_ended = """
        pass"""
    
    get_completion_time = """
        pass"""
    
    get_time_spent = """
        pass"""
    
    get_completion_template = """
        pass"""
    
    get_score_template = """
        pass"""

class AssessmentTakenForm:
    
    import_statements = [
    ]

class AssessmentSection:
    
    has_allocated_time = """
        pass"""
    
    get_allocated_time = """
        pass"""
    
    are_items_sequential = """
        pass"""
    
    are_items_shuffled = """
        pass"""

class Response:
    
    import_statements = [
    ]
    
    init = """
"""
    
    get_item_id = """
        pass"""
    
    get_item = """
       """
    
    get_response_record = """
        pass"""

