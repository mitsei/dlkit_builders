from build_controller import BaseBuilder
from interface_builders import InterfaceBuilder


class TestBuilder(InterfaceBuilder, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(TestBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir
        self._template_dir = self._abs_path + '/builders/test_templates'

        self._class = 'tests'

    def _build_method_doc(self, method):
        return '{0}\"\"\"Tests {1}\"\"\"'.format(self._dind,
                                                 method['name'])

    def _clean_up_impl(self, impl, interface, method):
        if impl == '':
            impl = '{}pass'.format(self._dind)
        else:
            context = self._get_method_context(method, interface)
            interface_sn = interface['shortname']
            method_n = method['name']
            interface_cat = interface['category']

            if (interface_cat in self.patterns['impl_log'] and
                    interface_sn in self.patterns['impl_log'][interface_cat]):
                self.patterns['impl_log'][context['module_name']][interface_sn][method_n][1] = 'implemented'
        return impl

    def _get_method_sig(self, method, interface):
        args = self._get_method_args(method, interface)
        method_impl = self._make_method_impl(method, interface)
        method_sig = '{}def test_{}({}):'.format(self._ind,
                                                 method['name'],
                                                 ', '.join(args))

        if method_impl == '{}pass'.format(self._dind):
            method_sig = '{}@unittest.skip(\'unimplemented test\')\n{}'.format(self._ind,
                                                                               method_sig)

        return method_sig

    def _update_module_imports(self, modules, interface):
        imports = modules[interface['category']]['imports']
        self.append(imports, 'import unittest')

        # Check to see if there are any additional inheritances required
        # by the implementation patterns.  THIS MAY WANT TO BE REDESIGNED
        # TO ALLOW INSERTING THE INHERITANCE IN A PARTICULAR ORDER.
        impl_class = self._load_impl_class(interface['shortname'])
        if hasattr(impl_class, 'inheritance_imports'):
            self.append(imports, getattr(impl_class, 'inheritance_imports'))

        self._append_pattern_imports(imports, interface)
        self._append_templated_imports(imports, interface)

        imports = list(set(imports))  # let's remove repeats

    def _wrap(self, text):
        return text

    def _write_module_string(self, write_file, module):
        write_file.write('{0}\n{1}\n'.format('\n'.join(self._order_module_imports(module['imports'])),
                                             module['body'].strip()).encode('utf-8'))

    def build_this_interface(self, interface):
        return self._build_this_interface(interface)

    def class_doc(self, interface):
        return '{0}\"\"\"Tests for {1}\"\"\"'.format(self._ind,
                                                     interface['shortname'])

    def class_sig(self, interface, inheritance):
        return 'class Test{}{}:'.format(interface['shortname'],
                                        inheritance)

    def make(self):
        self.make_osids()

    def module_body(self, interface):
        inheritance = self._get_class_inheritance(interface)
        init_methods = self._make_init_methods(interface)
        methods = self.make_methods(interface)
        additional_methods = self._additional_methods(interface)
        additional_classes = self._additional_classes(interface)

        if additional_methods:
            methods += '\n' + additional_methods

        if additional_classes:
            # extra newlines generated in self._additional_classes
            methods += additional_classes

        init_methods_not_blank = init_methods != '' and not init_methods.isspace()
        if init_methods_not_blank:
            init_methods = self._wrap(init_methods) + '\n'
        else:
            init_methods = ''

        if methods:
            if init_methods_not_blank:
                methods = '{0}\n'.format(methods)
            else:
                methods = '\n{0}\n'.format(methods)

        body = '\n\n{0}\n{1}\n{2}{3}'.format(self.class_sig(interface, inheritance),
                                             self._wrap(self.class_doc(interface)),
                                             init_methods,
                                             methods)
        return body

    def module_header(self, module):
        return '\"\"\"Unit tests of {0} {1}.\"\"\"'.format(self.package['name'],
                                                           module)

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
                with open(self._abc_module(module_name, test=True), 'wb') as write_file:
                    self._write_module_string(write_file,
                                              modules[module])
