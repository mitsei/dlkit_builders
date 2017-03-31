# type templates for kit_osid


class TypeProfile:

    supports_visible_federation = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceProfile.supports_visible_federation
        return self._provider_manager.supports_visible_federation()"""

    supports_resource_lookup = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceProfile.supports_resource_lookup
        return self._provider_manager.supports_resource_lookup()"""


class TypeManager:

    init = """

    def __init__(self):
        import settings
        import importlib
        provider_module = importlib.import_module(settings.TYPE_PROVIDER_MANAGER_PATH, settings.ANCHOR_PATH)
        provider_manager_class = getattr(provider_module, 'TypeManager')
        self._provider_manager = provider_manager_class()
        self._provider_sessions = dict()

    def _get_provider_session(self, session):
        if session in self._provider_sessions:
            return self._provider_sessions[session]
        else:
            try:
                get_session = getattr(self._provider_manager, 'get_' + session)
            except:
                raise # Unimplemented???
            else:
                self._provider_sessions[session] = get_session()
            return self._provider_sessions[session]

"""

    get_type_lookup_session = """
        # Implemented from  -
        # osid.resource.ResourceManager.get_type_lookup_session
        self._provider_sessions[\'TypeLookupSession\'] = self._provider_manager.get_type_lookup_session()
        return self"""

    get_type_admin_session = """
        # Implemented from  -
        # osid.resource.ResourceManager.get_type_admin_session
        self._provider_sessions[\'TypeAdminSession\'] = self._provider_manager.get_type_admin_session()
        return self"""


class TypeProxyManager:
    pass


class TypeLookupSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session
"""

    can_lookup_types = """
        # Implemented from
        # osid.type.TypeLookupSession.can_lookup_types
        return self._get_provider_session('type_lookup_session').can_lookup_types()"""

    get_type = """
        # Implemented from
        # osid.type.TypeLookupSession.get_type
        return self._get_provider_session('type_lookup_session').get_type(namespace, identifier, authority)"""

    has_type = """
        # Implemented from
        # osid.type.TypeLookupSession.has_type
        return self._get_provider_session('type_lookup_session').has_type(type_)"""

    get_types_by_domain = """
        # Implemented from
        # osid.type.TypeLookupSession.get_types_by_domain
        return self._get_provider_session('type_lookup_session').get_types_by_domain(domain)"""

    get_types_by_authority = """
        # Implemented from
        # osid.type.TypeLookupSession.get_types_by_authority
        return self._get_provider_session('type_lookup_session').get_types_by_authority(authority)"""

    get_types_by_domain_and_authority = """
        # Implemented from
        # osid.type.TypeLookupSession.get_types_by_domain_and_authority
        return self._get_provider_session('type_lookup_session').get_types_by_domain_and_authority(domain, authority)"""

    get_types = """
        # Implemented from
        # osid.type.TypeLookupSession.get_types
        return self._get_provider_session('type_lookup_session').get_types()"""

    is_equivalent = """
        # Implemented from
        # osid.type.TypeLookupSession.is_equivalent
        return self._get_provider_session('type_lookup_session').is_equivalent(type_, equivalent_type)"""

    implies_support = """
        # Implemented from
        # osid.type.TypeLookupSession.implies_support
        return self._get_provider_session('type_lookup_session').implies_support(type_, base_type)"""

    has_base_type = """
        # Implemented from
        # osid.type.TypeLookupSession.has_base_type
        return self._get_provider_session('type_lookup_session').has_base_type(type_)"""

    get_base_types = """
        # Implemented from
        # osid.type.TypeLookupSession.get_base_types
        return self._get_provider_session('type_lookup_session').get_base_types(type_)"""

    get_relation_types = """
        # Implemented from
        # osid.type.TypeLookupSession.get_relation_types
        return self._get_provider_session('type_lookup_session').get_relation_types()"""

    get_source_types_by_relation_type = """
        # Implemented from
        # osid.type.TypeLookupSession.get_source_types_by_relation_type
        return self._get_provider_session('type_lookup_session').get_source_types_by_relation_type(relation_type)"""

    get_relation_types_by_source = """
        # Implemented from
        # osid.type.TypeLookupSession.get_relation_types_by_source
        return self._get_provider_session('type_lookup_session').get_relation_types_by_source(source_type)"""

    get_destination_types_by_source_and_relation_type = """
        # Implemented from
        # osid.type.TypeLookupSession.get_destination_types_by_source_and_relation_type
        return self._get_provider_session('type_lookup_session').get_destination_types_by_source_and_relation_type(source_type, relation_type)"""

    get_destination_types_by_relation_type = """
        # Implemented from
        # osid.type.TypeLookupSession.get_destination_types_by_relation_type
        return self._get_provider_session('type_lookup_session').get_destination_types_by_relation_type(relation_type)"""

    get_source_types_by_destination = """
        # Implemented from
        # osid.type.TypeLookupSession.get_destination_types_by_destination
        return self._get_provider_session('type_lookup_session').get_destination_types_by_destination(destination_type)"""

    get_destination_types_by_destination_and_relation_type = """
        # Implemented from
        # osid.type.TypeLookupSession.get_destination_types_by_destination_and_relation_type
        return self._get_provider_session('type_lookup_session').get_destination_types_by_destination_and_relation_type(destination_type, relation_type)"""


class TypeAdminSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session
"""

    can_create_types = """
        # Implemented from
        # osid.type.TypeAdminSession.can_create_types
        return self._get_provider_session('type_admin_session').can_create_types()"""

    get_type_form_for_create = """
        # Implemented from
        # osid.type.TypeAdminSession.get_type_form_for_create
        return self._get_provider_session('type_admin_session').get_type_form_for_create()"""

    create_type = """
        # Implemented from
        # osid.type.TypeAdminSession.create_type
        return self._get_provider_session('type_admin_session').create_type(authority, identifier_ns, identifier, type_form)"""

    can_update_types = """
        # Implemented from
        # osid.type.TypeAdminSession.can_update_types
        return self._get_provider_session('type_admin_session').can_update_types()"""

    can_update_type = """
        # Implemented from
        # osid.type.TypeAdminSession.can_update_type
        return self._get_provider_session('type_admin_session').can_update_type(type_)"""

    get_type_form_for_update = """
        # Implemented from
        # osid.type.TypeAdminSession.get_type_form_for_update
        return self._get_provider_session('type_admin_session').get_type_form_for_update(type_)"""

    update_type = """
        # Implemented from
        # osid.type.TypeAdminSession.update_type
        return self._get_provider_session('type_admin_session').update_type(type, type_form)"""

    can_delete_types = """
        # Implemented from
        # osid.type.TypeAdminSession.can_delete_types
        return self._get_provider_session('type_admin_session').can_delete_types()"""

    can_delete_type = """
        # Implemented from
        # osid.type.TypeAdminSession.can_delete_type
        return self._get_provider_session('type_admin_session').can_delete_type(type_)"""

    delete_type = """
        # Implemented from
        # osid.type.TypeAdminSession.delete_type
        self._get_provider_session('type_admin_session').delete_type(type_)"""

    make_equivalent = """
        # Implemented from
        # osid.type.TypeAdminSession.make_equivalent
        self._get_provider_session('type_admin_session').make_equivalent(primary_type, equivalent_type)"""

    add_base_type = """
        # Implemented from
        # osid.type.TypeAdminSession.add_base_type
        self._get_provider_session('type_admin_session').add_base_type(type_, base_type)"""

    remove_base_type = """
        # Implemented from
        # osid.type.TypeAdminSession.remove_base_type
        self._get_provider_session('type_admin_session').remove_base_type(type_, base_type)"""

    add_type_relation = """
        # Implemented from
        # osid.type.TypeAdminSession.add_type_relation
        self._get_provider_session('type_admin_session').add_type_relation(source_type, destination_type, relation_type)"""

    remove_type_relation = """
        # Implemented from
        # osid.type.TypeAdminSession.remove_type_relation
        self._get_provider_session('type_admin_session').remove_type_relation(source_type, destination_type, relation_type)"""
