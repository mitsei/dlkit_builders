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

    def _write_module_string(self, write_file, module):
        write_file.write('{0}\n\n\n{1}'.format('\n'.join(module['imports']),
                                               module['body']).encode('utf-8'))

    def build_this_interface(self, interface):
        return self._build_this_interface(interface)

    def class_doc(self, interface):
        return '{0}\"\"\"Tests for {1}\"\"\"'.format(self._ind,
                                                     interface['shortname'])

    def class_sign(self, interface, inheritance):
        return 'class Test{}{}:'.format(interface['shortname'],
                                        inheritance)

    def make(self):
        self.make_osids()

    def module_header(self, module):
        return '\"\"\"Unit tests of {0} {1}.\"\"\"\n'.format(self.package['name'],
                                                             module)
