# resource templates for kit_osid

class ResourceProfile:

    supports_visible_federation_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceProfile.supports_visible_federation
        return self._provider_manager.${method_name}()"""

    supports_resource_lookup_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceProfile.supports_resource_lookup
        return self._provider_manager.${method_name}()"""

#    get_resource_record_types = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceProfile.get_resource_record_types
#        return self._provider_manager.${method_name}()"""

class ResourceManager:

    init_template = """
    DEFAULT = 0
    COMPARATIVE = 0
    PLENARY = 1
    FEDERATED = 0
    ISOLATED = 1

    def __init__(self):
        import settings
        import importlib
        provider_module = importlib.import_module(settings.${pkg_name_upper}_PROVIDER_MANAGER_PATH, settings.ANCHOR_PATH)
        provider_manager_class = getattr(provider_module, '${interface_name}')
        self._provider_manager = provider_manager_class()
        self._provider_sessions = dict()
        self._views = dict()

    def _get_view(self, view):
        if view in self._views:
            return self._views[view]
        else:
            self._views[view] = DEFAULT
            return DEFAULT

    def _get_provider_session(self, session):
#        from osid_kit.osid_errors import Unimplemented
        if session in self._provider_sessions:
            return self._provider_sessions[session]
        else:
            try:
                get_session = getattr(self._provider_manager, 'get_' + session)
            except:
                raise # Unimplemented???
            else: 
                self._provider_sessions[session] = get_session()
                ## DO WE NEED THESE VIEW INITERS???
                if '${cat_name_under}_view' not in self._views:
                    self._views['${cat_name_under}_view'] = self.DEFAULT
                if self._views['${cat_name_under}_view'] == self.COMPARATIVE:
                    try:
                        self._provider_sessions[session].use_comparative_${cat_name_under}_view()
                    except AttributeError:
                        pass
                else:
                    try:
                        self._provider_sessions[session].use_plenary_${cat_name_under}_view()
                    except AttributeError:
                        pass
            return self._provider_sessions[session]

"""

    get_resource_lookup_session_managertemplate = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_manager_template
        self._provider_sessions[\'${return_type}\'] = self._provider_manager.${method_name}()
        return self"""

    get_resource_lookup_session_for_bin_managertemplate = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_manager_template
        self._provider_sessions[\'${return_type}\'] = self._provider_manager.${method_name}(${arg0_name})
        return self"""

    get_resource_lookup_session_catalogtemplate = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_catalog_template
        session = self._provider_manager.${method_name}()
        return ${cat_name}(self._provider_manager, session.get_${cat_name_under}().get_id(), ${return_type_under} = session)"""

    get_resource_lookup_session_for_bin_catalogtemplate = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_catalog_template
        session = self._provider_manager.${method_name}(${arg0_name})
        return ${cat_name}(self._provider_manager, session.get_${cat_name_under}().get_id(), ${return_type_under} = session)"""


class ResourceLookupSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session
"""

    get_bin_id_template = None

    get_bin_template = None

    can_lookup_resources_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.can_lookup_resources_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}()"""

    use_comparative_resource_view_template = """
        self._views['${object_name_under}_view'] = self.COMPARATIVE
        for session in self._provider_sessions:
            try:
                session.use_comparative_${object_name_under}_view()
            except AttributeError():
                pass"""

    use_plenary_resource_view_template = """
        self._views[\'${object_name_under}_view\'] = self.PLENARY
        for session in self._provider_sessions:
            try:
                session.use_comparative_${object_name_under}_view()
            except AttributeError():
                pass"""

    use_federated_bin_view_template = """
        self._views[\'${cat_name_under}_view\'] = self.FEDERATED
        for session in self._provider_sessions:
            try:
                session.use_comparative_${cat_name_under}_view()
            except AttributeError():
                pass"""

    use_isolated_bin_view_template = """
        self._views[\'${cat_name_under}_view\'] = self.ISOLATED
        for session in self._provider_sessions:
            try:
                session.use_comparative_${cat_name_under}_view()
            except AttributeError():
                pass"""

    get_resource_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resource_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    get_resources_by_ids_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_ids_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    get_resources_by_genus_type_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_genus_type_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    get_resources_by_parent_genus_type_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_parent_genus_type_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    get_resources_by_record_type_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_record_type_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    get_resources_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resources_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}()"""

class ResourceAdminSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session
"""

    can_create_resources_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.can_create_resources_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}()"""

    can_create_resource_with_record_types_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.can_create_resource_with_record_types_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    get_resource_form_for_create_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_create_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    create_resource_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.create_resource_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    get_resource_form_for_update_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_update_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    update_resource_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.update_resource_template
        self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    delete_resource_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.delete_resource_template
        self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    alias_resources_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.alias_resources_template
        self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name}=${arg0_name}, ${arg1_name}=${arg1_name})"""


class BinLookupSession:


    use_comparative_bin_view_template = """
        self._views[\'${cat_name_under}_view\'] = self.COMPARATIVE
        for session in self._provider_sessions:
            try:
                session.use_comparative_${cat_name_under}_view()
            except AttributeError():
                pass"""

    use_plenary_bin_view_template = """
        self._views[\'${cat_name_under}_view\'] = self.PLENARY
        for session in self._provider_sessions:
            try:
                session.use_plenary_${cat_name_under}_view()
            except AttributeError():
                pass"""

#    use_comparative_bin_view_template = None

#    use_plenary_bin_view_template = None

    get_bin_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bin
#        from .objects import ${cat_name}
        return ${cat_name}(self._provider_manager, self._get_provider_session('${interface_name_under}').${method_name}(${arg0_name}))"""

    get_bins_by_ids_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_ids
#        from .objects import ${cat_name}, ${cat_name}List
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${arg0_name})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat))
        return ${cat_name}List(cat_list)"""

    get_bins_by_genus_type_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_genus_type
#        from .objects import ${cat_name}, ${cat_name}List
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${arg0_name})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat))
        return ${cat_name}List(cat_list)"""

    get_bins_by_parent_genus_type_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_parent_genus_type
#        from .objects import ${cat_name}, ${cat_name}List
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${arg0_name})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat))
        return ${cat_name}List(cat_list)"""

    get_bins_by_record_type_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_record_type
#        from .objects import ${cat_name}, ${cat_name}List
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${arg0_name})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat))
        return ${cat_name}List(cat_list)"""

    get_bins_by_provider_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_provider
#        from .objects import ${cat_name}, ${cat_name}List
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${arg0_name})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat))
        return ${cat_name}List(cat_list)"""

    get_bins_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_template
#        from .objects import ${cat_name}, ${cat_name}List
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}()
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat))
        return ${cat_name}List(cat_list)"""


class BinAdminSession:

    get_bin_form_for_create_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.get_bin_form_for_create
        return self._get_provider_session('${interface_name_under}').${method_name}(${arg0_name})"""

    create_bin_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.create_bin
#        from .objects import ${cat_name}
        return ${cat_name}(self._provider_manager, self._get_provider_session('${interface_name_under}').${method_name}(${arg0_name}))"""

    get_bin_form_for_update_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.get_bin_form_for_update
        return self._get_provider_session('${interface_name_under}').${method_name}(${arg0_name})"""

    update_bin_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.update_bin
#        from .objects import ${cat_name}
        # OSID spec does not require returning updated catalog
        return ${cat_name}(self._provider_manager, self._get_provider_session('${interface_name_under}').${method_name}(${arg0_name}))"""

    delete_bin_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.delete_bin
        self._get_provider_session('${interface_name_under}').${method_name}(${arg0_name})"""

class ResourceList:

    get_next_resource_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceList.get_next_resource
        import sys
#        from osid_kit.osid_errors import IllegalState, OperationFailed
        try:
            next_item = self.next()
        except StopIteration:
            raise IllegalState('no more elements available in this list')
        except: #Need to specify exceptions here
            raise OperationFailed()
        else:
            return next_item
            
    def next(self):
        # Implemented from kitosid template for -
        # osid.resource.ResourceList.get_next_resource
        from .osid import OsidList
        try:
            next_item = OsidList.next(self)
        except:
            raise
        return next_item"""
            
    get_next_resources_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceList.get_next_resources
        import sys
#        from osid_kit.osid_errors import IllegalState, OperationFailed
        if ${arg0_name} > self.available():
            # !!! This is not quite as specified (see method docs) !!!
            raise IllegalState('not enough elements available in this list')
        else:
            next_list = []
            x = 0
            while x < ${arg0_name}:
                try:
                    next_list.append(self.next())
                except: #Need to specify exceptions here
                    raise OperationFailed()
                x = x + 1
            return next_list"""


class Bin:

    init_template = """
    DEFAULT = 0
    COMPARATIVE = 0
    PLENARY = 1
    FEDERATED = 0
    ISOLATED = 1

                        ## THINK. WILL THIS EVER BE CALLED DIRECTLY
                        ## OUTSIDE OF A MANAGER?
    def __init__(self, provider_manager, catalog, **kwargs):
#        if provider_manager:
        self._provider_manager = provider_manager
#        else:
#            import settings
#            import importlib
#            provider_module = importlib.import_module(settings.PROVIDER_MANAGER_MODULE_PATH)
#            provider_manager_class = getattr(provider_module, '${pkg_name_caps}Manager')
#            self._provider_manager = provider_manager_class()
        self._catalog = catalog
        self._catalog_id = catalog.get_id()
        self._provider_sessions = kwargs
        self._osid_object = self._catalog # This so that the inherited osid 
                                          # methods work.  Don't ask.
        self._views = dict()

    def _get_provider_session(self, session, session_object):
#        from osid_kit.osid_errors import Unimplemented
        if session in self._provider_sessions:
            return self._provider_sessions[session]
        else:
            try:
                get_session_class = getattr(self._provider_manager, 'get_' + session + '_for_${cat_name_under}')
            except:
                raise # Unimplemented???
            else:
                self._provider_sessions[session] = get_session_class(self._catalog.get_id())
            return self._provider_sessions[session]

    def get_${cat_name_under}_id(self):
        return self._catalog_id
    
    def get_${cat_name_under}(self):
        return self

    def get_objective_hierarchy_id(self):
        return self._catalog_id
    
    def get_objective_hierarchy(self):
        return self
"""




















































class OLD_Bin: # CAN PROBABLY DELETE THIS?!?!
####################################################################################
####################################################################################
###################################################################################
    init_template = """
    COMPARATIVE = 0
    PLENARY = 1
    FEDERATED = 0
    ISOLATED = 1
###################################################################################

    def __init__(self, provider_manager, catalog=None, **kwargs):
        self._provider_manager = provider_manager
        self._provider_sessions = kwargs
        self._catalog = catalog
        self._osid_object = self._catalog # This so that the inherited osid 
                                          # methods work.  Don't ask.
        self._catalog_view = self.FEDERATED
        # THIS SHOULD BE IMPLEMENTED IN KIT BUILDER AS AN INITER?:
        self._catalog_view = self.COMPARATIVE
###################################################################################

    def _get_provider_session(self, session, session_object):
#        from osid_kit.osid_errors import Unimplemented
        if session in self._provider_sessions:
            return _provider_sessions[session]
        else:
            try:
                get_session = getattr(self._provider_manager, 'get_' + session)
            except:
                raise # Unimplemented???
            else: 
                if getattr(self, object_session + '_view', ) == self.COMPARATIVE:
                    self._provider_sessions[session].use_comparative_${object_name_under}_view()
                else:
                    self._provider_sessions[session].use_plenary_${object_name_under}_view()
                if self._catalog_view == self.FEDERATED:
                    self._provider_sessions[session].use_federated_${cat_name_under}_view()
                else:
                    self._provider_sessions[session].use_isolated_${cat_name_under}_view()
                self._provider_sessions[session] = get_session(self._catalog_id)
            return self._provider_sessions[session]
###################################################################################

    def get_${cat_name_under}_id(self):
        return self._catalog.get_id()
###################################################################################
   
    def get_${cat_name_under}(self):
        return self._catalog
${obj_view_methods}
    def use_federated_${cat_name_under}_view():
        self._catalog_view = self.FEDERATED
        for session in self._provider_sessions:
            try:
                session.use_federated_${cat_name_under}_view()
            except AttributeError():
                pass
###################################################################################

    def use_isolated_${cat_name_under}_view():
        self._catalog_view = self.ISOLATED
        for session in self._provider_sessions:
            try:
                session.use_isolated_${cat_name_under}_view()
            except AttributeError():
                pass
###################################################################################

    # THE FOLLOWING SHOULD BE IMPLEMENTED AS AN init = STYLE.  
    # BUILDERS NEED TO BE ALTERED TO ALLOW BOTH init and init_template
    def use_comparative_agent_view():
        self._object_view = self.COMPARATIVE
        for session in self._provider_sessions:
            try:
                session.use_comparative_agent_view()
            except AttributeError():
                pass
###################################################################################

    def use_plenary_agent_view():
        self._object_view = self.PLENARY
        for session in self._provider_sessions:
            try:
                session.use_plenary_agent_view()
            except AttributeError():
                pass
"""

