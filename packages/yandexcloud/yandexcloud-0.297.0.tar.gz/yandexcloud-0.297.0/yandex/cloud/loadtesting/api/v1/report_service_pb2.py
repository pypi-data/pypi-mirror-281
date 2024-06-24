# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/loadtesting/api/v1/report_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from yandex.cloud.loadtesting.api.v1.report.table import report_pb2 as yandex_dot_cloud_dot_loadtesting_dot_api_dot_v1_dot_report_dot_table_dot_report__pb2
from yandex.cloud.loadtesting.api.v1.report import status_pb2 as yandex_dot_cloud_dot_loadtesting_dot_api_dot_v1_dot_report_dot_status__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n4yandex/cloud/loadtesting/api/v1/report_service.proto\x12\x1fyandex.cloud.loadtesting.api.v1\x1a\x1cgoogle/api/annotations.proto\x1a\x39yandex/cloud/loadtesting/api/v1/report/table/report.proto\x1a\x33yandex/cloud/loadtesting/api/v1/report/status.proto\x1a\x1dyandex/cloud/validation.proto\".\n\x15GetTableReportRequest\x12\x15\n\x07test_id\x18\x01 \x01(\tB\x04\xe8\xc7\x31\x01\"\xd6\x02\n\x16GetTableReportResponse\x12>\n\x06status\x18\x01 \x01(\x0e\x32..yandex.cloud.loadtesting.api.v1.report.Status\x12\x45\n\x07overall\x18\x02 \x01(\x0b\x32\x34.yandex.cloud.loadtesting.api.v1.report.table.Report\x12Q\n\x05\x63\x61ses\x18\x03 \x03(\x0b\x32\x42.yandex.cloud.loadtesting.api.v1.GetTableReportResponse.CasesEntry\x1a\x62\n\nCasesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x43\n\x05value\x18\x02 \x01(\x0b\x32\x34.yandex.cloud.loadtesting.api.v1.report.table.Report:\x02\x38\x01\x32\xc2\x01\n\rReportService\x12\xb0\x01\n\x08GetTable\x12\x36.yandex.cloud.loadtesting.api.v1.GetTableReportRequest\x1a\x37.yandex.cloud.loadtesting.api.v1.GetTableReportResponse\"3\x82\xd3\xe4\x93\x02-\x12+/loadtesting/api/v1/reports/{test_id}/tableBv\n#yandex.cloud.api.loadtesting.api.v1ZOgithub.com/yandex-cloud/go-genproto/yandex/cloud/loadtesting/api/v1;loadtestingb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.loadtesting.api.v1.report_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n#yandex.cloud.api.loadtesting.api.v1ZOgithub.com/yandex-cloud/go-genproto/yandex/cloud/loadtesting/api/v1;loadtesting'
  _GETTABLEREPORTREQUEST.fields_by_name['test_id']._options = None
  _GETTABLEREPORTREQUEST.fields_by_name['test_id']._serialized_options = b'\350\3071\001'
  _GETTABLEREPORTRESPONSE_CASESENTRY._options = None
  _GETTABLEREPORTRESPONSE_CASESENTRY._serialized_options = b'8\001'
  _REPORTSERVICE.methods_by_name['GetTable']._options = None
  _REPORTSERVICE.methods_by_name['GetTable']._serialized_options = b'\202\323\344\223\002-\022+/loadtesting/api/v1/reports/{test_id}/table'
  _globals['_GETTABLEREPORTREQUEST']._serialized_start=262
  _globals['_GETTABLEREPORTREQUEST']._serialized_end=308
  _globals['_GETTABLEREPORTRESPONSE']._serialized_start=311
  _globals['_GETTABLEREPORTRESPONSE']._serialized_end=653
  _globals['_GETTABLEREPORTRESPONSE_CASESENTRY']._serialized_start=555
  _globals['_GETTABLEREPORTRESPONSE_CASESENTRY']._serialized_end=653
  _globals['_REPORTSERVICE']._serialized_start=656
  _globals['_REPORTSERVICE']._serialized_end=850
# @@protoc_insertion_point(module_scope)
