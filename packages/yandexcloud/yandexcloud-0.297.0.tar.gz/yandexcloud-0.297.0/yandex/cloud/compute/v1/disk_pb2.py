# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/compute/v1/disk.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"yandex/cloud/compute/v1/disk.proto\x12\x17yandex.cloud.compute.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"\xeb\x04\n\x04\x44isk\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\tfolder_id\x18\x02 \x01(\t\x12.\n\ncreated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x39\n\x06labels\x18\x06 \x03(\x0b\x32).yandex.cloud.compute.v1.Disk.LabelsEntry\x12\x0f\n\x07type_id\x18\x07 \x01(\t\x12\x0f\n\x07zone_id\x18\x08 \x01(\t\x12\x0c\n\x04size\x18\t \x01(\x03\x12\x12\n\nblock_size\x18\x0f \x01(\x03\x12\x13\n\x0bproduct_ids\x18\n \x03(\t\x12\x34\n\x06status\x18\x0b \x01(\x0e\x32$.yandex.cloud.compute.v1.Disk.Status\x12\x19\n\x0fsource_image_id\x18\x0c \x01(\tH\x00\x12\x1c\n\x12source_snapshot_id\x18\r \x01(\tH\x00\x12\x14\n\x0cinstance_ids\x18\x0e \x03(\t\x12K\n\x15\x64isk_placement_policy\x18\x10 \x01(\x0b\x32,.yandex.cloud.compute.v1.DiskPlacementPolicy\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"R\n\x06Status\x12\x16\n\x12STATUS_UNSPECIFIED\x10\x00\x12\x0c\n\x08\x43REATING\x10\x01\x12\t\n\x05READY\x10\x02\x12\t\n\x05\x45RROR\x10\x03\x12\x0c\n\x08\x44\x45LETING\x10\x04\x42\x08\n\x06source\"T\n\x13\x44iskPlacementPolicy\x12\x1a\n\x12placement_group_id\x18\x01 \x01(\t\x12!\n\x19placement_group_partition\x18\x02 \x01(\x03\"y\n\x19\x44iskPlacementPolicyChange\x12\x0f\n\x07\x64isk_id\x18\x01 \x01(\t\x12K\n\x15\x64isk_placement_policy\x18\x02 \x01(\x0b\x32,.yandex.cloud.compute.v1.DiskPlacementPolicyBb\n\x1byandex.cloud.api.compute.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/compute/v1;computeb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.compute.v1.disk_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\033yandex.cloud.api.compute.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/compute/v1;compute'
  _DISK_LABELSENTRY._options = None
  _DISK_LABELSENTRY._serialized_options = b'8\001'
  _globals['_DISK']._serialized_start=97
  _globals['_DISK']._serialized_end=716
  _globals['_DISK_LABELSENTRY']._serialized_start=577
  _globals['_DISK_LABELSENTRY']._serialized_end=622
  _globals['_DISK_STATUS']._serialized_start=624
  _globals['_DISK_STATUS']._serialized_end=706
  _globals['_DISKPLACEMENTPOLICY']._serialized_start=718
  _globals['_DISKPLACEMENTPOLICY']._serialized_end=802
  _globals['_DISKPLACEMENTPOLICYCHANGE']._serialized_start=804
  _globals['_DISKPLACEMENTPOLICYCHANGE']._serialized_end=925
# @@protoc_insertion_point(module_scope)
