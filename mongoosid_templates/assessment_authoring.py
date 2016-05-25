
class AssessmentPartLookupSession:
    
    additional_methods = """
    @utilities.arguments_not_none
    def get_assessment_parts_for_assessment_part(self, assessment_part_id):
        \"\"\"Gets an ``AssessmentPart`` for the given assessment part.

        arg:    assessment_part_id (osid.id.Id): an assessment part ``Id``
        return: (osid.assessment.authoring.AssessmentPartList) - the
                returned ``AssessmentPart`` list
        raise:  NullArgument - ``assessment_part_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  PermissionDenied - authorization failure
        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        # NOT IN SPEC - Implemented from
        # osid.assessment_authoring.AssessmentPartLookupSession.additional_methods
        # NOTE: This implementation currently ignores plenary view
        collection = MongoClientValidated('assessment_authoring',
                                          collection='AssessmentPart',
                                          runtime=self._runtime)
        result = collection.find(
            dict({'assessmentPartId': str(assessment_part_id)},
                 **self._view_filter()))
        return objects.AssessmentPartList(result, runtime=self._runtime)"""

class AssessmentPartAdminSession:
    import_statements = [
        'from . import objects',
        'from dlkit.abstract_osid.osid import errors',
        'from ...abstract_osid.assessment_authoring.objects import AssessmentPartForm as ABCAssessmentPartForm',
        'from ...abstract_osid.id.primitives import Id as ABCId',
        'DESCENDING = -1',
        'ASCENDING = 1',
        'CREATED = True',
        'UPDATED = True',
        'ACTIVE = 0',
        'ANY_STATUS = 1',
        'SEQUESTERED = 0',
        'UNSEQUESTERED = 1',
    ]

    get_assessment_part_form_for_create_for_assessment_part = """
        if not isinstance(assessment_part_id, ABCId):
            raise errors.InvalidArgument('argument is not a valid OSID Id')
        for arg in assessment_part_record_types:
            if not isinstance(arg, ABCType):
                raise errors.InvalidArgument('one or more argument array elements is not a valid OSID Type')
        if assessment_part_record_types == []:
            assessment_part_record_types = None
        mgr = self._get_provider_manager('ASSESSMENT_AUTHORING', local)
        lookup_session = mgr.get_assessment_part_lookup_session_for_bank(self._catalog_id)
        child_parts = lookup_session.get_assessment_parts_for_assessment_part(assessment_part_id)
        mdata = {}
        # Check for underlying Parts, whether Sections and set appropriate mdata overrides:
        if child_parts.available == 0:
            pass
        else:
            mdata['sequestered']['is_read_only'] = True
            mdata['sequestered']['is_required'] = True
            if child_parts.next().is_section():
                mdata['sequestered']['default_boolean_values'] = ['False']
            else:
                mdata['sequestered']['default_boolean_values'] = ['True']
        ## WHY are we passing bank_id = self._catalog_id below, seems redundant:
        obj_form = objects.AssessmentPartForm(
            bank_id=self._catalog_id,
            record_types=assessment_part_record_types,
            assessment_part_id=assessment_part_id,
            catalog_id=self._catalog_id,
            runtime=self._runtime,
            mdata=mdata)
        obj_form._for_update = False
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form"""

    get_assessment_part_form_for_update = """
        collection = MongoClientValidated('assessment_authoring',
                                          collection='AssessmentPart',
                                          runtime=self._runtime)
        if not isinstance(assessment_part_id, ABCId):
            raise errors.InvalidArgument('the argument is not a valid OSID Id')
        if assessment_part_id.get_identifier_namespace() != 'assessment_authoring.AssessmentPart':
            if assessment_part_id.get_authority() != self._authority:
                raise errors.InvalidArgument()
            else:
                assessment_part_id = self._get_assessment_part_id_with_enclosure(assessment_part_id)
        result = collection.find_one({'_id': ObjectId(assessment_part_id.get_identifier())})

        mdata = {}
        if not result['assessmentPartId']:
            pass
        else:
            parent_part_id = Id(result['assessmentPartId'])
            mgr = self._get_provider_manager('ASSESSMENT_AUTHORING', local)
            lookup_session = mgr.get_assessment_part_lookup_session_for_bank(self._catalog_id)
            if lookup_session.get_assessment_parts_for_assessment_part(parent_part_id).available() > 1:
                mdata['sequestered']['is_read_only'] = True
                mdata['sequestered']['is_required'] = True
        obj_form = objects.AssessmentPartForm(result, runtime=self._runtime, mdata=mdata)
        self._forms[obj_form.get_id().get_identifier()] = not UPDATED

        return obj_form
"""

class AssessmentPart:
    
    # Is there a way to template this so that all sub-package objects get a catalog import?
    import_statements = [
        'from ..assessment.objects import Bank'
    ]

    is_section = """
        return not self.is_sequestered()"""
    
    additional_methods = """
    def are_items_sequential(self):
        \"\"\"This can be overwridden by a record extension\"\"\"
        return True

    def are_items_shuffled(self):
        \"\"\"This can be overwridden by a record extension\"\"\"
        return False"""


class AssessmentPartForm:
    init = """
    _record_type_data_sets = {}
    _namespace = 'assessment_authoring.AssessmentPart'

    def __init__(self, osid_object_map=None, record_types=None, runtime=None, **kwargs):
        self._record_type_data_sets = get_registry('ASSESSMENT_PART_RECORD_TYPES', runtime)
        osid_objects.OsidContainableForm.__init__(self)
        osid_objects.OsidOperableForm.__init__(self)
        osid_objects.OsidObjectForm.__init__(
            self, osid_object_map=osid_object_map, record_types=record_types, runtime=runtime, **kwargs)
        self._mdata = dict(default_mdata.ASSESSMENT_PART)
        self._init_metadata(**kwargs)
        if not self.is_for_update():
            self._init_map(record_types, **kwargs)

    def _init_metadata(self, **kwargs):
        \"\"\"Initialize form metadata\"\"\"
        osid_objects.OsidContainableForm._init_metadata(self)
        osid_objects.OsidOperableForm._init_metadata(self)
        osid_objects.OsidObjectForm._init_metadata(self, **kwargs)
        if 'assessmentPartId' not in kwargs:
            # Only "Section" Parts are allowed directly under Assessments
            self._mdata['sequestered']['is_read_only'] = True
            self._mdata['sequestered']['is_required'] = True
            self._mdata['sequestered']['default_boolean_values'] = ['False']
        self._assessment_part_default = self._mdata['assessment_part']['default_id_values'][0]
        self._assessment_default = self._mdata['assessment']['default_id_values'][0]
        self._weight_default = self._mdata['weight']['default_integer_values'][0]
        self._allocated_time_default = self._mdata['allocated_time']['default_duration_values'][0]
        self._items_sequential_default = None
        self._items_shuffled_default = None

    def _init_map(self, record_types, **kwargs):
        \"\"\"Initialize form map\"\"\"
        osid_objects.OsidContainableForm._init_map(self)
        osid_objects.OsidOperableForm._init_map(self)
        osid_objects.OsidObjectForm._init_map(self, record_types=record_types)
        if 'assessment_part_id' in kwargs:
            self._my_map['assessmentPartId'] = str(kwargs['assessment_part_id'])
        else:
            self._my_map['assessmentPartId'] = self._assessment_part_default
            self._my_map['sequestered'] = False # Parts under Assessments must be "Sections"
        if 'assessment_id' in kwargs:
            self._my_map['assessmentId'] = str(kwargs['assessment_id'])
        else:
            self._my_map['assessmentId'] = self._assessment_default
        self._my_map['assignedBankIds'] = [str(kwargs['bank_id'])]
        self._my_map['allocatedTime'] = self._allocated_time_default
        self._my_map['itemsSequential'] = self._items_sequential_default
        self._my_map['itemsShuffled'] = self._items_shuffled_default"""

    # Need to add metadata as well
    additional_methods = """
        def set_items_sequential(self, sequential):
            self._my_map['itemsSequential'] = sequential

        def set_items_sequential(self, shuffled):
            self._my_map['itemsShuffled'] = shuffled"""
