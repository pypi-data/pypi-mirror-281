# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/mdb/clickhouse/v1/resource_preset_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2
from yandex.cloud.mdb.clickhouse.v1 import resource_preset_pb2 as yandex_dot_cloud_dot_mdb_dot_clickhouse_dot_v1_dot_resource__preset__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n<yandex/cloud/mdb/clickhouse/v1/resource_preset_service.proto\x12\x1eyandex.cloud.mdb.clickhouse.v1\x1a\x1cgoogle/api/annotations.proto\x1a\x1dyandex/cloud/validation.proto\x1a\x34yandex/cloud/mdb/clickhouse/v1/resource_preset.proto\"D\n\x18GetResourcePresetRequest\x12(\n\x12resource_preset_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"Z\n\x1aListResourcePresetsRequest\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06<=1000\x12\x1d\n\npage_token\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=100\"\x80\x01\n\x1bListResourcePresetsResponse\x12H\n\x10resource_presets\x18\x01 \x03(\x0b\x32..yandex.cloud.mdb.clickhouse.v1.ResourcePreset\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t2\x80\x03\n\x15ResourcePresetService\x12\xb4\x01\n\x03Get\x12\x38.yandex.cloud.mdb.clickhouse.v1.GetResourcePresetRequest\x1a..yandex.cloud.mdb.clickhouse.v1.ResourcePreset\"C\x82\xd3\xe4\x93\x02=\x12;/managed-clickhouse/v1/resourcePresets/{resource_preset_id}\x12\xaf\x01\n\x04List\x12:.yandex.cloud.mdb.clickhouse.v1.ListResourcePresetsRequest\x1a;.yandex.cloud.mdb.clickhouse.v1.ListResourcePresetsResponse\".\x82\xd3\xe4\x93\x02(\x12&/managed-clickhouse/v1/resourcePresetsBs\n\"yandex.cloud.api.mdb.clickhouse.v1ZMgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/clickhouse/v1;clickhouseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.mdb.clickhouse.v1.resource_preset_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\"yandex.cloud.api.mdb.clickhouse.v1ZMgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/clickhouse/v1;clickhouse'
  _GETRESOURCEPRESETREQUEST.fields_by_name['resource_preset_id']._options = None
  _GETRESOURCEPRESETREQUEST.fields_by_name['resource_preset_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _LISTRESOURCEPRESETSREQUEST.fields_by_name['page_size']._options = None
  _LISTRESOURCEPRESETSREQUEST.fields_by_name['page_size']._serialized_options = b'\372\3071\006<=1000'
  _LISTRESOURCEPRESETSREQUEST.fields_by_name['page_token']._options = None
  _LISTRESOURCEPRESETSREQUEST.fields_by_name['page_token']._serialized_options = b'\212\3101\005<=100'
  _RESOURCEPRESETSERVICE.methods_by_name['Get']._options = None
  _RESOURCEPRESETSERVICE.methods_by_name['Get']._serialized_options = b'\202\323\344\223\002=\022;/managed-clickhouse/v1/resourcePresets/{resource_preset_id}'
  _RESOURCEPRESETSERVICE.methods_by_name['List']._options = None
  _RESOURCEPRESETSERVICE.methods_by_name['List']._serialized_options = b'\202\323\344\223\002(\022&/managed-clickhouse/v1/resourcePresets'
  _globals['_GETRESOURCEPRESETREQUEST']._serialized_start=211
  _globals['_GETRESOURCEPRESETREQUEST']._serialized_end=279
  _globals['_LISTRESOURCEPRESETSREQUEST']._serialized_start=281
  _globals['_LISTRESOURCEPRESETSREQUEST']._serialized_end=371
  _globals['_LISTRESOURCEPRESETSRESPONSE']._serialized_start=374
  _globals['_LISTRESOURCEPRESETSRESPONSE']._serialized_end=502
  _globals['_RESOURCEPRESETSERVICE']._serialized_start=505
  _globals['_RESOURCEPRESETSERVICE']._serialized_end=889
# @@protoc_insertion_point(module_scope)
