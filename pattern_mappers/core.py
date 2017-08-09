from binder_helpers import make_plural


# Investigate all the methods in the core osid service.  It is assumed
# that most, of not all of these will need to be implemented by hand.
def map_osid_patterns(interface, package, index):

    for method in interface['methods']:
        var_name = method['name'].split('_', 1)[-1]

        if (interface['shortname'] == 'Metadata' and
                method['name'] in ['get_element_label', 'get_instructions']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_metadata.GenericMetadata.get_element_label',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type']))

        elif (interface['shortname'] == 'Metadata' and
                'supports_' not in method['name'] and
                len(method['errors']) == 0):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_metadata.GenericMetadata.get_element_id',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type']))

        elif (interface['shortname'] == 'Metadata' and
                'supports_' not in method['name'] and
                len(method['errors']) == 1 and
                'ILLEGAL_STATE' in method['errors']):
            error_string_list = method['error_doc'].split()
            syntax_list = []
            for s in error_string_list:
                if s.strip('`').isupper() and s.strip('`') != 'ILLEGAL_STATE':
                    syntax_list.append(s.strip('`'))
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_metadata.GenericMetadata.get_minimum_cardinal',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            syntax_list='[\'' + '\', \''.join(syntax_list) + '\']',
                            return_type_full=method['return_type']))

        elif (interface['shortname'] == 'Metadata' and
                method['name'].startswith('supports_') and
                len(method['errors']) == 2 and
                'NULL_ARGUMENT' in method['errors']):
            error_string_list = method['error_doc'].split()
            syntax_list = []
            for s in error_string_list:
                if s.isupper() and s not in ['ILLEGAL_STATE', 'NULL_ARGUMENT']:
                    syntax_list.append(s)
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_metadata.GenericMetadata.supports_coordinate_type',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=make_plural(var_name),
                            syntax_list='[\'' + '\', \''.join(syntax_list) + '\']',
                            return_type_full=method['return_type'],
                            arg0_name=method['args'][0]['var_name']))

        elif (interface['shortname'] == 'Metadata' and
                method['name'].startswith('get_existing_')):
            error_string_list = method['error_doc'].split()
            syntax_list = []
            for s in error_string_list:
                if s.isupper() and s not in ['ILLEGAL_STATE', 'NULL_ARGUMENT']:
                    syntax_list.append(s)
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_metadata.GenericMetadata.get_existing_cardinal_values',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=make_plural(var_name),
                            syntax_list='[\'' + '\', \''.join(syntax_list) + '\']',
                            return_type_full=method['return_type'],
                            arg0_name=method['args'][0]['var_name']))

        else:
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name']))
            for arg_index, arg in enumerate(method['args']):
                arg_dict = {}
                arg_dict['arg{0}_name'.format(str(arg_index))] = arg['var_name']
                index[interface['shortname'] + '.' + method['name']]['kwargs'].update(arg_dict)
    return index


# Investigate all the methods in the osid.type service.  It is assumed
# that most, of not all of these will need to be implemented by hand.
def map_type_patterns(interface, package, index):

    object_name = 'Type'
    for method in interface['methods']:

        if method['name'] == 'get_next_type':
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_list.GenericObjectList.get_next_object',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            return_type_full=method['return_type']))

        elif method['name'] == 'get_next_types':
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_list.GenericObjectList.get_next_objects',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            arg0_name=method['args'][0]['var_name'],
                            return_type_full=method['return_type']))

        else:
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name']))
    return index


# Investigate all the methods in the osid.id service.  It is assumed
# that most, of not all of these will need to be implemented by hand.
def map_id_patterns(interface, package, index):

    object_name = 'Id'
    for method in interface['methods']:

        if method['name'] == 'get_next_id':
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_list.GenericObjectList.get_next_object',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            return_type_full=method['return_type']))

        elif method['name'] == 'get_next_ids':
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_list.GenericObjectList.get_next_objects',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            arg0_name=method['args'][0]['var_name'],
                            return_type_full=method['return_type']))

        else:
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name']))
    return index
