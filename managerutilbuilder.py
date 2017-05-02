import json
import glob

from build_dlkit import BaseBuilder
from config import managers_to_implement
from interface_builders import InterfaceBuilder


class ManagerUtilBuilder(InterfaceBuilder, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(ManagerUtilBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir + '/manager_impls'
        self._template_dir = self._abs_path + '/managerutil_templates'

        self._class = 'manager'

    def _get_method_args(self, method, interface):
        args = ['self']
        args += ['{0}=None'.format(a['var_name'].strip()) for a in method['args']]
        return args

    def _get_method_sig(self, method, interface):
        args = self._get_method_args(method, interface)
        method_sig = '{}def {}({}):'.format(self._ind,
                                            method['name'],
                                            ', '.join(args))
        return method_sig

    def _get_sub_package_imports(self, interface):
        # get the imports from sub-packages
        sub_package_imports = []
        current_package = self.package['name']

        for json_file in glob.glob(self._package_directory()):
            sub_package_prefix = '{}_'.format(current_package)
            if sub_package_prefix in json_file:
                with open(json_file, 'r') as read_file:
                    sub_package = json.load(read_file)
                    # for inf in sub_package['interfaces']:
                    #     self.patterns = self._update_patterns_with_manager_catalog_flags(self.patterns,
                    #                                                                      inf,
                    #                                                                      sub_package)

                    # need to update self.patterns with the new subpackage patterns
                    # this is OK here because it assumes that the main package has already been constructed
                    pattern_file = self._package_pattern_file(package=sub_package)
                    with open(pattern_file, 'r') as sub_package_patterns:
                        self.patterns.update(json.load(sub_package_patterns))

                    # for sub_inf in sub_package['interfaces']:
                    #     if self._is_matching_interface(interface, sub_inf):
                    #         self._append_pattern_imports(sub_package_imports, sub_inf)

        return sub_package_imports

    def _package_directory(self):
        if self.package_maps[-1] != '/':
            directory = self.package_maps + '/*.json'
        else:
            directory = self.package_maps + '*.json'

        return directory

    def _update_module_imports(self, modules, interface):
        imports = modules[interface['category']]['imports']

        self.append(imports, self._abc_package_imports(interface))
        self._append_inherited_imports(imports, interface)
        self._append_pattern_imports(imports, interface)

        # Don't forget the OsidSession inheritance:
        # if (('OsidManager' in interface['inherit_shortnames'] or
        #         interface['shortname'] == self.patterns['package_catalog_caps']) and
        #         self.package['name'] != 'osid'):
        #     self.append(imports, 'from . import osid')

        # And don't forget the osid_error import:
        # import_str = 'from ..osid.osid_errors import NullArgument, Unimplemented'
        # self.append(imports, import_str)

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

    def build_this_interface(self, interface):
        # Check to see if interface should be implemented
        if (interface['category'] == 'managers' and
                self.package['name'] in managers_to_implement):
            pass
        elif interface['shortname'] in ['OsidList', 'TypeList', 'Sourceable']:
            pass
        else:
            return False
        return True

    def make(self):
        self.make_osids()

    def module_header(self, module):
        return """\"\"\"Manager utility implementations of {0} {1}.\"\"\"
# pylint: disable=no-init
#     Numerous classes don\'t require __init__.
# pylint: disable=too-many-public-methods
#     Number of methods are defined in specification
# pylint: disable=too-many-ancestors
#     Inheritance defined in specification""".format(self.package['name'],
                                                     module)
