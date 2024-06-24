# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/kms/v1/asymmetricsignature/asymmetric_signature_key.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nFyandex/cloud/kms/v1/asymmetricsignature/asymmetric_signature_key.proto\x12\'yandex.cloud.kms.v1.asymmetricsignature\x1a\x1fgoogle/protobuf/timestamp.proto\"\xb9\x04\n\x16\x41symmetricSignatureKey\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\tfolder_id\x18\x02 \x01(\t\x12.\n\ncreated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12[\n\x06labels\x18\x06 \x03(\x0b\x32K.yandex.cloud.kms.v1.asymmetricsignature.AsymmetricSignatureKey.LabelsEntry\x12V\n\x06status\x18\x07 \x01(\x0e\x32\x46.yandex.cloud.kms.v1.asymmetricsignature.AsymmetricSignatureKey.Status\x12\x62\n\x13signature_algorithm\x18\x08 \x01(\x0e\x32\x45.yandex.cloud.kms.v1.asymmetricsignature.AsymmetricSignatureAlgorithm\x12\x1b\n\x13\x64\x65letion_protection\x18\t \x01(\x08\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"H\n\x06Status\x12\x16\n\x12STATUS_UNSPECIFIED\x10\x00\x12\x0c\n\x08\x43REATING\x10\x01\x12\n\n\x06\x41\x43TIVE\x10\x02\x12\x0c\n\x08INACTIVE\x10\x03*\xda\x03\n\x1c\x41symmetricSignatureAlgorithm\x12.\n*ASYMMETRIC_SIGNATURE_ALGORITHM_UNSPECIFIED\x10\x00\x12\x1d\n\x19RSA_2048_SIGN_PSS_SHA_256\x10\x01\x12\x1d\n\x19RSA_2048_SIGN_PSS_SHA_384\x10\x02\x12\x1d\n\x19RSA_2048_SIGN_PSS_SHA_512\x10\x03\x12\x1d\n\x19RSA_3072_SIGN_PSS_SHA_256\x10\x04\x12\x1d\n\x19RSA_3072_SIGN_PSS_SHA_384\x10\x05\x12\x1d\n\x19RSA_3072_SIGN_PSS_SHA_512\x10\x06\x12\x1d\n\x19RSA_4096_SIGN_PSS_SHA_256\x10\x07\x12\x1d\n\x19RSA_4096_SIGN_PSS_SHA_384\x10\x08\x12\x1d\n\x19RSA_4096_SIGN_PSS_SHA_512\x10\t\x12\x1b\n\x17\x45\x43\x44SA_NIST_P256_SHA_256\x10\n\x12\x1b\n\x17\x45\x43\x44SA_NIST_P384_SHA_384\x10\x0b\x12\x1b\n\x17\x45\x43\x44SA_NIST_P521_SHA_512\x10\x0c\x12\x1c\n\x18\x45\x43\x44SA_SECP256_K1_SHA_256\x10\rBj\n\x17yandex.cloud.api.kms.v1ZOgithub.com/yandex-cloud/go-genproto/yandex/cloud/kms/v1/asymmetricsignature;kmsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.kms.v1.asymmetricsignature.asymmetric_signature_key_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\027yandex.cloud.api.kms.v1ZOgithub.com/yandex-cloud/go-genproto/yandex/cloud/kms/v1/asymmetricsignature;kms'
  _ASYMMETRICSIGNATUREKEY_LABELSENTRY._options = None
  _ASYMMETRICSIGNATUREKEY_LABELSENTRY._serialized_options = b'8\001'
  _globals['_ASYMMETRICSIGNATUREALGORITHM']._serialized_start=721
  _globals['_ASYMMETRICSIGNATUREALGORITHM']._serialized_end=1195
  _globals['_ASYMMETRICSIGNATUREKEY']._serialized_start=149
  _globals['_ASYMMETRICSIGNATUREKEY']._serialized_end=718
  _globals['_ASYMMETRICSIGNATUREKEY_LABELSENTRY']._serialized_start=599
  _globals['_ASYMMETRICSIGNATUREKEY_LABELSENTRY']._serialized_end=644
  _globals['_ASYMMETRICSIGNATUREKEY_STATUS']._serialized_start=646
  _globals['_ASYMMETRICSIGNATUREKEY_STATUS']._serialized_end=718
# @@protoc_insertion_point(module_scope)
