
class AuthorizationSession:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from ..osid.sessions import OsidSession',
        'from ..utilities import JSONClientValidated',
        'from . import objects'
    ]

    init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        self._catalog_class = objects.Vault
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

    # def _get_qualifier_idstrs(self, qualifier_id):
    #     def generate_qualifier_ids():
    #         try:
    #             authority = qualifier_id.get_identifier_namespace().split('.')[0].upper()
    #             identifier = qualifier_id.get_identifier_namespace().split('.')[1].upper()
    #         except:
    #             return [str(qualifier_id)]
    #         root_qualifier_id = Id(
    #             authority=qualifier_id.get_authority(),
    #             namespace=qualifier_id.get_identifier_namespace(),
    #             identifier='ROOT')
    #         if qualifier_id.get_identifier() == 'ROOT':
    #             return [str(root_qualifier_id)]
    #         hierarchy_mgr = self._get_provider_manager('HIERARCHY') # local=True ???
    #         hierarchy_session = hierarchy_mgr.get_hierarchy_traversal_session_for_hierarchy(
    #             Id(authority=authority,
    #                namespace='CATALOG',
    #                identifier=identifier),
    #                proxy=self._proxy)
    #         node = hierarchy_session.get_nodes(qualifier_id, 10, 0, False)
    #         return self._get_ancestor_idstrs(node) + [str(root_qualifier_id)]
    #     use_caching = False
    #     try:
    #         config = self._runtime.get_configuration()
    #         parameter_id = Id('parameter:useCachingForQualifierIds@mongo')
    #         if config.get_value_by_parameter(parameter_id).get_boolean_value():
    #             use_caching = True
    #         else:
    #             pass
    #     except (AttributeError, KeyError, errors.NotFound):
    #         pass
    #     if use_caching:
    #         import memcache
    #         mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    #
    #         key = 'hierarchy-qualifier-ids-{0}'.format(str(qualifier_id))
    #
    #         if mc.get(key) is None:
    #             qualifier_ids = generate_qualifier_ids()
    #             mc.set(key, qualifier_ids, time=30 * 60)
    #         else:
    #             qualifier_ids = mc.get(key)
    #     else:
    #         qualifier_ids = generate_qualifier_ids()
    #     return qualifier_ids
    #
    # def _get_ancestor_idstrs(self, node):
    #     def get_ancestors(internal_node):
    #         node_list = [str(internal_node.get_id())]
    #         if internal_node.has_parents():
    #             for parent_node in internal_node.get_parents():
    #                 node_list += self._get_ancestor_idstrs(parent_node)
    #         return list(set(node_list))
    #
    #     use_caching = False
    #     try:
    #         config = self._runtime.get_configuration()
    #         parameter_id = Id('parameter:useCachingForQualifierIds@json')
    #         if config.get_value_by_parameter(parameter_id).get_boolean_value():
    #             use_caching = True
    #         else:
    #             pass
    #     except (AttributeError, KeyError, errors.NotFound):
    #         pass
    #     if use_caching:
    #         import memcache
    #         mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    #
    #         key = 'ancestor-ids-{0}'.format(str(node.ident))
    #
    #         if mc.get(key) is None:
    #             ancestor_ids = get_ancestors(node)
    #             mc.set(key, ancestor_ids, time=30 * 60)
    #         else:
    #             ancestor_ids = mc.get(key)
    #     else:
    #         ancestor_ids = get_ancestors(node)
    #     return ancestor_ids

    def _get_hierarchy_session(self, hierarchy_id):
        \"\"\"Returns a hierarchy traversal session for the hierarchy\"\"\"
        hierarchy_mgr = self._get_provider_manager('HIERARCHY', local=True)
        return hierarchy_mgr.get_hierarchy_traversal_session_for_hierarchy(
            hierarchy_id,
            proxy=self._proxy)

    def _caching_enabled(self):
        \"\"\"Returns True if caching is enabled per configuration, false otherwise.\"\"\"
        try:
            config = self._runtime.get_configuration()
            parameter_id = Id('parameter:useCachingForQualifierIds@json')
            if config.get_value_by_parameter(parameter_id).get_boolean_value():
                return True
            else:
                return False
        except (AttributeError, KeyError, errors.NotFound):
            return False

    def _get_parent_id_list(self, qualifier_id, hierarchy_id):
        \"\"\"Returns list of parent id strings for qualifier_id in hierarchy.

        Uses memcache if caching is enabled.

        \"\"\"
        if self._caching_enabled():
            import memcache
            mc = memcache.Client(['127.0.0.1:11211'], debug=0)
            key = 'parent_id_list_{0}'.format(str(qualifier_id))
            parent_id_list = mc.get(key)
            if parent_id_list is None:
                parent_ids = self._get_hierarchy_session(hierarchy_id).get_parents(qualifier_id)
                parent_id_list = [str(parent_id) for parent_id in parent_ids]
                mc.set(key, parent_id_list)
        else:
            parent_ids = self._get_hierarchy_session(hierarchy_id).get_parents(qualifier_id)
            parent_id_list = [str(parent_id) for parent_id in parent_ids]
        return parent_id_list"""

    can_access_authorizations = """
        return True"""

    is_authorized = """
        collection = JSONClientValidated('authorization',
                                         collection='Authorization',
                                         runtime=self._runtime)

        def is_parent_authorized(catalog_id):
            \"\"\"Recursively checks parents for implicit authorizations\"\"\"
            parent_id_list = self._get_parent_id_list(catalog_id, hierarchy_id)
            if parent_id_list:
                try:
                    collection.find_one(
                        {'agentId': str(agent_id),
                         'functionId': str(function_id),
                         'qualifierId': {'$in': parent_id_list}})
                except errors.NotFound:
                    for parent_id in parent_id_list:
                        if is_parent_authorized(Id(parent_id)):
                            return True
                    return False
                else:
                    return True
            else:
                return False

        # Check first for an explicit or 'ROOT' level implicit authorization:
        try:
            authority = qualifier_id.get_identifier_namespace().split('.')[0].upper()
            identifier = qualifier_id.get_identifier_namespace().split('.')[1].upper()
        except KeyError:
            idstr_list = [str(qualifier_id)]
            authority = identifier = None
        else:
            # handle aliased IDs
            package_name = qualifier_id.get_identifier_namespace().split('.')[0]
            qualifier_id = self._get_id(qualifier_id, package_name)

            root_qualifier_id = Id(
                authority=qualifier_id.get_authority(),
                namespace=qualifier_id.get_identifier_namespace(),
                identifier='ROOT')
            idstr_list = [str(root_qualifier_id), str(qualifier_id)]
        try:
            collection.find_one(
                {'agentId': str(agent_id),
                 'functionId': str(function_id),
                 'qualifierId': {'$in': idstr_list}})

        # Otherwise check for implicit authorization through inheritance:
        except errors.NotFound:
            if authority and identifier:
                hierarchy_id = Id(authority=authority,
                                  namespace='CATALOG',
                                  identifier=identifier)
                return is_parent_authorized(qualifier_id)
            else:
                return False
        else:
            return True"""


class AuthorizationLookupSession:

    get_authorizations_for_agent_and_function = """
        collection = JSONClientValidated('authorization',
                                         collection='Authorization',
                                         runtime=self._runtime)
        result = collection.find(
            dict({'agentId': str(agent_id),
                  'functionId': str(function_id)},
                 **self._view_filter())).sort('_sort_id', ASCENDING)
        return objects.AuthorizationList(result, runtime=self._runtime)
"""


class AuthorizationAdminSession:

    import_statements = [
        'from dlkit.abstract_osid.id.primitives import Id as ABCId',
        'from dlkit.abstract_osid.type.primitives import Type as ABCType',
    ]

    create_authorization = """
        # TODO: not using the create_resource template
        # because want to prevent duplicate authorizations
        collection = JSONClientValidated('authorization',
                                         collection='Authorization',
                                         runtime=self._runtime)
        if not isinstance(authorization_form, ABCAuthorizationForm):
            raise errors.InvalidArgument('argument type is not an AuthorizationForm')
        if authorization_form.is_for_update():
            raise errors.InvalidArgument('the AuthorizationForm is for update only, not create')
        try:
            if self._forms[authorization_form.get_id().get_identifier()] == CREATED:
                raise errors.IllegalState('authorization_form already used in a create transaction')
        except KeyError:
            raise errors.Unsupported('authorization_form did not originate from this session')
        if not authorization_form.is_valid():
            raise errors.InvalidArgument('one or more of the form elements is invalid')

        # try to check first here
        try:
            osid_map = collection.find_one({"agentId": authorization_form._my_map['agentId'],
                                            "functionId": authorization_form._my_map['functionId'],
                                            "qualifierId": authorization_form._my_map['qualifierId'],
                                            "assignedVaultIds": authorization_form._my_map['assignedVaultIds']})
            osid_map['startDate'] = authorization_form._my_map['startDate']
            osid_map['endDate'] = authorization_form._my_map['endDate']
            collection.save(osid_map)
        except errors.NotFound:
            insert_result = collection.insert_one(authorization_form._my_map)

            self._forms[authorization_form.get_id().get_identifier()] = CREATED
            osid_map = collection.find_one({'_id': insert_result.inserted_id})
        result = objects.Authorization(
            osid_object_map=osid_map,
            runtime=self._runtime,
            proxy=self._proxy)

        return result"""

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
            # WHY are we passing vault_id = self._catalog_id below, seems redundant:
            # We probably also don't need to send agent_id. The form can now get that from the proxy
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
            # WHY are we passing vault_id = self._catalog_id below, seems redundant:
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
        osid_objects.OsidRelationshipForm.__init__(self, **kwargs)
        self._mdata = default_mdata.get_authorization_mdata()  # Don't know if we need default mdata for this
        self._init_metadata(**kwargs)

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
        self._my_map['agentId'] = None
        self._my_map['resourceId'] = None
        self._my_map['trustId'] = None
        self._my_map['implicit'] = None
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

    object_map = property(fget=get_object_map)"""


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
        collection = JSONClientValidated('authorization',
                                         collection='Vault',
                                         runtime=self._runtime)
        result = collection.find({'genusTypeId': {'$in': [str(vault_genus_type)]}}).sort('_id', DESCENDING)

        return objects.VaultList(result, runtime=self._runtime)"""
