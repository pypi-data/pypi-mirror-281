# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/speechsense/v1/analysis/text_classifiers.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n;yandex/cloud/speechsense/v1/analysis/text_classifiers.proto\x12$yandex.cloud.speechsense.v1.analysis\x1a\x1egoogle/protobuf/wrappers.proto\"l\n\x0fTextClassifiers\x12Y\n\x15\x63lassification_result\x18\x01 \x03(\x0b\x32:.yandex.cloud.speechsense.v1.analysis.ClassificationResult\"\x85\x01\n\x14\x43lassificationResult\x12\x12\n\nclassifier\x18\x01 \x01(\t\x12Y\n\x15\x63lassifier_statistics\x18\x02 \x03(\x0b\x32:.yandex.cloud.speechsense.v1.analysis.ClassifierStatistics\"\xa5\x01\n\x14\x43lassifierStatistics\x12\x33\n\x0e\x63hannel_number\x18\x01 \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12\x13\n\x0btotal_count\x18\x02 \x01(\x03\x12\x43\n\nhistograms\x18\x03 \x03(\x0b\x32/.yandex.cloud.speechsense.v1.analysis.Histogram\"!\n\tHistogram\x12\x14\n\x0c\x63ount_values\x18\x01 \x03(\x03\x42\x96\x01\n(yandex.cloud.api.speechsense.v1.analysisB\x14TextClassifiersProtoZTgithub.com/yandex-cloud/go-genproto/yandex/cloud/speechsense/v1/analysis;speechsenseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.speechsense.v1.analysis.text_classifiers_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n(yandex.cloud.api.speechsense.v1.analysisB\024TextClassifiersProtoZTgithub.com/yandex-cloud/go-genproto/yandex/cloud/speechsense/v1/analysis;speechsense'
  _globals['_TEXTCLASSIFIERS']._serialized_start=133
  _globals['_TEXTCLASSIFIERS']._serialized_end=241
  _globals['_CLASSIFICATIONRESULT']._serialized_start=244
  _globals['_CLASSIFICATIONRESULT']._serialized_end=377
  _globals['_CLASSIFIERSTATISTICS']._serialized_start=380
  _globals['_CLASSIFIERSTATISTICS']._serialized_end=545
  _globals['_HISTOGRAM']._serialized_start=547
  _globals['_HISTOGRAM']._serialized_end=580
# @@protoc_insertion_point(module_scope)
