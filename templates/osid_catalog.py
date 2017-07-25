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
        osid_objects.OsidCatalog.__init__(self, object_name='${object_name_upper}', **kwargs)"""
        }
    }
