import glob
import json

import inflection

from build_controller import BaseBuilder
from binder_helpers import SkipMethod, fix_reserved_word
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

    def _clean_up_impl(self, impl, interface, method):
        un_impl_doc = '{}\"\"\"Pass through to provider unimplemented\"\"\"\n'.format(self._dind)

        if impl == '' and method['args']:
            impl = ('{}{}raise Unimplemented(\'Unimplemented in dlkit.services - ' +
                    'args=\' + str(args) + \', kwargs=\' + str(kwargs))').format(un_impl_doc,
                                                                                 self._dind)
        elif impl == '' and not method['args']:
            impl = '{}{}raise Unimplemented(\'Unimplemented in dlkit.services\')'.format(un_impl_doc,
                                                                                         self._dind)
        return impl

    def _compile_method(self, args, decorator, method_sig, method_doc, method_impl):
        return method_sig + '\n' + method_impl

    def _confirm_build_method(self, impl_class, method_name):
        # Check if this method is marked to be skipped (the assumption
        # is that it will be implemented elsewhere, perhaps in an init.)
        if (impl_class and
                hasattr(impl_class, method_name) and
                getattr(impl_class, method_name) is None):
            raise SkipMethod()

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

    def _get_method_args(self, method, interface):
        args = ['self']
        args += [a['var_name'] for a in method['args']]
        return args

    def _get_method_sig(self, method, interface):
        # The following method sig builder specifically creates the arguments.  It
        # is the one used by most of the other builders.
        interface_name = interface['shortname']
        if interface_name.endswith('List') or method['name'] == 'initialize':
            args = self._get_method_args(method, interface)
            method_sig = '{}def {}({}):'.format(self._ind,
                                                method['name'],
                                                ', '.join(args))
        # The following method sig builder uses *args, **kwargs for all methods. It is used
        # by the dlkit builder to pass arguments in the blind.
        elif (method['args'] or interface_name.endswith('Manager') and
                not 'Runtime' in interface_name):
            method_sig = '{}def {}(self, *args, **kwargs):'.format(self._ind,
                                                                   method['name'])
        else:
            method_sig = '{}def {}(self):'.format(self._ind,
                                                  method['name'])
        return method_sig

    def _get_sub_package_imports(self, interface):
        # get the imports from sub-packages
        return []

    def _get_sub_package_methods(self, interface):
        # check the packages directory for related sub-packages
        sub_package_methods = ''
        current_package = self.package['name']

        for json_file in glob.glob(self._package_directory()):
            sub_package_prefix = '{}_'.format(current_package)
            if sub_package_prefix in json_file:
                with open(json_file, 'r') as read_file:
                    sub_package = json.load(read_file)
                    for inf in sub_package['interfaces']:
                        self.patterns = self._update_patterns_with_manager_catalog_flags(self.patterns,
                                                                                         inf,
                                                                                         sub_package)

                    for sub_inf in sub_package['interfaces']:
                        sub_interface_name = sub_inf['shortname']
                        if self._is_matching_interface(interface, sub_inf):
                            sub_package_methods += '\n\n{}##Implemented from {} - {}\n'.format(self._ind,
                                                                                               sub_package['name'],
                                                                                               sub_interface_name)
                            sub_package_methods += self.make_methods(sub_inf)

        return sub_package_methods

    def _get_template_name(self, pattern, interface_name, method_name):
        template_name = self.last(pattern) + '_template'
        if interface_name.endswith('ProxyManager'):
            pass
        elif interface_name.endswith('Manager') and 'session' in method_name:
            if self.patterns[method_name[4:].split('_for_')[0] + '.is_manager_session']:
                template_name = self.last(pattern) + '_managertemplate'
            elif self.patterns[method_name[4:].split('_for_')[0] + '.is_catalog_session']:
                template_name = self.last(pattern) + '_catalogtemplate'
        return template_name

    @staticmethod
    def _is_matching_interface(potential_parent, potential_child):
        parent_name = potential_parent['shortname']
        child_name = potential_child['shortname']

        if potential_parent['category'] == 'managers':
            parent_parts = inflection.underscore(parent_name).split('_')
            num_parent_parts = len(parent_parts)
            child_parts = inflection.underscore(child_name).split('_')
            num_child_parts = len(child_parts)

            if num_child_parts <= num_parent_parts:
                return False

            num_matches = 0
            for part in parent_parts:
                if part in child_parts:
                    num_matches += 1

            if num_matches == num_parent_parts:
                return True
            else:
                return False
        else:
            # catalog / objects
            # check if potential_parent['shortname'].lower() has a corresponding
            # get_X method in potential_child['methods']
            catalog = potential_parent['shortname'].lower()
            get_catalog_method = 'get_{}'.format(catalog)
            child_methods = [m['name'] for m in potential_child['methods']]
            if get_catalog_method in child_methods:
                return True
            else:
                return False

    def _package_directory(self):
        if self.package_maps[-1] != '/':
            directory = self.package_maps + '/*.json'
        else:
            directory = self.package_maps + '*.json'

        return directory

    def _package_to_be_implemented(self):
        # don't build sub-packages separately...make them as part of the
        # main, base package
        if len(self.package['name'].split('.')) > 1:
            return False
        return True

    def _patterns(self):
        patterns = self._load_patterns_file()
        for inf in self.package['interfaces']:
            patterns = self._update_patterns_with_manager_catalog_flags(patterns,
                                                                        inf,
                                                                        self.package)
        return patterns

    def _update_implemented_view_methods(self, method, interface):
        if ((interface['shortname'] == 'LoggingSession' and method['name'] == 'get_log_id') or
                (interface['shortname'] == 'LoggingSession' and method['name'] == 'get_log')):
            # we want this to build, no matter what
            return
        method_name = method['name']
        if ('implemented_view_methods' in self.patterns and
                method_name in self.patterns['implemented_view_methods']):
            raise SkipMethod()
        elif 'implemented_view_methods' in self.patterns:
            self.patterns['implemented_view_methods'].append(method_name)

    def _update_module_imports(self, modules, interface):
        imports = modules[self.package['name']]['imports']

        self.append(imports, self._abc_package_imports(interface))
        self._append_inherited_imports(imports, interface)
        self._append_pattern_imports(imports, interface)

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

        new_imports += self._get_sub_package_imports(interface)

        for imp in new_imports:
            self.append(imports, imp)

    def _update_patterns_with_manager_catalog_flags(self, patterns, inf, package):
        patterns[self._is_session(inf, 'manager')] = self._is_manager_session(inf,
                                                                              package['name'],
                                                                              patterns=patterns)
        patterns[self._is_session(inf, 'catalog')] = self._is_catalog_session(inf,
                                                                              package['name'],
                                                                              patterns=patterns)
        return patterns

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
        methods = self.make_methods(interface)

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

        methods += self._get_sub_package_methods(interface)

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
                                              fix_reserved_word(self.first(self.package['name']), is_module=True)), 'w') as write_file:
                    self._write_module_string(write_file,
                                              modules[module])