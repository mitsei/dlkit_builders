import os
import glob
import json
import pprint
import shutil
import string
import datetime

from abcbinder_settings import ENCODING as utf_code
from binder_helpers import under_to_caps
from build_controller import Utilities, BaseBuilder
from config import sessions_to_implement, managers_to_implement,\
    objects_to_implement, variants_to_implement
from method_builders import MethodBuilder
from mappers import Mapper

from importlib import import_module


class InterfaceBuilder(Mapper, BaseBuilder, Utilities):
    """class that builds interfaces"""
    def __init__(self, method_class=None, root_dir=None, template_dir=None, *args, **kwargs):
        """method_class differentiates between different variations, i.e. abc
        looks different than mongo"""
        super(InterfaceBuilder, self).__init__()
        self._class = method_class or 'abc'
        self._ind = 4 * ' '
        self._dind = 2 * self._ind

        self._root_dir = root_dir
        self._template_dir = template_dir

        if root_dir is not None:
            self._make_dir(root_dir)
        if template_dir is not None:
            self._make_dir(template_dir)

        self.method_builder = MethodBuilder(method_class=self._class)

    def _get_class_inheritance(self, package, interface):
        def get_full_interface_class():
            return (self._abc_pkg_name(package['name'], abc=self._is('abc')) + '_' +
                    interface['category'] + '.' +
                    interface['shortname'])

        last_inheritance = []

        # Seed the inheritance list with this interface's abc_osid
        if package['name'] != 'osid' and interface['category'] == 'managers':
            inheritance = []
            last_inheritance = [get_full_interface_class()]
        else:
            inheritance = ['abc_' + get_full_interface_class()]

        # Iterate through any inherited interfaces and build the inheritance
        # list for this interface. Also, check if an import statement is
        # required and append to the appropriate module's import list.
        for i in interface['inheritance']:
            pkg_name = self._abc_pkg_name(i['pkg_name'], abc=self._is('abc'))
            unknown_module_protection = ''
            inherit_category = self.get_interface_module(i['pkg_name'], i['name'], True)
            if inherit_category == 'UNKNOWN_MODULE':
                unknown_module_protection = '\"\"\"'

            if (i['pkg_name'] == package['name'] and
                    inherit_category == interface['category']):
                inheritance.append(i['name'])
            else:
                inheritance.append(unknown_module_protection +
                                   pkg_name + '_' +
                                   inherit_category + '.' + i['name'] +
                                   unknown_module_protection)

        # Check to see if there are any additional inheritances required
        # by the implementation patterns.  THIS MAY WANT TO BE REDESIGNED
        # TO ALLOW INSERTING THE INHERITANCE IN A PARTICULAR ORDER.
        impl_class = load_impl_class(package['name'], interface['shortname'])
        if hasattr(impl_class, 'inheritance'):
            inheritance = inheritance + getattr(impl_class, 'inheritance')

        # Note that the following re-assigns the inheritance variable from a
        # list to a string.
        if last_inheritance:
            inheritance = inheritance + last_inheritance
        if inheritance:
            inheritance = '(' + ', '.join(inheritance) + ')'
        else:
            inheritance = ''

    # This function expects a file containing a json representation of an
    # osid package that was prepared by the mapper.
    def _make_osid(self, file_name):
        with open(file_name, 'r') as read_file:
            package = json.load(read_file)

        print "Building " + self._class + " osid for " + package['name']

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

        if self._root_dir is None:
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

        if self._is('abc'):
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
        with open(self._abc_module(package, 'summary_doc', abc=self._is('abc')), 'w') as write_file:
            write_file.write((utf_code + '\"\"\"' +
                              package['title'] + '\n' +
                              package['name'] + ' version ' +
                              package['version'] + '\n\n' +
                              package['summary'] + '\n\n\"\"\"').encode('utf-8') +
                             '\n')

        # Initialize the module doc and abc import string for each module
        for module in modules:
            if self._is('abc'):
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
            elif self._is('mongo'):
                docstr = '\"\"\"Mongodb implementations of ' + package['name'] + ' ' + module + '.\"\"\"\n'
                modules[module]['imports'].append(docstr)
                pylintstr = (
                    '# pylint: disable=no-init\n' +
                    '#     Numerous classes don\'t require __init__.\n' +
                    '# pylint: disable=too-many-public-methods,too-few-public-methods\n' +
                    '#     Number of methods are defined in specification\n' +
                    '# pylint: disable=protected-access\n' +
                    '#     Access to protected methods allowed in package mongo package scope\n' +
                    '# pylint: disable=too-many-ancestors\n' +
                    '#     Inheritance defined in specification\n')
                modules[module]['imports'].append(pylintstr)

        if self._is('mongo') and package['name'] in managers_to_implement:
            # Assemble and write profile.py file for this package.
            with open(self._abc_module(package, 'profile', abc=False), 'w') as write_file:
                write_file.write(self._make_profile_py(package))

        # The real work starts here.  Iterate through all interfaces to build
        # all the abc classes for this osid package.
        for interface in package['interfaces']:
            if self._is('mongo') and not build_this_interface(package, interface):
                continue  # don't build it

            if self._is('abc'):
                inheritance = ''
            else:
                inheritance = self._get_class_inheritance(package, interface)
            additional_methods = ''

            # Interate through any inherited interfaces and build the inheritance
            # list for this interface. Also, check if an import statement is
            # required and append to the appropriate module's import list.
            if not self._is('abc'):
                for i in interface['inheritance']:
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

    def _make_profile_py(self, package):
        """create the profile.py file for this package"""
        profile = {
            'VERSIONCOMPONENTS': [0, 1, 0],
            'RELEASEDATE': '',
            'SUPPORTS': []
        }
        old_supports = []
        osid_package = package['name']

        try:
            old_profile = import_module('.'.join(self._app_name(package['name']).split('/')[1:]) + '.' +
                                        self._abc_pkg_name(package['name'], abc=False) + '.profile', 'dlkit_project.builders')
        except ImportError:
            print 'Old Profile not found:', self._abc_pkg_name(package['name'], abc=False)
        else:
            if hasattr(old_profile, 'VERSIONCOMPONENTS'):
                profile['VERSIONCOMPONENTS'] = old_profile.VERSIONCOMPONENTS

            if hasattr(old_profile, 'SUPPORTS'):
                old_supports = old_profile.SUPPORTS

        profile['VERSIONCOMPONENTS'][2] += 1
        profile['RELEASEDATE'] = str(datetime.date.today())
        profile['SUPPORTS'].append('# Remove the # when implementations exist:',
                                   "#supports_journal_rollback",
                                   "#supports_journal_branching")

        # Find the Profile interface for this package
        if not any('OsidProfile' in i['inherit_shortnames'] for i in package['interfaces']):
            return ''
        else:
            profile_interface = [i for i in package['interfaces']
                                 if 'OsidProfile' in i['inherit_shortnames']][0]

        for method in profile_interface['methods']:
            if (len(method['args']) == 0 and
                    method['name'].startswith('supports_')):
                supports_str = ''
                # Check to see if support flagged in builder config OR
                # Check to see if someone activated support by hand
                if (under_to_caps(method['name'])[8:] + 'Session' in sessions_to_implement or
                        method['name'] in old_supports):
                    pass
                # Check to see if someone de-activated support by hand OR
                elif method['name'] not in old_supports:
                    supports_str += '#'
                else:  # Add check for session implementation flags here
                    supports_str += '#'

                supports_str += method['name']
                profile['SUPPORTS'].append(supports_str)

        profile = serialize(profile)

        try:
            from builders.mongoosid_templates import package_profile
            template = string.Template(package_profile.PROFILE_TEMPLATE)
        except (ImportError, AttributeError):
            return ''
        else:
            return template.substitute({'osid_package': osid_package,
                                        'version_str': profile['VERSIONCOMPONENTS'],
                                        'release_str': profile['RELEASEDATE'],
                                        'supports_str': profile['SUPPORTS']})

    def _patterns(self, package):
        # Get the pattern map for this osid package.
        with open(self._package_pattern_file(package), 'r') as read_file:
            return json.loads(read_file)

    def _template(self, directory):
        return self._template_dir + '/' + directory

    # This is the entry point for making the Python abstract base classes for
    # the osids. It processes all of the osids in the xosid directory, making
    # sure they have all been mapped to json, before sending each json file
    # off to be built into the abcosids.
    def make_osids(self, build_abc=False, re_index=False, re_map=False):
        if build_abc:
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
            self._make_osid(json_file)

        # Copy general config and primitive files, etc into the
        # implementation root directory:
        if os.path.exists(self._template('helpers')):
            for helper_file in glob.glob(self._template('helpers') + '/*.py'):
                shutil.copy(helper_file, self._root_dir)


def build_this_interface(package, interface):
    exceptions = ['ObjectiveHierarchySession',
                  'ObjectiveHierarchyDesignSession',
                  'ObjectiveSequencingSession',
                  'ObjectiveRequisiteSession',
                  'ObjectiveRequisiteAssignmentSession',]

    excepted_osid_categories = ['properties',
                                'query_inspectors',
                                'receivers',
                                'search_orders',
                                'searches',]

    # Check to see if manager should be implemented (this should
    # probably be moved to binder_helpers.flagged_for_implementation)
    if (interface['category'] == 'managers' and
            package['name'] not in managers_to_implement):
        return False

    # Check to see if this interface is meant to be implemented.
    if (package['name'] != 'osid' and
            interface['category'] not in excepted_osid_categories):
        if flagged_for_implementation(interface):
            if interface['shortname'] in exceptions:
                return False
            else:
                pass
        else:
            return False

    if interface['category'] in excepted_osid_categories:
        return False
    return True

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

def flagged_for_implementation(interface):
    """
    Check if this interface is meant to be implemented.

    """
    test = False
    if interface['category'] == 'managers':
        test = True
    elif (interface['category'] == 'sessions' and
            interface['shortname'] in sessions_to_implement):
        test = True
    elif interface['shortname'] in objects_to_implement:
        test = True
    else:
        for variant in variants_to_implement:
            if (interface['shortname'].endswith(variant) and
                    interface['shortname'][:-len(variant)] in objects_to_implement):
                test = True
    return test

def serialize(var_dict):
    """an attempt to make the builders more variable-based, instead of
    purely string based..."""
    return_dict = {}
    pp = pprint.PrettyPrinter(indent=4)

    for k, v in var_dict.iteritems():
        if isinstance(v, basestring):
            return_dict[k] = k + ' = ' + str(v)
        elif isinstance(v, list) and len(v) <= 3:  # this is stupid and horrible, I know
            return_dict[k] = k + ' = ' + str(v)
        elif isinstance(v, list) or isinstance(v, dict):
            return_dict[k] = k + ' = ' + pp.pprint(v)

    return return_dict

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
