# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/organizationmanager/v1/saml/federation_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from yandex.cloud.api import operation_pb2 as yandex_dot_cloud_dot_api_dot_operation__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2
from yandex.cloud.organizationmanager.v1.saml import federation_pb2 as yandex_dot_cloud_dot_organizationmanager_dot_v1_dot_saml_dot_federation__pb2
from yandex.cloud.organizationmanager.v1 import user_account_pb2 as yandex_dot_cloud_dot_organizationmanager_dot_v1_dot_user__account__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nAyandex/cloud/organizationmanager/v1/saml/federation_service.proto\x12(yandex.cloud.organizationmanager.v1.saml\x1a\x1cgoogle/api/annotations.proto\x1a\x1egoogle/protobuf/duration.proto\x1a google/protobuf/field_mask.proto\x1a yandex/cloud/api/operation.proto\x1a&yandex/cloud/operation/operation.proto\x1a\x39yandex/cloud/organizationmanager/v1/saml/federation.proto\x1a\x36yandex/cloud/organizationmanager/v1/user_account.proto\x1a\x1dyandex/cloud/validation.proto\"7\n\x14GetFederationRequest\x12\x1f\n\rfederation_id\x18\x01 \x01(\tB\x08\x8a\xc8\x31\x04<=50\"\x9a\x01\n\x16ListFederationsRequest\x12%\n\x0forganization_id\x18\x06 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x03 \x01(\x03\x42\n\xfa\xc7\x31\x06\x30-1000\x12\x1e\n\npage_token\x18\x04 \x01(\tB\n\x8a\xc8\x31\x06<=2000\x12\x1a\n\x06\x66ilter\x18\x05 \x01(\tB\n\x8a\xc8\x31\x06<=1000\"}\n\x17ListFederationsResponse\x12I\n\x0b\x66\x65\x64\x65rations\x18\x01 \x03(\x0b\x32\x34.yandex.cloud.organizationmanager.v1.saml.Federation\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\xd2\x05\n\x17\x43reateFederationRequest\x12!\n\x0forganization_id\x18\x01 \x01(\tB\x08\x8a\xc8\x31\x04<=50\x12\x31\n\x04name\x18\x02 \x01(\tB#\xf2\xc7\x31\x1f[a-z]([-a-z0-9]{0,61}[a-z0-9])?\x12\x1e\n\x0b\x64\x65scription\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=256\x12>\n\x0e\x63ookie_max_age\x18\x04 \x01(\x0b\x32\x19.google.protobuf.DurationB\x0b\xfa\xc7\x31\x07\x31\x30m-12h\x12$\n\x1c\x61uto_create_account_on_login\x18\x05 \x01(\x08\x12\x1e\n\x06issuer\x18\x06 \x01(\tB\x0e\xe8\xc7\x31\x01\x8a\xc8\x31\x06<=8000\x12J\n\x0bsso_binding\x18\x07 \x01(\x0e\x32\x35.yandex.cloud.organizationmanager.v1.saml.BindingType\x12\x1f\n\x07sso_url\x18\x08 \x01(\tB\x0e\xe8\xc7\x31\x01\x8a\xc8\x31\x06<=8000\x12_\n\x11security_settings\x18\t \x01(\x0b\x32\x44.yandex.cloud.organizationmanager.v1.saml.FederationSecuritySettings\x12!\n\x19\x63\x61se_insensitive_name_ids\x18\n \x01(\x08\x12\x9a\x01\n\x06labels\x18\x0b \x03(\x0b\x32M.yandex.cloud.organizationmanager.v1.saml.CreateFederationRequest.LabelsEntryB;\xf2\xc7\x31\x0b[-_0-9a-z]*\x82\xc8\x31\x04<=64\x8a\xc8\x31\x04<=63\xb2\xc8\x31\x18\x12\x10[a-z][-_0-9a-z]*\x1a\x04\x31-63\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"1\n\x18\x43reateFederationMetadata\x12\x15\n\rfederation_id\x18\x01 \x01(\t\"\x88\x06\n\x17UpdateFederationRequest\x12\x1f\n\rfederation_id\x18\x01 \x01(\tB\x08\x8a\xc8\x31\x04<=50\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12\x32\n\x04name\x18\x03 \x01(\tB$\xf2\xc7\x31 |[a-z]([-a-z0-9]{0,61}[a-z0-9])?\x12\x1e\n\x0b\x64\x65scription\x18\x04 \x01(\tB\t\x8a\xc8\x31\x05<=256\x12>\n\x0e\x63ookie_max_age\x18\x05 \x01(\x0b\x32\x19.google.protobuf.DurationB\x0b\xfa\xc7\x31\x07\x31\x30m-12h\x12$\n\x1c\x61uto_create_account_on_login\x18\x06 \x01(\x08\x12\x1e\n\x06issuer\x18\x07 \x01(\tB\x0e\xe8\xc7\x31\x01\x8a\xc8\x31\x06<=8000\x12J\n\x0bsso_binding\x18\x08 \x01(\x0e\x32\x35.yandex.cloud.organizationmanager.v1.saml.BindingType\x12\x1f\n\x07sso_url\x18\t \x01(\tB\x0e\xe8\xc7\x31\x01\x8a\xc8\x31\x06<=8000\x12_\n\x11security_settings\x18\n \x01(\x0b\x32\x44.yandex.cloud.organizationmanager.v1.saml.FederationSecuritySettings\x12!\n\x19\x63\x61se_insensitive_name_ids\x18\x0c \x01(\x08\x12\x9a\x01\n\x06labels\x18\r \x03(\x0b\x32M.yandex.cloud.organizationmanager.v1.saml.UpdateFederationRequest.LabelsEntryB;\xf2\xc7\x31\x0b[-_0-9a-z]*\x82\xc8\x31\x04<=64\x8a\xc8\x31\x04<=63\xb2\xc8\x31\x18\x12\x10[a-z][-_0-9a-z]*\x1a\x04\x31-63\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01J\x04\x08\x0b\x10\x0c\"1\n\x18UpdateFederationMetadata\x12\x15\n\rfederation_id\x18\x01 \x01(\t\":\n\x17\x44\x65leteFederationRequest\x12\x1f\n\rfederation_id\x18\x01 \x01(\tB\x08\x8a\xc8\x31\x04<=50\"1\n\x18\x44\x65leteFederationMetadata\x12\x15\n\rfederation_id\x18\x01 \x01(\t\"`\n\x1f\x41\x64\x64\x46\x65\x64\x65ratedUserAccountsRequest\x12\x1f\n\rfederation_id\x18\x01 \x01(\tB\x08\x8a\xc8\x31\x04<=50\x12\x1c\n\x08name_ids\x18\x02 \x03(\tB\n\x8a\xc8\x31\x06<=1000\"9\n AddFederatedUserAccountsMetadata\x12\x15\n\rfederation_id\x18\x01 \x01(\t\"k\n AddFederatedUserAccountsResponse\x12G\n\ruser_accounts\x18\x01 \x03(\x0b\x32\x30.yandex.cloud.organizationmanager.v1.UserAccount\"r\n\"DeleteFederatedUserAccountsRequest\x12#\n\rfederation_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\'\n\x0bsubject_ids\x18\x02 \x03(\tB\x12\x82\xc8\x31\x06\x31-1000\x8a\xc8\x31\x04\x31-50\"<\n#DeleteFederatedUserAccountsMetadata\x12\x15\n\rfederation_id\x18\x01 \x01(\t\"^\n#DeleteFederatedUserAccountsResponse\x12\x18\n\x10\x64\x65leted_subjects\x18\x01 \x03(\t\x12\x1d\n\x15non_existing_subjects\x18\x02 \x03(\t\"\xa2\x01\n ListFederatedUserAccountsRequest\x12#\n\rfederation_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06\x30-1000\x12\x1e\n\npage_token\x18\x03 \x01(\tB\n\x8a\xc8\x31\x06<=2000\x12\x1a\n\x06\x66ilter\x18\x04 \x01(\tB\n\x8a\xc8\x31\x06<=1010\"\x85\x01\n!ListFederatedUserAccountsResponse\x12G\n\ruser_accounts\x18\x01 \x03(\x0b\x32\x30.yandex.cloud.organizationmanager.v1.UserAccount\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\x81\x01\n\x1fListFederationOperationsRequest\x12\x1f\n\rfederation_id\x18\x01 \x01(\tB\x08\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06\x30-1000\x12\x1e\n\npage_token\x18\x03 \x01(\tB\n\x8a\xc8\x31\x06<=2000\"r\n ListFederationOperationsResponse\x12\x35\n\noperations\x18\x01 \x03(\x0b\x32!.yandex.cloud.operation.Operation\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t2\xfb\x10\n\x11\x46\x65\x64\x65rationService\x12\xbe\x01\n\x03Get\x12>.yandex.cloud.organizationmanager.v1.saml.GetFederationRequest\x1a\x34.yandex.cloud.organizationmanager.v1.saml.Federation\"A\x82\xd3\xe4\x93\x02;\x12\x39/organization-manager/v1/saml/federations/{federation_id}\x12\xbe\x01\n\x04List\x12@.yandex.cloud.organizationmanager.v1.saml.ListFederationsRequest\x1a\x41.yandex.cloud.organizationmanager.v1.saml.ListFederationsResponse\"1\x82\xd3\xe4\x93\x02+\x12)/organization-manager/v1/saml/federations\x12\xce\x01\n\x06\x43reate\x12\x41.yandex.cloud.organizationmanager.v1.saml.CreateFederationRequest\x1a!.yandex.cloud.operation.Operation\"^\xb2\xd2*&\n\x18\x43reateFederationMetadata\x12\nFederation\x82\xd3\xe4\x93\x02.\")/organization-manager/v1/saml/federations:\x01*\x12\xde\x01\n\x06Update\x12\x41.yandex.cloud.organizationmanager.v1.saml.UpdateFederationRequest\x1a!.yandex.cloud.operation.Operation\"n\xb2\xd2*&\n\x18UpdateFederationMetadata\x12\nFederation\x82\xd3\xe4\x93\x02>29/organization-manager/v1/saml/federations/{federation_id}:\x01*\x12\xe6\x01\n\x06\x44\x65lete\x12\x41.yandex.cloud.organizationmanager.v1.saml.DeleteFederationRequest\x1a!.yandex.cloud.operation.Operation\"v\xb2\xd2*1\n\x18\x44\x65leteFederationMetadata\x12\x15google.protobuf.Empty\x82\xd3\xe4\x93\x02;*9/organization-manager/v1/saml/federations/{federation_id}\x12\x9e\x02\n\x0f\x41\x64\x64UserAccounts\x12I.yandex.cloud.organizationmanager.v1.saml.AddFederatedUserAccountsRequest\x1a!.yandex.cloud.operation.Operation\"\x9c\x01\xb2\xd2*D\n AddFederatedUserAccountsMetadata\x12 AddFederatedUserAccountsResponse\x82\xd3\xe4\x93\x02N\"I/organization-manager/v1/saml/federations/{federation_id}:addUserAccounts:\x01*\x12\xad\x02\n\x12\x44\x65leteUserAccounts\x12L.yandex.cloud.organizationmanager.v1.saml.DeleteFederatedUserAccountsRequest\x1a!.yandex.cloud.operation.Operation\"\xa5\x01\xb2\xd2*J\n#DeleteFederatedUserAccountsMetadata\x12#DeleteFederatedUserAccountsResponse\x82\xd3\xe4\x93\x02Q\"L/organization-manager/v1/saml/federations/{federation_id}:deleteUserAccounts:\x01*\x12\xff\x01\n\x10ListUserAccounts\x12J.yandex.cloud.organizationmanager.v1.saml.ListFederatedUserAccountsRequest\x1aK.yandex.cloud.organizationmanager.v1.saml.ListFederatedUserAccountsResponse\"R\x82\xd3\xe4\x93\x02L\x12J/organization-manager/v1/saml/federations/{federation_id}:listUserAccounts\x12\xf5\x01\n\x0eListOperations\x12I.yandex.cloud.organizationmanager.v1.saml.ListFederationOperationsRequest\x1aJ.yandex.cloud.organizationmanager.v1.saml.ListFederationOperationsResponse\"L\x82\xd3\xe4\x93\x02\x46\x12\x44/organization-manager/v1/saml/federations/{federation_id}/operationsB\x81\x01\n,yandex.cloud.api.organizationmanager.v1.samlZQgithub.com/yandex-cloud/go-genproto/yandex/cloud/organizationmanager/v1/saml;samlb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.organizationmanager.v1.saml.federation_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n,yandex.cloud.api.organizationmanager.v1.samlZQgithub.com/yandex-cloud/go-genproto/yandex/cloud/organizationmanager/v1/saml;saml'
  _GETFEDERATIONREQUEST.fields_by_name['federation_id']._options = None
  _GETFEDERATIONREQUEST.fields_by_name['federation_id']._serialized_options = b'\212\3101\004<=50'
  _LISTFEDERATIONSREQUEST.fields_by_name['organization_id']._options = None
  _LISTFEDERATIONSREQUEST.fields_by_name['organization_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _LISTFEDERATIONSREQUEST.fields_by_name['page_size']._options = None
  _LISTFEDERATIONSREQUEST.fields_by_name['page_size']._serialized_options = b'\372\3071\0060-1000'
  _LISTFEDERATIONSREQUEST.fields_by_name['page_token']._options = None
  _LISTFEDERATIONSREQUEST.fields_by_name['page_token']._serialized_options = b'\212\3101\006<=2000'
  _LISTFEDERATIONSREQUEST.fields_by_name['filter']._options = None
  _LISTFEDERATIONSREQUEST.fields_by_name['filter']._serialized_options = b'\212\3101\006<=1000'
  _CREATEFEDERATIONREQUEST_LABELSENTRY._options = None
  _CREATEFEDERATIONREQUEST_LABELSENTRY._serialized_options = b'8\001'
  _CREATEFEDERATIONREQUEST.fields_by_name['organization_id']._options = None
  _CREATEFEDERATIONREQUEST.fields_by_name['organization_id']._serialized_options = b'\212\3101\004<=50'
  _CREATEFEDERATIONREQUEST.fields_by_name['name']._options = None
  _CREATEFEDERATIONREQUEST.fields_by_name['name']._serialized_options = b'\362\3071\037[a-z]([-a-z0-9]{0,61}[a-z0-9])?'
  _CREATEFEDERATIONREQUEST.fields_by_name['description']._options = None
  _CREATEFEDERATIONREQUEST.fields_by_name['description']._serialized_options = b'\212\3101\005<=256'
  _CREATEFEDERATIONREQUEST.fields_by_name['cookie_max_age']._options = None
  _CREATEFEDERATIONREQUEST.fields_by_name['cookie_max_age']._serialized_options = b'\372\3071\00710m-12h'
  _CREATEFEDERATIONREQUEST.fields_by_name['issuer']._options = None
  _CREATEFEDERATIONREQUEST.fields_by_name['issuer']._serialized_options = b'\350\3071\001\212\3101\006<=8000'
  _CREATEFEDERATIONREQUEST.fields_by_name['sso_url']._options = None
  _CREATEFEDERATIONREQUEST.fields_by_name['sso_url']._serialized_options = b'\350\3071\001\212\3101\006<=8000'
  _CREATEFEDERATIONREQUEST.fields_by_name['labels']._options = None
  _CREATEFEDERATIONREQUEST.fields_by_name['labels']._serialized_options = b'\362\3071\013[-_0-9a-z]*\202\3101\004<=64\212\3101\004<=63\262\3101\030\022\020[a-z][-_0-9a-z]*\032\0041-63'
  _UPDATEFEDERATIONREQUEST_LABELSENTRY._options = None
  _UPDATEFEDERATIONREQUEST_LABELSENTRY._serialized_options = b'8\001'
  _UPDATEFEDERATIONREQUEST.fields_by_name['federation_id']._options = None
  _UPDATEFEDERATIONREQUEST.fields_by_name['federation_id']._serialized_options = b'\212\3101\004<=50'
  _UPDATEFEDERATIONREQUEST.fields_by_name['name']._options = None
  _UPDATEFEDERATIONREQUEST.fields_by_name['name']._serialized_options = b'\362\3071 |[a-z]([-a-z0-9]{0,61}[a-z0-9])?'
  _UPDATEFEDERATIONREQUEST.fields_by_name['description']._options = None
  _UPDATEFEDERATIONREQUEST.fields_by_name['description']._serialized_options = b'\212\3101\005<=256'
  _UPDATEFEDERATIONREQUEST.fields_by_name['cookie_max_age']._options = None
  _UPDATEFEDERATIONREQUEST.fields_by_name['cookie_max_age']._serialized_options = b'\372\3071\00710m-12h'
  _UPDATEFEDERATIONREQUEST.fields_by_name['issuer']._options = None
  _UPDATEFEDERATIONREQUEST.fields_by_name['issuer']._serialized_options = b'\350\3071\001\212\3101\006<=8000'
  _UPDATEFEDERATIONREQUEST.fields_by_name['sso_url']._options = None
  _UPDATEFEDERATIONREQUEST.fields_by_name['sso_url']._serialized_options = b'\350\3071\001\212\3101\006<=8000'
  _UPDATEFEDERATIONREQUEST.fields_by_name['labels']._options = None
  _UPDATEFEDERATIONREQUEST.fields_by_name['labels']._serialized_options = b'\362\3071\013[-_0-9a-z]*\202\3101\004<=64\212\3101\004<=63\262\3101\030\022\020[a-z][-_0-9a-z]*\032\0041-63'
  _DELETEFEDERATIONREQUEST.fields_by_name['federation_id']._options = None
  _DELETEFEDERATIONREQUEST.fields_by_name['federation_id']._serialized_options = b'\212\3101\004<=50'
  _ADDFEDERATEDUSERACCOUNTSREQUEST.fields_by_name['federation_id']._options = None
  _ADDFEDERATEDUSERACCOUNTSREQUEST.fields_by_name['federation_id']._serialized_options = b'\212\3101\004<=50'
  _ADDFEDERATEDUSERACCOUNTSREQUEST.fields_by_name['name_ids']._options = None
  _ADDFEDERATEDUSERACCOUNTSREQUEST.fields_by_name['name_ids']._serialized_options = b'\212\3101\006<=1000'
  _DELETEFEDERATEDUSERACCOUNTSREQUEST.fields_by_name['federation_id']._options = None
  _DELETEFEDERATEDUSERACCOUNTSREQUEST.fields_by_name['federation_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _DELETEFEDERATEDUSERACCOUNTSREQUEST.fields_by_name['subject_ids']._options = None
  _DELETEFEDERATEDUSERACCOUNTSREQUEST.fields_by_name['subject_ids']._serialized_options = b'\202\3101\0061-1000\212\3101\0041-50'
  _LISTFEDERATEDUSERACCOUNTSREQUEST.fields_by_name['federation_id']._options = None
  _LISTFEDERATEDUSERACCOUNTSREQUEST.fields_by_name['federation_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _LISTFEDERATEDUSERACCOUNTSREQUEST.fields_by_name['page_size']._options = None
  _LISTFEDERATEDUSERACCOUNTSREQUEST.fields_by_name['page_size']._serialized_options = b'\372\3071\0060-1000'
  _LISTFEDERATEDUSERACCOUNTSREQUEST.fields_by_name['page_token']._options = None
  _LISTFEDERATEDUSERACCOUNTSREQUEST.fields_by_name['page_token']._serialized_options = b'\212\3101\006<=2000'
  _LISTFEDERATEDUSERACCOUNTSREQUEST.fields_by_name['filter']._options = None
  _LISTFEDERATEDUSERACCOUNTSREQUEST.fields_by_name['filter']._serialized_options = b'\212\3101\006<=1010'
  _LISTFEDERATIONOPERATIONSREQUEST.fields_by_name['federation_id']._options = None
  _LISTFEDERATIONOPERATIONSREQUEST.fields_by_name['federation_id']._serialized_options = b'\212\3101\004<=50'
  _LISTFEDERATIONOPERATIONSREQUEST.fields_by_name['page_size']._options = None
  _LISTFEDERATIONOPERATIONSREQUEST.fields_by_name['page_size']._serialized_options = b'\372\3071\0060-1000'
  _LISTFEDERATIONOPERATIONSREQUEST.fields_by_name['page_token']._options = None
  _LISTFEDERATIONOPERATIONSREQUEST.fields_by_name['page_token']._serialized_options = b'\212\3101\006<=2000'
  _FEDERATIONSERVICE.methods_by_name['Get']._options = None
  _FEDERATIONSERVICE.methods_by_name['Get']._serialized_options = b'\202\323\344\223\002;\0229/organization-manager/v1/saml/federations/{federation_id}'
  _FEDERATIONSERVICE.methods_by_name['List']._options = None
  _FEDERATIONSERVICE.methods_by_name['List']._serialized_options = b'\202\323\344\223\002+\022)/organization-manager/v1/saml/federations'
  _FEDERATIONSERVICE.methods_by_name['Create']._options = None
  _FEDERATIONSERVICE.methods_by_name['Create']._serialized_options = b'\262\322*&\n\030CreateFederationMetadata\022\nFederation\202\323\344\223\002.\")/organization-manager/v1/saml/federations:\001*'
  _FEDERATIONSERVICE.methods_by_name['Update']._options = None
  _FEDERATIONSERVICE.methods_by_name['Update']._serialized_options = b'\262\322*&\n\030UpdateFederationMetadata\022\nFederation\202\323\344\223\002>29/organization-manager/v1/saml/federations/{federation_id}:\001*'
  _FEDERATIONSERVICE.methods_by_name['Delete']._options = None
  _FEDERATIONSERVICE.methods_by_name['Delete']._serialized_options = b'\262\322*1\n\030DeleteFederationMetadata\022\025google.protobuf.Empty\202\323\344\223\002;*9/organization-manager/v1/saml/federations/{federation_id}'
  _FEDERATIONSERVICE.methods_by_name['AddUserAccounts']._options = None
  _FEDERATIONSERVICE.methods_by_name['AddUserAccounts']._serialized_options = b'\262\322*D\n AddFederatedUserAccountsMetadata\022 AddFederatedUserAccountsResponse\202\323\344\223\002N\"I/organization-manager/v1/saml/federations/{federation_id}:addUserAccounts:\001*'
  _FEDERATIONSERVICE.methods_by_name['DeleteUserAccounts']._options = None
  _FEDERATIONSERVICE.methods_by_name['DeleteUserAccounts']._serialized_options = b'\262\322*J\n#DeleteFederatedUserAccountsMetadata\022#DeleteFederatedUserAccountsResponse\202\323\344\223\002Q\"L/organization-manager/v1/saml/federations/{federation_id}:deleteUserAccounts:\001*'
  _FEDERATIONSERVICE.methods_by_name['ListUserAccounts']._options = None
  _FEDERATIONSERVICE.methods_by_name['ListUserAccounts']._serialized_options = b'\202\323\344\223\002L\022J/organization-manager/v1/saml/federations/{federation_id}:listUserAccounts'
  _FEDERATIONSERVICE.methods_by_name['ListOperations']._options = None
  _FEDERATIONSERVICE.methods_by_name['ListOperations']._serialized_options = b'\202\323\344\223\002F\022D/organization-manager/v1/saml/federations/{federation_id}/operations'
  _globals['_GETFEDERATIONREQUEST']._serialized_start=427
  _globals['_GETFEDERATIONREQUEST']._serialized_end=482
  _globals['_LISTFEDERATIONSREQUEST']._serialized_start=485
  _globals['_LISTFEDERATIONSREQUEST']._serialized_end=639
  _globals['_LISTFEDERATIONSRESPONSE']._serialized_start=641
  _globals['_LISTFEDERATIONSRESPONSE']._serialized_end=766
  _globals['_CREATEFEDERATIONREQUEST']._serialized_start=769
  _globals['_CREATEFEDERATIONREQUEST']._serialized_end=1491
  _globals['_CREATEFEDERATIONREQUEST_LABELSENTRY']._serialized_start=1446
  _globals['_CREATEFEDERATIONREQUEST_LABELSENTRY']._serialized_end=1491
  _globals['_CREATEFEDERATIONMETADATA']._serialized_start=1493
  _globals['_CREATEFEDERATIONMETADATA']._serialized_end=1542
  _globals['_UPDATEFEDERATIONREQUEST']._serialized_start=1545
  _globals['_UPDATEFEDERATIONREQUEST']._serialized_end=2321
  _globals['_UPDATEFEDERATIONREQUEST_LABELSENTRY']._serialized_start=1446
  _globals['_UPDATEFEDERATIONREQUEST_LABELSENTRY']._serialized_end=1491
  _globals['_UPDATEFEDERATIONMETADATA']._serialized_start=2323
  _globals['_UPDATEFEDERATIONMETADATA']._serialized_end=2372
  _globals['_DELETEFEDERATIONREQUEST']._serialized_start=2374
  _globals['_DELETEFEDERATIONREQUEST']._serialized_end=2432
  _globals['_DELETEFEDERATIONMETADATA']._serialized_start=2434
  _globals['_DELETEFEDERATIONMETADATA']._serialized_end=2483
  _globals['_ADDFEDERATEDUSERACCOUNTSREQUEST']._serialized_start=2485
  _globals['_ADDFEDERATEDUSERACCOUNTSREQUEST']._serialized_end=2581
  _globals['_ADDFEDERATEDUSERACCOUNTSMETADATA']._serialized_start=2583
  _globals['_ADDFEDERATEDUSERACCOUNTSMETADATA']._serialized_end=2640
  _globals['_ADDFEDERATEDUSERACCOUNTSRESPONSE']._serialized_start=2642
  _globals['_ADDFEDERATEDUSERACCOUNTSRESPONSE']._serialized_end=2749
  _globals['_DELETEFEDERATEDUSERACCOUNTSREQUEST']._serialized_start=2751
  _globals['_DELETEFEDERATEDUSERACCOUNTSREQUEST']._serialized_end=2865
  _globals['_DELETEFEDERATEDUSERACCOUNTSMETADATA']._serialized_start=2867
  _globals['_DELETEFEDERATEDUSERACCOUNTSMETADATA']._serialized_end=2927
  _globals['_DELETEFEDERATEDUSERACCOUNTSRESPONSE']._serialized_start=2929
  _globals['_DELETEFEDERATEDUSERACCOUNTSRESPONSE']._serialized_end=3023
  _globals['_LISTFEDERATEDUSERACCOUNTSREQUEST']._serialized_start=3026
  _globals['_LISTFEDERATEDUSERACCOUNTSREQUEST']._serialized_end=3188
  _globals['_LISTFEDERATEDUSERACCOUNTSRESPONSE']._serialized_start=3191
  _globals['_LISTFEDERATEDUSERACCOUNTSRESPONSE']._serialized_end=3324
  _globals['_LISTFEDERATIONOPERATIONSREQUEST']._serialized_start=3327
  _globals['_LISTFEDERATIONOPERATIONSREQUEST']._serialized_end=3456
  _globals['_LISTFEDERATIONOPERATIONSRESPONSE']._serialized_start=3458
  _globals['_LISTFEDERATIONOPERATIONSRESPONSE']._serialized_end=3572
  _globals['_FEDERATIONSERVICE']._serialized_start=3575
  _globals['_FEDERATIONSERVICE']._serialized_end=5746
# @@protoc_insertion_point(module_scope)
