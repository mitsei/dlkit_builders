##
# The functions in this module can be called upon to create a full dict/list
# representation of an entire osid package.  The data is returned following 
# the patterns in this example structure:

example_package = {
'name': 'osid.package',
'version': '3.#.#',
'title': 'Title of this OSID Package',
'copyright': 'The copyright statement',
'license': 'The terms of the OSID license',
'summary': 'The (often lengthy) package level descripion',
'interfaces': [
    {
    'fullname': 'osid.thispackage.FirstInterface',
    'shortname': 'FirstInterface',
    'category': 'sessions',
    'doc': {'headline': 'The first line of the doc string, non-indented.',
            'body': '    The full description of this interface, indented once.'},
    'inherit_fullnames': ['osid.package.FirstInheritedInterface',
                           'osid.anotherpackage.SecondInheritedInterface', '...'],
    'inherit_shortnames': ['FirstInheritedInterface', 
                           'SecondInheritedInterface', '...'],
    'inherit_pgk_names': ['package', 'anotherpackage', '...'],
    'inheritance': [{'name': 'FirstInheritedInterface', 'pkg_name': 'package'},
                    {'name': 'SecondInheritedInterface', 'pkg_name': 'anotherpackage'},
                    {'name': '...', 'pkg_name': '...'}],
    'method_names': ['first_method', 'second_method', '...'],
    'methods': [
        {
        'name': 'first_method',
        'doc': {'headline': 'The first line of the doc string, non-indented.',
                'body': '        The remaining description doc, if any, indented twice.'},
        'arg_doc': '        arg:    The doc lines for args, indented twice',
        'return_doc': '        return: The doc lines for return, ditto.',
        'error_doc': '        raise:  The doc lines for errors, and so on.',
        'sphinx_param_doc': '        :param arg_name: The doc lines for parameters, Sphinx form',
        'sphinx_return_doc': '        :return: The doc lines for return, ditto.',
        'sphinx_error_doc': '        :raise:  The doc lines for errors, and so on.',
        'compliance_doc': '        compliance: whether optional or mandatory.',
        'impl_notes_doc': '        implementation notes: If available.',
        'args': [{'var_name': 'firstArg', 'arg_type': 'osid.package.OsidThing[]', 'array': True},
                   {'var_name': 'secondArg', 'arg_type': 'cardinal', 'array': False}],
        'arg_types': ['osid.package.OsidThing', 'cardinal'],
        'return_type': 'osid.package.SomeClass',
        'errors': {'OperationFailed': 'Operational', 'IllegalState': 'ConsumerContract'}
        }
        # {and so on for each method...}
        ]
    },
    # {and so on for each interface...}
    ]
}

from abcbinder_settings import XOSIDNAMESPACEURI as ns
from abcbinder_settings import XOSIDDIRECTORY as xosid_dir
from abcbinder_settings import MAINDOCINDENTSTR as indent_str
from collections import OrderedDict
import os

OSID_ERRORS = ['ALREADY_EXISTS', 'NOT_FOUND', 'PERMISSION_DENIED', 
               'CONFIGURATION_ERROR', 'OPERATION_FAILED', 
               'TRANSACTION_FAILURE', 'ILLEGAL_STATE', 'INVALID_ARGUMENT',
               'INVALID_METHOD', 'NO_ACCESS', 'NULL_ARGUMENT', 
               'UNIMPLEMENTED', 'UNSUPPORTED']

def map_xosid(file_name):
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET
    import os
#    from django.core import management
    from binder_helpers import wrap_and_indent
    tree = ET.parse(file_name)
    root = tree.getroot()

    package = OrderedDict()
    package['name'] = ''
    package['version'] = ''
    package['title'] = ''
    package['copyright'] = ''
    package['license'] = ''
    package['summary'] = ''
    package['interfaces'] = []
    
    for elem in root.iter(ns + 'osid'):
        ##
        # Get version and package name information from XML header. I
        # don't recall why I was doing these seperately.
        full_name = (elem.get(ns + 'name'))
        package['full_name'] = full_name
        if full_name == 'osid':
            package['name'] = full_name
        else:
            package['name'] = full_name[5:]
        package['version'] = (elem.get(ns + 'version'))

    for child in root:
        ##
        # Load main documentation strings
        if child.tag == (ns + 'title'):
            package['title'] = wrap_and_indent(child.text, indent_str)
        if child.tag == (ns + 'copyright'):
            package['copyright'] = process_text(child, indent_str)
        if child.tag == (ns + 'license'):
            package['license'] = process_text(child, indent_str)
        if child.tag == (ns + 'description'):
            package['summary'] = process_text(child, indent_str)
        ##
        # For each interface fire up the interface iterator which will
        # return dictionaries that get added to an interfaces list.
        if child.tag == (ns + 'interface'):
            package['interfaces'].append(interface_iterator(child))

    return package

def interface_iterator(root):
    from djmodelmaker import make_models
    from binder_helpers import camel_to_under
    from binder_helpers import caps_under_to_camel
    from binder_helpers import get_pkg_name
    
    interface = OrderedDict()    
    interface['fullname'] = root.get(ns + 'name')
    interface['shortname'] = root.get(ns + 'name').split('.')[-1]

    ##
    # Initialize the various dictionary elements so as to assure that there
    # will always be a return value, even if it is empty, since not all of 
    # these will be caught in the for loop. This also helps ensure that the
    # ordering matches the example package, not that it matters.
    interface['category'] = ''
    interface['doc'] = {'headline': '', 'body': ''}
    interface['inherit_fullnames'] = []
    interface['inherit_shortnames'] = []
    interface['inherit_pkg_names'] = []
    interface['inheritance'] = []
    interface['method_names'] = []
    interface['methods'] = []
    
    for child in root:
        if child.tag == (ns + 'implements'):
            if child.get(ns + 'interface'):
                interface['inherit_fullnames'].append(child.get(ns + 'interface'))
                interface['inherit_shortnames'].append(child.get(ns + 'interface').split('.')[-1])
                interface['inherit_pkg_names'].append(child.get(ns + 'interface').split('.')[-2])
                interface['inheritance'].append({'name': child.get(ns + 'interface').split('.')[-1], 
                                                 'pkg_name': get_pkg_name(child.get(ns + 'interface'))})
#                                                 'pkg_name': child.get(ns + 'interface').split('.')[-2]})
        if child.tag == (ns + 'description'):
            interface['doc'] = parse_docstring(process_text(child, '    '), '    ')
            # Clean trailing whitespace issues:
            body = interface['doc']['body']
            interface['doc']['body'] = '\n\n'.join(body.split('\n    \n'))
        if child.tag == (ns + 'method'):
            interface['method_names'].append(camel_to_under(child.get(ns + 'name')))
            interface['methods'].append(method_iterator(child))
    
    interface['category'] = get_interface_category(
                                 interface['inherit_shortnames'],
                                 interface['shortname'])
    return interface

def method_iterator(root):
    from binder_helpers import fix_reserved_word
    from binder_helpers import camel_to_under

    method = OrderedDict()
    method['name'] = camel_to_under(root.get(ns + 'name'))

    ##
    # Initialize the various dictionary elements so as to assure that there
    # will always be a return value, even if it is empty, since not all of 
    # these will be caught in the for loop. This also helps ensure that the
    # ordering matches the example package, not that it matters.
    method['doc'] = {'headline': '', 'body': ''}
    method['arg_doc'] = ''
    method['return_doc'] = ''
    method['error_doc'] = ''
    method['sphinx_param_doc'] = ''
    method['sphinx_return_doc'] = ''
    method['sphinx_error_doc'] = ''
    method['compliance_doc'] = ''
    method['impl_notes_doc'] = ''
    method['args'] = []
    method['arg_types'] = []
    method['return_type'] = ''
    method['errors'] = OrderedDict()

    for child in root:
        ##
        # Process main method documentation:
        if child.tag == (ns + 'description'):
            method['doc'] = parse_docstring(process_text(child, '        '),
                                                                '        ')
            body = method['doc']['body']
            method['doc']['body'] = '\n\n'.join(body.split('\n        \n'))
        ##
        # Process parameter info into args dictionary and doc:
        if child.tag == (ns + 'parameter'):
            param = fix_reserved_word(camel_to_under(child.get(ns + 'name')))
            array = False
            for grand_child in child:
                if grand_child.tag == (ns + 'interfaceType'):
                    param_type = grand_child.get(ns + 'type')
                    if grand_child.get(ns + 'array') == 'true':
                        array = True
                if grand_child.tag == (ns + 'primitiveType'):
                    param_type = grand_child.get(ns + 'type')
                    if grand_child.get(ns + 'array') == 'true':
                        array = True
            if array == True:
                param_type = param_type + '[]'
            method['args'].append({'var_name': param, 
                                   'arg_type': param_type,
                                   'array': array})
            method['arg_types'].append(param_type)
            method['arg_doc'] = method['arg_doc'] + make_param_doc(child)
            method['sphinx_param_doc'] = method['sphinx_param_doc'] + make_sphinx_param_doc(child)
        ##
        # Process return info into return type and doc:
        if child.tag == (ns + 'return'):
            for grand_child in child:
                if grand_child.tag == (ns + 'interfaceType'):
                    return_type = grand_child.get(ns + 'type')
                if grand_child.tag == (ns + 'primitiveType'):
                    return_type = grand_child.get(ns + 'type')           
            method['return_type'] = return_type
            method['return_doc'] = make_return_doc(child)
            method['sphinx_return_doc'] = make_sphinx_return_doc(child)
        ##
        # Process error info into error doc. Note that at this time I
        # am not parsing the exceptions.  I have not found a need to do 
        # this as of yet.
        if child.tag == (ns + 'error'):
            method['errors'][child.get(ns + 'type')] = child.get(ns + 'category')
            if method['error_doc']:
                method['error_doc'] = method['error_doc'] + '\n'
            if method['sphinx_error_doc']:
                method['sphinx_error_doc'] = method['sphinx_error_doc'] + '\n'
            method['error_doc'] = method['error_doc'] + make_error_doc(child)
            method['sphinx_error_doc'] = method['sphinx_error_doc'] + make_sphinx_error_doc(child)
        ##
        # Process compliance info into compliance doc.
        if child.tag == (ns + 'compliance'):
            method['compliance_doc'] = make_compliance_doc(child)
        ##
        # Process implementation notes into impl notes doc.
        if child.tag == (ns + 'implNotes'):
            method['impl_notes_doc'] = make_implnotes_doc(child)

    return method

##
# Iterate through the method tree and return the documentation strings
# regarding method parameters.
def make_param_doc(root):
    from binder_helpers import wrap_and_indent, camel_to_under
    paramStr = 'arg:    ' + camel_to_under(root.get(ns + 'name'))
    for child in root:
        if child.tag == (ns + 'interfaceType'):
            paramStr = paramStr + ' (' + child.get(ns + 'type')
            if child.get(ns + 'array') == 'true':
                paramStr = paramStr + '[]): '
            else:
                paramStr = paramStr + '): '
        if child.tag == (ns + 'primitiveType'):
            paramStr = paramStr + ' (' + child.get(ns + 'type')
            if child.get(ns + 'array') == 'true':
                paramStr = paramStr + '[]): '
            else:
                paramStr = paramStr + '): '
        if child.tag == (ns + 'description'):
            paramStr = paramStr + process_text(child, '', '')
    return wrap_and_indent(paramStr.strip(),
                           '        ',
                           '                ') + '\n'

##
# Iterate through the method tree and return the Sphinx-style documentation 
# strings regarding method parameters.
def make_sphinx_param_doc(root):
    from binder_helpers import wrap_and_indent, camel_to_under
    paramStr = ':param ' + camel_to_under(root.get(ns + 'name')) + ': '
    typeStr = ':type ' + camel_to_under(root.get(ns + 'name')) + ': '
    for child in root:
        if child.tag == (ns + 'interfaceType'):
            typeStr = typeStr + '``' + child.get(ns + 'type')
            if child.get(ns + 'array') == 'true':
                typeStr = typeStr + '[]``'
            else:
                typeStr = typeStr + '``'
        if child.tag == (ns + 'primitiveType'):
            typeStr = typeStr + '``' + child.get(ns + 'type')
            if child.get(ns + 'array') == 'true':
                typeStr = typeStr + '[]``'
            else:
                typeStr = typeStr + '``'
        if child.tag == (ns + 'description'):
            paramStr = paramStr + process_text(child, '', '', width = 200)
    return '        ' + paramStr.strip() + '\n        ' + typeStr.strip() + '\n'


##
# Iterate through the method tree and return the documentation strings
# regarding the method return type.
def make_return_doc(root):
    from binder_helpers import wrap_and_indent
    returnStr = 'return: '
    for child in root:
        if child.tag == (ns + 'interfaceType'):
            returnStr = returnStr + '(' + child.get(ns + 'type') + ') - '
        if child.tag == (ns + 'primitiveType'):
            returnStr = returnStr + '(' + child.get(ns + 'type') + ') - '
        if child.tag == (ns + 'description'):
            returnStr = returnStr + process_text(child, '', '')
            return wrap_and_indent(returnStr.strip(),
                                   '        ',
                                   '                ')

##
# Iterate through the method tree and return the Sphinx-style documentation 
# strings regarding the method return type.
def make_sphinx_return_doc(root):
    returnStr = ':return: '
    returnTypeStr = ':rtype: '
    for child in root:
        if child.tag == (ns + 'interfaceType'):
            returnTypeStr = returnTypeStr + '``' + child.get(ns + 'type') + '``'
        if child.tag == (ns + 'primitiveType'):
            returnTypeStr = returnTypeStr + '``' + child.get(ns + 'type') + '``'
        if child.tag == (ns + 'description'):
            returnStr = returnStr + process_text(child, '', '', width = 200)
    return ('        ' + returnStr.strip() + '\n        ' + returnTypeStr.strip())

##
# Iterate through the method tree and return the documentation strings
# regarding the possible exceptions raised by this method.
def make_error_doc(root):
    from binder_helpers import wrap_and_indent, caps_under_to_camel
    errorStr = 'raise:  ' + caps_under_to_camel(root.get(ns + 'type')) + ' - '
    for child in root:
        if child.tag == (ns + 'description'):
            errorStr = errorStr + process_text(child, '', '')
    return wrap_and_indent(errorStr.strip(),
                           '        ',
                           '                ')

##
# Iterate through the method tree and return the Sphinx_style documentation 
# strings regarding the possible exceptions raised by this method.
def make_sphinx_error_doc(root):
    from binder_helpers import caps_under_to_camel
    errorStr = ':raise: ``' + caps_under_to_camel(root.get(ns + 'type')) + '`` -- '
    for child in root:
        if child.tag == (ns + 'description'):
            errorStr = errorStr + process_text(child, '', '', width = 200)
    return '        ' + errorStr.strip()

##
# Iterate through the method tree and return the documentation strings
# regarding the compliance required for this method.
def make_compliance_doc(root):
    from binder_helpers import wrap_and_indent
    compStr = '*compliance: ' + root.get(ns + 'type') + ' -- '
    for child in root:
        if child.tag == (ns + 'description'):
            compStr = compStr + process_text(child, '', '', width = 200) + '*'
    return wrap_and_indent(compStr.strip(),
                           '        ',
                           '        ', width = 72) + '\n'

##
# Iterate through the method tree and return the documentation string
# pertaining to implementation notes for this method.
def make_implnotes_doc(root):
    from binder_helpers import wrap_and_indent
    noteStr = '*implementation notes*: '
    noteStr = noteStr + process_text(root, '', '')
    return wrap_and_indent(noteStr.strip(),
                           '        ',
                           '        ') + '\n'

##
# Send any text blocks to this function that includes text tags for things
# like copyright symbols, paragraphs breaks, headings, tokens and code blocks
# and outlines.  Outlines are dispatched to make_outline which isn't afraid 
# to deal with them (but it should be).
def process_text(root, iIndent = '', 
                       sIndent = None, makeDocStringHead = False,
                                       makeDocStringTail = False,
                                       width = 72):
    from binder_helpers import wrap_and_indent
    from binder_helpers import reindent
    from binder_helpers import camel_to_under, caps_under_to_camel, is_mixed_case
    
    if not sIndent:
        sIndent = iIndent
    makeStr = ''
    iterStr = ' '.join(root.text.split())
    for child in root:
        if child.tag == (ns + 'copyrightSymbol'):
            iterStr = iterStr + ' (c) ' + ' '.join(child.tail.split()) + ' '
        if child.tag == (ns + 'pbreak'):
            makeStr = (makeStr + wrap_and_indent(iterStr, 
                                    iIndent, sIndent, width)) + '\n' + iIndent +'\n'
            iterStr = ' '.join(child.tail.split())
        if child.tag == (ns + 'heading'):
            iterStr = iterStr + ' '.join(str(child.text).split())
            iterStr = iterStr + '' + ' '.join(str(child.tail).split()) + ''
        if child.tag == (ns + 'token'):
            if is_mixed_case(str(child.text).strip()):
                if len(str(child.text).split('.')) > 1:
                    segments = str(child.text).split('.')
                    segments[-1] = camel_to_under(segments[-1])
                    convertedText = '.'.join(segments)
                elif str(child.text).strip().split(' ')[0] != 'a':
                    convertedText = camel_to_under(child.text.strip())
                else:
                    convertedText = child.text
            elif str(child.text).strip('. ') in OSID_ERRORS:
                convertedText = caps_under_to_camel(child.text)
            else:
                convertedText = child.text
            if convertedText is None or convertedText.strip() == '':
                pass
            elif convertedText.strip().endswith('.'):
                convertedText = convertedText.split('.')[0]
                iterStr = iterStr + ' ``' + ' '.join(str(convertedText).split()) + '``. '
            else:
                iterStr = iterStr + ' ``' + ' '.join(str(convertedText).split()) + '`` '
            iterStr = iterStr + '' + ' '.join(str(child.tail).split()) + ''
        if child.tag == (ns + 'code'):
            makeStr = (makeStr + wrap_and_indent(iterStr,
                                        iIndent, sIndent, width)).strip() + '\n'
            iterStr = reindent(child.text.strip(), iIndent + '  ')
            makeStr = makeStr + iterStr + iIndent + '\n'
            iterStr = ' '.join(child.tail.split())
        if child.tag == (ns + 'outline'):
            makeStr = (makeStr + wrap_and_indent(iterStr, 
                                        iIndent, sIndent, width)).strip() + '\n'
            iterStr = iIndent + '\n' + make_outline(child, iIndent + '  * ',
                                         iIndent + '    ', width)
            makeStr = makeStr + iterStr
            iterStr = ' '.join(child.tail.split())
            
    returnStr = makeStr + wrap_and_indent(iterStr, iIndent, sIndent, width)
    if makeDocStringHead:
        returnDoc = parse_docstring(returnStr, iIndent, sIndent,
                                    makeTail = makeDocStringTail)
        return returnDoc['headstring'] + '\n\n' + returnDoc['body']
    else:
        return returnStr

##
# Accepts a pre-formatted documentation block and splits out the first
# sentence from the remainder of the block.  All formatting in the
# remaining block should be retained.  If make_head or make_tail are True
# then parse_docstring will add the triple quotes in the right places.
# Otherwise its up to the calling code to insert these.  If make_head is
# False the returned headline will not be indented.  This too is left up
# to the calling code.  parse_doc assumes that the incoming text block
# does not begin with a special format section, like a code or outline, etc.
def parse_docstring(text, iIndent, sIndent = False, 
                         make_head = False, make_tail = False):
    from binder_helpers import wrap_and_indent

    if not sIndent:
        sIndent = iIndent
    tail_str = ''
    head_str = ''
    if text:
        first_paragraph = text.split('\n' + iIndent + '\n')[0]
        subsequent_paragraphs = ''
        if len(text.split('\n' + iIndent + '\n', 1)) > 1:
            subsequent_paragraphs = text.split('\n' + iIndent + '\n', 1)[1]
        if make_head:
            head_str = iIndent + '\"\"\"'
        headline_str = (head_str + 
                                (first_paragraph.split('.')[0]).strip() + '.')
        headline_str = ' '.join(headline_str.split('\n' + iIndent))
        if (len(first_paragraph.split('.', 1)) > 1 and 
               first_paragraph.split('.', 1)[1].strip() != ''):
            remaining_text = first_paragraph.split('.', 1)[1].strip()
            next_paragraph = remaining_text.split('\n' + iIndent + '\n', 1)[0]
            next_paragraph = ' '.join(next_paragraph.split())
            next_paragraph = wrap_and_indent(next_paragraph, iIndent, sIndent)
            if len(remaining_text.split('\n' + iIndent + '\n', 1)) > 1:
                remaining_text = next_paragraph + '\n' + remaining_text.split('\n' + iIndent + '\n', 1)[1]
            else:
                remaining_text = next_paragraph
            if subsequent_paragraphs.strip() != '':
                if make_tail:
                    tail_str = '\n\n' + iIndent + '\"\"\"'
                return {'headline': headline_str, 
                        'body': remaining_text + '\n\n' +
                        subsequent_paragraphs + tail_str}
            else:
                if make_tail:
                    tail_str = iIndent + '\"\"\"'
                return {'headline': headline_str,
                        'body': remaining_text + tail_str}
        else:
            if make_tail:
                tail_str = '\"\"\"'
            return {'headline': headline_str, 
                    'body': tail_str}
    else:
        return {'headline': '',
                'body': ''}

##
# This function is used to properly process outline tagged text
def make_outline(root, iIndent, sIndent = None, width = 72):
    from binder_helpers import wrap_and_indent
    if not sIndent:
        sIndent = iIndent
    outline = ''
    iterStr = ''
    for child in root:
        if child.tag == (ns + 'element'):
            iterStr = ' '.join(child.text.split())
            for elem in child.iter():
                if elem.tag == (ns + 'token'):
                    iterStr = iterStr + ' ``' + ' '.join(str(elem.text).split()) + '`` '
                    iterStr = iterStr + '' + ' '.join(str(elem.tail).split()) + ''
            iterStr = wrap_and_indent(iterStr, iIndent, sIndent)
            outline = outline + iterStr + '\n'
    return outline

##
# get_interface_category returns a string representing the type of the osid 
# interface, such as object, session, primitive, for creating a package 
# sructure. It expects a list of all inherited interfaces as well as the
# short name of the interface in question as a CapWords case class name.
def get_interface_category(inherit_list, interface_short_name):
    from binder_helpers import camel_to_list
    import interface_sets
    if (not interface_sets.PROPERTIES.isdisjoint(inherit_list) or
        interface_short_name in interface_sets.PROPERTIES):
        return 'properties'
    if (not interface_sets.OBJECTS.isdisjoint(inherit_list) or
        interface_short_name in interface_sets.OBJECTS):
        return 'objects'
    elif (not interface_sets.QUERIES.isdisjoint(inherit_list) or
          interface_short_name in interface_sets.QUERIES):
        return 'queries'
    elif (not interface_sets.QUERY_INSPECTORS.isdisjoint(inherit_list) or
          interface_short_name in interface_sets.QUERY_INSPECTORS):
        return 'query_inspectors'
    elif (not interface_sets.SEARCHES.isdisjoint(inherit_list) or
            interface_short_name in interface_sets.SEARCHES):
        return 'searches'
    elif (not interface_sets.SEARCH_ORDERS.isdisjoint(inherit_list) or
          interface_short_name in interface_sets.SEARCH_ORDERS):
        return 'search_orders'
    elif (not interface_sets.RULES.isdisjoint(inherit_list) or
          interface_short_name in interface_sets.RULES):
        return 'rules'
    elif (not interface_sets.METADATA.isdisjoint(inherit_list) or
          interface_short_name in interface_sets.METADATA):
        return 'metadata'
    elif (not interface_sets.RECEIVERS.isdisjoint(inherit_list) or
          interface_short_name in interface_sets.RECEIVERS):
        return 'receivers'
    elif (not interface_sets.SESSIONS.isdisjoint(inherit_list) or
          camel_to_list(interface_short_name)[-1] == 'Session'):
        return 'sessions'
    elif (not interface_sets.MANAGERS.isdisjoint(inherit_list) or
          interface_short_name in interface_sets.MANAGERS):
        return 'managers'
    elif (not interface_sets.RECORDS.isdisjoint(inherit_list) or
          interface_short_name in interface_sets.RECORDS):
        return 'records'
    elif ('OsidPrimitive' in inherit_list or
          interface_short_name in interface_sets.PRIMITIVES or
          camel_to_list(interface_short_name)[-1] in interface_sets.PRIMITIVES):
        return 'primitives'
    elif (interface_short_name in interface_sets.MARKERS):
        return 'markers'
    else:
        return 'others_please_move'

