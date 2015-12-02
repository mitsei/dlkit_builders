from build_controller import BaseBuilder
from interface_builders import InterfaceBuilder


class AZBuilder(InterfaceBuilder, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(AZBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir + '/authz_adapter'
        self._template_dir = self._abs_path + '/builders/azosid_templates'

        self._class = 'authz'

        # self.interface_builder = InterfaceBuilder('authz',
        #                                           self._root_dir,
        #                                           self._template_dir)

    def build_this_interface(self, interface):
        return (self.package['name'] in ['proxy'] or not
                (interface['category'] in ['sessions', 'managers'] or
                interface['shortname'] in ['Sourceable']))

    def make(self):
        self.make_osids()

    def module_header(self, module):
        return ('\"\"\"AuthZ Adapter implementations of ' + self.package['name'] + ' ' + module + '.\"\"\"\n' +
                '# pylint: disable=no-init\n' +
                '#     Numerous classes don\'t require __init__.\n' +
                '# pylint: disable=too-many-public-methods\n' +
                '#     Number of methods are defined in specification\n' +
                '# pylint: disable=too-many-ancestors\n' +
                '#     Inheritance defined in specification\n')
