# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/serverless/apigateway/websocket/v1/connection_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2
from yandex.cloud.serverless.apigateway.websocket.v1 import connection_pb2 as yandex_dot_cloud_dot_serverless_dot_apigateway_dot_websocket_dot_v1_dot_connection__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nHyandex/cloud/serverless/apigateway/websocket/v1/connection_service.proto\x12/yandex.cloud.serverless.apigateway.websocket.v1\x1a\x1cgoogle/api/annotations.proto\x1a\x1dyandex/cloud/validation.proto\x1a@yandex/cloud/serverless/apigateway/websocket/v1/connection.proto\";\n\x14GetConnectionRequest\x12#\n\rconnection_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"\xfc\x01\n\x17SendToConnectionRequest\x12#\n\rconnection_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1e\n\x04\x64\x61ta\x18\x02 \x01(\x0c\x42\x10\xe8\xc7\x31\x01\x8a\xc8\x31\x08<=131072\x12_\n\x04type\x18\x03 \x01(\x0e\x32Q.yandex.cloud.serverless.apigateway.websocket.v1.SendToConnectionRequest.DataType\";\n\x08\x44\x61taType\x12\x19\n\x15\x44\x41TA_TYPE_UNSPECIFIED\x10\x00\x12\n\n\x06\x42INARY\x10\x01\x12\x08\n\x04TEXT\x10\x02\"\x1a\n\x18SendToConnectionResponse\"8\n\x11\x44isconnectRequest\x12#\n\rconnection_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"\x14\n\x12\x44isconnectResponse2\x9a\x05\n\x11\x43onnectionService\x12\xc8\x01\n\x03Get\x12\x45.yandex.cloud.serverless.apigateway.websocket.v1.GetConnectionRequest\x1a;.yandex.cloud.serverless.apigateway.websocket.v1.Connection\"=\x82\xd3\xe4\x93\x02\x37\x12\x35/apigateways/websocket/v1/connections/{connection_id}\x12\xe2\x01\n\x04Send\x12H.yandex.cloud.serverless.apigateway.websocket.v1.SendToConnectionRequest\x1aI.yandex.cloud.serverless.apigateway.websocket.v1.SendToConnectionResponse\"E\x82\xd3\xe4\x93\x02?\":/apigateways/websocket/v1/connections/{connection_id}:send:\x01*\x12\xd4\x01\n\nDisconnect\x12\x42.yandex.cloud.serverless.apigateway.websocket.v1.DisconnectRequest\x1a\x43.yandex.cloud.serverless.apigateway.websocket.v1.DisconnectResponse\"=\x82\xd3\xe4\x93\x02\x37*5/apigateways/websocket/v1/connections/{connection_id}B\x94\x01\n3yandex.cloud.api.serverless.apigateway.websocket.v1Z]github.com/yandex-cloud/go-genproto/yandex/cloud/serverless/apigateway/websocket/v1;websocketb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n3yandex.cloud.api.serverless.apigateway.websocket.v1Z]github.com/yandex-cloud/go-genproto/yandex/cloud/serverless/apigateway/websocket/v1;websocket'
  _GETCONNECTIONREQUEST.fields_by_name['connection_id']._options = None
  _GETCONNECTIONREQUEST.fields_by_name['connection_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _SENDTOCONNECTIONREQUEST.fields_by_name['connection_id']._options = None
  _SENDTOCONNECTIONREQUEST.fields_by_name['connection_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _SENDTOCONNECTIONREQUEST.fields_by_name['data']._options = None
  _SENDTOCONNECTIONREQUEST.fields_by_name['data']._serialized_options = b'\350\3071\001\212\3101\010<=131072'
  _DISCONNECTREQUEST.fields_by_name['connection_id']._options = None
  _DISCONNECTREQUEST.fields_by_name['connection_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _CONNECTIONSERVICE.methods_by_name['Get']._options = None
  _CONNECTIONSERVICE.methods_by_name['Get']._serialized_options = b'\202\323\344\223\0027\0225/apigateways/websocket/v1/connections/{connection_id}'
  _CONNECTIONSERVICE.methods_by_name['Send']._options = None
  _CONNECTIONSERVICE.methods_by_name['Send']._serialized_options = b'\202\323\344\223\002?\":/apigateways/websocket/v1/connections/{connection_id}:send:\001*'
  _CONNECTIONSERVICE.methods_by_name['Disconnect']._options = None
  _CONNECTIONSERVICE.methods_by_name['Disconnect']._serialized_options = b'\202\323\344\223\0027*5/apigateways/websocket/v1/connections/{connection_id}'
  _globals['_GETCONNECTIONREQUEST']._serialized_start=252
  _globals['_GETCONNECTIONREQUEST']._serialized_end=311
  _globals['_SENDTOCONNECTIONREQUEST']._serialized_start=314
  _globals['_SENDTOCONNECTIONREQUEST']._serialized_end=566
  _globals['_SENDTOCONNECTIONREQUEST_DATATYPE']._serialized_start=507
  _globals['_SENDTOCONNECTIONREQUEST_DATATYPE']._serialized_end=566
  _globals['_SENDTOCONNECTIONRESPONSE']._serialized_start=568
  _globals['_SENDTOCONNECTIONRESPONSE']._serialized_end=594
  _globals['_DISCONNECTREQUEST']._serialized_start=596
  _globals['_DISCONNECTREQUEST']._serialized_end=652
  _globals['_DISCONNECTRESPONSE']._serialized_start=654
  _globals['_DISCONNECTRESPONSE']._serialized_end=674
  _globals['_CONNECTIONSERVICE']._serialized_start=677
  _globals['_CONNECTIONSERVICE']._serialized_end=1343
# @@protoc_insertion_point(module_scope)
