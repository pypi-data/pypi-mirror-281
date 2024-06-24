# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/resourcemanager/v1/cloud_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from yandex.cloud.resourcemanager.v1 import cloud_pb2 as yandex_dot_cloud_dot_resourcemanager_dot_v1_dot_cloud__pb2
from yandex.cloud.api import operation_pb2 as yandex_dot_cloud_dot_api_dot_operation__pb2
from yandex.cloud.access import access_pb2 as yandex_dot_cloud_dot_access_dot_access__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3yandex/cloud/resourcemanager/v1/cloud_service.proto\x12\x1fyandex.cloud.resourcemanager.v1\x1a\x1cgoogle/api/annotations.proto\x1a google/protobuf/field_mask.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a+yandex/cloud/resourcemanager/v1/cloud.proto\x1a yandex/cloud/api/operation.proto\x1a yandex/cloud/access/access.proto\x1a&yandex/cloud/operation/operation.proto\x1a\x1dyandex/cloud/validation.proto\"1\n\x0fGetCloudRequest\x12\x1e\n\x08\x63loud_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"\x91\x01\n\x11ListCloudsRequest\x12\x1d\n\tpage_size\x18\x01 \x01(\x03\x42\n\xfa\xc7\x31\x06<=1000\x12\x1e\n\npage_token\x18\x02 \x01(\tB\n\x8a\xc8\x31\x06<=2000\x12\x1a\n\x06\x66ilter\x18\x03 \x01(\tB\n\x8a\xc8\x31\x06<=1000\x12!\n\x0forganization_id\x18\x04 \x01(\tB\x08\x8a\xc8\x31\x04<=50\"e\n\x12ListCloudsResponse\x12\x36\n\x06\x63louds\x18\x01 \x03(\x0b\x32&.yandex.cloud.resourcemanager.v1.Cloud\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\xce\x02\n\x12\x43reateCloudRequest\x12%\n\x0forganization_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x33\n\x04name\x18\x02 \x01(\tB%\xe8\xc7\x31\x01\xf2\xc7\x31\x1d|[a-z][-a-z0-9]{1,61}[a-z0-9]\x12\x1e\n\x0b\x64\x65scription\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=256\x12\x8c\x01\n\x06labels\x18\x04 \x03(\x0b\x32?.yandex.cloud.resourcemanager.v1.CreateCloudRequest.LabelsEntryB;\xf2\xc7\x31\x0b[-_0-9a-z]*\x82\xc8\x31\x04<=64\x8a\xc8\x31\x04<=63\xb2\xc8\x31\x18\x12\x10[a-z][-_0-9a-z]*\x1a\x04\x31-63\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\'\n\x13\x43reateCloudMetadata\x12\x10\n\x08\x63loud_id\x18\x01 \x01(\t\"{\n\x1aListCloudOperationsRequest\x12\x1e\n\x08\x63loud_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06<=1000\x12\x1e\n\npage_token\x18\x03 \x01(\tB\n\x8a\xc8\x31\x06<=2000\"m\n\x1bListCloudOperationsResponse\x12\x35\n\noperations\x18\x01 \x03(\x0b\x32!.yandex.cloud.operation.Operation\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\xf6\x02\n\x12UpdateCloudRequest\x12\x1e\n\x08\x63loud_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12\x31\n\x04name\x18\x03 \x01(\tB#\xf2\xc7\x31\x1f[a-z]([-a-z0-9]{0,61}[a-z0-9])?\x12\x1e\n\x0b\x64\x65scription\x18\x04 \x01(\tB\t\x8a\xc8\x31\x05<=256\x12\x8c\x01\n\x06labels\x18\x05 \x03(\x0b\x32?.yandex.cloud.resourcemanager.v1.UpdateCloudRequest.LabelsEntryB;\xf2\xc7\x31\x0b[-_0-9a-z]*\x82\xc8\x31\x04<=64\x8a\xc8\x31\x04<=63\xb2\xc8\x31\x18\x12\x10[a-z][-_0-9a-z]*\x1a\x04\x31-63\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\'\n\x13UpdateCloudMetadata\x12\x10\n\x08\x63loud_id\x18\x01 \x01(\t\"f\n\x12\x44\x65leteCloudRequest\x12\x1e\n\x08\x63loud_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x30\n\x0c\x64\x65lete_after\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\xa1\x01\n\x13\x44\x65leteCloudMetadata\x12\x10\n\x08\x63loud_id\x18\x01 \x01(\t\x12\x30\n\x0c\x64\x65lete_after\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x14\n\x0c\x63\x61ncelled_by\x18\x03 \x01(\t\x12\x30\n\x0c\x63\x61ncelled_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp2\xe8\r\n\x0c\x43loudService\x12\x8f\x01\n\x03Get\x12\x30.yandex.cloud.resourcemanager.v1.GetCloudRequest\x1a&.yandex.cloud.resourcemanager.v1.Cloud\".\x82\xd3\xe4\x93\x02(\x12&/resource-manager/v1/clouds/{cloud_id}\x12\x94\x01\n\x04List\x12\x32.yandex.cloud.resourcemanager.v1.ListCloudsRequest\x1a\x33.yandex.cloud.resourcemanager.v1.ListCloudsResponse\"#\x82\xd3\xe4\x93\x02\x1d\x12\x1b/resource-manager/v1/clouds\x12\xa8\x01\n\x06\x43reate\x12\x33.yandex.cloud.resourcemanager.v1.CreateCloudRequest\x1a!.yandex.cloud.operation.Operation\"F\xb2\xd2*\x1c\n\x13\x43reateCloudMetadata\x12\x05\x43loud\x82\xd3\xe4\x93\x02 \"\x1b/resource-manager/v1/clouds:\x01*\x12\xb3\x01\n\x06Update\x12\x33.yandex.cloud.resourcemanager.v1.UpdateCloudRequest\x1a!.yandex.cloud.operation.Operation\"Q\xb2\xd2*\x1c\n\x13UpdateCloudMetadata\x12\x05\x43loud\x82\xd3\xe4\x93\x02+2&/resource-manager/v1/clouds/{cloud_id}:\x01*\x12\xc0\x01\n\x06\x44\x65lete\x12\x33.yandex.cloud.resourcemanager.v1.DeleteCloudRequest\x1a!.yandex.cloud.operation.Operation\"^\xb2\xd2*,\n\x13\x44\x65leteCloudMetadata\x12\x15google.protobuf.Empty\x82\xd3\xe4\x93\x02(*&/resource-manager/v1/clouds/{cloud_id}\x12\xc6\x01\n\x0eListOperations\x12;.yandex.cloud.resourcemanager.v1.ListCloudOperationsRequest\x1a<.yandex.cloud.resourcemanager.v1.ListCloudOperationsResponse\"9\x82\xd3\xe4\x93\x02\x33\x12\x31/resource-manager/v1/clouds/{cloud_id}/operations\x12\xbb\x01\n\x12ListAccessBindings\x12..yandex.cloud.access.ListAccessBindingsRequest\x1a/.yandex.cloud.access.ListAccessBindingsResponse\"D\x82\xd3\xe4\x93\x02>\x12</resource-manager/v1/clouds/{resource_id}:listAccessBindings\x12\xfa\x01\n\x11SetAccessBindings\x12-.yandex.cloud.access.SetAccessBindingsRequest\x1a!.yandex.cloud.operation.Operation\"\x92\x01\xb2\xd2*H\n access.SetAccessBindingsMetadata\x12$access.AccessBindingsOperationResult\x82\xd3\xe4\x93\x02@\";/resource-manager/v1/clouds/{resource_id}:setAccessBindings:\x01*\x12\x86\x02\n\x14UpdateAccessBindings\x12\x30.yandex.cloud.access.UpdateAccessBindingsRequest\x1a!.yandex.cloud.operation.Operation\"\x98\x01\xb2\xd2*K\n#access.UpdateAccessBindingsMetadata\x12$access.AccessBindingsOperationResult\x82\xd3\xe4\x93\x02\x43\">/resource-manager/v1/clouds/{resource_id}:updateAccessBindings:\x01*Bz\n#yandex.cloud.api.resourcemanager.v1ZSgithub.com/yandex-cloud/go-genproto/yandex/cloud/resourcemanager/v1;resourcemanagerb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.resourcemanager.v1.cloud_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n#yandex.cloud.api.resourcemanager.v1ZSgithub.com/yandex-cloud/go-genproto/yandex/cloud/resourcemanager/v1;resourcemanager'
  _GETCLOUDREQUEST.fields_by_name['cloud_id']._options = None
  _GETCLOUDREQUEST.fields_by_name['cloud_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _LISTCLOUDSREQUEST.fields_by_name['page_size']._options = None
  _LISTCLOUDSREQUEST.fields_by_name['page_size']._serialized_options = b'\372\3071\006<=1000'
  _LISTCLOUDSREQUEST.fields_by_name['page_token']._options = None
  _LISTCLOUDSREQUEST.fields_by_name['page_token']._serialized_options = b'\212\3101\006<=2000'
  _LISTCLOUDSREQUEST.fields_by_name['filter']._options = None
  _LISTCLOUDSREQUEST.fields_by_name['filter']._serialized_options = b'\212\3101\006<=1000'
  _LISTCLOUDSREQUEST.fields_by_name['organization_id']._options = None
  _LISTCLOUDSREQUEST.fields_by_name['organization_id']._serialized_options = b'\212\3101\004<=50'
  _CREATECLOUDREQUEST_LABELSENTRY._options = None
  _CREATECLOUDREQUEST_LABELSENTRY._serialized_options = b'8\001'
  _CREATECLOUDREQUEST.fields_by_name['organization_id']._options = None
  _CREATECLOUDREQUEST.fields_by_name['organization_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _CREATECLOUDREQUEST.fields_by_name['name']._options = None
  _CREATECLOUDREQUEST.fields_by_name['name']._serialized_options = b'\350\3071\001\362\3071\035|[a-z][-a-z0-9]{1,61}[a-z0-9]'
  _CREATECLOUDREQUEST.fields_by_name['description']._options = None
  _CREATECLOUDREQUEST.fields_by_name['description']._serialized_options = b'\212\3101\005<=256'
  _CREATECLOUDREQUEST.fields_by_name['labels']._options = None
  _CREATECLOUDREQUEST.fields_by_name['labels']._serialized_options = b'\362\3071\013[-_0-9a-z]*\202\3101\004<=64\212\3101\004<=63\262\3101\030\022\020[a-z][-_0-9a-z]*\032\0041-63'
  _LISTCLOUDOPERATIONSREQUEST.fields_by_name['cloud_id']._options = None
  _LISTCLOUDOPERATIONSREQUEST.fields_by_name['cloud_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _LISTCLOUDOPERATIONSREQUEST.fields_by_name['page_size']._options = None
  _LISTCLOUDOPERATIONSREQUEST.fields_by_name['page_size']._serialized_options = b'\372\3071\006<=1000'
  _LISTCLOUDOPERATIONSREQUEST.fields_by_name['page_token']._options = None
  _LISTCLOUDOPERATIONSREQUEST.fields_by_name['page_token']._serialized_options = b'\212\3101\006<=2000'
  _UPDATECLOUDREQUEST_LABELSENTRY._options = None
  _UPDATECLOUDREQUEST_LABELSENTRY._serialized_options = b'8\001'
  _UPDATECLOUDREQUEST.fields_by_name['cloud_id']._options = None
  _UPDATECLOUDREQUEST.fields_by_name['cloud_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _UPDATECLOUDREQUEST.fields_by_name['name']._options = None
  _UPDATECLOUDREQUEST.fields_by_name['name']._serialized_options = b'\362\3071\037[a-z]([-a-z0-9]{0,61}[a-z0-9])?'
  _UPDATECLOUDREQUEST.fields_by_name['description']._options = None
  _UPDATECLOUDREQUEST.fields_by_name['description']._serialized_options = b'\212\3101\005<=256'
  _UPDATECLOUDREQUEST.fields_by_name['labels']._options = None
  _UPDATECLOUDREQUEST.fields_by_name['labels']._serialized_options = b'\362\3071\013[-_0-9a-z]*\202\3101\004<=64\212\3101\004<=63\262\3101\030\022\020[a-z][-_0-9a-z]*\032\0041-63'
  _DELETECLOUDREQUEST.fields_by_name['cloud_id']._options = None
  _DELETECLOUDREQUEST.fields_by_name['cloud_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _CLOUDSERVICE.methods_by_name['Get']._options = None
  _CLOUDSERVICE.methods_by_name['Get']._serialized_options = b'\202\323\344\223\002(\022&/resource-manager/v1/clouds/{cloud_id}'
  _CLOUDSERVICE.methods_by_name['List']._options = None
  _CLOUDSERVICE.methods_by_name['List']._serialized_options = b'\202\323\344\223\002\035\022\033/resource-manager/v1/clouds'
  _CLOUDSERVICE.methods_by_name['Create']._options = None
  _CLOUDSERVICE.methods_by_name['Create']._serialized_options = b'\262\322*\034\n\023CreateCloudMetadata\022\005Cloud\202\323\344\223\002 \"\033/resource-manager/v1/clouds:\001*'
  _CLOUDSERVICE.methods_by_name['Update']._options = None
  _CLOUDSERVICE.methods_by_name['Update']._serialized_options = b'\262\322*\034\n\023UpdateCloudMetadata\022\005Cloud\202\323\344\223\002+2&/resource-manager/v1/clouds/{cloud_id}:\001*'
  _CLOUDSERVICE.methods_by_name['Delete']._options = None
  _CLOUDSERVICE.methods_by_name['Delete']._serialized_options = b'\262\322*,\n\023DeleteCloudMetadata\022\025google.protobuf.Empty\202\323\344\223\002(*&/resource-manager/v1/clouds/{cloud_id}'
  _CLOUDSERVICE.methods_by_name['ListOperations']._options = None
  _CLOUDSERVICE.methods_by_name['ListOperations']._serialized_options = b'\202\323\344\223\0023\0221/resource-manager/v1/clouds/{cloud_id}/operations'
  _CLOUDSERVICE.methods_by_name['ListAccessBindings']._options = None
  _CLOUDSERVICE.methods_by_name['ListAccessBindings']._serialized_options = b'\202\323\344\223\002>\022</resource-manager/v1/clouds/{resource_id}:listAccessBindings'
  _CLOUDSERVICE.methods_by_name['SetAccessBindings']._options = None
  _CLOUDSERVICE.methods_by_name['SetAccessBindings']._serialized_options = b'\262\322*H\n access.SetAccessBindingsMetadata\022$access.AccessBindingsOperationResult\202\323\344\223\002@\";/resource-manager/v1/clouds/{resource_id}:setAccessBindings:\001*'
  _CLOUDSERVICE.methods_by_name['UpdateAccessBindings']._options = None
  _CLOUDSERVICE.methods_by_name['UpdateAccessBindings']._serialized_options = b'\262\322*K\n#access.UpdateAccessBindingsMetadata\022$access.AccessBindingsOperationResult\202\323\344\223\002C\">/resource-manager/v1/clouds/{resource_id}:updateAccessBindings:\001*'
  _globals['_GETCLOUDREQUEST']._serialized_start=369
  _globals['_GETCLOUDREQUEST']._serialized_end=418
  _globals['_LISTCLOUDSREQUEST']._serialized_start=421
  _globals['_LISTCLOUDSREQUEST']._serialized_end=566
  _globals['_LISTCLOUDSRESPONSE']._serialized_start=568
  _globals['_LISTCLOUDSRESPONSE']._serialized_end=669
  _globals['_CREATECLOUDREQUEST']._serialized_start=672
  _globals['_CREATECLOUDREQUEST']._serialized_end=1006
  _globals['_CREATECLOUDREQUEST_LABELSENTRY']._serialized_start=961
  _globals['_CREATECLOUDREQUEST_LABELSENTRY']._serialized_end=1006
  _globals['_CREATECLOUDMETADATA']._serialized_start=1008
  _globals['_CREATECLOUDMETADATA']._serialized_end=1047
  _globals['_LISTCLOUDOPERATIONSREQUEST']._serialized_start=1049
  _globals['_LISTCLOUDOPERATIONSREQUEST']._serialized_end=1172
  _globals['_LISTCLOUDOPERATIONSRESPONSE']._serialized_start=1174
  _globals['_LISTCLOUDOPERATIONSRESPONSE']._serialized_end=1283
  _globals['_UPDATECLOUDREQUEST']._serialized_start=1286
  _globals['_UPDATECLOUDREQUEST']._serialized_end=1660
  _globals['_UPDATECLOUDREQUEST_LABELSENTRY']._serialized_start=961
  _globals['_UPDATECLOUDREQUEST_LABELSENTRY']._serialized_end=1006
  _globals['_UPDATECLOUDMETADATA']._serialized_start=1662
  _globals['_UPDATECLOUDMETADATA']._serialized_end=1701
  _globals['_DELETECLOUDREQUEST']._serialized_start=1703
  _globals['_DELETECLOUDREQUEST']._serialized_end=1805
  _globals['_DELETECLOUDMETADATA']._serialized_start=1808
  _globals['_DELETECLOUDMETADATA']._serialized_end=1969
  _globals['_CLOUDSERVICE']._serialized_start=1972
  _globals['_CLOUDSERVICE']._serialized_end=3740
# @@protoc_insertion_point(module_scope)
