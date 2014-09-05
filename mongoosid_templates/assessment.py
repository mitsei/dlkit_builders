
class AssessmentManager:

    get_assessment_taken_query_session_for_bank = """
        if not bank_id:
            raise NullArgument
        if not self.supports_assessment_taken_query():
            raise Unimplemented()
        try:
            from . import sessions
        except ImportError:
            raise OperationFailed()
        try:
            session = sessions.AssessmentTakenQuerySession(bank_id)
        except AttributeError:
            raise #OperationFailed()
        return session

    def get_assessment_taken_admin_session(self):
        try:
            from . import sessions
        except ImportError:
            raise OperationFailed()
        try:
            session = sessions.AssessmentTakenAdminSession()
        except AttributeError:
            raise #OperationFailed()
        return session

    def get_assessment_taken_admin_session_for_bank(self, bank_id):
        if not bank_id:
            raise NullArgument
        try:
            from . import sessions
        except ImportError:
            raise OperationFailed()
        try:
            session = sessions.AssessmentTakenAdminSession(bank_id)
        except AttributeError:
            raise #OperationFailed()
        return session"""

class AssessmentProxyManager:

    get_assessment_taken_query_session_for_bank = """
        if not bank_id or proxy is None:
            raise NullArgument
        if not self.supports_assessment_taken_query():
            raise Unimplemented()
        try:
            from . import sessions
        except ImportError:
            raise OperationFailed()
        try:
            session = sessions.AssessmentTakenQuerySession(bank_id, proxy)
        except AttributeError:
            raise #OperationFailed()
        return session

    def get_assessment_taken_admin_session(self, proxy):
        if proxy is None:
            raise NullArgument
        try:
            from . import sessions
        except ImportError:
            raise OperationFailed()
        try:
            session = sessions.AssessmentTakenAdminSession(proxy)
        except AttributeError:
            raise #OperationFailed()
        return session

    def get_assessment_taken_admin_session_for_bank(self, bank_id, proxy):
        if not bank_id or proxy is None:
            raise NullArgument
        try:
            from . import sessions
        except ImportError:
            raise OperationFailed()
        try:
            session = sessions.AssessmentTakenAdminSession(bank_id, proxy)
        except AttributeError:
            raise #OperationFailed()
        return session"""


class AssessmentSession:

    import_statements = [
        'from bson.objectid import ObjectId',
        'from pymongo import MongoClient',
        'from ..primitives import *',
        'from ..osid.osid_errors import *'
        ]

    init = """
    def __init__(self, catalog_id = None, proxy = None):
        from .objects import Bank
        from ..osid.sessions import OsidSession
        self._catalog_class = Bank
        self._session_name = 'AssessmentSession'
        self._catalog_name = 'Bank'
        OsidSession._init_object(self, catalog_id, proxy, db_name='assessment', cat_name='Bank', cat_class=Bank)
        self._forms = dict()
"""

    old_init ="""
    def __init__(self, catalog_id = None, *args, **kwargs):
        from .objects import Bank
        from ..osid.sessions import OsidSession
        from . import profile
        OsidSession.__init__(self, *args, **kwargs)
        from pymongo import MongoClient
        collection = MongoClient()['assessment']['Bank']
        if catalog_id is not None and catalog_id.get_identifier() != '000000000000000000000000':
            self._catalog_identifier = catalog_id.get_identifier()
            self._my_catalog_map = collection.find_one({'_id': ObjectId(self._catalog_identifier)})
            if self._my_catalog_map is None:
                raise NotFound('could not find catalog identifier ' + catalog_id.get_identifier())
        else:
            from ..primitives import Id, Type
            from .. import types
            self._catalog_identifier = '000000000000000000000000'
            self._my_catalog_map = {
                '_id': ObjectId(self._catalog_identifier),
                'displayName': {'text': 'Default Bank',
                                'languageType': str(Type(**types.Language().get_type_data('DEFAULT'))),
                                'scriptType': str(Type(**types.Script().get_type_data('DEFAULT'))),
                                'formatType': str(Type(**types.Format().get_type_data('DEFAULT'))),},
                'description': {'text': 'The Default Bank',
                                'languageType': str(Type(**types.Language().get_type_data('DEFAULT'))),
                                'scriptType': str(Type(**types.Script().get_type_data('DEFAULT'))),
                                'formatType': str(Type(**types.Format().get_type_data('DEFAULT'))),},
                'genusType': str(Type(**types.Genus().get_type_data('DEFAULT')))
            }
        self._catalog = Bank(self._my_catalog_map)
        self._catalog_id = self._catalog.get_id()
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

    finished_assessment = """
        collection = MongoClient()['assessment']['AssessmentTaken']
        assessment_taken = self._get_assessment_taken(assessment_taken_id)
        assessment_taken_map = assessment_taken._my_map
        if assessment_taken.has_started() and not assessment_taken.has_ended():
            assessment_taken_map['completionTime'] = DateTime.now()
            assessment_taken_map['ended'] = True
            collection.save(assessment_taken_map)
        else:
            raise IllegalState()"""

    requires_synchronous_sections = """
        # NOTE: For now we are not really dealing with sections. Re-implement when we do.
        return False"""

    get_first_assessment_section = """
        from .objects import AssessmentSection
        if assessment_taken_id is None:
            raise NullArgument()
        assessment_taken = self._get_assessment_taken(assessment_taken_id)
        if not assessment_taken.has_started() or assessment_taken.has_ended():
            raise IllegalState()
        assessment_taken_map = assessment_taken._my_map
        if assessment_taken_map['actualStartTime'] is None:
            collection = MongoClient()['assessment']['Assessment_Items']
            assessment_id = assessment_taken.get_assessment_offered().get_assessment_id()
            assessment_items = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})
            if assessment_items is None:
                item_ids = [] # But will this EVER be the case?
            else:
                item_ids = assessment_items['itemIds']
            assessment_taken_map['synchronousResponses'] = bool(assessment_taken.get_assessment_offered().are_items_sequential())
            assessment_taken_map['actualStartTime'] = DateTime.now()
            assessment_taken_map['itemIds'] = item_ids
            assessment_taken_map['responses'] = dict()
            for item_idstr in item_ids:
                assessment_taken_map['responses'][Id(item_idstr).get_identifier()] = None
            collection = MongoClient()['assessment']['AssessmentTaken']
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
        return AssessmentSection(assessment_section_map)"""

    has_next_assessment_section = """
        # For now we are only working only with 'sectionless' assessments
        if not self.has_assessment_begun(assessment_section_id):
            raise IllegalState()
        return False"""

    get_next_assessment_section = """
        # For now we are only working only with 'sectionless' assessments
        if not self.has_assessment_begun(assessment_section_id):
            raise IllegalState()
        raise IllegalState()"""

    has_previous_assessment_section = """
        # For now we are only working only with 'sectionless' assessments
        if not self.has_assessment_begun(assessment_section_id):
            raise IllegalState()
        return False"""

    get_previous_assessment_section = """
        # For now we are only working only with 'sectionless' assessments
        if not self.has_assessment_begun(assessment_section_id):
            raise IllegalState()
        raise IllegalState()"""

    get_assessment_section = """
        # currently implemented to take advantage of the 1 to 1 relationship 
        # between AssessmentSection and AssessmentTaken
        from .objects import AssessmentSection
        if not self.has_assessment_begun(assessment_section_id):
            raise IllegalState()
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
        return AssessmentSection(assessment_section_map)"""

    get_assessment_sections = """
        # This currently assumes that there is only one section:
        from .objects import AssessmentSectionList
        return AssessmentSectionList([self.get_first_assessment_section(assessment_taken_id)])

    def _get_assessment_taken(self, assessment_taken_id):
        ##
        # This is a little helper method for getting AssessmentTaken objects given an Id
        from . import managers
        mgr = managers.AssessmentManager()
        lookup_session = mgr.get_assessment_taken_lookup_session()
        lookup_session.use_federated_bank_view()
        return_object = lookup_session.get_assessment_taken(assessment_taken_id)
        return return_object"""

    is_assessment_section_complete = """
        return self.get_assessment_section(assessment_section_id).get_assessment_taken().has_ended()"""

    get_incomplete_assessment_sections = """
        from .objects import AssessmentSectionList
        assessment_taken = self._get_assessment_taken(assessment_taken_id)
        # Is this right?  How do we define complete?
        if assessment_taken.has_ended():
            return AssessmentSectionList([])
        else:
            return AssessmentSectionList([self.get_assessment_section(assessment_taken_id)])"""

    has_assessment_section_begun = """
        return self._get_assessment_taken(assessment_section_id).has_started()"""

    is_assessment_section_over = """
        return self._get_assessment_taken(assessment_section_id).has_ended()"""

    finished_assessment_section = """
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        self.finished_assessment(assessment_section_id)"""

    requires_synchronous_responses = """
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        return self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['synchronousResponses']"""

    get_first_question = """
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        ## What if there are no items???
        item_id_str = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds'][0]
        return self._get_question(item_id_str)""" 

    has_next_question = """
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        try:
            if len(item_ids) > item_ids.index(str(item_id)) + 1:
                return True
        except ValueError:
            raise NotFound('item id not in assessment')"""

    get_next_question = """
        if not self.has_next_question(assessment_section_id, item_id):
            raise IllegalState()
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        return self._get_question(item_ids[item_ids.index(str(item_id)) + 1])"""

    has_previous_question = """
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        try:
            if item_ids.index(str(item_id)) > 0:
                return True
        except ValueError:
            raise NotFound('item id not in assessment')"""

    get_previous_question = """
        if not self.has_previous_question():
            raise IllegalState()
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        return self._get_question(item_ids[item_ids.index(str(item_id)) - 1])"""

    get_question = """
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        if str(item_id) not in item_ids:
            raise NotFound()
        return self._get_question(str(item_id))

    def _get_question(self, item_idstr):
        item_id = Id(item_idstr)
        from .objects import Question
        collection = MongoClient()['assessment']['Item']
        item_map = collection.find_one({'_id': ObjectId(item_id.get_identifier())})
        if item_map is None:
            raise NotFound()
        return Question(item_map['question'])"""

    get_questions = """
        from .objects import QuestionList
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        if self.requires_synchronous_responses(assessment_section_id):
            raise IllegalState() # This may need to actually be implemented
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        questions = []
        for item_idstr in item_ids:
            questions.append(self._get_question(item_idstr))
        return QuestionList(questions)"""

    get_response_form = """
        from ...abstract_osid.id.primitives import Id as ABCId
        from .objects import AnswerForm
        SUBMITTED = True
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        if item_id is None:
            raise NullArgument()
        if not isinstance(item_id, ABCId):
            raise InvalidArgument('argument is not a valid OSID Id')
        ##
        # This is a little hack to get the answer record types from the Item's
        # Question record types. Should really get it from item genus types somehow:
        try:
            from .records.types import ANSWER_RECORD_TYPES as record_type_data_sets
        except ImportError, AttributeError:
            record_type_data_sets = dict()
        collection = MongoClient()['assessment']['Item']
        item_map = collection.find_one({'_id': ObjectId(item_id.get_identifier())})
        if item_map is None:
            raise NotFound()
        answer_record_types = []
        for record_type_idstr in item_map['question']['recordTypeIds']:
            identifier = Id(record_type_idstr).get_identifier()
            if identifier in record_type_data_sets:
                answer_record_types.append(Type(**record_type_data_sets[identifier]))
        # Thus endith the hack.
        ##
        obj_form = AnswerForm(bank_id = self._catalog_id, record_types = answer_record_types, item_id = item_id, catalog_id = self._catalog_id, assessment_section_id = assessment_section_id)
        obj_form._for_update = False # This may be redundant
        self._forms[obj_form.get_id().get_identifier()] = not SUBMITTED
        return obj_form"""

    submit_response = """
        from ...abstract_osid.assessment.objects import AnswerForm as ABCAnswerForm
        collection = MongoClient()['assessment']['AssessmentTaken']
        SUBMITTED = True
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        if answer_form is None:
            raise NullArgument()
        if not isinstance(answer_form, ABCAnswerForm):
            raise InvalidArgument('argument type is not an AnswerForm')
        ##
        # OK, so the following should actually NEVER be true:
        if answer_form.is_for_update():
            raise InvalidArgument('the AnswerForm is for update only, not submit')
        try:
            if self._forms[answer_form.get_id().get_identifier()] == SUBMITTED:
                raise IllegalState('answer_form already used in a submit transaction')
        except KeyError:
            raise Unsupported('answer_form did not originate from this assessment session')
        if not answer_form.is_valid():
            raise InvalidArgument('one or more of the form elements is invalid')
        answer_form._my_map['_id'] = ObjectId()
        assessment_taken_map = self._get_assessment_taken(assessment_section_id)._my_map
        if Id(answer_form._my_map['itemId']).get_identifier() in assessment_taken_map['responses']:
            assessment_taken_map['responses'][Id(answer_form._my_map['itemId']).get_identifier()] = answer_form._my_map
        else:
            raise NotFound()
        try:
            collection.save(assessment_taken_map)
        except: # what exceptions does mongodb insert raise?
            raise OperationFailed()
        self._forms[answer_form.get_id().get_identifier()] = SUBMITTED"""

    skip_item = """
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        raise Unimplemented()"""

    is_question_answered = """
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        if item_id.get_identifer() in reponses:
            return bool(responses[item_id.get_identifer()])
        else:
            raise NotFound()"""

    get_unanswered_questions = """
        # Note: this implementation returns them in order
        from .objects import QuestionList
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        question_list = []
        for item_idstr in item_ids:
            if responses[Id(item_idstr).get_identifier()] is None:
                question_list.append(self._get_question(item_idstr))
        return QuestionList(question_list)"""

    has_unanswered_questions = """
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        for item_idstr in responses:
            if responses[Id(item_idstr).get_identifier()] is None:
                return True
        return False"""

    get_first_unanswered_question = """
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        if not self.has_unanswered_questions(assessment_section_id):
            raise IllegalState('No more unanswered questions')
        unanswered_questions = self.get_unanswered_questions(assessment_section_id)
        return unanswered_questions.get_next_question()"""

    has_next_unanswered_question = """
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        try:
            item_index = item_ids.index(str(item_id))
        except ValueError:
            raise NotFound()
        # could use itertools.islice here?  Don't know if these will ever be large lists
        for item_idstr in item_ids[item_index:]:
            if responses[Id(item_idstr).get_identifier()] is None:
                return True
        return False"""

    get_next_unanswered_question = """
        # This seems to share a lot of code with has_next_unanswered_question.  Just sayin'.
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        try:
            item_index = item_ids.index(str(item_id))
        except ValueError:
            raise NotFound()
        # could use itertools.islice here?  Don't know if these will ever be large lists
        for item_idstr in item_ids[item_index:]:
            if responses[Id(item_idstr).get_identifier()] is None:
                return self._get_question(item_idstr)
        raise IllegalState()"""

    has_previous_unanswered_question = """
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        try:
            item_index = item_ids.index(str(item_id))
        except ValueError:
            raise NotFound()
        # could use itertools.islice here?  Don't know if these will ever be large lists
        for item_idstr in item_ids[:item_index].reverse():
            if responses[Id(item_idstr).get_identifier()] is None:
                return True
        return False"""

    get_previous_unanswered_question = """
        # This seems to share a lot of code with has_next_unanswered_question.  Just sayin'.
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        item_ids = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['itemIds']
        try:
            item_index = item_ids.index(str(item_id))
        except ValueError:
            raise NotFound()
        # could use itertools.islice here?  Don't know if these will ever be large lists
        for item_idstr in item_ids[:item_index].reverse():
            if responses[Id(item_idstr).get_identifier()] is None:
                return self._get_question(item_idstr)
        raise IllegalState()"""

    get_response = """
        from .rules import Response
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        if item_id.get_identifier() in responses and responses[item_id.get_identifier()] is not None:
            return Response(responses[item_id.get_identifier()])
        else:
            raise NotFound()"""

    get_responses = """
        from .objects import ResponseList
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        responses = self.get_assessment_section(assessment_section_id).get_assessment_taken()._my_map['responses']
        answer_list = []
        for item_idstr in responses:
            if responses[item_idstr] is not None:
                answer_list.append(responses[Id(item_idstr).get_identifier()])
        return ResponseList(answer_list)"""

    clear_response = """
        from .rules import Response
        collection = MongoClient()['assessment']['AssessmentTaken']
        if (not self.has_assessment_section_begun(assessment_section_id) or 
            self.is_assessment_section_over(assessment_section_id)):
            raise IllegalState()
        assessment_taken = self.get_assessment_section(assessment_section_id).get_assessment_taken()
        if item_id.get_identifier() in assessment_taken._my_map['responses']:
            assessment_taken._my_map['responses'][item_id.get_identifier()] = None
            collection.save(assessment_taken._my_map)
        else:
            raise NotFound()"""

    finish = """
        self.finished_assessment(assessment_section_id)
    
    def finish_assessment_section(self, assessment_section_id):
        self.finish(assessment_section_id)"""

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
            raise NotFound()
            """

    get_answers = """
        from .objects import AnswerList
        if self.is_answer_available(assessment_section_id, item_id):
            collection = MongoClient()['assessment']['Item']
            item_map = collection.find_one({'_id': ObjectId(item_id.get_identifier())})
            if item_map is None:
                raise NotFound()
            return AnswerList(item_map['answers'])
        else:
            raise IllegalState()"""
    

class ItemAdminSession:

    # This method is hand implemented to raise and error if the item
    # is found in the Assessment_Items table
    delete_item = """
        from ...abstract_osid.id.primitives import Id as ABCId
        from ..osid.osid_errors import NotFound, NullArgument, InvalidArgument, OperationFailed, PermissionDenied, Unsupported
        from .objects import Item
        from bson.objectid import ObjectId
        from pymongo import MongoClient
        UPDATED = True
        if item_id is None:
            raise NullArgument()
        if not isinstance(item_id, ABCId):
            return InvalidArgument('the argument is not a valid OSID Id')
        collection = MongoClient()['assessment']['Assessment_Items']
        if collection.find({'itemIds': str(item_id)}).count() != 0:
            raise IllegalState('this Item is still being used in one or more Assessments')
        collection = MongoClient()['assessment']['Item']
        item_map = collection.find_one({'_id': ObjectId(item_id.get_identifier())})
        if item_map is None:
            raise NotFound()
        Item(item_map)._delete()
        result = collection.remove({'_id': ObjectId(item_id.get_identifier())}, justOne=True)
        if 'err' in result and result['err'] is not None:
            raise OperationFailed()
        if result['n'] == 0:
            raise NotFound()"""

    # These methods overwrite the canonical aggregate object admin methods to 
    # deal with authoring Questions with are special: ie. there is only one per
    # Item.  Perhaps we will see this pattern again and can make templates.

    create_question = """
        from ...abstract_osid.assessment.objects import QuestionForm as ABCQuestionForm
        from bson.objectid import ObjectId
        from ..primitives import Id
        from ..osid.osid_errors import IllegalState, InvalidArgument, NullArgument, OperationFailed, PermissionDenied, AlreadyExists, Unsupported
        from pymongo import MongoClient
        collection = MongoClient()['assessment']['Item']
        CREATED = True
        if question_form is None:
            raise NullArgument()
        if not isinstance(question_form, ABCQuestionForm):
            raise InvalidArgument('argument type is not an QuestionForm')
        if question_form.is_for_update():
            raise InvalidArgument('the QuestionForm is for update only, not create')
        try:
            if self._forms[question_form.get_id().get_identifier()] == CREATED:
                raise IllegalState('question_form already used in a create transaction')
        except KeyError:
            raise Unsupported('question_form did not originate from this session')
        if not question_form.is_valid():
            raise InvalidArgument('one or more of the form elements is invalid')
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
            #raise AlreadyExists()
        try:
            id_ = collection.save(item)
        except: # what exceptions does mongodb insert raise?
            raise OperationFailed()
        self._forms[question_form.get_id().get_identifier()] = CREATED
        from .objects import Question
        return Question(question_form._my_map)"""

    get_question_form_for_update = """
        from bson.objectid import ObjectId
        from ...abstract_osid.id.primitives import Id as ABCId
        from .objects import QuestionForm
        from ..osid.osid_errors import NotFound, NullArgument, InvalidArgument, OperationFailed, PermissionDenied, Unsupported
        from bson.objectid import ObjectId
        from pymongo import MongoClient
        collection = MongoClient()['assessment']['Item']
        UPDATED = True
        if question_id is None:
            raise NullArgument()
        if not isinstance(question_id, ABCId):
            return InvalidArgument('the argument is not a valid OSID Id')
        document = collection.find_one({'question._id': ObjectId(question_id.get_identifier())})
        if document is None:
            raise NotFound()
        obj_form = QuestionForm(document['question'])
        #obj_form._for_update = True # This seems redundant
        self._forms[obj_form.get_id().get_identifier()] = not UPDATED
        return obj_form"""

    update_question = """
        from bson.objectid import ObjectId
        from ..primitives import Id
        from ...abstract_osid.assessment.objects import QuestionForm as ABCQuestionForm
        from ..osid.osid_errors import IllegalState, InvalidArgument, NullArgument, OperationFailed, PermissionDenied, Unsupported
        from pymongo import MongoClient
        collection = MongoClient()['assessment']['Item']
        UPDATED = True
        if question_form is None:
            raise NullArgument()
        if not isinstance(question_form, ABCQuestionForm):
            raise InvalidArgument('argument type is not an QuestionForm')
        if not question_form.is_for_update():
            raise InvalidArgument('the QuestionForm is for update only, not create')
        try:
            if self._forms[question_form.get_id().get_identifier()] == UPDATED:
                raise IllegalState('question_form already used in an update transaction')
        except KeyError:
            raise Unsupported('question_form did not originate from this session')
        if not question_form.is_valid():
            raise InvalidArgument('one or more of the form elements is invalid')
        item_id = Id(question_form._my_map['itemId']).get_identifier()
        item = collection.find_one({'$and': [{'_id': ObjectId(item_id)},
                                      {'bankId': str(self._catalog_id)}]})
        item['question'] = question_form._my_map
        try:
            collection.save(item)
        except: # what exceptions does mongodb save raise?
            raise OperationFailed()
        self._forms[question_form.get_id().get_identifier()] = UPDATED
        # Note: this is out of spec. The OSIDs don't require an object to be returned:
        from .objects import Question
        return Question(question_form._my_map)"""


class AssessmentAdminSession:

    delete_assessment = """
        from ...abstract_osid.id.primitives import Id as ABCId
        from ..osid.osid_errors import NotFound, NullArgument, InvalidArgument, OperationFailed, PermissionDenied, Unsupported
        from bson.objectid import ObjectId
        from pymongo import MongoClient
        collection = MongoClient()['assessment']['Assessment']
        UPDATED = True
        if assessment_id is None:
            raise NullArgument()
        if not isinstance(assessment_id, ABCId):
            return InvalidArgument('the argument is not a valid OSID Id')
        collection = MongoClient()['assessment']['AssessmentOffered']
        if collection.find({'assessmentId': str(assessment_id)}).count() != 0:
            raise IllegalState('there are still AssessmentsOffered associated with this Assessment')
        collection = MongoClient()['assessment']['Assessment']
        result = collection.remove({'_id': ObjectId(assessment_id.get_identifier())}, justOne=True)
        if 'err' in result and result['err'] is not None:
            raise OperationFailed()
        if result['n'] == 0:
            raise NotFound()
        else:
            collection = MongoClient()['assessment']['Assessment_Items']
            collection.remove({'_id': ObjectId(assessment_id.get_identifier())}, justOne=True)"""

class AssessmentTakenLookupSession:

    # This is hand built, but there may be a pattern to try to map, specifically
    # getting objects for another package object and a persisted id thingy
    get_assessments_taken_for_taker_and_assessment_offered = """
        # NOTE: This implementation currently ignores plenary view
        from .objects import AssessmentTakenList
        from ..osid.osid_errors import OperationFailed, PermissionDenied
        from pymongo import MongoClient
        collection = MongoClient()['assessment']['AssessmentTaken']
        if self._catalog_view == self.ISOLATED:
            result = collection.find({'assessmentOfferedId': str(assessment_offered_id),
                                      'takingAgentId': str(resource_id),
                                      'bankId': str(self._catalog_id)})
            count = collection.find({'assessmentOfferedId': str(assessment_offered_id),
                                     'takingAgentId': str(resource_id),
                                     'bankId': str(self._catalog_id)}).count()
        else:
            result = collection.find({'assessmentOfferedId': str(assessment_offered_id),
                                      'takingAgentId': str(resource_id)})
            count = collection.find({'assessmentOfferedId': str(assessment_offered_id),
                                     'takingAgentId': str(resource_id)}).count()
        return AssessmentTakenList(result, count)"""

    get_assessments_taken_for_assessment = """
        from .objects import AssessmentOfferedList, AssessmentTakenList
        from ..osid.osid_errors import OperationFailed, PermissionDenied
        from pymongo import MongoClient
        collection = MongoClient()['assessment']['AssessmentOffered']
        if self._catalog_view == self.ISOLATED:
            result = collection.find({'assessmentId': str(assessment_id),
                                     'bankId': str(self._catalog_id)})
            count = collection.find({'assessmentId': str(assessment_id),
                                     'bankId': str(self._catalog_id)}).count()
        else:
            result = collection.find({'assessmentId': str(assessment_id)})
            count = collection.find({'assessmentId': str(assessment_id)}).count()
        assessments_offered = AssessmentOfferedList(result, count)

        collection = MongoClient()['assessment']['AssessmentTaken']
        ao_ids = []
        for ao in assessments_offered:
            ao_ids.append(str(ao.get_id()))
            
        if self._catalog_view == self.ISOLATED:
            result = collection.find({'assessmentOfferedId': {'$in':[ao_ids]},
                                     'bankId': str(self._catalog_id)})
            count = collection.find({'assessmentOfferedId': {'$in':[ao_ids]},
                                     'bankId': str(self._catalog_id)}).count()
        else:
            result = collection.find({'assessmentOfferedId': {"$in":[ao_ids]}})
            count = collection.find({'assessmentOfferedId': {"$in":[ao_ids]}}).count()
        return AssessmentTakenList(result, count)"""


class AssessmentTakenAdminSession:

    import_statements = [
        'from ..osid.osid_errors import *',
        'from pymongo import MongoClient'
    ]

    create_assessment_taken = """
        ##
        # This impl differs from the usual create_osid_object method in that it
        # sets an agent id...
        from ...abstract_osid.assessment.objects import AssessmentTakenForm as ABCAssessmentTakenForm
#        from ..osid.osid_errors import IllegalState, InvalidArgument, NullArgument, OperationFailed, PermissionDenied, Unsupported
#        from pymongo import MongoClient
        collection = MongoClient()['assessment']['AssessmentTaken']
        CREATED = True
        if assessment_taken_form is None:
            raise NullArgument()
        if not isinstance(assessment_taken_form, ABCAssessmentTakenForm):
            raise InvalidArgument('argument type is not an AssessmentTakenForm')
        if assessment_taken_form.is_for_update():
            raise InvalidArgument('the AssessmentForm is for update only, not create')
        try:
            if self._forms[assessment_taken_form.get_id().get_identifier()] == CREATED:
                raise IllegalState('assessment_taken_form already used in a create transaction')
        except KeyError:
            raise Unsupported('assessment_taken_form did not originate from this session')
        if not assessment_taken_form.is_valid():
            raise InvalidArgument('one or more of the form elements is invalid')
        ##
        # ...here:
        assessment_taken_form._my_map['takingAgentId'] = str(self.get_effective_agent_id())
        try:
            id_ = collection.insert(assessment_taken_form._my_map)
        except: # what exceptions does mongodb insert raise?
            raise OperationFailed()
        from .objects import AssessmentTaken
        self._forms[assessment_taken_form.get_id().get_identifier()] = CREATED
        return AssessmentTaken(collection.find_one({'_id': id_}))
"""

class AssessmentBasicAuthoringSession:

    import_statements = [
        'from pymongo import MongoClient',
        'from bson.objectid import ObjectId',
        'from ..osid.osid_errors import *',
        'from .objects import ItemList',
        'from ..primitives import *'
    ]

    init = """
    def __init__(self, catalog_id = None, proxy = None):
        from .objects import Bank
        from ..osid.sessions import OsidSession
        self._catalog_class = Bank
        self._session_name = 'AssessmentBasicAuthoringSession'
        self._catalog_name = 'Bank'
        OsidSession._init_object(self, catalog_id, proxy, db_name='assessment', cat_name='Bank', cat_class=Bank)
"""

    old_init ="""
    def __init__(self, catalog_id = None, *args, **kwargs):
        from .objects import Bank
        from ..osid.sessions import OsidSession
        from . import profile
        OsidSession.__init__(self, *args, **kwargs)
        from pymongo import MongoClient
        collection = MongoClient()['assessment']['Bank']
        if catalog_id is not None and catalog_id.get_identifier() != '000000000000000000000000':
            self._catalog_identifier = catalog_id.get_identifier()
            self._my_catalog_map = collection.find_one({'_id': ObjectId(self._catalog_identifier)})
            if self._my_catalog_map is None:
                raise NotFound('could not find catalog identifier ' + catalog_id.get_identifier())
        else:
            from ..primitives import Id, Type
            from .. import types
            self._catalog_identifier = '000000000000000000000000'
            self._my_catalog_map = {
                '_id': ObjectId(self._catalog_identifier),
                'displayName': {'text': 'Default Bank',
                                'languageType': str(Type(**types.Language().get_type_data('DEFAULT'))),
                                'scriptType': str(Type(**types.Script().get_type_data('DEFAULT'))),
                                'formatType': str(Type(**types.Format().get_type_data('DEFAULT'))),},
                'description': {'text': 'The Default Bank',
                                'languageType': str(Type(**types.Language().get_type_data('DEFAULT'))),
                                'scriptType': str(Type(**types.Script().get_type_data('DEFAULT'))),
                                'formatType': str(Type(**types.Format().get_type_data('DEFAULT'))),},
                'genusType': str(Type(**types.Genus().get_type_data('DEFAULT')))
            }
        self._catalog = Bank(self._my_catalog_map)
        self._catalog_id = self._catalog.get_id()
        self._forms = dict()
"""

    can_author_assessment = """
        # NOTE: It is expected that real authentication hints will be 
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    get_items = """
        if assessment_id is None:
            raise NullArgument()
        collection = MongoClient()['assessment']['Assessment']
        assessment = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})
        if assessment is None:
            raise NotFound()
        collection = MongoClient()['assessment']['Assessment_Items']
        assessment_items = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})
        if assessment_items is None:
            return ItemList([])
        collection = MongoClient()['assessment']['Item']
        item_list = []
        # This appears to assume that all the Items exist. Need to consider this further:
        for i in assessment_items['itemIds']:
            item_list.append(collection.find_one({'_id': ObjectId(Id(i).get_identifier())}))
        return ItemList(item_list)"""

    add_item = """
        if assessment_id is None or item_id is None:
            raise NullArgument()
        collection = MongoClient()['assessment']['Assessment']
        assessment = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})
        if assessment is None:
            raise NotFound()
        collection = MongoClient()['assessment']['Item']
        item = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})
        if item == '':
            raise NotFound()
        collection = MongoClient()['assessment']['Assessment_Items']
        assessment_items = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})
        if assessment_items is None:
            assessment_items = {'_id': ObjectId(assessment_id.get_identifier()), 'itemIds': [str(item_id)]}
        else: 
            assessment_items['itemIds'].append(str(item_id))
        collection.save(assessment_items)"""

    remove_item = """
        if assessment_id is None or item_id is None:
            raise NullArgument()
        collection = MongoClient()['assessment']['Assessment']
        assessment = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})
        if assessment == '':
            raise NotFound('an assessment with assessment_id does not exist')
        collection = MongoClient()['assessment']['Assessment_Items']
        assessment_items = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})
        try:
            assessment_items['itemIds'].remove(str(item_id))
        except ValueError:
            raise NotFound('item_id not found on assessment')
        collection.save(assessment_items)"""

    move_item = """
        if (assessment_id is None or item_id is None or preceeding_item_id is None):
            raise NullArgument()
        collection = MongoClient()['assessment']['Assessment']
        assessment = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})
        if assessment is None:
            raise NotFound('an assessment with assessment_id does not exist')
        collection = MongoClient()['assessment']['Assessment_Items']
        assessment_items = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})
        if assessment_items is None:
            raise NotFound('item_id not found in Assessment items')
        try:
            p_index = assessment_items['itemIds'].index(str(preceeding_item_id))
        except ValueError:
            raise NotFound('preceeding_item_id not associated with assessment')
        try:
            assessment_items().remove(str(item_id))
        except ValueError:
            raise NotFound('item_id not associated with assessment')
        assessment_items['itemIds'].insert(str(item_id), p_index + 1)
        collection.save(assessment_items)"""


    order_items = """
    ## STILL NOT DONE???
        # Currently this implementation assumes that all item_ids are 
        # included in the argument list. The case where a subset is provided
        # will be implemented later, but this covers the primary case
        # that we will see from a RESTful consumer.
        if item_ids is None or assessment_id is None:
            raise NullArgument()
        collection = MongoClient()['assessment']['Assessments']
        assessment = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})
        if assessment is None:
            raise NotFound('an assessment with assessment_id does not exist')
        collection = MongoClient()['assessment']['Assessment_Items']
        assessment_items = collection.find_one({'_id': ObjectId(assessment_id.get_identifier())})
        if assessment_items is None:
            raise NotFound('no items were found for this assessment_id')        
        if len(assessment_items['itemIds']) != len(item_ids):
            raise OperationFailed()
        item_id_list = []
        for i in item_ids:
            if str(i) not in assessment_items['itemIds']:
                raise OperationFailed()
            item_id_list.append(str(i))
        assessment['itemIds'] = item_id_list
        collection.save(assessment)"""

class Question:

    import_statements = [
        'from ..osid.objects import OsidObject',
        'from ..primitives import *'
    ]

    additional_methods = """
    ##
    # Overide osid.Identifiable.get_id() method to cast this question id as its item id:
    def get_id(self):
        return Id(self._my_map['itemId'])

    id_ = property(fget=get_id)
    ident = property(fget=get_id)
"""

class Item:

    get_question_id = """
        self.get_question().get_id()"""

    get_question = """
        return Question(self._my_map['question'])"""

    additional_methods = """
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
    
    import_statements_pattern = [
        'from ..primitives import *',
        'from ..osid.osid_errors import *'
        ]

    has_start_time_template = """
        # Implemented from template for osid.assessment.AssessmentOffered.has_start_time_template
        return bool(self._my_map['${var_name_mixed}'])"""

    get_start_time_template = """
        # Implemented from template for osid.assessment.AssessmentOffered.get_start_time_template
        if not bool(self._my_map['${var_name_mixed}']):
            raise IllegalState()
        dt = self._my_map['${var_name_mixed}']
        return DateTime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)
#old        return DateTime(**self._my_map['${var_name_mixed}'])"""

    has_duration_template = """
        # Implemented from template for osid.assessment.AssessmentOffered.has_duration_template
        return bool(self._my_map['${var_name_mixed}'])"""

    get_duration_template = """
        # Implemented from template for osid.assessment.AssessmentOffered.get_duration_template
        if not bool(self._my_map['${var_name_mixed}']):
            raise IllegalState()
#        d = self._my_map['${var_name_mixed}']
#        return d
        return Duration(**self._my_map['${var_name_mixed}'])"""

class AssessmentOfferedForm:

    set_start_time_template = """
        # Implemented from template for osid.assessment.AssessmentOfferedForm.set_start_time_template
        if ${arg0_name} is None:
            raise NullArgument()
        if self.get_${var_name}_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_${arg0_type_under}(${arg0_name}, 
                                self.get_${var_name}_metadata()):
            raise InvalidArgument()
        self._my_map['${var_name_mixed}'] = ${arg0_name}

##
# The old wwy:
#        map = dict()
#        map['year'] = ${arg0_name}.year
#        map['month'] = ${arg0_name}.month
#        map['day'] = ${arg0_name}.day
#        map['hour'] = ${arg0_name}.hour
#        map['minute'] = ${arg0_name}.minute
#        map['second'] = ${arg0_name}.second
#        map['microsecond'] = ${arg0_name}.microsecond
#        self._my_map['${var_name_mixed}'] = map"""

    # This looks just like the generic one. Need to find in the pattern?
    clear_start_time_template = """
        if (self.get_${var_name}_metadata().is_read_only() or
            self.get_${var_name}_metadata().is_required()):
            raise NoAccess()
        self._my_map['${var_name_mixed}'] = self._${var_name}_default"""

    set_duration_template = """
        # Implemented from template for osid.assessment.AssessmentOfferedForm.set_duration_template
        if ${arg0_name} is None:
            raise NullArgument()
        if self.get_${var_name}_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_${arg0_type_under}(${arg0_name}, 
                                self.get_${arg0_name}_metadata()):
            raise InvalidArgument()
        map = dict()
        map['days'] = ${arg0_name}.days
        map['seconds'] = ${arg0_name}.seconds
        map['microseconds'] = ${arg0_name}.microseconds
        self._my_map['${var_name_mixed}'] = map"""

class AssessmentTaken:

    import_statements = [
        'from ..primitives import *',
        'from ..osid.osid_errors import *'
    ]

    get_taker_id = """
        if self._my_map['takerId']:
            return Id(self._my_map['takerId'])
        else:
            return Id(self._my_map['takingAgentId'])"""

    get_taker = """
        raise Unimplemented()"""

    get_taking_agent_id = """
        return Id(self._my_map['takingAgentId'])"""

    get_taking_agent = """
        raise Unimplemented()"""

    has_started = """
        if self._my_map['started']:
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
            raise IllegalState('this assessment has not yet started')
        if self._my_map['actualStartTime'] is None:
            raise IllegalState('this assessment has not yet been started by the taker')
        else:
            return self._my_map['actualStartTime']"""

    has_ended = """
        # Perhaps this should just check for existance of self._my_map['completionTime']?
        return bool(self._my_map['ended'])"""

    get_completion_time = """
        if not self.has_ended():
            raise IllegalState('this assessment has not yet ended')
        if not self._my_map['completionTime']:
            raise OperationFailed('someone forgot to set the completion time')
        return self._my_map['completionTime']"""

    get_time_spent = """
        if self.has_started() and self.has_ended():
            return self.get_completion_time() - self.get_actual_start_time()
        else:
            raise IllegalState()"""

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
        'from ..primitives import *',
        'default_language_type = Type(**types.Language().get_type_data(\'DEFAULT\'))',
        'default_script_type = Type(**types.Script().get_type_data(\'DEFAULT\'))',
        'default_format_type = Type(**types.Format().get_type_data(\'DEFAULT\'))'
    ]

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
        'from ..primitives import *',
        'from ..osid.osid_errors import *'
    ]

    init = """
    try:
        from .records.types import ANSWER_RECORD_TYPES as _record_type_data_sets
    except ImportError, AttributeError:
        _record_type_data_sets = dict()
    _namespace = 'assessment.Response'

    def __init__(self, response_map, **kwargs):
        self._my_map = response_map
        self._records = dict()
        self._load_records(response_map['recordTypeIds'])

    def _load_records(self, record_type_idstrs):
        for record_type_idstr in record_type_idstrs:
            self._init_record(record_type_idstr)

    def _init_record(self, record_type_idstr):
        import importlib
        from ..primitives import Id
        record_type_data = self._record_type_data_sets[Id(record_type_idstr).get_identifier()]
        module = importlib.import_module(record_type_data['module_path'])
        record = getattr(module, record_type_data['object_record_class_name'])
        self._records[record_type_idstr] = record(self)
"""

    get_item_id = """
        return Id(self._my_map['itemId'])"""

    get_item = """
        # So, why would we ever let an AssessmentSession user get the Item???
        raise PermissionDenied()"""

    get_response_record = """
        if item_record_type is None:
            raise NullArgument()
        if not self.has_record_type(item_record_type):
            raise Unsupported()
        if str(item_record_type) not in self._records:
            raise Unimplemented()
        return self._records[str(item_record_type)]"""

