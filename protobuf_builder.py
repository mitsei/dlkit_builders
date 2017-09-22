import glob
import json
import os

from build_dlkit import PatternBuilder
from interface_builders import InterfaceBuilder


class ProtoBuilder(InterfaceBuilder, PatternBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(ProtoBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir + '/proto'
        self._template_dir = self._abs_path + '/proto_templates'

        self._class = 'proto'

    def generate_grpc_service(self, grpc_service):
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
                'GetBook': ('GetBookRequest', 'Book'),
                'QueryBooks': ('QueryBooksRequest', 'stream Book')
            }
        }

        which will have to be translated (in another method) into:
        service BookService {
          rpc GetBook(GetBookRequest) returns (Book) {}
          rpc QueryBooks(QueryBooksRequest) returns (stream Book) {}
        }
        """
        pass

    def generate_protobuf_message(self, protobuf_message):
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
                'bank': 'OsidCatalog',
                'taker': 'Id'
            }
        }

        which will have to be translated (in another method) into:
        import '../primordium/id/primitives.proto';
        import 'osid/objects.proto';

        message Assessment {
          OsidCatalog bank = 1;
          Id taker = 2;
        }
        """
        def extract_base_message_name(full_name):
            """ For something like 'osid.id.Id' returns Id
                For something like 'OsidCatalog', returns OsidCatalog
                For something with a built-in type, like 'decimal', return the proto version ('float')
            """
            if full_name in type_mapping:
                return type_mapping[full_name]
            if '.' in full_name:
                return full_name.split('.')[-1]

            return full_name

        if not isinstance(protobuf_message, dict):
            raise TypeError('protobuf_message must be a dict')
        if not len(protobuf_message.keys()) == 1:
            raise KeyError('protobuf_message can only have one key')

        object_name = protobuf_message.keys()[0]

        if not isinstance(protobuf_message[object_name], dict):
            raise TypeError('protobuf_message value must be a dict')

        import_mapping = {
            'osid.id.Id': 'dlkit/primordium/id/primitives.proto',
            'osid.calendaring.DateTime': 'google/protobuf/timestamp.proto',  # a Google built-in one?
            'osid.calendaring.Duration': 'dlkit/primordium/calendaring/primitives.proto',
            'osid.locale.DisplayText': 'dlkit/primordium/locale/primitives.proto',
            'OsidCatalog': 'osid/objects.proto',
        }

        type_mapping = {
            'decimal': 'float',
            'cardinal': 'sint32',
            'boolean': 'bool',
            'osid.calendaring.DateTime': 'google.protobuf.Timestamp'
        }

        result = {
            object_name: {
                '_imports': []
            }
        }
        for variable, variable_type in protobuf_message[object_name].items():
            if variable_type in import_mapping:
                result[object_name]['_imports'].append(import_mapping[variable_type])
            result[object_name][variable] = extract_base_message_name(variable_type)

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
                if element_type == 'objects' and interface['category'] == element_type:
                    # for objects, we actually need to check the pattern_map
                    #   file, to get ``Object.persisted_data``
                    yield self.get_pattern_persisted_data(package_map,
                                                          interface['shortname'])
                elif interface['category'] == element_type:
                    yield interface

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
            if persisted_key not in pattern and initialized_key not in pattern:
                return
            data = {
                interface: {}
            }
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
        import pdb
        pdb.set_trace()
        proto_data = []
        for protobuf_message in self.get_package_elements(package_map_file, 'objects'):
            # treat objects as protobuf messages
            proto_data += self.generate_protobuf_message(protobuf_message)
        for grpc_service in self.get_package_elements(package_map_file, 'sessions'):
            # treat sessions as grpc services
            proto_data += self.generate_grpc_service(grpc_service)
        # do nothing with managers?
        self.write_proto_file(proto_data)

    def write_proto_file(self, proto_data):
        """ Write the given proto data to a ``.proto`` file.
        First, inject the standard headings:

            'syntax = "proto3";'

            package dlkit.proto.<package name>

        Then, organize the proto_data and make sure:
            1) imports are at the top
            2) ``message`` all appear before ``service``.

        Think about if we want to break things out even more? i.e. into separate files?
        """
        pass
