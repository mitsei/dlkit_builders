import os
import glob
import json
import shutil
import string

from binder_helpers import under_to_mixed, camel_to_mixed,\
    remove_plural, camel_to_under, make_plural, camel_to_caps_under
from build_controller import Utilities, BaseBuilder, Templates
from config import managers_to_implement, packages_to_test
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


class InterfaceBuilder(MethodBuilder, Mapper, BaseBuilder, Templates, Utilities):
    """class that builds interfaces"""
    def __init__(self, *args, **kwargs):
        """method_class differentiates between different variations, i.e. abc
        looks different than mongo"""
        super(InterfaceBuilder, self).__init__()
        self._ind = 4 * ' '
        self._dind = 2 * self._ind

    def _copy_package_helpers(self):
        if not self._is('abc'):
            package_helper_dir = self._template(self.package['name'] + '_helpers')
            for helper_file in glob.glob(package_helper_dir + '/*.py'):
                if self._is('services'):
                    shutil.copy(helper_file, self._root_dir)
                else:
                    package_dir = '{0}/{1}/'.format(self._root_dir,
                                                    self.package['name'])
                    self._make_dir(package_dir)
                    shutil.copy(helper_file, package_dir)

    def _get_class_inheritance(self, interface):
        def get_full_interface_class():
            return (self._abc_pkg_name(abc=self._is('abc')) + '_' +
                    interface['category'] + '.' +
                    interface['shortname'])

        if self._is('abc'):
            return ''

        last_inheritance = []

        # Seed the inheritance list with this interface's abc_osid
        if self._is('tests'):
            inheritance = ['unittest.TestCase']
        elif self.package['name'] != 'osid' and interface['category'] == 'managers':
            inheritance = []
            last_inheritance = [get_full_interface_class()]
        else:
            inheritance = ['abc_' + get_full_interface_class()]

        # Iterate through any inherited interfaces and build the inheritance
        # list for this interface. Also, check if an import statement is
        # required and append to the appropriate module's import list.
        if not self._is('tests'):
            for i in interface['inheritance']:
                pkg_name = self._abc_pkg_name(package_name=i['pkg_name'], abc=self._is('abc'))
                unknown_module_protection = ''
                inherit_category = self.get_interface_module(i['pkg_name'], i['name'], True)
                if inherit_category == 'UNKNOWN_MODULE':
                    unknown_module_protection = '\"\"\"'

                if (i['pkg_name'] == self.package['name'] and
                        inherit_category == interface['category']):
                    inheritance.append(i['name'])
                else:
                    if self._is('services') and i['pkg_name'] != self.package['name']:
                        inheritance.append(i['pkg_name'] + '.' + i['name'])

                    if not self._is('services'):
                        inheritance.append(unknown_module_protection +
                                           pkg_name + '_' +
                                           inherit_category + '.' + i['name'] +
                                           unknown_module_protection)

        if self._in(['mongo', 'services', 'authz', 'tests']):
            # Check to see if there are any additional inheritances required
            # by the implementation patterns.  THIS MAY WANT TO BE REDESIGNED
            # TO ALLOW INSERTING THE INHERITANCE IN A PARTICULAR ORDER.

            # For services, this is later in the code than the original
            # builder. Not sure if that matters or not...will find out.
            impl_class = self._load_impl_class(interface['shortname'])
            if hasattr(impl_class, 'inheritance'):
                inheritance += getattr(impl_class, 'inheritance')

        if self._is('services'):
            # Don't forget the OsidSession inheritance:
            if (('OsidManager' in interface['inherit_shortnames'] or
                    interface['shortname'] == self.patterns['package_catalog_caps']) and
                    self.package['name'] != 'osid'):
                inheritance.insert(1, 'osid.OsidSession')

        # Note that the following re-assigns the inheritance variable from a
        # list to a string.
        if last_inheritance:
            inheritance = inheritance + last_inheritance

        if inheritance:
            inheritance = '({})'.format(', '.join(inheritance))
        else:
            inheritance = ''

        return inheritance

    def _get_extra_patterns(self, interface_name, import_statement, default=None):
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

    def _get_init_context(self, init_pattern, interface):
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

        interface_name = interface['shortname']

        cat_name = self.patterns['package_catalog_caps']

        # Check for any special data initializations and call the appropriate makers
        # to assemble them.
        if init_pattern == 'resource.Bin':
            object_name = interface_name
        elif init_pattern == 'resource.BinForm':
            object_name = interface_name[:-4]
        elif init_pattern == 'resource.BinNode':
            object_name = interface_name[:-4]
        elif init_pattern == 'resource.ResourceLookupSession':
            object_name = interface_name[:-13]
        elif init_pattern == 'resource.ResourceQuerySession':
            object_name = interface_name[:-12]
        elif init_pattern == 'resource.ResourceSearchSession':
            object_name = interface_name.replace('SearchSession', '')
        elif init_pattern == 'resource.ResourceAdminSession':
            object_name = interface_name[:-12]
        elif init_pattern == 'resource.ResourceNotificationSession':
            object_name = interface_name[:-len('NotificationSession')]
        elif init_pattern == 'resource.ResourceBinSession':
            object_name = interface_name.replace(cat_name + 'Session', '')
        elif init_pattern == 'resource.ResourceBinAssignmentSession':
            object_name = interface_name.replace(cat_name + 'AssignmentSession', '')
        elif init_pattern == 'commenting.CommentLookupSession':
            object_name = interface_name.replace('LookupSession', '')
        elif init_pattern == 'commenting.CommentQuerySession':
            object_name = interface_name.replace('QuerySession', '')
        elif init_pattern == 'repository.CompositionLookupSession':
            object_name = interface_name.replace('LookupSession', '')
        elif init_pattern == 'repository.CompositionQuerySession':
            object_name = interface_name.replace('QuerySession', '')
        elif init_pattern == 'resource.Resource':
            object_name = interface_name
        elif init_pattern == 'resource.ResourceForm':
            object_name = interface_name[:-4]
            if not self._is('authz'):
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
                        self.patterns[interface_name[:-4] + '.persisted_data'],
                        self.patterns[interface_name[:-4] + '.initialized_data'],
                        self.patterns[interface_name[:-4] + '.aggregate_data'])
                except KeyError:
                    pass

                try:
                    metadata_initers = make_metadata_initers(
                        interface_name,
                        self.patterns[interface_name[:-4] + '.persisted_data'],
                        self.patterns[interface_name[:-4] + '.initialized_data'],
                        self.patterns[interface_name[:-4] + '.return_types'])
                except KeyError:
                    pass
        elif init_pattern == 'resource.ResourceQuery':
            object_name = interface_name[:-5]

        # Special one for services test builder to select whether a session method
        # should be called from a service manager or catalog
        if object_name == cat_name:
            svc_mgr_or_catalog = 'svc_mgr'
        else:
            svc_mgr_or_catalog = 'catalog'

        return {'app_name': self._app_name(),
                'implpkg_name': self._abc_pkg_name(abc=False),
                'kitpkg_name': self._abc_pkg_name(abc=False),
                'pkg_name': self.package['name'],
                'pkg_name_caps': self.package['name'].title(),
                'pkg_name_upper': self.package['name'].upper(),
                'interface_name': interface_name,
                'proxy_interface_name': proxy_manager_name(interface_name),
                'interface_name_title': interface_name.title(),
                'instance_initers': instance_initers,
                'persisted_initers': persisted_initers,
                'metadata_initers': metadata_initers,
                'metadata_super_initers': metadata_super_initers,
                'map_super_initers': map_super_initers,
                'object_name': object_name,
                'object_name_under': camel_to_under(object_name),
                'object_name_upper': camel_to_under(object_name).upper(),
                'object_name_plural': make_plural(object_name),
                'object_name_under_plural': camel_to_under(make_plural(object_name)),
                'cat_name': cat_name,
                'cat_name_plural': make_plural(cat_name),
                'cat_name_mixed': camel_to_mixed(cat_name),
                'cat_name_under': camel_to_under(cat_name),
                'cat_name_under_plural': make_plural(camel_to_under(cat_name)),
                'cat_name_upper': cat_name.upper(),
                'init_object': init_object,
                'svc_mgr_or_catalog': svc_mgr_or_catalog}

    def _grab_service_methods(self, type_check_method):
        self.patterns['implemented_view_methods'] = []
        inherited_imports = []
        methods = ''
        for inf in self.package['interfaces']:
            # Check to see if this interface is meant to be implemented.
            if self.package['name'] != 'osid' and not self._flagged_for_implementation(inf):
                continue

            if type_check_method(inf, self.patterns, self.package['name']):
                methods += '\n##\n# The following methods are from {}\n\n'.format(inf['fullname'])
                methods += self.make_methods(inf, self.patterns) + '\n\n'
                # methods += self.method_builder.make_methods(self.package['name'], inf, self.patterns) + '\n\n'
                inherited_imports = self.get_methods_templated_imports(self._abc_pkg_name(abc=False),
                                                                       inf,
                                                                       self.patterns)
                # inherited_imports = self.method_builder.get_methods_templated_imports(self._abc_pkg_name(abc=False),
                #                                                                       inf,
                #                                                                       self.patterns)
        return methods, inherited_imports

    def _initialize_directories(self):
        if self._root_dir is None:
            ##
            # Check if an app directory and abc osid subdirectory already exist.
            # If not, create them  This code specifically splits out the osid
            # packages in a Django app environment.  For other Python based
            # implementations try using the subsequent, more generic code instead.
            from django.core.management import call_command
            if not os.path.exists(self._app_name()):
                call_command('startapp', self._app_name())
            if self._is('mongo'):
                self._make_dir(self._app_name(), python=True)
        else:
            # Check if a directory already exists for the abc osid.  If not,
            # create one and initialize as a python package.
            self._make_dir(self._app_name(), python=True)
            if self._in(['mongo', 'authz', 'tests', 'doc_source']):
                self._make_dir(self._abc_pkg_path(), python=True)

    def _make_init_methods(self, interface):
        templates = None
        init_pattern = ''

        impl_class = self._load_impl_class(interface['shortname'],
                                           package_name=self._abc_pkg_name(abc=False))
        if hasattr(impl_class, 'init'):
            return getattr(impl_class, 'init') + '\n'
        elif interface['shortname'] + '.init_pattern' in self.patterns:
            init_pattern = self.patterns[interface['shortname'] + '.init_pattern']
            try:
                templates = import_module(self._package_templates(self.first(init_pattern)))
            except ImportError:
                pass

        if templates is not None and hasattr(templates, self.last(init_pattern)):
            template_class = getattr(templates, self.last(init_pattern))
            if hasattr(template_class, 'init_template'):
                context = self._get_init_context(init_pattern, interface)
                template = string.Template(getattr(template_class, 'init_template'))
                return template.substitute(context) + '\n'

        return ''

    def _make_osid(self, file_name):
        # This function expects a file containing a json representation of an
        # osid package that was prepared by the mapper.
        with open(file_name, 'r') as read_file:
            self.package = json.load(read_file)

        if not self._package_to_be_implemented():
            return

        self._copy_package_helpers()

        print "Building {0} osid for {1}".format(self._class, self.package['name'])

        self.patterns = self._patterns()

        # The map structure for the modules to be created by this function.
        # Each module will get a body string that holds the class and method
        # signatures for the particular interface category, and a list of
        # for the modules that the module's classes may inherit.
        modules = self._empty_modules_dict()

        self._initialize_directories()
        self.write_license_file()
        self.write_profile_file()

        # Initialize the module doc and abc import string for each module
        for module in modules:
            modules[module]['imports'].append(self.module_header(module))


        # The real work starts here.  Iterate through all interfaces to build
        # all the classes for this osid package.
        for interface in self.package['interfaces']:
            if not self.build_this_interface(interface):
                continue

            inheritance = self._get_class_inheritance(interface)

            additional_methods = ''

            if not self._is('abc'):
                self._update_module_imports(modules, interface)

            if self._is('abc'):
                # Add the equality methods to Ids and Types:
                if interface['shortname'] in ['Id', 'Type']:
                    additional_methods += eq_methods(interface['shortname'])
                    additional_methods += str_methods()
            else:
                # Look for additional methods defined in class patterns. These
                # need to be coded in the impl_class as a string with the
                # attribute name 'additional_methods_pattern'
                additional_methods += self._get_extra_patterns(interface['shortname'],
                                                               'additional_methods_pattern',
                                                               default='')

                # Here we further inspect the impl_class to identify any additional
                # hand built methods to be included at the end of the class definition. These
                # need to be coded in the impl_class as a string with the
                # attribute name 'additional_methods'
                impl_class = self._impl_class(interface)
                if hasattr(impl_class, 'additional_methods'):
                    additional_methods += getattr(impl_class, 'additional_methods')

            if self._is('authz'):
                class_doc = ('{}\"\"\"Adapts underlying {} methods' +
                             'with authorization checks.\"\"\"').format(self._ind,
                                                                        interface['shortname'])
            elif self._is('tests'):
                class_doc = '{}\"\"\"Tests for {}\"\"\"'.format(self._ind,
                                                                interface['shortname'])
            elif not self._is('services'):
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
            else:
                class_doc = ('{}\"\"\"{} convenience adapter ' +
                             'including related Session methods."\"\"').format(self._ind,
                                                                               interface['shortname'])

            class_sig = self.class_sig(interface, inheritance)

            if self._is('abc'):
                modules[interface['category']]['body'] = (
                    modules[interface['category']]['body'] +
                    class_sig + '\n' +
                    class_doc + '\n' +
                    '    __metaclass__ = abc.ABCMeta\n\n' +
                    additional_methods +
                    self.make_methods(interface,
                                      None) + '\n\n\n')
                    # self.method_builder.make_methods(self.package['name'],
                    #                                  interface,
                    #                                  None) + '\n\n\n')
            else:
                init_methods = self._make_init_methods(interface)
                methods = self.make_methods(interface,
                                            self.patterns)
                # methods = self.method_builder.make_methods(self._abc_pkg_name(abc=False),
                #                                            interface,
                #                                            self.patterns)

                if self._is('services'):
                    # Add all the appropriate manager related session methods to the manager interface
                    # Add all the appropriate catalog related session methods to the catalog interface
                    new_imports = []
                    if 'OsidManager' in interface['inherit_shortnames']:
                        new_methods, new_imports = self._grab_service_methods(self._is_manager_session)
                        methods += new_methods
                    # Add all the appropriate catalog related session methods to the catalog interface
                    elif interface['shortname'] == self.patterns['package_catalog_caps']:
                        new_methods, new_imports = self._grab_service_methods(self._is_catalog_session)
                        methods += new_methods

                    for imp in new_imports:
                        if imp not in modules[self.package['name']]['imports']:
                            modules[self.package['name']]['imports'].append(imp)

                    if not init_methods.strip() and not methods.strip():
                        init_methods = '{}pass'.format(self._ind)

                if additional_methods:
                    methods += '\n' + additional_methods

                body = '{}\n{}\n{}\n{}\n\n\n'.format(class_sig,
                                                     self._wrap(class_doc),
                                                     self._wrap(init_methods),
                                                     methods)

                if self._is('services'):
                    modules[self.package['name']]['body'] += body
                else:
                    modules[interface['category']]['body'] += body

        # Finally, iterate through the completed package module structure and
        # write out both the import statements and class definitions to the
        # appropriate module for this package.
        for module in modules:
            if module == 'records' and self.package['name'] != 'osid':
                module_name = 'record_templates'
            else:
                module_name = module

            if modules[module]['body'].strip() != '':
                if self._is('services'):
                    with open(self._abc_pkg_path(abc=False) + '.py', 'wb') as write_file:
                        constant_declarations = """

DEFAULT = 0
COMPARATIVE = 0
PLENARY = 1
FEDERATED = 0
ISOLATED = 1
AUTOMATIC = 0
MANDATORY = 1
DISABLED = -1"""
                        write_file.write('{}{}\n\n\n{}'.format('\n'.join(order_module_imports(modules[module]['imports'])),
                                                               constant_declarations,
                                                               modules[module]['body']).encode('utf-8'))
                elif self._is('tests'):
                    with open(self._abc_module(module_name, test=True), 'wb') as write_file:
                        write_file.write(('\n'.join(modules[module]['imports']) + '\n\n\n' +
                                         modules[module]['body']).encode('utf-8'))
                else:
                    with open(self._abc_module(module_name), 'wb') as write_file:
                        write_file.write(('\n'.join(order_module_imports(modules[module]['imports'])) +
                                          '\n\n\n' + modules[module]['body']).encode('utf-8'))

    def _package_to_be_implemented(self):
        if self._is('tests') and self.package['name'] not in packages_to_test:
            return False

        if self.package['name'] not in managers_to_implement:
            return False

        return True

    def _update_module_imports(self, modules, interface):
        # And make sure there is a corresponding import statement for this
        # interface's abc_osid and associated module/category name.
        if self._in(['mongo', 'authz', 'tests']):
            imports = modules[interface['category']]['imports']
        else:  # services
            imports = modules[self.package['name']]['imports']

        def append(import_str_):
            if import_str_ not in imports:
                imports.append(import_str_)

        def package_interface():
            return self._abc_pkg_name(package_name=self.package['name'] + '_' + interface['category'])

        if self._is('tests'):
            import_str = 'import unittest'
        else:
            if self.package['name'] != 'osid' and interface['category'] == 'managers':
                import_str = 'from dlkit.manager_impls.{} import {} as {}'.format(self._abc_pkg_name(),
                                                                                  interface['category'],
                                                                                  package_interface())
            else:
                import_str = 'from {}.{} import {} as abc_{}'.format(self._app_name(abstract=True),
                                                                     self._abc_pkg_name(),
                                                                     interface['category'],
                                                                     package_interface())

        append(import_str)

        if self._is('tests'):
            # Check to see if there are any additinal inheritances required
            # by the implementation patterns.  THIS MAY WANT TO BE REDESIGNED
            # TO ALLOW INSERTING THE INHERITANCE IN A PARTICULAR ORDER.
            impl_class = self._load_impl_class(interface['shortname'])
            if hasattr(impl_class, 'inheritance_imports'):
                modules[interface['category']]['imports'] += getattr(impl_class, 'inheritance_imports')
        else:
            # Iterate through any inherited interfaces and check if an import statement is
            # required and append to the appropriate module's import list.
            for i in interface['inheritance']:
                inherit_category = self.get_interface_module(i['pkg_name'], i['name'], True)
                if (i['pkg_name'] == self.package['name'] and
                        inherit_category == interface['category']):
                    pass
                else:
                    if self._is('services') and i['pkg_name'] != self.package['name']:
                        import_str = 'from . import {}'.format(i['pkg_name'])

                    if not self._is('services'):
                        import_str = 'from {0}.{1} import {2} as {1}_{2}'.format(self._import_path(
                                                                                 self._app_name(package_name=i['pkg_name'])),
                                                                                 self._abc_pkg_name(package_name=i['pkg_name'],
                                                                                                    abc=False),
                                                                                 inherit_category)

                    if inherit_category != 'UNKNOWN_MODULE':
                        append(import_str)

        if self._in(['mongo', 'tests']):
            # Check to see if there are any additional inheritances required
            # by the implementation patterns.  THIS MAY WANT TO BE REDESIGNED
            # TO ALLOW INSERTING THE INHERITANCE IN A PARTICULAR ORDER.
            impl_class = self._impl_class(interface)

            # Here we further inspect the impl_class to identify any additional
            # hand built import statements to be loaded at the module level. These
            # need to be coded in the impl_class as a list of strings with the
            # attribute name 'import_statements'
            if hasattr(impl_class, 'import_statements'):
                for import_str in getattr(impl_class, 'import_statements'):
                    append(import_str)

            # Look for module import statements defined in class patterns. These
            # need to be coded in the class pattern as a list of strings with the
            # attribute name 'import_statements_pattern'
            for import_str in self._get_extra_patterns(interface['shortname'],
                                                       'import_statements_pattern',
                                                       default=[]):
                append(import_str)

            if self._is('mongo'):
                # add the none-argument check import if not already present
                append('from .. import utilities')
        elif self._is('services'):
            # Don't forget the OsidSession inheritance:
            if (('OsidManager' in interface['inherit_shortnames'] or
                    interface['shortname'] == self.patterns['package_catalog_caps']) and
                    self.package['name'] != 'osid'):
                import_str = 'from . import osid'
                append(import_str)

            # And don't forget the osid_error import:
            import_str = 'from .osid_errors import Unimplemented, IllegalState'
            append(import_str)
        elif self._is('authz'):
            if self.package['name'] == 'osid' and interface['category'] not in ['markers', 'sessions']:
                # Add the osid_error import
                append('from ..osid.osid_errors import Unimplemented, IllegalState, NullArgument')
                # Add the primitive import
                append('from ..primitives import Id')
            elif self.package['name'] == 'osid' and interface['category'] == 'markers':
                # Add the osid_error import
                append('from ..osid.osid_errors import Unimplemented')
            elif self.package['name'] == 'osid' and interface['category'] == 'sessions':
                # Add the osid_error import
                append('from ..osid.osid_errors import IllegalState, Unimplemented')
                # Add the primitive import
                append('from ..primitives import Id')
            elif interface['category'] == 'managers':
                if inherit_category != 'UNKNOWN_MODULE':
                    # Add the osid_error import
                    append('from ..osid.osid_errors import Unimplemented, OperationFailed')
                   # Add the session import
                    append('from . import sessions')
                    # Add the primitive import
                    append('from ..primitives import Id')
            elif interface['category'] == 'sessions' and not self.package['name'] == 'osid':
                if inherit_category != 'UNKNOWN_MODULE':
                    # Add the primitive import
                    append('from ..primitives import Id')
                    # Add the osid_error import
                    append('from ..osid.osid_errors import PermissionDenied, NullArgument, Unimplemented')

        # Now also check for templated imports
        templated_imports = self.get_methods_templated_imports(self._abc_pkg_name(abc=False),
                                                               interface,
                                                               self.patterns)
        # templated_imports = self.method_builder.get_methods_templated_imports(self._abc_pkg_name(abc=False),
        #                                                                       interface,
        #                                                                       self.patterns)
        for imp in templated_imports:
            append(imp)

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
            if self._is('mdata'):
                self._make_mdata(json_file)
            else:
                self._make_osid(json_file)

        if not self._is('abc') and not self._is('mdata'):
            # Copy general config and primitive files, etc into the
            # implementation root directory:
            for helper_file in glob.glob(self._template('helpers') + '/*.py'):
                shutil.copy(helper_file, self._root_dir)
        else:
            # copy over the abc_errors.py file to abstract_osid.osid.errors.py
            error_file = self._abs_path + '/builders/abc_errors.py'
            if os.path.exists(error_file):
                shutil.copyfile(error_file, self._root_dir + '/osid/errors.py')

def eq_methods(interface_name):
    return (
"""    def __eq__(self, other):
        if isinstance(other, """ + interface_name + """):
            return (
                self.get_authority() == other.get_authority() and
                self.get_identifier_namespace() == other.get_identifier_namespace() and
                self.get_identifier() == other.get_identifier()
            )
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

""")

# Assemble the initializers for metadata managed by Osid Object Forms
def make_metadata_initers(interface_name, persisted_data, initialized_data, return_types):

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
        data_name_upper = camel_to_caps_under(interface_name[:-4]) + '_' + data_name.upper()

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

    import_lists = [docstrings, full_imports, partial_third_party_imports, local_imports, constants]

    results = []
    for import_list in import_lists:
        if len(import_list) > 0:
            results += import_list + newline

    return results

# Return the associated class name for a ProxyManager given a Manager name
def proxy_manager_name(string_):
    return string_.split('Manager')[0] + 'ProxyManager'

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
