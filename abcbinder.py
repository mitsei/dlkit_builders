import os
import json
import glob

from abcbinder_settings import ENCODING as utf_code

from method_builders import MethodBuilder
from build_controller import BaseBuilder
from mappers import Mapper

# These next two are here for the purpose of loading abc modules
# in a django app, where the goal is to distribute the abc osids
# across the service kit packages.
# from djbuilder_settings import APPNAMEPREFIX as app_prefix
# from djbuilder_settings import APPNAMESUFFIX as app_suffix

INCLUDE_INHERITANCE = False


class ABCBuilder(Mapper, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(ABCBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path

        self.method_builder = MethodBuilder(method_class='abc')

        self._abc_dir = build_dir + '/abstract_osids'
        self._app_prefix = ''
        self._abc_prefix = ''
        self._app_suffix = ''
        self._abc_suffix = ''
        self._make_dir(self._abc_dir)

    # The following functions return the app name and module name strings
    # by prepending and appending the appropriate suffixes and prefixes. Note
    # that the django app_name() function is included to support building of
    # the abc osids into a Django project environment.
    def _abc_pkg_name(self, string):
        return self._abc_prefix + '_'.join(string.split('.')) + self._abc_suffix

    def _app_name(self, package):
        if self._abc_dir:
            return self._abc_dir
        else:
            return self._app_prefix + package['name'] + self._app_suffix

    def _abc_module(self, package, module):
        return self._abc_pkg_path(package) + '/' + module + '.py'

    def _abc_pkg_path(self, package):
        return self._app_name(package) + '/' + self._abc_pkg_name(package['name'])

    # This function expects a file containing a json representation of an
    # osid package that was prepared by the mapper.
    def _make_abcosid(self, file_name):
        with open(file_name, 'r') as read_file:
            package = json.load(read_file)

        print "Building ABC osid for " + package['name']

        # The map structure for the modules to be created by this function.
        # Each module will get a body string that holds the class and method
        # signatures for the particular interface category, and a list of
        # for the modules that the module's classes may inherit.
        modules = dict(properties=dict(imports=[], body=''),
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

        if self._abc_dir is None:
            ##
            # Check if an app directory and abc osid subdirectory already exist.
            # If not, create them  This code specifically splits out the osid
            # packages in a Django app environment.  For other Python based
            # implementations try using the subsequent, more generic code instead.
            from django.core.management import call_command
            if not os.path.exists(self._app_name(package)):
                call_command('startapp', self._app_name(package))
            if not os.path.exists(self._app_name(package) + '/' +
                                  self._abc_pkg_name(package['name'])):
                os.system('mkdir '+ self._app_name(package) + '/' +
                          self._abc_pkg_name(package['name']))
                os.system('touch ' + self._app_name(package) + '/' +
                          self._abc_pkg_name(package['name']) + '/__init__.py')
        else:
            # Check if a directory already exists for the abc osid.  If not,
            # create one and initialize as a python package.
            self._make_dir(self._app_name(package))
            os.system('touch ' + self._app_name(package) + '/__init__.py')
            abc_path = self._abc_pkg_path(package)
            self._make_dir(abc_path)
            os.system('touch ' + abc_path + '/__init__.py')

        # Write the osid license documentation file.
        with open(self._abc_module(package, 'license'), 'w') as write_file:
            write_file.write((utf_code + '\"\"\"' +
                              package['title'] + '\n' +
                              package['name'] + ' version ' +
                              package['version'] + '\n\n' +
                              package['copyright'] + '\n\n' +
                              package['license'] + '\n\n\"\"\"').encode('utf-8') +
                             '\n')

        # Write the summary documentation for this package.
        with open(self._abc_module(package, 'doc'), 'w') as write_file:
            write_file.write((utf_code + '\"\"\"' +
                              package['title'] + '\n' +
                              package['name'] + ' version ' +
                              package['version'] + '\n\n' +
                              package['summary'] + '\n\n\"\"\"').encode('utf-8') +
                             '\n')

        # Initialize the module doc and abc import string for each module
        for module in modules:
            docstr = ('\"\"\"Implementations of ' + package['name'] +
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
                      '#     All apparent duplicates have been inspected. They aren\'t.\n')
            modules[module]['imports'].append(docstr)
            modules[module]['imports'].append('import abc')

        # The real work starts here.  Iterate through all interfaces to build
        # all the abc classes for this osid package.
        for interface in package['interfaces']:
            inheritance = []
            additional_methods = ''

            # Interate through any inherited interfaces and build the inheritance
            # list for this interface. Also, check if an import statement is
            # required and append to the appropriate module's import list.
            for i in interface['inheritance']:
                if not INCLUDE_INHERITANCE:
                    break
                unknown_module_protection = ''
                inherit_category = self.get_interface_module(i['pkg_name'], i['name'], True)
                if inherit_category == 'UNKNOWN_MODULE':
                    unknown_module_protection = '\"\"\"'
                if (i['pkg_name'] == package['name'] and
                        inherit_category == interface['category']):
                    inheritance.append(i['name'])
                else:
                    inheritance.append(unknown_module_protection +
                                       self._abc_pkg_name(i['pkg_name']) + '_' +
                                       inherit_category + '.' + i['name'] +
                                       unknown_module_protection)
                    import_str = ('from ..' + self._abc_pkg_name(i['pkg_name']) +
                                  ' import ' + inherit_category + ' as ' +
                                  self._abc_pkg_name(i['pkg_name']) + '_' + inherit_category)
                    if (import_str not in modules[interface['category']]['imports'] and
                            inherit_category != 'UNKNOWN_MODULE'):
                        modules[interface['category']]['imports'].append(import_str)

            # Note that the following re-assigns the inheritance variable from a
            # list to a string.
            if inheritance:
                inheritance = '(' + ', '.join(inheritance) + ')'
            else:
                inheritance = ''

            # Add the equality methods to Ids and Types:
            if interface['shortname'] == 'Id' or interface['shortname'] == 'Type':
                additional_methods += eq_methods(interface['shortname'])
                additional_methods += str_methods()

            # Inspect the class doc string for headline + body and create
            # appropriate doc string style. Trying to conform to PEP 257 as
            # much as the source osid doc will allow.
            if interface['doc']['body'].strip() == '':
                class_doc = ('    \"\"\"' +
                             self._wrap(interface['doc']['headline']) +
                             '\"\"\"')
            else:
                class_doc = ('    \"\"\"' +
                             self._wrap(interface['doc']['headline']) +
                             '\n\n' +
                             self._wrap(interface['doc']['body']) +
                             '\n\n    \"\"\"')

            class_sig = 'class ' + interface['shortname'] + inheritance + ':'

            modules[interface['category']]['body'] = (
                modules[interface['category']]['body'] +
                class_sig + '\n' +
                class_doc + '\n' +
                '    __metaclass__ = abc.ABCMeta\n\n' +
                additional_methods +
                self.method_builder.make_methods(package['name'],
                                                 interface,
                                                 None) + '\n\n\n')

        # Finally, iterate through the completed package module structure and
        # write out both the import statements and class definitions to the
        # appropriate module for this package.
        for module in modules:
            if modules[module]['body'].strip() != '':
                with open(self._abc_module(package, module), 'w') as write_file:
                    write_file.write(('\n'.join(modules[module]['imports']) + '\n\n\n' +
                                      modules[module]['body']).encode('utf-8'))

    # This is the entry point for making the Python abstract base classes for
    # the osids. It processes all of the osids in the xosid directory, making
    # sure they have all been mapped to json, before sending each json file
    # off to be built into the abcosids.
    def make_abcosids(self, re_index=False, re_map=False):
        for xosid_file in glob.glob(self.xosid_dir + '/*' + self.xosid_ext):
            package = None
            if (not os.path.exists(self._package_file(self.grab_osid_name(xosid_file)) or
                    re_map)):
                print 'mapping', self.grab_osid_name(xosid_file), 'osid.'
                package = self.make_xosid_map(xosid_file)
            if (not os.path.exists(self._package_interface_file(self.grab_osid_name(xosid_file))) or
                    re_index):
                print 'indexing interfaces for', self.grab_osid_name(xosid_file), 'osid.'
                self.make_interface_map(xosid_file, package)

        for json_file in glob.glob(self.package_maps + '/*.json'):
            self._make_abcosid(json_file)

def eq_methods(interface_name):
    return (
"""    def __eq__(self, other):
        if isinstance(other, """ + interface_name + """):
            return (
                self.get_authority() == other.get_authority() and
                self.get_identifier_namespace() == other.get_identifier_namespace() and
                self.get_identifier() == other.get_identifier()
            )
        return NotImplemented()

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

""")

def str_methods():
    return (
"""    def __str__(self):
        \"\"\"Provides serialized version of Id\"\"\"
        return self._escape(self._escape(self.get_identifier_namespace()) + ':' +
                            self._escape(self.get_identifier()) + '@' +
                            self._escape(self.get_authority()))

    def _escape(self, string):
        \"\"\"Private method for escaping : and @\"\"\"
        return string.replace("%", "%25").replace(":", "%3A").replace("@", "%40")

    def _unescape(self, string):
        \"\"\"Private method for un-escaping : and @\"\"\"
        return string.replace("%40", "@").replace("%3A", ":").replace("%25", "%")

""")
