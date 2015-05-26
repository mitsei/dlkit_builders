
#import time
import os
import json
from abcbinder_settings import XOSIDNAMESPACEURI as ns
from abcbinder_settings import XOSIDDIRECTORY as xosid_dir
from abcbinder_settings import PKGMAPSDIRECTORY as pkg_maps_dir
from abcbinder_settings import INTERFACMAPSDIRECTORY as interface_maps_dir
from abcbinder_settings import XOSIDFILESUFFIX as xosid_suffix
from abcbinder_settings import ABCROOTPACKAGE as abc_root_pkg
from abcbinder_settings import ABCPREFIX as abc_prefix
from abcbinder_settings import ABCSUFFIX as abc_suffix
#from abcbinder_settings import MAINDOCINDENTSTR as main_doc_indent
from abcbinder_settings import ENCODING as utf_code

# These next two are here for the purpose of loading abc modules
# in a django app, where the goal is to distribute the abc osids
# across the service kit packages.
from djbuilder_settings import APPNAMEPREFIX as app_prefix
from djbuilder_settings import APPNAMESUFFIX as app_suffix

include_inheritance = False

##
# This is the entry point for making the Python abstact base classes for
# the osids. It processes all of the osids in the xosid directory, making
# sure they have all been mapped to json, before sending each json file
# off to be built into the abcosids.
def make_abcosids(re_index = False, re_map = False):
    from mappers import make_xosid_map
    from mappers import make_interface_map
    for xosid_file in os.listdir(xosid_dir):
        package = None
        if xosid_file.endswith(xosid_suffix):
            if (not os.path.exists(pkg_maps_dir + '/' +
                xosid_file.split('.')[-2] + '.json') or re_map == True):
                print 'mapping', xosid_file.split('.')[-2], 'osid.'
                package = make_xosid_map(xosid_dir + '/' + xosid_file)
            if (not os.path.exists(interface_maps_dir + '/' +
                xosid_file.split('.')[-2] + '.json') or re_index == True):
                print 'indexing interfaces for', xosid_file.split('.')[-2], 'osid.'
                make_interface_map(xosid_dir + '/' + xosid_file, package)
    for json_file in os.listdir(pkg_maps_dir):
        if json_file.endswith('.json'):
            make_abcosid(pkg_maps_dir + '/' + json_file)

##
# This function expects a file containing a json representation of an
# osid package that was prepared by the mapper.
def make_abcosid(file_name):

    read_file = open(file_name, 'r')
    package = json.load(read_file)
    read_file.close()
    
    print "Building ABC osid for " + package['name']

    importStr = 'import abc\n'
    bodyStr = ''
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

    if not abc_root_pkg:
        ##
        # Check if an app directory and abc osid subdirectory already exist.  
        # If not, create them  This code specifically splits out the osid 
        # packages in a Django app environment.  For other Python based
        # implementations try using the subsequent, more generic code instead.
        from django.core.management import call_command
        if not os.path.exists(app_name(package['name'])):
            call_command('startapp', app_name(package['name']))
        if not os.path.exists(app_name(package['name']) + '/' + 
                              abc_pkg_name(package['name'])):
            os.system('mkdir '+ app_name(package['name']) + '/' + 
                      abc_pkg_name(package['name']))
            os.system('touch ' + app_name(package['name']) + '/' + 
                      abc_pkg_name(package['name']) + '/__init__.py')
    else:
        ##
        # Check if a directory already exists for the abc osid.  If not,
        # create one and initialize as a python package.
        if not os.path.exists(app_name(package['name'])):
            os.system('mkdir '+ app_name(package['name']))
            os.system('touch ./' + app_name(package['name']) + '/__init__.py')
        if not os.path.exists(app_name(package['name']) + '/' + 
                              abc_pkg_name(package['name'])):
            os.system('mkdir '+ app_name(package['name']) + '/' + 
                                abc_pkg_name(package['name']))
            os.system('touch ./' + app_name(package['name']) + '/' + 
                             abc_pkg_name(package['name']) + '/__init__.py')
    ##
    # Write the osid license documentation file.
    write_file = open(app_name(package['name']) + '/' + 
                     abc_pkg_name(package['name']) + '/license.py', 'w')
    write_file.write((utf_code + '\"\"\"' +
                      package['title'] + '\n' +
                      package['name'] + ' version ' +
                      package['version'] + '\n\n'+
                      package['copyright'] + '\n\n' +
                      package['license'] + '\n\n\"\"\"').encode('utf-8') +
                      '\n')
    write_file.close

    ##
    # Write the summary documentation for this package.
    write_file = open(app_name(package['name']) + '/' + 
                     abc_pkg_name(package['name']) + '/doc.py', 'w')
    write_file.write((utf_code + '\"\"\"' +
                      package['title'] + '\n' +
                      package['name'] + ' version ' +
                      package['version'] + '\n\n'+
                      package['summary'] + '\n\n\"\"\"').encode('utf-8') +
                      '\n')
    write_file.close

    ##
    # Initialize the module doc and abc import string for each module
    for module in modules:
        docstr = ('\"\"\"Implementations of ' + package['name'] + 
            ' abstract base class ' + module + '.\"\"\"\n' +
            '# pylint: disable=invalid-name\n' + 
            '#     Method names comply with OSID specification.\n' +
            '# pylint: disable=no-init\n' + 
            '#     Abstract classes do not define __init__.\n' +
            '# pylint: disable=too-few-public-methods\n' + 
            '#     Some interfaces are specified as \'markers\' and include no methods.\n'+
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

    ##
    # The real work starts here.  Iterate through all interfaces to build 
    # all the abc classes for this osid package.
    for interface in package['interfaces']:
        inheritance = []
        additional_methods = ''

        ##
        # Make certain foundational classes new-style Python objects,
        # but this may not be necessary, so now commented out:
        #if interface['shortname'] == 'Identifiable':
        #    inheritance.append('object')

        ##
        # Interate through any inherited interfaces and build the inheritance
        # list for this interface. Also, check if an import statement is
        # required and append to the appropriate module's import list.
        for i in interface['inheritance']:
            if not include_inheritance:
                break
            unknown_module_protection = ''
            inherit_category = get_interface_module(i['pkg_name'], i['name'], True)
            if inherit_category == 'UNKNOWN_MODULE':
                unknown_module_protection = '\"\"\"'
            if (i['pkg_name'] == package['name'] and
                  inherit_category == interface['category']):
                inheritance.append(i['name'])
            else:
                inheritance.append(unknown_module_protection + 
                                   abc_pkg_name(i['pkg_name']) + '_' +
                                   inherit_category + '.' + i['name'] +
                                   unknown_module_protection)
                import_str = ('from ..'+ abc_pkg_name(i['pkg_name']) + 
                              ' import ' + inherit_category + ' as ' +
                              abc_pkg_name(i['pkg_name']) + '_' + inherit_category)
#                import_str = ('from ' + app_name(i['pkg_name']) +
#                              '.'+ abc_pkg_name(i['pkg_name']) + 
#                              ' import ' + inherit_category + ' as ' +
#                              abc_pkg_name(i['pkg_name']) + '_' + inherit_category)
                if (import_str not in modules[interface['category']]['imports'] and
                    inherit_category != 'UNKNOWN_MODULE'):
                    modules[interface['category']]['imports'].append(import_str)

        ##
        # Note that the following re-assigne the inheritance variable from a 
        # list to a string.
        if inheritance:
            inheritance = '(' + ', '.join(inheritance) + ')'
        else:
            inheritance = ''
        
        ##
        # Add the equality methods to Ids and Types:
        if interface['shortname'] == 'Id' or interface['shortname'] == 'Type':
            additional_methods = additional_methods + eq_methods(interface['shortname'])
#        if interface['shortname'] == 'Id':
            additional_methods = additional_methods + str_methods()
        

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

        modules[interface['category']]['body'] = (
                            modules[interface['category']]['body'] + 
                            class_sig + '\n' +
                            class_doc + '\n' +
                            '    __metaclass__ = abc.ABCMeta\n\n' +
                            additional_methods +
                            make_methods(interface['methods']) + '\n\n\n')
    ##
    # Finally, iterate through the completed package module structure and
    # write out both the import statements and class definitions to the
    # appropriate module for this package.
    for module in modules:
        if modules[module]['body'].strip() != '':
            write_file = open(app_name(package['name']) + '/' + 
                              abc_pkg_name(package['name']) + '/' +
                              module + '.py', 'w')
            write_file.write(('\n'.join(modules[module]['imports']) + '\n\n\n' +
                              modules[module]['body']).encode('utf-8'))
            write_file.close

##
# This function also exists in binder_helpers. Should point callers to 
# that one instead
def get_interface_module(pkg_name, interface_shortname, report_error = False):
    category = 'UNKNOWN_MODULE'
    try:
        read_file = open(interface_maps_dir + '/' + pkg_name + '.json' , 'r')
        index = json.load(read_file)
        read_file.close()
    except IOError:
        if report_error:
            #print ('INTERFACE LOOKUP ERROR - interface map for \'' + pkg_name + 
            #       '\' not found.')
            pass
    else:
        try:
            category = index[pkg_name + '.' + interface_shortname]
        except KeyError:
            if report_error:
                #print ('INTERFACE LOOKUP ERROR - category for \'' + pkg_name + '.'
                #       + interface_shortname + '\' not found.')
                pass
    return category


def make_methods(methods):
    from binder_helpers import fix_reserved_word
    body = []
    for method in methods:
        body.append(make_method(method))

        ##
        # Here is where we add the Python properties stuff:
        if method['name'].startswith('get_') and method['args'] == []:
            body.append('    ' + fix_reserved_word(method['name'][4:]) + 
                    ' = abc.abstractproperty(fget=' + method['name'] + ')')
        elif method['name'].startswith('set_') and len(method['args']) == 1:
            if ('    ' + fix_reserved_word(method['name'][4:]) + ' = abc.abstractproperty(fdel=clear_' + method['name'][4:] + ')') in body:
                body.remove('    ' + fix_reserved_word(method['name'][4:]) + ' = abc.abstractproperty(fdel=clear_' + method['name'][4:] + ')')
                body.append('    ' + fix_reserved_word(method['name'][4:]) + 
                        ' = abc.abstractproperty(fset=' + method['name'] +
                        ', fdel=clear_' + method['name'][4:] + ')')
            else:
                body.append('    ' + fix_reserved_word(method['name'][4:]) + 
                        ' = abc.abstractproperty(fset=' + method['name'] + ')')
        elif method['name'].startswith('clear_') and method['args'] == []:
            if ('    ' + fix_reserved_word(method['name'][6:]) + ' = abc.abstractproperty(fset=set_' + method['name'][6:] + ')') in body:
                body.remove('    ' + fix_reserved_word(method['name'][6:]) + ' = abc.abstractproperty(fset=set_' + method['name'][6:] + ')')
                body.append('    ' + fix_reserved_word(method['name'][6:]) + 
                        ' = abc.abstractproperty(fset=set_' + method['name'][6:] +
                        ', fdel=' + method['name'] + ')')
            else:
                body.append('    ' + method['name'][6:] + 
                        ' = abc.abstractproperty(fdel=' + method['name'] + ')')
        if method['name'] == 'get_id':
                body.append('    ident = abc.abstractproperty(fget=' + method['name'] + ')')
        if method['name'] == 'get_identifier_namespace':
                body.append('    namespace = abc.abstractproperty(fget=' + method['name'] + ')')

    return '\n\n'.join(body)
    
def make_method(method):
    decorator = '    @abc.abstractmethod'
    args = ['self']
    method_doc = ''
    method_impl = make_method_impl(method) 

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
                                method['sphinx_error_doc'].strip('\n') + '\n',
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

    return (decorator + '\n' + method_sig + '\n' + method_doc + '\n' +
            make_method_impl(method))
    
def make_method_impl(method):
    if method['return_type'].strip():
        return '        return # ' + method['return_type']
    else:
        return '        pass'

##
# The following functions return the app name and module name strings
# by prepending and appending the appropriate suffixes and prefixes. Note
# that the django app_name() function is included to support building of
# the abc osids into a Django project environment.
def abc_pkg_name(string):
    return abc_prefix + '_'.join(string.split('.')) + abc_suffix
    
def app_name(string):
    if abc_root_pkg:
        return abc_root_pkg
    else:
        return app_prefix + string + app_suffix

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

######### Everything under this line may be unecessary #########
"""
def interface_iterator(root, packageName):
    interfaceStr = root.get(ns + 'name').split('.')[-1]
    inheritStr = ''
    docStr = '##\n'
    methodStr = ''
    for child in root:
        if child.tag == (ns + 'implements'):
            implName = child.get(ns + 'interface').split('.')[-1]
            if implName:
                implPkg = child.get(ns + 'interface').split('.')[-2] 
                if packageName != implPkg:
                    implName = abcModuleName(implPkg) + '.' + implName
                inheritStr = append_impl_str(implName, inheritStr)
        if child.tag == (ns + 'description'):
            docStr = docStr + process_text(child)
        if child.tag == (ns + 'method'):
            methodStr = methodStr + method_iterator(child) + '\n\n'
    if inheritStr:
        inheritStr = '(' + inheritStr + ')'
    classStr = 'class ' + interfaceStr + inheritStr + ':'
    return (docStr + '\n\n' + classStr + '\n    __metaclass__ = abc.ABCMeta' +
            '\n\n' + methodStr + '\n')

##
# This function creates all the parts of an abstract osid method, including
# the doc (most of the code deals with doc), and the method signature
# with abc decorator, input arguments and either a 'return' or 'pass'
# depending on whether the method returns anything or not.
def method_iterator(root):
    from binder_helpers import fix_reserved_word
    methodName = root.get(ns + 'name')
    defStr = '    @abc.abstractmethod\n    def ' + methodName
    docStr = '    ##\n'
    paramStr = '(self'
    returnStr = '        pass'
    for child in root:
        if child.tag == (ns + 'description'):
            docStr = docStr + process_text(child, '    # ') + '\n    #\n'
        if child.tag == (ns + 'parameter'):
            param = child.get(ns + 'name')
            param = fix_reserved_word(param)
            paramStr = paramStr + ', ' + param
            docStr = append_method_param_doc_str(child, docStr)
        if child.tag == (ns + 'return'):
            docStr = append_method_return_doc_str(child, docStr)
            returnStr = '        return'
        if child.tag == (ns + 'error'):
            docStr = append_method_error_doc_str(child, docStr)
        if child.tag == (ns + 'compliance'):
            docStr = append_method_compliance_doc_str(child, docStr)
        if child.tag == (ns + 'implNotes'):
            docStr = append_method_implnotes_doc_str(child, docStr)
        
    defStr = defStr  + paramStr + '):'
    return docStr + '\n' + defStr + '\n' + returnStr

##
# This function iterates through the method tree and appends the docs
# regarding method parameters to the documentation string
def append_method_param_doc_str(root, docStr):
    from binder_helpers import wrap_and_indent
    paramStr = 'arg:    ' + root.get(ns + 'name')
    for child in root:
        if child.tag == (ns + 'interfaceType'):
            paramStr = paramStr + ' (' + child.get(ns + 'type') + '): '
        if child.tag == (ns + 'primitiveType'):
            paramStr = paramStr + ' (' + child.get(ns + 'type') + '): '
        if child.tag == (ns + 'description'):
            paramStr = paramStr + process_text(child, '', '')
    return docStr + wrap_and_indent(paramStr.strip(),
                                    '    # ',
                                    '    #         ') + '\n'

##
# This function iterates through the method tree and appends the docs
# regarding the method return type to the documentation string
def append_method_return_doc_str(root, docStr):
    from binder_helpers import wrap_and_indent
    returnStr = 'return: '
    for child in root:
        if child.tag == (ns + 'interfaceType'):
            returnStr = returnStr + '(' + child.get(ns + 'type') + ') - '
        if child.tag == (ns + 'primitiveType'):
            returnStr = returnStr + '(' + child.get(ns + 'type') + ') - '
        if child.tag == (ns + 'description'):
            returnStr = returnStr + process_text(child, '', '')
            return docStr + wrap_and_indent(returnStr.strip(),
                                            '    # ',
                                            '    #         ') + '\n'

##
# This function iterates through the method tree and appends the docs
# regarding the possible exceptions raised by this method.
def append_method_error_doc_str(root, docStr):
    from binder_helpers import wrap_and_indent
    errorStr = 'raise:  ' + root.get(ns + 'type') + ' - '
    for child in root:
        if child.tag == (ns + 'description'):
            errorStr = errorStr + process_text(child, '', '')
    return docStr + wrap_and_indent(errorStr.strip(),
                                    '    # ',
                                    '    #         ') + '\n'

##
# This function iterates through the method tree and appends the docs
# regarding the comliance required for this method.
def append_method_compliance_doc_str(root, docStr):
    from binder_helpers import wrap_and_indent
    compStr = 'compliance: ' + root.get(ns + 'type') + ' - '
    for child in root:
        if child.tag == (ns + 'description'):
            compStr = compStr + process_text(child, '', '')
    return docStr + wrap_and_indent(compStr.strip(),
                                    '    # ',
                                    '    #             ') + '\n'

##
# This function iterates through the method tree and appends the docs
# pertaining to implementation notes for this method.
def append_method_implnotes_doc_str(root, docStr):
    from binder_helpers import wrap_and_indent
    noteStr = 'implementation notes: '
    noteStr = noteStr + process_text(root, '', '')
    return docStr + wrap_and_indent(noteStr.strip(),
                                    '    # ',
                                    '    # ') + '\n'

##
# Send any text blocks to this function that includes text tags for things
# like copyright symbols, paragraphs breaks, headings, tokens and code blocks
# and outlines.  Outlines are dispatched to make_outline which isn't afraid 
# to deal with them (but it should be).
def process_text(root, iIndent = '# ', sIndent = None):
    from binder_helpers import wrap_and_indent
    from binder_helpers import reindent
    if not sIndent:
        sIndent = iIndent
    makeStr = ''
    iterStr = ' '.join(root.text.split())
    for child in root:
        if child.tag == (ns + 'copyrightSymbol'):
            iterStr = iterStr + ' (c) ' + ' '.join(child.tail.split()) + ' '
        if child.tag == (ns + 'pbreak'):
            makeStr = (makeStr + wrap_and_indent(iterStr, 
                                    iIndent, sIndent)) + '\n' + iIndent +'\n'
            iterStr = ' '.join(child.tail.split())
        if child.tag == (ns + 'heading'):
            iterStr = iterStr + ' '.join(str(child.text).split())
            iterStr = iterStr + '' + ' '.join(str(child.tail).split()) + ''
        if child.tag == (ns + 'token'):
            iterStr = iterStr + ' ' + ' '.join(str(child.text).split()) + ' '
            iterStr = iterStr + '' + ' '.join(str(child.tail).split()) + ''
        if child.tag == (ns + 'code'):
            makeStr = (makeStr + wrap_and_indent(iterStr,
                                        iIndent, sIndent)).strip() + '\n'
            iterStr = reindent(child.text.strip(), iIndent + '  ')
            makeStr = makeStr + iterStr + iIndent + '\n'
            iterStr = ' '.join(child.tail.split())
        if child.tag == (ns + 'outline'):
            makeStr = (makeStr + wrap_and_indent(iterStr, 
                                        iIndent, sIndent)).strip() + '\n'
            iterStr = make_outline(child, iIndent + '  * ',
                                         iIndent + '    ')
            makeStr = makeStr + iterStr.strip()
            iterStr = ' '.join(child.tail.split())
    return makeStr + wrap_and_indent(iterStr, iIndent, sIndent)

##
# This function is used to properly process outline tagged text, so be kind
# to it.
def make_outline(root, iIndent, sIndent = None):
    from binder_helpers import wrap_and_indent
    if not sIndent:
        sIndent = iIndent
    outlineStr = ''
    iterStr = ''
    for child in root:
        if child.tag == (ns + 'element'):
            iterStr = ' '.join(child.text.split())
            for elem in child.iter():
                if elem.tag == (ns + 'token'):
                    iterStr = iterStr + ' ' + ' '.join(str(elem.text).split()) + ' '
                    iterStr = iterStr + '' + ' '.join(str(elem.tail).split()) + ''
            iterStr = wrap_and_indent(iterStr, iIndent, sIndent)
            outlineStr = outlineStr + iterStr + '\n'
    return outlineStr

##
# This little function simply appends the class inheritance string (implStr) 
# with each of the osid classes (impl's) sent to it by the method iterator
def append_impl_str(impl, implStr):
    if implStr:
        implStr = implStr + ', ' + impl
    else:
        implStr = implStr + impl
    return implStr


##
# This function returns a string the represents the type of osid interface,
# like object, session, primitive, for creating a package sructure.  If the
# global flag pkgScheme is set to 'verbose', then this function will simply 
# return the camelToUnderscore name of the interface, resulting in every
# interface living in its own sub-package
def spiType(inheritList, interfaceStr):
    from binder_helpers import camel_to_list
    if ('OsidObject' in inheritList or 
        'OsidObjectQuery' in inheritList or 
        'OsidObjectQueryInspector' in inheritList or 
        'OsidForm' in inheritList or 
        'OsidObjectForm' in inheritList or 
        'OsidObjectSearchOrder' in inheritList or 
        'OsidSearch' in inheritList or 
        'OsidSearchResults' in inheritList or 
        'OsidReceiver' in inheritList or 
        'OsidList' in inheritList or 
        'OsidNode' in inheritList or 
        'OsidRelationship' in inheritList or
        'OsidRelationshipQuery' in inheritList or 
        'OsidRelationshipQueryInspector' in inheritList or
        'OsidRelationshipForm' in inheritList or 
        'OsidRelationshipSearchOrder' in inheritList or
        'OsidCatalog' in inheritList or 
        'OsidCatalogQuery' in inheritList or
        'OsidCatalogQueryInspector' in inheritList or 
        'OsidCatalogForm' in inheritList or
        'OsidCatalogSearchOrder' in inheritList):
        return 'objects'
    elif ('OsidSession' in inheritList or
          camel_to_list(interfaceStr)[-1] == 'Session'):
        return 'sessions'
    elif ('OsidProfile' in inheritList or 
          'OsidManager' in inheritList or 
          'OsidProxyManager' in inheritList):
        return 'managers'
    elif ('OsidPrimitive' in inheritList):
        return 'primitives'
    elif ('OsidRecord' in inheritList):
        return 'records'
    else:
        return 'other_please_move'
"""
