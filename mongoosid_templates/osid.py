
class OsidProfile:

    get_id = """
        from . import profile
        from ..id.primitives import Id
        return Id(**profile.ID)
        """

    get_display_name = """
        from . import profile
        from ..primitives import Type, DisplayText
        return DisplayText(text = profile.DISPLAYNAME,
                           language_type = Type(**profile.LANGUAGETYPE),
                           script_type = Type(**profile.SCRIPTTYPE),
                           format_type = Type(**profile.FORMATTYPE))"""

    get_description = """
        from . import profile
        from ..primitives import Type, DisplayText
        return DisplayText(text = profile.DESCRIPTION,
                           language_type = Type(**profile.LANGUAGETYPE),
                           script_type = Type(**profile.SCRIPTTYPE),
                           format_type = Type(**profile.FORMATTYPE))"""

    get_version = """
        ## THIS ALL NEEDS TO BE FIXED:
        from . import profile
        try:
            from ..installation.primitives import Version
        except:
            from .common import Version
        try:
            from ..type.primitives import Type
        except:
            from .common import Type
        return Version(components = profile.VERSIONCOMPONENTS,
                       scheme = Type(**profile.VERSIONSCHEME))"""

    get_release_date = """
        # NEED TO IMPLEMENT
        pass"""

    supports_osid_version = """
        ## THIS ALL NEEDS TO BE FIXED:
        from . import profile
        try:
            from ..installation.primitives import Version
        except:
            from .common import Version
        try:
            from ..type.primitives import Type
        except:
            from .common import Type
        return Version(components = profile.OSIDVERSION,
                       scheme = Type(**profile.VERSIONSCHEME))"""

    get_locales = """
        # NEED TO IMPLEMENT
        pass"""

    supports_journal_rollback = """
        # Perhaps someday I will support journaling
        return False"""

    supports_journal_branching = """
        # Perhaps someday I will support journaling
        return False"""

    get_branch_id = """
        # Perhaps someday I will support journaling
        from .osid_errors import Unimplemented
        raise Unimplemented()"""

    get_branch = """
        # Perhaps someday I will support journaling
        # Perhaps someday I will support journaling
        from .osid_errors import Unimplemented
        raise Unimplemented()"""

    get_proxy_record_types = """
        # NEED TO IMPLEMENT
        pass"""

    supports_proxy_record_type = """
        # NEED TO IMPLEMENT
        pass"""

class Identifiable:

    init = """
    import socket
    _authority = socket.gethostname()
    #_authority = 'birdland.mit.edu'
"""

    get_id = """
        from ..primitives import Id
        return Id(identifier = str(self._my_map['_id']),
                   namespace = self._namespace,
                   authority = self._authority)"""

    is_current = """
        # Osid Objects in this implementation will quickly become stale
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


    def _delete(self):
        # Override this method in inheriting objects to perform special clearing operations
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
        from ..primitives import Type, Id
        from ..type.objects import TypeList
        type_list = []
        for type_idstr in self._supported_record_type_ids:
            type_list.append(Type(**self._record_type_data_sets[Id(type_idstr).get_identifier()]))
        return TypeList(type_list)"""


class Operable:

    is_active = """
        # THIS MAY NOT BE RIGHT. REVIEW LOGIC FROM OSID DOC
        return self.is_operational() and (not self.is_disabled() or is_enabled())"""

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
    'from ..primitives import *',
    'from .osid_errors import *',
    'from bson.objectid import ObjectId',
    'from pymongo import MongoClient',
    'from .. import types',
    ]

    init = """

    COMPARATIVE = 0
    PLENARY = 1
    FEDERATED = 0
    ISOLATED = 1
    CREATED = True
    UPDATED = True

    def _init_catalog(self, proxy = None):
        self._proxy = proxy        

    def _init_object(self, catalog_id, proxy, db_name, cat_name, cat_class):
        from . import profile
        self._catalog_identifier = None
        self._proxy = proxy
        from pymongo import MongoClient
        collection = MongoClient()[db_name][cat_name]
        if catalog_id is not None and catalog_id.get_identifier() != '000000000000000000000000':
            self._catalog_identifier = catalog_id.get_identifier()
            self._my_catalog_map = collection.find_one({'_id': ObjectId(self._catalog_identifier)})
            if self._my_catalog_map is None:
                # Should also check for the authority here:
                if catalog_id.get_identifier_namespace() != db_name + '.' + cat_name:
                    self._my_catalog_map = {
                        '_id': ObjectId(catalog_id.get_identifier()),
                        'displayName': {'text': catalog_id.get_identifier_namespace() + ' ' + cat_name,
                                        'languageTypeId': str(Type(**types.Language().get_type_data('DEFAULT'))),
                                        'scriptTypeId': str(Type(**types.Script().get_type_data('DEFAULT'))),
                                        'formatTypeId': str(Type(**types.Format().get_type_data('DEFAULT'))),},
                        'description': {'text': cat_name + ' for ' + catalog_id.get_identifier_namespace() + ' objects',
                                        'languageTypeId': str(Type(**types.Language().get_type_data('DEFAULT'))),
                                        'scriptTypeId': str(Type(**types.Script().get_type_data('DEFAULT'))),
                                        'formatTypeId': str(Type(**types.Format().get_type_data('DEFAULT'))),},
                        'genusType': str(Type(**types.Genus().get_type_data('DEFAULT')))
                    }
                    collection.insert(self._my_catalog_map)
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
                'genusType': str(Type(**types.Genus().get_type_data('DEFAULT')))
            }
        self._catalog = cat_class(self._my_catalog_map)
        self._catalog_id = self._catalog.get_id()
        self._forms = dict()

    def _get_orchestrated_catalog_identifier(self, service_name):
        from pymongo import MongoClient
        from bson.objectid import ObjectId
        client = MongoClient()
        from .osid_errors import NotFound
        catalogs = {'learning': 'ObjectiveBank',
                    'relationship': 'Family',
                    'repository': 'Repository'}
        if self._catalog_identifier is None:
            raise NotFound()
        elif self._catalog_identifier == '000000000000000000000000':
            return self._catalog_identifier
        else:
            db = client[service_name]
            collection = db[catalogs[service_name]]
            if collection.find_one({'_id': ObjectId(self._catalog_identifier)}) is None:
                catalog_map = self._my_catalog_map
                catalog_map['description']['text'] = ('Orchestrated ' + 
                    catalogs[service_name] + ' for ' + catalog_map['description']['text'])
                collection.insert(catalog_map)
            return self._catalog_identifier
    """

    get_locale = """
        from ..locale.objects import Locale
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
            return Id(identifier = 'MC3GUE$T@MIT.EDU',
                      namespace = 'agent.Agent',
                      authority = 'MIT-OEIT')"""

    get_effective_agent = """
        effective_agent_id = self.get_effective_agent_id()
        # This may want to be extended to get the Agent directly from the Authentication
        # if available and if not effective agent is available in the proxy
        return Agent(identifier = effective_agent_id.get_identifier(),
                  namespace = effective_agent_id.get_namespace(),
                  authority = effective_agent_id.get_authority())"""

    supports_transactions = """
        return False"""

    startTransaction = """
        if not supports_transactions:
            raise Unsupported('transactions ore not supported for this session')"""


class OsidObject:

    init = """
    _namespace = 'mongo.OsidObject'

    def __init__(self, osid_object_map):
        self._my_map = osid_object_map

#    def __getattr__(self, name): # moved this method to osid.markers.Extensible
#        if '_records' in self.__dict__:
#            for record in self._records:
#                try:
#                    return self._records[record][name]
#                except AttributeError:
#                    pass
#        raise AttributeError(name)
#
#    def _delete(self):
#        # Override this method in inheriting objects to perform special clearing operations
#        try: # Need to implement records for catalogs one of these days
#            for record in self._records:
#                try:
#                    self._records[record]._delete()
#                except AttributeError:
#                    pass
#        except AttributeError:
#            pass
        
    def get_object_map(self, obj_map=None):
        if obj_map is None:
            obj_map = dict(self._my_map)
        del obj_map['_id']
        my_idstr = str(self.get_id())

        # The following is crap. Should be over-ridden in the corresponding
        # aggregated object instead:
        if self._namespace == 'repository.Asset':
            obj_map['assetContent'] = []
            for asset_content in self.get_asset_content():
                obj_map['assetContent'].append(asset_content.get_object_map())
        if self._namespace == 'assessment.Item':
            if obj_map['question']:
                obj_map['question'] = self.get_question().get_object_map()
            obj_map['answers'] = []
            for answer in self.get_answers():
                obj_map['answers'].append(answer.get_object_map())
        if self._namespace == 'assessment.Question':
            my_idstr = obj_map['itemId']
            del obj_map['itemId']
        if self._namespace == 'assessment.Answer':
            del obj_map['itemId']
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
        from ..primitives import DisplayText
        return DisplayText(self._my_map['displayName'])"""

    get_description = """
        from ..primitives import DisplayText
        return DisplayText(self._my_map['description'])"""

    get_genus_type = """
        from .. import types
        from ..primitives import Id, Type
        ### Also LOOK FOR THE TYPE IN types or through type lookup
        genus_type_identifier = Id(self._my_map['genusTypeId']).get_identifier()
        return Type(**types.Genus().get_type_data(genus_type_identifier))"""

    is_of_genus_type = """
        from ..primitives import Type
        return genus_type == self.get_genus_type()"""

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

    init = """
    _namespace = 'mongo.OsidForm'

    def __init__(self):
        import uuid
        self._identifier = str(uuid.uuid4())
        self._for_update = None

    def _init_metadata(self):
        from . import mdata_conf
        from ..primitives import Id
        from ..primitives import DisplayText
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
                    validation['valid'] = (validation['valid'] and 
                        self._is_valid_input(element, metadata, False, validation))
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
        return LocaleList([])"""

    set_locale = """
        # Someday I might have a real implementation
        # For now only default Locale is supported
        from .osid_errors import Unsupported
        raise Unsupported()"""

    get_journal_comment_metadata = """
        from .metadata import Metadata
        return Metadata(**self._journal_comment_metadata)"""

    set_journal_comment = """
        from .osid_errors import InvalidArgument, NullArgument, NoAccess
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

class OsidObjectForm:

    #inheritance = ['OsidObject']

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

    def _init_metadata(self):
        from . import mdata_conf
        from ..primitives import Id
        from ..primitives import DisplayText ## WHY?
        OsidForm._init_metadata(self)
        self._display_name_metadata = {
            'element_id': Id(authority = self._authority,
                             namespace = self._namespace,
                             identifier = 'display_name')}
        self._display_name_metadata.update(mdata_conf.display_name)
        self._description_metadata = {
            'element_id': Id(authority = self._authority,
                             namespace = self._namespace, 
                             identifier = 'description')}
        self._description_metadata.update(mdata_conf.description)
        self._genus_type_metadata = {
            'element_id': Id(authority = self._authority,
                             namespace = self._namespace, 
                             identifier = 'description')}
        self._genus_type_metadata.update(mdata_conf.genus_type)

    def _init_map(self):
        from . import profile
        self._my_map['displayName'] = dict(self._display_name_metadata['default_string_values'][0])
        self._my_map['description'] = dict(self._description_metadata['default_string_values'][0])
        self._my_map['genusTypeId'] = self._genus_type_metadata['default_type_values'][0]
        self._my_map['recordTypeIds'] = []

    def __getattr__(self, name):
        if '_records' in self.__dict__:
            for record in self._records:
                try:
                    return self._records[record][name]
                except AttributeError:
                    pass
        raise AttributeError()
"""

    get_display_name_metadata = """
        from .metadata import Metadata
        return Metadata(**self._display_name_metadata)"""

    set_display_name = """
        from .osid_errors import InvalidArgument, NullArgument, NoAccess
        if display_name is None:
            raise NullArgument()
        if self.get_display_name_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_string(display_name, 
                                     self.get_display_name_metadata()):
            raise InvalidArgument()
        self._my_map['displayName']['text'] = display_name"""

    clear_display_name = """
        from .osid_errors import NoAccess
        if (self.get_display_name_metadata().is_read_only() or
            self.get_display_name_metadata().is_required()):
            raise NoAccess()
        self._my_map['displayName'] = dict(self._display_name_metadata['default_object_values'][0])"""

    get_description_metadata = """
        from .metadata import Metadata
        return Metadata(**self._description_metadata)"""

    set_description = """
        from .osid_errors import InvalidArgument, NullArgument, NoAccess
        if description is None:
            raise NullArgument()
        if self.get_description_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_string(description, 
                                     self.get_description_metadata()):
            raise InvalidArgument()
        self._my_map['description']['text'] = description"""

    clear_description = """
        from .osid_errors import NoAccess
        if (self.get_description_metadata().is_read_only() or
            self.get_description_metadata().is_required()):
            raise NoAccess()
        self._my_map['description'] = dict(self._description_metadata['default_object_values'][0])"""

    get_genus_type_metadata = """
        from .metadata import Metadata
        return Metadata(**self._genus_type_metadata)"""

    set_genus_type = """
        from .osid_errors import InvalidArgument, NullArgument, NoAccess
        if genus_type is None:
            raise NullArgument()
        if self.get_genus_type_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_type(genus_type):
            raise InvalidArgument()
        self._my_map['genusTypeId'] = str(genus_type)"""

    clear_genus_type = """
        from .osid_errors import NoAccess
        if (self.get_genus_type_metadata().is_read_only() or
            self.get_genus_type_metadata().is_required()):
            raise NoAccess()
        self._my_map['genusType'] = self._genus_type_metadata['default_type_values'][0]"""
        

class OsidList:

    init = """
    def __init__(self, iter_object = [], count = None):
        if count != None:
            self._count = count
        elif isinstance(iter_object, dict) or isinstance(iter_object, list):
            self._count = len(iter_object)
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
            return true"""

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

    init = """
    def __init__(self, **kwargs):
        self._kwargs = kwargs
"""

    get_element_id_template = """
        # Implemented from template for osid.Metadata.get_element_id_template
        return self._kwargs['${var_name}']"""

    get_minimum_cardinal_template = """
        # Implemented from template for osid.Metadata.get_minimum_cardinal
        from .osid_errors import IllegalState
        if self._kwargs['syntax'] not in ${syntax_list}:
            raise IllegalState()
        else:
            return self._kwargs['${var_name}']"""

    supports_coordinate_type_template = """
        # Implemented from template for osid.Metadata.supports_coordinate_type
        from .osid_errors import IllegalState, NullArgument
        if not ${arg0_name}:
            raise NullArgument('no input Type provided')
        if self._kwargs['syntax'] not in ${syntax_list}:
            raise IllegalState('put more meaninful message here')
        return ${arg0_name} in self.get_${var_name}"""
