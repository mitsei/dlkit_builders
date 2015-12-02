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

    def build_this_interface(self, interface):
        return self._build_this_interface(interface)

    def class_sign(self, interface, inheritance):
        return 'class Test{}{}:'.format(interface['shortname'],
                                        inheritance)

    def make(self):
        self.make_osids()

    def module_header(self, module):
        return '\"\"\"Unit tests of {0} {1}.\"\"\"\n'.format(self.package['name'],
                                                             module)
