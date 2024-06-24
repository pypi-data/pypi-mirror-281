# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/cdn/v1/origin_group_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from yandex.cloud.api import operation_pb2 as yandex_dot_cloud_dot_api_dot_operation__pb2
from yandex.cloud.cdn.v1 import origin_pb2 as yandex_dot_cloud_dot_cdn_dot_v1_dot_origin__pb2
from yandex.cloud.cdn.v1 import origin_group_pb2 as yandex_dot_cloud_dot_cdn_dot_v1_dot_origin__group__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.yandex/cloud/cdn/v1/origin_group_service.proto\x12\x13yandex.cloud.cdn.v1\x1a\x1cgoogle/api/annotations.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a yandex/cloud/api/operation.proto\x1a yandex/cloud/cdn/v1/origin.proto\x1a&yandex/cloud/cdn/v1/origin_group.proto\x1a&yandex/cloud/operation/operation.proto\x1a\x1dyandex/cloud/validation.proto\"Y\n\x15GetOriginGroupRequest\x12\x1f\n\tfolder_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1f\n\x0forigin_group_id\x18\x02 \x01(\x03\x42\x06\xfa\xc7\x31\x02>0\"x\n\x17ListOriginGroupsRequest\x12\x1f\n\tfolder_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06<=1000\x12\x1d\n\npage_token\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=100\"l\n\x18ListOriginGroupsResponse\x12\x37\n\rorigin_groups\x18\x01 \x03(\x0b\x32 .yandex.cloud.cdn.v1.OriginGroup\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\xab\x01\n\x18\x43reateOriginGroupRequest\x12\x1f\n\tfolder_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x0c\n\x04name\x18\x02 \x01(\t\x12,\n\x08use_next\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x32\n\x07origins\x18\x04 \x03(\x0b\x32!.yandex.cloud.cdn.v1.OriginParams\"<\n\x19\x43reateOriginGroupMetadata\x12\x1f\n\x0forigin_group_id\x18\x01 \x01(\x03\x42\x06\xfa\xc7\x31\x02>0\"\xf0\x01\n\x18UpdateOriginGroupRequest\x12\x1f\n\tfolder_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1f\n\x0forigin_group_id\x18\x02 \x01(\x03\x42\x06\xfa\xc7\x31\x02>0\x12\x30\n\ngroup_name\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12,\n\x08use_next\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x32\n\x07origins\x18\x05 \x03(\x0b\x32!.yandex.cloud.cdn.v1.OriginParams\"<\n\x19UpdateOriginGroupMetadata\x12\x1f\n\x0forigin_group_id\x18\x01 \x01(\x03\x42\x06\xfa\xc7\x31\x02>0\"\\\n\x18\x44\x65leteOriginGroupRequest\x12\x1f\n\tfolder_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1f\n\x0forigin_group_id\x18\x02 \x01(\x03\x42\x06\xfa\xc7\x31\x02>0\"<\n\x19\x44\x65leteOriginGroupMetadata\x12\x1f\n\x0forigin_group_id\x18\x01 \x01(\x03\x42\x06\xfa\xc7\x31\x02>02\xb5\x06\n\x12OriginGroupService\x12\x83\x01\n\x03Get\x12*.yandex.cloud.cdn.v1.GetOriginGroupRequest\x1a .yandex.cloud.cdn.v1.OriginGroup\".\x82\xd3\xe4\x93\x02(\x12&/cdn/v1/originGroups/{origin_group_id}\x12\x81\x01\n\x04List\x12,.yandex.cloud.cdn.v1.ListOriginGroupsRequest\x1a-.yandex.cloud.cdn.v1.ListOriginGroupsResponse\"\x1c\x82\xd3\xe4\x93\x02\x16\x12\x14/cdn/v1/originGroups\x12\xa7\x01\n\x06\x43reate\x12-.yandex.cloud.cdn.v1.CreateOriginGroupRequest\x1a!.yandex.cloud.operation.Operation\"K\xb2\xd2*(\n\x19\x43reateOriginGroupMetadata\x12\x0bOriginGroup\x82\xd3\xe4\x93\x02\x19\"\x14/cdn/v1/originGroups:\x01*\x12\xa7\x01\n\x06Update\x12-.yandex.cloud.cdn.v1.UpdateOriginGroupRequest\x1a!.yandex.cloud.operation.Operation\"K\xb2\xd2*(\n\x19UpdateOriginGroupMetadata\x12\x0bOriginGroup\x82\xd3\xe4\x93\x02\x19\x32\x14/cdn/v1/originGroups:\x01*\x12\xc0\x01\n\x06\x44\x65lete\x12-.yandex.cloud.cdn.v1.DeleteOriginGroupRequest\x1a!.yandex.cloud.operation.Operation\"d\xb2\xd2*2\n\x19\x44\x65leteOriginGroupMetadata\x12\x15google.protobuf.Empty\x82\xd3\xe4\x93\x02(*&/cdn/v1/originGroups/{origin_group_id}BV\n\x17yandex.cloud.api.cdn.v1Z;github.com/yandex-cloud/go-genproto/yandex/cloud/cdn/v1;cdnb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.cdn.v1.origin_group_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\027yandex.cloud.api.cdn.v1Z;github.com/yandex-cloud/go-genproto/yandex/cloud/cdn/v1;cdn'
  _GETORIGINGROUPREQUEST.fields_by_name['folder_id']._options = None
  _GETORIGINGROUPREQUEST.fields_by_name['folder_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _GETORIGINGROUPREQUEST.fields_by_name['origin_group_id']._options = None
  _GETORIGINGROUPREQUEST.fields_by_name['origin_group_id']._serialized_options = b'\372\3071\002>0'
  _LISTORIGINGROUPSREQUEST.fields_by_name['folder_id']._options = None
  _LISTORIGINGROUPSREQUEST.fields_by_name['folder_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _LISTORIGINGROUPSREQUEST.fields_by_name['page_size']._options = None
  _LISTORIGINGROUPSREQUEST.fields_by_name['page_size']._serialized_options = b'\372\3071\006<=1000'
  _LISTORIGINGROUPSREQUEST.fields_by_name['page_token']._options = None
  _LISTORIGINGROUPSREQUEST.fields_by_name['page_token']._serialized_options = b'\212\3101\005<=100'
  _CREATEORIGINGROUPREQUEST.fields_by_name['folder_id']._options = None
  _CREATEORIGINGROUPREQUEST.fields_by_name['folder_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _CREATEORIGINGROUPMETADATA.fields_by_name['origin_group_id']._options = None
  _CREATEORIGINGROUPMETADATA.fields_by_name['origin_group_id']._serialized_options = b'\372\3071\002>0'
  _UPDATEORIGINGROUPREQUEST.fields_by_name['folder_id']._options = None
  _UPDATEORIGINGROUPREQUEST.fields_by_name['folder_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _UPDATEORIGINGROUPREQUEST.fields_by_name['origin_group_id']._options = None
  _UPDATEORIGINGROUPREQUEST.fields_by_name['origin_group_id']._serialized_options = b'\372\3071\002>0'
  _UPDATEORIGINGROUPMETADATA.fields_by_name['origin_group_id']._options = None
  _UPDATEORIGINGROUPMETADATA.fields_by_name['origin_group_id']._serialized_options = b'\372\3071\002>0'
  _DELETEORIGINGROUPREQUEST.fields_by_name['folder_id']._options = None
  _DELETEORIGINGROUPREQUEST.fields_by_name['folder_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _DELETEORIGINGROUPREQUEST.fields_by_name['origin_group_id']._options = None
  _DELETEORIGINGROUPREQUEST.fields_by_name['origin_group_id']._serialized_options = b'\372\3071\002>0'
  _DELETEORIGINGROUPMETADATA.fields_by_name['origin_group_id']._options = None
  _DELETEORIGINGROUPMETADATA.fields_by_name['origin_group_id']._serialized_options = b'\372\3071\002>0'
  _ORIGINGROUPSERVICE.methods_by_name['Get']._options = None
  _ORIGINGROUPSERVICE.methods_by_name['Get']._serialized_options = b'\202\323\344\223\002(\022&/cdn/v1/originGroups/{origin_group_id}'
  _ORIGINGROUPSERVICE.methods_by_name['List']._options = None
  _ORIGINGROUPSERVICE.methods_by_name['List']._serialized_options = b'\202\323\344\223\002\026\022\024/cdn/v1/originGroups'
  _ORIGINGROUPSERVICE.methods_by_name['Create']._options = None
  _ORIGINGROUPSERVICE.methods_by_name['Create']._serialized_options = b'\262\322*(\n\031CreateOriginGroupMetadata\022\013OriginGroup\202\323\344\223\002\031\"\024/cdn/v1/originGroups:\001*'
  _ORIGINGROUPSERVICE.methods_by_name['Update']._options = None
  _ORIGINGROUPSERVICE.methods_by_name['Update']._serialized_options = b'\262\322*(\n\031UpdateOriginGroupMetadata\022\013OriginGroup\202\323\344\223\002\0312\024/cdn/v1/originGroups:\001*'
  _ORIGINGROUPSERVICE.methods_by_name['Delete']._options = None
  _ORIGINGROUPSERVICE.methods_by_name['Delete']._serialized_options = b'\262\322*2\n\031DeleteOriginGroupMetadata\022\025google.protobuf.Empty\202\323\344\223\002(*&/cdn/v1/originGroups/{origin_group_id}'
  _globals['_GETORIGINGROUPREQUEST']._serialized_start=312
  _globals['_GETORIGINGROUPREQUEST']._serialized_end=401
  _globals['_LISTORIGINGROUPSREQUEST']._serialized_start=403
  _globals['_LISTORIGINGROUPSREQUEST']._serialized_end=523
  _globals['_LISTORIGINGROUPSRESPONSE']._serialized_start=525
  _globals['_LISTORIGINGROUPSRESPONSE']._serialized_end=633
  _globals['_CREATEORIGINGROUPREQUEST']._serialized_start=636
  _globals['_CREATEORIGINGROUPREQUEST']._serialized_end=807
  _globals['_CREATEORIGINGROUPMETADATA']._serialized_start=809
  _globals['_CREATEORIGINGROUPMETADATA']._serialized_end=869
  _globals['_UPDATEORIGINGROUPREQUEST']._serialized_start=872
  _globals['_UPDATEORIGINGROUPREQUEST']._serialized_end=1112
  _globals['_UPDATEORIGINGROUPMETADATA']._serialized_start=1114
  _globals['_UPDATEORIGINGROUPMETADATA']._serialized_end=1174
  _globals['_DELETEORIGINGROUPREQUEST']._serialized_start=1176
  _globals['_DELETEORIGINGROUPREQUEST']._serialized_end=1268
  _globals['_DELETEORIGINGROUPMETADATA']._serialized_start=1270
  _globals['_DELETEORIGINGROUPMETADATA']._serialized_end=1330
  _globals['_ORIGINGROUPSERVICE']._serialized_start=1333
  _globals['_ORIGINGROUPSERVICE']._serialized_end=2154
# @@protoc_insertion_point(module_scope)
