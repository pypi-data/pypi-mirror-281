# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/mdb/mongodb/v1/database.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*yandex/cloud/mdb/mongodb/v1/database.proto\x12\x1byandex.cloud.mdb.mongodb.v1\x1a\x1dyandex/cloud/validation.proto\",\n\x08\x44\x61tabase\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x12\n\ncluster_id\x18\x02 \x01(\t\"A\n\x0c\x44\x61tabaseSpec\x12\x31\n\x04name\x18\x01 \x01(\tB#\xe8\xc7\x31\x01\xf2\xc7\x31\x13[a-zA-Z0-9_-]{1,63}\x8a\xc8\x31\x04<=63Bj\n\x1fyandex.cloud.api.mdb.mongodb.v1ZGgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/mongodb/v1;mongodbb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.mdb.mongodb.v1.database_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\037yandex.cloud.api.mdb.mongodb.v1ZGgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/mongodb/v1;mongodb'
  _DATABASESPEC.fields_by_name['name']._options = None
  _DATABASESPEC.fields_by_name['name']._serialized_options = b'\350\3071\001\362\3071\023[a-zA-Z0-9_-]{1,63}\212\3101\004<=63'
  _globals['_DATABASE']._serialized_start=106
  _globals['_DATABASE']._serialized_end=150
  _globals['_DATABASESPEC']._serialized_start=152
  _globals['_DATABASESPEC']._serialized_end=217
# @@protoc_insertion_point(module_scope)
