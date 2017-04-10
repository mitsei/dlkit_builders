class ResourceProfile:

    supports_visible_federation_template = """
        # Implemented from template for osid.resource.ResourceProfile.supports_visible_federation
        from . import profile
        return '${method_name}' in profile.SUPPORTS"""

    supports_resource_lookup_template = """
        # Implemented from template for osid.resource.ResourceProfile.supports_resource_lookup
        from . import profile
        return '${method_name}' in profile.SUPPORTS"""

    get_resource_record_types_template = """
        from ..type.primitives import Type
        from ..type.objects import TypeList
        try:
            from . import settings
            ${object_name_under}_records = settings.${object_name_under}_records
        except (ImportError, AttributeError):
            return TypeList([])
        record_types = []
        for r in ${object_name_under}_records:
            record_types.append(Type(
                authority = ${object_name_under}_records[r]['authority'],
                namespace = ${object_name_under}_records[r]['namespace'],
                identifier = ${object_name_under}_records[r]['identifier'],
                display_name = ${object_name_under}_records[r]['display_name'],
                display_label = ${object_name_under}_records[r]['display_label'],
                description = ${object_name_under}_records[r]['description'],
                domain = ${object_name_under}_records[r]['domain']
                )
            )
        return TypeList(record_types, count=len(record_types))"""

    supports_resource_record_type_template = """
        from ..type.primitives import Type
        from ..osid.osid_errors import NullArgument
        if ${arg0_name} is None:
            raise NullArgument()
        try:
            from . import settings
            ${object_name_under}_records = settings.${object_name_under}_records
        except (ImportError, AttributeError):
            return False
        supports = False
        for r in ${object_name_under}_records:
            if (${arg0_name}.get_authority() == ${object_name_under}_records[r]['authority'] and
                ${arg0_name}.get_identifier_namespace() == ${object_name_under}_records[r]['namespace'] and
                ${arg0_name}.get_identifier() == ${object_name_under}_records[r]['identifier']):
                supports = True
        return supports"""


class ResourceManager:

    get_resource_lookup_session_template = """
        from ..osid.osid_errors import OperationFailed, Unimplemented
        if not self.supports_${support_check}():
            raise Unimplemented()
        try:
            from . import ${return_module}
        except ImportError:
            raise OperationFailed()
        try:
            session = ${return_module}.${return_type}()
        except AttributeError:
            raise OperationFailed()
        return session"""

    get_resource_lookup_session_for_bin_template = """
        from ..osid.osid_errors import NotFound, NullArgument, OperationFailed, Unimplemented
        if not ${arg0_name}:
            raise NullArgument
        if not self.supports_${support_check}():
            raise Unimplemented()
        ##
        # Also include check to see if the binId is found otherwise raise NotFound
        ##
        try:
            from . import ${return_module}
        except ImportError:
            raise OperationFailed()
        try:
            session = ${return_module}.${return_type}(${arg0_name})
        except AttributeError:
            raise OperationFailed()
        return session"""


class ResourceLookupSession:

    init_template = """
    _session_name = '${interface_name}'

    def __init__(self, catalog_identifier = None, *args, **kwargs):
        from django.db.models.base import ObjectDoesNotExist
        from .models import ${cat_name} as ${cat_name}Model
        from .objects import ${cat_name}
        from ..osid.sessions import OsidSession
        from ..osid.osid_errors import NotFound
        if catalog_identifier and catalog_identifier != 'default':
            self._catalog_identifier = catalog_identifier
            try:
                self.my_catalog_model = ${cat_name}Model.objects.get(identifier=self._catalog_identifier)
            except ObjectDoesNotExist:
                raise NotFound('could not find catalog identifier ' + catalog_identifier)
            self._catalog_id = ${cat_name}(self.my_catalog_model).get_id()
        else:
            try:
                from ..id.primitives import Id
            except:
                from ..osid.common import Id
            self._catalog_identifier = 'default'
            self.my_catalog_model = self.Default${cat_name}Model(self._catalog_identifier)
            self._catalog_id = Id(identifier = self._catalog_identifier,
                                  namespace = '${pkg_name}.${cat_name}',
                                  authority = 'birdland.mit.edu')
        OsidSession.__init__(self, *args, **kwargs)
        self._object_view = self.COMPARATIVE
        self._catalog_view = self.ISOLATED

    ## PERHAPS THIS CAN GO INTO THE MODEL???
    ## OR IT MIGHT GO IN A defoult_model MODULE.
    class Default${cat_name}Model():
        def __init__(self, catalog_id):
            from . import profile
            self.identifier = catalog_id
            self.display_name = 'Default ${cat_name}'
            self.description = 'The Default ${cat_name}'
            self.genus_type_authority = 'default'
            self.genus_type_namespace = 'default'
            self.genus_type_identifier = 'default'
            self.language_type_identifier = profile.LANGUAGETYPE['identifier']
            self.script_type_identifier = profile.SCRIPTTYPE['identifier']
            self.format_type_identifier = profile.FORMATTYPE['identifier']
"""

    get_bin_id_template = """
        # Implemented from template for osid.resource.ResourceLookupSession.get_bin_id
        return self._catalog_id"""

    get_bin_template = """
        # Implemented from template for osid.resource.ResourceLookupSession.get_bin
        from ..osid.osid_errors import OperationFailed, PermissionDenied
        from .${return_module} import ${return_type}
        try:
            return ${return_type}(self.my_catalog_model)
        except:
            raise OperationFailed()"""

    can_lookup_resources_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.can_lookup_resources
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    use_comparative_resource_view_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.use_comparative_resource_view
        self._object_view = self.COMPARATIVE"""

    use_plenary_resource_view_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.use_plenary_resource_view
        self._object_view = self.PLENARY"""

    use_federated_bin_view_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.use_federated_bin_view
        self._catalog_view = self.FEDERATED"""

    use_isolated_bin_view_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.use_isolated_bin_view
        self._catalog_view = self.ISOLATED"""

    get_resource_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.get_resource
        # NOTE: This implementation currently ignores plenary view
        from django.db.models.base import ObjectDoesNotExist
        from .models import ${object_name} as ${object_name}Model
        from ..osid.osid_errors import NotFound, NullArgument, OperationFailed, PermissionDenied
        if not ${arg0_name}:
            raise NullArgument()
        if self._catalog_view == self.ISOLATED:
            try:
                result = ${object_name}Model.objects.get(identifier=${arg0_name}.get_identifier(),
                        ${object_name_under}_${cat_name_lower}__${cat_name_under}_identifier=self._catalog_identifier)
            except ObjectDoesNotExist:
                raise NotFound()
        else:
            try:
                result = ${object_name}Model.objects.get(identifier=${arg0_name}.get_identifier())
            except ObjectDoesNotExist:
                raise NotFound()
        from ..${return_app_name}.${return_djpkg_name}.${return_module} import ${return_type}
        return ${return_type}(result)"""

    get_resources_by_ids_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.get_resources_by_ids
        # NOTE: This implementation currently ignores plenary view
        from .models import ${object_name} as ${object_name}Model
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import NotFound, NullArgument, OperationFailed, PermissionDenied
        if not ${arg0_name}:
            raise NullArgument()
        t = ()
        for i in ${arg0_name}:
            t = t + (i.get_identifier(),)
        if self._catalog_view == self.ISOLATED:
            result = ${object_name}Model.objects.filter(identifier__in(t),
                    ${object_name_under}_${cat_name_lower}__${cat_name_under}_identifier=self._catalog_identifier)
            count = ${object_name}Model.objects.filter(identifier__in(t),
                    ${object_name_under}_${cat_name_lower}__${cat_name_under}_identifier=self._catalog_identifier).count()
        else:
            result = ${object_name}Model.objects.filter(identifier__in(t))
            count = ${object_name}Model.objects.filter(identifier__in(t)).count()
        return ${return_type}(result, count)"""

    get_resources_by_genus_type_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.get_resources_by_genus_type
        # NOTE: This implementation currently ignores plenary view
        from .models import ${object_name} as ${object_name}Model
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import OperationFailed, PermissionDenied
        if self._catalog_view == self.ISOLATED:
            result = ${object_name}Model.objects.filter(
                    genus_type_authority=${arg0_name}.get_authority(),
                    genus_type_namespace=${arg0_name}.get_identifier_namespace(),
                    genus_type_identifier=${arg0_name}.get_identifier(),
                    ${object_name_under}_${cat_name_lower}__${cat_name_under}_identifier=self._catalog_identifier)
            count = ${object_name}Model.objects.filter(
                    genus_type_authority=${arg0_name}.get_authority(),
                    genus_type_namespace=${arg0_name}.get_identifier_namespace(),
                    genus_type_identifier=${arg0_name}.get_identifier(),
                    ${object_name_under}_${cat_name_lower}__${cat_name_under}_identifier=self._catalog_identifier).count()
        else:
            result = ${object_name}Model.objects.filter(
                    genus_type_authority=${arg0_name}.get_authority(),
                    genus_type_namespace=${arg0_name}.get_identifier_namespace(),
                    genus_type_identifier=${arg0_name}.get_identifier())
            count = ${object_name}Model.objects.filter(
                    genus_type_authority=${arg0_name}.get_authority(),
                    genus_type_namespace=${arg0_name}.get_identifier_namespace(),
                    genus_type_identifier=${arg0_name}.get_identifier()).count()
        return ${return_type}(result, count)"""

    get_resources_by_parent_genus_type_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.get_resources_by_parent_genus_type
        # WILL THIS DEPEND ON A TYPE HIERARCHY SERVICE???
        from .${return_module} import ${return_type}
        return ${return_type}([])"""

    get_resources_by_record_type_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.get_resources_by_record_type
        # STILL NEED TO FIGURE OUT HOW TO DO RECORDS!!!
        from .${return_module} import ${return_type}
        return ${return_type}([])"""

    get_resources_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.get_resources
        # NOTE: This implementation currently ignores plenary view
        from .models import ${object_name} as ${object_name}Model
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import OperationFailed, PermissionDenied
        if self._catalog_view == self.ISOLATED:
            result = ${object_name}Model.objects.filter(
                    ${object_name_under}_${cat_name_lower}__${cat_name_under}_identifier=self._catalog_identifier)
            count = ${object_name}Model.objects.filter(
                    ${object_name_under}_${cat_name_lower}__${cat_name_under}_identifier=self._catalog_identifier).count()
        else:
            result = ${object_name}Model.objects.all()
            count = ${object_name}Model.objects.all().count()
        return ${return_type}(result, count)"""


class ResourceAdminSession:

    init_template = """
    _session_name = '${interface_name}'

    def __init__(self, catalog_identifier = None, *args, **kwargs):
        from .models import ${cat_name} as ${cat_name}Model
        from .objects import ${cat_name}
        from ..osid.sessions import OsidSession
        from ..osid.osid_errors import NotFound
        if catalog_identifier:
            self._catalog_identifier = catalog_identifier
            try:
                self.my_catalog_model = ${cat_name}Model.objects.get(identifier=self._catalog_identifier)
            except DoesNotExist:
                raise NotFound()
            self._catalog_id = ${cat_name}(self.my_catalog_model).get_id()
        else:
            try:
                from ..id.primitives import Id
            except:
                from ..osid.common import Id
            self._catalog_identifier = 'default'
            self.my_catalog_model = self.Default${cat_name}Model(self._catalog_identifier)
            # The default catalog id data may want to come from a settings file?
            self._catalog_id = Id(identifier = self._catalog_identifier,
                                  namespace = '${pkg_name}.${cat_name}',
                                  authority = 'birdland.mit.edu')
        OsidSession.__init__(self, *args, **kwargs)
        self._forms = dict()

    # PERHAPS THIS CAN GO INTO THE MODEL???
    # OR IT MIGHT GO IN A defoult_model MODULE.
    class Default${cat_name}Model():
        def __init__(self, catalog_id):
            from . import profile
            self.identifier = catalog_id
            self.display_name = 'Default ${cat_name}'
            self.description = 'The Default ${cat_name}'
            self.genus_type_authority = 'default'
            self.genus_type_namespace = 'default'
            self.genus_type_identifier = 'default'
            self.language_type_identifier = profile.LANGUAGETYPE['identifier']
            self.script_type_identifier = profile.SCRIPTTYPE['identifier']
            self.format_type_identifier = profile.FORMATTYPE['identifier']
"""

    can_create_resources_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.can_create_resources
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    can_create_resource_with_record_types_template = """
        # Implemented from template for
        # osid.resource.ResourceLookupSession.can_create_resource_with_record_types
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True"""

    get_resource_form_for_create_template = """
        from dlkit.${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from .${return_module} import ${return_type}
        from ..osid.osid_errors import NullArgument, InvalidArgument, OperationFailed, PermissionDenied, Unsupported
        CREATED = True
        if ${arg0_name} is None:
            raise NullArgument()
        for arg in ${arg0_name}:
            if not isinstance(arg, ABC${arg0_type}):
                raise InvalidArgument('one or more argument array elements is not a valid OSID ${arg0_type}')
        if ${arg0_name} == []:
            result = ${return_type}()
        else:
            raise Unsupported() # Need to deal with record types
        result._for_update = False
        self._forms[result.get_id().get_identifier()] = not CREATED
        return result"""

    create_resource_template = """
        from dlkit.${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from .models import ${object_name}_${cat_name}
        from ..osid.osid_errors import IllegalState, InvalidArgument, NullArgument, OperationFailed, PermissionDenied, Unsupported
        CREATED = True
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise InvalidArgument('argument type is not an ${arg0_type}')
        if ${arg0_name}.is_for_update():
            raise InvalidArgument('the ${arg0_type} is for update only, not create')
        try:
            if self._forms[${arg0_name}.get_id().get_identifier()] == CREATED:
                raise IllegalState('${arg0_name} already used in a create transaction')
        except KeyError:
            raise Unsupported('${arg0_name} did not originate from this session')
        if not ${arg0_name}.is_valid:
            raise InvalidArgument('one or more of the form elements is invalid')
        try:
            ${arg0_name}.my_model.save()
        except: # what exceptions does django model.save raise?
            raise OperationFailed()
        try:
            ${object_name_under}_${cat_name_lower} = ${object_name}_${cat_name}()
            ${object_name_under}_${cat_name_lower}.${object_name_under} = ${arg0_name}.my_model
            ${object_name_under}_${cat_name_lower}.${cat_name_under}_identifier = self._catalog_identifier
            ${object_name_under}_${cat_name_lower}.save()
        except: # roll back the my_model.save()
            ${arg0_name}.my_model.delete()
            raise OperationFailed()
        from .${return_module} import ${return_type}
        result = ${return_type}(${arg0_name}.my_model)
        self._forms[${arg0_name}.get_id().get_identifier()] = CREATED
        return result"""

    get_resource_form_for_update_template = """
        from dlkit.${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from .${return_module} import ${return_type}
        from .models import ${object_name} as ${object_name}Model
        from ..osid.osid_errors import NotFound, NullArgument, InvalidArgument, OperationFailed, PermissionDenied, Unsupported
        UPDATED = True
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            return InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        try:
            obj_model = ${object_name}Model.objects.get(identifier=${arg0_name}.get_identifier(),
                        ${object_name_under}_${cat_name_lower}__${cat_name_under}_identifier=self._catalog_identifier)
        except ObjectDoesNotExist:
            raise NotFound()
        obj_form = ${return_type}(obj_model)
        obj_form._for_update = True
        self._forms[obj_form.get_id().get_identifier()] = not UPDATED
        return obj_form"""

    update_resource_template = """
        from dlkit.${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from ..osid.osid_errors import IllegalState, InvalidArgument, NullArgument, OperationFailed, PermissionDenied, Unsupported
        UPDATED = True
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise InvalidArgument('argument type is not an ${arg0_type}')
        if not ${arg0_name}.is_for_update():
            raise InvalidArgument('the ${arg0_type} is for update only, not create')
        try:
            if self._forms[${arg0_name}.get_id().get_identifier()] == UPDATED:
                raise IllegalState('${arg0_name} already used in an update transaction')
        except KeyError:
            raise Unsupported('${arg0_name} did not originate from this session')
        if not ${arg0_name}.is_valid:
            raise InvalidArgument('one or more of the form elements is invalid')
        try:
            ${arg0_name}.my_model.save()
        except: # what exceptions does django model.save raise?
            raise OperationFailed()
        self._forms[${arg0_name}.get_id().get_identifier()] = UPDATED"""

    delete_resource_template = """
        from dlkit.${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
        from .models import ${object_name} as ${object_name}Model
        from ..osid.osid_errors import NotFound, NullArgument, InvalidArgument, OperationFailed, PermissionDenied, Unsupported
        UPDATED = True
        if ${arg0_name} is None:
            raise NullArgument()
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            return InvalidArgument('the argument is not a valid OSID ${arg0_type}')
        try:
            ${object_name_under}_model = ${object_name}Model.objects.get(identifier=${arg0_name}.get_identifier(),
                ${object_name_under}_${cat_name_lower}__${cat_name_under}_identifier=self._catalog_identifier)
        except ObjectDoesNotExist:
            raise NotFound()
        ${object_name_under}_model.delete()"""

    alias_resources_template = """
        from ..osid.osid_errors import Unimplemented
        # NEED TO FIGURE OUT HOW TO IMPLEMENT THIS SOMEDAY
        raise Unimplemented()"""


class Resource:

    init_template = """
    _namespace = '${djpkg_name}.${interface_name}'

    def __init__(self, osid_object_model, **kwargs):
        self.my_model = osid_object_model
${instance_initers}
"""

    is_group_template = """
        # Implemented from template for osid.resource.Resource.is_group
        return self.my_model.${var_name}"""

    is_demographic = """
        return self.demographic"""

    has_avatar_template = """
        # Implemented from template for osid.resource.Resource.has_avatar
        return bool(self.my_model.${var_name}_identifier)"""

    get_avatar_id_template = """
        # Implemented from template for osid.resource.Resource.get_avatar_id
        try:
            from ..id.primitives import Id
        except:
            from ..osid.common import Id
        from ..osid.osid_errors import IllegalState
        if not self.my_model.${var_name}_identifier:
            raise IllegalState('this objective has no ${var_name}')
        else:
            return Id(self.my_model.${var_name}_authority,
                      self.my_model.${var_name}_namespace,
                      self.my_model.${var_name}_identifier)"""

    get_avatar_template = """
        # Implemented from template for osid.resource.Resource.get_avatar
        from ..osid.osid_errors import IllegalState, OperationFailed
        if not self.my_model.${var_name}_identifier:
            raise IllegalState('no ${var_name} available')
        try:
            from ..${return_app_name}.${return_djpkg_name} import managers
        except ImportError:
            raise OperationFailed('failed to import ${return_app_name}.${return_djpkg_name}.managers')
${import_str}        try:
            mgr = managers.${return_pkg_title}Manager()
        except:
            raise OperationFailed('failed to instantiate ${return_pkg_title}Manager')
        if not mgr.supports_${return_type_under}_lookup():
            raise OperationFailed('${return_pkg_title} does not support ${return_type} lookup')
        try:
            osidObject = mgr.get_${return_type_under}_lookup_session().get${return_type_under}(self.get_${var_name}_id())
        except:
            raise OperationFailed()
        else:
            return osidObject"""


class ResourceForm:

    init_template = """
    _namespace = 'dj_osid.${interface_name}'

    def __init__(self, osid_object_model=None, **kwargs):
        from ..osid.objects import OsidForm
        OsidForm.__init__(self)
        if osid_object_model:
            self.my_model = osid_object_model
            self._for_update = True
        else:
            from .models import ${object_name} as ${object_name}Model
            self.my_model = ${object_name}Model()
            self._for_update = False
            self._init_model(**kwargs)
        self._init_metadata(**kwargs)

    def _init_model(self, **kwargs):
        from ..osid.objects import OsidObjectForm
        OsidObjectForm._init_model(self)
${persisted_initers}
    def _init_metadata(self, **kwargs):
        from ..osid.objects import OsidObjectForm
        try:
            from ..id.primitives import Id
        except:
            from ..osid.common import Id
        try:
            from ..locale.primitives import DisplayText
        except:
            from ..osid.common import DisplayText
        OsidObjectForm._init_metadata(self)
${metadata_initers}"""

    get_group_metadata_template = """
        from ..osid.metadata import Metadata
        return Metadata(**self._${var_name}_metadata)"""

    set_group_template = """
        from ..osid.osid_errors import InvalidArgument, NullArgument, NoAccess
        if ${arg0_name} is None:
            raise NullArgument()
        if self.get_${var_name}_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_${arg0_type}(${arg0_name},
                                     self.get_${arg0_name}_metadata()):
            raise InvalidArgument()
        self.my_model.${var_name} = ${arg0_name}"""

    clear_group_template = """
        from ..osid.osid_errors import NoAccess
        if (self.get_${var_name}_metadata().is_read_only() or
            self.get_${var_name}_metadata().is_required()):
            raise NoAccess()
        self.my_model.${var_name} = self._${var_name}_default"""

    set_avatar_template = """
        from ..osid.osid_errors import InvalidArgument, NullArgument, NoAccess
        if ${arg0_name} is None:
            raise NullArgument()
        if self.get_${var_name}_metadata().is_read_only():
            raise NoAccess()
        if not self._is_valid_${arg0_type}(${arg0_name},
                                self.get_${arg0_name}_metadata()):
            raise InvalidArgument()
        self.my_model.${var_name}_authority = ${arg0_name}.get_authority()
        self.my_model.${var_name}_namespace = ${arg0_name}.get_identifier_namespace()
        self.my_model.${var_name}_identifier = ${arg0_name}.get_identifier()"""

    clear_avatar_template = """
        from ..osid.osid_errors import NoAccess
        if (self.get_${var_name}_metadata().is_read_only() or
            self.get_${var_name}_metadata().is_required()):
            raise NoAccess()
        self.my_model.${var_name}_authority = self._${var_name}_default['authority']
        self.my_model.${var_name}_namespace = self._${var_name}_default['namespace']
        self.my_model.${var_name}_identifier = self._${var_name}_default['identifier']"""


class ResourceList:

    get_next_resource_template = """
        # Implemented from template for osid.resource.ResourceList.get_next_resource
        import sys
        from ..osid.osid_errors import IllegalState, OperationFailed
        try:
            next_item = self.next()
        except StopIteration:
            raise IllegalState('no more elements available in this list')
        except: #Need to specify exceptions here
            raise OperationFailed()
        else:
            return next_item

    def next(self):
        from ..osid.objects import OsidList
        from .${return_module} import ${return_type}
        from django.db import models
        try:
            next_item = OsidList.next(self)
        except:
            raise
        if isinstance(next_item, models.Model):
            next_item = ${return_type}(next_item)
        return next_item"""

    get_next_resources_template = """
        # Implemented from template for osid.resource.ResourceList.get_next_resources
        import sys
        from ..osid.osid_errors import IllegalState, OperationFailed
        if ${arg0_name} > self.available():
            # !!! This is not quite as specified (see method docs) !!!
            raise IllegalState('not enough elements available in this list')
        else:
            next_list = []
            x = 0
            while x < ${arg0_name}:
                try:
                    next_list.append(self.next())
                except:  # Need to specify exceptions here
                    raise OperationFailed()
                x = x + 1
            return next_list"""


class Bin:

    init_template = """
    _namespace = '${djpkg_name}.${interface_name}'

    def __init__(self, osid_catalog_model):
        self.my_model = osid_catalog_model
"""


class BinForm:

    init_template = """
    _namespace = 'dj_osid.${interface_name}'

    def __init__(self, osid_catalog_model = None):
        if osid_catalog_model:
            self.my_model = osid_catalog_model
        else:
            from .models import ${object_name} as ${object_name}Model
            self.my_model = ${object_name}Model()
        self._init_metadata()

    def _init_metadata(self):
        from ..osid.objects import OsidObjectForm
        OsidObjectForm._init_metadata(self)
"""
