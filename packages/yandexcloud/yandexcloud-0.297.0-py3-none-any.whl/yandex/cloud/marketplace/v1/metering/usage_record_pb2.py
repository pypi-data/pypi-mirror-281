# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/marketplace/v1/metering/usage_record.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n7yandex/cloud/marketplace/v1/metering/usage_record.proto\x12$yandex.cloud.marketplace.v1.metering\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1dyandex/cloud/validation.proto\"\x96\x01\n\x0bUsageRecord\x12\x1a\n\x04uuid\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=36\x12\x1c\n\x06sku_id\x18\x02 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x18\n\x08quantity\x18\x03 \x01(\x03\x42\x06\xfa\xc7\x31\x02>0\x12\x33\n\ttimestamp\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x04\xe8\xc7\x31\x01\"#\n\x13\x41\x63\x63\x65ptedUsageRecord\x12\x0c\n\x04uuid\x18\x01 \x01(\t\"\x9d\x02\n\x13RejectedUsageRecord\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12P\n\x06reason\x18\x02 \x01(\x0e\x32@.yandex.cloud.marketplace.v1.metering.RejectedUsageRecord.Reason\"\xa5\x01\n\x06Reason\x12\x16\n\x12REASON_UNSPECIFIED\x10\x00\x12\r\n\tDUPLICATE\x10\x01\x12\x0b\n\x07\x45XPIRED\x10\x02\x12\x15\n\x11INVALID_TIMESTAMP\x10\x03\x12\x12\n\x0eINVALID_SKU_ID\x10\x04\x12\x16\n\x12INVALID_PRODUCT_ID\x10\x05\x12\x14\n\x10INVALID_QUANTITY\x10\x06\x12\x0e\n\nINVALID_ID\x10\x07\x42}\n(yandex.cloud.api.marketplace.v1.meteringZQgithub.com/yandex-cloud/go-genproto/yandex/cloud/marketplace/v1/metering;meteringb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.marketplace.v1.metering.usage_record_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n(yandex.cloud.api.marketplace.v1.meteringZQgithub.com/yandex-cloud/go-genproto/yandex/cloud/marketplace/v1/metering;metering'
  _USAGERECORD.fields_by_name['uuid']._options = None
  _USAGERECORD.fields_by_name['uuid']._serialized_options = b'\350\3071\001\212\3101\004<=36'
  _USAGERECORD.fields_by_name['sku_id']._options = None
  _USAGERECORD.fields_by_name['sku_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _USAGERECORD.fields_by_name['quantity']._options = None
  _USAGERECORD.fields_by_name['quantity']._serialized_options = b'\372\3071\002>0'
  _USAGERECORD.fields_by_name['timestamp']._options = None
  _USAGERECORD.fields_by_name['timestamp']._serialized_options = b'\350\3071\001'
  _globals['_USAGERECORD']._serialized_start=162
  _globals['_USAGERECORD']._serialized_end=312
  _globals['_ACCEPTEDUSAGERECORD']._serialized_start=314
  _globals['_ACCEPTEDUSAGERECORD']._serialized_end=349
  _globals['_REJECTEDUSAGERECORD']._serialized_start=352
  _globals['_REJECTEDUSAGERECORD']._serialized_end=637
  _globals['_REJECTEDUSAGERECORD_REASON']._serialized_start=472
  _globals['_REJECTEDUSAGERECORD_REASON']._serialized_end=637
# @@protoc_insertion_point(module_scope)
