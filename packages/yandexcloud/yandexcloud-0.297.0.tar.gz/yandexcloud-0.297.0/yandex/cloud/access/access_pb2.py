# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/access/access.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n yandex/cloud/access/access.proto\x12\x13yandex.cloud.access\x1a\x1dyandex/cloud/validation.proto\"A\n\x07Subject\x12\x19\n\x02id\x18\x01 \x01(\tB\r\xe8\xc7\x31\x01\x8a\xc8\x31\x05<=100\x12\x1b\n\x04type\x18\x02 \x01(\tB\r\xe8\xc7\x31\x01\x8a\xc8\x31\x05<=100\"c\n\rAccessBinding\x12\x1d\n\x07role_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x33\n\x07subject\x18\x02 \x01(\x0b\x32\x1c.yandex.cloud.access.SubjectB\x04\xe8\xc7\x31\x01\"|\n\x19ListAccessBindingsRequest\x12!\n\x0bresource_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06<=1000\x12\x1d\n\npage_token\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=100\"r\n\x1aListAccessBindingsResponse\x12;\n\x0f\x61\x63\x63\x65ss_bindings\x18\x01 \x03(\x0b\x32\".yandex.cloud.access.AccessBinding\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\x86\x01\n\x18SetAccessBindingsRequest\x12!\n\x0bresource_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12G\n\x0f\x61\x63\x63\x65ss_bindings\x18\x02 \x03(\x0b\x32\".yandex.cloud.access.AccessBindingB\n\x82\xc8\x31\x06<=1000\"0\n\x19SetAccessBindingsMetadata\x12\x13\n\x0bresource_id\x18\x01 \x01(\t\"\x94\x01\n\x1bUpdateAccessBindingsRequest\x12!\n\x0bresource_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12R\n\x15\x61\x63\x63\x65ss_binding_deltas\x18\x02 \x03(\x0b\x32\'.yandex.cloud.access.AccessBindingDeltaB\n\x82\xc8\x31\x06\x31-1000\"3\n\x1cUpdateAccessBindingsMetadata\x12\x13\n\x0bresource_id\x18\x01 \x01(\t\"\x96\x01\n\x12\x41\x63\x63\x65ssBindingDelta\x12>\n\x06\x61\x63tion\x18\x01 \x01(\x0e\x32(.yandex.cloud.access.AccessBindingActionB\x04\xe8\xc7\x31\x01\x12@\n\x0e\x61\x63\x63\x65ss_binding\x18\x02 \x01(\x0b\x32\".yandex.cloud.access.AccessBindingB\x04\xe8\xc7\x31\x01\"b\n\x1d\x41\x63\x63\x65ssBindingsOperationResult\x12\x41\n\x10\x65\x66\x66\x65\x63tive_deltas\x18\x01 \x03(\x0b\x32\'.yandex.cloud.access.AccessBindingDelta*Q\n\x13\x41\x63\x63\x65ssBindingAction\x12%\n!ACCESS_BINDING_ACTION_UNSPECIFIED\x10\x00\x12\x07\n\x03\x41\x44\x44\x10\x01\x12\n\n\x06REMOVE\x10\x02\x42Y\n\x17yandex.cloud.api.accessZ>github.com/yandex-cloud/go-genproto/yandex/cloud/access;accessb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.access.access_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\027yandex.cloud.api.accessZ>github.com/yandex-cloud/go-genproto/yandex/cloud/access;access'
  _SUBJECT.fields_by_name['id']._options = None
  _SUBJECT.fields_by_name['id']._serialized_options = b'\350\3071\001\212\3101\005<=100'
  _SUBJECT.fields_by_name['type']._options = None
  _SUBJECT.fields_by_name['type']._serialized_options = b'\350\3071\001\212\3101\005<=100'
  _ACCESSBINDING.fields_by_name['role_id']._options = None
  _ACCESSBINDING.fields_by_name['role_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _ACCESSBINDING.fields_by_name['subject']._options = None
  _ACCESSBINDING.fields_by_name['subject']._serialized_options = b'\350\3071\001'
  _LISTACCESSBINDINGSREQUEST.fields_by_name['resource_id']._options = None
  _LISTACCESSBINDINGSREQUEST.fields_by_name['resource_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _LISTACCESSBINDINGSREQUEST.fields_by_name['page_size']._options = None
  _LISTACCESSBINDINGSREQUEST.fields_by_name['page_size']._serialized_options = b'\372\3071\006<=1000'
  _LISTACCESSBINDINGSREQUEST.fields_by_name['page_token']._options = None
  _LISTACCESSBINDINGSREQUEST.fields_by_name['page_token']._serialized_options = b'\212\3101\005<=100'
  _SETACCESSBINDINGSREQUEST.fields_by_name['resource_id']._options = None
  _SETACCESSBINDINGSREQUEST.fields_by_name['resource_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _SETACCESSBINDINGSREQUEST.fields_by_name['access_bindings']._options = None
  _SETACCESSBINDINGSREQUEST.fields_by_name['access_bindings']._serialized_options = b'\202\3101\006<=1000'
  _UPDATEACCESSBINDINGSREQUEST.fields_by_name['resource_id']._options = None
  _UPDATEACCESSBINDINGSREQUEST.fields_by_name['resource_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _UPDATEACCESSBINDINGSREQUEST.fields_by_name['access_binding_deltas']._options = None
  _UPDATEACCESSBINDINGSREQUEST.fields_by_name['access_binding_deltas']._serialized_options = b'\202\3101\0061-1000'
  _ACCESSBINDINGDELTA.fields_by_name['action']._options = None
  _ACCESSBINDINGDELTA.fields_by_name['action']._serialized_options = b'\350\3071\001'
  _ACCESSBINDINGDELTA.fields_by_name['access_binding']._options = None
  _ACCESSBINDINGDELTA.fields_by_name['access_binding']._serialized_options = b'\350\3071\001'
  _globals['_ACCESSBINDINGACTION']._serialized_start=1142
  _globals['_ACCESSBINDINGACTION']._serialized_end=1223
  _globals['_SUBJECT']._serialized_start=88
  _globals['_SUBJECT']._serialized_end=153
  _globals['_ACCESSBINDING']._serialized_start=155
  _globals['_ACCESSBINDING']._serialized_end=254
  _globals['_LISTACCESSBINDINGSREQUEST']._serialized_start=256
  _globals['_LISTACCESSBINDINGSREQUEST']._serialized_end=380
  _globals['_LISTACCESSBINDINGSRESPONSE']._serialized_start=382
  _globals['_LISTACCESSBINDINGSRESPONSE']._serialized_end=496
  _globals['_SETACCESSBINDINGSREQUEST']._serialized_start=499
  _globals['_SETACCESSBINDINGSREQUEST']._serialized_end=633
  _globals['_SETACCESSBINDINGSMETADATA']._serialized_start=635
  _globals['_SETACCESSBINDINGSMETADATA']._serialized_end=683
  _globals['_UPDATEACCESSBINDINGSREQUEST']._serialized_start=686
  _globals['_UPDATEACCESSBINDINGSREQUEST']._serialized_end=834
  _globals['_UPDATEACCESSBINDINGSMETADATA']._serialized_start=836
  _globals['_UPDATEACCESSBINDINGSMETADATA']._serialized_end=887
  _globals['_ACCESSBINDINGDELTA']._serialized_start=890
  _globals['_ACCESSBINDINGDELTA']._serialized_end=1040
  _globals['_ACCESSBINDINGSOPERATIONRESULT']._serialized_start=1042
  _globals['_ACCESSBINDINGSOPERATIONRESULT']._serialized_end=1140
# @@protoc_insertion_point(module_scope)
