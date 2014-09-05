import string
from collections import OrderedDict
from binder_helpers import camel_to_under
from binder_helpers import get_interface_module
from binder_helpers import make_plural
from binder_helpers import remove_plural
from binder_helpers import get_pkg_name
from osid_meta import OSID_Language_Primitives
from pattern_mappers.managers import map_manager_patterns
from pattern_mappers.sessions import map_session_patterns
from pattern_mappers.core import map_osid_patterns, map_type_patterns, map_id_patterns
from pattern_mappers.data import map_object_form_data_patterns, map_object_data_patterns, map_admin_session_data_patterns
from pattern_mappers.objects import map_object_form_patterns, map_object_patterns, map_list_patterns, map_catalog_patterns

def map_patterns(package, index, base_package=None):

    if base_package is None:
        catalog_name_caps = 'NoCatalog'
        catalog_name_under = 'no_catalog'
        object_names_caps = []
        object_names_under = []
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
        object_names_caps = base_package['package_objects_caps']
        object_names_under = base_package['package_objects_under']
        cataloged_object_names_caps = base_package['package_cataloged_objects_caps']
        cataloged_object_names_under = base_package['package_cataloged_objects_under']
        object_names_under_to_caps = base_package['package_objects_under_to_caps']
        relationship_names_caps = base_package['package_relationships_caps']
        relationship_names_under = base_package['package_relationships_under']
        rule_names_caps = base_package['package_rules_caps']
        rule_names_under = base_package['package_rules_under']
        relationships_detail = base_package['package_relationships_detail']

    for interface in package['interfaces']:
        ##
        # Find all OsidObject names in this package
        if (interface['category'] == 'objects' and
            'OsidObject' in interface['inherit_shortnames']):
            if not interface['shortname'] in object_names_caps:
                object_names_caps.append(interface['shortname'])
            if not camel_to_under(interface['shortname']) in object_names_under:
                object_names_under.append(camel_to_under(interface['shortname']))
            object_names_under_to_caps[camel_to_under(interface['shortname'])] = interface['shortname']
        ##
        # Find OsidRelationship names in this package
        if (interface['category'] == 'objects' and
            'OsidRelationship' in interface['inherit_shortnames']):
            if not interface['shortname'] in relationship_names_caps:
                relationship_names_caps.append(interface['shortname'])
            if not camel_to_under(interface['shortname']) in relationship_names_under:
                relationship_names_under.append(camel_to_under(interface['shortname']))
            object_names_under_to_caps[camel_to_under(interface['shortname'])] = interface['shortname']
            if not camel_to_under(interface['shortname']) in relationships_detail:
                relationships_detail[camel_to_under(interface['shortname'])] = {
                    'source_name': 'UNKNOWN',
                    'source_type': 'UNKNOWN',
                    'destination_name': 'UNKNOWN',
                    'destination_type': 'UNKNOWN'
                }
            #print 'found relationship:', interface['fullname']
            if len(interface['methods']) >= 4:
                first_method = interface['methods'][0]
                second_method = interface['methods'][1]
                third_method = interface['methods'][2]
                fourth_method = interface['methods'][3]
                if (first_method['name'] == second_method['name'] + '_id' and
                    third_method['name'] == fourth_method['name'] + '_id'):
                    relationships_detail[camel_to_under(interface['shortname'])] = {
                    'source_name': second_method['name'][4:],
                    'source_type': second_method['return_type'],
                    'destination_name': fourth_method['name'][4:],
                    'destination_type': fourth_method['return_type']                        
                    }
                    #print '    source =', second_method['name'][4:], 'dest =', fourth_method['name'][4:]
                else:
                    #print '    source and destination not found'
                    pass
            else:
                #print '    source and destination not found. less than 4 methods'
                pass
        ##
        # Find OsidRule names in this package AND ADD THEM TO OBJECTS AS WELL, FOR NOW
        if (interface['category'] == 'objects' and
            'OsidRule' in interface['inherit_shortnames']):
            if not interface['shortname'] in rule_names_caps:
                rule_names_caps.append(interface['shortname'])
            if not camel_to_under(interface['shortname']) in rule_names_under:
                rule_names_under.append(camel_to_under(interface['shortname']))
            # AND ADD THEM TO OBJECTS AS WELL, FOR NOW:
            if not interface['shortname'] in object_names_caps:
                object_names_caps.append(interface['shortname'])
            if not camel_to_under(interface['shortname']) in object_names_under:
                object_names_under.append(camel_to_under(interface['shortname']))
            object_names_under_to_caps[camel_to_under(interface['shortname'])] = interface['shortname']


        ##
        # Find OsidCatalog name (should be only one) in this package
        if (interface['category'] == 'objects' and
            'OsidCatalog' in interface['inherit_shortnames']):
            if not interface['shortname'] == catalog_name_caps:
                catalog_name_caps = interface['shortname']
            if not camel_to_under(interface['shortname']) == catalog_name_under:
                catalog_name_under = camel_to_under(interface['shortname'])

    for interface in package['interfaces']:    
        ##
        # Run through again to find all catalog managed OsidObject names in this package.
        if (interface['category'] == 'sessions' and
            interface['shortname'].endswith('LookupSession') and
            interface['shortname'][:-13] != catalog_name_caps):
            if not interface['shortname'][:-13] in cataloged_object_names_caps:
                cataloged_object_names_caps.append(interface['shortname'][:-13])
            if not camel_to_under(interface['shortname'][:-13]) in cataloged_object_names_under:
                cataloged_object_names_under.append(camel_to_under(interface['shortname'][:-13]))

    index['impl_log'] = OrderedDict()
    index['package_objects_caps'] = object_names_caps
    index['package_objects_under'] = object_names_under
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
                
    for interface in package['interfaces']:
        ##
        # Investigate only the ObjectForms for data patterns. We can assume that
        # all the data they deal with will want to be persisted.
        # NOTE THAT OsidRuleForm IS HERE AS WELL. MAY NEED TO BE SPLIT OUT
        if ('OsidObjectForm' in interface['inherit_shortnames'] or
            'OsidRuleForm' in interface['inherit_shortnames'] or
            'OsidRelationshipForm' in interface['inherit_shortnames'] or
            'OsidGovernatorForm' in interface['inherit_shortnames'] or
            'OsidEnablerForm' in interface['inherit_shortnames']):
            map_object_form_data_patterns(interface, package, index)

    for interface in package['interfaces']:
        ##
        # Now, compare the results of the ObjectForm investigation with the 
        # data-like patterns for the OsidObjects, and record what falls out.
        # NOTE THAT OsidRule IS HERE AS WELL. MAY NEED TO BE SPLIT OUT
        if ('OsidObject' in interface['inherit_shortnames'] or
            'OsidRule' in interface['inherit_shortnames'] or
            'OsidRelationship' in interface['inherit_shortnames'] or
            'OsidGovernator' in interface['inherit_shortnames'] or
            'OsidEnabler' in interface['inherit_shortnames']):
            map_object_data_patterns(interface, package, index)

    for interface in package['interfaces']:
        ##
        # Now, Look at data patterns that are indicated in AdminSessions
        if (interface['shortname'].endswith('AdminSession')):
            map_admin_session_data_patterns(interface, package, index)
        

    ## Uncomment the following lines to list package catalogs, relationships, etc.
#    print package['name']
#    print '    catalog -', catalog_name_caps, catalog_name_under
#    print '    relationships -', ', '.join(relationship_names_caps)
#    print '    objects -', ', '.join(object_names_caps)
#    print '    rules -', ', '.join(rule_names_caps)

    index['impl_log']['managers'] = OrderedDict()
    index['impl_log']['sessions'] = OrderedDict()

    for interface in package['interfaces']:
        if package['name'] == 'osid':
            map_osid_patterns(interface, package, index)
        elif package['name'] == 'type':
            map_type_patterns(interface, package, index)
        elif package['name'] == 'id':
            map_id_patterns(interface, package, index)
        elif interface['category'] == 'managers':
            index['impl_log']['managers'][interface['shortname']] = dict()
            map_manager_patterns(interface, package, index)
        elif interface['category'] == 'sessions':
            index['impl_log']['sessions'][interface['shortname']] = dict()
            map_session_patterns(interface, package, index)
        # THIS ONE MAY NEED TO BE SPLIT UP, BUT WE'LL TRY IT FOR NOW:
        elif ('OsidObjectForm' in interface['inherit_shortnames'] or
              'OsidRelationshipForm' in interface['inherit_shortnames']):
            map_object_form_patterns(interface, package, index)
        # THIS ONE MAY ALSO NEED TO BE SPLIT UP, BUT WE'LL TRY IT FOR NOW:
        elif ('OsidObject' in interface['inherit_shortnames'] or
              'OsidRule' in interface['inherit_shortnames'] or
              'OsidRelationship' in interface['inherit_shortnames']):
            map_object_patterns(interface, package, index)
        elif 'OsidList' in interface['inherit_shortnames']:
            map_list_patterns(interface, package, index)
        elif 'OsidCatalog' in interface['inherit_shortnames']:
            map_catalog_patterns(interface, package, index)

    return index
