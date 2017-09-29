# Test (at the very least) the helper methods in the ProtoBuilder,
#   to make sure they translate our pattern and package JSON data
#   into the correct proto formats.
import os
import pytest

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
    request.cls.result = request.cls.builder.generate_protobuf_message(request.cls.interface,
                                                                       'assessment.json')
    request.cls.object_name = request.cls.result.keys()[0]


@pytest.mark.usefixtures('proto_builder_class_fixture', 'proto_builder_message_test_fixture')
class TestProtoBuilderMessages(object):
    def test_generate_protobuf_message_returns_properly_formatted_dictionary(self):
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
  repeated dlkit.primordium.id.primitives.Id items = 6;
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
        result = self.builder.generate_protobuf_message(interface,
                                                        'assessment.json')
        assert result['QuestionList']['body'] == """
message QuestionList {
  repeated Question questions = 1;
}"""

    def test_generate_protobuf_message_handles_osid_package(self):
        interface = {
            'OsidCatalog': {
                'no_catalog': 'OsidCatalog'
            }
        }
        result = self.builder.generate_protobuf_message(interface,
                                                        'osid.json')
        assert result['OsidCatalog']['body'] == """
message OsidCatalog {
  OsidCatalog no_catalog = 1;
}"""
        assert result['OsidCatalog']['_imports'] == []

    def test_generate_protobuf_message_handles_other_same_package(self):
        interface = {
            'GetAgencyReply': {
                'agent': 'osid.authentication.Agent'
            }
        }
        result = self.builder.generate_protobuf_message(interface,
                                                        'authentication.json')
        assert result['GetAgencyReply']['body'] == """
message GetAgencyReply {
  Agent agent = 1;
}"""
        assert result['GetAgencyReply']['_imports'] == []


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
  rpc GetBankId(GetBankIdRequest) returns (GetBankIdReply) {}
  rpc GetItemsByParentGenusType(GetItemsByParentGenusTypeRequest) returns (GetItemsByParentGenusTypeReply) {}
  rpc GetItem(GetItemRequest) returns (GetItemReply) {}
  rpc GetItemsByIds(GetItemsByIdsRequest) returns (GetItemsByIdsReply) {}
  rpc FakeMethod(FakeMethodRequest) returns (FakeMethodReply) {}
}"""

    def test_generate_grpc_service_includes_session_name(self):
        assert len(self.result.keys()) == 1
        assert self.result.keys()[0] == self.interface['shortname']

    def test_generate_grpc_service_handles_duplicate_method_names(self):
        interface = {
            'shortname': 'ItemLookupSession',
            'methods': [{
                'name': 'get_bank_id',
                'args': [],
                'return_type': 'osid.id.Id'
            }, {
                'name': 'get_bank_id',
                'args': [],
                'return_type': 'osid.id.Id'
            }]
        }
        result = self.builder.generate_grpc_service(interface)
        assert result[self.session_name]['body'] == """
service ItemLookupSession {
  rpc GetBankId(GetBankIdRequest) returns (GetBankIdReply) {}
}"""


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
        assert len(self.result) == 3
        assert self.result[0] == 'foo'
        assert self.result[1] == 'bim'
        assert self.result[2] == 'bar'


@pytest.fixture(scope='function')
def proto_builder_format_request_message_test_fixture(request):
    request.cls.method_definition = {
        'name': 'get_items_by_ids',
        'args': [{
            'arg_type': 'osid.id.IdList',
            'var_name': 'item_ids'
        }],
        'return_type': 'osid.assessment.ItemList'
    }
    request.cls.result = request.cls.builder.format_method_to_protobuf_request_msg(request.cls.method_definition)


@pytest.mark.usefixtures('proto_builder_class_fixture', 'proto_builder_format_request_message_test_fixture')
class TestProtoBuilderFormatRequestMessage(object):
    def test_format_method_to_protobuf_request_msg_returns_right_data(self):
        assert isinstance(self.result, dict)
        assert len(self.result.keys()) == 1
        expected_name = 'GetItemsByIdsRequest'
        assert self.result.keys()[0] == expected_name
        assert isinstance(self.result[expected_name], dict)
        assert len(self.result[expected_name].keys()) == 1
        assert self.result[expected_name].keys()[0] == 'item_ids'
        assert self.result[expected_name]['item_ids'] == 'osid.id.IdList'


@pytest.fixture(scope='function')
def proto_builder_format_reply_message_test_fixture(request):
    request.cls.method_definition = {
        'name': 'get_items_by_ids',
        'args': [{
            'arg_type': 'osid.id.IdList',
            'var_name': 'item_ids'
        }],
        'return_type': 'osid.assessment.ItemList'
    }
    request.cls.result = request.cls.builder.format_method_to_protobuf_reply_msg(request.cls.method_definition)


@pytest.mark.usefixtures('proto_builder_class_fixture', 'proto_builder_format_reply_message_test_fixture')
class TestProtoBuilderFormatReplyMessage(object):
    def test_format_method_to_protobuf_reply_msg_returns_right_data(self):
        assert isinstance(self.result, dict)
        assert len(self.result.keys()) == 1
        expected_name = 'GetItemsByIdsReply'
        assert self.result.keys()[0] == expected_name
        assert isinstance(self.result[expected_name], dict)
        assert len(self.result[expected_name].keys()) == 1
        assert self.result[expected_name].keys()[0] == 'items'
        assert self.result[expected_name]['items'] == 'osid.assessment.ItemList'

    def test_format_method_to_protobuf_reply_msg_handles_no_return_data(self):
        method_definition = {
            'name': 'submit_response',
            'args': [{
                'arg_type': 'osid.assessment.Response',
                'var_name': 'response'
            }],
            'return_type': ''
        }
        result = self.builder.format_method_to_protobuf_reply_msg(method_definition)
        assert isinstance(result, dict)
        assert len(result.keys()) == 1
        expected_name = 'SubmitResponseReply'
        assert result.keys()[0] == expected_name
        assert isinstance(result[expected_name], dict)
        assert len(result[expected_name].keys()) == 0

    def test_format_method_to_protobuf_reply_msg_renames_boolean_return_variables(self):
        method_definition = {
            'name': 'is_question_answered',
            'args': [{
                "arg_type": "osid.id.Id",
                "var_name": "assessment_section_id",
            }, {
                "arg_type": "osid.id.Id",
                "var_name": "item_id",
            }],
            'return_type': 'boolean'
        }
        result = self.builder.format_method_to_protobuf_reply_msg(method_definition)
        assert isinstance(result, dict)
        assert len(result.keys()) == 1
        expected_name = 'IsQuestionAnsweredReply'
        assert result.keys()[0] == expected_name
        assert isinstance(result[expected_name], dict)
        assert len(result[expected_name].keys()) == 1
        assert result[expected_name].keys()[0] == 'is_question_answered'
        assert result[expected_name]['is_question_answered'] == 'boolean'


@pytest.fixture(scope='function')
def proto_builder_define_grpc_services_test_fixture(request):
    this_directory = os.path.dirname(os.path.abspath(__file__))
    fixture_file = os.path.join(this_directory, os.pardir, 'fixtures', 'package_maps', 'assessment-sessions.json')
    request.cls.package_map_file = fixture_file
    request.cls.result = request.cls.builder.define_grpc_services(request.cls.package_map_file)


@pytest.mark.usefixtures('proto_builder_class_fixture', 'proto_builder_define_grpc_services_test_fixture')
class TestProtoBuilderDefineGRPCServices(object):
    def test_define_grpc_services_also_creates_the_request_messages(self):
        messages = [m for m in self.result if m[m.keys()[0]]['_type'] == 'message']

        request_messages = [m for m in messages if m.keys()[0].endswith('Request')]
        reply_messages = [m for m in messages if m.keys()[0].endswith('Reply')]

        assert len(messages) == len(request_messages) + len(reply_messages)

        services = [s for s in self.result if s[s.keys()[0]]['_type'] == 'service']

        number_services = len(services)
        assert number_services == 1

        service = services[0]
        assert service[service.keys()[0]]['body'].count('rpc') == len(request_messages)
        assert service[service.keys()[0]]['body'].count('rpc') == len(reply_messages)


@pytest.fixture(scope='function')
def proto_builder_define_protobuf_messages_test_fixture(request):
    this_directory = os.path.dirname(os.path.abspath(__file__))
    fixture_file = os.path.join(this_directory, os.pardir, 'fixtures', 'package_maps', 'osid-objects.json')
    request.cls.package_map_file = fixture_file
    request.cls.result = request.cls.builder.define_protobuf_messages(request.cls.package_map_file)


@pytest.mark.usefixtures('proto_builder_class_fixture', 'proto_builder_define_protobuf_messages_test_fixture')
class TestProtoBuilderDefineProtobufMessages(object):
    def test_define_protobuf_messages_also_creates_an_empty_osid_message(self):
        messages = [m for m in self.result if m[m.keys()[0]]['_type'] == 'message']

        assert len(messages) == 2

        assert messages[0].keys()[0] == 'OsidList'
        assert messages[1].keys()[0] == 'Osid'


@pytest.fixture(scope='function')
def proto_builder_remove_duplicate_entries_test_fixture(request):
    request.cls.proto_data = [{
        'GetBankIdRequest': {
            '_type': 'message'
        }
    }, {
        'GetBankIdRequest': {
            '_type': 'message'
        }
    }, {
        'MySession': {
            '_type': 'service'
        }
    }]
    request.cls.result = request.cls.builder.remove_duplicate_entries(request.cls.proto_data)


@pytest.mark.usefixtures('proto_builder_class_fixture', 'proto_builder_remove_duplicate_entries_test_fixture')
class TestProtoBuilderRemoveDuplicateEntries(object):
    def test_duplicate_messages_removed(self):
        assert len(self.result) == 2
        assert self.result[0].keys()[0] == 'GetBankIdRequest'
        assert self.result[0]['GetBankIdRequest']['_type'] == 'message'
        assert self.result[1].keys()[0] == 'MySession'
        assert self.result[1]['MySession']['_type'] == 'service'


@pytest.mark.usefixtures('proto_builder_class_fixture')
class TestProtoBuilderHelperMethods(object):
    def test_is_list(self):
        assert not self.builder.is_list('Item')
        assert self.builder.is_list('ItemList')
        assert self.builder.is_list('Id[]')
        assert self.builder.is_list('Type[]')

    def test_is_same_package(self):
        assert not self.builder.is_same_package('osidy.json', 'OsidCatalog')
        assert not self.builder.is_same_package('package_maps/assessment.json', 'OsidCatalog')
        assert not self.builder.is_same_package('osid.json', 'osid.id.Id')

        assert self.builder.is_same_package('osid.json', 'OsidCatalog')
        assert self.builder.is_same_package('package_maps/authentication.json', 'osid.authentication.Agent')

    def test_make_non_list(self):
        assert self.builder.make_non_list('Item') == 'Item'
        assert self.builder.make_non_list('ItemList') == 'Item'
        assert self.builder.make_non_list('Id[]') == 'Id'
