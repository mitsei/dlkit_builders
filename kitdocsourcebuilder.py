from config import managers_to_implement

from binder_helpers import camel_to_list
from build_controller import BaseBuilder
from interface_builders import InterfaceBuilder


class KitSourceBuilder(InterfaceBuilder, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(KitSourceBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir + '/source'
        self._template_dir = self._abs_path + '/builders/kitosid_templates'

        self._excluded_packages = ['proxy', 'type']

        self._class = 'doc_source'

    def _empty_modules_dict(self):
        module = dict(manager=dict(imports=[], body=''),
                      services=dict(imports=[], body=''),
                      service_catalog=dict(imports=[], body=''),
                      service_managers=dict(imports=[], body=''),
                      catalog=dict(imports=[], body=''),
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
        module[self.patterns['package_catalog_under']] = dict(imports=[], body='')
        return module

    def _get_simple_module_body(self, interface):
        sn = interface['shortname']
        header = ' '.join(camel_to_list(sn))
        body = '{0}\n{1}\n\n.. autoclass:: {2}\n   :show-inheritance:\n\n'.format(header,
                                                                                  '-' * len(header),
                                                                                  sn)
        body = '{0}{1}\n\n'.format(body,
                                   self.make_methods(interface, self.patterns))

        return body

    def _grab_service_methods(self, type_check_method, catalog=None):
        self.patterns['implemented_view_methods'] = []
        methods = ''
        for inf in self.package['interfaces']:
            # Check to see if this interface is meant to be implemented.
            if self.package['name'] != 'osid' and not self._flagged_for_implementation(inf):
                continue

            if type_check_method(inf, self.patterns, self.package['name']):
                header = ' '.join(camel_to_list(inf['fullname'])[1:-1])
                full_header = '{0} Methods'.format(header)
                methods += '\n\n{0} Methods\n{1}\n\n{2}\n\n'.format(header,
                                                                    '-' * len(full_header),
                                                                    self.make_methods(inf,
                                                                                      self.patterns,
                                                                                      inf['shortname'],
                                                                                      service_catalog=catalog))

        return methods

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
        package = self.package['name']
        if any(sn in interface['inherit_shortnames']
               for sn in ['OsidManager', 'OsidProxyManager']):
            module_name = 'service_managers'
            currentmodule_str = '.. currentmodule:: dlkit.services.{0}'.format(package)
            automodule_str = '.. automodule:: dlkit.services.{0}'.format(package)

        elif interface['shortname'] == self.patterns['package_catalog_caps']:
            module_name = 'service_catalog'
            currentmodule_str = '.. currentmodule:: dlkit.services.{0}'.format(package)
            automodule_str = ''
        else:
            module_name = interface['category']
            currentmodule_str = '.. currentmodule:: dlkit.{0}.{1}'.format(package,
                                                                          module_name)
            automodule_str = '.. automodule:: dlkit.{0}.{1}'.format(package,
                                                                    module_name)

        module_title = '\n{0}\n{1}'.format(' '.join(module_name.split('_')).title(),
                                           '=' * len(module_name))

        self.append(modules[module_name]['imports'], currentmodule_str)
        self.append(modules[module_name]['imports'], automodule_str)
        self.append(modules[module_name]['imports'], module_title)

        self._module_name = module_name

    def _write_toc(self, modules):
        toc_str = '{0}\n{1}'.format(self.package['name'].title(),
                                    '=' * len(self.package['name']))

        toc_str = '{0}\n\n.. toctree::\n   :maxdepth: 2\n\n   summary\n   service_managers\n'.format(toc_str)

        for module in modules:
            if ('_'.join(module.split('.')) not in [
                    'service_managers',
                    self.patterns['package_catalog_under'],
                    'records',
                    'rules',
                    'no_catalog'] and
                    modules[module]['body'].strip() != ''):
                toc_str = '{0}   {1}\n'.format(toc_str,
                                               '_'.join(module.split('.')))

        if 'records' in modules and modules['records']['body'].strip() != '':
            toc_str = '{0}   records\n'.format(toc_str)
        if 'rules' in modules and modules['rules']['body'].strip() != '':
            toc_str = '{0}   rules\n'.format(toc_str)

        with open(self._abc_module('toc', extension='rst'), 'w') as write_file:
            write_file.write(toc_str)

    def build_this_interface(self, interface):
        return self._build_this_interface(interface)

    def make(self):
        self.make_osids()

    def make_methods(self, interface, patterns, package_name=None, service_catalog=None):
        body = []
        for method in interface['methods']:
            if package_name is None:
                class_name = interface['shortname']
            elif service_catalog is not None:
                class_name = service_catalog
            else:
                class_name = package_name
            ##
            # Here is where we check for the Python properties stuff:
            if method['name'] == 'get_id':
                automethod_str = '   .. autoattribute:: ' + class_name + '.ident'
            elif method['name'] == 'get_identifier_namespace':
                automethod_str = '   .. autoattribute:: ' + class_name + '.namespace'
            elif method['name'].startswith('get_') and method['args'] == []:
                automethod_str = '   .. autoattribute:: ' + class_name + '.' + method['name'][4:]
            elif method['name'].startswith('set_') and len(method['args']) == 1:
                automethod_str = '   .. autoattribute:: ' + class_name + '.' + method['name'][4:]
            elif method['name'].startswith('clear_') and method['args'] == []:
                automethod_str = '   .. autoattribute:: ' + class_name + '.' + method['name'][6:]
            ##
            # And finally all the methods:
            else:
                automethod_str = '   .. automethod:: ' + class_name + '.' + method['name']

            if automethod_str not in body:
                body.append(automethod_str)
        return '\n\n'.join(body)

    def module_body(self, interface):
        sn = interface['shortname']
        header = ' '.join(camel_to_list(sn))
        body = '{0}\n{1}\n\n.. autoclass:: {2}\n   :show-inheritance:\n\n'.format(header,
                                                                                  '-' * len(header),
                                                                                  sn)
        body = '{0}{1}\n\n'.format(body,
                                   self.make_methods(interface, self.patterns))
        if any(i in interface['inherit_shortnames']
               for i in ['OsidManager', 'OsidProxyManager']):
            catalog = sn
            body = '{0}{1}\n\n'.format(body,
                                       self._grab_service_methods(self._is_manager_session, catalog=catalog))
        elif any(i in interface['inherit_shortnames']
                 for i in ['OsidCatalog']):
            catalog = sn
            body = '{0}{1}\n\n'.format(body,
                                       self._grab_service_methods(self._is_catalog_session, catalog=catalog))

        return body

    def update_module_body(self, modules, interface):
        modules[self._module_name]['body'] += self.module_body(interface)
        if self._module_name in ['service_managers', 'service_catalog']:
            modules[interface['category']]['body'] += self._get_simple_module_body(interface)

    def write_license_file(self):
        with open(self._abc_module('summary', extension='rst'), 'w') as write_file:
            write_file.write(('Summary\n=======\n\n' +
                              '.. currentmodule:: dlkit.services.' +
                              self.package['name'] + '\n' +
                              '.. automodule:: dlkit.services.' +
                              self.package['name'] + '\n').encode('utf-8'))

    def write_modules(self, modules):
        # first, write the Table of Contents
        self._write_toc(modules)

        # Finally, iterate through the completed package module structure and
        # write out both the import statements and class definitions to the
        # appropriate module for this package.
        for module in modules:
            if modules[module]['body'].strip() != '':
                with open(self._abc_module('_'.join(module.split('.')),
                                           extension='rst'), 'w') as write_file:
                    write_file.write('{0}\n\n\n{1}'.format('\n'.join(modules[module]['imports']),
                                                           modules[module]['body']).encode('utf-8'))
