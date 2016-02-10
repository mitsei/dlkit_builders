from config import managers_to_implement, sessions_to_implement

from binder_helpers import camel_to_list, SkipMethod, under_to_caps
from build_controller import BaseBuilder
from interface_builders import InterfaceBuilder
from method_builders import argless_clear, argless_get,\
    simple_property, set_and_del_property, one_arg_set


class KitDocDLKitBuilder(InterfaceBuilder, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(KitDocDLKitBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir + '/dlkit'
        self._template_dir = self._abs_path + '/builders/kitosid_templates'

        self._excluded_packages = ['proxy', 'type']

        self._class = 'doc_dlkit'

    def _append_inherited_imports(self, imports, interface):
        # Iterate through any inherited interfaces and check if an import statement is
        # required and append to the appropriate module's import list.
        inherit_category = 'UNKNOWN_MODULE'
        for i in interface['inheritance']:
            inherit_category = self.get_interface_module(i['pkg_name'], i['name'], True)
            if (i['pkg_name'] == self.package['name'] and
                    inherit_category == interface['category']):
                pass
            else:
                import_str = 'from ..{0} import {1} as {0}_{1}'.format(self._abc_pkg_name(package_name=i['pkg_name'],
                                                                                          abc=False),
                                                                       inherit_category)

                if inherit_category != 'UNKNOWN_MODULE':
                    self.append(imports, import_str)
        return inherit_category

    def _build_as_service_interface(self, interface):
        # only build managers and catalogs
        basic_build = self._build_this_interface(interface)
        managers = ['managers', 'markers']
        catalogs = ['OsidSession', 'OsidObject', 'OsidCatalog', 'OsidList']
        catalogs += [self.patterns['package_catalog_caps']]
        catalogs += [self.patterns['package_catalog_caps'] + 'List']
        is_manager_or_cat = (interface['category'] in managers or
                             interface['shortname'] in catalogs)
        return basic_build and is_manager_or_cat

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
        module[self.package['name']] = dict(imports=[], body='')
        return module

    def _get_class_inheritance(self, interface):
        inheritance = []

        # Iterate through any inherited interfaces and build the inheritance
        # list for this interface. Also, check if an import statement is
        # required and append to the appropriate module's import list.
        for i in interface['inheritance']:
            inherit_category = self.get_interface_module(i['pkg_name'], i['name'], True)

            if i['pkg_name'] == self.package['name'] and inherit_category == interface['category']:
                inheritance.append(i['name'])
            else:
                inheritance.append(i['pkg_name'] + '_' +
                                   inherit_category + '.' + i['name'])

        # Don't forget the OsidSession inheritance:
        if (('OsidManager' in interface['inherit_shortnames'] or
                interface['shortname'] == self.patterns['package_catalog_caps']) and
                self.package['name'] != 'osid'):
            inheritance.insert(1, 'osid_sessions.OsidSession')

        if inheritance:
            inheritance = '({})'.format(', '.join(inheritance))
        else:
            inheritance = ''

        return inheritance

    def _get_method_args(self, method, interface, patterns):
        args = ['self']
        for arg in method['args']:
            args.append(arg['var_name'])
        return args

    @staticmethod
    def _get_method_doc(method):
        return filter(None, [method['sphinx_param_doc'].strip('\n'),
                             method['sphinx_return_doc'].strip('\n'),
                             method['sphinx_error_doc'].strip('\n') + '\n',
                             method['compliance_doc'].strip('\n'),
                             method['impl_notes_doc'].strip('\n')])

    def _grab_service_methods(self, type_check_method):
        self.patterns['implemented_view_methods'] = []
        inherited_imports = []
        methods = ''
        for inf in self.package['interfaces']:
            # Check to see if this interface is meant to be implemented.
            if self.package['name'] != 'osid' and not self._flagged_for_implementation(inf):
                continue

            if type_check_method(inf, self.package['name'], patterns=self.patterns):
                methods += '\n##\n# The following methods are from {}\n\n'.format(inf['fullname'])
                methods += self._make_service_methods(inf) + '\n\n'
                inherited_imports = self.get_methods_templated_imports(self._abc_pkg_name(abc=False),
                                                                       inf)
        return methods, inherited_imports

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

    def _make_method(self, method, interface, patterns=None):
        if patterns is None:
            patterns = self.patterns
        args = self._get_method_args(method, interface, patterns)
        method_impl = self._make_method_impl(method, interface)

        method_sig = '{}def {}({}):'.format(self._ind,
                                            method['name'],
                                            ', '.join(args))

        method_doc = self._build_method_doc(method)

        return (method_sig + '\n' +
                method_doc + '\n' +
                method_impl)

    def _make_method_impl(self, method, interface):
        if method['return_type'].strip():
            return '{}return # {}'.format(self._dind,
                                          method['return_type'])
        else:
            return '{}pass'.format(self._dind)

    def _make_service_methods(self, interface):
        body = []
        for method in interface['methods']:
            if method['name'] == 'get_items' and interface['shortname'] == 'AssessmentResultsSession':
                method['name'] = 'get_taken_items'
            if method['name'] == 'get_items' and interface['shortname'] == 'AssessmentBasicAuthoringSession':
                method['name'] = 'get_assessment_items'

            if not self.build_this_method(interface, method):
                continue

            try:
                body.append(self._make_method(method, interface, self.patterns))
            except SkipMethod:
                # Only expected from kitosid / services builder
                pass
            else:
                # Here is where we add the Python properties stuff:
                if argless_get(method):
                    body.append(simple_property('get', method))
                elif one_arg_set(method):
                    if (simple_property('del', method)) in body:
                        body.remove(simple_property('del', method))
                        body.append(set_and_del_property(method))
                    else:
                        body.append(simple_property('set', method))
                elif argless_clear(method):
                    if (simple_property('set', method)) in body:
                        body.remove(simple_property('set', method))
                        body.append(set_and_del_property(method))
                    else:
                        body.append(simple_property('del', method))

                if method['name'] == 'get_id':
                        body.append(simple_property('get', method, 'ident'))
                if method['name'] == 'get_identifier_namespace':
                        body.append(simple_property('get', method, 'namespace'))

        return '\n\n'.join(body)

    def _services_module_body(self, interface):
        additional_methods = self._additional_methods(interface)
        inheritance = self._get_class_inheritance(interface)
        init_methods = self._make_init_methods(interface)
        methods = self._make_service_methods(interface)
        body = ''

        # Add all the appropriate manager related session methods to the manager interface
        # Add all the appropriate catalog related session methods to the catalog interface
        if any(m in interface['inherit_shortnames']
               for m in ['OsidManager', 'OsidProxyManager', 'OsidProfile']):
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
                                                 self.class_doc(interface),
                                                 init_methods,
                                                 methods)
        return body

    def _update_module_imports(self, modules, interface):
        imports = modules[interface['category']]['imports']
        pkg_imports = modules[self.package['name']]['imports']

        self._append_inherited_imports(imports, interface)
        self._append_inherited_imports(pkg_imports, interface)

        # Don't forget the OsidSession inheritance:
        if (('OsidManager' in interface['inherit_shortnames'] or
                interface['shortname'] == self.patterns['package_catalog_caps']) and
                self.package['name'] != 'osid'):
            self.append(imports, 'from ..osid import sessions as osid_sessions')
            self.append(pkg_imports, 'from ..osid import sessions as osid_sessions')

    def build_this_interface(self, interface):
        # return True
        return self._build_this_interface(interface)

    def build_this_method(self, interface, method):
        package_name = self.package['name']
        build_me = True
        if (interface['category'] == 'managers' and
                package_name != 'osid' and
                interface['shortname'].endswith('Manager') and
                method['name'].startswith('get') and
                'session' in method['name']):
                # method['return_type'].split('.')[-1] not in sessions_to_implement):
            build_me = False
        if (interface['category'] == 'managers' and
                package_name != 'osid' and
                interface['shortname'].endswith('Profile') and
                method['name'].startswith('supports_') and
                under_to_caps(method['name'][9:]) + 'Session' not in sessions_to_implement):
            build_me = False
        # if (interface['category'] == 'sessions' and
        #         (method['name'] == 'get_' + self.patterns['package_catalog_under'] + '_id' or
        #          method['name'] == 'get_' + self.patterns['package_catalog_under'])):
        #     build_me = False
        return build_me

    def make(self):
        self.make_osids(build_abc=False)

    def module_body(self, interface):
        inheritance = self._get_class_inheritance(interface)
        return '{0}\n{1}\n{2}\n{3}\n\n\n'.format(self.class_sig(interface, inheritance),
                                                 self.class_doc(interface),
                                                 self._additional_methods(interface),
                                                 self.make_methods(interface))

    def update_module_body(self, modules, interface):
        modules[interface['category']]['body'] += self.module_body(interface)
        if self._build_as_service_interface(interface):
            modules[self.package['name']]['body'] += self._services_module_body(interface)

    def write_license_file(self):
        with open(self._abc_module('license'), 'w') as write_file:
            write_file.write((self._utf_code + '\"\"\"' +
                              self.package['title'] + '\n' +
                              self.package['name'] + ' version ' +
                              self.package['version'] + '\n\n' +
                              self.package['copyright'] + '\n\n' +
                              self.package['license'] + '\n\n\"\"\"').encode('utf-8') +
                             '\n')

    def write_modules(self, modules):
        summary = u'{0}\"\"\"{1}\n{2} version {3}\n\n{4}\n\n\"\"\"\n'.format(self._utf_code,
                                                                             self.package['title'],
                                                                             self.package['name'],
                                                                             self.package['version'],
                                                                             self.package['summary']).encode('utf-8')
        ##
        # Finally, iterate through the completed package module structure and
        # write out both the import statements and class definitions to the
        # appropriate module for this package.
        for module in modules:
            if modules[module]['body'] is not None and modules[module]['body'].strip() != '':
                with open(self._abc_module(module), 'w') as write_file:
                    write_file.write('{0}\n\n\n{1}'.format('\n'.join(modules[module]['imports']),
                                                           modules[module]['body']).decode('utf-8').encode('utf-8'))
                with open('{0}/services/{1}.py'.format(self._app_name(),
                                                       self.package['name']), 'w') as write_file:
                    write_file.write('{0}{1}\n\n\n{2}'.format(summary,
                                                              '\n'.join(modules[self.package['name']]['imports']),
                                                              modules[self.package['name']]['body']).decode('utf-8').encode('utf-8'))
