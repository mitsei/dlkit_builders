
class TypeProfile:

    supports_type_lookup = """
        from . import profile
        return 'supports_type_lookup' in profile.SUPPORTS"""

    supports_type_admin = """
        from . import profile
        return 'supports_type_admin' in profile.SUPPORTS"""


class TypeManager:

    get_type_lookup_session = """
        from ..osid.osid_errors import OperationFailed, Unimplemented
        if not self.supports_type_lookup():
            raise Unimplemented()
        try:
            from . import sessions
        except ImportError:
            raise OperationFailed()
        try:
            session = sessions.TypeLookupSession()
        except AttributeError:
            raise OperationFailed()
        return session"""

    get_type_admin_session = """
        from ..osid.osid_errors import OperationFailed, Unimplemented
        if not self.supports_type_admin():
            raise Unimplemented()
        try:
            from . import sessions
        except ImportError:
            raise OperationFailed()
        try:
            session = sessions.TypeAdminSession()
        except AttributeError:
            raise OperationFailed()
        return session"""


class TypeLookupSession:

    init = """
    def __init__(self, *args, **kwargs):
        from pymongo import MongoClient
        from .primitives import Type
        from ..osid.sessions import OsidSession
        from ..osid.osid_errors import NotFound
        OsidSession.__init__(self, *args, **kwargs)
        client = MongoClient()
        self._db = client['type']
"""

    can_lookup_types = """
        return True"""

    get_type = """
        from .primitives import Type
        from ..osid.osid_errors import NotFound, NullArgument, OperationFailed, PermissionDenied
        if namespace is None and identifier is None and authority is None:
            raise NullArgument()
        collection = self._db['Type']
        result = collection.find_one({'$and': [{'namespace': namespace},
                                               {'identifier': identifier},
                                               {'authority': authority}]})
        if result is None:
            raise NotFound()
        return Type(result)"""

    get_types = """
        from .objects import TypeList
        from ..osid.osid_errors import OperationFailed, PermissionDenied
        collection = self._db['Type']
        result = collection.find()
        count = collection.count()
        return TypeList(result, count)"""


class TypeAdminSession:

    init = """
    def __init__(self, catalog_identifier = None, *args, **kwargs):
        from pymongo import MongoClient
        from ..osid.sessions import OsidSession
        from ..osid.osid_errors import NotFound
        OsidSession.__init__(self, *args, **kwargs)
        self._forms = dict()
        client = MongoClient()
        self._db = client['type']
    """

    can_create_types = """
        return True"""

    get_type_form_for_create = """
        from ...abstract_osid.type.primitives import Type as ABCType
        from .objects import TypeForm
        from ..osid.osid_errors import NullArgument, InvalidArgument, OperationFailed, PermissionDenied, Unsupported, AlreadyExists
#        from bson.objectid import ObjectId
        collection = self._db['Type']
        CREATED = True
        if type_ is None:
            raise NullArgument()
        if not isinstance(type_, ABCType):
            raise InvalidArgument('argument is not a Type')
        result = collection.find_one({'$and': [{'namespace': type_.get_identifier_namespace()},
                                                {'identifier': type_.get_identifier()},
                                                {'authority': type_.get_authority()}]})
        if result is not None:
            raise AlreadyExists()
        form = TypeForm(type_=type_, update=False)
        form._for_update = False
        self._forms[form.get_id().get_identifier()] = not CREATED
        return form"""

    create_type = """
        from ...abstract_osid.type.objects import TypeForm as ABCTypeForm
        from ..osid.osid_errors import IllegalState, InvalidArgument, NullArgument, OperationFailed, PermissionDenied, Unsupported
        collection = self._db['Type']
        CREATED = True
        if type_form is None:
            raise NullArgument()
        if not isinstance(type_form, ABCTypeForm):
            raise InvalidArgument('argument type is not a TypeForm')
        if type_form.is_for_update():
            raise InvalidArgument('the TypeForm is for update only, not create')
        try:
            if self._forms[type_form.get_id().get_identifier()] == CREATED:
                raise IllegalState('type_form already used in a create transaction')
        except KeyError:
            raise Unsupported('type_form did not originate from this session')
        if not type_form.is_valid():
            raise InvalidArgument('one or more of the form elements is invalid')
        try:
            id_ = collection.insert(type_form._my_map)
        except: # what exceptions does mongodb insert raise?
            raise OperationFailed()
        from .primitives import Type
        self._forms[type_form.get_id().get_identifier()] = CREATED
        return Type(collection.find_one({'_id': id_}))"""

    can_update_types = """
        return True"""

    can_update_type = """
        return True"""

    get_type_form_for_update = """
        from ...abstract_osid.type.primitives import Type as ABCType
        from .objects import TypeForm
        from .primitives import Type
        from ..osid.osid_errors import NotFound, NullArgument, InvalidArgument, OperationFailed, PermissionDenied, Unsupported
#        from bson.objectid import ObjectId
        collection = self._db['Type']
        UPDATED = True
        if type_ is None:
            raise NullArgument()
        if not isinstance(type_, ABCType):
            return InvalidArgument('the argument is not a valid OSID Type')
        result = collection.find_one({'$and': [{'namespace': type_.get_identifier_namespace()},
                                                {'identifier': type_.get_identifier()},
                                                {'authority': type_.get_authority()}]})
        if result is None:
            raise NotFound()
        type_form = TypeForm(type_=Type(result), update=True)
        self._forms[type_form.get_id().get_identifier()] = not UPDATED
        return type_form"""

    update_type = """
        from ...abstract_osid.type.objects import TypeForm as ABCTypeForm
        from ..osid.osid_errors import IllegalState, InvalidArgument, NullArgument, OperationFailed, PermissionDenied, Unsupported
        collection = self._db['Type']
        UPDATED = True
        if type_form is None:
            raise NullArgument()
        if not isinstance(type_form, ABCTypeForm):
            raise InvalidArgument('argument type is not an TypeForm')
        if not type_form.is_for_update():
            raise InvalidArgument('the TypeForm is for update only, not create')
        try:
            if self._forms[type_form.get_id().get_identifier()] == UPDATED:
                raise IllegalState('type_form already used in an update transaction')
        except KeyError:
            raise Unsupported('type_form did not originate from this session')
        if not type_form.is_valid():
            raise InvalidArgument('one or more of the form elements is invalid')
        try:
            result = collection.save(type_form._my_map)
        except: # what exceptions does mongodb save raise?
            raise OperationFailed()
        self._forms[type_form.get_id().get_identifier()] = UPDATED"""

    can_delete_types = """
        return True"""

    can_delete_type = """
        return True"""

    delete_type = """
        from ...abstract_osid.type.primitives import Type as ABCType
        from ..osid.osid_errors import NotFound, NullArgument, InvalidArgument, OperationFailed, PermissionDenied, Unsupported
        from bson.objectid import ObjectId
        collection = self._db['Type']
        UPDATED = True
        if type_ is None:
            raise NullArgument()
        if not isinstance(type_, ABCType):
            return InvalidArgument('the argument is not a valid OSID Type')
        result = collection.remove({'$and': [{'namespace': type_.get_identifier_namespace()},
                                              {'identifier': type_.get_identifier()},
                                              {'authority': type_.get_authority()}]})
                                              # Tried using justOne above but pymongo doesn't support it
        if result['err'] is not None:
            raise OperationFailed()
        if result['n'] == 0:
            raise NotFound()
"""


class TypeForm:

    init = """
    def __init__(self, type_=None, update=False):
        from ..osid.objects import OsidForm
        OsidForm.__init__(self)
        self._init_metadata()
        self._my_map = {}
        self._init_map()
        self._my_map['authority'] = type_.get_authority()
        self._my_map['namespace'] = type_.get_identifier_namespace()
        self._my_map['identifier'] = type_.get_identifier()
        self._my_map['displayName']['text'] = type_.get_display_name().get_text()
        self._my_map['displayLabel']['text'] = type_.get_display_label().get_text()
        self._my_map['description']['text'] = type_.get_description().get_text()
        self._my_map['domain']['text'] = type_.get_domain().get_text()
        self._for_update = update
        

    def _init_metadata(self):
        from . import mdata_conf
        from ..primitives import Id
        from ..osid.objects import OsidForm
        OsidForm._init_metadata(self)
        self._display_name_metadata = {
            'element_id': Id(authority = self._authority,
                             namespace = self._namespace,
                             identifier = 'display_name')}
        self._display_name_metadata.update(mdata_conf.display_name)
        self._display_label_metadata = {
            'element_id': Id(authority = self._authority,
                             namespace = self._namespace, 
                             identifier = 'description')}
        self._display_label_metadata.update(mdata_conf.display_label)
        self._description_metadata = {
            'element_id': Id(authority = self._authority,
                             namespace = self._namespace, 
                             identifier = 'description')}
        self._description_metadata.update(mdata_conf.description)
        self._domain_metadata = {
            'element_id': Id(authority = self._authority,
                             namespace = self._namespace, 
                             identifier = 'description')}
        self._domain_metadata.update(mdata_conf.domain)

    def _init_map(self):
        from . import profile
        self._my_map['displayName'] = self._display_name_metadata['default_string_values'][0]
        self._my_map['displayLabel'] = self._display_label_metadata['default_string_values'][0]
        self._my_map['description'] = self._description_metadata['default_string_values'][0]
        self._my_map['domain'] = self._domain_metadata['default_string_values'][0]
"""

    get_display_name_metadata = """
        from ..osid.metadata import Metadata
        return Metadata(**self._display_name_metadata)"""

    set_display_name = """
        from ..osid.osid_errors import InvalidArgument, NullArgument, NoAccess
        if display_name is None:
            raise NullArgument()
        if self.get_display_name_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_string(display_name, 
                                     self.get_display_name_metadata()):
            raise InvalidArgument()
        self._my_map['displayName']['text'] = display_name"""

    clear_display_name = """
        from ..osid.osid_errors import NoAccess
        if (self.get_display_name_metadata().is_read_only() or
            self.get_display_name_metadata().is_required()):
            raise NoAccess()
        self._my_map['displayName'] = self._display_name_metadata['default_string_values'][0]"""

    get_display_label_metadata = """
        from ..osid.metadata import Metadata
        return Metadata(**self._display_label_metadata)"""

    set_display_label = """
        from ..osid.osid_errors import InvalidArgument, NullArgument, NoAccess
        if display_label is None:
            raise NullArgument()
        if self.get_display_label_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_string(display_label, 
                                     self.get_display_label_metadata()):
            raise InvalidArgument()
        self._my_map['displayLabel']['text'] = display_label"""

    clear_display_label = """
        from ..osid.osid_errors import NoAccess
        if (self.get_display_label_metadata().is_read_only() or
            self.get_display_label_metadata().is_required()):
            raise NoAccess()
        self._my_map['displayLabel'] = self._display_label_metadata['default_string_values'][0]"""

    get_description_metadata = """
        from ..osid.metadata import Metadata
        return Metadata(**self._description_metadata)"""

    set_description = """
        from ..osid.osid_errors import InvalidArgument, NullArgument, NoAccess
        if description is None:
            raise NullArgument()
        if self.get_description_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_string(description, 
                                     self.get_description_metadata()):
            raise InvalidArgument()
        self._my_map['description']['text'] = description"""

    clear_description = """
        from ..osid.osid_errors import NoAccess
        if (self.get_description_metadata().is_read_only() or
            self.get_description_metadata().is_required()):
            raise NoAccess()
        self._my_map['description'] = self._description_metadata['default_string_values'][0]"""

    get_domain_metadata = """
        from ..osid.metadata import Metadata
        return Metadata(**self._domain_metadata)"""

    set_domain = """
        from ..osid.osid_errors import InvalidArgument, NullArgument, NoAccess
        if domain is None:
            raise NullArgument()
        if self.get_domain_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_string(domain, 
                                     self.get_domain_metadata()):
            raise InvalidArgument()
        self._my_map['domain']['text'] = domain"""

    clear_description = """
        from ..osid.osid_errors import NoAccess
        if (self.get_domain_metadata().is_read_only() or
            self.get_domain_metadata().is_required()):
            raise NoAccess()
        self._my_map['domain'] = self._domain_metadata['default_string_values'][0]"""


class TypeList:

    get_next_type = """
        import sys
        from ..osid.osid_errors import IllegalState, OperationFailed
        try:
            next_item = self.next()
        except StopIteration:
            raise IllegalState('no more elements available in this list')
        except: #Need to specify exceptions here
            raise OperationFailed()
        else:
            return next_item
            
    def next(self):
        from ..osid.objects import OsidList
        from .primitives import Type 
        try:
            next_item = OsidList.next(self)
        except:
            raise
        if isinstance(next_item, dict):
            next_item = Type(next_item)
        return next_item

    next_type = property(fget=get_next_type)"""

    get_next_types = """
        import sys
        from ..osid.osid_errors import IllegalState, OperationFailed
        if n > self.available():
            # !!! This is not quite as specified (see method docs) !!!
            raise IllegalState('not enough elements available in this list')
        else:
            next_list = []
            x = 0
            while x < n:
                try:
                    next_list.append(self.next())
                except: #Need to specify exceptions here
                    raise OperationFailed()
                x = x + 1
            return next_list"""

class Type:

    init = """
    def __init__(self, type_map=None,
                       identifier=None,
                       authority=None,
                       namespace=None,
                       display_name=None,
                       display_label=None,
                       description=None,
                       domain=None):
        if type_map is not None:
            self._my_map = type_map
        elif (authority is not None and namespace is not None and identifier is not None and
            display_name is not None and description is not None and domain is not None):
            self._my_map = {}
            self._my_map['authority'] = authority
            self._my_map['namespace'] = namespace
            self._my_map['identifier'] = identifier
            self._my_map['displayName'] = self.display_text_map(display_name)
            self._my_map['displayLabel'] = self.display_text_map(display_label)
            self._my_map['description'] = self.display_text_map(description)
            self._my_map['domain'] = self.display_text_map(domain)
        else:
            raise NullArgument()
    
    def display_text_map(self, string):
        from .profile import LANGUAGETYPE, SCRIPTTYPE, FORMATTYPE
        from ..primitives import Id
        language_type_str = str(Id(**LANGUAGETYPE))
        script_type_str = str(Id(**SCRIPTTYPE))
        format_type_str = str(Id(**FORMATTYPE))
        return {'text': string,
                'languageTypeId': language_type_str,
                'scriptTypeId': script_type_str,
                'formatTypeId': format_type_str}
"""

    get_authority = """
        return self._my_map['authority']"""

    get_identifier_namespace = """
        return self._my_map['namespace']"""

    get_identifier = """
        return self._my_map['identifier']"""

    get_display_name = """
        from ..primitives import DisplayText
        return DisplayText(self._my_map['displayName'])"""

    get_display_label = """
        from ..primitives import DisplayText
        return DisplayText(self._my_map['displayLabel'])"""

    get_description = """
        from ..primitives import DisplayText
        return DisplayText(self._my_map['description'])"""

    get_domain = """
        from ..primitives import DisplayText
        return DisplayText(self._my_map['domain'])"""


class OldObsoleteTypeCanBeDeleted:

    init = """
    def __init__(self, type_map=None,
                       identifier=None,
                       authority=None,
                       namespace=None,
                       display_name=None,
                       display_label=None,
                       description=None,
                       domain=None):
        if type_map is not None:
            from .. import types
        elif (authority is not None and namespace is not None and identifier is not None and
            display_name is not None and description is not None and domain is not None):
            self._authority = authority
            self._namespace = namespace
            self._identifier = identifier
            self._display_name = display_name
            self._display_label = display_label
            self._description = description
            self._domain = domain
        else:
            raise NullArgument()
"""

    get_authority = """
        return self._authority"""

    get_identifier_namespace = """
        return self._namespace"""

    get_identifier = """
        return self._identifier"""

    get_display_name = """
        from ..primitives import DisplayText
        return DisplayText(text = self._display_name,
                           language_type = Type(**types.Language().get_type_data('DEFAULT')),
                           script_type = Type(**types.Script().get_type_data('DEFAULT')),
                           format_type = Type(**types.Format().get_type_data('DEFAULT')))"""

    get_display_label = """
        from ..primitives import DisplayText
        return DisplayText(text = self._display_label,
                           language_type = Type(**types.Language().get_type_data('DEFAULT')),
                           script_type = Type(**types.Script().get_type_data('DEFAULT')),
                           format_type = Type(**types.Format().get_type_data('DEFAULT')))"""

    get_description = """
        from ..locale.primitives import DisplayText
        return DisplayText(text = self._description,
                           language_type = Type(**types.Language().get_type_data('DEFAULT')),
                           script_type = Type(**types.Script().get_type_data('DEFAULT')),
                           format_type = Type(**types.Format().get_type_data('DEFAULT')))"""

    get_domain = """
        from ..primitives import DisplayText
        return DisplayText(text = self._domain,
                           language_type = Type(**types.Language().get_type_data('DEFAULT')),
                           script_type = Type(**types.Script().get_type_data('DEFAULT')),
                           format_type = Type(**types.Format().get_type_data('DEFAULT')))"""

