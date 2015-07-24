
from .error_lists import session_errors

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
        'from ..primitives import DateTime',
        'from dlkit.abstract_osid.osid import errors',
        'from bson.objectid import ObjectId',
        'from . import objects',
        'from .rules import Response',
        'from ..osid.sessions import OsidSession',
        'from ..utilities import MongoClientValidated',
        'SUBMITTED = True',
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
        self._forms = dict()
"""
    
    can_take_assessments = """
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
    
    has_assessment_begun = """
        return self._get_assessment_taken(assessment_taken_id).has_started()"""
    
    is_assessment_over = """
        return self._get_assessment_taken(assessment_taken_id).has_ended()"""
    
    ## This method has been deprecated:
    finished_assessment = """
        collection = MongoClientValidated('assessment',
                                          collection='AssessmentTaken',
                                          runtime=self._runtime)
        assessment_taken = self._get_assessment_taken(assessment_taken_id)
        assessment_taken_map = assessment_taken._my_map
        if assessment_taken.has_started() and not assessment_taken.has_ended():
            assessment_taken_map['completionTime'] = DateTime.now()
            assessment_taken_map['ended'] = True
            collection.save(assessment_taken_map)
        else:
            raise errors.IllegalState()"""
    
    requires_synchronous_sections = """
        # NOTE: For now we are not really dealing with sections. Re-implement when we do.
        return False"""
    
    get_first_assessment_section = """
        assessment_taken = self._get_assessment_taken(assessment_taken_id)
        if not assessment_taken.has_started() or assessment_taken.has_ended():
            raise errors.IllegalState()
        if 'actualStartTime' not in assessment_taken._my_map:
            assessment_taken._my_map['actualStartTime'] = None
        assessment_taken_map = assessment_taken._my_map
        if 'actualStartTime' not in assessment_taken_map or assessment_taken_map['actualStartTime'] is None:
            # perhaps put everything here in a separate helper method
            collection = MongoClientValidated('assessment',
                                              collection='Assessment',
                                              runtime=self._runtime)
            assessment_id = assessment_taken.get_assessment_offered().get_assessment_id()
            assessment = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})
            if 'itemIds' not in assessment:
                item_ids = [] # But will this EVER be the case?
            else:
                item_ids = assessment['itemIds']
            assessment_taken_map['synchronousResponses'] = bool(
                assessment_taken.get_assessment_offered().are_items_sequential())
            assessment_taken_map['actualStartTime'] = DateTime.now()
            assessment_taken_map['itemIds'] = item_ids
            assessment_taken_map['responses'] = dict()
            for item_idstr in item_ids:
                assessment_taken_map['responses'][Id(item_idstr).get_identifier()] = None
            collection = MongoClientValidated('assessment',
                                              collection='AssessmentTaken',
                                              runtime=self._runtime)
            collection.save(assessment_taken_map)
        assessment_section_map = {
            '_id': ObjectId(assessment_taken_id.get_identifier()),
            'displayName': assessment_taken_map['displayName'],
            'description': assessment_taken_map['description'],
            'genusTypeId': assessment_taken_map['genusTypeId'],
            'recordTypeIds': [],
            'bankId': str(self.get_bank_id()),
            'assessmentTakenId': str(assessment_taken_id)
        }
        return objects.AssessmentSection(assessment_section_map, db_prefix=self._db_prefix, runtime=self._runtime)"""
    
    has_next_assessment_section = """
        # For now we are only working only with 'sectionless' assessments
        if not self.has_assessment_begun(assessment_section_id):
            raise errors.IllegalState()
        return False"""
    
    get_next_assessment_section = """
        # For now we are only working only with 'sectionless' assessments
        if not self.has_assessment_begun(assessment_section_id):
            raise errors.IllegalState()
        raise errors.IllegalState()"""
    
    has_previous_assessment_section = """
        # For now we are only working only with 'sectionless' assessments
        if not self.has_assessment_begun(assessment_section_id):
            raise errors.IllegalState()
        return False"""
    
    get_previous_assessment_section = """
        # For now we are only working only with 'sectionless' assessments
        if not self.has_assessment_begun(assessment_section_id):
            raise errors.IllegalState()
        raise errors.IllegalState()"""
    
    get_assessment_section = """
        # currently implemented to take advantage of the 1 to 1 relationship
        # between AssessmentSection and AssessmentTaken
        if not self.has_assessment_begun(assessment_section_id):
            raise errors.IllegalState()
        assessment_taken = self._get_assessment_taken(assessment_section_id)
        assessment_taken_map = assessment_taken._my_map
        assessment_section_map = {
            '_id': assessment_taken_map['_id'],
            'displayName': assessment_taken_map['displayName'],
            'description': assessment_taken_map['description'],
            'genusTypeId': assessment_taken_map['genusTypeId'],
            'recordTypeIds': [],
            'bankId': str(self.get_bank_id()),
            'assessmentTakenId': str(assessment_taken.get_id())
        }
        return objects.AssessmentSection(assessment_section_map, db_prefix=self._db_prefix, runtime=self._runtime)"""
    
    get_assessment_sections = """
        # This currently assumes that there is only one section:
        return objects.AssessmentSectionList(
            [self.get_first_assessment_section(assessment_taken_id)],
            db_prefix=self._db_prefix,
            runtime=self._runtime)

    def _get_assessment_taken(self, assessment_taken_id):
        \"\"\"Helper method for getting an AssessmentTaken objects given an Id.\"\"\"
        mgr = self._get_provider_manager('ASSESSMENT')
        lookup_session = mgr.get_assessment_taken_lookup_session()
        lookup_session.use_federated_bank_view()
        return_object = lookup_session.get_assessment_taken(assessment_taken_id)
        return return_object"""
    
    is_assessment_section_complete = """
        return self.get_assessment_section(assessment_section_id).get_assessment_taken().has_ended()"""
    
    get_incomplete_assessment_sections = """
        assessment_taken = self._get_assessment_taken(assessment_taken_id)
        # Is this right?  How do we define complete?
        if assessment_taken.has_ended():
            return objects.AssessmentSectionList([], db_prefix=self._db_prefix, runtime=self._runtime)
        else:
            return objects.AssessmentSectionList(
                [self.get_assessment_section(assessment_taken_id)],
                db_prefix=self._db_prefix,
                runtime=self._runtime)"""
    
    has_assessment_section_begun = """
        return self._get_assessment_taken(assessment_section_id).has_started()"""
    
    is_assessment_section_over = """
        return self._get_assessment_taken(assessment_section_id).has_ended()"""
    
    ## This method has been deprecated:
    finished_assessment_section = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        self.finished_assessment(assessment_section_id)"""
    
    requires_synchronous_responses = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        return self.get_assessment_section(
            assessment_section_id).get_assessment_taken()._my_map['synchronousResponses']"""
    
    get_first_question = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        ## What if there are no items???
        item_id_str = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds'][0]
        return self._get_question(item_id_str)"""
    
    has_next_question = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        try:
            if len(item_ids) > item_ids.index(str(item_id)) + 1:
                return True
        except ValueError:
            raise errors.NotFound('item id not in assessment')"""
    
    get_next_question = """
        if not self.has_next_question(assessment_section_id, item_id):
            raise errors.IllegalState()
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        return self._get_question(item_ids[item_ids.index(str(item_id)) + 1])"""
    
    has_previous_question = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        try:
            if item_ids.index(str(item_id)) > 0:
                return True
        except ValueError:
            raise errors.NotFound('item id not in assessment')"""
    
    get_previous_question = """
        if not self.has_previous_question():
            raise errors.IllegalState()
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        return self._get_question(item_ids[item_ids.index(str(item_id)) - 1])"""
    
    get_question = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        if str(item_id) not in item_ids:
            raise errors.NotFound()
        return self._get_question(str(item_id))

    def _get_question(self, item_idstr):
        \"\"\"Helper method for getting a Question object given an Id.\"\"\"
        item_id = Id(item_idstr)
        collection = MongoClientValidated('assessment',
                                          collection='Item',
                                          runtime=self._runtime)
        item_map = collection.find_one({'_id': ObjectId(item_id.get_identifier())})
        return objects.Question(item_map['question'], db_prefix=self._db_prefix, runtime=self._runtime)"""
    
    get_questions = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        if self.requires_synchronous_responses(assessment_section_id):
            raise errors.IllegalState() # This may need to actually be implemented
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        questions = []
        for item_idstr in item_ids:
            questions.append(self._get_question(item_idstr))
        return objects.QuestionList(questions, db_prefix=self._db_prefix, runtime=self._runtime)"""

    get_response_form_import_templates = [
        'from ...abstract_osid.id.primitives import Id as ABCId'
    ]

    get_response_form = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        if not isinstance(item_id, ABCId):
            raise errors.InvalidArgument('argument is not a valid OSID Id')
        ##
        # This is a little hack to get the answer record types from the Item's
        # Question record types. Should really get it from item genus types somehow:
        try:
            from ..records.types import ANSWER_RECORD_TYPES as record_type_data_sets
        except (ImportError, AttributeError):
            record_type_data_sets = dict()
        collection = MongoClientValidated('assessment',
                                          collection='Item',
                                          runtime=self._runtime)
        item_map = collection.find_one({'_id': ObjectId(item_id.get_identifier())})
        answer_record_types = []
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
            db_prefix=self._db_prefix,
            runtime=self._runtime)
        obj_form._for_update = False # This may be redundant
        self._forms[obj_form.get_id().get_identifier()] = not SUBMITTED
        return obj_form"""

    submit_response_import_templates = [
        'from ...abstract_osid.assessment.objects import AnswerForm as ABCAnswerForm'
    ]

    submit_response = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        if not isinstance(answer_form, ABCAnswerForm):
            raise errors.InvalidArgument('argument type is not an AnswerForm')
        ##
        # OK, so the following should actually NEVER be true:
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
        assessment_taken_map = self._get_assessment_taken(assessment_section_id)._my_map
        if Id(answer_form._my_map['itemId']).get_identifier() in assessment_taken_map['responses']:
            assessment_taken_map['responses'][Id(answer_form._my_map['itemId']).get_identifier()] = answer_form._my_map
        else:
            raise errors.NotFound()
        try:
            collection = MongoClientValidated('assessment',
                                              'AssessmentTaken',
                                              runtime=self._runtime)
            collection.save(assessment_taken_map)
        except: # what exceptions does mongodb insert raise?
            raise errors.OperationFailed()
        self._forms[answer_form.get_id().get_identifier()] = SUBMITTED"""
    
    skip_item = """
        #if (not self.has_assessment_section_begun(assessment_section_id) or
        #    self.is_assessment_section_over(assessment_section_id)):
        #    raise errors.IllegalState()
        #item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        raise errors.Unimplemented()"""
    
    is_question_answered = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        if item_id.get_identifier() in responses:
            return bool(responses[item_id.get_identifier()])
        else:
            raise errors.NotFound()"""
    
    get_unanswered_questions = """
        # Note: this implementation returns them in order
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        question_list = []
        for item_idstr in item_ids:
            if responses[Id(item_idstr).get_identifier()] is None:
                question_list.append(self._get_question(item_idstr))
        return objects.QuestionList(question_list, db_prefix=self._db_prefix, runtime=self._runtime)"""
    
    has_unanswered_questions = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        for item_idstr in responses:
            if responses[Id(item_idstr).get_identifier()] is None:
                return True
        return False"""
    
    get_first_unanswered_question = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        if not self.has_unanswered_questions(assessment_section_id):
            raise errors.IllegalState('No more unanswered questions')
        unanswered_questions = self.get_unanswered_questions(assessment_section_id)
        return unanswered_questions.get_next_question()"""
    
    has_next_unanswered_question = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        try:
            item_index = item_ids.index(str(item_id))
        except ValueError:
            raise errors.NotFound()
        # could use itertools.islice here?  Don't know if these will ever be large lists
        for item_idstr in item_ids[item_index:]:
            if responses[Id(item_idstr).get_identifier()] is None:
                return True
        return False"""
    
    get_next_unanswered_question = """
        # This seems to share a lot of code with has_next_unanswered_question.  Just sayin'.
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        try:
            item_index = item_ids.index(str(item_id))
        except ValueError:
            raise errors.NotFound()
        # could use itertools.islice here?  Don't know if these will ever be large lists
        for item_idstr in item_ids[item_index:]:
            if responses[Id(item_idstr).get_identifier()] is None:
                return self._get_question(item_idstr)
        raise errors.IllegalState()"""
    
    has_previous_unanswered_question = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        try:
            item_index = item_ids.index(str(item_id))
        except ValueError:
            raise errors.NotFound()
        # could use itertools.islice here?  Don't know if these will ever be large lists
        for item_idstr in item_ids[:item_index].reverse():
            if responses[Id(item_idstr).get_identifier()] is None:
                return True
        return False"""
    
    get_previous_unanswered_question = """
        # This seems to share a lot of code with has_next_unanswered_question.  Just sayin'.
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        try:
            item_index = item_ids.index(str(item_id))
        except ValueError:
            raise errors.NotFound()
        # could use itertools.islice here?  Don't know if these will ever be large lists
        for item_idstr in item_ids[:item_index].reverse():
            if responses[Id(item_idstr).get_identifier()] is None:
                return self._get_question(item_idstr)
        raise errors.IllegalState()"""
    
    get_response = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        if item_id.get_identifier() in responses and responses[item_id.get_identifier()] is not None:
            return Response(objects.Answer(
                responses[item_id.get_identifier()],
                db_prefix=self._db_prefix,
                runtime=self._runtime))
        else:
            raise errors.NotFound()"""
    
    get_responses = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        answer_list = []
        for item_idstr in responses:
            if responses[item_idstr] is not None:
                answer_list.append(objects.Answer(
                    responses[Id(item_idstr).get_identifier()],
                    db_prefix=self._db_prefix,
                    runtime=self._runtime))
        return objects.ResponseList(answer_list)"""
    
    clear_response = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        assessment_taken = self.get_assessment_section(assessment_section_id).get_assessment_taken()
        if item_id.get_identifier() in assessment_taken._my_map['responses']:
            assessment_taken._my_map['responses'][item_id.get_identifier()] = None
            collection = MongoClientValidated('assessment',
                                              collection='AssessmentTaken',
                                              runtime=self._runtime)
            collection.save(assessment_taken._my_map)
        else:
            raise errors.NotFound()"""
    
    finish_assessment_section = """
        if (not self.has_assessment_section_begun(assessment_section_id) or
                self.is_assessment_section_over(assessment_section_id)):
            raise errors.IllegalState()
        self.finish_assessment(assessment_section_id)"""
    
    ## This is no longer needed:
    finish = """
        self.finished_assessment(assessment_section_id)
    
    def finish_assessment_section(self, assessment_section_id):
        self.finish(assessment_section_id)"""
    
    finish_assessment = """
        assessment_taken = self._get_assessment_taken(assessment_taken_id)
        assessment_taken_map = assessment_taken._my_map
        if assessment_taken.has_started() and not assessment_taken.has_ended():
            assessment_taken_map['completionTime'] = DateTime.now()
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
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        if item_id.get_identifier() in responses:
            if responses[item_id.get_identifier()] is None:
                return False
            else:
                return True
        else:
            raise errors.NotFound()"""
    
    get_answers = """
        if self.is_answer_available(assessment_section_id, item_id):
            collection = MongoClientValidated('assessment',
                                              collection='Item',
                                              runtime=self._runtime)
            item_map = collection.find_one({'_id': ObjectId(item_id.get_identifier())})
            return objects.AnswerList(item_map['answers'], db_prefix=self._db_prefix, runtime=self._runtime)
        else:
            raise errors.IllegalState()"""


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
        collection = MongoClientValidated('assessment',
                                          collection='Assessment',
                                          runtime=self._runtime)
        # This needs to be updated to actually check for AssessmentsTaken (and does that find even work?)
        if collection.find({'itemIds': str(item_id)}).count() != 0:
            raise errors.IllegalState('this Item is being used in one or more Assessments')
        collection = MongoClientValidated('assessment',
                                          collection='Item',
                                          runtime=self._runtime)
        item_map = collection.find_one({'_id': ObjectId(item_id.get_identifier())})
        objects.Item(item_map, db_prefix=self._db_prefix, runtime=self._runtime)._delete()
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
                                             {'bankId': str(self._catalog_id)}]})
        # set the name in the question, so it can be shown to students
        question_form._my_map['displayName']['text'] = item['displayName']['text']
        question_form._my_map['description']['text'] = item['description']['text']
        if item['question'] is None:
            item['question'] = question_form._my_map
        else:
            item['question'] = question_form._my_map # Let's just assume we can overwrite it
            #raise errors.AlreadyExists()
        collection.save(item)
        self._forms[question_form.get_id().get_identifier()] = CREATED
        return objects.Question(question_form._my_map, db_prefix=self._db_prefix, runtime=self._runtime)"""

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
        obj_form = objects.QuestionForm(document['question'], self._db_prefix, runtime=self._runtime)
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
        item = collection.find_one({'$and': [{'_id': ObjectId(item_id)}, {'bankId': str(self._catalog_id)}]})
        item['question'] = question_form._my_map
        try:
            collection.save(item)
        except: # what exceptions does mongodb save raise?
            raise errors.OperationFailed()
        self._forms[question_form.get_id().get_identifier()] = UPDATED
        # Note: this is out of spec. The OSIDs don't require an object to be returned:
        return objects.Question(question_form._my_map, db_prefix=self._db_prefix, runtime=self._runtime)"""


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
        'from ...abstract_osid.id.primitives import Id as ABCId'
    ]

    delete_assessment = """
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
        collection.delete_one({'_id': ObjectId(assessment_id.get_identifier())})"""

class AssessmentTakenLookupSession:
    
    import_statements = [
        'from ..primitives import Id',
        'from dlkit.abstract_osid.osid import errors',
        'from . import objects',
        'from ..utilities import MongoClientValidated'
    ]
    
    # This is hand built, but there may be a pattern to try to map, specifically
    # getting objects for another package object and a persisted id thingy
    get_assessments_taken_for_taker_and_assessment_offered = """
        # NOTE: This implementation currently ignores plenary view
        collection = MongoClientValidated('assessment',
                                          collection='AssessmentTaken',
                                          runtime=self._runtime)
        result = collection.find(
            dict({'assessmentOfferedId': str(assessment_offered_id),
                  'takingAgentId': str(resource_id)},
                  **self._bank_view_filter())).sort('_id', DESCENDING)
        return objects.AssessmentTakenList(result, db_prefix=self._db_prefix, runtime=self._runtime)"""

    get_assessments_taken_for_assessment = """
        collection = MongoClientValidated('assessment',
                                          collection='AssessmentOffered',
                                          runtime=self._runtime)
        result = collection.find(
            dict({'assessmentId': str(assessment_id)},
                 **self._bank_view_filter())).sort('_id', DESCENDING)
        assessments_offered = objects.AssessmentOfferedList(
            result,
            db_prefix=self._db_prefix,
            runtime=self._runtime)

        collection = MongoClientValidated('assessment',
                                          collection='AssessmentTaken',
                                          runtime=self._runtime)
        ao_ids = []
        for assessment_offered in assessments_offered:
            ao_ids.append(str(assessment_offered.get_id()))

        result = collection.find(
            dict({'assessmentOfferedId': {'$in':[ao_ids]}},
                 **self._bank_view_filter())).sort('_id', DESCENDING)
        return objects.AssessmentTakenList(result,
                                           db_prefix=self._db_prefix,
                                           runtime=self._runtime)"""


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
                db_prefix=self._db_prefix,
                runtime=self._runtime)
        else:
            obj_form = objects.AssessmentOfferedForm(
                bank_id=self._catalog_id,
                record_types=assessment_offered_record_types,
                assessment_id=assessment_id,
                catalog_id=self._catalog_id,
                default_display_name=assessment_map['displayName']['text'],
                db_prefix=self._db_prefix,
                runtime=self._runtime)
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
                num_takens = collection.find({'assessmentOfferedId': str(assessment_offered.get_id()),
                                              'takingAgentId': str(self.get_effective_agent_id()),
                                              'bankId': str(self._catalog_id)}).count()
                if num_takens >= max_attempts:
                    raise errors.PermissionDenied('exceeded max attempts')
        except AttributeError:
            pass
        assessment_taken_form._my_map['takingAgentId'] = str(self.get_effective_agent_id())

        insert_result = collection.insert_one(assessment_taken_form._my_map)
        self._forms[assessment_taken_form.get_id().get_identifier()] = CREATED
        return objects.AssessmentTaken(
            collection.find_one({'_id': insert_result.inserted_id}), db_prefix=self._db_prefix, runtime=self._runtime)"""

class AssessmentBasicAuthoringSession:
    
    import_statements = [
        'from bson.objectid import ObjectId',
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from . import objects',
        'from ..osid.sessions import OsidSession',
        'from ..utilities import MongoClientValidated'
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
        self._forms = dict()
"""
    
    can_author_assessments = """
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""
    
    get_items = """
        collection = MongoClientValidated('assessment',
                                          collection='Assessment',
                                          runtime=self._runtime)
        assessment = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})
        if 'itemIds' not in assessment or assessment['itemIds'] == []:
            return objects.ItemList([], db_prefix=self._db_prefix, runtime=self._runtime)

        collection = MongoClientValidated('assessment',
                                          collection='Item',
                                          runtime=self._runtime)
        item_list = []

        # This appears to assume that all the Items exist. Need to consider this further:
        for i in assessment['itemIds']:
            item_list.append(collection.find_one({'_id': ObjectId(Id(i).get_identifier())}))
        return objects.ItemList(item_list, db_prefix=self._db_prefix, runtime=self._runtime)"""
    
    add_item = """
        # make sure the item exists, first
        collection = MongoClientValidated('assessment',
                                          collection='Item',
                                          runtime=self._runtime)
        collection.find_one({'_id': ObjectId(item_id.get_identifier())})

        collection = MongoClientValidated('assessment',
                                          collection='Assessment',
                                          runtime=self._runtime)
        assessment = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})

        if 'itemIds' not in assessment:
            assessment['itemIds'] = [str(item_id)]
        else:
            assessment['itemIds'].append(str(item_id))
        collection.save(assessment)"""
    
    remove_item = """
        collection = MongoClientValidated('assessment',
                                          collection='Assessment',
                                          runtime=self._runtime)
        assessment = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})

        try:
            assessment['itemIds'].remove(str(item_id))
        except (KeyError, ValueError):
            raise errors.NotFound('item_id not found on assessment')
        collection.save(assessment)"""
    
    move_item = """
        collection = MongoClientValidated('assessment',
                                          collection='Assessment',
                                          runtime=self._runtime)
        assessment = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})

        try:
            p_index = assessment['itemIds'].index(str(preceeding_item_id))
        except (KeyError, ValueError):
            raise errors.NotFound('preceeding_item_id not associated with assessment')

        try:
            assessment['itemIds'].remove(str(item_id))
        except ValueError:
            raise errors.NotFound('item_id not associated with assessment')
        assessment['itemIds'].insert(str(item_id), p_index + 1)
        collection.save(assessment)"""
    
    order_items = """
        ## STILL NOT DONE???
        # Currently this implementation assumes that all item_ids are
        # included in the argument list. The case where a subset is provided
        # will be implemented later, but this covers the primary case
        # that we will see from a RESTful consumer.
        collection = MongoClientValidated('assessment',
                                          collection='Assessment',
                                          runtime=self._runtime)
        assessment = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})

        try:
            if len(assessment['itemIds']) != len(item_ids):
                raise errors.OperationFailed('number of items does not match those in assessment')
        except KeyError:
            raise errors.NotFound('no items were found for this assessment_id')
        item_id_list = []
        for i in item_ids:
            if str(i) not in assessment['itemIds']:
                raise errors.OperationFailed('one or more items are not associated with this assessment')
            item_id_list.append(str(i))
        assessment['itemIds'] = item_id_list
        collection.save(assessment)"""


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
"""

class Item:
    
    get_question_id = """
        self.get_question().get_id()"""
    
    get_question = """
        return Question(self._my_map['question'], db_prefix=self._db_prefix, runtime=self._runtime)"""
    
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
    
    def _delete(self):
        try:
            self.get_question()._delete()
        except:
            pass
        finally:
            for answer in self.get_answers():
                answer._delete()
            osid_objects.OsidObject._delete(self)"""

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
            return self.get_assessment().get_description()"""
    
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

class AssessmentOfferedForm:
    
    set_start_time_template = """
        # Implemented from template for osid.assessment.AssessmentOfferedForm.set_start_time_template
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_${arg0_type_under}(
                ${arg0_name},
                self.get_${var_name}_metadata()):
            raise errors.InvalidArgument()
        self._my_map['${var_name_mixed}'] = ${arg0_name}
"""
    
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
            return self.get_assessment_offered().get_description()"""
    
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
        # This needs to be updated to only reflect actual start time??
        if 'started' in self._my_map and self._my_map['started']:
            return True
        else:
            my_assessment_offered = self.get_assessment_offered()
            if my_assessment_offered.has_start_time():
                self._my_map['started'] = DateTime.now() >= my_assessment_offered.get_start_time()
                return self._my_map['started']
            else:
                self._my_map['started'] = True
                return True"""
    
    get_actual_start_time = """
        if not self.has_started():
            raise errors.IllegalState('this assessment has not yet started')
        if self._my_map['actualStartTime'] is None:
            raise errors.IllegalState('this assessment has not yet been started by the taker')
        else:
            return self._my_map['actualStartTime']"""
    
    has_ended = """
        # Perhaps this should just check for existance of self._my_map['completionTime']?
        return bool('ended' in self._my_map and self._my_map['ended'])"""
    
    get_completion_time = """
        if not self.has_ended():
            raise errors.IllegalState('this assessment has not yet ended')
        if not self._my_map['completionTime']:
            raise errors.OperationFailed('someone forgot to set the completion time')
        return self._my_map['completionTime']"""
    
    get_time_spent = """
        if self.has_started() and self.has_ended():
            return self.get_completion_time() - self.get_actual_start_time()
        else:
            raise errors.IllegalState()"""
    
    get_completion_template = """
        # Implemented from template for osid.assessment.AssessmentTaken.get_completion_template
        return int(self._my_map['${var_name_mixed}'])"""
    
    get_score_template = """
        # Implemented from template for osid.assessment.AssessmentTaken.get_score_template
        return float(self._my_map['${var_name_mixed}'])"""
    
    ### These methods are under consideration:
    additional_methods_under_consideration = """
    def _start_assessment(self)
        collection = MongoClientValidated('assessment',
                                          collection='Assessment',
                                          runtime=self._runtime)
        assessment_id = self.get_assessment_offered().get_assessment_id()
        assessment = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})
        if 'itemIds' not in assessment:
            item_ids = [] # But will this EVER be the case?
        else:
            item_ids = assessment['itemIds']

        collection = MongoClientValidated('assessment',
                                          collection='Items',
                                          runtime=self._runtime)
        item_identifier_list = []
        for item_id in item_ids:
            item_identifier_list.append(item_id.get_identifier())
        items = ItemList(collection.find({'_id': {'$$in': item_identifier_list}}))
        item_configs = dict()
        for item in items:
            try:
                item_configs['item.get_id().get_identifier()'] = item.get_configuration()
            except:
                item_configs['item.get_id().get_identifier()'] = dict()
        self._my_map['itemConfigs'] = item_parameters
        self._my_map['synchronousResponses'] = bool(assessment_taken.get_assessment_offered().are_items_sequential())
        self._my_map['actualStartTime'] = DateTime.now()
        # This is where we could check for randomization
        self._my_map['itemIds'] = item_ids
        self._my_map['responses'] = dict()
        for item_idstr in item_ids:
            self._my_map['responses'][Id(item_idstr).get_identifier()] = None
        collection = MongoClientValidated('assessment',
                                          collection='AssessmentTaken',
                                          runtime=self._runtime)
        collection.save(self._my_map)
    
    def _get_question(self, item_id):
        collection = MongoClientValidated('assessment',
                                          collection='Item',
                                          runtime=self._runtime)
        item_map = collection.find_one({'_id': ObjectId(item_id.get_identifier())})

        question = Item(item_map).get_question()
        if self._my_map['itemConfigs][str(item_id)]:
            question.config(self._my_map['itemConfigs][str(item_id)])
        return question"""


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
        self._add_match('takingAgentId', str(agent_id), bool(match))
    """


class AssessmentSection:
    
    has_allocated_time = """
        return self.get_assessment_taken().get_assessment_offered().has_duration()"""
    
    get_allocated_time = """
        return self.get_assessment_taken().get_assessment_offered().get_duration()"""
    
    are_items_sequential = """
        return self.get_assessment_taken().get_assessment_offered().are_items_sequential()"""
    
    are_items_shuffled = """
        return self.get_assessment_taken().get_assessment_offered().are_items_shuffled()"""

class Response:
    
    import_statements = [
        'from ..primitives import Id',
        'from dlkit.abstract_osid.osid import errors',
    ]
    
    init = """
    try:
        from ..records.types import RESPONSE_RECORD_TYPES as _record_type_data_sets
    except ImportError, AttributeError:
        _record_type_data_sets = dict()
    _namespace = 'assessment.Response'
    
    def __init__(self, answer, **kwargs):
        self._my_answer = answer
        self._records = dict()
        # Consider that responses may want to have their own records separate
        # from the enclosed Answer records:
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
                raise
"""
    
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
        self._add_match('learningObjectiveIds', str(objective_id), bool(match))
    """

    clear_learning_objective_id_terms = """
        self._clear_match('learningObjectiveIds')
    """
