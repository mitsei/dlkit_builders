
LOOKUP_STYLE_SESSIONS = ['LookupSession', 'QuerySession']


def map_manager_patterns(interface, package, index):
    if interface['shortname'].endswith('Profile'):
        index[interface['shortname'] + '.init_pattern'] = 'osid_managers.GenericProfile'
    if interface['shortname'].endswith('Manager'):
        index[interface['shortname'] + '.init_pattern'] = 'osid_managers.GenericManager'
    if interface['shortname'].endswith('ProxyManager'):
        index[interface['shortname'] + '.init_pattern'] = 'osid_managers.GenericProxyManager'

    for method in interface['methods']:

        index['impl_log']['managers'][interface['shortname']][method['name']] = ['mapped', 'unimplemented']
        lookup_style = False
        for session_type in LOOKUP_STYLE_SESSIONS:
            # Is there a better way to find the oddballs here?
            if (method['return_type'].split('.')[-1].endswith(session_type) and
                    (index['package_catalog_caps'] not in method['return_type'].split('.')[-1] or
                     method['return_type'].split('.')[-1].startswith('LogEntry') or
                     method['return_type'].split('.')[-1].startswith('GradebookColumn'))):
                lookup_style = True
                object_name = (method['return_type']).split('.')[-1][:-len(session_type)]

        ##################################################################
        #  First check this packages Profile methods.                   ##
        ##################################################################

        # Profile methods that test whether visible federation is supported.
        if method['name'] == 'supports_visible_federation':
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericProfile.supports_visible_federation',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name']))

        # Profile methods that test whether a particular session is supported.
        elif (method['name'].startswith('supports') and
                method['return_type'] == 'boolean' and
                not method['args']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericProfile.supports_object_lookup',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name']))

        # Profile methods that test whether a particulaar record Type is supported.
        elif (method['name'].startswith('supports') and
                method['name'].endswith('record_type') and
                method['return_type'] == 'boolean' and
                'osid.type.Type' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericProfile.supports_object_record_type',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][9:],
                            object_name_under=method['name'][9:-12],
                            arg0_name=method['args'][0]['var_name']))

        # Profile methods to get the supported record Types.
        elif (method['name'].startswith('get') and
                method['name'].endswith('record_types') and
                method['return_type'] == 'osid.type.TypeList'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericProfile.get_object_record_types',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][4:],
                            object_name_under=method['name'][4:-13]))

        # Profile methods that test whether a particulaar Type is supported.
        elif (method['name'].startswith('supports') and
                method['name'].endswith('type') and
                method['return_type'] == 'boolean' and
                'osid.type.Type' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='repository.RepositoryProfile.supports_coordinate_type',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][9:],
                            arg0_name=method['args'][0]['var_name']))

        # Profile methods to get the supported Types.
        elif (method['name'].startswith('get') and
                method['name'].endswith('types') and
                method['return_type'] == 'osid.type.TypeList'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='repository.RepositoryProfile.get_coordinate_types',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][4:]))

        ##################################################################
        #  Next, inspect this package's ProxyManager methods.           ##
        ##################################################################

        # ProxyManager methods to get a notification session with no catalog.
        elif (method['name'].startswith('get') and
                method['name'].endswith('notification_session') and
                method['return_type'].endswith('Session') and
                'osid.proxy.Proxy' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericProxyManager.get_object_notification_session',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][4:],
                            support_check=method['name'][4:].split('_session')[0],
                            arg0_name=method['args'][0]['var_name'],
                            arg1_name=method['args'][1]['var_name'],
                            return_type_full=method['return_type'],
                            cat_name=index['package_catalog_caps']))

        # ProxyManager methods to get a notification session for catalog.
        elif (method['name'].startswith('get') and
                method['name'].endswith('notification_session_for_' + index['package_catalog_under']) and
                method['return_type'].endswith('Session') and
                'osid.proxy.Proxy' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericProxyManager.get_object_notification_session_for_catalog',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][4:],
                            support_check=method['name'][4:].split('_session')[0],
                            arg0_name=method['args'][0]['var_name'],
                            arg1_name=method['args'][1]['var_name'],
                            arg2_name=method['args'][2]['var_name'],
                            return_type_full=method['return_type'],
                            cat_name=index['package_catalog_caps']))

        # ProxyManager methods to get an object lookup style session.
        elif (lookup_style and
                method['name'].startswith('get') and
                method['name'].endswith('session') and
                method['return_type'].endswith('Session') and
                'osid.proxy.Proxy' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericProxyManager.get_object_lookup_session',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][4:],
                            support_check=method['name'][4:].split('_session')[0],
                            arg0_name=method['args'][0]['var_name'],
                            return_type_full=method['return_type'],
                            object_name=object_name,
                            cat_name=index['package_catalog_caps']))

        # ProxyManager methods to get an object lookup style session for catalog.
        elif (lookup_style and
                method['name'].startswith('get') and
                method['name'].endswith(index['package_catalog_under']) and
                method['return_type'].endswith('Session') and
                'osid.proxy.Proxy' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericProxyManager.get_object_lookup_session_for_catalog',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][4:],
                            support_check=method['name'][4:].split('_session')[0],
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type'],
                            arg1_name=method['args'][1]['var_name'],
                            arg1_type_full=method['args'][1]['arg_type'],
                            return_type_full=method['return_type'],
                            object_name=object_name,
                            cat_name=index['package_catalog_caps']))

        # ProxyManager methods to get a session.
        elif (method['name'].startswith('get') and
                method['name'].endswith('session') and
                method['return_type'].endswith('Session') and
                'osid.proxy.Proxy' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericProxyManager.get_object_lookup_session',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][4:],
                            support_check=method['name'][4:].split('_session')[0],
                            arg0_name=method['args'][0]['var_name'],
                            return_type_full=method['return_type'],
                            cat_name=index['package_catalog_caps']))

        # ProxyManager methods to get a session for catalog.
        elif (method['name'].startswith('get') and
                method['name'].endswith(index['package_catalog_under']) and
                method['return_type'].endswith('Session') and
                'osid.proxy.Proxy' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericProxyManager.get_object_lookup_session_for_catalog',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][4:],
                            support_check=method['name'][4:].split('_session')[0],
                            arg0_name=method['args'][0]['var_name'],
                            arg0_type_full=method['args'][0]['arg_type'],
                            arg1_name=method['args'][1]['var_name'],
                            arg1_type_full=method['args'][1]['arg_type'],
                            return_type_full=method['return_type'],
                            cat_name=index['package_catalog_caps']))

        # ProxyManager methods to get manager for a related service
        elif (method['name'].startswith('get') and
                method['name'].endswith('proxy_manager')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericProxyManager.get_object_batch_proxy_manager',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][4:],
                            support_check=method['name'][4:].split('_proxy_manager')[0],
                            return_type_full=method['return_type']))

        ##################################################################
        #  Next, inspect this package's Manager methods.                ##
        ##################################################################

        # Manager methods to get a smart catalog session.
        elif (method['name'].startswith('get') and
                method['name'].endswith('smart_' + index['package_catalog_under'] + '_session') and
                method['return_type'].endswith('Session')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericManager.get_object_smart_catalog_session',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][4:],
                            support_check=method['name'][4:].split('_session')[0],
                            arg0_name=method['args'][0]['var_name'],
                            return_type_full=method['return_type'],
                            cat_name=index['package_catalog_caps']))

        # Manager methods to get a notification session with no catalog.
        elif (method['name'].startswith('get') and
                method['name'].endswith('notification_session') and
                method['return_type'].endswith('Session')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericManager.get_object_notification_session',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][4:],
                            support_check=method['name'][4:].split('_session')[0],
                            arg0_name=method['args'][0]['var_name'],
                            return_type_full=method['return_type'],
                            cat_name=index['package_catalog_caps']))

        # Manager methods to get a notification session for catalog.
        elif (method['name'].startswith('get') and
                method['name'].endswith('notification_session_for_' + index['package_catalog_under']) and
                method['return_type'].endswith('Session')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericManager.get_object_notification_session_for_catalog',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][4:],
                            support_check=method['name'][4:].split('_session')[0],
                            arg0_name=method['args'][0]['var_name'],
                            arg1_name=method['args'][1]['var_name'],
                            return_type_full=method['return_type'],
                            cat_name=index['package_catalog_caps']))

        # Manager methods to get an object lookup style session with no catalog.
        elif (lookup_style and
                method['name'].startswith('get') and
                method['name'].endswith('session') and
                method['return_type'].endswith('Session')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericManager.get_object_lookup_session',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][4:],
                            support_check=method['name'][4:].split('_session')[0],
                            return_type_full=method['return_type'],
                            object_name=object_name,
                            cat_name=index['package_catalog_caps']))

        # Manager methods to get an object lookup style session for catalog.
        elif (lookup_style and
                method['name'].startswith('get') and
                method['name'].endswith(index['package_catalog_under']) and
                method['return_type'].endswith('Session')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericManager.get_object_lookup_session_for_catalog',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][4:],
                            support_check=method['name'][4:].split('_session')[0],
                            arg0_name=method['args'][0]['var_name'],
                            return_type_full=method['return_type'],
                            object_name=object_name,
                            cat_name=index['package_catalog_caps']))

        # Manager methods to get session with no catalog.
        elif (method['name'].startswith('get') and
                method['name'].endswith('session') and
                method['return_type'].endswith('Session')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericManager.get_object_admin_session',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][4:],
                            support_check=method['name'][4:].split('_session')[0],
                            return_type_full=method['return_type'],
                            cat_name=index['package_catalog_caps']))

        # Manager methods to get a session for catalog.
        elif (method['name'].startswith('get') and
                method['name'].endswith(index['package_catalog_under']) and
                method['return_type'].endswith('Session')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericManager.get_object_admin_session_for_catalog',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][4:],
                            support_check=method['name'][4:].split('_session')[0],
                            arg0_name=method['args'][0]['var_name'],
                            return_type_full=method['return_type'],
                            cat_name=index['package_catalog_caps']))

        # Manager methods to get manager for a related service
        elif (method['name'].startswith('get') and
                method['name'].endswith('manager')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='osid_managers.GenericManager.get_object_batch_manager',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name'],
                            var_name=method['name'][4:],
                            support_check=method['name'][4:].split('_manager')[0],
                            return_type_full=method['return_type']))

        else:
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern='',
                kwargs=dict(interface_name=interface['shortname'],
                            package_name=package['name'],
                            module_name=interface['category'],
                            method_name=method['name']))
            index['impl_log']['managers'][interface['shortname']][method['name']][0] = 'unmapped'
    return index
