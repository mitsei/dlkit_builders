from build_controller import BaseBuilder
from interface_builders import InterfaceBuilder


class KitBuilder(InterfaceBuilder, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(KitBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir + '/services'
        self._template_dir = self._abs_path + '/builders/kitosid_templates'

        self._class = 'services'

        # self.interface_builder = InterfaceBuilder('services',
        #                                           self._root_dir,
        #                                           self._template_dir)

    def _empty_modules_dict(self):
        module = dict(manager=dict(imports=[], body=''),  # for kitosids only
                      catalog=dict(imports=[], body=''),  # for kitosids only
                      properties=dict(imports=[], body=''),
                      objects=dict(imports=[], body=''),
                      queries=dict(imports=[], body=''),
                      query_inspectors=dict(imports=[], body=''),
                      searches=dict(imports=[], body=''),
                      search_orders=dict(imports=[], body=''),
                      rules=dict(imports=[], body=''),
                      metadata=dict(imports=[], body=''),
                      receivers=dict(imports=[], body=''),
                      sessions=dict(imports=[], body=''),
                      managers=dict(imports=[], body=''),
                      records=dict(imports=[], body=''),
                      primitives=dict(imports=[], body=''),
                      markers=dict(imports=[], body=''),
                      others_please_move=dict(imports=[], body=''))
        module[self.package['name']] = dict(imports=[], body='')
        return module

    def _patterns(self):
        patterns = self._load_patterns_file()
        for inf in self.package['interfaces']:
            patterns[self._is_session(inf, 'manager')] = self._is_manager_session(inf,
                                                                                  patterns,
                                                                                  self.package['name'])
            patterns[self._is_session(inf, 'catalog')] = self._is_catalog_session(inf,
                                                                                  patterns,
                                                                                  self.package['name'])
        return patterns

    def build_this_interface(self, interface):
        # only build managers and catalogs
        basic_build = self._build_this_interface(interface)
        managers = ['managers', 'markers']
        catalogs = ['OsidSession', 'OsidObject', 'OsidCatalog', 'OsidList']
        catalogs += [self.patterns['package_catalog_caps']]
        catalogs += [self.patterns['package_catalog_caps'] + 'List']
        is_manager_or_cat = (interface['category'] in managers or
                             interface['shortname'] in catalogs)
        return basic_build and is_manager_or_cat

    def make(self):
        self.make_osids()

    def module_header(self, module):
        return ('\"\"\"DLKit Services implementations of ' + self.package['name'] + ' service.\"\"\"\n' +
                '# pylint: disable=no-init\n' +
                '#     osid specification includes some \'marker\' interfaces.\n' +
                '# pylint: disable=too-many-ancestors\n' +
                '#     number of ancestors defined in spec.\n' +
                '# pylint: disable=too-few-public-methods,too-many-public-methods\n' +
                '#     number of methods defined in spec. Worse yet, these are aggregates.\n' +
                '# pylint: disable=invalid-name\n' +
                '#     method and class names defined in spec.\n' +
                '# pylint: disable=no-self-use,unused-argument\n' +
                '#     to catch unimplemented methods.\n' +
                '# pylint: disable=super-init-not-called\n' +
                '#     it just isn\'t.\n')
