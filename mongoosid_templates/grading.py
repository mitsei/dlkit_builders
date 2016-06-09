
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
            ## Probably don't need effective agent id since form can now get that from proxy.
            obj_form = objects.GradeEntryForm(
                gradebook_id=self._catalog_id,
                gradebook_column_id=gradebook_column_id,
                resource_id=resource_id,
                effective_agent_id=str(self.get_effective_agent_id()),
                catalog_id=self._catalog_id,
                runtime=self._runtime,
                proxy=self._proxy)
        else:
            obj_form = objects.GradeEntryForm(
                gradebook_id=self._catalog_id,
                record_types=grade_entry_record_types,
                gradebook_column_id=gradebook_column_id,
                resource_id=resource_id,
                effective_agent_id=str(self.get_effective_agent_id()),
                catalog_id=self._catalog_id,
                runtime=self._runtime,
                proxy=self._proxy)
        obj_form._for_update = False
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form"""

    get_grade_entry_form_for_update = """
        collection = MongoClientValidated('grading',
                                          collection='GradeEntry',
                                          runtime=self._runtime)
        if not isinstance(grade_entry_id, ABCId):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        if grade_entry_id.get_identifier_namespace() != 'grading.GradeEntry':
            if grade_entry_id.get_authority() != self._authority:
                raise errors.InvalidArgument()
            else:
                grade_entry_id = self._get_grade_entry_id_with_enclosure(grade_entry_id)
        result = collection.find_one({'_id': ObjectId(grade_entry_id.get_identifier())})

        obj_form = objects.GradeEntryForm(
            osid_object_map=result,
            effective_agent_id=str(self.get_effective_agent_id()),
            runtime=self._runtime,
            proxy=self._proxy)
        self._forms[obj_form.get_id().get_identifier()] = not UPDATED

        return obj_form"""


class GradeSystem:
    import_statements = [
        'from decimal import Decimal',
    ]

    get_lowest_numeric_score_template = """
        # Implemented from template for osid.grading.GradeSystem.get_lowest_numeric_score_template
        if self._my_map['${var_name_mixed}'] is None:
            return None
        else:
            return Decimal(str(self._my_map['${var_name_mixed}']))"""

    # But the real implementations need to check is_based_on_grades():

    get_lowest_numeric_score = """
        if self.is_based_on_grades():
            raise errors.IllegalState('This GradeSystem is based on grades')
        if self._my_map['lowestNumericScore'] is None:
            return None
        else:
            return Decimal(str(self._my_map['lowestNumericScore']))"""

    get_highest_numeric_score = """
        if self.is_based_on_grades():
            raise errors.IllegalState('This GradeSystem is based on grades')
        if self._my_map['highestNumericScore'] is None:
            return None
        else:
            return Decimal(str(self._my_map['highestNumericScore']))"""

    get_numeric_score_increment = """
        if self.is_based_on_grades():
            raise errors.IllegalState('This GradeSystem is based on grades')
        if self._my_map['numericScoreIncrement'] is None:
            return None
        else:
            return Decimal(str(self._my_map['numericScoreIncrement']))"""

    additional_methods = """
    def get_object_map(self):
        obj_map = dict(self._my_map)
        obj_map['grades'] = []
        for grade in self.get_grades():
            obj_map['grades'].append(grade.get_object_map())
        return osid_objects.OsidObject.get_object_map(self, obj_map)

    object_map = property(fget=get_object_map)"""


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
        self._my_map['${var_name_mixed}'] = self._${var_name}_default"""

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
        return bool(self._my_map['gradeId'] is not None or self._my_map['score'] is not None)"""

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
        'from ..utilities import now_map',
        'from decimal import Decimal'
    ]

    init = """
    _record_type_data_sets = {}
    _namespace = 'grading.GradeEntry'

    def __init__(self, **kwargs):
        self._record_type_data_sets = get_registry('GRADE_ENTRY_RECORD_TYPES', kwargs['runtime'])
        osid_objects.OsidRelationshipForm.__init__(self, **kwargs)
        self._mdata = dict(default_mdata.GRADE_ENTRY)
        self._effective_agent_id = kwargs['effective_agent_id']
        mgr = self._get_provider_manager('GRADING')
        lookup_session = mgr.get_gradebook_column_lookup_session()
        lookup_session.use_federated_gradebook_view()
        if 'gradebook_column_id' in kwargs:
            gradebook_column = lookup_session.get_gradebook_column(kwargs['gradebook_column_id'])
        elif 'osid_object_map' in kwargs and kwargs['osid_object_map'] is not None:
            gradebook_column = lookup_session.get_gradebook_column(Id(kwargs['osid_object_map']['gradebookColumnId']))
        else:
            raise errors.NullArgument('gradebook_column_id required for create forms.')
        self._grade_system = gradebook_column.get_grade_system()
        self._init_metadata(**kwargs)

        if not self.is_for_update():
            self._init_map(**kwargs)

    def _init_metadata(self, **kwargs):
        osid_objects.OsidRelationshipForm._init_metadata(self, **kwargs)
        if self._grade_system.is_based_on_grades():
            self._mdata['score'].update(
                {'minimum_decimal': None,
                 'maximum_decimal': None})
            allowable_grades = self._grade_system.get_grades()
            allowable_grade_ids = [g.ident for g in allowable_grades]
            self._mdata['grade']['id_set'] = allowable_grade_ids
        else:
            self._mdata['score'].update(
                {'minimum_decimal': self._grade_system.get_lowest_numeric_score(),
                 'maximum_decimal': self._grade_system.get_highest_numeric_score()})
        self._grade_default = self._mdata['grade']['default_id_values'][0]
        self._ignored_for_calculations_default = self._mdata['ignored_for_calculations']['default_boolean_values'][0]
        self._score_default = self._mdata['score']['default_decimal_values'][0]


    def _init_map(self, record_types=None, **kwargs):
        osid_objects.OsidRelationshipForm._init_map(self, record_types=record_types)
        self._my_map['resourceId'] = str(kwargs['resource_id'])
        self._my_map['gradeId'] = self._grade_default
        self._my_map['agentId'] = str(kwargs['effective_agent_id'])
        self._my_map['ignoredForCalculations'] = self._ignored_for_calculations_default
        self._my_map['score'] = self._score_default
        self._my_map['gradingAgentId'] = ''
        self._my_map['gradebookColumnId'] = str(kwargs['gradebook_column_id'])
        self._my_map['assignedGradebookIds'] = [str(kwargs['gradebook_id'])]
        self._my_map['derived'] = False # This is probably not persisted data
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
        if not self._is_in_set(grade_id, self.get_grade_metadata()):
            raise errors.InvalidArgument('Grade ID not in the acceptable set.')
        self._my_map['gradeId'] = str(grade_id)
        self._my_map['gradingAgentId'] = str(self._effective_agent_id)
        self._my_map['timeGraded'] = now_map()"""

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
        if not isinstance(score, Decimal):
            score = Decimal(str(score))
        if (self._grade_system.get_numeric_score_increment() and 
                score % self._grade_system.get_numeric_score_increment() != 0):
            raise errors.InvalidArgument('score must be in increments of ' + str(self._score_increment))
        self._my_map['score'] = float(score)
        self._my_map['gradingAgentId'] = str(self._effective_agent_id)
        self._my_map['timeGraded'] = now_map()"""

    clear_score = """
        if self._grade_system.is_based_on_grades():
            return # do nothing, spec does not raise error
        if (self.get_score_metadata().is_read_only() or
                self.get_score_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['score'] = self._score_default
        self._my_map['gradingAgentId'] = ''
        self._my_map['timeGraded'] = None"""

class GradeEntryQuery:
    match_gradebook_column_id = """
        self._add_match('gradebookColumnId',
                        gradebook_column_id,
                        match)
    """

class GradebookColumnLookupSession:
    import_statements = [
        'from .objects import GradebookColumnSummary',
    ]

    supports_summary = """
        # Not yet:
        return False"""

    get_gradebook_column_summary = """
        gradebook_column = self.get_gradebook_column(gradebook_column_id)
        summary_map = gradebook_column._my_map
        summary_map['gradebookColumnId'] = str(gradebook_column.ident)
        return GradebookColumnSummary(osid_object_map=summary_map,
                                      runtime=self._runtime)"""

class GradebookColumnAdminSession:

    additional_methods = """
    def _has_entries(self, gradebook_column_id):
        grading_manager = self._get_provider_manager('GRADING')
        gels = grading_manager.get_grade_entry_lookup_session()
        gels.use_federated_gradebook_view()
        entries = gels.get_grade_entries_for_gradebook_column(gradebook_column_id)
        return entries.available() > 0
        """

    delete_gradebook_column = """
        if not isinstance(gradebook_column_id, ABCId):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')

        # check that no entries already exist for this gradebook column
        grading_manager = self._get_provider_manager('GRADING')
        gels = grading_manager.get_grade_entry_lookup_session()
        gels.use_federated_gradebook_view()
        entries = gels.get_grade_entries_for_gradebook_column(gradebook_column_id)
        if self._has_entries(gradebook_column_id):
            raise errors.IllegalState('Entries exist in this gradebook column. Cannot delete it.')

        collection = MongoClientValidated('grading',
                                          collection='GradebookColumn',
                                          runtime=self._runtime)

        gradebook_column_map = collection.find_one({'_id': ObjectId(gradebook_column_id.get_identifier())})

        objects.GradebookColumn(gradebook_column_map, runtime=self._runtime)._delete()
        collection.delete_one({'_id': ObjectId(gradebook_column_id.get_identifier())})
        """

    update_gradebook_column = """
        collection = MongoClientValidated('grading',
                                          collection='GradebookColumn',
                                          runtime=self._runtime)
        if not isinstance(gradebook_column_form, ABCGradebookColumnForm):
            raise errors.InvalidArgument('argument type is not an GradebookColumnForm')
        if not gradebook_column_form.is_for_update():
            raise errors.InvalidArgument('the GradebookColumnForm is for update only, not create')
        try:
            if self._forms[gradebook_column_form.get_id().get_identifier()] == UPDATED:
                raise errors.IllegalState('gradebook_column_form already used in an update transaction')
        except KeyError:
            raise errors.Unsupported('gradebook_column_form did not originate from this session')
        if not gradebook_column_form.is_valid():
            raise errors.InvalidArgument('one or more of the form elements is invalid')

        # check that there are no entries, if updating the gradeSystemId
        old_column = collection.find_one({"_id": gradebook_column_form._my_map['_id']})
        if old_column['gradeSystemId'] != gradebook_column_form._my_map['gradeSystemId']:
            if self._has_entries(gradebook_column_form.id_):
                raise errors.IllegalState('Entries exist in this gradebook column. ' +
                                          'Cannot change the grade system.')

        collection.save(gradebook_column_form._my_map)

        self._forms[gradebook_column_form.get_id().get_identifier()] = UPDATED

        # Note: this is out of spec. The OSIDs don't require an object to be returned:
        return objects.GradebookColumn(
            gradebook_column_form._my_map,
            runtime=self._runtime)
        """

class GradebookColumnQuery:

    match_grade_system_id = """
        self._add_match('gradeSystemId', str(grade_system_id), bool(match))
    """

class GradeSystemAdminSession:

    additional_methods = """
    def _has_columns(self, grade_system_id):
        grading_manager = self._get_provider_manager('GRADING')
        gcqs = grading_manager.get_gradebook_column_query_session()
        gcqs.use_federated_gradebook_view()
        querier = gcqs.get_gradebook_column_query()
        querier.match_grade_system_id(grade_system_id, match=True)
        columns = gcqs.get_gradebook_columns_by_query(querier)
        return columns.available() > 0
        """

    delete_grade_system = """
        collection = MongoClientValidated('grading',
                                          collection='GradeSystem',
                                          runtime=self._runtime)
        if not isinstance(grade_system_id, ABCId):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        grade_system_map = collection.find_one({'_id': ObjectId(grade_system_id.get_identifier())})

        # check if has columns first
        if self._has_columns(grade_system_id):
            raise errors.InvalidArgument('Grade system being used by gradebook columns. ' +
                                         'Cannot delete it.')

        objects.GradeSystem(grade_system_map, runtime=self._runtime)._delete()
        collection.delete_one({'_id': ObjectId(grade_system_id.get_identifier())})
        """


class GradebookColumnSummary:
    import_statements = [
        'import numpy as np',
    ]

    # Note: self._catalog_name = 'Gradebook below is currently 
    # only for osid.OsidObject.get_object_map() setting the now deprecated
    # gradebookId element and may be removed someday
    init = """
    _record_type_data_sets = {}
    _namespace = 'grading.GradebookColumnSummary'

    def __init__(self, osid_object_map, runtime=None):
        self._record_type_data_sets = get_registry('GRADEBOOK_COLUMN_SUMMARY_RECORD_TYPES', runtime)
        osid_objects.OsidObject.__init__(self, osid_object_map, runtime)
        self._records = dict()
        self._load_records(osid_object_map['recordTypeIds'])
        self._catalog_name = 'Gradebook'

        # Not set the entries to be included in the calculation
        self._entries = self._get_entries_for_calculation()
        self._entry_scores = self._get_entry_scores()

    def _get_entries_for_calculation(self):
        \"\"\"Ignores entries flagged with ignoreForCalculation\"\"\"
        mgr = self._get_provider_manager('Grading')
        if not mgr.supports_gradebook_column_lookup():
            raise errors.OperationFailed('Grading does not support GradebookColumn lookup')
        gradebook_id = Id(self._my_map['assignedGradebookIds'][0])
        lookup_session = mgr.get_grade_entry_lookup_session_for_gradebook(gradebook_id)
        entries = lookup_session.get_grade_entries_for_gradebook_column(self.get_gradebook_column_id())
        return [e for e in entries if not e.is_ignored_for_calculations()]

    def _get_entry_scores(self):
        \"\"\"Takes entries from self._entries and returns a list of scores (or
        output scores, if based on grades)\"\"\"
        if self.get_gradebook_column().get_grade_system().is_based_on_grades():
            return [e.get_grade().get_output_score() for e in self._entries if e.is_graded()]
        else:
            return [e.get_score() for e in self._entries if e.is_graded()]"""

    get_mean = """
        return np.mean(self._entry_scores)"""

    get_median = """
        return np.median(self._entry_scores)"""

    get_mode = """
        # http://stackoverflow.com/questions/10797819/finding-the-mode-of-a-list-in-python
        return max(set(self._entry_scores), key=self._entry_scores.count)"""

    get_rms = """
        return np.sqrt(np.mean(np.square(self._entry_scores)))"""

    get_standard_deviation = """
        return np.std(self._entry_scores)"""

    get_sum = """
        return sum(self._entry_scores)"""
