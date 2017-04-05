
from abcbinder_settings import XOSIDNAMESPACEURI as ns
from abcbinder_settings import xosid_dirECTORY as xosid_dir
from abcbinder_settings import xosid_fileSUFFIX as xosid_suffix
from abcbinder_settings import abc_prefix as abc_prefix
from abcbinder_settings import ABCROOTPACKAGE as abc_pkg_name
from abcbinder_settings import FIRSTDOCindent_str as indent_str
from djbuilder_settings import ENCODING as utfStr
from djbuilder_settings import app_namePREFIX as app_prefix
from djbuilder_settings import app_nameSUFFIX as app_suffix
from djbuilder_settings import PACKAGEPREFIX as prefix
from djbuilder_settings import PACKAGESUFFIX as suffix
from djbuilder_settings import SUBPACKAGEPREFIX as sub_prefix
from djbuilder_settings import SUBPACKAGESUFFIX as sub_suffix
pkgScheme = 'verbose'


def make_djosids(make_models=False):
    import time
    import os
    global _total_method_count
    global _implemented_method_count
    global _total_interface_count
    global _implemented_interface_count
    global _package_interface_count
    global _package_implemented_interface_count
    global _package_implemented_method_count
    global _package_method_count

    # Iterate over each xosid.xml package in the xosid directory:
    start_time = time.time()
    package_count = 0
    _total_method_count = 0
    _implemented_method_count = 0
    _total_interface_count = 0
    _implemented_interface_count = 0

    for xosid_file in os.listdir(xosid_dir):
        package_count += 1
        if xosid_file.endswith(xosid_suffix):
            make_djosid(xosid_dir + '/' + xosid_file, make_models)
            _total_method_count = _total_method_count + _package_method_count
            _implemented_method_count = _implemented_method_count + _package_implemented_method_count
            _total_interface_count = _total_interface_count + _package_interface_count
            _implemented_interface_count = _package_implemented_interface_count

    # When done, report out implementation statistics:
    print (str(package_count) + ' osid packages built in ' +
           str(time.time() - start_time) + ' seconds.\n' +
           str(_implemented_method_count) + ' of ' +
           str(_total_method_count) + ' methods (' +
           "{0:.0f}%".format(float(_implemented_method_count) /
                                  ( _total_method_count) * 100) +
           ') implemented in ' +
           str(_implemented_interface_count) + ' of ' +
           str(_total_interface_count) + ' interfaces.')



def make_djosid(file_name, make_models=False, make_package=True):
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET
    import os
    from django.core import management
    from binder_helpers import wrap_and_indent
    global _package_interface_count
    global _package_implemented_interface_count
    global _package_implemented_method_count
    global _package_method_count    
    _package_method_count = 0
    _package_implemented_method_count = 0
    _package_interface_count = 0
    _package_implemented_interface_count = 0

    tree = ET.parse(file_name)
    root = tree.getroot()
    body_str = ''
    model_import_str = 'from django.db import models\nimport osid_kit.models\n\n'
    this_model = ''
    model_str = ''
    modules = dict(objects='', sessions='', managers='',
                   primitives='', records='', other_please_move='')
    for elem in root.iter(ns + 'osid'):
        # Get version and package name information from XML header and
        # import osid package in all non-osid modules
        package_name = (elem.get(ns + 'name')).split('.')[-1]
        version_str = wrap_and_indent((elem.get(ns + 'name')) +
                                      ' ' + (elem.get(ns + 'version')),
                                      i_indent=indent_str) + '\n'
        import_str = ('import abc\nfrom ' + abc_pkg_name + ' import ' +
                      abc_prefix + package_name + '\n')
        if package_name != 'osid':
            import_str = (import_str + 'from ' + app_name('osid') + 
                          ' import ' + pkg_name('osid') + '\n')
        import_str = import_str + '\n\n'

    # Send the tree root through the three main documentation iterators
    # to build the basic package documentation strings.
    head_str = head_iterator(root, package_name, version_str)
    license_str = license_iterator(root, package_name, version_str)
    summary_string = summary_iterator(root, package_name, version_str)

    # Check if there is already a Django app with this toolkit name.  If not,
    # invoke the Django manager startapp function to create one.
    if not os.path.exists(app_name(package_name)):
        management.call_command('startapp', app_name(package_name))

    # The real work starts here.  Iterate through all child elements in the
    # tree root and invoke the interface_iterator to build all interfaces
    # of this osid package.  The package strings are sorted into thier
    # appropriate package modules.
    for child in root:
        if child.tag == (ns + 'interface'):
            interface = interface_iterator(child, package_name, root)
            module_name = interface['module_name']
            interface_str = interface['interfaceBody']
            modules[module_name] = modules[module_name] + interface_str
            if make_models:
                model_str = model_str + model_iterator(child, package_name, root)

    # Save the model string to the models.py file in the appropriate Django app
    # making sure not to overwrite the osid_kit and type_kit models while we
    # are still trying to figure things out.    
    if package_name != 'osid' and package_name != 'type' and make_models:
        print 'writing', app_name(package_name), 'Django models'
        write_file = open(app_name(package_name) + '/models.py', 'w')
        write_file.write((model_import_str + model_str).encode('utf-8'))
        write_file.close()

    # Finally create the modules for this osid package.  If older ones exist
    # this will overwrite them.
    print 'writing', app_name(package_name), 'packages'
    if not os.path.exists(app_name(package_name) + '/' + pkg_name(package_name)):
        os.makedirs(app_name(package_name) + '/' + pkg_name(package_name))
        os.system('touch ' + app_name(package_name) + '/' + 
                  pkg_name(package_name) + '/__init__.py')

    for module_name in modules:
        print module_name
        write_file = open(app_name(package_name) + '/' + pkg_name(package_name) +
                          '/' + module_name + '.py', 'w')
        write_file.write((head_str + import_str + modules[module_name]).encode('utf-8'))
        write_file.close()


def head_iterator(root, package_name, version_str):
    from binder_helpers import wrap_and_indent
    head_str = utfStr + '#\n#'

    # Iterate through the element tree searching for the 'title'.  That's all.
    # This used to do more, but now it only does this :(
    for child in root:
        if child.tag == (ns + 'title'):
            title_str = (wrap_and_indent(child.text, indent_str) +
                         '\n' + indent_str + '\n' + indent_str + '\n')
    return version_str + title_str


def license_iterator(root, package_name, version_str):
    from binder_helpers import wrap_and_indent
    head_str = utfStr + '#\n#'

    # Iterate through the element tree searching for the 'title', 'copyright'
    # and 'license' tags.  Returns the entire header string, including
    # the version string which is passed in.
    for child in root:
        if child.tag == (ns + 'title'):
            title_str = (wrap_and_indent(child.text, indent_str) +
                         '\n' + indent_str + '\n' + indent_str + '\n')
        if child.tag == (ns + 'copyright'):
            legal_str = (process_text(child) + '\n'
                                 + indent_str + '\n' + indent_str + '\n')
        if child.tag == (ns + 'license'):
            legal_str = legal_str + process_text(child) +'\n\n\n'
    return head_str + version_str + title_str + legal_str


def summary_iterator(root, package_name, version_str):
    from binder_helpers import wrap_and_indent
    head_str = utfStr + '#\n#'

    # Iterate through the element tree searching for the 'title', and
    # 'description' tags.  Returns the a string containing the summary,
    # documentation, including the version string which is passed in.
    for child in root:
        if child.tag == (ns + 'title'):
            title_str = (wrap_and_indent(child.text, indent_str) +
                         '\n' + indent_str + '\n' + indent_str + '\n')
        if child.tag == (ns + 'description'):
            info_str = (process_text(child) + '\n\n\n')
    return head_str + version_str + title_str + info_str


def interface_iterator(root, package_name, package_root, make_package=False):
    global _package_interface_count
    global _package_implemented_interface_count
    from djinitmaker import make_init_methods
    from djmodelmaker import make_models
    from binder_helpers import get_return_type
    from binder_helpers import get_param_list
    interface_str = root.get(ns + 'name').split('.')[-1]
    inherit_str = append_impl_str(abc_prefix + package_name +
                                  '.' + interface_str, '')
    inherit_list = []
    doc_str = '##\n'
    method_str = ''
    method_list = []
    init_methods = ''
    for child in root:
        if child.tag == (ns + 'implements'):
            impl_name = child.get(ns + 'interface').split('.')[-1]
            if impl_name:
                inherit_list.append(impl_name)
                impl_pkg = child.get(ns + 'interface').split('.')[-2]
                if package_name != impl_pkg:
                    impl_name = pkg_name(impl_pkg) + '.' + impl_name
                inherit_str = append_impl_str(impl_name, inherit_str)
        if child.tag == (ns + 'description'):
            doc_str = doc_str + process_text(child)
        if child.tag == (ns + 'method'):
            method_list.append(dict(method_name = child.get(ns + 'name'),
                                   return_type = get_return_type(child),
                                   param_list = get_param_list(child)))
            method_str = method_str + method_iterator(child, package_name,
                                    interface_str, inherit_list, root,
                                    package_root) + '\n\n'
    if inherit_str:
        inherit_str = '(' + inherit_str + ')'
    class_str = 'class ' + interface_str + inherit_str + ':'
    init_methods = make_init_methods(package_name, interface_str,
                                    inherit_list, method_list, package_root)
    if init_methods:
        init_methods = init_methods + '\n'
    if not method_str:
        method_str = '    pass\n\n'
        _package_implemented_interface_count += 1
    _package_interface_count += 1

    return dict(interfaceBody = (doc_str + '\n\n' + class_str + '\n\n' +
                init_methods + method_str + '\n'),
                module_name = spiType(inherit_list, interface_str))


def model_iterator(root, package_name, package_root):
    from djmodelmaker import make_models
    from binder_helpers import get_return_type
    from binder_helpers import get_param_list
    interface_str = root.get(ns + 'name').split('.')[-1]
    inherit_str = ''
    inherit_list = []
    method_list = []
    for child in root:
        if child.tag == (ns + 'implements'):
            impl_name = child.get(ns + 'interface').split('.')[-1]
            if impl_name:
                inherit_list.append(impl_name)
                impl_pkg = child.get(ns + 'interface').split('.')[-2]
                if package_name != impl_pkg:
                    impl_name = app_name(impl_pkg) + '.models.' + impl_name
                inherit_str = append_impl_str(impl_name, inherit_str)
        if child.tag == (ns + 'method'):
            method_list.append(dict(method_name=child.get(ns + 'name'),
                                   return_type=get_return_type(child),
                                   param_list=get_param_list(child)))
    inherit_str = append_impl_str('models.Model', inherit_str)
    if inherit_str:
        inherit_str = '(' + inherit_str + ')'
    class_str = 'class ' + interface_str + inherit_str + ':'
    model_str = make_models(package_name, interface_str,
                                    inherit_list, method_list, package_root)
    if model_str:
        return (class_str + '\n' + model_str + '\n')
    else:
        return ''


def method_iterator(root, package_name, interface_name, inherit_list, interface_root, package_root):
    from djimplmaker import make_method_impl
    from binder_helpers import fix_reserved_word
    from binder_helpers import get_return_type
    from binder_helpers import camel_to_under
    global _package_implemented_method_count
    global _package_method_count
    method_name = root.get(ns + 'name')
    def_str = '    def ' + camel_to_under(method_name)
    impl_str = ''
    doc_str = '    ##\n'
    param_str = '(self'
    param_list = ['self']
    error_list = []
    return_str = '        pass'
    return_type = get_return_type(root)
    for child in root:
        if child.tag == (ns + 'description'):
            doc_str = doc_str + process_text(child, '    # ') + '\n    #\n'
        if child.tag == (ns + 'parameter'):
            param = child.get(ns + 'name')
            param = fix_reserved_word(param)
            param_list.append(param)
            param_str = param_str + ', ' + param
            doc_str = append_method_param_doc_str(child, doc_str)
        if child.tag == (ns + 'return'):
            doc_str = append_method_return_doc_str(child, doc_str)
            return_str = '        return'
        if child.tag == (ns + 'error'):
            error_list.append(child.get(ns + 'type'))
            doc_str = append_method_error_doc_str(child, doc_str)
        if child.tag == (ns + 'compliance'):
            doc_str = append_method_compliance_doc_str(child, doc_str)
        if child.tag == (ns + 'implNotes'):
            doc_str = append_method_implnotes_doc_str(child, doc_str)
    impl_str = make_method_impl(package_name, interface_name,
                                inherit_list, method_name, param_list,
                                return_type, error_list, interface_root,
                                package_root)
    if not impl_str:
        impl_str = return_str
    else:
        _package_implemented_method_count += 1
    _package_method_count += 1
    def_str = def_str + param_str + '):'
    return doc_str + '\n' + def_str + '\n' + impl_str


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
    from binder_helpers import camel_to_under

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
            if '()' in str(child.text):
                converted_text = camel_to_under(child.text)
            else:
                converted_text = child.text
            iter_str = iter_str + ' ' + ' '.join(str(converted_text).split()) + ' '
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


# This function is used to properly process outline tagged text
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


# The following functions return the app name and package name strings
# by prepending and appending the appropriate suffixes and prefixes.
def app_name(string_):
    return app_prefix + string_ + app_suffix


def pkg_name(string_):
    return prefix + string_ + suffix


def subpkg_name(string_):
    return sub_prefix + string_ + sub_suffix


# This function returns a string the represents the type of osid interface,
# like object, session, primitive, for creating a package sructure.  If the
# global flag pkgScheme is set to 'verbose', then this function will simply
# return the camelToUnderscore name of the interface, resulting in every
# interface living in its own sub-package
def spiType(inherit_list, interface_str):
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
