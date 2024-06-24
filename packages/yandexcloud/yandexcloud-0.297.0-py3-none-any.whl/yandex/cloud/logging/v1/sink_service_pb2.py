# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/logging/v1/sink_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from yandex.cloud.access import access_pb2 as yandex_dot_cloud_dot_access_dot_access__pb2
from yandex.cloud.api import operation_pb2 as yandex_dot_cloud_dot_api_dot_operation__pb2
from yandex.cloud.logging.v1 import sink_pb2 as yandex_dot_cloud_dot_logging_dot_v1_dot_sink__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*yandex/cloud/logging/v1/sink_service.proto\x12\x17yandex.cloud.logging.v1\x1a\x1cgoogle/api/annotations.proto\x1a google/protobuf/field_mask.proto\x1a yandex/cloud/access/access.proto\x1a yandex/cloud/api/operation.proto\x1a\"yandex/cloud/logging/v1/sink.proto\x1a&yandex/cloud/operation/operation.proto\x1a\x1dyandex/cloud/validation.proto\"/\n\x0eGetSinkRequest\x12\x1d\n\x07sink_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=64\"\x87\x01\n\x10ListSinksRequest\x12\x1f\n\tfolder_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=64\x12\x11\n\tpage_size\x18\x03 \x01(\x03\x12\x1d\n\npage_token\x18\x04 \x01(\tB\t\x8a\xc8\x31\x05<=100\x12\x1a\n\x06\x66ilter\x18\x05 \x01(\tB\n\x8a\xc8\x31\x06<=1000J\x04\x08\x02\x10\x03\"Z\n\x11ListSinksResponse\x12,\n\x05sinks\x18\x01 \x03(\x0b\x32\x1d.yandex.cloud.logging.v1.Sink\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\xd0\x03\n\x11\x43reateSinkRequest\x12\x1f\n\tfolder_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=64\x12/\n\x04name\x18\x02 \x01(\tB!\xf2\xc7\x31\x1d|[a-z][-a-z0-9]{1,61}[a-z0-9]\x12\x1e\n\x0b\x64\x65scription\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=256\x12\x83\x01\n\x06labels\x18\x04 \x03(\x0b\x32\x36.yandex.cloud.logging.v1.CreateSinkRequest.LabelsEntryB;\xf2\xc7\x31\x0b[-_0-9a-z]*\x82\xc8\x31\x04<=64\x8a\xc8\x31\x04<=63\xb2\xc8\x31\x18\x12\x10[a-z][-_0-9a-z]*\x1a\x04\x31-63\x12$\n\x12service_account_id\x18\x05 \x01(\tB\x08\x8a\xc8\x31\x04<=64\x12\x30\n\x03yds\x18\x06 \x01(\x0b\x32!.yandex.cloud.logging.v1.Sink.YdsH\x00\x12.\n\x02s3\x18\x07 \x01(\x0b\x32 .yandex.cloud.logging.v1.Sink.S3H\x00\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x0c\n\x04sink\x12\x04\xc0\xc1\x31\x01\"%\n\x12\x43reateSinkMetadata\x12\x0f\n\x07sink_id\x18\x01 \x01(\t\"\xff\x03\n\x11UpdateSinkRequest\x12\x1d\n\x07sink_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=64\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12/\n\x04name\x18\x03 \x01(\tB!\xf2\xc7\x31\x1d|[a-z][-a-z0-9]{1,61}[a-z0-9]\x12\x1e\n\x0b\x64\x65scription\x18\x04 \x01(\tB\t\x8a\xc8\x31\x05<=256\x12\x83\x01\n\x06labels\x18\x05 \x03(\x0b\x32\x36.yandex.cloud.logging.v1.UpdateSinkRequest.LabelsEntryB;\xf2\xc7\x31\x0b[-_0-9a-z]*\x82\xc8\x31\x04<=64\x8a\xc8\x31\x04<=63\xb2\xc8\x31\x18\x12\x10[a-z][-_0-9a-z]*\x1a\x04\x31-63\x12$\n\x12service_account_id\x18\x06 \x01(\tB\x08\x8a\xc8\x31\x04<=64\x12\x30\n\x03yds\x18\x07 \x01(\x0b\x32!.yandex.cloud.logging.v1.Sink.YdsH\x00\x12.\n\x02s3\x18\x08 \x01(\x0b\x32 .yandex.cloud.logging.v1.Sink.S3H\x00\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x0c\n\x04sink\x12\x04\xc0\xc1\x31\x01\"%\n\x12UpdateSinkMetadata\x12\x0f\n\x07sink_id\x18\x01 \x01(\t\"2\n\x11\x44\x65leteSinkRequest\x12\x1d\n\x07sink_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=64\"%\n\x12\x44\x65leteSinkMetadata\x12\x0f\n\x07sink_id\x18\x01 \x01(\t\"\x94\x01\n\x19ListSinkOperationsRequest\x12\x1d\n\x07sink_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=64\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06\x30-1000\x12\x1d\n\npage_token\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=100\x12\x1a\n\x06\x66ilter\x18\x04 \x01(\tB\n\x8a\xc8\x31\x06<=1000\"l\n\x1aListSinkOperationsResponse\x12\x35\n\noperations\x18\x01 \x03(\x0b\x32!.yandex.cloud.operation.Operation\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t2\x91\x0c\n\x0bSinkService\x12r\n\x03Get\x12\'.yandex.cloud.logging.v1.GetSinkRequest\x1a\x1d.yandex.cloud.logging.v1.Sink\"#\x82\xd3\xe4\x93\x02\x1d\x12\x1b/logging/v1/sinks/{sink_id}\x12x\n\x04List\x12).yandex.cloud.logging.v1.ListSinksRequest\x1a*.yandex.cloud.logging.v1.ListSinksResponse\"\x19\x82\xd3\xe4\x93\x02\x13\x12\x11/logging/v1/sinks\x12\x93\x01\n\x06\x43reate\x12*.yandex.cloud.logging.v1.CreateSinkRequest\x1a!.yandex.cloud.operation.Operation\":\xb2\xd2*\x1a\n\x12\x43reateSinkMetadata\x12\x04Sink\x82\xd3\xe4\x93\x02\x16\"\x11/logging/v1/sinks:\x01*\x12\x9d\x01\n\x06Update\x12*.yandex.cloud.logging.v1.UpdateSinkRequest\x1a!.yandex.cloud.operation.Operation\"D\xb2\xd2*\x1a\n\x12UpdateSinkMetadata\x12\x04Sink\x82\xd3\xe4\x93\x02 2\x1b/logging/v1/sinks/{sink_id}:\x01*\x12\xab\x01\n\x06\x44\x65lete\x12*.yandex.cloud.logging.v1.DeleteSinkRequest\x1a!.yandex.cloud.operation.Operation\"R\xb2\xd2*+\n\x12\x44\x65leteSinkMetadata\x12\x15google.protobuf.Empty\x82\xd3\xe4\x93\x02\x1d*\x1b/logging/v1/sinks/{sink_id}\x12\xa9\x01\n\x0eListOperations\x12\x32.yandex.cloud.logging.v1.ListSinkOperationsRequest\x1a\x33.yandex.cloud.logging.v1.ListSinkOperationsResponse\".\x82\xd3\xe4\x93\x02(\x12&/logging/v1/sinks/{sink_id}/operations\x12\xb1\x01\n\x12ListAccessBindings\x12..yandex.cloud.access.ListAccessBindingsRequest\x1a/.yandex.cloud.access.ListAccessBindingsResponse\":\x82\xd3\xe4\x93\x02\x34\x12\x32/logging/v1/sinks/{resource_id}:listAccessBindings\x12\xe0\x01\n\x11SetAccessBindings\x12-.yandex.cloud.access.SetAccessBindingsRequest\x1a!.yandex.cloud.operation.Operation\"y\xb2\xd2*9\n access.SetAccessBindingsMetadata\x12\x15google.protobuf.Empty\x82\xd3\xe4\x93\x02\x36\"1/logging/v1/sinks/{resource_id}:setAccessBindings:\x01*\x12\xec\x01\n\x14UpdateAccessBindings\x12\x30.yandex.cloud.access.UpdateAccessBindingsRequest\x1a!.yandex.cloud.operation.Operation\"\x7f\xb2\xd2*<\n#access.UpdateAccessBindingsMetadata\x12\x15google.protobuf.Empty\x82\xd3\xe4\x93\x02\x39\x32\x34/logging/v1/sinks/{resource_id}:updateAccessBindings:\x01*Bb\n\x1byandex.cloud.api.logging.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/logging/v1;loggingb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.logging.v1.sink_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\033yandex.cloud.api.logging.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/logging/v1;logging'
  _GETSINKREQUEST.fields_by_name['sink_id']._options = None
  _GETSINKREQUEST.fields_by_name['sink_id']._serialized_options = b'\350\3071\001\212\3101\004<=64'
  _LISTSINKSREQUEST.fields_by_name['folder_id']._options = None
  _LISTSINKSREQUEST.fields_by_name['folder_id']._serialized_options = b'\350\3071\001\212\3101\004<=64'
  _LISTSINKSREQUEST.fields_by_name['page_token']._options = None
  _LISTSINKSREQUEST.fields_by_name['page_token']._serialized_options = b'\212\3101\005<=100'
  _LISTSINKSREQUEST.fields_by_name['filter']._options = None
  _LISTSINKSREQUEST.fields_by_name['filter']._serialized_options = b'\212\3101\006<=1000'
  _CREATESINKREQUEST_LABELSENTRY._options = None
  _CREATESINKREQUEST_LABELSENTRY._serialized_options = b'8\001'
  _CREATESINKREQUEST.oneofs_by_name['sink']._options = None
  _CREATESINKREQUEST.oneofs_by_name['sink']._serialized_options = b'\300\3011\001'
  _CREATESINKREQUEST.fields_by_name['folder_id']._options = None
  _CREATESINKREQUEST.fields_by_name['folder_id']._serialized_options = b'\350\3071\001\212\3101\004<=64'
  _CREATESINKREQUEST.fields_by_name['name']._options = None
  _CREATESINKREQUEST.fields_by_name['name']._serialized_options = b'\362\3071\035|[a-z][-a-z0-9]{1,61}[a-z0-9]'
  _CREATESINKREQUEST.fields_by_name['description']._options = None
  _CREATESINKREQUEST.fields_by_name['description']._serialized_options = b'\212\3101\005<=256'
  _CREATESINKREQUEST.fields_by_name['labels']._options = None
  _CREATESINKREQUEST.fields_by_name['labels']._serialized_options = b'\362\3071\013[-_0-9a-z]*\202\3101\004<=64\212\3101\004<=63\262\3101\030\022\020[a-z][-_0-9a-z]*\032\0041-63'
  _CREATESINKREQUEST.fields_by_name['service_account_id']._options = None
  _CREATESINKREQUEST.fields_by_name['service_account_id']._serialized_options = b'\212\3101\004<=64'
  _UPDATESINKREQUEST_LABELSENTRY._options = None
  _UPDATESINKREQUEST_LABELSENTRY._serialized_options = b'8\001'
  _UPDATESINKREQUEST.oneofs_by_name['sink']._options = None
  _UPDATESINKREQUEST.oneofs_by_name['sink']._serialized_options = b'\300\3011\001'
  _UPDATESINKREQUEST.fields_by_name['sink_id']._options = None
  _UPDATESINKREQUEST.fields_by_name['sink_id']._serialized_options = b'\350\3071\001\212\3101\004<=64'
  _UPDATESINKREQUEST.fields_by_name['name']._options = None
  _UPDATESINKREQUEST.fields_by_name['name']._serialized_options = b'\362\3071\035|[a-z][-a-z0-9]{1,61}[a-z0-9]'
  _UPDATESINKREQUEST.fields_by_name['description']._options = None
  _UPDATESINKREQUEST.fields_by_name['description']._serialized_options = b'\212\3101\005<=256'
  _UPDATESINKREQUEST.fields_by_name['labels']._options = None
  _UPDATESINKREQUEST.fields_by_name['labels']._serialized_options = b'\362\3071\013[-_0-9a-z]*\202\3101\004<=64\212\3101\004<=63\262\3101\030\022\020[a-z][-_0-9a-z]*\032\0041-63'
  _UPDATESINKREQUEST.fields_by_name['service_account_id']._options = None
  _UPDATESINKREQUEST.fields_by_name['service_account_id']._serialized_options = b'\212\3101\004<=64'
  _DELETESINKREQUEST.fields_by_name['sink_id']._options = None
  _DELETESINKREQUEST.fields_by_name['sink_id']._serialized_options = b'\350\3071\001\212\3101\004<=64'
  _LISTSINKOPERATIONSREQUEST.fields_by_name['sink_id']._options = None
  _LISTSINKOPERATIONSREQUEST.fields_by_name['sink_id']._serialized_options = b'\350\3071\001\212\3101\004<=64'
  _LISTSINKOPERATIONSREQUEST.fields_by_name['page_size']._options = None
  _LISTSINKOPERATIONSREQUEST.fields_by_name['page_size']._serialized_options = b'\372\3071\0060-1000'
  _LISTSINKOPERATIONSREQUEST.fields_by_name['page_token']._options = None
  _LISTSINKOPERATIONSREQUEST.fields_by_name['page_token']._serialized_options = b'\212\3101\005<=100'
  _LISTSINKOPERATIONSREQUEST.fields_by_name['filter']._options = None
  _LISTSINKOPERATIONSREQUEST.fields_by_name['filter']._serialized_options = b'\212\3101\006<=1000'
  _SINKSERVICE.methods_by_name['Get']._options = None
  _SINKSERVICE.methods_by_name['Get']._serialized_options = b'\202\323\344\223\002\035\022\033/logging/v1/sinks/{sink_id}'
  _SINKSERVICE.methods_by_name['List']._options = None
  _SINKSERVICE.methods_by_name['List']._serialized_options = b'\202\323\344\223\002\023\022\021/logging/v1/sinks'
  _SINKSERVICE.methods_by_name['Create']._options = None
  _SINKSERVICE.methods_by_name['Create']._serialized_options = b'\262\322*\032\n\022CreateSinkMetadata\022\004Sink\202\323\344\223\002\026\"\021/logging/v1/sinks:\001*'
  _SINKSERVICE.methods_by_name['Update']._options = None
  _SINKSERVICE.methods_by_name['Update']._serialized_options = b'\262\322*\032\n\022UpdateSinkMetadata\022\004Sink\202\323\344\223\002 2\033/logging/v1/sinks/{sink_id}:\001*'
  _SINKSERVICE.methods_by_name['Delete']._options = None
  _SINKSERVICE.methods_by_name['Delete']._serialized_options = b'\262\322*+\n\022DeleteSinkMetadata\022\025google.protobuf.Empty\202\323\344\223\002\035*\033/logging/v1/sinks/{sink_id}'
  _SINKSERVICE.methods_by_name['ListOperations']._options = None
  _SINKSERVICE.methods_by_name['ListOperations']._serialized_options = b'\202\323\344\223\002(\022&/logging/v1/sinks/{sink_id}/operations'
  _SINKSERVICE.methods_by_name['ListAccessBindings']._options = None
  _SINKSERVICE.methods_by_name['ListAccessBindings']._serialized_options = b'\202\323\344\223\0024\0222/logging/v1/sinks/{resource_id}:listAccessBindings'
  _SINKSERVICE.methods_by_name['SetAccessBindings']._options = None
  _SINKSERVICE.methods_by_name['SetAccessBindings']._serialized_options = b'\262\322*9\n access.SetAccessBindingsMetadata\022\025google.protobuf.Empty\202\323\344\223\0026\"1/logging/v1/sinks/{resource_id}:setAccessBindings:\001*'
  _SINKSERVICE.methods_by_name['UpdateAccessBindings']._options = None
  _SINKSERVICE.methods_by_name['UpdateAccessBindings']._serialized_options = b'\262\322*<\n#access.UpdateAccessBindingsMetadata\022\025google.protobuf.Empty\202\323\344\223\002924/logging/v1/sinks/{resource_id}:updateAccessBindings:\001*'
  _globals['_GETSINKREQUEST']._serialized_start=310
  _globals['_GETSINKREQUEST']._serialized_end=357
  _globals['_LISTSINKSREQUEST']._serialized_start=360
  _globals['_LISTSINKSREQUEST']._serialized_end=495
  _globals['_LISTSINKSRESPONSE']._serialized_start=497
  _globals['_LISTSINKSRESPONSE']._serialized_end=587
  _globals['_CREATESINKREQUEST']._serialized_start=590
  _globals['_CREATESINKREQUEST']._serialized_end=1054
  _globals['_CREATESINKREQUEST_LABELSENTRY']._serialized_start=995
  _globals['_CREATESINKREQUEST_LABELSENTRY']._serialized_end=1040
  _globals['_CREATESINKMETADATA']._serialized_start=1056
  _globals['_CREATESINKMETADATA']._serialized_end=1093
  _globals['_UPDATESINKREQUEST']._serialized_start=1096
  _globals['_UPDATESINKREQUEST']._serialized_end=1607
  _globals['_UPDATESINKREQUEST_LABELSENTRY']._serialized_start=995
  _globals['_UPDATESINKREQUEST_LABELSENTRY']._serialized_end=1040
  _globals['_UPDATESINKMETADATA']._serialized_start=1609
  _globals['_UPDATESINKMETADATA']._serialized_end=1646
  _globals['_DELETESINKREQUEST']._serialized_start=1648
  _globals['_DELETESINKREQUEST']._serialized_end=1698
  _globals['_DELETESINKMETADATA']._serialized_start=1700
  _globals['_DELETESINKMETADATA']._serialized_end=1737
  _globals['_LISTSINKOPERATIONSREQUEST']._serialized_start=1740
  _globals['_LISTSINKOPERATIONSREQUEST']._serialized_end=1888
  _globals['_LISTSINKOPERATIONSRESPONSE']._serialized_start=1890
  _globals['_LISTSINKOPERATIONSRESPONSE']._serialized_end=1998
  _globals['_SINKSERVICE']._serialized_start=2001
  _globals['_SINKSERVICE']._serialized_end=3554
# @@protoc_insertion_point(module_scope)
