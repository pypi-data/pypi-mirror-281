"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class Reference(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Type:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _TypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[Reference._Type.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        TYPE_UNSPECIFIED: Reference._Type.ValueType  # 0
        MANAGED_BY: Reference._Type.ValueType  # 1
        USED_BY: Reference._Type.ValueType  # 2

    class Type(_Type, metaclass=_TypeEnumTypeWrapper): ...
    TYPE_UNSPECIFIED: Reference.Type.ValueType  # 0
    MANAGED_BY: Reference.Type.ValueType  # 1
    USED_BY: Reference.Type.ValueType  # 2

    REFERRER_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    type: global___Reference.Type.ValueType
    @property
    def referrer(self) -> global___Referrer: ...
    def __init__(
        self,
        *,
        referrer: global___Referrer | None = ...,
        type: global___Reference.Type.ValueType = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["referrer", b"referrer"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["referrer", b"referrer", "type", b"type"]) -> None: ...

global___Reference = Reference

@typing.final
class Referrer(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TYPE_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    type: builtins.str
    """* `type = compute.instance, id = <instance id>`
    * `type = compute.instanceGroup, id = <instanceGroup id>`
    * `type = loadbalancer.networkLoadBalancer, id = <networkLoadBalancer id>`
    * `type = managed-kubernetes.cluster, id = <cluster id>`
    * `type = managed-mysql.cluster, id = <cluster id>`
    """
    id: builtins.str
    def __init__(
        self,
        *,
        type: builtins.str = ...,
        id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["id", b"id", "type", b"type"]) -> None: ...

global___Referrer = Referrer
