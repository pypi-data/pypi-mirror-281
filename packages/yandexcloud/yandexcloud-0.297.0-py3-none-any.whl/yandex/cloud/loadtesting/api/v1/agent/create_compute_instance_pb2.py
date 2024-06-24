# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/loadtesting/api/v1/agent/create_compute_instance.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from yandex.cloud.compute.v1 import instance_service_pb2 as yandex_dot_cloud_dot_compute_dot_v1_dot_instance__service__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nCyandex/cloud/loadtesting/api/v1/agent/create_compute_instance.proto\x12%yandex.cloud.loadtesting.api.v1.agent\x1a.yandex/cloud/compute/v1/instance_service.proto\x1a\x1dyandex/cloud/validation.proto\"\xbd\x05\n\x15\x43reateComputeInstance\x12\x9d\x01\n\x06labels\x18\x04 \x03(\x0b\x32H.yandex.cloud.loadtesting.api.v1.agent.CreateComputeInstance.LabelsEntryBC\xf2\xc7\x31\x0f[-_./\\@0-9a-z]*\x82\xc8\x31\x04<=64\x8a\xc8\x31\x04<=63\xb2\xc8\x31\x1c\x12\x14[a-z][-_./\\@0-9a-z]*\x1a\x04\x31-63\x12\x1d\n\x07zone_id\x18\x05 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x44\n\x0eresources_spec\x18\x07 \x01(\x0b\x32&.yandex.cloud.compute.v1.ResourcesSpecB\x04\xe8\xc7\x31\x01\x12\\\n\x08metadata\x18\x08 \x03(\x0b\x32J.yandex.cloud.loadtesting.api.v1.agent.CreateComputeInstance.MetadataEntry\x12G\n\x0e\x62oot_disk_spec\x18\t \x01(\x0b\x32).yandex.cloud.compute.v1.AttachedDiskSpecB\x04\xe8\xc7\x31\x01\x12U\n\x17network_interface_specs\x18\x0b \x03(\x0b\x32-.yandex.cloud.compute.v1.NetworkInterfaceSpecB\x05\x82\xc8\x31\x01\x31\x12\x1a\n\x12service_account_id\x18\x0e \x01(\t\x12\x13\n\x0bplatform_id\x18\x0f \x01(\t\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01J\x04\x08\n\x10\x0bJ\x04\x08\x0c\x10\x0eJ\x04\x08\x06\x10\x07\x42|\n)yandex.cloud.api.loadtesting.api.v1.agentZOgithub.com/yandex-cloud/go-genproto/yandex/cloud/loadtesting/api/v1/agent;agentb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.loadtesting.api.v1.agent.create_compute_instance_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n)yandex.cloud.api.loadtesting.api.v1.agentZOgithub.com/yandex-cloud/go-genproto/yandex/cloud/loadtesting/api/v1/agent;agent'
  _CREATECOMPUTEINSTANCE_LABELSENTRY._options = None
  _CREATECOMPUTEINSTANCE_LABELSENTRY._serialized_options = b'8\001'
  _CREATECOMPUTEINSTANCE_METADATAENTRY._options = None
  _CREATECOMPUTEINSTANCE_METADATAENTRY._serialized_options = b'8\001'
  _CREATECOMPUTEINSTANCE.fields_by_name['labels']._options = None
  _CREATECOMPUTEINSTANCE.fields_by_name['labels']._serialized_options = b'\362\3071\017[-_./\\@0-9a-z]*\202\3101\004<=64\212\3101\004<=63\262\3101\034\022\024[a-z][-_./\\@0-9a-z]*\032\0041-63'
  _CREATECOMPUTEINSTANCE.fields_by_name['zone_id']._options = None
  _CREATECOMPUTEINSTANCE.fields_by_name['zone_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _CREATECOMPUTEINSTANCE.fields_by_name['resources_spec']._options = None
  _CREATECOMPUTEINSTANCE.fields_by_name['resources_spec']._serialized_options = b'\350\3071\001'
  _CREATECOMPUTEINSTANCE.fields_by_name['boot_disk_spec']._options = None
  _CREATECOMPUTEINSTANCE.fields_by_name['boot_disk_spec']._serialized_options = b'\350\3071\001'
  _CREATECOMPUTEINSTANCE.fields_by_name['network_interface_specs']._options = None
  _CREATECOMPUTEINSTANCE.fields_by_name['network_interface_specs']._serialized_options = b'\202\3101\0011'
  _globals['_CREATECOMPUTEINSTANCE']._serialized_start=190
  _globals['_CREATECOMPUTEINSTANCE']._serialized_end=891
  _globals['_CREATECOMPUTEINSTANCE_LABELSENTRY']._serialized_start=779
  _globals['_CREATECOMPUTEINSTANCE_LABELSENTRY']._serialized_end=824
  _globals['_CREATECOMPUTEINSTANCE_METADATAENTRY']._serialized_start=826
  _globals['_CREATECOMPUTEINSTANCE_METADATAENTRY']._serialized_end=873
# @@protoc_insertion_point(module_scope)
