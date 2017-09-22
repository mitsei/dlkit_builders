import glob
import json
import os

from binder_helpers import under_to_camel
from build_dlkit import PatternBuilder
from interface_builders import InterfaceBuilder

IMPORT_MAPPING = {
    'osid.id.Id': 'dlkit/primordium/id/primitives.proto',
    'osid.calendaring.DateTime': 'google/protobuf/timestamp.proto',  # a Google built-in one?
    'osid.calendaring.Duration': 'dlkit/primordium/calendaring/primitives.proto',
    'osid.locale.DisplayText': 'dlkit/primordium/locale/primitives.proto',
    'OsidCatalog': 'osid/objects.proto',
    # Where to get IdList from??
}

TYPE_MAPPING = {
    'decimal': 'float',
    'cardinal': 'sint32',
    'boolean': 'bool',
    'osid.calendaring.DateTime': 'google.protobuf.Timestamp',
    'osid.id.Id[]': 'dlkit.primordium.id.primitives.IdList',
    'osid.id.Id': 'dlkit.primordium.id.primitives.Id',
    'OsidCatalog': 'dlkit.proto.osid.OsidCatalog'
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
                    'var_name': 'GetBookRequest'
                }],
                'return_type': 'Book'
            }, {
                'name': 'QueryBooks',
                'args': [{
                    'var_name': 'QueryBooksRequest'
                }],
                'return_type': 'Book[]'
            }]
        }

        this method would return:
        {
            'BookService': {
                '_imports': [],
                'body': \"\"\"
service BookService {
  rpc GetBook(GetBookRequest) returns (Book) {}
  rpc QueryBooks(QueryBooksRequest) returns (stream Book) {}
}\"\"\"
            }
        }
        """
        def get_return_text(return_type):
            """
            For 'ResourceList', should return 'stream Resource'
            For 'Resource', should return 'Resource'
            """
            return_type_without_package = return_type.split('.')[-1]
            if return_type_without_package.endswith('List'):
                return 'stream {0}'.format(return_type_without_package.replace('List', ''))
            return return_type_without_package

        def get_arg_type(arg_type):
            """
            Need to translate the argument type into the proto message "type", i.e.

            item_genus_type => GenusType
            bank_id => Id

            But for proto-defined messages in this package, it would just be the name in mixedCase
            """
            # TODO: see if these exceptions can get moved somewhere with the maps in ``generate_protobuf_message``
            if arg_type.endswith('Type'):
                return 'dlkit.primordium.type.primitives.Type'
            elif arg_type.endswith('IdList'):
                return 'dlkit.primordium.id.primitives.IdList'  # ?? This doesn't exist...
            elif arg_type.endswith('Id'):
                return 'dlkit.primordium.id.primitives.Id'
            elif arg_type in TYPE_MAPPING:
                return TYPE_MAPPING[arg_type]
            return arg_type

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
        for method in grpc_service['methods']:
            method_name = under_to_camel(method['name'])
            # TODO: Handle any imports here?
            service_args = []
            for arg in method['args']:
                service_args.append(get_arg_type(arg['arg_type']))
            service_fields.append('  rpc {0}({1}) returns ({2}) {{}}'.format(method_name,
                                                                             ', '.join(service_args),
                                                                             get_return_text(method['return_type'])))
        result[service_name]['body'] = """
service {0} {{
{1}
}}""".format(service_name,
             '\n'.join(service_fields))

        return result

    @staticmethod
    def generate_protobuf_message(protobuf_message):
        """
        given the data for an object, return a protobuf-style message

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
                'body': \"\"\"
message Assessment {
  OsidCatalog bank = 1;
  Id taker = 2;
}\"\"\"
            }
        }
        """
        def extract_base_message_name(full_name):
            """ For something like 'osid.id.Id' returns Id
                For something like 'OsidCatalog', returns OsidCatalog
                For something with a built-in type, like 'decimal', return the proto version ('float')
            """
            if full_name in TYPE_MAPPING:
                return TYPE_MAPPING[full_name]
            elif '.' in full_name:
                return full_name.split('.')[-1]

            return full_name

        if not isinstance(protobuf_message, dict):
            raise TypeError('protobuf_message must be a dict')
        if not len(protobuf_message.keys()) == 1:
            raise KeyError('protobuf_message can only have one key')

        object_name = protobuf_message.keys()[0]

        if not isinstance(protobuf_message[object_name], dict):
            raise TypeError('protobuf_message value must be a dict')

        result = {
            object_name: {
                '_imports': [],
                '_type': 'message'
            }
        }
        message_fields = []

        if object_name.endswith('List'):
            message_fields.append('  repeated {0} = 1;'.format(object_name.replace('List', '')))
        else:
            variable_counter = 1

            # Not sure if we want to have the fields sorted a certain way....we might care at some point
            for variable, variable_type in iter(sorted(protobuf_message[object_name].items())):
                if variable_type in IMPORT_MAPPING:
                    proto_import = 'import "{0}";'.format(IMPORT_MAPPING[variable_type])
                    if proto_import not in result[object_name]['_imports']:
                        result[object_name]['_imports'].append(proto_import)
                message_fields.append('  {0} {1} = {2};'.format(extract_base_message_name(variable_type),
                                                                variable,
                                                                str(variable_counter)))
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
            for interface in package_map['interfaces']:
                if element_type == 'objects' and interface['category'] in [element_type, 'queries', 'searches']:
                    # Objects also include queries and searches
                    # for objects, we actually need to check the pattern_map
                    #   file, to get ``Object.persisted_data``
                    yield self.get_pattern_persisted_data(package_map,
                                                          interface['shortname'])
                elif interface['category'] == element_type:
                    yield interface
                else:
                    continue

    def get_pattern_persisted_data(self, package, interface):
        """ We want to return the combined persisted and initialized data for the given interface, i.e.
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
        with open(self._package_pattern_file(package), 'rb') as pattern_file:
            pattern = json.load(pattern_file)
            persisted_key = '{0}.persisted_data'.format(interface)
            initialized_key = '{0}.initialized_data'.format(interface)
            data = {
                interface: {}
            }

            if persisted_key not in pattern and initialized_key not in pattern:
                return data

            if persisted_key in pattern:
                data[interface].update(pattern[persisted_key])
            if initialized_key in pattern:
                data[interface].update(pattern[initialized_key])
            return data

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

    def make_grpc_adapter(self, package_map_file):
        """ Add a gRPC adapter, like https://github.com/improbable-eng/grpc-web
        This should take the regular Python classes and somehow "merge" them / wrap the proto buf classes?
        And then send the protobuf data back, instead of JSON?
        """
        pass

    def make_proto_files(self, package_map_file):
        """ create the proto3 file that defines all the Catalogs and Objects for the given package """
        if not os.path.isfile(package_map_file):
            raise TypeError('package_map_file must be a path to a file')
        proto_data = []
        for protobuf_message in self.get_package_elements(package_map_file, 'objects'):
            # treat objects as protobuf messages
            proto_data.append(self.generate_protobuf_message(protobuf_message))
        for grpc_service in self.get_package_elements(package_map_file, 'sessions'):
            # treat sessions as grpc services
            proto_data.append(self.generate_grpc_service(grpc_service))
        # do nothing with managers?
        self.write_proto_file(package_map_file, proto_data)

        # TODO: Compile the proto files with protoc ?

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
        a single list"""
        unified_imports = []
        for proto_blob in proto_data:
            object_name = proto_blob.keys()[0]
            if '_imports' in proto_blob[object_name]:
                unified_imports += proto_blob[object_name]['_imports']
        return list(set(unified_imports))

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

        file_data = """syntax = "proto3";

package dlkit.proto.{0};

{1}
{2}""".format(self.package_name(package_map_file),
              '\n'.join(unified_imports),
              '\n'.join(unified_bodies))

        with open(self.proto_file(package_map_file), 'wb') as proto_file:
            proto_file.write(file_data)
            print('Wrote the proto file in {0}'.format(self.proto_file(package_map_file)))
