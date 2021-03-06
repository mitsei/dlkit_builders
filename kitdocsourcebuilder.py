import re

from config import managers_to_implement, sessions_to_implement

from binder_helpers import camel_to_list, fix_reserved_word, under_to_caps
from build_dlkit import BaseBuilder
from interface_builders import InterfaceBuilder
from method_builders import argless_get, argless_clear, one_arg_set, strip_prefixes


class KitSourceBuilder(InterfaceBuilder, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(KitSourceBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir + '/source'
        self._template_dir = self._abs_path + '/kitosid_templates'

        self._excluded_packages = ['proxy', 'type']

        self._class = 'doc_source'

    def _empty_modules_dict(self):
        module = dict(manager=dict(imports=[], body=''),
                      services=dict(imports=[], body=''),
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

    def _get_method_args(self, method, interface):
        args = []
        if self.extra_templates_exists(method, interface, '_arg_template'):
            arg_context = self._get_method_context(method, interface)
            arg_default_map = self.get_arg_default_map(arg_context,
                                                       method,
                                                       interface)
        else:
            arg_default_map = {}

        for arg in method['args']:
            if arg['var_name'] in arg_default_map:
                args.append(arg['var_name'] + '=' + arg_default_map[arg['var_name']])
            else:
                args.append(arg['var_name'])
        return args

    def _get_simple_module_body(self, interface):
        inheritance = self._get_class_inheritance(interface)
        sn = interface['shortname']
        header = ' '.join(camel_to_list(sn))
        body = '{0}\n{1}\n\n.. py:class:: {2}{3}\n{4}:noindex:\n\n'.format(header,
                                                                           '-' * len(header),
                                                                           sn,
                                                                           inheritance,
                                                                           self._dind)

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

            if type_check_method(inf, self.package['name'], patterns=self.patterns):
                header = ' '.join(camel_to_list(inf['fullname'])[1:-1])
                full_header = '{0} Methods'.format(header)
                methods += '\n\n{0} Methods\n{1}\n\n{2}\n\n'.format(header,
                                                                    '-' * len(full_header),
                                                                    self.make_methods(inf,
                                                                                      inf['shortname'],
                                                                                      service_catalog=catalog))

        return methods

    # Determine if the interface represents a catalog related session
    def _is_catalog_session(self, interface, package_name, patterns=None):
        if patterns is None:
            patterns = self.patterns
        is_catalog_session = False
        if (interface['category'] == 'sessions' and
                not interface['shortname'].startswith(patterns['package_catalog_caps']) and
                package_name not in ['type']):
            is_catalog_session = True
        return is_catalog_session

    # Determine if the interface represents a manager related session
    def _is_manager_session(self, interface, package_name, patterns=None):
        if patterns is None:
            patterns = self.patterns
        is_manager_session = False

        if package_name in ['type']:
            is_manager_session = True
        elif (interface['category'] == 'sessions' and
                interface['shortname'].startswith(patterns['package_catalog_caps'])):
            is_manager_session = True
        return is_manager_session

    def _make_method(self, method, interface, service_catalog=None):
        if service_catalog is None:
            class_name = interface['shortname']
        else:
            class_name = service_catalog
        method_name = method['name']
        method_sig = ''

        if not (('OsidManager' in interface['inherit_shortnames'] or
                 'OsidProxyManager' in interface['inherit_shortnames']) and
                '_session' in method_name):
            if method_name == 'get_id':
                method_sig = '   .. autoattribute:: ' + class_name + '.ident'
            elif method_name == 'get_identifier_namespace':
                method_sig = '   .. autoattribute:: ' + class_name + '.namespace'
            elif method_name.startswith('get_') and method['args'] == []:
                method_sig = '   .. autoattribute:: ' + class_name + '.' + fix_reserved_word(method_name[4:])
            elif method_name.startswith('set_') and len(method['args']) == 1:
                method_sig = '   .. autoattribute:: ' + class_name + '.' + fix_reserved_word(method_name[4:])
            elif method_name.startswith('clear_') and method['args'] == []:
                method_sig = '   .. autoattribute:: ' + class_name + '.' + fix_reserved_word(method_name[6:])

            # And finally all the methods:
            else:
                method_sig = '   .. automethod:: {0}.{1}'.format(class_name,
                                                                 method_name)

        return method_sig

    def _patterns(self):
        patterns = self._load_patterns_file()
        for inf in self.package['interfaces']:
            patterns[self._is_session(inf, 'manager')] = self._is_manager_session(inf,
                                                                                  self.package['name'],
                                                                                  patterns=patterns)
            patterns[self._is_session(inf, 'catalog')] = self._is_catalog_session(inf,
                                                                                  self.package['name'],
                                                                                  patterns=patterns)
        return patterns

    def _update_module_imports(self, modules, interface):
        package = self.replace(fix_reserved_word(self.package['name'], is_module=True))
        if any(sn in interface['inherit_shortnames']
               for sn in ['OsidManager', 'OsidProxyManager', 'OsidProfile']):
            module_name = 'service_managers'
            currentmodule_str = '.. currentmodule:: dlkit.services.{0}'.format(package)
            automodule_str = '.. automodule:: dlkit.services.{0}'.format(package)

        elif interface['shortname'] == self.patterns['package_catalog_caps']:
            module_name = self.patterns['package_catalog_under']
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

        if self.patterns['package_catalog_under'] != 'no_catalog':
            toc_str = '{0}   {1}\n'.format(toc_str,
                                           self.patterns['package_catalog_under'])

        for module in modules:
            if ('_'.join(module.split('.')) not in [
                    'service_managers',
                    self.patterns['package_catalog_under'],
                    'records',
                    'rules',
                    'managers',
                    'sessions',
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
        exceptions = []
        excepted_osid_categories = ['properties',
                                    'query_inspectors',
                                    'receivers',
                                    'search_orders',
                                    'searches']

        # Check to see if manager should be implemented (this should
        # probably be moved to binder_helpers.flagged_for_implementation)
        if (interface['category'] == 'managers' and
                self.package['name'] not in managers_to_implement):
            return False

        # Check to see if this interface is meant to be implemented.
        if (self.package['name'] != 'osid' and
                interface['category'] not in excepted_osid_categories):
            if self._flagged_for_implementation(interface):
                if interface['shortname'] in exceptions:
                    return False
                if interface['shortname'].endswith('ProxyManager'):
                    return False
            else:
                return False

        if interface['category'] in excepted_osid_categories:
            return False

        # if (interface['category'] in ['sessions', 'managers']):
        #     return False

        return True

    def build_this_method(self, interface, method):
        build_me = True
        package_name = self.package['name']

        if (interface['category'] == 'managers' and
                package_name != 'osid' and
                interface['shortname'].endswith('Profile') and
                method['name'].startswith('supports_') and
                under_to_caps(method['name'][9:]) + 'Session' not in sessions_to_implement):
            build_me = False

        if (('OsidManager' in interface['inherit_shortnames'] or
             'OsidProxyManager' in interface['inherit_shortnames']) and
                '_session' in method['name']):
            build_me = False

        return build_me

    def class_doc(self, interface):
        # Inspect the class doc string for headline + body and create
        # appropriate doc string style. Trying to conform to PEP 257 as
        # much as the source osid doc will allow.
        if interface['doc']['body'].strip() == '':
            class_doc = '{0}{1}'.format(self._ind,
                                        self._wrap(remove_extra_whitespace(interface['doc']['headline'])))
        else:
            class_doc = '{0}{1}\n\n{2}\n\n{3}'.format(self._ind,
                                                      self._wrap(remove_extra_whitespace(interface['doc']['headline'])),
                                                      self._wrap(interface['doc']['body']),
                                                      self._ind)
        return class_doc

    def make(self):
        self.make_osids()

    # def make_methods(self, interface, patterns, package_name=None, service_catalog=None):
    #     body = []
    #     for method in interface['methods']:
    #         if package_name is None:
    #             class_name = interface['shortname']
    #         elif service_catalog is not None:
    #             class_name = service_catalog
    #         else:
    #             class_name = package_name
    #         ##
    #         # Here is where we check for the Python properties stuff:
    #         if method['name'] == 'get_id':
    #             automethod_str = '   .. autoattribute:: ' + class_name + '.ident'
    #         elif method['name'] == 'get_identifier_namespace':
    #             automethod_str = '   .. autoattribute:: ' + class_name + '.namespace'
    #         elif method['name'].startswith('get_') and method['args'] == []:
    #             if method['name'] in ['get_copyright', 'get_license']:
    #                 automethod_str = '   .. autoattribute:: ' + class_name + '.' + method['name'][4:] + '_'
    #             else:
    #                 automethod_str = '   .. autoattribute:: ' + class_name + '.' + method['name'][4:]
    #         elif method['name'] == 'get_items' and len(method['args']) == 1:
    #             if method['args'][0]['var_name'] == 'assessment_id':
    #                 method_name = 'get_assessment_items'
    #             elif method['args'][0]['var_name'] == 'taken_id':
    #                 method_name = 'get_taken_items'
    #             else:
    #                 raise Exception
    #             automethod_str = '   .. automethod:: ' + class_name + '.' + method_name
    #         elif method['name'].startswith('set_') and len(method['args']) == 1:
    #             if method['name'] in ['set_copyright', 'set_license']:
    #                 automethod_str = '   .. autoattribute:: ' + class_name + '.' + method['name'][4:] + '_'
    #             else:
    #                 automethod_str = '   .. autoattribute:: ' + class_name + '.' + method['name'][4:]
    #         elif method['name'].startswith('clear_') and method['args'] == []:
    #             if method['name'] in ['clear_copyright', 'clear_license']:
    #                 automethod_str = '   .. autoattribute:: ' + class_name + '.' + method['name'][6:] + '_'
    #             else:
    #                 automethod_str = '   .. autoattribute:: ' + class_name + '.' + method['name'][6:]
    #         ##
    #         # And finally all the methods:
    #         else:
    #             automethod_str = '   .. automethod:: ' + class_name + '.' + method['name']
    #
    #         if automethod_str not in body:
    #             body.append(automethod_str)
    #     return '\n\n'.join(body)

    def make_methods(self, interface, package_name=None, service_catalog=None):
        body = []
        for method in interface['methods']:
            if not self.build_this_method(interface, method):
                continue

            method_sig = self._make_method(method, interface, service_catalog)
            if method_sig != '':
                self.append(body, method_sig)

        return '\n\n'.join(body)

    def module_body(self, interface):
        sn = interface['shortname']
        header = ' '.join(camel_to_list(sn))
        body = '{0}\n{1}\n\n.. autoclass:: {2}\n   :show-inheritance:\n\n'.format(header,
                                                                                  '-' * len(header),
                                                                                  sn)
        # body = '{0}\n{1}\n\n.. py:class:: {2}{3}\n{4}\n\n'.format(header,
        #                                                           '-' * len(header),
        #                                                           sn,
        #                                                           inheritance,
        #                                                           self._wrap(self.class_doc(interface)))

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
        if self._module_name in ['service_managers', self.patterns['package_catalog_under']]:
            modules[interface['category']]['body'] += self._get_simple_module_body(interface)

    def write_license_file(self):
        with open(self._abc_module('summary', extension='rst'), 'w') as write_file:
            pkg_name = self.replace(fix_reserved_word(self.package['name'],
                                                      is_module=True))
            write_file.write(('Summary\n=======\n\n' +
                              '.. currentmodule:: dlkit.services.' +
                              pkg_name + '\n' +
                              '.. automodule:: dlkit.services.' +
                              pkg_name + '\n').encode('utf-8'))

    def write_modules(self, modules):
        # first, write the Table of Contents
        self._write_toc(modules)

        # Finally, iterate through the completed package module structure and
        # write out both the import statements and class definitions to the
        # appropriate module for this package.
        for module in modules:
            if (modules[module]['body'].strip() != '' and
                    module not in ['sessions', 'managers']):
                with open(self._abc_module('_'.join(module.split('.')),
                                           extension='rst'), 'w') as write_file:
                    write_file.write('{0}\n\n\n{1}'.format('\n'.join(modules[module]['imports']),
                                                           modules[module]['body']).encode('utf-8'))


def format_module_docstring(module_docstring):
    fixed_return = re.sub(r'return:', ':return:', module_docstring)
    fixed_params = re.sub(r'arg:', ':arg:', fixed_return)
    fixed_raise = re.sub(r'raise:', ':raises:', fixed_params)
    return fixed_raise


def remove_extra_whitespace(headline):
    without_newlines = headline.replace('\n', ' ')
    return re.sub(r'\s+', ' ', without_newlines)


def set_and_del_property(method, service_catalog=None):
    method_name = strip_prefixes(method['name'])
    prop = '    .. py:attribute:: {0}\n'.format(fix_reserved_word(method_name))

    if service_catalog is None:
        prop += '{0}:noindex:\n'.format(8 * ' ')

    return prop


def simple_property(prop_type, method, property_name=None, service_catalog=None):
    method_name = strip_prefixes(method['name'])

    if property_name is None:
        attr_name = fix_reserved_word(method_name)
    else:
        attr_name = property_name

    prop = '    .. py:attribute:: {0}\n'.format(attr_name)
    if service_catalog is None:
        prop += '{0}:noindex:\n'.format(8 * ' ')

    return prop
