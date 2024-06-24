"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class PublishDeviceDataRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICE_ID_FIELD_NUMBER: builtins.int
    TOPIC_FIELD_NUMBER: builtins.int
    DATA_FIELD_NUMBER: builtins.int
    device_id: builtins.str
    """ID of device publishing message"""
    topic: builtins.str
    """Topic where message should be published"""
    data: builtins.bytes
    """Content of the message"""
    def __init__(
        self,
        *,
        device_id: builtins.str = ...,
        topic: builtins.str = ...,
        data: builtins.bytes = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["data", b"data", "device_id", b"device_id", "topic", b"topic"]) -> None: ...

global___PublishDeviceDataRequest = PublishDeviceDataRequest

@typing.final
class PublishDeviceDataResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___PublishDeviceDataResponse = PublishDeviceDataResponse
