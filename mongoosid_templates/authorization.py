
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
        self._kwargs = kwargs

    def _get_qualifier_idstrs(self, qualifier_id):
        try:
            authority = qualifier_id.get_identifier_namespace().split('.')[0].upper()
            identifier = qualifier_id.get_identifier_namespace().split('.')[1].upper()
        except:
            return [str(qualifier_id)]
        root_qualifier_id = Id(
            authority=qualifier_id.get_authority(),
            namespace=qualifier_id.get_identifier_namespace(),
            identifier='ROOT')
        if qualifier_id.get_identifier() == 'ROOT':
            return [str(root_qualifier_id)]
        hierarchy_mgr = self._get_provider_manager('HIERARCHY') # local=True ???
        hierarchy_session = hierarchy_mgr.get_hierarchy_traversal_session_for_hierarchy(
            Id(authority=authority,
               namespace='CATALOG',
               identifier=identifier),
             proxy=self._proxy)
        node = hierarchy_session.get_nodes(qualifier_id, 10, 0, False)
        return self._get_ancestor_idstrs(node) + [str(root_qualifier_id)]

    def _get_ancestor_idstrs(self, node):
        node_list = [str(node.get_id())]
        if node.has_parents():
            for parent_node in node.get_parents():
                node_list = node_list + self._get_ancestor_idstrs(parent_node)
        return node_list
"""

    can_access_authorizations = """
        return True"""

    is_authorized = """
        collection = MongoClientValidated('authorization',
                                          collection='Authorization',
                                          runtime=self._runtime)
        # NOTE: For now this only checks basic authorizations. It should
        # to be extended to deal with Resources and QualifierHierarchies
        #print 'AGENT ID=', str(agent_id)
        #print '    FUNCTION ID=', str(function_id)
        #print '    QUAL ID STRINGS=', self._get_qualifier_idstrs(qualifier_id)
        try:
            collection.find_one(
                {'agentId': str(agent_id),
                 'functionId': str(function_id),
                 'qualifierId': {'$in': self._get_qualifier_idstrs(qualifier_id)}})
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
            ## WHY are we passing vault_id = self._catalog_id below, seems redundant:
            ## We probably also don't need to send agent_id. The form can now get that from the proxy
            obj_form = objects.AuthorizationForm(
                vault_id=self._catalog_id,
                agent_id=agent_id,
                function_id=function_id,
                qualifier_id=qualifier_id,
                catalog_id=self._catalog_id,
                runtime=self._runtime,
                proxy=self._proxy)
        else:
            obj_form = objects.AuthorizationForm(
                vault_id=self._catalog_id,
                record_types=authorization_record_types,
                agent_id=agent_id,
                function_id=function_id,
                qualifier_id=qualifier_id,
                catalog_id=self._catalog_id,
                runtime=self._runtime,
                proxy=self._proxy)
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
            ## WHY are we passing vault_id = self._catalog_id below, seems redundant:
            obj_form = objects.AuthorizationForm(
                vault_id=self._catalog_id,
                resource_id=resource_id,
                function_id=function_id,
                qualifier_id=qualifier_id,
                catalog_id=self._catalog_id,
                runtime=self._runtime,
                prox=self._proxy)
        else:
            obj_form = objects.AuthorizationForm(
                vault_id=self._catalog_id,
                record_types=authorization_record_types,
                resource_id=resource_id,
                function_id=function_id,
                qualifier_id=qualifier_id,
                catalog_id=self._catalog_id,
                runtime=self._runtime,
                proxy=self._proxy)
        obj_form._for_update = False
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form
"""

class AuthorizationForm:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..osid import objects as osid_objects',
    ]

    init = """
    _namespace = 'authorization.Authorization'

    def __init__(self, **kwargs):
        osid_objects.OsidRelationshipForm.__init__(self, object_name='AUTHORIZATION', **kwargs)
        self._mdata = default_mdata.get_authorization_mdata() # Don't know if we need default mdata for this
        self._init_metadata(**kwargs)

        # self._records = dict()
        # self._supported_record_type_ids = []
        # if osid_object_map is not None:
        #     self._for_update = True
        #     self._my_map = osid_object_map
        #     self._load_records(osid_object_map['recordTypeIds'])
        # else:
        #     self._my_map = {}
        #     self._for_update = False
        #     self._init_map(**kwargs)

        if not self.is_for_update():
            self._init_map(**kwargs)

    def _init_metadata(self, **kwargs):
        \"\"\"Initialize form metadata\"\"\"
        osid_objects.OsidRelationshipForm._init_metadata(self, **kwargs)

    def _init_map(self, record_types=None, **kwargs):
        \"\"\"Initialize form map\"\"\"
        osid_objects.OsidRelationshipForm._init_map(self, record_types=record_types)
        self._my_map['assignedVaultIds'] = [str(kwargs['vault_id'])]
        self._my_map['functionId'] = str(kwargs['function_id'])
        self._my_map['qualifierId'] = str(kwargs['qualifier_id'])
        if 'agent_id' in kwargs:
            self._my_map['agentId'] = str(kwargs['agent_id'])
        if 'resource_id' in kwargs:
            self._my_map['resourceId'] = str(kwargs['resource_id'])"""


class Authorization:
    additional_methods = """
    def get_object_map(self):
        obj_map = dict(self._my_map)
        if obj_map['startDate'] is not None:
            start_date = obj_map['startDate']
            obj_map['startDate'] = dict()
            obj_map['startDate']['year'] = start_date.year
            obj_map['startDate']['month'] = start_date.month
            obj_map['startDate']['day'] = start_date.day
            obj_map['startDate']['hour'] = start_date.hour
            obj_map['startDate']['minute'] = start_date.minute
            obj_map['startDate']['second'] = start_date.second
            obj_map['startDate']['microsecond'] = start_date.microsecond
        if obj_map['endDate'] is not None:
            end_date = obj_map['endDate']
            obj_map['endDate'] = dict()
            obj_map['endDate']['year'] = end_date.year
            obj_map['endDate']['month'] = end_date.month
            obj_map['endDate']['day'] = end_date.day
            obj_map['endDate']['hour'] = end_date.hour
            obj_map['endDate']['minute'] = end_date.minute
            obj_map['endDate']['second'] = end_date.second
            obj_map['endDate']['microsecond'] = end_date.microsecond
        return osid_objects.OsidObject.get_object_map(self, obj_map)

    object_map = property(fget=get_object_map)
    """

class AuthorizationQuery:
    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
    ]

    init = """
    def __init__(self, runtime):
        self._namespace = 'authorization.Authorization'
        self._runtime = runtime
        record_type_data_sets = get_registry('AUTHORIZATION_RECORD_TYPES', runtime)
        self._all_supported_record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_ids = []
        for data_set in record_type_data_sets:
            self._all_supported_record_type_ids.append(str(Id(**record_type_data_sets[data_set])))
        osid_queries.OsidObjectQuery.__init__(self, runtime)
"""

    match_agent_id = """
        self._add_match('agentId', str(agent_id), bool(match))"""

    match_function_id = """
        self._add_match('functionId', str(function_id), bool(match))"""

    match_qualifier_id = """
        self._add_match('qualifierId', str(qualifier_id), bool(match))"""

class VaultLookupSession:
    get_vaults_by_genus_type = """
        collection = MongoClientValidated('authorization',
                                          collection='Vault',
                                          runtime=self._runtime)
        result = collection.find({'genusTypeId': {'$in': [str(vault_genus_type)]}}).sort('_id', DESCENDING)

        return objects.VaultList(result, runtime=self._runtime)"""