
class HierarchyTraversalSession:

    import_statements = [
        'from ..primitives import *',
        'from ..osid.sessions import OsidSession',
        'from ..osid.objects import OsidNode',
        'from ..id.objects import IdList',
        'FEDERATED = 0',
        'ISOLATED = 1',
    ]

    init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        from .objects import Hierarchy
        self._catalog_class = Hierarchy
        from ..osid.sessions import OsidSession
        self._session_name = 'HierarchyTraversalSession'
        self._catalog_name = 'Hierarchy'
        if 'relationship_type' in kwargs:
            self._relationship_type = kwargs['relationship_type']
        if catalog_id.get_identifier_namespace() == 'CATALOG':
            self._set_relationship_type(type_identifier=catalog_id.get_identifier().lower() + '.parent.child',
                                        display_name = catalog_id.get_identifier() + ' Hierarchy')
            namespace = catalog_id.get_authority().lower() + '.' + catalog_id.get_identifier().title()
            self._phantom_root_id = Id(authority = self._authority,
                                       namespace = namespace,
                                       identifier = '000000000000000000000000')
            try:
                catalog_id = self._get_catalog_hierarchy_id(catalog_id, proxy, runtime)
            except NotFound:
                catalog_id = self._create_catalog_hierarchy(catalog_id, proxy, runtime)
        OsidSession._init_object(self, catalog_id, proxy, runtime, db_name='hierarchy', cat_name='Hierarchy', cat_class=Hierarchy)
        self._object_view = COMPARATIVE
        self._catalog_view = ISOLATED
        self._kwargs = kwargs
        rm = self._get_provider_manager('RELATIONSHIP')
        self._rls = rm.get_relationship_lookup_session_for_family(catalog_id)

    def _get_catalog_hierarchy_id(self, catalog_id, proxy, runtime):
        seed_str = catalog_id.get_identifier() + catalog_id.get_authority() + '000000000000'
        ident = Id(authority = self._authority,
                   namespace = 'hierarchy.Hierarchy',
                   identifier = str(ObjectId(seed_str[:12])))
        return HierarchyLookupSession(proxy, runtime).get_hierarchy(ident).get_id() # Return the actual Id

    def _create_catalog_hierarchy(self, catalog_id, proxy, runtime):
        seed_str = catalog_id.get_identifier() + catalog_id.get_authority() + '000000000000'
        has = HierarchyAdminSession(proxy, runtime)
        hfc = has.get_hierarchy_form_for_create([])
        hfc.set_display_name(catalog_id.get_identifier().title() + ' Hierarchy')
        hfc.set_description('Hierarchy for ' + catalog_id.get_authority().title() + ' ' + catalog_id.get_identifier().title())
        hfc.set_genus_type(Type(authority = 'dlkit',
                                namespace = 'hierarchy.Hierarchy',
                                identifier = catalog_id.get_identifier().lower()))
        # This next tricks require serious inside knowledge:
        hfc._my_map['_id'] = ObjectId(seed_str[:12])
        hierarchy = has.create_hierarchy(hfc)
        return hierarchy.get_id() # Return the Id of newly created catalog hierarchy

    def _set_relationship_type(self, type_identifier, display_name=None, display_label=None, description=None, domain='Relationship'):
        if display_name is None:
            display_name = type_identifier
        if display_label is None:
            display_label = display_name
        if description is None:
            description = 'Relationship Type for ' + display_name
        self._relationship_type = Type(authority='dlkit',
                                       namespace='relationship.Relationship',
                                       identifier=type_identifier,
                                       display_name=display_name,
                                       display_label=display_label,
                                       description=description,
                                       domain=domain)
"""

    can_access_hierarchy = """
        # NOTE: It is expected that real authentication hints will be 
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    get_roots = """
        id_list = []
        for r in self._rls.get_relationships_by_genus_type_for_source(self._phantom_root_id, self._relationship_type):
            id_list.append(r.get_destination_id())
        return IdList(id_list)"""

    has_parents = """
        if self.get_parents(id_).available() == 0:
            return False
        return True"""

    is_parent = """
        return self._rls.get_relationships_by_genus_type_for_peers(parent_id, id_, self._relationship_type).available()"""

    get_parents = """
        if id_ is None:
            raise NullArgument()
        id_list = []
        for r in self._rls.get_relationships_by_genus_type_for_destination(id_, self._relationship_type):
            ident = r.get_source_id()
            if ident != self._phantom_root_id:
                id_list.append(ident)
        return IdList(id_list)"""

    is_ancestor = """
        raise Unimplemented()"""

    has_children = """
        if self.get_children(id_).available() == 0:
                return False
        return True"""

    is_child = """
        return self._rls.get_relationships_by_genus_type_for_peers(id_, child_id, self._relationship_type).available()"""

    get_children = """
        if id_ is None:
            raise NullArgument()
        id_list = []
        for r in self._rls.get_relationships_by_genus_type_for_source(id_, self._relationship_type):
            id_list.append(r.get_destination_id())
        return IdList(id_list)"""

    is_descendent = """
        raise Unimplemented()"""

    get_nodes = """
        if ancestor_levels is None:
            ancestor_levels = 10
        if descendant_levels is None:
            descendant_levels = 10
        include_siblings = bool(include_siblings)
        parent_node_list = []
        child_node_list = []
        if ancestor_levels != 0:
            pass # We'll figure this out later
        if descendant_levels != 0:
            for child_id in self.get_children(id_):
                child_node_list.append(self.get_nodes(child_id, 0, descendant_levels-1))
        return OsidNode({'type': 'OsidNode',
                         'id': str(id_),
                         'childNodes': child_node_list,
                         'parentNodes': parent_node_list,
                         'root': not self.has_parents(id_),
                         'leaf': not self.has_children(id_),
                         'sequestered': False})
"""

class HierarchyDesignSession:

    import_statements = [
        'from ..primitives import *',
        'from ..osid.sessions import OsidSession',
        'from ..id.objects import IdList'
    ]

    init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        from .objects import Hierarchy
        self._catalog_class = Hierarchy
        from ..osid.sessions import OsidSession
        self._session_name = 'HierarchyTraversalSession'
        self._catalog_name = 'Hierarchy'
        if catalog_id.get_identifier_namespace() == 'CATALOG':
            self._set_relationship_type(type_identifier=catalog_id.get_identifier().lower() + '.parent.child',
                                        display_name = catalog_id.get_identifier() + ' Hierarchy')
            namespace = catalog_id.get_authority().lower() + '.' + catalog_id.get_identifier().title()
            self._phantom_root_id = Id(authority = self._authority,
                                       namespace = namespace,
                                       identifier = '000000000000000000000000')
            try:
                catalog_id = self._get_catalog_hierarchy_id(catalog_id, proxy, runtime)
            except NotFound:
                catalog_id = self._create_catalog_hierarchy(catalog_id, proxy, runtime)
        OsidSession._init_object(self, catalog_id, proxy, runtime, db_name='hierarchy', cat_name='Hierarchy', cat_class=Hierarchy)
        self._kwargs = kwargs
        rm = self._get_provider_manager('RELATIONSHIP')
        self._rls = rm.get_relationship_lookup_session_for_family(catalog_id)
        self._ras = rm.get_relationship_admin_session_for_family(catalog_id)
        self._hts = HierarchyTraversalSession(self.get_hierarchy_id(), self._proxy, self._runtime, relationship_type=self._relationship_type)

    def _get_catalog_hierarchy_id(self, catalog_id, proxy, runtime):
        seed_str = catalog_id.get_identifier() + catalog_id.get_authority() + '000000000000'
        ident = Id(authority = self._authority,
                   namespace = 'hierarchy.Hierarchy',
                   identifier = str(ObjectId(seed_str[:12])))
        return HierarchyLookupSession(proxy, runtime).get_hierarchy(ident).get_id() # Return the actual Id

    def _create_catalog_hierarchy(self, catalog_id, proxy, runtime):
        seed_str = catalog_id.get_identifier() + catalog_id.get_authority() + '000000000000'
        has = HierarchyAdminSession(proxy, runtime)
        hfc = has.get_hierarchy_form_for_create([])
        hfc.set_display_name(catalog_id.get_authority() + ' ' + catalog_id.get_identifier() + ' Hierarchy')
        hfc.set_description('Catalog hierarchy for ' + catalog_id.get_authority() + ' ' + catalog_id.get_identifier())
        hfc.set_genus_type(Type(authority = 'dlkit',
                                namespace = 'hierarchy.Hierarchy',
                                identifier = catalog_id.get_identifier()))
        # This next tricks require serious inside knowledge:
        hfc._my_map['_id'] = ObjectId(seed_str[:12])
        hierarchy = has.create_hierarchy(hfc)
        return hierarchy.get_id() # Return the Id of newly created catalog hierarchy

    def _set_relationship_type(self, type_identifier, display_name=None, display_label=None, description=None, domain='Relationship'):
        if display_name is None:
            display_name = type_identifier
        if display_label is None:
            display_label = display_name
        if description is None:
            description = 'Relationship Type for ' + display_name
        self._relationship_type = Type(authority='dlkit',
                                       namespace='relationship.Relationship',
                                       identifier=type_identifier,
                                       display_name=display_name,
                                       display_label=display_label,
                                       description=description,
                                       domain=domain)
"""

    can_modify_hierarchy = """
        # NOTE: It is expected that real authentication hints will be 
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    add_root = """
        if id_ is None:
            raise NullArgument()
        if (bool(self._rls.get_relationships_by_genus_type_for_source(id_, self._relationship_type).available()) or
            bool(self._rls.get_relationships_by_genus_type_for_destination(id_, self._relationship_type).available())):
            raise AlreadyExists()
        self._assign_as_root(id_)"""

    add_child = """
        if id_ is None or child_id is None:
            raise NullArgument()
        if bool(self._rls.get_relationships_by_genus_type_for_peers(id_, child_id, self._relationship_type).available()):
            raise AlreadyExists()
        rfc = self._ras.get_relationship_form_for_create(id_, child_id, [])
        rfc.set_display_name(str(id_) + ' to ' + str(child_id) + ' Parent-Child Relationship')
        rfc.set_description(self._relationship_type.get_display_name().get_text() + ' relationship for parent: ' + str(id_) + ' and child: ' + str(child_id))
        rfc.set_genus_type(self._relationship_type)
        self._ras.create_relationship(rfc)"""

    remove_root = """
        if id_ is None:
            raise NullArgument()
        result = self._rls.get_relationships_by_genus_type_for_peers(self._phantom_root_id, id_, self._relationship_type)
        if not bool(result.available()):
            raise NotFound()
        self._ras.delete_relationship(result.get_next_relationship().get_id())
        self._adopt_orphans(id_)"""

    remove_child = """
        if id_ is None or child_id is None:
            raise NullArgument()
        result = self._rls.get_relationships_by_genus_type_for_peers(id_, child_id, self._relationship_type)
        if not bool(result.available()):
            raise NotFound()
        self._ras.delete_relationship(result.get_next_relationship().get_id())"""

    remove_children = """
        if id_ is None:
            raise NullArgument()
        results = self._rls.get_relationships_by_genus_type_for_source(id_, self._relationship_type)
        if results.available() == 0:
            raise NotFound()
        for r in results:
            self._ras.delete_relationship(r.get_id())
        """

    additional_methods = """
    def _adopt_orphans(self, negligent_parent_id):
        for child_id in self._hts.get_children(negligent_parent_id):
            self.remove_child(negligent_parent_id, child_id)
            if not self._hts.has_parents(child_id):
                self._assign_as_root(child_id)

    def _assign_as_root(self, id_):
        rfc = self._ras.get_relationship_form_for_create(self._phantom_root_id, id_, [])
        rfc.set_display_name('Implicit Root to ' + str(id_) + ' Parent-Child Relationship')
        rfc.set_description(self._relationship_type.get_display_name().get_text() + ' relationship for implicit root and child: ' + str(id_))
        rfc.set_genus_type(self._relationship_type)
        self._ras.create_relationship(rfc)        
"""

class HierarchyAdminSession:

    delete_hierarchy = """
        from ...abstract_osid.id.primitives import Id as ABCId
        collection = mongo_client[self._db_prefix + 'hierarchy']['Hierarchy']
        UPDATED = True
        if hierarchy_id is None:
            raise NullArgument()
        if not isinstance(hierarchy_id, ABCId):
            return InvalidArgument('the argument is not a valid OSID Id')

        # Should we delete the underlying Relationship Family here???

        result = collection.remove({'_id': ObjectId(hierarchy_id.get_identifier())})
                                   # Tried using justOne above but pymongo doesn't support it
        if 'err' in result and result['err'] is not None:
            raise OperationFailed()
        if result['n'] == 0:
            raise NotFound()
        mongo_client.close()"""
