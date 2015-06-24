
class AuthorizationSession:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from ..osid.sessions import OsidSession',
        'from ..utilities import MongoClientValidated',
        'from . import objects',
    ]

    init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        self._catalog_class = objects.Vault
        self._session_name = 'AuthorizationSession'
        self._catalog_name = 'Vault'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='authorization',
            cat_name='Vault',
            cat_class=objects.Vault)
        self._object_view = COMPARATIVE
        self._catalog_view = ISOLATED
        self._kwargs = kwargs
"""

    can_access_authorizations = """
        return True"""

    is_authorized = """
        collection = MongoClientValidated(self._db_prefix + 'authorization',
                                          collection='Authorization',
                                          runtime=self._runtime)
        # NOTE: For now this only checks basic authorizations. It should
        # to be extended to deal with Resources and QualifierHierarchies
        try:
            collection.find_one({'agentId': str(agent_id),
                                 'functionId': str(function_id),
                                 'qualifierId': str(qualifier_id)})
        except errors.NotFound:
            return False
        else:
            return True"""

class AuthorizationAdminSession:

    import_statements = [
        'from dlkit.abstract_osid.id.primitives import Id as ABCId',
        'from dlkit.abstract_osid.type.primitives import Type as ABCType',
]

    get_authorization_form_for_create_for_agent = """
        if not isinstance(agent_id, ABCId):
            raise errors.InvalidArgument('argument is not a valid OSID Id')
        if not isinstance(function_id, ABCId):
            raise errors.InvalidArgument('argument is not a valid OSID Id')
        if not isinstance(qualifier_id, ABCId):
            raise errors.InvalidArgument('argument is not a valid OSID Id')
        for arg in authorization_record_types:
            if not isinstance(arg, ABCType):
                raise errors.InvalidArgument('one or more argument array elements is not a valid OSID Type')
        if authorization_record_types == []:
            ## WHY are we passing family_id = self._catalog_id below, seems redundant:
            obj_form = objects.AuthorizationForm(
                vault_id=self._catalog_id,
                agent_id=agent_id,
                function_id=function_id,
                qualifier_id=qualifier_id,
                catalog_id=self._catalog_id,
                db_prefix=self._db_prefix,
                runtime=self._runtime)
        else:
            obj_form = objects.AuthorizationForm(
                vault_id=self._catalog_id,
                record_types=relationship_record_types,
                agent_id=agent_id,
                function_id=function_id,
                qualifier_id=qualifier_id,
                catalog_id=self._catalog_id,
                db_prefix=self._db_prefix,
                runtime=self._runtime)
        obj_form._for_update = False
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form
"""

    get_authorization_form_for_create_for_resource = """
        if not isinstance(resource_id, ABCId):
            raise errors.InvalidArgument('argument is not a valid OSID Id')
        if not isinstance(function_id, ABCId):
            raise errors.InvalidArgument('argument is not a valid OSID Id')
        if not isinstance(qualifier_id, ABCId):
            raise errors.InvalidArgument('argument is not a valid OSID Id')
        for arg in authorization_record_types:
            if not isinstance(arg, ABCType):
                raise errors.InvalidArgument('one or more argument array elements is not a valid OSID Type')
        if authorization_record_types == []:
            ## WHY are we passing family_id = self._catalog_id below, seems redundant:
            obj_form = objects.AuthorizationForm(
                vault_id=self._catalog_id,
                resource_id=resource_id,
                function_id=function_id,
                qualifier_id=qualifier_id,
                catalog_id=self._catalog_id,
                db_prefix=self._db_prefix,
                runtime=self._runtime)
        else:
            obj_form = objects.AuthorizationForm(
                vault_id=self._catalog_id,
                record_types=relationship_record_types,
                resource_id=resource_id,
                function_id=function_id,
                qualifier_id=qualifier_id,
                catalog_id=self._catalog_id,
                db_prefix=self._db_prefix,
                runtime=self._runtime)
        obj_form._for_update = False
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form
"""


class AuthorizationForm:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from . import objects',
    ]

    init = """
    try:
        #pylint: disable=no-name-in-module
        from ..records.types import AUTHORIZATION_RECORD_TYPES as _record_type_data_sets
    except (ImportError, AttributeError):
        _record_type_data_sets = dict()
    _namespace = 'authorization.Authorization'

    def __init__(self, osid_object_map=None, record_types=None, db_prefix='', runtime=None, **kwargs):
        osid_objects.OsidForm.__init__(self)
        self._runtime = runtime
        self._db_prefix = db_prefix
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
        osid_objects.OsidRelationshipForm._init_metadata(self, **kwargs)

    def _init_map(self, **kwargs):
        osid_objects.OsidRelationshipForm._init_map(self)
        self._my_map['vaultId'] = str(kwargs['vault_id'])
        self._my_map['functionId'] = str(kwargs['function_id'])
        self._my_map['qualifierId'] = str(kwargs['qualifier_id'])
        if 'agent_id' in kwargs:
            self._my_map['agentId'] = str(kwargs['agent_id'])
        if 'resource_id' in kwargs:
            self._my_map['resourceId'] = str(kwargs['resource_id'])
"""