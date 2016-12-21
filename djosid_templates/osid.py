
class OsidProfile:

    get_id = """
        from . import profile
        from ..id.primitives import Id
        return Id(**profile.ID)
        """

    get_display_name = """
        from . import profile
        try:
            from ..locale.primitives import DisplayText
        except:
            from .common import DisplayText
        return DisplayText(profile.DISPLAYNAME,
                           profile.LANGUAGETYPE['identifier'],
                           profile.SCRIPTTYPE['identifier'],
                           profile.FORMATTYPE['identifier'])"""

    get_description = """
        from . import profile
        try:
            from ..locale.primitives import DisplayText
        except:
            from .common import DisplayText
        return DisplayText(profile.DESCRIPTION,
                           profile.LANGUAGETYPE['identifier'],
                           profile.SCRIPTTYPE['identifier'],
                           profile.FORMATTYPE['identifier'])"""

    get_version = """
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
    _authority = 'birdland.mit.edu'
"""

    get_id = """
        try:
            from ..id.primitives import Id
        except:
            from .common import Id

        return Id(identifier = self.my_model.identifier,
                   namespace = self._namespace,
                   authority = self._authority)"""

    is_current = """
        # Osid Objects in this implementation can easily become stale
        return False"""


class Extensible:

    has_record_type = """
        # Someday I hope to have a real implementation
        return False"""

    get_record_types = """
        # Someday I, too, hope to have a real implementation
        from ..type.objects import TypeList
        return TypeList([])"""


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

    # This initter is temporary. Only exists to get user ID information 
    # For testing AuthZ. Eventually this will be replaces with Django session
    # stuff
    init = """

    COMPARATIVE = 0
    PLENARY = 1
    FEDERATED = 0
    ISOLATED = 1
    _session_name = 'OsidSession'

    def __init__(self):
        from django.contrib.auth import authenticate
        from django.contrib.auth.models import AnonymousUser
        from .settings import USERNAME, PASSWORD
        self._user = authenticate(username=USERNAME, password=PASSWORD)
        if self._user is not None:
            # the password verified for the user
            if self._user.is_active:
                print(self._session_name + ': User \\'' + USERNAME + '\\' is valid, active and authenticated.')
            else:
                print(self._session_name + ': The password is valid, but the account has been disabled!')
        else:
            # the authentication system was unable to verify the username and password
            print(self._session_name + ': The username and password were incorrect.')
            self._user = AnonymousUser()
    """

    get_locale = """
        from ..locale.objects import Locale
        ##
        # This implementation assumes that instantiating a new Locale
        # without constructor arguments wlll return the default Locale.
        return Locale()"""

    is_authenticated = """
        return self._user.is_authenticated()"""

    get_authenticated_agent_id = """
        from ..authentication.objects import Agent
        from .osid_errors import IllegalState
        if not self.is_authenticated:
            raise IllegalState()
        return Agent(self._user).get_id()"""  

    get_authenticated_agent = """
        from ..authentication.objects import Agent
        from .osid_errors import IllegalState, OperationFailed
        if not self.is_authenticated:
            raise IllegalState()
        try:
            return Agent(self._user)
        except:
            raise OperationFailed()"""

    get_effective_agent_id = """
        from ..authentication.objects import Agent
        if self.is_authenticated():
            return self.get_authenticated_agent_id()
        else:
            return Agent(self._user).get_id()"""

    get_effective_agent = """
        from ..authentication.objects import Agent
        from .osid_errors import OperationFailed
        try:
            return Agent(self._user)
        except:
            raise #OperationFailed()
        """

    supports_transactions = """
        return False"""

    startTransaction = """
        from .osid_errors import IllegalState, OperationFailed, Unsupported
        if not supports_transactions:
            raise Unsupported('transacstions ore not supported for this session')"""


class OsidObject:

    model = """
    from collections import OrderedDict
    from . import profile
    language_type_identifier = profile.LANGUAGETYPE['identifier']
    script_type_identifier = profile.SCRIPTTYPE['identifier']
    format_type_identifier = profile.FORMATTYPE['identifier']
    options = OrderedDict()
    moptions = OrderedDict()
    
    options['display_name'] = {
        'verbose_name': 'display name',
        'help_text': 'display name is required. enter no more than 128 characters',
        'blank': False,
        'default': 'no display name entered',
        'editable': True,
        'max_length': 128,
        'choices': OrderedDict(),
        }
    moptions['display_name'] = dict(options['display_name'])
    moptions['display_name'].update({
        'linked': False,
        'array': False,
        'syntax': 'STRING',
        'min_length': 0,
        'match_types': []
        })

    options['description'] = {
        'verbose_name': 'description',
        'help_text': 'enter no more than 256 characters',
        'blank': True,
        'default': '',
        'editable': True,
        'max_length': 256,
        'choices': OrderedDict(),
        }
    moptions['description'] = dict(options['description'])
    moptions['description'].update({
        'linked': False,
        'array': False,
        'syntax': 'STRING',
        'min_length': 0,
        'match_types': []
        })
    options['genus_type_authority'] = {
        'verbose_name': 'genus type authority',
        'help_text': '',
        'blank': False,
        'editable': True,
        'default': 'default',
        'max_length': 128,
        'choices': OrderedDict(),
        }
    options['genus_type_namespace'] = {
        'verbose_name': 'genus type namespace',
        'help_text': '',
        'blank': False,
        'editable': True,
        'default': 'default',
        'max_length': 128,
        'choices': OrderedDict(),
        }
    options['genus_type_identifier'] = {
        'verbose_name': 'genus type identifier',
        'help_text': '',
        'blank': False,
        'editable': True,
        'default': 'default',
        'max_length': 64,
        'choices': OrderedDict(),
        }
    moptions['genus_type'] = {
        'verbose_name': 'genus type',
        'help_text': 'accepts an osid.type.Type object',
        'blank': False,
        'editable': True,
        'syntax': 'TYPE',
        'type_set': [],
        }
    options['language_type_identifier'] = {
        'verbose_name': 'language type identifier',
        'help_text': '',
        'blank': False,
        'editable': True,
        'default': language_type_identifier,
        'max_length': 64,
        'choices': OrderedDict(),
        }
    options['script_type_identifier'] = {
        'verbose_name': 'script type identifier',
        'help_text': '',
        'blank': False,
        'editable': True,
        'default': script_type_identifier,
        'max_length': 64,
        'choices': OrderedDict(),
        }
    options['format_type_identifier'] = {
        'verbose_name': 'format type identifier',
        'help_text': '',
        'blank': False,
        'editable': True,
        'default': format_type_identifier,
        'max_length': 64,
        'choices': OrderedDict(),
        }

    identifier = models.AutoField(primary_key=True)
    display_name = models.CharField(**options['display_name'])
    description = models.CharField(**options['description'])
    genus_type_authority = models.CharField(**options['genus_type_authority'])
    genus_type_namespace = models.CharField(**options['genus_type_namespace'])
    genus_type_identifier = models.CharField(**options['genus_type_identifier'])
    language_type_identifier = models.CharField(**options['language_type_identifier'])
    script_type_identifier = models.CharField(**options['script_type_identifier'])
    format_type_identifier = models.CharField(**options['format_type_identifier'])
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return '' + str(self.display_name) + ' (identifier:' + str(self.identifier) + ')'
"""

    init = """
    _namespace = 'dj_osid.OsidObject'

    def __init__(self, osid_object_model):
        # Add type checking to this to see if I got a Model or OSID Object?
        self.my_model = osid_object_model
"""

    get_display_name = """
        try:
            from ..locale.primitives import DisplayText
        except:
            from .common import DisplayText
        return DisplayText(self.my_model.display_name,
               language_type_identifier = self.my_model.language_type_identifier,
               script_type_identifier = self.my_model.script_type_identifier,
               format_type_identifier = self.my_model.format_type_identifier)"""

    # Why did I make this a template too?
    get_display_name_template = """
        # Implemented from template for osid.OsidObject.getDisplayName
        try:
            from ..locale.primitives import DisplayText
        except:
            from .common import DisplayText
        return DisplayText(self.my_model.${var_name},
               language_type_identifier = self.my_model.language_type_identifier,
               script_type_identifier = self.my_model.script_type_identifier,
               format_type_identifier = self.my_model.format_type_identifier)"""

    get_description = """
        try:
            from ..locale.primitives import DisplayText
        except:
            from .common import DisplayText
        return DisplayText(self.my_model.description,
               language_type_identifier = self.my_model.language_type_identifier,
               script_type_identifier = self.my_model.script_type_identifier,
               format_type_identifier = self.my_model.format_type_identifier)"""


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
    _namespace = 'dj_osid.OsidForm'

    def __init__(self):
        import uuid
        self._identifier = str(uuid.uuid4())
        self._for_update = None

    def _init_metadata(self):
#        from .markers import Identifiable
        try:
            from ..id.primitives import Id
        except:
            from .common import Id
        try:
            from ..locale.primitives import DisplayText
        except:
            from .common import DisplayText
        self._comment = ''
        self._comment_metadata = {
            'element_id': Id(self._authority,
                             self._namespace,
                             'comment'),
             'element_label': DisplayText('Comment'),
             'instructions': DisplayText('Provide a brief comment.'),
             'required': False,
             'value': False,
             'read_only': False,
             'linked': False,
             'syntax': 'STRING',
             'array': False,
             'minimum_string_length': 0,   # Should these values come from 
             'maximum_string_length': 256} # a settings file somewhere?
        self._validation_messages = {}

    ##
    # Override get_id as implemented in Identifiable for the purpose of 
    # returning an Id unique to this form for submission purposed as 
    # recommended in the osid documentation. This implementation
    # substitutes the intialized Python uuid4 identifier, and the 
    # form namespace from the calling Osid Form thing.
    def get_id(self):
        try:
            from ..id.primitives import Id
        except:
            from .common import Id
        return Id(identifier = self._identifier,
                   namespace = self._namespace,
                   authority = self._authority)
                  
    ##
    # The _is_valid_input method takes two arguments, the user input to 
    # be checked and the associated _form metadata structure (not an osid.Metadata
    # object) that will store the  validation requirements.
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
        elif syntax == 'STRING':
            valid = self._is_valid_string(input, metadata)
        else:
            raise OperationFailed('no validation function available for ' + syntax)

        return valid 

    def _is_valid_id(self, input):
        from dlkit.abstract_osid.id.primitives import Id
        if isinstance(input, Id):
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
        if len(input) < metadata.get_minimum_string_length():
            return False
        elif len(input) > metadata.get_maximum_string_length():
            return False
        if (metadata.get_string_set() and
            input not in metadata.get_string_set()):
            return False
        else:
            return True
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

    get_comment_metadata = """
        from .metadata import Metadata
        return Metadata(**self._comment_metadata)"""

    set_comment = """
        from .osid_errors import InvalidArgument, NullArgument, NoAccess
        if comment is None:
            raise NullArgument()
        if self.get_comment_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_string(comment, 
                                     self.get_comment_metadata()):
            raise InvalidArgument()
        self._comment = comment"""

    is_valid = """
        from django.core.exceptions import ValidationError
        from .osid_errors import OperationFailed
        valid = True
        try:
            self.my_model.full_clean()
        except ValidationError as e:
            # change this to extract the error messages into DisplayTexts
            self._validation_messages = e.message_dict
            valid = False
        if not self._is_valid_string(self._comment, 
                                     self.get_comment_metadata()):
            self._validation_messages['comment'] = [u'Please enter a valid comment']
        return valid"""

    get_validation_messages = """
        self.is_valid()
        return self._validation_messages"""

    get_invalid_metadata = """
        self.is_valid()
        ## Need to change all metadata args to be held in instance attribute,
        ## Probably in a dict.
        return 'not yet implemented'"""

class OsidObjectForm:

    inheritance = ['OsidObject']

    init = """
    _namespace = "dj_osid.OsidObjectForm"

    ## In real world use this will never get called:
    def __init__(self, osid_object_model=False):
        OsidForm.__init__(self)
        if osid_object_model:
            self.my_model = osid_object_model
            self._for_update = True
        else:
            from .models import OsidObject as osid_object_model
            self.my_model = osid_object_model()
            self._for_update = False
            self._init_model()
        self._init_metadata()

    def _init_model(self):
        from . import profile
        self.my_model.language_type_identifier = profile.LANGUAGETYPE['identifier']
        self.my_model.script_type_identifier = profile.SCRIPTTYPE['identifier']
        self.my_model.format_type_identifier = profile.FORMATTYPE['identifier']
        self.my_model.genus_type_authority = 'birdland@mit.edu'
        self.my_model.genus_type_namespace = 'osid.OsidObject'
        self.my_model.genus_type_identifier = 'default'

    def _init_metadata(self):
        try:
            from ..id.primitives import Id
        except:
            from .common import Id
        try:
            from ..locale.primitives import DisplayText
        except:
            from .common import DisplayText
        OsidForm._init_metadata(self)
        self._display_name_metadata = {
            'element_id': Id(self._authority,
                             self._namespace,
                             'display_name'),
             'element_label': self.my_model.moptions['display_name']['verbose_name'],
             'instructions': DisplayText(self.my_model.moptions['display_name']['help_text']),
             'required': not self.my_model.moptions['display_name']['blank'],
             'value': bool(self.my_model.moptions['display_name']['default']),
             'read_only': not self.my_model.moptions['display_name']['editable'],
             'linked': self.my_model.moptions['display_name']['linked'],
             'syntax': self.my_model.moptions['display_name']['syntax'],
             'array': self.my_model.moptions['display_name']['array'],
             'minimum_string_length': self.my_model.moptions['display_name']['min_length'],
             'maximum_string_length': self.my_model.moptions['display_name']['max_length'],
             'string_set': self.my_model.moptions['display_name']['choices'],
             'string_match_types': self.my_model.moptions['display_name']['match_types']}

        self._description_metadata = {
            'element_id': Id(self._authority,
                             self._namespace,
                             'description'),
             'element_label': self.my_model.moptions['description']['verbose_name'],
             'instructions': DisplayText(self.my_model.moptions['description']['help_text']),
             'required': not self.my_model.moptions['description']['blank'],
             'value': bool(self.my_model.moptions['description']['default']),
             'read_only': not self.my_model.moptions['description']['editable'],
             'linked': self.my_model.moptions['description']['linked'],
             'syntax': self.my_model.moptions['description']['syntax'],
             'array': self.my_model.moptions['description']['array'],
             'minimum_string_length': self.my_model.moptions['description']['min_length'],
             'maximum_string_length': self.my_model.moptions['description']['max_length'],
             'string_set': self.my_model.moptions['description']['choices'],
             'string_match_types': self.my_model.moptions['description']['match_types']}
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
        self.my_model.display_name = display_name"""

    clear_display_name = """
        from .osid_errors import NoAccess
        if (self.get_display_name_metadata().is_read_only() or
            self.get_display_name_metadata().is_required()):
            raise NoAccess()
        self.my_model.display_name = ''"""

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
        self.my_model.description = description"""

    clear_description = """
        from .osid_errors import NoAccess
        if (self.get_description_metadata().is_read_only() or
            self.get_description_metadata().is_required()):
            raise NoAccess()
        self.my_model.description = ''"""


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

class Metadata:

    init = """
    def __init__(self, element_id,
                       element_label,
                       instructions = '', 
                       required = None, 
                       value = None, # has_value boolean
                       read_only = None, 
                       linked = None, 
                       syntax = None, 
                       array = None,
                       units = None, 
                       minimum_elements = None, 
                       maximum_elements = None, 
                       minimum_cardinal = None, 
                       maximum_cardinal = None, 
                       cardinal_set = [], 
                       coordinate_set = [], 
                       coordinate_types = [], 
                       axes_for_coordinate_type = None, 
                       minimum_coordinate_values = [], 
                       maximum_coordinate_values = [], 
                       minimum_currency = None, 
                       maximum_currency = None, 
                       currency_set = [], 
                       currency_types = [], 
                       minimum_date_time = None, 
                       maximum_date_time = None, 
                       date_time_set = [], 
                       date_time_resolution = None, 
                       calendar_types = [], 
                       time_types = [], 
                       minimum_decimal = None, 
                       maximum_decimal = None, 
                       decimal_set = [], 
                       decimal_scale = None, 
                       minimum_duration = None, 
                       maximum_duration = None, 
                       duration_set = [], 
                       duration_unit_types = [], 
                       minimum_distance = None, 
                       maximum_distance = None, 
                       distance_set = [], 
                       distance_resolution = None, 
                       heading_set = [], 
                       heading_types = [], 
                       axes_for_heading_type = None, 
                       minimum_heading_values = [], 
                       maximum_heading_values = [], 
                       minimum_integer = None, 
                       maximum_integer = None, 
                       integer_set = [], 
                       spatial_unit_set = [], 
                       patial_unit_record_types = [], 
                       minimum_speed = None, 
                       maximum_speed = None, 
                       speed_set = [], 
                       minimum_string_length = None, 
                       maximum_string_length = None, 
                       string_set = [], 
                       string_match_types = [], 
                       string_format = None, 
                       minimum_time = None, 
                       maximum_time = None, 
                       time_set = [], 
                       time_resolution = None, 
                       id_set = [], 
                       type_set = [], 
                       maximum_version = None, 
                       minimum_version = None, 
                       version_set = [], 
                       object_types = []):

        self._element_id = element_id
        self._element_label = element_label
        self._instructions = instructions
        self._required = required
        self._value = value # has_value boolean
        self._read_only = read_only
        self._linked = linked
        self._syntax = syntax
        self._array = array
        self._units = units
        self._minimum_elements = minimum_elements
        self._maximum_elements = maximum_elements
        self._minimum_cardinal = minimum_cardinal
        self._maximum_cardinal = maximum_cardinal
        self._cardinal_set = cardinal_set
        self._coordinate_set = coordinate_set
        self._coordinate_types = coordinate_types
        self._axes_for_coordinate_type = axes_for_coordinate_type # This may be algorithm
        self._minimum_coordinate_values = minimum_coordinate_values 
        self._maximum_coordinate_values = maximum_coordinate_values 
        self._minimum_currency = minimum_currency
        self._maximum_currency = maximum_currency
        self._currency_set = currency_set
        self._currency_types = currency_types
        self._minimum_date_time = minimum_date_time
        self._maximum_date_time = maximum_date_time
        self._date_time_set = date_time_set
        self._date_time_resolution = date_time_resolution
        self._calendar_types = calendar_types
        self._time_types = time_types
        self._minimum_decimal = minimum_decimal
        self._maximum_decimal = maximum_decimal
        self._decimal_set = decimal_set
        self._decimal_scale = decimal_scale
        self._minimum_duration = minimum_duration
        self._maximum_duration = maximum_duration
        self._duration_set = duration_set
        self._duration_unit_types = duration_unit_types
        self._minimum_distance = minimum_distance
        self._maximum_distance = maximum_distance
        self._distance_set = distance_set
        self._distance_resolution = distance_resolution
        self._heading_set = heading_set
        self._heading_types = heading_types
        self._axes_for_heading_type = axes_for_heading_type # This may be an algorithm
        self._minimum_heading_values = minimum_heading_values
        self._maximum_heading_values = maximum_heading_values
        self._minimum_integer = minimum_integer
        self._maximum_integer = maximum_integer
        self._integer_set = integer_set
        self._spatial_unit_set = spatial_unit_set
        self._patial_unit_record_types = patial_unit_record_types
        self._minimum_speed = minimum_speed
        self._maximum_speed = maximum_speed
        self._speed_set = speed_set
        self._minimum_string_length = minimum_string_length
        self._maximum_string_length = maximum_string_length
        self._string_set = string_set
        self._string_match_types = string_match_types
        self._string_format = string_format
        self._minimum_time = minimum_time
        self._maximum_time = maximum_time
        self._time_set = time_set
        self._time_resolution = time_resolution
        self._id_set = id_set
        self._type_set = type_set
        self._maximum_version = maximum_version
        self._minimum_version = minimum_version
        self._version_set = version_set
        self._object_types = object_types
"""

    get_element_id_template = """
        # Implemented from template for osid.Metadata.get_element_id_template
        return self._${var_name}"""

    get_minimum_cardinal_template = """
        # Implemented from template for osid.Metadata.get_minimum_cardinal
        from .osid_errors import IllegalState
        if self._syntax not in ${syntax_list}:
            raise IllegalState()
        else:
            return self._${var_name}"""

    supports_coordinate_type_template = """
        # Implemented from template for osid.Metadata.supports_coordinate_type
        from .osid_errors import IllegalState, NullArgument
        if not ${arg0_name}:
            raise NullArgument('no input Type provided')
        if self._syntax not in ${syntax_list}:
            raise IllegalState('put more meaninful message here')

        result = False
        if self.get.${var_name} != []:
            for t in self.get.${var_name}:
                if (t.get_authority == ${arg0_name}.get_authority and
                    t.get_identifier_namespace == ${arg0_name}.get_identifier_namespace and
                    t.get_identifier == ${arg0_name}.get_identifier):
                    result = True
        return result"""
