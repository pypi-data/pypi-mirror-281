"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.message
import google.protobuf.timestamp_pb2
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class BillableObject(google.protobuf.message.Message):
    """Represents a link to an object in other service.
    This object is being billed in the scope of a billing account.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    id: builtins.str
    """ID of the object in other service."""
    type: builtins.str
    """Billable object type. Can be one of the following:
    * `cloud`
    """
    def __init__(
        self,
        *,
        id: builtins.str = ...,
        type: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["id", b"id", "type", b"type"]) -> None: ...

global___BillableObject = BillableObject

@typing.final
class BillableObjectBinding(google.protobuf.message.Message):
    """Represents a binding of the BillableObject to a BillingAccount."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EFFECTIVE_TIME_FIELD_NUMBER: builtins.int
    BILLABLE_OBJECT_FIELD_NUMBER: builtins.int
    @property
    def effective_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Timestamp when binding was created."""

    @property
    def billable_object(self) -> global___BillableObject:
        """Object that is bound to billing account."""

    def __init__(
        self,
        *,
        effective_time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        billable_object: global___BillableObject | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["billable_object", b"billable_object", "effective_time", b"effective_time"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["billable_object", b"billable_object", "effective_time", b"effective_time"]) -> None: ...

global___BillableObjectBinding = BillableObjectBinding
