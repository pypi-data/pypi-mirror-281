# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/speechsense/v1/text.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&yandex/cloud/speechsense/v1/text.proto\x12\x1byandex.cloud.speechsense.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"E\n\x0bTextContent\x12\x36\n\x08messages\x18\x01 \x03(\x0b\x32$.yandex.cloud.speechsense.v1.Message\"\x8e\x01\n\x07Message\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12-\n\ttimestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x38\n\x04text\x18\x03 \x01(\x0b\x32(.yandex.cloud.speechsense.v1.TextPayloadH\x00\x42\t\n\x07payload\"\x1b\n\x0bTextPayload\x12\x0c\n\x04text\x18\x01 \x01(\tBy\n\x1fyandex.cloud.api.speechsense.v1B\tTextProtoZKgithub.com/yandex-cloud/go-genproto/yandex/cloud/speechsense/v1;speechsenseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.speechsense.v1.text_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\037yandex.cloud.api.speechsense.v1B\tTextProtoZKgithub.com/yandex-cloud/go-genproto/yandex/cloud/speechsense/v1;speechsense'
  _globals['_TEXTCONTENT']._serialized_start=104
  _globals['_TEXTCONTENT']._serialized_end=173
  _globals['_MESSAGE']._serialized_start=176
  _globals['_MESSAGE']._serialized_end=318
  _globals['_TEXTPAYLOAD']._serialized_start=320
  _globals['_TEXTPAYLOAD']._serialized_end=347
# @@protoc_insertion_point(module_scope)
