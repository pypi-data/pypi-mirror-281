# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/billing/v1/sku.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!yandex/cloud/billing/v1/sku.proto\x12\x17yandex.cloud.billing.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"\xa1\x01\n\x03Sku\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x12\n\nservice_id\x18\x04 \x01(\t\x12\x14\n\x0cpricing_unit\x18\x05 \x01(\t\x12\x41\n\x10pricing_versions\x18\x06 \x03(\x0b\x32\'.yandex.cloud.billing.v1.PricingVersion\"\xc8\x01\n\x0ePricingVersion\x12\x39\n\x04type\x18\x01 \x01(\x0e\x32+.yandex.cloud.billing.v1.PricingVersionType\x12\x32\n\x0e\x65\x66\x66\x65\x63tive_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12G\n\x13pricing_expressions\x18\x03 \x03(\x0b\x32*.yandex.cloud.billing.v1.PricingExpression\"A\n\x11PricingExpression\x12,\n\x05rates\x18\x02 \x03(\x0b\x32\x1d.yandex.cloud.billing.v1.Rate\"L\n\x04Rate\x12\x1e\n\x16start_pricing_quantity\x18\x01 \x01(\t\x12\x12\n\nunit_price\x18\x02 \x01(\t\x12\x10\n\x08\x63urrency\x18\x03 \x01(\t*`\n\x12PricingVersionType\x12$\n PRICING_VERSION_TYPE_UNSPECIFIED\x10\x00\x12\x10\n\x0cSTREET_PRICE\x10\x01\x12\x12\n\x0e\x43ONTRACT_PRICE\x10\x02\x42\x62\n\x1byandex.cloud.api.billing.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/billing/v1;billingb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.billing.v1.sku_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\033yandex.cloud.api.billing.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/billing/v1;billing'
  _globals['_PRICINGVERSIONTYPE']._serialized_start=607
  _globals['_PRICINGVERSIONTYPE']._serialized_end=703
  _globals['_SKU']._serialized_start=96
  _globals['_SKU']._serialized_end=257
  _globals['_PRICINGVERSION']._serialized_start=260
  _globals['_PRICINGVERSION']._serialized_end=460
  _globals['_PRICINGEXPRESSION']._serialized_start=462
  _globals['_PRICINGEXPRESSION']._serialized_end=527
  _globals['_RATE']._serialized_start=529
  _globals['_RATE']._serialized_end=605
# @@protoc_insertion_point(module_scope)
