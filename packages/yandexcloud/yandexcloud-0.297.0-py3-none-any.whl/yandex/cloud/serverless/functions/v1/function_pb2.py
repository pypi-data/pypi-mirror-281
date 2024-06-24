# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/serverless/functions/v1/function.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from yandex.cloud.logging.v1 import log_entry_pb2 as yandex_dot_cloud_dot_logging_dot_v1_dot_log__entry__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3yandex/cloud/serverless/functions/v1/function.proto\x12$yandex.cloud.serverless.functions.v1\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\'yandex/cloud/logging/v1/log_entry.proto\x1a\x1dyandex/cloud/validation.proto\"\xe1\x03\n\x08\x46unction\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\tfolder_id\x18\x02 \x01(\t\x12.\n\ncreated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x16\n\x04name\x18\x04 \x01(\tB\x08\x8a\xc8\x31\x04\x33-63\x12\x1e\n\x0b\x64\x65scription\x18\x05 \x01(\tB\t\x8a\xc8\x31\x05\x30-256\x12T\n\x06labels\x18\x06 \x03(\x0b\x32:.yandex.cloud.serverless.functions.v1.Function.LabelsEntryB\x08\x82\xc8\x31\x04<=64\x12\x14\n\x0clog_group_id\x18\x07 \x01(\t\x12\x17\n\x0fhttp_invoke_url\x18\x08 \x01(\t\x12\x45\n\x06status\x18\t \x01(\x0e\x32\x35.yandex.cloud.serverless.functions.v1.Function.Status\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"S\n\x06Status\x12\x16\n\x12STATUS_UNSPECIFIED\x10\x00\x12\x0c\n\x08\x43REATING\x10\x01\x12\n\n\x06\x41\x43TIVE\x10\x02\x12\x0c\n\x08\x44\x45LETING\x10\x03\x12\t\n\x05\x45RROR\x10\x04\"\xd7\t\n\x07Version\x12\n\n\x02id\x18\x01 \x01(\t\x12\x13\n\x0b\x66unction_id\x18\x02 \x01(\t\x12\x1e\n\x0b\x64\x65scription\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05\x30-256\x12.\n\ncreated_at\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0f\n\x07runtime\x18\x06 \x01(\t\x12\x12\n\nentrypoint\x18\x07 \x01(\t\x12\x42\n\tresources\x18\x08 \x01(\x0b\x32/.yandex.cloud.serverless.functions.v1.Resources\x12\x34\n\x11\x65xecution_timeout\x18\t \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x1a\n\x12service_account_id\x18\n \x01(\t\x12\x12\n\nimage_size\x18\x0c \x01(\x03\x12\x44\n\x06status\x18\r \x01(\x0e\x32\x34.yandex.cloud.serverless.functions.v1.Version.Status\x12\x0c\n\x04tags\x18\x0e \x03(\t\x12\x14\n\x0clog_group_id\x18\x0f \x01(\t\x12S\n\x0b\x65nvironment\x18\x10 \x03(\x0b\x32>.yandex.cloud.serverless.functions.v1.Version.EnvironmentEntry\x12H\n\x0c\x63onnectivity\x18\x11 \x01(\x0b\x32\x32.yandex.cloud.serverless.functions.v1.Connectivity\x12g\n\x16named_service_accounts\x18\x12 \x03(\x0b\x32G.yandex.cloud.serverless.functions.v1.Version.NamedServiceAccountsEntry\x12=\n\x07secrets\x18\x13 \x03(\x0b\x32,.yandex.cloud.serverless.functions.v1.Secret\x12\x45\n\x0blog_options\x18\x14 \x01(\x0b\x32\x30.yandex.cloud.serverless.functions.v1.LogOptions\x12J\n\x0estorage_mounts\x18\x15 \x03(\x0b\x32\x32.yandex.cloud.serverless.functions.v1.StorageMount\x12\\\n\x17\x61sync_invocation_config\x18\x16 \x01(\x0b\x32;.yandex.cloud.serverless.functions.v1.AsyncInvocationConfig\x12\x12\n\ntmpfs_size\x18\x17 \x01(\x03\x12\x1d\n\x0b\x63oncurrency\x18\x18 \x01(\x03\x42\x08\xfa\xc7\x31\x04\x30-16\x1a\x32\n\x10\x45nvironmentEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a;\n\x19NamedServiceAccountsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\":\n\x06Status\x12\x16\n\x12STATUS_UNSPECIFIED\x10\x00\x12\x0c\n\x08\x43REATING\x10\x01\x12\n\n\x06\x41\x43TIVE\x10\x02J\x04\x08\x0b\x10\x0cJ\x04\x08\x04\x10\x05\"5\n\tResources\x12(\n\x06memory\x18\x01 \x01(\x03\x42\x18\xfa\xc7\x31\x14\x31\x33\x34\x32\x31\x37\x37\x32\x38-4294967296\"O\n\x07Package\x12\x19\n\x0b\x62ucket_name\x18\x01 \x01(\tB\x04\xe8\xc7\x31\x01\x12\x19\n\x0bobject_name\x18\x02 \x01(\tB\x04\xe8\xc7\x31\x01\x12\x0e\n\x06sha256\x18\x03 \x01(\t\"A\n\x0c\x43onnectivity\x12\x12\n\nnetwork_id\x18\x01 \x01(\t\x12\x1d\n\tsubnet_id\x18\x02 \x03(\tB\n\x8a\xc8\x31\x02>0\x90\xc8\x31\x01\"\xf8\x01\n\rScalingPolicy\x12\x13\n\x0b\x66unction_id\x18\x01 \x01(\t\x12\x0b\n\x03tag\x18\x02 \x01(\t\x12.\n\ncreated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0bmodified_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12#\n\x1bprovisioned_instances_count\x18\x06 \x01(\x03\x12\x1c\n\x14zone_instances_limit\x18\x07 \x01(\x03\x12\x1b\n\x13zone_requests_limit\x18\x08 \x01(\x03J\x04\x08\x05\x10\x06\"b\n\x06Secret\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nversion_id\x18\x02 \x01(\t\x12\x0b\n\x03key\x18\x03 \x01(\t\x12\x1e\n\x14\x65nvironment_variable\x18\x04 \x01(\tH\x00\x42\x0b\n\treference\"\xe0\x01\n\nLogOptions\x12\x10\n\x08\x64isabled\x18\x01 \x01(\x08\x12;\n\x0clog_group_id\x18\x02 \x01(\tB#\xf2\xc7\x31\x1f([a-zA-Z][-a-zA-Z0-9_.]{0,63})?H\x00\x12\x38\n\tfolder_id\x18\x03 \x01(\tB#\xf2\xc7\x31\x1f([a-zA-Z][-a-zA-Z0-9_.]{0,63})?H\x00\x12:\n\tmin_level\x18\x04 \x01(\x0e\x32\'.yandex.cloud.logging.v1.LogLevel.LevelB\r\n\x0b\x64\x65stination\"\x9f\x01\n\x0cStorageMount\x12\x31\n\tbucket_id\x18\x01 \x01(\tB\x1e\xe8\xc7\x31\x01\xf2\xc7\x31\x0e[-.0-9a-zA-Z]*\x8a\xc8\x31\x04\x33-63\x12\x0e\n\x06prefix\x18\x02 \x01(\t\x12\x39\n\x10mount_point_name\x18\x03 \x01(\tB\x1f\xe8\xc7\x31\x01\xf2\xc7\x31\x0e[-_0-9a-zA-Z]*\x8a\xc8\x31\x05\x31-100\x12\x11\n\tread_only\x18\x04 \x01(\x08\"\xde\x03\n\x15\x41syncInvocationConfig\x12 \n\rretries_count\x18\x01 \x01(\x03\x42\t\xfa\xc7\x31\x05\x30-100\x12h\n\x0esuccess_target\x18\x02 \x01(\x0b\x32J.yandex.cloud.serverless.functions.v1.AsyncInvocationConfig.ResponseTargetB\x04\xe8\xc7\x31\x01\x12h\n\x0e\x66\x61ilure_target\x18\x03 \x01(\x0b\x32J.yandex.cloud.serverless.functions.v1.AsyncInvocationConfig.ResponseTargetB\x04\xe8\xc7\x31\x01\x12\x1a\n\x12service_account_id\x18\x04 \x01(\t\x1a\xb2\x01\n\x0eResponseTarget\x12I\n\x0c\x65mpty_target\x18\x01 \x01(\x0b\x32\x31.yandex.cloud.serverless.functions.v1.EmptyTargetH\x00\x12\x45\n\nymq_target\x18\x02 \x01(\x0b\x32/.yandex.cloud.serverless.functions.v1.YMQTargetH\x00\x42\x0e\n\x06target\x12\x04\xc0\xc1\x31\x01\"N\n\tYMQTarget\x12\x17\n\tqueue_arn\x18\x01 \x01(\tB\x04\xe8\xc7\x31\x01\x12(\n\x12service_account_id\x18\x02 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"\r\n\x0b\x45mptyTargetB~\n(yandex.cloud.api.serverless.functions.v1ZRgithub.com/yandex-cloud/go-genproto/yandex/cloud/serverless/functions/v1;functionsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.serverless.functions.v1.function_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n(yandex.cloud.api.serverless.functions.v1ZRgithub.com/yandex-cloud/go-genproto/yandex/cloud/serverless/functions/v1;functions'
  _FUNCTION_LABELSENTRY._options = None
  _FUNCTION_LABELSENTRY._serialized_options = b'8\001'
  _FUNCTION.fields_by_name['name']._options = None
  _FUNCTION.fields_by_name['name']._serialized_options = b'\212\3101\0043-63'
  _FUNCTION.fields_by_name['description']._options = None
  _FUNCTION.fields_by_name['description']._serialized_options = b'\212\3101\0050-256'
  _FUNCTION.fields_by_name['labels']._options = None
  _FUNCTION.fields_by_name['labels']._serialized_options = b'\202\3101\004<=64'
  _VERSION_ENVIRONMENTENTRY._options = None
  _VERSION_ENVIRONMENTENTRY._serialized_options = b'8\001'
  _VERSION_NAMEDSERVICEACCOUNTSENTRY._options = None
  _VERSION_NAMEDSERVICEACCOUNTSENTRY._serialized_options = b'8\001'
  _VERSION.fields_by_name['description']._options = None
  _VERSION.fields_by_name['description']._serialized_options = b'\212\3101\0050-256'
  _VERSION.fields_by_name['concurrency']._options = None
  _VERSION.fields_by_name['concurrency']._serialized_options = b'\372\3071\0040-16'
  _RESOURCES.fields_by_name['memory']._options = None
  _RESOURCES.fields_by_name['memory']._serialized_options = b'\372\3071\024134217728-4294967296'
  _PACKAGE.fields_by_name['bucket_name']._options = None
  _PACKAGE.fields_by_name['bucket_name']._serialized_options = b'\350\3071\001'
  _PACKAGE.fields_by_name['object_name']._options = None
  _PACKAGE.fields_by_name['object_name']._serialized_options = b'\350\3071\001'
  _CONNECTIVITY.fields_by_name['subnet_id']._options = None
  _CONNECTIVITY.fields_by_name['subnet_id']._serialized_options = b'\212\3101\002>0\220\3101\001'
  _LOGOPTIONS.fields_by_name['log_group_id']._options = None
  _LOGOPTIONS.fields_by_name['log_group_id']._serialized_options = b'\362\3071\037([a-zA-Z][-a-zA-Z0-9_.]{0,63})?'
  _LOGOPTIONS.fields_by_name['folder_id']._options = None
  _LOGOPTIONS.fields_by_name['folder_id']._serialized_options = b'\362\3071\037([a-zA-Z][-a-zA-Z0-9_.]{0,63})?'
  _STORAGEMOUNT.fields_by_name['bucket_id']._options = None
  _STORAGEMOUNT.fields_by_name['bucket_id']._serialized_options = b'\350\3071\001\362\3071\016[-.0-9a-zA-Z]*\212\3101\0043-63'
  _STORAGEMOUNT.fields_by_name['mount_point_name']._options = None
  _STORAGEMOUNT.fields_by_name['mount_point_name']._serialized_options = b'\350\3071\001\362\3071\016[-_0-9a-zA-Z]*\212\3101\0051-100'
  _ASYNCINVOCATIONCONFIG_RESPONSETARGET.oneofs_by_name['target']._options = None
  _ASYNCINVOCATIONCONFIG_RESPONSETARGET.oneofs_by_name['target']._serialized_options = b'\300\3011\001'
  _ASYNCINVOCATIONCONFIG.fields_by_name['retries_count']._options = None
  _ASYNCINVOCATIONCONFIG.fields_by_name['retries_count']._serialized_options = b'\372\3071\0050-100'
  _ASYNCINVOCATIONCONFIG.fields_by_name['success_target']._options = None
  _ASYNCINVOCATIONCONFIG.fields_by_name['success_target']._serialized_options = b'\350\3071\001'
  _ASYNCINVOCATIONCONFIG.fields_by_name['failure_target']._options = None
  _ASYNCINVOCATIONCONFIG.fields_by_name['failure_target']._serialized_options = b'\350\3071\001'
  _YMQTARGET.fields_by_name['queue_arn']._options = None
  _YMQTARGET.fields_by_name['queue_arn']._serialized_options = b'\350\3071\001'
  _YMQTARGET.fields_by_name['service_account_id']._options = None
  _YMQTARGET.fields_by_name['service_account_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_FUNCTION']._serialized_start=231
  _globals['_FUNCTION']._serialized_end=712
  _globals['_FUNCTION_LABELSENTRY']._serialized_start=582
  _globals['_FUNCTION_LABELSENTRY']._serialized_end=627
  _globals['_FUNCTION_STATUS']._serialized_start=629
  _globals['_FUNCTION_STATUS']._serialized_end=712
  _globals['_VERSION']._serialized_start=715
  _globals['_VERSION']._serialized_end=1954
  _globals['_VERSION_ENVIRONMENTENTRY']._serialized_start=1771
  _globals['_VERSION_ENVIRONMENTENTRY']._serialized_end=1821
  _globals['_VERSION_NAMEDSERVICEACCOUNTSENTRY']._serialized_start=1823
  _globals['_VERSION_NAMEDSERVICEACCOUNTSENTRY']._serialized_end=1882
  _globals['_VERSION_STATUS']._serialized_start=629
  _globals['_VERSION_STATUS']._serialized_end=687
  _globals['_RESOURCES']._serialized_start=1956
  _globals['_RESOURCES']._serialized_end=2009
  _globals['_PACKAGE']._serialized_start=2011
  _globals['_PACKAGE']._serialized_end=2090
  _globals['_CONNECTIVITY']._serialized_start=2092
  _globals['_CONNECTIVITY']._serialized_end=2157
  _globals['_SCALINGPOLICY']._serialized_start=2160
  _globals['_SCALINGPOLICY']._serialized_end=2408
  _globals['_SECRET']._serialized_start=2410
  _globals['_SECRET']._serialized_end=2508
  _globals['_LOGOPTIONS']._serialized_start=2511
  _globals['_LOGOPTIONS']._serialized_end=2735
  _globals['_STORAGEMOUNT']._serialized_start=2738
  _globals['_STORAGEMOUNT']._serialized_end=2897
  _globals['_ASYNCINVOCATIONCONFIG']._serialized_start=2900
  _globals['_ASYNCINVOCATIONCONFIG']._serialized_end=3378
  _globals['_ASYNCINVOCATIONCONFIG_RESPONSETARGET']._serialized_start=3200
  _globals['_ASYNCINVOCATIONCONFIG_RESPONSETARGET']._serialized_end=3378
  _globals['_YMQTARGET']._serialized_start=3380
  _globals['_YMQTARGET']._serialized_end=3458
  _globals['_EMPTYTARGET']._serialized_start=3460
  _globals['_EMPTYTARGET']._serialized_end=3473
# @@protoc_insertion_point(module_scope)
