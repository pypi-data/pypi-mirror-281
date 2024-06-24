# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/apploadbalancer/v1/load_balancer_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from yandex.cloud.api import operation_pb2 as yandex_dot_cloud_dot_api_dot_operation__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2
from yandex.cloud.apploadbalancer.v1 import load_balancer_pb2 as yandex_dot_cloud_dot_apploadbalancer_dot_v1_dot_load__balancer__pb2
from yandex.cloud.apploadbalancer.v1 import logging_pb2 as yandex_dot_cloud_dot_apploadbalancer_dot_v1_dot_logging__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n;yandex/cloud/apploadbalancer/v1/load_balancer_service.proto\x12\x1fyandex.cloud.apploadbalancer.v1\x1a\x1cgoogle/api/annotations.proto\x1a google/protobuf/field_mask.proto\x1a yandex/cloud/api/operation.proto\x1a&yandex/cloud/operation/operation.proto\x1a\x33yandex/cloud/apploadbalancer/v1/load_balancer.proto\x1a-yandex/cloud/apploadbalancer/v1/logging.proto\x1a\x1dyandex/cloud/validation.proto\"8\n\x16GetLoadBalancerRequest\x12\x1e\n\x10load_balancer_id\x18\x01 \x01(\tB\x04\xe8\xc7\x31\x01\"\x8d\x01\n\x18ListLoadBalancersRequest\x12\x17\n\tfolder_id\x18\x01 \x01(\tB\x04\xe8\xc7\x31\x01\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06\x30-1000\x12\x1d\n\npage_token\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=100\x12\x1a\n\x06\x66ilter\x18\x04 \x01(\tB\n\x8a\xc8\x31\x06<=1000\"{\n\x19ListLoadBalancersResponse\x12\x45\n\x0eload_balancers\x18\x01 \x03(\x0b\x32-.yandex.cloud.apploadbalancer.v1.LoadBalancer\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\";\n\x19\x44\x65leteLoadBalancerRequest\x12\x1e\n\x10load_balancer_id\x18\x01 \x01(\tB\x04\xe8\xc7\x31\x01\"6\n\x1a\x44\x65leteLoadBalancerMetadata\x12\x18\n\x10load_balancer_id\x18\x01 \x01(\t\"\xcf\x05\n\x19UpdateLoadBalancerRequest\x12\x1e\n\x10load_balancer_id\x18\x01 \x01(\tB\x04\xe8\xc7\x31\x01\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12\x34\n\x04name\x18\x03 \x01(\tB&\xf2\xc7\x31\"([a-z]([-a-z0-9]{0,61}[a-z0-9])?)?\x12\x1e\n\x0b\x64\x65scription\x18\x04 \x01(\tB\t\x8a\xc8\x31\x05<=256\x12\x9b\x01\n\x06labels\x18\x05 \x03(\x0b\x32\x46.yandex.cloud.apploadbalancer.v1.UpdateLoadBalancerRequest.LabelsEntryBC\xf2\xc7\x31\x0f[-_./\\@0-9a-z]*\x82\xc8\x31\x04<=64\x8a\xc8\x31\x04<=63\xb2\xc8\x31\x1c\x12\x14[a-z][-_./\\@0-9a-z]*\x1a\x04\x31-63\x12\x45\n\x0elistener_specs\x18\x06 \x03(\x0b\x32-.yandex.cloud.apploadbalancer.v1.ListenerSpec\x12L\n\x11\x61llocation_policy\x18\x07 \x01(\x0b\x32\x31.yandex.cloud.apploadbalancer.v1.AllocationPolicy\x12\x1a\n\x12security_group_ids\x18\x08 \x03(\t\x12K\n\x11\x61uto_scale_policy\x18\t \x01(\x0b\x32\x30.yandex.cloud.apploadbalancer.v1.AutoScalePolicy\x12@\n\x0blog_options\x18\n \x01(\x0b\x32+.yandex.cloud.apploadbalancer.v1.LogOptions\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"6\n\x1aUpdateLoadBalancerMetadata\x12\x18\n\x10load_balancer_id\x18\x01 \x01(\t\"\xca\x05\n\x19\x43reateLoadBalancerRequest\x12\x17\n\tfolder_id\x18\x01 \x01(\tB\x04\xe8\xc7\x31\x01\x12\x34\n\x04name\x18\x02 \x01(\tB&\xf2\xc7\x31\"([a-z]([-a-z0-9]{0,61}[a-z0-9])?)?\x12\x1e\n\x0b\x64\x65scription\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=256\x12\x9b\x01\n\x06labels\x18\x04 \x03(\x0b\x32\x46.yandex.cloud.apploadbalancer.v1.CreateLoadBalancerRequest.LabelsEntryBC\xf2\xc7\x31\x0f[-_./\\@0-9a-z]*\x82\xc8\x31\x04<=64\x8a\xc8\x31\x04<=63\xb2\xc8\x31\x1c\x12\x14[a-z][-_./\\@0-9a-z]*\x1a\x04\x31-63\x12\x17\n\tregion_id\x18\x05 \x01(\tB\x04\xe8\xc7\x31\x01\x12\x18\n\nnetwork_id\x18\x06 \x01(\tB\x04\xe8\xc7\x31\x01\x12\x45\n\x0elistener_specs\x18\x07 \x03(\x0b\x32-.yandex.cloud.apploadbalancer.v1.ListenerSpec\x12L\n\x11\x61llocation_policy\x18\x08 \x01(\x0b\x32\x31.yandex.cloud.apploadbalancer.v1.AllocationPolicy\x12\x1a\n\x12security_group_ids\x18\t \x03(\t\x12K\n\x11\x61uto_scale_policy\x18\n \x01(\x0b\x32\x30.yandex.cloud.apploadbalancer.v1.AutoScalePolicy\x12@\n\x0blog_options\x18\x0b \x01(\x0b\x32+.yandex.cloud.apploadbalancer.v1.LogOptions\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"6\n\x1a\x43reateLoadBalancerMetadata\x12\x18\n\x10load_balancer_id\x18\x01 \x01(\t\":\n\x18StartLoadBalancerRequest\x12\x1e\n\x10load_balancer_id\x18\x01 \x01(\tB\x04\xe8\xc7\x31\x01\"5\n\x19StartLoadBalancerMetadata\x12\x18\n\x10load_balancer_id\x18\x01 \x01(\t\"9\n\x17StopLoadBalancerRequest\x12\x1e\n\x10load_balancer_id\x18\x01 \x01(\tB\x04\xe8\xc7\x31\x01\"4\n\x18StopLoadBalancerMetadata\x12\x18\n\x10load_balancer_id\x18\x01 \x01(\t\"\x80\x01\n\x12\x41\x64\x64ListenerRequest\x12\x1e\n\x10load_balancer_id\x18\x01 \x01(\tB\x04\xe8\xc7\x31\x01\x12J\n\rlistener_spec\x18\x02 \x01(\x0b\x32-.yandex.cloud.apploadbalancer.v1.ListenerSpecB\x04\xe8\xc7\x31\x01\"F\n\x13\x41\x64\x64ListenerMetadata\x12\x18\n\x10load_balancer_id\x18\x01 \x01(\t\x12\x15\n\rlistener_name\x18\x02 \x01(\t\"K\n\x15RemoveListenerRequest\x12\x1e\n\x10load_balancer_id\x18\x01 \x01(\tB\x04\xe8\xc7\x31\x01\x12\x12\n\x04name\x18\x02 \x01(\tB\x04\xe8\xc7\x31\x01\"I\n\x16RemoveListenerMetadata\x12\x18\n\x10load_balancer_id\x18\x01 \x01(\t\x12\x15\n\rlistener_name\x18\x02 \x01(\t\"\xb4\x01\n\x15UpdateListenerRequest\x12\x1e\n\x10load_balancer_id\x18\x01 \x01(\tB\x04\xe8\xc7\x31\x01\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12J\n\rlistener_spec\x18\x03 \x01(\x0b\x32-.yandex.cloud.apploadbalancer.v1.ListenerSpecB\x04\xe8\xc7\x31\x01\"I\n\x16UpdateListenerMetadata\x12\x18\n\x10load_balancer_id\x18\x01 \x01(\t\x12\x15\n\rlistener_name\x18\x02 \x01(\t\"\xc3\x02\n\x0b\x41\x64\x64ressSpec\x12^\n\x1a\x65xternal_ipv4_address_spec\x18\x01 \x01(\x0b\x32\x38.yandex.cloud.apploadbalancer.v1.ExternalIpv4AddressSpecH\x00\x12^\n\x1ainternal_ipv4_address_spec\x18\x02 \x01(\x0b\x32\x38.yandex.cloud.apploadbalancer.v1.InternalIpv4AddressSpecH\x00\x12^\n\x1a\x65xternal_ipv6_address_spec\x18\x03 \x01(\x0b\x32\x38.yandex.cloud.apploadbalancer.v1.ExternalIpv6AddressSpecH\x00\x42\x14\n\x0c\x61\x64\x64ress_spec\x12\x04\xc0\xc1\x31\x01\"*\n\x17\x45xternalIpv4AddressSpec\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\"=\n\x17InternalIpv4AddressSpec\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x11\n\tsubnet_id\x18\x02 \x01(\t\"*\n\x17\x45xternalIpv6AddressSpec\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\"}\n\x0c\x45ndpointSpec\x12K\n\raddress_specs\x18\x01 \x03(\x0b\x32,.yandex.cloud.apploadbalancer.v1.AddressSpecB\x06\x82\xc8\x31\x02>0\x12 \n\x05ports\x18\x02 \x03(\x03\x42\x11\xfa\xc7\x31\x07\x31-65535\x82\xc8\x31\x02>0\"\xe5\x02\n\x0cListenerSpec\x12\x35\n\x04name\x18\x01 \x01(\tB\'\xe8\xc7\x31\x01\xf2\xc7\x31\x1f[a-z]([-a-z0-9]{0,61}[a-z0-9])?\x12M\n\x0e\x65ndpoint_specs\x18\x02 \x03(\x0b\x32-.yandex.cloud.apploadbalancer.v1.EndpointSpecB\x06\x82\xc8\x31\x02>0\x12=\n\x04http\x18\x03 \x01(\x0b\x32-.yandex.cloud.apploadbalancer.v1.HttpListenerH\x00\x12;\n\x03tls\x18\x04 \x01(\x0b\x32,.yandex.cloud.apploadbalancer.v1.TlsListenerH\x00\x12\x41\n\x06stream\x18\x05 \x01(\x0b\x32/.yandex.cloud.apploadbalancer.v1.StreamListenerH\x00\x42\x10\n\x08listener\x12\x04\xc0\xc1\x31\x01\"w\n\x16GetTargetStatesRequest\x12\x1e\n\x10load_balancer_id\x18\x01 \x01(\tB\x04\xe8\xc7\x31\x01\x12\x1e\n\x10\x62\x61\x63kend_group_id\x18\x02 \x01(\tB\x04\xe8\xc7\x31\x01\x12\x1d\n\x0ftarget_group_id\x18\x03 \x01(\tB\x04\xe8\xc7\x31\x01\"^\n\x17GetTargetStatesResponse\x12\x43\n\rtarget_states\x18\x01 \x03(\x0b\x32,.yandex.cloud.apploadbalancer.v1.TargetState\"\xc7\x01\n\x12\x41\x64\x64SniMatchRequest\x12\x1e\n\x10load_balancer_id\x18\x01 \x01(\tB\x04\xe8\xc7\x31\x01\x12\x1b\n\rlistener_name\x18\x02 \x01(\tB\x04\xe8\xc7\x31\x01\x12\x12\n\x04name\x18\x03 \x01(\tB\x04\xe8\xc7\x31\x01\x12\x1c\n\x0cserver_names\x18\x04 \x03(\tB\x06\x82\xc8\x31\x02>0\x12\x42\n\x07handler\x18\x05 \x01(\x0b\x32+.yandex.cloud.apploadbalancer.v1.TlsHandlerB\x04\xe8\xc7\x31\x01\"^\n\x13\x41\x64\x64SniMatchMetadata\x12\x18\n\x10load_balancer_id\x18\x01 \x01(\t\x12\x15\n\rlistener_name\x18\x02 \x01(\t\x12\x16\n\x0esni_match_name\x18\x03 \x01(\t\"r\n\x15RemoveSniMatchRequest\x12\x1e\n\x10load_balancer_id\x18\x01 \x01(\tB\x04\xe8\xc7\x31\x01\x12\x1b\n\rlistener_name\x18\x02 \x01(\tB\x04\xe8\xc7\x31\x01\x12\x1c\n\x0esni_match_name\x18\x03 \x01(\tB\x04\xe8\xc7\x31\x01\"a\n\x16RemoveSniMatchMetadata\x12\x18\n\x10load_balancer_id\x18\x01 \x01(\t\x12\x15\n\rlistener_name\x18\x02 \x01(\t\x12\x16\n\x0esni_match_name\x18\x03 \x01(\t\"\xfb\x01\n\x15UpdateSniMatchRequest\x12\x1e\n\x10load_balancer_id\x18\x01 \x01(\tB\x04\xe8\xc7\x31\x01\x12\x1b\n\rlistener_name\x18\x02 \x01(\tB\x04\xe8\xc7\x31\x01\x12\x12\n\x04name\x18\x03 \x01(\tB\x04\xe8\xc7\x31\x01\x12/\n\x0bupdate_mask\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12\x1c\n\x0cserver_names\x18\x05 \x03(\tB\x06\x82\xc8\x31\x02>0\x12\x42\n\x07handler\x18\x06 \x01(\x0b\x32+.yandex.cloud.apploadbalancer.v1.TlsHandlerB\x04\xe8\xc7\x31\x01\"a\n\x16UpdateSniMatchMetadata\x12\x18\n\x10load_balancer_id\x18\x01 \x01(\t\x12\x15\n\rlistener_name\x18\x02 \x01(\t\x12\x16\n\x0esni_match_name\x18\x03 \x01(\t\"\x89\x01\n!ListLoadBalancerOperationsRequest\x12&\n\x10load_balancer_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06<=1000\x12\x1d\n\npage_token\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=100\"t\n\"ListLoadBalancerOperationsResponse\x12\x35\n\noperations\x18\x01 \x03(\x0b\x32!.yandex.cloud.operation.Operation\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t2\xeb\x19\n\x13LoadBalancerService\x12\xab\x01\n\x03Get\x12\x37.yandex.cloud.apploadbalancer.v1.GetLoadBalancerRequest\x1a-.yandex.cloud.apploadbalancer.v1.LoadBalancer\"<\x82\xd3\xe4\x93\x02\x36\x12\x34/apploadbalancer/v1/loadBalancers/{load_balancer_id}\x12\xa8\x01\n\x04List\x12\x39.yandex.cloud.apploadbalancer.v1.ListLoadBalancersRequest\x1a:.yandex.cloud.apploadbalancer.v1.ListLoadBalancersResponse\")\x82\xd3\xe4\x93\x02#\x12!/apploadbalancer/v1/loadBalancers\x12\xc3\x01\n\x06\x43reate\x12:.yandex.cloud.apploadbalancer.v1.CreateLoadBalancerRequest\x1a!.yandex.cloud.operation.Operation\"Z\xb2\xd2**\n\x1a\x43reateLoadBalancerMetadata\x12\x0cLoadBalancer\x82\xd3\xe4\x93\x02&\"!/apploadbalancer/v1/loadBalancers:\x01*\x12\xd6\x01\n\x06Update\x12:.yandex.cloud.apploadbalancer.v1.UpdateLoadBalancerRequest\x1a!.yandex.cloud.operation.Operation\"m\xb2\xd2**\n\x1aUpdateLoadBalancerMetadata\x12\x0cLoadBalancer\x82\xd3\xe4\x93\x02\x39\x32\x34/apploadbalancer/v1/loadBalancers/{load_balancer_id}:\x01*\x12\xdc\x01\n\x06\x44\x65lete\x12:.yandex.cloud.apploadbalancer.v1.DeleteLoadBalancerRequest\x1a!.yandex.cloud.operation.Operation\"s\xb2\xd2*3\n\x1a\x44\x65leteLoadBalancerMetadata\x12\x15google.protobuf.Empty\x82\xd3\xe4\x93\x02\x36*4/apploadbalancer/v1/loadBalancers/{load_balancer_id}\x12\xd6\x01\n\x05Start\x12\x39.yandex.cloud.apploadbalancer.v1.StartLoadBalancerRequest\x1a!.yandex.cloud.operation.Operation\"o\xb2\xd2*)\n\x19StartLoadBalancerMetadata\x12\x0cLoadBalancer\x82\xd3\xe4\x93\x02<\":/apploadbalancer/v1/loadBalancers/{load_balancer_id}:start\x12\xd2\x01\n\x04Stop\x12\x38.yandex.cloud.apploadbalancer.v1.StopLoadBalancerRequest\x1a!.yandex.cloud.operation.Operation\"m\xb2\xd2*(\n\x18StopLoadBalancerMetadata\x12\x0cLoadBalancer\x82\xd3\xe4\x93\x02;\"9/apploadbalancer/v1/loadBalancers/{load_balancer_id}:stop\x12\xd9\x01\n\x0b\x41\x64\x64Listener\x12\x33.yandex.cloud.apploadbalancer.v1.AddListenerRequest\x1a!.yandex.cloud.operation.Operation\"r\xb2\xd2*#\n\x13\x41\x64\x64ListenerMetadata\x12\x0cLoadBalancer\x82\xd3\xe4\x93\x02\x45\"@/apploadbalancer/v1/loadBalancers/{load_balancer_id}:addListener:\x01*\x12\xe5\x01\n\x0eRemoveListener\x12\x36.yandex.cloud.apploadbalancer.v1.RemoveListenerRequest\x1a!.yandex.cloud.operation.Operation\"x\xb2\xd2*&\n\x16RemoveListenerMetadata\x12\x0cLoadBalancer\x82\xd3\xe4\x93\x02H\"C/apploadbalancer/v1/loadBalancers/{load_balancer_id}:removeListener:\x01*\x12\xe5\x01\n\x0eUpdateListener\x12\x36.yandex.cloud.apploadbalancer.v1.UpdateListenerRequest\x1a!.yandex.cloud.operation.Operation\"x\xb2\xd2*&\n\x16UpdateListenerMetadata\x12\x0cLoadBalancer\x82\xd3\xe4\x93\x02H\"C/apploadbalancer/v1/loadBalancers/{load_balancer_id}:updateListener:\x01*\x12\xe2\x01\n\x0b\x41\x64\x64SniMatch\x12\x33.yandex.cloud.apploadbalancer.v1.AddSniMatchRequest\x1a!.yandex.cloud.operation.Operation\"{\xb2\xd2*,\n\x13\x41\x64\x64SniMatchMetadata\x12\x15google.protobuf.Empty\x82\xd3\xe4\x93\x02\x45\"@/apploadbalancer/v1/loadBalancers/{load_balancer_id}:addSniMatch:\x01*\x12\xef\x01\n\x0eUpdateSniMatch\x12\x36.yandex.cloud.apploadbalancer.v1.UpdateSniMatchRequest\x1a!.yandex.cloud.operation.Operation\"\x81\x01\xb2\xd2*/\n\x16UpdateSniMatchMetadata\x12\x15google.protobuf.Empty\x82\xd3\xe4\x93\x02H\"C/apploadbalancer/v1/loadBalancers/{load_balancer_id}:updateSniMatch:\x01*\x12\xef\x01\n\x0eRemoveSniMatch\x12\x36.yandex.cloud.apploadbalancer.v1.RemoveSniMatchRequest\x1a!.yandex.cloud.operation.Operation\"\x81\x01\xb2\xd2*/\n\x16RemoveSniMatchMetadata\x12\x15google.protobuf.Empty\x82\xd3\xe4\x93\x02H\"C/apploadbalancer/v1/loadBalancers/{load_balancer_id}:removeSniMatch:\x01*\x12\xf4\x01\n\x0fGetTargetStates\x12\x37.yandex.cloud.apploadbalancer.v1.GetTargetStatesRequest\x1a\x38.yandex.cloud.apploadbalancer.v1.GetTargetStatesResponse\"n\x82\xd3\xe4\x93\x02h\x12\x66/apploadbalancer/v1/loadBalancers/{load_balancer_id}/targetStates/{backend_group_id}/{target_group_id}\x12\xe2\x01\n\x0eListOperations\x12\x42.yandex.cloud.apploadbalancer.v1.ListLoadBalancerOperationsRequest\x1a\x43.yandex.cloud.apploadbalancer.v1.ListLoadBalancerOperationsResponse\"G\x82\xd3\xe4\x93\x02\x41\x12?/apploadbalancer/v1/loadBalancers/{load_balancer_id}/operationsBz\n#yandex.cloud.api.apploadbalancer.v1ZSgithub.com/yandex-cloud/go-genproto/yandex/cloud/apploadbalancer/v1;apploadbalancerb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.apploadbalancer.v1.load_balancer_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n#yandex.cloud.api.apploadbalancer.v1ZSgithub.com/yandex-cloud/go-genproto/yandex/cloud/apploadbalancer/v1;apploadbalancer'
  _GETLOADBALANCERREQUEST.fields_by_name['load_balancer_id']._options = None
  _GETLOADBALANCERREQUEST.fields_by_name['load_balancer_id']._serialized_options = b'\350\3071\001'
  _LISTLOADBALANCERSREQUEST.fields_by_name['folder_id']._options = None
  _LISTLOADBALANCERSREQUEST.fields_by_name['folder_id']._serialized_options = b'\350\3071\001'
  _LISTLOADBALANCERSREQUEST.fields_by_name['page_size']._options = None
  _LISTLOADBALANCERSREQUEST.fields_by_name['page_size']._serialized_options = b'\372\3071\0060-1000'
  _LISTLOADBALANCERSREQUEST.fields_by_name['page_token']._options = None
  _LISTLOADBALANCERSREQUEST.fields_by_name['page_token']._serialized_options = b'\212\3101\005<=100'
  _LISTLOADBALANCERSREQUEST.fields_by_name['filter']._options = None
  _LISTLOADBALANCERSREQUEST.fields_by_name['filter']._serialized_options = b'\212\3101\006<=1000'
  _DELETELOADBALANCERREQUEST.fields_by_name['load_balancer_id']._options = None
  _DELETELOADBALANCERREQUEST.fields_by_name['load_balancer_id']._serialized_options = b'\350\3071\001'
  _UPDATELOADBALANCERREQUEST_LABELSENTRY._options = None
  _UPDATELOADBALANCERREQUEST_LABELSENTRY._serialized_options = b'8\001'
  _UPDATELOADBALANCERREQUEST.fields_by_name['load_balancer_id']._options = None
  _UPDATELOADBALANCERREQUEST.fields_by_name['load_balancer_id']._serialized_options = b'\350\3071\001'
  _UPDATELOADBALANCERREQUEST.fields_by_name['name']._options = None
  _UPDATELOADBALANCERREQUEST.fields_by_name['name']._serialized_options = b'\362\3071\"([a-z]([-a-z0-9]{0,61}[a-z0-9])?)?'
  _UPDATELOADBALANCERREQUEST.fields_by_name['description']._options = None
  _UPDATELOADBALANCERREQUEST.fields_by_name['description']._serialized_options = b'\212\3101\005<=256'
  _UPDATELOADBALANCERREQUEST.fields_by_name['labels']._options = None
  _UPDATELOADBALANCERREQUEST.fields_by_name['labels']._serialized_options = b'\362\3071\017[-_./\\@0-9a-z]*\202\3101\004<=64\212\3101\004<=63\262\3101\034\022\024[a-z][-_./\\@0-9a-z]*\032\0041-63'
  _CREATELOADBALANCERREQUEST_LABELSENTRY._options = None
  _CREATELOADBALANCERREQUEST_LABELSENTRY._serialized_options = b'8\001'
  _CREATELOADBALANCERREQUEST.fields_by_name['folder_id']._options = None
  _CREATELOADBALANCERREQUEST.fields_by_name['folder_id']._serialized_options = b'\350\3071\001'
  _CREATELOADBALANCERREQUEST.fields_by_name['name']._options = None
  _CREATELOADBALANCERREQUEST.fields_by_name['name']._serialized_options = b'\362\3071\"([a-z]([-a-z0-9]{0,61}[a-z0-9])?)?'
  _CREATELOADBALANCERREQUEST.fields_by_name['description']._options = None
  _CREATELOADBALANCERREQUEST.fields_by_name['description']._serialized_options = b'\212\3101\005<=256'
  _CREATELOADBALANCERREQUEST.fields_by_name['labels']._options = None
  _CREATELOADBALANCERREQUEST.fields_by_name['labels']._serialized_options = b'\362\3071\017[-_./\\@0-9a-z]*\202\3101\004<=64\212\3101\004<=63\262\3101\034\022\024[a-z][-_./\\@0-9a-z]*\032\0041-63'
  _CREATELOADBALANCERREQUEST.fields_by_name['region_id']._options = None
  _CREATELOADBALANCERREQUEST.fields_by_name['region_id']._serialized_options = b'\350\3071\001'
  _CREATELOADBALANCERREQUEST.fields_by_name['network_id']._options = None
  _CREATELOADBALANCERREQUEST.fields_by_name['network_id']._serialized_options = b'\350\3071\001'
  _STARTLOADBALANCERREQUEST.fields_by_name['load_balancer_id']._options = None
  _STARTLOADBALANCERREQUEST.fields_by_name['load_balancer_id']._serialized_options = b'\350\3071\001'
  _STOPLOADBALANCERREQUEST.fields_by_name['load_balancer_id']._options = None
  _STOPLOADBALANCERREQUEST.fields_by_name['load_balancer_id']._serialized_options = b'\350\3071\001'
  _ADDLISTENERREQUEST.fields_by_name['load_balancer_id']._options = None
  _ADDLISTENERREQUEST.fields_by_name['load_balancer_id']._serialized_options = b'\350\3071\001'
  _ADDLISTENERREQUEST.fields_by_name['listener_spec']._options = None
  _ADDLISTENERREQUEST.fields_by_name['listener_spec']._serialized_options = b'\350\3071\001'
  _REMOVELISTENERREQUEST.fields_by_name['load_balancer_id']._options = None
  _REMOVELISTENERREQUEST.fields_by_name['load_balancer_id']._serialized_options = b'\350\3071\001'
  _REMOVELISTENERREQUEST.fields_by_name['name']._options = None
  _REMOVELISTENERREQUEST.fields_by_name['name']._serialized_options = b'\350\3071\001'
  _UPDATELISTENERREQUEST.fields_by_name['load_balancer_id']._options = None
  _UPDATELISTENERREQUEST.fields_by_name['load_balancer_id']._serialized_options = b'\350\3071\001'
  _UPDATELISTENERREQUEST.fields_by_name['listener_spec']._options = None
  _UPDATELISTENERREQUEST.fields_by_name['listener_spec']._serialized_options = b'\350\3071\001'
  _ADDRESSSPEC.oneofs_by_name['address_spec']._options = None
  _ADDRESSSPEC.oneofs_by_name['address_spec']._serialized_options = b'\300\3011\001'
  _ENDPOINTSPEC.fields_by_name['address_specs']._options = None
  _ENDPOINTSPEC.fields_by_name['address_specs']._serialized_options = b'\202\3101\002>0'
  _ENDPOINTSPEC.fields_by_name['ports']._options = None
  _ENDPOINTSPEC.fields_by_name['ports']._serialized_options = b'\372\3071\0071-65535\202\3101\002>0'
  _LISTENERSPEC.oneofs_by_name['listener']._options = None
  _LISTENERSPEC.oneofs_by_name['listener']._serialized_options = b'\300\3011\001'
  _LISTENERSPEC.fields_by_name['name']._options = None
  _LISTENERSPEC.fields_by_name['name']._serialized_options = b'\350\3071\001\362\3071\037[a-z]([-a-z0-9]{0,61}[a-z0-9])?'
  _LISTENERSPEC.fields_by_name['endpoint_specs']._options = None
  _LISTENERSPEC.fields_by_name['endpoint_specs']._serialized_options = b'\202\3101\002>0'
  _GETTARGETSTATESREQUEST.fields_by_name['load_balancer_id']._options = None
  _GETTARGETSTATESREQUEST.fields_by_name['load_balancer_id']._serialized_options = b'\350\3071\001'
  _GETTARGETSTATESREQUEST.fields_by_name['backend_group_id']._options = None
  _GETTARGETSTATESREQUEST.fields_by_name['backend_group_id']._serialized_options = b'\350\3071\001'
  _GETTARGETSTATESREQUEST.fields_by_name['target_group_id']._options = None
  _GETTARGETSTATESREQUEST.fields_by_name['target_group_id']._serialized_options = b'\350\3071\001'
  _ADDSNIMATCHREQUEST.fields_by_name['load_balancer_id']._options = None
  _ADDSNIMATCHREQUEST.fields_by_name['load_balancer_id']._serialized_options = b'\350\3071\001'
  _ADDSNIMATCHREQUEST.fields_by_name['listener_name']._options = None
  _ADDSNIMATCHREQUEST.fields_by_name['listener_name']._serialized_options = b'\350\3071\001'
  _ADDSNIMATCHREQUEST.fields_by_name['name']._options = None
  _ADDSNIMATCHREQUEST.fields_by_name['name']._serialized_options = b'\350\3071\001'
  _ADDSNIMATCHREQUEST.fields_by_name['server_names']._options = None
  _ADDSNIMATCHREQUEST.fields_by_name['server_names']._serialized_options = b'\202\3101\002>0'
  _ADDSNIMATCHREQUEST.fields_by_name['handler']._options = None
  _ADDSNIMATCHREQUEST.fields_by_name['handler']._serialized_options = b'\350\3071\001'
  _REMOVESNIMATCHREQUEST.fields_by_name['load_balancer_id']._options = None
  _REMOVESNIMATCHREQUEST.fields_by_name['load_balancer_id']._serialized_options = b'\350\3071\001'
  _REMOVESNIMATCHREQUEST.fields_by_name['listener_name']._options = None
  _REMOVESNIMATCHREQUEST.fields_by_name['listener_name']._serialized_options = b'\350\3071\001'
  _REMOVESNIMATCHREQUEST.fields_by_name['sni_match_name']._options = None
  _REMOVESNIMATCHREQUEST.fields_by_name['sni_match_name']._serialized_options = b'\350\3071\001'
  _UPDATESNIMATCHREQUEST.fields_by_name['load_balancer_id']._options = None
  _UPDATESNIMATCHREQUEST.fields_by_name['load_balancer_id']._serialized_options = b'\350\3071\001'
  _UPDATESNIMATCHREQUEST.fields_by_name['listener_name']._options = None
  _UPDATESNIMATCHREQUEST.fields_by_name['listener_name']._serialized_options = b'\350\3071\001'
  _UPDATESNIMATCHREQUEST.fields_by_name['name']._options = None
  _UPDATESNIMATCHREQUEST.fields_by_name['name']._serialized_options = b'\350\3071\001'
  _UPDATESNIMATCHREQUEST.fields_by_name['server_names']._options = None
  _UPDATESNIMATCHREQUEST.fields_by_name['server_names']._serialized_options = b'\202\3101\002>0'
  _UPDATESNIMATCHREQUEST.fields_by_name['handler']._options = None
  _UPDATESNIMATCHREQUEST.fields_by_name['handler']._serialized_options = b'\350\3071\001'
  _LISTLOADBALANCEROPERATIONSREQUEST.fields_by_name['load_balancer_id']._options = None
  _LISTLOADBALANCEROPERATIONSREQUEST.fields_by_name['load_balancer_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _LISTLOADBALANCEROPERATIONSREQUEST.fields_by_name['page_size']._options = None
  _LISTLOADBALANCEROPERATIONSREQUEST.fields_by_name['page_size']._serialized_options = b'\372\3071\006<=1000'
  _LISTLOADBALANCEROPERATIONSREQUEST.fields_by_name['page_token']._options = None
  _LISTLOADBALANCEROPERATIONSREQUEST.fields_by_name['page_token']._serialized_options = b'\212\3101\005<=100'
  _LOADBALANCERSERVICE.methods_by_name['Get']._options = None
  _LOADBALANCERSERVICE.methods_by_name['Get']._serialized_options = b'\202\323\344\223\0026\0224/apploadbalancer/v1/loadBalancers/{load_balancer_id}'
  _LOADBALANCERSERVICE.methods_by_name['List']._options = None
  _LOADBALANCERSERVICE.methods_by_name['List']._serialized_options = b'\202\323\344\223\002#\022!/apploadbalancer/v1/loadBalancers'
  _LOADBALANCERSERVICE.methods_by_name['Create']._options = None
  _LOADBALANCERSERVICE.methods_by_name['Create']._serialized_options = b'\262\322**\n\032CreateLoadBalancerMetadata\022\014LoadBalancer\202\323\344\223\002&\"!/apploadbalancer/v1/loadBalancers:\001*'
  _LOADBALANCERSERVICE.methods_by_name['Update']._options = None
  _LOADBALANCERSERVICE.methods_by_name['Update']._serialized_options = b'\262\322**\n\032UpdateLoadBalancerMetadata\022\014LoadBalancer\202\323\344\223\002924/apploadbalancer/v1/loadBalancers/{load_balancer_id}:\001*'
  _LOADBALANCERSERVICE.methods_by_name['Delete']._options = None
  _LOADBALANCERSERVICE.methods_by_name['Delete']._serialized_options = b'\262\322*3\n\032DeleteLoadBalancerMetadata\022\025google.protobuf.Empty\202\323\344\223\0026*4/apploadbalancer/v1/loadBalancers/{load_balancer_id}'
  _LOADBALANCERSERVICE.methods_by_name['Start']._options = None
  _LOADBALANCERSERVICE.methods_by_name['Start']._serialized_options = b'\262\322*)\n\031StartLoadBalancerMetadata\022\014LoadBalancer\202\323\344\223\002<\":/apploadbalancer/v1/loadBalancers/{load_balancer_id}:start'
  _LOADBALANCERSERVICE.methods_by_name['Stop']._options = None
  _LOADBALANCERSERVICE.methods_by_name['Stop']._serialized_options = b'\262\322*(\n\030StopLoadBalancerMetadata\022\014LoadBalancer\202\323\344\223\002;\"9/apploadbalancer/v1/loadBalancers/{load_balancer_id}:stop'
  _LOADBALANCERSERVICE.methods_by_name['AddListener']._options = None
  _LOADBALANCERSERVICE.methods_by_name['AddListener']._serialized_options = b'\262\322*#\n\023AddListenerMetadata\022\014LoadBalancer\202\323\344\223\002E\"@/apploadbalancer/v1/loadBalancers/{load_balancer_id}:addListener:\001*'
  _LOADBALANCERSERVICE.methods_by_name['RemoveListener']._options = None
  _LOADBALANCERSERVICE.methods_by_name['RemoveListener']._serialized_options = b'\262\322*&\n\026RemoveListenerMetadata\022\014LoadBalancer\202\323\344\223\002H\"C/apploadbalancer/v1/loadBalancers/{load_balancer_id}:removeListener:\001*'
  _LOADBALANCERSERVICE.methods_by_name['UpdateListener']._options = None
  _LOADBALANCERSERVICE.methods_by_name['UpdateListener']._serialized_options = b'\262\322*&\n\026UpdateListenerMetadata\022\014LoadBalancer\202\323\344\223\002H\"C/apploadbalancer/v1/loadBalancers/{load_balancer_id}:updateListener:\001*'
  _LOADBALANCERSERVICE.methods_by_name['AddSniMatch']._options = None
  _LOADBALANCERSERVICE.methods_by_name['AddSniMatch']._serialized_options = b'\262\322*,\n\023AddSniMatchMetadata\022\025google.protobuf.Empty\202\323\344\223\002E\"@/apploadbalancer/v1/loadBalancers/{load_balancer_id}:addSniMatch:\001*'
  _LOADBALANCERSERVICE.methods_by_name['UpdateSniMatch']._options = None
  _LOADBALANCERSERVICE.methods_by_name['UpdateSniMatch']._serialized_options = b'\262\322*/\n\026UpdateSniMatchMetadata\022\025google.protobuf.Empty\202\323\344\223\002H\"C/apploadbalancer/v1/loadBalancers/{load_balancer_id}:updateSniMatch:\001*'
  _LOADBALANCERSERVICE.methods_by_name['RemoveSniMatch']._options = None
  _LOADBALANCERSERVICE.methods_by_name['RemoveSniMatch']._serialized_options = b'\262\322*/\n\026RemoveSniMatchMetadata\022\025google.protobuf.Empty\202\323\344\223\002H\"C/apploadbalancer/v1/loadBalancers/{load_balancer_id}:removeSniMatch:\001*'
  _LOADBALANCERSERVICE.methods_by_name['GetTargetStates']._options = None
  _LOADBALANCERSERVICE.methods_by_name['GetTargetStates']._serialized_options = b'\202\323\344\223\002h\022f/apploadbalancer/v1/loadBalancers/{load_balancer_id}/targetStates/{backend_group_id}/{target_group_id}'
  _LOADBALANCERSERVICE.methods_by_name['ListOperations']._options = None
  _LOADBALANCERSERVICE.methods_by_name['ListOperations']._serialized_options = b'\202\323\344\223\002A\022?/apploadbalancer/v1/loadBalancers/{load_balancer_id}/operations'
  _globals['_GETLOADBALANCERREQUEST']._serialized_start=365
  _globals['_GETLOADBALANCERREQUEST']._serialized_end=421
  _globals['_LISTLOADBALANCERSREQUEST']._serialized_start=424
  _globals['_LISTLOADBALANCERSREQUEST']._serialized_end=565
  _globals['_LISTLOADBALANCERSRESPONSE']._serialized_start=567
  _globals['_LISTLOADBALANCERSRESPONSE']._serialized_end=690
  _globals['_DELETELOADBALANCERREQUEST']._serialized_start=692
  _globals['_DELETELOADBALANCERREQUEST']._serialized_end=751
  _globals['_DELETELOADBALANCERMETADATA']._serialized_start=753
  _globals['_DELETELOADBALANCERMETADATA']._serialized_end=807
  _globals['_UPDATELOADBALANCERREQUEST']._serialized_start=810
  _globals['_UPDATELOADBALANCERREQUEST']._serialized_end=1529
  _globals['_UPDATELOADBALANCERREQUEST_LABELSENTRY']._serialized_start=1484
  _globals['_UPDATELOADBALANCERREQUEST_LABELSENTRY']._serialized_end=1529
  _globals['_UPDATELOADBALANCERMETADATA']._serialized_start=1531
  _globals['_UPDATELOADBALANCERMETADATA']._serialized_end=1585
  _globals['_CREATELOADBALANCERREQUEST']._serialized_start=1588
  _globals['_CREATELOADBALANCERREQUEST']._serialized_end=2302
  _globals['_CREATELOADBALANCERREQUEST_LABELSENTRY']._serialized_start=1484
  _globals['_CREATELOADBALANCERREQUEST_LABELSENTRY']._serialized_end=1529
  _globals['_CREATELOADBALANCERMETADATA']._serialized_start=2304
  _globals['_CREATELOADBALANCERMETADATA']._serialized_end=2358
  _globals['_STARTLOADBALANCERREQUEST']._serialized_start=2360
  _globals['_STARTLOADBALANCERREQUEST']._serialized_end=2418
  _globals['_STARTLOADBALANCERMETADATA']._serialized_start=2420
  _globals['_STARTLOADBALANCERMETADATA']._serialized_end=2473
  _globals['_STOPLOADBALANCERREQUEST']._serialized_start=2475
  _globals['_STOPLOADBALANCERREQUEST']._serialized_end=2532
  _globals['_STOPLOADBALANCERMETADATA']._serialized_start=2534
  _globals['_STOPLOADBALANCERMETADATA']._serialized_end=2586
  _globals['_ADDLISTENERREQUEST']._serialized_start=2589
  _globals['_ADDLISTENERREQUEST']._serialized_end=2717
  _globals['_ADDLISTENERMETADATA']._serialized_start=2719
  _globals['_ADDLISTENERMETADATA']._serialized_end=2789
  _globals['_REMOVELISTENERREQUEST']._serialized_start=2791
  _globals['_REMOVELISTENERREQUEST']._serialized_end=2866
  _globals['_REMOVELISTENERMETADATA']._serialized_start=2868
  _globals['_REMOVELISTENERMETADATA']._serialized_end=2941
  _globals['_UPDATELISTENERREQUEST']._serialized_start=2944
  _globals['_UPDATELISTENERREQUEST']._serialized_end=3124
  _globals['_UPDATELISTENERMETADATA']._serialized_start=3126
  _globals['_UPDATELISTENERMETADATA']._serialized_end=3199
  _globals['_ADDRESSSPEC']._serialized_start=3202
  _globals['_ADDRESSSPEC']._serialized_end=3525
  _globals['_EXTERNALIPV4ADDRESSSPEC']._serialized_start=3527
  _globals['_EXTERNALIPV4ADDRESSSPEC']._serialized_end=3569
  _globals['_INTERNALIPV4ADDRESSSPEC']._serialized_start=3571
  _globals['_INTERNALIPV4ADDRESSSPEC']._serialized_end=3632
  _globals['_EXTERNALIPV6ADDRESSSPEC']._serialized_start=3634
  _globals['_EXTERNALIPV6ADDRESSSPEC']._serialized_end=3676
  _globals['_ENDPOINTSPEC']._serialized_start=3678
  _globals['_ENDPOINTSPEC']._serialized_end=3803
  _globals['_LISTENERSPEC']._serialized_start=3806
  _globals['_LISTENERSPEC']._serialized_end=4163
  _globals['_GETTARGETSTATESREQUEST']._serialized_start=4165
  _globals['_GETTARGETSTATESREQUEST']._serialized_end=4284
  _globals['_GETTARGETSTATESRESPONSE']._serialized_start=4286
  _globals['_GETTARGETSTATESRESPONSE']._serialized_end=4380
  _globals['_ADDSNIMATCHREQUEST']._serialized_start=4383
  _globals['_ADDSNIMATCHREQUEST']._serialized_end=4582
  _globals['_ADDSNIMATCHMETADATA']._serialized_start=4584
  _globals['_ADDSNIMATCHMETADATA']._serialized_end=4678
  _globals['_REMOVESNIMATCHREQUEST']._serialized_start=4680
  _globals['_REMOVESNIMATCHREQUEST']._serialized_end=4794
  _globals['_REMOVESNIMATCHMETADATA']._serialized_start=4796
  _globals['_REMOVESNIMATCHMETADATA']._serialized_end=4893
  _globals['_UPDATESNIMATCHREQUEST']._serialized_start=4896
  _globals['_UPDATESNIMATCHREQUEST']._serialized_end=5147
  _globals['_UPDATESNIMATCHMETADATA']._serialized_start=5149
  _globals['_UPDATESNIMATCHMETADATA']._serialized_end=5246
  _globals['_LISTLOADBALANCEROPERATIONSREQUEST']._serialized_start=5249
  _globals['_LISTLOADBALANCEROPERATIONSREQUEST']._serialized_end=5386
  _globals['_LISTLOADBALANCEROPERATIONSRESPONSE']._serialized_start=5388
  _globals['_LISTLOADBALANCEROPERATIONSRESPONSE']._serialized_end=5504
  _globals['_LOADBALANCERSERVICE']._serialized_start=5507
  _globals['_LOADBALANCERSERVICE']._serialized_end=8814
# @@protoc_insertion_point(module_scope)
