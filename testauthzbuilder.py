import json
from collections import OrderedDict

from build_dlkit import BaseBuilder
from interface_builders import InterfaceBuilder
from config import objects_to_implement
from binder_helpers import under_to_caps, under_to_mixed, camel_to_mixed, camel_to_under, remove_plural


class TestAuthZBuilder(InterfaceBuilder, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(TestAuthZBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir
        self._template_dir = self._abs_path + '/testauthz_templates'

        self._class = 'test_authz'

    def _build_method_doc(self, method):
        return '{0}// Tests {1}'.format(self._ind,
                                        under_to_mixed(method['name']))

    def _clean_up_impl(self, impl, interface, method):
        if not impl.strip():
            impl = ''
        elif impl.strip() == 'NOT READY':
            impl = '{}assertTrue("This test is not ready.", false);\n{}}}'.format(self._dind, self._ind)
        else:
            context = self._get_method_context(method, interface)
            interface_sn = interface['shortname']
            method_n = method['name']
            interface_cat = interface['category']

            if (interface_cat in self.patterns['impl_log'] and
                    interface_sn in self.patterns['impl_log'][interface_cat]):
                self.patterns['impl_log'][context['module_name']][interface_sn][method_n][1] = 'implemented'
        return impl

    def _get_method_args(self, method, interface):
        return ['']

    def _get_init_context(self, init_pattern, interface):
        context = super(TestAuthZBuilder, self)._get_init_context(init_pattern, interface)
        if init_pattern == 'commenting.CommentLookupSession':
            print '    building relationship -', interface['shortname']
            obj_name_under = camel_to_under(interface['shortname'].replace('LookupSession', ''))
            try:
                source_type = self.patterns['package_relationships_detail'][obj_name_under]['source_type']
            except KeyError:
                source_type = 'KEY_ERROR'
            try:
                destination_type = self.patterns['package_relationships_detail'][obj_name_under]['destination_type']
            except KeyError:
                destination_type = 'KEY_ERROR'
            print '        source_type =', source_type
            print '        destination_type =', destination_type
            # source_obj_name = source_type.split('.')[-1]
            # source_pkg_name = source_type.split('.')[-2]
            # destination_obj_name = destination_type.split('.')[-1]
            # destination_pkg_name = destination_type.split('.')[-2]
            context['create_source_object'] = self.get_create_object(source_type, obj_name_under)
            context['create_destination_object'] = self.get_create_object(destination_type, obj_name_under)
            if context['create_destination_object'] == context['create_source_object']:
                context['create_destination_object'] = ''
            context['relationship_form_args'] = self.get_relationship_form_args(source_type, destination_type)
            source_tear_down = self.get_object_tear_down(source_type)
            destination_tear_down = self.get_object_tear_down(destination_type)
            context['tear_down_source_and_dest'] = source_tear_down
            if destination_tear_down != source_tear_down:
                context['tear_down_source_and_dest'] += destination_tear_down
        return context

    def get_create_object(self, object_type, relationship_object_name_under):
        if object_type in ['UNKNOWN', 'osid.authentication.Agent']:
            return ''
        elif object_type.split('.')[-1] in self.patterns['package_cataloged_objects_caps']:
            cat_name_under = self.patterns['package_catalog_under']
            object_name = object_type.split('.')[-1]
            object_name_under = camel_to_under(object_name)
            relationship_object_name = under_to_caps(relationship_object_name_under)
            return """
        create_form = request.cls.{0}_list[0].get_{1}_form_for_create([])
        create_form.display_name = '{2} for {3} Tests'
        create_form.description = '{2} for authz adapter tests for {3}'
        request.cls.{1} = request.cls.{0}_list[0].create_{1}(create_form)""".format(cat_name_under,
                                                                                    object_name_under,
                                                                                    object_name,
                                                                                    relationship_object_name)
        else:
            object_name = object_type.split('.')[-1]
            object_name_under = camel_to_under(object_name)
            pkg_name = object_type.split('.')[1]
            return """
        {0}_id = Id(authority='TEST', namespace='{1}.{2}', identifier='TEST')""".format(object_name_under,
                                                                                        pkg_name,
                                                                                        object_name)

    def get_relationship_form_args(self, source_type, destination_type):
        arg_list = []
        for object_type in [source_type, destination_type]:
            if object_type == 'UNKNOWN':
                pass
            elif object_type == 'osid.authentication.Agent':
                arg_list.append('AGENT_ID')
            elif object_type.split('.')[-1] in self.patterns['package_cataloged_objects_caps']:
                arg_list.append('request.cls.' + camel_to_under(object_type.split('.')[-1]) + '.ident')
            else:
                arg_list.append(camel_to_under(object_type.split('.')[-1]) + '_id')
        arg_list.append('[]')
        return ', '.join(arg_list)

    def get_object_tear_down(self, object_type):
        if object_type.split('.')[-1] in self.patterns['package_cataloged_objects_caps']:
            cat_name_under = self.patterns['package_catalog_under']
            object_name_under = camel_to_under(object_type.split('.')[-1])
            return '\n            request.cls.{0}_list[0].delete_{1}(request.cls.{1}.ident)'.format(cat_name_under, object_name_under)
        else:
            return ''

    def _get_method_sig(self, method, interface):
        method_sig = ''
        return method_sig

    def _update_module_imports(self, modules, interface):
        imports = modules[interface['category']]['imports']
        # self.append(imports, 'package this.is.not.where.package.path.goes')

        # Check to see if there are any additional inheritances required
        # by the implementation patterns.  THIS MAY WANT TO BE REDESIGNED
        # TO ALLOW INSERTING THE INHERITANCE IN A PARTICULAR ORDER.
        impl_class = self._load_impl_class(interface['shortname'])
        if hasattr(impl_class, 'inheritance_imports'):
            self.append(imports, getattr(impl_class, 'inheritance_imports'))

        self._append_pattern_imports(imports, interface)
        self._append_templated_imports(imports, interface)

    def _get_module_imports(self, modules, interface):
        if interface['shortname'] != 'osid':
            imports = [
                # put global imports here
            ]
        else:
            imports = []
        # self.append(imports, 'package this.is.not.where.package.path.goes')

        # Check to see if there are any additional inheritances required
        # by the implementation patterns.  THIS MAY WANT TO BE REDESIGNED
        # TO ALLOW INSERTING THE INHERITANCE IN A PARTICULAR ORDER.
        impl_class = self._load_impl_class(interface['shortname'])
        if hasattr(impl_class, 'inheritance_imports'):
            self.append(imports, getattr(impl_class, 'inheritance_imports'))

        self._append_pattern_imports(imports, interface)
        self._append_templated_imports(imports, interface)
        return imports

    def _compile_method(self, args, decorators, method_sig, method_doc, method_impl):
        if not method_impl.strip():
            return ''
        elif decorators:
            decorators = '\n'.join(decorators)
            return self._wrap('{0}\n{1}\n{2}\n{3}'.format(method_doc,
                                                          decorators,
                                                          method_sig,
                                                          method_impl))
        else:
            return self._wrap('{0}\n{1}\n{2}'.format(method_doc,
                                                     method_sig,
                                                     method_impl))

    def _wrap(self, text):
        return text

    # DON'T NEED FOR THIS BUILDER?
    def _write_module_string(self, write_file, module):
        write_file.write('{0}\n\n\n{1}'.format('\n'.join(module['imports']),
                                               module['body']).encode('utf-8'))

    def build_this_interface(self, interface):
        # return (('OsidObject' in interface['inherit_shortnames'] or
        #         'OsidRelationship' in interface['inherit_shortnames']) and
        #         'Subjugateable' not in interface['inherit_shortnames'] and
        #         self._build_this_interface(interface))
        if interface['shortname'] == 'SequenceRuleLookupSession':
            return False  # Until we figure out why its not building properly in services
        if interface['shortname'] in ['FunctionLookupSession', 'QualifierLookupSession']:
            return False  # Until we can properly implement these in json impls
        if interface['shortname'] in ['GradeEntryLookupSession']:
            return False  # GradeEntries can't be assigned to catalogs
        return (interface['shortname'].endswith('LookupSession') and
                'OsidCatalog' not in interface['inherit_shortnames'] and
                interface['shortname'][:-13] in objects_to_implement)

    def class_doc(self, interface):
        return ''

    def class_sig(self, interface, inheritance):
        return ''

    def make(self):
        self.make_osids()

    # This function is not used for this builder:
    def package_header(self):
        package_name = self._abc_pkg_path().split('/')[-1]
        return '"""TestAuthZ implementations of {} objects."""'.format(package_name)

    def module_doc(self, interface):
        package_name = self._abc_pkg_path().split('/')[-1]
        return '"""TestAuthZ implementations of {0}.{1}"""'.format(
            package_name,
            interface['shortname'].split('LookupSession')[0])

    def module_body(self, interface):
        inheritance = self._get_class_inheritance(interface)
        init_methods = self._make_init_methods(interface)
        methods = self.make_methods(interface)
        additional_methods = self._additional_methods(interface)
        additional_classes = self._additional_classes(interface)

        if additional_methods:
            methods += additional_methods

        if additional_classes:
            # extra newlines generated in self._additional_classes
            methods += additional_classes

        if init_methods:
            init_methods = self._wrap(init_methods)

        if methods:
            methods = '\n{0}\n'.format(methods)

        body = '\n\n{0}\n{1}\n{2}{3}'.format(self.class_sig(interface, inheritance),
                                             self._wrap(self.class_doc(interface)),
                                             init_methods,
                                             methods)
        return body

    def _make_osid(self, file_name):
        # Overrides for implementing java style
        # This function expects a file containing a json representation of an
        # osid package that was prepared by the mapper.
        # for sub-packages, append them to a base package file...
        with open(file_name, 'r') as read_file:
            self.package = json.load(read_file)

        if not self._package_to_be_implemented():
            return

        self._copy_package_helpers()

        print("Building authz tests for {1}".format(self._class, self.package['name']))

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
            '    ', interface['shortname'], 'inherits', interface['inherit_shortnames']
            if not self.build_this_interface(interface):
                continue
            print '    building -', interface['shortname']
            imports = self._get_module_imports(modules, interface)  # DONT NEED modules in this method?
            body = self.module_body(interface)
            if body.strip():
                self.write_class(interface, imports, body)

        # self.write_modules(modules)

    def write_class(self, interface, imports, body):
        # Writes one java class per file:
        if body != '' and len(interface['fullname'].split('.')) != 2:  # Hack to not build osid
            class_name = 'test_' + camel_to_under(interface['shortname'][:-13]) + '_authz'
            # module_dir = self._abc_pkg_path(abc=True) + '/authz_tests/'
            module_dir = self._app_name() + '/functional/test_authz/' + self._abc_pkg_name(abc=True) + '/'
            module_path = module_dir + class_name + '.py'
            # module_path = self._abc_module(class_name, extension='py')
            self._make_dir(module_dir, python=True)
            with open(module_path, 'wb') as write_file:
                write_file.write('{0}\n\n{1}\n{2}\n'.format(
                    self.module_doc(interface),
                    '\n'.join(imports),
                    body.strip()).encode('utf-8'))
