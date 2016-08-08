
class AssessmentManager:
    
    import_statements = [
        'from . import sessions',
    ]
    
    awkward_get_assessment_taken_query_session_for_bank_to_delete = """
        if not self.supports_assessment_taken_query():
            raise errors.Unimplemented()
        return sessions.AssessmentTakenQuerySession(bank_id, runtime=self._runtime)
    
    def get_assessment_taken_admin_session(self):
        if not self.supports_assessment_taken_admin():
            raise errors.Unimplemented()
        return sessions.AssessmentTakenAdminSession(runtime=self._runtime)
    
    def get_assessment_taken_admin_session_for_bank(self, bank_id):
        if not self.supports_assessment_taken_admin():
            raise errors.Unimplemented()
        return sessions.AssessmentTakenAdminSession(bank_id, runtime=self._runtime)"""


class AssessmentProxyManager:

    import_statements = [
        'from . import sessions',
    ]
    
    awkward_get_assessment_taken_query_session_for_bank_to_delete = """
        if not self.supports_assessment_taken_query():
            raise errors.Unimplemented()
        return sessions.AssessmentTakenQuerySession(bank_id, proxy, runtime=self._runtime)
    
    def get_assessment_taken_admin_session(self, proxy):
        if not self.supports_assessment_taken_admin():
            raise errors.Unimplemented()
        return sessions.AssessmentTakenAdminSession(proxy=proxy, runtime=self._runtime)
    
    def get_assessment_taken_admin_session_for_bank(self, bank_id, proxy):
        if not self.supports_assessment_taken_admin():
            raise errors.Unimplemented()
        return sessions.AssessmentTakenAdminSession(bank_id, proxy=proxy, runtime=self._runtime)"""


class AssessmentSession:
    
    import_statements = [
        'from ..primitives import Id',
        'from ..primitives import Type',
        'from dlkit.abstract_osid.osid import errors',
        'from bson.objectid import ObjectId',
        'from . import objects',
        'from .rules import Response',
        'from ..osid.sessions import OsidSession',
        'from ..utilities import MongoClientValidated',
		'from ..utilities import get_registry',
        'SUBMITTED = True',
        'from importlib import import_module',
        'from .assessment_utilities import get_assessment_section as get_section_util',
        'from .assessment_utilities import check_effective',
    ]
    
    init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None):
        OsidSession.__init__(self)
        self._catalog_class = objects.Bank
        self._session_name = 'AssessmentSession'
        self._catalog_name = 'Bank'
        OsidSession._init_object(
            self, catalog_id,
            proxy,
            runtime,
            db_name='assessment',
            cat_name='Bank',
            cat_class=objects.Bank)
        self._forms = dict()"""

    can_take_assessments = """
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
    
    has_assessment_begun = """
        return self._get_assessment_taken(assessment_taken_id).has_started()"""
    
    is_assessment_over = """
        return self._get_assessment_taken(assessment_taken_id).has_ended()"""
    
    ## This method has been deprecated and NOT updated:
    finished_assessment = """
        collection = MongoClientValidated('assessment',
                                          collection='AssessmentTaken',
                                          runtime=self._runtime)
        assessment_taken = self._get_assessment_taken(assessment_taken_id)
        assessment_taken_map = assessment_taken._my_map
        if assessment_taken.has_started() and not assessment_taken.has_ended():
            assessment_taken_map['completionTime'] = DateTime.utcnow()
            assessment_taken_map['ended'] = True
            collection.save(assessment_taken_map)
        else:
            raise errors.IllegalState()"""

    requires_synchronous_sections = """
        return self._get_assessment_taken(assessment_taken_id).get_assessment_offered().are_sections_sequential()"""
    
    get_first_assessment_section = """
        assessment_taken = self._get_assessment_taken(assessment_taken_id)
        return assessment_taken._get_first_assessment_section()"""
   
    has_next_assessment_section = """
        try:
            self.get_next_assessment_section(assessment_section_id)
        except errors.IllegalState:
            return False
        else:
            return True"""
    
    get_next_assessment_section = """
        assessment_taken = self.get_assessment_section(assessment_section_id)._assessment_taken
        return assessment_taken._get_next_assessment_section(assessment_section_id)"""
    
    has_previous_assessment_section = """
        try:
            self.get_previous_assessment_section(assessment_section_id)
        except errors.IllegalState:
            return False
        else:
            return True"""
    
    get_previous_assessment_section = """
        assessment_taken = self.get_assessment_section(assessment_section_id)._assessment_taken
        return assessment_taken._get_previous_assessment_section(assessment_section_id)"""
    
    get_assessment_section = """
        return get_section_util(assessment_section_id, runtime=self._runtime, proxy=self._proxy)"""

    get_assessment_sections = """
        assessment_taken = self._get_assessment_taken(assessment_taken_id)
        return assessment_taken._get_assessment_sections()"""
    
    is_assessment_section_complete = """
        return self.get_assessment_section(assessment_section_id)._is_complete()"""
    
    get_incomplete_assessment_sections = """
        section_list = []
        for section in self.get_assessment_sections(assessment_taken_id):
            if not section._is_complete():
                section_list.append(section)
        return objects.AssessmentSectionList(section_list, runtime=self._runtime, proxy=self._proxy)"""
    
    ## Has this method has been deprecated???
    ## IMPLEMENT ME PROPERLY!
    has_assessment_section_begun = """
        return get_section_util(assessment_section_id,
                                runtime=self._runtime)._assessment_taken.has_started()"""
    
    ## Has this method has been deprecated???
    is_assessment_section_over = """
        return get_section_util(assessment_section_id,
                                runtime=self._runtime)._is_over()"""
    
    ## This method has been deprecated:
    finished_assessment_section = """
            raise errors.IllegalState()
        self.finished_assessment(assessment_section_id)"""
    
    ## Has this method has been deprecated???
    requires_synchronous_responses = """
        return self.get_assessment_section(assessment_section_id).are_items_sequential()"""
    
    get_first_question = """
        return self.get_assessment_section(assessment_section_id)._get_first_question()"""

    has_next_question = """
        try:
            self.get_next_question(assessment_section_id, item_id)
        except errors.IllegalState:
            return False
        else:
            return True"""
   
    get_next_question = """
        return self.get_assessment_section(assessment_section_id)._get_next_question(question_id=item_id)"""
    
    has_previous_question = """
        try:
            self.get_previous_question(assessment_section_id, item_id)
        except errors.IllegalState:
            return False
        else:
            return True"""

    get_previous_question = """
        return self.get_assessment_section(assessment_section_id)._get_previous_question(question_id=item_id)"""

    get_question = """
        return self.get_assessment_section(assessment_section_id)._get_question(item_id)"""
    
    get_questions = """
        # Does this want to return a blocking list of available questions?
        return self.get_assessment_section(assessment_section_id)._get_questions()"""

    get_response_form_import_templates = [
        'from ...abstract_osid.id.primitives import Id as ABCId'
    ]

    get_response_form = """
        if not isinstance(item_id, ABCId):
            raise errors.InvalidArgument('argument is not a valid OSID Id')

        ##
        # This is a little hack to get the answer record types from the Item's
        # first Answer record types. Should really get it from item genus types somehow:
        record_type_data_sets = get_registry('ANSWER_RECORD_TYPES', self._runtime)
        mgr = self._get_provider_manager('ASSESSMENT', local=True)
        ils = self.get_assessment_section(assessment_section_id)._get_item_lookup_session()
        item = ils.get_item(item_id)
        item_map = item.object_map
        answer_record_types = []
        if len(item_map['answers']) > 0:
            for record_type_idstr in item_map['answers'][0]['recordTypeIds']:
                identifier = Id(record_type_idstr).get_identifier()
                if identifier in record_type_data_sets:
                    answer_record_types.append(Type(**record_type_data_sets[identifier]))
        else:
            for record_type_idstr in item_map['question']['recordTypeIds']:
                identifier = Id(record_type_idstr).get_identifier()
                if identifier in record_type_data_sets:
                    answer_record_types.append(Type(**record_type_data_sets[identifier]))
        # Thus endith the hack.
        ##

        obj_form = objects.AnswerForm(
            bank_id=self._catalog_id,
            record_types=answer_record_types,
            item_id=item_id,
            catalog_id=self._catalog_id,
            assessment_section_id=assessment_section_id,
            runtime=self._runtime,
            proxy=self._proxy)
        obj_form._for_update = False # This may be redundant
        self._forms[obj_form.get_id().get_identifier()] = not SUBMITTED
        return obj_form"""

    submit_response_import_templates = [
        'from ...abstract_osid.assessment.objects import AnswerForm as ABCAnswerForm'
    ]

    submit_response = """
        if not isinstance(answer_form, ABCAnswerForm):
            raise errors.InvalidArgument('argument type is not an AnswerForm')
        ##
        # OK, so the following should actually NEVER be true. Remove it?
        if answer_form.is_for_update():
            raise errors.InvalidArgument('the AnswerForm is for update only, not submit')
        ##

        try:
            if self._forms[answer_form.get_id().get_identifier()] == SUBMITTED:
                raise errors.IllegalState('answer_form already used in a submit transaction')
        except KeyError:
            raise errors.Unsupported('answer_form did not originate from this assessment session')
        if not answer_form.is_valid():
            raise errors.InvalidArgument('one or more of the form elements is invalid')
        answer_form._my_map['_id'] = ObjectId()
        self.get_assessment_section(assessment_section_id)._submit_response(item_id, answer_form)
        self._forms[answer_form.get_id().get_identifier()] = SUBMITTED"""
    
    skip_item = """
        # if the assessment or part allows us to skip:
        self.get_assessment_section(assessment_section_id)._submit_response(item_id, None)"""
    
    is_question_answered = """
        return self.get_assessment_section(assessment_section_id)._is_question_answered(item_id)"""
    
    get_unanswered_questions = """
        return self.get_assessment_section(assessment_section_id)._get_questions(answered=False)"""
    
    has_unanswered_questions = """
        # There's probably a more efficient way to implement this:
        return bool(self.get_unanswered_questions(assessment_section_id).available())"""
    
    get_first_unanswered_question = """
        questions = self.get_unanswered_questions(assessment_section_id)
        if not questions.available():
            raise errors.IllegalState('There are no more unanswered questions available')
        return questions.next()"""
    
    has_next_unanswered_question = """
        # There's probably a more efficient way to implement this:
        try:
            self.get_next_unanswered_question(assessment_section_id, item_id)
        except errors.IllegalState:
            return False
        else:
            return True"""
    
    get_next_unanswered_question = """
        questions = self.get_unanswered_questions(assessment_section_id)
        for question in questions:
            if question.get_id() == item_id:
                if questions.available():
                    return questions.next()
                else:
                    raise errors.IllegalState('No next unanswered question is available')
        raise errors.NotFound('item_id is not found in Section')"""
    
    has_previous_unanswered_question = """
        # There's probably a more efficient way to implement this:
        try:
            self.get_previous_unanswered_question(assessment_section_id, item_id)
        except errors.IllegalState:
            return False
        else:
            return True"""
    
    get_previous_unanswered_question = """
        # could itertools be useful for any of this?
        questions = self.get_unanswered_questions(assessment_section_id)
        previous_question = questions.next()
        if previous_question.get_id() == item_id:
            raise errors.IllegalState('No previous unanswered question is available')
        for question in questions:
            if question.get_id() == item_id:
                return previous_question
            else:
                previous_question = question
        raise errors.NotFound('item_id is not found in Section')"""
    
    get_response = """
        return self.get_assessment_section(assessment_section_id)._get_response(question_id=item_id)"""

    get_responses = """
        return self.get_assessment_section(assessment_section_id)._get_responses()"""
   
    clear_response = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        # Should probably check to see if responses can be cleared, but how?
        self.get_assessment_section(assessment_section_id)._submit_response(item_id, None)"""
    
    finish_assessment_section = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        self.get_assessment_section(assessment_section_id)._finish()"""
    
    ## This is no longer needed:
    finish = """
        self.finished_assessment(assessment_section_id)
    
    def finish_assessment_section(self, assessment_section_id):
        self.finish(assessment_section_id)"""
    
    finish_assessment = """
        assessment_taken = self._get_assessment_taken(assessment_taken_id)
        assessment_taken_map = assessment_taken._my_map
        if assessment_taken.has_started() and not assessment_taken.has_ended():
            assessment_taken_map['completionTime'] = DateTime.utcnow()
            assessment_taken_map['ended'] = True
            collection = MongoClientValidated('assessment',
                                              collection='AssessmentTaken',
                                              runtime=self._runtime)
            collection.save(assessment_taken_map)
        else:
            raise errors.IllegalState()"""

    is_answer_available = """
        # Note: we need more settings elsewhere to indicate answer available conditions
        # This makes the simple assumption that answers are available only when
        # a response has been submitted for an Item.
        try:
            self.get_response(assessment_section_id, item_id)
        except errors.IllegalState:
            return False
        else:
            return True"""
    
    get_answers = """
        if self.is_answer_available(assessment_section_id, item_id):
            return self.get_assessment_section(assessment_section_id)._get_answers(question_id=item_id)
        raise errors.IllegalState()"""

    additional_methods = """

    def is_feedback_available(assessment_section_id, item_id):
        \"\"\"Is feedback available for this item in this section\"\"\"
        return self.get_assessment_section(assessment_section_id)._is_feedback_available(item_id)

    def get_feedback(assessment_section_id, item_id):
        \"\"\"Get feedback for this item in this section\"\"\"
        return self.get_assessment_section(assessment_section_id)._get_feedback(item_id)

    def is_solution_available(assessment_section_id, item_id):
        \"\"\"Is a solution available for this item in this section\"\"\"
        return self.get_assessment_section(assessment_section_id)._is_solution_available(item_id)

    def get_solution(assessment_section_id, item_id):
        \"\"\"Get solution for this item in this section\"\"\"
        return self.get_assessment_section(assessment_section_id)._get_solution(item_id)

    def is_correctness_available(assessment_section_id, item_id):
        \"\"\"Is a determination of correctness available for this item in this section\"\"\"
        return self.get_assessment_section(assessment_section_id)._is_correctness_available(item_id)

    def is_correct(assessment_section_id, item_id):
        \"\"\"is the response for this item in this section correct\"\"\"
        return self.get_assessment_section(assessment_section_id)._is_correct(item_id)

    def get_correctness(assessment_section_id, item_id):
        \"\"\"Get correctness for this item in this section\"\"\"
        return self.get_assessment_section(assessment_section_id)._get_correctness(item_id)

    def get_confused_learning_objective_ids(assessment_section_id, item_id):
        \"\"\"Get confused objective ids for this item in this section\"\"\"
        return self.get_assessment_section(assessment_section_id)._get_confused_learning_objective_ids(item_id)

    def _get_assessment_taken(self, assessment_taken_id):
        \"\"\"Helper method for getting an AssessmentTaken objects given an Id.\"\"\"
        mgr = self._get_provider_manager('ASSESSMENT')
        lookup_session = mgr.get_assessment_taken_lookup_session(proxy=self._proxy) # Should this be _for_bank?
        lookup_session.use_federated_bank_view()
        return lookup_session.get_assessment_taken(assessment_taken_id)"""

class AssessmentResultsSession:

    import_statements = [
        'from .assessment_utilities import get_assessment_section',
        'from .assessment_utilities import get_item_lookup_session',
        'from ..utilities import OsidListList',
        'from ..primitives import Id',
        'from .objects import ItemList',
        'from .objects import ResponseList',
    ]

    init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None):
        OsidSession.__init__(self)
        self._catalog_class = objects.Bank
        self._session_name = 'AssessmentResultsSession'
        self._catalog_name = 'Bank'
        OsidSession._init_object(
            self, catalog_id,
            proxy,
            runtime,
            db_name='assessment',
            cat_name='Bank',
            cat_class=objects.Bank)"""

    can_access_assessment_results = """
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    get_items = """
        mgr = self._get_provider_manager('ASSESSMENT', local=True)
        taken_lookup_session = mgr.get_assessment_taken_lookup_session(proxy=self._proxy)
        taken = taken_lookup_session.get_assessment_taken(assessment_taken_id)
        ils = get_item_lookup_session(runtime=self._runtime, proxy=self._proxy)
        item_list = []
        if 'sections' in taken._my_map:
            for section_id in taken._my_map['sections']:
                section = get_assessment_section(Id(section_id))
                for question in section._my_map['questions']:
                    item_list.append(ils.get_item(question['questionId']))
        return ItemList(item_list)"""

    get_responses = """
        mgr = self._get_provider_manager('ASSESSMENT', local=True)
        taken_lookup_session = mgr.get_assessment_taken_lookup_session(proxy=self._proxy)
        taken = taken_lookup_session.get_assessment_taken(assessment_taken_id)
        response_list = OsidListList
        if 'sections' in taken._my_map:
            for section_id in taken._my_map['sections']:
                section = get_assessment_section(Id(section_id))
                response_list.append(section._get_responses())
        return ResponseList(response_list)"""

    are_results_available = """
        # not implemented yet
        return False"""

    get_grade_entries = """
        # not implemented yet and are_results_available is False
        raise IllegalState()"""

class ItemAdminSession:
    
    import_statements = [
        'from ..primitives import Id',
        'from dlkit.abstract_osid.osid import errors',
        'from bson.objectid import ObjectId',
        'from ..utilities import MongoClientValidated',
        'UPDATED = True',
        'CREATED = True'
    ]
    
    # This method is hand implemented to raise errors.and error if the item
    # is found to be associated with an assessment
    delete_item_import_templates = [
        'from ...abstract_osid.id.primitives import Id as ABCId'
    ]

    delete_item = """
        if not isinstance(item_id, ABCId):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        collection = MongoClientValidated('assessment_authoring',
                                          collection='AssessmentPart',
                                          runtime=self._runtime)
        # This needs to be updated to actually check for AssessmentsTaken (and does that find even work?)
        if collection.find({'itemIds': str(item_id)}).count() != 0:
            raise errors.IllegalState('this Item is being used in one or more Assessments')
        collection = MongoClientValidated('assessment',
                                          collection='Item',
                                          runtime=self._runtime)
        item_map = collection.find_one({'_id': ObjectId(item_id.get_identifier())})
        objects.Item(osid_object_map=item_map,
                     runtime=self._runtime,
                     proxy=self._proxy)._delete()
        collection.delete_one({'_id': ObjectId(item_id.get_identifier())})"""
    
    # These methods overwrite the canonical aggregate object admin methods to
    # deal with authoring Questions with are special: ie. there is only one per
    # Item.  Perhaps we will see this pattern again and can make templates.
    create_question_import_templates = [
        'from ...abstract_osid.assessment.objects import QuestionForm as ABCQuestionForm'
    ]

    create_question = """
        collection = MongoClientValidated('assessment',
                                          collection='Item',
                                          runtime=self._runtime)
        if not isinstance(question_form, ABCQuestionForm):
            raise errors.InvalidArgument('argument type is not an QuestionForm')
        if question_form.is_for_update():
            raise errors.InvalidArgument('the QuestionForm is for update only, not create')
        try:
            if self._forms[question_form.get_id().get_identifier()] == CREATED:
                raise errors.IllegalState('question_form already used in a create transaction')
        except KeyError:
            raise errors.Unsupported('question_form did not originate from this session')
        if not question_form.is_valid():
            raise errors.InvalidArgument('one or more of the form elements is invalid')
        item_id = Id(question_form._my_map['itemId']).get_identifier()
        question_form._my_map['_id'] = ObjectId(item_id)
        item = collection.find_one({'$and': [{'_id': ObjectId(item_id)},
                                             {'assigned' + self._catalog_name + 'Ids': {'$in': [str(self._catalog_id)]}}]})
        # set the name in the question, so it can be shown to students
        question_form._my_map['displayName']['text'] = item['displayName']['text']
        question_form._my_map['description']['text'] = item['description']['text']
        if item['question'] is None:
            item['question'] = question_form._my_map
        else:
            item['question'] = question_form._my_map # Let's just assume we can overwrite it
        collection.save(item)
        self._forms[question_form.get_id().get_identifier()] = CREATED
        return objects.Question(osid_object_map=question_form._my_map,
                                runtime=self._runtime,
                                proxy=self._proxy)"""

    get_question_form_for_update_import_templates = [
        'from ...abstract_osid.id.primitives import Id as ABCId'
    ]

    get_question_form_for_update = """
        collection = MongoClientValidated('assessment',
                                          collection='Item',
                                          runtime=self._runtime)
        if not isinstance(question_id, ABCId):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        document = collection.find_one({'question._id': ObjectId(question_id.get_identifier())})
        obj_form = objects.QuestionForm(osid_object_map=document['question'],
                                        runtime=self._runtime,
                                        proxy=self._proxy)
        self._forms[obj_form.get_id().get_identifier()] = not UPDATED
        return obj_form"""

    update_question_import_templates = [
        'from ...abstract_osid.assessment.objects import QuestionForm as ABCQuestionForm'
    ]

    update_question = """
        collection = MongoClientValidated('assessment',
                                          collection='Item',
                                          runtime=self._runtime)
        if not isinstance(question_form, ABCQuestionForm):
            raise errors.InvalidArgument('argument type is not an QuestionForm')
        if not question_form.is_for_update():
            raise errors.InvalidArgument('the QuestionForm is for update only, not create')
        try:
            if self._forms[question_form.get_id().get_identifier()] == UPDATED:
                raise errors.IllegalState('question_form already used in an update transaction')
        except KeyError:
            raise errors.Unsupported('question_form did not originate from this session')
        if not question_form.is_valid():
            raise errors.InvalidArgument('one or more of the form elements is invalid')
        item_id = Id(question_form._my_map['itemId']).get_identifier()
        item = collection.find_one({'$and': [{'_id': ObjectId(item_id)},
                                   {'assigned' + self._catalog_name + 'Ids': {'$in': [str(self._catalog_id)]}}]})
        item['question'] = question_form._my_map
        try:
            collection.save(item)
        except: # what exceptions does mongodb save raise?
            raise errors.OperationFailed()
        self._forms[question_form.get_id().get_identifier()] = UPDATED
        # Note: this is out of spec. The OSIDs don't require an object to be returned:
        return objects.Question(osid_object_map=question_form._my_map,
                                runtime=self._runtime,
                                proxy=self._proxy)"""


class AssessmentAdminSession:
    
    import_statements = [
        'from ..primitives import Id',
        'from dlkit.abstract_osid.osid import errors',
        'from bson.objectid import ObjectId',
        'from ..utilities import MongoClientValidated',
        'UPDATED = True',
        'CREATED = True'
        ]

    delete_assessment_import_templates = [
        'from ...abstract_osid.id.primitives import Id as ABCId',
        'from ..assessment_authoring import objects as assessment_authoring_objects'
    ]

    delete_assessment = """
        \"\"\"Delete all the children AssessmentParts recursively, too\"\"\"
        def remove_children_parts(parent_id):
            part_collection = MongoClientValidated('assessment_authoring',
                                                    collection='AssessmentPart',
                                                    runtime=self._runtime)
            if 'assessment.Assessment' in parent_id:
                query = {"assessmentId": parent_id}
            else:
                query = {"assessmentPartId": parent_id}

            for part in part_collection.find(query):
                part = assessment_authoring_objects.AssessmentPart(osid_object_map=part,
                                              runtime=self._runtime,
                                              proxy=self._proxy)
                part_collection.delete_one({'_id': ObjectId(part.ident.get_identifier())})
                remove_children_parts(str(part.ident))

        if not isinstance(assessment_id, ABCId):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        collection = MongoClientValidated('assessment',
                                          collection='AssessmentOffered',
                                          runtime=self._runtime)
        if collection.find({'assessmentId': str(assessment_id)}).count() != 0:
            raise errors.IllegalState('there are still AssessmentsOffered associated with this Assessment')
        collection = MongoClientValidated('assessment',
                                          collection='Assessment',
                                          runtime=self._runtime)
        collection.delete_one({'_id': ObjectId(assessment_id.get_identifier())})
        remove_children_parts(str(assessment_id))
        """

class AssessmentTakenLookupSession:
    
    import_statements = [
        'from ..primitives import Id',
        'from dlkit.abstract_osid.osid import errors',
        'from . import objects',
        'from ..utilities import MongoClientValidated'
    ]
    
    # This is hand-built, but there may be a pattern to try to map, specifically
    # getting objects for another package object and a persisted id thingy
    get_assessments_taken_for_taker_and_assessment_offered = """
        # NOTE: This implementation currently ignores plenary view
        collection = MongoClientValidated('assessment',
                                          collection='AssessmentTaken',
                                          runtime=self._runtime)

        am = self._get_provider_manager('ASSESSMENT')
        aols = am.get_assessment_offered_lookup_session(proxy=self._proxy)
        aols.use_federated_bank_view()
        offered = aols.get_assessment_offered(assessment_offered_id)
        try:
            deadline = offered.get_deadline()
            nowutc = DateTime.utcnow()
            if nowutc > deadline:
                raise errors.PermissionDenied('you are passed the deadline for the offered')
        except errors.IllegalState:
            # no deadline set
            pass

        result = collection.find(
            dict({'assessmentOfferedId': str(assessment_offered_id),
                  'takingAgentId': str(resource_id)},
                  **self._view_filter())).sort('_id', DESCENDING)
        return objects.AssessmentTakenList(result, runtime=self._runtime, proxy=self._proxy)"""

    get_assessments_taken_for_assessment = """
        collection = MongoClientValidated('assessment',
                                          collection='AssessmentOffered',
                                          runtime=self._runtime)
        result = collection.find(
            dict({'assessmentId': str(assessment_id)},
                 **self._view_filter())).sort('_id', DESCENDING)
        assessments_offered = objects.AssessmentOfferedList(
            result,
            runtime=self._runtime)

        collection = MongoClientValidated('assessment',
                                          collection='AssessmentTaken',
                                          runtime=self._runtime)
        ao_ids = []
        for assessment_offered in assessments_offered:
            ao_ids.append(str(assessment_offered.get_id()))

        result = collection.find(
            dict({'assessmentOfferedId': {'$in':[ao_ids]}},
                 **self._view_filter())).sort('_id', DESCENDING)
        return objects.AssessmentTakenList(result,
                                           runtime=self._runtime,
                                           proxy=self._proxy)"""


class AssessmentOfferedAdminSession:
    
    deprecated_import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..utilities import MongoClientValidated',
        'UPDATED = True',
        'CREATED = True',
    ]
    
    deprecated_get_assessment_offered_form_for_create = """
        ##
        # This impl differs from the usual get_osid_object_form_for_create method in that it
        # sets a default display name based on the underlying Assessment...
        from ...abstract_osid.id.primitives import Id as ABCId
        from ...abstract_osid.type.primitives import Type as ABCType
        if not isinstance(assessment_id, ABCId):
            raise errors.InvalidArgument('argument is not a valid OSID Id')
        for arg in assessment_offered_record_types:
            if not isinstance(arg, ABCType):
                raise errors.InvalidArgument('one or more argument array elements is not a valid OSID Type')
        ##
        #...Here:
        collection = MongoClientValidated('assessment',
                                          collection='Assessment',
                                          runtime=self._runtime)
        assessment_map = collection.find_one(
            {'$and': [{'_id': ObjectId(assessment_id.get_identifier())}, {'bankId': str(self._catalog_id)}]})
        ##
        if assessment_offered_record_types == []:
            ## WHY are we passing bank_id = self._catalog_id below, seems redundant:
            obj_form = objects.AssessmentOfferedForm(
                bank_id=self._catalog_id,
                assessment_id=assessment_id,
                catalog_id=self._catalog_id,
                default_display_name=assessment_map['displayName']['text'],
                runtime=self._runtime,
                proxy=self._proxy)
        else:
            obj_form = objects.AssessmentOfferedForm(
                bank_id=self._catalog_id,
                record_types=assessment_offered_record_types,
                assessment_id=assessment_id,
                catalog_id=self._catalog_id,
                default_display_name=assessment_map['displayName']['text'],
                runtime=self._runtime,
                proxy=self._proxy)
        obj_form._for_update = False
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form"""

class AssessmentTakenAdminSession:
    
    deprecated_import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..utilities import MongoClientValidated',
        'UPDATED = True',
        'CREATED = True',
    ]

    import_statements = [
        'from dlkit.primordium.calendaring.primitives import DateTime'
    ]

    create_assessment_taken_import_templates = [
        'from ...abstract_osid.assessment.objects import AssessmentTakenForm as ABCAssessmentTakenForm',
        'from ..osid.osid_errors import PermissionDenied'
    ]
    
    create_assessment_taken = """
        ##
        # This impl differs from the usual create_osid_object method in that it
        # sets an agent id and default display name based on the underlying Assessment
        # and checks for exceeding max attempts...
        collection = MongoClientValidated('assessment',
                                          collection='AssessmentTaken',
                                          runtime=self._runtime)
        if not isinstance(assessment_taken_form, ABCAssessmentTakenForm):
            raise errors.InvalidArgument('argument type is not an AssessmentTakenForm')
        if assessment_taken_form.is_for_update():
            raise errors.InvalidArgument('the AssessmentForm is for update only, not create')
        try:
            if self._forms[assessment_taken_form.get_id().get_identifier()] == CREATED:
                raise errors.IllegalState('assessment_taken_form already used in a create transaction')
        except KeyError:
            raise errors.Unsupported('assessment_taken_form did not originate from this session')
        if not assessment_taken_form.is_valid():
            raise errors.InvalidArgument('one or more of the form elements is invalid')
        ##
        # ...here:
        assessment_offered_id = Id(assessment_taken_form._my_map['assessmentOfferedId'])
        assessment_offered = AssessmentOfferedLookupSession(
            catalog_id=self._catalog_id, runtime=self._runtime).get_assessment_offered(assessment_offered_id)
        try:
            if assessment_offered.has_max_attempts():
                max_attempts = assessment_offered.get_max_attempts()
                num_takens = collection.find({'$and': [{'assessmentOfferedId': str(assessment_offered.get_id())},
                                                       {'takingAgentId': str(self.get_effective_agent_id())},
                                                       {'assigned' + self._catalog_name + 'Ids': {'$in': [str(self._catalog_id)]}}]}).count()
                if num_takens >= max_attempts:
                    raise errors.PermissionDenied('exceeded max attempts')
        except AttributeError:
            pass
        assessment_taken_form._my_map['takingAgentId'] = str(self.get_effective_agent_id())

        insert_result = collection.insert_one(assessment_taken_form._my_map)
        self._forms[assessment_taken_form.get_id().get_identifier()] = CREATED
        return objects.AssessmentTaken(
            osid_object_map=collection.find_one({'_id': insert_result.inserted_id}),
            runtime=self._runtime,
            proxy=self._proxy)"""

    get_assessment_taken_form_for_create = """
        if not isinstance(assessment_offered_id, ABCId):
            raise errors.InvalidArgument('argument is not a valid OSID Id')
        for arg in assessment_taken_record_types:
            if not isinstance(arg, ABCType):
                raise errors.InvalidArgument('one or more argument array elements is not a valid OSID Type')

        am = self._get_provider_manager('ASSESSMENT')
        aols = am.get_assessment_offered_lookup_session(proxy=self._proxy)
        aols.use_federated_bank_view()
        offered = aols.get_assessment_offered(assessment_offered_id)
        try:
            deadline = offered.get_deadline()
            nowutc = DateTime.utcnow()
            if nowutc > deadline:
                raise errors.PermissionDenied('you are passed the deadline for the offered')
        except errors.IllegalState:
            # no deadline set
            pass

        if assessment_taken_record_types == []:
            ## WHY are we passing bank_id = self._catalog_id below, seems redundant:
            obj_form = objects.AssessmentTakenForm(
                bank_id=self._catalog_id,
                assessment_offered_id=assessment_offered_id,
                catalog_id=self._catalog_id,
                runtime=self._runtime,
                proxy=self._proxy)
        else:
            obj_form = objects.AssessmentTakenForm(
                bank_id=self._catalog_id,
                record_types=assessment_taken_record_types,
                assessment_offered_id=assessment_offered_id,
                catalog_id=self._catalog_id,
                runtime=self._runtime,
                proxy=self._proxy)
        obj_form._for_update = False
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form"""

class AssessmentBasicAuthoringSession:
    
    import_statements = [
        #'from bson.objectid import ObjectId',
        'from dlkit.abstract_osid.osid import errors',
        #'from ..primitives import Id',
        'from . import objects',
        'from ..osid.sessions import OsidSession',
        'from .assessment_utilities import get_first_part_id_for_assessment',
    ]
    
    init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None):
        OsidSession.__init__(self)
        self._catalog_class = objects.Bank
        self._session_name = 'AssessmentSession'
        self._catalog_name = 'Bank'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='assessment',
            cat_name='Bank',
            cat_class=objects.Bank)
        mgr = self._get_provider_manager('ASSESSMENT_AUTHORING', local=True)
        self._part_item_session = mgr.get_assessment_part_item_session_for_bank(self._catalog_id, proxy=self._proxy)
        self._part_item_design_session = mgr.get_assessment_part_item_design_session_for_bank(self._catalog_id, proxy=self._proxy)
        self._part_item_session.use_federated_bank_view()
        self._first_part_index = {}

    def _get_first_part_id(self, assessment_id):
        \"\"\"\This session implemenation assumes all items are assigned to the first assessment part"\"\"
        if assessment_id not in self._first_part_index:
            self._first_part_index[assessment_id] = get_first_part_id_for_assessment(
                assessment_id,
                runtime=self._runtime,
                proxy=self._proxy,
                create=True,
                bank_id=self._catalog_id)
        return self._first_part_index[assessment_id]"""
    
    can_author_assessments = """
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
    
    get_items = """
        if assessment_id.get_identifier_namespace() != 'assessment.Assessment':
            raise errors.InvalidArgument
        return self._part_item_session.get_assessment_part_items(self._get_first_part_id(assessment_id))"""
    
    add_item = """
        if assessment_id.get_identifier_namespace() != 'assessment.Assessment':
            raise errors.InvalidArgument
        self._part_item_design_session.add_item(item_id, self._get_first_part_id(assessment_id))"""
    
    remove_item = """
        if assessment_id.get_identifier_namespace() != 'assessment.Assessment':
            raise errors.InvalidArgument
        self._part_item_design_session.remove_item(item_id, self._get_first_part_id(assessment_id))"""
    
    move_item = """
        if assessment_id.get_identifier_namespace() != 'assessment.Assessment':
            raise errors.InvalidArgument
        self._part_item_design_session.move_item_behind(item_id, self._get_first_part_id(assessment_id), preceeding_item_id)"""
    
    order_items = """
        if assessment_id.get_identifier_namespace() != 'assessment.Assessment':
            raise errors.InvalidArgument
        self._part_item_design_session.order_items(item_ids, self._get_first_part_id(assessment_id))"""


class Question:
    
    import_statements = [
        '#from ..osid.objects import OsidObject',
        'from ..id.objects import IdList',
        'from ..primitives import Id',
        'from ..utilities import MongoClientValidated',
        'from bson.objectid import ObjectId',
    ]
    
    additional_methods = """
    ##
    # Overide osid.Identifiable.get_id() method to cast this question id as its item id:
    def get_id(self):
        return Id(self._my_map['itemId'])
    
    id_ = property(fget=get_id)
    ident = property(fget=get_id)
    
    ##
    # This method mirrors that in the Item so that questions can also be inspected for learning objectives:
    def get_learning_objective_ids(self):
        collection = MongoClientValidated('assessment',
                                          collection='Item',
                                          runtime=self._runtime)
        item_map = collection.find_one({'_id': ObjectId(Id(self._my_map['itemId']).get_identifier())})
        return IdList(item_map['learningObjectiveIds'])

    def get_object_map(self):
        obj_map = dict(self._my_map)
        del obj_map['itemId']
        lo_ids = self.get_learning_objective_ids()
        obj_map['learningObjectiveIds'] = [str(lo_id) for lo_id in lo_ids]
        obj_map = osid_objects.OsidObject.get_object_map(self, obj_map)
        obj_map['id'] = str(self.get_id())
        return obj_map

    object_map = property(fget=get_object_map)"""

class Answer:

    additional_methods = """
    def get_object_map(self):
        obj_map = dict(self._my_map)
        del obj_map['itemId']
        return osid_objects.OsidObject.get_object_map(self, obj_map)

    object_map = property(fget=get_object_map)"""

class Item:
    
    get_question_id = """
        self.get_question().get_id()"""
    
    get_question = """
        return Question(osid_object_map=self._my_map['question'], runtime=self._runtime)"""
    
    additional_methods = """
    
    def get_configuration(self):
        config = dict()
        try:
            dict.update(self.get_question().get_configuration())
        except AttributeError:
            pass
        for record in self._records:
            try:
                dict.update(record.get_configuration())
            except AttributeError:
                pass
        return config # SHould this method build a real OSID configuration instead?
    
    def get_object_map(self):
        obj_map = dict(self._my_map)
        if obj_map['question']:
            obj_map['question'] = self.get_question().get_object_map()
        obj_map['answers'] = []
        for answer in self.get_answers():
            obj_map['answers'].append(answer.get_object_map())
        return osid_objects.OsidObject.get_object_map(self, obj_map)

    object_map = property(fget=get_object_map)

    def _delete(self):
        try:
            self.get_question()._delete()
        except:
            pass
        finally:
            for answer in self.get_answers():
                answer._delete()
            osid_objects.OsidObject._delete(self)

    def is_feedback_available(self):
        \"\"\"is general feedback available for this Item

        to be overriden in a record extension

        \"\"\"
        return False

    def get_feedback(self):
        \"\"\"get general feedback for this Item
        to be overriden in a record extension

        \"\"\"
        if self.is_feedback_available():
            pass # what is feedback anyway? Just a DisplayText or something more?
        raise IllegalState()

    def is_solution_available(self):
        \"\"\"is a solution available for this Item (is this different than feedback?)

        to be overriden in a record extension

        \"\"\"
        return False

    def get_solution(self):
        \"\"\"get general feedback for this Item (is this different than feedback?)

        to be overriden in a record extension

        \"\"\"
        if self.is_solution_available():
            pass
        raise IllegalState()

    def is_feedback_available_for_response(self, response):
        \"\"\"is feedback available for a particular response
        to be overriden in a record extension

        \"\"\"
        return False

    def get_feedback_for_response(self, response):
        \"\"\"get feedback for a particular response
        to be overriden in a record extension
        \"\"\"
        if self.is_feedback_available_for_response(response):
            pass # what is feedback anyway? Just a DisplayText or something more?
        raise IllegalState()

    def is_correctness_available_for_response(self, response):
        \"\"\"is a measure of correctness available for a particular response
        
        to be overriden in a record extension

        \"\"\"
        return False
    
    def is_response_correct(self, response):
        \"\"\"returns True if response evaluates to an Item Answer that is 100 percent correct

        to be overriden in a record extension

        \"\"\"
        if self.is_correctness_available_for_response(response):
            pass # return True or False
        raise IllegalState()

    def get_correctness_for_response(self, response):
        \"\"\"get measure of correctness available for a particular response

        to be overriden in a record extension

        \"\"\"
        if self.is_correctness_available_for_response(response):
            pass # return a correctness score 0 thru 100
        raise IllegalState()

    def are_confused_learning_objective_ids_available_for_response(self, response):
        \"\"\"is a learning objective available for a particular response
        to be overriden in a record extension

        \"\"\"
        return False

    def get_confused_learning_objective_ids_for_response(self, response):
        \"\"\"get learning objectives for a particular response
        
        to be overriden in a record extension

        \"\"\"
        if self.are_confused_learning_objective_ids_available_for_response(response):
            pass # return Objective IdList
        raise IllegalState()"""


class Assessment:

    import_statements = [
        "from .assessment_utilities import SIMPLE_SEQUENCE_RECORD_TYPE"
    ]

    additional_methods = """
    def has_children(self):
        \"\"\"This method can be overwritten by a record extension.\"\"\"
        return self._supports_simple_sequencing() and self._my_map['childIds']

    def get_child_ids(self):
        \"\"\"This method can be overwritten by a record extension.\"\"\"
        if self._supports_simple_sequencing():
            return IdList(self._my_map['childIds'])
        else:
            raise errors.IllegalState()

    def has_next_assessment_part(self, assessment_part_id):
        \"\"\"This supports the basic simple sequence case. Can be overriden in a record for other cases\"\"\"
        if not self.supports_child_ordering or not self.supports_simple_child_sequencing:
            raise AttributeError() # Only available through a record extension
        if 'childIds' in self._my_map and str(assessment_part_id) in self._my_map['childIds']:
            if self._my_map['childIds'][-1] != str(assessment_part_id):
                return True
            else:
                return False
        raise errors.NotFound('the Part with Id ' + str(assessment_part_id) + ' is not a child of this Part')

    def get_next_assessment_part_id(self, assessment_part_id=None):
        \"\"\"This supports the basic simple sequence case. Can be overriden in a record for other cases\"\"\"
        if assessment_part_id is None:
            part_id = self.get_id()
        else:
            part_id = assessment_part_id
        return get_next_part_id(part_id,
                                runtime=self._runtime,
                                proxy=self._proxy)[0]
        # if self.has_next_assessment_part(assessment_part_id):
        #     return Id(self._my_map['childIds'][self._my_map['childIds'].index(str(assessment_part_id)) + 1])

    def get_next_assessment_part(self, assessment_part_id):
        next_part_id = self.get_next_assessment_part_id(assessment_part_id)
        mgr = self._get_provider_manager('ASSESSMENT_AUTHORING', local=True)
        lookup_session = mgr.get_assessment_part_lookup_session(proxy=self._proxy)
        return lookup_session.get_assessment_part(next_part_id)

    def are_items_sequential(self):
        \"\"\"This method can be overwritten by a record extension.\"\"\"
        return False

    def are_items_shuffled(self):
        \"\"\"This method can be overwritten by a record extension.\"\"\"
        return False

    def _supports_simple_sequencing(self):
        return bool(str(SIMPLE_SEQUENCE_RECORD_TYPE) in self._my_map['recordTypeIds'])

    def get_object_map(self):
        obj_map = dict(self._my_map)
        if 'itemIds' in obj_map:
            del obj_map['itemIds']
        return osid_objects.OsidObject.get_object_map(self, obj_map)

    object_map = property(fget=get_object_map)"""


class AssessmentForm:

    import_statements = [
        "from .assessment_utilities import SIMPLE_SEQUENCE_RECORD_TYPE"
    ]

    init = """
    _namespace = 'assessment.Assessment'

    def __init__(self, **kwargs):
        osid_objects.OsidObjectForm.__init__(self, object_name='ASSESSMENT', **kwargs)
        self._mdata = default_mdata.get_assessment_mdata()
        self._init_metadata(**kwargs)
        if not self.is_for_update():
            self._init_map(**kwargs)

    def _init_metadata(self, **kwargs):
        \"\"\"Initialize form metadata\"\"\"
        osid_objects.OsidObjectForm._init_metadata(self, **kwargs)
        self._rubric_default = self._mdata['rubric']['default_id_values'][0]
        self._level_default = self._mdata['level']['default_id_values'][0]

    def _init_map(self, record_types=None, **kwargs):
        \"\"\"Initialize form map\"\"\"
        osid_objects.OsidObjectForm._init_map(self, record_types=record_types)
        self._my_map['rubricId'] = self._rubric_default
        self._my_map['assignedBankIds'] = [str(kwargs['bank_id'])]
        self._my_map['levelId'] = self._level_default
        if self._supports_simple_sequencing():
            self._my_map['childIds'] = []"""

    additional_methods = """
    def _supports_simple_sequencing(self):
        return bool(str(SIMPLE_SEQUENCE_RECORD_TYPE) in self._my_map['recordTypeIds'])

    def set_children(self, child_ids):
        \"\"\"Set the children IDs\"\"\"
        if not self._supports_simple_sequencing():
            raise errors.IllegalState()
        self._my_map['childIds'] = [str(i) for i in child_ids]"""

class AssessmentOffered:
    
    import_statements = [
        'from ..primitives import Id',
        'from ..primitives import DateTime',
        'from ..primitives import Duration',
        'from dlkit.abstract_osid.osid import errors',
        ]
    
    additional_methods = """
    def get_display_name(self):
        # Overrides osid.objects.OsidObject.get_display_name to default to Assessment's
        # display_name if none has been authored for this AssessmentOffered
        from ..osid.objects import OsidObject
        if osid_objects.OsidObject.get_display_name(self).get_text():
            return osid_objects.OsidObject.get_display_name(self)
        else:
            return self.get_assessment().get_display_name()
    
    def get_description(self):
        # Overrides osid.objects.OsidObject.get_description to default to Assessment's
        # description if none has been authored for this AssessmentOffered
        from ..osid.objects import OsidObject
        if osid_objects.OsidObject.get_description(self).get_text():
            return osid_objects.OsidObject.get_description(self)
        else:
            return self.get_assessment().get_description()

    def get_object_map(self):
        obj_map = dict(self._my_map)
        if obj_map['startTime'] is not None:
            start_time = obj_map['startTime']
            obj_map['startTime'] = dict()
            obj_map['startTime']['year'] = start_time.year
            obj_map['startTime']['month'] = start_time.month
            obj_map['startTime']['day'] = start_time.day
            obj_map['startTime']['hour'] = start_time.hour
            obj_map['startTime']['minute'] = start_time.minute
            obj_map['startTime']['second'] = start_time.second
            obj_map['startTime']['microsecond'] = start_time.microsecond
        if obj_map['deadline'] is not None:
            deadline = obj_map['deadline']
            obj_map['deadline'] = dict()
            obj_map['deadline']['year'] = deadline.year
            obj_map['deadline']['month'] = deadline.month
            obj_map['deadline']['day'] = deadline.day
            obj_map['deadline']['hour'] = deadline.hour
            obj_map['deadline']['minute'] = deadline.minute
            obj_map['deadline']['second'] = deadline.second
            obj_map['deadline']['microsecond'] = deadline.microsecond
        obj_map = osid_objects.OsidObject.get_object_map(self, obj_map)
        if obj_map['displayName']['text'] == '':
            obj_map['displayName']['text'] = self.get_display_name().get_text()
        if obj_map['description']['text'] == '':
            obj_map['description']['text'] = self.get_description().get_text()
        return obj_map

    object_map = property(fget=get_object_map)

    def are_sections_sequential(self):
        \"\"\"This method can be overwritten by a record extension.\"\"\"
        if not self.get_assessment().uses_simple_section_sequencing(): # Records should check this
            return True
        return True

    def are_sections_shuffled(self):
        \"\"\"This method can be overwritten by a record extension.\"\"\"
        if not self.get_assessment().uses_simple_section_sequencing(): # Records should check this
            return False
        return False"""
    
    has_start_time_template = """
        # Implemented from template for osid.assessment.AssessmentOffered.has_start_time_template
        return bool(self._my_map['${var_name_mixed}'])"""
    
    get_start_time_template = """
        # Implemented from template for osid.assessment.AssessmentOffered.get_start_time_template
        if not bool(self._my_map['${var_name_mixed}']):
            raise errors.IllegalState()
        dt = self._my_map['${var_name_mixed}']
        return DateTime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)"""
    
    has_duration_template = """
        # Implemented from template for osid.assessment.AssessmentOffered.has_duration_template
        return bool(self._my_map['${var_name_mixed}'])"""
    
    get_duration_template = """
        # Implemented from template for osid.assessment.AssessmentOffered.get_duration_template
        if not bool(self._my_map['${var_name_mixed}']):
            raise errors.IllegalState()
        return Duration(**self._my_map['${var_name_mixed}'])"""

    are_items_sequential = """
        if self._my_map['itemsSequential'] is None:
            return self.get_assessment().are_items_sequential()
        return bool(self._my_map['itemsSequential'])"""

    are_items_shuffled = """
        if self._my_map['itemsShuffled'] is None:
            return self.get_assessment().are_items_shuffled()
        return bool(self._my_map['itemsShuffled'])"""


class AssessmentOfferedForm:
    
    set_start_time_template = """
        # Implemented from template for osid.assessment.AssessmentOfferedForm.set_start_time_template
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_${arg0_type_under}(
                ${arg0_name},
                self.get_${var_name}_metadata()):
            raise errors.InvalidArgument()
        self._my_map['${var_name_mixed}'] = ${arg0_name}"""
    
    # This looks just like the generic one. Need to find in the pattern?
    clear_start_time_template = """
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['${var_name_mixed}'] = self._${var_name}_default"""
    
    set_duration_template = """
        # Implemented from template for osid.assessment.AssessmentOfferedForm.set_duration_template
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_${arg0_type_under}(${arg0_name},
                                self.get_${arg0_name}_metadata()):
            raise errors.InvalidArgument()
        map = dict()
        map['days'] = ${arg0_name}.days
        map['seconds'] = ${arg0_name}.seconds
        map['microseconds'] = ${arg0_name}.microseconds
        self._my_map['${var_name_mixed}'] = map"""

class AssessmentOfferedQuery:
    
    match_start_time_template = """
        self._match_minimum_date_time('${var_name_mixed}', ${arg0_name}, match)
        self._match_maximum_date_time('${var_name_mixed}', ${arg1_name}, match)"""

class AssessmentTaken:
    
    import_statements = [
        'from ..primitives import Id',
        'from dlkit.abstract_osid.osid import errors',
        'from ..osid.objects import OsidObject',
        'from ..utilities import MongoClientValidated',
        'from .assessment_utilities import get_first_part_id_for_assessment',
        'from .assessment_utilities import get_next_part_id',
        'from .assessment_utilities import get_assessment_section',
        'from dlkit.primordium.id.primitives import Id',
        'from bson.objectid import ObjectId',
        'from ..primitives import DateTime, DisplayText',
    ]
    
    additional_methods = """
    def get_display_name(self):
        # Overrides osid.objects.OsidObject.get_display_name to default to AssessmentOffered's
        # display_name if none has been authored for this AssessmentTaken
        from ..osid.objects import OsidObject
        if OsidObject.get_display_name(self).get_text():
            return OsidObject.get_display_name(self)
        else:
            return self.get_assessment_offered().get_display_name()

    def get_description(self):
        # Overrides osid.objects.OsidObject.get_description to default to AssessmentOffered's
        # description if none has been authored for this AssessmentTaken
        from ..osid.objects import OsidObject
        if OsidObject.get_description(self).get_text():
            return OsidObject.get_description(self)
        else:
            return self.get_assessment_offered().get_description()

    def _update_available_sections(self):
        # THIS IS NOT RIGHT. LOOPS WITH _get_first_assessment_section
        if ('sections' not in self._my_map or not self._my_map['sections']):
            section_id = self._get_first_assessment_section().get_id()
        else:
            section_id = Id(self._my_map['sections'][0])
        finished = False
        while not finished:
            try:
                section_id = self._get_next_assessment_section(section_id)
            except errors.IllegalState:
                finished = True

    def _create_section(self, part_id):
            init_map = {'assessmentPartId': str(part_id),
                        'assessmentTakenId': str(self.get_id()),
                        'recordTypeIds': []}
            return AssessmentSection(osid_object_map=init_map, runtime=self._runtime, proxy=self._proxy)

    def _get_first_assessment_section(self):
        \"\"\"Gets the first section for this Taken's Assessment.\"\"\"
        if ('sections' not in self._my_map or not self._my_map['sections']):
            # This is the first time for this Taken, so start assessment
            # SHOULD THIS USE self._update_available_sections????
            assessment_id = self.get_assessment_offered().get_assessment().get_id()
            first_part_id = get_first_part_id_for_assessment(assessment_id, runtime=self._runtime, proxy=self._proxy)
            first_section = self._create_section(first_part_id)
            self._my_map['sections'] = [str(first_section.get_id())]
            self._my_map['actualStartTime'] = DateTime.utcnow()
            self._save()
            return first_section
        else:
            return get_assessment_section(Id(self._my_map['sections'][0]),
                                          runtime=self._runtime)

    def _get_next_assessment_section(self, assessment_section_id):
        \"\"\"Gets the next section following section_id. 
        
        Assumes that section list exists in taken and section_id is in section list.
        Assumes that Section parts only exist as children of Assessments
        
        \"\"\"
        if self._my_map['sections'][-1] == str(assessment_section_id):
            # section_id represents the last seen section
            section = get_assessment_section(assessment_section_id,
                                             runtime=self._runtime,
                                             proxy=self._proxy)
            next_part_id, level = get_next_part_id(section._assessment_part_id,
                                                   runtime=self._runtime,
                                                   proxy=self._proxy) # Raises IllegalState
            next_section = self._create_section(next_part_id)
            self._my_map['sections'].append(str(next_section.get_id()))
            self._save()
            return next_section
        else:
            return get_assessment_section(
                Id(self._my_map['sections'][self._my_map['sections'].index(str(assessment_section_id)) + 1]),
                runtime=self._runtime)

    def _get_assessment_sections(self):
        \"\"\"Gets a SectionList of all Sections currently known to this AssessmentTaken\"\"\"
        section_list = []
        for section_idstr in self._my_map['sections']:
            section_list.append(get_assessment_section(Id(section_idstr)))
        return AssessmentSectionList(section_list, runtime=self._runtime, proxy=self._proxy)

    def _save(self):
        \"\"\"Saves the current state of this AssessmentTaken.

        Should be called every time the sections map changes.

        \"\"\"
        collection = MongoClientValidated('assessment',
                                          collection='AssessmentTaken',
                                          runtime=self._runtime)
        collection.save(self._my_map)

    def get_object_map(self):
        obj_map = dict(self._my_map)
        if obj_map['actualStartTime'] is not None:
            actual_start_time = obj_map['actualStartTime']
            obj_map['actualStartTime'] = dict()
            obj_map['actualStartTime']['year'] = actual_start_time.year
            obj_map['actualStartTime']['month'] = actual_start_time.month
            obj_map['actualStartTime']['day'] = actual_start_time.day
            obj_map['actualStartTime']['hour'] = actual_start_time.hour
            obj_map['actualStartTime']['minute'] = actual_start_time.minute
            obj_map['actualStartTime']['second'] = actual_start_time.second
            obj_map['actualStartTime']['microsecond'] = actual_start_time.microsecond
        if obj_map['completionTime'] is not None:
            completion_time = obj_map['completionTime']
            obj_map['completionTime'] = dict()
            obj_map['completionTime']['year'] = completion_time.year
            obj_map['completionTime']['month'] = completion_time.month
            obj_map['completionTime']['day'] = completion_time.day
            obj_map['completionTime']['hour'] = completion_time.hour
            obj_map['completionTime']['minute'] = completion_time.minute
            obj_map['completionTime']['second'] = completion_time.second
            obj_map['completionTime']['microsecond'] = completion_time.microsecond
        if 'sections' in obj_map:
            del obj_map['sections']
        obj_map = osid_objects.OsidObject.get_object_map(self, obj_map)
        if obj_map['displayName']['text'] == '':
            obj_map['displayName']['text'] = self.get_display_name().get_text()
        if obj_map['description']['text'] == '':
            obj_map['description']['text'] = self.get_description().get_text()
        return obj_map

    object_map = property(fget=get_object_map)"""

    get_taker_id = """
        if self._my_map['takerId']:
            return Id(self._my_map['takerId'])
        else:
            return Id(self._my_map['takingAgentId'])"""
    
    get_taker = """
        raise errors.Unimplemented()"""
    
    get_taking_agent_id = """
        return Id(self._my_map['takingAgentId'])"""
    
    get_taking_agent = """
        raise errors.Unimplemented()"""
    
    has_started = """
        assessment_offered = self.get_assessment_offered()
        if assessment_offered.has_start_time():
            return DateTime.utcnow() >= assessment_offered.get_start_time()
        else:
            return True"""
    
    get_actual_start_time = """
        if not self.has_started():
            raise errors.IllegalState('this assessment has not yet started')
        if self._my_map['actualStartTime'] is None:
            raise errors.IllegalState('this assessment has not yet been started by the taker')
        else:
            return self._my_map['actualStartTime']"""
    
    has_ended = """
        assessment_offered = self.get_assessment_offered()
        now = DateTime.utcnow()
        # There's got to be a better way to do this:
        if self._my_map['completionTime'] is not None:
            return True
        elif assessment_offered.has_deadline() and assessment_offered.has_duration():
            if self._my_map['actualStartTime'] is None:
                return now >= assessment_offered.get_deadline()
            else:
                return (now >= assessment_offered.get_deadline() and
                        now >= self._my_map['actualStartTime'] + assessment_offered.get_duration())
        elif assessment_offered.has_deadline():
            return now >= assessment_offered.get_deadline()
        elif assessment_offered.has_duration() and self._my_map['actualStartTime'] is not None:
            return now >= self._my_map['actualStartTime'] + assessment_offered.get_duration()
        else:
            return False"""
    
    get_completion_time = """
        if not self.has_ended():
            raise errors.IllegalState('this assessment has not yet ended')
        if not self._my_map['completionTime']:
            raise errors.OperationFailed('someone forgot to set the completion time')
        return self._my_map['completionTime']"""
    
    get_time_spent = """
        # Take another look at this. Not sure it's correct:
        if not self.has_started or not self.has_ended():
            raise errors.IllegalState()
        if self._my_map['completionTime'] is not None:
            return self.get_completion_time() - self.get_actual_start_time()
        else:
            raise errors.IllegalState()"""
    
    # This is not right.  Needs to be calculated?
    get_completion_template = """
        # Implemented from template for osid.assessment.AssessmentTaken.get_completion_template
        return int(self._my_map['${var_name_mixed}'])"""
    
    get_score_template = """
        # Implemented from template for osid.assessment.AssessmentTaken.get_score_template
        return float(self._my_map['${var_name_mixed}'])"""


class AssessmentTakenForm:
    
    ##
    # These import statements are here to make sure that the DisplayText related default
    # types are available for initializing data:
    import_statements = [
        'from .. import types',
        'from ..primitives import Type',
        'default_language_type = Type(**types.Language().get_type_data(\'DEFAULT\'))',
        'default_script_type = Type(**types.Script().get_type_data(\'DEFAULT\'))',
        'default_format_type = Type(**types.Format().get_type_data(\'DEFAULT\'))'
    ]


class AssessmentTakenQuery:
    match_taking_agent_id = """
        self._add_match('takingAgentId', str(agent_id), bool(match))"""


class AssessmentQuery:
    match_item_id = """
        self._add_match('itemIds', str(item_id), match)"""


class AssessmentSection:

    import_statements = [
        'from ..primitives import Id',
        'from .assessment_utilities import get_assessment_section',
        'from .assessment_utilities import get_default_question_map',
        'from .assessment_utilities import get_default_part_map',
        'from .rules import Response',
    ]

    init = """
    _namespace = 'assessment.AssessmentSection'

    def __init__(self, **kwargs):
        osid_objects.OsidObject.__init__(self, object_name='AssessmentSection', **kwargs)
        self._assessment_part_id = Id(self._my_map['assessmentPartId'])
        self._assessment_taken_id = Id(self._my_map['assessmentTakenId'])

        assessment_mgr = self._get_provider_manager('ASSESSMENT', local=True)
        if self._proxy:
            taken_lookup_session = assessment_mgr.get_assessment_taken_lookup_session(proxy=self._proxy)
        else:
            taken_lookup_session = assessment_mgr.get_assessment_taken_lookup_session()
        taken_lookup_session.use_federated_bank_view()
        self._assessment_taken = taken_lookup_session.get_assessment_taken(self._assessment_taken_id)

        authoring_mgr = self._get_provider_manager('ASSESSMENT_AUTHORING', local=True)
        if self._proxy:
            part_lookup_session = authoring_mgr.get_assessment_part_lookup_session(proxy=self._proxy)
        else:
            part_lookup_session = authoring_mgr.get_assessment_part_lookup_session()
        part_lookup_session.use_federated_bank_view()
        self._assessment_part = part_lookup_session.get_assessment_part(self._assessment_part_id)

        if 'questions' not in self._my_map: # This is the first instantiation
            self._initialize_part_map()

        if '_id' not in self._my_map:
            # could happen if not created with items -- then self._initialize_part_map()
            # will not call self._save(). But we need to assign it an ID
            self._save()

    def _initialize_part_map(self):
        \"\"\"Sets up assessmentPartMap with as much information as is initially available.\"\"\"
        self._my_map['assessmentParts'] = []
        self._my_map['questions'] = []
        item_ids = self._assessment_part.get_item_ids()
        if item_ids.available():
            # This is a simple section:
            self._load_simple_section_questions(item_ids)
        else:
            # This goes down the winding path...
            self._update_questions()

    def _load_simple_section_questions(self, item_ids):
        \"\"\"For the simple section case (common) just load the questions for the section.\"\"\"
        assessment_mgr = self._get_provider_manager('ASSESSMENT', local=True)
        lookup_session = assessment_mgr.get_item_lookup_session(proxy=self._proxy)
        lookup_session.use_federated_bank_view()
        items = lookup_session.get_items_by_ids(item_ids)
        display_num = 1
        for item in items:
            question_id = item.get_question().get_id()
            self._my_map['questions'].append(get_default_question_map(
                item.get_id(),
                question_id,
                self._assessment_part_id,
                [display_num]))
            display_num += 1
        self._save()

    def _save(self):
        \"\"\"Saves the current state of this AssessmentSection.

        Should be called every time the question map changes.

        \"\"\"
        collection = MongoClientValidated('assessment',
                                          collection='AssessmentSection',
                                          runtime=self._runtime)
        if '_id' in self._my_map: # This is the first time:
            collection.save(self._my_map)
        else:
            insert_result = collection.insert_one(self._my_map)
            self._my_map = collection.find_one({'_id': insert_result.inserted_id}) # To get the _id

    def get_object_map(self, obj_map=None):
        if obj_map is None:
            obj_map = dict(self._my_map)
        del obj_map['_id']

        obj_map.update(
            {'type': self._namespace.split('.')[-1],
             'id': str(self.get_id())})
        return obj_map

    object_map = property(get_object_map)

    # Let's give the Part attributes to the Section
    def __getattribute__(self, name):
        if not name.startswith('_') and name not in ['ident', 'get_id', 'id_']:
            try:
                return self._assessment_part[name]
            except AttributeError:
                return object.__getattribute__(self, name)
        return object.__getattribute__(self, name)"""

    get_assessment_taken_id = """
        return self._assessment_taken_id"""

    get_assessment_taken = """
        return self._assessment_taken"""

    has_allocated_time = """
        return bool(self._assessment_part.get_allocated_time())"""
    
    get_allocated_time = """
        return self._assessment_part.get_allocated_time()"""
    
    are_items_sequential = """
        return self._assessment_part.are_items_sequential()"""
    
    are_items_shuffled = """
        return self._assessment_part.are_items_shuffled()"""

    additional_methods = """
    # Model for question map to be constructed through taking an assessment section:
    #
    #   'questions': [{
    #       'questionId: <idstr of question>
    #       'itemId': <idstr of question's item>
    #       'partId': <idstr of the part this question came from>
    #       'labelElements': <list for constructing label, based on part levels, like [3, 1, 2]
    #       'responses: [<dict of the student's Answer>,
    #                    <or empty dict() if response has been cleared>,
    #                    <or None if no attempts have yet been made on question>,
    #                    <etc for additional attempts>...]
    #       }, <etc for additional questions>...]

    def _is_simple_section(self):
        \"\"\"Tests if this section is simple (ie, items assigned directly to Section Part).\"\"\"
        item_ids = self._get_assessment_part(self._assessment_part_id).get_item_ids()
        if item_ids.available():
            return True
        return False

    def _get_assessment_part(self, part_id):
        \"\"\"Gets an AssessmentPart given a part_id\"\"\"
        lookup_session = self._get_assessment_part_lookup_session()
        return lookup_session.get_assessment_part(part_id)

    def _update(self):
        \"\"\"Updates AssessmentSection to latest state in database.

        Should be called prior to major object events to assure that an
        assessment being taken on multiple devices are reasonably synchronized.

        \"\"\"
        collection = MongoClientValidated('assessment',
                                          collection='AssessmentSection',
                                          runtime=self._runtime)
        self._my_map = collection.find_one({'_id': self._my_map['_id']})

    def _update_questions(self):
        if self._update_part_map():
            self._update_question_map()
            self._save()

    def _update_part_map(self, part_id=None):
        def get_part_level(target_part_id):
            for p in self._my_map['assessmentParts']:
                if p['assessmentPartId'] == str(target_part_id):
                    return p['level']
            return 0

        def insert_part_map():
            part_index = self._my_map['assessmentParts'].index(str(prev_part_id)) + 1
            absolute_level = prev_part_level + delta
            self._my_map['assessmentParts'].insert(part_index, get_default_part_map(part_id, absolute_level))
            return True

        if part_id is None:
            part_id = self._assessment_part_id
        if part_id == self._assessment_part_id and self._is_simple_section():
            return
        finished = False
        updated = False
        prev_part_id = None
        while not finished:
            prev_part_level = get_part_level(prev_part_id)
            prev_part_id = part_id
            try:
                part_id, delta = get_next_part_id(part_id, runtime=self._runtime, proxy=self._proxy)
            except errors.IllegalState:
                finished = True
            else:
                if self._get_assessment_part(part_id).has_items():
                    if str(part_id) not in self._my_map['assessmentParts']:
                        updated = insert_part_map()
        return updated

    def _update_question_map(self):
        index = 0
        for part_map in self._my_map['assessmentParts']:

            if (len(self._my_map['questions']) == index or 
                    self._my_map['questions'][index]['assessmentPartId'] != part_map['assessmentPartId']):
                part_id = part_map['assessmentPartId']
                for item in self._get_assessment_part_lookup_session().get_part(part_id).get_items():
                    self._my_map['questions'].insert(index, get_default_question_map(
                        item.get_id(), item.get_question().get_id(), Id(part_id), []))
                    index += 1
                    
            else: # skip through all remaining questions for this part
                while (len(self._my_map['questions']) > index and
                       self._my_map['questions'][index]['assessmentPartId'] == part_map['assessmentPartId']):
                    index += 1
            
    def _get_assessment_part_lookup_session(self):
        # This appears to share code with _get_item_lookup_session
        # First do something special to get a magic session, if available.
        try:
            config = self._runtime.get_configuration()
            parameter_id = Id('parameter:magicAssessmentPartLookupSessions@mongo')
            import_path_with_class = config.get_value_by_parameter(parameter_id).get_string_value()
            module_path = '.'.join(import_path_with_class.split('.')[0:-1])
            magic_class = import_path_with_class.split('.')[-1]
            module = importlib.import_module(module_path)
            session = getattr(module, magic_class)(self.get_id(),
                                                   catalog_id=Id(self._assessment_taken._my_map['assignedBankIds'][0]),
                                                   runtime=self._runtime,
                                                   proxy=self._proxy)
        except (AttributeError, KeyError, errors.NotFound):
            mgr = self._get_provider_manager('ASSESSMENT_AUTHORING', local=True)
            session = mgr.get_assessment_part_lookup_session(proxy=self._proxy)
        session.use_federated_bank_view()
        return session

    def _get_item_lookup_session(self):
        # This appears to share code with _get_assessment_part_lookup_session
        # First do something special to get a magic session, if available.
        try:
            config = self._runtime.get_configuration()
            parameter_id = Id('parameter:magicItemLookupSessions@mongo')
            import_path_with_class = config.get_value_by_parameter(parameter_id).get_string_value()
            module_path = '.'.join(import_path_with_class.split('.')[0:-1])
            magic_class = import_path_with_class.split('.')[-1]
            module = importlib.import_module(module_path)
            session = getattr(module, magic_class)(catalog_id=Id(self._assessment_taken._my_map['assignedBankIds'][0]),
                                                   runtime=self._runtime,
                                                   proxy=self._proxy)
        except (AttributeError, KeyError, errors.NotFound):
            mgr = self._get_provider_manager('ASSESSMENT', local=True)
            session = mgr.get_item_lookup_session(catalog_id=Id(self._assessment_taken._my_map['assignedBankIds'][0]),
                                                  proxy=self._proxy)
        session.use_federated_bank_view()
        return session

    def _get_questions(self, answered=None):
        def update_question_list():
            \"\"\"Supportive function to aid readability of _get_questions.\"\"\"
            question_id = Id(question_map['questionId'])
            question_answered = bool(question_map['responses'][0])
            if answered is None or answered == question_answered:
                question_list.append(self._get_question(question_id))
            return question_answered

        prev_question_answered = True
        question_list = []
        # self._update() # Make sure we are current with database. Do we need this?
        for question_map in self._my_map['questions']:
            if self.are_items_sequential():
                if prev_question_answered:
                    prev_question_answered = update_question_list()
            else:
                update_question_list()
        return QuestionList(question_list, runtime=self._runtime, proxy=self._proxy)

    def _get_question(self, question_id):
        # This is where we might inject a new display_name
        item = self._get_item_lookup_session().get_item(question_id)
        question = item.get_question()
        try:
            matching_questions = [q['displayElements']
                                  for q in self._my_map['questions']
                                  if q['questionId'] == str(question_id)]
            if len(matching_questions) > 0:
                new_display_name = matching_questions[0]
                new_display_name = [str(e) for e in new_display_name]
                question.set_display_label('.'.join(new_display_name))

        except AttributeError:
            pass

        # only return the question if the item is part of this section ... not just "in this bank"
        section_question_ids = [q['questionId'] for q in self._my_map['questions']]
        if str(question_id) in section_question_ids:
            return question
        else:
            raise errors.NotFound

    def _get_answers(self, question_id):
        # What if we want the wrong answers, too?
        # collection = MongoClientValidated('assessment',
        #                                   collection='Item',
        #                                   runtime=self._runtime)
        # item_map = collection.find_one({'_id': ObjectId(item_id.get_identifier())})
        # return objects.AnswerList(item_map['answers'], runtime=self._runtime, proxy=self._proxy)
        item = self._get_item_lookup_session().get_item(question_id)
        answers = list(item.get_answers())
        try:
            answers += list(item.get_wrong_answers())
        except AttributeError:
            pass
        return answers

    def _get_first_question(self):
        question_id = Id(self._my_map['questions'][0]['questionId'])
        # This is where we might inject a new display_name
        return self._item_lookup_session.get_item(question_id).get_question()

    def _get_next_question(self, question_id, answered=None):
        \"\"\"Inspects question map to return the next available question.\"\"\"
        # self._update() # Make sure we are current with database. Do we need this?
        self._update_questions() # Make sure questions list is current
        if self._my_map['questions'][-1]['questionId'] == str(question_id):
            raise errors.IllegalState('No more Questions currently available for this Section')
        current_index = None
        for index, question_map in enumerate(self._my_map['questions']):
            if question_map['questionId'] == str(question_id):
                question_answered = bool(question_map['responses'][0])
                if answered is None or question_answered == answered:
                    current_index = index
                    break
        if current_index is not None:
            return self._get_question(Id(self._my_map['questions'][current_index + 1]['questionId']))
        ### SHOULD THIS RAISE NotFound?
        raise errors.IllegalState('No more Questions currently available for this Section')

    ### THIS IS STILL NOT RIGHT.  LOOK AT previous_question_map.  what if unanswered?
    def _get_previous_question(self, question_id, answered=None):
        \"\"\"Inspects question map to return previous next question.\"\"\"
        # self._update() # Make sure we are current with database. Do we need this?
        self._update_questions() # Make sure questions list is current
        if self._my_map['questions'][0]['questionId'] == str(question_id):
            raise errors.IllegalState('No previous Questions available for this Section')
        current_index = None
        for index, question_map in enumerate(self._my_map['questions']):
            if question_map['questionId'] == str(question_id):
                current_index = index
                break
        if current_index is not None:
            return self._get_question(Id(self._my_map['questions'][current_index - 1]['questionId']))
        ### SHOULD THIS RAISE NotFound?
        raise errors.IllegalState('No more Questions currently available for this Section')

    def _submit_response(self, item_id, answer_form=None):
        \"\"\"Updates assessmentParts map to insert an item response.
        
        answer_form is None indicates that the current response is to be cleared
        
        \"\"\"
        if answer_form is None:
            response = {}
        else:
            response = dict(answer_form._my_map)
            response['submissionTime'] = DateTime.utcnow()
        for question_map in self._my_map['questions']:
            if question_map['questionId'] == str(item_id):
                if question_map['responses'][0] is None: # No existing attempts
                    question_map['responses'] = []
                question_map['responses'].insert(0, response)
                self._save()
                return
        raise errors.NotFound('item_id not found in this AssessmentSection')

    def _get_response(self, question_id):
        \"\"\"Gets the latest response\"\"\"
        for question_map in self._my_map['questions']:
            if question_map['questionId'] == str(question_id):
                if (len(question_map['responses']) > 0 and
                        question_map['responses'][0] is not None):
                    return Response(Answer(
                        osid_object_map=question_map['responses'][0],
                        runtime=self._runtime,
                        proxy=self._proxy))
                else:
                    raise errors.IllegalState('No response is currently available for question_id')
        raise errors.NotFound()

    def _get_responses(self):
        answer_list = []
        for question_map in self._my_map['questions']:
            if (len(question_map['responses']) > 0 and
                    question_map['responses'][0] is not None):
                answer_list.append(Answer(
                        osid_object_map=question_map['responses'][0],
                        runtime=self._runtime,
                        proxy=self._proxy))
        return ResponseList(answer_list,
                            runtime=self._runtime,
                            proxy=self._proxy)

    def _is_question_answered(self, item_id):
        for question_map in self._my_map['questions']:
            if question_map['questionId'] == item_id:
                if question_map['responses'][0]:
                    return True
                else:
                    return False
        raise errors.NotFound()

    def _get_question_map(self, item_id):
        return (map for map in self._my_map['questions'] if map['questionId'] == str(item_id))

    def _is_feedback_available(self, item_id):
        item = self._item_lookup_session.get_item(item_id)
        response = self._get_question_map(item_id)['responses'][0]
        if response:
            return item.is_feedback_available_for_response(response)
        return item.is_feedback_available()

    def _get_feedback(self, item_id):
        item = self._item_lookup_session.get_item(item_id)
        response = self._get_question_map(item_id)['responses'][0]
        if response:
            try:
                return item.get_feedback_for_response(
                    Response(Answer(response, runtime=self._runtime, proxy=self._proxy)))
            except errors.IllegalState:
                pass
        else:
            return item.get_feedback() # raises IllegalState

    def _get_confused_learning_objective_ids(self, item_id):
        item = self._item_lookup_session.get_item(item_id)
        response = self._get_question_map(item_id)['responses'][0]
        if response:
            return item.get_confused_learning_objective_ids_for_response(
                Response(Answer(response, runtime=self._runtime, proxy=self._proxy)))
        raise errors.IllegalState()

    def _is_correctness_available(self, item_id):
        item = self._item_lookup_session.get_item(item_id)
        response = self._get_question_map(item_id)['responses'][0]
        if response:
            return item.is_correctness_available_for_response(
                Response(Answer(response, runtime=self._runtime, proxy=self._proxy)))
        return False

    def _is_correct(self, item_id):
        item = self._item_lookup_session.get_item(item_id)
        response = self._get_question_map(item_id)['responses'][0]
        if response:
            return item.is_response_correct(
                Response(Answer(response, runtime=self._runtime, proxy=self._proxy)))
        raise errors.IllegalState()

    def _get_correctness(self, item_id):
        item = self._item_lookup_session.get_item(item_id)
        response = self._get_question_map(item_id)['responses'][0]
        if response:
            return item.get_correctness_for_response(
                Response(Answer(response, runtime=self._runtime, proxy=self._proxy)))
        raise errors.IllegalState()

    def _finish(self):
        self._my_map['over'] = True # finished == over?
        self._my_map['completionTime'] = DateTime.utcnow()
        self._save()

    def _is_over(self):
        if 'over' in self._my_map and self._my_map['over']:
            return True
        return False
        
    def _is_complete(self):
        \"\"\"Check all Questions for completeness
        
        For now, completeness simply means that all questions have been 
        responded to and not skipped or cleared.
        
        \"\"\"
        # self._update() # Make sure we are current with database
        self._update_questions() # Make sure questions list is current
        for question_map in self._my_map['questions']:
            if not question_map['responses'][0]:
                return False
        return True"""


class Response:
    
    import_statements = [
        'from ..primitives import Id',
        'from dlkit.abstract_osid.osid import errors',
        'from ..utilities import get_registry',
    ]
    
    init = """
    _record_type_data_sets = {}
    _namespace = 'assessment.Response'
    
    def __init__(self, answer, **kwargs):
        self._my_answer = answer
        self._records = dict()
        # Consider that responses may want to have their own records separate
        # from the enclosed Answer records:
        self._record_type_data_sets = get_registry('RESPONSE_RECORD_TYPES', answer._runtime)
        response_map = answer.object_map
        self._load_records(response_map['recordTypeIds'])

    def _load_records(self, record_type_idstrs):
        for record_type_idstr in record_type_idstrs:
            self._init_record(record_type_idstr)

    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith('__'):
                yield attr
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __getattr__(self, name):
        if not name.startswith('__'):
            try:
                return getattr(self._my_answer, name)
            except:
                raise"""
    
    get_item_id = """
        return Id(self._my_answer._my_map['itemId'])"""
    
    get_item = """
        # So, why would we ever let an AssessmentSession user get the Item???
        raise errors.PermissionDenied()"""
    
    get_response_record = """
        if not self.has_record_type(item_record_type):
            raise errors.Unsupported()
        if str(item_record_type) not in self._records:
            raise errors.Unimplemented()
        return self._records[str(item_record_type)]"""

class ItemQuery:

    match_learning_objective_id = """
        self._add_match('learningObjectiveIds', str(objective_id), bool(match))"""

    clear_learning_objective_id_terms = """
        self._clear_terms('learningObjectiveIds')"""

    match_any_learning_objective = """
        match_key = 'learningObjectiveIds'
        param = '$exists'
        if match:
            flag = 'true'
        else:
            flag = 'false'
        if match_key in self._query_terms:
            self._query_terms[match_key][param] = flag
        else:
            self._query_terms[match_key] = {param: flag}
        self._query_terms[match_key]['$nin'] = [[], ['']]"""

    clear_learning_objective_terms = """
        self._clear_terms('learningObjectiveIds')"""

class ItemSearch:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from dlkit.mongo.osid import searches as osid_searches',
		'from ..utilities import get_registry',
    ]

    init = """
    def __init__(self, runtime):
        self._namespace = 'assessment.Item'
        self._runtime = runtime
        record_type_data_sets = get_registry('ITEM_RECORD_TYPES', runtime)
        self._record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_ids = []
        self._id_list = None
        for data_set in record_type_data_sets:
            self._all_supported_record_type_ids.append(str(Id(**record_type_data_sets[data_set])))
        osid_searches.OsidSearch.__init__(self, runtime)"""
    search_among_items = """
        self._id_list = item_ids"""

class ItemSearchResults:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from . import objects',
    ]

    init = """
    def __init__(self, results, runtime):
        # if you don't iterate, then .count() on the cursor is an inaccurate representation of limit / skip
        self._results = results
        self._runtime = runtime
        self.retrieved = False"""

    get_items = """
        if self.retrieved:
            raise errors.IllegalState('List has already been retrieved.')
        self.retrieved = True
        return objects.ItemList(self._results, runtime=self._runtime)"""


class ItemSearchSession:

    import_statements = [
        'from . import searches',
    ]

class BankForm:
    get_bank_form_record = """
        # this should be templated from Resource, but
        # would have to update pattern mappers
        return self._get_record(bank_record_type)"""

class BankQuery:
    import_statements = [
        'from bson import ObjectId'
    ]

    match_ancestor_bank_id = """
        # matches when the bank_id param is an ancestor of
        # any bank
        bank_descendants = self._get_descendant_catalog_ids(bank_id)
        identifiers = [ObjectId(i.identifier) for i in bank_descendants]
        self._query_terms['_id'] = {'$in': identifiers}
        """

