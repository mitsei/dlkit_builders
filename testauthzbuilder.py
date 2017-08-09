import json
from collections import OrderedDict

from build_dlkit import BaseBuilder
from interface_builders import InterfaceBuilder
from binder_helpers import under_to_caps, under_to_mixed, camel_to_mixed, camel_to_under, remove_plural


class TestAuthZBuilder(InterfaceBuilder, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(TestAuthZBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir
        self._template_dir = self._abs_path + '/testauthz_templates'

        self._class = 'test_authz'

    def _build_method_doc(self, method):
        return '{0}// Tests {1}'.format(self._ind,
                                        under_to_mixed(method['name']))

    def _clean_up_impl(self, impl, interface, method):
        if not impl.strip():
            impl = ''
        elif impl.strip() == 'NOT READY':
            impl = '{}assertTrue("This test is not ready.", false);\n{}}}'.format(self._dind, self._ind)
        else:
            context = self._get_method_context(method, interface)
            interface_sn = interface['shortname']
            method_n = method['name']
            interface_cat = interface['category']

            if (interface_cat in self.patterns['impl_log'] and
                    interface_sn in self.patterns['impl_log'][interface_cat]):
                self.patterns['impl_log'][context['module_name']][interface_sn][method_n][1] = 'implemented'
        return impl

    def _get_method_args(self, method, interface):
        return ['']

    def _get_init_context(self, init_pattern, interface):
        context = super(TestAuthZBuilder, self)._get_init_context(init_pattern, interface)
        # Add additional context mappings here
        return context

    def _get_method_sig(self, method, interface):
        method_sig = ''
        return method_sig

    def _update_module_imports(self, modules, interface):
        imports = modules[interface['category']]['imports']
        # self.append(imports, 'package this.is.not.where.package.path.goes')

        # Check to see if there are any additional inheritances required
        # by the implementation patterns.  THIS MAY WANT TO BE REDESIGNED
        # TO ALLOW INSERTING THE INHERITANCE IN A PARTICULAR ORDER.
        impl_class = self._load_impl_class(interface['shortname'])
        if hasattr(impl_class, 'inheritance_imports'):
            self.append(imports, getattr(impl_class, 'inheritance_imports'))

        self._append_pattern_imports(imports, interface)
        self._append_templated_imports(imports, interface)

    def _get_module_imports(self, modules, interface):
        if interface['shortname'] != 'osid':
            imports = [
                # put global imports here
            ]
        else:
            imports = []
        # self.append(imports, 'package this.is.not.where.package.path.goes')

        # Check to see if there are any additional inheritances required
        # by the implementation patterns.  THIS MAY WANT TO BE REDESIGNED
        # TO ALLOW INSERTING THE INHERITANCE IN A PARTICULAR ORDER.
        impl_class = self._load_impl_class(interface['shortname'])
        if hasattr(impl_class, 'inheritance_imports'):
            self.append(imports, getattr(impl_class, 'inheritance_imports'))

        self._append_pattern_imports(imports, interface)
        self._append_templated_imports(imports, interface)
        return imports

    def _compile_method(self, args, decorators, method_sig, method_doc, method_impl):
        if not method_impl.strip():
            return ''
        elif decorators:
            decorators = '\n'.join(decorators)
            return self._wrap('{0}\n{1}\n{2}\n{3}'.format(method_doc,
                                                          decorators,
                                                          method_sig,
                                                          method_impl))
        else:
            return self._wrap('{0}\n{1}\n{2}'.format(method_doc,
                                                     method_sig,
                                                     method_impl))

    def _wrap(self, text):
        return text

    # DON'T NEED FOR THIS BUILDER?
    def _write_module_string(self, write_file, module):
        write_file.write('{0}\n\n\n{1}'.format('\n'.join(module['imports']),
                                               module['body']).encode('utf-8'))

    def build_this_interface(self, interface):
        # return (('OsidObject' in interface['inherit_shortnames'] or
        #         'OsidRelationship' in interface['inherit_shortnames']) and
        #         'Subjugateable' not in interface['inherit_shortnames'] and
        #         self._build_this_interface(interface))
        if interface['shortname'] == 'SequenceRuleLookupSession':
            return False  # Until we figure out why its not building properly in services
        if interface['shortname'] in ['FunctionLookupSession', 'QualifierLookupSession']:
            return False  # Until we can properly implement these in json impls
        return (interface['shortname'].endswith('LookupSession') and
                'OsidCatalog' not in interface['inherit_shortnames'])

    def class_doc(self, interface):
        return ''

    def class_sig(self, interface, inheritance):
        return ''

    def make(self):
        self.make_osids()

    # This function is not used for this builder:
    def package_header(self):
        package_name = self._abc_pkg_path().split('/')[-1]
        return '"""TestAuthZ implementations of {} objects."""'.format(package_name)

    def module_doc(self, interface):
        package_name = self._abc_pkg_path().split('/')[-1]
        return '"""TestAuthZ implementations of {0}.{1}"""'.format(
            package_name,
            interface['shortname'].split('LookupSession')[0])

    def module_body(self, interface):
        inheritance = self._get_class_inheritance(interface)
        init_methods = self._make_init_methods(interface)
        methods = self.make_methods(interface)
        additional_methods = self._additional_methods(interface)
        additional_classes = self._additional_classes(interface)

        if additional_methods:
            methods += additional_methods

        if additional_classes:
            # extra newlines generated in self._additional_classes
            methods += additional_classes

        if init_methods:
            init_methods = self._wrap(init_methods)

        if methods:
            methods = '\n{0}\n'.format(methods)

        body = '\n\n{0}\n{1}\n{2}{3}'.format(self.class_sig(interface, inheritance),
                                             self._wrap(self.class_doc(interface)),
                                             init_methods,
                                             methods)
        return body

    def _make_osid(self, file_name):
        # Overrides for implementing java style
        # This function expects a file containing a json representation of an
        # osid package that was prepared by the mapper.
        # for sub-packages, append them to a base package file...
        with open(file_name, 'r') as read_file:
            self.package = json.load(read_file)

        if not self._package_to_be_implemented():
            return

        self._copy_package_helpers()

        print("Building authz tests for {1}".format(self._class, self.package['name']))

        self.patterns = self._patterns()

        # The map structure for the modules to be created by this function.
        # Each module will get a body string that holds the class and method
        # signatures for the particular interface category, and a list of
        # for the modules that the module's classes may inherit.
        modules = self._empty_modules_dict()

        self._initialize_directories()
        self.write_license_file()
        self.write_profile_file()

        # Initialize the module doc and abc import string for each module
        for module in modules:
            modules[module]['imports'].append(self.module_header(module))

        # The real work starts here.  Iterate through all interfaces to build
        # all the classes for this osid package.
        for interface in self.package['interfaces']:
            # print '    ', interface['shortname'], 'inherits', interface['inherit_shortnames']
            if not self.build_this_interface(interface):
                continue
            print '    building -', interface['shortname']
            imports = self._get_module_imports(modules, interface)  # DONT NEED modules in this method?
            body = self.module_body(interface)
            if body.strip():
                self.write_class(interface, imports, body)

        # self.write_modules(modules)

    def write_class(self, interface, imports, body):
        # Writes one java class per file:
        if body != '' and len(interface['fullname'].split('.')) != 2:  # Hack to not build osid
            class_name = 'test_' + camel_to_under(interface['shortname'][:-13]) + '_authz'
            # module_dir = self._abc_pkg_path(abc=True) + '/authz_tests/'
            module_dir = self._app_name() + '/functional/test_authz/' + self._abc_pkg_name(abc=True) + '/'
            module_path = module_dir + class_name + '.py'
            # module_path = self._abc_module(class_name, extension='py')
            self._make_dir(module_dir, python=True)
            with open(module_path, 'wb') as write_file:
                write_file.write('{0}\n\n{1}\n{2}\n'.format(
                    self.module_doc(interface),
                    '\n'.join(imports),
                    body.strip()).encode('utf-8'))
