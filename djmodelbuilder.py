
import time
import os
import json
import string
from abcbinder_settings import PKGMAPSDIRECTORY as pkg_maps_dir
from abcbinder_settings import MAINDOCINDENTSTR as main_doc_indent
from abcbinder_settings import ENCODING as utf_code
from djbuilder_settings import APPNAMEPREFIX as app_prefix
from djbuilder_settings import APPNAMESUFFIX as app_suffix
from djbuilder_settings import PACKAGEPREFIX as pkg_prefix
from djbuilder_settings import PACKAGESUFFIX as pkg_suffix
from djbuilder_settings import ROOTPACKAGE as root_pkg
from djbuilder_settings import ROOTPATH as root_path

##
# This is the entry point for making django-based python models for
# the osids. It processes all of the osid maps in the package maps
# directory.
def make_djmodels():
    for json_file in os.listdir(pkg_maps_dir):
        if json_file.endswith('.json'):
            make_djmodel(pkg_maps_dir + '/' + json_file)

##
# This function expects a file containing a json representation of an
# osid package that was prepared by the mapper.
def make_djmodel(file_name):
    from binder_helpers import get_interface_module

    ##
    # Get the package map for this osid package
    read_file = open(file_name, 'r')
    package = json.load(read_file)
    read_file.close()
    
    ##
    # Get the pattern map for this osid package.
    read_file = open('builders/pattern_maps/' + 
                      package['name'] + '.json', 'r')
    patterns = json.load(read_file)
    read_file.close()

    models = ''

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
        if (interface['shortname'] in patterns['package_objects_caps'] or
            interface['shortname'] in patterns['package_relationships_caps'] or
            interface['shortname'] == 'OsidObject' or
            interface['category'] == 'markers' or
            interface['shortname'] == patterns['package_catalog_caps']):
            inheritance = []
            imports = ['from django.db import models']
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
            ##
            # Build all model fields, checking to see if there is a hand
            # modelimplementation available
            if not hasattr(impl_class, 'model'):
                model_fields = make_model_fields(interface, patterns)
            else:
                model_fields = getattr(impl_class, 'model')
            ##
            # Assemble complete model string to be saved as models.py
            models = (models + class_sig + '\n' +  model_fields + '\n')

    ##
    # Finally, save the model to the appropriate models.py file.
    if models.strip() != '':
        write_file = open(app_name(package['name']) + '/' + 
                          pkg_name(package['name']) + '/models.py', 'w')
        write_file.write(('\n'.join(imports) + '\n\n' +
                          models).encode('utf-8'))
        write_file.close

def load_impl_class(package_name, interface_name):
    ##
    # Try loading implentations for this interface
    impl_class = None
    try:
        impls = __import__('builders.djosid_templates.' +
                                     package_name,
                                     fromlist = [interface_name])
    except (ImportError, KeyError):
        pass
    else:
        if hasattr(impls, interface_name):
            impl_class = getattr(impls, interface_name)
    return impl_class

def make_model_fields(interface, patterns):
    from builders.djosid_templates import options
    pd = interface['shortname'] + '.persisted_data'
    model = ''
    field_options = ''
    id_table = ''
    cat_table = ''
    if pd in patterns and patterns[pd] != {}:
        for data_name in patterns[pd]:
            if patterns[pd][data_name] == 'OsidCatalog':
                cat_table = cat_table + make_cat_table(data_name,
                                        interface['shortname'],
                                        patterns['package_objects_caps'],
                                        patterns['package_catalog_caps'])
            elif patterns[pd][data_name] == 'osid.id.Id[]':
                id_table = id_table + make_id_table(data_name,
                                                    interface['shortname'])
                field_options = field_options + make_field_options(data_name, 
                                    patterns[pd][data_name][:-2], options)
            else:
                field_options = field_options + make_field_options(data_name, 
                                    patterns[pd][data_name], options)
                model = model + make_model_field(data_name, 
                                    patterns[pd][data_name], options) + '\n'
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
    return model

##### NEED TO FINISH THIS #####
def make_field_options(data_name, data_type, options):
    field_options = ''
    osid_options = ''
    lead_in = '    options[\'' + data_name + '\'] = {'
    lead_out = '\n            }\n'
    osid_lead_in = ('    moptions[\'' + data_name + '\'] = dict(options[\'' 
                                              + data_name + '\'])\n' +
                        '    moptions[\'' + data_name + '\'].update({')
    osid_lead_out = '\n            })\n'
    if data_type == 'boolean':
        template = string.Template(options.COMMON_FIELD_OPTIONS + 
                                   options.BOOLEAN_FIELD_OPTIONS)
        field_options = template.substitute({
            'verbose_name': ' '.join(data_name.split('_')),
            'help_text': 'enter either true or false.'
            })
        osid_options = (options.COMMON_OSID_OPTIONS +
                        options.BOOLEAN_OSID_OPTIONS)
    elif data_type == 'string':
        template = string.Template(options.COMMON_FIELD_OPTIONS + 
                                   options.STRING_FIELD_OPTIONS)
        # In the following max_length may want to come from a settings file:
        field_options = template.substitute({
            'verbose_name': ' '.join(data_name.split('_')),
            'help_text': 'enter no more than 256 characters.',
            'max_length': 256
            })
        osid_options = (options.COMMON_OSID_OPTIONS +
                        options.STRING_OSID_OPTIONS)
    elif data_type in ['authority','namespace','identifier']:
        l = {'authority': 128, 'namespace': 128, 'identifier': 64}
        osid_lead_in = osid_lead_out = ''
        template = string.Template(options.COMMON_FIELD_OPTIONS + 
                                   options.STRING_FIELD_OPTIONS)
        field_options = template.substitute({
            'verbose_name': ' '.join(data_name.split('_')),
            'help_text': '',
            'max_length': l[data_type]
            })
        osid_options = ''
    elif data_type in ['osid.id.Id', 'osid.type.Type']:
        lead_in = lead_out = ''
        osid_lead_in = '    moptions[\'' + data_name + '\'] = {'
        osid_lead_out = '\n            }\n'
        authority_options = make_field_options(data_name + '_authority', 'authority', options)
        namespace_options = make_field_options(data_name + '_namespace', 'namespace', options)
        identifier_options = make_field_options(data_name + '_identifier', 'identifier', options)
        field_options = authority_options + namespace_options + identifier_options
        template = string.Template(options.COMMON_FIELD_OPTIONS +
                                   options.COMMON_OSID_OPTIONS +
                                   options.ID_OSID_OPTIONS)
        osid_options = template.substitute({
            'verbose_name': ' '.join(data_name.split('_')),
            'help_text': 'accepts an ' + data_type + ' object',
            'id_type': data_type.split('.')[-1].lower()
            })

    elif data_type == 'osid.type.Type':
        pass
    if field_options:
        field_options = (lead_in + field_options + lead_out)
    if osid_options:
        osid_options = (osid_lead_in + osid_options  + osid_lead_out)
    return field_options + osid_options

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


