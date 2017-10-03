# TODO: Include docstrings so that ``protoc`` includes them in the final build?

import glob
import json
import os
import subprocess

from binder_helpers import under_to_camel, make_plural, camel_to_under
from build_dlkit import PatternBuilder
from config import sessions_to_implement, objects_to_implement
from interface_builders import InterfaceBuilder

IMPORT_MAPPING = {
    'osid.id.Id': 'dlkit/primordium/id/primitives.proto',
    'Id': 'dlkit/primordium/id/primitives.proto',
    'osid.calendaring.DateTime': 'google/protobuf/timestamp.proto',  # a Google built-in one?
    'osid.calendaring.DateTimeInterval': 'dlkit/primordium/calendaring/primitives.proto',
    'osid.calendaring.Duration': 'dlkit/primordium/calendaring/primitives.proto',
    'osid.calendaring.Time': 'dlkit/primordium/calendaring/primitives.proto',
    'osid.locale.DisplayText': 'dlkit/primordium/locale/primitives.proto',
    'osid.type.Type': 'dlkit/primordium/type/primitives.proto',
    'Type': 'dlkit/primordium/type/primitives.proto',
    'OsidCatalog': 'dlkit/proto/osid.proto',
    'osid.assessment.Bank': 'dlkit/proto/assessment.proto',
    'osid.assessment.Item': 'dlkit/proto/assessment.proto',
    'osid.authentication.Agency': 'dlkit/proto/authentication.proto',
    'osid.authentication.Agent': 'dlkit/proto/authentication.proto',
    'osid.hierarchy.Hierarchy': 'dlkit/proto/hierarchy.proto',
    'osid.hierarchy.Node': 'dlkit/proto/hierarchy.proto',
    'osid.acknowledgement.BillingNode': 'dlkit/proto/hierarchy.proto',  # bug in spec for GroupHierarchySession
    'osid.financials.Currency': 'dlkit/primordium/financials/unimplemented_primitives.proto',
    'osid.grading.Grade': 'dlkit/proto/grading.proto',
    'osid.grading.GradeEntry': 'dlkit/proto/grading.proto',
    'osid.installation.Version': 'dlkit/primordium/installation/primitives.proto',
    'osid.mapping.Coordinate': 'dlkit/primordium/mapping/coordinate_primitives.proto',
    'Coordinate': 'dlkit/primordium/mapping/coordinate_primitives.proto',
    'osid.mapping.Distance': 'dlkit/primordium/mapping/unimplemented_primitives.proto',
    # 'osid.mapping.Location': 'dlkit/primordium/mapping/unimplemented_primitives.proto',
    'osid.mapping.SpatialUnit': 'dlkit/primordium/mapping/spatial_units.proto',
    'SpatialUnit': 'dlkit/primordium/mapping/spatial_units.proto',
    'osid.mapping.Speed': 'dlkit/primordium/mapping/unimplemented_primitives.proto',
    'osid.resource.Resource': 'dlkit/proto/resource.proto',
    'osid.transport.DataInputStream': 'dlkit/primordium/transport/objects.proto',
}

TYPE_MAPPING = {
    'decimal': 'float',
    'cardinal': 'sint32',
    'integer': 'sint32',
    'boolean': 'bool',
    'byte': 'bytes',
    'object': 'bytes',  # could also do a protobuf Map, except we can't define all possible type combinations...
    'UNKNOWN': 'dlkit.primordium.id.primitives.Id',  # currently this only happens to Ontology.Relevance...
    'timestamp': 'google.protobuf.Timestamp',
    'osid.calendaring.DateTime': 'google.protobuf.Timestamp',
    'DateTime': 'google.protobuf.Timestamp',
    'osid.calendaring.DateTimeInterval': 'dlkit.primordium.calendaring.primitives.DateTimeInterval',
    'DateTimeInterval': 'dlkit.primordium.calendaring.primitives.DateTimeInterval',
    'osid.calendaring.Duration': 'dlkit.primordium.calendaring.primitives.Duration',
    'Duration': 'dlkit.primordium.calendaring.primitives.Duration',
    'osid.calendaring.Time': 'dlkit.primordium.calendaring.primitives.Time',
    'Time': 'dlkit.primordium.calendaring.primitives.Time',
    'osid.id.Id': 'dlkit.primordium.id.primitives.Id',
    'Id': 'dlkit.primordium.id.primitives.Id',
    'osid.type.Type': 'dlkit.primordium.type.primitives.Type',
    'Type': 'dlkit.primordium.type.primitives.Type',
    'osid.locale.DisplayText': 'dlkit.primordium.locale.primitives.DisplayText',
    'OsidCatalog': 'dlkit.proto.osid.OsidCatalog',
    'osid.assessment.Bank': 'dlkit.proto.assessment.Bank',
    'osid.assessment.Item': 'dlkit.proto.assessment.Item',
    'osid.authentication.Agency': 'dlkit.proto.authentication.Agency',
    'osid.authentication.Agent': 'dlkit.proto.authentication.Agent',
    'osid.hierarchy.Hierarchy': 'dlkit.proto.hierarchy.Hierarchy',
    'osid.hierarchy.Node': 'dlkit.proto.hierarchy.Node',
    'osid.acknowledgement.BillingNode': 'dlkit.proto.hierarchy.Node',  # bug in spec for GroupHierarchySession
    'osid.financials.Currency': 'dlkit.primordium.financials.unimplemented_primitives.Currency',
    'Currency': 'dlkit.primordium.financials.unimplemented_primitives.Currency',
    'osid.grading.Grade': 'dlkit.proto.grading.Grade',
    'osid.grading.GradeEntry': 'dlkit.proto.grading.GradeEntry',
    'osid.installation.Version': 'dlkit.primordium.installation.primitives.Version',
    'Version': 'dlkit.primordium.installation.primitives.Version',
    'osid.mapping.Coordinate': 'dlkit.primordium.mapping.coordinate_primitives.Coordinate',
    'Coordinate': 'dlkit.primordium.mapping.coordinate_primitives.Coordinate',
    'osid.mapping.Distance': 'dlkit.primordium.mapping.unimplemented_primitives.Distance',
    'Distance': 'dlkit.primordium.mapping.unimplemented_primitives.Distance',
    # 'osid.mapping.Location': 'dlkit.primordium.mapping.unimplemented_primitives.Location',
    # 'Location': 'dlkit.primordium.mapping.unimplemented_primitives.Location',
    'osid.mapping.SpatialUnit': 'dlkit.primordium.mapping.spatial_units.SpatialUnit',
    'SpatialUnit': 'dlkit.primordium.mapping.spatial_units.SpatialUnit',
    'osid.mapping.Speed': 'dlkit.primordium.mapping.unimplemented_primitives.Speed',
    'Speed': 'dlkit.primordium.mapping.unimplemented_primitives.Speed',
    'osid.resource.Resource': 'dlkit.proto.resource.Resource',
    'osid.transport.DataInputStream': 'dlkit.primordium.transport.objects.DataInputStream',
    'DataInputStream': 'dlkit.primordium.transport.objects.DataInputStream'
}

# Is there a way to generate this map?
AGGREGATEABLE_MAPPING = {
    'Item': {
        'question': 'Question',
        'answers': 'AnswerList'
    },
    'Asset': {
        'asset_contents': 'AssetContentList'
    }
}


class ProtoBuilder(InterfaceBuilder, PatternBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(ProtoBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir + '/proto'
        self._template_dir = self._abs_path + '/proto_templates'

        self._class = 'proto'

    def build_this_interface(self, interface):
        """override the one in build_dlkit.py because we need query_inspectors"""
        if (interface['category'] == 'sessions' and
                interface['shortname'] not in sessions_to_implement):
            return False

        # if (self.package['name'] != 'osid' and
        #         interface['category'] in ['objects', 'queries',
        #                                   'searches', 'rules',
        #                                   'search_orders', 'query_inspectors'] and
        #         not any(interface['shortname'].startswith(object_name) for object_name in objects_to_implement)):
        #     return False

        if interface['category'] == 'managers':
            return False

        return True

    def compile_proto_files(self):
        """For each *.proto file in dlkit/proto and dlkit/primordium, call ``protoc``:

        grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. *.proto   (basically)

        https://grpc.io/docs/quickstart/python.html
        """
        for proto_file in glob.iglob('{0}/**/*.proto'.format(self._build_dir)):
            directory = os.path.dirname(proto_file)
            # Don't use  separate build directory because it seems to compile the wrong paths for import
            #   i.e. using a build directory will result in _pb2.py files that import from ``dlkit.proto``,
            #        instead of ``dlkit.proto.build``
            # proto_output = os.path.join(directory, 'build')
            filename = os.path.basename(proto_file)
            call_list = ['python',
                         '-m',
                         'grpc_tools.protoc',
                         '-I', '../dlkit-pip/',
                         '--proto_path', directory,
                         '--python_out', directory,
                         '--grpc_python_out', directory,
                         filename]
            try:
                subprocess.check_call(call_list)
            except OSError:
                raise RuntimeError('Running the proto builder requires having grpcio-tools installed.')

    def define_grpc_services(self, package_map_file):
        """split this out for testing -- just grab all the data from the interface sessions"""
        if not os.path.isfile(package_map_file):
            raise TypeError('package_map_file must be a path to a file')
        proto_data = []
        for grpc_service in self.get_package_elements(package_map_file, 'sessions'):
            # treat sessions as grpc services
            # Also need to generate the SessionRequest message, that will get passed into
            #   the service RPC
            for method in grpc_service['methods']:
                proto_data.append(self.generate_protobuf_message(self.format_method_to_protobuf_reply_msg(method),
                                                                 package_map_file))
                proto_data.append(self.generate_protobuf_message(self.format_method_to_protobuf_request_msg(method),
                                                                 package_map_file))
            proto_data.append(self.generate_grpc_service(grpc_service))
        return proto_data

    def define_protobuf_messages(self, package_map_file):
        """split this out for testing -- just grab all the data from the interface objects"""
        def osid_list_exception():
            return {
                'Osid': {
                    '_imports': [],
                    '_type': 'message',
                    'body': """
message Osid {
}"""
                }
            }

        if not os.path.isfile(package_map_file):
            raise TypeError('package_map_file must be a path to a file')
        proto_data = []
        for protobuf_message in self.get_package_elements(package_map_file, 'objects'):
            # treat objects as protobuf messages
            proto_data.append(self.generate_protobuf_message(protobuf_message,
                                                             package_map_file))
            # Exception for OsidList, because the repeated "Osid" object doesn't exist, so we have to make it...
            if protobuf_message.keys()[0] == 'OsidList':
                proto_data.append(osid_list_exception())
        return proto_data

    def format_method_to_protobuf_reply_msg(self, method_definition):
        """
        Given a method definition from a package.json file, reformat it into the expected input format
        for ``generate_protobuf_message``, for an RPC reply.

        i.e. given {
            'name': 'get_items_by_ids',
            'args': [{
                'arg_type': 'osid.id.IdList',
                'var_name': 'item_ids'
            }],
            'return_type': 'osid.assessment.ItemList'
        }

        this method will return {
            'GetItemsByIdsReply': {
                'items': 'osid.assessment.ItemList'
            }
        }
        """
        if not isinstance(method_definition, dict):
            raise TypeError('method_definition must be a dictionary')
        reply_name = '{0}Reply'.format(under_to_camel(method_definition['name']))
        result = {
            reply_name: {}
        }

        if self.osid_blacklist(reply_name):
            return result

        return_type = method_definition['return_type']
        if return_type != '':
            return_type_last = return_type.split('.')[-1]
            if self.is_list(return_type):
                return_variable = make_plural(camel_to_under(self.make_non_list(return_type_last)))
            elif return_type == 'boolean':
                # Let's give the variable a clearer name than "boolean" in the message definition
                return_variable = method_definition['name']
            else:
                return_variable = camel_to_under(return_type_last)
            result[reply_name][return_variable] = return_type
        return result

    def format_method_to_protobuf_request_msg(self, method_definition):
        """
        Given a method definition from a package.json file, reformat it into the expected input format
        for ``generate_protobuf_message``, for an RPC Request.

        i.e. given {
            'name': 'get_items_by_ids',
            'args': [{
                'arg_type': 'osid.id.IdList',
                'var_name': 'item_ids'
            }],
            'return_type': 'osid.assessment.ItemList'
        }

        this method will return {
            'GetItemsByIdsRequest': {
                'item_ids': 'osid.id.IdList'
            }
        }
        """
        if not isinstance(method_definition, dict):
            raise TypeError('method_definition must be a dictionary')
        request_name = '{0}Request'.format(under_to_camel(method_definition['name']))
        result = {
            request_name: {}
        }

        if self.osid_blacklist(request_name):
            return result

        for argument in method_definition['args']:
            result[request_name][argument['var_name']] = argument['arg_type']
        return result

    @staticmethod
    def generate_grpc_service(grpc_service):
        """
        given an interface definition, return a gRPC service block based
        on the interface['methods']

        :param grpc_service: package ``interface`` definition
        :return: JSON-ish format of the service definition: {
            'ServiceName': {
                'methodName': (message, return)
            }
        }

        i.e. for

        {
            'shortname': 'BookService',
            'methods': [{
                'name': 'GetBook',
                'args': [{
                    'arg_type': 'Book',
                    'var_name': 'GetBookRequest'
                }],
                'return_type': 'Book'
            }, {
                'name': 'QueryBooks',
                'args': [{
                    'arg_type': 'BookQuery',
                    'var_name': 'QueryBooksRequest'
                }],
                'return_type': 'Book[]'
            }]
        }

        this method would return:
        {
            'BookService': {
                '_imports': [],
                '_type': 'service',
                'body': \"\"\"
service BookService {
  rpc GetBook(GetBookRequest) returns (Book) {}
  rpc QueryBooks(QueryBooksRequest) returns (stream Book) {}
}\"\"\"
            }
        }
        """
        if not isinstance(grpc_service, dict):
            raise TypeError('grpc_service must be a dict')
        if 'shortname' not in grpc_service:
            raise KeyError('grpc_service must contain a shortname')
        if 'methods' not in grpc_service:
            raise KeyError('grpc_service must contain a list of methods')

        service_name = grpc_service['shortname']

        if not isinstance(grpc_service['methods'], list):
            raise TypeError('grpc_service methods must be a list')

        result = {
            service_name: {
                '_imports': [],
                '_type': 'service'
            }
        }
        service_fields = []
        # For some reason we're getting duplicates in the package_map?
        defined_rpcs = []
        for method in grpc_service['methods']:
            method_name = under_to_camel(method['name'])
            # TODO: Handle any imports here?
            if method_name not in defined_rpcs:
                service_fields.append('  rpc {0}({1}) returns ({2}) {{}}'.format(method_name,
                                                                                 '{0}Request'.format(method_name),
                                                                                 '{0}Reply'.format(method_name)))
                defined_rpcs.append(method_name)
        result[service_name]['body'] = """
service {0} {{
{1}
}}""".format(service_name,
             '\n'.join(service_fields))

        return result

    def generate_protobuf_message(self, protobuf_message, package_map_file):
        """
        given the data for an object, return a protobuf-style message
        use the package_map_file to guard against same-package imports, i.e. osid.proto importing OsidCatalog

        :param protobuf_message: dictionary with persisted and initialized data
        :return: JSON-ish format of the message definition: {
            'MessageName': {
                'argument': 'type'
            }
        }

        i.e. for
        {
            'Assessment': {
                'bank': 'OsidCatalog',
                'taker': 'osid.id.Id',
            }
        }

        this method will return:
        {
            'Assessment': {
                '_imports': ['osid/objects.proto', '../primordium/id/primitives.proto'],
                '_type': 'message',
                'body': \"\"\"
message Assessment {
  OsidCatalog bank = 1;
  Id taker = 2;
}\"\"\"
            }
        }
        """
        def append_imports(_variable_type):
            if (_variable_type in IMPORT_MAPPING and
                    (self.is_primitive(_variable_type) or not self.is_same_package(package_map_file, _variable_type))):
                proto_import = 'import "{0}";'.format(IMPORT_MAPPING[_variable_type])
                if proto_import not in result[object_name]['_imports']:
                    result[object_name]['_imports'].append(proto_import)

        def extract_base_message_name(full_name):
            """ For something like 'osid.id.Id' returns Id
                For something like 'OsidCatalog', returns OsidCatalog
                For something with a built-in type, like 'decimal', return the proto version ('float')
            """
            if self.is_primitive(full_name):
                # This takes precedence over everything else
                return TYPE_MAPPING[full_name]
            elif self.is_same_package(package_map_file, full_name):
                return full_name.split('.')[-1]
            elif full_name in TYPE_MAPPING:
                return TYPE_MAPPING[full_name]
            elif '.' in full_name:
                return full_name.split('.')[-1]

            return full_name

        def format_message(_repeated, _variable_type, _variable_name, count):
            """DRY -- we use this several times in various configs, so extracting it here"""
            # osid.Syntax is special -- make it an enum
            if _variable_type == 'osid.Syntax':
                return """  enum Syntax {{
    NONE = 0;
    BOOLEAN = 1;
    BYTE = 2;
    CARDINAL = 3;
    COORDINATE = 4;
    CURRENCY = 5;
    DATETIME = 6;
    DECIMAL = 7;
    DISPLAYTEXT = 8;
    DISTANCE = 9;
    DURATION = 10;
    HEADING = 11;
    ID = 12;
    INTEGER = 13;
    OBJECT = 14;
    SPATIALUNIT = 15;
    SPEED = 16;
    STRING = 17;
    TIME = 18;
    TYPE = 19;
    VERSION = 20;
  }}
  Syntax {0} = {1};""".format(_variable_name, str(count))

            if _repeated:
                return '  repeated {0} {1} = {2};'.format(extract_base_message_name(_variable_type),
                                                          _variable_name,
                                                          str(count))
            else:
                return '  {0} {1} = {2};'.format(extract_base_message_name(_variable_type),
                                                 _variable_name,
                                                 str(count))

        if not isinstance(protobuf_message, dict):
            raise TypeError('protobuf_message must be a dict')
        if not len(protobuf_message.keys()) == 1:
            raise KeyError('protobuf_message can only have one key')

        object_name = protobuf_message.keys()[0]

        if not isinstance(protobuf_message[object_name], dict):
            raise TypeError('protobuf_message["{0}"] must be a dict'.format(object_name))

        result = {
            object_name: {
                '_imports': [],
                '_type': 'message'
            }
        }
        message_fields = []

        if self.is_list(object_name):
            non_list_name = self.make_non_list(object_name)
            variable_name = make_plural(camel_to_under(non_list_name))
            append_imports(non_list_name)
            message_fields.append(format_message(True, non_list_name, variable_name, 1))
        else:
            variable_counter = 1

            # Not sure if we want to have the fields sorted a certain way....we might care at some point
            for variable, variable_type in iter(sorted(protobuf_message[object_name].items())):
                repeated = False
                if self.is_list(variable_type):
                    variable_type = self.make_non_list(variable_type)
                    repeated = True

                append_imports(variable_type)

                message_fields.append(format_message(repeated,
                                                     variable_type,
                                                     variable,
                                                     variable_counter))
                variable_counter += 1
        result[object_name]['body'] = """
message {0} {{
{1}
}}""".format(object_name,
             '\n'.join(message_fields))

        return result

    def get_package_elements(self, package_map_file, element_type):
        """ Extract all the X elements from the given package file
        X must be in the set of (objects, managers, sessions)
        """
        if element_type not in ['objects', 'managers', 'sessions']:
            raise ValueError('element_type must be one of "objects", "managers", or "sessions"')
        if not os.path.isfile(package_map_file):
            raise ValueError('package_map_file must be a path to a file')
        with open(package_map_file, 'rb') as package_map_handle:
            package_map = json.load(package_map_handle)
            self.package = package_map
            for interface in package_map['interfaces']:
                if not self.build_this_interface(interface):
                    continue

                if element_type == 'objects' and interface['category'] in ['objects', 'queries',
                                                                           'searches', 'rules',
                                                                           'search_orders', 'query_inspectors']:
                    # Objects also include queries and searches
                    # for objects, we actually need to check the pattern_map
                    #   file, to get ``Object.persisted_data``
                    yield self.get_pattern_persisted_data(package_map,
                                                          interface)
                elif interface['category'] == element_type:
                    yield interface
                else:
                    continue

    def get_pattern_persisted_data(self, package, interface):
        """
        We want to return the combined persisted and initialized data for the given interface. Because protobuf3
        cannot inherit / extend from other classes, we also need to find all the inherited object fields.

        **NOTE** Will most likely have to hard-code some of the markers / osid data patterns. Not sure how to
                 automatically generate them...right now it appears they could come from the ``Form`` objects,
                 but might be messy to grab and incomplete. i.e. OsidIdentifiableForm does not have any
                 methods / data for the ``id`` field, so how would we know to generate it? Is this
                 implementation-dependent?

        Example:
          (From package_maps/assessment.json)
            "AssessmentTaken": {
              "inherit_fullnames": [
                 "osid.OsidObject"
              ]
          }

          (From pattern_maps/assessment.json)
            "AssessmentTaken.persisted_data": {
              "bank": "OsidCatalog",
              "taker": "osid.id.Id",
              "assessment_offered": "osid.id.Id"
            },
            "AssessmentTaken.initialized_data": {
              "bank": "OsidCatalog",
              "actual_start_time": "osid.calendaring.DateTime",
              "completion_time": "osid.calendaring.DateTime",
              "score": "decimal",
              "grade": "osid.id.Id",
              "assessment_offered": "osid.id.Id"
            },

            We just want the simplified (and unified) dictionary:
            {
                "AssessmentTaken": {
                    "displayName": "
                    "bank": "OsidCatalog",
                    "taker": "osid.id.Id",
                    "assessment_offered": "osid.id.Id"
                    "actual_start_time": "osid.calendaring.DateTime",
                    "completion_time": "osid.calendaring.DateTime",
                    "score": "decimal",
                    "grade": "osid.id.Id"
                }
            },
        """
        if not isinstance(package, dict):
            raise TypeError('package must be a dictionary')
        if not isinstance(interface, dict):
            raise TypeError('interface must be a dictionary')
        inheritance = interface['inherit_shortnames']
        object_name = interface['shortname']
        with open(self._package_pattern_file(package), 'rb') as pattern_file:
            pattern = json.load(pattern_file)
            persisted_key = '{0}.persisted_data'.format(object_name)
            initialized_key = '{0}.initialized_data'.format(object_name)
            data = {
                object_name: {}
            }
            if any(base_object in inheritance for base_object in ['OsidObject', 'OsidCatalog']):
                data[object_name] = {
                    'displayName': 'osid.locale.DisplayText',
                    'description': 'osid.locale.DisplayText',
                    'genusTypeId': 'osid.type.Type',
                    'id': 'osid.id.Id',
                    'recordTypeIds': 'osid.type.Type[]'
                }
            if 'Aggregateable' in inheritance and object_name in AGGREGATEABLE_MAPPING:
                # hardcode from a map for now...
                data[object_name].update(AGGREGATEABLE_MAPPING[object_name])

            if persisted_key not in pattern and initialized_key not in pattern:
                return data

            if persisted_key in pattern:
                data[object_name].update(pattern[persisted_key])
            if initialized_key in pattern:
                data[object_name].update(pattern[initialized_key])
            return data

    @staticmethod
    def is_list(variable_name):
        """Many of the variables in the spec end with List or []. We need to detect those
            when formatting messages / services so that we can apply the correct ``repeated``
            or ``stream`` label"""
        return variable_name.endswith('List') or variable_name.endswith('[]')

    @staticmethod
    def is_primitive(variable_name):
        """to make sure all primordium imports go there, even for "same packages". """
        return (variable_name in ['osid.id.Id', 'osid.calendaring.DateTime',
                                  'osid.calendaring.Duration', 'osid.calendaring.Time',
                                  'osid.mapping.Coordinate', 'osid.mapping.SpatialUnit',
                                  'osid.type.Type', 'osid.installation.Version',
                                  'osid.transport.DataInputStream'] or
                variable_name in ['Id', 'DateTime', 'Duration',
                                  'Coordinate', 'SpatialUnit',
                                  'Time', 'Type', 'Version',
                                  'DataInputStream'])

    @staticmethod
    def is_same_package(package_map_file, variable_name):
        """Because we don't want recursive imports
        """
        package_name = os.path.basename(package_map_file).split('.')[0]
        if package_name == 'osid':
            if variable_name == 'OsidCatalog':
                return True
        else:
            return package_name in variable_name.lower()
        return False

    def make(self):
        # Generate the proto files for all of the Catalogs and Objects
        for xosid_file in glob.glob(self.xosid_dir + '/*' + self.xosid_ext):
            package = None
            if not os.path.exists(self._package_file(self.grab_osid_name(xosid_file))):
                print('mapping {0} osid.'.format(self.grab_osid_name(xosid_file)))
                package = self.make_xosid_map(xosid_file)
                if not self._pattern_map_exists(package):
                    self._make_impl_pattern_map(package=package)
            if not os.path.exists(self._package_interface_file(self.grab_osid_name(xosid_file))):
                print('indexing interfaces for {0} osid.'.format(self.grab_osid_name(xosid_file)))
                self.make_interface_map(xosid_file, package)

        for json_file in glob.glob(self.package_maps + '/*.json'):
            self.make_proto_files(json_file)

            # Generate a grpc adapter on top, that converts all the passed data into gRPC streams?
            self.make_grpc_adapter(json_file)

        # do this after all .proto files are defined
        self.compile_proto_files()

    def make_grpc_adapter(self, package_map_file):
        """ Add a gRPC adapter, like https://github.com/improbable-eng/grpc-web
        This should take the regular dlkit Python classes and somehow "merge" them / wrap the proto buf classes?
        And then send the protobuf data back, instead of JSON?
        """
        pass

    @staticmethod
    def make_non_list(variable_name):
        """Many of the variables in the spec end with List or []. We need to change those when
            formatting messages / services to the non-list version. i.e. ItemList => Item"""
        return variable_name.replace('[]', '').replace('List', '')

    def make_proto_files(self, package_map_file):
        """ create the proto3 file that defines all the Catalogs and Objects for the given package """
        if not os.path.isfile(package_map_file):
            raise TypeError('package_map_file must be a path to a file')
        proto_data = []
        proto_data += self.define_protobuf_messages(package_map_file)
        proto_data += self.define_grpc_services(package_map_file)
        # do nothing with managers?

        # remove duplicates, like GetBankIdRequest
        proto_data = self.remove_duplicate_entries(proto_data)

        self.write_proto_file(package_map_file, proto_data)

    @staticmethod
    def osid_blacklist(message_name):
        """
        From either a Reply or a Request message (for a session), in the OSID package, we blacklist a set
          of methods for now, because they inherit from other packages. This creates recursive imports,
          which breaks the protoc compiler. Since we currently don't support or use these methods, and we assume
          the OSID package is a "base" package with no dependencies,
          we just blacklist them. This may change in the future, if we implement these methods.

        :param message_name: string, like "GetAuthenticatedAgentReply"
        :return: boolean, True or False
        """
        return message_name in ['GetAuthenticatedAgentReply', 'GetEffectiveAgentReply',
                                'StartTransactionReply', 'GetLocaleReply']

    @staticmethod
    def package_name(package_map_file):
        """Just pulls out the package name from the package_map"""
        return os.path.basename(package_map_file).replace('.json', '')

    def proto_file(self, package_map_file):
        """
        Given a package dictionary, returns the path to the ``dlkit.proto.<package>.proto`` file
        i.e. given /home/user/dlkit-project/builders/package_maps/assessment.json with ``--buildto dlkit/dlkit``,
        returns /home/user/dlkit-project/dlkit/dlkit/proto/assessment.proto
        """
        if not os.path.isfile(package_map_file):
            raise TypeError('package_map_file must be a path to a file')

        package_name = self.package_name(package_map_file)
        proto_file_path = os.path.join(self._build_dir, 'proto')

        if not os.path.isdir(proto_file_path):
            os.makedirs(proto_file_path)
        proto_file_name = os.path.join(proto_file_path, '{0}.proto'.format(package_name))

        return proto_file_name

    @staticmethod
    def remove_duplicate_entries(proto_data):
        """For many of the sessions, there will be duplicate / identical "Request" objects, like
        GetBankIdRequest.

        Remove the duplicates (assuming the same message name means they are identical?)
        """
        used_keys = []
        unique_proto_data = []
        for message in proto_data:
            message_name = message.keys()[0]
            if message_name not in used_keys:
                unique_proto_data.append(message)
                used_keys.append(message_name)
        return unique_proto_data

    @staticmethod
    def unify_bodies(proto_data):
        """From a list of messages / services, extract the ``body`` of all entries into
        a single list.
        Sort by messages first, then services"""
        def filter_data_by_type(proto_type):
            for proto_blob in proto_data:
                object_name = proto_blob.keys()[0]

                if '_type' in proto_blob[object_name] and proto_blob[object_name]['_type'] == proto_type:
                    yield proto_blob[object_name]

        unified_bodies = []
        for blob in filter_data_by_type('message'):
            unified_bodies.append(blob['body'])
        for blob in filter_data_by_type('service'):
            unified_bodies.append(blob['body'])
        return unified_bodies

    @staticmethod
    def unify_imports(proto_data):
        """From a list of messages / services, extract all the ``_imports`` into
        a single list and sort them alphabetically"""
        unified_imports = []
        for proto_blob in proto_data:
            object_name = proto_blob.keys()[0]
            if '_imports' in proto_blob[object_name]:
                unified_imports += proto_blob[object_name]['_imports']
        return sorted(list(set(unified_imports)))

    def write_proto_file(self, package_map_file, proto_data):
        """ Write the given proto data to a ``.proto`` file.
        First, inject the standard headings:

            syntax = "proto3";

            package dlkit.proto.<package name>;

        Then, organize the proto_data and make sure:
            1) imports are at the top
            2) ``message`` all appear before ``service``.

        Think about if we want to break things out even more? i.e. into separate files?
        """
        unified_imports = self.unify_imports(proto_data)
        unified_bodies = self.unify_bodies(proto_data)

        file_data = """// This file is auto-generated by ``protobuf_builder.py``
// DO NOT EDIT THIS BY HAND!
syntax = "proto3";

package dlkit.proto.{0};

{1}
{2}""".format(self.package_name(package_map_file),
              '\n'.join(unified_imports),
              '\n'.join(unified_bodies))

        with open(self.proto_file(package_map_file), 'wb') as proto_file:
            proto_file.write(file_data)
            print('Wrote the proto file in {0}'.format(self.proto_file(package_map_file)))
