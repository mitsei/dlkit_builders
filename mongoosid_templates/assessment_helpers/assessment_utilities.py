"""Utilities for use by assessment package implementations"""
import importlib

from dlkit.abstract_osid.osid.errors import NotFound, NullArgument, IllegalState
from dlkit.abstract_osid.assessment.objects import Assessment as abc_assessment
from ..utilities import get_provider_manager, MongoClientValidated
from dlkit.primordium.id.primitives import Id
from dlkit.primordium.type.primitives import Type
from bson import ObjectId

SIMPLE_SEQUENCE_RECORD_TYPE = Type(**{
    'authority': 'ODL.MIT.EDU',
    'namespace': 'osid-object',
    'identifier': 'simple-child-sequencing'})


def check_effective(func):
    """decorator, tests if an Assessment or Section is effective, raises error if not

    Side benefit: raised NotFound on AssessmentSections and AssessmentTakens

    """
    def wrapper(*args, **kwargs):
        if ('assessment_section_id' in kwargs or
                args and 'Section' in args[1].get_identifier_namespace()):
            try:
                assessment_section_id = kwargs['assessment_section_id']
            except KeyError:
                assessment_section_id = args[1]
            if (not args[0].has_assessment_section_begun(assessment_section_id) or
                    args[0].is_assessment_section_over(assessment_section_id)):
                raise IllegalState()
        else:
            if 'assessment_taken_id' in kwargs:
                assessment_taken_id = kwargs['assessment_taken_id']
            else:
                assessment_taken_id = args[1]
            assessment_taken = args[0]._get_assessment_taken(assessment_taken_id)
            if not assessment_taken.has_started() or assessment_taken.has_ended():
                raise IllegalState()
        return func(*args, **kwargs)
    return wrapper

def get_first_part_id_for_assessment(assessment_id, runtime=None, proxy=None, create=False, bank_id=None):
    """Gets the first part id, which represents the first section, of assessment"""
    if create and bank_id is None:
        raise NullArgument('Bank Id must be provided for create option')
    try:
        return get_next_part_id(assessment_id, runtime, proxy)[0]
    except IllegalState:
        if create:
            return create_first_assessment_section(assessment_id, runtime, proxy, bank_id)
        else:
            raise

def get_next_part_id(part_id, runtime=None, proxy=None, level=0, prev_part_id=None, unsequestered=False, section=None):
    part, rule, siblings = get_decision_objects(part_id, runtime, proxy, unsequestered, section)
    check_parent = True
    if rule is not None: # A SequenceRule trumps everything.
        next_part_id = rule.get_next_assessment_part_id()
        level = get_level_delta(part_id, next_part_id, runtime, proxy)
        check_parent = False
    elif part.has_children(): # This is a special AssessmentPart that can manage child Parts
        if prev_part_id is None:
            try:
                if unsequestered or isinstance(part, abc_assessment):
                    next_part_id = part.get_child_ids().next()
                else:
                    next_part = part.get_child_assessment_parts().next()
                    next_part_id = next_part.ident
                level += 1
                check_parent = False
            except StopIteration:
                check_parent = True
        else:
            # this is to make sure that we don't get into an infinite loop, when
            # a parent object (see below, check_parent) has children, it will
            # return here. We don't want it to automatically return the first
            # child, because that will get into an infinite loop ... so pass
            # the given child as a param (prev_part_id) and make sure we
            # get the next child.
            child_ids = list(part.get_child_ids())
            child_id_strs = [str(c) for c in child_ids]
            if str(prev_part_id) not in child_id_strs:
                raise IllegalState('previous part is not a child of its own parent')
            if str(prev_part_id) == child_id_strs[-1]:
                pass
            else:
                for index, child_id_str in enumerate(child_id_strs):
                    if child_id_str == str(prev_part_id):
                        next_part_id = child_ids[index + 1]
                        level += 1
                        check_parent = False
                        break
    elif siblings and str(siblings[-1]) != str(part_id):
        siblings_str = [str(s) for s in siblings]
        try:
            next_part_id = siblings[siblings_str.index(str(part_id)) + 1]
            check_parent = False
        except ValueError:
            # the given partId is not in the siblings
            check_parent = True

    if check_parent: # We are at a lowest leaf and need to check parent
        if isinstance(part, abc_assessment): # This is an Assessment masquerading as an AssessmentPart
            raise IllegalState('No next AssessmentPart is available for part_id')
        elif part.has_parent_part(): # This is the child of another AssessmentPart
            next_part_id, level = get_next_part_id(part.get_assessment_part_id(), runtime, proxy, level - 1, part_id)
        else: # This is the child of an Assessment. Will this ever be the case?
            next_part_id, level = get_next_part_id(part.get_assessment_id(), runtime, proxy, -1, part_id)
    return next_part_id, level

def get_level_delta(part1_id, part2_id, runtime, proxy):
    def count_levels(part, increment):
        level = 0
        while part.has_parent_part():
            level = level + increment
            part = part.get_assessment_part()
        return level

    mgr = get_provider_manager('ASSESSMENT_AUTHORING', runtime, proxy)
    lookup_session = mgr.get_assessment_part_lookoup_session(proxy=proxy)
    part1 = lookup_session.get_assessment_part(part1_id)
    part2 = lookup_session.get_assessment_part(part2_id)
    while part1.has_parent_part() and part2.has_parent_part:
        part1 = part1.get_assessment_part
        part2 = part2.get_assessment_part
    if part1.has_parent_part():
        return count_levels(part1, -1)
    elif part2.has_parent_part():
        return count_levels(part2, 1)
    else:
        return 0

def get_decision_objects(part_id, runtime, proxy, unsequestered, section):
    assessment_lookup_session, part_lookup_session, rule_lookup_session = get_lookup_sessions(runtime,
                                                                                              proxy,
                                                                                              unsequestered,
                                                                                              section)
    sibling_ids = []
    try:
        part = part_lookup_session.get_assessment_part(part_id)
    except NotFound: # perhaps this is an assessment masquerading as a part:
        part = assessment_lookup_session.get_assessment(part_id)
    else:
        if part.has_parent_part():
            parent = part.get_assessment_part()
        else:
            parent = part.get_assessment()
        if parent.has_children():
            sibling_ids = parent.get_child_ids()
    rule = get_first_successful_sequence_rule_for_part(part_id, rule_lookup_session)
    return part, rule, list(sibling_ids)

def create_first_assessment_section(assessment_id, runtime, proxy, bank_id):
    assessment_admin_session, part_admin_session, rule_admin_session = get_admin_sessions(runtime, proxy, bank_id)
    mgr = get_provider_manager('ASSESSMENT', runtime=runtime, proxy=proxy, local=True)
    assessment_lookup_session = mgr.get_assessment_lookup_session(proxy=proxy)
    assessment_lookup_session.use_federated_bank_view()
    assessment = assessment_lookup_session.get_assessment(assessment_id)
    part_form = part_admin_session.get_assessment_part_form_for_create_for_assessment(assessment_id,
                                                                                      [SIMPLE_SEQUENCE_RECORD_TYPE])
    part_form.set_display_name(assessment.get_display_name().get_text() + ' First Part')
    part_form.set_sequestered(False) # Any Part of an Assessment must be a Section (i.e. non sequestered)
    # part_form.set_weight(100) # Uncomment this line when set_weight is implemented
    # Should we set allocated time?
    part_id = part_admin_session.create_assessment_part_for_assessment(part_form).get_id()
    if assessment._supports_simple_sequencing():
        child_ids = list(assessment.get_child_ids())
        child_ids.insert(0, str(part_id))
        update_form = assessment_admin_session.get_assessment_form_for_update(assessment.get_id())
        update_form.set_children([Id(i) for i in child_ids])
        assessment_admin_session.update_assessment(update_form)
    else:
        rule_form = rule_admin_session.get_rule_form_for_create(assessment.get_id(), part_id, [])
        rule_form.set_display_name('First Part Rule')
        rule_admin_session.create_rule(rule_form)
    return part_id

def get_lookup_sessions(runtime, proxy, unsequestered, section):
    # this has to use the magic part lookup session, too, if available ...
    mgr = get_provider_manager('ASSESSMENT', runtime=runtime, proxy=proxy, local=True)
    assessment_lookup_session = mgr.get_assessment_lookup_session(proxy=proxy)
    assessment_lookup_session.use_federated_bank_view()
    mgr = get_provider_manager('ASSESSMENT_AUTHORING', runtime=runtime, proxy=proxy, local=True)
    part_lookup_session = get_assessment_part_lookup_session(runtime, proxy, section)
    if unsequestered:
        part_lookup_session.use_unsequestered_assessment_part_view()
    part_lookup_session.use_federated_bank_view()
    rule_lookup_session = mgr.get_sequence_rule_lookup_session(proxy=proxy)
    rule_lookup_session.use_federated_bank_view()
    return assessment_lookup_session, part_lookup_session, rule_lookup_session

def get_assessment_part_lookup_session(runtime, proxy, section=None):
    """returns an assessment part lookup session, perhaps even a magic one"""
    # This appears to share code with get_item_lookup_session
    try:
        config = runtime.get_configuration()
        parameter_id = Id('parameter:magicAssessmentPartLookupSessions@mongo')
        import_path_with_class = config.get_value_by_parameter(parameter_id).get_string_value()
        module_path = '.'.join(import_path_with_class.split('.')[0:-1])
        magic_class = import_path_with_class.split('.')[-1]
        module = importlib.import_module(module_path)
        part_lookup_session = getattr(module, magic_class)(section,
                                                           runtime=runtime,
                                                           proxy=proxy)
    except (AttributeError, KeyError, NotFound):
        mgr = get_provider_manager('ASSESSMENT_AUTHORING', local=True)
        part_lookup_session = mgr.get_assessment_part_lookup_session(proxy=proxy)
    return part_lookup_session

def get_item_lookup_session(self, runtime=None, proxy=None):
    """returns an item lookup session, perhaps even a magic one"""
    # This appears to share code with get_assessment_part_lookup_session
    try:
        config = runtime.get_configuration()
        parameter_id = Id('parameter:magicItemLookupSessions@mongo')
        import_path_with_class = config.get_value_by_parameter(parameter_id).get_string_value()
        module_path = '.'.join(import_path_with_class.split('.')[0:-1])
        magic_class = import_path_with_class.split('.')[-1]
        module = importlib.import_module(module_path)
        item_lookup_session = getattr(module, magic_class)(runtime=runtime,
                                               proxy=proxy)
    except (AttributeError, KeyError, errors.NotFound):
        mgr = get_provider_manager('ASSESSMENT', runtime=runtime, proxy=proxy, local=True)
        item_lookup_session = mgr.get_item_lookup_session(proxy=proxy)
    return item_lookup_session

def get_admin_sessions(runtime, proxy, bank_id):
    mgr = get_provider_manager('ASSESSMENT', runtime=runtime, proxy=proxy, local=True)
    assessment_admin_session = mgr.get_assessment_admin_session_for_bank(bank_id=bank_id, proxy=proxy)
    mgr = get_provider_manager('ASSESSMENT_AUTHORING', runtime=runtime, proxy=proxy, local=True)
    part_admin_session = mgr.get_assessment_part_admin_session_for_bank(bank_id=bank_id, proxy=proxy)
    rule_admin_session = mgr.get_sequence_rule_admin_session_for_bank(bank_id=bank_id, proxy=proxy)
    return assessment_admin_session, part_admin_session, rule_admin_session

def get_first_successful_sequence_rule_for_part(part_id, rule_lookup_session):
    for rule in rule_lookup_session.get_sequence_rules_for_assessment_part(part_id):
        if rule._evaluates_true(): # Or wherever this wants to be evaluated
            return rule
    return None

def get_assessment_section(section_id, runtime=None, proxy=None):
    """Gets a Section given a section_id"""
    from .objects import AssessmentSection
    collection = MongoClientValidated('assessment',
                                      collection='AssessmentSection',
                                      runtime=runtime)
    result = collection.find_one(dict({'_id': ObjectId(section_id.get_identifier())}))
    return AssessmentSection(osid_object_map=result, runtime=runtime, proxy=proxy)

def get_default_part_map(part_id, level):
    return {
        'assessmentPartId': str(part_id),
        'level': level
    }

def get_default_question_map(item_id, question_id, assessment_part_id, display_elements):
    return {
        'itemId': str(item_id),
        'questionId': str(question_id),
        'assessmentPartId': str(assessment_part_id),
        'displayElements': display_elements,
        'responses': [None]
    }

def update_parent_sequence_map(child_part, delete=False):
    """Updates the child map of a simple sequence assessment assessment part"""
    if child_part.has_parent_part():
        object_map = child_part.get_assessment_part()._my_map
        database = 'assessment_authoring'
        collection_type = 'AssessmentPart'
    else:
        object_map = child_part.get_assessment()._my_map
        database = 'assessment'
        collection_type = 'Assessment'
    collection = MongoClientValidated(database,
                                      collection=collection_type,
                                      runtime=child_part._runtime)
    if delete:
        object_map['childIds'].remove(str(child_part.get_id()))
    else:
        object_map['childIds'].append(str(child_part.get_id()))
    collection.save(object_map)

def remove_from_parent_sequence_map(assessment_part_admin_session, assessment_part_id):
    """Updates the child map of a simple sequence assessment assessment part to remove child part"""
    mgr = get_provider_manager('ASSESSMENT_AUTHORING',
                               runtime=assessment_part_admin_session._runtime,
                               proxy=assessment_part_admin_session._proxy,
                               local=True)
    apls = mgr.get_assessment_part_lookup_session(proxy=assessment_part_admin_session._proxy)
    apls.use_federated_bank_view()
    child_part = apls.get_assessment_part(assessment_part_id)
    update_parent_sequence_map(child_part, delete=True)

# This may not be needed anymore, Time will tell
def simple_sequencing_error_check(assessment_part_id, next_assessment_part_id, *args, **kwargs):
    """This may not be needed anymore. Time will tell"""
    mgr = get_provider_manager('ASSESSMENT_AUTHORING', runtime=None, proxy=None, local=True)
    for child_part_id in [assessment_part_id, next_assessment_part_id]:
        child_part = mgr.get_assessment_part_lookup_session().get_assessment_part(child_part_id)
        if child_part.has_parent_part() and child_part.get_assessment_part().supports_simple_child_sequencing():
            raise IllegalState('AssessmentPart only supports simple sequencing')
        elif child_part.get_assessment().supports_simple_child_sequencing():
            raise IllegalState('Assessment only supports simple sequencing')