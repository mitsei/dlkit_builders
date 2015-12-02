""" general controller for building things. Makes the builders configurable and
executable from the command line, not necessarily a Python shell.

Packages to build is read-in from config.py
"""
import os
import sys
import json
import glob
import string
import textwrap

from collections import OrderedDict
from importlib import import_module

from binder_helpers import camel_to_under
from config import sessions_to_implement, managers_to_implement,\
    objects_to_implement, variants_to_implement

from pattern_mapper import map_patterns
from xosid_mapper import XOsidMapper

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
ABS_PATH = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir))


def remove_abs_path(path):
    local_template_dir = path.replace(ABS_PATH, '')
    if local_template_dir[0] == '/':
        local_template_dir = local_template_dir[1::]
    return local_template_dir


class Utilities(object):
    def _make_dir(self, target_dir, python=False):
        if ABS_PATH not in target_dir:
            target_dir = (ABS_PATH + target_dir).replace('//', '/')
        if target_dir[-1] == '/':
            target_dir = target_dir[0:-1]
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        if python:
            os.system('touch ' + target_dir + '/__init__.py')
            # for every directory between ABS_PATH and target_dir, add __init__.py
            intermediate_dirs = target_dir.replace(ABS_PATH, '').split('/')
            start_dir = ABS_PATH + '/'
            for dir_ in intermediate_dirs:
                start_dir += dir_ + '/'
                if not os.path.exists(start_dir + '__init__.py'):
                    os.system('touch ' + start_dir + '__init__.py')
        return target_dir

    def _wrap(self, text):
        result = []
        wrapper = textwrap.TextWrapper(subsequent_indent=8*' ', width=120)
        for line in text.splitlines():
            result.append('\n'.join(wrapper.wrap(line)))
        return '\n'.join(result)

    def append(self, iterator, item):
        if item not in iterator:
            iterator.append(item)

    def first(self, package_path, char='.'):
        """a lot of builder patterns refer to the first item in a
        dot-separated path"""
        return package_path.split(char)[0]

    def last(self, package_path, char='.'):
        """a lot of builder patterns refer to the last item in a
        dot-separated path"""
        return package_path.split(char)[-1]


class BaseBuilder(Utilities):
    """base builder with some shared items, like package_maps dir, etc."""
    def __init__(self,
                 package_maps_dir='/builders/package_maps',
                 pattern_maps_dir='/builders/pattern_maps',
                 interface_maps_dir='/builders/interface_maps',
                 *args, **kwargs):
        self._package_maps_dir = None
        self._pattern_maps_dir = None
        self._interface_maps_dir = None
        self._map_ext = '.json'
        self._abs_path = ABS_PATH
        self.package = None

        self._app_prefix = ''
        self._abc_prefix = ''
        self._pkg_prefix = ''
        self._app_suffix = ''
        self._abc_suffix = ''
        self._pkg_suffix = ''
        self._root_dir = None
        self._class = None
        self._utf_code = '# -*- coding: utf-8 -*-\n'

        self.package_maps = package_maps_dir
        self.pattern_maps = pattern_maps_dir
        self.interface_maps = interface_maps_dir
        super(BaseBuilder, self).__init__(*args, **kwargs)

    # The following functions return the app name and module name strings
    # by prepending and appending the appropriate suffixes and prefixes. Note
    # that the django app_name() function is included to support building of
    # the abc osids into a Django project environment.
    def _abc_pkg_name(self, abc=True, package_name=None):
        if package_name is None:
            package_name = self.package['name']

        if abc:
            return self._abc_prefix + '_'.join(package_name.split('.')) + self._abc_suffix
        else:
            return self._pkg_prefix + '_'.join(package_name.split('.')) + self._pkg_suffix

    def _app_name(self, abstract=False, package_name=None):
        if package_name is None:
            package_name = self.package['name']
        if abstract:
            if self._is('services'):
                return '..abstract_osid'
            else:
                return '...abstract_osid'
        elif self._root_dir is not None:
            return self._root_dir
        else:
            return self._app_prefix + package_name + self._app_suffix

    def _abc_module(self, module, abc=True, test=False, extension='py'):
        if test:
            return '{0}/test_{1}.{2}'.format(self._abc_pkg_path(abc),
                                             module,
                                             extension)
        else:
            return '{0}/{1}.{2}'.format(self._abc_pkg_path(abc),
                                        module,
                                        extension)

    def _abc_pkg_path(self, abc=True):
        return self._app_name() + '/' + self._abc_pkg_name(abc)

    def _build_this_interface(self, interface):
        exceptions = []
        excepted_osid_categories = ['properties',
                                    'query_inspectors',
                                    'receivers']

        # Check to see if manager should be implemented (this should
        # probably be moved to binder_helpers.flagged_for_implementation)
        if (interface['category'] == 'managers' and
                self.package['name'] not in managers_to_implement):
            return False

        # Check to see if this interface is meant to be implemented.
        if (self.package['name'] != 'osid' and
                interface['category'] not in excepted_osid_categories):
            if self._flagged_for_implementation(interface):
                if interface['shortname'] in exceptions:
                    return False
            else:
                return False

        if interface['category'] in excepted_osid_categories:
            return False

        return True

    def _empty_modules_dict(self):
        return dict(manager=dict(imports=[], body=''),  # for kitosids only
                    catalog=dict(imports=[], body=''),  # for kitosids only
                    properties=dict(imports=[], body=''),
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

    def _flagged_for_implementation(self, interface):
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

    def _import_path(self, path, limited=True):
        if limited:
            return '.'.join(remove_abs_path(path).split('/')[-2::])
        else:
            return '.'.join(remove_abs_path(path).split('/'))

    def _in(self, desired_types_list):
        return self._class in desired_types_list

    def _is(self, desired_type):
        return self._class == str(desired_type)

    # Determine if the interface represents a catalog related session
    def _is_catalog_session(self, interface, patterns, package_name):
        is_catalog_session = False
        if package_name in ['type', 'proxy']:
            is_catalog_session = False
        elif (interface['category'] == 'sessions' and
                interface['shortname'].startswith('GradebookColumn')):
            is_catalog_session = True
        elif (interface['category'] == 'sessions' and
                interface['shortname'].endswith(patterns['package_catalog_caps'] + 'Session')):
            is_catalog_session = False
        elif (interface['category'] == 'sessions' and
                interface['shortname'].endswith(patterns['package_catalog_caps'] + 'AssignmentSession')):
            is_catalog_session = False
        elif (interface['category'] == 'sessions' and
                not interface['shortname'].startswith(patterns['package_catalog_caps'])):
            is_catalog_session = True
        return is_catalog_session

    # Determine if the interface represents a manager related session
    def _is_manager_session(self, interface, patterns, package_name):
        is_manager_session = False
        if package_name in ['type', 'proxy'] and interface['category'] == 'sessions':
            is_manager_session = True
        elif (interface['category'] == 'sessions' and
                interface['shortname'].startswith('GradebookColumn')):
            is_manager_session = False
        elif (interface['category'] == 'sessions' and
                interface['shortname'].endswith(patterns['package_catalog_caps'] + 'Session')):
            is_manager_session = True
        elif (interface['category'] == 'sessions' and
                interface['shortname'].endswith(patterns['package_catalog_caps'] + 'AssignmentSession')):
            is_manager_session = True
        elif (interface['category'] == 'sessions' and
                interface['shortname'].startswith(patterns['package_catalog_caps'])):
            is_manager_session = True
        return is_manager_session

    def _is_session(self, interface, type_):
        return '{}.is_{}_session'.format(camel_to_under(interface['shortname']),
                                         type_)

    def _load_patterns_file(self):
        # Get the pattern map for this osid package.
        with open(self._package_pattern_file(), 'r') as read_file:
            return json.load(read_file)

    def _package_file(self, package):
        if isinstance(package, dict) and 'name' in package:
            return self.package_maps + '/' + self.first(package['name']) + self._map_ext
        else:
            return self.package_maps + '/' + package + self._map_ext

    def _package_interface_file(self, package):
        if isinstance(package, dict) and 'name' in package:
            return self.interface_maps + '/' + self.first(package['name']) + self._map_ext
        else:
            # assume is package name string
            return self.interface_maps + '/' + package + self._map_ext

    def _package_pattern_file(self, package=None):
        if package is None:
            package = self.package

        if isinstance(package, dict):
            return self.pattern_maps + '/' + self.first(package['name']) + self._map_ext
        else:
            return self.pattern_maps + '/' + package + self._map_ext

    def _pattern_map_exists(self, package):
        return self.first(package['name']) + self._map_ext in os.listdir(self.pattern_maps)

    def _patterns(self):
        # Get the pattern map for this osid package.
        return self._load_patterns_file()

    def build_this_interface(self, interface):
        pass

    def class_sig(self, interface, inheritance):
        return 'class {}{}:'.format(interface['shortname'],
                                    inheritance)

    @property
    def interface_maps(self):
        return self._interface_maps_dir

    @interface_maps.setter
    def interface_maps(self, interface_maps_dir):
        self._interface_maps_dir = self._make_dir(interface_maps_dir)

    def module_header(self, module):
        return ''

    @property
    def package_maps(self):
        return self._package_maps_dir

    @package_maps.setter
    def package_maps(self, package_maps_dir):
        self._package_maps_dir = self._make_dir(package_maps_dir)

    @property
    def pattern_maps(self):
        return self._pattern_maps_dir

    @pattern_maps.setter
    def pattern_maps(self, pattern_maps_dir):
        self._pattern_maps_dir = self._make_dir(pattern_maps_dir)

    def grab_osid_name(self, xosid_filepath):
        return xosid_filepath.split('/')[-1].split('.')[-2]

    def get_interface_module(self, pkg_name, interface_shortname, report_error=False):
        """This function returns the category, or 'module' for the interface in question
        By default it does not raise an exception, but can be called with report-
        error equals True so that you can track un-categorized interfaces.
        """
        category = 'UNKNOWN_MODULE'
        try:
            with open(self._package_interface_file(pkg_name), 'r') as read_file:
                index = json.load(read_file)
        except IOError:
            if report_error:
                print ('INTERFACE LOOKUP ERROR - interface map for \'' + pkg_name +
                       '.' + interface_shortname + '\' not found.')
        else:
            try:
                category = index[pkg_name + '.' + interface_shortname]
            except KeyError:
                if report_error:
                    print ('INTERFACE LOOKUP ERROR - category for \'' + pkg_name + '.'
                           + interface_shortname + '\' not found.')
        return category

    def write_license_file(self):
        pass

    def write_profile_file(self):
        pass


class PatternBuilder(XOsidMapper, BaseBuilder):
    def _make_impl_pattern_map(self, file_name=None, package=None, **kwargs):
        if package is None:
            package = self.map_xosid(file_name)
        self._make_dir(self.pattern_maps)
        pattern_index = OrderedDict()
        if package is not None:
            pattern_index = map_patterns(package, pattern_index, **kwargs)
            with open(self._package_pattern_file(package=package), 'w') as write_file:
                json.dump(pattern_index, write_file, indent=3)
        return True

    def make_patterns(self):
        sub_packages = []

        if self.package_maps[-1] != '/':
            json_pattern = self.package_maps + '/*.json'
        else:
            json_pattern = self.package_maps + '*.json'

        for json_file in glob.glob(json_pattern):
            with open(json_file, 'r') as read_file:
                package = json.load(read_file)

            if len(package['name'].split('.')) > 1:
                sub_packages.append(package)
            else:
                self._make_impl_pattern_map(package=package)

        for package in sub_packages:
            if self._pattern_map_exists(package):
                with open(self._package_pattern_file(package), 'r') as read_file:
                    base_package = json.load(read_file)

                self._make_impl_pattern_map(package=package,
                                            base_package=base_package)
            else:
                print 'Could not find pattern map' + \
                      self.first(package['name']) + \
                      'required for processing package' + \
                      package['name']


class Templates(Utilities):
    def __init__(self, template_dir=None, *args, **kwargs):
        self._template_dir = template_dir
        self.package = None

        if template_dir is not None:
            self._make_dir(template_dir)
        super(Templates, self).__init__()

    def _get_templates(self, interface, method, patterns, template_extension):
        """get the extra templates for specified method name"""
        impl_class = self._load_impl_class(interface['shortname'])
        templates_obj = None
        template_name = method['name'] + template_extension
        interface_dot_name = interface['shortname'] + '.' + method['name']

        if (impl_class and
                hasattr(impl_class, template_name)):
            templates_obj = getattr(impl_class, template_name)
        elif interface_dot_name in patterns:
            pattern = patterns[interface_dot_name]['pattern']
            try:
                templates = import_module(self._package_templates(self.first(pattern)))
            except ImportError:
                pass
            else:
                if hasattr(templates, pattern.split('.')[-2]):
                    template_class = getattr(templates, pattern.split('.')[-2])
                    pattern_template = self.last(pattern) + '_import_templates'
                    if hasattr(template_class, pattern_template):
                        templates_obj = getattr(template_class, pattern_template)

        return templates_obj

    def _impl_class(self, interface):
        return self._load_impl_class(interface['shortname'])

    def _load_impl_class(self, interface_name, package_name=None):
        # Try loading hand-built implementations class for this interface
        if package_name is None:
            package_name = self.package['name']
        impl_class = None
        try:
            if ABS_PATH not in sys.path:
                sys.path.insert(0, ABS_PATH)
            impls = import_module(self._package_templates(package_name))
        except ImportError:
            pass
        else:
            if hasattr(impls, interface_name):
                impl_class = getattr(impls, interface_name)
        return impl_class

    def _package_templates(self, package):
        local_template_dir = remove_abs_path(self._template_dir)
        if isinstance(package, dict) and 'name' in package:
            return '.'.join(local_template_dir.split('/')) + '.' + package['name']
        else:
            return '.'.join(local_template_dir.split('/')) + '.' + package

    def _template(self, directory):
        return self._template_dir + '/' + directory

    def extra_templates_exists(self, method, interface, patterns, template_extension):
        """checks if an argument template with default values
         exists for the given method"""

        # first check for non-templated methods, if they have arg_default_template
        impl_class = self._load_impl_class(interface['shortname'])
        if (impl_class and
                hasattr(impl_class, method['name'] + template_extension)):
            return True
        # now check if it is a templated method.
        elif interface['shortname'] + '.' + method['name'] in patterns:
            pattern = patterns[interface['shortname'] + '.' + method['name']]['pattern']
            if pattern != '':
                try:
                    templates = import_module(self._package_templates(self.first(pattern)))
                except ImportError:
                    pass
                else:
                    if hasattr(templates, pattern.split('.')[-2]):
                        template_class = getattr(templates, pattern.split('.')[-2])
                        if hasattr(template_class, self.last(pattern) + template_extension):
                            return True
        return False

    def get_arg_default_map(self, arg_context, method, interface, patterns):
        """gets an argument template and maps the keys to the actual arg names"""
        arg_map = {}
        arg_template = self._get_templates(interface, method, patterns, '_arg_template')

        if arg_template is not None:
            arg_list = arg_context['arg_list'].split(',')
            for index, val in arg_template.iteritems():
                try:
                    arg_map[arg_list[int(index)].strip()] = str(val)
                except KeyError:
                    pass

        return arg_map

    def get_templated_imports(self, arg_context, package_name, method, interface, patterns):
        """gets an import template and maps the keys to the actual arg names.
        Returns a list of imports..."""
        imports = []
        import_templates = self._get_templates(interface, method, patterns, '_import_templates')
        if import_templates is not None:
            for item in import_templates:
                template = string.Template(item)
                imports.append(template.substitute(arg_context))

        return imports


class Builder(Utilities):
    def __init__(self, build_dir='/dlkit'):
        """configure the builder"""
        self._build_to_dir = None
        self.build_dir = build_dir
        self._xosid_dir = '/xosid'
        super(Builder, self).__init__()

    @property
    def build_dir(self):
        return self._build_to_dir

    @build_dir.setter
    def build_dir(self, value):
        self._build_to_dir = self._make_dir(value, python=True)

    def abc(self):
        from abcbinder import ABCBuilder
        ABCBuilder(build_dir=self.build_dir).make()

    def authz(self):
        from azbuilder import AZBuilder
        AZBuilder(build_dir=self.build_dir).make()

    def map(self):
        """map all the xosid files"""
        from mappers import Mapper
        print "Mapping OSIDs"
        Mapper().map_all('all')

    def mongo(self):
        from mongobuilder import MongoBuilder
        MongoBuilder(build_dir=self.build_dir).make()

    def mdata(self):
        from mdatabuilder import MDataBuilder
        MDataBuilder(build_dir=self.build_dir).make()

    def patterns(self):
        print "Creating pattern files"
        PatternBuilder().make_patterns()

    def services(self):
        from kitbuilder import KitBuilder
        KitBuilder(build_dir=self.build_dir).make()

    def tests(self, create_parent_dir=False):
        from testbuilder import TestBuilder
        if create_parent_dir:
            TestBuilder(build_dir=self.build_dir + '/tests').make()
        else:
            TestBuilder(build_dir=self.build_dir).make()

if __name__ == '__main__':

    def usage():
        print "Usage: python build_controller.py [commands]"
        print "where:"
        print "  [commands] is any set of supported commands"
        print ""
        print "Supported commands:"
        print "  map: map the xosid files into pattern_maps/ and package_maps/"
        print "  abc: build the abstract_osids"
        print "  patterns: build the patterns"
        print "  #mdata: build the metadata files"
        print "  authz: build the authz_adapter impl"
        print "  mongo: build the mongo OSID impl"
        print "  services: build the dlkit convenience service impls"
        print "  tests: build the tests"
        print "  --all: build all of the above"
        print "  --buildto <directory>: the target build-to directory"
        print ""
        print "This searches the ./xosid/ directory for *.xosid files, which are parsed into code."
        print ""
        print "NOTE: if Tests are built with the other apps, they will be in a sub-folder of the "
        print "      buildto directory called \"tests/\". Otherwise they will be built into the "
        print "      specified directory."
        print ""
        print "This will build the files to the directory specified, default of ./dlkit/."
        print ''
        print "examples:"
        print "  python build_controller.py map patterns abc mdata mongo"
        print "  python build_controller.py --all"

    if len(sys.argv) == 1:
        usage()
    else:
        builder = Builder()
        commands = ['--all',
                    '--buildto',
                    'map',
                    'patterns',
                    'abc',
                    'mdata',
                    'mongo',
                    'authz',
                    'services',
                    'tests']
        if not any(c in sys.argv for c in commands):
            usage()
            sys.exit(1)

        # check that a follow-on directory to --buildto exists
        target_dir = None

        if '--buildto' in sys.argv:
            try:
                target_dir = sys.argv[sys.argv.index('--buildto') + 1]
            except IndexError:
                # no follow-on directory
                usage()
                sys.exit(1)
            else:
                if target_dir in commands:
                    usage()
                    sys.exit(1)
                builder.build_dir = target_dir

        if '--all' in sys.argv:
            # ignore the other commands
            builder.map()
            builder.patterns()
            builder.abc()
            builder.mongo()
            builder.mdata()
            builder.services()
            builder.authz()
            builder.tests(True)
        else:
            # need to do these in a specific order, regardless of how
            # they are passed in.
            non_test_build = False
            if 'map' in sys.argv:
                builder.map()
                non_test_build = True
            if 'patterns' in sys.argv:
                builder.patterns()
                non_test_build = True
            if 'abc' in sys.argv:
                builder.abc()
                non_test_build = True
            if 'mongo' in sys.argv:
                builder.mongo()
                non_test_build = True
            if 'mdata' in sys.argv:
                builder.mdata()
                non_test_build = True
            if 'services' in sys.argv:
                builder.services()
                non_test_build = True
            if 'authz' in sys.argv:
                builder.authz()
                non_test_build = True
            if 'tests' in sys.argv:
                builder.tests(non_test_build)
    sys.exit(0)
