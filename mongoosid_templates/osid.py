
class OsidProfile:

    import_statements = [
        'from . import profile',
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from ..primitives import Type',
    ]

    init = """
    
    def __init__(self):
        self._runtime = None
        self._config = None

    def _initialize_manager(self, runtime):
        \"\"\"Sets the runtime, configuration and mongo client\"\"\"
        if self._runtime is not None:
            raise errors.IllegalState('this manager has already been initialized.')
        self._runtime = runtime
        self._config = runtime.get_configuration()
        if not MONGO_CLIENT.is_mongo_client_set():
            try:
                mongo_host_param_id = Id('parameter:mongoHostURI@mongo')
                mongo_host = runtime.get_configuration().get_value_by_parameter(mongo_host_param_id).get_string_value()
            except (AttributeError, KeyError, errors.NotFound):
                MONGO_CLIENT.set_mongo_client(MongoClient())
            else:
                MONGO_CLIENT.set_mongo_client(MongoClient(mongo_host))
"""

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
        raise errors.Unimplemented()"""

    get_release_date = """
        # NEED TO IMPLEMENT
        raise errors.Unimplemented()"""

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
        raise errors.Unimplemented()"""

    get_locales = """
        # NEED TO IMPLEMENT
        raise errors.Unimplemented()"""

    supports_journal_rollback = """
        # Perhaps someday I will support journaling
        return False"""

    supports_journal_branching = """
        # Perhaps someday I will support journaling
        return False"""

    get_branch_id = """
        # Perhaps someday I will support journaling
        raise errors.Unimplemented()"""

    get_branch = """
        # Perhaps someday I will support journaling
        raise errors.Unimplemented()"""

    get_proxy_record_types = """
        # NEED TO IMPLEMENT
        raise errors.Unimplemented()"""

    supports_proxy_record_type = """
        # NEED TO IMPLEMENT
        raise errors.Unimplemented()"""

class OsidManager:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import DisplayText',
        'from pymongo import MongoClient',
        'from .. import MONGO_CLIENT',
    ]  

    init = """
    def __init__(self):
        OsidProfile.__init__(self)
"""
    
    initialize = """
        OsidProfile._initialize_manager(self, runtime)"""

class OsidProxyManager:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
    ]  

    init = """
    def __init__(self):
        OsidProfile.__init__(self)
"""
    
    initialize = """
        OsidProfile._initialize_manager(self, runtime)"""


class OsidRuntimeManager:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
    ]  

    init = """
    def __init__(self, configuration_key = None):
        self._configuration_key = configuration_key"""


class Identifiable:

    import_statements = [
        'from ..primitives import Id',
        'from dlkit.abstract_osid.osid import errors',
    ]  

    init = """
    def __init__(self, authority=None):
        self._namespace = 'osid.Identifiable'
        self._authority = authority or 'ODL.MIT.EDU'
        self._my_map = {}

    def _set_authority(self, runtime):
        try:
            authority_param_id = Id('parameter:authority@mongo')
            self._authority = runtime.get_configuration().get_value_by_parameter(
                authority_param_id).get_string_value()
        except (KeyError, errors.NotFound):
            self._authority = 'ODL.MIT.EDU'
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

    import_statements = [
        'from ..primitives import Id',
        'from ..primitives import Type',
        'from importlib import import_module',
        'from ..utilities import get_provider_manager',
    ]  

    init = """

    def __init__(self):
        self._records = None
        self._supported_record_type_ids = None
        self._record_type_data_sets = None
        self._runtime = None
        self._proxy = None

    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith('__'):
                yield attr

    def __getitem__(self, item):
        return getattr(self, item)

    def __getattribute__(self, name):
        if not name.startswith('_'):
            if '_records' in self.__dict__:
                for record in self._records:
                    try:
                        return self._records[record][name]
                    except AttributeError:
                        pass
        return object.__getattribute__(self, name)

    def __getattr__(self, name):
        if '_records' in self.__dict__:
            for record in self._records:
                try:
                    return self._records[record][name]
                except AttributeError:
                    pass
        raise AttributeError()

    def _get_record(self, record_type):
        \"\"\"Get the record string type value given the record_type.\"\"\"
        if not self.has_record_type(record_type):
            raise errors.Unsupported()
        if str(record_type) not in self._records:
            raise errors.Unimplemented()
        return self._records[str(record_type)]

    def _load_records(self, record_type_idstrs):
        \"\"\"Load all records from given record_type_idstrs.\"\"\"
        for record_type_idstr in record_type_idstrs:
            self._init_record(record_type_idstr)

    def _init_records(self, record_types):
        \"\"\"Initalize all records for this form.\"\"\"
        for record_type in record_types:
            # This conditional was inserted on 7/11/14. It may prove problematic:
            if str(record_type) not in self._my_map['recordTypeIds']:
                self._init_record(str(record_type))
                self._my_map['recordTypeIds'].append(str(record_type))

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

    def _get_provider_manager(self, osid, local=False):
        \"\"\"Gets the most appropriate provider manager depending on config.\"\"\"
        return get_provider_manager(osid, runtime=self._runtime, local=local)
"""

    has_record_type = """
        return str(record_type) in self._supported_record_type_ids"""

    get_record_types = """
        from ..type.objects import TypeList
        type_list = []
        for type_idstr in self._supported_record_type_ids:
            type_list.append(Type(**self._record_type_data_sets[Id(type_idstr).get_identifier()]))
        return TypeList(type_list)"""

class Temporal:

    import_statements = [
        'from ..primitives import DateTime',
    ]

    init = """
    def __init__(self):
        self._my_map = {}
"""

    is_effective = """
        now = DateTime.now()
        return self.get_start_date() <= now and self.get_end_date() >= now"""

    get_start_date = """
        sdate = self._my_map['startDate']
        return DateTime(
            sdate['year'],
            sdate['month'],
            sdate['day'],
            sdate['hour'],
            sdate['minute'],
            sdate['second'],
            sdate['microsecond'])"""

    get_end_date = """
        edate = self._my_map['endDate']
        return DateTime(
            edate['year'],
            edate['month'],
            edate['day'],
            edate['hour'],
            edate['minute'],
            edate['second'],
            edate['microsecond'])"""

class Containable:

    init = """
    def __init__(self):
        self._my_map = {}
"""

    is_sequestered = """
        return self._my_map['sequestered']"""

class Sourceable:

    import_statements = [
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.locale.primitives import DisplayText',
    ]

    get_provider_id = """
        if 'providerId' not in self._my_map or not self._my_map['providerId']:
            raise errors.IllegalState('this sourceable object has no provider set')
        return Id(self._my_map['providerId'])"""

    get_provider = """
        if 'providerId' not in self._my_map or not self._my_map['providerId']:
            raise errors.IllegalState('this sourceable object has no provider set')
        mgr = self._get_provider_manager('RESOURCE')
        lookup_session = mgr.get_resource_lookup_session()
        lookup_session.use_federated_bin_view()
        resource = lookup_session.get_resource(self.get_provider_id())"""

    get_branding_ids = """
        from ..id.objects import IdList
        if 'brandingIds' not in self._my_map:
            return IdList([])
        id_list = []
        for idstr in self._my_map['brandingIds']:
            id_list.append(Id(idstr))
        return IdList(id_list)"""

    get_branding = """
        mgr = self._get_provider_session('REPOSITORY')
        lookup_session = mgr.get_asset_lookup_session()
        lookup_session.get_federated_repository_view()
        return lookup_session.get_assets_by_ids(self.get_branding_ids())"""

    get_license = """
        if 'license' in self._my_map:
            license_text = self._my_map['license']
        else:
            license_text = ''
        return DisplayText('license_text')"""


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
        'import datetime',
        'from ..primitives import Id',
        'from ..primitives import Type',
        'from dlkit.abstract_osid.osid import errors',
        'from bson.objectid import ObjectId',
        'from importlib import import_module',
        'from ..utilities import MongoClientValidated',
        'from ..utilities import get_provider_manager',
        'from .. import types',
        'COMPARATIVE = 0',
        'PLENARY = 1',
        'FEDERATED = 0',
        'ISOLATED = 1',
        'EFFECTIVE = 0',
        'ANY_EFFECTIVE = 1',
        'CREATED = True',
        'UPDATED = True',
    ]

    init = """
    def __init__(self):
        self._proxy = None
        self._runtime = None
        self._db_prefix = None
        self._catalog_identifier = None
        self._my_catalog_map = None
        self._catalog_id = None
        self._catalog = None
        self._forms = None
        self._object_view = COMPARATIVE
        self._catalog_view = ISOLATED
        self._effective_view = ANY_EFFECTIVE
        self._authority = 'ODL.MIT.EDU'

    def _init_proxy_and_runtime(self, proxy, runtime):
        self._proxy = proxy
        self._runtime = runtime
        if runtime is not None:
            prefix_param_id = Id('parameter:mongoDBNamePrefix@mongo')
            self._db_prefix = runtime.get_configuration().get_value_by_parameter(prefix_param_id).get_string_value()

            try:
                authority_param_id = Id('parameter:authority@mongo')
                self._authority = runtime.get_configuration().get_value_by_parameter(
                    authority_param_id).get_string_value()
            except (KeyError, errors.NotFound):
                self._authority = 'ODL.MIT.EDU'
        else:
            self._db_prefix = ''

    def _init_catalog(self, proxy=None, runtime=None):
        \"\"\"Initialize this object as an OsidCatalog.\"\"\"
        self._init_proxy_and_runtime(proxy, runtime)

    def _init_object(self, catalog_id, proxy, runtime, db_name, cat_name, cat_class):
        \"\"\"Initialize this object as an OsidObject.\"\"\"
        self._catalog_identifier = None
        self._init_proxy_and_runtime(proxy, runtime)

        if catalog_id is not None and catalog_id.get_identifier() != '000000000000000000000000':
            self._catalog_identifier = catalog_id.get_identifier()

            collection = MongoClientValidated(self._db_prefix + db_name,
                                              collection=cat_name,
                                              runtime=self._runtime)
            try:
                self._my_catalog_map = collection.find_one({'_id': ObjectId(self._catalog_identifier)})
            except errors.NotFound:
                if catalog_id.get_identifier_namespace() != db_name + '.' + cat_name:
                    self._my_catalog_map = self._create_orchestrated_cat(catalog_id, db_name, cat_name)
                else:
                    raise errors.NotFound('could not find catalog identifier ' + catalog_id.get_identifier() + cat_name)
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
        self._catalog._authority = self._authority  # there should be a better way...
        self._catalog_id = self._catalog.get_id()
        self._forms = dict()

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
            collection = MongoClientValidated(self._db_prefix + foreign_db_name,
                                              collection=foreign_cat_name,
                                              runtime=self._runtime)
            collection.find_one({'_id': ObjectId(foreign_catalog_id.get_identifier())})
        except KeyError:
            raise errors.NotFound()
        collection = MongoClientValidated(self._db_prefix + db_name,
                                          collection=cat_name,
                                          runtime=self._runtime)
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
            'genusTypeId': str(Type(**types.Genus().get_type_data('DEFAULT'))),
            'recordTypeIds': [] # Could this somehow inherit source catalog records?

        }
        collection.insert_one(catalog_map)
        return catalog_map

    def _get_provider_manager(self, osid, local=False):
        \"\"\"Gets the most appropriate provider manager depending on config.\"\"\"
        return get_provider_manager(osid, runtime=self._runtime, local=local)

    def _get_id(self, id_, pkg_name):
        \"\"\"
        Returns the primary id given an alias.

        If the id provided is not in the alias table, it will simply be
        returned as is.

        Only looks within the Id Alias namespace for the session package

        \"\"\"
        collection = MongoClientValidated(self._db_prefix + 'id',
                                          collection=pkg_name + 'Ids',
                                          runtime=self._runtime)
        try:
            result = collection.find_one({'aliasIds': {'$in': [str(id_)]}})
        except errors.NotFound:
            return id_
        else:
            return Id(result['_id'])

    def _alias_id(self, primary_id, equivalent_id):
        \"\"\"Adds the given equivalent_id as an alias for primary_id if possible\"\"\"
        pkg_name = primary_id.get_identifier_namespace().split('.')[0]
        obj_name = primary_id.get_identifier_namespace().split('.')[1]
        collection = MongoClientValidated(self._db_prefix + pkg_name,
                                          collection=obj_name,
                                          runtime=self._runtime)
        collection.find_one({'_id': ObjectId(primary_id.get_identifier())}) # to raise NotFound
        collection = MongoClientValidated(self._db_prefix + 'id',
                                          collection=pkg_name + 'Ids',
                                          runtime=self._runtime)
        try:
            result = collection.find_one({'aliasIds': {'$in': [str(equivalent_id)]}})
        except errors.NotFound:
            pass
        else:
            result['aliasIds'].remove(str(equivalent_id))
            collection.save(result)
        try:
            id_map = collection.find_one({'_id': str(primary_id)})
        except errors.NotFound:
            collection.insert_one({'_id': str(primary_id), 'aliasIds': [str(equivalent_id)]})
        else:
            id_map['aliasIds'].append(str(equivalent_id))
            collection.save(id_map)

    def _get_catalog_idstrs(self):
        \"\"\"Returns the proper list of catalog idstrs based on catalog view\"\"\"
        if self._catalog_view == ISOLATED:
            return [str(self._catalog_id)]
        else:
            return self._get_descendent_cat_idstrs(self._catalog_id)

    def _get_descendent_cat_idstrs(self, cat_id, hierarchy_session=None):
        \"\"\"Recursively returns a list of all descendent catalog ids, inclusive\"\"\"
        idstr_list = [str(cat_id)]
        if hierarchy_session is None:
            pkg_name = cat_id.get_identifier_namespace().split('.')[0]
            cat_name = cat_id.get_identifier_namespace().split('.')[1]
            try:
                mgr = self._get_provider_manager('HIERARCHY')
                hierarchy_session = mgr.get_hierarchy_traversal_session_for_hierarchy(
                    Id(authority=pkg_name.upper(),
                       namespace='CATALOG',
                       identifier=cat_name.upper()))
            except (errors.OperationFailed, errors.Unsupported):
                return idstr_list # there is no hierarchy
        if hierarchy_session.has_children(cat_id):
            for child_id in hierarchy_session.get_children(cat_id):
                idstr_list = idstr_list + self._get_descendent_cat_idstrs(child_id, hierarchy_session)
        return idstr_list

    def _is_phantom_root_federated(self):
        return (self._catalog_view == FEDERATED and 
                self._catalog_id.get_identifier() == '000000000000000000000000')

    def _use_comparative_object_view(self):
        self._object_view = COMPARATIVE

    def _use_plenary_object_view(self):
        self._object_view = PLENARY

    def _use_federated_catalog_view(self):
        self._catalog_view = FEDERATED

    def _use_isolated_catalog_view(self):
        self._catalog_view = ISOLATED

    def _use_effective_view(self):
        self._effective_view = EFFECTIVE

    def _use_any_effective_view(self):
        self._effective_view = ANY_EFFECTIVE

    def _effective_view_filter(self):
        \"\"\"Returns the mongodb relationship filter for effective views\"\"\"
        if self._effective_view == EFFECTIVE:
            now = datetime.datetime.now()
            return {'startDate': {'$$lte': now}, 'endDate': {'$$gte': now}}
        return {}

    def _assign_object_to_catalog(self, obj_id, cat_id):
        pkg_name = obj_id.get_identifier_namespace().split('.')[0]
        obj_name = obj_id.get_identifier_namespace().split('.')[1]
        collection = MongoClientValidated(self._db_prefix + pkg_name,
                                          collection=obj_name,
                                          runtime=self._runtime)
        obj_map = collection.find_one({'_id': ObjectId(obj_id.get_identifier())})
        if 'assignedCatalogIds' in obj_map:
            if str(cat_id) in obj_map['assignedCatalogIds']:
                raise errors.AlreadyExists()
            else:
                obj_map['assignedCatalogIds'].append(str(cat_id))
        else:
            obj_map['assignedCatalogIds'] = [str(cat_id)]
        collection.save(obj_map)

    def _unassign_object_from_catalog(self, obj_id, cat_id):
        pkg_name = obj_id.get_identifier_namespace().split('.')[0]
        obj_name = obj_id.get_identifier_namespace().split('.')[1]
        collection = MongoClientValidated(self._db_prefix + pkg_name,
                                          collection=obj_name,
                                          runtime=self._runtime)
        obj_map = collection.find_one({'_id': ObjectId(obj_id.get_identifier())})
        try:
            obj_map['assignedCatalogIds'].remove(str(cat_id))
        except (KeyError, ValueError):
            raise errors.NotFound()
        collection.save(obj_map)
"""

    get_locale = """
        #from ..locale.objects import Locale
        ##
        # This implementation could assume that instantiating a new Locale
        # without constructor arguments wlll return the default Locale.
        #return Locale()
        raise errors.Unimplemented()"""  

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
            raise errors.IllegalState()"""  

    get_authenticated_agent = """
        if self.is_authenticated():
            return self._proxy.get_authentication().get_agent()
        else:
            raise errors.IllegalState()"""

    get_effective_agent_id = """
        if self.is_authenticated():
            if self._proxy.has_effective_agent():
                return self._proxy.get_effective_agent_id()
            else:
                return self._proxy.get_authentication().get_agent_id()
        else:
            return Id(
                identifier='MC3GUE$T@MIT.EDU',
                namespace='authentication.Agent',
                authority='MIT-ODL')"""

    get_effective_agent = """
        #effective_agent_id = self.get_effective_agent_id()
        # This may want to be extended to get the Agent directly from the Authentication
        # if available and if not effective agent is available in the proxy
        #return Agent(
        #    identifier=effective_agent_id.get_identifier(),
        #    namespace=effective_agent_id.get_namespace(),
        #    authority=effective_agent_id.get_authority())
        raise errors.Unimplemented()"""

    supports_transactions = """
        return False"""

    startTransaction = """
        if not supports_transactions:
            raise errors.Unsupported('transactions ore not supported for this session')"""


class OsidObject:

    import_statements = [
        'from ..primitives import Type',
        'from ..primitives import DisplayText',
        'from dlkit.abstract_osid.osid import errors',
        'from .. import types',
    ]

    init = """
    _namespace = 'mongo.OsidObject'

    def __init__(self, osid_object_map, runtime=None):
        self._my_map = osid_object_map
        self._runtime = runtime
        if runtime is not None:
            self._set_authority(runtime=runtime)

    def get_object_map(self, obj_map=None):
        # pylint: disable=too-many-branches
        if obj_map is None:
            obj_map = dict(self._my_map)
        del obj_map['_id']
        my_idstr = str(self.get_id())

        # to handle over-ridden fields, like for enclosed assessments
        obj_map['displayName']['text'] = self.display_name.text
        obj_map['description']['text'] = self.description.text
        obj_map['genusTypeId'] = str(self.genus_type)

        # The following is crappy. Should be over-ridden in the corresponding
        # object's get_object_map() methods instead:
        if self._namespace == 'repository.Asset':
            obj_map['assetContents'] = []
            obj_map['assetContent'] = [] # This is deprecated, switch to assetContents
            for asset_content in self.get_asset_contents():
                obj_map['assetContents'].append(asset_content.get_object_map())
                obj_map['assetContent'].append(asset_content.get_object_map())
        if self._namespace == 'resource.Resource':
            if 'agentIds' in obj_map:
                del obj_map['agentIds']
        if self._namespace == 'repository.AssetContent':
            if 'dbPrefix' in obj_map:
                del obj_map['dbPrefix']
        if self._namespace == 'repository.Composition':
            if 'assetIds' in obj_map:
                del obj_map['assetIds']
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
                actual_start_time = obj_map['actualStartTime']
                obj_map['actualStartTime'] = dict()
                obj_map['actualStartTime']['year'] = actual_start_time.year
                obj_map['actualStartTime']['month'] = actual_start_time.month
                obj_map['actualStartTime']['day'] = actual_start_time.day
                obj_map['actualStartTime']['hour'] = actual_start_time.hour
                obj_map['actualStartTime']['minute'] = actual_start_time.minute
                obj_map['actualStartTime']['second'] = actual_start_time.second
                obj_map['actualStartTime']['microsecond'] = actual_start_time.microsecond
            if obj_map['completionTime'] is not None:
                completion_time = obj_map['completionTime']
                obj_map['completionTime'] = dict()
                obj_map['completionTime']['year'] = completion_time.year
                obj_map['completionTime']['month'] = completion_time.month
                obj_map['completionTime']['day'] = completion_time.day
                obj_map['completionTime']['hour'] = completion_time.hour
                obj_map['completionTime']['minute'] = completion_time.minute
                obj_map['completionTime']['second'] = completion_time.second
                obj_map['completionTime']['microsecond'] = completion_time.microsecond
            if obj_map['displayName']['text'] == '':
                obj_map['displayName']['text'] = self.get_display_name().get_text()
            if obj_map['description']['text'] == '':
                obj_map['description']['text'] = self.get_description().get_text()
            if 'itemIds' in obj_map:
                del obj_map['itemIds']
            if 'responses' in obj_map:
                del obj_map['responses']
        if self._namespace == 'grading.GradeSystem':
            obj_map['grades'] = []
            for grade in self.get_grades():
                obj_map['grades'].append(grade.object_map)

        try: # Need to implement records for catalogs one of these days
            for record in self._records:
                try:
                    self._records[record]._update_object_map(obj_map)
                except AttributeError:
                    pass
        except AttributeError:
            pass
        
        if 'assignedCatalogs' in obj_map:
            del obj_map['assignedCatalogs']

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
        # Someday I'll have a real implementation, but for now I just:
        raise errors.IllegalState()"""
    
    get_rule= """
        # Someday I'll have a real implementation, but for now I just:
        raise errors.IllegalState()"""

class OsidForm:

    import_statements = [
        'from ..primitives import Id',
        'from dlkit.abstract_osid.osid import errors',
        'from . import mdata_conf',
        'from .metadata import Metadata',
        'import uuid',
        'from decimal import Decimal',
    ]

    init = """
    # pylint: disable=no-self-use
    # MUCH OF THIS SHOULD BE MOVED TO A UTILITY MODULE

    _namespace = 'mongo.OsidForm'

    def __init__(self, runtime=None):
        self._identifier = str(uuid.uuid4())
        self._for_update = None
        self._runtime = runtime
        if runtime is not None:
            self._set_authority(runtime=runtime)

    def _init_metadata(self):
        \"\"\"Initialize OsidObjectForm metadata.\"\"\"

        # pylint: disable=attribute-defined-outside-init
        # this method is called from descendent __init__
        self._journal_comment_metadata = {
            'element_id': Id(authority=self._authority,
                             namespace=self._namespace,
                             identifier='display_name')}
        self._journal_comment_metadata.update(mdata_conf.JOURNAL_COMMENT)
        self._journal_comment_default = dict(self._journal_comment_metadata['default_string_values'][0])
        self._journal_comment = self._journal_comment_default
        self._validation_messages = {}

    def get_id(self):
        \"\"\" Override get_id as implemented in Identifiable.

        for the purpose of returning an Id unique to this form for
        submission purposed as recommended in the osid specification.
        This implementation substitutes the intialized Python uuid4
        identifier, and the form namespace from the calling Osid Form.

         \"\"\"
        return Id(identifier=self._identifier,
                  namespace=self._namespace,
                  authority=self._authority)

    def _is_valid_input(self, inpt, metadata, array):
        \"\"\"The _is_valid_input method takes three arguments:

        the user input to be checked, the associated  osid.Metadata object
        containing validation requirements and a boolean value indicating
        whether this is an array value.

        \"\"\"
        # pylint: disable=too-many-branches,no-self-use
        # Please redesign, and move to utility module
        syntax = metadata.get_syntax

        ##
        # First check if this is a required data element
        if metadata.is_required == True and not inpt:
            return False

        valid = True # Innocent until proven guilty
        ##
        # Recursively run through all the elements of an array
        if array == True:
            if len(inpt) < metadata['minimum_elements']:
                valid = False
            elif len(inpt) > metadata['maximum_elements']:
                valid = False
            else:
                for element in array:
                    valid = (valid and self._is_valid_input(element, metadata, False))
        ##
        # Run through all the possible syntax types
        elif syntax == 'ID':
            valid = self._is_valid_id(inpt)
        elif syntax == 'TYPE':
            valid = self._is_valid_type(inpt)
        elif syntax == 'BOOLEAN':
            valid = self._is_valid_boolean(inpt)
        elif syntax == 'STRING':
            valid = self._is_valid_string(inpt, metadata)
        elif syntax == 'INTEGER':
            valid = self._is_valid_integer(inpt, metadata)
        elif syntax == 'DECIMAL':
            valid = self._is_valid_decimal(inpt, metadata)
        elif syntax == 'DATETIME':
            valid = self._is_valid_date_time(inpt, metadata)
        elif syntax == 'DURATION':
            valid = self._is_valid_duration(inpt, metadata)
        elif syntax == 'CARDINAL':
            valid = self._is_valid_cardinal(inpt, metadata)
        elif syntax == 'INTEGER':
            valid = self._is_valid_integer(inpt, metadata)
        elif syntax == 'DECIMAL':
            valid = self._is_valid_decimal(inpt, metadata)
        else:
            raise errors.OperationFailed('no validation function available for ' + syntax)

        return valid

    def _is_valid_id(self, inpt):
        \"\"\"Checks if input is a valid Id\"\"\"
        from ...abstract_osid.id.primitives import Id as abc_id
        if isinstance(inpt, abc_id):
            return True
        else:
            return False

    def _is_valid_type(self, inpt):
        \"\"\"Checks if input is a valid Type\"\"\"
        from ...abstract_osid.type.primitives import Type as abc_type
        if isinstance(inpt, abc_type):
            return True
        else:
            return False

    def _is_valid_boolean(self, inpt):
        \"\"\"Checks if input is a valid boolean\"\"\"
        if isinstance(inpt, bool):
            return True
        else:
            return False

    def _is_valid_string(self, inpt, metadata):
        \"\"\"Checks if input is a valid string\"\"\"
        if not isinstance(inpt, basestring):
            return False
        if metadata.get_minimum_string_length() and len(inpt) < metadata.get_minimum_string_length():
            return False
        elif metadata.get_maximum_string_length() and len(inpt) > metadata.get_maximum_string_length():
            return False
        if metadata.get_string_set() and inpt not in metadata.get_string_set():
            return False
        else:
            return True

    def _is_valid_cardinal(self, inpt, metadata):
        \"\"\"Checks if input is a valid cardinal value\"\"\"
        if not isinstance(inpt, int):
            return False
        if metadata.get_minimum_cardinal() and inpt < metadata.get_maximum_cardinal():
            return False
        if metadata.get_maximum_cardinal() and inpt > metadata.get_minimum_cardinal():
            return False
        if metadata.get_cardinal_set() and inpt not in metadata.get_cardinal_set():
            return False
        else:
            return True

    def _is_valid_integer(self, inpt, metadata):
        \"\"\"Checks if input is a valid integer value\"\"\"
        if not isinstance(inpt, int):
            return False
        if metadata.get_minimum_integer() and inpt < metadata.get_maximum_integer():
            return False
        if metadata.get_maximum_integer() and inpt > metadata.get_minimum_integer():
            return False
        if metadata.get_integer_set() and inpt not in metadata.get_integer_set():
            return False
        else:
            return True

    def _is_valid_decimal(self, inpt, metadata):
        \"\"\"Checks if input is a valid decimal value\"\"\"
        if not (isinstance(inpt, float) or isinstance(inpt, Decimal)):
            return False
        if metadata.get_minimum_decimal() and inpt < metadata.get_minimum_decimal():
            return False
        if metadata.get_maximum_decimal() and inpt > metadata.get_maximum_decimal():
            return False
        if metadata.get_decimal_set() and inpt not in metadata.get_decimal_set():
            return False
        if metadata.get_decimal_scale() and len(str(inpt).split('.')[-1]) != metadata.get_decimal_scale():
            return False
        else:
            return True

    def _is_valid_date_time(self, inpt, metadata):
        \"\"\"Checks if input is a valid DateTime object\"\"\"
        # NEED TO ADD CHECKS FOR OTHER METADATA, LIKE MINIMUM, MAXIMUM, ETC.
        from ...abstract_osid.calendaring.primitives import DateTime as abc_datetime
        if isinstance(inpt, abc_datetime):
            return True
        else:
            return False

    def _is_valid_timestamp(self, *args, **kwargs):
        \"\"\"Checks if input is a valid timestamp\"\"\"
        # This should be temporary to deal with a bug in the OSID RC3 spec
        # Check assessment.AssessmentOffered.set_deadline to see if this
        # is still required.
        return self._is_valid_date_time(*args, **kwargs)

    def _is_valid_duration(self, inpt, metadata):
        \"\"\"Checks if input is a valid Duration\"\"\"
        # NEED TO ADD CHECKS FOR OTHER METADATA, LIKE MINIMUM, MAXIMUM, ETC.
        from ...abstract_osid.calendaring.primitives import Duration as abc_duration
        if isinstance(inpt, abc_duration):
            return True
        else:
            return False

    def _is_in_set(self, inpt, metadata):
        \"\"\"checks if the input is in the metadata's *_set list\"\"\"
        # makes an assumption there is only one _set in the metadata dict
        get_set_methods = [m for m in dir(metadata) if 'get_' in m and '_set' in m]
        set_results = None
        for m in get_set_methods:
            try:
                set_results = getattr(metadata, m)()
                break
            except errors.IllegalState:
                pass
        if set_results is not None and inpt in set_results:
            return True
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
        raise errors.Unsupported()"""

    get_journal_comment_metadata = """
        return Metadata(**self._journal_comment_metadata)"""

    set_journal_comment = """
        if self.get_journal_comment_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_string(comment, self.get_journal_comment_metadata()):
            raise errors.InvalidArgument()
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
    import_statements = [
        'import importlib',
    ]

    init = """
    def _get_record(self, recordType):
        \"\"\"This overrides _get_record in osid.Extensible.

        Perhaps we should leverage it somehow?

        \"\"\"
        if not self.has_record_type(recordType):
            raise errors.Unsupported()
        if str(recordType) not in self._records: # Currently this should never be True
            self._init_record(str(recordType))
            if str(recordType) not in self._my_map['recordTypeIds']: # nor this
                self._my_map['recordTypeIds'].append(str(recordType))
        return self._records[str(recordType)]

    def _init_record(self, record_type_idstr):
        \"\"\"Override this from osid.Extensible because Forms use a different
        attribute in record_type_data.\"\"\"
        record_type_data = self._record_type_data_sets[Id(record_type_idstr).get_identifier()]
        module = importlib.import_module(record_type_data['module_path'])
        record = getattr(module, record_type_data['form_record_class_name'])
        self._records[record_type_idstr] = record(self)
"""

class OsidTemporalForm:

    import_statements = [
        'from ..primitives import Id',
        'from dlkit.abstract_osid.osid import errors',
        'import datetime',
        'from . import mdata_conf',
        'from .metadata import Metadata',
        ]

    init = """
    _namespace = "mongo.OsidTemporalForm"

    def _init_metadata(self, **kwargs):
        # pylint: disable=attribute-defined-outside-init
        # this method is called from descendent __init__
        self._start_date_metadata = {
            'element_id': Id(authority=self._authority,
                             namespace=self._namespace,
                             identifier='start_date')}
        self._start_date_metadata.update(mdata_conf.START_DATE)
        self._start_date_metadata.update({'default_date_time_values': [self._get_date_map(datetime.datetime.now())]})
        self._end_date_metadata = {
            'element_id': Id(authority=self._authority,
                             namespace=self._namespace,
                             identifier='end_date')}
        self._end_date_metadata.update(mdata_conf.END_DATE)

    def _init_map(self):
        # pylint: disable=attribute-defined-outside-init
        # this method is called from descendent __init__
        self._my_map['startDate'] = self._start_date_metadata['default_date_time_values'][0]
        self._my_map['endDate'] = self._end_date_metadata['default_date_time_values'][0]
"""

    get_start_date_metadata = """
        metadata = dict(self._start_date_metadata)
        metadata.update({'existing_date_time_values': self._my_map['startDate']})
        return Metadata(**metadata)"""

    set_start_date = """
        if self.get_start_date_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_date_time(date, self.get_start_date_metadata()):
            raise errors.InvalidArgument()
        self._my_map['startDate'] = self._get_date_map(date)"""

    clear_start_date = """
        if (self.get_start_date_metadata().is_read_only() or
                self.get_start_date_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['startDate'] = self.get_start_date_metadata['default_date_time_values'][0]"""

    get_end_date_metadata = """
        metadata = dict(self._end_date_metadata)
        metadata.update({'existing_date_time_values': self._my_map['endDate']})
        return Metadata(**metadata)"""

    set_end_date = """
        if self.get_end_date_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_date_time(date, self.get_end_date_metadata()):
            raise errors.InvalidArgument()
        self._my_map['endDate'] = self._get_date_map(date)"""

    clear_end_date = """
        if (self.get_end_date_metadata().is_read_only() or
                self.get_end_date_metadata().is_required()):
            raise errors.NoAccess()
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

class OsidContainableForm:

    init = """
    def __init__(self):
        self._sequestered_metadata = None
        self._sequestered_default = None
        self._sequestered = None

    def _init_metadata(self):
        self._sequestered_metadata = {
            'element_id': Id(authority=self._authority,
                             namespace=self._namespace,
                             identifier='sequestered')}
        self._sequestered_metadata.update(mdata_conf.SEQUESTERED)
        self._sequestered_default = False
        self._sequestered = self._sequestered_default

    def _init_map(self):
        self._my_map['sequestered'] = self._sequestered_default
"""

    get_sequestered_metadata = """
        return Metadata(**self._sequestered_metadata)"""

    set_sequestered = """
        if sequestered is None:
            raise errors.NullArgument()
        if self.get_sequestered_metadata().is_read_only():
            raise errors.NoAccess()
        if not isinstance(sequestered, bool):
            raise errors.InvalidArgument()
        self._my_map['sequestered'] = sequestered"""

    clear_sequestered = """
        if (self.get_sequestered_metadata().is_read_only() or
                self.get_sequestered_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['sequestered'] = self._sequestered_default"""


class OsidSourceableForm:

    init = """
    def __init__(self):
        self._provider_metadata = None
        self._provider_default = None
        self._branding_metadata = None
        self._branding_default = None
        self._license_metadata = None
        self._license_default = None
        self._catalog_id = None

    def _init_metadata(self):
        self._provider_metadata = {
            'element_id': Id(authority=self._authority,
                             namespace=self._namespace,
                             identifier='provider')}
        self._provider_metadata.update(mdata_conf.PROVIDER)
        self._provider_default = self._provider_metadata['default_id_values'][0]

        self._branding_metadata = {
            'element_id': Id(authority=self._authority,
                             namespace=self._namespace,
                             identifier='branding')}
        self._branding_metadata.update(mdata_conf.BRANDING)
        self._branding_default = self._branding_metadata['default_id_values']

        self._license_metadata = {
            'element_id': Id(authority=self._authority,
                             namespace=self._namespace,
                             identifier='license')}
        self._license_metadata.update(mdata_conf.LICENSE)
        self._license_default = self._license_metadata['default_string_values'][0]

    def _init_map(self, **kwargs):
        if 'effective_agent_id' in kwargs:
            try:
                mgr = self._get_provider_manager('RESOURCE', local=True)
                agent_session = mgr.get_resource_agent_session()
                agent_session.use_federated_bin_view()
                resource_idstr = str(agent_session.get_resource_id_by_agent(kwargs['effective_agent_id']))
            except (errors.OperationFailed,
                    errors.Unsupported,
                    errors.Unimplemented,
                    errors.NotFound):
                resource_idstr = self._provider_default
            self._my_map['providerId'] = resource_idstr
        else:
            self._my_map['providerId'] = self._provider_default
        self._my_map['brandingIds'] = self._branding_default
        self._my_map['license'] = dict(self._license_default)
"""

    get_provider_metadata = """
        metadata = dict(self._provider_metadata)
        metadata.update({'existing_id_values': self._my_map['providerId']})
        return Metadata(**metadata)"""

    set_provider = """
        if self.get_provider_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_id(provider_id):
            raise errors.InvalidArgument()
        self._my_map['providerId'] = str(provider_id)"""

    clear_provider = """
        if (self.get_provider_metadata().is_read_only() or
                self.get_provider_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['providerId'] = self._provider_default"""

    get_branding_metadata = """
        metadata = dict(self._branding_metadata)
        metadata.update({'existing_id_values': self._my_map['brandingIds']})
        return Metadata(**metadata)"""

    set_branding = """
        if self.get_branding_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_input(asset_ids, self.get_branding_metadata(), array=True):
            raise errors.InvalidArgument()
        branding_ids = []
        for asset_id in asset_ids:
            branding_ids.append(str(asset_id))
        self._my_map['brandingIds'] = branding_ids"""

    clear_branding = """
        if (self.get_branding_metadata().is_read_only() or
                self.get_branding_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['brandingIds'] = self._branding_default"""

    get_license_metadata = """
        metadata = dict(self._license_metadata)
        metadata.update({'existing_string_values': self._my_map['license']})
        return Metadata(**metadata)"""

    set_license = """
        if self.get_license_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_string(license, self.get_license_metadata()):
            raise errors.InvalidArgument()
        self._my_map['license']['text'] = license"""

    clear_license = """
        if (self.get_license_metadata().is_read_only() or
                self.get_license_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['license'] = dict(self._license_default)"""


class OsidObjectForm:

    #inheritance = ['OsidObject']

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from . import mdata_conf',
        'from .metadata import Metadata',
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
        \"\"\"Initialize metadata for form\"\"\"
        OsidForm._init_metadata(self)
        self._display_name_metadata = {
            'element_id': Id(authority=self._authority,
                             namespace=self._namespace,
                             identifier='display_name')}
        self._display_name_metadata.update(mdata_conf.DISPLAY_NAME)
        if 'default_display_name' in kwargs:
            self._display_name_metadata['default_string_values'][0]['text'] = kwargs['default_display_name']
        self._description_metadata = {
            'element_id': Id(authority=self._authority,
                             namespace=self._namespace,
                             identifier='description')}
        self._description_metadata.update(mdata_conf.DESCRIPTION)
        self._genus_type_metadata = {
            'element_id': Id(authority=self._authority,
                             namespace=self._namespace,
                             identifier='description')}
        if 'default_description' in kwargs:
            self._description_metadata['default_string_values'][0]['text'] = kwargs['default_description']
        self._genus_type_metadata.update(mdata_conf.GENUS_TYPE)

    def _init_map(self):
        self._my_map['displayName'] = dict(self._display_name_metadata['default_string_values'][0])
        self._my_map['description'] = dict(self._description_metadata['default_string_values'][0])
        self._my_map['genusTypeId'] = self._genus_type_metadata['default_type_values'][0]
        self._my_map['recordTypeIds'] = []
"""

    get_display_name_metadata = """
        return Metadata(**self._display_name_metadata)"""

    set_display_name = """
        if self.get_display_name_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_string(display_name,
                                     self.get_display_name_metadata()):
            raise errors.InvalidArgument()
        self._my_map['displayName']['text'] = display_name"""

    clear_display_name = """
        if (self.get_display_name_metadata().is_read_only() or
                self.get_display_name_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['displayName'] = dict(self._display_name_metadata['default_object_values'][0])"""

    get_description_metadata = """
        return Metadata(**self._description_metadata)"""

    set_description = """
        if self.get_description_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_string(description,
                                     self.get_description_metadata()):
            raise errors.InvalidArgument()
        self._my_map['description']['text'] = description"""

    clear_description = """
        if (self.get_description_metadata().is_read_only() or
                self.get_description_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['description'] = dict(self._description_metadata['default_object_values'][0])"""

    get_genus_type_metadata = """
        return Metadata(**self._genus_type_metadata)"""

    set_genus_type = """
        if self.get_genus_type_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_type(genus_type):
            raise errors.InvalidArgument()
        self._my_map['genusTypeId'] = str(genus_type)"""

    clear_genus_type = """
        if (self.get_genus_type_metadata().is_read_only() or
                self.get_genus_type_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['genusTypeId'] = self._genus_type_metadata['default_type_values'][0]"""

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
    import_statements = [
        'from pymongo.cursor import Cursor',
    ]

    init = """
    def __init__(self, iter_object=None, db_prefix='', runtime=None):
        if iter_object is None:
            iter_object = []
        if isinstance(iter_object, dict) or isinstance(iter_object, list):
            self._count = len(iter_object)
        elif isinstance(iter_object, Cursor):
            self._count = iter_object.count()
        else:
            self._count = None
        self._runtime = runtime
        self._db_prefix = db_prefix
        self._iter_object = iter(iter_object)

    def __iter__(self):
        return self

    def _get_next_n(self, number=None):
        \"\"\"Gets the next set of \"n\" elements in this list.

        The specified amount must be less than or equal to the return
        from ``available()``.

        arg:    n (cardinal): the number of ``Relationship`` elements
                requested which must be less than or equal to
                ``available()``
        return: (osid.relationship.Relationship) - an array of
                ``Relationship`` elements.The length of the array is
                less than or equal to the number specified.
        raise:  IllegalState - no more elements available in this list
        raise:  OperationFailed - unable to complete request
        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        if number > self.available():
            # !!! This is not quite as specified (see method docs) !!!
            raise errors.IllegalState('not enough elements available in this list')
        else:
            next_list = []
            counter = 0
            while counter < number:
                try:
                    next_list.append(self.next())
                except Exception:  # Need to specify exceptions here!
                    raise errors.OperationFailed()
                counter += 1
            return next_list

    def _get_next_object(self, object_class):
        \"\"\"stub\"\"\"
        try:
            next_object = OsidList.next(self)
        except StopIteration:
            raise
        except Exception:  # Need to specify exceptions here!
            raise errors.OperationFailed()
        if isinstance(next_object, dict):
            next_object = object_class(next_object, db_prefix=self._db_prefix, runtime=self._runtime)
        return next_object

    def next(self):
        \"\"\"next method for iterator.\"\"\"
        next_object = self._iter_object.next()
        if self._count != None:
            self._count -= 1
        return next_object

    def len(self):
        \"\"\"Returns number of available elements\"\"\"
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
        'from ..primitives import Type',
        'from dlkit.abstract_osid.osid import errors',
        'from dlkit.primordium.locale.types.string import get_type_data',
        'from .. import utilities',
    ]

    init = """
    def __init__(self):
        self._records = dict()
        # _load_records is in OsidExtensibleQuery:
        # _all_supported_record_type_ids comes from inheriting query object
        # THIS SHOULD BE RE-DONE:
        self._load_records(self._all_supported_record_type_ids)
        self._query_terms = {}

    def _get_string_match_value(self, string, string_match_type):
        \"\"\"Gets the match value\"\"\"
        if string_match_type == Type(**get_type_data(\'EXACT\')):
            return string
        elif string_match_type == Type(**get_type_data(\'IGNORECASE\')):
            return re.compile('^' + string, re.I)
        elif string_match_type == Type(**get_type_data(\'WORD\')):
            return re.compile('.*' + string + '.*')
        elif string_match_type == Type(**get_type_data(\'WORDIGNORECASE\')):
            return re.compile('.*' + string + '.*', re.I)

    @utilities.arguments_not_none
    def _add_match(self, match_key, match_value, match=True):
        \"\"\"Adds a match key/value\"\"\"
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

    @utilities.arguments_not_none
    def _match_display_text(self, element_key, string, string_match_type, match):
        \"\"\"Matches a display text value\"\"\"
        match_value = self._get_string_match_value(string, string_match_type)
        self._add_match(element_key + '.text', match_value, match)

    @utilities.arguments_not_none
    def _match_minimum_decimal(self, match_key, decimal_value, match=True):
        \"\"\"Matches a minimum decimal value\"\"\"
        if match:
            gtelt = '$gte'
        else:
            gtelt = '$lt'
        if match_key in self._query_terms:
            self._query_terms[match_key][gtelt] = decimal_value
        else:
            self._query_terms[match_key] = {gtelt: decimal_value}

    @utilities.arguments_not_none
    def _match_maximum_decimal(self, match_key, decimal_value, match=True):
        \"\"\"Matches a minimum decimal value\"\"\"
        if match:
            ltegt = '$lte'
        else:
            ltegt = '$gt'
        if match_key in self._query_terms:
            self._query_terms[match_key][ltegt] = decimal_value
        else:
            self._query_terms[match_key] = {ltegt: decimal_value}

    @utilities.arguments_not_none
    def _match_minimum_date_time(self, match_key, date_time_value, match=True):
        \"\"\"Matches a minimum date time value\"\"\"
        if match:
            gtelt = '$gte'
        else:
            gtelt = '$lt'
        if match_key in self._query_terms:
            self._query_terms[match_key][gtelt] = date_time_value
        else:
            self._query_terms[match_key] = {gtelt: date_time_value}

    @utilities.arguments_not_none
    def _match_maximum_date_time(self, match_key, date_time_value, match=True):
        \"\"\"Matches a maximum date time value\"\"\"
        if match:
            gtelt = '$lte'
        else:
            gtelt = '$gt'
        if match_key in self._query_terms:
            self._query_terms[match_key][gtelt] = date_time_value
        else:
            self._query_terms[match_key] = {gtelt: date_time_value}

    def _clear_terms(self, match_key):
        \"\"\"clears all match_key term values\"\"\"
        try:
            del self._query_terms[match_key]
        except KeyError:
            pass

    def _clear_minimum_terms(self, match_key):
        \"\"\"clears minimum match_key term values\"\"\"
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
        \"\"\"clears maximum match_key term values\"\"\"
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
        'from dlkit.abstract_osid.osid import errors',
    ]

    match_id = """
        self._add_match('id_', id_.get_identifier(), match)"""
    
    clear_id_terms = """
        self._clear_terms('id_')"""

class OsidExtensibleQuery:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'import importlib',
        'from ..primitives import Id',
    ]

    init = """
    def _load_records(self, record_type_idstrs):
        \"\"\"Loads query records\"\"\"
        for record_type_idstr in record_type_idstrs:
            try:
                self._init_record(record_type_idstr)
            except (ImportError, KeyError):
                pass

    def _init_record(self, record_type_idstr):
        \"\"\"Initializes a query record\"\"\"
        record_type_data = self._all_supported_record_type_data_sets[Id(record_type_idstr).get_identifier()]
        module = importlib.import_module(record_type_data['module_path'])
        record = getattr(module, record_type_data['query_record_class_name'])
        self._records[record_type_idstr] = record(self)
"""

class OsidObjectQuery:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
    ]

    match_display_name = """
        self._match_display_text('displayName', display_name, string_match_type, match)"""

    match_any_display_name = """
        raise errors.Unimplemented()"""

    clear_display_name_terms = """
        self._clear_terms('displayName.text')"""
    
    match_description = """
        self._match_display_text('description', description, string_match_type, match)"""

    match_any_description = """
        raise errors.Unimplemented()"""

    clear_description_terms = """
        self._clear_terms('description.text')"""

class OsidQueryInspector:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
    ]

class OsidRecord:

    consider_init = """
    def __init__(self):
        # This is set in implemented Records.  Should super __init__
        self._implemented_record_type_identifiers = None

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
        'from dlkit.abstract_osid.osid import errors',
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
            raise errors.IllegalState()
        return self._kwargs['${var_name}']"""

    supports_coordinate_type_template = """
        # Implemented from template for osid.Metadata.supports_coordinate_type
        if self._kwargs['syntax'] not in ${syntax_list}:
            raise errors.IllegalState()
        return ${arg0_name} in self.get_${var_name}"""

    get_existing_cardinal_values_template = """
        # Implemented from template for osid.Metadata.get_existing_cardinal_values_template
        # This template may only work well for very primitive return types, like string or cardinal.
        # Need to update it to support DisplayName, or Id etc.
        if self._kwargs['syntax'] not in ${syntax_list}:
            raise errors.IllegalState()
        return self._kwargs['${var_name}']"""


class OsidNode:

    init = """
    def __init__(self, node_map):
        self._my_map = node_map
"""

    is_root = """
        return self._my_map['root']"""

    has_parents = """
        return bool(self._my_map['parentNodes'])"""

    get_parent_ids = """
        id_list = []
        from ..id.objects import IdList
        for parent_node in self._my_map['parentNodes']:
            id_list.append(parent_node['id'])
        return IdList(id_list)"""

    is_leaf = """
        return self._my_map['leaf']"""

    has_children = """
        return bool(self._my_map['childNodes'])"""

    get_child_ids = """
        id_list = []
        from ..id.objects import IdList
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

class Property:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
    ]


class OsidReceiver:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
    ]


class OsidSearchOrder:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
    ]

class OsidSearch:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
    ]
