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

    def _update_module_imports(self, modules, interface):
        imports = modules[self.package['name']]['imports']

        self.append(imports, self._abc_package_imports(interface))
        self._append_inherited_imports(imports, interface)

        # Don't forget the OsidSession inheritance:
        if (('OsidManager' in interface['inherit_shortnames'] or
                interface['shortname'] == self.patterns['package_catalog_caps']) and
                self.package['name'] != 'osid'):
            self.append(imports, 'from . import osid')

        # And don't forget the osid_error import:
        import_str = 'from .osid_errors import Unimplemented, IllegalState'
        self.append(imports, import_str)

        self._append_templated_imports(imports, interface)

        # get inherited imports for services
        new_imports = []
        if 'OsidManager' in interface['inherit_shortnames']:
            new_methods, new_imports = self._grab_service_methods(self._is_manager_session)
        # Add all the appropriate catalog related session methods to the catalog interface
        elif interface['shortname'] == self.patterns['package_catalog_caps']:
            new_methods, new_imports = self._grab_service_methods(self._is_catalog_session)

        for imp in new_imports:
            self.append(imports, imp)

    def _write_module_string(self, write_file, module):
        constant_declarations = """

DEFAULT = 0
COMPARATIVE = 0
PLENARY = 1
FEDERATED = 0
ISOLATED = 1
AUTOMATIC = 0
MANDATORY = 1
DISABLED = -1"""
        write_file.write('{0}{1}\n\n\n{2}'.format('\n'.join(self._order_module_imports(module['imports'])),
                                                  constant_declarations,
                                                  module['body']).encode('utf-8'))

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

    def class_doc(self, interface):
        return ('{0}\"\"\"{1} convenience adapter ' +
                'including related Session methods."\"\"').format(self._ind,
                                                                  interface['shortname'])

    def make(self):
        self.make_osids()

    def module_body(self, interface):
        additional_methods = self._additional_methods(interface)
        inheritance = self._get_class_inheritance(interface)
        init_methods = self._make_init_methods(interface)
        methods = self.make_methods(interface, self.patterns)

        # Add all the appropriate manager related session methods to the manager interface
        # Add all the appropriate catalog related session methods to the catalog interface
        if 'OsidManager' in interface['inherit_shortnames']:
            new_methods, new_imports = self._grab_service_methods(self._is_manager_session)
            methods += new_methods
        # Add all the appropriate catalog related session methods to the catalog interface
        elif interface['shortname'] == self.patterns['package_catalog_caps']:
            new_methods, new_imports = self._grab_service_methods(self._is_catalog_session)
            methods += new_methods

        if not init_methods.strip() and not methods.strip():
            init_methods = '{0}pass'.format(self._ind)

        if additional_methods:
            methods += '\n' + additional_methods

        body = '{0}\n{1}\n{2}\n{3}\n\n\n'.format(self.class_sig(interface, inheritance),
                                                 self._wrap(self.class_doc(interface)),
                                                 self._wrap(init_methods),
                                                 methods)
        return body

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

    def update_module_body(self, modules, interface):
        modules[self.package['name']]['body'] += self.module_body(interface)

    def write_modules(self, modules):
        # Finally, iterate through the completed package module structure and
        # write out both the import statements and class definitions to the
        # appropriate module for this package.
        for module in modules:
            if module == 'records' and self.package['name'] != 'osid':
                module_name = 'record_templates'
            else:
                module_name = module

            if modules[module]['body'].strip() != '':
                with open('{0}/{1}.py'.format(self._app_name(),
                                              self.package['name']), 'w') as write_file:
                    self._write_module_string(write_file,
                                              modules[module])