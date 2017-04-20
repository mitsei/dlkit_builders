# type templates for kit_osid


class TypeProfile:

    supports_visible_federation = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceProfile.supports_visible_federation
        return self._provider_manager.supports_visible_federation()"""

    supports_type_lookup = """
        \"\"\"Pass through to provider method\"\"\"
        return self._provider_manager.supports_type_lookup()"""

    supports_type_admin = """
        \"\"\"Pass through to provider method\"\"\"
        return self._provider_manager.supports_type_admin()"""


class TypeManager:

    init = """

    def __init__(self, proxy=None):
        self._runtime = None
        self._provider_manager = None
        self._provider_sessions = dict()
        self._session_management = AUTOMATIC
        self._bin_view = DEFAULT
        # This is to initialize self._proxy
        osid.OsidSession.__init__(self, proxy)
        self._sub_package_provider_managers = dict()

    def _get_provider_session(self, session):
        if session in self._provider_sessions:
            return self._provider_sessions[session]
        else:
            try:
                get_session = getattr(self._provider_manager, 'get_' + session)
            except:
                raise  # Unimplemented???
            else:
                self._provider_sessions[session] = get_session()
            return self._provider_sessions[session]

    def initialize(self, runtime):
        \"\"\"OSID Manager initialize\"\"\"
        from .primitives import Id
        if self._runtime is not None:
            raise IllegalState('Manager has already been initialized')
        self._runtime = runtime
        config = runtime.get_configuration()
        parameter_id = Id('parameter:typeProviderImpl@dlkit_service')
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        # do not account for TypeProxyManager yet...not used in Handcar
        # need to add version argument
        self._provider_manager = runtime.get_manager('TYPE', provider_impl)

    def get_types(self, *args, **kwargs):
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.get_types
        return self._get_provider_session('type_lookup_session').get_types(*args, **kwargs)

    def get_type_lookup_session(self, *args, **kwargs):
        \"\"\"Pass through to provider method\"\"\"
        return self._provider_manager.get_type_lookup_session(*args, **kwargs)

    def get_type_admin_session(self, *args, **kwargs):
        \"\"\"Pass through to provider method\"\"\"
        return self._provider_manager.get_type_admin_session(*args, **kwargs)"""


class TypeProxyManager:
    pass


class TypeLookupSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session"""

    can_lookup_types = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.can_lookup_types
        return self._get_provider_session('type_lookup_session').can_lookup_types(*args, **kwargs)"""

    get_type = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.get_type
        return self._get_provider_session('type_lookup_session').get_type(*args, **kwargs)"""

    has_type = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.has_type
        return self._get_provider_session('type_lookup_session').has_type(*args, **kwargs)"""

    get_types_by_domain = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.get_types_by_domain
        return self._get_provider_session('type_lookup_session').get_types_by_domain(*args, **kwargs)"""

    get_types_by_authority = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.get_types_by_authority
        return self._get_provider_session('type_lookup_session').get_types_by_authority(*args, **kwargs)"""

    get_types_by_domain_and_authority = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.get_types_by_domain_and_authority
        return self._get_provider_session('type_lookup_session').get_types_by_domain_and_authority(*args, **kwargs)"""

    get_types = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.get_types
        return self._get_provider_session('type_lookup_session').get_types(*args, **kwargs)"""

    is_equivalent = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.is_equivalent
        return self._get_provider_session('type_lookup_session').is_equivalent(*args, **kwargs)"""

    implies_support = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.implies_support
        return self._get_provider_session('type_lookup_session').implies_support(*args, **kwargs)"""

    has_base_type = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.has_base_type
        return self._get_provider_session('type_lookup_session').has_base_type(*args, **kwargs)"""

    get_base_types = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.get_base_types
        return self._get_provider_session('type_lookup_session').get_base_types(*args, **kwargs)"""

    get_relation_types = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.get_relation_types
        return self._get_provider_session('type_lookup_session').get_relation_types(*args, **kwargs)"""

    get_source_types_by_relation_type = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.get_source_types_by_relation_type
        return self._get_provider_session('type_lookup_session').get_source_types_by_relation_type(*args, **kwargs)"""

    get_relation_types_by_source = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.get_relation_types_by_source
        return self._get_provider_session('type_lookup_session').get_relation_types_by_source(*args, **kwargs)"""

    get_destination_types_by_source_and_relation_type = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.get_destination_types_by_source_and_relation_type
        return self._get_provider_session('type_lookup_session').get_destination_types_by_source_and_relation_type(*args, **kwargs)"""

    get_destination_types_by_relation_type = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.get_destination_types_by_relation_type
        return self._get_provider_session('type_lookup_session').get_destination_types_by_relation_type(*args, **kwargs)"""

    get_source_types_by_destination = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.get_destination_types_by_destination
        return self._get_provider_session('type_lookup_session').get_destination_types_by_destination(*args, **kwargs)"""

    get_destination_types_by_destination_and_relation_type = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeLookupSession.get_destination_types_by_destination_and_relation_type
        return self._get_provider_session('type_lookup_session').get_destination_types_by_destination_and_relation_type(*args, **kwargs)"""


class TypeAdminSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session"""

    can_create_types = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeAdminSession.can_create_types
        return self._get_provider_session('type_admin_session').can_create_types(*args, **kwargs)"""

    get_type_form_for_create = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeAdminSession.get_type_form_for_create
        return self._get_provider_session('type_admin_session').get_type_form_for_create(*args, **kwargs)"""

    create_type = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeAdminSession.create_type
        return self._get_provider_session('type_admin_session').create_type(*args, **kwargs)"""

    can_update_types = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeAdminSession.can_update_types
        return self._get_provider_session('type_admin_session').can_update_types(*args, **kwargs)"""

    can_update_type = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeAdminSession.can_update_type
        return self._get_provider_session('type_admin_session').can_update_type(*args, **kwargs)"""

    get_type_form_for_update = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeAdminSession.get_type_form_for_update
        return self._get_provider_session('type_admin_session').get_type_form_for_update(*args, **kwargs)"""

    update_type = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeAdminSession.update_type
        return self._get_provider_session('type_admin_session').update_type(*args, **kwargs)"""

    can_delete_types = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeAdminSession.can_delete_types
        return self._get_provider_session('type_admin_session').can_delete_types(*args, **kwargs)"""

    can_delete_type = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeAdminSession.can_delete_type
        return self._get_provider_session('type_admin_session').can_delete_type(*args, **kwargs)"""

    delete_type = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeAdminSession.delete_type
        self._get_provider_session('type_admin_session').delete_type(*args, **kwargs)"""

    make_equivalent = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeAdminSession.make_equivalent
        self._get_provider_session('type_admin_session').make_equivalent(*args, **kwargs)"""

    add_base_type = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeAdminSession.add_base_type
        self._get_provider_session('type_admin_session').add_base_type(*args, **kwargs)"""

    remove_base_type = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeAdminSession.remove_base_type
        self._get_provider_session('type_admin_session').remove_base_type(*args, **kwargs)"""

    add_type_relation = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeAdminSession.add_type_relation
        self._get_provider_session('type_admin_session').add_type_relation(*args, **kwargs)"""

    remove_type_relation = """
        \"\"\"Pass through to provider method\"\"\"
        # Implemented from
        # osid.type.TypeAdminSession.remove_type_relation
        self._get_provider_session('type_admin_session').remove_type_relation(*args, **kwargs)"""
