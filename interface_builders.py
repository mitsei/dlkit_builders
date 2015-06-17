import os
import sys
import glob
import json
import pprint
import shutil
import string
import datetime

from abcbinder_settings import ENCODING as utf_code
from binder_helpers import under_to_caps, under_to_mixed,\
    remove_plural, camel_to_under, make_plural
from build_controller import Utilities, BaseBuilder, Templates
from config import sessions_to_implement, managers_to_implement,\
    objects_to_implement, variants_to_implement
from method_builders import MethodBuilder
from mappers import Mapper

from importlib import import_module


METADATA_INITER = """
        self._${data_name}_metadata = {
            'element_id': Id(
                self._authority,
                self._namespace,
                '${data_name}')}
        self._${data_name}_metadata.update(mdata_conf.${data_name_upper})"""


class InterfaceBuilder(Mapper, BaseBuilder, Templates, Utilities):
    """class that builds interfaces"""
    def __init__(self, method_class=None, root_dir=None, template_dir=None, *args, **kwargs):
        """method_class differentiates between different variations, i.e. abc
        looks different than mongo"""
        super(InterfaceBuilder, self).__init__(template_dir=template_dir)
        self._class = method_class or 'abc'
        self._ind = 4 * ' '
        self._dind = 2 * self._ind

        self._root_dir = root_dir

        if root_dir is not None:
            self._make_dir(root_dir)

        self.method_builder = MethodBuilder(method_class=self._class,
                                            template_dir=self._template_dir)

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
        impl_class = self._load_impl_class(package['name'], interface['shortname'])
        if hasattr(impl_class, 'inheritance'):
            inheritance = inheritance + getattr(impl_class, 'inheritance')

        # Note that the following re-assigns the inheritance variable from a
        # list to a string.
        if last_inheritance:
            inheritance = inheritance + last_inheritance
        if inheritance:
            inheritance = '({})'.format(', '.join(inheritance))
        else:
            inheritance = ''

        return inheritance

    def _get_extra_patterns(self, package, interface_name, import_statement, default=None):
        if interface_name + '.init_pattern' in self.patterns:
            init_pattern = self.patterns[interface_name + '.init_pattern']
            try:
                templates = import_module(self._package_templates(self.first(init_pattern)))
                if hasattr(templates, self.last(init_pattern)):
                    template_class = getattr(templates, self.last(init_pattern))
                    if hasattr(template_class, import_statement):
                        return getattr(template_class, import_statement)
            except ImportError:
                return default
        return default

    def _get_init_context(self, init_pattern, interface, package):
        """get the init context, for templating"""
        def init_string(name, init_type):
            return '\n{}osid_objects.{}._init_{}(self)'.format(self._dind,
                                                               name,
                                                               init_type)

        instance_initers = ''
        persisted_initers = ''
        metadata_initers = ''
        metadata_super_initers = ''
        map_super_initers = ''
        object_name = ''
        init_object = ''

        cat_name = self.patterns['package_catalog_caps']

        # Check for any special data initializations and call the appropriate makers
        # to assemble them.
        if init_pattern == 'resource.Bin':
            object_name = interface['shortname']
        elif init_pattern == 'resource.BinForm':
            object_name = interface['shortname'][:-4]
        elif init_pattern == 'resource.ResourceLookupSession':
            object_name = interface['shortname'][:-13]
        elif init_pattern == 'commenting.CommentLookupSession':
            object_name = interface['shortname'][:-13]
        elif init_pattern == 'resource.Resource':
            object_name = interface['shortname']
        elif init_pattern == 'resource.ResourceForm':
            object_name = interface['shortname'][:-4]
            if object_name in self.patterns['package_relationships_caps']:
                init_object = 'osid_objects.OsidRelationshipForm'
            else:
                init_object = 'osid_objects.OsidObjectForm'

            for inherit_object in interface['inherit_shortnames']:
                if inherit_object in ['OsidSourceableForm', 'OsidContainableForm']:
                    metadata_super_initers += init_string(inherit_object, 'metadata')
                    map_super_initers += init_string(inherit_object, 'map')

            if metadata_super_initers:
                metadata_super_initers += '\n'
            if map_super_initers:
                map_super_initers += '\n'
            try:
                persisted_initers = make_persistance_initers(
                    self.patterns[interface['shortname'][:-4] + '.persisted_data'],
                    self.patterns[interface['shortname'][:-4] + '.initialized_data'],
                    self.patterns[interface['shortname'][:-4] + '.aggregate_data'])
            except KeyError:
                pass

            try:
                metadata_initers = make_metadata_initers(
                    self.patterns[interface['shortname'][:-4] + '.persisted_data'],
                    self.patterns[interface['shortname'][:-4] + '.initialized_data'],
                    self.patterns[interface['shortname'][:-4] + '.return_types'])
            except KeyError:
                pass
        elif init_pattern == 'resource.ResourceQuery':
            object_name = interface['shortname'][:-5]

        return {'app_name': self._app_name(package['name']),
                'implpkg_name': self._abc_pkg_name(package['name'], abc=False),
                'pkg_name': package['name'],
                'pkg_name_upper': package['name'].upper(),
                'interface_name': interface['shortname'],
                'instance_initers': instance_initers,
                'persisted_initers': persisted_initers,
                'metadata_initers': metadata_initers,
                'metadata_super_initers': metadata_super_initers,
                'map_super_initers': map_super_initers,
                'object_name': object_name,
                'object_name_under': camel_to_under(object_name),
                'object_name_upper': camel_to_under(object_name).upper(),
                'cat_name': cat_name,
                'cat_name_plural': make_plural(cat_name),
                'cat_name_under': camel_to_under(cat_name),
                'cat_name_under_plural': make_plural(camel_to_under(cat_name)),
                'cat_name_upper': cat_name.upper(),
                'init_object': init_object}

    def _make_init_methods(self, package, interface):
        templates = None
        init_pattern = ''

        impl_class = self._load_impl_class(self._abc_pkg_name(package['name'], abc=False),
                                           interface['shortname'])
        if hasattr(impl_class, 'init'):
            return getattr(impl_class, 'init')
        elif interface['shortname'] + '.init_pattern' in self.patterns:
            init_pattern = self.patterns[interface['shortname'] + '.init_pattern']
            try:
                templates = import_module(self._package_templates(self.first(init_pattern)))
            except ImportError:
                pass

        if templates is not None and hasattr(templates, self.last(init_pattern)):
            template_class = getattr(templates, self.last(init_pattern))
            if hasattr(template_class, 'init_template'):
                context = self._get_init_context(init_pattern, interface, package)
                template = string.Template(getattr(template_class, 'init_template'))
                return template.substitute(context)

        return ''

    def _make_osid(self, file_name):
        # This function expects a file containing a json representation of an
        # osid package that was prepared by the mapper.
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
            self._make_dir(self._app_name(package), python=True)
            self._make_dir(self._abc_pkg_path(package), python=True)

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
            new_profile = self._make_profile_py(package)
            with open(self._abc_module(package, 'profile', abc=False), 'w') as write_file:
                write_file.write(new_profile)

        self.patterns = self._patterns(package)

        # The real work starts here.  Iterate through all interfaces to build
        # all the classes for this osid package.
        for interface in package['interfaces']:
            if self._is('mongo') and not build_this_interface(package, interface):
                continue  # don't build it

            if self._is('abc'):
                inheritance = ''
            else:
                inheritance = self._get_class_inheritance(package, interface)

            additional_methods = ''

            if not self._is('abc'):
                self._update_module_imports(modules, package, interface)

            if self._is('abc'):
                # Add the equality methods to Ids and Types:
                if interface['shortname'] == 'Id' or interface['shortname'] == 'Type':
                    additional_methods += eq_methods(interface['shortname'])
                    additional_methods += str_methods()
            else:
                # Look for additional methods defined in class patterns. These
                # need to be coded in the impl_class as a string with the
                # attribute name 'additional_methods_pattern'
                additional_methods += self._get_extra_patterns(package,
                                                               interface['shortname'],
                                                               'additional_methods_pattern',
                                                               default='')

                # Here we further inspect the impl_class to identify any additional
                # hand built methods to be included at the end of the class definition. These
                # need to be coded in the impl_class as a string with the
                # attribute name 'additional_methods'
                impl_class = self._impl_class(package, interface)
                if hasattr(impl_class, 'additional_methods'):
                    additional_methods += getattr(impl_class, 'additional_methods')

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

            if self._is('abc'):
                modules[interface['category']]['body'] = (
                    modules[interface['category']]['body'] +
                    class_sig + '\n' +
                    class_doc + '\n' +
                    '    __metaclass__ = abc.ABCMeta\n\n' +
                    additional_methods +
                    self.method_builder.make_methods(package['name'],
                                                     interface,
                                                     None) + '\n\n\n')
            else:
                init_methods = self._make_init_methods(package, interface)

                methods = self.method_builder.make_methods(self._abc_pkg_name(package['name'], abc=False),
                                                           interface,
                                                           self.patterns)

                if additional_methods:
                    methods += '\n' + additional_methods

                modules[interface['category']]['body'] += '{}\n{}\n{}\n{}\n\n\n'.format(class_sig,
                                                                                        class_doc,
                                                                                        init_methods,
                                                                                        methods)

        # Finally, iterate through the completed package module structure and
        # write out both the import statements and class definitions to the
        # appropriate module for this package.
        for module in modules:
            if module == 'records' and package['name'] != 'osid':
                module_name = 'record_templates'
            else:
                module_name = module

            if modules[module]['body'].strip() != '':
                with open(self._abc_module(package, module_name), 'wb') as write_file:
                    write_file.write(('\n'.join(order_module_imports(modules[module]['imports'])) +
                                      '\n\n\n' + modules[module]['body']).encode('utf-8'))

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
            # http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
            if self._root_dir not in sys.path:
                sys.path.insert(0, self._abs_path)
            profile_module = '{}.{}.{}.profile'.format(self.first(self._import_path(self._root_dir)),
                                                       self.last(self._import_path(self._root_dir)),
                                                       self._abc_pkg_name(package['name'], abc=False))
            old_profile = import_module(profile_module)
        except ImportError:
            print 'Old Profile not found:', self._abc_pkg_name(package['name'], abc=False)
        else:
            if hasattr(old_profile, 'VERSIONCOMPONENTS'):
                profile['VERSIONCOMPONENTS'] = old_profile.VERSIONCOMPONENTS

            if hasattr(old_profile, 'SUPPORTS'):
                old_supports = old_profile.SUPPORTS

        profile['VERSIONCOMPONENTS'][2] += 1
        profile['RELEASEDATE'] = str(datetime.date.today())
        profile['SUPPORTS'].extend(['# Remove the # when implementations exist:',
                                    "#supports_journal_rollback",
                                    "#supports_journal_branching"])

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
                profile['SUPPORTS'].append(str(supports_str))

        profile = serialize(profile)

        try:
            from mongoosid_templates import package_profile
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
            return json.load(read_file)

    def _update_module_imports(self, modules, package, interface):
        # And make sure there is a corresponding import statement for this
        # interface's abc_osid and associated module/category name.
        imports = modules[interface['category']]['imports']

        def append(import_str):
            if import_str not in imports:
                imports.append(import_str)

        def package_interface():
            return self._abc_pkg_name(package['name'] + '_' + interface['category'])

        if package['name'] != 'osid' and interface['category'] == 'managers':
            import_str = ('from dlkit.manager_impls.' +
                          self._abc_pkg_name(package) + ' import ' +
                          interface['category'] + ' as ' +
                          package_interface())
        else:
            import_str = ('from ' + self._app_name(package, abstract=True) + '.' +
                          self._abc_pkg_name(package) + ' import ' +
                          interface['category'] + ' as abc_' +
                          package_interface())

        append(import_str)

        # Iterate through any inherited interfaces and build the inheritance
        # list for this interface. Also, check if an import statement is
        # required and append to the appropriate module's import list.
        for i in interface['inheritance']:
            inherit_category = self.get_interface_module(i['pkg_name'], i['name'], True)
            if (i['pkg_name'] == package['name'] and
                  inherit_category == interface['category']):
                pass
            else:
                import_str = 'from {0}.{1} import {2} as {1}_{2}'.format(self._import_path(self._app_name(i['pkg_name'])),
                                                                         self._abc_pkg_name(i['pkg_name'], abc=False),
                                                                         inherit_category)

                if inherit_category != 'UNKNOWN_MODULE':
                    append(import_str)

        # Check to see if there are any additional inheritances required
        # by the implementation patterns.  THIS MAY WANT TO BE REDESIGNED
        # TO ALLOW INSERTING THE INHERITANCE IN A PARTICULAR ORDER.
        impl_class = self._impl_class(package, interface)
        # if hasattr(impl_class, 'inheritance_imports'):
        #     modules[interface['category']]['imports'] = (
        #         modules[interface['category']]['imports'] +
        #         getattr(impl_class, 'inheritance_imports'))

        ##
        # Here we further inspect the impl_class to identify any additional
        # hand built import statements to be loaded at the module level. These
        # need to be coded in the impl_class as a list of strings with the
        # attribute name 'import_statements'
        if hasattr(impl_class, 'import_statements'):
            for import_str in getattr(impl_class, 'import_statements'):
                append(import_str)

        ##
        # Look for module import statements defined in class patterns. These
        # need to be coded in the class pattern as a list of strings with the
        # attribute name 'import_statements_pattern'
        for import_str in self._get_extra_patterns(package,
                                                   interface['shortname'],
                                                   'import_statements_pattern',
                                                   default=[]):
            append(import_str)

        # add the none-argument check import if not already present
        append('from .. import utilities')


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

        if not self._is('abc'):
            # Copy general config and primitive files, etc into the
            # implementation root directory:
            if os.path.exists(self._template('helpers')):
                for helper_file in glob.glob(self._template('helpers') + '/*.py'):
                    shutil.copy(helper_file, self._root_dir)
        else:
            # copy over the abc_errors.py file to abstract_osid.osid.errors.py
            error_file = self._abs_path + '/builders/abc_errors.py'
            if os.path.exists(error_file):
                shutil.copyfile(error_file, self._root_dir + '/osid/errors.py')


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

# Assemble the initializers for metadata managed by Osid Object Forms
def make_metadata_initers(persisted_data, initialized_data, return_types):

    def default_string(name, default_type, is_list=False):
        dind = 8 * ' '
        if is_list:
            return '{0}self._{1}_default = self._{1}_metadata[\'default_{2}_values\']\n'.format(dind,
                                                                                                name,
                                                                                                default_type)
        else:
            return '{0}self._{1}_default = self._{1}_metadata[\'default_{2}_values\'][0]\n'.format(dind,
                                                                                                   name,
                                                                                                   default_type)

    imports = ''
    initer = ''
    default = ''
    for data_name in persisted_data:
        data_name_upper = data_name.upper()

        if (persisted_data[data_name] != 'OsidCatalog' and
                data_name not in initialized_data):
            template = string.Template(METADATA_INITER)
            if persisted_data[data_name] == 'boolean':
                default += '        self._{}_default = None\n'.format(data_name)
            elif (persisted_data[data_name] == 'string' and
                    return_types[data_name] == 'osid.locale.DisplayText'):
                default += '        self._{0}_default = ' \
                           'dict(self._{0}_metadata[\'default_string_values\'][0])\n'.format(data_name)
            elif persisted_data[data_name] == 'string':
                default += default_string(data_name, 'string')
            elif (persisted_data[data_name] == 'osid.id.Id' and
                    data_name not in initialized_data):
                default += default_string(data_name, 'id')
            elif persisted_data[data_name] == 'osid.id.Id[]':
                default += default_string(data_name, 'id', is_list=True)
            elif (persisted_data[data_name] == 'osid.type.Type' and
                    data_name not in initialized_data):
                default += default_string(data_name, 'type')
            elif persisted_data[data_name] == 'osid.type.Type[]':
                default += default_string(data_name, 'type', is_list=True)
            elif persisted_data[data_name] in ['osid.calendaring.DateTime', 'timestamp']:
                default += default_string(data_name, 'date_time')
            elif persisted_data[data_name] == 'osid.calendaring.Duration':
                default += default_string(data_name, 'duration')
            elif persisted_data[data_name] == 'osid.transport.DataInputStream':
                default += default_string(data_name, 'object')
            elif persisted_data[data_name] == 'osid.mapping.SpatialUnit':
                pass  # Put SpatialUnit initters here
            elif persisted_data[data_name] == 'decimal':
                default += default_string(data_name, 'decimal')

            initer += template.substitute({'data_name': data_name,
                                           'data_name_upper': data_name_upper})
    if initer:
        initer += '\n'
    if default:
        default += '\n'
    return imports + initer + default

# Assemble the initializers for persistance data managed by Osid Object Forms
# initialized with the form.
def make_persistance_initers(persisted_data, initialized_data, aggregate_data):
    initers = ''

    singular_data_types = ['osid.id.Id', 'osid.type.Type', 'string', 'decimal',
                           'boolean', 'OsidCatalog', 'osid.calendaring.DateTime',
                           'timestamp','osid.calendaring.Duration',
                           'osid.transport.DataInputStream']

    append_ids = ['osid.id.Id', 'osid.type.Type']

    plural_data_types = ['osid.id.Id[]', 'osid.type.Type[]']

    for data_name in persisted_data:
        mixed_name = under_to_mixed(data_name)
        mixed_singular = under_to_mixed(remove_plural(data_name))

        persisted_name = persisted_data[data_name]

        if ((persisted_name == 'osid.id.Id' or
                persisted_name == 'OsidCatalog') and
                data_name in initialized_data):
            initers += '        self._my_map[\'{}Id\'] = str(kwargs[\'{}_id\'])\n'.format(mixed_name,
                                                                                          data_name)
        elif (persisted_name == 'osid.resource.Resource' and
                data_name in initialized_data):
            initers += '        self._my_map[\'{}Id\'] = str(kwargs[\'effective_agent_id\'])\n'.format(mixed_name)
        elif persisted_name in singular_data_types:
            if persisted_name in append_ids:
                initers += '        self._my_map[\'{}Id\'] = self._{}_default\n'.format(mixed_name,
                                                                                        data_name)
            else:
                initers += '        self._my_map[\'{}\'] = self._{}_default\n'.format(mixed_name,
                                                                                        data_name)
        elif persisted_name in plural_data_types:
            initers += '        self._my_map[\'{}Ids\'] = self._{}_default\n'.format(mixed_singular,
                                                                                     data_name)

    for data_name in aggregate_data:
        mixed_name = under_to_mixed(data_name)
        if aggregate_data[data_name].endswith('List'):
            initers += '        self._my_map[\'{}\'] = []\n'.format(mixed_name)
        else:
            initers += '        self._my_map[\'{}\'] = None\n'.format(mixed_name)


    initialize_to_none = ['boolean', 'osid.calendaring.DateTime', 'timestamp',
                          'osid.calendaring.Duration']
    initialize_to_empty_string = ['decimal', 'cardinal', 'string']

    for data_name in initialized_data:
        mixed_name = under_to_mixed(data_name)

        if data_name in persisted_data:
            pass
        elif initialized_data[data_name] in initialize_to_none:
            initers += '        self._my_map[\'{}\'] = None\n'.format(mixed_name)
        elif initialized_data[data_name] in initialize_to_empty_string:
            initers += '        self._my_map[\'{}\'] = \'\'\n'.format(mixed_name)
        elif initialized_data[data_name] == 'osid.locale.DisplayText':
            initers += (
                '        self._my_map[\'{}\'] = {\n' +
                '            \'text\': \'\',\n' +
                '            \'languageTypeId\': str(default_language_type),\n' +
                '            \'scriptTypeId\': str(default_script_type),\n' +
                '            \'formatTypeId\': str(default_format_type),\n' +
                '        }\n').format(mixed_name)
        elif initialized_data[data_name] == 'osid.id.Id':
            initers += '        self._my_map[\'{}Id\'] = \'\'\n'.format(mixed_name)
        elif initialized_data[data_name] == 'osid.id.Id[]':
            initers += '        self._my_map[\'{}Id\'] = []\n'.format(mixed_name)

    return initers

def order_module_imports(imports):
    # does not separate built-in libraries from third-party libraries
    docstrings = [imp for imp in imports if '"""' in imp or imp.startswith('#')]
    full_imports = [imp for imp in imports if imp.startswith('import ')]
    local_imports = [imp for imp in imports if imp.startswith('from .') or imp.startswith('from dlkit')]
    constants = [imp for imp in imports if 'import' not in imp and imp not in docstrings]
    partial_third_party_imports = [imp for imp in imports
                                   if imp not in full_imports and
                                   imp not in local_imports and
                                   imp not in constants and
                                   imp not in docstrings and
                                   imp.strip() != '']

    newline = ['\n']

    full_imports.sort()
    local_imports.sort()
    partial_third_party_imports.sort()

    return docstrings + newline + full_imports + newline + partial_third_party_imports + newline + local_imports + newline + constants


def serialize(var_dict):
    """an attempt to make the builders more variable-based, instead of
    purely string based..."""
    return_dict = {}
    ppr = pprint.PrettyPrinter(indent=4)

    for k, v in var_dict.iteritems():
        if isinstance(v, basestring):
            return_dict[k] = k + ' = ' + str(v)
        elif isinstance(v, list) and len(v) <= 3:  # this is stupid and horrible, I know
            return_dict[k] = k + ' = ' + str(v)
        elif isinstance(v, list) or isinstance(v, dict):
            return_dict[k] = k + ' = ' + ppr.pformat(v)

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
