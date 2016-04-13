from collections import OrderedDict
from binder_helpers import camel_to_under
from pattern_mappers.managers import map_manager_patterns
from pattern_mappers.sessions import map_session_patterns
from pattern_mappers.core import map_osid_patterns, map_type_patterns, map_id_patterns
from pattern_mappers.data import map_object_form_data_patterns, map_object_data_patterns, map_admin_session_data_patterns
from pattern_mappers.objects import map_object_form_patterns,\
    map_object_patterns, map_list_patterns, map_receiver_patterns,\
    map_query_patterns, map_catalog_patterns,\
    map_catalog_query_patterns, map_catalog_node_patterns


def append_caps(value, caps_list):
    if not value in caps_list:
        caps_list.append(value)

def append_under(value, under_list):
    if not camel_to_under(value) in under_list:
        under_list.append(camel_to_under(value))

def idify(value):
    return value + '_id'

def is_id_version_of(method_1, method_2):
    return method_1['name'] == idify(method_2['name'])

def map_under_to_camel(camel_value, under_to_camel_map):
    under_to_camel_map[camel_to_under(camel_value)] = camel_value

def update_admin_data_sessions_in_index(package, index):
    for interface in package['interfaces']:
        # Now, Look at data patterns that are indicated in AdminSessions
        if interface['shortname'].endswith('AdminSession'):
            map_admin_session_data_patterns(interface, package, index)

def update_object_data_patterns_in_index(package, index):
    osid_objects = ['OsidObject', 'OsidRule', 'OsidRelationship',
                    'OsidGovernator', 'OsidEnabler']
    for interface in package['interfaces']:
        # Now, compare the results of the ObjectForm investigation with the
        # data-like patterns for the OsidObjects, and record what falls out.
        # NOTE THAT OsidRule IS HERE AS WELL. MAY NEED TO BE SPLIT OUT
        if any(oo in interface['inherit_shortnames'] for oo in osid_objects):
            map_object_data_patterns(interface, package, index)

def update_object_form_patterns_in_index(package, index):
    object_forms = ['OsidObjectForm', 'OsidRuleForm', 'OsidRelationshipForm',
                    'OsidGovernatorForm', 'OsidEnablerForm']
    for interface in package['interfaces']:
        # Investigate only the ObjectForms for data patterns. We can assume that
        # all the data they deal with will want to be persisted.
        # NOTE THAT OsidRuleForm IS HERE AS WELL. MAY NEED TO BE SPLIT OUT
        if any(of in interface['inherit_shortnames'] for of in object_forms):
            map_object_form_data_patterns(interface, package, index)

def update_relationships_detail(relationships, interface,
                                source=None, dest=None,
                                source_unknown=False, dest_unknown=False):
    if source is None and dest is None:
        relationships[camel_to_under(interface['shortname'])] = {
            'source_name': 'source',
            'source_type': 'osid.id.Id',
            'destination_name': 'destination',
            'destination_type': 'osid.id.Id'
        }
    else:
        if not source_unknown and not dest_unknown:
            relationships[camel_to_under(interface['shortname'])] = {
                'source_name': source['name'][4:],
                'source_type': source['return_type'],
                'destination_name': dest['name'][4:],
                'destination_type': dest['return_type']
            }
        elif not source_unknown and dest_unknown:
            relationships[camel_to_under(interface['shortname'])] = {
                'source_name': source['name'][4:],
                'source_type': source['return_type'],
                'destination_name': dest['name'][4:-3],
                'destination_type': 'UNKNOWN'
            }
        elif source_unknown and not dest_unknown:
            relationships[camel_to_under(interface['shortname'])] = {
                'source_name': source['name'][4:-3],
                'source_type': 'UNKNOWN',
                'destination_name': dest['name'][4:],
                'destination_type': dest['return_type']
            }
        else:
            relationships[camel_to_under(interface['shortname'])] = {
                'source_name': 'UNKNOWN',
                'source_type': 'UNKNOWN',
                'destination_name': 'UNKNOWN',
                'destination_type': 'UNKNOWN'
            }


def map_patterns(package, index, base_package=None):
    if base_package is None:
        catalog_name_caps = 'NoCatalog'
        catalog_name_under = 'no_catalog'
        object_namespace_table = OrderedDict()
        object_names_caps = []
        object_names_under = []
        containable_object_names_caps = []
        containable_object_names_under = []
        cataloged_object_names_caps = []
        cataloged_object_names_under = []
        object_names_under_to_caps = OrderedDict()
        relationship_names_caps = []
        relationship_names_under = []
        rule_names_caps = []
        rule_names_under = []
        relationships_detail = {}
    else:
        catalog_name_caps = base_package['package_catalog_caps']
        catalog_name_under = base_package['package_catalog_under']
        object_namespace_table = base_package['package_object_namespace_table']
        object_names_caps = base_package['package_objects_caps']
        object_names_under = base_package['package_objects_under']
        containable_object_names_caps = base_package['package_containable_objects_caps']
        containable_object_names_under = base_package['package_containable_objects_under']
        cataloged_object_names_caps = base_package['package_cataloged_objects_caps']
        cataloged_object_names_under = base_package['package_cataloged_objects_under']
        object_names_under_to_caps = base_package['package_objects_under_to_caps']
        relationship_names_caps = base_package['package_relationships_caps']
        relationship_names_under = base_package['package_relationships_under']
        rule_names_caps = base_package['package_rules_caps']
        rule_names_under = base_package['package_rules_under']
        relationships_detail = base_package['package_relationships_detail']

    index['impl_log'] = OrderedDict()
    index['impl_log']['managers'] = OrderedDict()
    index['impl_log']['sessions'] = OrderedDict()

    for interface in package['interfaces']:
        if 'Containable' in interface['inherit_shortnames']:
            append_caps(interface['shortname'], containable_object_names_caps)
            append_under(interface['shortname'], containable_object_names_under)
        # Find all OsidObject names in this package
        if interface['category'] == 'objects':
            object_namespace_table[interface['shortname']] = interface['fullname'][5:]
            if 'OsidObject' in interface['inherit_shortnames']:
                append_caps(interface['shortname'], object_names_caps)
                append_under(interface['shortname'], object_names_under)
                map_under_to_camel(interface['shortname'], object_names_under_to_caps)
            # Find OsidRelationship names in this package
            elif 'OsidRelationship' in interface['inherit_shortnames']:
                append_caps(interface['shortname'], relationship_names_caps)
                append_under(interface['shortname'], relationship_names_under)
                map_under_to_camel(interface['shortname'], object_names_under_to_caps)

                if not camel_to_under(interface['shortname']) in relationships_detail:
                    update_relationships_detail(relationships_detail,
                                                interface,
                                                source_unknown=True,
                                                dest_unknown=True)
                print 'found relationship: ', interface['fullname']
                if interface['shortname'] == 'Relationship':
                    update_relationships_detail(relationships_detail,
                                                interface)
                elif len(interface['methods']) >= 4:
                    first_method = interface['methods'][0]
                    second_method = interface['methods'][1]
                    third_method = interface['methods'][2]
                    fourth_method = interface['methods'][3]
                    if (is_id_version_of(first_method, second_method) and
                            is_id_version_of(third_method, fourth_method)):
                        update_relationships_detail(relationships_detail,
                                                    interface,
                                                    source=second_method,
                                                    dest=fourth_method)
                        print '    2 args source =', second_method['name'][4:], 'dest =', fourth_method['name'][4:]
                    elif (is_id_version_of(first_method, second_method) and
                            third_method['name'].endswith('_id')):
                        update_relationships_detail(relationships_detail,
                                                    interface,
                                                    source=second_method,
                                                    dest=third_method,
                                                    dest_unknown=True)
                        print '    1 arg source =', second_method['name'][4:], 'dest =', third_method['name'][4:-3]
                    elif (first_method['name'].endswith('_id') and
                            is_id_version_of(second_method, third_method)):
                        update_relationships_detail(relationships_detail,
                                                    interface,
                                                    source=first_method,
                                                    dest=third_method,
                                                    source_unknown=True)
                        print '    1 arg source =', first_method['name'][4:-3], 'dest =', third_method['name'][4:]
                    else:
                        print '    source and destination not found'
                else:
                    print '    source and destination not found. less than 4 methods'
            # Find OsidRule names in this package AND ADD THEM TO OBJECTS AS WELL, FOR NOW
            elif 'OsidRule' in interface['inherit_shortnames']:
                append_caps(interface['shortname'], rule_names_caps)
                append_under(interface['shortname'], rule_names_under)

                # AND ADD THEM TO OBJECTS AS WELL, FOR NOW:
                append_caps(interface['shortname'], object_names_caps)
                append_under(interface['shortname'], object_names_under)
                map_under_to_camel(interface['shortname'], object_names_under_to_caps)

            # Find OsidCatalog name (should be only one) in this package
            elif 'OsidCatalog' in interface['inherit_shortnames']:
                if not interface['shortname'] == catalog_name_caps:
                    catalog_name_caps = interface['shortname']
                if not camel_to_under(interface['shortname']) == catalog_name_under:
                    catalog_name_under = camel_to_under(interface['shortname'])

        # Run through again to find all catalog managed OsidObject names in this package.
        if (interface['category'] == 'sessions' and
                interface['shortname'].endswith('LookupSession') and
                interface['shortname'][:-13] != catalog_name_caps):
            append_caps(interface['shortname'][:-13], cataloged_object_names_caps)
            append_under(interface['shortname'][:-13], cataloged_object_names_under)

    # Now that we have the index, we can map things
    index['package_object_namespace_table'] = object_namespace_table
    index['package_objects_caps'] = object_names_caps
    index['package_objects_under'] = object_names_under
    index['package_containable_objects_caps'] = containable_object_names_caps
    index['package_containable_objects_under'] = containable_object_names_under
    index['package_cataloged_objects_caps'] = cataloged_object_names_caps
    index['package_cataloged_objects_under'] = cataloged_object_names_under
    index['package_objects_under_to_caps'] = object_names_under_to_caps
    index['package_relationships_caps'] = relationship_names_caps
    index['package_relationships_under'] = relationship_names_under
    index['package_rules_caps'] = rule_names_caps
    index['package_rules_under'] = rule_names_under
    index['package_catalog_caps'] = catalog_name_caps
    index['package_catalog_under'] = catalog_name_under
    index['package_relationships_detail'] = relationships_detail

    package_mapper_map = {
        'osid': map_osid_patterns,
        'type': map_type_patterns,
        'id': map_id_patterns
    }

    interface_category_map = {
        'managers': map_manager_patterns,
        'sessions': map_session_patterns,
    }

    update_object_form_patterns_in_index(package, index)
    update_object_data_patterns_in_index(package, index)
    update_admin_data_sessions_in_index(package, index)

    for interface in package['interfaces']:
        if package['name'] in package_mapper_map.keys():
            package_mapper_map[package['name']](interface, package, index)
        elif interface['category'] in interface_category_map.keys():
            cat = interface['category']
            sn = interface['shortname']
            index['impl_log'][cat][sn] = dict()
            interface_category_map[cat](interface, package, index)
        # THIS ONE MAY NEED TO BE SPLIT UP, BUT WE'LL TRY IT FOR NOW:
        elif ('OsidObjectForm' in interface['inherit_shortnames'] or
              'OsidRelationshipForm' in interface['inherit_shortnames']):
            map_object_form_patterns(interface, package, index)
        # THIS ONE MAY ALSO NEED TO BE SPLIT UP, BUT WE'LL TRY IT FOR NOW:
        elif ('OsidObject' in interface['inherit_shortnames'] or
              'OsidRule' in interface['inherit_shortnames'] or
              'OsidRelationship' in interface['inherit_shortnames']):
            map_object_patterns(interface, package, index)
        elif any(q in interface['inherit_shortnames']
                 for q in ['OsidObjectQuery', 'OsidRelationshipQuery']):
            map_query_patterns(interface, package, index)
        elif 'OsidList' in interface['inherit_shortnames']:
            map_list_patterns(interface, package, index)
        elif 'OsidReceiver' in interface['inherit_shortnames']:
            map_receiver_patterns(interface, package, index)
        elif 'OsidCatalog' in interface['inherit_shortnames']:
            map_catalog_patterns(interface, package, index)
        elif 'OsidCatalogQuery' in interface['inherit_shortnames']:
            map_catalog_query_patterns(interface, package, index)
        elif ('OsidNode' in interface['inherit_shortnames'] and 
                interface['shortname'][:-4] == index['package_catalog_caps']):
            map_catalog_node_patterns(interface, package, index)

    return index
