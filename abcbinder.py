from build_controller import BaseBuilder
from interface_builders import InterfaceBuilder
from mappers import Mapper

# These next two are here for the purpose of loading abc modules
# in a django app, where the goal is to distribute the abc osids
# across the service kit packages.
# from djbuilder_settings import APPNAMEPREFIX as app_prefix
# from djbuilder_settings import APPNAMESUFFIX as app_suffix


class ABCBuilder(InterfaceBuilder, Mapper, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(ABCBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path

        self._root_dir = build_dir + '/abstract_osid'
        self._make_dir(self._root_dir)

        self._class = 'abc'

    def _additional_methods(self, interface):
        additional_methods = ''
        # Add the equality methods to Ids and Types:
        if interface['shortname'] in ['Id', 'Type']:
            additional_methods += eq_methods(interface['shortname'])
            additional_methods += str_methods()
        return additional_methods

    def additional_classes(self, interface):
        additional_classes = ''
        if interface['shortname'] == 'AssetLookupSession':
            additional_classes += asset_content_lookup_session()
        return additional_classes

    def _get_method_args(self, method, interface):
        args = ['self']
        args += [a['var_name'].strip() for a in method['args']]
        return args

    @staticmethod
    def _get_method_doc(method):
        return filter(None, [method['sphinx_param_doc'].strip('\n'),
                             method['sphinx_return_doc'].strip('\n'),
                             method['sphinx_error_doc'].strip('\n') + '\n',
                             method['compliance_doc'].strip('\n'),
                             method['impl_notes_doc'].strip('\n')])

    def _make_method(self, method, interface):
        decorator = self._ind + '@abc.abstractmethod'
        args = self._get_method_args(method, interface)
        method_impl = self._make_method_impl(method, interface)

        method_sig = '{0}def {1}({2}):'.format(self._ind,
                                               method['name'],
                                               ', '.join(args))

        method_doc = self._build_method_doc(method)

        return (decorator + '\n' +
                self._wrap(method_sig) + '\n' +
                self._wrap(method_doc) + '\n' +
                self._wrap(method_impl))

    def _make_method_impl(self, method, interface):
        if method['return_type'].strip():
            return '{}return  # {}'.format(self._dind,
                                           method['return_type'])
        else:
            return '{}pass'.format(self._dind)

    def build_this_interface(self, interface):
        return True

    def make(self):
        self.make_osids(build_abc=True)

    def module_body(self, interface):
        inheritance = self._get_class_inheritance(interface)
        end_methods = '{0}\n{1}\n{2}'.format(self._additional_methods(interface),
                                             self.make_methods(interface),
                                             self.additional_classes(interface))
        if end_methods.strip() == '':
            end_methods = end_methods.strip()

        return '\n\n{0}\n{1}\n{2}__metaclass__ = abc.ABCMeta\n{3}'.format(self.class_sig(interface, inheritance),
                                                                          self.class_doc(interface),
                                                                          self._ind,
                                                                          end_methods)

    def module_header(self, module):
        return ('\"\"\"Implementations of ' + self.package['name'] +
                ' abstract base class ' + module + '.\"\"\"\n' +
                '# pylint: disable=invalid-name\n' +
                '#     Method names comply with OSID specification.\n' +
                '# pylint: disable=no-init\n' +
                '#     Abstract classes do not define __init__.\n' +
                '# pylint: disable=too-few-public-methods\n' +
                '#     Some interfaces are specified as \'markers\' and include no methods.\n' +
                '# pylint: disable=too-many-public-methods\n' +
                '#     Number of methods are defined in specification\n' +
                '# pylint: disable=too-many-ancestors\n' +
                '#     Inheritance defined in specification\n' +
                '# pylint: disable=too-many-arguments\n' +
                '#     Argument signature defined in specification.\n' +
                '# pylint: disable=duplicate-code\n' +
                '#     All apparent duplicates have been inspected. They aren\'t.\n' +
                'import abc')

    def write_license_file(self):
        with open(self._abc_module('license'), 'w') as write_file:
            write_file.write((self._utf_code + '\"\"\"' +
                              self.package['title'] + '\n' +
                              self.package['name'] + ' version ' +
                              self.package['version'] + '\n\n' +
                              self.package['copyright'] + '\n\n' +
                              self.package['license'] + '\n\n\"\"\"').encode('utf-8') +
                             '\n')


def eq_methods(interface_name):
    return ("""
    def __hash__(self):
        return hash((self.get_authority(),
                     self.get_identifier_namespace(),
                     self.get_identifier()))

    def __eq__(self, other):
        if isinstance(other, """ + interface_name + """):
            return (
                self.get_authority() == other.get_authority() and
                self.get_identifier_namespace() == other.get_identifier_namespace() and
                self.get_identifier() == other.get_identifier()
            )
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

""")


def str_methods():
    return ("""
    def __str__(self):
        \"\"\"Provides serialized version of Id\"\"\"
        return self._escape(self._escape(self.get_identifier_namespace()) + ':' +
                            self._escape(self.get_identifier()) + '@' +
                            self._escape(self.get_authority()))

    def _escape(self, string):
        \"\"\"Private method for escaping : and @\"\"\"
        return string.replace("%", "%25").replace(":", "%3A").replace("@", "%40")

    def _unescape(self, string):
        \"\"\"Private method for un-escaping : and @\"\"\"
        return string.replace("%40", "@").replace("%3A", ":").replace("%25", "%")

""")


def asset_content_lookup_session():
    return ("""


class AssetContentLookupSession:
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
    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def get_repository_id(self):
        \"\"\"Gets the ``Repository``  ``Id`` associated with this session.

        :return: the ``Repository Id`` associated with this session
        :rtype: ``osid.id.Id``


        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        return # osid.id.Id

    repository_id = property(fget=get_repository_id)

    @abc.abstractmethod
    def get_repository(self):
        \"\"\"Gets the ``Repository`` associated with this session.

        :return: the ``Repository`` associated with this session
        :rtype: ``osid.repository.Repository``
        :raise: ``OperationFailed`` -- unable to complete request
        :raise: ``PermissionDenied`` -- authorization failure

        *compliance: mandatory -- This method must be implemented.*

        \"\"\"
        return # osid.repository.Repository

    repository = property(fget=get_repository)

    @abc.abstractmethod
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
        return # boolean

    @abc.abstractmethod
    def use_comparative_asset_content_view(self):
        \"\"\"The returns from the lookup methods may omit or translate elements based on this session, such as authorization, and not result in an error.

        This view is used when greater interoperability is desired at
        the expense of precision.



        *compliance: mandatory -- This method is must be implemented.*

        \"\"\"
        pass

    @abc.abstractmethod
    def use_plenary_asset_content_view(self):
        \"\"\"A complete view of the ``Asset`` returns is desired.

        Methods will return what is requested or result in an error.
        This view is used when greater precision is desired at the
        expense of interoperability.



        *compliance: mandatory -- This method is must be implemented.*

        \"\"\"
        pass

    @abc.abstractmethod
    def use_federated_repository_view(self):
        \"\"\"Federates the view for methods in this session.

        A federated view will include assets in repositories which are
        children of this repository in the repository hierarchy.



        *compliance: mandatory -- This method is must be implemented.*

        \"\"\"
        pass

    @abc.abstractmethod
    def use_isolated_repository_view(self):
        \"\"\"Isolates the view for methods in this session.

        An isolated view restricts lookups to this repository only.



        *compliance: mandatory -- This method is must be implemented.*

        \"\"\"
        pass

    @abc.abstractmethod
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
        return # osid.repository.AssetContent

    @abc.abstractmethod
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
        return # osid.repository.AssetContentList

    @abc.abstractmethod
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
        return # osid.repository.AssetContentList

    @abc.abstractmethod
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
        return # osid.repository.AssetContentList

    @abc.abstractmethod
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
        return # osid.repository.AssetContentList

    @abc.abstractmethod
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
        return  # osid.repository.AssetContentList

    @abc.abstractmethod
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
        return  # osid.repository.AssetContentList""")
