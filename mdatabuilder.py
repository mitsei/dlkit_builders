
import time
import os
import json
import string
from .binder_helpers import *
from .config import *
from abcbinder_settings import PKGMAPSDIRECTORY as pkg_maps_dir
from abcbinder_settings import MAINDOCINDENTSTR as main_doc_indent
from abcbinder_settings import ENCODING as utf_code
from mongobuilder_settings import APPNAMEPREFIX as app_prefix
from mongobuilder_settings import APPNAMESUFFIX as app_suffix
from mongobuilder_settings import PACKAGEPREFIX as pkg_prefix
from mongobuilder_settings import PACKAGESUFFIX as pkg_suffix
from mongobuilder_settings import ROOTPACKAGE as root_pkg
from mongobuilder_settings import ROOTPATH as root_path

##
# This is the entry point for making django-based python models for
# the osids. It processes all of the osid maps in the package maps
# directory.
def make_mdata():
    for json_file in os.listdir(pkg_maps_dir):
        if json_file.endswith('.json'):
            make_mdatum(pkg_maps_dir + '/' + json_file)

##
# This function expects a file containing a json representation of an
# osid package that was prepared by the mapper.
def make_mdatum(file_name):
    from binder_helpers import get_interface_module

    ##
    # Get the package map for this osid package
    read_file = open(file_name, 'r')
    package = json.load(read_file)
    read_file.close()

    if package['name'] not in managers_to_implement:
        return
    
    ##
    # Get the pattern map for this osid package.
    read_file = open('builders/pattern_maps/' + 
                      package['name'] + '.json', 'r')
    patterns = json.load(read_file)
    read_file.close()

    mdata = ''
    import_str = '\"\"\"Mongo osid metadata configurations for ' + package['name'] + ' service.\"\"\"\n\n'
    import_str = import_str + """
from .. import types
from ..primitives import Type
DEFAULT_LANGUAGE_TYPE = Type(**types.Language().get_type_data('DEFAULT'))
DEFAULT_SCRIPT_TYPE = Type(**types.Script().get_type_data('DEFAULT'))
DEFAULT_FORMAT_TYPE = Type(**types.Format().get_type_data('DEFAULT'))
DEFAULT_GENUS_TYPE = Type(**types.Genus().get_type_data('DEFAULT'))"""




    if not root_pkg:
        ##
        # Check if an app directory and dj osid subdirectory already exist.  
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
    # The real work starts here.  Iterate through all interfaces to build 
    # all the model classes for this osid package.
    for interface in package['interfaces']:

        ##
        # Check to see if this interface is meant to be implemented.
        if package['name'] != 'osid':
            if flagged_for_implementation(interface, 
                    sessions_to_implement, objects_to_implement, variants_to_implement):
                pass
            else:
                continue

        if (interface['shortname'] in patterns['package_objects_caps'] or
            interface['shortname'] in patterns['package_relationships_caps'] or
            interface['shortname'] == 'OsidObject' or
            interface['category'] == 'markers' or
            interface['shortname'] == patterns['package_catalog_caps']):
            inheritance = []
            imports = []

            impl_class = load_impl_class(package['name'], interface['shortname'])

            """
            ##
            # Check to see if there are any additinal inheritances required
            # by the implementation patterns.
            impl_class = load_impl_class(package['name'], interface['shortname'])
            if hasattr(impl_class, 'inheritance'):
                inheritance = inheritance + getattr(impl_class, 'inheritance')
            ##
            # Interate through any inherited interfaces and build the inheritance
            # list for this interface. Also, check if an import statement is
            # required and append to the appropriate module's import list.
            for i in interface['inheritance']:
                if i['pkg_name'] == package['name']:
                    inheritance.append(i['name'])
                else:
                    inheritance.append(pkg_name(i['pkg_name']) +
                                       '_models.' + i['name'])
                    import_str = ('from ' + impl_root_path(i['pkg_name']) +
                                  pkg_name(i['pkg_name']) + 
                                  ' import models as ' + pkg_name(i['pkg_name']) +
                                  '_models')
                    if import_str not in imports:
                        imports.append(import_str)
            inheritance.append('models.Model')
            ##
            # Note that the following re-assigne the inheritance variable from a 
            # list to a string.
            if inheritance:
                inheritance = '(' + ', '.join(inheritance) + ')'
            else:
                inheritance = ''
            ##
            # Assemble class signature
            class_sig = 'class ' + interface['shortname'] + inheritance + ':'
            """
            
            ##
            # Build all mdata maps, checking to see if there is a hand built
            # mdataimplementation available
            if not hasattr(impl_class, 'mdata'):
                mdata_maps = make_mdata_maps(interface, patterns)
            else:
                mdata_maps = getattr(impl_class, 'mdata')
            ##
            # Assemble complete model string to be saved as models.py
            mdata = (mdata +  '\n' +  mdata_maps + '\n')

    ##
    # Finally, save the mdata to the appropriate mdata_conf.py file.
    if mdata.strip() != '':
        write_file = open(app_name(package['name']) + '/' + 
                          pkg_name(package['name']) + '/mdata_conf.py', 'w')
        write_file.write((import_str + '\n'.join(imports) + '\n\n' +
                          mdata).encode('utf-8'))
        write_file.close


def load_impl_class(package_name, interface_name):
    ##
    # Try loading implentations for this interface
    impl_class = None
    try:
        impls = __import__('builders.mongoosid_templates.' +
                                     package_name,
                                     fromlist = [interface_name])
    except (ImportError, KeyError):
        pass
    else:
        if hasattr(impls, interface_name):
            impl_class = getattr(impls, interface_name)
    return impl_class


def make_mdata_maps(interface, patterns):
    from builders.mongoosid_templates import options
    pd = interface['shortname'] + '.persisted_data'
    rt = interface['shortname'] + '.return_types'
    mdata = ''
    field_options = ''
    id_table = ''
    cat_table = ''
    if pd in patterns and patterns[pd] != {}:
        for data_name in patterns[pd]:
            if patterns[pd][data_name] == 'OsidCatalog':
                pass
                """
                cat_table = cat_table + make_cat_table(data_name,
                                        interface['shortname'],
                                        patterns['package_objects_caps'],
                                        patterns['package_catalog_caps'])
                """
            elif (rt in patterns and 
                  data_name in patterns[rt] and 
                  patterns[rt][data_name] == 'osid.locale.DisplayText'):
                mdata = mdata + make_mdata_map(data_name, 
                                    'DisplayText', options) + '\n'                
            else:
                mdata = mdata + make_mdata_map(data_name, 
                                    patterns[pd][data_name], options) + '\n'

    """
    if field_options != '':
        model = ('\n    from collections import OrderedDict' +
                 '\n    from ..osid.models import OsidObject' +
                 '\n    options = OrderedDict(OsidObject.options)' +
                 '\n    moptions = OrderedDict(OsidObject.moptions)\n' +
                 field_options + '\n' + model)
    if model != '' and (interface['shortname'].startswith('Osid') or
                        interface['category'] == 'markers'):
        model = model + '\n    class Meta:\n        abstract = True\n'
    if model == '' and (interface['shortname'].startswith('Osid') or
                        interface['category'] == 'markers'):
        model = '    class Meta:\n        abstract = True\n'
    elif model == '':
        model = '    pass\n\n'
    if id_table != '':
        model = model + '\n' + id_table
    if cat_table != '':
        model = model + '\n' + cat_table
    """
    return mdata

##### NEED TO FINISH THIS #####
def make_mdata_map(data_name, data_type, options):
    mdata = ''
    lead_in = data_name.upper() + ' = {'
    lead_out = '\n    }\n'

    if data_type == 'boolean':
        template = string.Template(options.COMMON_MDATA + 
                                   options.BOOLEAN_MDATA)
        mdata = template.substitute({
            'element_identifier': data_name,
            'element_label': ' '.join(data_name.split('_')),
            'instructions': 'enter either true or false.',
            'array': 'False'
            })
    elif data_type == 'string':
        template = string.Template(options.COMMON_MDATA + 
                                   options.STRING_MDATA)
        # In the following max_length may want to come from a configuration setting:
        mdata = template.substitute({
            'element_identifier': data_name,
            'element_label': ' '.join(data_name.split('_')),
            'instructions': 'enter no more than 256 characters.',
            'max_length': 256,
            'array': 'False'
            })
    elif data_type == 'decimal':
        template = string.Template(options.COMMON_MDATA + 
                                   options.DECIMAL_MDATA)
        mdata = template.substitute({
            'element_identifier': data_name,
            'element_label': ' '.join(data_name.split('_')),
            'instructions': 'enter a decimal value.',
            'array': 'False'
            })
    elif data_type == 'DisplayText':
        template = string.Template(options.COMMON_MDATA + 
                                   options.DISPLAY_TEXT_MDATA)
        # In the following max_length may want to come from a configuration setting:
        mdata = template.substitute({
            'element_identifier': data_name,
            'element_label': ' '.join(data_name.split('_')),
            'instructions': 'enter no more than 256 characters.',
            'max_length': 256,
            'array': 'False'
            })
    elif data_type in ['osid.id.Id']:
        template = string.Template(options.COMMON_MDATA +
                                   options.ID_MDATA)
        mdata = template.substitute({
            'element_identifier': data_name,
            'element_label': ' '.join(data_name.split('_')),
            'instructions': 'accepts an ' + data_type + ' object',
            'syntax': data_type.split('.')[-1].upper(),
            'id_type': data_type.split('.')[-1].lower(),
            'array': 'False'
            })
    elif data_type in ['osid.type.Type']:
        template = string.Template(options.COMMON_MDATA +
                                   options.TYPE_MDATA)
        mdata = template.substitute({
            'element_identifier': data_name,
            'element_label': ' '.join(data_name.split('_')),
            'instructions': 'accepts an ' + data_type + ' object',
            'syntax': data_type.split('.')[-1].upper(),
            'id_type': data_type.split('.')[-1].lower(),
            'array': 'False'
            })
    elif data_type in ['osid.id.Id[]', 'osid.type.Type[]']:
        template = string.Template(options.COMMON_MDATA +
                                   options.ID_LIST_MDATA)
        mdata = template.substitute({
            'element_identifier': data_name,
            'element_label': ' '.join(data_name.split('_')),
            'instructions': 'accepts an ' + data_type + ' object',
            'syntax': data_type.split('.')[-1].strip('[]').upper(),
            'id_type': data_type.split('.')[-1].strip('[]').lower(),
            'array': 'True'
            })
    elif data_type in ['osid.calendaring.DateTime', 'timestamp']:
        template = string.Template(options.COMMON_MDATA + 
                                   options.DATE_TIME_MDATA)
        mdata = template.substitute({
            'element_identifier': data_name,
            'element_label': ' '.join(data_name.split('_')),
            'instructions': 'enter a valid datetime object.',
            'array': 'False'
            })
    elif data_type == 'osid.calendaring.Duration':
        template = string.Template(options.COMMON_MDATA + 
                                   options.DURATION_MDATA)
        mdata = template.substitute({
            'element_identifier': data_name,
            'element_label': ' '.join(data_name.split('_')),
            'instructions': 'enter a valid duration object.',
            'array': 'False'
            })
    elif data_type == 'osid.transport.DataInputStream':
        template = string.Template(options.COMMON_MDATA + 
                                   options.OBJECT_MDATA)
        mdata = template.substitute({
            'element_identifier': data_name,
            'element_label': ' '.join(data_name.split('_')),
            'instructions': 'accepts a valid data input stream.',
            'array': 'False'
            })
    if mdata:
        mdata = (lead_in + mdata + lead_out)
    return mdata

""" DONT NEED THESE ANYMORE
def make_model_field(data_name, data_type, options):
    model_field = ''
    template = string.Template(options.MODEL_FIELD_OPTIONS)
    if data_type == 'boolean':
        model_field = (
        '    ' + data_name + ' = models.NullBooleanField(**options[\'' + data_name + '\'])'
        )
    elif data_type == 'string':
        field_options = template.substitute({'data_name': data_name})
        model_field = (
        '    ' + data_name + ' = models.CharField(**options[\'' + data_name + '\'])'
        )
    elif data_type in ['osid.id.Id', 'osid.type.Type']:
        model_field = (
        '    ' + data_name + '_authority = models.CharField(**options[\'' + data_name + '_authority\'])\n' +
        '    ' + data_name + '_namespace = models.CharField(**options[\'' + data_name + '_namespace\'])\n' +
        '    ' + data_name + '_identifier = models.CharField(**options[\'' + data_name + '_identifier\'])'
        )
    else:
        model_field = '    # data field for ' + data_name + ' ' + data_type + ' not processed'
    return model_field

def make_id_table(data_name, interface_name):
    model = (
    'class ' + interface_name + '_' + data_name.title() + '(models.Model):\n' +
    '    ' + interface_name.lower() + ' = models.ForeignKey(\'' + interface_name + '\')\n' +
    '    authority = models.CharField(**' + interface_name + '.options[\'' + data_name + '_authority\'])\n' + 
    '    namespace = models.CharField(**' + interface_name + '.options[\'' + data_name + '_namespace\'])\n' +
    '    identifier = models.CharField(**' + interface_name + '.options[\'' + data_name + '_identifier\'])\n\n'
    )
    return model
    
def make_cat_table(data_name, interface_name, 
                   package_objects_caps, package_catalog_caps):
    if data_name == 'no_catalog':
        return ''
    else:
        return (
    'class ' + interface_name + '_' + package_catalog_caps + '(models.Model):\n' +
    '    ' + interface_name.lower() + ' = models.ForeignKey(\'' + interface_name + '\')\n' +
    '    ' + data_name + '_identifier = models.CharField(max_length=64, blank=False, default=\'default\')\n\n')
"""


##
# The following functions return the app name and module name strings
# by prepending and appending the appropriate suffixes and prefixes. Note
# that the django app_name() function is included to support building of
# the abc osids into a Django project environment.
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


