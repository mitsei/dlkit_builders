
class OsidProfile:

    import_statements = [
        'from . import profile',
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
        'from ..primitives import Type',
        'from ..utilities import set_json_client'
    ]

    init = """

    def __init__(self):
        self._runtime = None
        self._config = None

    def _initialize_manager(self, runtime):
        \"\"\"Sets the runtime, configuration and json client\"\"\"
        if self._runtime is not None:
            raise errors.IllegalState('this manager has already been initialized.')
        self._runtime = runtime
        self._config = runtime.get_configuration()
        set_json_client(runtime)
"""

    get_id = """
        return Id(**profile.ID)"""

    get_display_name = """
        return DisplayText(
            text=profile.DISPLAYNAME,
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
        # THIS ALL NEEDS TO BE FIXED:
        # try:
        #    from ..installation.primitives import Version
        # except:
        #    from .common import Version
        # try:
        #    from ..type.primitives import Type
        # except:
        #    from .common import Type
        # return Version(
        #    components=profile.VERSIONCOMPONENTS,
        #    scheme=Type(**profile.VERSIONSCHEME))
        raise errors.Unimplemented()"""

    get_release_date = """
        # NEED TO IMPLEMENT
        raise errors.Unimplemented()"""

    supports_osid_version = """
        # THIS ALL NEEDS TO BE FIXED:
        # try:
        #    from ..installation.primitives import Version
        # except:
        #    from .common import Version
        # try:
        #    from ..type.primitives import Type
        # except:
        #    from .common import Type
        # return Version(
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
        'from .. import JSON_CLIENT',
        'from dlkit.abstract_osid.proxy.rules import Proxy as abc_proxy',
    ]

    init = """
    def __init__(self):
        OsidProfile.__init__(self)"""

    initialize = """
        OsidProfile._initialize_manager(self, runtime)"""

    additional_methods = """
    def _proxy_in_args(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, abc_proxy):
                return True
        if 'proxy' in kwargs and kwargs['proxy'] is not None:
            return True
        else:
            return False"""


class OsidProxyManager:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
    ]

    init = """
    def __init__(self):
        OsidProfile.__init__(self)"""

    initialize = """
        OsidProfile._initialize_manager(self, runtime)"""


class OsidRuntimeManager:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
    ]

    init = """
    def __init__(self, configuration_key=None):
        self._configuration_key = configuration_key"""


class Identifiable:

    import_statements = [
        'from ..primitives import Id',
        'from dlkit.abstract_osid.osid import errors',
    ]

    init = """
    _namespace = 'osid.Identifiable'

    def __init__(self, runtime=None):
        self._set_authority(runtime)
        self._my_map = {}

    def _set_authority(self, runtime):
        try:
            authority_param_id = Id('parameter:authority@json')
            self._authority = runtime.get_configuration().get_value_by_parameter(
                authority_param_id).get_string_value()
        except (AttributeError, KeyError, errors.NotFound):
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
        'from ..utilities import get_registry',
        'from collections import OrderedDict'
    ]

    init = """
    def __init__(self, object_name, runtime=None, proxy=None, **kwargs):
        self._records = OrderedDict()
        self._supported_record_type_ids = []
        self._record_type_data_sets = get_registry(object_name + '_RECORD_TYPES', runtime)
        self._runtime = runtime
        self._proxy = proxy

    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith('__'):
                yield attr

    def __getitem__(self, item):
        return getattr(self, item)

    def __getattribute__(self, name):
        if not name.startswith('_'):
            if '_records' in self.__dict__:
                for record in reversed(self._records):
                    try:
                        return self._records[record][name]
                    except AttributeError:
                        pass
        return object.__getattribute__(self, name)

    def __getattr__(self, name):
        if '_records' in self.__dict__:
            for record in reversed(self._records):
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
                record_initialized = self._init_record(str(record_type))
                if record_initialized:
                    self._my_map['recordTypeIds'].append(str(record_type))

    def _init_record(self, record_type_idstr):
        \"\"\"Initialize the record identified by the record_type_idstr.\"\"\"
        import importlib
        record_type_data = self._record_type_data_sets[Id(record_type_idstr).get_identifier()]
        module = importlib.import_module(record_type_data['module_path'])
        record = getattr(module, record_type_data['object_record_class_name'], None)
        # only add recognized records ... so apps don't break
        # if new records are injected by another app
        if record is not None:
            self._records[record_type_idstr] = record(self)
            return True
        else:
            return False

    def _delete(self):
        \"\"\"Override this method in inheriting objects to perform special clearing operations.\"\"\"
        try:
            for record in self._records:
                try:
                    self._records[record]._delete()
                except AttributeError:
                    pass
        except AttributeError:
            pass

    def _get_provider_manager(self, osid, local=False):
        \"\"\"Gets the most appropriate provider manager depending on config.\"\"\"
        return get_provider_manager(osid,
                                    runtime=self._runtime,
                                    proxy=getattr(self, '_proxy', None),
                                    local=local)"""

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
        now = DateTime.utcnow()
        return self.get_start_date() <= now and self.get_end_date() >= now"""

    get_start_date = """
        sdate = self._my_map['startDate']
        return DateTime(
            sdate.year,
            sdate.month,
            sdate.day,
            sdate.hour,
            sdate.minute,
            sdate.second,
            sdate.microsecond)"""

    get_end_date = """
        edate = self._my_map['endDate']
        return DateTime(
            edate.year,
            edate.month,
            edate.day,
            edate.hour,
            edate.minute,
            edate.second,
            edate.microsecond)"""


class Containable:

    init = """
    def __init__(self):
        self._my_map = {}"""

    is_sequestered = """
        return self._my_map['sequestered']"""


class Sourceable:

    import_statements = [
        'from dlkit.primordium.id.primitives import Id',
        'from dlkit.primordium.locale.primitives import DisplayText',
        'from .. import types'
    ]

    get_provider_id = """
        if 'providerId' not in self._my_map or not self._my_map['providerId']:
            raise errors.IllegalState('this sourceable object has no provider set')
        return Id(self._my_map['providerId'])"""

    get_provider = """
        if 'providerId' not in self._my_map or not self._my_map['providerId']:
            raise errors.IllegalState('this sourceable object has no provider set')
        mgr = self._get_provider_manager('RESOURCE')
        lookup_session = mgr.get_resource_lookup_session()  # What about the Proxy?
        lookup_session.use_federated_bin_view()
        return lookup_session.get_resource(self.get_provider_id())"""

    get_branding_ids = """
        from ..id.objects import IdList
        if 'brandingIds' not in self._my_map:
            return IdList([])
        id_list = []
        for idstr in self._my_map['brandingIds']:
            id_list.append(Id(idstr))
        return IdList(id_list)"""

    get_branding = """
        mgr = self._get_provider_manager('REPOSITORY')
        lookup_session = mgr.get_asset_lookup_session()
        lookup_session.use_federated_repository_view()
        return lookup_session.get_assets_by_ids(self.get_branding_ids())"""

    get_license = """
        if 'license' in self._my_map:
            license_text = self._my_map['license']
            return DisplayText(display_text_map=license_text)
        return DisplayText(text='',
                           language_type=types.Language().get_type_data('DEFAULT'),
                           format_type=types.Format().get_type_data('DEFAULT'),
                           script_type=types.Script().get_type_data('DEFAULT'))"""


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
        '# import inflection',
        'import datetime',
        'from ..primitives import Id',
        'from ..primitives import Type',
        'from dlkit.abstract_osid.osid import errors',
        'from bson.objectid import ObjectId',
        'from importlib import import_module',
        'from ..locale.objects import Locale',
        'from ..utilities import PHANTOM_ROOT_IDENTIFIER',
        'from ..utilities import JSONClientValidated',
        'from ..utilities import get_provider_manager',
        'from ..utilities import is_authenticated_with_proxy',
        'from ..utilities import get_authenticated_agent_id_with_proxy',
        'from ..utilities import get_authenticated_agent_with_proxy',
        'from ..utilities import get_effective_agent_id_with_proxy',
        'from ..utilities import get_effective_agent_with_proxy',
        'from ..utilities import get_locale_with_proxy',
        'from ..utilities import make_catalog_map',
        'from ..utilities import camel_to_under',
        'from ..cataloging.objects import Catalog',
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
        self._catalog_identifier = None
        self._my_catalog_map = None
        self._catalog_id = None
        self._catalog = None
        self._forms = None
        self._object_view = COMPARATIVE
        self._catalog_view = ISOLATED
        self._effective_view = ANY_EFFECTIVE
        self._authority = 'ODL.MIT.EDU'
        self._cataloging_manager = None
        self._catalog_session = None

    def _init_proxy_and_runtime(self, proxy, runtime):
        self._proxy = proxy
        self._runtime = runtime
        if runtime is not None:
            try:
                authority_param_id = Id('parameter:authority@mongo')
                self._authority = runtime.get_configuration().get_value_by_parameter(
                    authority_param_id).get_string_value()
            except (KeyError, errors.NotFound):
                self._authority = 'ODL.MIT.EDU'

    def _init_catalog(self, proxy=None, runtime=None):
        \"\"\"Initialize this session as an OsidCatalog based session.\"\"\"
        self._init_proxy_and_runtime(proxy, runtime)
        osid_name = self._session_namespace.split('.')[0]
        try:
            config = self._runtime.get_configuration()
            parameter_id = Id('parameter:' + osid_name + 'CatalogingProviderImpl@mongo')
            provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
            self._cataloging_manager = self._runtime.get_manager('CATALOGING', provider_impl)  # need to add version argument
        except (AttributeError, KeyError, errors.NotFound):
            pass

    def _init_object(self, catalog_id, proxy, runtime, db_name, cat_name, cat_class):
        \"\"\"Initialize this session an OsidObject based session.\"\"\"
        self._catalog_identifier = None
        self._init_proxy_and_runtime(proxy, runtime)

        uses_cataloging = False
        if catalog_id is not None and catalog_id.get_identifier() != PHANTOM_ROOT_IDENTIFIER:
            self._catalog_identifier = catalog_id.get_identifier()

            config = self._runtime.get_configuration()
            parameter_id = Id('parameter:' + db_name + 'CatalogingProviderImpl@mongo')

            try:
                provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
            except (AttributeError, KeyError, errors.NotFound):
                collection = JSONClientValidated(db_name,
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
                uses_cataloging = True
                cataloging_manager = self._runtime.get_manager('CATALOGING',
                                                               provider_impl)  # need to add version argument
                lookup_session = cataloging_manager.get_catalog_lookup_session()
                self._my_catalog_map = lookup_session.get_catalog(catalog_id)._my_map
                self._catalog = Catalog(osid_object_map=self._my_catalog_map, runtime=self._runtime,
                                        proxy=self._proxy)
        else:
            self._catalog_identifier = PHANTOM_ROOT_IDENTIFIER
            self._my_catalog_map = make_catalog_map(cat_name, identifier=self._catalog_identifier)

        if not uses_cataloging:
            self._catalog = cat_class(osid_object_map=self._my_catalog_map, runtime=self._runtime, proxy=self._proxy)

        self._catalog._authority = self._authority  # there should be a better way...
        self._catalog_id = self._catalog.get_id()
        self._forms = dict()

    def _get_phantom_root_catalog(self, cat_name, cat_class):
        \"\"\"Get's the catalog id corresponding to the root of all implementation catalogs.\"\"\"
        catalog_map = make_catalog_map(cat_name, identifier=PHANTOM_ROOT_IDENTIFIER)
        return cat_class(osid_object_map=catalog_map, runtime=self._runtime, proxy=self._proxy)

    def _create_orchestrated_cat(self, foreign_catalog_id, db_name, cat_name):
        \"\"\"Creates a catalog in the current service orchestrated with a foreign service Id.\"\"\"
        if (foreign_catalog_id.identifier_namespace == db_name + '.' + cat_name and
                foreign_catalog_id.authority == self._authority):
            raise errors.NotFound()  # This is not a foreign catalog
        foreign_service_name = foreign_catalog_id.get_identifier_namespace().split('.')[0]
        # foreign_cat_name = inflection.underscore(foreign_catalog_id.namespace.split('.')[1])
        # catalog_name = foreign_cat_name.lower()
        catalog_name = camel_to_under(foreign_catalog_id.namespace.split('.')[1])
        manager = self._get_provider_manager(foreign_service_name.upper())
        lookup_session = getattr(manager, 'get_{0}_lookup_session'.format(catalog_name))(proxy=self._proxy)
        getattr(lookup_session, 'get_{0}'.format(catalog_name))(foreign_catalog_id)  # Raises NotFound
        collection = JSONClientValidated(db_name,
                                         collection=cat_name,
                                         runtime=self._runtime)
        foreign_identifier = ObjectId(foreign_catalog_id.get_identifier())
        default_text = 'Orchestrated ' + foreign_service_name
        catalog_map = make_catalog_map(cat_name, identifier=foreign_identifier, default_text=default_text)
        collection.insert_one(catalog_map)
        alias_id = Id(identifier=foreign_catalog_id.identifier,
                      namespace=db_name + '.' + cat_name,
                      authority=self._authority)
        try:
            admin_session = getattr(manager, 'get_{0}_admin_session'.format(catalog_name))(proxy=self._proxy)
            getattr(admin_session, 'alias_{0}'.format(catalog_name))(foreign_catalog_id, alias_id)
        except (errors.Unimplemented, AttributeError):
            pass
        return catalog_map

    def _get_provider_manager(self, osid, local=False):
        \"\"\"Gets the most appropriate provider manager depending on config.\"\"\"
        return get_provider_manager(osid, runtime=self._runtime, proxy=self._proxy, local=local)

    def _get_id(self, id_, pkg_name):
        \"\"\"
        Returns the primary id given an alias.

        If the id provided is not in the alias table, it will simply be
        returned as is.

        Only looks within the Id Alias namespace for the session package

        \"\"\"
        collection = JSONClientValidated('id',
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
        collection = JSONClientValidated(pkg_name,
                                         collection=obj_name,
                                         runtime=self._runtime)
        collection.find_one({'_id': ObjectId(primary_id.get_identifier())})  # to raise NotFound
        collection = JSONClientValidated('id',
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
        def get_descendent_ids(h_session):
            idstr_list = [str(cat_id)]
            if h_session is None:
                pkg_name = cat_id.get_identifier_namespace().split('.')[0]
                cat_name = cat_id.get_identifier_namespace().split('.')[1]
                try:
                    mgr = self._get_provider_manager('HIERARCHY')
                    h_session = mgr.get_hierarchy_traversal_session_for_hierarchy(
                        Id(authority=pkg_name.upper(),
                           namespace='CATALOG',
                           identifier=cat_name.upper()),
                        proxy=self._proxy)
                except (errors.OperationFailed, errors.Unsupported):
                    return idstr_list  # there is no hierarchy
            if h_session.has_children(cat_id):
                for child_id in h_session.get_children(cat_id):
                    idstr_list += self._get_descendent_cat_idstrs(child_id, h_session)
            return list(set(idstr_list))

        use_caching = False
        try:
            config = self._runtime.get_configuration()
            parameter_id = Id('parameter:useCachingForQualifierIds@json')
            if config.get_value_by_parameter(parameter_id).get_boolean_value():
                use_caching = True
            else:
                pass
        except (AttributeError, KeyError, errors.NotFound):
            pass
        if use_caching:
            import memcache
            mc = memcache.Client(['127.0.0.1:11211'], debug=0)

            key = 'descendent-catalog-ids-{0}'.format(str(cat_id))

            catalog_ids = mc.get(key)
            if catalog_ids is None:
                catalog_ids = get_descendent_ids(hierarchy_session)
                mc.set(key, catalog_ids)
        else:
            catalog_ids = get_descendent_ids(hierarchy_session)
        return catalog_ids

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
            now = datetime.datetime.utcnow()
            return {'startDate': {'$$lte': now}, 'endDate': {'$$gte': now}}
        return {}

    def _view_filter(self):
        \"\"\"
        Returns the mongodb catalog filter for isolated or federated views.

        This also searches across all underlying catalogs in federated
        catalog views. Real authz for controlling access to underlying
        catalogs will need to be managed in an adapter above the
        pay grade of this implementation.

        \"\"\"
        if self._is_phantom_root_federated():
            return {}
        idstr_list = self._get_catalog_idstrs()
        return {'assigned' + self._catalog_name + 'Ids': {'$in': idstr_list}}
        # return {'assigned' + utilities.format_catalog(self._catalog_name) + 'Ids': {'$in': idstr_list}}

    def _assign_object_to_catalog(self, obj_id, cat_id):
        pkg_name = obj_id.get_identifier_namespace().split('.')[0]
        obj_name = obj_id.get_identifier_namespace().split('.')[1]
        catalog_key = 'assigned' + self._catalog_name + 'Ids'
        collection = JSONClientValidated(pkg_name,
                                         collection=obj_name,
                                         runtime=self._runtime)
        obj_map = collection.find_one({'_id': ObjectId(obj_id.get_identifier())})
        if catalog_key in obj_map:
            if str(cat_id) in obj_map[catalog_key]:
                raise errors.AlreadyExists()
            else:
                obj_map[catalog_key].append(str(cat_id))
        else:
            obj_map[catalog_key] = [str(cat_id)]
        collection.save(obj_map)

    def _unassign_object_from_catalog(self, obj_id, cat_id):
        pkg_name = obj_id.get_identifier_namespace().split('.')[0]
        obj_name = obj_id.get_identifier_namespace().split('.')[1]
        catalog_key = 'assigned' + self._catalog_name + 'Ids'
        collection = JSONClientValidated(pkg_name,
                                         collection=obj_name,
                                         runtime=self._runtime)
        obj_map = collection.find_one({'_id': ObjectId(obj_id.get_identifier())})
        if obj_map[catalog_key] == [str(cat_id)]:
            raise errors.OperationFailed('unassigning object from ${cat_name_under} would leave it unattached')
        try:
            obj_map[catalog_key].remove(str(cat_id))
        except (KeyError, ValueError):
            raise errors.NotFound()
        collection.save(obj_map)"""

    get_locale = """
        return get_locale_with_proxy(self._proxy)"""

    is_authenticated = """
        return is_authenticate_with_proxy(self._proxy)"""

    get_authenticated_agent_id = """
        return get_authenticated_agent_id_with_proxy(self._proxy)"""

    get_authenticated_agent = """
        return get_authenticated_agent_with_proxy(self._proxy)"""

    get_effective_agent_id = """
        return get_effective_agent_id_with_proxy(self._proxy)"""

    get_effective_agent = """
        return get_effective_agent_id_with_proxy(self._proxy)  # Currently raises Unimplemented"""

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
    _namespace = 'osid.OsidObject'

    def __init__(self, osid_object_map, runtime=None, **kwargs):
        osid_markers.Identifiable.__init__(self, runtime=runtime)
        osid_markers.Extensible.__init__(self, runtime=runtime, **kwargs)
        self._my_map = osid_object_map
        self._load_records(osid_object_map['recordTypeIds'])

    def get_object_map(self, obj_map=None):
        if obj_map is None:
            obj_map = dict(self._my_map)
        del obj_map['_id']

        obj_map['displayName']['text'] = self.display_name.text
        obj_map['displayName']['languageTypeId'] = str(self.display_name.language_type)
        obj_map['displayName']['scriptTypeId'] = str(self.display_name.script_type)
        obj_map['description']['text'] = self.description.text
        obj_map['description']['languageTypeId'] = str(self.description.language_type)
        obj_map['description']['scriptTypeId'] = str(self.description.script_type)
        obj_map['genusTypeId'] = str(self.genus_type)
        # Note: The following should be deprecated:
        try:
            obj_map[utilities.caps_to_mixed(self._catalog_name) + 'Id'] = obj_map['assigned' + self._catalog_name + 'Ids'][0]
        except AttributeError:
            # catalogs do not have this attribute
            pass

        try:  # Need to implement records for catalogs one of these days
            for record in self._records:
                try:
                    self._records[record]._update_object_map(obj_map)
                except AttributeError:
                    pass
        except AttributeError:
            pass

        obj_map.update(
            {'type': self._namespace.split('.')[-1],
             'id': str(self.get_id())})
        return obj_map

    object_map = property(get_object_map)"""

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


class OsidCatalog:

    init = """
    _namespace = 'osid.OsidCatalog'

    def __init__(self, **kwargs):
        OsidObject.__init__(self, **kwargs)
        # Should we initialize Sourceable?
        # Should we initialize Federatable?
    """


class OsidRule:

    has_rule = """
        # Someday I'll have a real implementation, but for now I just:
        return False"""

    get_rule_id = """
        # Someday I'll have a real implementation, but for now I just:
        raise errors.IllegalState()"""

    get_rule = """
        # Someday I'll have a real implementation, but for now I just:
        raise errors.IllegalState()"""


class OsidForm:

    import_statements = [
        'from ..primitives import Id',
        'from dlkit.abstract_osid.osid import errors',
        'from . import default_mdata',
        'from .metadata import Metadata',
        'from ..utilities import get_locale_with_proxy',
        'from ..utilities import update_display_text_defaults',
        'from ..utilities import is_string',
        'import uuid',
        'from decimal import Decimal',
        'from dlkit.abstract_osid.id.primitives import Id as abc_id',
        'from dlkit.abstract_osid.type.primitives import Type as abc_type',
        'from dlkit.abstract_osid.calendaring.primitives import DateTime as abc_datetime',
        'from dlkit.abstract_osid.calendaring.primitives import Duration as abc_duration'
    ]

    init = """
    # pylint: disable=no-self-use
    # MUCH OF THIS SHOULD BE MOVED TO A UTILITY MODULE

    _namespace = 'osid.OsidForm'

    def __init__(self, runtime=None, proxy=None, **kwargs):
        self._identifier = str(uuid.uuid4())
        self._mdata = None
        self._for_update = None
        self._runtime = None  # This is now being set in Extensible by higher order objects
        self._proxy = None  # This is now being set in Extensible by higher order objects
        self._kwargs = kwargs
        self._locale_map = dict()
        locale = get_locale_with_proxy(proxy)
        self._locale_map['languageTypeId'] = str(locale.get_language_type())
        self._locale_map['scriptTypeId'] = str(locale.get_script_type())
        if runtime is not None:
            self._set_authority(runtime=runtime)
        else:
            self._authority = 'ODL.MIT.EDU'
        if 'catalog_id' in kwargs:
            self._catalog_id = kwargs['catalog_id']

    def _init_metadata(self):
        \"\"\"Initialize OsidObjectForm metadata.\"\"\"

        # pylint: disable=attribute-defined-outside-init
        # this method is called from descendent __init__
        self._mdata.update(default_mdata.get_osid_form_mdata())
        update_display_text_defaults(self._mdata['journal_comment'], self._locale_map)
        for element_name in self._mdata:
            self._mdata[element_name].update(
                {'element_id': Id(self._authority,
                                  self._namespace,
                                  element_name)})
        self._journal_comment_default = self._mdata['journal_comment']['default_string_values'][0]
        self._validation_messages = {}

    def _init_map(self):
        self._journal_comment = self._journal_comment_default

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
        syntax = metadata.get_syntax()

        # First check if this is a required data element
        if metadata.is_required and not inpt:
            return False

        valid = True  # Innocent until proven guilty
        # Recursively run through all the elements of an array
        if array:
            if len(inpt) < metadata.get_minimum_elements():
                valid = False
            elif len(inpt) > metadata.get_maximum_elements():
                valid = False
            else:
                for element in inpt:
                    valid = (valid and self._is_valid_input(element, metadata, False))

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
        from dlkit.abstract_osid.id.primitives import Id as abc_id
        if isinstance(inpt, abc_id):
            return True
        else:
            return False

    def _is_valid_type(self, inpt):
        \"\"\"Checks if input is a valid Type\"\"\"
        from dlkit.abstract_osid.type.primitives import Type as abc_type
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
        if not is_string(inpt):
            return False
        if metadata.get_minimum_string_length() and len(inpt) < metadata.get_minimum_string_length():
            return False
        elif metadata.get_maximum_string_length() and len(inpt) > metadata.get_maximum_string_length():
            return False
        if metadata.get_string_set() and inpt not in metadata.get_string_set():
            return False
        else:
            return True

    def _get_display_text(self, inpt, metadata):
        if metadata.is_read_only():
            raise errors.NoAccess()
        if isinstance(inpt, abc_display_text):
            display_text = {
                'text': inpt.text,
                'languageTypeId': str(inpt.language_type),
                'formatTypeId': str(inpt.format_type),
                'scriptTypeId': str(inpt.script_type)
            }
        elif self._is_valid_string(inpt, metadata):
            display_text = dict(metadata.get_default_string_values()[0])
            display_text.update({'text': inpt})
        else:
            raise errors.InvalidArgument()
        return display_text

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
        if not isinstance(inpt, Decimal):
            inpt = Decimal(str(inpt))
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
        from dlkit.abstract_osid.calendaring.primitives import DateTime as abc_datetime
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
        from dlkit.abstract_osid.calendaring.primitives import Duration as abc_duration
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
        return False"""

    is_for_update = """
        return self._for_update"""

    get_default_locale = """
        from ..locale.objects import Locale
        # If no constructor arguments are given it is expected that the
        # locale service will return the default Locale.
        return get_locale_with_proxy(self._proxy)"""

    get_locales = """
        # Someday I might have a real implementation
        # For now only default Locale is supported
        from ..locale.objects import LocaleList
        return LocaleList([])"""

    set_locale = """
        # Someday I might have a real implementation
        # For now only default Locale is supported
        self._locale_map['languageType'] = language_type
        self._locale_map['scriptType'] = script_type"""

    get_journal_comment_metadata = """
        return Metadata(**self._mdata['journal_comment'])"""

    set_journal_comment = """
        self._my_map['journal_comment'] = self._get_display_text(comment, self.get_journal_comment_metadata())"""

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
    def __init__(self, **kwargs):
        osid_markers.Extensible.__init__(self, **kwargs)

    def _init_map(self, record_types):
        self._my_map['recordTypeIds'] = []
        if record_types is not None:
            self._init_records(record_types)
        self._supported_record_type_ids = self._my_map['recordTypeIds']

    def _get_record(self, record_type):
        \"\"\"This overrides _get_record in osid.Extensible.

        Perhaps we should leverage it somehow?

        \"\"\"
        if (not self.has_record_type(record_type) and
                record_type.get_identifier() not in self._record_type_data_sets):
            raise errors.Unsupported()
        if str(record_type) not in self._records:
            record_initialized = self._init_record(str(record_type))
            if record_initialized and str(record_type) not in self._my_map['recordTypeIds']:
                self._my_map['recordTypeIds'].append(str(record_type))
        return self._records[str(record_type)]

    def _init_record(self, record_type_idstr):
        \"\"\"Override this from osid.Extensible because Forms use a different
        attribute in record_type_data.\"\"\"
        record_type_data = self._record_type_data_sets[Id(record_type_idstr).get_identifier()]
        module = importlib.import_module(record_type_data['module_path'])
        record = getattr(module, record_type_data['form_record_class_name'])
        if record is not None:
            self._records[record_type_idstr] = record(self)
            return True
        else:
            return False"""


class OsidTemporalForm:

    import_statements = [
        'from ..primitives import Id',
        'from dlkit.abstract_osid.osid import errors',
        'import datetime',
        'from . import default_mdata',
        'from .metadata import Metadata',
    ]

    init = """
    _namespace = "osid.OsidTemporalForm"

    def __init__(self):
        self._mdata = None

    def _init_metadata(self, **kwargs):
        # pylint: disable=attribute-defined-outside-init
        # this method is called from descendent __init__
        self._mdata.update(default_mdata.get_osid_temporal_mdata())
        self._mdata['start_date'].update({'default_date_time_values': [datetime.datetime.utcnow()]})
        self._mdata['end_date'].update({
            'default_date_time_values': [datetime.datetime.utcnow() + datetime.timedelta(weeks=9999)]
        })

    def _init_map(self):
        # pylint: disable=attribute-defined-outside-init
        # this method is called from descendent __init__
        self._my_map['startDate'] = self._mdata['start_date']['default_date_time_values'][0]
        self._my_map['endDate'] = self._mdata['end_date']['default_date_time_values'][0]
"""

    get_start_date_metadata = """
        metadata = dict(self._mdata['start_date'])
        metadata.update({'existing_date_time_values': self._my_map['startDate']})
        return Metadata(**metadata)"""

    set_start_date = """
        if self.get_start_date_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_date_time(date, self.get_start_date_metadata()):
            raise errors.InvalidArgument()
        # self._my_map['startDate'] = self._get_date_map(date)
        self._my_map['startDate'] = date"""

    clear_start_date = """
        if (self.get_start_date_metadata().is_read_only() or
                self.get_start_date_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['startDate'] = self._mdata['start_date']['default_date_time_values'][0]"""

    get_end_date_metadata = """
        metadata = dict(self._mdata['end_date'])
        metadata.update({'existing_date_time_values': self._my_map['endDate']})
        return Metadata(**metadata)"""

    set_end_date = """
        if self.get_end_date_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_date_time(date, self.get_end_date_metadata()):
            raise errors.InvalidArgument()
        # self._my_map['endDate'] = self._get_date_map(date)
        self._my_map['endDate'] = date"""

    clear_end_date = """
        if (self.get_end_date_metadata().is_read_only() or
                self.get_end_date_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['endDate'] = self._mdata['end_date']['default_date_time_values'][0]"""

    additional_methods = """
    # This should go in a utility module:
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
        self._mdata = None
        self._sequestered_default = None
        self._sequestered = None

    def _init_metadata(self):
        self._mdata.update(default_mdata.get_osid_containable_mdata())
        self._sequestered_default = self._mdata['sequestered']['default_boolean_values'][0]
        self._sequestered = self._sequestered_default

    def _init_map(self):
        self._my_map['sequestered'] = self._sequestered_default"""

    get_sequestered_metadata = """
        return Metadata(**self._mdata['sequestered'])"""

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
        self._mdata = None
        self._provider_default = None
        self._branding_default = None
        self._license_default = None
        self._catalog_id = None  # Why is this here?

    def _init_metadata(self):
        # pylint: disable=attribute-defined-outside-init
        # this method is called from descendent __init__
        self._mdata.update(default_mdata.get_osid_sourceable_mdata())
        update_display_text_defaults(self._mdata['license'], self._locale_map)
        self._provider_default = str(self._mdata['provider']['default_id_values'][0])
        self._branding_default = list(self._mdata['branding']['default_id_values'])
        self._license_default = dict(self._mdata['license']['default_string_values'][0])

    def _init_map(self, **kwargs):
        if 'effective_agent_id' in kwargs:
            try:
                mgr = self._get_provider_manager('RESOURCE', local=True)
                agent_session = mgr.get_resource_agent_session(proxy=self._proxy)
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
        self._my_map['license'] = dict(self._license_default)"""

    get_provider_metadata = """
        metadata = dict(self._mdata['provider'])
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
        metadata = dict(self._mdata['branding'])
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
        metadata = dict(self._mdata['license'])
        metadata.update({'existing_string_values': self._my_map['license']})
        return Metadata(**metadata)"""

    set_license = """
        self._my_map['license'] = self._get_display_text(license_, self.get_license_metadata())"""

    clear_license = """
        if (self.get_license_metadata().is_read_only() or
                self.get_license_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['license'] = dict(self._license_default)"""


class OsidFederateableForm:

    init = """
    def __init__(self):
        pass"""


class OsidOperableForm:

    init = """
    def __init__(self):
        # Need to implement someday
        pass

    def _init_metadata(self):
        # Need to implement someday
        pass

    def _init_map(self):
        # Need to implement someday
        pass
"""


class OsidObjectForm:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from . import default_mdata',
        'from .metadata import Metadata',
        'from dlkit.abstract_osid.locale.primitives import DisplayText as abc_display_text',
        'from ..utilities import update_display_text_defaults',
    ]

    init = """
    _namespace = "osid.OsidObjectForm"

    def __init__(self, osid_object_map=None, **kwargs):  # removed record_types=None, runtime=None,
        self._display_name_default = None
        self._description_default = None
        self._genus_type_default = None
        OsidForm.__init__(self, **kwargs)
        OsidExtensibleForm.__init__(self, **kwargs)
        if osid_object_map is not None:
            self._for_update = True
            self._my_map = osid_object_map
            self._load_records(osid_object_map['recordTypeIds'])
        else:
            self._for_update = False
            self._my_map = {}

    def _init_metadata(self, **kwargs):
        \"\"\"Initialize metadata for form\"\"\"
        self._mdata.update(default_mdata.get_osid_object_mdata())
        OsidForm._init_metadata(self)
        if 'default_display_name' in kwargs:
            self._mdata['display_name']['default_string_values'][0]['text'] = kwargs['default_display_name']
        update_display_text_defaults(self._mdata['display_name'], self._locale_map)
        if 'default_description' in kwargs:
            self._mdata['description']['default_string_values'][0]['text'] = kwargs['default_description']
        update_display_text_defaults(self._mdata['description'], self._locale_map)
        self._display_name_default = dict(self._mdata['display_name']['default_string_values'][0])
        self._description_default = dict(self._mdata['description']['default_string_values'][0])
        self._genus_type_default = self._mdata['genus_type']['default_type_values'][0]

        if 'mdata' in kwargs:
            self._mdata.update(kwargs['mdata'])

    def _init_map(self, record_types=None):
        \"\"\"Initialize map for form\"\"\"
        OsidForm._init_map(self)
        self._my_map['displayName'] = dict(self._display_name_default)
        self._my_map['description'] = dict(self._description_default)
        self._my_map['genusTypeId'] = self._genus_type_default
        OsidExtensibleForm._init_map(self, record_types)
"""

    get_display_name_metadata = """
        metadata = dict(self._mdata['display_name'])
        metadata.update({'existing_string_values': self._my_map['displayName']['text']})
        return Metadata(**metadata)"""

    set_display_name = """
        self._my_map['displayName'] = self._get_display_text(display_name, self.get_display_name_metadata())"""

    clear_display_name = """
        if (self.get_display_name_metadata().is_read_only() or
                self.get_display_name_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['displayName'] = dict(self._display_name_default)"""

    get_description_metadata = """
        metadata = dict(self._mdata['description'])
        metadata.update({'existing_string_values': self._my_map['description']['text']})
        return Metadata(**metadata)"""

    set_description = """
        self._my_map['description'] = self._get_display_text(description, self.get_description_metadata())"""

    clear_description = """
        if (self.get_description_metadata().is_read_only() or
                self.get_description_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['description'] = dict(self._description_default)"""

    get_genus_type_metadata = """
        metadata = dict(self._mdata['genus_type'])
        metadata.update({'existing_string_values': self._my_map['genusTypeId']})
        return Metadata(**metadata)"""

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
        self._my_map['genusTypeId'] = self._genus_type_default"""


class OsidRelationshipForm:

    init = """
    def __init__(self, **kwargs):
        OsidTemporalForm.__init__(self)
        OsidObjectForm.__init__(self, **kwargs)

    def _init_metadata(self, **kwargs):
        OsidTemporalForm._init_metadata(self, **kwargs)
        OsidObjectForm._init_metadata(self, **kwargs)

    def _init_map(self, record_types=None, **kwargs):
        OsidTemporalForm._init_map(self)
        OsidObjectForm._init_map(self, record_types=record_types, **kwargs)"""


class OsidCatalogForm:

    init = """
    def __init__(self, **kwargs):
        OsidSourceableForm.__init__(self)
        OsidFederateableForm.__init__(self)
        OsidObjectForm.__init__(self, **kwargs)

    def _init_metadata(self, **kwargs):
        OsidSourceableForm._init_metadata(self)
        OsidFederateableForm._init_metadata(self)
        OsidObjectForm._init_metadata(self, **kwargs)

    def _init_map(self, record_types=None, **kwargs):
        OsidSourceableForm._init_map(self, **kwargs)
        OsidFederateableForm._init_map(self)
        OsidObjectForm._init_map(self, record_types)
"""


class OsidList:
    import_statements = [
        'from pymongo.cursor import Cursor',
        'from ..utilities import OsidListList, is_string',
        'import itertools'
    ]

    init = """
    def __init__(self, iter_object=None, runtime=None, proxy=None):
        if iter_object is None:
            iter_object = []
        if isinstance(iter_object, OsidListList):
            self._count = 0
            for osid_list in iter_object:
                self._count += osid_list.available()
            iter_object = itertools.chain(*iter_object)
        elif isinstance(iter_object, dict) or isinstance(iter_object, list):
            self._count = len(iter_object)
        elif isinstance(iter_object, Cursor):
            self._count = iter_object.count(True)
        else:
            self._count = None
        self._runtime = runtime
        self._proxy = proxy
        self._iter_object = iter(iter_object)

    def __iter__(self):
        return self

    def _get_next_n(self, object_class, number=None):
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
                    next_list.append(next(self))
                except Exception:  # Need to specify exceptions here!
                    raise errors.OperationFailed()
                counter += 1
            return object_class(next_list)

    def _get_next_object(self, object_class):
        \"\"\"stub\"\"\"
        next_object = OsidList.next(self)
        if isinstance(next_object, dict):
            next_object = object_class(osid_object_map=next_object, runtime=self._runtime, proxy=self._proxy)
        elif is_string(next_object) and object_class == Id:
            next_object = Id(next_object)
        return next_object

    def next(self):
        \"\"\"next method for iterator.\"\"\"
        next_object = next(self._iter_object)
        if self._count is not None:
            self._count -= 1
        return next_object

    __next__ = next

    def len(self):
        \"\"\"Returns number of available elements\"\"\"
        return self.available()"""

    has_next = """
        if self._count is not None:
            # If count is available, use it
            return bool(self._count)
        else:
            # otherwise we have no idea
            return True"""

    available = """
        if self._count is not None:
            # If count is available, use it
            return self._count
        else:
            # We have no idea.
            return 0  # Don't know what to do here"""

    skip = """
        try:
            self._iter_object.skip(n)
        except AttributeError:
            for i in range(0, n):
                self.next()"""


class OsidQuery:

    import_statements = [
        'import re',
        'from ..primitives import Type',
        'from dlkit.abstract_osid.osid import errors',
        'from dlkit.primordium.locale.types.string import get_type_data as get_string_type_data',
        'DEFAULT_STRING_MATCH_TYPE = Type(**get_string_type_data(\'WORDIGNORECASE\'))',
        'from .. import utilities',
        'from collections import OrderedDict'
    ]

    init = """
    def __init__(self, runtime):
        self._records = OrderedDict()
        # _load_records is in OsidExtensibleQuery:
        # _all_supported_record_type_ids comes from inheriting query object
        # THIS SHOULD BE RE-DONE:
        self._load_records(self._all_supported_record_type_ids)
        self._runtime = runtime
        self._query_terms = {}
        self._keyword_terms = {}
        self._keyword_fields = ['displayName.text', 'description.text']
        try:
            # Try to get additional keyword fields from the runtime, if available:
            config = runtime.get_configuration()
            parameter_id = Id('parameter:keywordFields@json')
            additional_keyword_fields = config.get_value_by_parameter(parameter_id).get_object_value()
            self._keyword_fields += additional_keyword_fields[self._namespace]
        except (AttributeError, KeyError, errors.NotFound):
            pass

    def _get_string_match_value(self, string, string_match_type):
        \"\"\"Gets the match value\"\"\"
        if string_match_type == Type(**get_string_type_data(\'EXACT\')):
            return string
        elif string_match_type == Type(**get_string_type_data(\'IGNORECASE\')):
            return re.compile('^' + string, re.I)
        elif string_match_type == Type(**get_string_type_data(\'WORD\')):
            return re.compile('.*' + string + '.*')
        elif string_match_type == Type(**get_string_type_data(\'WORDIGNORECASE\')):
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
        try:  # clear match = True case
            del self._query_terms[match_key]['$gte']
        except KeyError:
            pass
        try:  # clear match = False case
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
        try:  # clear match = True case
            del self._query_terms[match_key]['$lte']
        except KeyError:
            pass
        try:  # clear match = False case
            del self._query_terms[match_key]['$gt']
        except KeyError:
            pass
        try:
            if self._query_terms[match_key] == {}:
                del self._query_terms[match_key]
        except KeyError:
            pass"""

    match_keyword_arg_template = {
        1: 'DEFAULT_STRING_MATCH_TYPE',
        2: True
    }

    match_keyword = """
        # Note: this currently ignores match argument
        match_value = self._get_string_match_value(keyword, string_match_type)
        for field_name in self._keyword_fields:
            if field_name not in self._keyword_terms:
                self._keyword_terms[field_name] = {'$in': list()}
            self._keyword_terms[field_name]['$in'].append(match_value)"""

    clear_keyword_terms = """
        self._keyword_terms = {}"""

    match_any = """
        match_key = '_id'
        param = '$exists'
        if match:
            flag = 'true'
        else:
            flag = 'false'
        if match_key in self._query_terms:
            self._query_terms[match_key][param] = flag
        else:
            self._query_terms[match_key] = {param: flag}"""

    clear_any_terms = """
        # How to implement this?"""


class OsidIdentifiableQuery:

    import_statements = [
        'from bson.objectid import ObjectId'
    ]

    match_id = """
        self._add_match('_id', ObjectId(id_.get_identifier()))"""

    clear_id_terms = """
        self._clear_terms('_id')"""


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
        self._records[record_type_idstr] = record(self)"""

    match_record_type = """
        self._add_match('recordTypeIds', str(record_type), match)"""


class OsidObjectQuery:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Type',
        'from dlkit.primordium.locale.types.string import get_type_data as get_string_type_data',
        'DEFAULT_STRING_MATCH_TYPE = Type(**get_string_type_data(\'WORDIGNORECASE\'))'
    ]

    init = """
    def __init__(self, runtime):
        OsidQuery.__init__(self, runtime)"""

    match_display_name_arg_template = {
        1: 'DEFAULT_STRING_MATCH_TYPE',
        2: True
    }

    match_display_name = """
        self._match_display_text('displayName', display_name, string_match_type, match)"""

    match_any_display_name = """
        raise errors.Unimplemented()"""

    clear_display_name_terms = """
        self._clear_terms('displayName.text')"""

    match_description_arg_template = {
        1: 'DEFAULT_STRING_MATCH_TYPE',
        2: True
    }

    match_description = """
        self._match_display_text('description', description, string_match_type, match)"""

    match_genus_type = """
        self._add_match('genusTypeId', str(genus_type), match)"""

    match_any_description = """
        raise errors.Unimplemented()"""

    clear_description_terms = """
        self._clear_terms('description.text')"""

    clear_genus_type_terms = """
        self._clear_terms('genusTypeId')"""


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
        return getattr(self, item)"""

    implements_record_type = """
        return record_type.get_identifier() in self._implemented_record_type_identifiers"""


class Metadata:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from dlkit.primordium.locale.primitives import DisplayText'
    ]

    init = """
    def __init__(self, **kwargs):
        self._kwargs = kwargs"""

    get_element_id_template = """
        # Implemented from template for osid.Metadata.get_element_id_template
        return self._kwargs['${var_name}']"""

    get_element_label_template = """
        # Implemented from template for osid.Metadata.get_element_id_template
        return DisplayText(self._kwargs['${var_name}'])"""

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

    import_statements = [
        'from dlkit.primordium.id.primitives import Id',
    ]

    init = """
    def __init__(self, node_map):
        self._my_map = node_map

    def get_id(self):
        \"\"\"Override markers.identifiable.get_id\"\"\"
        return Id(self._my_map['id'])

    id_ = property(fget=get_id)

    ident = property(fget=get_id)"""

    is_root = """
        return self._my_map['root']"""

    has_parents = """
        return bool(self._my_map['parentNodes'])"""

    get_parent_ids = """
        id_list = []
        from ..id.objects import IdList
        for parent_node in self._my_map['parentNodes']:
            id_list.append(str(parent_node.ident))
        return IdList(id_list)"""

    is_leaf = """
        return self._my_map['leaf']"""

    has_children = """
        return bool(self._my_map['childNodes'])"""

    get_child_ids = """
        id_list = []
        from ..id.objects import IdList
        for child_node in self._my_map['childNodes']:
            id_list.append(str(child_node.ident))
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
        return node_map"""


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
        'from dlkit.primordium.id.primitives import Id',
        'from collections import OrderedDict'
    ]

    init = """
    def __init__(self, runtime):
        self._records = OrderedDict()
        # _load_records is in OsidExtensibleQuery:
        # _all_supported_record_type_ids comes from inheriting query object
        # THIS SHOULD BE RE-DONE:
        self._load_records(self._all_supported_record_type_ids)
        self._runtime = runtime
        self._query_terms = {}
        self._keyword_terms = {}
        self._keyword_fields = ['displayName.text', 'description.text']
        try:
            # Try to get additional keyword fields from the runtime, if available:
            config = runtime.get_configuration()
            parameter_id = Id('parameter:keywordFields@json')
            additional_keyword_fields = config.get_value_by_parameter(parameter_id).get_object_value()
            self._keyword_fields += additional_keyword_fields[self._namespace]
        except (AttributeError, KeyError, errors.NotFound):
            pass
        self._limit_result_set_start = None
        self._limit_result_set_end = None"""

    limit_result_set = """
        if not isinstance(start, int) or not isinstance(end, int):
            raise errors.InvalidArgument('start and end arguments must be integers.')
        if end <= start:
            raise errors.InvalidArgument('End must be greater than start.')

        # because Python is 0 indexed
        # Spec says that passing in (1, 25) should include 25 entries (1 - 25)
        # Python indices 0 - 24
        # Python [#:##] stops before the last index, but does not include it
        self._limit_result_set_start = start - 1
        self._limit_result_set_end = end

    @property
    def start(self):
        return self._limit_result_set_start

    @property
    def end(self):
        return self._limit_result_set_end"""


class OsidSearchResults:

    import_statements = [
    ]

    get_result_size = """
        return self._results.count(True)"""


class OsidTemporalQuery:
    import_statements = [

    ]

    match_date = """
        if match:
            if to < from_:
                raise errors.InvalidArgument('end date must be >= start date when match = True')
            self._query_terms['startDate'] = {
                '$gte': from_
            }
            self._query_terms['endDate'] = {
                '$lte': to
            }
        else:
            raise errors.InvalidArgument('match = False not currently supported')"""

    match_start_date = """
        if match:
            if end < start:
                raise errors.InvalidArgument('end date must be >= start date when match = True')
            self._query_terms['startDate'] = {
                '$gte': start,
                '$lte': end
            }
        else:
            raise errors.InvalidArgument('match = False not currently supported')"""

    match_end_date = """
        if match:
            if end < start:
                raise errors.InvalidArgument('end date must be >= start date when match = True')
            self._query_terms['endDate'] = {
                '$gte': start,
                '$lte': end
            }
        else:
            raise errors.InvalidArgument('match = False not currently supported')"""
