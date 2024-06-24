# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/dataproc/v1/subcluster_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2
from yandex.cloud.dataproc.v1 import common_pb2 as yandex_dot_cloud_dot_dataproc_dot_v1_dot_common__pb2
from yandex.cloud.dataproc.v1 import subcluster_pb2 as yandex_dot_cloud_dot_dataproc_dot_v1_dot_subcluster__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2
from yandex.cloud.api import operation_pb2 as yandex_dot_cloud_dot_api_dot_operation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1yandex/cloud/dataproc/v1/subcluster_service.proto\x12\x18yandex.cloud.dataproc.v1\x1a\x1cgoogle/api/annotations.proto\x1a google/protobuf/field_mask.proto\x1a&yandex/cloud/operation/operation.proto\x1a%yandex/cloud/dataproc/v1/common.proto\x1a)yandex/cloud/dataproc/v1/subcluster.proto\x1a\x1dyandex/cloud/validation.proto\x1a yandex/cloud/api/operation.proto\"]\n\x14GetSubclusterRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12#\n\rsubcluster_id\x18\x02 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"\x94\x01\n\x16ListSubclustersRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06<=1000\x12\x1d\n\npage_token\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=100\x12\x1a\n\x06\x66ilter\x18\x04 \x01(\tB\n\x8a\xc8\x31\x06<=1000\"m\n\x17ListSubclustersResponse\x12\x39\n\x0bsubclusters\x18\x01 \x03(\x0b\x32$.yandex.cloud.dataproc.v1.Subcluster\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\xea\x02\n\x17\x43reateSubclusterRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12/\n\x04name\x18\x02 \x01(\tB!\xf2\xc7\x31\x1d|[a-z][-a-z0-9]{1,61}[a-z0-9]\x12\x32\n\x04role\x18\x03 \x01(\x0e\x32\x1e.yandex.cloud.dataproc.v1.RoleB\x04\xe8\xc7\x31\x01\x12<\n\tresources\x18\x04 \x01(\x0b\x32#.yandex.cloud.dataproc.v1.ResourcesB\x04\xe8\xc7\x31\x01\x12\x1f\n\tsubnet_id\x18\x05 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12 \n\x0bhosts_count\x18\x06 \x01(\x03\x42\x0b\xe8\xc7\x31\x01\xfa\xc7\x31\x03>=1\x12G\n\x12\x61utoscaling_config\x18\x07 \x01(\x0b\x32+.yandex.cloud.dataproc.v1.AutoscalingConfig\"Y\n\x18\x43reateSubclusterMetadata\x12\x1c\n\ncluster_id\x18\x01 \x01(\tB\x08\x8a\xc8\x31\x04<=50\x12\x1f\n\rsubcluster_id\x18\x02 \x01(\tB\x08\x8a\xc8\x31\x04<=50\"\x90\x03\n\x17UpdateSubclusterRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12#\n\rsubcluster_id\x18\x02 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12/\n\x0bupdate_mask\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12\x36\n\tresources\x18\x04 \x01(\x0b\x32#.yandex.cloud.dataproc.v1.Resources\x12/\n\x04name\x18\x05 \x01(\tB!\xf2\xc7\x31\x1d|[a-z][-a-z0-9]{1,61}[a-z0-9]\x12 \n\x0bhosts_count\x18\x06 \x01(\x03\x42\x0b\xe8\xc7\x31\x01\xfa\xc7\x31\x03>=1\x12)\n\x14\x64\x65\x63ommission_timeout\x18\x07 \x01(\x03\x42\x0b\xfa\xc7\x31\x07\x30-86400\x12G\n\x12\x61utoscaling_config\x18\x08 \x01(\x0b\x32+.yandex.cloud.dataproc.v1.AutoscalingConfig\"Y\n\x18UpdateSubclusterMetadata\x12\x1c\n\ncluster_id\x18\x01 \x01(\tB\x08\x8a\xc8\x31\x04<=50\x12\x1f\n\rsubcluster_id\x18\x02 \x01(\tB\x08\x8a\xc8\x31\x04<=50\"\x8b\x01\n\x17\x44\x65leteSubclusterRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12#\n\rsubcluster_id\x18\x02 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12)\n\x14\x64\x65\x63ommission_timeout\x18\x03 \x01(\x03\x42\x0b\xfa\xc7\x31\x07\x30-86400\"Y\n\x18\x44\x65leteSubclusterMetadata\x12\x1c\n\ncluster_id\x18\x01 \x01(\tB\x08\x8a\xc8\x31\x04<=50\x12\x1f\n\rsubcluster_id\x18\x02 \x01(\tB\x08\x8a\xc8\x31\x04<=502\xd9\x07\n\x11SubclusterService\x12\xa3\x01\n\x03Get\x12..yandex.cloud.dataproc.v1.GetSubclusterRequest\x1a$.yandex.cloud.dataproc.v1.Subcluster\"F\x82\xd3\xe4\x93\x02@\x12>/dataproc/v1/clusters/{cluster_id}/subclusters/{subcluster_id}\x12\xa3\x01\n\x04List\x12\x30.yandex.cloud.dataproc.v1.ListSubclustersRequest\x1a\x31.yandex.cloud.dataproc.v1.ListSubclustersResponse\"6\x82\xd3\xe4\x93\x02\x30\x12./dataproc/v1/clusters/{cluster_id}/subclusters\x12\xc3\x01\n\x06\x43reate\x12\x31.yandex.cloud.dataproc.v1.CreateSubclusterRequest\x1a!.yandex.cloud.operation.Operation\"c\xb2\xd2*&\n\x18\x43reateSubclusterMetadata\x12\nSubcluster\x82\xd3\xe4\x93\x02\x33\"./dataproc/v1/clusters/{cluster_id}/subclusters:\x01*\x12\xd3\x01\n\x06Update\x12\x31.yandex.cloud.dataproc.v1.UpdateSubclusterRequest\x1a!.yandex.cloud.operation.Operation\"s\xb2\xd2*&\n\x18UpdateSubclusterMetadata\x12\nSubcluster\x82\xd3\xe4\x93\x02\x43\x32>/dataproc/v1/clusters/{cluster_id}/subclusters/{subcluster_id}:\x01*\x12\xdb\x01\n\x06\x44\x65lete\x12\x31.yandex.cloud.dataproc.v1.DeleteSubclusterRequest\x1a!.yandex.cloud.operation.Operation\"{\xb2\xd2*1\n\x18\x44\x65leteSubclusterMetadata\x12\x15google.protobuf.Empty\x82\xd3\xe4\x93\x02@*>/dataproc/v1/clusters/{cluster_id}/subclusters/{subcluster_id}Be\n\x1cyandex.cloud.api.dataproc.v1ZEgithub.com/yandex-cloud/go-genproto/yandex/cloud/dataproc/v1;dataprocb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.dataproc.v1.subcluster_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\034yandex.cloud.api.dataproc.v1ZEgithub.com/yandex-cloud/go-genproto/yandex/cloud/dataproc/v1;dataproc'
  _GETSUBCLUSTERREQUEST.fields_by_name['cluster_id']._options = None
  _GETSUBCLUSTERREQUEST.fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _GETSUBCLUSTERREQUEST.fields_by_name['subcluster_id']._options = None
  _GETSUBCLUSTERREQUEST.fields_by_name['subcluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _LISTSUBCLUSTERSREQUEST.fields_by_name['cluster_id']._options = None
  _LISTSUBCLUSTERSREQUEST.fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _LISTSUBCLUSTERSREQUEST.fields_by_name['page_size']._options = None
  _LISTSUBCLUSTERSREQUEST.fields_by_name['page_size']._serialized_options = b'\372\3071\006<=1000'
  _LISTSUBCLUSTERSREQUEST.fields_by_name['page_token']._options = None
  _LISTSUBCLUSTERSREQUEST.fields_by_name['page_token']._serialized_options = b'\212\3101\005<=100'
  _LISTSUBCLUSTERSREQUEST.fields_by_name['filter']._options = None
  _LISTSUBCLUSTERSREQUEST.fields_by_name['filter']._serialized_options = b'\212\3101\006<=1000'
  _CREATESUBCLUSTERREQUEST.fields_by_name['cluster_id']._options = None
  _CREATESUBCLUSTERREQUEST.fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _CREATESUBCLUSTERREQUEST.fields_by_name['name']._options = None
  _CREATESUBCLUSTERREQUEST.fields_by_name['name']._serialized_options = b'\362\3071\035|[a-z][-a-z0-9]{1,61}[a-z0-9]'
  _CREATESUBCLUSTERREQUEST.fields_by_name['role']._options = None
  _CREATESUBCLUSTERREQUEST.fields_by_name['role']._serialized_options = b'\350\3071\001'
  _CREATESUBCLUSTERREQUEST.fields_by_name['resources']._options = None
  _CREATESUBCLUSTERREQUEST.fields_by_name['resources']._serialized_options = b'\350\3071\001'
  _CREATESUBCLUSTERREQUEST.fields_by_name['subnet_id']._options = None
  _CREATESUBCLUSTERREQUEST.fields_by_name['subnet_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _CREATESUBCLUSTERREQUEST.fields_by_name['hosts_count']._options = None
  _CREATESUBCLUSTERREQUEST.fields_by_name['hosts_count']._serialized_options = b'\350\3071\001\372\3071\003>=1'
  _CREATESUBCLUSTERMETADATA.fields_by_name['cluster_id']._options = None
  _CREATESUBCLUSTERMETADATA.fields_by_name['cluster_id']._serialized_options = b'\212\3101\004<=50'
  _CREATESUBCLUSTERMETADATA.fields_by_name['subcluster_id']._options = None
  _CREATESUBCLUSTERMETADATA.fields_by_name['subcluster_id']._serialized_options = b'\212\3101\004<=50'
  _UPDATESUBCLUSTERREQUEST.fields_by_name['cluster_id']._options = None
  _UPDATESUBCLUSTERREQUEST.fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _UPDATESUBCLUSTERREQUEST.fields_by_name['subcluster_id']._options = None
  _UPDATESUBCLUSTERREQUEST.fields_by_name['subcluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _UPDATESUBCLUSTERREQUEST.fields_by_name['name']._options = None
  _UPDATESUBCLUSTERREQUEST.fields_by_name['name']._serialized_options = b'\362\3071\035|[a-z][-a-z0-9]{1,61}[a-z0-9]'
  _UPDATESUBCLUSTERREQUEST.fields_by_name['hosts_count']._options = None
  _UPDATESUBCLUSTERREQUEST.fields_by_name['hosts_count']._serialized_options = b'\350\3071\001\372\3071\003>=1'
  _UPDATESUBCLUSTERREQUEST.fields_by_name['decommission_timeout']._options = None
  _UPDATESUBCLUSTERREQUEST.fields_by_name['decommission_timeout']._serialized_options = b'\372\3071\0070-86400'
  _UPDATESUBCLUSTERMETADATA.fields_by_name['cluster_id']._options = None
  _UPDATESUBCLUSTERMETADATA.fields_by_name['cluster_id']._serialized_options = b'\212\3101\004<=50'
  _UPDATESUBCLUSTERMETADATA.fields_by_name['subcluster_id']._options = None
  _UPDATESUBCLUSTERMETADATA.fields_by_name['subcluster_id']._serialized_options = b'\212\3101\004<=50'
  _DELETESUBCLUSTERREQUEST.fields_by_name['cluster_id']._options = None
  _DELETESUBCLUSTERREQUEST.fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _DELETESUBCLUSTERREQUEST.fields_by_name['subcluster_id']._options = None
  _DELETESUBCLUSTERREQUEST.fields_by_name['subcluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _DELETESUBCLUSTERREQUEST.fields_by_name['decommission_timeout']._options = None
  _DELETESUBCLUSTERREQUEST.fields_by_name['decommission_timeout']._serialized_options = b'\372\3071\0070-86400'
  _DELETESUBCLUSTERMETADATA.fields_by_name['cluster_id']._options = None
  _DELETESUBCLUSTERMETADATA.fields_by_name['cluster_id']._serialized_options = b'\212\3101\004<=50'
  _DELETESUBCLUSTERMETADATA.fields_by_name['subcluster_id']._options = None
  _DELETESUBCLUSTERMETADATA.fields_by_name['subcluster_id']._serialized_options = b'\212\3101\004<=50'
  _SUBCLUSTERSERVICE.methods_by_name['Get']._options = None
  _SUBCLUSTERSERVICE.methods_by_name['Get']._serialized_options = b'\202\323\344\223\002@\022>/dataproc/v1/clusters/{cluster_id}/subclusters/{subcluster_id}'
  _SUBCLUSTERSERVICE.methods_by_name['List']._options = None
  _SUBCLUSTERSERVICE.methods_by_name['List']._serialized_options = b'\202\323\344\223\0020\022./dataproc/v1/clusters/{cluster_id}/subclusters'
  _SUBCLUSTERSERVICE.methods_by_name['Create']._options = None
  _SUBCLUSTERSERVICE.methods_by_name['Create']._serialized_options = b'\262\322*&\n\030CreateSubclusterMetadata\022\nSubcluster\202\323\344\223\0023\"./dataproc/v1/clusters/{cluster_id}/subclusters:\001*'
  _SUBCLUSTERSERVICE.methods_by_name['Update']._options = None
  _SUBCLUSTERSERVICE.methods_by_name['Update']._serialized_options = b'\262\322*&\n\030UpdateSubclusterMetadata\022\nSubcluster\202\323\344\223\002C2>/dataproc/v1/clusters/{cluster_id}/subclusters/{subcluster_id}:\001*'
  _SUBCLUSTERSERVICE.methods_by_name['Delete']._options = None
  _SUBCLUSTERSERVICE.methods_by_name['Delete']._serialized_options = b'\262\322*1\n\030DeleteSubclusterMetadata\022\025google.protobuf.Empty\202\323\344\223\002@*>/dataproc/v1/clusters/{cluster_id}/subclusters/{subcluster_id}'
  _globals['_GETSUBCLUSTERREQUEST']._serialized_start=330
  _globals['_GETSUBCLUSTERREQUEST']._serialized_end=423
  _globals['_LISTSUBCLUSTERSREQUEST']._serialized_start=426
  _globals['_LISTSUBCLUSTERSREQUEST']._serialized_end=574
  _globals['_LISTSUBCLUSTERSRESPONSE']._serialized_start=576
  _globals['_LISTSUBCLUSTERSRESPONSE']._serialized_end=685
  _globals['_CREATESUBCLUSTERREQUEST']._serialized_start=688
  _globals['_CREATESUBCLUSTERREQUEST']._serialized_end=1050
  _globals['_CREATESUBCLUSTERMETADATA']._serialized_start=1052
  _globals['_CREATESUBCLUSTERMETADATA']._serialized_end=1141
  _globals['_UPDATESUBCLUSTERREQUEST']._serialized_start=1144
  _globals['_UPDATESUBCLUSTERREQUEST']._serialized_end=1544
  _globals['_UPDATESUBCLUSTERMETADATA']._serialized_start=1546
  _globals['_UPDATESUBCLUSTERMETADATA']._serialized_end=1635
  _globals['_DELETESUBCLUSTERREQUEST']._serialized_start=1638
  _globals['_DELETESUBCLUSTERREQUEST']._serialized_end=1777
  _globals['_DELETESUBCLUSTERMETADATA']._serialized_start=1779
  _globals['_DELETESUBCLUSTERMETADATA']._serialized_end=1868
  _globals['_SUBCLUSTERSERVICE']._serialized_start=1871
  _globals['_SUBCLUSTERSERVICE']._serialized_end=2856
# @@protoc_insertion_point(module_scope)
