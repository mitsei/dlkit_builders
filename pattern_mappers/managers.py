import string
from collections import OrderedDict
from builders.binder_helpers import camel_to_under
from builders.binder_helpers import get_interface_module
from builders.binder_helpers import make_plural
from builders.binder_helpers import remove_plural
from builders.binder_helpers import get_pkg_name
from builders.osid_meta import OSID_Language_Primitives

def map_manager_patterns(interface, package, index):
    if interface['shortname'].endswith('Profile'):
        index[interface['shortname'] + '.init_pattern'] = 'resource.ResourceProfile'
    if interface['shortname'].endswith('Manager'):
        index[interface['shortname'] + '.init_pattern'] = 'resource.ResourceManager'
    if interface['shortname'].endswith('ProxyManager'):
        index[interface['shortname'] + '.init_pattern'] = 'resource.ResourceProxyManager'

    for method in interface['methods']:
        
        index['impl_log']['managers'][interface['shortname']][method['name']] = ['mapped', 'unimplemented']

        ##################################################################
        ## First check this packages Profile methods.                   ##
        ##################################################################
        
        ##
        # Profile methods that test whether visible federation is supported.
        if method['name'] == 'supports_visible_federation':
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceProfile.supports_visible_federation',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name']))
                
        ##
        # Profile methods that test whether a particulaar session is supported.
        elif (method['name'].startswith('supports') and 
              method['return_type'] == 'boolean' and
              not method['args']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                pattern = 'resource.ResourceProfile.supports_resource_lookup',
                kwargs = dict(interface_name = interface['shortname'],
                              package_name = package['name'],
                              module_name = interface['category'],
                              method_name = method['name'],
                              var_name = method['name']))
        ##
        # Profile methods that test whether a particulaar record Type is supported.
        elif (method['name'].startswith('supports') and 
              method['name'].endswith('record_type') and
              method['return_type'] == 'boolean' and
              'osid.type.Type' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                  pattern = 'resource.ResourceProfile.supports_resource_record_type',
                  kwargs = dict(interface_name = interface['shortname'],
                                package_name = package['name'],
                                module_name = interface['category'],
                                method_name = method['name'],
                                var_name = method['name'][9:],
                                object_name_under = method['name'][9:-12],
                                arg0_name = method['args'][0]['var_name']))

        ##
        # Profile methods to get the supported record Types.
        elif (method['name'].startswith('get') and 
              method['name'].endswith('record_types') and
              method['return_type'] == 'osid.type.TypeList'):
            index[interface['shortname'] + '.' + method['name']] = dict(
                  pattern = 'resource.ResourceProfile.get_resource_record_types',
                  kwargs = dict(interface_name = interface['shortname'],
                                package_name = package['name'],
                                module_name = interface['category'],
                                method_name = method['name'],
                                var_name = method['name'][4:],
                                object_name_under = method['name'][4:-13]))



        ##################################################################
        ## Next, inspect this package's ProxyManager methods.           ##
        ##################################################################

        ##
        # ProxyManager methods to get a session.
        elif (method['name'].startswith('get') and 
              method['name'].endswith('session') and
              method['return_type'].endswith('Session') and
              'osid.proxy.Proxy' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                  pattern = 'resource.ResourceProxyManager.get_resource_lookup_session',
                  kwargs = dict(interface_name = interface['shortname'],
                                package_name = package['name'],
                                module_name = interface['category'],
                                method_name = method['name'],
                                var_name = method['name'][4:],
                                support_check = method['name'][4:].split('_session')[0],
                                arg0_name = method['args'][0]['var_name'],
                                return_type_full = method['return_type'],
                                cat_name = index['package_catalog_caps']))

        ##
        # ProxyManager methods to get a session for catalog.
        elif (method['name'].startswith('get') and 
              method['name'].endswith(index['package_catalog_under']) and
              method['return_type'].endswith('Session') and
              'osid.proxy.Proxy' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                  pattern = 'resource.ResourceProxyManager.get_resource_lookup_session_for_bin',
                  kwargs = dict(interface_name = interface['shortname'],
                                package_name = package['name'],
                                module_name = interface['category'],
                                method_name = method['name'],
                                var_name = method['name'][4:],
                                support_check = method['name'][4:].split('_session')[0],
                                arg0_name = method['args'][0]['var_name'],
                                arg0_type_full = method['args'][0]['arg_type'],
                                return_type_full = method['return_type'],
                                cat_name = index['package_catalog_caps']))

        ##
        # ProxyManager methods to get manager for a related service
        elif (method['name'].startswith('get') and 
              method['name'].endswith('proxy_manager') and
              'osid.proxy.Proxy' in method['arg_types']):
            index[interface['shortname'] + '.' + method['name']] = dict(
                  pattern = 'resource.ResourceProxyManager.get_resource_batch_proxy_manager',
                  kwargs = dict(interface_name = interface['shortname'],
                                package_name = package['name'],
                                module_name = interface['category'],
                                method_name = method['name'],
                                var_name = method['name'][4:],
                                support_check = method['name'][4:].split('_proxy_manager')[0],
                                return_type_full = method['return_type']))



        ##################################################################
        ## Next, inspect this package's Manager methods.                ##
        ##################################################################

        ##
        # Manager methods to get a smart catalog session.
        elif (method['name'].startswith('get') and 
              method['name'].endswith('smart_' + index['package_catalog_under'] + '_session') and
              method['return_type'].endswith('Session')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                  pattern = 'resource.ResourceManager.get_resource_smart_bin_session',
                  kwargs = dict(interface_name = interface['shortname'],
                                package_name = package['name'],
                                module_name = interface['category'],
                                method_name = method['name'],
                                var_name = method['name'][4:],
                                support_check = method['name'][4:].split('_session')[0],
                                arg0_name = method['args'][0]['var_name'],
                                return_type_full = method['return_type'],
                                cat_name = index['package_catalog_caps']))

        ##
        # Manager methods to get a notification session with no catalog.
        elif (method['name'].startswith('get') and 
              method['name'].endswith('notification_session') and
              method['return_type'].endswith('Session')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                  pattern = 'resource.ResourceManager.get_resource_notification_session',
                  kwargs = dict(interface_name = interface['shortname'],
                                package_name = package['name'],
                                module_name = interface['category'],
                                method_name = method['name'],
                                var_name = method['name'][4:],
                                support_check = method['name'][4:].split('_session')[0],
                                arg0_name = method['args'][0]['var_name'],
                                return_type_full = method['return_type'],
                                cat_name = index['package_catalog_caps']))

        ##
        # Manager methods to get a session for catalog.
        elif (method['name'].startswith('get') and 
              method['name'].endswith('notification_session_for_' + index['package_catalog_under']) and
              method['return_type'].endswith('Session')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                  pattern = 'resource.ResourceManager.get_resource_notification_session_for_bin',
                  kwargs = dict(interface_name = interface['shortname'],
                                package_name = package['name'],
                                module_name = interface['category'],
                                method_name = method['name'],
                                var_name = method['name'][4:],
                                support_check = method['name'][4:].split('_session')[0],
                                arg0_name = method['args'][0]['var_name'],
                                arg1_name = method['args'][1]['var_name'],
                                return_type_full = method['return_type'],
                                cat_name = index['package_catalog_caps']))
                                        
        ##
        # Manager methods to get a session with no catalog.
        elif (method['name'].startswith('get') and 
              method['name'].endswith('session') and
              method['return_type'].endswith('Session')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                  pattern = 'resource.ResourceManager.get_resource_lookup_session',
                  kwargs = dict(interface_name = interface['shortname'],
                                package_name = package['name'],
                                module_name = interface['category'],
                                method_name = method['name'],
                                var_name = method['name'][4:],
                                support_check = method['name'][4:].split('_session')[0],
                                return_type_full = method['return_type'],
                                cat_name = index['package_catalog_caps']))

        ##
        # Manager methods to get a session for catalog.
        elif (method['name'].startswith('get') and 
              method['name'].endswith(index['package_catalog_under']) and
              method['return_type'].endswith('Session')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                  pattern = 'resource.ResourceManager.get_resource_lookup_session_for_bin',
                  kwargs = dict(interface_name = interface['shortname'],
                                package_name = package['name'],
                                module_name = interface['category'],
                                method_name = method['name'],
                                var_name = method['name'][4:],
                                support_check = method['name'][4:].split('_session')[0],
                                arg0_name = method['args'][0]['var_name'],
                                return_type_full = method['return_type'],
                                cat_name = index['package_catalog_caps']))
                                        
        ##
        # Manager methods to get manager for a related service
        elif (method['name'].startswith('get') and 
              method['name'].endswith('manager')):
            index[interface['shortname'] + '.' + method['name']] = dict(
                  pattern = 'resource.ResourceManager.get_resource_batch_manager',
                  kwargs = dict(interface_name = interface['shortname'],
                                package_name = package['name'],
                                module_name = interface['category'],
                                method_name = method['name'],
                                var_name = method['name'][4:],
                                support_check = method['name'][4:].split('_manager')[0],
                                return_type_full = method['return_type']))

        else:
            ## Uncomment the following line to print all unknown manager patterns
            #print 'unknown manager pattern:', interface['fullname'], method['name']
            index[interface['shortname'] + '.' + method['name']] = dict(
                  pattern = '',
                  kwargs = dict(interface_name = interface['shortname'],
                                package_name = package['name'],
                                module_name = interface['category'],
                                method_name = method['name']))
            index['impl_log']['managers'][interface['shortname']][method['name']][0] = 'unmapped'
    return index


