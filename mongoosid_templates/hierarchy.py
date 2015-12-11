
class HierarchyTraversalSession:

    import_statements = [
        'from ..primitives import Id',
        'from ..primitives import Type',
        'from ..osid.sessions import OsidSession',
        #'from ..osid.objects import OsidNode',
        'from . import objects',
        'from ..id.objects import IdList',
    ]

    init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        from .objects import Hierarchy
        self._catalog_class = Hierarchy
        self._session_name = 'HierarchyTraversalSession'
        self._catalog_name = 'Hierarchy'
        if 'relationship_type' in kwargs:
            self._relationship_type = kwargs['relationship_type']
        if catalog_id.get_identifier_namespace() == 'CATALOG':
            self._set_relationship_type(type_identifier=catalog_id.get_identifier().lower() + '.parent.child',
                                        display_name=catalog_id.get_identifier() + ' Hierarchy')
            namespace = catalog_id.get_authority().lower() + '.' + catalog_id.get_identifier().title()
            self._phantom_root_id = Id(authority=self._authority,
                                       namespace=namespace,
                                       identifier='000000000000000000000000')
            try:
                catalog_id = self._get_catalog_hierarchy_id(catalog_id, proxy, runtime)
            except errors.NotFound:
                catalog_id = self._create_catalog_hierarchy(catalog_id, proxy, runtime)
        OsidSession._init_object(self, catalog_id, proxy, runtime, db_name='hierarchy', cat_name='Hierarchy', cat_class=Hierarchy)
        self._kwargs = kwargs
        rm = self._get_provider_manager('RELATIONSHIP')
        self._rls = rm.get_relationship_lookup_session_for_family(catalog_id)

    def _get_catalog_hierarchy_id(self, catalog_id, proxy, runtime):
        \"\"\"Gets the catalog hierarchy\"\"\"
        seed_str = str(catalog_id.get_identifier() + catalog_id.get_authority() + '000000000000')
                  #^^^ make sure its not a unicode type
        ident = Id(authority=self._authority,
                   namespace='hierarchy.Hierarchy',
                   identifier=str(ObjectId(seed_str[:12])))
        return HierarchyLookupSession(proxy, runtime).get_hierarchy(ident).get_id() # Return the actual Id

    def _create_catalog_hierarchy(self, catalog_id, proxy, runtime):
        \"\"\"Creates a catalog hierarchy\"\"\"
        seed_str = catalog_id.get_identifier() + catalog_id.get_authority() + '000000000000'
        has = HierarchyAdminSession(proxy, runtime)
        hfc = has.get_hierarchy_form_for_create([])
        hfc.set_display_name(catalog_id.get_identifier().title() + ' Hierarchy')
        hfc.set_description(
            'Hierarchy for ' + catalog_id.get_authority().title() +
            ' ' + catalog_id.get_identifier().title())
        hfc.set_genus_type(Type(authority='dlkit',
                                namespace='hierarchy.Hierarchy',
                                identifier=catalog_id.get_identifier().lower()))
        # This next tricks require serious inside knowledge:
        hfc._my_map['_id'] = ObjectId(seed_str[:12])
        hierarchy = has.create_hierarchy(hfc)
        return hierarchy.get_id() # Return the Id of newly created catalog hierarchy

    def _set_relationship_type(self, type_identifier, display_name=None, display_label=None, description=None, domain='Relationship'):
        \"\"\"Sets the relationship type\"\"\"
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
        return bool(self._rls.get_relationships_by_genus_type_for_peers(
            parent_id,
            id_,
            self._relationship_type).available())"""

    get_parents = """
        id_list = []
        for r in self._rls.get_relationships_by_genus_type_for_destination(id_, self._relationship_type):
            ident = r.get_source_id()
            if ident != self._phantom_root_id:
                id_list.append(ident)
        return IdList(id_list)"""

    is_ancestor = """
        raise errors.Unimplemented()"""

    has_children = """
        if self.get_children(id_).available() == 0:
            return False
        return True"""

    is_child = """
        return bool(self._rls.get_relationships_by_genus_type_for_peers(
            id_,
            child_id,
            self._relationship_type).available())"""

    get_children = """
        id_list = []
        for r in self._rls.get_relationships_by_genus_type_for_source(id_, self._relationship_type):
            id_list.append(r.get_destination_id())
        return IdList(id_list)"""

    is_descendent = """
        raise errors.Unimplemented()"""

    get_nodes_arg_template = {
        1: 10,  # ancestor_levels,
        2: 10,  # descendant_levels
        3: False  # include_siblings
    }

    get_nodes = """
        # This impl ignores include_siblings, assumes false
        include_siblings = bool(include_siblings)
        parent_node_list = []
        child_node_list = []
        if ancestor_levels != 0:
            for parent_id in self.get_parents(id_):
                parent_node_list.append(self.get_nodes(parent_id, ancestor_levels-1, 0))
        if descendant_levels != 0:
            for child_id in self.get_children(id_):
                child_node_list.append(self.get_nodes(child_id, 0, descendant_levels-1))
        return objects.Node({'type': 'OsidNode',
                             'id': str(id_),
                             'childNodes': child_node_list,
                             'parentNodes': parent_node_list,
                             'root': not self.has_parents(id_),
                             'leaf': not self.has_children(id_),
                             'sequestered': False})
"""

class HierarchyDesignSession:

    import_statements = [
        'from ..primitives import Id',
        'from ..primitives import Type',
        'from dlkit.abstract_osid.osid import errors',
        'from ..osid.sessions import OsidSession',
        'from ..id.objects import IdList'
    ]

    init = """
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        from .objects import Hierarchy
        self._catalog_class = Hierarchy
        self._session_name = 'HierarchyTraversalSession'
        self._catalog_name = 'Hierarchy'
        if catalog_id.get_identifier_namespace() == 'CATALOG':
            self._set_relationship_type(type_identifier=catalog_id.get_identifier().lower() + '.parent.child',
                                        display_name=catalog_id.get_identifier() + ' Hierarchy')
            namespace = catalog_id.get_authority().lower() + '.' + catalog_id.get_identifier().title()
            self._phantom_root_id = Id(authority=self._authority,
                                       namespace=namespace,
                                       identifier='000000000000000000000000')
            try:
                catalog_id = self._get_catalog_hierarchy_id(catalog_id, proxy, runtime)
            except errors.NotFound:
                catalog_id = self._create_catalog_hierarchy(catalog_id, proxy, runtime)
        OsidSession._init_object(self, catalog_id, proxy, runtime, db_name='hierarchy', cat_name='Hierarchy', cat_class=Hierarchy)
        self._kwargs = kwargs
        rm = self._get_provider_manager('RELATIONSHIP')
        self._rls = rm.get_relationship_lookup_session_for_family(catalog_id)
        self._ras = rm.get_relationship_admin_session_for_family(catalog_id)
        self._hts = HierarchyTraversalSession(self.get_hierarchy_id(), self._proxy, self._runtime, relationship_type=self._relationship_type)

    def _get_catalog_hierarchy_id(self, catalog_id, proxy, runtime):
        \"\"\"Gets the catalog hierarchy\"\"\"
        seed_str = catalog_id.get_identifier() + catalog_id.get_authority() + '000000000000'
        ident = Id(authority=self._authority,
                   namespace='hierarchy.Hierarchy',
                   identifier=str(ObjectId(seed_str[:12])))
        return HierarchyLookupSession(proxy, runtime).get_hierarchy(ident).get_id() # Return the actual Id

    def _create_catalog_hierarchy(self, catalog_id, proxy, runtime):
        \"\"\"Creates a catalog hierarchy\"\"\"
        seed_str = catalog_id.get_identifier() + catalog_id.get_authority() + '000000000000'
        has = HierarchyAdminSession(proxy, runtime)
        hfc = has.get_hierarchy_form_for_create([])
        hfc.set_display_name(catalog_id.get_authority() + ' ' + catalog_id.get_identifier() + ' Hierarchy')
        hfc.set_description('Catalog hierarchy for ' + catalog_id.get_authority() + ' ' + catalog_id.get_identifier())
        hfc.set_genus_type(Type(authority='dlkit',
                                namespace='hierarchy.Hierarchy',
                                identifier=catalog_id.get_identifier()))
        # This next tricks require serious inside knowledge:
        hfc._my_map['_id'] = ObjectId(seed_str[:12])
        hierarchy = has.create_hierarchy(hfc)
        return hierarchy.get_id() # Return the Id of newly created catalog hierarchy

    def _set_relationship_type(self, type_identifier, display_name=None, display_label=None, description=None, domain='Relationship'):
        \"\"\"Sets the relationship type\"\"\"
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
        if (bool(self._rls.get_relationships_by_genus_type_for_source(id_, self._relationship_type).available()) or
                bool(self._rls.get_relationships_by_genus_type_for_destination(id_, self._relationship_type).available())):
            raise errors.AlreadyExists()
        self._assign_as_root(id_)"""

    add_child = """
        if bool(self._rls.get_relationships_by_genus_type_for_peers(id_, child_id, self._relationship_type).available()):
            raise errors.AlreadyExists()
        rfc = self._ras.get_relationship_form_for_create(id_, child_id, [])
        rfc.set_display_name(str(id_) + ' to ' + str(child_id) + ' Parent-Child Relationship')
        rfc.set_description(self._relationship_type.get_display_name().get_text() + ' relationship for parent: ' + str(id_) + ' and child: ' + str(child_id))
        rfc.set_genus_type(self._relationship_type)
        self._ras.create_relationship(rfc)"""

    remove_root = """
        result = self._rls.get_relationships_by_genus_type_for_peers(self._phantom_root_id, id_, self._relationship_type)
        if not bool(result.available()):
            raise errors.NotFound()
        self._ras.delete_relationship(result.get_next_relationship().get_id())
        self._adopt_orphans(id_)"""

    remove_child = """
        result = self._rls.get_relationships_by_genus_type_for_peers(id_, child_id, self._relationship_type)
        if not bool(result.available()):
            raise errors.NotFound()
        self._ras.delete_relationship(result.get_next_relationship().get_id())"""

    remove_children = """
        results = self._rls.get_relationships_by_genus_type_for_source(id_, self._relationship_type)
        if results.available() == 0:
            raise errors.NotFound()
        for r in results:
            self._ras.delete_relationship(r.get_id())
        """

    additional_methods = """
    def _adopt_orphans(self, negligent_parent_id):
        \"\"\"Clean up orphaned children\"\"\"
        for child_id in self._hts.get_children(negligent_parent_id):
            self.remove_child(negligent_parent_id, child_id)
            if not self._hts.has_parents(child_id):
                self._assign_as_root(child_id)

    def _assign_as_root(self, id_):
        \"\"\"Assign an id_ a root object in the hierarchy\"\"\"
        rfc = self._ras.get_relationship_form_for_create(self._phantom_root_id, id_, [])
        rfc.set_display_name('Implicit Root to ' + str(id_) + ' Parent-Child Relationship')
        rfc.set_description(self._relationship_type.get_display_name().get_text() + ' relationship for implicit root and child: ' + str(id_))
        rfc.set_genus_type(self._relationship_type)
        self._ras.create_relationship(rfc)
"""

class HierarchyAdminSession:
    import_statements = [
        'from ..utilities import MongoClientValidated'
    ]

    delete_hierarchy_import_templates = [
        'from ...abstract_osid.id.primitives import Id as ABCId'
    ]

    delete_hierarchy = """
        collection = MongoClientValidated('hierarchy',
                                          collection='Hierarchy',
                                          runtime=self._runtime)
        if not isinstance(hierarchy_id, ABCId):
            return InvalidArgument('the argument is not a valid OSID Id')

        # Should we delete the underlying Relationship Family here???

        collection.delete_one({'_id': ObjectId(hierarchy_id.get_identifier())})"""

class Hierarchy:

    import_statements = [
        'from ..primitives import Id',
        'from dlkit.abstract_osid.osid import errors',
    ]


class HierarchyQuery:

    import_statements = [
        'from ..osid.osid_errors import Unimplemented',
    ]


class Node:
    
    get_parents = """
        return NodeList(self._my_map['parentNodes'])"""

    get_children = """
        return NodeList(self._my_map['childNodes'])"""
