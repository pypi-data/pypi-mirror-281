# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/mdb/mongodb/v1/backup.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(yandex/cloud/mdb/mongodb/v1/backup.proto\x12\x1byandex.cloud.mdb.mongodb.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"\xd0\x02\n\x06\x42\x61\x63kup\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\tfolder_id\x18\x02 \x01(\t\x12.\n\ncreated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x19\n\x11source_cluster_id\x18\x04 \x01(\t\x12.\n\nstarted_at\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1a\n\x12source_shard_names\x18\x06 \x03(\t\x12\x0c\n\x04size\x18\x07 \x01(\x03\x12<\n\x04type\x18\x08 \x01(\x0e\x32..yandex.cloud.mdb.mongodb.v1.Backup.BackupType\"D\n\nBackupType\x12\x1b\n\x17\x42\x41\x43KUP_TYPE_UNSPECIFIED\x10\x00\x12\r\n\tAUTOMATED\x10\x01\x12\n\n\x06MANUAL\x10\x02\x42j\n\x1fyandex.cloud.api.mdb.mongodb.v1ZGgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/mongodb/v1;mongodbb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.mdb.mongodb.v1.backup_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\037yandex.cloud.api.mdb.mongodb.v1ZGgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/mongodb/v1;mongodb'
  _globals['_BACKUP']._serialized_start=107
  _globals['_BACKUP']._serialized_end=443
  _globals['_BACKUP_BACKUPTYPE']._serialized_start=375
  _globals['_BACKUP_BACKUPTYPE']._serialized_end=443
# @@protoc_insertion_point(module_scope)
