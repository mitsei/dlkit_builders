from .resource import ResourceLookupSession
from .resource import ResourceQuerySession


class CommentLookupSession:

    import_statements_pattern = ResourceLookupSession.import_statements_pattern

    init_template = ResourceLookupSession.init_template


class CommentQuerySession:

    import_statements_pattern = ResourceQuerySession.import_statements_pattern

    init_template = ResourceQuerySession.init_template


class CommentAdminSession:

    get_comment_form_for_create_import_templates = [
        'from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}',
        'from ${arg1_abcapp_name}.${arg1_abcpkg_name}.${arg1_module} import ${arg1_type} as ABC${arg1_type}'
    ]

    get_comment_form_for_create_template = """
        # Implemented from template for
        # osid.relationship.CommentAdminSession.get_comment_form_for_create_template
        # These really need to be in module imports:
        if not isinstance(${arg0_name}, ABC${arg0_type}):
            raise errors.InvalidArgument('argument is not a valid OSID ${arg0_type}')
        for arg in ${arg1_name}:
            if not isinstance(arg, ABC${arg1_type}):
                raise errors.InvalidArgument('one or more argument array elements is not a valid OSID ${arg1_type}')
        obj_form = objects.${return_type}(
            record_types=${arg1_name},
            runtime=self._runtime,
            proxy=self._proxy)
        obj_form._init_metadata()
        obj_form._init_map(${cat_name_under}_id=self._catalog_id,
                           ${arg0_name}=${arg0_name},
                           effective_agent_id=self.get_effective_agent_id(),
                           record_types=${arg1_name})
        obj_form._for_update = False
        self._forms[obj_form.get_id().get_identifier()] = not CREATED
        return obj_form"""


class Comment:

    import_statements = [
        'from ..primitives import DisplayText',
    ]

    get_commenting_agent_id = """
        return self.get_commentor_id()"""

    get_commenting_agent = """
        if not self.has_commentor():
            raise errors.IllegalState('this Comment has no commenting_agent')
        try:
            from ..authentication import managers
        except ImportError:
            raise errors.OperationFailed('failed to import authentication.managers')
        try:
            mgr = managers.AuthenticationManager()
        except:
            raise errors.OperationFailed('failed to instantiate AuthenticationManager')
        if not mgr.supports_agent_lookup():
            raise errors.OperationFailed('Authentication does not support Agent lookup')
        try:
            osid_object = mgr.get_agent_lookup_session().get_agent(self.get_commenting_agent_id())
        except:
            raise errors.OperationFailed()
        else:
            return osid_object"""

    additional_methods = """
    def has_commentor(self):
        return bool(self._my_map['commentorId'])

    def get_object_map(self):
        obj_map = dict(self._my_map)
        obj_map['commentingAgentId'] = str(self.get_commenting_agent_id())
        return osid_objects.OsidObject.get_object_map(self, obj_map)

    object_map = property(fget=get_object_map)"""


class CommentQuery:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
    ]
