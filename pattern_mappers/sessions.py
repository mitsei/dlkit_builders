from binder_helpers import make_twargs, camel_to_under, make_plural, remove_plural

def map_session_patterns(interface, package, index):
    if (interface['shortname'].endswith('LookupSession') and
        interface['shortname'][:-13] in index['package_containable_objects_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'repository.CompositionLookupSession'
    elif (interface['shortname'].endswith('QuerySession') and
        interface['shortname'][:-13] in index['package_containable_objects_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'repository.CompositionLookupSession'
    elif (interface['shortname'].endswith('LookupSession') and
        interface['shortname'][:-13] in index['package_objects_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'resource.ResourceLookupSession'
    elif (interface['shortname'].endswith('AdminSession') and
        interface['shortname'][:-12] in index['package_objects_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'resource.ResourceAdminSession'
    elif (interface['shortname'].endswith('NotificationSession') and
        interface['shortname'][:-len('NotificationSession')] in index['package_objects_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'resource.ResourceNotificationSession'
    elif interface['shortname'] == "RelationshipLookupSession":
        index[interface['shortname'] + '.init_pattern'] = 'resource.ResourceLookupSession'
    elif (interface['shortname'].endswith('LookupSession') and
        interface['shortname'][:-13] in index['package_relationships_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'commenting.CommentLookupSession'
    elif (interface['shortname'].endswith('AdminSession') and
        interface['shortname'][:-12] in index['package_relationships_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'resource.ResourceAdminSession'

    elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'Session') and
        'Smart' not in interface['shortname'] and
        interface['shortname'].replace(index['package_catalog_caps'] + 'Session', '') in index['package_objects_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'resource.ResourceBinSession'
    elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'AssignmentSession') and
        interface['shortname'].replace(index['package_catalog_caps'] + 'AssignmentSession', '') in index['package_objects_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'resource.ResourceBinAssignmentSession'
    elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'Session') and
        'Smart' not in interface['shortname'] and
        interface['shortname'].replace(index['package_catalog_caps'] + 'Session', '') in index['package_relationships_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'resource.ResourceBinSession'
    elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'AssignmentSession') and
        interface['shortname'].replace(index['package_catalog_caps'] + 'AssignmentSession', '') in index['package_relationships_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'resource.ResourceBinAssignmentSession'

    elif (interface['shortname'].endswith('QuerySession') and
        interface['shortname'][:-12] in index['package_objects_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'resource.ResourceQuerySession'
    elif (interface['shortname'].endswith('QuerySession') and
        interface['shortname'][:-12] in index['package_relationships_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'commenting.CommentQuerySession'
    elif (interface['shortname'].endswith('LookupSession') and
        interface['shortname'][:-13] in index['package_catalog_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'resource.BinLookupSession'
    elif (interface['shortname'].endswith('QuerySession') and
            interface['shortname'][:-12] in index['package_catalog_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'resource.BinQuerySession'
    elif (interface['shortname'].endswith('AdminSession') and
        interface['shortname'][:-12] in index['package_catalog_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'resource.BinAdminSession'
    elif (interface['shortname'].endswith('NotificationSession') and
        interface['shortname'][:-len('NotificationSession')] in index['package_catalog_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'resource.BinNotificationSession'
    elif (interface['shortname'].endswith('HierarchySession') and
        interface['shortname'][:-16] in index['package_catalog_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'resource.BinHierarchySession'
    elif (interface['shortname'].endswith('HierarchyDesignSession') and
        interface['shortname'] != 'HierarchyDesignSession' and
        interface['shortname'][:-22] in index['package_catalog_caps']):
        index[interface['shortname'] + '.init_pattern'] = 'resource.BinHierarchyDesignSession'

    for method in interface['methods']:
        # Uncomment the following line to see which session raised an error.
        #print interface['fullname'], method['name']
        #print 'length args =', len(method['args'])
        
        index['impl_log']['sessions'][interface['shortname']][method['name']] = ['mapped', 'unimplemented']


        ##################################################################
        ## Inspect this package's CatalogLookupSession methods.         ##
        ##################################################################

        ##
        # CatalogLookupSession methods that returns a catalog with no id.
        # this matches the filing.DirectoryLookupSession first get directory method
        if (interface['shortname'] == index['package_catalog_caps'] + 'LookupSession' and
            method['name'] == 'get_' + index['package_catalog_under'] and
            len(method['args']) == 0):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'filing.DirectoryLookupSession.get_directory',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              return_type_full = method['return_type'],
                              cat_name = index['package_catalog_caps']))

        ##
        # CatalogLookupSession methods that returns a catalog.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'LookupSession' and
            method['name'] == 'get_' + index['package_catalog_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinLookupSession.get_bin',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              cat_name = index['package_catalog_caps']))

        ##
        # CatalogLookupSession methods that returns catalogs by ids.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'LookupSession' and
            method['name'] == 'get_' + make_plural(index['package_catalog_under']) + '_by_ids' and
            'osid.id.IdList' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinLookupSession.get_bins_by_ids',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              cat_name = index['package_catalog_caps']))

        ##
        # CatalogLookupSession methods that returns catalogs by genus type.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'LookupSession' and
            method['name'] == 'get_' + make_plural(index['package_catalog_under']) + '_by_genus_type' and
            'osid.type.Type' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinLookupSession.get_bins_by_genus_type',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              cat_name = index['package_catalog_caps']))

        ##
        # CatalogLookupSession methods that returns catalogs by parent genus type.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'LookupSession' and
            method['name'] == 'get_' + make_plural(index['package_catalog_under']) + '_by_parent_genus_type' and
            'osid.type.Type' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinLookupSession.get_bins_by_parent_genus_type',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              cat_name = index['package_catalog_caps']))

        ##
        # CatalogLookupSession methods that returns catalogs by record type.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'LookupSession' and
            method['name'] == 'get_' + make_plural(index['package_catalog_under']) + '_by_record_type' and
            'osid.type.Type' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinLookupSession.get_bins_by_record_type',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              cat_name = index['package_catalog_caps']))

        ##
        # CatalogLookupSession methods that returns catalogs by provider.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'LookupSession' and
            method['name'] == 'get_' + make_plural(index['package_catalog_under']) + '_by_provider' and
            'osid.id.Id' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinLookupSession.get_bins_by_provider',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              cat_name = index['package_catalog_caps']))

        ##
        # CatalogLookupSession methods that returns all catalogs.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'LookupSession' and
            method['name'] == 'get_' + make_plural(index['package_catalog_under'])):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinLookupSession.get_bins',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              return_type_full = method['return_type'],
                              cat_name = index['package_catalog_caps']))



        ##################################################################
        ## Inspect this package's CatalogQuerySession methods.          ##
        ##################################################################

        ##
        # CatalogQuerySession methods that get a catalog Query.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'QuerySession' and
            method['name'] == 'get_' + index['package_catalog_under'] + '_query'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinQuerySession.get_bin_query',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              return_type_full = method['return_type'],
                              cat_name = index['package_catalog_caps']))

        ##
        # CatalogQuerySession methods that returns catalogs given catalog query.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'QuerySession' and
            method['name'] == 'get_' + make_plural(index['package_catalog_under']) + '_by_query'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinQuerySession.get_bins_by_query',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              return_type_full = method['return_type'],
                              cat_name = index['package_catalog_caps'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))



        ##################################################################
        ## Inspect this package's CatalogSearchSession methods.         ##
        ##################################################################

        ##
        # CatalogSearchSession methods that get a catalog Search.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'SearchSession' and
            method['name'] == 'get_' + index['package_catalog_under'] + '_search'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinSearchSession.get_bin_search',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              return_type_full = method['return_type'],
                              cat_name = index['package_catalog_caps']))

        ##
        # CatalogSearchSession methods that get a catalog SearchOrder.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'SearchSession' and
            method['name'] == 'get_' + index['package_catalog_under'] + '_search_order'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinSearchSession.get_bin_search_order',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              return_type_full = method['return_type'],
                              cat_name = index['package_catalog_caps']))

        ##
        # CatalogSearchSession methods that gets catalogs by Search.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'SearchSession' and
            method['name'] == 'get_' + make_plural(index['package_catalog_under']) + '_by_search'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinSearchSession.get_bins_by_search',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              return_type_full = method['return_type'],
                              cat_name = index['package_catalog_caps'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type'],
                              arg1_name = method['args'][1]['var_name'],
                              arg1_type = method['args'][1]['arg_type']))

        ##
        # CatalogSearchSession methods that gets catalog Query from an Inspector.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'SearchSession' and
            method['name'] == 'get_' + index['package_catalog_under'] + '_query_from_inspector'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinSearchSession.get_bin_query_from_inspector',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              return_type_full = method['return_type'],
                              cat_name = index['package_catalog_caps'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))



        ##################################################################
        ## Inspect this package's CatalogAdminSession methods.          ##
        ##################################################################

        ##
        # CatalogAdminSession methods that gets catalog form for create.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'AdminSession' and
            method['name'] == 'get_' + index['package_catalog_under'] + '_form_for_create'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinAdminSession.get_bin_form_for_create',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              return_type_full = method['return_type'],
                              cat_name = index['package_catalog_caps'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))

        ##
        # CatalogAdminSession methods that create catalogs.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'AdminSession' and
            method['name'] == 'create_' + index['package_catalog_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinAdminSession.create_bin',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              return_type_full = method['return_type'],
                              cat_name = index['package_catalog_caps'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))

        ##
        # CatalogAdminSession methods that gets catalog form for update.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'AdminSession' and
            method['name'] == 'get_' + index['package_catalog_under'] + '_form_for_update'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinAdminSession.get_bin_form_for_update',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))

        ##
        # CatalogAdminSession methods that update catalogs and take two arguments.
        # THIS WAS IN SUPPORT OF A BUG IN learning.ObjectiveBankLookupSession.update_objective_bank.
        # IT CAN GO AS SOON AS TOM FIXES:
        elif (interface['shortname'] == index['package_catalog_caps'] + 'AdminSession' and
            method['name'] == 'update_' + index['package_catalog_under'] and
            len(method['args']) == 2):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinAdminSession.update_bin',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['args'][0]['arg_type'][:-4],
                              arg0_name = method['args'][1]['var_name'],
                              arg0_type_full = method['args'][1]['arg_type']))

        ##
        # CatalogAdminSession methods that update catalogs.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'AdminSession' and
            method['name'] == 'update_' + index['package_catalog_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinAdminSession.update_bin',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['args'][0]['arg_type'][:-4],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))

        ##
        # CatalogAdminSession methods that delete catalogs in packages where there are managed objects.
        # So this will not identify HierarchyAdminSession.delete_hierarchy for instance
        elif (interface['shortname'] == index['package_catalog_caps'] + 'AdminSession' and
            (index['package_objects_caps'] != [] or index['package_relationships_caps'] != []) and
            method['name'] == 'delete_' + index['package_catalog_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinAdminSession.delete_bin',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              cat_name = index['package_catalog_caps'],
                              cataloged_object_caps_list = '[\'' + '\', \''.join(index['package_cataloged_objects_caps']) + '\']',
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))

        ##
        # CatalogAdminSession methods that alias catalogs.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'AdminSession' and
            method['name'] == 'alias_' + index['package_catalog_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinAdminSession.alias_bin',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              cat_name = index['package_catalog_caps'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['arg_type']))



        ##################################################################
        ## Inspect this package's CatalogNotificationSession methods.   ##
        ##################################################################

        ##
        # CatalogNotificationSession methods that register for new catalogs.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'NotificationSession' and
            method['name'] == 'register_for_new_' + make_plural(index['package_catalog_under'])):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinNotificationSession.register_for_new_bins',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name']))

        ##
        # CatalogNotificationSession methods that register for new catalog ancestors.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'NotificationSession' and
            method['name'] == 'register_for_new_' + index['package_catalog_under'] + '_ancestors'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinNotificationSession.register_for_new_bin_ancestors',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # CatalogNotificationSession methods that register for new catalog decendents.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'NotificationSession' and
            method['name'] == 'register_for_new_' + index['package_catalog_under'] + '_descendants'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinNotificationSession.register_for_new_bin_descendants',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # CatalogNotificationSession methods that register for changed catalogs.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'NotificationSession' and
            method['name'] == 'register_for_changed_' + make_plural(index['package_catalog_under'])):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinNotificationSession.register_for_changed_bins',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name']))

        ##
        # CatalogNotificationSession methods that register for changed catalog.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'NotificationSession' and
            method['name'] == 'register_for_changed_' + index['package_catalog_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinNotificationSession.register_for_changed_bin',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # CatalogNotificationSession methods that register for deleted catalogs.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'NotificationSession' and
            method['name'] == 'register_for_deleted_' + make_plural(index['package_catalog_under'])):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinNotificationSession.register_for_deleted_bins',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name']))

        ##
        # CatalogNotificationSession methods that register for deleted catalog.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'NotificationSession' and
            method['name'] == 'register_for_deleted_' + index['package_catalog_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinNotificationSession.register_for_deleted_bin',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # CatalogNotificationSession methods that register for deleted catalog ancestors.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'NotificationSession' and
            method['name'] == 'register_for_deleted_' + index['package_catalog_under'] + '_ancestors'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinNotificationSession.register_for_deleted_bin_ancestors',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # CatalogNotificationSession methods that register for deleted catalog decendents.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'NotificationSession' and
            method['name'] == 'register_for_deleted_' + index['package_catalog_under'] + '_decendents'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinNotificationSession.register_for_deleted_bin_decendents',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              arg0_name = method['args'][0]['var_name']))



        ##################################################################
        ## The following are a couple of potentially special hierarchy  ##
        ## related sessions that seem to want be be located here.       ##
        ##################################################################

        ## (This one may not be necessary. Will the generic do?)
        # CatalogHierarchySession methods that gets the id for the catalog hierarchy.
        elif (method['name'] == 'get_' + index['package_catalog_under'] + '_hierarchy_id'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchySession.get_bin_hierarchy_id',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type']))

        ## (This one may not be necessary. Will the generic do?)
        # CatalogHierarchySession methods that gets the hierarchy for the catalog.
        elif (method['name'] == 'get_' + index['package_catalog_under'] + '_hierarchy'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchySession.get_bin_hierarchy',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type']))



        ##################################################################
        ## Inspect this package's CatalogHierarchySession methods.      ##
        ##################################################################

        ## (This one may not be necessary. Will the generic do?)
        # CatalogHierarchySession methods that return an authorization hint.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchySession' and
            method['name'] == 'can_access_' + index['package_catalog_under'] + '_hierarchy'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchySession.can_access_bin_hierarchy',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:]))

        ##
        # CatalogHierarchySession methods that gets the root catalog Ids.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchySession' and
            method['name'] == 'get_root_' + index['package_catalog_under'] + '_ids'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchySession.get_root_bin_ids',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type']))

        ##
        # CatalogHierarchySession methods that gets the root catalogs.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchySession' and
            method['name'] == 'get_root_' + make_plural(index['package_catalog_under'])):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchySession.get_root_bins',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              cat_name = index['package_catalog_caps']))

        ##
        # CatalogHierarchySession methods that tests for parent catalogs.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchySession' and
            method['name'] == 'has_parent_' + make_plural(index['package_catalog_under'])):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchySession.has_parent_bins',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # CatalogHierarchySession methods that tests if an Id is a direct parent of a catalog.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchySession' and
            method['name'] == 'is_parent_of_' + index['package_catalog_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchySession.is_parent_of_bin',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name']))

        ##
        # CatalogHierarchySession methods that gets parent catalog Ids.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchySession' and
            method['name'] == 'get_parent_' + index['package_catalog_under'] + '_ids'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchySession.get_parent_bin_ids',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # CatalogHierarchySession methods that gets parent catalogs.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchySession' and
            method['name'] == 'get_parent_' + make_plural(index['package_catalog_under'])):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchySession.get_parent_bins',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              cat_name = index['package_catalog_caps']))

        ##
        # CatalogHierarchySession methods that tests if an Id is an ancestor of a catalog.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchySession' and
            method['name'] == 'is_ancestor_of_' + index['package_catalog_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchySession.is_ancestor_of_bin',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name']))

        ##
        # CatalogHierarchySession methods that tests for child catalogs.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchySession' and
            method['name'] == 'has_child_' + make_plural(index['package_catalog_under'])):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchySession.has_child_bins',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # CatalogHierarchySession methods that tests if an Id is a direct child of a catalog.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchySession' and
            method['name'] == 'is_child_of_' + index['package_catalog_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchySession.is_child_of_bin',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name']))

        ##
        # CatalogHierarchySession methods that gets child catalog Ids.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchySession' and
            method['name'] == 'get_child_' + index['package_catalog_under'] + '_ids'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchySession.get_child_bin_ids',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # CatalogHierarchySession methods that gets child catalogs.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchySession' and
            method['name'] == 'get_child_' + make_plural(index['package_catalog_under'])):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchySession.get_child_bins',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              cat_name = index['package_catalog_caps']))

        ##
        # CatalogHierarchySession methods that tests if an Id is an descendant of a catalog.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchySession' and
            method['name'] == 'is_descendant_of_' + index['package_catalog_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchySession.is_descendant_of_bin',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name']))

        ##
        # CatalogHierarchySession methods that gets parent catalog node Ids.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchySession' and
            method['name'] == 'get_' + index['package_catalog_under'] + '_node_ids'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchySession.get_bin_node_ids',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name'],
                              arg2_name = method['args'][2]['var_name'],
                              arg3_name = method['args'][3]['var_name']))

        ##
        # CatalogHierarchySession methods that gets catalog nodes.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchySession' and
            method['name'] == 'get_' + index['package_catalog_under'] + '_nodes'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchySession.get_bin_nodes',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name'],
                              arg2_name = method['args'][2]['var_name'],
                              arg3_name = method['args'][3]['var_name'],
                              cat_name = index['package_catalog_caps']))



        ##################################################################
        ## Inspect this package's CatalogHierarchyDesignSession methods ##
        ##################################################################

        ## (This one may not be necessary. Will a generic do?)
        # CatalogHierarchyDesignSession methods that return an authorization hint.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchyDesignSession' and
            method['name'] == 'can_modify_' + index['package_catalog_under'] + '_hierarchy'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchyDesignSession.can_modify_bin_hierarchy',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              var_name = method['name'][4:]))

        ##
        # CatalogHierarchyDesignSession methods that adds a root catalog.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchyDesignSession' and
            method['name'] == 'add_root_' + index['package_catalog_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchyDesignSession.add_root_bin',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # CatalogHierarchyDesignSession methods that removes a root catalog.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchyDesignSession' and
            method['name'] == 'remove_root_' + index['package_catalog_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchyDesignSession.remove_root_bin',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              var_name = method['name'][7:],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # CatalogHierarchyDesignSession methods that adds a child catalog.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchyDesignSession' and
            method['name'] == 'add_child_' + index['package_catalog_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchyDesignSession.add_child_bin',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name']))

        ##
        # CatalogHierarchyDesignSession methods that removes a child catalog.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchyDesignSession' and
            method['name'] == 'remove_child_' + index['package_catalog_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchyDesignSession.remove_child_bin',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              var_name = method['name'][7:],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name']))

        ##
        # CatalogHierarchyDesignSession methods that removes all children from a catalog.
        elif (interface['shortname'] == index['package_catalog_caps'] + 'HierarchyDesignSession' and
            method['name'] == 'remove_child_' + make_plural(index['package_catalog_under'])):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinHierarchyDesignSession.remove_child_bins',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              var_name = method['name'][7:],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name']))



        ##################################################################
        ## Inspect the Session methods that returns the associated      ##
        ## Catalog or Catalog Id                                        ##
        ##################################################################

        ##
        # Session methods that return the Id of the associated catalog.
        elif (method['name'] == 'get_' + index['package_catalog_under'] + '_id' and
            method['return_type'] == 'osid.id.Id'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceLookupSession.get_bin_id',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type']))

        ##
        # Session methods that return the associated catalog.
        elif (method['name'] == 'get_' + index['package_catalog_under'] and
            method['name'][4:] == camel_to_under((method['return_type']).split('.')[-1])):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceLookupSession.get_bin',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type']))



        ##################################################################
        ## Inspect this package's RelationshipLookupSession methods.    ##
        ##################################################################

        ##
        # Session methods to use effective Relationship view.
        elif (method['name'].startswith('use_effective_') and
              method['name'].endswith('_view') and
              method['name'][14:-5] in index['package_relationships_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'relationship.RelationshipLookupSession.use_effective_relationship_view',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13]))

        ##
        # Session methods to use any effective Relationship view.
        elif (method['name'].startswith('use_any_effective_') and
              method['name'].endswith('_view') and
              method['name'][18:-5] in index['package_relationships_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'relationship.RelationshipLookupSession.use_any_effective_relationship_view',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13]))

        ##
        # Session methods that get Relationships effective during the given date range.
        elif (method['name'].startswith('get_') and
              method['name'].endswith('_on_date') and
              len(method['args']) == 2 and
              remove_plural(method['name'][4:-8]) in index['package_relationships_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'relationship.RelationshipLookupSession.get_relationships_on_date',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name']))

        ##
        # Session methods that get the Relationships of a source object.
        # Also matches like learning.ProficienciesLookupSession.get_proficiencies_for_objective
        elif (remove_plural(method['name'].split('_for_')[0][4:]) in index['package_relationships_under'] and
              method['name'].startswith('get_') and
              '_for_' + index['package_relationships_detail'][remove_plural(method['name'].split('_for_')[0][4:])]['source_name'] in method['name'] and
              not method['name'].endswith('_on_date') and
              not '_by_genus_type_' in method['name'] and
              len(method['args']) == 1):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'relationship.RelationshipLookupSession.get_relationships_for_source',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              source_name = index['package_relationships_detail'][camel_to_under(interface['shortname'][:-13])]['source_name'],
                              arg0_name = method['args'][0]['var_name'],
                              obj_type = (method['name'].split('_for_')[-1]).split('source_', 1)[-1]))

        ##
        # Session methods that get the Relationships of a source object for an effective date range.
        # Also matches like learning.ProficienciesLookupSession.get_proficiencies_for_objective_on_date
        elif (remove_plural(method['name'].split('_for_')[0][4:]) in index['package_relationships_under'] and
              method['name'].startswith('get_') and
              '_for_' + index['package_relationships_detail'][remove_plural(method['name'].split('_for_')[0][4:])]['source_name'] in method['name'] and
              method['name'].endswith('_on_date') and
              not '_by_genus_type_' in method['name'] and
              len(method['args']) == 3):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'relationship.RelationshipLookupSession.get_relationships_for_source_on_date',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              object_name = interface['shortname'][:-13],
                              return_type_full = method['return_type'],
                              source_name = index['package_relationships_detail'][camel_to_under(interface['shortname'][:-13])]['source_name'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name'],
                              arg2_name = method['args'][2]['var_name'],
                              obj_type = (method['name'].split('_for_')[-1]).split('source_', 1)[-1][:-8]))

        ##
        # Session methods that get the Relationships of a source object by genus type.
        # Also matches learning.ProficienciesLookupSession.get_proficiencies_by_genus_type_for_objective
        elif (remove_plural(method['name'].split('_by_')[0][4:]) in index['package_relationships_under'] and
              method['name'].startswith('get_') and
              '_for_' + index['package_relationships_detail'][remove_plural(method['name'].split('_by_')[0][4:])]['source_name'] in method['name'] and
              '_by_genus_type_' in method['name'] and
              not method['name'].endswith('_on_date') and
              len(method['args']) == 2):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'relationship.RelationshipLookupSession.get_relationships_by_genus_type_for_source',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              source_name = index['package_relationships_detail'][camel_to_under(interface['shortname'][:-13])]['source_name'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name'],
                              obj_type = (method['name'].split('_for_')[-1]).split('source_', 1)[-1]))

        ##
        # Session methods that get the Relationships of a source object for an effective date range by genus type.
        # Also matches like learning.ProficienciesLookupSession.get_proficiencies_by_genus_type_for_objective_on_date
        elif (remove_plural(method['name'].split('_by_')[0][4:]) in index['package_relationships_under'] and
              method['name'].startswith('get_') and
              '_for_' + index['package_relationships_detail'][remove_plural(method['name'].split('_by_')[0][4:])]['source_name'] in method['name'] and
              '_by_genus_type_' in method['name'] and
              method['name'].endswith('_on_date') and
              len(method['args']) == 4):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'relationship.RelationshipLookupSession.get_relationships_by_genus_type_for_source_on_date',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              source_name = index['package_relationships_detail'][camel_to_under(interface['shortname'][:-13])]['source_name'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name'],
                              arg2_name = method['args'][2]['var_name'],
                              arg3_name = method['args'][3]['var_name'],
                              obj_type = (method['name'].split('_for_')[-1]).split('source_', 1)[-1][:-8]))

        ##
        # Session methods that get the Relationships of a destination resource.
        # Tests for both the 'destination_resource' version in resource package as well as generic 'resource'
        elif (remove_plural(method['name'].split('_for_')[0][4:]) in index['package_relationships_under'] and
              method['name'].startswith('get_') and
              '_for_' + index['package_relationships_detail'][remove_plural(method['name'].split('_for_')[0][4:])]['destination_name'] in method['name'] and
              not method['name'].endswith('_on_date') and
              not '_by_genus_type_' in method['name'] and
              len(method['args']) == 1):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'relationship.RelationshipLookupSession.get_relationships_for_destination',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              destination_name = index['package_relationships_detail'][camel_to_under(interface['shortname'][:-13])]['destination_name'],
                              arg0_name = method['args'][0]['var_name'],
                              obj_type = 'resource'))

        ##
        # Session methods that get the Relationships of a destination resource for an effective date range.
        # Tests for both the 'destination_resource' version in resource package as well as generic 'resource'
        elif (remove_plural(method['name'].split('_for_')[0][4:]) in index['package_relationships_under'] and
              method['name'].startswith('get_') and
              '_for_' + index['package_relationships_detail'][remove_plural(method['name'].split('_for_')[0][4:])]['destination_name'] in method['name'] and
              method['name'].endswith('_on_date') and
              not '_by_genus_type_' in method['name'] and
              len(method['args']) == 3):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'relationship.RelationshipLookupSession.get_relationships_for_destination_on_date',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              destination_name = index['package_relationships_detail'][camel_to_under(interface['shortname'][:-13])]['destination_name'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name'],
                              arg2_name = method['args'][2]['var_name'],
                              obj_type = 'resource'))

        ##
        # Session methods that get the Relationships of a destination resource by genus type.
        # Tests for both the 'destination_resource' version in resource package as well as generic 'resource'
        elif (remove_plural(method['name'].split('_by_')[0][4:]) in index['package_relationships_under'] and
              method['name'].startswith('get_') and
              '_for_' + index['package_relationships_detail'][remove_plural(method['name'].split('_by_')[0][4:])]['destination_name'] in method['name'] and
              not method['name'].endswith('_on_date') and
              '_by_genus_type_' in method['name'] and
              len(method['args']) == 2):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'relationship.RelationshipLookupSession.get_relationships_by_genus_type_for_destination',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              destination_name = index['package_relationships_detail'][camel_to_under(interface['shortname'][:-13])]['destination_name'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name'],
                              obj_type = 'resource'))

        ##
        # Session methods that get the Relationships of a destination resource for an effective date range by genus type.
        # Tests for both the 'destination_resource' version in resource package as well as generic 'resource'
        elif (remove_plural(method['name'].split('_by_')[0][4:]) in index['package_relationships_under'] and
              method['name'].startswith('get_') and
              '_for_' + index['package_relationships_detail'][remove_plural(method['name'].split('_by_')[0][4:])]['destination_name'] in method['name'] and
              method['name'].endswith('_on_date') and
              '_by_genus_type_' in method['name'] and
              len(method['args']) == 4):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'relationship.RelationshipLookupSession.get_relationships_by_by_genus_type_for_destination_on_date',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              destination_name = index['package_relationships_detail'][camel_to_under(interface['shortname'][:-13])]['destination_name'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name'],
                              arg2_name = method['args'][2]['var_name'],
                              arg3_name = method['args'][3]['var_name'],
                              obj_type = 'resource'))

        ##
        # Session methods that get the Relationships for two objects (peers).
        # works for generic relationship service and the resource.ResourceRelationship like case
        elif (method['name'].startswith('get_') and
              '_for_' in method['name'] and
              not method['name'].endswith('_on_date') and
              not '_by_genus_type_' in method['name'] and
              len(method['args']) == 2 and
              remove_plural(method['name'].split('_for_')[0][4:]) in index['package_relationships_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'relationship.RelationshipLookupSession.get_relationships_for_peers',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              source_name = index['package_relationships_detail'][camel_to_under(interface['shortname'][:-13])]['source_name'],
                              destination_name = index['package_relationships_detail'][camel_to_under(interface['shortname'][:-13])]['destination_name'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name'],
                              obj_type = 'resource'))

        ##
        # Session methods that get the Relationships for two objects for an effective date range.
        # works for generic relationship service and the resource.ResourceRelationship like case
        elif (method['name'].startswith('get_') and
              '_for_' in method['name'] and
              method['name'].endswith('_on_date') and
              not '_by_genus_type_' in method['name'] and
              len(method['args']) == 4 and
              remove_plural(method['name'].split('_for_')[0][4:]) in index['package_relationships_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'relationship.RelationshipLookupSession.get_relationships_for_peers_on_date',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              source_name = index['package_relationships_detail'][camel_to_under(interface['shortname'][:-13])]['source_name'],
                              destination_name = index['package_relationships_detail'][camel_to_under(interface['shortname'][:-13])]['destination_name'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name'],
                              arg2_name = method['args'][2]['var_name'],
                              arg3_name = method['args'][3]['var_name'],
                              obj_type = 'resource'))


        ##
        # Session methods that get the Relationships for two objects by genus type.
        # works for generic relationship service and the resource.ResourceRelationship like case
        elif (method['name'].startswith('get_') and
              '_for_' in method['name'] and
              not method['name'].endswith('_on_date') and
              '_by_genus_type_' in method['name'] and
              len(method['args']) == 3 and
              remove_plural(method['name'].split('_by_genus_type_for_')[0][4:]) in index['package_relationships_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'relationship.RelationshipLookupSession.get_relationships_by_genus_type_for_peers',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              source_name = index['package_relationships_detail'][camel_to_under(interface['shortname'][:-13])]['source_name'],
                              destination_name = index['package_relationships_detail'][camel_to_under(interface['shortname'][:-13])]['destination_name'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name'],
                              arg2_name = method['args'][2]['var_name'],
                              obj_type = 'resource'))

        ##
        # Session methods that get the Relationships for two objects for an effective date range by genus type.
        # works for generic relationship service and the resource.ResourceRelationship like case
        elif (method['name'].startswith('get_') and
              '_for_' in method['name'] and
              method['name'].endswith('_on_date') and
              '_by_genus_type_' in method['name'] and
              len(method['args']) == 5 and
              remove_plural(method['name'].split('_by_genus_type_for_')[0][4:]) in index['package_relationships_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'relationship.RelationshipLookupSession.get_relationships_by_genus_type_for_peers_on_date',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              cat_name = index['package_catalog_caps'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type'],
                              source_name = index['package_relationships_detail'][camel_to_under(interface['shortname'][:-13])]['source_name'],
                              destination_name = index['package_relationships_detail'][camel_to_under(interface['shortname'][:-13])]['destination_name'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name'],
                              arg2_name = method['args'][2]['var_name'],
                              arg3_name = method['args'][3]['var_name'],
                              arg4_name = method['args'][4]['var_name'],
                              obj_type = 'resource'))



        ##################################################################
        ## Inspect this package's ObjectLookupSession methods.  This    ##
        ## and many of the following fuctions will also find common     ##
        ## patterns that also occur in Catalog, Relationahsip and other ##
        ## session's methods                                            ##
        ##################################################################

        ##
        # ObjectLookupSession methods that return an authorization hint.
        elif (interface['shortname'].endswith('LookupSession') and
              method['name'].startswith('can_') and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceLookupSession.can_lookup_resources',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              var_name = method['name']))

        ##
        # ObjectLookupSession methods that returns an object (without id, where there appears to be one and only one).
        elif (interface['shortname'].endswith('LookupSession') and
              method['name'].startswith('get_') and
              method['name'][4:] == camel_to_under((method['return_type']).split('.')[-1]) and
              len(method['args']) == 0):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'installation.InstallationLookupSession.get_site',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type']))

        ##
        # ObjectLookupSession methods that returns an object by an id.
        elif (interface['shortname'].endswith('LookupSession') and
              method['name'].startswith('get_') and
              method['name'][4:] == camel_to_under((method['return_type']).split('.')[-1]) and
              len(method['args']) == 1):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceLookupSession.get_resource',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # ObjectLookupSession methods that returns objects by ids.
        elif (interface['shortname'].endswith('LookupSession') and
              method['name'].startswith('get_') and
              method['name'].endswith('_by_ids') and
              'osid.id.IdList' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceLookupSession.get_resources_by_ids',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # ObjectLookupSession methods that returns objects by genus type.
        elif (interface['shortname'].endswith('LookupSession') and
              method['name'].startswith('get_') and
              method['name'].endswith('_by_genus_type') and
              'osid.type.Type' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceLookupSession.get_resources_by_genus_type',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # ObjectLookupSession methods that returns objects by parent genus type.
        elif (interface['shortname'].endswith('LookupSession') and
              method['name'].startswith('get_') and
              method['name'].endswith('_by_parent_genus_type') and
              'osid.type.Type' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceLookupSession.get_resources_by_parent_genus_type',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # ObjectLookupSession methods that returns objects by record type.
        elif (interface['shortname'].endswith('LookupSession') and
              method['name'].startswith('get_') and
              method['name'].endswith('_by_record_type') and
              'osid.type.Type' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceLookupSession.get_resources_by_record_type',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # ObjectLookupSession methods that returns all objects.
        elif (interface['shortname'].endswith('LookupSession') and
              method['name'].startswith('get_') and
              camel_to_under((method['return_type']).split('.')[-1]) == 
                        remove_plural(method['name'][4:]) + '_list'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceLookupSession.get_resources',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type']))

        ##
        # ObjectLookupSession methods that return objects for another object 
        # in the package.
        elif (interface['shortname'].endswith('LookupSession') and
              method['name'].startswith('get_') and
              camel_to_under((method['return_type']).split('.')[-1]) == 
                        remove_plural(method['name'].split('_for_')[0][4:]) + '_list' and
                        method['name'].split('_for_')[1] in index['package_objects_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'learning.ActivityLookupSession.get_activities_for_objective',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type'],
                              arg0_object = index['package_objects_under_to_caps'][method['name'].split('_for_')[1]]))

        ##
        # ObjectLookupSession methods that return objects given an IdList of Ids
        # for other objects in the package.
        elif (interface['shortname'].endswith('LookupSession') and
              method['name'].startswith('get_') and
              camel_to_under((method['return_type']).split('.')[-1]) == 
                        remove_plural(method['name'].split('_for_')[0][4:]) + '_list' and
                        remove_plural(method['name'].split('_for_')[1]) in index['package_objects_under']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'learning.ActivityLookupSession.get_activities_for_objectives',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type'],
                              arg0_object = index['package_objects_under_to_caps'][remove_plural(method['name'].split('_for_')[1])]))



        ##################################################################
        ## Inspect this package's ObjectQuerySession methods.           ##
        ##################################################################

        ##
        # ObjectQuerySession methods that return an authorization hint.
        elif (interface['shortname'].endswith('QuerySession') and
              method['name'].startswith('can_search') and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceQuerySession.can_search_resources',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              var_name = method['name']))

        ##
        # ObjectQuerySession methods that return objects by Query.
        elif (interface['shortname'].endswith('QuerySession') and
              method['name'].startswith('get_') and
              method['name'].endswith('_by_query')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceQuerySession.get_resources_by_query',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))

        ##
        # ObjectQuerySession methods that return an object Query.
        elif (interface['shortname'].endswith('QuerySession') and
              method['name'].startswith('get_') and
              method['name'].endswith('_query')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceQuerySession.get_resource_query',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type']))



        ##################################################################
        ## Inspect this package's ObjectSearchSession methods.          ##
        ##################################################################

        ##
        # ObjectSearchSession methods that return objects by Search.
        elif (interface['shortname'].endswith('SearchSession') and
              method['name'].startswith('get_') and
              method['name'].endswith('_by_search')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceSearchSession.get_resources_by_search',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type'],
                              arg1_name = method['args'][1]['var_name'],
                              arg1_type = method['args'][1]['arg_type']))

        ##
        # ObjectSearchSession methods that return an object SearchOrder.
        elif (interface['shortname'].endswith('SearchSession') and
              method['name'].startswith('get_') and
              method['name'].endswith('_search_order')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceSearchSession.get_resource_search_order',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type']))

        ##
        # ObjectSearchSession methods that return an objects Search.
        elif (interface['shortname'].endswith('SearchSession') and
              method['name'].startswith('get_') and
              method['name'].endswith('_search')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceSearchSession.get_resource_search',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type']))

        ##
        # ObjectSearchSession methods that return objects query from an inspector.
        elif (interface['shortname'].endswith('SearchSession') and
              method['name'].startswith('get_') and
              method['name'].endswith('_query_from_inspector')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceSearchSession.get_resource_query_from_inspector',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-13],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))



        ##################################################################
        ## Capture any package's AdminBatchSession methods. the id      ##
        ## package has one that needs to be dealt with differently      ##
        ## There may be others.                                         ##
        ##################################################################
        
        
        elif (interface['shortname'].endswith('BatchAdminSession')):
            #print 'FOUND BATCH ADMIN SESSION:', interface['fullname'], method['name']
            pass



        ##################################################################
        ## Inspect this package's ObjectAdminSession methods.           ##
        ##################################################################


        ##
        # ObjectAdminSession methods that return an authn hint for with record types.
        elif (interface['shortname'].endswith('AdminSession') and
              method['name'].startswith('can_create_') and
              method['name'].endswith('_with_record_types') and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceAdminSession.can_create_resource_with_record_types',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              var_name = method['name'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # Session methods that return an authn hint for a given object id.
        # NOTE: This needs to be looked at more carefully.  There are a number
        # of kinds of situations in the osids where authn hints are provided
        # for an Id for aparently various reasons.
        elif (interface['shortname'].endswith('AdminSession') and
              method['name'].startswith('can_update_') and
              method['return_type'] == 'boolean' and
              'osid.id.Id' in method['arg_types']):
            #print 'Found can_update_agent pattern in', interface['shortname'], method['name']
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'authentication.AgentAdminSession.can_update_agent',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              var_name = method['name']))

        ##
        # ObjectAdminSession methods that return an authn hint for CrUD.
        elif (interface['shortname'].endswith('AdminSession') and
              (method['name'].startswith('can_create_') or
               method['name'].startswith('can_update_') or
               method['name'].startswith('can_delete_')) and
               method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceAdminSession.can_create_resources',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              var_name = method['name']))
        ##
        # ObjectAdminSession methods that return an authn hint for Manage Alias.
        elif (interface['shortname'].endswith('AdminSession') and
               method['name'].startswith('can_manage_') and
               method['name'].endswith('_aliases') and
               method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceAdminSession.can_manage_resource_aliases',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              var_name = method['name']))        

        ##
        # ObjectAdminSession methods that gets object form for create where the
        # id of one other package object is included as the first parameter.
        elif (interface['shortname'].endswith('AdminSession') and
            method['name'].startswith('get_') and
            method['name'].endswith('_form_for_create') and
            len(method['args']) == 2 and 
            method['args'][0]['arg_type'] == 'osid.id.Id' and
            method['args'][0]['var_name'].split('_')[0] in index['package_objects_under']):
            object_name = index['package_objects_under_to_caps'][method['name'][4:-16]]
            #print 'ActivityAdminSession.get_activity_form_for_create', [method['args'][0]['var_name'][:-3]]
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'learning.ActivityAdminSession.get_activity_form_for_create',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type'],
                              arg1_name = method['args'][1]['var_name'],
                              arg1_type_full = method['args'][1]['arg_type']))
            ##
            # And record that we have found initialized and persisted data
#            index[object_name + '.initialized_data'][method['args'][0]['var_name'][:-3]] = method['args'][0]['arg_type']
#            index[object_name + '.arg_detail'][method['args'][0]['var_name'][:-3]] = []
#            index[object_name + '.persisted_data'][method['args'][0]['var_name'][:-3]] = method['args'][0]['arg_type']            
            ##
            # And delete from instance data if they exist:
#            if method['args'][0]['var_name'][:-3] in index[object_name + '.instance_data']:
#                if interface['shortname'] == 'AssetAdminSession':
#                    print 'DELETED INSTANCE', index[object_name + '.instance_data'][method['args'][0]['var_name'][:-3]]
#                del index[object_name + '.instance_data'][method['args'][0]['var_name'][:-3]]
            ## Uncomment following line to see where this initilization pattern is found:
            #print 'FOUND INITIALIZED DATA in', interface['shortname'], method['name']

        ##
        # ObjectAdminSession get_x_form_for_create methods that draw relatioships between two 
        # osid objects where two object ids are included as the first two parameters.
        elif (interface['shortname'].endswith('AdminSession') and
            method['name'][4:-16] in index['package_relationships_under'] and
            method['name'].startswith('get_') and
            method['name'].endswith('_form_for_create') and
            len(method['args']) == 3 and 
            method['args'][0]['arg_type'] == 'osid.id.Id' and
            method['args'][1]['arg_type'] == 'osid.id.Id'):
            #print interface['shortname'], method['name']
            object_name = index['package_objects_under_to_caps'][method['name'][4:-16]]
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'relationship.RelationshipAdminSession.get_relationship_form_for_create',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type'],
                              arg1_name = method['args'][1]['var_name'],
                              arg1_type_full = method['args'][1]['arg_type'],
                              arg2_name = method['args'][2]['var_name'],
                              arg2_type_full = method['args'][2]['arg_type']))

        ##
        # ObjectAdminSession get_x_form_for_create methods that draw relatioships between two 
        # osid objects where one object ids is included as the first parameter.
        elif (interface['shortname'].endswith('AdminSession') and
            method['name'][4:-16] in index['package_relationships_under'] and
            method['name'].startswith('get_') and
            method['name'].endswith('_form_for_create') and
            len(method['args']) == 2 and 
            method['args'][0]['arg_type'] == 'osid.id.Id'):
            #print interface['shortname'], method['name']
            object_name = index['package_objects_under_to_caps'][method['name'][4:-16]]
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'commenting.CommentAdminSession.get_comment_form_for_create',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type'],
                              arg1_name = method['args'][1]['var_name'],
                              arg1_type_full = method['args'][1]['arg_type']))

            ##
            # And record that we have found two initialized data elements which are also persisted:
#            index[object_name + '.initialized_data'][method['args'][0]['var_name'][:-3]] = method['args'][0]['arg_type']
#            index[object_name + '.persisted_data'][method['args'][0]['var_name'][:-3]] = method['args'][0]['arg_type']
#            index[object_name + '.arg_detail'][method['args'][0]['var_name'][:-3]] = []
#            index[object_name + '.initialized_data'][method['args'][1]['var_name'][:-3]] = method['args'][1]['arg_type']
#            index[object_name + '.persisted_data'][method['args'][1]['var_name'][:-3]] = method['args'][1]['arg_type']
#            index[object_name + '.arg_detail'][method['args'][1]['var_name'][:-3]] = []
            ##
            # And delete from instance data if they exist:
#            if method['args'][0]['var_name'][:-3] in index[object_name + '.instance_data']:
#                if interface['shortname'] == 'AssetAdminSession':
#                    print 'DELETED INSTANCE', index[object_name + '.instance_data'][method['args'][0]['var_name'][:-3]]
#                del index[object_name + '.instance_data'][method['args'][0]['var_name'][:-3]]
#            if method['args'][1]['var_name'][:-3] in index[object_name + '.instance_data']:
#                if interface['shortname'] == 'AssetAdminSession':
#                    print 'DELETED INSTANCE', index[object_name + '.instance_data'][method['args'][0]['var_name'][:-3]]
#                del index[object_name + '.instance_data'][method['args'][1]['var_name'][:-3]]
            ## Uncomment following line to see where this initilization pattern is found:
            #print 'FOUND INITIALIZED DATA in', interface['shortname'], method['name']

        ##
        # ObjectAdminSession methods that gets object form for create.
        elif (interface['shortname'].endswith('AdminSession') and
            method['name'].startswith('get_') and
            method['name'].endswith('_form_for_create')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceAdminSession.get_resource_form_for_create',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))

        ##
        # ObjectAdminSession methods that create objects that are aggregates of 
        # the primary object administered by the session. NOTE that this checks
        # for both singular and plural forms of the object name in the method name.
        # WHICH MAY BE A MISTAKE.  TIME WILL TELL.
        # NOTE that this also asserts that the assessment.ItemAdminSession that 
        # creates Answers is of the same pattern.  Also a likely mistake :)
        # NOTE that this also asserts that the assessment.ItemAdminSession that 
        # creates Questions is of the same pattern.  Also a likely mistake :)
        elif (interface['shortname'].endswith('AdminSession') and
            interface['shortname'][:-12] != index['package_catalog_caps'] and
            method['name'].startswith('create_') and
            method['name'][7:] == camel_to_under((method['return_type']).split('.')[-1]) and
            method['return_type'].split('.')[-1] != interface['shortname'][:-12] and
            (method['name'][7:] in index[interface['shortname'][:-12] + '.aggregate_data'] or
            make_plural(method['name'][7:]) in index[interface['shortname'][:-12] + '.aggregate_data'] or
            method['name'] == 'create_answer' or
            method['name'] == 'create_question') and
            len(method['args']) > 0):
            #print 'FOUND CREATE', interface['shortname'], method['name'], method['name'][7:]
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'repository.AssetAdminSession.create_asset_content',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              aggregated_object_name = index['package_objects_under_to_caps'][method['name'][7:]],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))

        ##
        # ObjectAdminSession methods that create objects.
        elif (interface['shortname'].endswith('AdminSession') and
            interface['shortname'][:-12] != index['package_catalog_caps'] and
            method['name'].startswith('create_') and
            method['name'][7:] == camel_to_under((method['return_type']).split('.')[-1]) and
            len(method['args']) > 0):
            
            # This is to deal with an error in the OSID RC3 build:
            if method['name'] == 'create_assessment_offered':
                method['args'][0]['arg_type'] = 'assessment.AssessmentOfferedForm'

            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceAdminSession.create_resource',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))

        ##
        # ObjectAdminSession methods that gets object form for update objects
        # that are aggregates of the primary object administered by the session. 
        # NOTE that this checks for both singular and plural forms of the object name 
        # in the method name WHICH MAY BE A MISTAKE.  TIME WILL TELL.
        # NOTE that this also asserts that the assessment ItemAdminSession that gets
        # update from for Answers is of the same pattern.  Also a likely mistake :)
        # NOTE that this also asserts that the assessment ItemAdminSession that gets
        # update form for Questions is of the same pattern.  Also a likely mistake :)
        elif (interface['shortname'].endswith('AdminSession') and
            interface['shortname'][:-12] != index['package_catalog_caps'] and
            method['name'].startswith('get_') and
            method['name'].endswith('_form_for_update') and
            len(method['args']) == 1 and 
            method['args'][0]['arg_type'] == 'osid.id.Id' and
            method['name'][4:-16] != camel_to_under(interface['shortname'][:-12]) and
            (method['name'][4:-16] in index[interface['shortname'][:-12] + '.aggregate_data'] or
            make_plural(method['name'][4:-16]) in index[interface['shortname'][:-12] + '.aggregate_data'] or
            method['name'] == 'get_answer_form_for_update' or
            method['name'] == 'get_question_form_for_update')):
            #print 'FOUND FORM FOR UPDATE', interface['shortname'], method['name']
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'repository.AssetAdminSession.get_asset_content_form_for_update',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              aggregated_object_name = index['package_objects_under_to_caps'][method['name'][4:-16]],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))
        ##
        # ObjectAdminSession methods that gets object form for update.
        elif (interface['shortname'].endswith('AdminSession') and
            interface['shortname'][:-12] != index['package_catalog_caps'] and
            method['name'].startswith('get_') and
            method['name'].endswith('_form_for_update')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceAdminSession.get_resource_form_for_update',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))


        ##
        # ObjectAdminSession methods that update objects that are aggregates of 
        # the primary object administered by the session. NOTE that this checks
        # for both singular and plural forms of the object name in the method name -
        # WHICH MAY BE A MISTAKE.  TIME WILL TELL.
        # NOTE that this also asserts that the assessment ItemAdminSession that 
        # updates Answers is of the same pattern.  Also a likely mistake :)
        # NOTE that this also asserts that the assessment ItemAdminSession that 
        # updates Questions is of the same pattern.  Also a likely mistake :)
        elif (interface['shortname'].endswith('AdminSession') and
            interface['shortname'][:-12] != index['package_catalog_caps'] and
            method['name'].startswith('update_') and
            camel_to_under((method['arg_types'][0]).split('.')[-1]) == method['name'][7:] + '_form' and
            method['name'][7:] != camel_to_under(interface['shortname'][:-12]) and
            (method['name'][7:] in index[interface['shortname'][:-12] + '.aggregate_data'] or
            make_plural(method['name'][7:]) in index[interface['shortname'][:-12] + '.aggregate_data'] or
            method['name'] == 'update_answer' or
            method['name'] == 'update_question')):
            #print 'FOUND UPDATE', interface['shortname'], method['name']
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'repository.AssetAdminSession.update_asset_content',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              aggregated_object_name = index['package_objects_under_to_caps'][method['name'][7:]],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['args'][0]['arg_type'][:-4],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))

        ##
        # ObjectAdminSession methods that update objects.
        elif (interface['shortname'].endswith('AdminSession') and
            interface['shortname'][:-12] != index['package_catalog_caps'] and
            method['name'].startswith('update_') and
            camel_to_under((method['arg_types'][0]).split('.')[-1]) == 
                        method['name'][7:] + '_form'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceAdminSession.update_resource',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['args'][0]['arg_type'][:-4],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))

        ##
        # ObjectAdminSession methods that delete objects that are dependencies for 
        # one other object in the service package.
        elif (interface['shortname'].endswith('AdminSession') and
            interface['shortname'][:-12] + '.dependent_objects' in index and
            len(index[interface['shortname'][:-12] + '.dependent_objects']) == 1 and
            camel_to_under(index[interface['shortname'][:-12] + '.dependent_objects'][0]) not in index[interface['shortname'][:-12] + '.aggregate_data'] and
            make_plural(camel_to_under(index[interface['shortname'][:-12] + '.dependent_objects'][0])) not in index[interface['shortname'][:-12] + '.aggregate_data'] and
            interface['shortname'][:-12] != index['package_catalog_caps'] and
            method['name'].startswith('delete_') and
            camel_to_under(interface['shortname'][:-12]) == method['name'][7:] and
            'osid.id.Id' in method['arg_types']):
            #print 'DEPENDENT', camel_to_under(index[interface['shortname'][:-12] + '.dependent_objects'][0]), index[interface['shortname'][:-12] + '.aggregate_data']
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'learning.ObjectiveAdminSession.delete_objective',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              dependent_object_name = index[interface['shortname'][:-12] + '.dependent_objects'][0],
                              cat_name = index['package_catalog_caps'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))

        ##
        # ObjectAdminSession methods that delete objects that are aggregates of 
        # the primary object administered by the session. NOTE that this checks
        # for both singular and plural forms of the object name in the method name.
        elif (interface['shortname'].endswith('AdminSession') and
            interface['shortname'][:-12] != index['package_catalog_caps'] and
            method['name'].startswith('delete_') and
            #camel_to_under(interface['shortname'][:-12]) == method['name'][7:] and
            method['name'][7:] != camel_to_under(interface['shortname'][:-12]) and
            'osid.id.Id' in method['arg_types'] and
            (method['name'][7:] in index[interface['shortname'][:-12] + '.aggregate_data'] or
            make_plural(method['name'][7:]) in index[interface['shortname'][:-12] + '.aggregate_data'])):
            #print 'FOUND DELETE', interface['shortname'], method['name']
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'repository.AssetAdminSession.delete_asset_content',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              aggregated_object_name = index['package_objects_under_to_caps'][method['name'][7:]],
                              cat_name = index['package_catalog_caps'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))

        ##
        # ObjectAdminSession methods that delete objects.
        elif (interface['shortname'].endswith('AdminSession') and
            interface['shortname'][:-12] != index['package_catalog_caps'] and
            method['name'].startswith('delete_') and
            camel_to_under(interface['shortname'][:-12]) == method['name'][7:] and
            'osid.id.Id' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceAdminSession.delete_resource',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              cat_name = index['package_catalog_caps'],
                              arg0_name = method['args'][0]['var_name'],
                              arg0_type_full = method['args'][0]['arg_type']))

        ##
        # ObjectAdminSession methods that delete all objects.
        elif (interface['shortname'].endswith('AdminSession') and
            interface['shortname'][:-12] != index['package_catalog_caps'] and
            method['name'].startswith('delete_') and
            camel_to_under(interface['shortname'][:-12]) == remove_plural(method['name'][7:])):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'learning.ProficiencyAdminSession.delete_proficiencies',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12]))

        ##
        # ObjectAdminSession methods that alias objects.
        elif (interface['shortname'].endswith('AdminSession') and
            interface['shortname'][:-12] != index['package_catalog_caps'] and
            method['name'].startswith('alias_') and
            camel_to_under(interface['shortname'][:-12]) == method['name'][6:]):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceAdminSession.alias_resource',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-12],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name']))


        ##################################################################
        ## Catch the get_hierarchy and get_hierarchy_id methods         ##
        ##################################################################

        ##
        # ObjectHierarchySession methods that return hierarchy id.
        elif ('Hierarchy' in interface['shortname'] and
              method['name'].startswith('get_') and
              method['name'].endswith('_hierarchy_id')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchySession.get_subject_hierarchy_id',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-16],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type']))

        ##
        # ObjectHierarchySession methods that return hierarchy.
        elif ('Hierarchy' in interface['shortname'] and
              method['name'].startswith('get_') and
              method['name'].endswith('_hierarchy')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchySession.get_subject_hierarchy',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-16],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type']))

        ##################################################################
        ## Inspect this package's ObjectHierarchySession methods.       ##
        ##################################################################

        ##
        # ObjectHierarchySession methods that return an authorization hint.
        elif (interface['shortname'].endswith('HierarchySession') and
              method['name'].startswith('can_access') and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchySession.can_access_subject_hierarchy',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-16],
                              var_name = method['name']))

        ##
        # ObjectHierarchySession methods that return root ids.
        elif (interface['shortname'].endswith('HierarchySession') and
              method['name'].startswith('get_root_') and
              method['name'].endswith('_ids')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchySession.get_root_subject_ids',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-16],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type']))

        ##
        # ObjectHierarchySession methods that return roots.
        elif (interface['shortname'].endswith('HierarchySession') and
              method['name'].startswith('get_root_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchySession.get_root_subjects',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-16],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type']))

        ##
        # ObjectHierarchySession methods that checks whether an object
        # has a parent.
        elif (interface['shortname'].endswith('HierarchySession') and
              method['name'].startswith('has_parent_') and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchySession.has_parent_subjects',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-16],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name']))
                              
        ##
        # ObjectHierarchySession methods that checks whether one object
        # is the parent of another.
        elif (interface['shortname'].endswith('HierarchySession') and
              method['name'].startswith('is_parent_of') and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchySession.is_parent_of_subject',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-16],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name']))
                              
        ##
        # ObjectHierarchySession methods that return parent ids.
        elif (interface['shortname'].endswith('HierarchySession') and
              method['name'].startswith('get_parent_') and
              method['name'].endswith('_ids')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchySession.get_parent_subject_ids',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-16],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # ObjectHierarchySession methods that return parents.
        elif (interface['shortname'].endswith('HierarchySession') and
              method['name'].startswith('get_parent_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchySession.get_parent_subjects',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-16],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # ObjectHierarchySession methods that checks whether one object
        # is an ancestor of another.
        elif (interface['shortname'].endswith('HierarchySession') and
              method['name'].startswith('is_ancestor_of') and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchySession.is_ancestor_of_subject',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-16],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name']))
                              
        ##
        # ObjectHierarchySession methods that checks whether an object
        # has a child.
        elif (interface['shortname'].endswith('HierarchySession') and
              method['name'].startswith('has_child_') and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchySession.has_child_subjects',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-16],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name']))
                              
        ##
        # ObjectHierarchySession methods that checks whether one object
        # is the child of another.
        elif (interface['shortname'].endswith('HierarchySession') and
              method['name'].startswith('is_child_of') and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchySession.is_child_of_subject',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-16],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name']))
                              
        ##
        # ObjectHierarchySession methods that return child ids.
        elif (interface['shortname'].endswith('HierarchySession') and
              method['name'].startswith('get_child_') and
              method['name'].endswith('_ids')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchySession.get_child_subject_ids',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-16],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # ObjectHierarchySession methods that return children.
        elif (interface['shortname'].endswith('HierarchySession') and
              method['name'].startswith('get_child_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchySession.get_child_subjects',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-16],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name']))

        ##
        # ObjectHierarchySession methods that checks whether one object
        # is a descendant of another.
        elif (interface['shortname'].endswith('HierarchySession') and
              method['name'].startswith('is_descendant_of') and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchySession.is_descendant_of_subject',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-16],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name']))
                              
        ##
        # ObjectHierarchySession methods that return Node ids.
        elif (interface['shortname'].endswith('HierarchySession') and
              method['name'].startswith('get_') and
              method['name'].endswith('_node_ids')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchySession.get_subject_node_ids',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-16],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name'],
                              arg2_name = method['args'][2]['var_name'],
                              arg3_name = method['args'][3]['var_name']))

        ##
        # ObjectHierarchySession methods that return Nodes.
        elif (interface['shortname'].endswith('HierarchySession') and
              method['name'].startswith('get_') and
              method['name'].endswith('_nodes')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchySession.get_subject_nodes',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name = interface['shortname'][:-16],
                              cat_name = index['package_catalog_caps'],
                              return_type_full = method['return_type'],
                              arg0_name = method['args'][0]['var_name'],
                              arg1_name = method['args'][1]['var_name'],
                              arg2_name = method['args'][2]['var_name'],
                              arg3_name = method['args'][3]['var_name']))


        ##################################################################
        ## Inspect this package's ObjectHierarchyDesignSession methods. ##
        ##################################################################

        ##
        # ObjectHierarchyDesignSession methods that return an authorization hint.
        elif (interface['shortname'].endswith('HierarchyDesignSession') and
              method['name'].startswith('can_modify') and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchyDesignSession.can_modify_subject_hierarchy',
                kwargs = make_twargs(index, package, interface, method, 
                    rtype=True, object_name=interface['shortname'][:-22]))

        ##
        # ObjectHierarchyDesignSession methods that add roots.
        elif (interface['shortname'].endswith('HierarchyDesignSession') and
              method['name'].startswith('add_root_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchyDesignSession.add_root_subject',
                kwargs = make_twargs(index, package, interface, method, 
                    rtype=False, object_name=interface['shortname'][:-22], arg_count=1))

        ##
        # ObjectHierarchyDesignSession methods that remove roots.
        elif (interface['shortname'].endswith('HierarchyDesignSession') and
              method['name'].startswith('remove_root_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchyDesignSession.remove_root_subject',
                kwargs = make_twargs(index, package, interface, method, 
                    rtype=False, object_name=interface['shortname'][:-22], arg_count=1))

        ##
        # ObjectHierarchyDesignSession methods that add a child.
        elif (interface['shortname'].endswith('HierarchyDesignSession') and
              method['name'].startswith('add_child_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchyDesignSession.add_child_subject',
                kwargs = make_twargs(index, package, interface, method, 
                    rtype=False, object_name=interface['shortname'][:-22], arg_count=2))

        ##
        # ObjectHierarchyDesignSession methods that remove a child.
        elif (interface['shortname'].endswith('HierarchyDesignSession') and
              method['name'].startswith('remove_child_') and
              len(method['args']) == 2):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchyDesignSession.remove_child_subject',
                kwargs = make_twargs(index, package, interface, method, 
                    rtype=False, object_name=interface['shortname'][:-22], arg_count=2))

        ##
        # ObjectHierarchyDesignSession methods that remove children.
        elif (interface['shortname'].endswith('HierarchyDesignSession') and
              method['name'].startswith('remove_child_') and
              len(method['args']) == 1):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'ontology.SubjectHierarchyDesignSession.remove_child_subjects',
                kwargs = make_twargs(index, package, interface, method, 
                    rtype=False, object_name=interface['shortname'][:-22], arg_count=1))


        ##################################################################
        ## Inspect this package's catalog notification methods.         ##
        ##################################################################

        ##
        # CatalogNotificationSession methods that return an authorization hint.
        elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'NotificationSession') and
              method['name'].startswith('can_register_for_') and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinNotificationSession.can_register_for_bin_notifications',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=False,
                    object_name=interface['shortname'].replace('NotificationSession', '')))


        ##################################################################
        ## Inspect this package's object notification methods.          ##
        ##################################################################

        ##
        # ObjectNotificationSession methods that return an authorization hint.
        elif (interface['shortname'].endswith('NotificationSession') and
              method['name'].startswith('can_register_for_') and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceNotificationSession.can_register_for_resource_notifications',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=True,
                    object_name=interface['shortname'].replace('NotificationSession', '')))

        ##
        # ObjectNotificationSession methods that acknowledge notification.
        elif (interface['shortname'].endswith('NotificationSession') and
              method['name'].startswith('acknowledge_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceNotificationSession.acknowledge_resource_notification',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=False,
                    object_name=interface['shortname'].replace('NotificationSession', ''),
                    arg_count=1))

        ##
        # ObjectNotificationSession methods that register for a new object.
        elif (interface['shortname'].endswith('NotificationSession') and
              method['name'].startswith('register_for_new_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceNotificationSession.register_for_new_resources',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=False,
                    object_name=interface['shortname'].replace('NotificationSession', '')))

        ##
        # ObjectNotificationSession methods that register for a changed object.
        elif (interface['shortname'].endswith('NotificationSession') and
              method['name'].startswith('register_for_changed_') and
              len(method['args']) == 1):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceNotificationSession.register_for_changed_resource',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=False,
                    object_name=interface['shortname'].replace('NotificationSession', ''),
                    arg_count=1))

        ##
        # ObjectNotificationSession methods that register changed objects.
        elif (interface['shortname'].endswith('NotificationSession') and
              method['name'].startswith('register_for_changed_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceNotificationSession.register_for_changed_resources',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=False,
                    object_name=interface['shortname'].replace('NotificationSession', '')))

        ##
        # ObjectNotificationSession methods that register for a deleted object.
        elif (interface['shortname'].endswith('NotificationSession') and
              method['name'].startswith('register_for_deleted_') and
              len(method['args']) == 1):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceNotificationSession.register_for_deleted_resource',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=False,
                    object_name=interface['shortname'].replace('NotificationSession', ''),
                    arg_count=1))

        ##
        # ObjectNotificationSession methods that register deleted objects.
        elif (interface['shortname'].endswith('NotificationSession') and
              method['name'].startswith('register_for_deleted_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceNotificationSession.register_for_deleted_resources',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=False,
                    object_name=interface['shortname'].replace('NotificationSession', '')))


        ##################################################################
        ## Inspect this package's Object-Catalog methods.               ##
        ##################################################################

        ##
        # ObjectCatalogSession methods that return an authorization hint.
        elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'Session') and
              'Smart' not in interface['shortname'] and 
              method['name'].startswith('can_lookup_') and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceBinSession.can_lookup_resource_bin_mappings',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=True,
                    object_name=interface['shortname'].replace(index['package_catalog_caps'] + 'Session', '')))

        ##
        # ObjectCatalogSession methods that return object ids by catalog.
        elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'Session') and
              'Smart' not in interface['shortname'] and 
              method['name'].endswith('by_' + index['package_catalog_under']) and
              method['return_type'] == 'osid.id.IdList'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceBinSession.get_resource_ids_by_bin',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=True,
                    object_name=interface['shortname'].replace(index['package_catalog_caps'] + 'Session', ''),
                    arg_count=1))

        ##
        # ObjectCatalogSession methods that return objects by catalog.
        elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'Session') and
              'Smart' not in interface['shortname'] and 
              method['name'].endswith('by_' + index['package_catalog_under']) and
              method['return_type'] != 'osid.id.IdList'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceBinSession.get_resources_by_bin',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=True,
                    object_name=interface['shortname'].replace(index['package_catalog_caps'] + 'Session', ''),
                    arg_count=1))

        ##
        # ObjectCatalogSession methods that return object ids by multiple catalogs.
        elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'Session') and
              'Smart' not in interface['shortname'] and 
              method['name'].endswith('by_' + make_plural(index['package_catalog_under'])) and
              method['return_type'] == 'osid.id.IdList'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceBinSession.get_resource_ids_by_bins',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=True,
                    object_name=interface['shortname'].replace(index['package_catalog_caps'] + 'Session', ''),
                    arg_count=1))

        ##
        # ObjectCatalogSession methods that return objects by multiple catalogs.
        elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'Session') and
              'Smart' not in interface['shortname'] and 
              method['name'].endswith('by_' + make_plural(index['package_catalog_under'])) and
              method['return_type'] != 'osid.id.IdList'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceBinSession.get_resources_by_bins',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=True,
                    object_name=interface['shortname'].replace(index['package_catalog_caps'] + 'Session', ''),
                    arg_count=1))

        ##
        # ObjectCatalogSession methods that return catalog ids by object.
        elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'Session') and
              'Smart' not in interface['shortname'] and 
              method['name'].startswith('get_' + index['package_catalog_under'] + '_ids') and
              method['return_type'] == 'osid.id.IdList'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceBinSession.get_bin_ids_by_resource',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=True,
                    object_name=interface['shortname'].replace(index['package_catalog_caps'] + 'Session', ''),
                    arg_count=1))

        ##
        # ObjectCatalogSession methods that return catalogs by object.
        elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'Session') and
              'Smart' not in interface['shortname'] and 
              method['name'].startswith('get_' + make_plural(index['package_catalog_under'])) and
              method['return_type'] != 'osid.id.IdList'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceBinSession.get_bins_by_resource',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=True,
                    object_name=interface['shortname'].replace(index['package_catalog_caps'] + 'Session', ''),
                    arg_count=1))




        ##################################################################
        ## Inspect this package's Object-Catalog Assignment methods.    ##
        ##################################################################

        ##
        # ObjectCatalogAssignmentSession methods that return a basic authorization hint.
        elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'AssignmentSession') and
              method['name'].startswith('can_assign_') and
              '_to_' not in method['name'] and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceBinAssignmentSession.can_assign_resources',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=True,
                    object_name=interface['shortname'].replace(index['package_catalog_caps'] + 'AssignmentSession', '')))

        ##
        # ObjectCatalogAssignmentSession methods that return authorization hint specific to assignable catalogs.
        elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'AssignmentSession') and
              method['name'].startswith('can_assign_') and
              method['name'].endswith('_to_' + index['package_catalog_under']) and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceBinAssignmentSession.can_assign_resources_to_bin',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=True,
                    object_name=interface['shortname'].replace(index['package_catalog_caps'] + 'AssignmentSession', ''),
                    arg_count=1))

        ##
        # ObjectCatalogAssignmentSession methods that return assignable catalogs.
        elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'AssignmentSession') and
              method['name'].startswith('get_assignable_') and
              '_for_' not in method['name'] and
              method['return_type'] == 'osid.id.IdList'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceBinAssignmentSession.get_assignable_bin_ids',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=True,
                    object_name=interface['shortname'].replace(index['package_catalog_caps'] + 'AssignmentSession', ''),
                    arg_count=1))

        ##
        # ObjectCatalogAssignmentSession methods that return assignable catalogs for object.
        elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'AssignmentSession') and
              method['name'].startswith('get_assignable_') and
              '_for_' in method['name'] and
              method['return_type'] == 'osid.id.IdList'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceBinAssignmentSession.get_assignable_bin_ids_for_resource',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=True,
                    object_name=interface['shortname'].replace(index['package_catalog_caps'] + 'AssignmentSession', ''),
                    arg_count=2))

        ##
        # ObjectCatalogAssignmentSession methods that assigns an object to a catalog.
        elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'AssignmentSession') and
              method['name'].startswith('assign_') and
              method['name'].endswith('_to_' + index['package_catalog_under'])):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceBinAssignmentSession.assign_resource_to_bin',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=False,
                    object_name=interface['shortname'].replace(index['package_catalog_caps'] + 'AssignmentSession', ''),
                    arg_count=2))

        ##
        # ObjectCatalogAssignmentSession methods that unassign an object from a catalog.
        elif (interface['shortname'].endswith(index['package_catalog_caps'] + 'AssignmentSession') and
              method['name'].startswith('unassign_') and
              method['name'].endswith('_from_' + index['package_catalog_under'])):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceBinAssignmentSession.unassign_resource_from_bin',
                kwargs = make_twargs(
                    index,
                    package,
                    interface,
                    method, 
                    rtype=False,
                    object_name=interface['shortname'].replace(index['package_catalog_caps'] + 'AssignmentSession', ''),
                    arg_count=2))



        ##################################################################
        ## Inspect this package's HierarchyDesignSession methods.       ##
        ##################################################################

        ##
        # ObjectRequisiteSession methods that return an authorization hint.
        elif (interface['shortname'].endswith('HierarchyDesignSession') and
              method['name'].startswith('can_lookup_') and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'learning.ObjectiveRequisiteSession.can_lookup_objective_prerequisites',
                kwargs = make_twargs(index, package, interface, method, 
                    rtype=True, object_name=interface['shortname'][:-22]))

        ##
        # ObjectRequisiteSession methods that return immediate requisites.
        elif (interface['shortname'].endswith('RequisiteSession') and
              method['name'].startswith('get_requisite_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'learning.ObjectiveRequisiteSession.get_requisite_objectives',
                kwargs = make_twargs(index, package, interface, method, 
                    rtype=True, object_name=interface['shortname'][:-16], arg_count=1))

        ##
        # ObjectRequisiteSession methods that all requisites.
        elif (interface['shortname'].endswith('RequisiteSession') and
              method['name'].startswith('get_all_requisite_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'learning.ObjectiveRequisiteSession.get_all_requisite_objectives',
                kwargs = make_twargs(index, package, interface, method, 
                    rtype=True, object_name=interface['shortname'][:-16], arg_count=1))

        ##
        # ObjectRequisiteSession methods that return immediate dependent.
        elif (interface['shortname'].endswith('RequisiteSession') and
              method['name'].startswith('get_dependent_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'learning.ObjectiveRequisiteSession.get_dependent_objectives',
                kwargs = make_twargs(index, package, interface, method, 
                    rtype=True, object_name=interface['shortname'][:-16], arg_count=1))

        ##
        # ObjectRequisiteSession methods that checks whether one object
        # is required by another.
        elif (interface['shortname'].endswith('RequisiteSession') and
              method['name'].startswith('is_') and
              method['name'].endswith('_required')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'learning.ObjectiveRequisiteSession.is_objective_required',
                kwargs = make_twargs(index, package, interface, method, 
                    rtype=True, object_name=interface['shortname'][:-16], arg_count=2))

        ##
        # ObjectRequisiteSession methods that return equivanent objectives for
        # the purpose of following requisites.
        elif (interface['shortname'].endswith('RequisiteSession') and
              method['name'].startswith('get_equivalent_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'learning.ObjectiveRequisiteSession.get_equivalent_objectives',
                kwargs = make_twargs(index, package, interface, method, 
                    rtype=True, object_name=interface['shortname'][:-16], arg_count=1))

        ######################################################################
        ## Inspect this package's ObjectRequisiteAssignmentSession methods. ##
        ######################################################################

        ##
        # ObjectRequisiteAssignmentSession methods that return an authorization hint.
        elif (interface['shortname'].endswith('RequisiteAssignmentSession') and
              method['name'].startswith('can_assign') and
              method['return_type'] == 'boolean'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'learning.ObjectiveRequisiteAssignmentSession.can_assign_requisites',
                kwargs = make_twargs(index, package, interface, method, 
                    rtype=True, object_name=interface['shortname'][:-26]))

        ##
        # ObjectRequisiteAssignmentSession methods that assign a requisite.
        elif (interface['shortname'].endswith('RequisiteAssignmentSession') and
              method['name'].startswith('assign_') and
              method['name'].endswith('_requisite')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'learning.ObjectiveRequisiteAssignmentSession.assign_objective_requisite',
                kwargs = make_twargs(index, package, interface, method, 
                    rtype=False, object_name=interface['shortname'][:-26], arg_count=2))

        ##
        # ObjectRequisiteAssignmentSession methods that unassign a requisite.
        elif (interface['shortname'].endswith('RequisiteAssignmentSession') and
              method['name'].startswith('unassign_') and
              method['name'].endswith('_requisite')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'learning.ObjectiveRequisiteAssignmentSession.unassign_objective_requisite',
                kwargs = make_twargs(index, package, interface, method, 
                    rtype=False, object_name=interface['shortname'][:-26], arg_count=2))

        ##
        # ObjectRequisiteAssignmentSession methods that assigns equivalent.
        elif (interface['shortname'].endswith('RequisiteAssignmentSession') and
              method['name'].startswith('assign_equivalent_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'learning.ObjectiveRequisiteAssignmentSession.assign_equivalent_objective',
                kwargs = make_twargs(index, package, interface, method, 
                    rtype=False, object_name=interface['shortname'][:-26], arg_count=2))

        ##
        # ObjectRequisiteAssignmentSession methods that unassigns equivalent.
        elif (interface['shortname'].endswith('RequisiteAssignmentSession') and
              method['name'].startswith('unassign_equivalent_')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'learning.ObjectiveRequisiteAssignmentSession.unassign_equivalent_objective',
                kwargs = make_twargs(index, package, interface, method, 
                    rtype=False, object_name=interface['shortname'][:-26], arg_count=2))



        ##################################################################
        ## Inspect the generic Session methods for this package.        ##
        ##################################################################

        ##
        # Session methods that return the Id of the associated catalog.
        # THIS IS ALSO CHECKED FURTHER UP. DO WE NEED IT HERE?
        elif (method['name'] == 'get_' + index['package_catalog_under'] + '_id' and
            method['return_type'] == 'osid.id.Id'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceLookupSession.get_bin_id',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name'][4:],
                              return_type_full = method['return_type']))

        ##
        # Session methods that set comparative catalog views.
        elif (method['name'].startswith('use_comparative') and
              method['name'].endswith(index['package_catalog_under'] + '_view')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinLookupSession.use_comparative_bin_view',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              cat_name = index['package_catalog_caps'],
                              var_name = 'comparative_view'))

        ##
        # Session methods that set plenary catalog views.
        elif (method['name'].startswith('use_plenary') and
              method['name'].endswith(index['package_catalog_under'] + '_view')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.BinLookupSession.use_plenary_bin_view',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              cat_name = index['package_catalog_caps'],
                              var_name = 'plenary_view'))

        ##
        # Session methods that set comparative object views.
        elif method['name'].startswith('use_comparative'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceLookupSession.use_comparative_resource_view',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name_under = method['name'].split('_comparative_')[1][:-5],
                              var_name = 'comparative_view'))

        ##
        # Session methods that set plenary object views.
        elif method['name'].startswith('use_plenary'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceLookupSession.use_plenary_resource_view',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              object_name_under = method['name'].split('_plenary_')[1][:-5],
                              var_name = 'plenary_view'))

        ##
        # Session methods that set federated catalog views.
        elif (method['name'].startswith('use_federated') and
              method['name'].endswith(index['package_catalog_under'] + '_view')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceLookupSession.use_federated_bin_view',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              cat_name = index['package_catalog_caps'],
                              var_name = 'federated_vew'))

        ##
        # Session methods that set isolated catalog views.
        elif (method['name'].startswith('use_isolated') and
              method['name'].endswith(index['package_catalog_under'] + '_view')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceLookupSession.use_isolated_bin_view',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              cat_name = index['package_catalog_caps'],
                              var_name = 'isolated_view'))

        ##
        # Session methods that set reliable notifications.
        elif method['name'].startswith('reliable'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceNotificationSession.reliable_resource_notifications',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              cat_name = index['package_catalog_caps'],
                              var_name = 'reliable'))

        ##
        # Session methods that set unreliable notifications.
        elif method['name'].startswith('unreliable'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceNotificationSession.unreliable_resource_notifications',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              cat_name = index['package_catalog_caps'],
                              var_name = 'reliable'))




        ##################################################################
        ## Finally create map entry for any Session methods that can't  ##
        ## identified, and give hem an empty pattern string.            ##
        ##################################################################

        else:
            
            ## Uncomment the following line to print all unknown session patterns
            #print 'unknown session pattern:', interface['fullname'], method['name']
            index[interface['shortname'] + '.' + method['name']] = dict(
                  pattern = '',
                  kwargs = dict(interface_name = interface['shortname'],
                                package_name = package['name'],
                                module_name = interface['category'],
                                method_name = method['name']))  
            index['impl_log']['sessions'][interface['shortname']][method['name']][0] = 'unmapped'
    return index
