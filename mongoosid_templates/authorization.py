
class AuthorizationSession:

    init = """
    _session_name = 'AuthorizationSession'
"""

    is_authorized = """
        from .models import Authorization as AuthorizationModel
        from .osid_errors import NotFound, NullArgument, InvalidArgument, OperationFailed, PermissionDenied

        return bool(
            AuthorizationModel.objects.filter(
                agent_authority = agent_id.get_authority(),
                agent_namespace = agent_id.get_identifier_namespace(),
                agent_identifier = agent_id.get_identifier(),
                function_authority = function_id.get_authority(),
                function_namespace = function_id.get_identifier_namespace(),
                function_identifier = function_id.get_identifier(),
                qualifier_authority = qualifier_id.get_authority(),
                qualifier_namespace = qualifier_id.get_identifier_namespace(),
                qualifier_identifier = qualifier_id.get_identifier()
            )
        )
        """

class Authorization:

    model = """
    from collections import OrderedDict
    from ..osid.models import OsidObject
    options = OsidObject.options
    moptions = OsidObject.moptions
    options['resource_authority'] = {
        'verbose_name': 'resource authority',
        'help_text': '',
        'blank': True,
        'editable': True,
        'default': '',
        'max_length': 128,
        'choices': OrderedDict(),
    }
    options['resource_namespace'] = {
        'verbose_name': 'resource namespace',
        'help_text': '',
        'blank': True,
        'editable': True,
        'default': '',
        'max_length': 128,
        'choices': OrderedDict(),
    }
    options['resource_identifier'] = {
        'verbose_name': 'resource identifier',
        'help_text': '',
        'blank': True,
        'editable': True,
        'default': '',
        'max_length': 64,
        'choices': OrderedDict(),
    }
    options['trust_authority'] = {
        'verbose_name': 'trust authority',
        'help_text': '',
        'blank': True,
        'editable': True,
        'default': '',
        'max_length': 128,
        'choices': OrderedDict(),
    }
    options['trust_namespace'] = {
        'verbose_name': 'trust namespace',
        'help_text': '',
        'blank': True,
        'editable': True,
        'default': '',
        'max_length': 128,
        'choices': OrderedDict(),
    }
    options['trust_identifier'] = {
        'verbose_name': 'trust identifier',
        'help_text': '',
        'blank': True,
        'editable': True,
        'default': '',
        'max_length': 64,
        'choices': OrderedDict(),
    }
    options['agent_authority'] = {
        'verbose_name': 'agent authority',
        'help_text': '',
        'blank': True,
        'editable': True,
        'default': '',
        'max_length': 128,
        'choices': OrderedDict(),
    }
    options['agent_namespace'] = {
        'verbose_name': 'agent namespace',
        'help_text': '',
        'blank': True,
        'editable': True,
        'default': '',
        'max_length': 128,
        'choices': OrderedDict(),
    }
    options['agent_identifier'] = {
        'verbose_name': 'agent identifier',
        'help_text': '',
        'blank': True,
        'editable': True,
        'default': '',
        'max_length': 64,
        'choices': OrderedDict(),
    }
    options['function_authority'] = {
        'verbose_name': 'function authority',
        'help_text': '',
        'blank': True,
        'editable': True,
        'default': '',
        'max_length': 128,
        'choices': OrderedDict(),
    }
    options['function_namespace'] = {
        'verbose_name': 'function namespace',
        'help_text': '',
        'blank': True,
        'editable': True,
        'default': '',
        'max_length': 128,
        'choices': OrderedDict(),
    }
    options['function_identifier'] = {
        'verbose_name': 'function identifier',
        'help_text': '',
        'blank': True,
        'editable': True,
        'default': '',
        'max_length': 64,
        'choices': OrderedDict(),
    }
    options['qualifier_authority'] = {
        'verbose_name': 'qualifier authority',
        'help_text': '',
        'blank': True,
        'editable': True,
        'default': '',
        'max_length': 128,
        'choices': OrderedDict(),
    }
    options['qualifier_namespace'] = {
        'verbose_name': 'qualifier namespace',
        'help_text': '',
        'blank': True,
        'editable': True,
        'default': '',
        'max_length': 128,
        'choices': OrderedDict(),
    }
    options['qualifier_identifier'] = {
        'verbose_name': 'qualifier identifier',
        'help_text': '',
        'blank': True,
        'editable': True,
        'default': '',
        'max_length': 64,
        'choices': OrderedDict(),
    }

    resource_authority = models.CharField(**options['resource_authority'])
    resource_namespace = models.CharField(**options['resource_namespace'])
    resource_identifier = models.CharField(**options['resource_identifier'])
    trust_authority = models.CharField(**options['trust_authority'])
    trust_namespace = models.CharField(**options['trust_namespace'])
    trust_identifier = models.CharField(**options['trust_identifier'])
    agent_authority = models.CharField(**options['agent_authority'])
    agent_namespace = models.CharField(**options['agent_namespace'])
    agent_identifier = models.CharField(**options['agent_identifier'])
    function_authority = models.CharField(**options['function_authority'])
    function_namespace = models.CharField(**options['function_namespace'])
    function_identifier = models.CharField(**options['function_identifier'])
    qualifier_authority = models.CharField(**options['qualifier_authority'])
    qualifier_namespace = models.CharField(**options['qualifier_namespace'])
    qualifier_identifier = models.CharField(**options['qualifier_identifier'])
"""
