from copy import deepcopy


class GenericObjectForm:
    import_statements_pattern = {
        'python': {
            'json': [
                'import importlib',
                'import base64',
                'import gridfs',
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id, DateTime, Duration, DataInputStream',
                'from ..osid.metadata import Metadata',
                'from . import default_mdata',
                'from ..utilities import get_registry',
                'from ..utilities import update_display_text_defaults',
                'from ..utilities import JSONClientValidated'
            ],
            'tests': [
                'from dlkit.json_.osid.metadata import Metadata',
                'from dlkit.primordium.type.primitives import Type',
                'from dlkit.primordium.id.primitives import Id',
                'from dlkit.abstract_osid.id.primitives import Id as ABC_Id',
                'from dlkit.abstract_osid.locale.primitives import DisplayText as ABC_DisplayText'
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    ${pattern_name}
    _namespace = '${implpkg_name}.${object_name}'

    def __init__(self, **kwargs):
        ${init_object}.__init__(self, object_name='${object_name_upper}', **kwargs)
        self._mdata = default_mdata.get_${object_name_under}_mdata()
        self._init_metadata(**kwargs)
        if not self.is_for_update():
            self._init_map(**kwargs)

    def _init_metadata(self, **kwargs):
        \"\"\"Initialize form metadata\"\"\"
${metadata_super_initers}        ${init_object}._init_metadata(self, **kwargs)
        ${metadata_initers}
    def _init_map(self, record_types=None, **kwargs):
        \"\"\"Initialize form map\"\"\"
${map_super_initers}        ${init_object}._init_map(self, record_types=record_types)
${persisted_initers}""",
            'tests': """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::ResourceForm::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    if not is_never_authz(request.cls.service_config):
        create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::ResourceForm::init_template
    if not is_never_authz(request.cls.service_config):
        request.cls.form = request.cls.catalog.get_${object_name_under}_form_for_create([])"""
        }
    }

    # this needs to be re-designed to know about variable syntax type
    get_simple_attribute_metadata_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        metadata = dict(self._mdata['${var_name}'])
        metadata.update({'existing_${syntax_under}_values': self._my_map['${var_name_mixed}']})
        return Metadata(**metadata)""",
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        mdata = self.form.${method_name}()
        assert isinstance(mdata, Metadata)
        assert isinstance(mdata.get_element_id(), ABC_Id)
        assert isinstance(mdata.get_element_label(), ABC_DisplayText)
        assert isinstance(mdata.get_instructions(), ABC_DisplayText)
        assert mdata.get_syntax() == '${syntax}'
        assert not mdata.is_array()
        assert isinstance(mdata.is_required(), bool)
        assert isinstance(mdata.is_read_only(), bool)
        assert isinstance(mdata.is_linked(), bool)"""
        }
    }

    get_id_attribute_metadata_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        metadata = dict(self._mdata['${var_name}'])
        metadata.update({'existing_${syntax_under}_values': self._my_map['${var_name_mixed}Id']})
        return Metadata(**metadata)""",
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        mdata = self.form.${method_name}()
        assert isinstance(mdata, Metadata)
        assert isinstance(mdata.get_element_id(), ABC_Id)
        assert isinstance(mdata.get_element_label(), ABC_DisplayText)
        assert isinstance(mdata.get_instructions(), ABC_DisplayText)
        assert mdata.get_syntax() == '${syntax}'
        assert not mdata.is_array()
        assert isinstance(mdata.is_required(), bool)
        assert isinstance(mdata.is_read_only(), bool)
        assert isinstance(mdata.is_linked(), bool)"""
        }
    }

    set_simple_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess('${arg0_name} is read only')
        if not self._is_valid_${arg0_type}(${arg0_name}):
            raise errors.InvalidArgument('${arg0_name} is not a valid ${arg0_type}')
        self._my_map['${var_name_mixed}'] = ${arg0_name}""",
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        self.form.${method_name}(True)
        assert self.form._my_map['${var_name_mixed}']
        with pytest.raises(errors.InvalidArgument):
            self.form.${method_name}('false')"""
        }
    }

    clear_simple_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess('Sorry you cannot clear ${var_name}')
        self._my_map['${var_name_mixed}'] = self._${var_name}_default""",
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        self.form.set_${var_name}(True)
        assert self.form._my_map['${var_name_mixed}']
        self.form.${method_name}()
        assert self.form._my_map['${var_name_mixed}'] is None"""
        }
    }

    set_id_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess('${arg0_name} is read only')
        if not self._is_valid_${syntax_under}(${arg0_name}):
            raise errors.InvalidArgument('${arg0_name} is not a valid ${syntax}')
        self._my_map['${var_name_mixed}Id'] = str(${arg0_name})""",
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        assert self.form._my_map['${var_name_mixed}Id'] == ''
        self.form.set_${var_name}(Id('repository.Asset%3Afake-id%40ODL.MIT.EDU'))
        assert self.form._my_map['${var_name_mixed}Id'] == 'repository.Asset%3Afake-id%40ODL.MIT.EDU'
        with pytest.raises(errors.InvalidArgument):
            self.form.${method_name}(True)"""
        }
    }

    clear_id_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess('Sorry you cannot clear ${var_name}')
        self._my_map['${var_name_mixed}Id'] = self._${var_name}_default""",
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        self.form.set_${var_name}(Id('repository.Asset%3Afake-id%40ODL.MIT.EDU'))
        assert self.form._my_map['${var_name_mixed}Id'] == 'repository.Asset%3Afake-id%40ODL.MIT.EDU'
        self.form.${method_name}()
        assert self.form._my_map['${var_name_mixed}Id'] == self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0]"""
        }
    }

    get_object_form_record_template = {
        'python': {
            'json': """
    def ${method_name}(self, $arg0_name):
        ${doc_string}
        ${pattern_name}
        return self._get_record(${arg0_name})""",
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        with pytest.raises(errors.Unsupported):
            self.form.${method_name}(Type('osid.Osid%3Afake-record%40ODL.MIT.EDU'))
        # Here check for a real record?"""
        }
    }

    get_id_list_attribute_metadata_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        metadata = dict(self._mdata['${var_name}'])
        metadata.update({'existing_${var_name}_values': self._my_map['${var_name_singular_mixed}Ids']})
        return Metadata(**metadata)""",
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        if not is_never_authz(self.service_config):
            assert isinstance(self.form.${method_name}(), Metadata)"""
        }
    }

    set_id_list_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        if not isinstance(${arg0_name}, list):
            raise errors.InvalidArgument()
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        idstr_list = []
        for object_id in ${arg0_name}:
            if not self._is_valid_${syntax_under}(object_id):
                raise errors.InvalidArgument('{0} is not a valid ${syntax}'.format(object_id))
            idstr_list.append(str(object_id))
        self._my_map['${var_name_singular_mixed}Ids'] = idstr_list""",
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        if not is_never_authz(self.service_config):
            test_id = Id('osid.Osid%3A1%40ODL.MIT.EDU')
            self.form.${method_name}([test_id])
            assert len(self.form._my_map['${var_name_singular_mixed}Ids']) == 1
            assert self.form._my_map['${var_name_singular_mixed}Ids'][0] == str(test_id)
            with pytest.raises(errors.InvalidArgument):
                self.form.${method_name}('this is not a list')
            # reset this for other tests
            self.form._my_map['${var_name_singular_mixed}Ids'] = list()"""
        }
    }

    clear_id_list_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess('Sorry you cannot clear ${var_name}')
        self._my_map['${var_name_singular_mixed}Ids'] = self._${var_name}_default""",
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        if not is_never_authz(self.service_config):
            test_id = Id('osid.Osid%3A1%40ODL.MIT.EDU')
            self.form.set_${var_name}([test_id])
            assert len(self.form._my_map['${var_name_singular_mixed}Ids']) == 1
            assert self.form._my_map['${var_name_singular_mixed}Ids'][0] == str(test_id)
            self.form.${method_name}()
            assert self.form._my_map['${var_name_singular_mixed}Ids'] == []"""
        }
    }

    clear_single_id_list_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess('Sorry you cannot clear ${var_name}')
        if not isinstance(${arg0_name}, ${arg0_type}):
            raise errors.InvalidArgument('${arg0_name} is not ${arg0_type}')
        self._my_map['${var_name_singular_mixed}Ids'] = [current_id for current_id in self._my_map['${var_name_singular_mixed}Ids']
                                                         if current_id != str(${arg0_name})]"""
        }
    }

    set_display_text_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        self._my_map['${var_name_mixed}'] = self._get_display_text(${arg0_name}, self.get_${var_name}_metadata())"""
        }
    }

    # The only thing different from the generic ``clear_simple_attribute_template`` is the ``dict()`` call
    clear_display_text_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess('Sorry you cannot clear ${var_name}')
        self._my_map['${var_name_mixed}'] = dict(self._${var_name}_default)"""
        }
    }

    # Make this separate from ``set_simple_attribute_template`` because the string validation
    #   method has additional arguments
    set_string_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess('${arg0_name} is read only')
        if not self._is_valid_${arg0_type}(
                ${arg0_name},
                self.get_${var_name}_metadata()):
            raise errors.InvalidArgument('${arg0_name} is not a valid string')
        self._my_map['${var_name_mixed}'] = ${arg0_name}"""
        }
    }

    clear_string_attribute_template = clear_simple_attribute_template

    set_decimal_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess('${arg0_name} is read only')
        try:
            ${arg0_name} = float(${arg0_name})
        except ValueError:
            raise errors.InvalidArgument('${arg0_name} needs to be a float')
        if not self._is_valid_${arg0_type}(${arg0_name}, self.get_${var_name}_metadata()):
            raise errors.InvalidArgument('${arg0_name} is not a valid float')
        self._my_map['${var_name_mixed}'] = ${arg0_name}"""
        }
    }

    clear_decimal_attribute_template = clear_simple_attribute_template

    set_date_time_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess('${arg0_name} is read only')
        if not isinstance(${arg0_name}, DateTime):
            raise errors.InvalidArgument('${arg0_name} is not a DateTime')
        if not self._is_valid_${arg0_type_under}(
                ${arg0_name},
                self.get_${var_name}_metadata()):
            raise errors.InvalidArgument('${arg0_name} is not a valid DateTime')
        self._my_map['${var_name_mixed}'] = ${arg0_name}""",
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        if not is_never_authz(self.service_config):
            test_time = DateTime.utcnow()
            assert self.form._my_map['${var_name_mixed}'] is None
            self.form.${method_name}(test_time)
            assert self.form._my_map['${var_name_mixed}'] == test_time
            with pytest.raises(errors.InvalidArgument):
                self.form.${method_name}(True)
            # reset this for other tests
            self.form._my_map['${var_name_mixed}'] = None"""
        }
    }

    clear_date_time_attribute_template = deepcopy(clear_simple_attribute_template)
    clear_date_time_attribute_template['python']['tests'] = """
    def test_${method_name}(self):
        ${pattern_name}
        if not is_never_authz(self.service_config):
            test_time = DateTime.utcnow()
            assert self.form._my_map['${var_name_mixed}'] is None
            self.form.set_${var_name}(test_time)
            assert self.form._my_map['${var_name_mixed}'] == test_time
            self.form.${method_name}()
            assert self.form._my_map['${var_name_mixed}'] == self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0]"""

    set_duration_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess('${arg0_name} is read only')
        if not isinstance(${arg0_name}, Duration):
            raise errors.InvalidArgument('${arg0_name} is not a Duration')
        if not self._is_valid_${arg0_type_under}(
                ${arg0_name},
                self.get_${var_name}_metadata()):
            raise errors.InvalidArgument('${arg0_name} is not a valid Duration')
        map = dict()
        map['days'] = ${arg0_name}.days
        map['seconds'] = ${arg0_name}.seconds
        map['microseconds'] = ${arg0_name}.microseconds
        self._my_map['${var_name_mixed}'] = map""",
            'tests': """
    def test_${method_name}(self):
        ${pattern_name}
        if not is_never_authz(self.service_config):
            test_duration = Duration(hours=1)
            assert self.form._my_map['${var_name_mixed}'] is None
            self.form.${method_name}(test_duration)
            assert self.form._my_map['${var_name_mixed}']['seconds'] == 3600
            assert self.form._my_map['${var_name_mixed}']['days'] == 0
            assert self.form._my_map['${var_name_mixed}']['microseconds'] == 0
            with pytest.raises(errors.InvalidArgument):
                self.form.${method_name}(1.05)
            # reset this for other tests
            self.form._my_map['${var_name_mixed}'] = None"""
        }
    }

    clear_duration_attribute_template = deepcopy(clear_simple_attribute_template)
    clear_duration_attribute_template['python']['tests'] = """
    def test_${method_name}(self):
        ${pattern_name}
        if not is_never_authz(self.service_config):
            test_duration = Duration(hours=1)
            assert self.form._my_map['${var_name_mixed}'] is None
            self.form.set_${var_name}(test_duration)
            assert self.form._my_map['${var_name_mixed}']['seconds'] == 3600
            assert self.form._my_map['${var_name_mixed}']['days'] == 0
            assert self.form._my_map['${var_name_mixed}']['microseconds'] == 0
            self.form.${method_name}()
            assert self.form._my_map['${var_name_mixed}'] == self.form.get_${var_name}_metadata().get_default_${syntax_under}_values()[0]"""

    set_data_input_stream_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        if ${arg0_name} is None:
            raise errors.NullArgument('${arg0_name} cannot be None')
        if not isinstance(${arg0_name}, DataInputStream):
            raise errors.InvalidArgument('${arg0_name} must be instance of DataInputStream')
        dbase = JSONClientValidated('repository',
                                    runtime=self._runtime).raw()
        filesys = gridfs.GridFS(dbase)
        self._my_map['${var_name_mixed}'] = filesys.put(${arg0_name}._my_data)
        ${arg0_name}._my_data.seek(0)
        self._my_map['base64'] = base64.b64encode(${arg0_name}._my_data.read())"""
        }
    }

    clear_data_input_stream_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess('Sorry you cannot clear ${var_name}')
        if self._my_map['${var_name_mixed}'] == self._${var_name}_default:
            return
        dbase = JSONClientValidated('repository',
                                    runtime=self._runtime).raw()
        filesys = gridfs.GridFS(dbase)
        filesys.delete(self._my_map['${var_name_mixed}'])
        self._my_map['${var_name_mixed}'] = self._${var_name}_default
        del self._my_map['base64']"""
        }
    }


class GenericCatalogForm(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from . import default_mdata'
            ],
            'tests': [
                'from dlkit.runtime import PROXY_SESSION, proxy_example',
                'from dlkit.runtime.managers import Runtime',
                'REQUEST = proxy_example.SimpleRequest()',
                'CONDITION = PROXY_SESSION.get_proxy_condition()',
                'CONDITION.set_http_request(REQUEST)',
                'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
                'from dlkit.primordium.type.primitives import Type',
                'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
                'from dlkit.abstract_osid.osid import errors',
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
${pattern_name}
_namespace = '${implpkg_name}.${object_name}'

def __init__(self, **kwargs):
    osid_objects.OsidCatalogForm.__init__(self, object_name='${object_name_upper}', **kwargs)
    self._mdata = default_mdata.get_${object_name_under}_mdata()
    self._init_metadata(**kwargs)
    if not self.is_for_update():
        self._init_map(**kwargs)

def _init_metadata(self, **kwargs):
    \"\"\"Initialize form metadata\"\"\"
    osid_objects.OsidCatalogForm._init_metadata(self, **kwargs)

def _init_map(self, record_types=None, **kwargs):
    \"\"\"Initialize form map\"\"\"
    osid_objects.OsidCatalogForm._init_map(self, record_types, **kwargs)""",
            'tests': """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::BinForm::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)

    def class_tear_down():
        pass

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::BinForm::init_template
    if not is_never_authz(request.cls.service_config):
        request.cls.object = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])

    def test_tear_down():
        pass

    request.addfinalizer(test_tear_down)"""
        }
    }

    get_catalog_form_record_template = GenericObjectForm.get_object_form_record_template
