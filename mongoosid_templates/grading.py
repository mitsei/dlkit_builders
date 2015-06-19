
class GradeEntryAdminSession:

    import_statements = [
        'from dlkit.abstract_osid.id.primitives import Id as ABCId',
        'from dlkit.abstract_osid.type.primitives import Type as ABCType',
    ]

    get_grade_entry_form_for_create = """
        if not isinstance(gradebook_column_id, ABCId):
            raise errors.InvalidArgument('argument is not a valid OSID Id')
        if not isinstance(resource_id, ABCId):
            raise errors.InvalidArgument('argument is not a valid OSID Id')
        # Add code for checking Id and getting gradebook_column enclosure
        for arg in grade_entry_record_types:
            if not isinstance(arg, ABCType):
                raise errors.InvalidArgument('one or more argument array elements is not a valid OSID Type')
        if grade_entry_record_types == []:
            ## WHY are we passing gradebook_id = self._catalog_id below, seems redundant:
            obj_form = objects.GradeEntryForm(
                gradebook_id=self._catalog_id,
                gradebook_column_id=gradebook_column_id,
                resource_id=resource_id,
                effective_agent_id=str(self.get_effective_agent_id()),
                catalog_id=self._catalog_id,
                db_prefix=self._db_prefix,
                runtime=self._runtime)
        else:
            obj_form = objects.GradeEntryForm(
                gradebook_id=self._catalog_id,
                record_types=grade_entry_record_types,
                gradebook_column_id=gradebook_column_id,
                resource_id=resource_id,
                effective_agent_id=str(self.get_effective_agent_id()),
                catalog_id=self._catalog_id,
                db_prefix=self._db_prefix,
                runtime=self._runtime)
        obj_form._for_update = False
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form"""

    get_grade_entry_form_for_update = """
        collection = MongoClientValidated(self._db_prefix + 'grading', 'GradeEntry')
        if not isinstance(grade_entry_id, ABCId):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        if grade_entry_id.get_identifier_namespace() != 'grading.GradeEntry':
            if grade_entry_id.get_authority() != self._authority:
                raise errors.InvalidArgument()
            else:
                grade_entry_id = self._get_grade_entry_id_with_enclosure(grade_entry_id)
        result = collection.find_one({'_id': ObjectId(grade_entry_id.get_identifier())})

        obj_form = objects.GradeEntryForm(
            result,
            effective_agent_id=str(self.get_effective_agent_id()),
            db_prefix=self._db_prefix,
            runtime=self._runtime)
        self._forms[obj_form.get_id().get_identifier()] = not UPDATED

        return obj_form"""


class GradeSystem:

    get_lowest_numeric_score_template = """
        # Implemented from template for osid.grading.GradeSystem.get_lowest_numeric_score_template
        return self._my_map['${var_name_mixed}']"""

    # But the real implementations need to check is_based_on_grades():

    get_lowest_numeric_score = """
        if self.is_based_on_grades():
            raise errors.IllegalState('This GradeSystem is based on grades')
        return self._my_map['lowestNumericScore']"""

    get_highest_numeric_score = """
        if self.is_based_on_grades():
            raise errors.IllegalState('This GradeSystem is based on grades')
        return self._my_map['highestNumericScore']"""

    get_numeric_score_increment = """
        if self.is_based_on_grades():
            raise errors.IllegalState('This GradeSystem is based on grades')
        return self._my_map['numericScoreIncrement']"""


class GradeSystemForm:

    set_lowest_numeric_score_template = """
        # Implemented from template for osid.grading.GradeSystemForm.set_lowest_numeric_score
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        try:
            ${arg0_name} = float(${arg0_name})
        except ValueError:
            raise errors.InvalidArgument()
        if not self._is_valid_${arg0_type}(${arg0_name}, self.get_${var_name}_metadata()):
            raise errors.InvalidArgument()
        self._my_map['${var_name_mixed}'] = ${arg0_name}"""

    clear_lowest_numeric_score_template = """
        # Implemented from template for osid.grading.GradeSystemForm.clear_lowest_numeric_score
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['${var_name_mixed}'] = ${var_name}_default"""

class GradeEntry:

    import_statements = [
        'from ..resource.simple_agent import Agent',
    ]

    get_key_resource_id = """
        return self._my_map['resourceId']"""

    get_time_graded = """
        if not self.is_graded or self.is_derived():
            raise errors.IllegalState()
        time_graded = self._my_map['timeGraded']
        return DateTime(
            time_graded['year'],
            time_graded['month'],
            time_graded['day'],
            time_graded['hour'],
            time_graded['minute'],
            time_graded['second'],
            time_graded['microsecond'])"""

    is_graded = """
        return self._my_map['gradeId'] or self._my_map['score']"""

    get_grading_agent_id = """
        if not self.is_graded or self.is_derived():
            raise errors.IllegalState()
        return Id(self._my_map['gradingAgentId'])"""

    get_grading_agent = """
        return Agent(self.get_grading_agent_id())"""

    overrides_calculated_entry = """
        return bool(self._my_map('overriddenCalculatedEntryId'))"""

    get_overridden_calculated_entry_id = """
        if not self.overrides_calculated_entry():
            raise errors.IllegalState()
        return self._my_map['overriddenCalculatedEntryId']"""

class GradeEntryForm:

    import_statements = [
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.calendaring.primitives import DateTime',
        'from ..utilities import now_map'
    ]

    init = """
    try:
        from ..records.types import GRADE_ENTRY_RECORD_TYPES as _record_type_data_sets #pylint: disable=no-name-in-module
    except (ImportError, AttributeError):
        _record_type_data_sets = dict()
    _namespace = 'grading.GradeEntry'

    def __init__(self, osid_object_map=None, record_types=None, db_prefix='', runtime=None, **kwargs):
        osid_objects.OsidForm.__init__(self)
        self._runtime = runtime
        self._db_prefix = db_prefix
        self._kwargs = kwargs
        self._effective_agent_id = kwargs['effective_agent_id']

        mgr = self._get_provider_manager('GRADING')
        lookup_session = mgr.get_gradebook_column_lookup_session()
        lookup_session.use_federated_gradebook_view()
        gradebook_column = lookup_session.get_gradebook_column(kwargs['gradebook_column_id'])
        self._grade_system = gradebook_column.get_grade_system()

        if 'catalog_id' in kwargs:
            self._catalog_id = kwargs['catalog_id']
        self._init_metadata(**kwargs)
        self._records = dict()
        self._supported_record_type_ids = []
        if osid_object_map is not None:
            self._for_update = True
            self._my_map = osid_object_map
            self._load_records(osid_object_map['recordTypeIds'])
        else:
            self._my_map = {}
            self._for_update = False
            self._init_map(**kwargs)
            if record_types is not None:
                self._init_records(record_types)
        self._supported_record_type_ids = self._my_map['recordTypeIds']

    def _init_metadata(self, **kwargs):
        osid_objects.OsidRelationshipForm._init_metadata(self, **kwargs)
        self._grade_metadata = {
            'element_id': Id(
                self._authority,
                self._namespace,
                'grade')}
        self._grade_metadata.update(mdata_conf.GRADE_ENTRY_GRADE)
        self._ignored_for_calculations_metadata = {
            'element_id': Id(
                self._authority,
                self._namespace,
                'ignored_for_calculations')}
        self._ignored_for_calculations_metadata.update(mdata_conf.GRADE_ENTRY_IGNORED_FOR_CALCULATIONS)
        self._score_metadata = {
            'element_id': Id(
                self._authority,
                self._namespace,
                'score')}
        self._score_metadata.update(mdata_conf.GRADE_ENTRY_SCORE)
        self._score_metadata.update(
            {'minimum_decimal_value': self._grade_system.get_lowest_numeric_score(),
             'maximum_decimal_value': self._grade_system.get_highest_numeric_score()})
        self._grade_default = self._grade_metadata['default_id_values'][0]
        self._ignored_for_calculations_default = None
        self._score_default = self._score_metadata['default_decimal_values'][0]


    def _init_map(self, **kwargs):
        osid_objects.OsidRelationshipForm._init_map(self)
        self._my_map['resourceId'] = str(kwargs['resource_id'])
        self._my_map['gradeId'] = self._grade_default
        self._my_map['agentId'] = str(kwargs['effective_agent_id'])
        self._my_map['ignoredForCalculations'] = self._ignored_for_calculations_default
        self._my_map['score'] = self._score_default
        self._my_map['gradingAgentId'] = ''
        self._my_map['gradebookColumnId'] = str(kwargs['gradebook_column_id'])
        self._my_map['gradebookId'] = str(kwargs['gradebook_id'])
        self._my_map['derived'] = False
        self._my_map['timeGraded'] = None
        self._my_map['overriddenCalculatedEntryId'] = '' # This will soon do something different
"""

    set_grade = """
        if not self._grade_system.is_based_on_grades():
            raise errors.InvalidArgument()
        if self.get_grade_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_id(grade_id):
            raise errors.InvalidArgument()
        self._my_map['gradeId'] = str(grade_id)
        self._my_map['gradingAgentId'] = str(self._effective_agent_id)
        self._my_map['timeGraded'] = now_map"""

    clear_grade = """
        if not self._grade_system.is_based_on_grades():
            return # do nothing, spec does not raise error
        if (self.get_grade_metadata().is_read_only() or
                self.get_grade_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['gradeId'] = self._grade_default
        self._my_map['gradingAgentId'] = ''
        self._my_map['timeGraded'] = None"""

    set_score = """
        if self._grade_system.is_based_on_grades():
            raise errors.InvalidArgument()
        if self.get_score_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_decimal(score, self.get_score_metadata()):
            raise errors.InvalidArgument()
        if (self._grade_system.get_numeric_score_increment() and 
                score % self._grade_system.get_numeric_score_increment() != 0):
            raise errors.InvalidArgument('score must be in increments of ' + str(self._score_increment))
        self._my_map['score'] = score
        self._my_map['gradingAgentId'] = str(self._effective_agent_id)
        self._my_map['timeGraded'] = now_map"""

    clear_score = """
        if self._grade_system.is_based_on_grades():
            return # do nothing, spec does not raise error
        if (self.get_score_metadata().is_read_only() or
                self.get_score_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['score'] = score_default
        self._my_map['gradingAgentId'] = ''
        self._my_map['timeGraded'] = None"""

class GradebookColumnLookupSession:

    supports_summary = """
        # Not yet:
        return False"""

    get_gradebook_column_summary = """
        raise errors.Unimplemented()"""