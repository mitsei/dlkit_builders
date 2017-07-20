
class GradeEntryAdminSession:

    import_statements = [
        'from dlkit.abstract_osid.id.primitives import Id as ABCId',
        'from dlkit.abstract_osid.type.primitives import Type as ABCType'
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
            # WHY are we passing gradebook_id = self._catalog_id below, seems redundant:
            # Probably don't need effective agent id since form can now get that from proxy.
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
        collection = JSONClientValidated('grading',
                                         collection='GradeEntry',
                                         runtime=self._runtime)
        if not isinstance(grade_entry_id, ABCId):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        if (grade_entry_id.get_identifier_namespace() != 'grading.GradeEntry' or
                grade_entry_id.get_authority() != self._authority):
            raise errors.InvalidArgument()
        result = collection.find_one({'_id': ObjectId(grade_entry_id.get_identifier())})

        obj_form = objects.GradeEntryForm(
            osid_object_map=result,
            effective_agent_id=str(self.get_effective_agent_id()),
            runtime=self._runtime,
            proxy=self._proxy)
        self._forms[obj_form.get_id().get_identifier()] = not UPDATED

        return obj_form"""


class GradeSystem:
    import_statements_pattern = [
        'from decimal import Decimal',
    ]

    # get_lowest_numeric_score_template = """
    #     # Implemented from template for osid.grading.GradeSystem.get_lowest_numeric_score_template
    #     if self._my_map['${var_name_mixed}'] is None:
    #         return None
    #     else:
    #         return Decimal(str(self._my_map['${var_name_mixed}']))"""

    # But the real implementations need to check is_based_on_grades():
    # So overwrite the templated version
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


class GradeEntry:

    import_statements = [
        'from dlkit.primordium.id.primitives import Id',
        'from ..resource.simple_agent import Agent',
    ]

    get_key_resource_id = """
        return Id(self._my_map['resourceId'])"""

    get_key_resource = """
        return Agent(self.get_key_resource_id())"""

    get_time_graded = """
        if not self.is_graded() or self.is_derived():
            raise errors.IllegalState()
        time_graded = self._my_map['timeGraded']
        return DateTime(
            year=time_graded.year,
            month=time_graded.month,
            day=time_graded.day,
            hour=time_graded.hour,
            minute=time_graded.minute,
            second=time_graded.second,
            microsecond=time_graded.microsecond)"""

    is_graded = """
        return bool(self._my_map['gradeId'] != '' or self._my_map['score'] is not None)"""

    get_grading_agent_id = """
        if not self.is_graded or self.is_derived():
            raise errors.IllegalState()
        return Id(self._my_map['gradingAgentId'])"""

    get_grading_agent = """
        return Agent(self.get_grading_agent_id())"""

    overrides_calculated_entry = """
        return bool(self._my_map['overriddenCalculatedEntryId'])"""

    get_overridden_calculated_entry_id = """
        if not self.overrides_calculated_entry():
            raise errors.IllegalState()
        return self._my_map['overriddenCalculatedEntryId']"""

    get_grade = """
        grade_system = self.get_gradebook_column().get_grade_system()

        for grade in grade_system.get_grades():
            if str(grade.ident) == self._my_map['gradeId']:
                return grade
        raise errors.IllegalState('gradeId does not exist in this GradeSystem')"""


class GradeEntryForm:

    import_statements = [
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.calendaring.primitives import DateTime',
        'from ..utilities import now_map',
        'from decimal import Decimal'
    ]

    init = """
    _namespace = 'grading.GradeEntry'

    def __init__(self, **kwargs):
        osid_objects.OsidRelationshipForm.__init__(self, object_name='GRADE_ENTRY', **kwargs)
        self._mdata = default_mdata.get_grade_entry_mdata()
        self._effective_agent_id = kwargs['effective_agent_id']

        mgr = self._get_provider_manager('GRADING')  # What about the Proxy?
        lookup_session = mgr.get_gradebook_column_lookup_session(proxy=getattr(self, "_proxy", None))
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
        self._grade_default = list(self._mdata['grade']['default_id_values'])[0]
        self._ignored_for_calculations_default = list(self._mdata['ignored_for_calculations']['default_boolean_values'])[0]
        self._score_default = list(self._mdata['score']['default_decimal_values'])[0]

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
        self._my_map['derived'] = False  # This is probably not persisted data
        self._my_map['timeGraded'] = None
        self._my_map['overriddenCalculatedEntryId'] = ''  # This will soon do something different
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
        self._my_map['timeGraded'] = DateTime.utcnow()"""

    clear_grade = """
        if not self._grade_system.is_based_on_grades():
            return  # do nothing, spec does not raise error
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
        self._my_map['timeGraded'] = DateTime.utcnow()"""

    clear_score = """
        if self._grade_system.is_based_on_grades():
            return  # do nothing, spec does not raise error
        if (self.get_score_metadata().is_read_only() or
                self.get_score_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['score'] = self._score_default
        self._my_map['gradingAgentId'] = ''
        self._my_map['timeGraded'] = None"""


class GradeEntryQuery:
    match_gradebook_column_id = """
        self._add_match('gradebookColumnId',
                        str(gradebook_column_id),
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
                                      runtime=self._runtime,
                                      proxy=self._proxy)"""


class GradebookColumnAdminSession:

    additional_methods = """
    def _has_entries(self, gradebook_column_id):
        grading_manager = self._get_provider_manager('GRADING')
        gels = grading_manager.get_grade_entry_lookup_session(proxy=getattr(self, "_proxy", None))
        gels.use_federated_gradebook_view()
        entries = gels.get_grade_entries_for_gradebook_column(gradebook_column_id)
        return entries.available() > 0"""

    delete_gradebook_column = """
        if not isinstance(gradebook_column_id, ABCId):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')

        # check that no entries already exist for this gradebook column
        grading_manager = self._get_provider_manager('GRADING')
        gels = grading_manager.get_grade_entry_lookup_session(proxy=getattr(self, "_proxy", None))
        gels.use_federated_gradebook_view()
        entries = gels.get_grade_entries_for_gradebook_column(gradebook_column_id)
        if self._has_entries(gradebook_column_id):
            raise errors.IllegalState('Entries exist in this gradebook column. Cannot delete it.')

        collection = JSONClientValidated('grading',
                                         collection='GradebookColumn',
                                         runtime=self._runtime)

        gradebook_column_map = collection.find_one({'_id': ObjectId(gradebook_column_id.get_identifier())})

        objects.GradebookColumn(osid_object_map=gradebook_column_map,
                                runtime=self._runtime,
                                proxy=self._proxy)._delete()
        collection.delete_one({'_id': ObjectId(gradebook_column_id.get_identifier())})
        """

    update_gradebook_column = """
        collection = JSONClientValidated('grading',
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
            osid_object_map=gradebook_column_form._my_map,
            runtime=self._runtime,
            proxy=self._proxy)
        """


class GradebookColumnQuery:

    match_grade_system_id = """
        self._add_match('gradeSystemId', str(grade_system_id), bool(match))
    """


class GradeSystemAdminSession:

    additional_methods = """
    def _has_columns(self, grade_system_id):
        grading_manager = self._get_provider_manager('GRADING')
        gcqs = grading_manager.get_gradebook_column_query_session(proxy=self._proxy)
        gcqs.use_federated_gradebook_view()
        querier = gcqs.get_gradebook_column_query()
        querier.match_grade_system_id(grade_system_id, match=True)
        columns = gcqs.get_gradebook_columns_by_query(querier)
        return columns.available() > 0"""

    delete_grade_system = """
        collection = JSONClientValidated('grading',
                                         collection='GradeSystem',
                                         runtime=self._runtime)
        if not isinstance(grade_system_id, ABCId):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        grade_system_map = collection.find_one({'_id': ObjectId(grade_system_id.get_identifier())})

        # check if has columns first
        if self._has_columns(grade_system_id):
            raise errors.InvalidArgument('Grade system being used by gradebook columns. ' +
                                         'Cannot delete it.')

        objects.GradeSystem(osid_object_map=grade_system_map,
                            runtime=self._runtime,
                            proxy=self._proxy)._delete()
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

    def __init__(self, **kwargs):
        osid_objects.OsidObject.__init__(self, object_name='GRADEBOOK_COLUMN_SUMMARY', **kwargs)
        self._catalog_name = 'gradebook'

        # Not set the entries to be included in the calculation
        self._entries = self._get_entries_for_calculation()
        self._entry_scores = self._get_entry_scores()

    def _get_entries_for_calculation(self):
        \"\"\"Ignores entries flagged with ignoreForCalculation\"\"\"
        mgr = self._get_provider_manager('Grading')  # what about the Proxy?
        if not mgr.supports_gradebook_column_lookup():
            raise errors.OperationFailed('Grading does not support GradebookColumn lookup')
        gradebook_id = Id(self._my_map['assignedGradebookIds'][0])
        lookup_session = mgr.get_grade_entry_lookup_session_for_gradebook(gradebook_id,
                                                                          proxy=getattr(self, "_proxy", None))
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


class GradebookColumnSummaryQuery:
    init = """
    def __init__(self, runtime):
        self._namespace = 'grading.GradebookColumnSummaryQuery'
        self._runtime = runtime
        record_type_data_sets = get_registry('GRADEBOOK_COLUMN_SUMMARY_QUERY_RECORD_TYPES', runtime)
        self._all_supported_record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_ids = []
        for data_set in record_type_data_sets:
            self._all_supported_record_type_ids.append(str(Id(**record_type_data_sets[data_set])))
        osid_queries.OsidRuleQuery.__init__(self, runtime)"""
