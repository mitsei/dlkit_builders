import json
import glob
import os

from xosid_mapper import XOsidMapper
from collections import OrderedDict

from build_controller import BaseBuilder


class Mapper(XOsidMapper, BaseBuilder):
    def __init__(self, xosid_dir='xosid', xosid_ext='.xosid', *args, **kwargs):
        super(Mapper, self).__init__(*args, **kwargs)

        self._xosid_dir = None
        self._xosid_ext = None

        self.xosid_dir = xosid_dir
        self.xosid_ext = xosid_ext

    @property
    def xosid_dir(self):
        return self._xosid_dir

    @property
    def xosid_ext(self):
        return self._xosid_ext

    @xosid_dir.setter
    def xosid_dir(self, xosid_dir):
        if self._abs_path not in xosid_dir:
            xosid_dir = os.path.join(self._abs_path, xosid_dir)
        self._xosid_dir = xosid_dir

    @xosid_ext.setter
    def xosid_ext(self, xosid_ext):
        self._xosid_ext = xosid_ext

    def map_all(self, map_type='all'):
        make_package_keywords = ['all', 'interface', 'i']
        make_interface_keywords = ['all', 'package', 'pkg', 'p']
        make_impl_pattern_keywords = ['all', 'impl', 'patterns']
        package = None
        for xosid_file in glob.glob(self.xosid_dir + '/*' + self.xosid_ext):
            if map_type in make_package_keywords:
                print('mapping osid package {0}.'.format(self.grab_osid_name(xosid_file)))
                package = self.make_xosid_map(xosid_file)
            if map_type in make_interface_keywords:
                print('creating interface map for {0} osid.'.format(self.grab_osid_name(xosid_file)))
                self.make_interface_map(xosid_file, package)
            if map_type in make_impl_pattern_keywords:
                print('creating implementation pattern map for {0} osid.'.format(self.grab_osid_name(xosid_file)))
                self.make_interface_map(xosid_file, package)

    def make_xosid_map(self, file_name):
        package = self.map_xosid(file_name)
        with open(self._package_file(package), 'w') as write_file:
            json.dump(package, write_file, indent=3)
        return package

    def make_interface_map(self, file_name=None, package=None):
        if package is None:
            package = self.map_xosid(file_name)
        osid_type_index = OrderedDict()
        if package is not None:
            pkg_name = self._abc_pkg_name(package_name=package['name'],
                                          abc=False)
            for i in package['interfaces']:
                osid_type_index[pkg_name + '.' + i['shortname']] = i['category']
                if i['category'] == 'others_please_move':
                    print('Please move: ' + i['fullname'])
            with open(self._package_interface_file(pkg_name), 'w') as write_file:
                json.dump(osid_type_index, write_file, indent=3)
        else:
            print('No OSID package available.')
        return osid_type_index
