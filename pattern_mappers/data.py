from collections import OrderedDict
from binder_helpers import make_plural, remove_plural

##
# Investigate all the setter-like methods in each form interface to find
# all the easily identifiable persisted data elements.
def map_object_form_data_patterns(interface, package, index):

    index[interface['shortname'][:-4] + '.arg_detail'] = OrderedDict()
    index[interface['shortname'][:-4] + '.persisted_data'] = OrderedDict()
    index[interface['shortname'][:-4] + '.initialized_data'] = OrderedDict() # This may be used elsewhere
    index[interface['shortname'][:-4] + '.persisted_data'][index['package_catalog_under']] = 'OsidCatalog'
    index[interface['shortname'][:-4] + '.initialized_data'][index['package_catalog_under']] = 'OsidCatalog'

    """
    ##
    # Here is where we look (by hand) for some initialized data that we can't 
    # seem to find elsewhere
    if interface['shortname'] == 'RelationshipForm':
        index[interface['shortname'][:-4] + '.persisted_data']['source'] = 'osid.id.Id'
        index[interface['shortname'][:-4] + '.initialized_data']['source'] = 'osid.id.Id'
        index[interface['shortname'][:-4] + '.persisted_data']['destination'] = 'osid.id.Id'
        index[interface['shortname'][:-4] + '.initialized_data']['destination'] = 'osid.id.Id'
        ## This could be sketchy:
        index[interface['shortname'][:-4] + '.arg_detail']['source'] = []
        index[interface['shortname'][:-4] + '.arg_detail']['destination'] = []"""

    for method in interface['methods']:

        ##
        # Get all data elements that have setter methods in an ObjectForm
        # and take one and only one arguement to be persisted
        if (method['name'].startswith('set_') and
            len(method['args']) == 1):
            index[interface['shortname'][:-4] + '.arg_detail'][method['name'].split('_', 1)[1]] = method['args']

            if ('Proficiency' in interface['shortname'] and
                    'level' in method['name'] and
                    'osid.grading.Grade' == method['args'][0]['arg_type']):
                # to fix error in OSID spec
                index[interface['shortname'][:-4] + '.persisted_data'][method['name'].split('_', 1)[1]] = 'osid.id.Id'
            else:
                index[interface['shortname'][:-4] + '.persisted_data'][method['name'].split('_', 1)[1]] = method['args'][0]['arg_type']

        ##
        # Get all data elements that have adder methods in an ObjectForm
        # and take one and only one arguement to be persisted
        if (method['name'].startswith('add_') and
            len(method['args']) == 1):
            index[interface['shortname'][:-4] + '.arg_detail'][method['name'].split('_', 1)[1]] = method['args']
            index[interface['shortname'][:-4] + '.persisted_data'][method['name'].split('_', 1)[1]] = method['args'][0]['arg_type']

        ##
        # Create a data element specifically for repository.Composition compositions
        if (interface['shortname'] == 'CompositionForm' and method['name'] == 'get_composition_form_record'):
            index[interface['shortname'][:-4] + '.arg_detail']['children'] = {
                "var_name": "children_ids", 
                "array": True, 
                "arg_type": "osid.id.Id[]"
             }
            index[interface['shortname'][:-4] + '.persisted_data']['children'] = 'osid.id.Id[]'

    return index

##
# Investigate all the getter-like methods in each object interface to
# further sort aout other data elements, both persisted and others that
# may only need to be instance data..
def map_object_data_patterns(interface, package, index):
    
    object_name = interface['shortname']
    index[interface['shortname'] + '.instance_data'] = OrderedDict()
    for method in interface['methods']:
        var_name = method['name'].split('_', 1)[-1]
        if var_name.endswith('_id'):
            var_name = '_'.join(var_name.split('_')[:-1])
        if var_name.endswith('_ids'):
            var_name = make_plural('_'.join(var_name.split('_')[:-1]))
        if (not (object_name + '.persisted_data') in index):
            index[object_name + '.persisted_data'] = OrderedDict()
        if (not (object_name + '.initialized_data') in index):
            index[object_name + '.initialized_data'] = OrderedDict()
        if (not (object_name + '.aggregate_data') in index):
            index[object_name + '.aggregate_data'] = OrderedDict()
        if (not (object_name + '.arg_detail') in index):
            index[object_name + '.arg_detail'] = OrderedDict()
        if (not (object_name + '.return_types') in index):
            index[object_name + '.return_types'] = OrderedDict()

        ##
        # Log all getter return types for this object:
        if method['name'].startswith('get_'):
            index[object_name + '.return_types'][var_name] = method['return_type']

        ##
        # Here is where we can list by hand any persisted data that we know won't be caught.
        # For instance, some of the AssessmentTaken data is set in the AssessmentSession
        # So it wouldn't have been found 
        if (interface['shortname'] == 'AssessmentTaken' and
              method['name'] in ['get_actual_start_time', 'get_completion_time',
                                 'get_score', 'get_grade_id']):
            index[interface['shortname'] + '.initialized_data'][var_name] = method['return_type']
            index[object_name + '.arg_detail'][var_name] = []

        ##
        # Check for relationship source and destinations:
        if (object_name in index['package_relationships_caps'] and
            object_name.lower() in index['package_relationships_detail'] and
            var_name == index['package_relationships_detail'][object_name.lower()]['source_name']):
            index[interface['shortname'] + '.persisted_data'][var_name] = index['package_relationships_detail'][object_name.lower()]['source_type']
            index[interface['shortname'] + '.initialized_data'][var_name] = index['package_relationships_detail'][object_name.lower()]['source_type']
            index[object_name + '.arg_detail'][var_name] = []
        elif (object_name in index['package_relationships_caps'] and
            object_name.lower() in index['package_relationships_detail'] and
            var_name == index['package_relationships_detail'][object_name.lower()]['destination_name']):
            index[interface['shortname'] + '.persisted_data'][var_name] = index['package_relationships_detail'][object_name.lower()]['destination_type']
            index[interface['shortname'] + '.initialized_data'][var_name] = index['package_relationships_detail'][object_name.lower()]['destination_type']
            index[object_name + '.arg_detail'][var_name] = []
        
        ##
        # Check for any other methods that appear to want to persist data
        # but dont show up in object forms.
        # NOTE this specifically checks for item for assessment
        # question because it is special.
        #"""
        #if (interface['fullname'] == 'osid.learning.Activity' and 
        #    '_based_' in method['name'] and 
        #    not var_name in index[interface['shortname'] + '.persisted_data']):
        #    index[interface['shortname'] + '.persisted_data'][var_name] = method['return_type']"""
        elif (method['name'].startswith('get_') and
              method['name'].endswith('_id') and
              (var_name in index['package_objects_under'] or var_name in index['package_relationships_under']) and
              var_name != 'question' and
              not var_name in index[interface['shortname'] + '.persisted_data']):
            index[interface['shortname'] + '.persisted_data'][var_name] = method['return_type']

        ##
        # Check to see if this method's data variable name, or its
        # plural or singular, has already been seen in persisted data.
        if (var_name in index[object_name + '.persisted_data'] or
            make_plural(var_name) in index[object_name + '.persisted_data'] or 
            remove_plural(var_name) in index[object_name + '.persisted_data']):
            #if interface['shortname'] == 'Asset':
            #    print 'ALREADY PERSISTED', var_name
            pass
        ##
        # Find methods in OsidObject that are aggregates and return objects that
        # that exist in the same package.
        # NOTE: This also asserts that assessment.Answer adn Question is an aggregateable
        # THIS MAY BE A MISTAKE
        elif (method['return_type'].split('.')[-1].split('List')[0] in index['package_objects_caps'] and
            ('Aggregateable' in interface['inherit_shortnames'] or
             var_name == 'answers' or
             var_name == 'question') and
            not var_name in index[object_name + '.persisted_data']):
            #print 'VARNAME =', var_name
            #if interface['shortname'] == 'Asset':
            #    print 'FOUND AGGREGATEABLE OBJECT', var_name
            index[interface['shortname'] + '.aggregate_data'][var_name] = method['return_type']
        ##
        # Next, check to see if this method's data variable name plural
        # or singular varient has already been seen in instance data.
        elif (make_plural(var_name) in index[object_name + '.instance_data'] or 
            remove_plural(var_name) in index[object_name + '.instance_data']):
            #if interface['shortname'] == 'Asset':
            #    print 'ALREADY INSTANCE', var_name
            pass
        ##
        # Find methods in OsidObject that return boolean and have data names
        # that haven't already been found.  These may be overwritten later if
        # it is found that the boolean value refers to the existent of another 
        # return type. 
        elif (method['return_type'] == 'boolean' and
              not var_name in index[object_name + '.instance_data']):
            #if interface['shortname'] == 'Asset':
            #    print 'FOUND INSTANCE BOOLEAN', var_name
            index[interface['shortname'] + '.instance_data'][var_name] = method['return_type']
        ##
        # Find methods in OsidObject that return Ids and have data names
        # that haven't already been found.
        elif ((method['return_type'] == 'osid.id.Id' or
            method['return_type'] == 'osid.id.IdList') and
            not var_name in index[object_name + '.instance_data'] and
            var_name not in ['answers', 'question']):
            #if interface['shortname'] == 'Item':
            #    print 'FOUND INSTANCE ID', var_name
            index[interface['shortname'] + '.instance_data'][var_name] = method['return_type']
        ##
        # Find methods in OsidObject that return Ids where the data name
        # has already been found as boolean and needs to be overwritten.
        # [Don't know why we have this.  The next one seems useful though.]
        elif ((method['return_type'] == 'osid.id.Id' or
            method['return_type'] == 'osid.id.IdList') and
            var_name in index[object_name + '.instance_data'] and
            index[object_name + '.instance_data'][var_name] == 'boolean'):
            #if interface['shortname'] == 'Item':
            #    print 'OVERWROTE INSTANCE ID', var_name
            index[interface['shortname'] + '.instance_data'][var_name] = method['return_type']
        ##
        # Find methods in OsidObject that return Ids where the data name
        # has already been found and needs to be overwritten.
        elif ((method['return_type'] == 'osid.id.Id' or
            method['return_type'] == 'osid.id.IdList') and
            var_name in index[object_name + '.instance_data']):
            #if interface['shortname'] == 'Item':
            #    print 'OVERWROTE INSTANCE ID', var_name
            index[interface['shortname'] + '.instance_data'][var_name] = method['return_type']
        ##
        # Find methods in OsidObject that return other non-boolean/Id things 
        # and have data names that haven't already been found  
        elif (method['return_type'] != 'osid.id.Id' and
              method['return_type'] != 'osid.id.IdList' and
              method['return_type'] != 'boolean' and
              not var_name in index[object_name + '.instance_data']):
            #if interface['shortname'] == 'Item':
            #    print 'FOUND NON-BOOL/ID', var_name
            index[interface['shortname'] + '.instance_data'][var_name] = method['return_type']
        ##
        # Find methods in OsidObject that return other non-boolean/Id things 
        # and have data names that have already been found as Ids
        # perhaps want to change this to look for primitives and not just boolean?!?
        elif (method['return_type'] != 'osid.id.Id' and
              method['return_type'] != 'osid.id.IdList' and
              method['return_type'] != 'boolean' and
              var_name in index[object_name + '.instance_data']):
            #if interface['shortname'] == 'Item':
            #    print 'FOUND NON-BOOL/ID', var_name
            pass
        ##
        # Find methods in OsidObject that return other non-boolean/Id things 
        # and an existing boolean value needs to be overwritten.  
        elif (method['return_type'] != 'osid.id.Id' and
              method['return_type'] != 'osid.id.IdList' and
              method['return_type'] != 'boolean' and
              (index[object_name + '.instance_data'][var_name] != 'osid.id.Id' or
              index[object_name + '.instance_data'][var_name] != 'osid.id.IdList')):
            #if interface['shortname'] == 'Item':
            #    print 'OVERWROTE NON-BOOL/ID', var_name
            index[interface['shortname'] + '.instance_data'][var_name] = method['return_type']
        ##
        # Check to see whether this method has miraculously been discovered
        # already.
        elif (var_name in index[object_name + '.instance_data']):
            pass

        else:
            print 'Still Must Consider:', interface['fullname'], method['name']

##
# Investigate all sessions to see if there are any other data patterns not
# previously found
def map_admin_session_data_patterns(interface, package, index):
    
    object_name = interface['shortname'][:-12]
    index[interface['shortname'] + '.instance_data'] = OrderedDict()
    for method in interface['methods']:
        var_name = method['name'].split('_', 1)[-1]
        if var_name.endswith('_id'):
            var_name = '_'.join(var_name.split('_')[:-1])
        if var_name.endswith('_ids'):
            var_name = make_plural('_'.join(var_name.split('_')[:-1]))

        ##
        # ObjectAdminSession methods that gets object form for create where the
        # id of one other package object is included as the first parameter.
        elif (interface['shortname'].endswith('AdminSession') and
            method['name'].startswith('get_') and
            '_form_for_create' in method['name'] and
            len(method['args']) == 2 and 
            method['args'][0]['arg_type'] == 'osid.id.Id' and
            method['args'][0]['var_name'].split('_')[0] in index['package_objects_under']):
            object_name = index['package_objects_under_to_caps'][method['name'][4:method['name'].index('_form_')]]
            ##
            # Record that we have found initialized and persisted data
            index[object_name + '.initialized_data'][method['args'][0]['var_name'][:-3]] = method['args'][0]['arg_type']
            index[object_name + '.arg_detail'][method['args'][0]['var_name'][:-3]] = []
            index[object_name + '.persisted_data'][method['args'][0]['var_name'][:-3]] = method['args'][0]['arg_type']            
            ##
            # Delete from instance data if they exist:
            if method['args'][0]['var_name'][:-3] in index[object_name + '.instance_data']:
                #if interface['shortname'] == 'AssetAdminSession':
                    #print 'DELETED INSTANCE', index[object_name + '.instance_data'][method['args'][0]['var_name'][:-3]]
                del index[object_name + '.instance_data'][method['args'][0]['var_name'][:-3]]
            ##
            # Flag dependent oobjects that will need to be checked before deletion:
            index[index['package_objects_under_to_caps'][method['args'][0]['var_name'][:-3]] + '.dependent_objects'] = [object_name]
            ## Uncomment following line to see where this initilization pattern is found:
            #print 'FOUND INITIALIZED DATA in', interface['shortname'], method['name']

        ##
        # ObjectAdminSession methods that gets object form for create where the
        # id of one foreign object is included as the first parameter.
        # NOTE: This is for the case where a getter for the foreign object is not included
        # So we might need to check for the case where such a getter is included.
        elif (interface['shortname'].endswith('AdminSession') and
            method['name'].startswith('get_') and
            '_form_for_create' in method['name'] and
            len(method['args']) == 2 and 
            method['args'][0]['arg_type'] == 'osid.id.Id'):
            #object_name = index['package_objects_under_to_caps'][method['name'][4:-16]]
            ##
            # Record that we have found initialized and persisted data
            index[object_name + '.initialized_data'][method['args'][0]['var_name'][:-3]] = method['args'][0]['arg_type']
            index[object_name + '.arg_detail'][method['args'][0]['var_name'][:-3]] = []
            index[object_name + '.persisted_data'][method['args'][0]['var_name'][:-3]] = method['args'][0]['arg_type']            
            ##
            # Delete from instance data if they exist:
            #if method['args'][0]['var_name'][:-3] in index[object_name + '.instance_data']:
                #if interface['shortname'] == 'AssetAdminSession':
                    #print 'DELETED INSTANCE', index[object_name + '.instance_data'][method['args'][0]['var_name'][:-3]]
            #    del index[object_name + '.instance_data'][method['args'][0]['var_name'][:-3]]
            ##
            # Flag dependent oobjects that will need to be checked before deletion:
            #index[index['package_objects_under_to_caps'][method['args'][0]['var_name'][:-3]] + '.dependent_objects'] = [object_name]
            ## Uncomment following line to see where this initilization pattern is found:
            #print 'FOUND INITIALIZED DATA in', interface['shortname'], method['name']


        ##
        # ObjectAdminSession get_x_form_for_create methods that draw relationships between two
        # osid objects where two object ids are included as the first two parameters.
        elif (interface['shortname'].endswith('AdminSession') and
            method['name'].startswith('get_') and
            method['name'].endswith('_form_for_create') and
            len(method['args']) == 3 and 
            method['args'][0]['arg_type'] == 'osid.id.Id' and
            method['args'][1]['arg_type'] == 'osid.id.Id'):
            object_name = index['package_objects_under_to_caps'][method['name'][4:-16]]
            ##
            # Record that we have found two initialized data elements which are also persisted:
            # But first look for the pesky 'id_' args
            if method['args'][0]['var_name'] == 'id_':
                arg0_name = 'id_'
            else:
                arg0_name = method['args'][0]['var_name'][:-3]
            if method['args'][1]['var_name'] == 'id_':
                arg1_name = 'id_'
            else:
                arg1_name = method['args'][1]['var_name'][:-3]
            index[object_name + '.initialized_data'][arg0_name] = method['args'][0]['arg_type']
            index[object_name + '.persisted_data'][arg0_name] = method['args'][0]['arg_type']
            index[object_name + '.arg_detail'][arg0_name] = []
            index[object_name + '.initialized_data'][arg1_name] = method['args'][1]['arg_type']
            index[object_name + '.persisted_data'][arg1_name] = method['args'][1]['arg_type']
            index[object_name + '.arg_detail'][arg1_name] = []
            ##
            # And delete from instance data if they exist:
            if method['args'][0]['var_name'][:-3] in index[object_name + '.instance_data']:
                #if interface['shortname'] == 'AssetAdminSession':
                    #print 'DELETED INSTANCE', index[object_name + '.instance_data'][method['args'][0]['var_name'][:-3]]
                del index[object_name + '.instance_data'][method['args'][0]['var_name'][:-3]]
            if method['args'][1]['var_name'][:-3] in index[object_name + '.instance_data']:
                #if interface['shortname'] == 'AssetAdminSession':
                    #print 'DELETED INSTANCE', index[object_name + '.instance_data'][method['args'][0]['var_name'][:-3]]
                del index[object_name + '.instance_data'][method['args'][1]['var_name'][:-3]]
            ## Uncomment following line to see where this initilization pattern is found:
            #print 'FOUND INITIALIZED DATA in', interface['shortname'], method['name']


