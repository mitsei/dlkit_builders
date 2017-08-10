import os
import glob
import json
import shutil
import string

from binder_helpers import under_to_mixed, under_to_caps, camel_to_mixed,\
    remove_plural, camel_to_under, make_plural, camel_to_caps_under,\
    fix_reserved_word, under_to_camel
from build_dlkit import Utilities, BaseBuilder, Templates
from config import managers_to_implement, packages_to_test, test_service_configs
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
        looks different than json"""
        super(InterfaceBuilder, self).__init__()
        self._ind = 4 * ' '
        self._dind = 2 * self._ind

    def _copy_package_helpers(self):
        if not self._is('abc'):
            package_helper_dir = self._template(self.replace(self.package['name']) + '_helpers')
            package_helper_dir = '{0}/{1}/*.py'.format(package_helper_dir,
                                                       self._class)
            for helper_file in glob.glob(package_helper_dir):
                if self._is('services'):
                    shutil.copy(helper_file, self._root_dir)
                else:
                    package_dir = '{0}/{1}/'.format(self._root_dir,
                                                    fix_reserved_word(self.replace(self.package['name']), is_module=True))
                    self._make_dir(package_dir)
                    shutil.copy(helper_file, package_dir)

    def _get_class_inheritance(self, interface):
        def get_full_interface_class():
            return (self._abc_pkg_name(abc=self._is('abc'), reserved_word=False) + '_' +
                    interface['category'] + '.' +
                    interface['shortname'])

        if self._is('abc'):
            return ''

        last_inheritance = []

        # Seed the inheritance list with this interface's abc_osid
        if self._is('tests'):
            return '(object)'
        elif not self._is('manager') and self.package['name'] != 'osid' and interface['category'] == 'managers':
            inheritance = []
            last_inheritance = [get_full_interface_class()]
        elif self._is('doc_dlkit'):
            inheritance = []
        else:
            inheritance = ['abc_' + get_full_interface_class()]

        # Iterate through any inherited interfaces and build the inheritance
        # list for this interface. Also, check if an import statement is
        # required and append to the appropriate module's import list.
        for i in interface['inheritance']:
            pkg_name = self._abc_pkg_name(package_name=i['pkg_name'], abc=self._is('abc'))
            unknown_module_protection = ''
            inherit_category = self.get_interface_module(pkg_name, i['name'], True)
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

        if self._in(['json', 'stub', 'services', 'authz', 'manager']):
            # Check to see if there are any additional inheritances required
            # by the implementation patterns.  THIS MAY WANT TO BE REDESIGNED
            # TO ALLOW INSERTING THE INHERITANCE IN A PARTICULAR ORDER.

            # For services, this is later in the code than the original
            # builder. Not sure if that matters or not...will find out.
            impl_class = self._load_impl_class(interface['shortname'])
            if hasattr(impl_class, 'inheritance'):
                inheritance += getattr(impl_class, 'inheritance')

            # Try to consolidate ProxyManager code with Manager code, so inherit the Manager
            if self.is_proxy_manager(interface):
                inheritance.append(interface['shortname'].replace('Proxy', ''))

        if self._in(['services', 'doc_dlkit']):
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

    def _get_extra_patterns(self, interface, import_statement='', default=None):
        if default is None:
            default = []
        if isinstance(interface, basestring) and interface + '.init_pattern' in self.patterns:
            interface_name = interface
            init_pattern = self.patterns[interface_name + '.init_pattern']
            try:
                templates = import_module(self._package_templates(self.first(init_pattern)))
                if hasattr(templates, self.last(init_pattern)):
                    template_class = getattr(templates, self.last(init_pattern))
                    if hasattr(template_class, import_statement):
                        return getattr(template_class, import_statement)
            except ImportError:
                return default
        elif isinstance(interface, dict):
            template_imports = []
            interface_name = interface['shortname']
            import_statement = 'import_statements_pattern'
            if interface_name + '.init_pattern' in self.patterns:
                init_pattern = self.patterns[interface_name + '.init_pattern']
                try:
                    templates = import_module(self._package_templates(self.first(init_pattern)))
                    if hasattr(templates, self.last(init_pattern)):
                        template_class = getattr(templates, self.last(init_pattern))
                        if hasattr(template_class, import_statement):
                            template_imports += self.get_impl_from_templates(template_class, import_statement)
                except ImportError:
                    return default

            for method in interface['methods']:
                pattern = self._get_pattern(method, interface)

                template_class = None
                if pattern:
                    try:
                        templates = import_module(self._package_templates(self.first(pattern)))
                    except ImportError:
                        pass
                    else:
                        if hasattr(templates, pattern.split('.')[-2]):
                            template_class = getattr(templates, pattern.split('.')[-2])

                # Check if there is a 'by hand' implementation available for this method
                imports = 'import_statements_pattern'
                if (template_class and
                        hasattr(template_class, imports)):
                    template_imports += self.get_impl_from_templates(template_class, imports)

            # also apply the context here
            context = self._get_init_context(interface_name, interface)
            for index, import_str in enumerate(template_imports):
                import_template = string.Template(import_str)
                template_imports[index] = import_template.substitute(context)

            return template_imports
        return default

    def _get_init_context(self, init_pattern, interface):
        """get the init context, for templating"""
        def grab_object_name():
            """from the interface, get the object name. Typically want to remove the XSession part

            i.e. assessment.Bank => assessment.Bank
                 assessment.Item => assessment.Item
                 assessment.ItemLookupSession => assessment.Item
                 resource.ResourceBinAssignmentSession => resource.Resource
                 grading.GradeSystemAdminSession => grading.GradeSystem

            """
            just_the_object_name = interface_name
            if '.' in interface_name:
                just_the_object_name = self.last(interface_name)
            if 'Form' in just_the_object_name:
                just_the_object_name = just_the_object_name.replace('Form', '')

            underscore_name = camel_to_under(just_the_object_name)

            # In general, keep only the first word in ``underscore_name``, however also have to
            #   account for two-word objects, like AssessmentPart and SequenceRule
            two_word_objects = ['assessment_part', 'sequence_rule', 'grade_entry',
                                'log_entry', 'grade_system', 'gradebook_column',
                                'asset_content', 'assessment_offered', 'assessment_taken',
                                'assessment_section', 'objective_bank', 'resource_relationship']

            object_name_ = under_to_camel(underscore_name.split('_')[0])

            if any(two in underscore_name for two in two_word_objects) or 'profile' in underscore_name:
                try:
                    object_name_ = under_to_camel(next(two for two in two_word_objects
                                                       if two in underscore_name))
                except StopIteration:
                    object_name_ = interface_name

            return object_name_

        def init_string(name, init_type):
            return '\n{}osid_objects.{}._init_{}(self)'.format(self._dind,
                                                               name,
                                                               init_type)

        instance_initers = ''
        persisted_initers = ''
        metadata_initers = ''
        metadata_super_initers = ''
        map_super_initers = ''
        init_object = ''

        interface_name = interface['shortname']
        object_name = grab_object_name()

        cat_name = self.patterns['package_catalog_caps']

        # Check for any special data initializations and call the appropriate makers
        # to assemble them.
        if init_pattern == 'osid_form.GenericObjectForm':
            if not self._is('authz'):
                if object_name in self.patterns['package_relationships_caps']:
                    init_object = 'osid_objects.OsidRelationshipForm'
                else:  # maybe need to check for other init objects, like Rules?
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
                        self.patterns[object_name + '.persisted_data'],
                        self.patterns[object_name + '.initialized_data'],
                        self.patterns[object_name + '.aggregate_data'])
                except KeyError:
                    pass

                try:
                    metadata_initers = make_metadata_initers(
                        interface_name,
                        self.patterns[object_name + '.persisted_data'],
                        self.patterns[object_name + '.initialized_data'],
                        self.patterns[object_name + '.return_types'])
                    if metadata_initers != '':
                        metadata_initers += '\n'
                except KeyError:
                    pass

        # Special one for services test builder to select whether a session method
        # should be called from a service manager or catalog
        if object_name == cat_name:
            svc_mgr_or_catalog = 'svc_mgr'
        else:
            svc_mgr_or_catalog = 'catalog'

        fixed_package_name = fix_reserved_word(self.package['name'], is_module=True)

        session_related_words = ['my', 'session', 'assignment', 'design', 'query', 'admin',
                                 'notification', 'lookup', 'basic', 'authoring']
        interface_namespace = '_'.join([word for word in camel_to_under(interface_name).split('_')
                                        if word not in session_related_words])

        return {'app_name': self._app_name(),
                'implpkg_name': self._abc_pkg_name(abc=False, reserved_word=False),
                'kitpkg_name': self._abc_pkg_name(abc=False),
                'pkg_name': self.package['name'],
                'base_pkg_name': self.package['name'].split('.')[0],
                'base_pkg_name_reserved': fixed_package_name.split('.')[0],
                'pkg_name_caps': self.first(self.package['name']).title(),
                'pkg_name_replaced': self.replace(self.package['name']),
                'pkg_name_replaced_reserved': self.replace(fixed_package_name),
                'pkg_name_replaced_caps': self.replace(self.package['name'].title(), desired=''),
                'pkg_name_replaced_upper': self.replace(self.package['name']).upper(),
                'pkg_name_replaced_under': camel_to_under(self.replace(self.package['name'])),
                'pkg_name_upper': self.first(self.package['name']).upper(),
                'interface_name': interface_name,
                'interface_name_under': camel_to_under(interface_name),
                'interface_namespace_camel': under_to_camel(interface_namespace),
                'proxy_interface_name': proxy_manager_name(interface_name),
                'interface_name_title': interface_name.title(),
                'instance_initers': instance_initers,
                'persisted_initers': persisted_initers,
                'metadata_initers': metadata_initers,
                'metadata_super_initers': metadata_super_initers,
                'map_super_initers': map_super_initers,
                'object_name': object_name,
                'object_name_under': camel_to_under(object_name),
                'object_name_caps_under': camel_to_caps_under(object_name),
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
                'svc_mgr_or_catalog': svc_mgr_or_catalog,
                'test_service_configs': test_service_configs or ['TEST_SERVICE']}

    def _grab_service_methods(self, type_check_method):
        self.patterns['implemented_view_methods'] = []
        inherited_imports = []
        methods = ''
        for inf in self.package['interfaces']:
            # Check to see if this interface is meant to be implemented.
            if self.package['name'] != 'osid' and not self._flagged_for_implementation(inf):
                continue
            if type_check_method(inf, self.package['name']):
                additional_methods = self._additional_methods(inf)
                methods += '\n##\n# The following methods are from {}\n\n'.format(inf['fullname'])
                methods += self.make_methods(inf)

                if additional_methods:
                    methods += '\n\n{0}'.format(additional_methods)

                inherited_imports = self.get_methods_templated_imports(self._abc_pkg_name(abc=False),
                                                                       inf)
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
            if self._is('json'):
                self._make_dir(self._app_name(), python=True)
        else:
            # Check if a directory already exists for the abc osid.  If not,
            # create one and initialize as a python package.
            self._make_dir(self._app_name(), python=True)
            if self._in(['abc', 'json', 'stub', 'authz', 'tests', 'doc_source', 'doc_dlkit']):
                self._make_dir(self._abc_pkg_path(), python=True)

    def _make_init_methods(self, interface):
        templates = None
        template_str = ''
        init_pattern = ''

        impl_class = self._load_impl_class(interface['shortname'],
                                           package_name=self._abc_pkg_name(abc=False, reserved_word=False))
        context = self._get_init_context(init_pattern, interface)
        context['pattern_name'] = self.get_pattern_name('{0}.init_template'.format(init_pattern))

        if (hasattr(impl_class, 'init') and
                self._language in getattr(impl_class, 'init') and
                self._class in getattr(impl_class, 'init')[self._language]):
            template_str = self.get_impl_from_templates(impl_class, 'init')

        elif interface['shortname'] + '.init_pattern' in self.patterns:
            init_pattern = self.patterns[interface['shortname'] + '.init_pattern']
            templates = import_module(self._package_templates(self.first(init_pattern)))

        if templates is not None and hasattr(templates, self.last(init_pattern)):
            template_class = getattr(templates, self.last(init_pattern))
            if hasattr(template_class, 'init_template'):
                context = self._get_init_context(init_pattern, interface)
                context['pattern_name'] = self.get_pattern_name('{0}.init_template'.format(init_pattern))
                template_str = self.get_impl_from_templates(template_class, 'init_template')

        if bool(template_str):
            template = string.Template(template_str)
            return template.substitute(context) + '\n'

        return ''

    def _make_osid(self, file_name):
        # This function expects a file containing a json representation of an
        # osid package that was prepared by the mapper.
        # for sub-packages, append them to a base package file...
        with open(file_name, 'r') as read_file:
            self.package = json.load(read_file)

        if not self._package_to_be_implemented():
            return

        self._copy_package_helpers()

        print("Building {0} osid for {1}".format(self._class, self.package['name']))

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
            self._update_module_imports(modules, interface)
            self.update_module_body(modules, interface)

        self.write_modules(modules)

    def _package_to_be_implemented(self):
        if (self._is('tests') or self._is('test_authz')) and self.package['name'] not in packages_to_test:
            return False

        if self.package['name'] not in managers_to_implement:
            return False

        return True

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
                    print('mapping {0} osid.'.format(self.grab_osid_name(xosid_file)))
                    package = self.make_xosid_map(xosid_file)
                if (not os.path.exists(self._package_interface_file(self.grab_osid_name(xosid_file))) or
                        re_index):
                    print('indexing interfaces for {0} osid.'.format(self.grab_osid_name(xosid_file)))
                    self.make_interface_map(xosid_file, package)

        for json_file in glob.glob(self.package_maps + '/*.json'):
            if self._is('mdata'):
                self._make_mdata(json_file)
            else:
                self._make_osid(json_file)

        if not self._is('abc') and not self._is('mdata'):
            # Copy general config and primitive files, etc into the
            # implementation root directory:
            helper_dir = '{0}/{1}/*.py'.format(self._template('helpers'),
                                               self._class)
            for helper_file in glob.glob(helper_dir):
                shutil.copy(helper_file, self._root_dir)
        else:
            # copy over the abc_errors.py file to abstract_osid.osid.errors.py
            error_file = self._abs_path + '/builders/abc_errors.py'
            if os.path.exists(error_file):
                shutil.copyfile(error_file, self._root_dir + '/osid/errors.py')


# Assemble the initializers for metadata managed by Osid Object Forms
def make_metadata_initers(interface_name, persisted_data, initialized_data, return_types):

    def default_string(name, default_type, is_list=False):
        dind = 8 * ' '
        if is_list:
            return '{0}self._{1}_default = self._mdata[\'{1}\'][\'default_{2}_values\']\n'.format(dind,
                                                                                                  name,
                                                                                                  default_type)
        else:
            return '{0}self._{1}_default = self._mdata[\'{1}\'][\'default_{2}_values\'][0]\n'.format(dind,
                                                                                                     name,
                                                                                                     default_type)

    imports = ''
    default = ''
    for data_name in persisted_data:

        if (persisted_data[data_name] != 'OsidCatalog' and
                data_name not in initialized_data):
            if persisted_data[data_name] == 'boolean':
                default += default_string(data_name, 'boolean')
            elif (persisted_data[data_name] == 'string' and
                    return_types[data_name] == 'osid.locale.DisplayText'):
                default += '        update_display_text_defaults(self._mdata[\'{0}\'], self._locale_map)\n' \
                           '        self._{0}_default = ' \
                           'dict(self._mdata[\'{0}\'][\'default_string_values\'][0])\n'.format(data_name)
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

    return (imports + default).strip()


# Assemble the initializers for persistance data managed by Osid Object Forms
# initialized with the form.
def make_persistance_initers(persisted_data, initialized_data, aggregate_data):
    initers = ''

    singular_data_types = ['osid.id.Id', 'osid.type.Type', 'string', 'decimal',
                           'boolean', 'OsidCatalog', 'osid.calendaring.DateTime',
                           'timestamp', 'osid.calendaring.Duration',
                           'osid.transport.DataInputStream']

    append_ids = ['osid.id.Id', 'osid.type.Type']

    plural_data_types = ['osid.id.Id[]', 'osid.type.Type[]']

    for data_name in persisted_data:
        mixed_name = under_to_mixed(data_name)
        # caps_name = mixed_name.title()
        caps_name = under_to_caps(data_name)
        mixed_singular = under_to_mixed(remove_plural(data_name))

        persisted_name = persisted_data[data_name]
        if persisted_name == 'OsidCatalog':
            initers += '        self._my_map[\'assigned{}Ids\'] = [str(kwargs[\'{}_id\'])]\n'.format(caps_name,
                                                                                                     data_name)
        # if ((persisted_name == 'osid.id.Id' or
        #         persisted_name == 'OsidCatalog') and
        #         data_name in initialized_data):
        elif (persisted_name == 'osid.id.Id' and
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
        elif persisted_name in ['osid.grading.Grade'] and data_name == 'level':  # fix bug with ProficiencyForm
            initers += "        self._my_map['level'] = self._level_metadata['default_id_values'][0]\n"

    for data_name in aggregate_data:
        mixed_name = under_to_mixed(data_name)
        if aggregate_data[data_name].endswith('List'):
            initers += '        self._my_map[\'{}\'] = []\n'.format(mixed_name)
        else:
            initers += '        self._my_map[\'{}\'] = None\n'.format(mixed_name)

    initialize_to_none = ['boolean', 'osid.calendaring.DateTime', 'timestamp',
                          'osid.calendaring.Duration']
    initialize_to_empty_string = ['cardinal', 'string']
    initialize_to_zero = ['decimal']

    for data_name in initialized_data:
        mixed_name = under_to_mixed(data_name)

        if data_name in persisted_data:
            pass
        elif initialized_data[data_name] in initialize_to_none:
            initers += '        self._my_map[\'{}\'] = None\n'.format(mixed_name)
        elif initialized_data[data_name] in initialize_to_empty_string:
            initers += '        self._my_map[\'{}\'] = \'\'\n'.format(mixed_name)
        elif initialized_data[data_name] in initialize_to_zero:
            initers += '        self._my_map[\'{}\'] = 0.0\n'.format(mixed_name)
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


# Return the associated class name for a ProxyManager given a Manager name
def proxy_manager_name(string_):
    return string_.split('Manager')[0] + 'ProxyManager'
