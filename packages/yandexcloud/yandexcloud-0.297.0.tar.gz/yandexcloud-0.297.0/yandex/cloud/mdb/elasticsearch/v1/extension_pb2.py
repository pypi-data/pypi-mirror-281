# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/mdb/elasticsearch/v1/extension.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1yandex/cloud/mdb/elasticsearch/v1/extension.proto\x12!yandex.cloud.mdb.elasticsearch.v1\x1a\x1dyandex/cloud/validation.proto\"Z\n\tExtension\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x12\n\ncluster_id\x18\x03 \x01(\t\x12\x0f\n\x07version\x18\x04 \x01(\x03\x12\x0e\n\x06\x61\x63tive\x18\x05 \x01(\x08\"J\n\rExtensionSpec\x12\x1a\n\x04name\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x0b\n\x03uri\x18\x02 \x01(\t\x12\x10\n\x08\x64isabled\x18\x03 \x01(\x08\x42|\n%yandex.cloud.api.mdb.elasticsearch.v1ZSgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/elasticsearch/v1;elasticsearchb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.mdb.elasticsearch.v1.extension_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n%yandex.cloud.api.mdb.elasticsearch.v1ZSgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/elasticsearch/v1;elasticsearch'
  _EXTENSIONSPEC.fields_by_name['name']._options = None
  _EXTENSIONSPEC.fields_by_name['name']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_EXTENSION']._serialized_start=119
  _globals['_EXTENSION']._serialized_end=209
  _globals['_EXTENSIONSPEC']._serialized_start=211
  _globals['_EXTENSIONSPEC']._serialized_end=285
# @@protoc_insertion_point(module_scope)
