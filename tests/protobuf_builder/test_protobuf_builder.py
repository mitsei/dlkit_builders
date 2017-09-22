# Test (at the very least) the helper methods in the ProtoBuilder,
#   to make sure they translate our pattern and package JSON data
#   into the correct proto formats.
import pytest

from ...binder_helpers import under_to_mixed
from ...protobuf_builder import ProtoBuilder


@pytest.fixture(scope='class')
def proto_builder_class_fixture(request):
    request.cls.builder = ProtoBuilder()


@pytest.fixture(scope='function')
def proto_builder_message_test_fixture(request):
    request.cls.interface = {
        'AssessmentTaken': {
            'bank': 'OsidCatalog',
            'taker': 'osid.id.Id',
            'assessment_offered': 'osid.id.Id',
            'actual_start_time': 'osid.calendaring.DateTime',
            'completion_time': 'osid.calendaring.DateTime',
            'score': 'decimal',
            'grade': 'osid.id.Id'
        }
    }
    request.cls.result = request.cls.builder.generate_protobuf_message(request.cls.interface)
    request.cls.object_name = request.cls.result.keys()[0]


@pytest.mark.usefixtures('proto_builder_class_fixture', 'proto_builder_message_test_fixture')
class TestProtoBuilderMessages(object):
    def test_generate_protobuf_message_returns_propertly_formatted_dictionary(self):
        assert isinstance(self.result, dict)

        assert isinstance(self.result[self.object_name], dict)
        assert '_imports' in self.result[self.object_name]
        assert len(self.result[self.object_name]['_imports']) == 3
        for variable in self.interface[self.object_name].keys():
            assert variable in self.result[self.object_name].keys()

    def test_generate_protobuf_message_handles_primordium_imports(self):
        assert self.result[self.object_name]['grade'] == 'Id'
        assert 'dlkit/primordium/id/primitives.proto' in self.result[self.object_name]['_imports']

    def test_generate_protobuf_message_handles_osid_package_imports(self):
        assert self.result[self.object_name]['bank'] == 'OsidCatalog'
        assert 'osid/objects.proto' in self.result[self.object_name]['_imports']

    def test_generate_protobuf_message_handles_proto_types(self):
        assert self.result[self.object_name]['actual_start_time'] == 'google.protobuf.Timestamp'
        assert self.result[self.object_name]['completion_time'] == 'google.protobuf.Timestamp'

    def test_generate_protobuf_message_includes_object_name(self):
        assert len(self.result.keys()) == 1
        assert self.result.keys()[0] == self.interface.keys()[0]


@pytest.fixture(scope='function')
def proto_builder_service_test_fixture(request):
    request.cls.interface = {
        'shortname': 'ItemLookupSession',
        'methods': [{
            'name': 'get_bank_id',
            'args': [],
            'return_type': 'osid.id.Id'
        }, {
            'name': 'get_items_by_parent_genus_type',
            'args': [{
                'var_name': 'item_genus_type'
            }],
            'return_type': 'osid.assessment.ItemList'
        }, {
            'name': 'get_item',
            'args': [{
                'var_name': 'item_id'
            }],
            'return_type': 'osid.assessment.Item'
        }]
    }
    request.cls.result = request.cls.builder.generate_grpc_service(request.cls.interface)
    request.cls.session_name = request.cls.interface['shortname']


@pytest.mark.usefixtures('proto_builder_class_fixture', 'proto_builder_service_test_fixture')
class TestProtoBuilderServices(object):
    def test_generate_grpc_service_returns_expected_format(self):
        assert isinstance(self.result, dict)

        assert isinstance(self.result[self.session_name], dict)
        assert len(self.result[self.session_name].keys()) == 3
        for method in self.interface['methods']:
            assert under_to_mixed(method['name']) in self.result[self.session_name].keys()

    def test_generate_grpc_service_handles_list_returns(self):
        assert self.result[self.session_name]['getItemsByParentGenusType']['returns'] == 'stream Item'

    def test_generate_grpc_service_handles_no_args(self):
        assert self.result[self.session_name]['getBankId']['args'] == []

    def test_generate_grpc_service_handles_genus_type_args(self):
        assert self.result[self.session_name]['getItemsByParentGenusType']['args'][0] == 'GenusType'

    def test_generate_grpc_service_handles_id_type_args(self):
        assert self.result[self.session_name]['getItem']['args'][0] == 'Id'

    def test_generate_grpc_service_handles_package_return_object(self):
        assert self.result[self.session_name]['getItem']['returns'] == 'Item'
