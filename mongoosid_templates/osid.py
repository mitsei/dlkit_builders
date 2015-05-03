
class OsidProfile:

    import_statements = [
        'from . import profile',
        'from ..osid.osid_errors import * # pylint: disable=wildcard-import,unused-wildcard-import',
        'from ..primitives import Id',
        'from ..primitives import Type',
    ]

    get_id = """
        return Id(**profile.ID)
        """

    get_display_name = """
        return DisplayText(
            text = profile.DISPLAYNAME,
            language_type=Type(**profile.LANGUAGETYPE),
            script_type=Type(**profile.SCRIPTTYPE),
            format_type=Type(**profile.FORMATTYPE))"""

    get_description = """
        return DisplayText(
            text=profile.DESCRIPTION,
            language_type=Type(**profile.LANGUAGETYPE),
            script_type=Type(**profile.SCRIPTTYPE),
            format_type=Type(**profile.FORMATTYPE))"""

    get_version = """
        ## THIS ALL NEEDS TO BE FIXED:
        #try:
        #    from ..installation.primitives import Version
        #except:
        #    from .common import Version
        #try:
        #    from ..type.primitives import Type
        #except:
        #    from .common import Type
        #return Version(
        #    components=profile.VERSIONCOMPONENTS,
        #    scheme=Type(**profile.VERSIONSCHEME))
        raise Unimplemented()"""

    get_release_date = """
        # NEED TO IMPLEMENT
        raise Unimplemented()"""

    supports_osid_version = """
        ## THIS ALL NEEDS TO BE FIXED:
        #try:
        #    from ..installation.primitives import Version
        #except:
        #    from .common import Version
        #try:
        #    from ..type.primitives import Type
        #except:
        #    from .common import Type
        #return Version(
        #    components=profile.OSIDVERSION,
        #    scheme=Type(**profile.VERSIONSCHEME))
        raise Unimplemented()"""

    get_locales = """
        # NEED TO IMPLEMENT
        raise Unimplemented()"""

    supports_journal_rollback = """
        # Perhaps someday I will support journaling
        return False"""

    supports_journal_branching = """
        # Perhaps someday I will support journaling
        return False"""

    get_branch_id = """
        # Perhaps someday I will support journaling
        raise Unimplemented()"""

    get_branch = """
        # Perhaps someday I will support journaling
        raise Unimplemented()"""

    get_proxy_record_types = """
        # NEED TO IMPLEMENT
        raise Unimplemented()"""

    supports_proxy_record_type = """
        # NEED TO IMPLEMENT
        raise Unimplemented()"""

class OsidManager:

    import_statements = [
        'from ..osid.osid_errors import * # pylint: disable=wildcard-import,unused-wildcard-import',
        'from ..primitives import DisplayText',
    ]  

    init = """
    def __init__(self):
        self._runtime = None
        self._config = None
"""
    
    initialize = """
        if runtime is None:
            raise NullArgument()
        if self._runtime is not None:
            raise IllegalState('this manager has already been initialized.')
        self._runtime = runtime
        self._config = runtime.get_configuration()"""

class OsidProxyManager:

    import_statements = [
        'from ..osid.osid_errors import * # pylint: disable=wildcard-import,unused-wildcard-import',
    ]  

    init = """
    def __init__(self):
        self._runtime = None
        self._config = None
"""
    
    initialize = """
        if runtime is None:
            raise NullArgument()
        if self._runtime is not None:
            raise IllegalState('this manager has already been initialized.')
        self._runtime = runtime
        self._config = runtime.get_configuration()"""


class OsidRuntimeManager:

    import_statements = [
        'from ..osid.osid_errors import * # pylint: disable=wildcard-import,unused-wildcard-import',
    ]  

    init = """
    def __init__(self, configuration_key = None):
        self._configuration_key = configuration_key"""


class Identifiable:

    import_statements = [
        'from ..primitives import *'
    ]  

    init = """
    import socket
    if 'macbook' in socket.gethostname().lower():
        _authority = socket.gethostname().lower().split('.')[0]
    else:
        _authority = socket.gethostname()
"""

    get_id = """
        return Id(
            identifier=str(self._my_map['_id']),
            namespace=self._namespace,
            authority=self._authority)"""

    is_current = """
        # Osid Objects in this implementation will immediately become stale.
        return False"""


class Extensible:

    init = """
    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith('__'):
                yield attr

    def __getitem__(self, item):
        return getattr(self, item)

    def __getattr__(self, name):
        if '_records' in self.__dict__:
            for record in self._records:
                try:
                    return self._records[record][name]
                except AttributeError:
                    pass
        raise AttributeError(name)

    def _get_record(self, recordType):
        \"\"\"Get the record string type value given the recordType.\"\"\"
        if recordType is None:
            raise NullArgument()
        if not self.has_record_type(recordType):
            raise Unsupported()
        if str(recordType) not in self._records:
            raise Unimplemented()
        return self._records[str(recordType)]

    def _load_records(self, record_type_idstrs):
        \"\"\"Load all records from given record_type_idstrs.\"\"\"
        for record_type_idstr in record_type_idstrs:
            self._init_record(record_type_idstr)

    def _init_record(self, record_type_idstr):
        \"\"\"Initialize the record identified by the record_type_idstr.\"\"\"
        import importlib
        record_type_data = self._record_type_data_sets[Id(record_type_idstr).get_identifier()]
        module = importlib.import_module(record_type_data['module_path'])
        record = getattr(module, record_type_data['object_record_class_name'])
        self._records[record_type_idstr] = record(self)

    def _delete(self):
        \"\"\"Override this method in inheriting objects to perform special clearing operations.\"\"\"
        try: # Need to implement records for catalogs one of these days
            for record in self._records:
                try:
                    self._records[record]._delete()
                except AttributeError:
                    pass
        except AttributeError:
            pass
"""

    has_record_type = """
        return str(record_type) in self._supported_record_type_ids"""

    get_record_types = """
        from ..primitives import Id
        from ..primitives import Type
        from ..type.objects import TypeList
        type_list = []
        for type_idstr in self._supported_record_type_ids:
            type_list.append(Type(**self._record_type_data_sets[Id(type_idstr).get_identifier()]))
        return TypeList(type_list)"""

class Temporal:

    import_statements = [
        'from ..primitives import DateTime',
        'import datetime'
    ]

    is_effective = """
        now = DateTime.now()
        return (self.get_start_date() <= now and self.get_end_date() >= now)"""

    get_start_date = """
        sd = self._my_map['startDate']
        return DateTime(sd['year'], sd['month'], sd['day'], sd['hour'], sd['minute'], sd['second'], sd['microsecond'])"""

    get_end_date = """
        ed = self._my_map['endDate']
        return DateTime(ed['year'], ed['month'], ed['day'], ed['hour'], ed['minute'], ed['second'], ed['microsecond'])"""

class Containable:

    is_sequestered = """
        return self._my_map['sequestered']"""

class Operable:

    is_active = """
        # THIS MAY NOT BE RIGHT. REVIEW LOGIC FROM OSID DOC
        return self.is_operational() and (not self.is_disabled() or self.is_enabled())"""

    is_enabled = """
        # Someday I'll have a real implementation, but for now I just: 
        return False"""

    is_disabled = """
        # Someday I'll have a real implementation, but for now I just:
        return True"""

    is_operational = """
        # Someday I'll have a real implementation, but for now I just:
        return False"""


class OsidSession:

    import_statements = [
        'import socket',
        'from ..primitives import Id',
        'from ..primitives import Type',
        'from ..osid.osid_errors import * # pylint: disable=wildcard-import,unused-wildcard-import',
        'from bson.objectid import ObjectId',
        'from importlib import import_module',
        'from .. import mongo_client',
        'from .. import types',
        '#from . import profile',
        'COMPARATIVE = 0',
        'PLENARY = 1',
        'FEDERATED = 0',
        'ISOLATED = 1',
        'CREATED = True',
        'UPDATED = True'
    ]

    init = """
    if 'macbook' in socket.gethostname().lower():
        _authority = socket.gethostname().lower().split('.')[0]
    else:
        _authority = socket.gethostname()

    def __init__(self):
        self._proxy = None
        self._runtime = None
        self._db_prefix = None
        self._catalog_identifier = None
        self._my_catalog_map = None
        self._catalog_id = None
        self._catalog = None
        self._forms = None

    def _init_catalog(self, proxy=None, runtime=None):
        \"\"\"Initialize this object as an OsidCatalog.\"\"\"
        self._proxy = proxy
        self._runtime = runtime
        if runtime is not None:
            prefix_param_id = Id('parameter:mongoDBNamePrefix@mongo')
            self._db_prefix = runtime.get_configuration().get_value_by_parameter(prefix_param_id).get_string_value()
        else:
            self._db_prefix = ''

    def _init_object(self, catalog_id, proxy, runtime, db_name, cat_name, cat_class):
        \"\"\"Initialize this object as an OsidObject.\"\"\"
        self._catalog_identifier = None
        self._proxy = proxy
        self._runtime = runtime
        if runtime is not None:
            prefix_param_id = Id('parameter:mongoDBNamePrefix@mongo')
            self._db_prefix = runtime.get_configuration().get_value_by_parameter(prefix_param_id).get_string_value()
        else:
            self._db_prefix = ''
        collection = mongo_client[self._db_prefix + db_name][cat_name]
        if catalog_id is not None and catalog_id.get_identifier() != '000000000000000000000000':
            self._catalog_identifier = catalog_id.get_identifier()
            self._my_catalog_map = collection.find_one({'_id': ObjectId(self._catalog_identifier)})
            if self._my_catalog_map is None:
                # Should also check for the authority here:
                if catalog_id.get_identifier_namespace() != db_name + '.' + cat_name:
                    self._my_catalog_map = self._create_orchestrated_cat(catalog_id, db_name, cat_name)
                else:
                    raise NotFound('could not find catalog identifier ' + catalog_id.get_identifier() + cat_name)
        else:
            self._catalog_identifier = '000000000000000000000000'
            self._my_catalog_map = {
                '_id': ObjectId(self._catalog_identifier),
                'displayName': {'text': 'Default ' + cat_name,
                                'languageTypeId': str(Type(**types.Language().get_type_data('DEFAULT'))),
                                'scriptTypeId': str(Type(**types.Script().get_type_data('DEFAULT'))),
                                'formatTypeId': str(Type(**types.Format().get_type_data('DEFAULT'))),},
                'description': {'text': 'The Default ' + cat_name,
                                'languageTypeId': str(Type(**types.Language().get_type_data('DEFAULT'))),
                                'scriptTypeId': str(Type(**types.Script().get_type_data('DEFAULT'))),
                                'formatTypeId': str(Type(**types.Format().get_type_data('DEFAULT'))),},
                'genusType': str(Type(**types.Genus().get_type_data('DEFAULT'))),
                'recordTypeIds': [] # Could this somehow inherit source catalog records?
            }
        self._catalog = cat_class(self._my_catalog_map)
        self._catalog_id = self._catalog.get_id()
        self._forms = dict()
        mongo_client.close()

    def _get_phantom_root_catalog(self, cat_name, cat_class):
        \"\"\"Get's the catalog id corresponding to the root of all implementation catalogs.\"\"\"
        catalog_map = {
            '_id': ObjectId('000000000000000000000000'),
            'displayName': {'text': 'Default ' + cat_name,
                            'languageTypeId': str(Type(**types.Language().get_type_data('DEFAULT'))),
                            'scriptTypeId': str(Type(**types.Script().get_type_data('DEFAULT'))),
                            'formatTypeId': str(Type(**types.Format().get_type_data('DEFAULT'))),},
            'description': {'text': 'The Default ' + cat_name,
                            'languageTypeId': str(Type(**types.Language().get_type_data('DEFAULT'))),
                            'scriptTypeId': str(Type(**types.Script().get_type_data('DEFAULT'))),
                            'formatTypeId': str(Type(**types.Format().get_type_data('DEFAULT'))),},
            'genusType': str(Type(**types.Genus().get_type_data('DEFAULT'))),
            'recordTypeIds': [] # Could this somehow inherit source catalog records?
        }
        return cat_class(catalog_map)

    def _create_orchestrated_cat(self, foreign_catalog_id, db_name, cat_name):
        \"\"\"Creates a catalog in the current service orchestrated with a foreign service Id.\"\"\"
        # Need to test if the catalog_id exists for the foreign catalog
        try:
            foreign_db_name = foreign_catalog_id.get_identifier_namespace().split('.')[0]
            foreign_cat_name = foreign_catalog_id.get_identifier_namespace().split('.')[1]
            collection = mongo_client[self._db_prefix + foreign_db_name][foreign_cat_name]
            if not collection.find_one({'_id': ObjectId(foreign_catalog_id.get_identifier())}):
                mongo_client.close()
                raise NotFound()
        except KeyError:
            mongo_client.close()
            raise NotFound()
        collection = mongo_client[self._db_prefix + db_name][cat_name]
        catalog_map = {
            '_id': ObjectId(foreign_catalog_id.get_identifier()),
            'displayName': {'text': ('Orchestrated ' + foreign_catalog_id.get_identifier_namespace().split('.')[0] + ' ' + cat_name),
                            'languageTypeId': str(Type(**types.Language().get_type_data('DEFAULT'))),
                            'scriptTypeId': str(Type(**types.Script().get_type_data('DEFAULT'))),
                            'formatTypeId': str(Type(**types.Format().get_type_data('DEFAULT'))),},
            'description': {'text': ('Orchestrated ' + cat_name + ' for the ' + foreign_catalog_id.get_identifier_namespace().split('.')[0] + ' service'),
                            'languageTypeId': str(Type(**types.Language().get_type_data('DEFAULT'))),
                            'scriptTypeId': str(Type(**types.Script().get_type_data('DEFAULT'))),
                            'formatTypeId': str(Type(**types.Format().get_type_data('DEFAULT'))),},
            'genusType': str(Type(**types.Genus().get_type_data('DEFAULT'))),
            'recordTypeIds': [] # Could this somehow inherit source catalog records?

        }
        collection.insert(catalog_map)
        mongo_client.close()
        return catalog_map

    def _get_provider_manager(self, osid):
        \"\"\"Gets the most appropriate provider manager depending on config\"\"\"
        try:
            # Try to get the Manager from the runtime, if available:
            config = self._runtime.get_configuration()
            parameter_id = Id('parameter:repositoryProviderImpl@mongo')
            impl_name = config.get_value_by_parameter(parameter_id).get_string_value()
            manager = self._runtime.get_manager(osid, impl_name) # What about ProxyManagers?
        except (AttributeError, KeyError, NotFound):
            # Just return a Manager from this implementation:
            module = import_module('dlkit.mongo.' + osid.lower() + '.managers')
            manager = getattr(module, osid.title() + 'Manager')()
            if self._runtime is not None:
                manager.initialize(self._runtime)
        return manager
"""

    get_locale = """
        #from ..locale.objects import Locale
        ##
        # This implementation could assume that instantiating a new Locale
        # without constructor arguments wlll return the default Locale.
        #return Locale()
        raise Unimplemented()"""  

    is_authenticated = """
        if self._proxy is None:
            return False
        elif self._proxy.has_authentication():
            return self._proxy.get_authentication().is_valid()
        else:
            return False"""

    get_authenticated_agent_id = """
        if self.is_authenticated():
            return self._proxy.get_authentication().get_agent_id()
        else:
            raise IllegalState()"""  

    get_authenticated_agent = """
        if self.is_authenticated():
            return self._proxy.get_authentication().get_agent()
        else:
            raise IllegalState()"""

    get_effective_agent_id = """
        if self.is_authenticated():
            if self._proxy.has_effective_agent():
                return self._proxy.get_effective_agent_id()
            else:
                return self._proxy.get_authentication().get_agent_id()
        else:
            return Id(
                identifier='MC3GUE$T@MIT.EDU',
                namespace='agent.Agent',
                authority='MIT-OEIT')"""

    get_effective_agent = """
        #effective_agent_id = self.get_effective_agent_id()
        # This may want to be extended to get the Agent directly from the Authentication
        # if available and if not effective agent is available in the proxy
        #return Agent(
        #    identifier=effective_agent_id.get_identifier(),
        #    namespace=effective_agent_id.get_namespace(),
        #    authority=effective_agent_id.get_authority())
        raise Unimplemented()"""

    supports_transactions = """
        return False"""

    startTransaction = """
        if not supports_transactions:
            raise Unsupported('transactions ore not supported for this session')"""


class OsidObject:

    import_statements = [
        'from ..primitives import *',
        'from ..osid.osid_errors import *',
        'from .. import types',
        'from importlib import import_module'
        ]

    init = """
    _namespace = 'mongo.OsidObject'

    def __init__(self, osid_object_map, runtime=None):
        self._my_map = osid_object_map
        self._runtime = runtime
    
    def _get_provider_manager(self, osid):
        try:
            # Try to get the Manager from the runtime, if available:
            config = self._runtime.get_configuration()
            parameter_id = Id('parameter:repositoryProviderImpl@mongo')
            impl_name = config.get_value_by_parameter(parameter_id).get_string_value()
            manager = self._runtime.get_manager(osid, impl_name) # What about ProxyManagers?
        except (AttributeError, KeyError, NotFound):
            # Just return a Manager from this implementation:
            module = import_module('dlkit.mongo.' + osid.lower() + '.managers')
            manager = getattr(module, osid.title() + 'Manager')()
            if self._runtime is not None:
                manager.initialize(self._runtime)
        return manager

    def get_object_map(self, obj_map=None):
        if obj_map is None:
            obj_map = dict(self._my_map)
        del obj_map['_id']
        my_idstr = str(self.get_id())

        # The following is crappy. Should be over-ridden in the corresponding
        # object's get_object_map() methods instead:
        if self._namespace == 'repository.Asset':
            obj_map['assetContents'] = []
            obj_map['assetContent'] = [] # This is deprecated, switch to assetContents
            for asset_content in self.get_asset_contents():
                obj_map['assetContents'].append(asset_content.get_object_map())
                obj_map['assetContent'].append(asset_content.get_object_map())
        if self._namespace == 'repository.AssetContent':
            if 'dbPrefix' in obj_map:
                del obj_map['dbPrefix']
        if self._namespace == 'assessment.Item':
            if obj_map['question']:
                obj_map['question'] = self.get_question().get_object_map()
            obj_map['answers'] = []
            for answer in self.get_answers():
                obj_map['answers'].append(answer.get_object_map())
        if self._namespace == 'assessment.Question':
            my_idstr = obj_map['itemId']
            del obj_map['itemId']
            lo_ids = self.get_learning_objective_ids()
            obj_map['learningObjectiveIds'] = [str(lo_id) for lo_id in lo_ids]
        if self._namespace == 'assessment.Answer':
            del obj_map['itemId']
        if self._namespace == 'commenting.Comment':
            obj_map['commentingAgentId'] = str(self.get_commenting_agent_id())
        if self._namespace == 'assessment.Assessment':
            if 'itemIds' in obj_map:
                del obj_map['itemIds']
        if self._namespace == 'assessment.AssessmentOffered':
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
                obj_map['startTime'] = dict()
                obj_map['startTime']['year'] = deadline.year
                obj_map['startTime']['month'] = deadline.month
                obj_map['startTime']['day'] = deadline.day
                obj_map['startTime']['hour'] = deadline.hour
                obj_map['startTime']['minute'] = deadline.minute
                obj_map['startTime']['second'] = deadline.second
                obj_map['startTime']['microsecond'] = deadline.microsecond
            if obj_map['displayName']['text'] == '':
                obj_map['displayName']['text'] = self.get_display_name().get_text()
            if obj_map['description']['text'] == '':
                obj_map['description']['text'] = self.get_description().get_text()
        if self._namespace == 'assessment.AssessmentTaken':
            if obj_map['actualStartTime'] is not None:
                actualStartTime = obj_map['actualStartTime']
                obj_map['actualStartTime'] = dict()
                obj_map['actualStartTime']['year'] = actualStartTime.year
                obj_map['actualStartTime']['month'] = actualStartTime.month
                obj_map['actualStartTime']['day'] = actualStartTime.day
                obj_map['actualStartTime']['hour'] = actualStartTime.hour
                obj_map['actualStartTime']['minute'] = actualStartTime.minute
                obj_map['actualStartTime']['second'] = actualStartTime.second
                obj_map['actualStartTime']['microsecond'] = actualStartTime.microsecond
            if obj_map['completionTime'] is not None:
                completionTime = obj_map['completionTime']
                obj_map['completionTime'] = dict()
                obj_map['completionTime']['year'] = completionTime.year
                obj_map['completionTime']['month'] = completionTime.month
                obj_map['completionTime']['day'] = completionTime.day
                obj_map['completionTime']['hour'] = completionTime.hour
                obj_map['completionTime']['minute'] = completionTime.minute
                obj_map['completionTime']['second'] = completionTime.second
                obj_map['completionTime']['microsecond'] = completionTime.microsecond
            if obj_map['displayName']['text'] == '':
                obj_map['displayName']['text'] = self.get_display_name().get_text()
            if obj_map['description']['text'] == '':
                obj_map['description']['text'] = self.get_description().get_text()
            if 'itemIds' in obj_map:
                del obj_map['itemIds']
            if 'responses' in obj_map:
                del obj_map['responses']

        try: # Need to implement records for catalogs one of these days
            for record in self._records:
                try:
                    self._records[record]._update_object_map(obj_map)
                except AttributeError:
                    pass
        except AttributeError:
            pass
        
        obj_map.update(
            {'type': self._namespace.split('.')[-1],
             'id': my_idstr})
        return obj_map

    object_map = property(get_object_map)
"""

    get_display_name = """
        return DisplayText(self._my_map['displayName'])"""

    get_description = """
        return DisplayText(self._my_map['description'])"""

    get_genus_type = """
        try:
            # Try to stand up full Type objects if they can be found
            # (Also need to LOOK FOR THE TYPE IN types or through type lookup)
            genus_type_identifier = Id(self._my_map['genusTypeId']).get_identifier()
            return Type(**types.Genus().get_type_data(genus_type_identifier))
        except:
            # If that doesn't work, return the id only type, still useful for comparison.
            return Type(idstr=self._my_map['genusTypeId'])"""

    is_of_genus_type = """
        return genus_type == Type(idstr=self._my_map['genusTypeId'])"""

class OsidRule:

    has_rule = """
        # Someday I'll have a real implementation, but for now I just:
        return False"""

    get_rule_id = """
        from .osid_errors import IllegalState
        # Someday I'll have a real implementation, but for now I just:
        raise IllegalState()"""
    
    get_rule= """
        from .osid_errors import IllegalState
        # Someday I'll have a real implementation, but for now I just:
        raise IllegalState()"""

class OsidForm:

    import_statements = [
        'from ..primitives import *',
        'from ..osid.osid_errors import *',
        'from . import mdata_conf',
        'from .metadata import Metadata',
        ]

    init = """
    _namespace = 'mongo.OsidForm'

    def __init__(self):
        import uuid
        self._identifier = str(uuid.uuid4())
        self._for_update = None

    def _init_metadata(self):
        self._journal_comment_metadata = {
            'element_id': Id(authority = self._authority,
                             namespace = self._namespace,
                             identifier = 'display_name')}
        self._journal_comment_metadata.update(mdata_conf.journal_comment)
        self._journal_comment_default = dict(self._journal_comment_metadata['default_string_values'][0])
        self._journal_comment = self._journal_comment_default
        self._validation_messages = {}

    ##
    # Override get_id as implemented in Identifiable for the purpose of 
    # returning an Id unique to this form for submission purposed as 
    # recommended in the osid documentation. This implementation
    # substitutes the intialized Python uuid4 identifier, and the 
    # form namespace from the calling Osid Form thing.
    def get_id(self):
        from ..primitives import Id
        return Id(identifier = self._identifier,
                   namespace = self._namespace,
                   authority = self._authority)
                  
    ##
    # The _is_valid_input method takes three arguments, the user input to 
    # be checked, the associated  osid.Metadata object containing validation 
    # requirements and a boolean value indicating whether this is an array value.
    def _is_valid_input(self, input, metadata, array):
        syntax = metadata.get_syntax

        ##
        # First check if this is a required data element
        if metadata.is_required == True and not input:
            return False
            
        valid = True # Innocent until proven guilty        
        ##
        # Recursively run through all the elements of an array
        if array == True:
            if len(input) < metadata['minimum_elements']:
                valid = False
            elif len(input) > metadata['maximum_elements']:
                valid = False
            else:
                for element in array:
                    valid = (valid and 
                        self._is_valid_input(element, metadata, False))
        ##
        # Run through all the possible syntax types
        elif syntax == 'ID':
            valid = self._is_valid_id(input)
        elif syntax == 'TYPE':
            valid = self._is_valid_type(input)
        elif syntax == 'BOOLEAN':
            valid = self._is_valid_boolean(input)
        elif syntax == 'STRING':
            valid = self._is_valid_string(input, metadata)
        elif syntax == 'INTEGER':
            valid = self._is_valid_integer(input, metadata)
        elif syntax == 'DECIMAL':
            valid = self._is_valid_decimal(input, metadata)
        elif syntax == 'DATETIME':
            valid = self._is_valid_date_time(input, metadata)
        elif syntax == 'DURATION':
            valid = self._is_valid_duration(input, metadata)
        elif syntax == 'CARDINAL':
            valid = self._is_valid_cardinal(input, metadata)
        elif syntax == 'INTEGER':
            valid = self._is_valid_integer(input, metadata)
        elif syntax == 'DECIMAL':
            valid = self._is_valid_decimal(input, metadata)
        else:
            raise OperationFailed('no validation function available for ' + syntax)

        return valid 

    def _is_valid_id(self, input):
        from ...abstract_osid.id.primitives import Id
        if isinstance(input, Id):
            return True
        else:
            return False

    def _is_valid_type(self, input):
        from ...abstract_osid.type.primitives import Type
        if isinstance(input, Type):
            return True
        else:
            return False

    def _is_valid_boolean(self, input):
        if isinstance(input, bool):
            return True
        else:
            return False

    def _is_valid_string(self, input, metadata):
        if not isinstance(input, basestring):
            return False
        if metadata.get_minimum_string_length() and len(input) < metadata.get_minimum_string_length():
            return False
        elif metadata.get_maximum_string_length() and len(input) > metadata.get_maximum_string_length():
            return False
        if (metadata.get_string_set() and
            input not in metadata.get_string_set()):
            return False
        else:
            return True

    def _is_valid_cardinal(self, input, metadata):
        if not isinstance(input, int):
            return False
        if metadata.get_minimum_cardinal() and input < metadata.get_maximum_cardinal():
            return False
        if metadata.get_maximum_cardinal() and input > metadata.get_minimum_cardinal():
            return False
        if metadata.get_cardinal_set() and input not in metadata.get_cardinal_set():
            return False
        else:
            return True

    def _is_valid_integer(self, input, metadata):
        if not isinstance(input, int):
            return False
        if metadata.get_minimum_integer() and input < metadata.get_maximum_integer():
            return False
        if metadata.get_maximum_integer() and input > metadata.get_minimum_integer():
            return False
        if metadata.get_integer_set() and input not in metadata.get_integer_set():
            return False
        else:
            return True

    def _is_valid_decimal(self, input, metadata):
        if not isinstance(input, float):
            return False
        if metadata.get_minimum_decimal() and input < metadata.get_minimum_decimal():
            return False
        if metadata.get_maximum_decimal() and input > metadata.get_maximum_decimal():
            return False
        if metadata.get_decimal_set() and input not in metadata.get_decimal_set():
            return False
        if metadata.get_decimal_scale() and len(str(input).split('.')[-1]) != metadata.get_decimal_scale():
            return False
        else:
            return True

    def _is_valid_date_time(self, input, metadata):
        # NEED TO ADD CHECKS FOR OTHER METADATA, LIKE MINIMUM, MAXIMUM, ETC.
        from ...abstract_osid.calendaring.primitives import DateTime
        if isinstance(input, DateTime):
            return True
        else:
            return False

    def _is_valid_timestamp(self, *args, **kwargs):
        # This should be temporary to deal with a bug in the OSID RC3 spec
        # Check assessment.AssessmentOffered.set_deadline to see if this 
        # is still required.
        return self._is_valid_date_time(*args, **kwargs)

    def _is_valid_duration(self, input, metadata):
        # NEED TO ADD CHECKS FOR OTHER METADATA, LIKE MINIMUM, MAXIMUM, ETC.
        from ...abstract_osid.calendaring.primitives import Duration
        if isinstance(input, Duration):
            return True
        else:
            return False
"""

    is_for_update = """
        return self._for_update"""

    get_default_locale = """
        from ..locale.objects import Locale
        # If no constructor arguments are given it is expected that the 
        # locale service will return the default Locale.
        return Locale()"""

    get_locales = """
        # Someday I might have a real implementation
        # For now only default Locale is supported
        from ..locale.objects import LocaleList
        return LocaleList([])"""

    set_locale = """
        # Someday I might have a real implementation
        # For now only default Locale is supported
        raise Unsupported()"""

    get_journal_comment_metadata = """
        return Metadata(**self._journal_comment_metadata)"""

    set_journal_comment = """
        if comment is None:
            raise NullArgument()
        if self.get_comment_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_string(comment, 
                                     self.get_journal_comment_metadata()):
            raise InvalidArgument()
        self._journal_comment = comment"""

    is_valid = """
        # It is assumed that all setter methods check validity so there 
        # should never be a state where invalid data exists in the form.  
        # And if you believe that...
        return True"""

    get_validation_messages = """
        # See note above
        return []"""

    get_invalid_metadata = """
        # See notes above
        return []"""

class OsidExtensibleForm:

    init = """
    # This overrides _get_record in osid.Extensible. Perhaps we should leverage it somehow?
    def _get_record(self, recordType):
        if recordType is None:
            raise NullArgument()
        if not self.has_record_type(recordType):
            raise Unsupported()
        if str(recordType) not in self._records: # Currently this should never be True
            self._init_record(str(recordType))
            if str(recordType) not in self._my_map['recordTypeIds']: # nor this
                self._my_map['recordTypeIds'].append(str(recordType))
        return self._records[str(recordType)]
"""

class OsidTemporalForm:

    import_statements = [
        'from ..primitives import *',
        'from ..osid.osid_errors import *',
        'import datetime',
        'from . import mdata_conf',
        'from .metadata import Metadata',
        #'from . import profile'
        ]

    init = """
    _namespace = "mongo.OsidTemporalForm"

    def _init_metadata(self, **kwargs):
        self._start_date_metadata = {
            'element_id': Id(authority = self._authority,
                             namespace = self._namespace, 
                             identifier = 'start_date')}
        self._start_date_metadata.update(mdata_conf.start_date)
        self._start_date_metadata.update({'default_date_time_values': [self._get_date_map(datetime.datetime.now())]})
        self._end_date_metadata = {
            'element_id': Id(authority = self._authority,
                             namespace = self._namespace, 
                             identifier = 'end_date')}
        self._end_date_metadata.update(mdata_conf.end_date)

    def _init_map(self):
        self._my_map['startDate'] = self._start_date_metadata['default_date_time_values'][0]
        self._my_map['endDate'] = self._end_date_metadata['default_date_time_values'][0]
"""

    get_start_date_metadata = """
        metadata = dict(self._start_date_metadata)
        metadata.update({'existing_date_time_values': self._my_map['startDate']})
        return Metadata(**metadata)"""

    set_start_date = """
        if date is None:
            raise NullArgument()
        if self.get_start_date_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_date_time(date):
            raise InvalidArgument()
        self._my_map['startDate'] = self._get_date_map(date)"""

    clear_start_date = """
        if (self.get_start_date_metadata().is_read_only() or
            self.get_start_date_metadata().is_required()):
            raise NoAccess()
        self._my_map['startDate'] = self.get_start_date_metadata['default_date_time_values'][0]"""

    get_end_date_metadata = """
        metadata = dict(self._end_date_metadata)
        metadata.update({'existing_date_time_values': self._my_map['endDate']})
        return Metadata(**metadata)"""

    set_end_date = """
        if date is None:
            raise NullArgument()
        if self.get_end_date_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_date_time(date):
            raise InvalidArgument()
        self._my_map['endDate'] = self._get_date_map(date)"""

    clear_end_date = """
        if (self.get_end_date_metadata().is_read_only() or
            self.get_end_date_metadata().is_required()):
            raise NoAccess()
        self._my_map['endDate'] = self.get_end_date_metadata['default_date_time_values'][0]"""

    additional_methods = """
    def _get_date_map(self, date):
        return {
            'year': date.year,
            'month': date.month,
            'day': date.day,
            'hour': date.hour,
            'minute': date.minute,
            'second': date.second,
            'microsecond': date.microsecond,
        }"""

class OsidObjectForm:

    #inheritance = ['OsidObject']

    import_statements = [
        'from ..primitives import *',
        'from ..osid.osid_errors import *',
        'from . import mdata_conf',
        'from .metadata import Metadata',
        'from . import profile'
        ]

    init = """
    _namespace = "mongo.OsidObjectForm"

    ## In the real world this will never get called:
    def __init__(self, osid_object_map=None):
        OsidForm.__init__(self)
        self._init_metadata()
        if osid_object_map is not None:
            self._my_map = osid_object_map
            self._for_update = True
        else:
            self._my_map = {}
            self._for_update = False
            self._init_map()

    def _init_metadata(self, **kwargs):
        OsidForm._init_metadata(self)
        self._display_name_metadata = {
            'element_id': Id(authority = self._authority,
                             namespace = self._namespace,
                             identifier = 'display_name')}
        self._display_name_metadata.update(mdata_conf.display_name)
        if 'default_display_name' in kwargs:
            self._display_name_metadata['default_string_values'][0]['text'] = kwargs['default_display_name']
        self._description_metadata = {
            'element_id': Id(authority = self._authority,
                             namespace = self._namespace, 
                             identifier = 'description')}
        self._description_metadata.update(mdata_conf.description)
        self._genus_type_metadata = {
            'element_id': Id(authority = self._authority,
                             namespace = self._namespace, 
                             identifier = 'description')}
        if 'default_description' in kwargs:
            self._description_metadata['default_string_values'][0]['text'] = kwargs['default_description']
        self._genus_type_metadata.update(mdata_conf.genus_type)

    def _init_map(self):
        self._my_map['displayName'] = dict(self._display_name_metadata['default_string_values'][0])
        self._my_map['description'] = dict(self._description_metadata['default_string_values'][0])
        self._my_map['genusTypeId'] = self._genus_type_metadata['default_type_values'][0]
        self._my_map['recordTypeIds'] = []

    # Deprecate this:
    def _old_get_provider_manager(self, osid):
        if self._runtime is None:
            # Return a Manager from this implementation:
            module = import_module('dlkit.mongo.' + osid.lower() + '.managers')
            manager = getattr(module, osid.title() + 'Manager')()
        else:
            # Get the Manager from the runtime:
            config = self._runtime.get_configuration()
            parameter_id = Id('parameter:repositoryProviderImpl@mongo')
            impl_name = config.get_value_by_parameter(parameter_id).get_string_value()
            manager = self._runtime.get_manager(osid, impl_name) # What about ProxyManagers?
        return manager

    def _get_provider_manager(self, osid):
        try:
            # Try to get the Manager from the runtime, if available:
            config = self._runtime.get_configuration()
            parameter_id = Id('parameter:repositoryProviderImpl@mongo')
            impl_name = config.get_value_by_parameter(parameter_id).get_string_value()
            manager = self._runtime.get_manager(osid, impl_name) # What about ProxyManagers?
        except:
            # Just return a Manager from this implementation:
            module = import_module('dlkit.mongo.' + osid.lower() + '.managers')
            manager = getattr(module, osid.title() + 'Manager')()
        return manager

    #def __getattr__(self, name):
    #    if '_records' in self.__dict__:
    #        for record in self._records:
    #            try:
    #                return self._records[record][name]
    #            except AttributeError:
    #                pass
    #    raise AttributeError()
"""

    get_display_name_metadata = """
        return Metadata(**self._display_name_metadata)"""

    set_display_name = """
        if display_name is None:
            raise NullArgument()
        if self.get_display_name_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_string(display_name, 
                                     self.get_display_name_metadata()):
            raise InvalidArgument()
        self._my_map['displayName']['text'] = display_name"""

    clear_display_name = """
        if (self.get_display_name_metadata().is_read_only() or
            self.get_display_name_metadata().is_required()):
            raise NoAccess()
        self._my_map['displayName'] = dict(self._display_name_metadata['default_object_values'][0])"""

    get_description_metadata = """
        return Metadata(**self._description_metadata)"""

    set_description = """
        if description is None:
            raise NullArgument()
        if self.get_description_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_string(description, 
                                     self.get_description_metadata()):
            raise InvalidArgument()
        self._my_map['description']['text'] = description"""

    clear_description = """
        if (self.get_description_metadata().is_read_only() or
            self.get_description_metadata().is_required()):
            raise NoAccess()
        self._my_map['description'] = dict(self._description_metadata['default_object_values'][0])"""

    get_genus_type_metadata = """
        return Metadata(**self._genus_type_metadata)"""

    set_genus_type = """
        if genus_type is None:
            raise NullArgument()
        if self.get_genus_type_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_type(genus_type):
            raise InvalidArgument()
        self._my_map['genusTypeId'] = str(genus_type)"""

    clear_genus_type = """
        if (self.get_genus_type_metadata().is_read_only() or
            self.get_genus_type_metadata().is_required()):
            raise NoAccess()
        self._my_map['genusType'] = self._genus_type_metadata['default_type_values'][0]"""

class OsidRelationshipForm:

    init = """
    def _init_metadata(self, **kwargs):
        OsidObjectForm._init_metadata(self, **kwargs)
        OsidTemporalForm._init_metadata(self, **kwargs)

    def _init_map(self, **kwargs):
        OsidObjectForm._init_map(self, **kwargs)
        OsidTemporalForm._init_map(self, **kwargs)
"""

class OsidList:

    init = """
    def __init__(self, iter_object=[], count=None, db_prefix='', runtime=None):
        if count != None:
            self._count = count
        elif isinstance(iter_object, dict) or isinstance(iter_object, list):
            self._count = len(iter_object)
        else:
            self._count = None
        self._runtime = runtime
        self._db_prefix = db_prefix
        self._iter_object = iter(iter_object)

    def __iter__(self):
        return self

    def next(self):
        try:
            next_object = self._iter_object.next()
        except: 
            raise
        if self._count != None:
            self._count -= 1
        return next_object

    def len(self):
        return self.available()
"""

    has_next = """
        if self._count != None:
            # If count is available, use it
            return bool(self._count)
        else:
            # otherwise we have no idea
            return True"""

    available = """
        if self._count != None:
            # If count is available, use it
            return self._count
        else:
            # We have no idea.
            return 0  # Don't know what to do here"""

    skip = """
        ### STILL NEED TO IMPLEMENT THIS ###
        pass"""

class OsidQuery:

    import_statements = [
        'import re',
        'from ..primitives import *',
        'from ..osid.osid_errors import *',
        'from ..locale.types import String',
        'EXACT_STRING_MATCH_TYPE = Type(**String().get_type_data(\'EXACT\'))',
        'IGNORECASE_STRING_MATCH_TYPE = Type(**String().get_type_data(\'IGNORECASE\'))',
        'WORD_STRING_MATCH_TYPE = Type(**String().get_type_data(\'WORD\'))',
        'WORDIGNORECASE_STRING_MATCH_TYPE = Type(**String().get_type_data(\'WORDIGNORECASE\'))',
        'WILDCARD_STRING_MATCH_TYPE = Type(**String().get_type_data(\'WILDCARD\'))',
        'REGEX_STRING_MATCH_TYPE = Type(**String().get_type_data(\'REGEX\'))',
        'SOUND_STRING_MATCH_TYPE = Type(**String().get_type_data(\'SOUND\'))',
        'SOUNDEX_STRING_MATCH_TYPE = Type(**String().get_type_data(\'SOUNDEX\'))',
        'METAPHONE_STRING_MATCH_TYPE = Type(**String().get_type_data(\'METAPHONE\'))',
        'SOUNDEX_STRING_MATCH_TYPE = Type(**String().get_type_data(\'SOUNDEX\'))',
        'DMETAPHONE_STRING_MATCH_TYPE = Type(**String().get_type_data(\'DMETAPHONE\'))',
        'LEVENSHTEIN_STRING_MATCH_TYPE = Type(**String().get_type_data(\'LEVENSHTEIN\'))',
    ]

    init = """
    def __init__(self):
        self._records = dict()
        self._load_records(self._all_supported_record_type_ids)
        self._query_terms = {}

    def _get_string_match_value(self, string, string_match_type):
        if string_match_type == EXACT_STRING_MATCH_TYPE:
            return string
        elif string_match_type == IGNORECASE_STRING_MATCH_TYPE:
            return re.compile('^' + string, re.I)
        elif string_match_type == WORD_STRING_MATCH_TYPE:
            return re.compile('.*' + string + '.*')
        elif string_match_type == WORDIGNORECASE_STRING_MATCH_TYPE:
            return re.compile('.*' + string + '.*', re.I)

    def _add_match(self, match_key, match_value, match):
        if match_key is None:
            raise NullArgument()
        if match is None:
            match = True
        if match:
            inin = '$in'
        else:
            inin = '$nin'
        if match_key in self._query_terms:
            if inin in self._query_terms[match_key]:
                self._query_terms[match_key][inin].append(match_value)
            else:
                self._query_terms[match_key][inin] = [match_value]
        else:
            self._query_terms[match_key] = {inin: [match_value]}

    def _match_display_text(self, element_key, string, string_match_type, match):
        if string is None or string_match_type is None:
            raise NullArgument()
        match_value = self._get_string_match_value(string, string_match_type)
        self._add_match(element_key + '.text', match_value, match)

    def _match_minimum_decimal(self, match_key, decimal_value, match):
        if decimal_value is None:
            raise NullArgument()
        if match is None:
            match = True
        if match:
            gtelt = '$gte'
        else:
            gtelt = '$lt'
        if match_key in self._query_terms:
            self._query_terms[match_key][gtelt] = decimal_value
        else:
            self._query_terms[match_key] = {gtelt: decimal_value}
        
    def _match_maximum_decimal(self, match_key, decimal_value, match):
        if decimal_value is None:
            raise NullArgument()
        if match is None:
            match = True
        if match:
            ltegt = '$lte'
        else:
            ltegt = '$gt'
        if match_key in self._query_terms:
            self._query_terms[match_key][ltegt] = decimal_value
        else:
            self._query_terms[match_key] = {ltegt: decimal_value}

    def _match_minimum_date_time(self, match_key, date_time_value, match):
        if date_time_value is None:
            raise NullArgument()
        if match is None:
            match = True
        if match:
            gtelt = '$gte'
        else:
            gtelt = '$lt'
        if match_key in self._query_terms:
            self._query_terms[match_key][gtelt] = date_time_value
        else:
            self._query_terms[match_key] = {gtelt: date_time_value}
        
    def _match_maximum_date_time(self, match_key, date_time_value, match):
        if date_time_value is None:
            raise NullArgument()
        if match is None:
            match = True
        if match:
            gtelt = '$lte'
        else:
            gtelt = '$gt'
        if match_key in self._query_terms:
            self._query_terms[match_key][gtelt] = date_time_value
        else:
            self._query_terms[match_key] = {gtelt: date_time_value}
        
    def _clear_terms(self, match_key):
        try:
            del self._query_terms[match_key]
        except KeyError:
            pass

    def _clear_minimum_terms(self, match_key):
        try: # clear match = True case
            del self._query_terms[match_key]['$gte']
        except KeyError:
            pass
        try: # clear match = False case
            del self._query_terms[match_key]['$lt']
        except KeyError:
            pass
        try:
            if self._query_terms[match_key] == {}:
                del self._query_terms[match_key]
        except KeyError:
            pass

    def _clear_maximum_terms(self, match_key):
        try: # clear match = True case
            del self._query_terms[match_key]['$lte']
        except KeyError:
            pass
        try: # clear match = False case
            del self._query_terms[match_key]['$gt']
        except KeyError:
            pass
        try:
            if self._query_terms[match_key] == {}:
                del self._query_terms[match_key]
        except KeyError:
            pass
"""

class OsidIdentifiableQuery:

    import_statements = [
        'from ..osid.osid_errors import *',
        'from ..primitives import *'
    ]

    match_id = """
        self._add_match('id_', id_.get_identifier(), match)"""
    
    clear_id_terms = """
        self._clear_terms('id_')"""

class OsidExtensibleQuery:

    import_statements = [
        'import importlib',
        'from ..primitives import *',
    ]

    init = """
    def _load_records(self, record_type_idstrs):
        for record_type_idstr in record_type_idstrs:
            try:
                self._init_record(record_type_idstr)
            except (ImportError, KeyError):
                pass

    def _init_record(self, record_type_idstr):
        record_type_data = self._all_supported_record_type_data_sets[Id(record_type_idstr).get_identifier()]
        module = importlib.import_module(record_type_data['module_path'])
        record = getattr(module, record_type_data['query_record_class_name'])
        self._records[record_type_idstr] = record(self)
    """

class OsidObjectQuery:

    import_statements = [
        'from ..osid.osid_errors import *',
    ]

    match_display_name = """
        self._match_display_text('displayName', display_name, string_match_type, match)"""

    match_any_display_name = """
        raise Unimplemented()"""

    clear_display_name_terms = """
        self._clear_terms('displayName.text')"""
    
    match_description = """
        self._match_display_text('description', description, string_match_type, match)"""

    match_any_description = """
        raise Unimplemented()"""

    clear_description_terms = """
        self._clear_terms('description.text')"""
    
class OsidRecord:

    init = """
    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith('__'):
                yield attr

    def __getitem__(self, item):
        return getattr(self, item)
"""

    implements_record_type = """
        return record_type.get_identifier() in self._implemented_record_type_identifiers"""
    

class Metadata:

    import_statements = [
        'from .osid_errors import *'
    ]

    init = """
    def __init__(self, **kwargs):
        self._kwargs = kwargs
"""

    get_element_id_template = """
        # Implemented from template for osid.Metadata.get_element_id_template
        return self._kwargs['${var_name}']"""

    get_minimum_cardinal_template = """
        # Implemented from template for osid.Metadata.get_minimum_cardinal
        if self._kwargs['syntax'] not in ${syntax_list}:
            raise IllegalState()
        return self._kwargs['${var_name}']"""

    supports_coordinate_type_template = """
        # Implemented from template for osid.Metadata.supports_coordinate_type
        if not ${arg0_name}:
            raise NullArgument('no input Type provided')
        if self._kwargs['syntax'] not in ${syntax_list}:
            raise IllegalState()
        return ${arg0_name} in self.get_${var_name}"""

    get_existing_cardinal_values_template = """
        # Implemented from template for osid.Metadata.get_existing_cardinal_values_template
        # This template may only work well for very primitive return types, like string or cardinal.
        # Need to update it to support DisplayName, or Id etc.
        if self._kwargs['syntax'] not in ${syntax_list}:
            raise IllegalState()
        return self._kwargs['${var_name}']"""


class OsidNode:

    init = """
    def __init__(self, node_map):
        self._my_map = node_map
"""

    is_root = """
        return self._my_map['root']"""

    has_parents = """
        return bool(self._my_map[parentdNodes])"""

    get_parent_ids = """
        id_list = []
        for child_node in self._my_map['parentdNodes']:
            id_list.append(parent_node['id'])
        return IdList(id_list)"""

    is_leaf = """
        return self._my_map['leaf']"""

    has_children = """
        return bool(self._my_map[childNodes])"""

    get_child_ids = """
        id_list = []
        for child_node in self._my_map['childNodes']:
            id_list.append(child_node['id'])
        return IdList(id_list)"""

    additional_methods = """
    def get_node_map(self):
        node_map = dict(self._my_map)
        node_map['parentNodes'] = []
        node_map['childNodes'] = []
        for node in self._my_map['parentNodes']:
            node_map['parentNodes'].append(node.get_node_map())
        for node in self._my_map['childNodes']:
            node_map['childNodes'].append(node.get_node_map())
        return node_map
"""
        

