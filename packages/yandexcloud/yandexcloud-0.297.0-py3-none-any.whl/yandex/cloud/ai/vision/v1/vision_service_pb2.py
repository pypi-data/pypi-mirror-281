# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/ai/vision/v1/vision_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from yandex.cloud.ai.vision.v1 import text_detection_pb2 as yandex_dot_cloud_dot_ai_dot_vision_dot_v1_dot_text__detection__pb2
from yandex.cloud.ai.vision.v1 import classification_pb2 as yandex_dot_cloud_dot_ai_dot_vision_dot_v1_dot_classification__pb2
from yandex.cloud.ai.vision.v1 import face_detection_pb2 as yandex_dot_cloud_dot_ai_dot_vision_dot_v1_dot_face__detection__pb2
from yandex.cloud.ai.vision.v1 import image_copy_search_pb2 as yandex_dot_cloud_dot_ai_dot_vision_dot_v1_dot_image__copy__search__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.yandex/cloud/ai/vision/v1/vision_service.proto\x12\x19yandex.cloud.ai.vision.v1\x1a.yandex/cloud/ai/vision/v1/text_detection.proto\x1a.yandex/cloud/ai/vision/v1/classification.proto\x1a.yandex/cloud/ai/vision/v1/face_detection.proto\x1a\x31yandex/cloud/ai/vision/v1/image_copy_search.proto\x1a\x1dyandex/cloud/validation.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x17google/rpc/status.proto\"z\n\x13\x42\x61tchAnalyzeRequest\x12\x46\n\ranalyze_specs\x18\x01 \x03(\x0b\x32&.yandex.cloud.ai.vision.v1.AnalyzeSpecB\x07\x82\xc8\x31\x03\x31-8\x12\x1b\n\tfolder_id\x18\x02 \x01(\tB\x08\x8a\xc8\x31\x04<=50\"\xc5\x01\n\x0b\x41nalyzeSpec\x12!\n\x07\x63ontent\x18\x01 \x01(\x0c\x42\x0e\x8a\xc8\x31\n<=10485760H\x00\x12 \n\tsignature\x18\x05 \x01(\tB\x0b\x8a\xc8\x31\x07<=16384H\x00\x12=\n\x08\x66\x65\x61tures\x18\x03 \x03(\x0b\x32\".yandex.cloud.ai.vision.v1.FeatureB\x07\x82\xc8\x31\x03\x31-8\x12\x1c\n\tmime_type\x18\x04 \x01(\tB\t\x8a\xc8\x31\x05<=255B\x0e\n\x06source\x12\x04\xc0\xc1\x31\x01J\x04\x08\x02\x10\x03\"\xec\x02\n\x07\x46\x65\x61ture\x12\x35\n\x04type\x18\x01 \x01(\x0e\x32\'.yandex.cloud.ai.vision.v1.Feature.Type\x12W\n\x15\x63lassification_config\x18\x02 \x01(\x0b\x32\x36.yandex.cloud.ai.vision.v1.FeatureClassificationConfigH\x00\x12V\n\x15text_detection_config\x18\x03 \x01(\x0b\x32\x35.yandex.cloud.ai.vision.v1.FeatureTextDetectionConfigH\x00\"o\n\x04Type\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\x12\n\x0eTEXT_DETECTION\x10\x01\x12\x12\n\x0e\x43LASSIFICATION\x10\x02\x12\x12\n\x0e\x46\x41\x43\x45_DETECTION\x10\x03\x12\x15\n\x11IMAGE_COPY_SEARCH\x10\x04\x42\x08\n\x06\x63onfig\"7\n\x1b\x46\x65\x61tureClassificationConfig\x12\x18\n\x05model\x18\x01 \x01(\tB\t\x8a\xc8\x31\x05<=256\"]\n\x1a\x46\x65\x61tureTextDetectionConfig\x12&\n\x0elanguage_codes\x18\x01 \x03(\tB\x0e\x82\xc8\x31\x03\x31-8\x8a\xc8\x31\x03<=3\x12\x17\n\x05model\x18\x02 \x01(\tB\x08\x8a\xc8\x31\x04<=50\"Q\n\x14\x42\x61tchAnalyzeResponse\x12\x39\n\x07results\x18\x01 \x03(\x0b\x32(.yandex.cloud.ai.vision.v1.AnalyzeResult\"m\n\rAnalyzeResult\x12\x39\n\x07results\x18\x02 \x03(\x0b\x32(.yandex.cloud.ai.vision.v1.FeatureResult\x12!\n\x05\x65rror\x18\x01 \x01(\x0b\x32\x12.google.rpc.Status\"\xe0\x02\n\rFeatureResult\x12\x43\n\x0etext_detection\x18\x02 \x01(\x0b\x32).yandex.cloud.ai.vision.v1.TextAnnotationH\x00\x12\x44\n\x0e\x63lassification\x18\x03 \x01(\x0b\x32*.yandex.cloud.ai.vision.v1.ClassAnnotationH\x00\x12\x43\n\x0e\x66\x61\x63\x65_detection\x18\x04 \x01(\x0b\x32).yandex.cloud.ai.vision.v1.FaceAnnotationH\x00\x12Q\n\x11image_copy_search\x18\x05 \x01(\x0b\x32\x34.yandex.cloud.ai.vision.v1.ImageCopySearchAnnotationH\x00\x12!\n\x05\x65rror\x18\x01 \x01(\x0b\x32\x12.google.rpc.StatusB\t\n\x07\x66\x65\x61ture2\xa5\x01\n\rVisionService\x12\x93\x01\n\x0c\x42\x61tchAnalyze\x12..yandex.cloud.ai.vision.v1.BatchAnalyzeRequest\x1a/.yandex.cloud.ai.vision.v1.BatchAnalyzeResponse\"\"\x82\xd3\xe4\x93\x02\x1c\"\x17/vision/v1/batchAnalyze:\x01*Be\n\x1dyandex.cloud.api.ai.vision.v1ZDgithub.com/yandex-cloud/go-genproto/yandex/cloud/ai/vision/v1;visionb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.ai.vision.v1.vision_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\035yandex.cloud.api.ai.vision.v1ZDgithub.com/yandex-cloud/go-genproto/yandex/cloud/ai/vision/v1;vision'
  _BATCHANALYZEREQUEST.fields_by_name['analyze_specs']._options = None
  _BATCHANALYZEREQUEST.fields_by_name['analyze_specs']._serialized_options = b'\202\3101\0031-8'
  _BATCHANALYZEREQUEST.fields_by_name['folder_id']._options = None
  _BATCHANALYZEREQUEST.fields_by_name['folder_id']._serialized_options = b'\212\3101\004<=50'
  _ANALYZESPEC.oneofs_by_name['source']._options = None
  _ANALYZESPEC.oneofs_by_name['source']._serialized_options = b'\300\3011\001'
  _ANALYZESPEC.fields_by_name['content']._options = None
  _ANALYZESPEC.fields_by_name['content']._serialized_options = b'\212\3101\n<=10485760'
  _ANALYZESPEC.fields_by_name['signature']._options = None
  _ANALYZESPEC.fields_by_name['signature']._serialized_options = b'\212\3101\007<=16384'
  _ANALYZESPEC.fields_by_name['features']._options = None
  _ANALYZESPEC.fields_by_name['features']._serialized_options = b'\202\3101\0031-8'
  _ANALYZESPEC.fields_by_name['mime_type']._options = None
  _ANALYZESPEC.fields_by_name['mime_type']._serialized_options = b'\212\3101\005<=255'
  _FEATURECLASSIFICATIONCONFIG.fields_by_name['model']._options = None
  _FEATURECLASSIFICATIONCONFIG.fields_by_name['model']._serialized_options = b'\212\3101\005<=256'
  _FEATURETEXTDETECTIONCONFIG.fields_by_name['language_codes']._options = None
  _FEATURETEXTDETECTIONCONFIG.fields_by_name['language_codes']._serialized_options = b'\202\3101\0031-8\212\3101\003<=3'
  _FEATURETEXTDETECTIONCONFIG.fields_by_name['model']._options = None
  _FEATURETEXTDETECTIONCONFIG.fields_by_name['model']._serialized_options = b'\212\3101\004<=50'
  _VISIONSERVICE.methods_by_name['BatchAnalyze']._options = None
  _VISIONSERVICE.methods_by_name['BatchAnalyze']._serialized_options = b'\202\323\344\223\002\034\"\027/vision/v1/batchAnalyze:\001*'
  _globals['_BATCHANALYZEREQUEST']._serialized_start=358
  _globals['_BATCHANALYZEREQUEST']._serialized_end=480
  _globals['_ANALYZESPEC']._serialized_start=483
  _globals['_ANALYZESPEC']._serialized_end=680
  _globals['_FEATURE']._serialized_start=683
  _globals['_FEATURE']._serialized_end=1047
  _globals['_FEATURE_TYPE']._serialized_start=926
  _globals['_FEATURE_TYPE']._serialized_end=1037
  _globals['_FEATURECLASSIFICATIONCONFIG']._serialized_start=1049
  _globals['_FEATURECLASSIFICATIONCONFIG']._serialized_end=1104
  _globals['_FEATURETEXTDETECTIONCONFIG']._serialized_start=1106
  _globals['_FEATURETEXTDETECTIONCONFIG']._serialized_end=1199
  _globals['_BATCHANALYZERESPONSE']._serialized_start=1201
  _globals['_BATCHANALYZERESPONSE']._serialized_end=1282
  _globals['_ANALYZERESULT']._serialized_start=1284
  _globals['_ANALYZERESULT']._serialized_end=1393
  _globals['_FEATURERESULT']._serialized_start=1396
  _globals['_FEATURERESULT']._serialized_end=1748
  _globals['_VISIONSERVICE']._serialized_start=1751
  _globals['_VISIONSERVICE']._serialized_end=1916
# @@protoc_insertion_point(module_scope)
