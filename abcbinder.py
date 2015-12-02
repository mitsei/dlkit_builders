from build_controller import BaseBuilder
from interface_builders import InterfaceBuilder
from mappers import Mapper

# These next two are here for the purpose of loading abc modules
# in a django app, where the goal is to distribute the abc osids
# across the service kit packages.
# from djbuilder_settings import APPNAMEPREFIX as app_prefix
# from djbuilder_settings import APPNAMESUFFIX as app_suffix


class ABCBuilder(InterfaceBuilder, Mapper, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(ABCBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path

        self._root_dir = build_dir + '/abstract_osid'
        self._make_dir(self._root_dir)

        self._class = 'abc'

        # self.interface_builder = InterfaceBuilder('abc',
        #                                           self._root_dir)

    def make(self):
        self.make_osids(build_abc=True)

    def module_header(self, module):
        return ('\"\"\"Implementations of ' + self.package['name'] +
                ' abstract base class ' + module + '.\"\"\"\n' +
                '# pylint: disable=invalid-name\n' +
                '#     Method names comply with OSID specification.\n' +
                '# pylint: disable=no-init\n' +
                '#     Abstract classes do not define __init__.\n' +
                '# pylint: disable=too-few-public-methods\n' +
                '#     Some interfaces are specified as \'markers\' and include no methods.\n' +
                '# pylint: disable=too-many-public-methods\n' +
                '#     Number of methods are defined in specification\n' +
                '# pylint: disable=too-many-ancestors\n' +
                '#     Inheritance defined in specification\n' +
                '# pylint: disable=too-many-arguments\n' +
                '#     Argument signature defined in specification.\n' +
                '# pylint: disable=duplicate-code\n' +
                '#     All apparent duplicates have been inspected. They aren\'t.\n' +
                'import abc\n')

    def write_license_file(self):
        with open(self._abc_module('license'), 'w') as write_file:
            write_file.write((self._utf_code + '\"\"\"' +
                              self.package['title'] + '\n' +
                              self.package['name'] + ' version ' +
                              self.package['version'] + '\n\n' +
                              self.package['copyright'] + '\n\n' +
                              self.package['license'] + '\n\n\"\"\"').encode('utf-8') +
                             '\n')



