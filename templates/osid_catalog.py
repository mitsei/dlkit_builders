class GenericCatalogNode(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from ..utilities import get_provider_manager',
                'from dlkit.primordium.id.primitives import Id',
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    ${pattern_name}
    def __init__(self, node_map, runtime=None, proxy=None, lookup_session=None):
        osid_objects.OsidNode.__init__(self, node_map)
        self._lookup_session = lookup_session
        self._runtime = runtime
        self._proxy = proxy

    def get_object_node_map(self):
        node_map = dict(self.get_${object_name_under}().get_object_map())
        node_map['type'] = '${object_name}Node'
        node_map['parentNodes'] = []
        node_map['childNodes'] = []
        for ${object_name_under}_node in self.get_parent_${object_name_under}_nodes():
            node_map['parentNodes'].append(${object_name_under}_node.get_object_node_map())
        for ${object_name_under}_node in self.get_child_${object_name_under}_nodes():
            node_map['childNodes'].append(${object_name_under}_node.get_object_node_map())
        return node_map"""
        }
    }

    get_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if self._lookup_session is None:
            mgr = get_provider_manager('${package_name_upper}', runtime=self._runtime, proxy=self._proxy)
            self._lookup_session = mgr.get_${object_name_under}_lookup_session(proxy=getattr(self, "_proxy", None))
        return self._lookup_session.get_${object_name_under}(Id(self._my_map['id']))"""
        }
    }

    get_parent_catalog_nodes_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        parent_${object_name_under}_nodes = []
        for node in self._my_map['parentNodes']:
            parent_${object_name_under}_nodes.append(${object_name}Node(
                node._my_map,
                runtime=self._runtime,
                proxy=self._proxy,
                lookup_session=self._lookup_session))
        return ${return_type}(parent_${object_name_under}_nodes)"""
        }
    }

    get_child_catalog_nodes_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        parent_${object_name_under}_nodes = []
        for node in self._my_map['childNodes']:
            parent_${object_name_under}_nodes.append(${object_name}Node(
                node._my_map,
                runtime=self._runtime,
                proxy=self._proxy,
                lookup_session=self._lookup_session))
        return ${return_type}(parent_${object_name_under}_nodes)"""
        }
    }


class GenericCatalog(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'import importlib',
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    ${pattern_name}
    _namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, **kwargs):
        osid_objects.OsidCatalog.__init__(self, object_name='${object_name_upper}', **kwargs)""",
        'services': """
    ${pattern_name}
    # WILL THIS EVER BE CALLED DIRECTLY - OUTSIDE OF A MANAGER?
    def __init__(self, provider_manager, catalog, runtime, proxy, **kwargs):
        self._provider_manager = provider_manager
        self._catalog = catalog
        self._runtime = runtime
        osid.OsidObject.__init__(self, self._catalog)  # This is to initialize self._object
        osid.OsidSession.__init__(self, proxy)  # This is to initialize self._proxy
        self._catalog_id = catalog.get_id()
        self._provider_sessions = kwargs
        self._session_management = AUTOMATIC
        self._${cat_name_under}_view = DEFAULT
        self._object_views = dict()
        self._operable_views = dict()
        self._containable_views = dict()

    def _set_${cat_name_under}_view(self, session):
        \"\"\"Sets the underlying ${cat_name_under} view to match current view\"\"\"
        if self._${cat_name_under}_view == FEDERATED:
            try:
                session.use_federated_${cat_name_under}_view()
            except AttributeError:
                pass
        else:
            try:
                session.use_isolated_${cat_name_under}_view()
            except AttributeError:
                pass

    def _set_object_view(self, session):
        \"\"\"Sets the underlying object views to match current view\"\"\"
        for obj_name in self._object_views:
            if self._object_views[obj_name] == PLENARY:
                try:
                    getattr(session, 'use_plenary_' + obj_name + '_view')()
                except AttributeError:
                    pass
            else:
                try:
                    getattr(session, 'use_comparative_' + obj_name + '_view')()
                except AttributeError:
                    pass

    def _set_operable_view(self, session):
        \"\"\"Sets the underlying operable views to match current view\"\"\"
        for obj_name in self._operable_views:
            if self._operable_views[obj_name] == ACTIVE:
                try:
                    getattr(session, 'use_active_' + obj_name + '_view')()
                except AttributeError:
                    pass
            else:
                try:
                    getattr(session, 'use_any_status_' + obj_name + '_view')()
                except AttributeError:
                    pass

    def _set_containable_view(self, session):
        \"\"\"Sets the underlying containable views to match current view\"\"\"
        for obj_name in self._containable_views:
            if self._containable_views[obj_name] == SEQUESTERED:
                try:
                    getattr(session, 'use_sequestered_' + obj_name + '_view')()
                except AttributeError:
                    pass
            else:
                try:
                    getattr(session, 'use_unsequestered_' + obj_name + '_view')()
                except AttributeError:
                    pass

    def _get_provider_session(self, session_name):
        \"\"\"Returns the requested provider session.

        Instantiates a new one if the named session is not already known.

        "\"\"
        agent_key = self._get_agent_key()
        if session_name in self._provider_sessions[agent_key]:
            return self._provider_sessions[agent_key][session_name]
        else:
            session_class = getattr(self._provider_manager, 'get_' + session_name + '_for_${cat_name_under}')
            if self._proxy is None:
                if 'notification_session' in session_name:
                    # Is there something else we should do about the receiver field?
                    session = session_class('fake receiver', self._catalog.get_id())
                else:
                    session = session_class(self._catalog.get_id())
            else:
                if 'notification_session' in session_name:
                    # Is there something else we should do about the receiver field?
                    session = session_class('fake receiver', self._catalog.get_id(), self._proxy)
                else:
                    session = session_class(self._catalog.get_id(), self._proxy)
            self._set_${cat_name_under}_view(session)
            self._set_object_view(session)
            self._set_operable_view(session)
            self._set_containable_view(session)
            if self._session_management != DISABLED:
                self._provider_sessions[agent_key][session_name] = session
            return session

    def get_${cat_name_under}_id(self):
        \"\"\"Gets the Id of this ${cat_name_under}."\"\"
        return self._catalog_id

    def get_${cat_name_under}(self):
        \"\"\"Strange little method to assure conformance for inherited Sessions."\"\"
        return self

    def __getattr__(self, name):
        if '_catalog' in self.__dict__:
            try:
                return self._catalog[name]
            except AttributeError:
                pass
        raise AttributeError

    def close_sessions(self):
        \"\"\"Close all sessions currently being managed by this Manager to save memory."\"\"
        if self._session_management != MANDATORY:
            self._provider_sessions = dict()
        else:
            raise IllegalState()

    def use_automatic_session_management(self):
        \"\"\"Session state will be saved until closed by consumers."\"\"
        self._session_management = AUTOMATIC

    def use_mandatory_session_management(self):
        \"\"\"Session state will always be saved and can not be closed by consumers."\"\"
        # Session state will be saved and can not be closed by consumers
        self._session_management = MANDATORY

    def disable_session_management(self):
        \"\"\"Session state will never be saved."\"\"
        self._session_management = DISABLED
        self.close_sessions()"""
        }
    }
