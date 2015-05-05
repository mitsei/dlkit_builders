import time
import os
import json
import string
import datetime
import importlib
from importlib import import_module
from .binder_helpers import *
from .config import *
from builders.mongoosid_templates import options
from abcbinder_settings import XOSIDNAMESPACEURI as ns
from abcbinder_settings import XOSIDDIRECTORY as xosid_dir
from abcbinder_settings import PKGMAPSDIRECTORY as pkg_maps_dir
from abcbinder_settings import INTERFACMAPSDIRECTORY as interface_maps_dir
from abcbinder_settings import XOSIDFILESUFFIX as xosid_suffix
#from abcbinder_settings import ABCROOTPACKAGE as abc_root_pkg
from abcbinder_settings import ABCPREFIX as abc_prefix
from abcbinder_settings import ABCSUFFIX as abc_suffix
from abcbinder_settings import MAINDOCINDENTSTR as main_doc_indent
from abcbinder_settings import ENCODING as utf_code
from mongobuilder_settings import ABCROOTPACKAGE as abc_root_pkg
from mongobuilder_settings import ROOTPACKAGE as root_pkg
from mongobuilder_settings import ROOTPATH as root_path
from mongobuilder_settings import APPNAMEPREFIX as app_prefix
from mongobuilder_settings import APPNAMESUFFIX as app_suffix
from mongobuilder_settings import PACKAGEPREFIX as pkg_prefix
from mongobuilder_settings import PACKAGESUFFIX as pkg_suffix
from mongobuilder_settings import PATTERN_DIR as pattern_dir
from mongobuilder_settings import TEMPLATE_DIR as template_dir
template_pkg = '.'.join(template_dir.split('/'))

def make_mongoosids(build_abc = False, re_index = False, re_map = False):
    """
    This is the entry point for making mongo-based osid impls.

    It processes all of the osid maps in the package maps directory.
    
    """
    from abcbinder import make_abcosids
    if build_abc:
        make_abcosids(re_index, re_map)
    for json_file in os.listdir(pkg_maps_dir):
        if json_file.endswith('.json'):
            make_mongoosid(pkg_maps_dir + '/' + json_file)
    ##
    # Copy general config and primitive files, etc into the
    # implementation root directory:
    if os.path.exists('./' + template_dir + '/helpers'):
        for helper_file in os.listdir('./' + template_dir + '/helpers'):
            if helper_file.endswith('.py'):
                os.system('cp ./' + template_dir + '/helpers/' + helper_file + ' ' +
                          root_pkg + '/' + helper_file)


def make_mongoosid(file_name):
    """
    make all the mongo osid impls for a particular package.
    
    Expects a file containing a json representation of an osid package that 
    was prepared by the mapper.
    """

    read_file = open(file_name, 'r')
    package = json.load(read_file)
    read_file.close()
    
    if package['name'] not in packages_to_implement:
        return
    print "--> Mongo Implement Package:", package['name']

    ##
    # The map structure for the modules to be created by this function.
    # Each module will get a body string that holds the class and method
    # signatures for the particular interface category, and a list of 
    # for the modules that the module's classes may inherit.
    modules = dict(properties = dict(imports = [], body = ''),
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

    if not root_pkg:
        ##
        # Check if an app directory and mongo osid subdirectory already exist.  
        # If not, create them  This code specifically splits out the osid 
        # packages in a Django app environment, one Django app per osid package.
        from django.core.management import call_command
        if not os.path.exists(app_name(package['name'])):
            call_command('startapp', app_name(package['name']))
        if not os.path.exists(app_name(package['name']) + '/' + 
                              pkg_name(package['name'])):
            os.system('mkdir '+ app_name(package['name']) + '/' + 
                      pkg_name(package['name']))
            call_command('startapp', pkg_name(package['name']),
                         './' + app_name(package['name']) + '/' + 
                         pkg_name(package['name']))
    else:
        ##
        # Check if a directory already exists for the implementation.  If not,
        # create one and initialize as a python package.
        if not os.path.exists(app_name(package['name'])):
            os.system('mkdir '+ app_name(package['name']))
            os.system('touch ./' + app_name(package['name']) + '/__init__.py')
        if not os.path.exists(app_name(package['name']) + '/' + 
                              pkg_name(package['name'])):
            os.system('mkdir '+ app_name(package['name']) + '/' + 
                                pkg_name(package['name']))
            os.system('touch ./' + app_name(package['name']) + '/' + 
                             pkg_name(package['name']) + '/__init__.py')
            ## Should also install placeholder views.py, tests.py, models.py


                     
    ##
    # Write the osid license documentation file.
    #write_file = open(app_name(package['name']) + '/' + 
    #                 pkg_name(package['name']) + '/license.py', 'w')
    #write_file.write((utf_code + '\"\"\"' +
    #                  package['title'] + '\n' +
    #                  package['name'] + ' version ' +
    #                  package['version'] + '\n\n'+
    #                  package['copyright'] + '\n\n' +
    #                  package['license'] + '\n\n\"\"\"').encode('utf-8') +
    #                  '\n')
    #write_file.close
    
    ##
    # Write the summary documentation for this package.
    write_file = open(app_name(package['name']) + '/' + 
                      pkg_name(package['name']) + '/summary_doc.py', 'w')
    write_file.write((utf_code + '\"\"\"' +
                      package['title'] + '\n' +
                      package['name'] + ' version ' +
                      package['version'] + '\n\n'+
                      package['summary'] + '\n\n\"\"\"').encode('utf-8') +
                      '\n')
    write_file.close

    ##
    # Initialize the module doc
    for module in modules:
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

    ##
    # Copy settings and types and other files from the tamplates into the
    # appropriate implementation directories
    if os.path.exists('./' + template_dir + '/' + package['name'] + '_helpers'):
        #print 'FOUND:', package['name'] + '_helpers'
        for helper_file in os.listdir('./' + template_dir + '/' +
                                        package['name'] + '_helpers'):
            if helper_file.endswith('.py'):
                os.system('cp ./' + template_dir + '/' +
                          package['name'] + '_helpers/' + helper_file + ' ' +
                          app_name(package['name']) + '/' + pkg_name(package['name']) +
                          '/' + helper_file)

    ##
    # Assemble and write profile.py file for this package.
    if package['name'] in managers_to_implement:
        profile_str = make_profile_py(package)
        writeFile = open(app_name(package['name']) + '/' +
                         pkg_name(package['name']) + '/profile.py', 'w')
        writeFile.write(profile_str)
        writeFile.close() 

    ##
    # Get the pattern map for this osid package.
    read_file = open(pattern_dir + '/' + 
                      package['name'] + '.json', 'r')
    patterns = json.load(read_file)
    read_file.close()

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


    ##
    # The real work starts here.  Iterate through all interfaces to build 
    # all the django classes for this osid package.
    for interface in package['interfaces']:

        ##
        # Check to see if manager should be implemented (this should 
        # probably be moved to binder_helpers.flagged_for_implementation)
        if (interface['category'] == 'managers' and 
                      package['name'] not in managers_to_implement):
            continue

        ##
        # Check to see if this interface is meant to be implemented.
        if package['name'] != 'osid' and interface['category'] not in excepted_osid_categories:
            if flagged_for_implementation(interface, 
                    sessions_to_implement, objects_to_implement, variants_to_implement):
                if interface['shortname'] in exceptions:
                    continue
                else:
                    pass
            else:
                continue
        
        ##
        # Seed the inheritance list with this interface's abc_osid
        inheritance = ['abc_' + abc_pkg_name(package['name']) + '_' +
                       interface['category'] + '.' +
                       interface['shortname']]
        ##
        # And make sure there is a corresponding import statement for this
        # interface's abc_osid and associated module/category name.
        import_str = ('from ' + abc_app_name(package['name']) + '.' +
                       abc_pkg_name(package['name']) + ' import ' +
                       interface['category'] + ' as abc_' + 
                       abc_pkg_name(package['name'] + '_' + interface['category']))
        if not import_str in modules[interface['category']]['imports']:
            modules[interface['category']]['imports'].append(import_str)

        ##
        # Interate through any inherited interfaces and build the inheritance
        # list for this interface. Also, check if an import statement is
        # required and append to the appropriate module's import list.
        for i in interface['inheritance']:
            unknown_module_protection = ''
            inherit_category = get_interface_module(i['pkg_name'], i['name'], True)
            if inherit_category == 'UNKNOWN_MODULE':
                unknown_module_protection = '\"\"\"'
            if (i['pkg_name'] == package['name'] and
                  inherit_category == interface['category']):
                inheritance.append(i['name'])
            else:
                inheritance.append(unknown_module_protection + 
                                   pkg_name(i['pkg_name']) + '_' +
                                   inherit_category + '.' + i['name'] +
                                   unknown_module_protection)
                import_str = ('from ' + impl_root_path(i['pkg_name']) +
                              pkg_name(i['pkg_name']) + 
                              ' import ' + inherit_category + ' as ' +
                              pkg_name(i['pkg_name']) + '_' + inherit_category)

                if (import_str not in modules[interface['category']]['imports'] and
                    inherit_category != 'UNKNOWN_MODULE'):
                    modules[interface['category']]['imports'].append(import_str)

        ##
        # Check to see if there are any additinal inheritances required
        # by the implementation patterns.  THIS MAY WANT TO BE REDESIGNED
        # TO ALLOW INSERTING THE INHERITANCE IN A PARTICULAR ORDER.
        impl_class = load_impl_class(package['name'], interface['shortname'])
        if hasattr(impl_class, 'inheritance'):
            inheritance = inheritance + getattr(impl_class, 'inheritance')
        if hasattr(impl_class, 'inheritance_imports'):
            modules[interface['category']]['imports'] = (
                modules[interface['category']]['imports'] +
                getattr(impl_class, 'inheritance_imports'))

        ##
        # Here we further inspect the impl_class to identify any additional 
        # hand built import statements to be loaded at the module level. These
        # need to be coded in the impl_class as a list of strings with the 
        # attribute name 'import_statements'
        if hasattr(impl_class, 'import_statements'):
            #print 'FOUND import_statements', package['name'], interface['shortname']
            for import_str in getattr(impl_class, 'import_statements'):
                if import_str not in modules[interface['category']]['imports']:
                    modules[interface['category']]['imports'].append(import_str)

        ##
        # Look for module import statements defined in class patterns. These
        # need to be coded in the class pattern as a list of strings with the 
        # attribute name 'import_statements_pattern'
        for import_str in make_module_imports(interface['shortname'], package, patterns):
            if import_str not in modules[interface['category']]['imports']:
                modules[interface['category']]['imports'].append(import_str)

        additional_methods = ''
        ##
        # Look for additional methods defined in class patterns. These
        # need to be coded in the impl_class as a string with the 
        # attribute name 'additional_methods_pattern'
        additional_methods = additional_methods + make_additional_methods(interface['shortname'], package, patterns)
            
        ##
        # Here we further inspect the impl_class to identify any additional 
        # hand built methods to be included at the end of the class definition. These
        # need to be coded in the impl_class as a string with the 
        # attribute name 'additional_methods'
        if hasattr(impl_class, 'additional_methods'):
            additional_methods = additional_methods + getattr(impl_class, 'additional_methods')
            #print additional_methods

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
            
        class_sig = 'class ' + interface['shortname'] + inheritance + ':'
        
        init_methods = make_init_methods(interface['shortname'], package, patterns) 
        
        methods = make_methods(pkg_name(package['name']), interface, patterns)

        if additional_methods:
            methods = methods + '\n' + additional_methods

        modules[interface['category']]['body'] = (
                          modules[interface['category']]['body'] + 
                          class_sig + '\n' +
                          class_doc + '\n' +
                          init_methods + '\n' +
                          methods + '\n\n\n')
    ##
    # Iterate through the completed package module structure and write
    # out both the import statements and class definitions to the
    # appropriate module for this package.
    for module in modules:
        if module == 'records' and package['name'] != 'osid':
            module_name = 'record_templates'
        else:
            module_name = module
        if modules[module]['body'].strip() != '':
            write_file = open(app_name(package['name']) + '/' + 
                              pkg_name(package['name']) + '/' +
                              module_name + '.py', 'w')
            write_file.write(('\n'.join(modules[module]['imports']) + '\n\n\n' +
                              modules[module]['body']).encode('utf-8'))
            write_file.close

    ##
    # Finally,  write out the implementation log for this service package
    #write_file = open(app_name(package['name']) + '/' + 
    #                  pkg_name(package['name']) + '/impl_log.txt', 'w')
    #write_file.write(make_impl_log(patterns['impl_log']))
    #write_file.close

##
# Try loading hand-built implementations class for this interface
def load_impl_class(package_name, interface_name):
    impl_class = None
    try:
        impls = importlib.import_module(template_pkg + '.' + package_name)
    except ImportError:
        pass
    else:
        if hasattr(impls, interface_name):
            impl_class = getattr(impls, interface_name)
    return impl_class

def make_module_imports(interface_name, package, patterns):
    if interface_name + '.init_pattern' in patterns:
        init_pattern = patterns[interface_name + '.init_pattern']
        try:
            templates = importlib.import_module(template_pkg + '.' +
                                                init_pattern.split('.')[0])
            if hasattr(templates, init_pattern.split('.')[-1]):
                template_class = getattr(templates, init_pattern.split('.')[-1])
                if hasattr(template_class, 'import_statements_pattern'):
                    #print 'FOUND import_statements_pattern', package['name'], interface_name
                    return getattr(template_class, 'import_statements_pattern')
                else:
                    #print 'import_statements_pattern not found
                    return []
            else:
                #print 'template class not found'
                return []
        except ImportError:
            #print 'import error'
            return []
    else:
        #print 'cant find init pattern', interface_name
        return []

def make_class_attributes(interface_name, package, patterns):
    if interface_name + '.init_pattern' in patterns:
        init_pattern = patterns[interface_name + '.init_pattern']
        try:
            templates = importlib.import_module(template_pkg + '.' +
                                                init_pattern.split('.')[0])
            if hasattr(templates, init_pattern.split('.')[-1]):
                template_class = getattr(templates, init_pattern.split('.')[-1])
                if hasattr(template_class, 'class_attributes_pattern'):
                    #print 'FOUND class_attributes_pattern', package['name'], interface_name
                    return getattr(template_class, 'class_attributes_pattern')
                else:
                    #print 'class_attributes_pattern not found
                    return ''
            else:
                #print 'template class not found'
                return ''
        except ImportError:
            #print 'import error'
            return ''
    else:
        #print 'cant find init pattern', interface_name
        return ''

def make_additional_methods(interface_name, package, patterns):
    if interface_name + '.init_pattern' in patterns:
        init_pattern = patterns[interface_name + '.init_pattern']
        try:
            templates = importlib.import_module(template_pkg + '.' +
                                                init_pattern.split('.')[0])
            if hasattr(templates, init_pattern.split('.')[-1]):
                template_class = getattr(templates, init_pattern.split('.')[-1])
                if hasattr(template_class, 'additional_methods_pattern'):
                    #print 'FOUND additional_methods_pattern', package['name'], interface_name
                    return getattr(template_class, 'additional_methods_pattern')
                else:
                    #print 'additional_methods_pattern not found
                    return ''
            else:
                #print 'template class not found'
                return ''
        except ImportError:
            #print 'import error'
            return ''
    else:
        #print 'cant find init pattern', interface_name
        return ''


def make_init_methods(interface_name, package, patterns):
    templates = None
    init_pattern = ''
    instance_initers = ''
    persisted_initers = ''
    metadata_initers = ''
    object_name = ''
    init_object = ''
    cat_name = patterns['package_catalog_caps']
    impl_class = load_impl_class(pkg_name(package['name']), interface_name)
    if hasattr(impl_class, 'init'):
        return getattr(impl_class, 'init')
    elif interface_name + '.init_pattern' in patterns:
        init_pattern = patterns[interface_name + '.init_pattern']
        try:
            templates = importlib.import_module(template_pkg + '.' +
                                                init_pattern.split('.')[0])
        except ImportError:
            return ''
    else:
        return ''

    ##
    # Check for any special data initializations and call the appropriate makers
    # to assemble them.
    if init_pattern == 'resource.Bin':
        object_name = interface_name
    elif init_pattern == 'resource.BinForm':
        object_name = interface_name[:-4]
    elif init_pattern == 'resource.ResourceLookupSession':
        object_name = interface_name[:-13]
    elif init_pattern == 'resource.Resource':
        object_name = interface_name
        try:
            instance_initers = make_instance_initers(
                patterns[interface_name + '.instance_data'])
        except KeyError:
            pass
    elif init_pattern == 'resource.ResourceForm':
        object_name = interface_name[:-4]
        if object_name in patterns['package_relationships_caps']:
            init_object = 'osid_objects.OsidRelationshipForm'
        else:
            init_object = 'osid_objects.OsidObjectForm'
        try:
            persisted_initers = make_persistance_initers(
                patterns[interface_name[:-4] + '.persisted_data'],
                patterns[interface_name[:-4] + '.initialized_data'],
                patterns[interface_name[:-4] + '.aggregate_data'])
            #persisted_initers = make_persistance_initers(
            #    patterns[interface_name[:-4] + '.persisted_data'],
            #    dict(patterns[interface_name[:-4] + '.initialized_data'], **patterns[interface_name[:-4] + '.instance_data']),
            #    patterns[interface_name[:-4] + '.aggregate_data'])
        except KeyError:
            pass
        try:
            metadata_initers = make_metadata_initers(
                patterns[interface_name[:-4] + '.persisted_data'],
                patterns[interface_name[:-4] + '.initialized_data'],
                patterns[interface_name[:-4] + '.return_types'])
        except KeyError:
            pass
    elif init_pattern == 'resource.ResourceQuery':
        object_name = interface_name[:-5]
    
    #object_imports = []
    #abject_import.append(patterns['package_objects_caps'])
    #abject_import.append(patterns['package_relationships_caps'])
    #for 

    if hasattr(templates, init_pattern.split('.')[-1]):
        template_class = getattr(templates, init_pattern.split('.')[-1])
        if hasattr(template_class, 'init_template'):
            template = string.Template(getattr(template_class, 'init_template'))
            return template.substitute({'app_name': app_name(package['name']),
                                        'implpkg_name': pkg_name(package['name']),
                                        'pkg_name': package['name'],
                                        'pkg_name_upper': package['name'].upper(),
                                        'interface_name': interface_name,
                                        'instance_initers': instance_initers,
                                        'persisted_initers': persisted_initers,
                                        'metadata_initers': metadata_initers,
                                        'object_name': object_name,
                                        'object_name_upper': camel_to_under(object_name).upper(),
                                        'cat_name': cat_name,
                                        'cat_name_plural': make_plural(cat_name),
                                        'cat_name_under': cat_name.lower(),
                                        'cat_name_under_plural': make_plural(cat_name).lower(),
                                        'cat_name_upper': cat_name.upper(),
                                        'init_object': init_object})
        else:
            return ''
    else:
        return ''

##
# Assemble the initializers for instance data managed by Osid Objects
def make_instance_initers(instance_data):
    initers = ''
#    for i in instance_data:
#        if instance_data[i] == 'boolean':
#            initers = initers + (initers + 
#                '        self.' + i + ' = None\n')
#        elif instance_data[i] == 'osid.id.Id':
#            initers = initers + (initers + 
#                '        self.' + i + '_authority = \'\'\n' +
#                '        self.' + i + '_namespace = \'\'\n' +
#                '        self.' + i + '_identifier = \'\'\n')
    return initers

##
# Assemble the initializers for persistance data managed by Osid Object Forms
# initialized with the form.
def make_persistance_initers(persisted_data, initialized_data, aggregate_data):
    initers = ''
    for data_name in persisted_data:
        if ((persisted_data[data_name] == 'osid.id.Id' or
             persisted_data[data_name] == 'OsidCatalog') and
            data_name in initialized_data):
            initers = initers + (
    '        self._my_map[\'' + under_to_mixed(data_name) + 'Id\'] = str(kwargs[\'' + data_name + '_id\'])\n')
        elif (persisted_data[data_name] == 'osid.resource.Resource' and
            data_name in initialized_data):
            initers = initers + (
    '        self._my_map[\'' + under_to_mixed(data_name) + 'Id\'] = str(kwargs[\'effective_agent_id\'])\n')
        elif persisted_data[data_name] == 'osid.id.Id':
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + 'Id\'] = self._' + 
                data_name + '_default\n')
        elif persisted_data[data_name] == 'osid.id.Id[]':
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(remove_plural(data_name)) + 'Ids\'] = self._' + 
                data_name + '_default\n')
        elif persisted_data[data_name] == 'osid.type.Type':
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + 'Id\'] = self._' + 
                data_name + '_default\n')
        elif persisted_data[data_name] == 'osid.type.Type[]':
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(remove_plural(data_name)) + 'Ids\'] = self._' + 
                data_name + '_default\n')
        elif persisted_data[data_name] == 'string':
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + '\'] = self._' + 
                data_name + '_default\n')
        elif persisted_data[data_name] == 'boolean':
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + '\'] = self._' + 
                data_name + '_default\n')
        elif persisted_data[data_name] == 'OsidCatalog':
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + '\'] = self._' + 
                data_name + '_default\n')
        elif persisted_data[data_name] in ['osid.calendaring.DateTime', 'timestamp']:
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + '\'] = self._' + 
                data_name + '_default\n')
        elif persisted_data[data_name] == 'osid.calendaring.Duration':
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + '\'] = self._' + 
                data_name + '_default\n')
        elif persisted_data[data_name] == 'osid.transport.DataInputStream':
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + '\'] = self._' + 
                data_name + '_default\n')
          
    for data_name in aggregate_data:
        if aggregate_data[data_name].endswith('List'):
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + '\'] = []\n')
        else:
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + '\'] = None\n')

    for data_name in initialized_data:
        if data_name in persisted_data:
            pass
        elif initialized_data[data_name] == 'boolean':
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + '\'] = None\n')
        elif initialized_data[data_name] == 'decimal':
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + '\'] = \'\'\n')
        elif initialized_data[data_name] == 'cardinal':
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + '\'] = \'\'\n')
        elif initialized_data[data_name] == 'string':
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + '\'] = \'\'\n')
        elif initialized_data[data_name] == 'osid.locale.DisplayText':
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + '\'] = {\n' +
            '            \'text\': \'\',\n' +
            '            \'languageTypeId\': str(default_language_type),\n' +
            '            \'scriptTypeId\': str(default_script_type),\n' +
            '            \'formatTypeId\': str(default_format_type),\n' +
            '        }\n')
        elif initialized_data[data_name] == 'osid.id.Id':
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + 'Id\'] = \'\'\n')
        elif initialized_data[data_name] == 'osid.id.Id[]':
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + 'Id\'] = []\n')
        elif initialized_data[data_name] in ['osid.calendaring.DateTime', 'timestamp']:
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + '\'] = None\n')
        elif initialized_data[data_name] == 'osid.calendaring.Duration':
            initers = initers + (
            '        self._my_map[\'' + under_to_mixed(data_name) + '\'] = None\n')

    return initers

##
# Assemble the initializers for metadata managed by Osid Object Forms
def make_metadata_initers(persisted_data, initialized_data, return_types):
    imports = ''
    initer = ''
    default = ''
    for data_name in persisted_data:
        data_name_upper = data_name.upper()
        template = ''
        if (persisted_data[data_name] != 'OsidCatalog' and 
            data_name not in initialized_data):
            if persisted_data[data_name] == 'boolean':
                template = string.Template(options.METADATA_INITER)
                default = default + ('        self._' + data_name + 
                    '_default = None\n')
            elif persisted_data[data_name] == 'string' and return_types[data_name] == 'osid.locale.DisplayText':
                template = string.Template(options.METADATA_INITER)
                default = default + ('        self._' + data_name + 
                    '_default = dict(self._' + data_name + '_metadata[\'default_string_values\'][0])\n')
            elif persisted_data[data_name] == 'string':
                template = string.Template(options.METADATA_INITER)
                default = default + ('        self._' + data_name + 
                    '_default = self._' + data_name + '_metadata[\'default_string_values\'][0]\n')
            elif (persisted_data[data_name] == 'osid.id.Id' and
                  not data_name in initialized_data):
                template = string.Template(options.METADATA_INITER)
                default = default + ('        self._' + data_name + 
                    '_default = self._' + data_name + '_metadata[\'default_id_values\'][0]\n')
            elif persisted_data[data_name] == 'osid.id.Id[]':
                template = string.Template(options.METADATA_INITER)
                default = default + ('        self._' + data_name + 
                    '_default = self._' + data_name + '_metadata[\'default_id_values\']\n')
            elif (persisted_data[data_name] == 'osid.type.Type' and
                  not data_name in initialized_data):
                template = string.Template(options.METADATA_INITER)
                default = default + ('        self._' + data_name + 
                    '_default = self._' + data_name + '_metadata[\'default_type_values\'][0]\n')
            elif persisted_data[data_name] == 'osid.type.Type[]':
                template = string.Template(options.METADATA_INITER)
                default = default + ('        self._' + data_name + 
                    '_default = self._' + data_name + '_metadata[\'default_type_values\']\n')
            elif persisted_data[data_name] in ['osid.calendaring.DateTime', 'timestamp']:
                template = string.Template(options.METADATA_INITER)
                default = default + ('        self._' + data_name + 
                    '_default = self._' + data_name + '_metadata[\'default_date_time_values\'][0]\n')
            elif persisted_data[data_name] == 'osid.calendaring.Duration':
                template = string.Template(options.METADATA_INITER)
                default = default + ('        self._' + data_name + 
                    '_default = self._' + data_name + '_metadata[\'default_duration_values\'][0]\n')
            elif persisted_data[data_name] == 'osid.transport.DataInputStream':
                template = string.Template(options.METADATA_INITER)
                default = default + ('        self._' + data_name + 
                    '_default = self._' + data_name + '_metadata[\'default_object_values\'][0]\n')
            elif persisted_data[data_name] == 'osid.mapping.SpatialUnit':
                pass # Put SpatialUnit initters here
            elif persisted_data[data_name] == 'decimal':
                template = string.Template(options.METADATA_INITER)
                default = default + ('        self._' + data_name + 
                    '_default = self._' + data_name + '_metadata[\'default_decimal_values\'][0]\n')

        if template:
            initer = (initer + template.substitute({'data_name': data_name, 'data_name_upper': data_name_upper}))
    return imports + initer + '\n' + default +'\n'


def make_methods(package_name, interface, patterns):
    body = []
    for method in interface['methods']:
        if method['name'] == 'read' and interface['shortname'] == 'DataInputStream':
            method['name'] = 'read_to_buffer'
        body.append(make_method(package_name, method, interface, patterns))

        ##
        # Here is where we add the Python properties stuff:
        if method['name'].startswith('get_') and method['args'] == []:
            body.append('    ' + fix_reserved_word(method['name'][4:]) + 
                    ' = property(fget=' + method['name'] + ')')
        elif method['name'].startswith('set_') and len(method['args']) == 1:
            if ('    ' + fix_reserved_word(method['name'][4:]) + ' = property(fdel=clear_' + method['name'][4:] + ')') in body:
                body.remove('    ' + fix_reserved_word(method['name'][4:]) + ' = property(fdel=clear_' + method['name'][4:] + ')')
                body.append('    ' + fix_reserved_word(method['name'][4:]) + 
                        ' = property(fset=' + method['name'] +
                        ', fdel=clear_' + method['name'][4:] + ')')
            else:
                body.append('    ' + fix_reserved_word(method['name'][4:]) + 
                        ' = property(fset=' + method['name'] + ')')
        elif method['name'].startswith('clear_') and method['args'] == []:
            if ('    ' + fix_reserved_word(method['name'][6:]) + ' = property(fset=set_' + method['name'][6:] + ')') in body:
                body.remove('    ' + fix_reserved_word(method['name'][6:]) + ' = property(fset=set_' + method['name'][6:] + ')')
                body.append('    ' + fix_reserved_word(method['name'][6:]) + 
                        ' = property(fset=set_' + method['name'][6:] +
                        ', fdel=' + method['name'] + ')')
            else:
                body.append('    ' + method['name'][6:] + 
                        ' = property(fdel=' + method['name'] + ')')
        if method['name'] == 'get_id':
                body.append('    ident = property(fget=' + method['name'] + ')')
        if method['name'] == 'get_identifier_namespace':
                body.append('    namespace = property(fget=' + method['name'] + ')')

    return '\n\n'.join(body)
    
def make_method(package_name, method, interface, patterns):
    args = ['self']
    method_doc = ''
    method_impl = make_method_impl(package_name, method, interface, patterns)

    for arg in method['args']:
        args.append(arg['var_name'] + '=None')
    method_sig = ('    def ' + method['name'] + '(' +
                ', '.join(args) + '):')

    method_doc = ''
    detail_docs = filter(None, [method['arg_doc'].strip('\n'),
                                method['return_doc'].strip('\n'),
                                method['error_doc'].strip('\n'),
                                method['compliance_doc'].strip('\n'),
                                method['impl_notes_doc'].strip('\n')])

    if method['doc']['body'].strip() == '' and not detail_docs:
        method_doc = ('        \"\"\"' + 
                      method['doc']['headline'] + 
                      '\"\"\"')
    elif method['doc']['body'].strip() == '':
        method_doc = ('        \"\"\"' + method['doc']['headline'] + 
                      '\n\n' +
                      '\n'.join(detail_docs) + '\n\n        \"\"\"')
    else:
        method_doc = ('        \"\"\"' + method['doc']['headline'] + 
                      '\n\n' +
                      method['doc']['body'] + '\n\n' +
                      '\n'.join(detail_docs) + '\n\n        \"\"\"')

    return (method_sig + '\n' + method_doc + '\n' + method_impl)
    
def make_method_impl(package_name, method, interface, patterns):
    impl = ''
    pattern = ''
    kwargs = {}
    templates = None

    
    if interface['shortname'] + '.' + method['name'] in patterns:
        pattern = patterns[interface['shortname'] + '.' + method['name']]['pattern']
        kwargs = patterns[interface['shortname'] + '.' + method['name']]['kwargs']

    impl_class = load_impl_class(package_name, interface['shortname'])

    template_class = None
    if pattern:
        try:
            templates = importlib.import_module(template_pkg + '.' +
                                                pattern.split('.')[0])
        except ImportError:
            pass
        else:
            if hasattr(templates, pattern.split('.')[-2]):
                template_class = getattr(templates, pattern.split('.')[-2])

    ##
    # Check if there is a 'by hand' implementation available for this method
    if (impl_class and 
        hasattr(impl_class, method['name'])):
        impl = getattr(impl_class, method['name']).strip('\n')

    ##
    # If there is no 'by hand' implementation, get the template for the 
    # method implementation that serves as the pattern, if one exixts.
    elif (template_class and
          hasattr(template_class, pattern.split('.')[-1] + '_template')):
        template_str = getattr(template_class, pattern.split('.')[-1] + 
                                '_template').strip('\n')
        template = string.Template(template_str)
        
        ##
        # Add keyword arguments to template kwargs that are particuler
        # to the mongo implementation
        kwargs['app_name'] = app_name(kwargs['package_name'])
        kwargs['implpkg_name'] = pkg_name(kwargs['package_name'])
        kwargs['abcapp_name'] = abc_app_name(kwargs['package_name'])
        kwargs['abcpkg_name'] = abc_pkg_name(kwargs['package_name'])
        kwargs['interface_name_under'] = camel_to_under(kwargs['interface_name'])
        kwargs['interface_name_dot'] = '.'.join(kwargs['interface_name_under'].split('_')[:-1])
        kwargs['package_name_caps'] = package_name.title()
 
        if kwargs['interface_name_under'].endswith('_session'):
            kwargs['session_shortname_dot'] = '.'.join(kwargs['interface_name_under'].split('_')[:-1])
        
        if 'arg0_type_full' in kwargs:
            kwargs['arg0_type'] = kwargs['arg0_type_full'].split('.')[-1].strip('[]')
            kwargs['arg0_type_under'] = camel_to_under(kwargs['arg0_type'])
            kwargs['arg0_type_mixed'] = camel_to_mixed(kwargs['arg0_type'])
            kwargs['arg0_abcapp_name'] = abc_app_name(get_pkg_name(kwargs['arg0_type_full'].strip('[]')))
            kwargs['arg0_abcpkg_name'] = abc_pkg_name(get_pkg_name(kwargs['arg0_type_full'].strip('[]')))
            kwargs['arg0_module'] = get_interface_module(
                                    get_pkg_name(kwargs['arg0_type_full']),
                                    kwargs['arg0_type_full'].split('.')[-1].strip('[]'))
        if 'arg1_type_full' in kwargs:
            kwargs['arg1_type'] = kwargs['arg1_type_full'].split('.')[-1].strip('[]')
            kwargs['arg1_type_under'] = camel_to_under(kwargs['arg1_type'])
            kwargs['arg1_type_mixed'] = camel_to_mixed(kwargs['arg1_type'])
            kwargs['arg1_abcapp_name'] = abc_app_name(get_pkg_name(kwargs['arg1_type_full'].strip('[]')))
            kwargs['arg1_abcpkg_name'] = abc_pkg_name(get_pkg_name(kwargs['arg1_type_full'].strip('[]')))
            kwargs['arg1_module'] = get_interface_module(
                                    get_pkg_name(kwargs['arg1_type_full']),
                                    kwargs['arg1_type_full'].split('.')[-1].strip('[]'))
        if 'arg2_type_full' in kwargs:
            kwargs['arg2_type'] = kwargs['arg2_type_full'].split('.')[-1].strip('[]')
            kwargs['arg2_type_under'] = camel_to_under(kwargs['arg2_type'])
            kwargs['arg2_type_mixed'] = camel_to_mixed(kwargs['arg2_type'])
            kwargs['arg2_abcapp_name'] = abc_app_name(get_pkg_name(kwargs['arg2_type_full'].strip('[]')))
            kwargs['arg2_abcpkg_name'] = abc_pkg_name(get_pkg_name(kwargs['arg2_type_full'].strip('[]')))
            kwargs['arg2_module'] = get_interface_module(
                                    get_pkg_name(kwargs['arg2_type_full']),
                                    kwargs['arg2_type_full'].split('.')[-1].strip('[]'))
        if 'arg3_type_full' in kwargs:
            kwargs['arg3_type'] = kwargs['arg3_type_full'].split('.')[-1].strip('[]')
            kwargs['arg3_type_under'] = camel_to_under(kwargs['arg3_type'])
            kwargs['arg3_type_mixed'] = camel_to_mixed(kwargs['arg3_type'])
            kwargs['arg3_abcapp_name'] = abc_app_name(get_pkg_name(kwargs['arg3_type_full'].strip('[]')))
            kwargs['arg3_abcpkg_name'] = abc_pkg_name(get_pkg_name(kwargs['arg3_type_full'].strip('[]')))
            kwargs['arg3_module'] = get_interface_module(
                                    get_pkg_name(kwargs['arg3_type_full']),
                                    kwargs['arg3_type_full'].split('.')[-1].strip('[]'))
        if 'arg0_object' in kwargs:
            kwargs['arg0_object_under'] = camel_to_under(kwargs['arg0_object'])
            kwargs['arg0_object_mixed'] = camel_to_mixed(kwargs['arg0_object'])
        if 'return_type_full' in kwargs:
            kwargs['return_type'] = kwargs['return_type_full'].split('.')[-1]
            kwargs['return_pkg'] = get_pkg_name(kwargs['return_type_full'])
            kwargs['return_module'] = get_interface_module(
                                      get_pkg_name(kwargs['return_type_full']), 
                                      kwargs['return_type_full'].split('.')[-1])
        if 'return_pkg' in kwargs:
            kwargs['return_app_name'] = app_name(kwargs['return_pkg'])
            kwargs['return_implpkg_name'] = pkg_name(kwargs['return_pkg'])
            kwargs['return_pkg_title'] = kwargs['return_pkg'].title()
            kwargs['return_pkg_caps'] = kwargs['return_pkg'].upper()
        if 'object_name_under' in kwargs:
            kwargs['object_name_upper'] = kwargs['object_name_under'].upper()
            # Might want to add creating kwargs['object_name' from this as well]
        if 'object_name' in kwargs and 'package_name' in kwargs:
            kwargs['object_app_name'] = app_name(kwargs['package_name'])
            kwargs['object_implpkg_name'] = pkg_name(kwargs['package_name'])
            kwargs['object_module'] = get_interface_module('package_name', 'object_name')
        if 'var_name' in kwargs:
            kwargs['var_name_upper'] = kwargs['var_name'].upper()
            kwargs['var_name_mixed'] = under_to_mixed(kwargs['var_name'])
            kwargs['var_name_plural'] = make_plural(kwargs['var_name'])
            kwargs['var_name_plural_mixed'] = under_to_mixed(kwargs['var_name_plural'])
            kwargs['var_name_singular'] = remove_plural(kwargs['var_name'])
            kwargs['var_name_singular_mixed'] = under_to_mixed(kwargs['var_name_singular'])
        if 'return_type' in kwargs:
            kwargs['return_type_under'] = camel_to_under(kwargs['return_type'])
        if 'return_type' in kwargs and kwargs['return_type'].endswith('List'):
            kwargs['return_type_list_object'] = kwargs['return_type'][:-4]
            kwargs['return_type_list_object_under'] = camel_to_under(kwargs['return_type_list_object'])
            kwargs['return_type_list_object_plural_under'] = make_plural(kwargs['return_type_list_object_under'])
        if 'object_name' in kwargs and not 'object_name_under' in kwargs and not 'object_name_upper' in kwargs:
            kwargs['object_name_under'] = camel_to_under(kwargs['object_name'])
            kwargs['object_name_mixed'] = camel_to_mixed(kwargs['object_name'])
            kwargs['object_name_upper'] = camel_to_under(kwargs['object_name']).upper()
        if 'aggregated_object_name' in kwargs:
            kwargs['aggregated_object_name_under'] = camel_to_under(kwargs['aggregated_object_name'])
            kwargs['aggregated_object_name_mixed'] = camel_to_mixed(kwargs['aggregated_object_name'])
            kwargs['aggregated_objects_name_under'] = camel_to_under(make_plural(kwargs['aggregated_object_name']))
            kwargs['aggregated_objects_name_mixed'] = camel_to_mixed(make_plural(kwargs['aggregated_object_name']))
        if 'source_name' in kwargs:
            kwargs['source_name_mixed'] = under_to_mixed(kwargs['source_name'])
        if 'destination_name' in kwargs:
            kwargs['destination_name_mixed'] = under_to_mixed(kwargs['destination_name'])
        if 'cat_name' in kwargs:
            kwargs['cat_name_under'] = camel_to_under(kwargs['cat_name'])
            kwargs['cat_name_lower'] = kwargs['cat_name'].lower()
            kwargs['cat_name_mixed'] = camel_to_mixed(kwargs['cat_name'])
            kwargs['cat_name_plural'] = make_plural(kwargs['cat_name'])
            kwargs['cat_name_plural_under'] = camel_to_under(kwargs['cat_name_plural'])
            kwargs['cat_name_plural_lower'] = kwargs['cat_name_plural'].lower()
            kwargs['cat_name_plural_mixed'] = camel_to_mixed(kwargs['cat_name_plural'])
        if 'return_cat_name' in kwargs:
            kwargs['return_cat_name_under'] = camel_to_under(kwargs['return_cat_name'])
            kwargs['return_cat_name_lower'] = kwargs['return_cat_name'].lower()
            kwargs['return_cat_name_mixed'] = camel_to_mixed(kwargs['return_cat_name'])
        if 'Proxy' in kwargs['interface_name']:
            kwargs['non_proxy_interface_name'] = ''.join(kwargs['interface_name'].split('Proxy'))
        if ('return_pkg' in kwargs and 'return_module' in kwargs and
            kwargs['package_name'] == kwargs['return_pkg'] and
            kwargs['module_name'] == kwargs['return_module']):
            kwargs['import_str'] = ''
        elif ('package_name' in kwargs and 'return_pkg' in kwargs and
              'return_type' in kwargs and 'return_module' in kwargs):
            kwargs['import_str'] = ('        from ..' +
                                    kwargs['return_implpkg_name'] + '.' +
                                    kwargs['return_module'] + ' import ' +
                                    kwargs['return_type'] + '\n')  ### WHY DO WE NEED import_str???

# Uncomment next line to identify on which method a KeyError is occuring
        #print interface['shortname'], method['name']

        impl = template.substitute(kwargs).strip('\n')
    if impl == '':
        impl = '        raise Unimplemented()'
    else:
        if (interface['category'] in patterns['impl_log'] and
            interface['shortname'] in patterns['impl_log'][interface['category']]):
            patterns['impl_log'][kwargs['module_name']][interface['shortname']][method['name']][1] = 'implemented'
    return impl
        

def make_profile_py(package):    
    osid_package = package['name']
    #print ('.'.join(app_name(package['name']).split('/')[1:]) + '.' +
    #                                pkg_name(package['name']) + '.profile', 'dlkit_project.builders')
    try:
        old_profile = import_module('.'.join(app_name(package['name']).split('/')[1:]) + '.' +
                                    pkg_name(package['name']) + '.profile', 'dlkit_project.builders')
    except ImportError:
        print 'Old Profile not found:', pkg_name(package['name'])
        version_list = [0, 1, 0]
        old_supports = []
    else:
        if hasattr(old_profile, 'VERSIONCOMPONENTS'):
            version_list = old_profile.VERSIONCOMPONENTS
        else:
            version_list = [0, 1, 0]
        if hasattr(old_profile, 'SUPPORTS'):
            old_supports = old_profile.SUPPORTS
        
    version_str = ('VERSIONCOMPONENTS = [' +
                  str(version_list[0]) + ', ' +
                  str(version_list[1]) + ', ' +
                  str(version_list[2] + 1) + ']')

    release_str = 'RELEASEDATE = \'' + str(datetime.date.today()) + '\''

    supports_str = """
SUPPORTS = [ # Uncomment the following lines when implementations exist:
    #'supports_journal_rollback',
    #'supports_journal_branching'"""

    ##
    # Find the Profile interface for this package
    profile_interface = None
    for i in package['interfaces']:
        if 'OsidProfile' in i['inherit_shortnames']:
            profile_interface = i
            break
    if not profile_interface:
        return ''

    for method in profile_interface['methods']:
        if (len(method['args']) == 0 and
            method['name'].startswith('supports_')):
            ##
            # Check to see if support flagged in builder config
            if under_to_caps(method['name'])[8:] + 'Session' in sessions_to_implement:
                comment = ''
            ##
            # Check to see if someone activited support by hand
            elif method['name'] in old_supports:
                comment = ''
            else: # Add check for session implementation flags here
                comment = '#'
            supports_str = supports_str + ',\n    ' + comment + '\'' + method['name'] +'\''
    supports_str = supports_str + '\n]'

    try:
        from builders.mongoosid_templates import package_profile
        template = string.Template(package_profile.PROFILE_TEMPLATE)
    except ImportError, AttributeError:
        return ''
    else:
        return template.substitute({'osid_package': osid_package,
                                    'version_str': version_str,
                                    'release_str': release_str,
                                    'supports_str': supports_str})

def make_impl_log(log):
    log_str = ''
    for category in log:
        #print category
        log_str = log_str + category + '\n'
        for interface in log[category]:
            #print '  ', interface
            log_str = log_str + '    ' + interface + '\n'
            for method in log[category][interface]:
                #print '    ', method
                if (log[category][interface][method][0] == 'unmapped' or
                    log[category][interface][method][1] == 'unimplemented'):
                        #print '      ', log[category][interface][method][0], log[category][interface][method][1]
                        log_str = (log_str + '        ' + method + ': ' +
                            log[category][interface][method][0] + ', ' +
                            log[category][interface][method][1] + '\n')
    return log_str
            

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
    
def impl_root_path(string):
    if root_path:
        return root_path
    else:
        return app_prefix + string + app_suffix

def app_name(string):
    if root_pkg:
        return root_pkg
    else:
        return app_prefix + string + app_suffix

def pkg_name(string):
    return pkg_prefix + '_'.join(string.split('.')) + pkg_suffix
