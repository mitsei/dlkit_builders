# repository templates for aws_adapter


class RepositoryProfile:

    import_statements = [
        'from . import profile'
    ]

    supports_asset_lookup = """
        return 'supports_asset_lookup' in profile.SUPPORTS"""

    supports_asset_query = """
        return 'supports_asset_query' in profile.SUPPORTS"""

    supports_asset_search = """
        return 'supports_asset_search' in profile.SUPPORTS"""

    supports_asset_admin = """
        return 'supports_asset_admin' in profile.SUPPORTS"""


class RepositoryManager:

    import_statements = [
        'from .sessions import *'
    ]

    get_asset_lookup_session = """
        return AssetLookupSession(self._provider_manager.get_asset_lookup_session(), self._config_map)"""

    get_asset_lookup_session_for_repository = """
        return AssetLookupSession(self._provider_manager.get_asset_lookup_session_for_repository(repository_id), self._config_map)"""

    get_asset_query_session = """
        return AssetQuerySession(self._provider_manager.get_asset_query_session(), self._config_map)"""

    get_asset_query_session_for_repository = """
        return AssetQuerySession(self._provider_manager.get_asset_query_session_for_repository(repository_id), self._config_map)"""

    get_asset_search_session = """
        return AssetSearchSession(self._provider_manager.get_asset_search_session(), self._config_map)"""

    get_asset_search_session_for_repository = """
        return AssetSearchSession(self._provider_manager.get_asset_search_session_for_repository(repository_id), self._config_map)"""

    get_asset_admin_session = """
        asset_lookup_session = self._provider_manager.get_asset_lookup_session()
        return AssetAdminSession(self._provider_manager.get_asset_admin_session(), self._config_map, asset_lookup_session)"""

    get_asset_admin_session_for_repository = """
        asset_lookup_session = self._provider_manager.get_asset_lookup_session_for_repository(repository_id)
        return AssetAdminSession(self._provider_manager.get_asset_admin_session_for_repository(repository_id), self._config_map, asset_lookup_session)"""


class RepositoryProxyManager:

    import_statements = [
        'from .sessions import *'
    ]

    get_asset_lookup_session = """
        return AssetLookupSession(self._provider_manager.get_asset_lookup_session(proxy), self._config_map)"""

    get_asset_lookup_session_for_repository = """
        return AssetLookupSession(self._provider_manager.get_asset_lookup_session_for_repository(repository_id, proxy), self._config_map)"""

    get_asset_query_session = """
        return AssetQuerySession(self._provider_manager.get_asset_query_session(proxy), self._config_map)"""

    get_asset_query_session_for_repository = """
        return AssetQuerySession(self._provider_manager.get_asset_query_session_for_repository(repository_id, proxy), self._config_map)"""

    get_asset_search_session = """
        return AssetSearchSession(self._provider_manager.get_asset_search_session(proxy), self._config_map)"""

    get_asset_search_session_for_repository = """
        return AssetSearchSession(self._provider_manager.get_asset_search_session_for_repository(repository_id, proxy), self._config_map)"""

    get_asset_admin_session = """
        asset_lookup_session = self._provider_manager.get_asset_lookup_session(proxy)
        return AssetAdminSession(self._provider_manager.get_asset_admin_session(proxy), self._config_map, asset_lookup_session)"""

    get_asset_admin_session_for_repository = """
        asset_lookup_session = self._provider_manager.get_asset_lookup_session_for_repository(repository_id, proxy)
        return AssetAdminSession(self._provider_manager.get_asset_admin_session_for_repository(repository_id, proxy), self._config_map, asset_lookup_session)"""


class AssetLookupSession:

    get_asset = """
        return Asset(self._provider_session.get_asset(asset_id), self._config_map)"""

    get_assets_by_ids = """
        return AssetList(self._provider_session.get_assets_by_ids(asset_ids), self._config_map)"""

    get_assets_by_genus_type = """
        return AssetList(self._provider_session.get_assets_by_genus_type(asset_genus_type), self._config_map)"""

    get_assets_by_parent_genus_type = """
        return AssetList(self._provider_session.get_assets_by_parent_genus_type(asset_genus_type), self._config_map)"""

    get_assets_by_record_type = """
        return AssetList(self._provider_session.get_assets_by_record_type(asset_record_type), self._config_map)"""

    get_assets_by_provider = """
        return AssetList(self._provider_session.get_assets_by_provider(resource_id), self._config_map)"""

    get_assets = """
        return AssetList(self._provider_session.get_assets(), self._config_map)"""


class AssetQuerySession:

    get_assets_by_query = """
        return AssetList(self._provider_session.get_assets_by_query(asset_query), self._config_map)"""


class AssetSearchSession:

    get_assets_by_search = """
        return AssetList(self._provider_session.get_assets_by_search(asset_search), self._config_map)"""


class AssetAdminSession:

    import_statements = [
        'from .objects import Asset, AssetList, AssetContent, AssetContentForm',
        'from ..types import AWS_ASSET_CONTENT_RECORD_TYPE',
        'from ..osid.osid_errors import *'
    ]

    init = """
    def __init__(self, provider_session, config_map, lookup_session, proxy = None):
        osid_sessions.OsidSession.__init__(self, provider_session, config_map, proxy)
        self._asset_lookup_session = lookup_session
"""

    update_asset = """
        return Asset(self._provider_session.update_asset(asset_form), self._config_map)"""

    get_asset_content_form_for_create = """
        if AWS_ASSET_CONTENT_RECORD_TYPE in asset_content_record_types:
            asset_content_record_types.remove(AWS_ASSET_CONTENT_RECORD_TYPE)
            return AssetContentForm(self._provider_session.get_asset_content_form_for_create(asset_id, asset_content_record_types), self._config_map, self.get_repository_id())
        else:
            return self._provider_session.get_asset_content_form_for_create(asset_id, asset_content_record_types)"""

    create_asset_content_template = """
        # Implemented from azosid template for -
        # osid.repository.AssetAdminSession.create_asset_content_template
        return self._provider_session.${method_name}(${arg0_name})"""

    create_asset_content = """
        if isinstance(asset_content_form, AssetContentForm):
            asset_content = self._provider_session.create_asset_content(asset_content_form._payload)
        else:
            asset_content = self._provider_session.create_asset_content(asset_content_form)
        if asset_content.has_url() and 'amazonaws.com' in asset_content.get_url():
            return AssetContent(asset_content, self._config_map)
        return asset_content"""

    get_asset_content_form_for_update_template = """
        # Implemented from azosid template for -
        # osid.repository.AssetAdminSession.get_asset_content_form_for_update_template
        return self._provider_session.${method_name}(${arg0_name})"""

    get_asset_content_form_for_update = """
        asset_content_form = self._provider_session.get_asset_content_form_for_update(asset_content_id)
        if 'amazonaws.com' in asset_content_form.get_url_metadata().get_existing_string_values()[0]:
            return AssetContentForm(asset_content_form, self._config_map, self.get_repository_id())
        return asset_content_form"""

    update_asset_content_template = """
        # Implemented from azosid template for -
        # osid.repository.AssetAdminSession.update_asset_content_template
        return self._provider_session.${method_name}(${arg0_name})"""

    update_asset_content = """
        if isinstance(asset_content_form, AssetContentForm):
            asset_content = self._provider_session.update_asset_content(asset_content_form._payload)
        else:
            asset_content = self._provider_session.update_asset_content(asset_content_form)
        if asset_content is not None and asset_content.has_url() and 'amazonaws.com' in asset_content.get_url():
            return AssetContent(asset_content, self._config_map)
        return asset_content"""

    delete_asset_content_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.delete_asset_content_template
        self._provider_session.${method_name}(${arg0_name})"""

    delete_asset_content = """
        asset_content = self._get_asset_content(asset_content_id)
        if asset_content.has_url() and 'amazonaws.com' in asset_content.get_url():
            print "Still have to implement removing files from aws"
            self._provider_session.delete_asset_content(asset_content_id)
        else:
            self._provider_session.delete_asset_content(asset_content_id)"""

    additional_methods = """
    def _get_asset_content(self, asset_content_id):
        asset_content = None
        for asset in self._asset_lookup_session.get_assets():
            for ac in asset.get_asset_contents():
                if ac.get_id() == asset_content_id:
                    asset_content = ac
                    break
            if asset_content is not None:
                break
        if asset_content is None:
            raise NotFound('THe AWS Adapter could not find AssetContent ' + str(asset_content_id))
        return asset_content
    """


class Asset:

    init = """
    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith('__'):
                yield attr

    def __getitem__(self, item):
        return getattr(self, item)

    def __getattr__(self, name):
        if '_payload' in self.__dict__:
            try:
                return self._payload[name]
            except:
                raise
        raise AttributeError(name)
"""

    get_title = """
        return self._payload.get_title()"""

    is_copyright_status_known = """
        return self._payload.is_copyright_status_known()"""

    is_public_domain = """
        return self._payload.is_public_domain()"""

    get_copyright = """
        return self._payload.get_copyright()"""

    get_copyright_registration = """
        return self._payload.get_copyright_registration()"""

    can_distribute_verbatim = """
        return self._payload.can_distribute_verbatim()"""

    can_distribute_alterations = """
        return self._payload.can_distribute_alterations()"""

    can_distribute_compositions = """
        return self._payload.can_distribute_compositions()"""

    get_source_id = """
        return self._payload.get_source_id()"""

    get_source = """
        return self._payload.get_source()"""

    get_provider_link_ids = """
        return self._payload.get_provider_link_ids()"""

    get_provider_links = """
        return self._payload.get_provider_links()"""

    get_created_date = """
        return self._payload.get_created_date()"""

    is_published = """
        return self._payload.is_published()"""

    get_published_date = """
        return self._payload.get_published_date()"""

    get_principal_credit_string = """
        return self._payload.get_principal_credit_string()"""

    get_asset_content_ids = """
        return self._payload.get_asset_content_ids()"""

    get_asset_contents = """
        # Note that this one is different. It wraps the returned AssetContentList in an AWS AssetContentList
        return AssetContentList(self._payload.get_asset_contents(), self._config_map)"""

    is_composition = """
        return self._payload.is_composition()"""

    get_composition_id = """
        return self._payload.get_composition_id()"""

    get_composition = """
        return self._payload.get_composition()"""

    get_asset_record = """
        return self._payload.get_asset_record()

    def get_object_map(self):
        obj_map = self._payload.get_object_map()
        obj_map['assetContents'] = []
        for asset_content in self.get_asset_contents():
            obj_map['assetContents'].append(asset_content.get_object_map())
        return obj_map"""


class AssetContent:

    import_statements = [
        'from ..osid.osid_errors import *',
        'from ..primitives import *',
        'from .aws_utils import *',
        'from ..types import AWS_ASSET_CONTENT_RECORD_TYPE',
    ]

    init = """
    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith('__'):
                yield attr

    def __getitem__(self, item):
        return getattr(self, item)

    def __getattr__(self, name):
        if '_payload' in self.__dict__:
            try:
                return self._payload[name]
            except:
                raise
        raise AttributeError(name)
"""

    get_asset_id = """
        return self._payload.get_asset_id()"""

    get_asset = """
        return self._payload.get_asset()"""

    get_accessibility_types = """
        return self._payload.get_accessibility_types()"""

    has_data_length = """
        return False  # can we get a data length from AWS?"""

    get_data_length = """
        raise IllegalState()  # can we get a data length from AWS?"""

    get_data = """
        raise Unimplemented()  # need to get data from aws"""

    has_url = """
        return self._payload.has_url()"""

    get_url = """
        return get_signed_url(self._payload.get_url(), self._config_map)"""

    get_asset_content_record = """
        return self._payload.get_asset_content_record()

    def get_object_map(self):
        obj_map = self._payload.get_object_map()
        obj_map.update({'url': self.get_url()})
        obj_map['recordTypeIds'].append(str(AWS_ASSET_CONTENT_RECORD_TYPE))
        return obj_map"""


class AssetContentForm:

    import_statements = [
        'from ..osid.osid_errors import *',
        'from ..primitives import *',
        'from .aws_utils import *',
        'from ..types import AWS_ASSET_CONTENT_RECORD_TYPE',
        'import re',
        'from bson.objectid import ObjectId'
    ]

    init = """
    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith('__'):
                yield attr

    def __getitem__(self, item):
        return getattr(self, item)

    def __getattr__(self, name):
        if '_payload' in self.__dict__:
            try:
                return self._payload[name]
            except:
                raise
        raise AttributeError(name)
"""

    get_accessibility_type_metadata = """
        return self._payload.get_accessibility_type_metadata()"""

    add_accessibility_type = """
        self._payload.add_accessibility_type(accessibility_type)"""

    remove_accessibility_type = """
        self._payload.remove_accessibility_type(accessibility_type)"""

    clear_accessibility_types = """
        self._payload.clear_accessibility_types()"""

    get_data_metadata = """
        return self._payload.get_data_metadata()"""

    set_data = """
        # cjshaw, Jan 7, 2015
        # Testing this with AWS -- set data + set_url (to save the S3 URL)
        # Uses:
        #    1) AWS repository-put user key pair
        #    2) S3 bucket for odl-repository
        #
        # For now, follow a convention of all items need to be in a catalog_id
        # folder...like:
        #    self._repository_id.identifier/<file>
        #
        # following: http://stackoverflow.com/questions/15085864/how-to-upload-a-file-to-directory-in-s3-bucket-using-boto
        odl_repo, url = get_aws_s3_handle(self._config_map)
        repository_id = self._repository_id.get_identifier()
        try:
            filename = data.name.split('/')[-1]
            filename = re.sub(r'[^\w.]', '_', filename)  # clean out the spaces
        except:
            filename = ObjectId()
        remote_location = str(repository_id) + '/' + str(filename)
        url += '/' + remote_location

        data.seek(0)

        odl_repo.key = remote_location
        odl_repo.set_contents_from_file(data._my_data)

        # this should set the original S3 location, so we can retrieve the original document if needed
        # do NOT set to the Cloudfront location...that should be locked down for expiring URLs
        # constructed by the Cloudfront keypair only.
        self._payload.set_url(url)"""

    clear_data = """
        # cjshaw@mit.edu, Jan 9, 2015
        # Removes the item from AWS S3 and resets URL to ''
        odl_repo, url = get_aws_s3_handle(self._config_map)
        existing_url = self._payload.get_url_metadata().get_existing_string_values()[0]
        # try to clear from payload first, in case that fails we won't mess with AWS
        self._payload.clear_url()
        key_path = existing_url.replace(url, '')
        odl_repo.key = key_path
        odl_repo.delete()"""

    get_url_metadata = """
        return self._payload.get_url_metadata()"""

    set_url = """
        raise NoAccess('Use set_data() only. URLs for AWS AssetContents are managed by the system')"""

    clear_url = """
        raise NoAccess('Use clear_data() only. URLs for AWS AssetContents are managed by the system')"""

    get_asset_content_form_record = """
        return self._payload.get_asset_content_form_record(asset_content_record_type)"""

    additional_methods = """
    def _clean_up(self):
        pass  # This is where we could deal with the un-updated form issue"""


class AssetList:

    import_statements = [
        'from ..osid.osid_errors import *',
        'from ..primitives import *',
    ]

    get_next_asset_content = """
        return self.next()

    def next(self):
        return Asset(self._payload_list.next(), self._config_map)"""

    get_next_assets = """
        if n is None:
            raise NullArgument()
        if not isinstance(n, int):
            raise InvalidArgument()
        provider_list = self._payload_list.get_next_assets(n)
        new_list = []
        for asset in provider_list:
            new_list.append(Asset(asset))
        return new_list"""


class AssetContentList:

    import_statements = [
        'from ..osid.osid_errors import *',
        'from ..primitives import *',
    ]

    get_next_asset_content = """
        return self.next()

    def next(self):
        asset_content = self._payload_list.next()
        if asset_content.has_url() and 'amazonaws.com' in asset_content.get_url():
            return AssetContent(asset_content, self._config_map)
        return asset_content"""

    get_next_asset_contents = """
        if n is None:
            raise NullArgument()
        if not isinstance(n, int):
            raise InvalidArgument()
        provider_list = self._payload_list.get_next_asset_contents(n)
        new_list = []
        for asset_content in provider_list:
            if asset_content.has_url() and 'amazonaws.com' in asset_content.get_url():
                new_list.append(AssetContent(asset_content, self._config_map))
            else:
                new_list.append(asset_content)
        return new_list"""
