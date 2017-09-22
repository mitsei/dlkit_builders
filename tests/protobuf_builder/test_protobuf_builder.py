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
            'grade': 'osid.id.Id',
            'items': 'osid.id.Id[]',
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
        assert '_type' in self.result[self.object_name]
        assert self.result[self.object_name]['_type'] == 'message'
        assert 'body' in self.result[self.object_name]
        assert len(self.result[self.object_name]['_imports']) == 3
        for proto_import in self.result[self.object_name]['_imports']:
            assert 'import' in proto_import

        assert self.result[self.object_name]['body'] == """
message AssessmentTaken {
  google.protobuf.Timestamp actual_start_time = 1;
  dlkit.primordium.id.primitives.Id assessment_offered = 2;
  dlkit.proto.osid.OsidCatalog bank = 3;
  google.protobuf.Timestamp completion_time = 4;
  dlkit.primordium.id.primitives.Id grade = 5;
  dlkit.primordium.id.primitives.IdList items = 6;
  float score = 7;
  dlkit.primordium.id.primitives.Id taker = 8;
}"""

    def test_generate_protobuf_message_includes_object_name(self):
        assert len(self.result.keys()) == 1
        assert self.result.keys()[0] == self.interface.keys()[0]

    def test_generate_protobuf_message_handles_list_objects(self):
        interface = {
            'QuestionList': {
            }
        }
        result = self.builder.generate_protobuf_message(interface)
        assert result['QuestionList']['body'] == """
message QuestionList {
  repeated Question = 1;
}"""


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
                'arg_type': 'osid.type.Type'
            }],
            'return_type': 'osid.assessment.ItemList'
        }, {
            'name': 'get_item',
            'args': [{
                'arg_type': 'osid.id.Id'
            }],
            'return_type': 'osid.assessment.Item'
        }, {
            'name': 'get_items_by_ids',
            'args': [{
                'arg_type': 'osid.id.IdList'
            }],
            'return_type': 'osid.assessment.ItemList'
        }, {
            'name': 'fake_method',
            'args': [{
                'arg_type': 'boolean'
            }],
            'return_type': 'osid.id.IdList'
        }]
    }
    request.cls.result = request.cls.builder.generate_grpc_service(request.cls.interface)
    request.cls.session_name = request.cls.interface['shortname']


@pytest.mark.usefixtures('proto_builder_class_fixture', 'proto_builder_service_test_fixture')
class TestProtoBuilderServices(object):
    def test_generate_grpc_service_returns_expected_format(self):
        assert isinstance(self.result, dict)

        assert isinstance(self.result[self.session_name], dict)
        assert '_imports' in self.result[self.session_name]
        assert '_type' in self.result[self.session_name]
        assert self.result[self.session_name]['_type'] == 'service'
        assert 'body' in self.result[self.session_name]

        assert self.result[self.session_name]['body'] == """
service ItemLookupSession {
  rpc GetBankId() returns (Id) {}
  rpc GetItemsByParentGenusType(dlkit.primordium.type.primitives.Type) returns (stream Item) {}
  rpc GetItem(dlkit.primordium.id.primitives.Id) returns (Item) {}
  rpc GetItemsByIds(dlkit.primordium.id.primitives.IdList) returns (stream Item) {}
  rpc FakeMethod(bool) returns (stream Id) {}
}"""

    def test_generate_grpc_service_includes_session_name(self):
        assert len(self.result.keys()) == 1
        assert self.result.keys()[0] == self.interface['shortname']


@pytest.fixture(scope='function')
def proto_builder_unify_imports_test_fixture(request):
    request.cls.proto_data = [{
        'Object1': {
            '_imports': ['foo', 'bar', 'baz']
        },
    }, {
        'Session1': {
            '_imports': ['bar', 'bim', 'bop']
        }
    }]
    request.cls.result = request.cls.builder.unify_imports(request.cls.proto_data)


@pytest.mark.usefixtures('proto_builder_class_fixture', 'proto_builder_unify_imports_test_fixture')
class TestProtoBuilderUnifyImports(object):
    def test_unify_imports_returns_list(self):
        assert isinstance(self.result, list)

    def test_unify_imports_removes_duplicates(self):
        assert len(self.result) == 5


@pytest.fixture(scope='function')
def proto_builder_unify_bodies_test_fixture(request):
    request.cls.proto_data = [{
        'Object1': {
            'body': 'foo',
            '_type': 'message'
        },
    }, {
        'Session1': {
            'body': 'bar',
            '_type': 'service'
        }
    }, {
        'Object2': {
            'body': 'bim',
            '_type': 'message'
        }
    }]
    request.cls.result = request.cls.builder.unify_bodies(request.cls.proto_data)


@pytest.mark.usefixtures('proto_builder_class_fixture', 'proto_builder_unify_bodies_test_fixture')
class TestProtoBuilderUnifyBodies(object):
    def test_unify_bodies_returns_list(self):
        assert isinstance(self.result, list)

    def test_unify_bodies_orders_messages_first(self):
        # There really should never be duplicates, but just in case...
        assert len(self.result) == 3
        assert self.result[0] == 'foo'
        assert self.result[1] == 'bim'
        assert self.result[2] == 'bar'