# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/ai/foundation_models/v1/image_generation/image_generation.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nLyandex/cloud/ai/foundation_models/v1/image_generation/image_generation.proto\x12\x35yandex.cloud.ai.foundation_models.v1.image_generation\"\'\n\x07Message\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x0e\n\x06weight\x18\x02 \x01(\x01\"8\n\x0b\x41spectRatio\x12\x13\n\x0bwidth_ratio\x18\x01 \x01(\x03\x12\x14\n\x0cheight_ratio\x18\x02 \x01(\x03\"\x93\x01\n\x16ImageGenerationOptions\x12\x11\n\tmime_type\x18\x01 \x01(\t\x12\x0c\n\x04seed\x18\x02 \x01(\x03\x12X\n\x0c\x61spect_ratio\x18\x03 \x01(\x0b\x32\x42.yandex.cloud.ai.foundation_models.v1.image_generation.AspectRatioB\xa7\x01\n9yandex.cloud.api.ai.foundation_models.v1.image_generationZjgithub.com/yandex-cloud/go-genproto/yandex/cloud/ai/foundation_models/v1/image_generation;image_generationb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.ai.foundation_models.v1.image_generation.image_generation_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n9yandex.cloud.api.ai.foundation_models.v1.image_generationZjgithub.com/yandex-cloud/go-genproto/yandex/cloud/ai/foundation_models/v1/image_generation;image_generation'
  _globals['_MESSAGE']._serialized_start=135
  _globals['_MESSAGE']._serialized_end=174
  _globals['_ASPECTRATIO']._serialized_start=176
  _globals['_ASPECTRATIO']._serialized_end=232
  _globals['_IMAGEGENERATIONOPTIONS']._serialized_start=235
  _globals['_IMAGEGENERATIONOPTIONS']._serialized_end=382
# @@protoc_insertion_point(module_scope)
