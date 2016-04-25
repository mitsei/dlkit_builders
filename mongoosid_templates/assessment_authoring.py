class AssessmentPart:
    import_statements = [
        'from ..assessment.objects import Bank'
    ]


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

class AssessmentPart:
    
    additional_methods = """
    def are_items_sequential()
        \"\"\"This can be overwridden by a record extension\"\"\"
        return True

    def are_items_shuffled()
        \"\"\"This can be overwridden by a record extension\"\"\"
        return False"""


class AssessmentPartForm:
    init = """
    _record_type_data_sets = {}
    _namespace = 'assessment_authoring.AssessmentPart'

    def __init__(self, osid_object_map=None, record_types=None, runtime=None, **kwargs):
        osid_objects.OsidForm.__init__(self, runtime=runtime)
        self._record_type_data_sets = self._get_registry('ASSESSMENT_PART_RECORD_TYPES')
        self._kwargs = kwargs
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
        osid_objects.OsidObjectForm._init_metadata(self, **kwargs)
        osid_objects.OsidContainableForm._init_metadata(self)

        self._assessment_part_metadata = {
            'element_id': Id(
                self._authority,
                self._namespace,
                'assessment_part')}
        self._assessment_part_metadata.update(mdata_conf.ASSESSMENT_PART_ASSESSMENT_PART)
        self._assessment_metadata = {
            'element_id': Id(
                self._authority,
                self._namespace,
                'assessment')}
        self._assessment_metadata.update(mdata_conf.ASSESSMENT_PART_ASSESSMENT)
        self._weight_metadata = {
            'element_id': Id(
                self._authority,
                self._namespace,
                'weight')}
        self._weight_metadata.update(mdata_conf.ASSESSMENT_PART_WEIGHT)
        self._allocated_time_metadata = {
            'element_id': Id(
                self._authority,
                self._namespace,
                'allocated_time')}
        self._allocated_time_metadata.update(mdata_conf.ASSESSMENT_PART_ALLOCATED_TIME)
        self._assessment_part_default = self._assessment_part_metadata['default_id_values'][0]
        self._assessment_default = self._assessment_metadata['default_id_values'][0]
        self._allocated_time_default = self._allocated_time_metadata['default_duration_values'][0]
        self._items_sequential_default = None
        self._items_shuffled_default = None

    def _init_map(self, **kwargs):
        osid_objects.OsidObjectForm._init_map(self)
        osid_objects.OsidContainableForm._init_map(self)

        if 'assessment_part_id' in kwargs:
            self._my_map['assessmentPartId'] = str(kwargs['assessment_part_id'])
        else:
            self._my_map['assessmentPartId'] = self._assessment_part_default
        if 'assessment_id' in kwargs:
            self._my_map['assessmentId'] = str(kwargs['assessment_id'])
        else:
            self._my_map['assessmentId'] = self._assessment_default
        self._my_map['assignedBankIds'] = [str(kwargs['bank_id'])]
        self._my_map['allocatedTime'] = self._allocated_time_default
        self._my_map[itemsSequential'] = self._items_sequential_default
        self._my_map[itemsShuffled'] = self._items_shuffled_default"""

    # Need to add metadata as well
    additional_methods = """
        def set_items_sequential(self, sequential):
            self._my_map['itemsSequential'] = sequential

        def set_items_sequential(self, shuffled):
            self._my_map['itemsShuffled'] = shuffled"""