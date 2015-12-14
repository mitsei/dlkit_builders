from config import managers_to_implement, sessions_to_implement

from binder_helpers import camel_to_list
from build_controller import BaseBuilder
from interface_builders import InterfaceBuilder


class KitDocDLKitBuilder(InterfaceBuilder, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(KitDocDLKitBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir + '/dlkit'
        self._template_dir = self._abs_path + '/builders/kitosid_templates'

        self._excluded_packages = ['proxy', 'type']

        self._class = 'doc_dlkit'

    def _append_inherited_imports(self, imports, interface):
        # Iterate through any inherited interfaces and check if an import statement is
        # required and append to the appropriate module's import list.
        inherit_category = 'UNKNOWN_MODULE'
        for i in interface['inheritance']:
            inherit_category = self.get_interface_module(i['pkg_name'], i['name'], True)
            if (i['pkg_name'] == self.package['name'] and
                    inherit_category == interface['category']):
                pass
            else:
                import_str = 'from ..{0} import {1} as {0}_{1}'.format(self._abc_pkg_name(package_name=i['pkg_name'],
                                                                                          abc=False),
                                                                       inherit_category)

                if inherit_category != 'UNKNOWN_MODULE':
                    self.append(imports, import_str)
        return inherit_category

    def _build_as_service_interface(self, interface):
        # only build managers and catalogs
        basic_build = self._build_this_interface(interface)
        managers = ['managers', 'markers']
        catalogs = ['OsidSession', 'OsidObject', 'OsidCatalog', 'OsidList']
        catalogs += [self.patterns['package_catalog_caps']]
        catalogs += [self.patterns['package_catalog_caps'] + 'List']
        is_manager_or_cat = (interface['category'] in managers or
                             interface['shortname'] in catalogs)
        return basic_build and is_manager_or_cat

    def _empty_modules_dict(self):
        module = dict(manager=dict(imports=[], body=''),
                      services=dict(imports=[], body=''),
                      service_managers=dict(imports=[], body=''),
                      catalog=dict(imports=[], body=''),
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
        module[self.package['name']] = dict(imports=[], body='')
        return module

    def _get_class_inheritance(self, interface):
        inheritance = []

        # Iterate through any inherited interfaces and build the inheritance
        # list for this interface. Also, check if an import statement is
        # required and append to the appropriate module's import list.
        for i in interface['inheritance']:
            inherit_category = self.get_interface_module(i['pkg_name'], i['name'], True)

            if i['pkg_name'] == self.package['name'] and inherit_category == interface['category']:
                inheritance.append(i['name'])
            else:
                inheritance.append(i['pkg_name'] + '_' +
                                   inherit_category + '.' + i['name'])

        # Don't forget the OsidSession inheritance:
        if (('OsidManager' in interface['inherit_shortnames'] or
                interface['shortname'] == self.patterns['package_catalog_caps']) and
                self.package['name'] != 'osid'):
            inheritance.insert(1, 'osid_sessions.OsidSession')

        if inheritance:
            inheritance = '({})'.format(', '.join(inheritance))
        else:
            inheritance = ''

        return inheritance

    def _make_method(self, method, interface, patterns):
        args = ['self']
        method_impl = self._make_method_impl(method, interface, patterns)

        for arg in method['args']:
            args.append(arg['var_name'])

        method_sig = '{}def {}({}):'.format(self._ind,
                                            method['name'],
                                            ', '.join(args))

        method_doc = self._build_method_doc(method)

        return (self._wrap(method_sig) + '\n' +
                self._wrap(method_doc) + '\n' +
                self._wrap(method_impl))

    def _services_module_body(self, interface):
        additional_methods = self._additional_methods(interface)
        inheritance = self._get_class_inheritance(interface)
        init_methods = self._make_init_methods(interface)
        methods = self.make_methods(interface, self.patterns)
        body = ''

        # Add all the appropriate manager related session methods to the manager interface
        # Add all the appropriate catalog related session methods to the catalog interface
        if any(m in interface['inherit_shortnames'] for m in ['OsidManager', 'OsidProfile']):
            new_methods, new_imports = self._grab_service_methods(self._is_manager_session)
            methods += new_methods
        # Add all the appropriate catalog related session methods to the catalog interface
        elif interface['shortname'] == self.patterns['package_catalog_caps']:
            new_methods, new_imports = self._grab_service_methods(self._is_catalog_session)
            methods += new_methods

        if not init_methods.strip() and not methods.strip():
            init_methods = '{0}pass'.format(self._ind)

        if additional_methods:
            methods += '\n' + additional_methods

        body = '{0}\n{1}\n{2}\n{3}\n\n\n'.format(self.class_sig(interface, inheritance),
                                                 self._wrap(self.class_doc(interface)),
                                                 self._wrap(init_methods),
                                                 methods)
        return body

    def _update_module_imports(self, modules, interface):
        imports = modules[interface['category']]['imports']
        pkg_imports = modules[self.package['name']]['imports']

        self._append_inherited_imports(imports, interface)
        self._append_inherited_imports(pkg_imports, interface)

        # Don't forget the OsidSession inheritance:
        if (('OsidManager' in interface['inherit_shortnames'] or
                interface['shortname'] == self.patterns['package_catalog_caps']) and
                self.package['name'] != 'osid'):
            self.append(imports, 'from ..osid import sessions as osid_sessions')
            self.append(pkg_imports, 'from ..osid import sessions as osid_sessions')

    def build_this_interface(self, interface):
        # return True
        return (not interface['shortname'].endswith('ProxyManager') and
                self._build_this_interface(interface))

    def build_this_method(self, interface, method):
        return True

    def make(self):
        self.make_osids(build_abc=False)

    def module_body(self, interface):
        inheritance = self._get_class_inheritance(interface)
        return '{0}\n{1}\n{2}\n{3}\n\n\n'.format(self.class_sig(interface, inheritance),
                                                 self.class_doc(interface),
                                                 self._additional_methods(interface),
                                                 self.make_methods(interface, None))

    def update_module_body(self, modules, interface):
        modules[interface['category']]['body'] += self.module_body(interface)
        if self._build_as_service_interface(interface):
            modules[self.package['name']]['body'] += self._services_module_body(interface)

    def write_license_file(self):
        with open(self._abc_module('license'), 'w') as write_file:
            write_file.write((self._utf_code + '\"\"\"' +
                              self.package['title'] + '\n' +
                              self.package['name'] + ' version ' +
                              self.package['version'] + '\n\n' +
                              self.package['copyright'] + '\n\n' +
                              self.package['license'] + '\n\n\"\"\"').encode('utf-8') +
                             '\n')

    def write_modules(self, modules):
        summary = u'{0}\"\"\"{1}\n{2} version {3}\n\n{4}\n\n\"\"\"\n'.format(self._utf_code,
                                                                             self.package['title'],
                                                                             self.package['name'],
                                                                             self.package['version'],
                                                                             self.package['summary']).encode('utf-8')
        ##
        # Finally, iterate through the completed package module structure and
        # write out both the import statements and class definitions to the
        # appropriate module for this package.
        for module in modules:
            if modules[module]['body'] is not None and modules[module]['body'].strip() != '':
                with open(self._abc_module(module), 'w') as write_file:
                    write_file.write('{0}\n\n\n{1}'.format('\n'.join(modules[module]['imports']),
                                                           modules[module]['body']).decode('utf-8').encode('utf-8'))
                with open('{0}/services/{1}.py'.format(self._app_name(),
                                                       self.package['name']), 'w') as write_file:
                    write_file.write('{0}{1}\n\n\n{2}'.format(summary,
                                                              '\n'.join(modules[self.package['name']]['imports']),
                                                              modules[self.package['name']]['body']).decode('utf-8').encode('utf-8'))


##
# This is the entry point for making django-based python classes for
# the osids. It processes all of the osid maps in the package maps
# directory.
def make_kitdocs(build_abc = False, re_index = False, re_map = False):
    from abcbinder import make_abcosids
    if build_abc:
        make_abcosids(re_index, re_map)
    for json_file in os.listdir(pkg_maps_dir):
        if json_file.endswith('.json'):
            make_kitdoc(pkg_maps_dir + '/' + json_file)

##
# This function expects a file containing a json representation of an
# osid package that was prepared by the mapper.
def make_kitdoc(file_name):
    from binder_helpers import get_interface_module

    read_file = open(file_name, 'r')
    package = json.load(read_file)
    read_file.close()

    if package['name'] not in packages_to_implement:
        return
    if package['name'] in excluded_packages:
        return
    print "--> Build DLKit Doc Package:", package['name']

    importStr = ''
    bodyStr = ''
    module_name = None
    ##
    # The map structure for the modules to be created by this function.
    # Each module will get a body string that holds the class and method
    # signatures for the particular interface category, and a list of 
    # for the modules that the module's classes may inherit.
    modules = dict(manager = dict(imports = [], body = ''),
                   catalog = dict(imports = [], body = ''),
                   properties = dict(imports = [], body = ''),
                   objects = dict(imports = [], body = ''),
                   queries = dict(imports = [], body = ''),
                   query_inspectors = dict(imports = [], body = ''),
                   searches = dict(imports = [], body = ''),
                   search_orders = dict(imports = [], body = ''),
                   rules = dict(imports = [], body = ''),
                   metadata = dict(imports = [], body = ''),
                   receivers = dict(imports = [], body = ''),
                   sessions = dict(imports = [], body = ''),
                   managers = dict(imports = [], body = ''),
                   records = dict(imports = [], body = ''),
                   primitives = dict(imports = [], body = ''),
                   markers = dict(imports = [], body = ''),
                   others_please_move = dict(imports = [], body = ''))
#    modules[fix_reserved_word(package['name'])] = dict(imports = [], body = '')
    modules[package['name']] = dict(imports = [], body = '')

    if not doc_root_pkg:
        ##
        # Check if an app directory and service subdirectory already exist.  
        # If not, create them  This code specifically splits out the osid 
        # packages in a Django app environment, one Django app per osid package.
        from django.core.management import call_command
        if not os.path.exists(app_name(package['name'])):
            call_command('startapp', app_name(package['name']))
    #    if not os.path.exists(app_name(package['name']) + '/' + 
    #                          pkg_name(package['name'])):
    #        os.system('mkdir '+ app_name(package['name']) + '/' + 
    #                  pkg_name(package['name']))
    #        os.system('touch ' + app_name(package['name']) + '/' + 
    #                      pkg_name(package['name']) + '/__init__.py')
    else:
        ##
        # Check if a directory already exists for the docs.  If not,
        # create one and initialize as a python package.
        if not os.path.exists(app_name(package['name'])):
            os.system('mkdir '+ app_name(package['name']))
            os.system('touch ./' + app_name(package['name']) + '/__init__.py')



            
    ##
    # Write the osid license documentation file.
    write_file = open(app_name(package['name']) + '/' + 
                     pkg_name(package['name']) + '/license.py', 'w')
    write_file.write((utf_code + '\"\"\"' +
                      package['title'] + '\n' +
                      package['name'] + ' version ' +
                      package['version'] + '\n\n'+
                      package['copyright'] + '\n\n' +
                      package['license'] + '\n\n\"\"\"').encode('utf-8'))
    write_file.close

    """
    ##
    # Write the summary documentation for this package.
    write_file = open(app_name(package['name']) + '/' + 
                      pkg_name(package['name']) + '/summary.py', 'w')
    write_file.write((utf_code + '\"\"\"' +
                      package['title'] + '\n' +
                      package['name'] + ' version ' +
                      package['version'] + '\n\n'+
                      package['summary'] + '\n\n\"\"\"').encode('utf-8'))
    write_file.close"""
    
    

    
    ##
    # Copy settings and types and other files from the kit tamplates into the
    # appropriate implementation directories
    if os.path.exists('./builders/kitdoc_templates/' +
                      package['name'] + '_helpers'):
        #print 'FOUND:', package['name'] + '_helpers'
        for helper_file in os.listdir('./builders/kitdoc_templates/' +
                                        package['name'] + '_helpers'):
            if helper_file.endswith('.py'):
                os.system('cp ./builders/kitdoc_templates/' +
                          package['name'] + '_helpers/' + helper_file + ' ' +
                          app_name(package['name']) +
                          '/' + helper_file)
    
    """
    ##
    # Write profile.py file for this package.
    profile_str = make_profile_py(package)
    writeFile = open(app_name(package['name']) + '/' +
                     pkg_name(package['name']) + '/profile.py', 'w')
    writeFile.write(profile_str)
    writeFile.close()
    """

    ##
    # Get the pattern map for this osid package.
    read_file = open('builders/pattern_maps/' + 
                      package['name'] + '.json', 'r')
    patterns = json.load(read_file)
    read_file.close()

    ##
    # Add manager and catalog session checks to patterns for later use
    for inf in package['interfaces']:
        patterns[camel_to_under(inf['shortname']) + 
                '.is_manager_session'] = is_manager_session(inf, patterns, package['name'])
        patterns[camel_to_under(inf['shortname']) + 
                '.is_catalog_session'] = is_catalog_session(inf, patterns, package['name'])

    exceptions = []

    excepted_osid_categories = ['properties',
                                'query_inspectors',
                                'receivers',
                                'search_orders',
                                'searches',]

    ##
    # The real work starts here.  Iterate through manager and catalog 
    # interfaces only to build the 'managers' and some 'objects' modules.
    for interface in package['interfaces']:
        if ((interface['category'] == 'managers' or
            interface['shortname'] == patterns['package_catalog_caps'] or
            interface['shortname'] == patterns['package_catalog_caps'] + 'List' or
            interface['shortname'] in ['OsidSession', 'OsidObject', 'OsidCatalog', 'OsidList'] or
            interface['category'] == 'markers')):

            """
            if ('OsidManager' in interface['inherit_shortnames'] or
                'OsidProfile' in interface['inherit_shortnames'] or
                'OsidProxyManager' in interface['inherit_shortnames']):
                module_name = 'services'
            elif interface['shortname'] == patterns['package_catalog_caps']:
                module_name = 'catalog'
            else:"""
#            module_name = interface['category']
#            module_name = fix_reserved_word(package['name'])
            module_name = package['name']
            
            ##
            # Check to see if this interface is meant to be implemented.
            if package['name'] != 'osid' and interface['category'] not in excepted_osid_categories:
                if flagged_for_implementation(interface, 
                        sessions_to_implement, objects_to_implement, variants_to_implement):
                    if interface['shortname'] in exceptions:
                        continue
                    if interface['shortname'].endswith('ProxyManager'):
                        continue
                    else:
                        pass
                else:
                    continue

            if interface['category'] in excepted_osid_categories:
                continue

            inheritance = []

            """
            ##
            # Seed the inheritance list with this interface's abc_osid
            inheritance = ['abc_' + package['name'] + '_' +
                           interface['category'] + '.' +
                           interface['shortname']]
            ##
            # Check to see if there are any additinal inheritances required
            # by the implementation patterns.
            impl_class = load_impl_class(package['name'], interface['shortname'])
            if hasattr(impl_class, 'inheritance'):
                inheritance = inheritance + getattr(impl_class, 'inheritance')

            ##
            # And make sure there is a corresponding import statement for this
            # interface's abc_osid and associated module/category name.
            import_str = ('from ' + abc_app_name(package['name']) + '.' +
                           abc_pkg_name(package['name']) + ' import ' +
                           interface['category'] + ' as ' + 
                           'abc_' + package['name'] + '_' + interface['category'])
            if not import_str in modules[module_name]['imports']:
                modules[module_name]['imports'].append(import_str)

            ##
            # If this is the OsidManager interface then include all the
            # abc osids and imports for the Manager related Sessions:
            if 'OsidManager' in interface['inherit_shortnames']:
                for inf in package['interfaces']:
                    if is_manager_session(inf, patterns, package['name']):
                        if inf['shortname'].endswith('SearchSession'):
                            inheritance.insert(1, 'abc_' + package['name'] + '_' +
                                               inf['category'] + '.' +
                                               inf['shortname'])
                        else:
                            inheritance.append('abc_' + package['name'] + '_' +
                                               inf['category'] + '.' +
                                               inf['shortname'])
                        import_str = ('from ' + abc_app_name(package['name']) + '.' +
                                      abc_pkg_name(package['name']) + ' import ' +
                                      inf['category'] + ' as ' + 
                                      'abc_' + package['name'] + '_' + inf['category'])
                        if not import_str in modules[module_name]['imports']:
                            modules[module_name]['imports'].append(import_str)

            ##
            # If this is the catalog interface then include all the
            # abc osids and imports for the catalog related Sessions:
            if interface['shortname'] == patterns['package_catalog_caps']:
                for inf in package['interfaces']:
                    if is_catalog_session(inf, patterns, package['name']):
                        if inf['shortname'].endswith('SearchSession'):
                            inheritance.insert(1, 'abc_' + package['name'] + '_' +
                                               inf['category'] + '.' +
                                               inf['shortname'])
                        else:
                            inheritance.append('abc_' + package['name'] + '_' +
                                               inf['category'] + '.' +
                                               inf['shortname'])
                        import_str = ('from ' + abc_app_name(package['name']) + '.' +
                                      abc_pkg_name(package['name']) + ' import ' +
                                      inf['category'] + ' as ' + 
                                      'abc_' + package['name'] + '_' + inf['category'])
                        if not import_str in modules[module_name]['imports']:
                            modules[module_name]['imports'].append(import_str)"""

            ##
            # Interate through any inherited interfaces and build the inheritance
            # list for this interface. Also, check if an import statement is
            # required and append to the appropriate module's import list.
            for i in interface['inheritance']:
                unknown_module_protection = ''
                inherit_category = get_interface_module(i['pkg_name'], i['name'], True)
                if inherit_category == 'UNKNOWN_MODULE':
                    unknown_module_protection = '\"\"\"'
#                if (i['pkg_name'] == package['name'] and
#                      inherit_category == interface['category']):
                if (i['pkg_name'] == package['name']):
                    inheritance.append(i['name'])
                else:
#                    inheritance.append(unknown_module_protection + 
#                                       app_name(i['pkg_name']) + '_' +
#                                       inherit_category + '.' + i['name'] +
#                                       unknown_module_protection)
                    inheritance.append(i['pkg_name']+ '_' +
                                       inherit_category + '.' + i['name'])
#                    import_str = ('from ' + app_name(i['pkg_name']) +
#                                  ' import ' + inherit_category + ' as ' +
#                                  app_name(i['pkg_name']) + '_' + inherit_category)
                    import_str = ('from ..' + i['pkg_name'] + 
                                  ' import ' + inherit_category + ' as ' +
                                  i['pkg_name'] + '_' + inherit_category)

                    if (import_str not in modules[module_name]['imports'] and
                        inherit_category != 'UNKNOWN_MODULE'):
                        modules[module_name]['imports'].append(import_str)

            ##
            # Don't forget the OsidSession inheritance:
            if (('OsidManager' in interface['inherit_shortnames'] or
                interface['shortname'] == patterns['package_catalog_caps']) and
                package['name'] != 'osid'):
                inheritance.insert(1, 'osid_sessions.OsidSession')
                import_str = 'from ..osid import sessions as osid_sessions'
                if import_str not in modules[module_name]['imports']: 
                    modules[module_name]['imports'].append(import_str)

            ##
            # And don't forget the osid_error import:
            #import_str = 'from .osid_errors import Unimplemented, IllegalState, OperationFailed'
            #if import_str not in modules[module_name]['imports']: 
            #    modules[module_name]['imports'].append(import_str)

            ##
            # Note that the following re-assigns the inheritance variable from a 
            # list to a string.
            if inheritance:
                inheritance = '(' + ', '.join(inheritance) + ')'
            else:
                inheritance = ''


            ##
            # Inspect the class doc string for headline + body and create
            # appropriate doc string style. Trying to conform to PEP 257 as 
            # much as the source osid doc will allow.
            if interface['doc']['body'].strip() == '':
                class_doc = ('    \"\"\"' + interface['doc']['headline'] + '\"\"\"')
            else:
                class_doc = ('    \"\"\"' + interface['doc']['headline'] + '\n\n' +
                                        interface['doc']['body'] + '\n\n    \"\"\"')
            
            ##
            # Build the interface implementation
            class_sig = 'class ' + interface['shortname'] + inheritance + ':'
            init_methods = make_init_methods(interface['shortname'], package, patterns)
            methods = make_methods(package['name'], interface, patterns) + '\n\n'

            ##
            # Add all the appropriate manager related session methods to the manager interface
            if ('OsidManager' in interface['inherit_shortnames'] or
                'OsidProxyManager' in interface['inherit_shortnames']):
                patterns['implemented_view_methods'] = []
                for inf in package['interfaces']:
                    if is_manager_session(inf, patterns, package['name']):
                            methods = methods + '\n##\n# The following methods are from ' + inf['fullname'] + '\n\n'
                            methods = methods + make_methods(package['name'], inf, patterns) + '\n\n'

            ##
            # Add all the appropriate catalog related session methods to the catalog interface
            if interface['shortname'] == patterns['package_catalog_caps']:
                patterns['implemented_view_methods'] = []
                for inf in package['interfaces']:
                    if is_catalog_session(inf, patterns, package['name']):
                            methods = methods + '\n##\n# The following methods are from ' + inf['fullname'] + '\n\n'
                            methods = methods + make_methods(package['name'], inf, patterns) + '\n\n'

            if not init_methods.strip() and not methods.strip():
                init_methods = '    pass'

            modules[module_name]['body'] = (
                              modules[module_name]['body'] + 
                              class_sig + '\n' +
                              #class_doc + '\n' +
                              init_methods + '\n' +
                              methods + '\n\n')
    ##
    # Add catalogs class
    if patterns['package_catalog_caps'] != 'NoCatalog':
        catalogs_plural = make_plural(patterns['package_catalog_caps'])
        modules[fix_reserved_word(package['name'])]['body'] = modules[fix_reserved_word(package['name'])]['body'] + (
'class ' + catalogs_plural + '(' + package['name'].title() + 'Manager):\n' +
'    pass\n\n\n')

    ##
    # Add summary doc
    summary = (utf_code + '\"\"\"' +
               package['title'] + '\n' +
               package['name'] + ' version ' +
               package['version'] + '\n\n'+
               package['summary'] + '\n\n\"\"\"\n')
    
    ##
    # Finally, iterate through the completed package module structure and
    # write out both the import statements and class definitions to the
    # appropriate module for this package.
    for module in modules:
        if modules[module]['body'].strip() != '':
#            write_file = open(app_name(package['name']) + '/' + 
#                              pkg_name(package['name']) + '/' +
#                              '_'.join(module.split('.')) + '.py', 'w')
            write_file = open(app_name(package['name']) + '/' + 
                              '_'.join(module.split('.')) + '.py', 'w')
            write_file.write((summary + '\n'.join(modules[module]['imports']) + '\n\n\n' +
                              modules[module]['body']).encode('utf-8'))
            write_file.close

##
# Determine if the interface represents a manager related session
def is_manager_session(interface, patterns, package_name):
    is_manager_session = False
#    if (interface['category'] == 'sessions' and
#        (not 'get_' + patterns['package_catalog_under'] in interface['method_names'] and
#        not interface['shortname'].endswith('SearchSession') or
#        interface['shortname'].startswith(patterns['package_catalog_caps']))):
    if package_name in ['type']:
        is_manager_session = True
    elif (interface['category'] == 'sessions' and
        interface['shortname'].startswith(patterns['package_catalog_caps'])):
        is_manager_session = True
    return is_manager_session

##
# Determine if the interface represents a manager related session
def is_catalog_session(interface, patterns, package_name):
    is_catalog_session = False
#    if (interface['category'] == 'sessions' and
#        ('get_' + patterns['package_catalog_under'] in interface['method_names'] or
#        interface['shortname'].endswith('SearchSession')) and
#        not interface['shortname'].startswith(patterns['package_catalog_caps'])):
    if (interface['category'] == 'sessions' and
        not interface['shortname'].startswith(patterns['package_catalog_caps']) and
        package_name not in ['type']):
        is_catalog_session = True
    return is_catalog_session

def load_impl_class(package_name, interface_name):
    ##
    # Try loading implentations for this interface
    impl_class = None
    try:
        impls = __import__('builders.kitdoc_templates.' +
                                     package_name,
                                     fromlist = [interface_name])
    except (ImportError, KeyError):
        pass
    else:
        if hasattr(impls, interface_name):
            impl_class = getattr(impls, interface_name)
    return impl_class

def make_init_methods(interface_name, package, patterns):
    from binder_helpers import camel_to_under
    templates = None
    init_pattern = ''
    defaults = ''
    initers = ''
    object_name = ''
    cat_name_caps = patterns['package_catalog_caps']
    cat_name_under = patterns['package_catalog_under']
    obj_view_methods = ''
    obj_view_initers = ''
    impl_class = load_impl_class(package['name'], interface_name)
    if hasattr(impl_class, 'init'):
        return getattr(impl_class, 'init')
    elif interface_name + '.init_pattern' in patterns:
        init_pattern = patterns[interface_name + '.init_pattern']
        try:
            templates = __import__('builders.kitdoc_templates.' +
                                    init_pattern.split('.')[0], 
                                    globals(), locals(), 
                                    [init_pattern.split('.')[-1]])
        except ImportError:
            return ''
    else:
        return ''

    ##
    # Check for any special data initializations and call the appropriate makers
    # to assemble them.
    if init_pattern == 'resource.Bin':
        initers = ''
        ## THESE ARE NO LONGER NEEDED ?!?!
        method_tmp = string.Template("""
    def use_comparative_${obj}_view():
        self._${obj}_view = self.COMPARATIVE
        for session in self._provider_sessions:
            try:
                session.use_comparative_${obj}_view()
            except AttributeError():
                pass

    def use_plenary_${obj}_view():
        self._${obj}_view = self.PLENARY
        for session in self._provider_sessions:
            try:
                session.use_plenary_${obj}_view()
            except AttributeError():
                pass
""")
        initer_tmp = string.Template("""
        self._${obj}_view = self.COMPARATIVE""")
        
        for obj in patterns['package_objects_under'] + patterns['package_relationships_under']:
            obj_view_methods = obj_view_methods + method_tmp.substitute({'obj': obj})
            obj_view_initers = obj_view_initers + initer_tmp.substitute({'obj': obj})

        ## ALSO NEED TO DO Relationship Effective Views !!!

    elif init_pattern == 'resource.BinForm':
        initers = ''
        object_name = interface_name[:-4]
    elif init_pattern == 'resource.ResourceLookupSession':
        initers = ''
        object_name = interface_name[:-13]
    elif init_pattern == 'resource.ResourceAdminSession':
        initers = ''
        object_name = interface_name[:-12]
    elif init_pattern == 'resource.Resource':
        initers = ''
    elif init_pattern == 'resource.ResourceForm':
        object_name = interface_name[:-4]
        initers = ''

    if hasattr(templates, init_pattern.split('.')[-1]):
        template_class = getattr(templates, init_pattern.split('.')[-1])
        if hasattr(template_class, 'init_template'):
            template = string.Template(getattr(template_class, 'init_template'))
            return template.substitute({'app_name': app_name(package['name']),
                                        'kitpkg_name': pkg_name(package['name']),
                                        'pkg_name': package['name'],
                                        'pkg_name_caps': package['name'].title(),
                                        'pkg_name_upper': package['name'].upper(),
                                        'interface_name': interface_name,
                                        'interface_name_title': interface_name.title(),
                                        'initers': initers,
                                        'object_name': object_name,
                                        'object_name_under': camel_to_under(object_name),
                                        'cat_name': cat_name_caps,
                                        'cat_name_under': cat_name_under,
                                        'obj_view_methods': obj_view_methods,
                                        'obj_view_initers': obj_view_initers})
        else:
            return ''
    else:
        return ''

def make_methods(package_name, interface, patterns):
    from binder_helpers import SkipMethod, fix_reserved_word
    body = []
    for method in interface['methods']:

        if (interface['category'] == 'managers' and
                package_name != 'osid' and
                interface['shortname'].endswith('Manager')  and
                method['name'].startswith('get') and
                'session' in method['name'] and
                method['return_type'].split('.')[-1] not in sessions_to_implement):
            print "excepting:", interface['shortname'], method['name']
            continue
        if (interface['category'] == 'managers' and
                package_name != 'osid' and
                interface['shortname'].endswith('Profile')  and
                method['name'].startswith('supports_') and
                under_to_caps(method['name'][9:]) + 'Session' not in sessions_to_implement):
            print "excepting:", interface['shortname'], method['name']
            continue
        if (interface['category'] == 'sessions' and
                (method['name'] == 'get_' + patterns['package_catalog_under'] + '_id' or
                 method['name'] == 'get_' + patterns['package_catalog_under'])):
            continue

        try:
            body.append(make_method(package_name, method, interface['shortname'], patterns))
        except SkipMethod:
            pass
        else:
            ##
            # Here is where we add the Python properties stuff:
            if method['name'].startswith('get_') and method['args'] == []:
                body.append('    ' + fix_reserved_word(method['name'][4:]) + 
                        ' = property(fget=' + method['name'] + ')')
            elif method['name'].startswith('set_') and len(method['args']) == 1:
                if ('    ' + fix_reserved_word(method['name'][4:]) + ' = property(fdel=clear_' + method['name'][4:] + ')') in body:
                    body.remove('    ' + fix_reserved_word(method['name'][4:]) + ' = property(fdel=clear_' + method['name'][4:] + ')')
                    body.append('    ' + fix_reserved_word(method['name'][4:]) + 
                            ' = property(fget=' + method['name'] +
                            ', fdel=clear_' + method['name'][4:] + ')')
                else:
                    body.append('    ' + fix_reserved_word(method['name'][4:]) + 
                            ' = property(fset=' + method['name'] + ')')
            elif method['name'].startswith('clear_') and method['args'] == []:
                if ('    ' + fix_reserved_word(method['name'][6:]) + ' = property(fset=set_' + method['name'][6:] + ')') in body:
                    body.remove('    ' + fix_reserved_word(method['name'][6:]) + ' = property(fset=set_' + method['name'][6:] + ')')
                    body.append('    ' + fix_reserved_word(method['name'][6:]) + 
                            ' = property(fget=set_' + method['name'][6:] +
                            ', fdel=' + method['name'] + ')')
                else:
                    body.append('    ' + method['name'][6:] + 
                            ' = property(fdel=' + method['name'] + ')')
            if method['name'] == 'get_id':
                    body.append('    ident = property(fget=' + method['name'] + ')')
            if method['name'] == 'get_identifier_namespace':
                    body.append('    namespace = property(fget=' + method['name'] + ')')
                    
    return '\n\n'.join(body)
    
def make_method(package_name, method, interface_name, patterns):
    args = ['self']
    method_doc = ''
    method_impl = make_method_impl(package_name, method, interface_name, patterns)

    for arg in method['args']:
        args.append(arg['var_name'])
    method_sig = ('    def ' + method['name'] + '(' +
                ', '.join(args) + '):')

    method_doc = ''
    ##
    # Uncomment the following for readable doc details:
#    detail_docs = filter(None, [method['arg_doc'].strip('\n'),
#                                method['return_doc'].strip('\n'),
#                                method['error_doc'].strip('\n'),
#                                method['compliance_doc'].strip('\n'),
#                                method['impl_notes_doc'].strip('\n')])
    ##
    # Uncomment the following for Sphinx-style doc details
    detail_docs = filter(None, [method['sphinx_param_doc'].strip('\n'),
                                method['sphinx_return_doc'].strip('\n'),
                                method['sphinx_error_doc'].strip('\n')])

    if method['doc']['body'].strip() == '' and not detail_docs:
        method_doc = ('        \"\"\"' + 
                      method['doc']['headline'] + 
                      '\"\"\"')
    else:
        if method['doc']['body']:
            method['doc']['body'] = method['doc']['body'] + '\n'
        method_doc = ('        \"\"\"' + method['doc']['headline'] + 
                      '\n' +
                      method['doc']['body'] + '\n' +
                      '\n'.join(detail_docs) + '\n\n        \"\"\"')


## Use this return statement for method docs
    return (method_sig + '\n' + method_doc + '\n' + method_impl)
## Use this return statement to eliminate method docs
#    return (method_sig + '\n' + method_impl)
    
def make_method_impl(package_name, method, interface_name, patterns):
    from binder_helpers import camel_to_under
    from binder_helpers import get_interface_module
    from binder_helpers import get_pkg_name
    from binder_helpers import SkipMethod
    impl = ''
    pattern = ''
    kwargs = {}
    templates = None

    if ('implemented_view_methods' in patterns and
       method['name'] in patterns['implemented_view_methods']):
        raise SkipMethod()
    elif 'implemented_view_methods' in patterns:
        patterns['implemented_view_methods'].append(method['name'])

    
    if interface_name + '.' + method['name'] in patterns:
        pattern = patterns[interface_name + '.' + method['name']]['pattern']
        kwargs = patterns[interface_name + '.' + method['name']]['kwargs']

    impl_class = load_impl_class(package_name, interface_name)

    template_class = None
    if pattern:
        try: 
            templates = __import__('builders.kitdoc_templates.' +
                                   pattern.split('.')[0],
                                   fromlist = [pattern.split('.')[-2]])
        except (ImportError, KeyError):
            pass
        else:
            if hasattr(templates, pattern.split('.')[-2]):
                template_class = getattr(templates, pattern.split('.')[-2])

    ##
    # Check if this method is marked to be skipped (the assumption
    # is that it will be implemented elsewhere, perhaps in an init.)
    if (impl_class and 
        hasattr(impl_class, method['name']) and
        getattr(impl_class, method['name']) is None):
        raise SkipMethod()

    ##
    # Set the template flag string that will be used for identifying the 
    # appropriate template implementations in cases where there are differing
    # requirements:
    template_flag = '_template'
    if interface_name.endswith('Manager') and 'session' in method['name']:
        if patterns[method['name'][4:].split('_for_')[0] + '.is_manager_session']:
            template_flag = '_managertemplate'
        elif patterns[method['name'][4:].split('_for_')[0] + '.is_catalog_session']:
            template_flag = '_catalogtemplate'

    ##
    # Check if there is a 'by hand' implementation available for this method
    if (impl_class and 
        hasattr(impl_class, method['name'])):
        impl = getattr(impl_class, method['name']).strip('\n')

    ##
    # If there is no 'by hand' implementation, get the template for the 
    # method implementation that serves as the pattern, if one exixts.
    elif (template_class and
          hasattr(template_class, pattern.split('.')[-1] + template_flag)):
        if getattr(template_class, pattern.split('.')[-1] + template_flag) is None:
            raise SkipMethod()
        template_str = getattr(template_class, pattern.split('.')[-1] + 
                                template_flag).strip('\n')
        template = string.Template(template_str)
        
        ##
        # Add keyword arguments to template kwargs that are particuler
        # to the osid kit implementation
        kwargs['app_name'] = app_name(kwargs['package_name'])
        kwargs['djpkg_name'] = pkg_name(kwargs['package_name'])
        kwargs['abcapp_name'] = abc_app_name(kwargs['package_name'])
        kwargs['abcpkg_name'] = abc_pkg_name(kwargs['package_name'])
        kwargs['interface_name_under'] = camel_to_under(kwargs['interface_name'])
        kwargs['package_name_caps'] = package_name.title()
        
        if 'arg0_type_full' in kwargs:
            kwargs['arg0_type'] = kwargs['arg0_type_full'].split('.')[-1].strip('[]')
            kwargs['arg0_abcapp_name'] = abc_app_name(get_pkg_name(kwargs['arg0_type_full'].strip('[]')))
            kwargs['arg0_abcpkg_name'] = abc_pkg_name(get_pkg_name(kwargs['arg0_type_full'].strip('[]')))
            kwargs['arg0_module'] = get_interface_module(
                                    get_pkg_name(kwargs['arg0_type_full']),
                                    kwargs['arg0_type_full'].split('.')[-1].strip('[]'))
        if 'arg1_type_full' in kwargs:
            kwargs['arg1_type'] = kwargs['arg1_type_full'].split('.')[-1].strip('[]')
            kwargs['arg1_abcapp_name'] = abc_app_name(get_pkg_name(kwargs['arg1_type_full'].strip('[]')))
            kwargs['arg1_abcpkg_name'] = abc_pkg_name(get_pkg_name(kwargs['arg1_type_full'].strip('[]')))
            kwargs['arg1_module'] = get_interface_module(
                                    get_pkg_name(kwargs['arg1_type_full']),
                                    kwargs['arg1_type_full'].split('.')[-1].strip('[]'))
        if 'arg2_type_full' in kwargs:
            kwargs['arg2_type'] = kwargs['arg2_type_full'].split('.')[-1].strip('[]')
            kwargs['arg2_abcapp_name'] = abc_app_name(get_pkg_name(kwargs['arg2_type_full'].strip('[]')))
            kwargs['arg2_abcpkg_name'] = abc_pkg_name(get_pkg_name(kwargs['arg2_type_full'].strip('[]')))
            kwargs['arg2_module'] = get_interface_module(
                                    get_pkg_name(kwargs['arg2_type_full']),
                                    kwargs['arg2_type_full'].split('.')[-1].strip('[]'))
        if 'arg3_type_full' in kwargs:
            kwargs['arg3_type'] = kwargs['arg3_type_full'].split('.')[-1].strip('[]')
            kwargs['arg3_abcapp_name'] = abc_app_name(get_pkg_name(kwargs['arg3_type_full'].strip('[]')))
            kwargs['arg3_abcpkg_name'] = abc_pkg_name(get_pkg_name(kwargs['arg3_type_full'].strip('[]')))
            kwargs['arg3_module'] = get_interface_module(
                                    get_pkg_name(kwargs['arg3_type_full']),
                                    kwargs['arg3_type_full'].split('.')[-1].strip('[]'))
        if 'return_type_full' in kwargs:
            kwargs['return_type'] = kwargs['return_type_full'].split('.')[-1]
            kwargs['return_pkg'] = get_pkg_name(kwargs['return_type_full'])
            kwargs['return_module'] = get_interface_module(
                                      get_pkg_name(kwargs['return_type_full']), 
                                      kwargs['return_type_full'].split('.')[-1])
        if 'return_pkg' in kwargs:
            kwargs['return_app_name'] = app_name(kwargs['return_pkg'])
            kwargs['return_djpkg_name'] = pkg_name(kwargs['return_pkg'])
            kwargs['return_pkg_title'] = kwargs['return_pkg'].title()
        if 'object_name' in kwargs and 'package_name' in kwargs:
            kwargs['object_app_name'] = app_name(kwargs['package_name'])
            kwargs['object_djpkg_name'] = pkg_name(kwargs['package_name'])
            kwargs['object_module'] = get_interface_module('package_name', 'object_name')
        if 'return_type' in kwargs:
            kwargs['return_type_under'] = camel_to_under(kwargs['return_type'])
        if 'object_name' in kwargs:
            kwargs['object_name_under'] = camel_to_under(kwargs['object_name'])
        if 'cat_name' in kwargs:
            kwargs['cat_name_under'] = camel_to_under(kwargs['cat_name'])
            kwargs['cat_name_lower'] = kwargs['cat_name'].lower()
        if ('return_pkg' in kwargs and 'return_module' in kwargs and
            kwargs['package_name'] == kwargs['return_pkg'] and
            kwargs['module_name'] == kwargs['return_module']):
            kwargs['import_str'] = ''
        elif ('package_name' in kwargs and 'return_pkg' in kwargs and
              'return_type' in kwargs and 'return_module' in kwargs):
            kwargs['import_str'] = ('        from ' +
                                    kwargs['return_app_name'] + '.' +
                                    kwargs['return_djpkg_name'] + '.' +
                                    kwargs['return_module'] + ' import ' +
                                    kwargs['return_type'] + '\n')

# Uncomment next line to identify on which method a key error is occuring
        #print interface_name, method['name']

        impl = template.substitute(kwargs).strip('\n')
    if impl == '':
        if method['return_type'].strip():
            return '        return # ' + method['return_type']
        else:
            return '        pass'
    else:
        return impl
        

def make_profile_py(package):
    import string
    import datetime
    from importlib import import_module
    
    osid_package = package['name']
    try:
        old_profile = import_module(app_name(package['name']) + '.' +
                                    pkg_name(package['name']) + '.profile')
    except ImportError:
        version_list = [0, 0, 0]
    else:
        if hasattr(old_profile, 'VERSIONCOMPONENTS'):
            version_list = old_profile.VERSIONCOMPONENTS
        else:
            version_list = [0, 0, 0]
        
    version_str = ('VERSIONCOMPONENTS = [' +
                  str(version_list[0]) + ', ' +
                  str(version_list[1]) + ', ' +
                  str(version_list[2] + 1) + ']')

    release_str = 'RELEASEDATE = \'' + str(datetime.date.today()) + '\''

    supports_str = """
SUPPORTS = [ # Uncomment the following lines when implementations exist:
#supports_journal_rollback,
#supports_journal_branching"""

    ##
    # Find the Profile interface for this package
    profile_interface = None
    for i in package['interfaces']:
        if 'OsidProfile' in i['inherit_shortnames']:
            profile_interface = i
            break
    if not profile_interface:
        return ''

    for m in profile_interface['methods']:
        if (len(m['args']) == 0 and
            m['name'].startswith('supports_')):
            supports_str = supports_str + ',\n#' + m['name']
    supports_str = supports_str + '\n]'

    try:
        from builders.kitdoc_templates import package_profile
        template = string.Template(package_profile.PROFILE_TEMPLATE)
    except ImportError, AttributeError:
        return ''
    else:
        return template.substitute({'osid_package': osid_package,
                                    'version_str': version_str,
                                    'release_str': release_str,
                                    'supports_str': supports_str})

##
# The following functions return the app name and module name strings
# by prepending and appending the appropriate suffixes and prefixes. Note
# that the django app_name() function is included to support building of
# the abc osids into a Django project environment.
def abc_app_name(string):
    if abc_root_pkg:
        return abc_root_pkg
    else:
        return app_prefix + string + app_suffix
    
def abc_pkg_name(string):
    return abc_prefix + '_'.join(string.split('.')) + abc_suffix
    
def app_name(string):
    if doc_root_pkg:
        return doc_root_pkg
    else:
        return app_prefix + string + app_suffix

def pkg_name(string):
#    if kit_pkg_name:
#        return kit_pkg_name
#    else:
#        return pkg_prefix + string + pkg_suffix
    return ''



