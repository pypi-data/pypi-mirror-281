# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/mdb/greenplum/v1/pxf_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from yandex.cloud.api import operation_pb2 as yandex_dot_cloud_dot_api_dot_operation__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2
from yandex.cloud.mdb.greenplum.v1 import pxf_pb2 as yandex_dot_cloud_dot_mdb_dot_greenplum_dot_v1_dot_pxf__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/yandex/cloud/mdb/greenplum/v1/pxf_service.proto\x12\x1dyandex.cloud.mdb.greenplum.v1\x1a\x1cgoogle/api/annotations.proto\x1a google/protobuf/field_mask.proto\x1a yandex/cloud/api/operation.proto\x1a\x1dyandex/cloud/validation.proto\x1a&yandex/cloud/operation/operation.proto\x1a\'yandex/cloud/mdb/greenplum/v1/pxf.proto\"}\n\x1b\x43reatePXFDatasourceMetadata\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12<\n\x0f\x64\x61tasource_name\x18\x02 \x01(\tB#\xe8\xc7\x31\x01\xf2\xc7\x31\x12^[^\\|/*?.,;\"\'<>]+$\x8a\xc8\x31\x05\x33-200\"}\n\x1bUpdatePXFDatasourceMetadata\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12<\n\x0f\x64\x61tasource_name\x18\x02 \x01(\tB#\xe8\xc7\x31\x01\xf2\xc7\x31\x12^[^\\|/*?.,;\"\'<>]+$\x8a\xc8\x31\x05\x33-200\"}\n\x1b\x44\x65letePXFDatasourceMetadata\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12<\n\x0f\x64\x61tasource_name\x18\x02 \x01(\tB#\xe8\xc7\x31\x01\xf2\xc7\x31\x12^[^\\|/*?.,;\"\'<>]+$\x8a\xc8\x31\x05\x33-200\"=\n\x19ListPXFDatasourcesRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"_\n\x1aListPXFDatasourcesResponse\x12\x41\n\x0b\x64\x61tasources\x18\x01 \x03(\x0b\x32,.yandex.cloud.mdb.greenplum.v1.PXFDatasource\"\x80\x01\n\x1a\x43reatePXFDatasourceRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12@\n\ndatasource\x18\x02 \x01(\x0b\x32,.yandex.cloud.mdb.greenplum.v1.PXFDatasource\"\xb1\x01\n\x1aUpdatePXFDatasourceRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12@\n\ndatasource\x18\x03 \x01(\x0b\x32,.yandex.cloud.mdb.greenplum.v1.PXFDatasource\"|\n\x1a\x44\x65letePXFDatasourceRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12<\n\x0f\x64\x61tasource_name\x18\x02 \x01(\tB#\xe8\xc7\x31\x01\xf2\xc7\x31\x12^[^\\|/*?.,;\"\'<>]+$\x8a\xc8\x31\x05\x33-2002\x93\x07\n\x14PXFDatasourceService\x12\xc0\x01\n\x04List\x12\x38.yandex.cloud.mdb.greenplum.v1.ListPXFDatasourcesRequest\x1a\x39.yandex.cloud.mdb.greenplum.v1.ListPXFDatasourcesResponse\"C\x82\xd3\xe4\x93\x02=\x12;/managed-greenplum/v1/clusters/{cluster_id}/pxf_datasources\x12\xde\x01\n\x06\x43reate\x12\x39.yandex.cloud.mdb.greenplum.v1.CreatePXFDatasourceRequest\x1a!.yandex.cloud.operation.Operation\"v\xb2\xd2*,\n\x1b\x43reatePXFDatasourceMetadata\x12\rPXFDatasource\x82\xd3\xe4\x93\x02@\";/managed-greenplum/v1/clusters/{cluster_id}/pxf_datasources:\x01*\x12\xde\x01\n\x06Update\x12\x39.yandex.cloud.mdb.greenplum.v1.UpdatePXFDatasourceRequest\x1a!.yandex.cloud.operation.Operation\"v\xb2\xd2*,\n\x1bUpdatePXFDatasourceMetadata\x12\rPXFDatasource\x82\xd3\xe4\x93\x02@2;/managed-greenplum/v1/clusters/{cluster_id}/pxf_datasources:\x01*\x12\xf5\x01\n\x06\x44\x65lete\x12\x39.yandex.cloud.mdb.greenplum.v1.DeletePXFDatasourceRequest\x1a!.yandex.cloud.operation.Operation\"\x8c\x01\xb2\xd2*4\n\x1b\x44\x65letePXFDatasourceMetadata\x12\x15google.protobuf.Empty\x82\xd3\xe4\x93\x02N*L/managed-greenplum/v1/clusters/{cluster_id}/pxf_datasource/{datasource_name}Bp\n!yandex.cloud.api.mdb.greenplum.v1ZKgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/greenplum/v1;greenplumb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.mdb.greenplum.v1.pxf_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n!yandex.cloud.api.mdb.greenplum.v1ZKgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/greenplum/v1;greenplum'
  _CREATEPXFDATASOURCEMETADATA.fields_by_name['cluster_id']._options = None
  _CREATEPXFDATASOURCEMETADATA.fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _CREATEPXFDATASOURCEMETADATA.fields_by_name['datasource_name']._options = None
  _CREATEPXFDATASOURCEMETADATA.fields_by_name['datasource_name']._serialized_options = b'\350\3071\001\362\3071\022^[^\\|/*?.,;\"\'<>]+$\212\3101\0053-200'
  _UPDATEPXFDATASOURCEMETADATA.fields_by_name['cluster_id']._options = None
  _UPDATEPXFDATASOURCEMETADATA.fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _UPDATEPXFDATASOURCEMETADATA.fields_by_name['datasource_name']._options = None
  _UPDATEPXFDATASOURCEMETADATA.fields_by_name['datasource_name']._serialized_options = b'\350\3071\001\362\3071\022^[^\\|/*?.,;\"\'<>]+$\212\3101\0053-200'
  _DELETEPXFDATASOURCEMETADATA.fields_by_name['cluster_id']._options = None
  _DELETEPXFDATASOURCEMETADATA.fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _DELETEPXFDATASOURCEMETADATA.fields_by_name['datasource_name']._options = None
  _DELETEPXFDATASOURCEMETADATA.fields_by_name['datasource_name']._serialized_options = b'\350\3071\001\362\3071\022^[^\\|/*?.,;\"\'<>]+$\212\3101\0053-200'
  _LISTPXFDATASOURCESREQUEST.fields_by_name['cluster_id']._options = None
  _LISTPXFDATASOURCESREQUEST.fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _CREATEPXFDATASOURCEREQUEST.fields_by_name['cluster_id']._options = None
  _CREATEPXFDATASOURCEREQUEST.fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _UPDATEPXFDATASOURCEREQUEST.fields_by_name['cluster_id']._options = None
  _UPDATEPXFDATASOURCEREQUEST.fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _DELETEPXFDATASOURCEREQUEST.fields_by_name['cluster_id']._options = None
  _DELETEPXFDATASOURCEREQUEST.fields_by_name['cluster_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _DELETEPXFDATASOURCEREQUEST.fields_by_name['datasource_name']._options = None
  _DELETEPXFDATASOURCEREQUEST.fields_by_name['datasource_name']._serialized_options = b'\350\3071\001\362\3071\022^[^\\|/*?.,;\"\'<>]+$\212\3101\0053-200'
  _PXFDATASOURCESERVICE.methods_by_name['List']._options = None
  _PXFDATASOURCESERVICE.methods_by_name['List']._serialized_options = b'\202\323\344\223\002=\022;/managed-greenplum/v1/clusters/{cluster_id}/pxf_datasources'
  _PXFDATASOURCESERVICE.methods_by_name['Create']._options = None
  _PXFDATASOURCESERVICE.methods_by_name['Create']._serialized_options = b'\262\322*,\n\033CreatePXFDatasourceMetadata\022\rPXFDatasource\202\323\344\223\002@\";/managed-greenplum/v1/clusters/{cluster_id}/pxf_datasources:\001*'
  _PXFDATASOURCESERVICE.methods_by_name['Update']._options = None
  _PXFDATASOURCESERVICE.methods_by_name['Update']._serialized_options = b'\262\322*,\n\033UpdatePXFDatasourceMetadata\022\rPXFDatasource\202\323\344\223\002@2;/managed-greenplum/v1/clusters/{cluster_id}/pxf_datasources:\001*'
  _PXFDATASOURCESERVICE.methods_by_name['Delete']._options = None
  _PXFDATASOURCESERVICE.methods_by_name['Delete']._serialized_options = b'\262\322*4\n\033DeletePXFDatasourceMetadata\022\025google.protobuf.Empty\202\323\344\223\002N*L/managed-greenplum/v1/clusters/{cluster_id}/pxf_datasource/{datasource_name}'
  _globals['_CREATEPXFDATASOURCEMETADATA']._serialized_start=292
  _globals['_CREATEPXFDATASOURCEMETADATA']._serialized_end=417
  _globals['_UPDATEPXFDATASOURCEMETADATA']._serialized_start=419
  _globals['_UPDATEPXFDATASOURCEMETADATA']._serialized_end=544
  _globals['_DELETEPXFDATASOURCEMETADATA']._serialized_start=546
  _globals['_DELETEPXFDATASOURCEMETADATA']._serialized_end=671
  _globals['_LISTPXFDATASOURCESREQUEST']._serialized_start=673
  _globals['_LISTPXFDATASOURCESREQUEST']._serialized_end=734
  _globals['_LISTPXFDATASOURCESRESPONSE']._serialized_start=736
  _globals['_LISTPXFDATASOURCESRESPONSE']._serialized_end=831
  _globals['_CREATEPXFDATASOURCEREQUEST']._serialized_start=834
  _globals['_CREATEPXFDATASOURCEREQUEST']._serialized_end=962
  _globals['_UPDATEPXFDATASOURCEREQUEST']._serialized_start=965
  _globals['_UPDATEPXFDATASOURCEREQUEST']._serialized_end=1142
  _globals['_DELETEPXFDATASOURCEREQUEST']._serialized_start=1144
  _globals['_DELETEPXFDATASOURCEREQUEST']._serialized_end=1268
  _globals['_PXFDATASOURCESERVICE']._serialized_start=1271
  _globals['_PXFDATASOURCESERVICE']._serialized_end=2186
# @@protoc_insertion_point(module_scope)
