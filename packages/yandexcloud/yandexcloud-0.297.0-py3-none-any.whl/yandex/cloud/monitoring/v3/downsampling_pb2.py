# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/monitoring/v3/downsampling.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-yandex/cloud/monitoring/v3/downsampling.proto\x12\x1ayandex.cloud.monitoring.v3\"\xbd\x04\n\x0c\x44ownsampling\x12\x14\n\nmax_points\x18\x01 \x01(\x03H\x00\x12\x17\n\rgrid_interval\x18\x02 \x01(\x03H\x00\x12\x12\n\x08\x64isabled\x18\x03 \x01(\x08H\x00\x12R\n\x10grid_aggregation\x18\x04 \x01(\x0e\x32\x38.yandex.cloud.monitoring.v3.Downsampling.GridAggregation\x12H\n\x0bgap_filling\x18\x05 \x01(\x0e\x32\x33.yandex.cloud.monitoring.v3.Downsampling.GapFilling\"\xd2\x01\n\x0fGridAggregation\x12 \n\x1cGRID_AGGREGATION_UNSPECIFIED\x10\x00\x12\x18\n\x14GRID_AGGREGATION_MAX\x10\x01\x12\x18\n\x14GRID_AGGREGATION_MIN\x10\x02\x12\x18\n\x14GRID_AGGREGATION_SUM\x10\x03\x12\x18\n\x14GRID_AGGREGATION_AVG\x10\x04\x12\x19\n\x15GRID_AGGREGATION_LAST\x10\x05\x12\x1a\n\x16GRID_AGGREGATION_COUNT\x10\x06\"o\n\nGapFilling\x12\x1b\n\x17GAP_FILLING_UNSPECIFIED\x10\x00\x12\x14\n\x10GAP_FILLING_NULL\x10\x01\x12\x14\n\x10GAP_FILLING_NONE\x10\x02\x12\x18\n\x14GAP_FILLING_PREVIOUS\x10\x03\x42\x06\n\x04modeBk\n\x1eyandex.cloud.api.monitoring.v3ZIgithub.com/yandex-cloud/go-genproto/yandex/cloud/monitoring/v3;monitoringb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.monitoring.v3.downsampling_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\036yandex.cloud.api.monitoring.v3ZIgithub.com/yandex-cloud/go-genproto/yandex/cloud/monitoring/v3;monitoring'
  _globals['_DOWNSAMPLING']._serialized_start=78
  _globals['_DOWNSAMPLING']._serialized_end=651
  _globals['_DOWNSAMPLING_GRIDAGGREGATION']._serialized_start=320
  _globals['_DOWNSAMPLING_GRIDAGGREGATION']._serialized_end=530
  _globals['_DOWNSAMPLING_GAPFILLING']._serialized_start=532
  _globals['_DOWNSAMPLING_GAPFILLING']._serialized_end=643
# @@protoc_insertion_point(module_scope)
