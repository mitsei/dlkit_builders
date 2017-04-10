
import time
import os
import json
import string
from abcbinder_settings import XOSIDNAMESPACEURI as ns
from abcbinder_settings import XOSIDDIRECTORY as xosid_dir
from abcbinder_settings import PKGMAPSDIRECTORY as pkg_maps_dir
from abcbinder_settings import INTERFACMAPSDIRECTORY as interface_maps_dir
from abcbinder_settings import XOSIDFILESUFFIX as xosid_suffix
# from abcbinder_settings import ABCROOTPACKAGE as abc_root_pkg
from abcbinder_settings import ABCPREFIX as abc_prefix
from abcbinder_settings import ABCSUFFIX as abc_suffix
from abcbinder_settings import MAINDOCINDENTSTR as main_doc_indent
from abcbinder_settings import ENCODING as utf_code
from fedbuilder_settings import ABCROOTPACKAGE as abc_root_pkg
from fedbuilder_settings import ROOTPACKAGE as root_pkg
from fedbuilder_settings import ROOTPATH as root_path
from fedbuilder_settings import APPNAMEPREFIX as app_prefix
from fedbuilder_settings import APPNAMESUFFIX as app_suffix
from fedbuilder_settings import PACKAGEPREFIX as pkg_prefix
from fedbuilder_settings import PACKAGESUFFIX as pkg_suffix
from fedbuilder_settings import TEMPLATEDIR as template_dir


# This is the entry point for making django-based python classes for
# the osids. It processes all of the osid maps in the package maps
# directory.
def make_fedosids(build_abc=False, re_index=False, re_map=False):
    from abcbinder import make_abcosids
    if build_abc:
        make_abcosids(re_index, re_map)
    for json_file in os.listdir(pkg_maps_dir):
        if json_file.endswith('.json'):
            make_fedosid(pkg_maps_dir + '/' + json_file)


# This function expects a file containing a json representation of an
# osid package that was prepared by the mapper.
def make_fedosid(file_name):
    from binder_helpers import get_interface_module

    read_file = open(file_name, 'r')
    package = json.load(read_file)
    read_file.close()

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

    if not root_pkg:
        # Check if an app directory and  osid subdirectory already exist.
        # If not, create them  This code specifically splits out the osid
        # packages in a Django app environment.  For other Python based
        # implementations try using the subsequent, more generic code instead.
        from django.core.management import call_command
        if not os.path.exists(app_name(package['name'])):
            call_command('startapp', app_name(package['name']))
        if not os.path.exists(app_name(package['name']) + '/' +
                              abc_pkg_name(package['name'])):
            os.system('mkdir ' + app_name(package['name']) + '/' +
                      abc_pkg_name(package['name']))
            os.system('touch ' + app_name(package['name']) + '/' +
                      abc_pkg_name(package['name']) + '/__init__.py')
    else:
        # Check if a directory already exists for the implementation.  If not,
        # create one and initialize as a python package.
        if not os.path.exists(app_name(package['name'])):
            os.system('mkdir ' + app_name(package['name']))
            os.system('touch ./' + app_name(package['name']) + '/__init__.py')
        if not os.path.exists(app_name(package['name']) + '/' +
                              abc_pkg_name(package['name'])):
            os.system('mkdir ' + app_name(package['name']) + '/' +
                      abc_pkg_name(package['name']))
            os.system('touch ./' + app_name(package['name']) + '/' +
                      abc_pkg_name(package['name']) + '/__init__.py')

    """
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

    ##
    # Write the summary documentation for this package.
    write_file = open(app_name(package['name']) + '/' +
                      pkg_name(package['name']) + '/doc.py', 'w')
    write_file.write((utf_code + '\"\"\"' +
                      package['title'] + '\n' +
                      package['name'] + ' version ' +
                      package['version'] + '\n\n'+
                      package['summary'] + '\n\n\"\"\"').encode('utf-8'))
    write_file.close

    """

    # Copy settings and types and other files from the authz tamplates into the
    # appropriate implementation directories
    # NEED TO CHANGE TEMPLATE REFERENCE TO USE template_dir VARIABLE
    if os.path.exists('./builders/fedosid_templates/' +
                      package['name'] + '_helpers'):
        # print 'FOUND:', package['name'] + '_helpers'
        for helper_file in os.listdir('./builders/fedosid_templates/' +
                                      package['name'] + '_helpers'):
            if helper_file.endswith('.py'):
                os.system('cp ./builders/fedosid_templates/' +
                          package['name'] + '_helpers/' + helper_file + ' ' +
                          app_name(package['name']) + '/' + pkg_name(package['name']) +
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

    # Get the pattern map for this osid package.
    read_file = open('builders/pattern_maps/' +
                     package['name'] + '.json', 'r')
    patterns = json.load(read_file)
    read_file.close()

    # The real work starts here.  Iterate through all interfaces to build
    # all the django classes for this osid package.
    for interface in package['interfaces']:
        # Seed the inheritance list with this interface's abc_osid
        inheritance = [abc_pkg_name(package['name']) + '_' +
                       interface['category'] + '.' +
                       interface['shortname']]
        # Check to see if there are any additinal inheritances required
        # by the implementation patterns.
        impl_class = load_impl_class(package['name'], interface['shortname'])
        if hasattr(impl_class, 'inheritance'):
            inheritance = inheritance + getattr(impl_class, 'inheritance')

        # And make sure there is a corresponding import statement for this
        # interface's abc_osid and associated module/category name.
        import_str = ('from ' + abc_app_name(package['name']) + '.' +
                      abc_pkg_name(package['name']) + ' import ' +
                      interface['category'] + ' as ' +
                      abc_pkg_name(package['name'] + '_' + interface['category']))
        if import_str not in modules[interface['category']]['imports']:
            modules[interface['category']]['imports'].append(import_str)

        # Iterate through any inherited interfaces and build the inheritance
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

        # Note that the following re-assigns the inheritance variable from a
        # list to a string.
        if inheritance:
            inheritance = '(' + ', '.join(inheritance) + ')'
        else:
            inheritance = ''

        """
        ##
        # Inspect the class doc string for headline + body and create
        # appropriate doc string style. Trying to conform to PEP 257 as
        # much as the source osid doc will allow.
        if interface['doc']['body'].strip() == '':
            class_doc = ('    \"\"\"' + interface['doc']['headline'] + '\"\"\"')
        else:
            class_doc = ('    \"\"\"' + interface['doc']['headline'] + '\n\n' +
                                    interface['doc']['body'] + '\n\n    \"\"\"')
        """

        class_sig = 'class ' + interface['shortname'] + inheritance + ':'

        init_methods = make_init_methods(interface['shortname'], package, patterns)

        methods = make_methods(package['name'], interface, patterns)

        if not init_methods.strip() and not methods.strip():
            init_methods = '    pass'

        modules[interface['category']]['body'] = (
            modules[interface['category']]['body'] +
            class_sig + '\n' +
            # class_doc + '\n' +
            init_methods + '\n' +
            methods + '\n\n\n')

    # Finally, iterate through the completed package module structure and
    # write out both the import statements and class definitions to the
    # appropriate module for this package.
    for module in modules:
        if modules[module]['body'].strip() != '':
            write_file = open(app_name(package['name']) + '/' +
                              pkg_name(package['name']) + '/' +
                              module + '.py', 'w')
            write_file.write(('\n'.join(modules[module]['imports']) + '\n\n\n' +
                              modules[module]['body']).encode('utf-8'))
            write_file.close()


def load_impl_class(package_name, interface_name):
    # Try loading implementations for this interface
    impl_class = None
    try:
        impls = __import__('builders.fedosid_templates.' +
                           package_name,
                           fromlist=[interface_name])
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
    cat_name = patterns['package_catalog_caps']
    impl_class = load_impl_class(package['name'], interface_name)
    if hasattr(impl_class, 'init'):
        return getattr(impl_class, 'init')
    elif interface_name + '.init_pattern' in patterns:
        init_pattern = patterns[interface_name + '.init_pattern']
        try:
            templates = __import__('builders.fedosid_templates.' +
                                   init_pattern.split('.')[0],
                                   globals(), locals(),
                                   [init_pattern.split('.')[-1]])
        except ImportError:
            return ''
    else:
        return ''

    # Check for any special data initializations and call the appropriate makers
    # to assemble them.
    if init_pattern == 'resource.Bin':
        initers = ''
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
                                        'djpkg_name': pkg_name(package['name']),
                                        'pkg_name': package['name'],
                                        'interface_name': interface_name,
                                        'interface_name_title': interface_name.title(),
                                        'initers': initers,
                                        'object_name': object_name,
                                        'object_name_under': camel_to_under(object_name),
                                        'cat_name': cat_name,
                                        'cat_name_under': camel_to_under(cat_name)})
        else:
            return ''
    else:
        return ''


def make_methods(package_name, interface, patterns):
    body = []
    for method in interface['methods']:
        body.append(make_method(package_name, method, interface['shortname'], patterns))
    return '\n\n'.join(body)


def make_method(package_name, method, interface_name, patterns):
    args = ['self']
    method_doc = ''
    method_impl = make_method_impl(package_name, method, interface_name, patterns)

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

# TAKE ANOTHER LOOK AT THIS TO MAKE SURE THE LINE SPACING IS CORRECT #####
#    if method['doc']['body'].strip() == '':
#        blank_lines = '\n\n'
#    else:
#        blank_lines = '\n'
    if method['doc']['body'].strip() == '' and not detail_docs:
        method_doc = ('        \"\"\"' +
                      method['doc']['headline'] +
                      '\"\"\"')
    else:
        method_doc = ('        \"\"\"' + method['doc']['headline'] +
                      '\n' +
                      method['doc']['body'] + '\n' +
                      '\n'.join(detail_docs) + '\n\n        \"\"\"')

# Use this return statement for method docs
#    return (method_sig + '\n' + method_doc + '\n' + method_impl)
# Use this return statement to eliminate method docs
    return method_sig + '\n' + method_impl


def make_method_impl(package_name, method, interface_name, patterns):
    from binder_helpers import camel_to_under
    from binder_helpers import get_interface_module
    from binder_helpers import get_pkg_name
    from binder_helpers import make_plural
    impl = ''
    pattern = ''
    kwargs = {}
    templates = None

    if interface_name + '.' + method['name'] in patterns:
        pattern = patterns[interface_name + '.' + method['name']]['pattern']
        kwargs = patterns[interface_name + '.' + method['name']]['kwargs']

    impl_class = load_impl_class(package_name, interface_name)

    template_class = None
    if pattern:
        try:
            templates = __import__('builders.fedosid_templates.' +
                                   pattern.split('.')[0],
                                   fromlist=[pattern.split('.')[-2]])
        except (ImportError, KeyError):
            pass
        else:
            if hasattr(templates, pattern.split('.')[-2]):
                template_class = getattr(templates, pattern.split('.')[-2])

    # Check if there is a 'by hand' implementation available for this method
    if (impl_class and
            hasattr(impl_class, method['name'])):
        impl = getattr(impl_class, method['name']).strip('\n')

    # If there is no 'by hand' implementation, get the template for the
    # method implementation that serves as the pattern, if one exixts.
    elif (template_class and
          hasattr(template_class, pattern.split('.')[-1] + '_template')):
        template_str = getattr(template_class, pattern.split('.')[-1] +
                               '_template').strip('\n')
        template = string.Template(template_str)

        # Add keyword arguments to template kwargs that are particular
        # to the django implementation
        kwargs['app_name'] = app_name(kwargs['package_name'])
        kwargs['djpkg_name'] = pkg_name(kwargs['package_name'])
        kwargs['abcapp_name'] = abc_app_name(kwargs['package_name'])
        kwargs['abcpkg_name'] = abc_pkg_name(kwargs['package_name'])

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
            kwargs['object_name_under_plural'] = make_plural(camel_to_under(kwargs['object_name']))
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

        impl = template.substitute(kwargs).strip('\n')
    if impl == '':
        impl = '        pass'
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
            supports_str += ',\n#' + m['name']
    supports_str += '\n]'

    try:
        from builders.fedosid_templates import package_profile
        template = string.Template(package_profile.PROFILE_TEMPLATE)
    except (ImportError, AttributeError):
        return ''
    else:
        return template.substitute({'osid_package': osid_package,
                                    'version_str': version_str,
                                    'release_str': release_str,
                                    'supports_str': supports_str})


# The following functions return the app name and module name strings
# by prepending and appending the appropriate suffixes and prefixes. Note
# that the django app_name() function is included to support building of
# the abc osids into a Django project environment.
def abc_app_name(string_):
    if abc_root_pkg:
        return abc_root_pkg
    else:
        return app_prefix + string_ + app_suffix


def abc_pkg_name(string_):
    return abc_prefix + '_'.join(string_.split('.')) + abc_suffix


def impl_root_path(string_):
    if root_path:
        return root_path
    else:
        return app_prefix + string_ + app_suffix


def app_name(string_):
    if root_pkg:
        return root_pkg
    else:
        return app_prefix + string_ + app_suffix


def pkg_name(string_):
    return pkg_prefix + '_'.join(string_.split('.')) + pkg_suffix
