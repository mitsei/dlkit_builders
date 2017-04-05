
import time
import os
import json
import string
from abcbinder_settings import XOSIDNAMESPACEURI as ns
from abcbinder_settings import XOSIDDIRECTORY as xosid_dir
from abcbinder_settings import PKGMAPSDIRECTORY as pkg_maps_dir
from abcbinder_settings import INTERFACMAPSDIRECTORY as interface_maps_dir
from abcbinder_settings import XOSIDFILESUFFIX as xosid_suffix
from abcbinder_settings import ABCPREFIX as abc_prefix
from abcbinder_settings import ABCSUFFIX as abc_suffix
from abcbinder_settings import MAINDOCINDENTSTR as main_doc_indent
from abcbinder_settings import ENCODING as utf_code
from djbuilder_settings import APPNAMEPREFIX as app_prefix
from djbuilder_settings import APPNAMESUFFIX as app_suffix
from djbuilder_settings import PACKAGEPREFIX as pkg_prefix
from djbuilder_settings import PACKAGESUFFIX as pkg_suffix


# This is the entry point for making django-based python classes for
# the osids. It processes all of the osid maps in the package maps
# directory.
def make_djosids(build_abc=False, re_index=False, re_map=False):
    from abcbinder import make_abcosids
    if build_abc:
        make_abcosids(re_index, re_map)
    for json_file in os.listdir(pkg_maps_dir):
        if json_file.endswith('.json'):
            make_djosid(pkg_maps_dir + '/' + json_file)


# This function expects a file containing a json representation of an
# osid package that was prepared by the mapper.
def make_djosid(file_name):
    from django.core.management import call_command
    from binder_helpers import get_interface_module

    read_file = open(file_name, 'r')
    package = json.load(read_file)
    read_file.close()

    import_str = ''
    body_str = ''

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

    # Check if an app directory and dj osid subdirectory already exist.
    # If not, create them  This code specifically splits out the osid
    # packages in a Django app environment, one Django app per osid package.
    if not os.path.exists(app_name(package['name'])):
        call_command('startapp', app_name(package['name']))
    if not os.path.exists(app_name(package['name']) + '/' +
                          pkg_name(package['name'])):
        os.system('mkdir ' + app_name(package['name']) + '/' +
                  pkg_name(package['name']))
        call_command('startapp', pkg_name(package['name']),
                     './' + app_name(package['name']) + '/' +
                     pkg_name(package['name']))

    # Write the osid license documentation file.
    write_file = open(app_name(package['name']) + '/' +
                      pkg_name(package['name']) + '/license.py', 'w')
    write_file.write((utf_code + '\"\"\"' +
                      package['title'] + '\n' +
                      package['name'] + ' version ' +
                      package['version'] + '\n\n' +
                      package['copyright'] + '\n\n' +
                      package['license'] + '\n\n\"\"\"').encode('utf-8'))
    write_file.close()

    # Write the summary documentation for this package.
    write_file = open(app_name(package['name']) + '/' +
                      pkg_name(package['name']) + '/doc.py', 'w')
    write_file.write((utf_code + '\"\"\"' +
                      package['title'] + '\n' +
                      package['name'] + ' version ' +
                      package['version'] + '\n\n' +
                      package['summary'] + '\n\n\"\"\"').encode('utf-8'))
    write_file.close()

    # Copy settings and types and other files from the dj tamplates into the
    # appropriate implementation directories
    if os.path.exists('./builders/djosid_templates/' +
                      package['name'] + '_helpers'):
        print 'FOUND:', package['name'] + '_helpers'
        for helper_file in os.listdir('./builders/djosid_templates/' +
                                      package['name'] + '_helpers'):
            if helper_file.endswith('.py'):
                os.system('cp ./builders/djosid_templates/' +
                          package['name'] + '_helpers/' + helper_file + ' ' +
                          app_name(package['name']) + '/' + pkg_name(package['name']) +
                          '/' + helper_file)

    # Write profile.py file for this package.
    profile_str = make_profile_py(package)
    write_file = open(app_name(package['name']) + '/' +
                      pkg_name(package['name']) + '/profile.py', 'w')
    write_file.write(profile_str)
    write_file.close()

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
        import_str = ('from ' + app_name(package['name']) + '.' +
                      abc_pkg_name(package['name']) + ' import ' +
                      interface['category'] + ' as ' +
                      abc_pkg_name(package['name'] + '_' + interface['category']))
        if import_str not in modules[interface['category']]['imports']:
            modules[interface['category']]['imports'].append(import_str)

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
                import_str = ('from ' + app_name(i['pkg_name']) +
                              '.' + pkg_name(i['pkg_name']) +
                              ' import ' + inherit_category + ' as ' +
                              pkg_name(i['pkg_name']) + '_' + inherit_category)

                if (import_str not in modules[interface['category']]['imports'] and
                        inherit_category != 'UNKNOWN_MODULE'):
                    modules[interface['category']]['imports'].append(import_str)

        # Note that the following re-assigne the inheritance variable from a
        # list to a string.
        if inheritance:
            inheritance = '(' + ', '.join(inheritance) + ')'
        else:
            inheritance = ''

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

        methods = make_methods(package['name'], interface, patterns)

        modules[interface['category']]['body'] = (
            modules[interface['category']]['body'] +
            class_sig + '\n' +
            class_doc + '\n' +
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

# def make_init_methods(interface_name, package, patterns):
#    if interface_name in patterns['package_objects_caps']:
#        return make_object_init_methods(interface_name, package, patterns)
#    else:
#        return ''


def load_impl_class(package_name, interface_name):
    # Try loading implentations for this interface
    impl_class = None
    try:
        impls = __import__('builders.djosid_templates.' +
                           package_name,
                           fromlist=[interface_name])
    except (ImportError, KeyError):
        pass
    else:
        if hasattr(impls, interface_name):
            impl_class = getattr(impls, interface_name)
    return impl_class


def make_init_methods(interface_name, package, patterns):
    templates = None
    init_pattern = ''
    defaults = ''
    initers = ''
    impl_class = load_impl_class(package['name'], interface_name)
    if hasattr(impl_class, 'init'):
        return getattr(impl_class, 'init')
    elif interface_name + '.init_pattern' in patterns:
        init_pattern = patterns[interface_name + '.init_pattern']
        try:
            templates = __import__('builders.djosid_templates.' +
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
    elif init_pattern == 'resource.Resource':
        try:
            initers = make_data_initers(patterns[interface_name + '.persisted_data'],
                                        patterns[interface_name + '.instance_data'])
        except KeyError:
            initers = ''
    elif init_pattern == 'resource.ResourceForm':
        print interface_name
        try:
            initers = make_metadata_initers(patterns[interface_name[:-4] + '.persisted_data'])
        except KeyError:
            initers = ''

    if hasattr(templates, init_pattern.split('.')[-1]):
        template_class = getattr(templates, init_pattern.split('.')[-1])
        if hasattr(template_class, 'init_template'):
            template = string.Template(getattr(template_class, 'init_template'))
            return template.substitute({'app_name': app_name(package['name']),
                                        'dj_pkg_name': pkg_name(package['name']),
                                        'interface_name': interface_name,
                                        'initers': initers})
        else:
            return ''
    else:
        return ''


# Assemble the initializers for data managed by Osid Objects
def make_data_initers(persisted_data, instance_data):
    initers = ''
    for p in persisted_data:
        if (persisted_data[p] in ['boolean',
                                  'string']):
            initers = (
                initers +
                '        self.my_model.' + p + ' = self._' + p +
                '_default = self.my_model.options[\'' + p + '\'][\'default\']\n')
        elif persisted_data[p] == 'osid.id.Id':
            initers = (
                initers +
                '        self.my_model.' + p + '_authority = \'\'\n' +
                '        self.my_model.' + p + '_namespace = \'\'\n' +
                '        self.my_model.' + p + '_identifier = \'\'\n')
    for i in instance_data:
        if instance_data[i] == 'boolean':
            initers = (
                initers +
                '        self.' + i + ' = None\n')
        elif instance_data[i] == 'osid.id.Id':
            initers = (
                initers +
                '        self.' + i + '_authority = \'\'\n' +
                '        self.' + i + '_namespace = \'\'\n' +
                '        self.' + i + '_identifier = \'\'\n')
    return initers


# Assemble the initializers for metadata manged by Osid ObjectForms
def make_metadata_initers(persisted_data):
    from builders.djosid_templates import options
    initers = ''
    defaults = ''
    for data_name in persisted_data:
        template = ''
        if persisted_data[data_name] == 'boolean':
            template = string.Template(options.COMMON_METADATA)
        elif persisted_data[data_name] == 'string':
            template = string.Template(options.COMMON_METADATA +
                                       options.STRING_METADATA)
        elif persisted_data[data_name] == 'osid.id.Id':
            pass
        if template:
            initers = (initers + '        self._' + data_name + '_metadata = {' +
                       template.substitute({'data_name': data_name}) + '\n    }\n')
    return initers


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

    return (method_sig + '\n' + method_doc + '\n' + method_impl)


def make_method_impl(package_name, method, interface_name, patterns):
    from binder_helpers import camel_to_under
    impl = ''
    pattern = ''
    kwargs = {}
    templates = None

    if interface_name + '.' + method['name'] in patterns:
        pattern = patterns[interface_name + '.' + method['name']]['pattern']
        kwargs = patterns[interface_name + '.' + method['name']]['kwargs']

#    try:
#        pattern = patterns[interface_name + '.' + method['name']]['pattern']
#    except KeyError:
#        pass
#    try:
#        kwargs = patterns[interface_name + '.' + method['name']]['kwargs']
#    except KeyError:
#        pass

    impl_class = None
    try:
        impl_class = load_impl_class(package_name, interface_name)
    except KeyError:
        pass

    template_class = None
    if pattern:
        try:
            templates = __import__('builders.djosid_templates.' +
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
        if 'return_pkg' in kwargs:
            kwargs['return_app_name'] = app_name(kwargs['return_pkg'])
            kwargs['return_djpkg_name'] = pkg_name(kwargs['return_pkg'])
            kwargs['return_pkg_title'] = kwargs['return_pkg'].title()
        if 'return_type' in kwargs:
            kwargs['return_type_under'] = camel_to_under(kwargs['return_type'])
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
        print interface_name, method['name']
        impl = template.substitute(kwargs).strip('\n')

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
                   str(version_list[2] + 1) + '] # Not updating properly, please fix!')

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
            supports_str = supports_str + ',\n#' + m['name']
    supports_str = supports_str + '\n]'

    try:
        from builders.djosid_templates import package_profile
        template = string.Template(package_profile.PROFILE_TEMPLATE)
    except (ImportError, AttributeError):
        return ''
    else:
        return template.substitute({'osid_package': osid_package,
                                    'version_str': version_str,
                                    'release_str': release_str,
                                    'supports_str': supports_str})

# ------ Functions below this line may or may not be necessary #########


def interface_iterator(root, package_name):
    interface_str = root.get(ns + 'name').split('.')[-1]
    inherit_str = ''
    doc_str = '##\n'
    method_str = ''
    for child in root:
        if child.tag == (ns + 'implements'):
            impl_name = child.get(ns + 'interface').split('.')[-1]
            if impl_name:
                impl_pkg = child.get(ns + 'interface').split('.')[-2]
                if package_name != impl_pkg:
                    impl_name = abc_module_name(impl_pkg) + '.' + impl_name
                inherit_str = append_impl_str(impl_name, inherit_str)
        if child.tag == (ns + 'description'):
            doc_str = doc_str + process_text(child)
        if child.tag == (ns + 'method'):
            method_str = method_str + method_iterator(child) + '\n\n'
    if inherit_str:
        inherit_str = '(' + inherit_str + ')'
    class_str = 'class ' + interface_str + inherit_str + ':'
    return (doc_str + '\n\n' + class_str + '\n    __metaclass__ = abc.ABCMeta' +
            '\n\n' + method_str + '\n')


# This function creates all the parts of an abstract osid method, including
# the doc (most of the code deals with doc), and the method signature
# with abc decorator, input arguments and either a 'return' or 'pass'
# depending on whether the method returns anything or not.
def method_iterator(root):
    from binder_helpers import fix_reserved_word
    method_name = root.get(ns + 'name')
    def_str = '    @abc.abstractmethod\n    def ' + method_name
    doc_str = '    ##\n'
    param_str = '(self'
    return_str = '        pass'
    for child in root:
        if child.tag == (ns + 'description'):
            doc_str = doc_str + process_text(child, '    # ') + '\n    #\n'
        if child.tag == (ns + 'parameter'):
            param = child.get(ns + 'name')
            param = fix_reserved_word(param)
            param_str = param_str + ', ' + param
            doc_str = append_method_param_doc_str(child, doc_str)
        if child.tag == (ns + 'return'):
            doc_str = append_method_return_doc_str(child, doc_str)
            return_str = '        return'
        if child.tag == (ns + 'error'):
            doc_str = append_method_error_doc_str(child, doc_str)
        if child.tag == (ns + 'compliance'):
            doc_str = append_method_compliance_doc_str(child, doc_str)
        if child.tag == (ns + 'implNotes'):
            doc_str = append_method_implnotes_doc_str(child, doc_str)

    def_str = def_str + param_str + '):'
    return doc_str + '\n' + def_str + '\n' + return_str


# This function iterates through the method tree and appends the docs
# regarding method parameters to the documentation string
def append_method_param_doc_str(root, doc_str):
    from binder_helpers import wrap_and_indent
    param_str = 'arg:    ' + root.get(ns + 'name')
    for child in root:
        if child.tag == (ns + 'interfaceType'):
            param_str = param_str + ' (' + child.get(ns + 'type') + '): '
        if child.tag == (ns + 'primitiveType'):
            param_str = param_str + ' (' + child.get(ns + 'type') + '): '
        if child.tag == (ns + 'description'):
            param_str = param_str + process_text(child, '', '')
    return doc_str + wrap_and_indent(param_str.strip(),
                                     '    # ',
                                     '    #         ') + '\n'


# This function iterates through the method tree and appends the docs
# regarding the method return type to the documentation string
def append_method_return_doc_str(root, doc_str):
    from binder_helpers import wrap_and_indent
    return_str = 'return: '
    for child in root:
        if child.tag == (ns + 'interfaceType'):
            return_str = return_str + '(' + child.get(ns + 'type') + ') - '
        if child.tag == (ns + 'primitiveType'):
            return_str = return_str + '(' + child.get(ns + 'type') + ') - '
        if child.tag == (ns + 'description'):
            return_str = return_str + process_text(child, '', '')
            return doc_str + wrap_and_indent(return_str.strip(),
                                             '    # ',
                                             '    #         ') + '\n'


# This function iterates through the method tree and appends the docs
# regarding the possible exceptions raised by this method.
def append_method_error_doc_str(root, doc_str):
    from binder_helpers import wrap_and_indent
    error_str = 'raise:  ' + root.get(ns + 'type') + ' - '
    for child in root:
        if child.tag == (ns + 'description'):
            error_str = error_str + process_text(child, '', '')
    return doc_str + wrap_and_indent(error_str.strip(),
                                     '    # ',
                                     '    #         ') + '\n'


# This function iterates through the method tree and appends the docs
# regarding the comliance required for this method.
def append_method_compliance_doc_str(root, doc_str):
    from binder_helpers import wrap_and_indent
    comp_str = 'compliance: ' + root.get(ns + 'type') + ' - '
    for child in root:
        if child.tag == (ns + 'description'):
            comp_str = comp_str + process_text(child, '', '')
    return doc_str + wrap_and_indent(comp_str.strip(),
                                     '    # ',
                                     '    #             ') + '\n'


# This function iterates through the method tree and appends the docs
# pertaining to implementation notes for this method.
def append_method_implnotes_doc_str(root, doc_str):
    from binder_helpers import wrap_and_indent
    note_str = 'implementation notes: '
    note_str = note_str + process_text(root, '', '')
    return doc_str + wrap_and_indent(note_str.strip(),
                                     '    # ',
                                     '    # ') + '\n'


# Send any text blocks to this function that includes text tags for things
# like copyright symbols, paragraphs breaks, headings, tokens and code blocks
# and outlines.  Outlines are dispatched to make_outline which isn't afraid
# to deal with them (but it should be).
def process_text(root, i_indent='# ', s_indent=None):
    from binder_helpers import wrap_and_indent
    from binder_helpers import reindent
    if not s_indent:
        s_indent = i_indent
    make_str = ''
    iter_str = ' '.join(root.text.split())
    for child in root:
        if child.tag == (ns + 'copyrightSymbol'):
            iter_str = iter_str + ' (c) ' + ' '.join(child.tail.split()) + ' '
        if child.tag == (ns + 'pbreak'):
            make_str = (make_str + wrap_and_indent(iter_str,
                                                   i_indent, s_indent)) + '\n' + i_indent + '\n'
            iter_str = ' '.join(child.tail.split())
        if child.tag == (ns + 'heading'):
            iter_str = iter_str + ' '.join(str(child.text).split())
            iter_str = iter_str + '' + ' '.join(str(child.tail).split()) + ''
        if child.tag == (ns + 'token'):
            iter_str = iter_str + ' ' + ' '.join(str(child.text).split()) + ' '
            iter_str = iter_str + '' + ' '.join(str(child.tail).split()) + ''
        if child.tag == (ns + 'code'):
            make_str = (make_str + wrap_and_indent(iter_str,
                                                   i_indent, s_indent)).strip() + '\n'
            iter_str = reindent(child.text.strip(), i_indent + '  ')
            make_str = make_str + iter_str + i_indent + '\n'
            iter_str = ' '.join(child.tail.split())
        if child.tag == (ns + 'outline'):
            make_str = (make_str + wrap_and_indent(iter_str,
                                                   i_indent, s_indent)).strip() + '\n'
            iter_str = make_outline(child, i_indent + '  * ',
                                    i_indent + '    ')
            make_str = make_str + iter_str.strip()
            iter_str = ' '.join(child.tail.split())
    return make_str + wrap_and_indent(iter_str, i_indent, s_indent)


# This function is used to properly process outline tagged text, so be kind
# to it.
def make_outline(root, i_indent, s_indent=None):
    from binder_helpers import wrap_and_indent
    if not s_indent:
        s_indent = i_indent
    outline_str = ''
    iter_str = ''
    for child in root:
        if child.tag == (ns + 'element'):
            iter_str = ' '.join(child.text.split())
            for elem in child.iter():
                if elem.tag == (ns + 'token'):
                    iter_str = iter_str + ' ' + ' '.join(str(elem.text).split()) + ' '
                    iter_str = iter_str + '' + ' '.join(str(elem.tail).split()) + ''
            iter_str = wrap_and_indent(iter_str, i_indent, s_indent)
            outline_str = outline_str + iter_str + '\n'
    return outline_str


# This little function simply appends the class inheritance string (impl_str)
# with each of the osid classes (impl's) sent to it by the method iterator
def append_impl_str(impl, impl_str):
    if impl_str:
        impl_str = impl_str + ', ' + impl
    else:
        impl_str = impl_str + impl
    return impl_str


# The following functions return the app name and module name strings
# by prepending and appending the appropriate suffixes and prefixes. Note
# that the django app_name() function is included to support building of
# the abc osids into a Django project environment.
def abc_pkg_name(string_):
    return abc_prefix + string_ + abc_suffix


def app_name(string_):
    return app_prefix + string_ + app_suffix


def pkg_name(string_):
    return pkg_prefix + string_ + pkg_suffix


# This function returns a string the represents the type of osid interface,
# like object, session, primitive, for creating a package sructure.  If the
# global flag pkgScheme is set to 'verbose', then this function will simply
# return the camelToUnderscore name of the interface, resulting in every
# interface living in its own sub-package
def spi_type(inherit_list, interface_str):
    from binder_helpers import camel_to_list
    if ('OsidObject' in inherit_list or
            'OsidObjectQuery' in inherit_list or
            'OsidObjectQueryInspector' in inherit_list or
            'OsidForm' in inherit_list or
            'OsidObjectForm' in inherit_list or
            'OsidObjectSearchOrder' in inherit_list or
            'OsidSearch' in inherit_list or
            'OsidSearchResults' in inherit_list or
            'OsidReceiver' in inherit_list or
            'OsidList' in inherit_list or
            'OsidNode' in inherit_list or
            'OsidRelationship' in inherit_list or
            'OsidRelationshipQuery' in inherit_list or
            'OsidRelationshipQueryInspector' in inherit_list or
            'OsidRelationshipForm' in inherit_list or
            'OsidRelationshipSearchOrder' in inherit_list or
            'OsidCatalog' in inherit_list or
            'OsidCatalogQuery' in inherit_list or
            'OsidCatalogQueryInspector' in inherit_list or
            'OsidCatalogForm' in inherit_list or
            'OsidCatalogSearchOrder' in inherit_list):
        return 'objects'
    elif ('OsidSession' in inherit_list or
          camel_to_list(interface_str)[-1] == 'Session'):
        return 'sessions'
    elif ('OsidProfile' in inherit_list or
          'OsidManager' in inherit_list or
          'OsidProxyManager' in inherit_list):
        return 'managers'
    elif ('OsidPrimitive' in inherit_list):
        return 'primitives'
    elif ('OsidRecord' in inherit_list):
        return 'records'
    else:
        return 'other_please_move'
