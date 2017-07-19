from binder_helpers import make_plural, remove_plural, get_cat_name_for_pkg,\
    camel_to_under
from osid_meta import OSID_Language_Primitives
from syntax_helpers import get_syntax_for_arg_type
OSID_Calendaring_Primitives = ['osid.calendaring.Time', 'osid.calendaring.DateTime', 'osid.calendaring.Duration']


def map_object_form_patterns(interface, package, index):
    object_name = interface['shortname'][:-4]
    index[interface['shortname'] + '.init_pattern'] = 'osid_form.GenericObjectForm'

    for method in interface['methods']:
        var_name = method['name'].split('_', 1)[-1]

        # ObjectForm methods that set a persisted boolean value.
        if (method['name'].startswith('set_') and
                len(method['arg_types']) == 1 and
                method['arg_types'][0] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.set_simple_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type'],
                            syntax='BOOLEAN'))

        # ObjectForm methods that clear a persisted boolean value.
        elif (method['name'].startswith('clear_') and
              var_name in index[object_name + '.persisted_data'] and
              len(index[object_name + '.arg_detail'][var_name]) == 1 and
              index[object_name + '.arg_detail'][var_name][0]['arg_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.clear_simple_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            syntax='BOOLEAN'))

        # ObjectForm methods that set a persisted osid.id.Id of another
        # osid object.
        elif (method['name'].startswith('set_') and
                len(method['arg_types']) == 1 and
                method['arg_types'][0] == 'osid.id.Id'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.set_id_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type'],
                            syntax='ID'))

        ##
        # ObjectForm methods that clear a persisted osid.id.Id.
        elif (method['name'].startswith('clear_') and
              var_name in index[object_name + '.persisted_data'] and
              len(index[object_name + '.arg_detail'][var_name]) == 1 and
              index[object_name + '.arg_detail'][var_name][0]['arg_type'] == 'osid.id.Id'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.clear_id_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            syntax='ID'))

        # ObjectForm methods that set multiple persisted osid.id.Ids of
        # other osid objects.
        elif (method['name'].startswith('set_') and
                len(method['arg_types']) == 1 and
                method['arg_types'][0] == 'osid.id.Id[]' and
                method['args'][0]['array'] is True):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.set_id_list_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type'],
                            syntax='ID'))

        # ObjectForm methods that clear multiple persisted osid.id.Ids of
        # other osid objects.
        elif (method['name'].startswith('clear_') and
                var_name in index[object_name + '.persisted_data'] and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] == 'osid.id.Id[]' and
                index[object_name + '.arg_detail'][var_name][0]['array'] is True):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.clear_id_list_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            syntax='ID'))

        # ObjectForm methods that return a metadata object for an Id element
        elif (method['name'].startswith('get_') and
                method['name'].endswith('_metadata') and
                var_name[:-9] in index[object_name + '.persisted_data'] and
                index[object_name + '.persisted_data'][var_name[:-9]] == 'osid.id.Id'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.get_id_attribute_metadata',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name[:-9],
                            return_type_full=method['return_type'],
                            syntax='ID'))

        # ObjectForm methods that return a metadata object for an Id element list
        elif (method['name'].startswith('get_') and
                method['name'].endswith('_metadata') and
                var_name[:-9] in index[object_name + '.persisted_data'] and
                index[object_name + '.persisted_data'][var_name[:-9]] == 'osid.id.Id[]'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.get_id_list_attribute_metadata',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name[:-9],
                            return_type_full=method['return_type'],
                            syntax='ID'))

        # ObjectForm methods that return a metadata object for a Type element
        elif (method['name'].startswith('get_') and
                method['name'].endswith('_metadata') and
                var_name[:-9] in index[object_name + '.persisted_data'] and
                index[object_name + '.persisted_data'][var_name[:-9]] == 'osid.type.Type'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                # pattern='logging.LogEntryForm.get_priority_metadata',
                pattern='osid_form.GenericObjectForm.get_id_attribute_metadata',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name[:-9],
                            return_type_full=method['return_type'],
                            syntax='TYPE'))

        # ObjectForm methods that return a metadata object for a primitive element
        elif (method['name'].startswith('get_') and
                method['name'].endswith('_metadata')):
            try:
                arg_type = index[object_name + '.arg_detail'][var_name[:-9]][0]['arg_type'].strip('[]')
            except KeyError:
                try:
                    arg_type = index[object_name + '.arg_detail'][make_plural(var_name[:-9])][0]['arg_type'].strip('[]')
                except KeyError:
                    arg_type = 'none'
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.get_simple_attribute_metadata',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name[:-9],
                            return_type_full=method['return_type'],
                            syntax=get_syntax_for_arg_type(arg_type)))

        # ObjectForm methods that set a persisted DisplayText string.
        elif (method['name'].startswith('set_') and
                len(method['arg_types']) == 1 and
                method['arg_types'][0] == 'string' and
                interface['shortname'][:-4] + '.return_types' in index and
                index[interface['shortname'][:-4] + '.return_types'][var_name] == 'osid.locale.DisplayText'):
            print("FOUND DISPLAY TEXT {0}".format(var_name))
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.set_display_text_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type'],
                            syntax='STRING'))

        # ObjectForm methods that set a persisted string.
        elif (method['name'].startswith('set_') and
                len(method['arg_types']) == 1 and
                method['arg_types'][0] == 'string'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.set_string_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type'],
                            syntax='STRING'))

        # ObjectForm methods that set a persisted decimal value.
        elif (method['name'].startswith('set_') and
                len(method['arg_types']) == 1 and
                method['arg_types'][0] == 'decimal'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.set_decimal_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type'],
                            syntax='DECIMAL'))

        # ObjectForm methods that clear a persisted decimal value.
        elif (method['name'].startswith('clear_') and
                var_name in index[object_name + '.persisted_data'] and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] == 'decimal'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.clear_decimal_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            syntax='DECIMAL'))

        # ObjectForm methods that set a persisted DateTime. Also looks for timestamps
        elif (method['name'].startswith('set_') and
                len(method['arg_types']) == 1 and
                method['arg_types'][0] in ['osid.calendaring.DateTime', 'timestamp']):
            print("FOUND STRING {0}".format(var_name))
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='assessment.AssessmentOfferedForm.set_start_time',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type'],
                            syntax='DATETIME'))

        # ObjectForm methods that set a persisted Durations.
        elif (method['name'].startswith('set_') and
                len(method['arg_types']) == 1 and
                method['arg_types'][0] == 'osid.calendaring.Duration'):
            print("FOUND STRING {0}".format(var_name))
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='assessment.AssessmentOfferedForm.set_duration',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type'],
                            syntax='DURATION'))

        # ObjectForm methods that clear a persisted string for a DisplayText.
        elif (method['name'].startswith('clear_') and
                var_name in index[object_name + '.persisted_data'] and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.return_types'][var_name] == 'osid.locale.DisplayText' and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] == 'string'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.clear_display_text_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            syntax='STRING'))

        # ObjectForm methods that clear a persisted string.
        elif (method['name'].startswith('clear_') and
                var_name in index[object_name + '.persisted_data'] and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] == 'string'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.clear_string_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            syntax='STRING'))

        # ObjectForm methods that clear a persisted DateTime.
        elif (method['name'].startswith('clear_') and
                var_name in index[object_name + '.persisted_data'] and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] in ['osid.calendaring.DateTime', 'timestamp']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='assessment.AssessmentOfferedForm.clear_start_time',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            syntax='DATETIME'))

        # ObjectForm methods that clear a persisted Duration.
        elif (method['name'].startswith('clear_') and
                var_name in index[object_name + '.persisted_data'] and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] == 'osid.calendaring.Duration'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='assessment.AssessmentOfferedForm.clear_duration',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            syntax='DURATION'))

        # ObjectForm methods that set a persisted DataInputStream.
        elif (method['name'].startswith('set_') and
                len(method['arg_types']) == 1 and
                method['arg_types'][0] == 'osid.transport.DataInputStream'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='repository.AssetContentForm.set_content_data',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type'],
                            syntax='OBJECT'))

        # ObjectForm methods that clear a persisted DataInputStream.
        elif (method['name'].startswith('clear_') and
                var_name in index[object_name + '.persisted_data'] and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] == 'osid.transport.DataInputStream'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='repository.AssetContentForm.clear_content_data',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            syntax='OBJECT'))

        # ObjectForm methods that add a persisted Type.
        elif (method['name'].startswith('add_') and
                len(method['arg_types']) == 1 and
                method['arg_types'][0] == 'osid.type.Type'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='repository.AssetContentForm.add_accessibility_type',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            arg0_name=method['args'][0]['var_name'],
                            syntax='TYPE'))

        # ObjectForm methods that remove a persisted Type.
        elif (method['name'].startswith('remove_') and
                var_name in index[object_name + '.persisted_data'] and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] == 'osid.type.Type'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='repository.AssetContentForm.remove_accessibility_type',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            arg0_name=method['args'][0]['var_name'],
                            syntax='TYPE'))

        # ObjectForm methods that clear all of persisted Types. Note
        # that the AssetContentForm version of this uses the plural. and is
        # associated with the above add and remove methods. Is this
        # a typical pattern?
        elif (method['name'].startswith('clear_') and
                method['name'].endswith('_types') and
                remove_plural(var_name) in index[object_name + '.persisted_data'] and
                len(index[object_name + '.arg_detail'][remove_plural(var_name)]) == 1 and
                index[object_name + '.arg_detail'][remove_plural(var_name)][0]['arg_type'] == 'osid.type.Type'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='repository.AssetContentForm.clear_accessibility_types',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=remove_plural(var_name),
                            syntax='TYPE'))

        # ObjectForm methods that sets a persisted Type.
        elif (method['name'].startswith('set_') and
                len(method['arg_types']) == 1 and
                method['arg_types'][0] == 'osid.type.Type'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.set_id_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type'],
                            syntax='TYPE'))

        # ObjectForm methods that clears a persisted Type.
        elif (method['name'].startswith('clear_') and
                var_name in index[object_name + '.persisted_data'] and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] == 'osid.type.Type'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.clear_id_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            syntax='TYPE'))

        # ObjectForm methods that get an extension record.
        elif (method['name'].startswith('get_') and
                method['name'].endswith('_record')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_form.GenericObjectForm.get_object_form_record',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type'],
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type']))

        else:
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name']))

    return index


def map_object_patterns(interface, package, index):
    object_name = interface['shortname']
    index[object_name + '.init_pattern'] = 'osid_object.GenericObject'

    for method in interface['methods']:
        var_name = method['name'].split('_', 1)[-1]

        if var_name.endswith('_id') or var_name.endswith('_ids'):
            var_name = '_'.join(var_name.split('_')[:-1])
        # Object methods that get a persisted boolean value with an
        # 'is_something_based_otherthing' question.  Perhaps only found
        # in learning Activities
        if (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('is_') and
                '_based_' in method['name'] and
                index[object_name + '.persisted_data'][var_name] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='learning.Activity.is_asset_based_activity',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type']))

        # Object methods that get a persisted boolean value with an
        # 'is' question.
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('is_') and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObject.is_attribute_boolean',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type']))

        # Object methods that get a persisted boolean value with an
        # 'is' question. NOTE This is currently patterned as above
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('are_') and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObject.is_attribute_boolean',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type']))

        # Object methods that get an instance boolean value with an
        # 'is' question.  NOTE This is currently patterned as above
        elif (var_name in index[object_name + '.instance_data'] and
                method['name'].startswith('is_') and
                index[object_name + '.instance_data'][var_name] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObject.is_attribute_boolean',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type']))

        # Object methods in repository.Asset that get a persisted boolean value
        # with a 'can' question.
        elif (interface['shortname'] == 'Asset' and
                var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('can_') and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObject.can_attribute_boolean',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type']))

        # Object methods that get a boolean value with a 'has' question
        # to check for the existence of a persisted object from this package
        # referenced by an Id.
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('has_') and
                var_name in index['package_objects_under'] and
                'get_' + var_name + '_id' in interface['method_names']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='calendar.Schedule.has_time_period',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type']))

        # Object methods that get a boolean value with a 'has' question
        # to check for the existence of an instance object from this package
        # referenced by an Id. NOTE this is currently patterned as above
        elif (var_name in index[object_name + '.instance_data'] and
                method['name'].startswith('has_') and
                var_name in index['package_objects_under'] and
                'get_' + var_name + '_id' in interface['method_names']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='calendar.Schedule.has_time_period',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type']))

        # Object methods that get a boolean value with a 'has' question
        # to check for the existence of a persisted object from another osid package
        # referenced by an Id.
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('has_') and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] == 'osid.id.Id'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObject.has_id_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type']))

        # Object methods that get a boolean value with a 'has' question
        # to check for the existence of a persisted object from another osid package
        # referenced by an Id. NOTE this is currently patterned as above
        elif (var_name in index[object_name + '.instance_data'] and
                method['name'].startswith('has_') and
                index[object_name + '.instance_data'][var_name] == 'osid.id.Id'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObject.has_id_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type']))

        # Object methods that get a boolean value with a 'has' question
        # to check for the existence of a DisplayTest object.
        # THERE MAY NOT BE ANY OF THESE
        elif (False and var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('has_') and
                index[object_name + '.persisted_data'][var_name] == 'string' and
                method['return_type'] == 'osid.locale.DisplayText'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='????????????',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type']))

        # Object methods that get a boolean value with a 'has' question
        # to check for the existence of Time or DateTime objects.
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('has_') and
                index[object_name + '.persisted_data'][var_name] in ['osid.calendaring.Time', 'osid.calendaring.DateTime', 'timestamp'] and
                method['return_type'] in ['osid.calendaring.Time', 'osid.calendaring.DateTime']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='assessment.AssessmentOffered.has_start_time',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type']))

        # Object methods that get a boolean value with a 'has' question
        # to check for the existence of a primitive.
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('has_') and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] in OSID_Language_Primitives):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='repository.AssetContent.has_url',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type']))

        # Object methods that get a boolean value with a 'has' question
        # to check for the existence of a DateTime or Duration, etc.
        # NOTE: Patterned same as for primitive above
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('has_') and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] in OSID_Calendaring_Primitives):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='repository.AssetContent.has_url',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type']))

        # Object methods that get a persisted DisplayText.
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('get_') and
                index[object_name + '.persisted_data'][var_name] == 'string' and
                method['return_type'] == 'osid.locale.DisplayText'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='repository.Asset.get_title',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get an instance DisplayText.
        # NOTE this is currently patterned the same as above
        elif (var_name in index[object_name + '.instance_data'] and
                method['name'].startswith('get_') and
                index[object_name + '.instance_data'][var_name] == 'osid.locale.DisplayText' and
                method['return_type'] == 'osid.locale.DisplayText'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='repository.Asset.get_title',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get a persisted string.
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('get_') and
                index[object_name + '.persisted_data'][var_name] == 'string'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='repository.AssetContent.get_url',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get a persisted decimal value.
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('get_') and
                index[object_name + '.persisted_data'][var_name] == 'decimal'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='grading.GradeSystem.get_lowest_numeric_score',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get an instance decimal value.
        # NOTE this may want to be patterned as above, if we can find a persisted pattern for decimals
        elif (var_name in index[object_name + '.instance_data'] and
                method['name'].startswith('get_') and
                index[object_name + '.instance_data'][var_name] == 'decimal'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='assessment.AssessmentTaken.get_score',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get a persisted cardinal value.
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('get_') and
                index[object_name + '.persisted_data'][var_name] == 'cardinal'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='????????????????',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get an instance cardinal value.
        # NOTE this may want to be patterned as above, if we can find a persisted pattern for cardinals
        elif (var_name in index[object_name + '.instance_data'] and
                method['name'].startswith('get_') and
                index[object_name + '.instance_data'][var_name] == 'cardinal'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='assessment.AssessmentTaken.get_completion',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get the osid.id.Id of a persisted but not
        # required object from this osid package. this investigates whether
        # a 'has_thing' method also exists.
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('get_') and
                method['name'].endswith('_id') and
                'has_' + var_name in interface['method_names'] and
                var_name in index['package_objects_under'] and
                index[object_name + '.persisted_data'][var_name] == 'osid.id.Id'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='calendar.Schedule.get_time_period_id',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get the a persisted Type
        # This does not look for a has_thing method
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('get_') and
                index[object_name + '.persisted_data'][var_name] == 'osid.type.Type'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='logging.LogEntry.get_priority',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get the osid.id.Id of an instance object from this
        # osid package. this investigates whether a 'has_thing' method also exists.
        # FOR NOW, The pattern is set to the same as above
        elif (var_name in index[object_name + '.instance_data'] and
              method['name'].startswith('get_') and
              method['name'].endswith('_id') and
              ('has_' + var_name in interface['method_names'] or
               'is_' + var_name + 'ed' in interface['method_names']) and
              var_name in index['package_objects_under'] and
              index[object_name + '.instance_data'][var_name] == 'osid.id.Id'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='calendar.Schedule.get_time_period_id',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get a persisted but not required datetime.
        # this investigates whether a 'has_thing' method also exists.
        # this also deals with the timestamp that appears in some args that set persisted data
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('get_') and
                'has_' + var_name in interface['method_names'] and
                index[object_name + '.persisted_data'][var_name] in ['osid.calendaring.DateTime', 'timestamp']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='assessment.AssessmentOffered.get_start_time',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get an instance but not required datetime.
        # this investigates whether a 'has_thing' method also exists.
        # this also deals with the timestamp that appears in some args that set persisted data
        # NOTE this is currently patterned as above
        elif (var_name in index[object_name + '.instance_data'] and
                method['name'].startswith('get_') and
                'has_' + var_name in interface['method_names'] and
                index[object_name + '.instance_data'][var_name] in ['osid.calendaring.DateTime', 'timestamp']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='assessment.AssessmentOffered.get_start_time',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get a persisted but not required duration.
        # this investigates whether a 'has_thing' method also exists.
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('get_') and
                'has_' + var_name in interface['method_names'] and
                index[object_name + '.persisted_data'][var_name] == 'osid.calendaring.Duration'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='assessment.AssessmentOffered.get_duration',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get an instance but not required duration.
        # this investigates whether a 'has_thing' method also exists.
        # NOTE this is currently patterned as above
        elif (var_name in index[object_name + '.instance_data'] and
                method['name'].startswith('get_') and
                'has_' + var_name in interface['method_names'] and
                index[object_name + '.instance_data'][var_name] == 'osid.calendaring.Duration'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='assessment.AssessmentOffered.get_duration',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get the osid.id.Id of an aggregated object
        # from this package.  Note that this is for a plural form method:
        elif (object_name + '.aggregate_data' in index and
                make_plural(var_name) in index[object_name + '.aggregate_data'] and
                method['name'].startswith('get_') and
                method['name'].endswith('_ids') and
                var_name in index['package_objects_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='repository.Asset.get_asset_content_ids',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            aggregated_object_name=index['package_objects_under_to_caps'][var_name],
                            return_type_full=method['return_type']))

        # Object methods that get an osid.id.IdList for a list of objects not
        # from this package:
        elif (method['name'].startswith('get_') and
                method['name'].endswith('_ids') and
                var_name not in index['package_objects_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='learning.Activity.get_asset_ids',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get the osid.id.Id of a persisted object that
        # appears to be an initialized relationship source.
        elif (object_name in index['package_relationships_caps'] and
                object_name.lower() in index['package_relationships_detail'] and
                var_name in index['package_relationships_detail'][object_name.lower()]['source_name'] and
                method['name'].startswith('get_') and
                method['name'].endswith('_id')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='relationship.Relationship.get_source_id',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get the osid.id.Id of a persisted object that
        # appears to be an initialized relationship destination.
        # uses same pattern as for sources (above)
        elif (object_name in index['package_relationships_caps'] and
                object_name.lower() in index['package_relationships_detail'] and
                var_name in index['package_relationships_detail'][object_name.lower()]['destination_name'] and
                method['name'].startswith('get_') and
                method['name'].endswith('_id')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='relationship.Relationship.get_source_id',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get the osid.id.Id of a persisted and
        # required object from this osid package.
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('get_') and
                method['name'].endswith('_id') and
                var_name in index['package_objects_under'] and
                index[object_name + '.persisted_data'][var_name] == 'osid.id.Id'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='learning.Activity.get_objective_id',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get the osid.id.Id of an instance object that may
        # be required and and is from this osid package. NOTE: Patterned as above
        elif (var_name in index[object_name + '.instance_data'] and
                method['name'].startswith('get_') and
                method['name'].endswith('_id') and
                var_name in index['package_objects_under'] and
                index[object_name + '.instance_data'][var_name] == 'osid.id.Id'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='learning.Activity.get_objective_id',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get the osid.id.Id of a persisted but not
        # required object from another osid package.
        # PERHAPS ADD A BINDER HELPER FOR PAST-TENSE for 'is' conditions????
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('get_') and
                method['name'].endswith('_id') and
                ('has_' + var_name in interface['method_names'] or
                 'is_' + var_name + 'd' in interface['method_names']) and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] == 'osid.id.Id'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObject.get_id_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get the osid.id.Id of an object from
        # another osid package.  NOTE that at this time these are patterned as above
        elif (var_name in index[object_name + '.instance_data'] and
                method['name'].startswith('get_') and
                method['name'].endswith('_id') and
                ('has_' + var_name in interface['method_names'] or
                 'is_' + var_name + 'd' in interface['method_names']) and
                index[object_name + '.instance_data'][var_name] == 'osid.id.Id'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObject.get_id_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # THIS ONE SHOULD NEVER GET CALLED.  SHOULD BE CAUGHT IN THE RELATIONSHIP ONES ABOVE
        # Object methods that get the osid.id.Id of a persisted object that
        # appears to be an initialized data element like a relationship source
        # or destination.
        elif (var_name in index[object_name + '.initialized_data'] and
                method['name'].startswith('get_') and
                method['name'].endswith('_id')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='relationship.Relationship.get_source_id',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get an aggregated object from this package.
        # Note that this is for a plural form method:
        elif (object_name + '.aggregate_data' in index and
                var_name in index[object_name + '.aggregate_data'] and
                method['name'].startswith('get_') and
                remove_plural(var_name) in index['package_objects_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='repository.Asset.get_asset_contents',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=remove_plural(var_name),
                            object_name=object_name,
                            aggregated_object_name=index['package_objects_under_to_caps'][remove_plural(var_name)],
                            return_type_full=method['return_type']))

        # Object methods that get the a persisted but not required object
        # from this package for which an osid.id.Id is persisted.  This
        # investigates whether a 'has_thing' method also exists.
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('get_') and
                'has_' + var_name in interface['method_names'] and
                var_name in index['package_objects_under'] and
                method['name'] + '_id' in interface['method_names']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='calendar.Schedule.get_time_period',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get the an instance but not required object
        # from this package for which an osid.id.Id is persisted.  This
        # investigates whether a 'has_thing' method also exists.
        # NOTE for now this is patterned as above
        elif (var_name in index[object_name + '.instance_data'] and
                method['name'].startswith('get_') and
                ('has_' + var_name in interface['method_names'] or
                 'is_' + var_name + 'd' in interface['method_names']) and
                var_name in index['package_objects_under'] and
                method['name'] + '_id' in interface['method_names']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='calendar.Schedule.get_time_period',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get the a persisted and required object
        # from this package for which an osid.id.Id is persisted.
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('get_') and
                var_name in index['package_objects_under'] and
                method['name'] + '_id' in interface['method_names']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='learning.Activity.get_objective',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type'],
                            return_cat_name=get_cat_name_for_pkg(method['return_type'].split('.')[1]),
                            cat_name=index['package_catalog_caps']))

        # Object methods that get the an instance and perhaps required object
        # from this package for which an osid.id.Id is persisted.
        # NOTE this is currently patterned as above
        elif (var_name in index[object_name + '.instance_data'] and
                method['name'].startswith('get_') and
                var_name in index['package_objects_under'] and
                method['name'] + '_id' in interface['method_names']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='learning.Activity.get_objective',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type'],
                            return_cat_name=get_cat_name_for_pkg(method['return_type'].split('.')[1]),
                            cat_name=index['package_catalog_caps']))

        # We might need one that checks for persisted and not required object,
        # That looks for related has_ and is_ type methods

        # Object methods that get the a persisted object id from another
        # package for which an osid.id.Id is persisted.  This doesn't check
        # for a "has" method, but is currently patterned like it does
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('get_') and
                method['name'].endswith('_id') and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] == 'osid.id.Id'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObject.get_id_attribute',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Object methods that get the a persisted object from another
        # package for which an osid.id.Id is persisted .
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('get_') and
                len(index[object_name + '.arg_detail'][var_name]) == 1 and
                index[object_name + '.arg_detail'][var_name][0]['arg_type'] == 'osid.id.Id'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObject.get_id_attribute_object',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type'],
                            return_cat_name=get_cat_name_for_pkg(method['return_type'].split('.')[1])))

        # We might need one that checks for instance and not required object,
        # That looks for related has_ and is_ type methods

        # Object methods that get an instance object from another
        # package for which an osid.id.Id is persisted .
        # NOTE that currently this is patterned as above
        elif (var_name in index[object_name + '.instance_data'] and
                method['name'].startswith('get_') and
                index[object_name + '.instance_data'][var_name] == 'osid.id.Id'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObject.get_id_attribute_object',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type'],
                            return_cat_name=get_cat_name_for_pkg(method['return_type'].split('.')[1])))

        # Object methods that get a persisted object list from another
        # package for which an osid.id.IdList is persisted .
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('get_') and
                index[object_name + '.persisted_data'][var_name] == 'osid.id.Id[]'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='learning.Activity.get_assets',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            return_type_full=method['return_type'],
                            return_cat_name=get_cat_name_for_pkg(method['return_type'].split('.')[1])))

        # Object methods that get an extension record.
        elif (method['name'].startswith('get_') and
                method['name'].endswith('_record')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObject.get_object_record',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type'],
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type']))

        else:
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name']))
    return index


def is_catalog(index, object_name):
    return index['package_catalog_under'] == camel_to_under(object_name)


def is_catalog_node(index, object_name):
    return index['package_catalog_under'] + '_node' == camel_to_under(object_name)


def map_list_patterns(interface, package, index):
    object_name = interface['shortname'][:-4]
    if is_catalog(index, object_name):
        # then this is a catalog, not an object!
        index[interface['shortname'] + '.init_pattern'] = 'resource.BinList'
    elif is_catalog_node(index, object_name):
        # then this is a catalog node, so part of a hierarchy
        index[interface['shortname'] + '.init_pattern'] = 'resource.BinNodeList'
    else:
        index[interface['shortname'] + '.init_pattern'] = 'osid_object.GenericObjectList'

    for method in interface['methods']:
        var_name = method['name'].split('_', 2)[-1]
        # List methods that get next item in a list.
        if (method['name'].startswith('get_next') and
                method['arg_types'] == []):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObjectList.get_next_resource',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            return_type_full=method['return_type']))

        # List methods that get next item in a list.
        elif (method['name'].startswith('get_next') and
                method['arg_types'][0] == 'cardinal'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObjectList.get_next_resources',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
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


def map_catalog_patterns(interface, package, index):

    object_name = interface['shortname']
    index[object_name + '.init_pattern'] = 'resource.Bin'
    index[object_name + 'Form.init_pattern'] = 'resource.BinForm'
    return index


def map_query_patterns(interface, package, index):

    object_name = interface['shortname'][:-5]
    index[interface['shortname'] + '.init_pattern'] = 'osid_object.GenericObjectQuery'

    for method in interface['methods']:
        var_name = method['name'].split('_', 1)[-1]

        # Query methods that clear catalog id terms
        if (method['name'].endswith('_terms') and
                var_name[:-6] == index['package_catalog_under'] + '_id' and
                method['name'].startswith('clear_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObjectQuery.clear_bin_id_terms',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name[:-6],
                            object_name=object_name,
                            cat_name=index['package_catalog_caps']))

        # Query methods that clear catalog id terms
        elif (method['name'].endswith('_id_terms') and
                method['name'].startswith('clear_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObjectQuery.clear_avatar_id_terms',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name[:-6],
                            object_name=object_name,
                            cat_name=index['package_catalog_caps']))

        # Query methods that clear all terms (do we need one for each element type?)
        elif (method['name'].endswith('_terms') and
                var_name[:-6] in index[object_name + '.persisted_data'] and
                method['name'].startswith('clear_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObjectQuery.clear_group_terms',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name[:-6],
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Query methods that query on a DateTime range - DOES THIS WORK??
        elif (var_name in index[object_name + '.persisted_data'] and
                method['name'].startswith('match_') and
                index[object_name + '.persisted_data'][var_name] in ['osid.calendaring.DateTime', 'timestamp'] and
                len(method['args']) == 3):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='assessment.AssessmentOfferedQuery.match_start_time',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type'],
                            arg1_name=method['args'][1]['var_name'],
                            arg1_type_full=method['args'][1]['arg_type'],
                            arg2_name=method['args'][2]['var_name'],
                            arg2_type_full=method['args'][2]['arg_type'],
                            object_name=object_name,
                            return_type_full=method['return_type']))

        # Query methods that match a catalog Id
        elif (method['name'] == 'match_' + index['package_catalog_under'] + '_id' and
                len(method['args']) == 2):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObjectQuery.match_bin_id',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type'],
                            arg1_name=method['args'][1]['var_name'],
                            arg1_type_full=method['args'][1]['arg_type'],
                            cat_name=index['package_catalog_caps'],
                            object_name=object_name))

        # Query methods that match an object Id
        elif (method['name'].startswith('match_') and
                method['name'].endswith('_id') and
                len(method['args']) == 2):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObjectQuery.match_avatar_id',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type'],
                            arg1_name=method['args'][1]['var_name'],
                            arg1_type_full=method['args'][1]['arg_type'],
                            cat_name=index['package_catalog_caps'],
                            object_name=object_name))

        else:
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name']))
    return index


def map_search_patterns(interface, package, index):

    object_name = interface['shortname'][:-6]
    index[interface['shortname'] + '.init_pattern'] = 'osid_object.GenericObjectSearch'

    for method in interface['methods']:
        var_name = method['name'].split('_', 1)[-1]

        # Search methods that search among ids
        if (method['name'].startswith('search_among')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObjectSearch.search_among_resources',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name[5:],
                            object_name=object_name,
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type'],
                            cat_name=index['package_catalog_caps']))

        # Search methods that order search results
        elif (method['name'].startswith('order_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObjectSearch.order_resource_results',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type'],
                            cat_name=index['package_catalog_caps']))

        else:
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name']))
    return index


def map_search_results_patterns(interface, package, index):

    object_name = interface['shortname'][:-13]
    index[interface['shortname'] + '.init_pattern'] = 'osid_object.GenericObjectSearchResults'

    for method in interface['methods']:
        var_name = method['name'].split('_', 1)[-1]

        # SearchResults methods that search among ids
        if (method['name'].startswith('get_') and
                not method['name'].endswith('_record') and
                'query_inspector' not in method['name']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObjectSearchResults.get_resources',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            cat_name=index['package_catalog_caps'],
                            return_type_full=method['return_type']))

        # SearchResults methods that get a query inspector
        elif (method['name'].startswith('get_') and
              'query_inspector' in method['name']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObjectSearchResults.get_resource_query_inspector',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            cat_name=index['package_catalog_caps'],
                            return_type_full=method['return_type']))

        else:
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name']))
    return index


def map_catalog_query_patterns(interface, package, index):

    object_name = interface['shortname'][:-5]
    index[interface['shortname'] + '.init_pattern'] = 'resource.BinQuery'

    for method in interface['methods']:
        var_name = method['name'].split('_', 1)[-1]

        # Query methods that clear all terms (do we need one for each element type?)
        if (method['name'].endswith('_terms') and
                method['name'].startswith('clear_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='resource.BinQuery.clear_group_terms',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name[:-6],
                            object_name=object_name,
                            return_type_full=method['return_type']))

        else:
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name']))
    return index


def map_catalog_node_patterns(interface, package, index):

    object_name = interface['shortname'][:-4]
    index[interface['shortname'] + '.init_pattern'] = 'resource.BinNode'

    for method in interface['methods']:
        var_name = method['name'].split('_', 1)[-1]

        # Object Node methods that get the parent object Nodes
        if (method['name'].startswith('get_parent_') and
                method['name'].endswith('_nodes')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='resource.BinNode.get_parent_bin_nodes',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=index['package_catalog_caps'],
                            cat_name=index['package_catalog_caps'],
                            return_type_full=method['return_type']))

        # Object Node methods that get the child object Nodes
        elif (method['name'].startswith('get_child_') and
                method['name'].endswith('_nodes')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='resource.BinNode.get_child_bin_nodes',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=index['package_catalog_caps'],
                            cat_name=index['package_catalog_caps'],
                            return_type_full=method['return_type']))

        # Object Node methods that get the object at this Node
        elif method['name'].startswith('get_'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='resource.BinNode.get_bin',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=index['package_catalog_caps'],
                            cat_name=index['package_catalog_caps'],
                            return_type_full=method['return_type']))

        else:
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name']))
    return index


def map_receiver_patterns(interface, package, index):

    object_name = interface['shortname'][:-len('Receiver')]
    index[interface['shortname'] + '.init_pattern'] = 'osid_object.GenericObjectReceiver'

    for method in interface['methods']:
        var_name = method['name'].split('_', 1)[-1]

        # Receiver methods that callback for new objects
        # NOTE: This includes a hack to the arguments. Needs to be fixed
        # When upgrading to RC6
        if method['name'].startswith('new_'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObjectReceiver.new_resources',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            cat_name=index['package_catalog_caps'],
                            arg0_name='notification_id',
                            arg0_type_full='osid.id.Id',
                            arg1_name=method['args'][0]['var_name'],
                            arg1_type_full=method['args'][0]['arg_type']))

        # Receiver methods that callback for new objects
        # NOTE: This includes a hack to the arguments. Needs to be fixed
        # When upgrading to RC6
        elif method['name'].startswith('changed_'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObjectReceiver.changed_resources',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            cat_name=index['package_catalog_caps'],
                            arg0_name='notification_id',
                            arg0_type_full='osid.id.Id',
                            arg1_name=method['args'][0]['var_name'],
                            arg1_type_full=method['args'][0]['arg_type']))

        # Receiver methods that callback for new objects
        # NOTE: This includes a hack to the arguments. Needs to be fixed
        # When upgrading to RC6
        elif method['name'].startswith('deleted_'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_object.GenericObjectReceiver.deleted_resources',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=var_name,
                            object_name=object_name,
                            cat_name=index['package_catalog_caps'],
                            arg0_name='notification_id',
                            arg0_type_full='osid.id.Id',
                            arg1_name=method['args'][0]['var_name'],
                            arg1_type_full=method['args'][0]['arg_type']))

        else:
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name']))
    return index
