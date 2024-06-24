# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/datatransfer/v1/transfer.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from yandex.cloud.datatransfer.v1 import endpoint_pb2 as yandex_dot_cloud_dot_datatransfer_dot_v1_dot_endpoint__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+yandex/cloud/datatransfer/v1/transfer.proto\x12\x1cyandex.cloud.datatransfer.v1\x1a+yandex/cloud/datatransfer/v1/endpoint.proto\"\xe7\x04\n\x08Transfer\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\tfolder_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x42\n\x06labels\x18\x06 \x03(\x0b\x32\x32.yandex.cloud.datatransfer.v1.Transfer.LabelsEntry\x12\x36\n\x06source\x18\x07 \x01(\x0b\x32&.yandex.cloud.datatransfer.v1.Endpoint\x12\x36\n\x06target\x18\x08 \x01(\x0b\x32&.yandex.cloud.datatransfer.v1.Endpoint\x12\x36\n\x07runtime\x18\t \x01(\x0b\x32%.yandex.cloud.datatransfer.v1.Runtime\x12<\n\x06status\x18\n \x01(\x0e\x32,.yandex.cloud.datatransfer.v1.TransferStatus\x12\x38\n\x04type\x18\x0c \x01(\x0e\x32*.yandex.cloud.datatransfer.v1.TransferType\x12\x0f\n\x07warning\x18\x0f \x01(\t\x12\x44\n\x0etransformation\x18\x11 \x01(\x0b\x32,.yandex.cloud.datatransfer.v1.Transformation\x12\x11\n\tprestable\x18\x16 \x01(\x08\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01J\x04\x08\x03\x10\x04J\x04\x08\x0b\x10\x0cJ\x04\x08\r\x10\x0fJ\x04\x08\x10\x10\x11J\x04\x08\x12\x10\x16\"Y\n\x07Runtime\x12=\n\nyc_runtime\x18\x04 \x01(\x0b\x32\'.yandex.cloud.datatransfer.v1.YcRuntimeH\x00\x42\t\n\x07runtimeJ\x04\x08\x01\x10\x04\"@\n\x14ShardingUploadParams\x12\x11\n\tjob_count\x18\x01 \x01(\x03\x12\x15\n\rprocess_count\x18\x02 \x01(\x03\"u\n\tYcRuntime\x12\x11\n\tjob_count\x18\x01 \x01(\x03\x12O\n\x13upload_shard_params\x18\x08 \x01(\x0b\x32\x32.yandex.cloud.datatransfer.v1.ShardingUploadParamsJ\x04\x08\x02\x10\x08\"m\n\x0cMaskFunction\x12L\n\x12mask_function_hash\x18\x01 \x01(\x0b\x32..yandex.cloud.datatransfer.v1.MaskFunctionHashH\x00\x42\x0f\n\rmask_function\"-\n\x10MaskFunctionHash\x12\x19\n\x11user_defined_salt\x18\x01 \x01(\t\">\n\x0cTablesFilter\x12\x16\n\x0einclude_tables\x18\x01 \x03(\t\x12\x16\n\x0e\x65xclude_tables\x18\x02 \x03(\t\"A\n\rColumnsFilter\x12\x17\n\x0finclude_columns\x18\x01 \x03(\t\x12\x17\n\x0f\x65xclude_columns\x18\x02 \x03(\t\"\xa1\x01\n\x14MaskFieldTransformer\x12:\n\x06tables\x18\x01 \x01(\x0b\x32*.yandex.cloud.datatransfer.v1.TablesFilter\x12\x0f\n\x07\x63olumns\x18\x02 \x03(\t\x12<\n\x08\x66unction\x18\x03 \x01(\x0b\x32*.yandex.cloud.datatransfer.v1.MaskFunction\"\x94\x01\n\x18\x46ilterColumnsTransformer\x12:\n\x06tables\x18\x01 \x01(\x0b\x32*.yandex.cloud.datatransfer.v1.TablesFilter\x12<\n\x07\x63olumns\x18\x02 \x01(\x0b\x32+.yandex.cloud.datatransfer.v1.ColumnsFilter\")\n\x05Table\x12\x12\n\nname_space\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"\x80\x01\n\x0bRenameTable\x12:\n\roriginal_name\x18\x01 \x01(\x0b\x32#.yandex.cloud.datatransfer.v1.Table\x12\x35\n\x08new_name\x18\x02 \x01(\x0b\x32#.yandex.cloud.datatransfer.v1.Table\"[\n\x17RenameTablesTransformer\x12@\n\rrename_tables\x18\x01 \x03(\x0b\x32).yandex.cloud.datatransfer.v1.RenameTable\"h\n\x1cReplacePrimaryKeyTransformer\x12:\n\x06tables\x18\x01 \x01(\x0b\x32*.yandex.cloud.datatransfer.v1.TablesFilter\x12\x0c\n\x04keys\x18\x02 \x03(\t\"\x8f\x01\n\x13ToStringTransformer\x12:\n\x06tables\x18\x01 \x01(\x0b\x32*.yandex.cloud.datatransfer.v1.TablesFilter\x12<\n\x07\x63olumns\x18\x02 \x01(\x0b\x32+.yandex.cloud.datatransfer.v1.ColumnsFilter\"\xa4\x01\n\x12SharderTransformer\x12:\n\x06tables\x18\x01 \x01(\x0b\x32*.yandex.cloud.datatransfer.v1.TablesFilter\x12<\n\x07\x63olumns\x18\x02 \x01(\x0b\x32+.yandex.cloud.datatransfer.v1.ColumnsFilter\x12\x14\n\x0cshards_count\x18\x03 \x01(\x03\"y\n\x18TableSplitterTransformer\x12:\n\x06tables\x18\x01 \x01(\x0b\x32*.yandex.cloud.datatransfer.v1.TablesFilter\x12\x0f\n\x07\x63olumns\x18\x02 \x03(\t\x12\x10\n\x08splitter\x18\x03 \x01(\t\"c\n\x15\x46ilterRowsTransformer\x12:\n\x06tables\x18\x01 \x01(\x0b\x32*.yandex.cloud.datatransfer.v1.TablesFilter\x12\x0e\n\x06\x66ilter\x18\x02 \x01(\t\"\xc6\x05\n\x0bTransformer\x12H\n\nmask_field\x18\x01 \x01(\x0b\x32\x32.yandex.cloud.datatransfer.v1.MaskFieldTransformerH\x00\x12P\n\x0e\x66ilter_columns\x18\x02 \x01(\x0b\x32\x36.yandex.cloud.datatransfer.v1.FilterColumnsTransformerH\x00\x12N\n\rrename_tables\x18\x04 \x01(\x0b\x32\x35.yandex.cloud.datatransfer.v1.RenameTablesTransformerH\x00\x12Y\n\x13replace_primary_key\x18\x06 \x01(\x0b\x32:.yandex.cloud.datatransfer.v1.ReplacePrimaryKeyTransformerH\x00\x12N\n\x11\x63onvert_to_string\x18\x07 \x01(\x0b\x32\x31.yandex.cloud.datatransfer.v1.ToStringTransformerH\x00\x12O\n\x13sharder_transformer\x18\t \x01(\x0b\x32\x30.yandex.cloud.datatransfer.v1.SharderTransformerH\x00\x12\\\n\x1atable_splitter_transformer\x18\r \x01(\x0b\x32\x36.yandex.cloud.datatransfer.v1.TableSplitterTransformerH\x00\x12J\n\x0b\x66ilter_rows\x18\x0e \x01(\x0b\x32\x33.yandex.cloud.datatransfer.v1.FilterRowsTransformerH\x00\x42\r\n\x0btransformerJ\x04\x08\x03\x10\x04J\x04\x08\x05\x10\x06J\x04\x08\x08\x10\tJ\x04\x08\n\x10\r\"Q\n\x0eTransformation\x12?\n\x0ctransformers\x18\x01 \x03(\x0b\x32).yandex.cloud.datatransfer.v1.Transformer*p\n\x0cTransferType\x12\x1d\n\x19TRANSFER_TYPE_UNSPECIFIED\x10\x00\x12\x1a\n\x16SNAPSHOT_AND_INCREMENT\x10\x01\x12\x11\n\rSNAPSHOT_ONLY\x10\x02\x12\x12\n\x0eINCREMENT_ONLY\x10\x03*\x9b\x01\n\x0eTransferStatus\x12\x1f\n\x1bTRANSFER_STATUS_UNSPECIFIED\x10\x00\x12\x0c\n\x08\x43REATING\x10\x01\x12\x0b\n\x07\x43REATED\x10\x02\x12\x0b\n\x07RUNNING\x10\x03\x12\x0c\n\x08STOPPING\x10\x04\x12\x0b\n\x07STOPPED\x10\x05\x12\t\n\x05\x45RROR\x10\x06\x12\x10\n\x0cSNAPSHOTTING\x10\x07\x12\x08\n\x04\x44ONE\x10\x08\x42q\n yandex.cloud.api.datatransfer.v1ZMgithub.com/yandex-cloud/go-genproto/yandex/cloud/datatransfer/v1;datatransferb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.datatransfer.v1.transfer_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n yandex.cloud.api.datatransfer.v1ZMgithub.com/yandex-cloud/go-genproto/yandex/cloud/datatransfer/v1;datatransfer'
  _TRANSFER_LABELSENTRY._options = None
  _TRANSFER_LABELSENTRY._serialized_options = b'8\001'
  _globals['_TRANSFERTYPE']._serialized_start=3326
  _globals['_TRANSFERTYPE']._serialized_end=3438
  _globals['_TRANSFERSTATUS']._serialized_start=3441
  _globals['_TRANSFERSTATUS']._serialized_end=3596
  _globals['_TRANSFER']._serialized_start=123
  _globals['_TRANSFER']._serialized_end=738
  _globals['_TRANSFER_LABELSENTRY']._serialized_start=663
  _globals['_TRANSFER_LABELSENTRY']._serialized_end=708
  _globals['_RUNTIME']._serialized_start=740
  _globals['_RUNTIME']._serialized_end=829
  _globals['_SHARDINGUPLOADPARAMS']._serialized_start=831
  _globals['_SHARDINGUPLOADPARAMS']._serialized_end=895
  _globals['_YCRUNTIME']._serialized_start=897
  _globals['_YCRUNTIME']._serialized_end=1014
  _globals['_MASKFUNCTION']._serialized_start=1016
  _globals['_MASKFUNCTION']._serialized_end=1125
  _globals['_MASKFUNCTIONHASH']._serialized_start=1127
  _globals['_MASKFUNCTIONHASH']._serialized_end=1172
  _globals['_TABLESFILTER']._serialized_start=1174
  _globals['_TABLESFILTER']._serialized_end=1236
  _globals['_COLUMNSFILTER']._serialized_start=1238
  _globals['_COLUMNSFILTER']._serialized_end=1303
  _globals['_MASKFIELDTRANSFORMER']._serialized_start=1306
  _globals['_MASKFIELDTRANSFORMER']._serialized_end=1467
  _globals['_FILTERCOLUMNSTRANSFORMER']._serialized_start=1470
  _globals['_FILTERCOLUMNSTRANSFORMER']._serialized_end=1618
  _globals['_TABLE']._serialized_start=1620
  _globals['_TABLE']._serialized_end=1661
  _globals['_RENAMETABLE']._serialized_start=1664
  _globals['_RENAMETABLE']._serialized_end=1792
  _globals['_RENAMETABLESTRANSFORMER']._serialized_start=1794
  _globals['_RENAMETABLESTRANSFORMER']._serialized_end=1885
  _globals['_REPLACEPRIMARYKEYTRANSFORMER']._serialized_start=1887
  _globals['_REPLACEPRIMARYKEYTRANSFORMER']._serialized_end=1991
  _globals['_TOSTRINGTRANSFORMER']._serialized_start=1994
  _globals['_TOSTRINGTRANSFORMER']._serialized_end=2137
  _globals['_SHARDERTRANSFORMER']._serialized_start=2140
  _globals['_SHARDERTRANSFORMER']._serialized_end=2304
  _globals['_TABLESPLITTERTRANSFORMER']._serialized_start=2306
  _globals['_TABLESPLITTERTRANSFORMER']._serialized_end=2427
  _globals['_FILTERROWSTRANSFORMER']._serialized_start=2429
  _globals['_FILTERROWSTRANSFORMER']._serialized_end=2528
  _globals['_TRANSFORMER']._serialized_start=2531
  _globals['_TRANSFORMER']._serialized_end=3241
  _globals['_TRANSFORMATION']._serialized_start=3243
  _globals['_TRANSFORMATION']._serialized_end=3324
# @@protoc_insertion_point(module_scope)
