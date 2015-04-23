# osid templates for az_osid

class OsidProfile:

#    init = """ """

    get_id = """
        return self._provider_manager.get_id()"""

    get_display_name = """
        return self._provider_manager.get_display_name()"""

    get_description = """
        return self._provider_manager.get_description()"""

    get_version = """
        return self._provider_manager.get_version()"""

    get_release_date = """
        return self._provider_manager.get_release_date()"""

    supports_osid_version = """
        return self._provider_manager.supports_osid_version(version)"""

    get_locales = """
        return self._provider_manager.get_locales()"""

    supports_journal_rollback = """
        return self._provider_manager.supports_journal_rollback()"""

    supports_journal_branching = """
        return self._provider_manager.supports_journal_branching()"""

    get_branch_id = """
        return self._provider_manager.get_branch_id()"""

    get_branch = """
        return self._provider_manager.get_branch()"""

    get_proxy_record_types = """
        return self._provider_manager.get_proxy_record_types()"""

    supports_proxy_record_type = """
        return self._provider_manager.supports_proxy_record_type(proxy_record_type)"""

class OsidManager:

    import_statements = [
        'from ..primitives import *',
        'from ..osid.osid_errors import *'
    ]

    init = """
    def __init__(self):
        self._my_runtime = None
        self._config_map = {}
"""
    
    initialize = """
        if runtime is None:
            raise NullArgument()
        if self._my_runtime is not None:
            raise IllegalState('this manager has already been initialized.')
        self._my_runtime = runtime
        config = runtime.get_configuration()

        cf_public_key_parameter_id = Id('parameter:cloudFrontPublicKey@aws_adapter')
        cf_private_key_parameter_id = Id('parameter:cloudFrontPrivateKey@aws_adapter')
        cf_keypair_id_parameter_id = Id('parameter:cloudFrontSigningKeypairId@aws_adapter')
        cf_private_key_file_parameter_id = Id('parameter:cloudFrontSigningPrivateKeyFile@aws_adapter')
        cf_distro_parameter_id = Id('parameter:cloudFrontDistro@aws_adapter')
        cf_distro_id_parameter_id = Id('parameter:cloudFrontDistroId@aws_adapter')
        s3_public_key_parameter_id = Id('parameter:S3PublicKey@aws_adapter')
        s3_private_key_parameter_id = Id('parameter:S3PrivateKey@aws_adapter')
        s3_bucket_parameter_id = Id('parameter:S3Bucket@aws_adapter')

        cf_public_key = config.get_value_by_parameter(cf_public_key_parameter_id).get_string_value()
        cf_private_key = config.get_value_by_parameter(cf_private_key_parameter_id).get_string_value()
        cf_keypair_id = config.get_value_by_parameter(cf_keypair_id_parameter_id).get_string_value()
        cf_private_key_file = config.get_value_by_parameter(cf_private_key_file_parameter_id).get_string_value()
        cf_distro = config.get_value_by_parameter(cf_distro_parameter_id).get_string_value()
        cf_distro_id = config.get_value_by_parameter(cf_distro_id_parameter_id).get_string_value()
        s3_public_key = config.get_value_by_parameter(s3_public_key_parameter_id).get_string_value()
        s3_private_key = config.get_value_by_parameter(s3_private_key_parameter_id).get_string_value()
        s3_bucket = config.get_value_by_parameter(s3_bucket_parameter_id).get_string_value()

        self._config_map['cloudfront_public_key'] = cf_public_key
        self._config_map['cloudfront_private_key'] = cf_private_key
        self._config_map['cloudfront_keypair_id'] = cf_keypair_id
        self._config_map['cloudfront_private_key_file'] = cf_private_key_file
        self._config_map['cloudfront_distro'] = cf_distro
        self._config_map['cloudfront_distro_id'] = cf_distro_id
        self._config_map['put_public_key'] = s3_public_key
        self._config_map['put_private_key'] = s3_private_key
        self._config_map['s3_bucket'] = s3_bucket
"""

    rollback_service = """
        return self._provider_manager.rollback_service(rollback_time)"""

    change_branch = """
        return self._provider_manager.change_branch(branch_id)"""


class OsidProxyManager:

    init = """
    def __init__(self):
        self._my_runtime = None
        self._config_map = {}
"""
    
    initialize = """
        if runtime is None:
            raise NullArgument()
        if self._my_runtime is not None:
            raise IllegalState('this manager has already been initialized.')
        self._my_runtime = runtime
        config = runtime.get_configuration()

        cf_public_key_parameter_id = Id('parameter:cloudFrontPublicKey@aws_adapter')
        cf_private_key_parameter_id = Id('parameter:cloudFrontPrivateKey@aws_adapter')
        cf_keypair_id_parameter_id = Id('parameter:cloudFrontSigningKeypairId@aws_adapter')
        cf_private_key_file_parameter_id = Id('parameter:cloudFrontSigningPrivateKeyFile@aws_adapter')
        cf_distro_parameter_id = Id('parameter:cloudFrontDistro@aws_adapter')
        cf_distro_id_parameter_id = Id('parameter:cloudFrontDistroId@aws_adapter')
        s3_public_key_parameter_id = Id('parameter:S3PublicKey@aws_adapter')
        s3_private_key_parameter_id = Id('parameter:S3PrivateKey@aws_adapter')
        s3_bucket_parameter_id = Id('parameter:S3Bucket@aws_adapter')

        cf_public_key = config.get_value_by_parameter(cf_public_key_parameter_id).get_string_value()
        cf_private_key = config.get_value_by_parameter(cf_private_key_parameter_id).get_string_value()
        cf_keypair_id = config.get_value_by_parameter(cf_keypair_id_parameter_id).get_string_value()
        cf_private_key_file = config.get_value_by_parameter(cf_private_key_file_parameter_id).get_string_value()
        cf_distro = config.get_value_by_parameter(cf_distro_parameter_id).get_string_value()
        cf_distro_id = config.get_value_by_parameter(cf_distro_id_parameter_id).get_string_value()
        s3_public_key = config.get_value_by_parameter(s3_public_key_parameter_id).get_string_value()
        s3_private_key = config.get_value_by_parameter(s3_private_key_parameter_id).get_string_value()
        s3_bucket = config.get_value_by_parameter(s3_bucket_parameter_id).get_string_value()

        self._config_map['cloudfront_public_key'] = cf_public_key
        self._config_map['cloudfront_private_key'] = cf_private_key
        self._config_map['cloudfront_keypair_id'] = cf_keypair_id
        self._config_map['cloudfront_private_key_file'] = cf_private_key_file
        self._config_map['cloudfront_distro'] = cf_distro
        self._config_map['cloudfront_distro_id'] = cf_distro_id
        self._config_map['put_public_key'] = s3_public_key
        self._config_map['put_private_key'] = s3_private_key
        self._config_map['s3_bucket'] = s3_bucket
"""

    rollback_service = """
        return self._provider_manager.rollback_service(rollback_time)"""

    change_branch = """
        return self._provider_manager.change_branch(branch_id)"""



class Identifiable:

#    init = """  """

    get_id = """
        return self._payload.get_id()"""

    is_current = """
        return False"""


class Extensible:

    import_statements = [
        'from ..types import AWS_ASSET_CONTENT_RECORD_TYPE'
    ]

    has_record_type = """
        return (record_type == AWS_ASSET_CONTENT_RECORD_TYPE or self._payload.has_record_type(record_type))"""

    get_record_types = """
        # This should  add the AWS_ASSET_CONTENT_RECORD_TYPE to self._payload.get_record_types()
        pass"""


class Operable:

    is_active = """
        pass"""

    is_enabled = """
        pass"""

    is_disabled = """
        pass"""

    is_operational = """
        pass"""


class OsidSession:

    init = """
    def __init__(self, provider_session, config_map, proxy = None):
        self._provider_session = provider_session
        self._config_map = config_map
        self._proxy = proxy # Proxy is not currently used, and will always 
                            # be None, but someday may come in handy. Manager
                            # set_session methods would need to be updated to
                            # pass proxy information to aws_adapter sessiosns.
"""

    get_locale = """
        return self._provider_session.is_authenticated()"""

    is_authenticated = """
        return self._provider_session.is_authenticated()"""

    get_authenticated_agent_id = """
        return self._provider_session.get_authenticated_agent_id()"""  

    get_authenticated_agent = """
        return self._provider_session.get_authenticated_agent()"""

    get_effective_agent_id = """
        return self._provider_session.get_effective_agent_id()"""

    get_effective_agent = """
        return self._provider_session.get_effective_agent()"""

    supports_transactions = """
        return self._provider_session.supports_transactions()"""

    start_transaction = """
        return self._provider_session.start_transaction()"""


class OsidObject:

    init = """
    def __init__(self, payload, config_map):
        self._payload = payload
        self._config_map = config_map
"""

    get_display_name = """
        return self._payload.get_display_name()"""

    get_description = """
        return self._payload.get_description()"""

    get_genus_type = """
        return self._payload.get_genus_type()"""

    is_of_genus_type = """
        return self._payload.is_of_genus_type(genus_type)"""


class OsidForm:

    init = """ 
    def __init__(self, payload, config_map, repository_id):
        self._payload = payload
        self._config_map = config_map
        # This should probably go in the AssetContentForm initter:
        self._repository_id = repository_id
"""

    is_for_update = """
        return self._payload.is_for_update()"""

    get_default_locale = """
        return self._payload.get_default_locale()"""

    get_locales = """
        return self._payload.get_locales()"""

    set_locale = """
        return self._payload.set_locale(language_type, script_type)"""

    get_comment_metadata = """
        return self._payload.get_comment_metadata()"""

    get_journal_comment_metadata = """
        return self._payload.get_journal_comment_metadata()"""

    #set_comment = """
    #    return self._payload.set_comment(comment)"""

    set_journal_comment = """
        return self._payload.set_comment(comment)"""

    is_valid = """
        return self._payload.is_valid()"""

    get_validation_messages = """
        return self._payload.get_validation_messages()"""

    get_invalid_metadata = """
        return self._payload.get_invalid_metadata()"""

class OsidObjectForm:

#    init = """ """

    get_display_name_metadata = """
        return self._payload.get_display_name_metadata()"""

    set_display_name = """
        self._payload.set_display_name(display_name)"""

    clear_display_name = """
        self._payload.clear_display_name()"""

    get_description_metadata = """
        return self._payload.get_description_metadata()"""

    set_description = """
        return self._payload.set_description(description)"""

    clear_description = """
        self._payload.clear_description()"""

    get_genus_type_metadata = """
        self._payload.get_genus_type_metadata()"""

    set_genus_type = """
        self._payload.set_genus_type(genus_type)"""

    clear_genus_type = """
        self._payload.clear_genus_type()"""


class OsidList:

    init = """
    def __init__(self, payload_list, config_map):
        self._payload_list = payload_list
        self._config_map = config_map

    def __iter__(self):
        return self
"""

    has_next = """
        self._payload_list.has_next()"""

    available = """
        self._payload_list.available()"""

