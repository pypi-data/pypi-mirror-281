# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/loadtesting/agent/v1/trail_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n5yandex/cloud/loadtesting/agent/v1/trail_service.proto\x12!yandex.cloud.loadtesting.agent.v1\x1a\x1cgoogle/api/annotations.proto\"\x94\x01\n\x12\x43reateTrailRequest\x12\x1b\n\x13\x63ompute_instance_id\x18\x01 \x01(\t\x12\x36\n\x04\x64\x61ta\x18\x02 \x03(\x0b\x32(.yandex.cloud.loadtesting.agent.v1.Trail\x12\x0e\n\x06job_id\x18\x03 \x01(\t\x12\x19\n\x11\x61gent_instance_id\x18\x04 \x01(\t\"\xfc\x04\n\x05Trail\x12\x0f\n\x07overall\x18\x01 \x01(\x03\x12\x0f\n\x07\x63\x61se_id\x18\x02 \x01(\t\x12\x0c\n\x04time\x18\x03 \x01(\t\x12\r\n\x05reqps\x18\x04 \x01(\x03\x12\r\n\x05resps\x18\x05 \x01(\x03\x12\x0e\n\x06\x65xpect\x18\x06 \x01(\x01\x12\r\n\x05input\x18\x07 \x01(\x03\x12\x0e\n\x06output\x18\x08 \x01(\x03\x12\x14\n\x0c\x63onnect_time\x18\t \x01(\x01\x12\x11\n\tsend_time\x18\n \x01(\x01\x12\x0f\n\x07latency\x18\x0b \x01(\x01\x12\x14\n\x0creceive_time\x18\x0c \x01(\x01\x12\x0f\n\x07threads\x18\r \x01(\x03\x12\x0b\n\x03q50\x18\x0e \x01(\x01\x12\x0b\n\x03q75\x18\x0f \x01(\x01\x12\x0b\n\x03q80\x18\x10 \x01(\x01\x12\x0b\n\x03q85\x18\x11 \x01(\x01\x12\x0b\n\x03q90\x18\x12 \x01(\x01\x12\x0b\n\x03q95\x18\x13 \x01(\x01\x12\x0b\n\x03q98\x18\x14 \x01(\x01\x12\x0b\n\x03q99\x18\x15 \x01(\x01\x12\x0c\n\x04q100\x18\x16 \x01(\x01\x12\x42\n\nhttp_codes\x18\x17 \x03(\x0b\x32..yandex.cloud.loadtesting.agent.v1.Trail.Codes\x12\x41\n\tnet_codes\x18\x18 \x03(\x0b\x32..yandex.cloud.loadtesting.agent.v1.Trail.Codes\x12J\n\x0etime_intervals\x18\x19 \x03(\x0b\x32\x32.yandex.cloud.loadtesting.agent.v1.Trail.Intervals\x1a$\n\x05\x43odes\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x03\x12\r\n\x05\x63ount\x18\x02 \x01(\x03\x1a&\n\tIntervals\x12\n\n\x02to\x18\x01 \x01(\x01\x12\r\n\x05\x63ount\x18\x02 \x01(\x03\"5\n\x13\x43reateTrailResponse\x12\x10\n\x08trail_id\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\x03\x32\xb1\x01\n\x0cTrailService\x12\xa0\x01\n\x06\x43reate\x12\x35.yandex.cloud.loadtesting.agent.v1.CreateTrailRequest\x1a\x36.yandex.cloud.loadtesting.agent.v1.CreateTrailResponse\"\'\x82\xd3\xe4\x93\x02!\"\x1c/loadtesting/agent/v1/trails:\x01*Bt\n%yandex.cloud.api.loadtesting.agent.v1ZKgithub.com/yandex-cloud/go-genproto/yandex/cloud/loadtesting/agent/v1;agentb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.loadtesting.agent.v1.trail_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n%yandex.cloud.api.loadtesting.agent.v1ZKgithub.com/yandex-cloud/go-genproto/yandex/cloud/loadtesting/agent/v1;agent'
  _TRAILSERVICE.methods_by_name['Create']._options = None
  _TRAILSERVICE.methods_by_name['Create']._serialized_options = b'\202\323\344\223\002!\"\034/loadtesting/agent/v1/trails:\001*'
  _globals['_CREATETRAILREQUEST']._serialized_start=123
  _globals['_CREATETRAILREQUEST']._serialized_end=271
  _globals['_TRAIL']._serialized_start=274
  _globals['_TRAIL']._serialized_end=910
  _globals['_TRAIL_CODES']._serialized_start=834
  _globals['_TRAIL_CODES']._serialized_end=870
  _globals['_TRAIL_INTERVALS']._serialized_start=872
  _globals['_TRAIL_INTERVALS']._serialized_end=910
  _globals['_CREATETRAILRESPONSE']._serialized_start=912
  _globals['_CREATETRAILRESPONSE']._serialized_end=965
  _globals['_TRAILSERVICE']._serialized_start=968
  _globals['_TRAILSERVICE']._serialized_end=1145
# @@protoc_insertion_point(module_scope)
