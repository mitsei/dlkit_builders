import os
import re

from abcbinder_settings import XOSIDNAMESPACEURI as ns
from abcbinder_settings import INTERFACMAPSDIRECTORY as interface_maps_dir
from abcbinder_settings import PKGMAPSDIRECTORY as pkg_maps_dir
from mongobuilder_settings import PATTERN_DIR as pattern_maps_dir
import json
import keyword
import textwrap

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
ABS_PATH = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir))
##
# This function takes an element tree method root and finds the 'return' tag
# and returns the type.
# def get_return_type(root):
#     returnType = ''
#     for child in root:
#         if child.tag == (ns + 'return'):
#             for grandChild in child:
#                 if grandChild.tag == (ns + 'interfaceType'):
#                     returnType = grandChild.get(ns + 'type')
#                 if grandChild.tag == (ns + 'primitiveType'):
#                     returnType = grandChild.get(ns + 'type')
#     return returnType

# def get_param_list(root):
#     """
#     Gets parameters from method roots.
#
#     This function takes an element tree method root and iterates through any
#     parameter names that are defined, beginning with the ubiquitous 'self', and
#     returns a list.  It may want to be extended in the future to return a list
#     of dicts that also include the osid type of the parameter, but so far that
#     has not been necessary.  In fact so far I haven't even used this.
#
#     """
#     paramList = ['self']
#     for child in root:
#         if child.tag == (ns + 'parameter'):
#             param = child.get(ns + 'name')
#             param = fix_reserved_word(param)
#             paramList.append(param)
#     return paramList

def reindent(text, iIndent):
    """ Reindents a block of text to the new without re-wrapping"""
    text = text.split('\n')
    retStr = ''
    for line in text:
        retStr = retStr + iIndent + line + '\n'
    return retStr

def wrap_and_indent(text, iIndent = '', sIndent = None, width = 72):
    """
    Wraps and indents with initial, subsequent strings and max width.
    
    Wraps and indents a block of text given initial and subsequent indent
    strings and a max width.  Will also strip any leading or trailing spaces
    and lines (I believe, need to check this)
    
    """
    if not sIndent:
        sIndent = iIndent
    wrapper = textwrap.TextWrapper()
    wrapper.width = width
    wrapper.initial_indent = iIndent
    wrapper.subsequent_indent = sIndent
    wrapper.drop_whitespace = True
    return wrapper.fill(textwrap.dedent(text.strip()))

def fix_reserved_word(word, is_module=False):
    """
    Replaces words that may be problematic
    
    In particular the term 'type' is used in the osid spec, primarily as an argument
    parameter where a type is provided to a method.  'type' is a reserved word
    in python, so we give ours a trailing underscore. If we come across any other 
    osid things that are reserved word they can be dealt with here.
    
    """
    if is_module:
        if word == 'logging':
            word = 'logging_' # Still deciding this
    else:
        if keyword.iskeyword(word):
            word += '_'
        elif word in ['id', 'type', 'str', 'max', 'input', 'license', 'copyright', 'credits', 'help']:
            word += '_'
    return word

##
# Takes a CamelCase string (standard OSID method name case) and returns a list.
# Useful for parsing out words when inspecting methods for bindings, etc. It 
# will also work for mixedCase strings.
def camel_to_list(string):
    string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).split('_')

def camel_to_mixed(string):
    """ CamelCase to mixedCase. """
    words = camel_to_list(string)
    words[0] = words[0].lower()
    return ''.join(words)

def under_to_mixed(string):
    """ underscore_delimited to mixedCase. """
    words = string.title().split('_')
    words[0] = words[0].lower()
    return ''.join(words)

def under_to_caps(string):
    """ underscore_delimited to CapsCase. """
    words = string.title().split('_')
    return ''.join(words)

##
# Takes a CAPS_UNDER style string (standard OSID exception case) and return
# a CamelCase version, for converting to Python exception convention
def caps_under_to_camel(string):
    return ''.join(string.title().split('_'))

def is_mixed_case(s):
    return s != s.lower() and s != s.upper() and not s[0].isupper()

##
# These two functions deal with plurals.  At times in the osid spec you will
# find method names like 'hasThing' where the underlying model is really 
# storing a bunch of things, and a 'getThings' call is available for that. 
# These methods come in handy when inspecting for these kinds of patterns.
# feel free to update the following singular to plural list as exceptions 
# to the "just add an 's' rule" are found.

_singular_to_plural = {
    'Millenium': 'Millenia',
    'millenium': 'millenium',
    'Century': 'Centuries',
    'century': 'centuries',
    'Child': 'Children',
    'child': 'children',
    'Proficiency': 'Proficiencies',
    'proficiency': 'proficiencies',
    'Entry': 'Entries',
    'entry': 'entries',
    'Activity': 'Activities',
    'activity': 'activities',
    'Ontology': 'Ontologies',
    'ontology': 'ontologies',
    'Repository': 'Repositories',
    'repository': 'repositories',
    'Agency': 'Agencies',
    'agency': 'agencies',
    'type_': 'types',
    'id_': 'ids',
    'family': 'families',
    'Family': 'Families',
    'assessment_offered': 'assessments_offered',
    'AssessmentOffered': 'AssessmentsOffered',
    'assessment_taken': 'assessments_taken',
    'AssessmentTaken': 'AssessmentsTaken',
    'Hierarchy': 'Hierarchies',
    'hierarchy': 'hierarchies',
    'Query': 'Queries',
    'query': 'queries',
    'GradeEntry': 'GradeEntries',
    'grade_entry': 'grade_entries',
    'log_entry': 'log_entries',
    'LogEntry': 'LogEntries'
}

_plural_to_singular = {v: k for k, v in _singular_to_plural.items()}

def make_plural(string):
    if string in _singular_to_plural:
        return _singular_to_plural[string]
    else:
        return string + 's'

def remove_plural(string):
    if string in _plural_to_singular:
        return _plural_to_singular[string]
    else:
        return string[:-1]

##
# This little function is used to convert each osid method name
# from camelCase to underscore_case to make the binding and impls
# a little more Pythonic.
def camel_to_under(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def camel_to_verbose(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1).lower()

def camel_to_caps_under(name):
    return camel_to_under(name).upper()

##
# This function returns the category, or 'module' for the interface in question
# By default it does not raise an exception, but can be called with report-
# error equals True so that you can track un-categorized interfaces.
def get_interface_module(pkg_name, interface_shortname, report_error = False):
    category = 'UNKNOWN_MODULE'
    try:
        read_file = open(interface_maps_dir + '/' + pkg_name + '.json' , 'r')
        index = json.load(read_file)
        read_file.close()
    except IOError:
        if report_error:
            print ('INTERFACE LOOKUP ERROR - interface map for \'' + pkg_name + 
                   '.' + interface_shortname + '\' not found.')
    else:
        try:
            category = index[pkg_name + '.' + interface_shortname]
        except KeyError:
            if report_error:
                print ('INTERFACE LOOKUP ERROR - category for \'' + pkg_name + '.'
                       + interface_shortname + '\' not found.')
    return category


##
# This function simply returns the package string, parsing and input
# interface full name.
#def get_pkg_name(interface):
#    interface_components = interface.split('.')
#    if len(interface_components) == 1:
#        return ''
#    elif len(interface_components) == 2:
#        return interface_components[0]
#    else:
#        return interface_components[1]

##
# This function simply returns the package string, parsing and input
# interface full name.
def get_pkg_name(interface):
    interface_components = interface.split('.')
    if len(interface_components) == 1:
        return ''
    elif len(interface_components) == 2:
        return interface_components[0]
    elif len(interface_components) == 3:
        return interface_components[1]
    else:
        return '.'.join(interface_components[1:-1])

##
# Return the associated class name for a ProxyManager given a Manager name
def proxy_manager_name(string):
    return string.split('Manager')[0] + 'ProxyManager'
#
# ## THIS FUNCTION WAS PROBABLY A WASTE OF TIME.  REMOVE SOMEDAY???
# # This function returns the appropriate import string given a package and
# # module of a class being built and the interface name.
# def make_import_string(source_pkg, source_module, interface):
#     interface_components = interface.split('.')
#     if len(interface_components) == 1:
#         return ''
#     elif len(interface_components) == 2:
#         interface_pkg = interface_components[0]
#         interface_module = get_interface_module(
#                            interface_components[0],
#                            interface_components[-1])
#     else:
#         interface_pkg = interface_components[1]
#         interface_module = get_interface_module(
#                            interface_components[1],
#                            interface_components[-1])
#     interface_name = interface_components[-1]
#     if (interface_pkg == source_pkg and
#         interface_module == source_module):
#         return ''
#     elif interface_module == 'UNKNOWN_MODULE':
#         return ('# IMPORT STRING ERROR: Unknown module for ' +
#                 interface)
#     else:
#         return ('from ${app_root}' + interface_pkg + '.' +
#                                      interface_module +
#                 ' import ' + interface_name)

# This function returns the category, or 'module' for the interface in question
# By default it does not raise an exception, but can be called with report-
# error equals True so that you can track un-categorized interfaces.

##
# The SkipMethod exception is used for implementation builders like the
# Kit builder where methods must occasionally be skipped for whatever reason.
class SkipMethod(Exception):
    pass

def make_twargs(index, package, interface, method, rtype=True, object_name=None, containable_object_name=None, arg_count=0):
    twargs = dict()
    twargs['interface_name'] = interface['shortname']
    twargs['package_name'] = package['name']
    twargs['module_name'] = interface['category']
    twargs['method_name'] = method['name']
    twargs['cat_name'] = index['package_catalog_caps']
    if object_name is not None:
        twargs['object_name'] = object_name
    if containable_object_name is not None:
        twargs['containable_object_name'] = containable_object_name
    if rtype:
        twargs['return_type_full'] = method['return_type']
    n = 0
    while n < arg_count:
        twargs['arg' + str(n) +'_name'] = method['args'][n]['var_name']
        twargs['arg' + str(n) +'_type_full'] = method['args'][n]['arg_type']
        n += 1
    return twargs

def get_cat_name_for_pkg(pkg):
    try:
        read_file = open(ABS_PATH + '/builders/package_maps/' + pkg + '.json', 'r')
        package = json.load(read_file)
        read_file.close()
    except IOError:
        print 'No package map found for package \'' + pkg + '\''
        return 'NoCatalog'
    for interface in package['interfaces']:
        if (interface['category'] == 'objects' and
            'OsidCatalog' in interface['inherit_shortnames']):
            return interface['shortname']
    return 'NoCatalog'

def get_cat_name_for_pkg_from_pattern(pkg):
    try:
        read_file = open(pattern_maps_dir + '/' + pkg + '.json', 'r')
        pattern = json.load(read_file)
        read_file.close()
    except IOError:
        #print 'No pattern map found for package \'' + pkg + '\''
        return 'NoCatalog'
    if 'package_catalog_caps' in pattern:
        #print pattern['package_catalog_caps']
        return pattern['package_catalog_caps']
    return 'NoCatalog'

def flagged_for_implementation(interface,
        sessions_to_implement, objects_to_implement, variants_to_implement):
    """
    Check if this interface is meant to be implemented.
    
    """
    #print "    Checking:", interface['shortname']
    test = False
    if interface['category'] == 'managers':
        test = True
    elif (interface['category'] == 'sessions' and 
            interface['shortname'] in sessions_to_implement):
        #print "        Implement session:", interface['shortname']
        test = True
    elif interface['shortname'] in objects_to_implement:
        #print "        Implement", interface['category'] + ":", interface['shortname']
        test = True
    else:
        for variant in variants_to_implement:
            if (interface['shortname'].endswith(variant) and
                    interface['shortname'][:-len(variant)] in objects_to_implement):
                #print "        Implement", interface['category'] + ":", interface['shortname']
                test = True
    return test

def fix_bad_name(name, optional_match_term=None):
    """
    Occasionally there are bad names of things in the osid spec.
    
    Here these can be overriden until they are fixed in the spec.
    
    """
    bad_names_map = {
        'set_base_on_grades': 'set_based_on_grades',
        'clear_lowest_score': 'clear_lowest_numeric_score',
        'clear_input_start_score_range': 'clear_input_score_start_range',
        'osid.repository.CompositionSearchSession': 'osid.repository.CompositionQuerySession',
        'osid.repository.CompositionQuerySession': 'osid.repository.CompositionQuerySession',
    }

    if optional_match_term == 'get_composition_query_session':
        name = bad_names_map[name]
    elif optional_match_term in ['get_composition_search_session',
                                 'get_composition_search_session_for_repository']:
        name = 'osid.repository.CompositionSearchSession'
    else:
        if name in bad_names_map:
            name = bad_names_map[name]
    return name

def add_missing_args(method, interface_name):
    if (interface_name.endswith('Receiver') and
            method['name'].split('_')[0] in ['new', 'changed', 'deleted'] and
            len(method['args']) == 1):
        method['args'] = ([{"arg_type": "osid.id.Id", 
                            "var_name": "notification_id", 
                            "array": False}] + method['args'])
        method['arg_types'] = ['osid.id.Id'] + method['arg_types']
        method['arg_doc'] = '        arg:    notification_id (osid.id.Id): the notification ``Id``\n' + method['arg_doc']
        method['sphinx_param_doc'] = '        :param notification_id: the notification ``Id``\n        :type notification_id: ``osid.id.Id``\n' + method['sphinx_param_doc']
    return method

def add_missing_methods(interface):
    if (interface['shortname'].endswith('NotificationSession') and
            'acknowledge_' + camel_to_under(interface['shortname'][:len('Session')]) not in interface['method_names']):
        object_name_under = camel_to_under(interface['shortname'][:-len('NotificationSession')])
        interface['methods'] = (interface['methods'] + [{
               'name': 'reliable_' + object_name_under + '_notifications', 
               'doc': {
                  'headline': 'Reliable notifications are desired.', 
                  'body': '        In reliable mode, notifications are to be acknowledged using\n        ``acknowledge_item_notification()`` .'
               }, 
               'arg_doc': '', 
               'return_doc': '', 
               'error_doc': '', 
               'sphinx_param_doc': '', 
               'sphinx_return_doc': '', 
               'sphinx_error_doc': '', 
               'compliance_doc': '        *compliance: mandatory -- This method is must be implemented.*\n', 
               'impl_notes_doc': '', 
               'args': [], 
               'arg_types': [], 
               'return_type': '', 
               'errors': {}
            }, 
            {
               'name': 'unreliable_' + object_name_under + '_notifications', 
               'doc': {
                  'headline': 'Unreliable notifications are desired.', 
                  'body': '        In unreliable mode, notifications do not need to be\n        acknowledged.'
               }, 
               'arg_doc': '', 
               'return_doc': '', 
               'error_doc': '', 
               'sphinx_param_doc': '', 
               'sphinx_return_doc': '', 
               'sphinx_error_doc': '', 
               'compliance_doc': '        *compliance: mandatory -- This method is must be implemented.*\n', 
               'impl_notes_doc': '', 
               'args': [], 
               'arg_types': [], 
               'return_type': '', 
               'errors': {}
            }, 
            {
               'name': 'acknowledge_' + object_name_under + '_notification', 
               'doc': {
                  'headline': 'Acknowledge an ' + object_name_under + ' notification.', 
                  'body': ''
               }, 
               'arg_doc': '        arg:    notification_id (osid.id.Id): the ``Id`` of the\n                notification\n', 
               'return_doc': '', 
               'error_doc': '        raise:  OperationFailed - unable to complete request\n        raise:  PermissionDenied - authorization failure', 
               'sphinx_param_doc': '        :param notification_id: the ``Id`` of the notification\n        :type notification_id: ``osid.id.Id``\n', 
               'sphinx_return_doc': '', 
               'sphinx_error_doc': '        :raise: ``OperationFailed`` -- unable to complete request\n        :raise: ``PermissionDenied`` -- authorization failure', 
               'compliance_doc': '        *compliance: mandatory -- This method must be implemented.*\n', 
               'impl_notes_doc': '', 
               'args': [
                  {
                     'arg_type': 'osid.id.Id', 
                     'var_name': 'notification_id', 
                     'array': False
                  }
               ], 
               'arg_types': [
                  'osid.id.Id'
               ], 
               'return_type': '', 
               'errors': {
                  'OPERATION_FAILED': 'Operational', 
                  'PERMISSION_DENIED': 'User'
               }
            }] 
        )
    elif interface['shortname'] == 'LoggingProfile':
        interface['method_names'].append('supports_log_entry_admin')
        interface['methods'].append({
           "name": "supports_log_entry_admin",
           "doc": {
              "headline": "Tests if log entry admin is supported.",
              "body": ""
           },
           "arg_doc": "",
           "return_doc": "        return: (boolean) - ``true`` if log entry admin is supported,\n                ``false`` otherwise",
           "error_doc": "",
           "sphinx_param_doc": "",
           "sphinx_return_doc": "        :return: ``true`` if log entry admin is supported, ``false`` otherwise\n        :rtype: ``boolean``",
           "sphinx_error_doc": "",
           "compliance_doc": "        *compliance: mandatory -- This method must be implemented.*\n",
           "impl_notes_doc": "",
           "args": [],
           "arg_types": [],
           "return_type": "boolean",
           "errors": {}
        })
