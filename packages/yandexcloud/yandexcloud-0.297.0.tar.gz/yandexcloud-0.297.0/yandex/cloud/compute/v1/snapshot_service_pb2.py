# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/compute/v1/snapshot_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from yandex.cloud.access import access_pb2 as yandex_dot_cloud_dot_access_dot_access__pb2
from yandex.cloud.api import operation_pb2 as yandex_dot_cloud_dot_api_dot_operation__pb2
from yandex.cloud.compute.v1 import snapshot_pb2 as yandex_dot_cloud_dot_compute_dot_v1_dot_snapshot__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.yandex/cloud/compute/v1/snapshot_service.proto\x12\x17yandex.cloud.compute.v1\x1a\x1cgoogle/api/annotations.proto\x1a google/protobuf/field_mask.proto\x1a yandex/cloud/access/access.proto\x1a yandex/cloud/api/operation.proto\x1a&yandex/cloud/compute/v1/snapshot.proto\x1a&yandex/cloud/operation/operation.proto\x1a\x1dyandex/cloud/validation.proto\"7\n\x12GetSnapshotRequest\x12!\n\x0bsnapshot_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"\xae\x01\n\x14ListSnapshotsRequest\x12\x1f\n\tfolder_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06<=1000\x12\x1d\n\npage_token\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=100\x12\x1a\n\x06\x66ilter\x18\x04 \x01(\tB\n\x8a\xc8\x31\x06<=1000\x12\x1b\n\x08order_by\x18\x05 \x01(\tB\t\x8a\xc8\x31\x05<=100\"f\n\x15ListSnapshotsResponse\x12\x34\n\tsnapshots\x18\x01 \x03(\x0b\x32!.yandex.cloud.compute.v1.Snapshot\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\xf2\x02\n\x15\x43reateSnapshotRequest\x12\x1f\n\tfolder_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\x07\x64isk_id\x18\x02 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x32\n\x04name\x18\x03 \x01(\tB$\xf2\xc7\x31 |[a-z]([-a-z0-9]{0,61}[a-z0-9])?\x12\x1e\n\x0b\x64\x65scription\x18\x04 \x01(\tB\t\x8a\xc8\x31\x05<=256\x12\x8f\x01\n\x06labels\x18\x06 \x03(\x0b\x32:.yandex.cloud.compute.v1.CreateSnapshotRequest.LabelsEntryBC\xf2\xc7\x31\x0f[-_./\\@0-9a-z]*\x82\xc8\x31\x04<=64\x8a\xc8\x31\x04<=63\xb2\xc8\x31\x1c\x12\x14[a-z][-_./\\@0-9a-z]*\x1a\x04\x31-63\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01J\x04\x08\x05\x10\x06\">\n\x16\x43reateSnapshotMetadata\x12\x13\n\x0bsnapshot_id\x18\x01 \x01(\t\x12\x0f\n\x07\x64isk_id\x18\x02 \x01(\t\"\x80\x03\n\x15UpdateSnapshotRequest\x12!\n\x0bsnapshot_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12\x32\n\x04name\x18\x03 \x01(\tB$\xf2\xc7\x31 |[a-z]([-a-z0-9]{0,61}[a-z0-9])?\x12\x1e\n\x0b\x64\x65scription\x18\x04 \x01(\tB\t\x8a\xc8\x31\x05<=256\x12\x8f\x01\n\x06labels\x18\x05 \x03(\x0b\x32:.yandex.cloud.compute.v1.UpdateSnapshotRequest.LabelsEntryBC\xf2\xc7\x31\x0f[-_./\\@0-9a-z]*\x82\xc8\x31\x04<=64\x8a\xc8\x31\x04<=63\xb2\xc8\x31\x1c\x12\x14[a-z][-_./\\@0-9a-z]*\x1a\x04\x31-63\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"-\n\x16UpdateSnapshotMetadata\x12\x13\n\x0bsnapshot_id\x18\x01 \x01(\t\":\n\x15\x44\x65leteSnapshotRequest\x12!\n\x0bsnapshot_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"-\n\x16\x44\x65leteSnapshotMetadata\x12\x13\n\x0bsnapshot_id\x18\x01 \x01(\t\"\x80\x01\n\x1dListSnapshotOperationsRequest\x12!\n\x0bsnapshot_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06<=1000\x12\x1d\n\npage_token\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=100\"p\n\x1eListSnapshotOperationsResponse\x12\x35\n\noperations\x18\x01 \x03(\x0b\x32!.yandex.cloud.operation.Operation\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t2\xa3\r\n\x0fSnapshotService\x12\x82\x01\n\x03Get\x12+.yandex.cloud.compute.v1.GetSnapshotRequest\x1a!.yandex.cloud.compute.v1.Snapshot\"+\x82\xd3\xe4\x93\x02%\x12#/compute/v1/snapshots/{snapshot_id}\x12\x84\x01\n\x04List\x12-.yandex.cloud.compute.v1.ListSnapshotsRequest\x1a..yandex.cloud.compute.v1.ListSnapshotsResponse\"\x1d\x82\xd3\xe4\x93\x02\x17\x12\x15/compute/v1/snapshots\x12\xa3\x01\n\x06\x43reate\x12..yandex.cloud.compute.v1.CreateSnapshotRequest\x1a!.yandex.cloud.operation.Operation\"F\xb2\xd2*\"\n\x16\x43reateSnapshotMetadata\x12\x08Snapshot\x82\xd3\xe4\x93\x02\x1a\"\x15/compute/v1/snapshots:\x01*\x12\xb1\x01\n\x06Update\x12..yandex.cloud.compute.v1.UpdateSnapshotRequest\x1a!.yandex.cloud.operation.Operation\"T\xb2\xd2*\"\n\x16UpdateSnapshotMetadata\x12\x08Snapshot\x82\xd3\xe4\x93\x02(2#/compute/v1/snapshots/{snapshot_id}:\x01*\x12\xbb\x01\n\x06\x44\x65lete\x12..yandex.cloud.compute.v1.DeleteSnapshotRequest\x1a!.yandex.cloud.operation.Operation\"^\xb2\xd2*/\n\x16\x44\x65leteSnapshotMetadata\x12\x15google.protobuf.Empty\x82\xd3\xe4\x93\x02%*#/compute/v1/snapshots/{snapshot_id}\x12\xb9\x01\n\x0eListOperations\x12\x36.yandex.cloud.compute.v1.ListSnapshotOperationsRequest\x1a\x37.yandex.cloud.compute.v1.ListSnapshotOperationsResponse\"6\x82\xd3\xe4\x93\x02\x30\x12./compute/v1/snapshots/{snapshot_id}/operations\x12\xb5\x01\n\x12ListAccessBindings\x12..yandex.cloud.access.ListAccessBindingsRequest\x1a/.yandex.cloud.access.ListAccessBindingsResponse\">\x82\xd3\xe4\x93\x02\x38\x12\x36/compute/v1/snapshots/{resource_id}:listAccessBindings\x12\xf4\x01\n\x11SetAccessBindings\x12-.yandex.cloud.access.SetAccessBindingsRequest\x1a!.yandex.cloud.operation.Operation\"\x8c\x01\xb2\xd2*H\n access.SetAccessBindingsMetadata\x12$access.AccessBindingsOperationResult\x82\xd3\xe4\x93\x02:\"5/compute/v1/snapshots/{resource_id}:setAccessBindings:\x01*\x12\x80\x02\n\x14UpdateAccessBindings\x12\x30.yandex.cloud.access.UpdateAccessBindingsRequest\x1a!.yandex.cloud.operation.Operation\"\x92\x01\xb2\xd2*K\n#access.UpdateAccessBindingsMetadata\x12$access.AccessBindingsOperationResult\x82\xd3\xe4\x93\x02=\"8/compute/v1/snapshots/{resource_id}:updateAccessBindings:\x01*Bb\n\x1byandex.cloud.api.compute.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/compute/v1;computeb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.compute.v1.snapshot_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\033yandex.cloud.api.compute.v1ZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/compute/v1;compute'
  _GETSNAPSHOTREQUEST.fields_by_name['snapshot_id']._options = None
  _GETSNAPSHOTREQUEST.fields_by_name['snapshot_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _LISTSNAPSHOTSREQUEST.fields_by_name['folder_id']._options = None
  _LISTSNAPSHOTSREQUEST.fields_by_name['folder_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _LISTSNAPSHOTSREQUEST.fields_by_name['page_size']._options = None
  _LISTSNAPSHOTSREQUEST.fields_by_name['page_size']._serialized_options = b'\372\3071\006<=1000'
  _LISTSNAPSHOTSREQUEST.fields_by_name['page_token']._options = None
  _LISTSNAPSHOTSREQUEST.fields_by_name['page_token']._serialized_options = b'\212\3101\005<=100'
  _LISTSNAPSHOTSREQUEST.fields_by_name['filter']._options = None
  _LISTSNAPSHOTSREQUEST.fields_by_name['filter']._serialized_options = b'\212\3101\006<=1000'
  _LISTSNAPSHOTSREQUEST.fields_by_name['order_by']._options = None
  _LISTSNAPSHOTSREQUEST.fields_by_name['order_by']._serialized_options = b'\212\3101\005<=100'
  _CREATESNAPSHOTREQUEST_LABELSENTRY._options = None
  _CREATESNAPSHOTREQUEST_LABELSENTRY._serialized_options = b'8\001'
  _CREATESNAPSHOTREQUEST.fields_by_name['folder_id']._options = None
  _CREATESNAPSHOTREQUEST.fields_by_name['folder_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _CREATESNAPSHOTREQUEST.fields_by_name['disk_id']._options = None
  _CREATESNAPSHOTREQUEST.fields_by_name['disk_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _CREATESNAPSHOTREQUEST.fields_by_name['name']._options = None
  _CREATESNAPSHOTREQUEST.fields_by_name['name']._serialized_options = b'\362\3071 |[a-z]([-a-z0-9]{0,61}[a-z0-9])?'
  _CREATESNAPSHOTREQUEST.fields_by_name['description']._options = None
  _CREATESNAPSHOTREQUEST.fields_by_name['description']._serialized_options = b'\212\3101\005<=256'
  _CREATESNAPSHOTREQUEST.fields_by_name['labels']._options = None
  _CREATESNAPSHOTREQUEST.fields_by_name['labels']._serialized_options = b'\362\3071\017[-_./\\@0-9a-z]*\202\3101\004<=64\212\3101\004<=63\262\3101\034\022\024[a-z][-_./\\@0-9a-z]*\032\0041-63'
  _UPDATESNAPSHOTREQUEST_LABELSENTRY._options = None
  _UPDATESNAPSHOTREQUEST_LABELSENTRY._serialized_options = b'8\001'
  _UPDATESNAPSHOTREQUEST.fields_by_name['snapshot_id']._options = None
  _UPDATESNAPSHOTREQUEST.fields_by_name['snapshot_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _UPDATESNAPSHOTREQUEST.fields_by_name['name']._options = None
  _UPDATESNAPSHOTREQUEST.fields_by_name['name']._serialized_options = b'\362\3071 |[a-z]([-a-z0-9]{0,61}[a-z0-9])?'
  _UPDATESNAPSHOTREQUEST.fields_by_name['description']._options = None
  _UPDATESNAPSHOTREQUEST.fields_by_name['description']._serialized_options = b'\212\3101\005<=256'
  _UPDATESNAPSHOTREQUEST.fields_by_name['labels']._options = None
  _UPDATESNAPSHOTREQUEST.fields_by_name['labels']._serialized_options = b'\362\3071\017[-_./\\@0-9a-z]*\202\3101\004<=64\212\3101\004<=63\262\3101\034\022\024[a-z][-_./\\@0-9a-z]*\032\0041-63'
  _DELETESNAPSHOTREQUEST.fields_by_name['snapshot_id']._options = None
  _DELETESNAPSHOTREQUEST.fields_by_name['snapshot_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _LISTSNAPSHOTOPERATIONSREQUEST.fields_by_name['snapshot_id']._options = None
  _LISTSNAPSHOTOPERATIONSREQUEST.fields_by_name['snapshot_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _LISTSNAPSHOTOPERATIONSREQUEST.fields_by_name['page_size']._options = None
  _LISTSNAPSHOTOPERATIONSREQUEST.fields_by_name['page_size']._serialized_options = b'\372\3071\006<=1000'
  _LISTSNAPSHOTOPERATIONSREQUEST.fields_by_name['page_token']._options = None
  _LISTSNAPSHOTOPERATIONSREQUEST.fields_by_name['page_token']._serialized_options = b'\212\3101\005<=100'
  _SNAPSHOTSERVICE.methods_by_name['Get']._options = None
  _SNAPSHOTSERVICE.methods_by_name['Get']._serialized_options = b'\202\323\344\223\002%\022#/compute/v1/snapshots/{snapshot_id}'
  _SNAPSHOTSERVICE.methods_by_name['List']._options = None
  _SNAPSHOTSERVICE.methods_by_name['List']._serialized_options = b'\202\323\344\223\002\027\022\025/compute/v1/snapshots'
  _SNAPSHOTSERVICE.methods_by_name['Create']._options = None
  _SNAPSHOTSERVICE.methods_by_name['Create']._serialized_options = b'\262\322*\"\n\026CreateSnapshotMetadata\022\010Snapshot\202\323\344\223\002\032\"\025/compute/v1/snapshots:\001*'
  _SNAPSHOTSERVICE.methods_by_name['Update']._options = None
  _SNAPSHOTSERVICE.methods_by_name['Update']._serialized_options = b'\262\322*\"\n\026UpdateSnapshotMetadata\022\010Snapshot\202\323\344\223\002(2#/compute/v1/snapshots/{snapshot_id}:\001*'
  _SNAPSHOTSERVICE.methods_by_name['Delete']._options = None
  _SNAPSHOTSERVICE.methods_by_name['Delete']._serialized_options = b'\262\322*/\n\026DeleteSnapshotMetadata\022\025google.protobuf.Empty\202\323\344\223\002%*#/compute/v1/snapshots/{snapshot_id}'
  _SNAPSHOTSERVICE.methods_by_name['ListOperations']._options = None
  _SNAPSHOTSERVICE.methods_by_name['ListOperations']._serialized_options = b'\202\323\344\223\0020\022./compute/v1/snapshots/{snapshot_id}/operations'
  _SNAPSHOTSERVICE.methods_by_name['ListAccessBindings']._options = None
  _SNAPSHOTSERVICE.methods_by_name['ListAccessBindings']._serialized_options = b'\202\323\344\223\0028\0226/compute/v1/snapshots/{resource_id}:listAccessBindings'
  _SNAPSHOTSERVICE.methods_by_name['SetAccessBindings']._options = None
  _SNAPSHOTSERVICE.methods_by_name['SetAccessBindings']._serialized_options = b'\262\322*H\n access.SetAccessBindingsMetadata\022$access.AccessBindingsOperationResult\202\323\344\223\002:\"5/compute/v1/snapshots/{resource_id}:setAccessBindings:\001*'
  _SNAPSHOTSERVICE.methods_by_name['UpdateAccessBindings']._options = None
  _SNAPSHOTSERVICE.methods_by_name['UpdateAccessBindings']._serialized_options = b'\262\322*K\n#access.UpdateAccessBindingsMetadata\022$access.AccessBindingsOperationResult\202\323\344\223\002=\"8/compute/v1/snapshots/{resource_id}:updateAccessBindings:\001*'
  _globals['_GETSNAPSHOTREQUEST']._serialized_start=318
  _globals['_GETSNAPSHOTREQUEST']._serialized_end=373
  _globals['_LISTSNAPSHOTSREQUEST']._serialized_start=376
  _globals['_LISTSNAPSHOTSREQUEST']._serialized_end=550
  _globals['_LISTSNAPSHOTSRESPONSE']._serialized_start=552
  _globals['_LISTSNAPSHOTSRESPONSE']._serialized_end=654
  _globals['_CREATESNAPSHOTREQUEST']._serialized_start=657
  _globals['_CREATESNAPSHOTREQUEST']._serialized_end=1027
  _globals['_CREATESNAPSHOTREQUEST_LABELSENTRY']._serialized_start=976
  _globals['_CREATESNAPSHOTREQUEST_LABELSENTRY']._serialized_end=1021
  _globals['_CREATESNAPSHOTMETADATA']._serialized_start=1029
  _globals['_CREATESNAPSHOTMETADATA']._serialized_end=1091
  _globals['_UPDATESNAPSHOTREQUEST']._serialized_start=1094
  _globals['_UPDATESNAPSHOTREQUEST']._serialized_end=1478
  _globals['_UPDATESNAPSHOTREQUEST_LABELSENTRY']._serialized_start=976
  _globals['_UPDATESNAPSHOTREQUEST_LABELSENTRY']._serialized_end=1021
  _globals['_UPDATESNAPSHOTMETADATA']._serialized_start=1480
  _globals['_UPDATESNAPSHOTMETADATA']._serialized_end=1525
  _globals['_DELETESNAPSHOTREQUEST']._serialized_start=1527
  _globals['_DELETESNAPSHOTREQUEST']._serialized_end=1585
  _globals['_DELETESNAPSHOTMETADATA']._serialized_start=1587
  _globals['_DELETESNAPSHOTMETADATA']._serialized_end=1632
  _globals['_LISTSNAPSHOTOPERATIONSREQUEST']._serialized_start=1635
  _globals['_LISTSNAPSHOTOPERATIONSREQUEST']._serialized_end=1763
  _globals['_LISTSNAPSHOTOPERATIONSRESPONSE']._serialized_start=1765
  _globals['_LISTSNAPSHOTOPERATIONSRESPONSE']._serialized_end=1877
  _globals['_SNAPSHOTSERVICE']._serialized_start=1880
  _globals['_SNAPSHOTSERVICE']._serialized_end=3579
# @@protoc_insertion_point(module_scope)
