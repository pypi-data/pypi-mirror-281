# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/compute/v1/image.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#yandex/cloud/compute/v1/image.proto\x12\x17yandex.cloud.compute.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"\xfa\x03\n\x05Image\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\tfolder_id\x18\x02 \x01(\t\x12.\n\ncreated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12:\n\x06labels\x18\x06 \x03(\x0b\x32*.yandex.cloud.compute.v1.Image.LabelsEntry\x12\x0e\n\x06\x66\x61mily\x18\x07 \x01(\t\x12\x14\n\x0cstorage_size\x18\x08 \x01(\x03\x12\x15\n\rmin_disk_size\x18\t \x01(\x03\x12\x13\n\x0bproduct_ids\x18\n \x03(\t\x12\x35\n\x06status\x18\x0b \x01(\x0e\x32%.yandex.cloud.compute.v1.Image.Status\x12\'\n\x02os\x18\x0c \x01(\x0b\x32\x1b.yandex.cloud.compute.v1.Os\x12\x0e\n\x06pooled\x18\r \x01(\x08\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"R\n\x06Status\x12\x16\n\x12STATUS_UNSPECIFIED\x10\x00\x12\x0c\n\x08\x43REATING\x10\x01\x12\t\n\x05READY\x10\x02\x12\t\n\x05\x45RROR\x10\x03\x12\x0c\n\x08\x44\x45LETING\x10\x04\"j\n\x02Os\x12.\n\x04type\x18\x01 \x01(\x0e\x32 .yandex.cloud.compute.v1.Os.Type\"4\n\x04Type\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\t\n\x05LINUX\x10\x01\x12\x0b\n\x07WINDOWS\x10\x02\x42\x62\n\x1byandex.cloud.api.compute.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/compute/v1;computeb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.compute.v1.image_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\033yandex.cloud.api.compute.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/compute/v1;compute'
  _IMAGE_LABELSENTRY._options = None
  _IMAGE_LABELSENTRY._serialized_options = b'8\001'
  _globals['_IMAGE']._serialized_start=98
  _globals['_IMAGE']._serialized_end=604
  _globals['_IMAGE_LABELSENTRY']._serialized_start=475
  _globals['_IMAGE_LABELSENTRY']._serialized_end=520
  _globals['_IMAGE_STATUS']._serialized_start=522
  _globals['_IMAGE_STATUS']._serialized_end=604
  _globals['_OS']._serialized_start=606
  _globals['_OS']._serialized_end=712
  _globals['_OS_TYPE']._serialized_start=660
  _globals['_OS_TYPE']._serialized_end=712
# @@protoc_insertion_point(module_scope)
