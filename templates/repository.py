
# class RepositoryProfile:

    # get_coordinate_types_template = """
    #     # Implemented from template for
    #     # osid.repository.RepositoryProfile.get_coordinate_types
    #     return TypeList([])"""
    #
    # supports_coordinate_type_template = """
    #     # Implemented from template for
    #     # osid.repository.RepositoryProfile.supports_coordinate_type
    #     return False"""


class RepositoryManager:
    # This is here temporarily until Tom adds missing methods to RepositoryManager

    additional_methods = {
        'python': {
            'json': """
    @utilities.arguments_not_none
    def get_asset_composition_session_for_repository(self, repository_id):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        if not self.supports_asset_composition():
            raise errors.Unimplemented()

        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        return sessions.AssetCompositionSession(repository_id, runtime=self._runtime)  # pylint: disable=no-member

    @utilities.arguments_not_none
    def get_asset_composition_design_session_for_repository(self, repository_id):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        if not self.supports_asset_composition():
            raise errors.Unimplemented()

        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        return sessions.AssetCompositionDesignSession(repository_id, runtime=self._runtime)  # pylint: disable=no-member

    def get_asset_content_lookup_session(self):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        if not self.supports_asset_lookup():  # should be asset_content_lookup
            raise errors.Unimplemented()
        return sessions.AssetContentLookupSession(runtime=self._runtime)  # pylint: disable=no-member

    @utilities.arguments_not_none
    def get_asset_content_lookup_session_for_repository(self, repository_id):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        if not self.supports_asset_lookup():  # should be asset_content_lookup
            raise errors.Unimplemented()

        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        return sessions.AssetContentLookupSession(repository_id, runtime=self._runtime)  # pylint: disable=no-member"""
        }
    }


class RepositoryProxyManager:
    # This is here temporarily until Tom adds missing methods to RepositoryProxyManager

    additional_methods = {
        'python': {
            'json': """
    @utilities.arguments_not_none
    def get_asset_composition_session_for_repository(self, repository_id, proxy):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        if not self.supports_asset_composition():
            raise errors.Unimplemented()

        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        return sessions.AssetCompositionSession(catalog_id=repository_id, proxy=proxy, runtime=self._runtime)  # pylint: disable=no-member

    @utilities.arguments_not_none
    def get_asset_composition_design_session_for_repository(self, repository_id, proxy):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        if not self.supports_asset_composition():
            raise errors.Unimplemented()

        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        return sessions.AssetCompositionDesignSession(catalog_id=repository_id, proxy=proxy, runtime=self._runtime)  # pylint: disable=no-member

    def get_asset_content_lookup_session(self, proxy):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        if not self.supports_asset_lookup():  # should be asset_content_lookup
            raise errors.Unimplemented()
        return sessions.AssetContentLookupSession(proxy=proxy, runtime=self._runtime)  # pylint: disable=no-member

    @utilities.arguments_not_none
    def get_asset_content_lookup_session_for_repository(self, repository_id, proxy):
        # This impl is temporary until Tom adds missing methods to RepositoryProxyManager in spec
        if not self.supports_asset_lookup():  # should be asset_content_lookup
            raise errors.Unimplemented()

        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        return sessions.AssetContentLookupSession(catalog_id=repository_id, proxy=proxy, runtime=self._runtime)  # pylint: disable=no-member"""
        }
    }


class AssetLookupSession:

    additional_methods = {
        'python': {
            'json': """
    # def get_asset_content(self, asset_content_id):
    #     collection = JSONClientValidated('repository',
    #                                      collection='Asset',
    #                                      runtime=self._runtime)
    #     asset_content_identifier = ObjectId(self._get_id(asset_content_id, 'repository').get_identifier())
    #     result = collection.find_one(
    #         dict({'assetContents._id': {'$in': [asset_content_identifier]}},
    #              **self._view_filter()))
    #     # if a match is not found, NotFound exception will be thrown by find_one, so
    #     # the below should always work
    #     asset_content_map = [ac for ac in result['assetContents'] if ac['_id'] == asset_content_identifier][0]
    #     return objects.AssetContent(osid_object_map=asset_content_map, runtime=self._runtime, proxy=self._proxy)


class AssetContentLookupSession(abc_repository_sessions.AssetContentLookupSession, osid_sessions.OsidSession):
    \"\"\"This session defines methods for retrieving asset contents.

    An ``AssetContent`` represents an element of content stored associated
    with an ``Asset``.

    This lookup session defines several views:

      * comparative view: elements may be silently omitted or re-ordered
      * plenary view: provides a complete result set or is an error
        condition
      * isolated repository view: All asset content methods in this session
        operate, retrieve and pertain to asset contents defined explicitly in
        the current repository. Using an isolated view is useful for
        managing ``AssetContents`` with the ``AssetAdminSession.``
      * federated repository view: All asset content methods in this session
        operate, retrieve and pertain to all asset contents defined in this
        repository and any other asset contents implicitly available in this
        repository through repository inheritence.


    The methods ``use_federated_repository_view()`` and
    ``use_isolated_repository_view()`` behave as a radio group and one
    should be selected before invoking any lookup methods.

    AssetContents may have an additional records indicated by their respective
    record types. The record may not be accessed through a cast of the
    ``AssetContent``.

    \"\"\"
    def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
        OsidSession.__init__(self)
        self._catalog_class = objects.Repository
        self._catalog_name = 'Repository'
        OsidSession._init_object(
            self,
            catalog_id,
            proxy,
            runtime,
            db_name='repository',
            cat_name='Repository',
            cat_class=objects.Repository)
        self._kwargs = kwargs

    def get_repository_id(self):
        \"\"\"Gets the ``Repository``  ``Id`` associated with this session.

        :return: the ``Repository Id`` associated with this session
        :rtype: ``osid.id.Id``


        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        return self._catalog_id

    repository_id = property(fget=get_repository_id)

    def get_repository(self):
        \"\"\"Gets the ``Repository`` associated with this session.

        :return: the ``Repository`` associated with this session
        :rtype: ``osid.repository.Repository``
        :raise: ``OperationFailed`` -- unable to complete request
        :raise: ``PermissionDenied`` -- authorization failure

        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        return self._catalog

    repository = property(fget=get_repository)

    def can_lookup_asset_contents(self):
        \"\"\"Tests if this user can perform ``Asset`` lookups.

        A return of true does not guarantee successful authorization. A
        return of false indicates that it is known all methods in this
        session will result in a ``PermissionDenied``. This is intended
        as a hint to an application that may opt not to offer lookup
        operations.

        :return: ``false`` if lookup methods are not authorized, ``true`` otherwise
        :rtype: ``boolean``


        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        # NOTE: It is expected that real authentication hints will be
        # handled in a service adapter above the pay grade of this impl.
        return True

    def use_comparative_asset_content_view(self):
        \"\"\"The returns from the lookup methods may omit or translate elements based on this session, such as authorization, and not result in an error.

        This view is used when greater interoperability is desired at
        the expense of precision.



        *compliance: mandatory -- This method is must be implemented.*

        \"\"\"
        self._use_comparative_object_view()

    def use_plenary_asset_content_view(self):
        \"\"\"A complete view of the ``Asset`` returns is desired.

        Methods will return what is requested or result in an error.
        This view is used when greater precision is desired at the
        expense of interoperability.



        *compliance: mandatory -- This method is must be implemented.*

        \"\"\"
        self._use_plenary_object_view()

    def use_federated_repository_view(self):
        \"\"\"Federates the view for methods in this session.

        A federated view will include assets in repositories which are
        children of this repository in the repository hierarchy.



        *compliance: mandatory -- This method is must be implemented.*

        \"\"\"
        self._use_federated_catalog_view()

    def use_isolated_repository_view(self):
        \"\"\"Isolates the view for methods in this session.

        An isolated view restricts lookups to this repository only.



        *compliance: mandatory -- This method is must be implemented.*

        \"\"\"
        self._use_isolated_catalog_view()

    @utilities.arguments_not_none
    def get_asset_content(self, asset_content_id):
        \"\"\"Gets the ``AssetContent`` specified by its ``Id``.

        In plenary mode, the exact ``Id`` is found or a ``NotFound``
        results. Otherwise, the returned ``AssetContent`` may have a different
        ``Id`` than requested, such as the case where a duplicate ``Id``
        was assigned to an ``AssetContent`` and retained for compatibility.

        :param asset_content_id: the ``Id`` of the ``AssetContent`` to retrieve
        :type asset_content_id: ``osid.id.Id``
        :return: the returned ``AssetContent``
        :rtype: ``osid.repository.Asset``
        :raise: ``NotFound`` -- no ``AssetContent`` found with the given ``Id``
        :raise: ``NullArgument`` -- ``asset_content_id`` is ``null``
        :raise: ``OperationFailed`` -- unable to complete request
        :raise: ``PermissionDenied`` -- authorization failure

        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        collection = JSONClientValidated('repository',
                                         collection='Asset',
                                         runtime=self._runtime)
        asset_content_identifier = ObjectId(self._get_id(asset_content_id, 'repository').get_identifier())
        result = collection.find_one(
            dict({'assetContents._id': {'$in': [asset_content_identifier]}},
                 **self._view_filter()))
        # if a match is not found, NotFound exception will be thrown by find_one, so
        # the below should always work
        asset_content_map = [ac for ac in result['assetContents'] if ac['_id'] == asset_content_identifier][0]
        return objects.AssetContent(osid_object_map=asset_content_map, runtime=self._runtime, proxy=self._proxy)

    @utilities.arguments_not_none
    def get_asset_contents_by_ids(self, asset_content_ids):
        \"\"\"Gets an ``AssetList`` corresponding to the given ``IdList``.

        In plenary mode, the returned list contains all of the asset contents
        specified in the ``Id`` list, in the order of the list,
        including duplicates, or an error results if an ``Id`` in the
        supplied list is not found or inaccessible. Otherwise,
        inaccessible ``AssetContnts`` may be omitted from the list and may
        present the elements in any order including returning a unique
        set.

        :param asset_content_ids: the list of ``Ids`` to retrieve
        :type asset_content_ids: ``osid.id.IdList``
        :return: the returned ``AssetContent list``
        :rtype: ``osid.repository.AssetContentList``
        :raise: ``NotFound`` -- an ``Id`` was not found
        :raise: ``NullArgument`` -- ``asset_ids`` is ``null``
        :raise: ``OperationFailed`` -- unable to complete request
        :raise: ``PermissionDenied`` -- authorization failure

        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        collection = JSONClientValidated('repository',
                                         collection='Asset',
                                         runtime=self._runtime)
        object_id_list = [ObjectId(self._get_id(i, 'repository').get_identifier()) for i in asset_content_ids]

        results = collection.find(
            dict({'assetContents._id': {'$in': object_id_list}},
                 **self._view_filter()))
        # if a match is not found, NotFound exception will be thrown by find_one, so
        # the below should always work
        asset_content_maps = [ac
                              for asset in results
                              for ac in asset['assetContents']
                              for object_id in object_id_list
                              if ac['_id'] == object_id]
        return objects.AssetContentList(asset_content_maps, runtime=self._runtime, proxy=self._proxy)

    @utilities.arguments_not_none
    def get_asset_contents_by_genus_type(self, asset_content_genus_type):
        \"\"\"Gets an ``AssetContentList`` corresponding to the given asset content genus ``Type`` which does not include asset contents of types derived from the specified ``Type``.

        In plenary mode, the returned list contains all known asset contents or
        an error results. Otherwise, the returned list may contain only
        those asset contents that are accessible through this session.

        :param asset_content_genus_type: an asset content genus type
        :type asset_content_genus_type: ``osid.type.Type``
        :return: the returned ``AssetContent list``
        :rtype: ``osid.repository.AssetContentList``
        :raise: ``NullArgument`` -- ``asset_content_genus_type`` is ``null``
        :raise: ``OperationFailed`` -- unable to complete request
        :raise: ``PermissionDenied`` -- authorization failure

        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        collection = JSONClientValidated('repository',
                                         collection='Asset',
                                         runtime=self._runtime)
        results = collection.find(
            dict({'assetContents.genusTypeId': {'$in': [str(asset_content_genus_type)]}},
                 **self._view_filter()))
        # if a match is not found, NotFound exception will be thrown by find_one, so
        # the below should always work
        asset_content_maps = [ac
                              for asset in results
                              for ac in asset['assetContents']
                              if ac['genusTypeId'] == str(asset_content_genus_type)]
        return objects.AssetContentList(asset_content_maps, runtime=self._runtime, proxy=self._proxy)

    @utilities.arguments_not_none
    def get_asset_contents_by_parent_genus_type(self, asset_content_genus_type):
        \"\"\"Gets an ``AssetContentList`` corresponding to the given asset content genus ``Type`` and include any additional asset contents with genus types derived from the specified ``Type``.

        In plenary mode, the returned list contains all known asset contents or
        an error results. Otherwise, the returned list may contain only
        those asset contents that are accessible through this session.

        :param asset_content_genus_type: an asset content genus type
        :type asset_content_genus_type: ``osid.type.Type``
        :return: the returned ``AssetContent list``
        :rtype: ``osid.repository.AssetContentList``
        :raise: ``NullArgument`` -- ``asset_content_genus_type`` is ``null``
        :raise: ``OperationFailed`` -- unable to complete request
        :raise: ``PermissionDenied`` -- authorization failure

        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        raise errors.Unimplemented()

    @utilities.arguments_not_none
    def get_asset_contents_by_record_type(self, asset_content_record_type):
        \"\"\"Gets an ``AssetContentList`` containing the given asset record ``Type``.

        In plenary mode, the returned list contains all known asset contents or
        an error results. Otherwise, the returned list may contain only
        those asset contents that are accessible through this session.

        :param asset_content_record_type: an asset content record type
        :type asset_content_record_type: ``osid.type.Type``
        :return: the returned ``AssetContent list``
        :rtype: ``osid.repository.AssetContentList``
        :raise: ``NullArgument`` -- ``asset_content_record_type`` is ``null``
        :raise: ``OperationFailed`` -- unable to complete request
        :raise: ``PermissionDenied`` -- authorization failure

        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        raise errors.Unimplemented()

    @utilities.arguments_not_none
    def get_asset_contents_for_asset(self, asset_id):
        \"\"\"Gets an ``AssetList`` from the given Asset.

        In plenary mode, the returned list contains all known asset contents or
        an error results. Otherwise, the returned list may contain only
        those asset contents that are accessible through this session.

        :param asset_id: an asset ``Id``
        :type asset_id: ``osid.id.Id``
        :return: the returned ``AssetContent list``
        :rtype: ``osid.repository.AssetContentList``
        :raise: ``NullArgument`` -- ``asset_id`` is ``null``
        :raise: ``OperationFailed`` -- unable to complete request
        :raise: ``PermissionDenied`` -- authorization failure

        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        collection = JSONClientValidated('repository',
                                         collection='Asset',
                                         runtime=self._runtime)
        result = collection.find_one(
            dict({'_id': ObjectId(self._get_id(asset_id, 'repository').get_identifier())},
                 **self._view_filter()))
        asset_content_maps = [ac for ac in result['assetContents']]
        return objects.AssetContentList(asset_content_maps, runtime=self._runtime, proxy=self._proxy)

    @utilities.arguments_not_none
    def get_asset_contents_by_genus_type_for_asset(self, asset_content_genus_type, asset_id):
        \"\"\"Gets an ``AssetContentList`` from the given GenusType and Asset Id.

        In plenary mode, the returned list contains all known asset contents or
        an error results. Otherwise, the returned list may contain only
        those asset contents that are accessible through this session.

        :param asset_content_genus_type: an an asset content genus type
        :type asset_id: ``osid.type.Type``
        :param asset_id: an asset ``Id``
        :type asset_id: ``osid.id.Id``
        :return: the returned ``AssetContent list``
        :rtype: ``osid.repository.AssetContentList``
        :raise: ``NullArgument`` -- ``asset_content_genus_type`` or ``asset_id`` is ``null``
        :raise: ``OperationFailed`` -- unable to complete request
        :raise: ``PermissionDenied`` -- authorization failure

        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        collection = JSONClientValidated('repository',
                                         collection='Asset',
                                         runtime=self._runtime)
        result = collection.find_one(
            dict({'_id': ObjectId(self._get_id(asset_id, 'repository').get_identifier())},
                 **self._view_filter()))
        asset_content_maps = [ac for ac in result['assetContents'] if ac['genusTypeId'] == str(asset_content_genus_type)]
        return objects.AssetContentList(asset_content_maps, runtime=self._runtime, proxy=self._proxy)"""
        }
    }


class AssetAdminSession:

    # import_statements_pattern = [
    #     'from dlkit.abstract_osid.osid import errors',
    #     'from bson.objectid import ObjectId',
    #     'from ..utilities import JSONClientValidated',
    #     'CREATED = True',
    #     'UPDATED = True',
    # ]
    #
    # create_asset_content_template = """
    #     # Implemented from template for
    #     # osid.repository.AssetAdminSession.create_asset_content_template
    #     from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
    #     collection = JSONClientValidated('${package_name}',
    #                                      collection='${object_name}',
    #                                      runtime=self._runtime)
    #     if not isinstance(${arg0_name}, ABC${arg0_type}):
    #         raise errors.InvalidArgument('argument type is not an ${arg0_type}')
    #     if ${arg0_name}.is_for_update():
    #         raise errors.InvalidArgument('the ${arg0_type} is for update only, not create')
    #     try:
    #         if self._forms[${arg0_name}.get_id().get_identifier()] == CREATED:
    #             raise errors.IllegalState('${arg0_name} already used in a create transaction')
    #     except KeyError:
    #         raise errors.Unsupported('${arg0_name} did not originate from this session')
    #     if not ${arg0_name}.is_valid():
    #         raise errors.InvalidArgument('one or more of the form elements is invalid')
    #     ${arg0_name}._my_map['_id'] = ObjectId()
    #     ${object_name_under}_id = Id(${arg0_name}._my_map['${object_name_mixed}Id']).get_identifier()
    #     ${object_name_under} = collection.find_one(
    #         {'$$and': [{'_id': ObjectId(${object_name_under}_id)},
    #                   {'assigned' + self._catalog_name + 'Ids': {'$$in': [str(self._catalog_id)]}}]})
    #     ${object_name_under}['${aggregated_objects_name_mixed}'].append(${arg0_name}._my_map)
    #     result = collection.save(${object_name_under})
    #
    #     self._forms[${arg0_name}.get_id().get_identifier()] = CREATED
    #     from .${return_module} import ${aggregated_object_name}
    #     return ${return_type}(
    #         osid_object_map=${arg0_name}._my_map,
    #         runtime=self._runtime,
    #         proxy=self._proxy)"""
    #
    # get_asset_content_form_for_update_template = """
    #     # Implemented from template for
    #     # osid.repository.AssetAdminSession.get_asset_content_form_for_update_template
    #     from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
    #     from .${return_module} import ${return_type}
    #     collection = JSONClientValidated('${package_name}',
    #                                      collection='${object_name}',
    #                                      runtime=self._runtime)
    #     if not isinstance(${arg0_name}, ABC${arg0_type}):
    #         raise errors.InvalidArgument('the argument is not a valid OSID ${arg0_type}')
    #     document = collection.find_one({'${aggregated_objects_name_mixed}._id': ObjectId(${arg0_name}.get_identifier())})
    #     for sub_doc in document['${aggregated_objects_name_mixed}']:  # There may be a MongoDB shortcut for this
    #         if sub_doc['_id'] == ObjectId(${arg0_name}.get_identifier()):
    #             result = sub_doc
    #     obj_form = ${return_type}(
    #         osid_object_map=result,
    #         runtime=self._runtime,
    #         proxy=self._proxy)
    #     obj_form._for_update = True
    #     self._forms[obj_form.get_id().get_identifier()] = not UPDATED
    #     return obj_form"""
    #
    # update_asset_content_template = """
    #     # Implemented from template for
    #     # osid.repository.AssetAdminSession.update_asset_content_template
    #     from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
    #     collection = JSONClientValidated('${package_name}',
    #                                      collection='${object_name}',
    #                                      runtime=self._runtime)
    #     if not isinstance(${arg0_name}, ABC${arg0_type}):
    #         raise errors.InvalidArgument('argument type is not an ${arg0_type}')
    #     if not ${arg0_name}.is_for_update():
    #         raise errors.InvalidArgument('the ${arg0_type} is for update only, not create')
    #     try:
    #         if self._forms[${arg0_name}.get_id().get_identifier()] == UPDATED:
    #             raise errors.IllegalState('${arg0_name} already used in an update transaction')
    #     except KeyError:
    #         raise errors.Unsupported('${arg0_name} did not originate from this session')
    #     if not ${arg0_name}.is_valid():
    #         raise errors.InvalidArgument('one or more of the form elements is invalid')
    #     ${object_name_under}_id = Id(${arg0_name}._my_map['${object_name_mixed}Id']).get_identifier()
    #     ${object_name_under} = collection.find_one(
    #         {'$$and': [{'_id': ObjectId(${object_name_under}_id)},
    #                   {'assigned' + self._catalog_name + 'Ids': {'$$in': [str(self._catalog_id)]}}]})
    #     index = 0
    #     found = False
    #     for i in ${object_name_under}['${aggregated_objects_name_mixed}']:
    #         if i['_id'] == ObjectId(${arg0_name}._my_map['_id']):
    #             ${object_name_under}['${aggregated_objects_name_mixed}'].pop(index)
    #             ${object_name_under}['${aggregated_objects_name_mixed}'].insert(index, ${arg0_name}._my_map)
    #             found = True
    #             break
    #         index += 1
    #     if not found:
    #         raise errors.NotFound()
    #     try:
    #         collection.save(${object_name_under})
    #     except:  # what exceptions does mongodb save raise?
    #         raise errors.OperationFailed()
    #     self._forms[${arg0_name}.get_id().get_identifier()] = UPDATED
    #     # Note: this is out of spec. The OSIDs don't require an object to be returned:
    #     from .objects import ${aggregated_object_name}
    #
    #     return ${aggregated_object_name}(
    #         osid_object_map=${arg0_name}._my_map,
    #         runtime=self._runtime,
    #         proxy=self._proxy)"""
    #
    # delete_asset_content_template = """
    #     # Implemented from template for
    #     # osid.repository.AssetAdminSession.delete_asset_content_template
    #     from ${arg0_abcapp_name}.${arg0_abcpkg_name}.${arg0_module} import ${arg0_type} as ABC${arg0_type}
    #     from .objects import ${aggregated_object_name}
    #     collection = JSONClientValidated('${package_name}',
    #                                      collection='${object_name}',
    #                                      runtime=self._runtime)
    #     if not isinstance(${arg0_name}, ABC${arg0_type}):
    #         raise errors.InvalidArgument('the argument is not a valid OSID ${arg0_type}')
    #     ${object_name_under} = collection.find_one({'${aggregated_objects_name_mixed}._id': ObjectId(${arg0_name}.get_identifier())})
    #
    #     index = 0
    #     found = False
    #     for i in ${object_name_under}['${aggregated_objects_name_mixed}']:
    #         if i['_id'] == ObjectId(${arg0_name}.get_identifier()):
    #             ${aggregated_object_name_under}_map = ${object_name_under}['${aggregated_objects_name_mixed}'].pop(index)
    #         index += 1
    #         found = True
    #     if not found:
    #         raise errors.OperationFailed()
    #     ${aggregated_object_name}(
    #         osid_object_map=${aggregated_object_name_under}_map,
    #         runtime=self._runtime,
    #         proxy=self._proxy)._delete()
    #     collection.save(${object_name_under})"""

    additional_methods = {
        'python': {
            'json': """
    def _get_asset_id_with_enclosure(self, enclosure_id):
        \"\"\"Create an Asset with an enclosed foreign object.

        This is here to support AssetCompositionSession.set_asset. May need
        to add this in other objects to support other osid.Containable objects.
        return: (osid.id.Id) - the id of the new Asset

        \"\"\"
        mgr = self._get_provider_manager('REPOSITORY')
        query_session = mgr.get_asset_query_session_for_repository(self._catalog_id, proxy=self._proxy)
        query_form = query_session.get_asset_query()
        query_form.match_enclosed_object_id(enclosure_id)
        query_result = query_session.get_assets_by_query(query_form)
        if query_result.available() > 0:
            asset_id = query_result.next().get_id()
        else:
            create_form = self.get_asset_form_for_create([ENCLOSURE_RECORD_TYPE])
            create_form.set_enclosed_object(enclosure_id)
            asset_id = self.create_asset(create_form).get_id()
        return asset_id

    # This is out of spec, but used by the EdX / LORE record extensions...
    @utilities.arguments_not_none
    def duplicate_asset(self, asset_id):
        collection = JSONClientValidated('repository',
                                         collection='Asset',
                                         runtime=self._runtime)
        mgr = self._get_provider_manager('REPOSITORY')
        lookup_session = mgr.get_asset_lookup_session(proxy=self._proxy)
        lookup_session.use_federated_repository_view()
        try:
            lookup_session.use_unsequestered_asset_view()
        except AttributeError:
            pass
        asset_map = dict(lookup_session.get_asset(asset_id)._my_map)
        del asset_map['_id']
        if 'repositoryId' in asset_map:
            asset_map['repositoryId'] = str(self._catalog_id)
        if 'assignedRepositoryIds' in asset_map:
            asset_map['assignedRepositoryIds'] = [str(self._catalog_id)]
        insert_result = collection.insert_one(asset_map)
        result = objects.Asset(
            osid_object_map=collection.find_one({'_id': insert_result.inserted_id}),
            runtime=self._runtime,
            proxy=self._proxy)
        return result"""
        }
    }


# class CompositionLookupSession:

#     import_statements = [
#         'ACTIVE = 0',
#         'ANY_STATUS = 1',
#         'SEQUESTERED = 0',
#         'UNSEQUESTERED = 1',
#     ]
#
#     init_template = """
#     def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
#         OsidSession.__init__(self)
#         self._catalog_class = objects.${cat_name}
#         self._catalog_name = '${cat_name}'
#         OsidSession._init_object(
#             self,
#             catalog_id,
#             proxy,
#             runtime,
#             db_name='${pkg_name_replaced}',
#             cat_name='${cat_name}',
#             cat_class=objects.${cat_name})
#         self._kwargs = kwargs
#         self._status_view = ACTIVE
#         self._sequestered_view = SEQUESTERED
#
#     def _view_filter(self):
#         \"\"\"
#         Overrides OsidSession._view_filter to add sequestering filter.
#
#         \"\"\"
#         view_filter = OsidSession._view_filter(self)
#         if self._sequestered_view == SEQUESTERED:
#             view_filter['sequestered'] = False
#         return view_filter
# """

    # use_active_composition_view_template = """
    #     # Implemented from template for
    #     # osid.repository.CompositionLookupSession.use_active_composition_view_template
    #     self._status_view = ACTIVE"""
    #
    # use_any_status_composition_view_template = """
    #     # Implemented from template for
    #     # osid.repository.CompositionLookupSession.use_any_status_composition_view_template
    #     self._status_view = ANY_STATUS"""
    #
    # use_sequestered_composition_view_template = """
    #     # Implemented from template for
    #     # osid.repository.CompositionLookupSession.use_sequestered_composition_view_template
    #     self._sequestered_view = SEQUESTERED"""
    #
    # use_unsequestered_composition_view_template = """
    #     # Implemented from template for
    #     # osid.repository.CompositionLookupSession.use_unsequestered_composition_view_template
    #     self._sequestered_view = UNSEQUESTERED"""


# class CompositionQuerySession:

    # import_statements = [
    #     'ACTIVE = 0',
    #     'ANY_STATUS = 1',
    #     'SEQUESTERED = 0',
    #     'UNSEQUESTERED = 1',
    # ]
    #
    # init_template = CompositionLookupSession.init_template
    #
    # old_init = """
    # def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
    #     OsidSession.__init__(self)
    #     self._catalog_class = objects.Repository
    #     self._catalog_name = 'Repository'
    #     OsidSession._init_object(
    #         self,
    #         catalog_id,
    #         proxy,
    #         runtime,
    #         db_name='repository',
    #         cat_name='Repository',
    #         cat_class=objects.Repository)
    #     self._kwargs = kwargs
    #     self._status_view = ACTIVE
    #     self._sequestered_view = SEQUESTERED
    #
    # def _view_filter(self):
    #     \"\"\"
    #     Overrides OsidSession._view_filter to add sequestering filter.
    #
    #     \"\"\"
    #     view_filter = OsidSession._view_filter(self)
    #     if self._sequestered_view == SEQUESTERED:
    #         view_filter['sequestered'] = False
    #     return view_filter"""

    # old_use_sequestered_composition_view = """ #NOW TEMPLATED FROM LOOKUP SESSION
    #     self._sequestered_view = SEQUESTERED"""
    #
    # old_use_unsequestered_composition_view = """ #NOW TEMPLATED LOOKUP SESSION
    #     self._sequestered_view = UNSEQUESTERED"""


class CompositionSearchSession:

    import_statements = {
        'python': {
            'json': [
                'from . import searches',
            ]
        }
    }


# class AssetCompositionSession:

    # import_statements = [
    #     'from dlkit.primordium.id.primitives import Id'
    # ]

    # import_statements_pattern = [
    #     'from dlkit.primordium.id.primitives import Id'
    # ]
    #
    # old_init = """
    # def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
    #     OsidSession.__init__(self)
    #     self._catalog_class = objects.Repository
    #     self._catalog_name = 'Repository'
    #     OsidSession._init_object(
    #         self,
    #         catalog_id,
    #         proxy,
    #         runtime,
    #         db_name='repository',
    #         cat_name='Repository',
    #         cat_class=objects.Repository)
    #     self._kwargs = kwargs"""
    #
    # init_template = """
    # def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
    #     OsidSession.__init__(self)
    #     self._catalog_class = objects.${cat_name}
    #     self._catalog_name = '${cat_name}'
    #     OsidSession._init_object(
    #         self,
    #         catalog_id,
    #         proxy,
    #         runtime,
    #         db_name='${pkg_name_replaced}',
    #         cat_name='${cat_name}',
    #         cat_class=objects.${cat_name})
    #     self._kwargs = kwargs"""

    # can_access_asset_compositions_template = """
    #     # Implemented from template for
    #     # osid.repository.AssetCompositionSession.can_access_asset_compositions
    #     # NOTE: It is expected that real authentication hints will be
    #     # handled in a service adapter above the pay grade of this impl.
    #     return True"""
    #
    # old_get_composition_assets = """
    #     collection = JSONClientValidated('repository',
    #                                      collection='Composition',
    #                                      runtime=self._runtime)
    #     composition = collection.find_one(
    #         dict({'_id': ObjectId(composition_id.get_identifier())},
    #              **self._view_filter()))
    #     if 'assetIds' not in composition:
    #         raise errors.NotFound('no Assets are assigned to this Composition')
    #     asset_ids = []
    #     for idstr in composition['assetIds']:
    #         asset_ids.append(Id(idstr))
    #     mgr = self._get_provider_manager('REPOSITORY')
    #     als = mgr.get_asset_lookup_session(proxy=self._proxy)
    #     als.use_federated_repository_view()
    #     return als.get_assets_by_ids(asset_ids)"""
    #
    # get_composition_assets_template = """
    #     # Implemented from template for
    #     # osid.repository.AssetCompositionSession.get_composition_assets
    #     collection = JSONClientValidated('${package_name_replace}',
    #                                      collection='${containable_object_name}',
    #                                      runtime=self._runtime)
    #     ${containable_object_name_under} = collection.find_one(
    #         dict({'_id': ObjectId(${containable_object_name_under}_id.get_identifier())},
    #              **self._view_filter()))
    #     if '${object_name_mixed}Ids' not in ${containable_object_name_under}:
    #         raise errors.NotFound('no ${object_name_plural} are assigned to this ${containable_object_name}')
    #     ${object_name_under}_ids = []
    #     for idstr in ${containable_object_name_under}['${object_name_mixed}Ids']:
    #         ${object_name_under}_ids.append(Id(idstr))
    #     mgr = self._get_provider_manager('${package_name_replace_upper}')
    #     lookup_session = mgr.get_${object_name_under}_lookup_session(proxy=self._proxy)
    #     lookup_session.use_federated_${cat_name_under}_view()
    #     return lookup_session.get_${object_name_plural_under}_by_ids(${object_name_under}_ids)"""
    #
    # old_get_compositions_by_asset = """
    #     collection = JSONClientValidated('repository',
    #                                      collection='Composition',
    #                                      runtime=self._runtime)
    #     result = collection.find(
    #         dict({'assetIds': {'$in': [str(asset_id)]}},
    #              **self._view_filter())).sort('_id', DESCENDING)
    #     return objects.CompositionList(result, runtime=self._runtime)"""
    #
    # get_compositions_by_asset_template = """
    #     # Implemented from template for
    #     # osid.repository.AssetCompositionSession.get_compositions_by_asset
    #     collection = JSONClientValidated('${package_name_replace}',
    #                                      collection='${containable_object_name}',
    #                                      runtime=self._runtime)
    #     result = collection.find(
    #         dict({'${object_name_mixed}Ids': {'$$in': [str(${object_name_under}_id)]}},
    #              **self._view_filter())).sort('_id', DESCENDING)
    #     return objects.${return_type}(result, runtime=self._runtime)"""


# class AssetCompositionDesignSession:

# import_statements_pattern = [
#     'from ..list_utilities import move_id_ahead, move_id_behind, order_ids',
# ]
#
# old_init = """
# def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
#     OsidSession.__init__(self)
#     self._catalog_class = objects.Repository
#     self._catalog_name = 'Repository'
#     OsidSession._init_object(
#         self,
#         catalog_id,
#         proxy,
#         runtime,
#         db_name='repository',
#         cat_name='Repository',
#         cat_class=objects.Repository)
#     self._kwargs = kwargs"""
#
# init_template = """
# def __init__(self, catalog_id=None, proxy=None, runtime=None, **kwargs):
#     OsidSession.__init__(self)
#     self._catalog_class = objects.${cat_name}
#     self._catalog_name = '${cat_name}'
#     OsidSession._init_object(
#         self,
#         catalog_id,
#         proxy,
#         runtime,
#         db_name='${pkg_name_replaced}',
#         cat_name='${cat_name}',
#         cat_class=objects.${cat_name})
#     self._kwargs = kwargs"""

# old_can_compose_assets = """
#     return True"""

#     can_compose_assets_template = """
#         # Implemented from template for
#         # osid.repository.AssetCompositionDesignSession.can_compose_assets_template
#         # NOTE: It is expected that real authentication hints will be
#         # handled in a service adapter above the pay grade of this impl.
#         return True"""
#
#     add_asset_template = """
#         # The ${object_name_under} found check may want to be run through _get_provider_manager
#         # so as to ensure access control:
#         from dlkit.abstract_osid.id.primitives import Id as ABCId
#         if not isinstance(${object_name_under}_id, ABCId):
#             raise errors.InvalidArgument('the argument is not a valid OSID Id')
#         if (not isinstance(${containable_object_name_under}_id, ABCId) and
#                 ${containable_object_name_under}_id.get_identifier_namespace() != '${package_name_replace}.${containable_object_name}'):
#             raise errors.InvalidArgument('the argument is not a valid OSID Id')
#         if ${object_name_under}_id.get_identifier_namespace() != '${object_namespace}':
#             if ${object_name_under}_id.get_authority() != self._authority:
#                 raise errors.InvalidArgument()
#             else:
#                 mgr = self._get_provider_manager('${object_package_name_replace_upper}')
#                 admin_session = mgr.get_${object_name_under}_admin_session_for_${cat_name_under}(self._catalog_id, proxy=self._proxy)
#                 ${object_name_under}_id = admin_session._get_${object_name_under}_id_with_enclosure(${object_name_under}_id)
#         collection = JSONClientValidated('${object_package_name_replace}',
#                                          collection='${object_name}',
#                                          runtime=self._runtime)
#         ${object_name_under} = collection.find_one({'_id': ObjectId(${object_name_under}_id.get_identifier())})
#         collection = JSONClientValidated('${package_name_replace}',
#                                          collection='${containable_object_name}',
#                                          runtime=self._runtime)
#         ${containable_object_name_under} = collection.find_one({'_id': ObjectId(${containable_object_name_under}_id.get_identifier())})
#         if '${object_name_mixed}Ids' in ${containable_object_name_under}:
#             if str(${object_name_under}_id) not in ${containable_object_name_under}['${object_name_mixed}Ids']:
#                 ${containable_object_name_under}['${object_name_mixed}Ids'].append(str(${object_name_under}_id))
#         else:
#             ${containable_object_name_under}['${object_name_mixed}Ids'] = [str(${object_name_under}_id)]
#         collection.save(${containable_object_name_under})"""
#
#     older_move_asset_ahead_template = """
#         collection = JSONClientValidated('${package_name_replace}',
#                                          collection='${containable_object_name}',
#                                          runtime=self._runtime)
#         ${containable_object_name_under} = collection.find_one({'_id': ObjectId(${containable_object_name_under}_id.get_identifier())})
#         if '${object_name_mixed}Ids' not in ${containable_object_name_under}:
#             raise errors.NotFound('no ${object_name_plural} are assigned to this ${containable_object_name}')
#         ${containable_object_name_under}['${object_name_mixed}Ids'] = move_id_ahead(${object_name_under}_id, reference_id, ${containable_object_name_under}['${object_name_mixed}Ids'])
#         collection.save(${containable_object_name_under})"""
#
#     move_asset_ahead_template = """
#         if (not isinstance(${containable_object_name_under}_id, ABCId) and
#                 ${containable_object_name_under}_id.get_identifier_namespace() != '${package_name_replace}.${containable_object_name}'):
#             raise errors.InvalidArgument('the argument is not a valid OSID Id')
#         ${containable_object_name_under}_map, collection = self._get_${containable_object_name_under}_collection(${containable_object_name_under}_id)
#         ${containable_object_name_under}_map['${object_name_mixed}Ids'] = move_id_ahead(${object_name_under}_id, reference_id, ${containable_object_name_under}_map['${object_name_mixed}Ids'])
#         collection.save(${containable_object_name_under}_map)"""
#
#     older_move_asset_behind_template = """
#         collection = JSONClientValidated('${package_name_replace}',
#                                          collection='${containable_object_name}',
#                                          runtime=self._runtime)
#         ${containable_object_name_under} = collection.find_one({'_id': ObjectId(${containable_object_name_under}_id.get_identifier())})
#         if '${object_name_mixed}Ids' not in ${containable_object_name_under}:
#             raise errors.NotFound('no ${object_name_plural} are assigned to this ${containable_object_name}')
#         ${containable_object_name_under}['${object_name_mixed}Ids'] = move_id_behind(${object_name_under}_id, reference_id, ${containable_object_name_under}['${object_name_mixed}Ids'])
#         collection.save(${containable_object_name_under})"""
#
#     move_asset_behind_template = """
#         if (not isinstance(${containable_object_name_under}_id, ABCId) and
#                 ${containable_object_name_under}_id.get_identifier_namespace() != '${package_name_replace}.${containable_object_name}'):
#             raise errors.InvalidArgument('the argument is not a valid OSID Id')
#         ${containable_object_name_under}_map, collection = self._get_${containable_object_name_under}_collection(${containable_object_name_under}_id)
#         ${containable_object_name_under}_map['${object_name_mixed}Ids'] = move_id_behind(${object_name_under}_id, reference_id, ${containable_object_name_under}_map['${object_name_mixed}Ids'])
#         collection.save(${containable_object_name_under}_map)"""
#
#     older_order_assets_template = """
#         collection = JSONClientValidated('${package_name_replace}',
#                                          collection='${containable_object_name}',
#                                          runtime=self._runtime)
#         ${containable_object_name_under} = collection.find_one({'_id': ObjectId(${containable_object_name_under}_id.get_identifier())})
#         if '${object_name_mixed}Ids' not in ${containable_object_name_under}:
#             raise errors.NotFound('no ${object_name_plural} are assigned to this ${containable_object_name}')
#         ${containable_object_name_under}['${object_name_mixed}Ids'] = order_ids(${object_name_under}_ids, ${containable_object_name_under}['${object_name_mixed}Ids'])
#         collection.save(${containable_object_name_under})"""
#
#     order_assets_template = """
#         if (not isinstance(${containable_object_name_under}_id, ABCId) and
#                 ${containable_object_name_under}_id.get_identifier_namespace() != '${package_name_replace}.${containable_object_name}'):
#             raise errors.InvalidArgument('the argument is not a valid OSID Id')
#         ${containable_object_name_under}_map, collection = self._get_${containable_object_name_under}_collection(${containable_object_name_under}_id)
#         ${containable_object_name_under}_map['${object_name_mixed}Ids'] = order_ids(${object_name_under}_ids, ${containable_object_name_under}_map['${object_name_mixed}Ids'])
#         collection.save(${containable_object_name_under}_map)"""
#
#     older_remove_asset_template = """
#         collection = JSONClientValidated('${package_name_replace}',
#                                          collection='${containable_object_name}',
#                                          runtime=self._runtime)
#         ${containable_object_name_under} = collection.find_one({'_id': ObjectId(${containable_object_name_under}_id.get_identifier())})
#         try:
#             ${containable_object_name_under}['${object_name_mixed}Ids'].remove(str(${object_name_under}_id))
#         except (KeyError, ValueError):
#             raise errors.NotFound()
#         collection.save(${containable_object_name_under})"""
#
#     remove_asset_template = """
#         if (not isinstance(${containable_object_name_under}_id, ABCId) and
#                 ${containable_object_name_under}_id.get_identifier_namespace() != '${package_name_replace}.${containable_object_name}'):
#             raise errors.InvalidArgument('the argument is not a valid OSID Id')
#         ${containable_object_name_under}_map, collection = self._get_${containable_object_name_under}_collection(${containable_object_name_under}_id)
#         try:
#             ${containable_object_name_under}_map['${object_name_mixed}Ids'].remove(str(${object_name_under}_id))
#         except (KeyError, ValueError):
#             raise errors.NotFound()
#         collection.save(${containable_object_name_under}_map)
#
#     def _get_${containable_object_name_under}_collection(self, ${containable_object_name_under}_id):
#         \"\"\"Returns a Mongo Collection and ${containable_object_name} given a ${containable_object_name} Id\"\"\"
#         collection = JSONClientValidated('${package_name_replace}',
#                                          collection='${containable_object_name}',
#                                          runtime=self._runtime)
#         ${containable_object_name_under}_map = collection.find_one({'_id': ObjectId(${containable_object_name_under}_id.get_identifier())})
#         if '${object_name_mixed}Ids' not in ${containable_object_name_under}_map:
#             raise errors.NotFound('no ${object_name_plural} are assigned to this ${containable_object_name}')
#         return ${containable_object_name_under}_map, collection
# """


class Asset:

    import_statements = {
        'python': {
            'json': [
                'from ..primitives import DisplayText',
                'from ..id.objects import IdList',
                'from ..osid.markers import Extensible'
            ]
        }
    }

    # Note: self._catalog_name = 'Repository' below is currently
    # only for osid.OsidObject.get_object_map() setting the now deprecated
    # repositoryId element and may be removed someday
    init = {
        'python': {
            'json': """
    _namespace = 'repository.Asset'

    def __init__(self, **kwargs):
        osid_objects.OsidObject.__init__(self, object_name='ASSET', **kwargs)
        self._catalog_name = 'Repository'
        if self.is_composition():
            self._composition = self.get_composition()

    def __getattr__(self, name):
        if self.is_composition():
            try:
                return self._composition[name]
            except AttributeError:
                raise AttributeError()
        # HOW TO PASS TO EXTENSIBLE!!!!"""
        }
    }

    # get_title_template = """
    #     # Implemented from template for osid.repository.Asset.get_title_template
    #     return DisplayText(self._my_map['${var_name_mixed}'])"""

    # get_asset_content_ids_template = """
    #     # Implemented from template for osid.repository.Asset.get_asset_content_ids_template
    #     id_list = []
    #     for ${var_name} in self.get_${var_name_plural}():
    #         id_list.append(${var_name}.get_id())
    #     return IdList(id_list)"""

    # get_asset_contents_template = """
    #     # Implemented from template for osid.repository.Asset.get_asset_contents_template
    #     return ${aggregated_object_name}List(
    #         self._my_map['${var_name_plural_mixed}'],
    #         runtime=self._runtime,
    #         proxy=self._proxy)
    #
    # def _delete(self):
    #     for ${aggregated_object_name_under} in self.get_${aggregated_objects_name_under}():
    #         ${aggregated_object_name_under}._delete()
    #     osid_objects.OsidObject._delete(self)"""

    is_composition = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        return bool(self._my_map['compositionId'])"""
        }
    }

    is_copyright_status_known = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        return bool(self._my_map['copyright']['text'])"""
        }
    }

    additional_methods = {
        'python': {
            'json': """
    def get_object_map(self):
        obj_map = dict(self._my_map)
        obj_map['assetContent'] = obj_map['assetContents'] = [ac.object_map
                                                              for ac in self.get_asset_contents()]
        # note: assetContent is deprecated
        return osid_objects.OsidObject.get_object_map(self, obj_map)

    object_map = property(fget=get_object_map)"""
        }
    }


# class AssetSearch:
#
#     import_statements = [
#         'from dlkit.abstract_osid.osid import errors',
#         'from ..primitives import Id',
#         'from ..utilities import get_registry',
#         'from ..osid import searches as osid_searches',
#     ]
#
#     init = """
#     def __init__(self, runtime):
#         self._namespace = 'repository.Asset'
#         record_type_data_sets = get_registry('ASSET_RECORD_TYPES', runtime)
#         self._record_type_data_sets = record_type_data_sets
#         self._all_supported_record_type_data_sets = record_type_data_sets
#         self._all_supported_record_type_ids = []
#         self._id_list = None
#         for data_set in record_type_data_sets:
#             self._all_supported_record_type_ids.append(str(Id(**record_type_data_sets[data_set])))
#         osid_searches.OsidSearch.__init__(self, runtime)"""
#
#     search_among_assets = """
#         self._id_list = asset_ids"""


# class AssetSearchResults:
#
#     import_statements = [
#         'from dlkit.abstract_osid.osid import errors',
#         'from . import objects',
#     ]
#
#     init = """
#     def __init__(self, results, runtime):
#         # if you don't iterate, then .count() on the cursor is an inaccurate representation of limit / skip
#         self._results = results
#         self._runtime = runtime
#         self.retrieved = False"""
#
#     get_assets = """
#         if self.retrieved:
#             raise errors.IllegalState('List has already been retrieved.')
#         self.retrieved = True
#         return objects.AssetList(self._results, runtime=self._runtime)"""


class AssetSearchSession:

    import_statements = {
        'python': {
            'json': [
                'from . import searches',
            ]
        }
    }


class AssetContent:

    import_statements = {
        'python': {
            'json': [
                'import gridfs',
                'from ..primitives import DataInputStream',
                'from ..utilities import JSONClientValidated'
            ]
        }
    }

    # has_url_template = """
    #     # Implemented from template for osid.repository.AssetContent.has_url_template
    #     try:
    #         return bool(self._my_map['${var_name_mixed}'])
    #     except KeyError:
    #         return False"""
    #
    # get_url_template = """
    #     # Implemented from template for osid.repository.AssetContent.get_url_template
    #     if not bool(self._my_map['${var_name_mixed}']):
    #         raise errors.IllegalState()
    #     return self._my_map['${var_name_mixed}']"""

    get_data = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        if not bool(self._my_map['data']):
            raise errors.IllegalState('no data')
        dbase = JSONClientValidated('repository',
                                    runtime=self._runtime).raw()
        filesys = gridfs.GridFS(dbase)
        return DataInputStream(filesys.get(self._my_map['data']))"""
        }
    }

    additional_methods = {
        'python': {
            'json': """
    def _delete(self):
        dbase = JSONClientValidated('repository',
                                    runtime=self._runtime).raw()
        try:
            filesys = gridfs.GridFS(dbase)
        except TypeError:
            # Not MongoDB, perhaps filesystem. Assume this is then taken care of in
            # an adapter.
            pass
        else:
            if self._my_map['data'] and filesys.exists(self._my_map['data']):
                filesys.delete(self._my_map['data'])
        osid_objects.OsidObject._delete(self)"""
        }
    }


class AssetContentForm:

    import_statements = {
        'python': {
            'json': [
                'import base64',
                'import gridfs',
                'from ..primitives import DataInputStream',
                'from dlkit.abstract_osid.osid import errors',
                'from ..utilities import JSONClientValidated'
            ]
        }
    }

    set_data = {
        'python': {
            'json': """
    def ${method_name}(self, data):
        ${doc_string}
        if data is None:
            raise errors.NullArgument('data cannot be None')
        if not isinstance(data, DataInputStream):
            raise errors.InvalidArgument('data must be instance of DataInputStream')
        dbase = JSONClientValidated('repository',
                                    runtime=self._runtime).raw()
        filesys = gridfs.GridFS(dbase)
        self._my_map['data'] = filesys.put(data._my_data)
        data._my_data.seek(0)
        self._my_map['base64'] = base64.b64encode(data._my_data.read())"""
        }
    }

    clear_data = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        if (self.get_data_metadata().is_read_only() or
                self.get_data_metadata().is_required()):
            raise errors.NoAccess()
        if self._my_map['data'] == self._data_default:
            return
        dbase = JSONClientValidated('repository',
                                    runtime=self._runtime).raw()
        filesys = gridfs.GridFS(dbase)
        filesys.delete(self._my_map['data'])
        self._my_map['data'] = self._data_default
        del self._my_map['base64']"""
        }
    }


class Composition:

    # This two methods are defined here because of an inconsistency with
    # Naming conventions.  The pattern mapper expected get_child_ids.  The second
    # should otherwise come from the template for learning.Activity.get_asset_ids
    get_children_ids = {
        'pythohn': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        return IdList(self._my_map['childIds'])

    def get_child_ids(self):
        return self.get_children_ids()"""
        }
    }

    additional_methods = {
        'python': {
            'json': """
    def get_object_map(self):
        obj_map = dict(self._my_map)
        if 'assetIds' in obj_map:
            del obj_map['assetIds']
        return osid_objects.OsidObject.get_object_map(self, obj_map)

    object_map = property(fget=get_object_map)"""
        }
    }


class CompositionForm:
    # per Tom Coppeto. We are moving composition design to the CompositionForm
    additional_methods = {
        'python': {
            'json': """
    def get_children_metadata(self):
        \"\"\"Gets the metadata for children.

        return: (osid.Metadata) - metadata for the children
        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        metadata = dict(self._mdata['children'])
        metadata.update({'existing_children_values': self._my_map['childIds']})
        return Metadata(**metadata)

    children_metadata = property(fget=get_children_metadata)

    @utilities.arguments_not_none
    def set_children(self, child_ids):
        \"\"\"Sets the children.

        arg:    child_ids (osid.id.Id[]): the children``Ids``
        raise:  InvalidArgument - ``child_ids`` is invalid
        raise:  NoAccess - ``Metadata.isReadOnly()`` is ``true``
        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        if not isinstance(child_ids, list):
            raise errors.InvalidArgument()
        if self.get_children_metadata().is_read_only():
            raise errors.NoAccess()
        idstr_list = []
        for object_id in child_ids:
            if not self._is_valid_id(object_id):
                raise errors.InvalidArgument()
            if str(object_id) not in idstr_list:
                idstr_list.append(str(object_id))
        self._my_map['childIds'] = idstr_list

    def clear_children(self):
        \"\"\"Clears the children.

        raise:  NoAccess - ``Metadata.isRequired()`` or
                ``Metadata.isReadOnly()`` is ``true``
        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        if (self.get_children_metadata().is_read_only() or
                self.get_children_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['childIds'] = self._children_default

    children = property(fset=set_children, fdel=clear_children)"""
        }
    }


class CompositionQuery:
    match_containing_composition_id = {
        'python': {
            'json': """
    def ${method_name}(self, composition_id, match):
        ${doc_string}
        # I'm not sure this does what the spec says it should do...
        #   I think it should look at a hierarchy of compositions.
        self._add_match('_id', composition_id.identifier, match)"""
        }
    }

    clear_containing_composition_id_terms = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        self._clear_terms('_id')"""
        }
    }

    match_contained_composition_id = {
        'python': {
            'json': """
    def ${method_name}(self, composition_id, match):
        ${doc_string}
        self._add_match('childIds', str(composition_id), match)"""
        }
    }

    clear_contained_composition_id_terms = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        self._clear_terms('childIds')"""
        }
    }

    match_asset_id = {
        'python': {
            'json': """
    def ${method_name}(self, asset_id, match):
        ${doc_string}
        self._add_match('assetIds', str(asset_id), match)"""
        }
    }

    clear_asset_id_terms = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        self._clear_terms('assetIds')"""
        }
    }


class CompositionAdminSession:
    additional_methods = {
        'python': {
            'json': """
    # This is out of spec, but used by the EdX / LORE record extensions...
    @utilities.arguments_not_none
    def duplicate_composition(self, composition_id):
        collection = JSONClientValidated('repository',
                                         collection='Composition',
                                         runtime=self._runtime)
        mgr = self._get_provider_manager('REPOSITORY')
        lookup_session = mgr.get_composition_lookup_session(proxy=self._proxy)
        lookup_session.use_federated_repository_view()
        try:
            lookup_session.use_unsequestered_composition_view()
        except AttributeError:
            pass
        composition_map = dict(lookup_session.get_composition(composition_id)._my_map)
        del composition_map['_id']
        if 'repositoryId' in composition_map:
            composition_map['repositoryId'] = str(self._catalog_id)
        if 'assignedRepositoryIds' in composition_map:
            composition_map['assignedRepositoryIds'] = [str(self._catalog_id)]
        insert_result = collection.insert_one(composition_map)
        result = objects.Composition(
            osid_object_map=collection.find_one({'_id': insert_result.inserted_id}),
            runtime=self._runtime,
            proxy=self._proxy)
        return result"""
        }
    }


# class CompositionSearch:
#
#     import_statements = [
#         'from dlkit.abstract_osid.osid import errors',
#         'from ..primitives import Id',
#         'from ..utilities import get_registry',
#         'from ..osid import searches as osid_searches',
#     ]
#
#     init = """
#     def __init__(self, runtime):
#         self._namespace = 'repository.Composition'
#         record_type_data_sets = get_registry('COMPOSITION_RECORD_TYPES', runtime)
#         self._record_type_data_sets = record_type_data_sets
#         self._all_supported_record_type_data_sets = record_type_data_sets
#         self._all_supported_record_type_ids = []
#         self._id_list = None
#         for data_set in record_type_data_sets:
#             self._all_supported_record_type_ids.append(str(Id(**record_type_data_sets[data_set])))
#         osid_searches.OsidSearch.__init__(self, runtime)"""
#
#     search_among_compositions = """
#         self._id_list = composition_ids"""


# class CompositionSearchResults:
#
#     import_statements = [
#         'from dlkit.abstract_osid.osid import errors',
#         'from . import objects',
#     ]
#
#     init = """
#     def __init__(self, results, runtime):
#         # if you don't iterate, then .count() on the cursor is an inaccurate representation of limit / skip
#         self._results = results
#         self._runtime = runtime
#         self.retrieved = False"""
#
#     get_compositions = """
#         if self.retrieved:
#             raise errors.IllegalState('List has already been retrieved.')
#         self.retrieved = True
#         return objects.CompositionList(self._results, runtime=self._runtime)"""


class CompositionRepositorySession:
    get_repository_ids_by_composition = {
        'python': {
            'json': """
    def ${method_name}(self, composition_id):
        ${doc_string}
        mgr = self._get_provider_manager('REPOSITORY', local=True)
        lookup_session = mgr.get_composition_lookup_session(proxy=self._proxy)
        lookup_session.use_federated_repository_view()
        lookup_session.use_unsequestered_composition_view()
        composition = lookup_session.get_composition(composition_id)
        id_list = []
        if 'assignedRepositoryIds' in composition._my_map:
            for idstr in composition._my_map['assignedRepositoryIds']:
                id_list.append(Id(idstr))
        return IdList(id_list)"""
        }
    }


class AssetQuerySession:
    additional_methods = {
        'python': {
            'json': """
    def get_asset_content_query(self):
        return queries.AssetContentQuery(runtime=self._runtime)

    def get_asset_contents_by_query(self, asset_content_query):
        import re
        and_list = list()
        or_list = list()
        for term in asset_content_query._query_terms:
            content_term = 'assetContents.{0}'.format(term)
            and_list.append({content_term: asset_content_query._query_terms[term]})
        for term in asset_content_query._keyword_terms:
            content_term = 'assetContents.{0}'.format(term)
            or_list.append({content_term: asset_content_query._keyword_terms[term]})
        if or_list:
            and_list.append({'$or': or_list})
        view_filter = self._view_filter()
        if view_filter:
            and_list.append(view_filter)
        if and_list:
            query_terms = {'$and': and_list}
        collection = JSONClientValidated('repository',
                                         collection='Asset',
                                         runtime=self._runtime)
        result = collection.find(query_terms).sort('_id', DESCENDING)

        # these are Asset results ... need to pull out the matching contents
        matching_asset_contents = []
        for asset in result:
            for asset_content in asset['assetContents']:
                is_match = True

                # all the ANDs must be true for this to still be a match
                for term in asset_content_query._query_terms:
                    if '.' in term:
                        # is nested
                        split_terms = term.split('.')  # assume 2 max
                        for key, value in asset_content[split_terms[0]].items():
                            if key == split_terms[1]:
                                search_value = asset_content_query._query_terms[term]
                                if isinstance(search_value, dict):
                                    search_value = search_value['$in'][0]
                                if isinstance(search_value, re._pattern_type):
                                    # then we need to do a regex comparison on the content value
                                    if search_value.match(value) is None:
                                        is_match = False
                                elif value != asset_content_query._query_terms[term]:
                                    is_match = False
                    else:
                        if asset_content[term] != asset_content_query._query_terms[term]:
                            is_match = False

                # check the ORs
                for term in asset_content_query._keyword_terms:
                    if '.' in term:
                        # is nested
                        split_terms = term.split('.')
                        for key, value in asset_content[split_terms[0]].items():
                            if key == split_terms[1] and asset_content_query._keyword_terms[term] in value:
                                is_match = True
                                break
                    else:
                        if asset_content_query._keyword_terms[term] in asset_content[term]:
                            is_match = True
                            break

                if is_match:
                    matching_asset_contents.append(asset_content)

        return objects.AssetContentList(matching_asset_contents,
                                        runtime=self._runtime,
                                        proxy=self._proxy)"""
        }
    }
