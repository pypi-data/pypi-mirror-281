# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/ai/llm/v1alpha/llm.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%yandex/cloud/ai/llm/v1alpha/llm.proto\x12\x1byandex.cloud.ai.llm.v1alpha\x1a\x1egoogle/protobuf/wrappers.proto\"\x90\x01\n\x11GenerationOptions\x12\x17\n\x0fpartial_results\x18\x01 \x01(\x08\x12\x31\n\x0btemperature\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12/\n\nmax_tokens\x18\x03 \x01(\x0b\x32\x1b.google.protobuf.Int64Value\">\n\x0b\x41lternative\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\r\n\x05score\x18\x02 \x01(\x01\x12\x12\n\nnum_tokens\x18\x03 \x01(\x03\"%\n\x07Message\x12\x0c\n\x04role\x18\x01 \x01(\t\x12\x0c\n\x04text\x18\x02 \x01(\t\"2\n\x05Token\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x0c\n\x04text\x18\x02 \x01(\t\x12\x0f\n\x07special\x18\x03 \x01(\x08\x42\x66\n\x1fyandex.cloud.api.ai.llm.v1alphaZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/ai/llm/v1alpha;llmb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.ai.llm.v1alpha.llm_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\037yandex.cloud.api.ai.llm.v1alphaZCgithub.com/yandex-cloud/go-genproto/yandex/cloud/ai/llm/v1alpha;llm'
  _globals['_GENERATIONOPTIONS']._serialized_start=103
  _globals['_GENERATIONOPTIONS']._serialized_end=247
  _globals['_ALTERNATIVE']._serialized_start=249
  _globals['_ALTERNATIVE']._serialized_end=311
  _globals['_MESSAGE']._serialized_start=313
  _globals['_MESSAGE']._serialized_end=350
  _globals['_TOKEN']._serialized_start=352
  _globals['_TOKEN']._serialized_end=402
# @@protoc_insertion_point(module_scope)
