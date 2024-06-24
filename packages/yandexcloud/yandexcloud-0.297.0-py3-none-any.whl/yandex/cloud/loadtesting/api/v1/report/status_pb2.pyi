"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _Status:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _StatusEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_Status.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    STATUS_UNSPECIFIED: _Status.ValueType  # 0
    """Status is not specified."""
    COLLECTING: _Status.ValueType  # 1
    """Report is being collected."""
    CALCULATING: _Status.ValueType  # 2
    """Report is being calculated."""
    READY: _Status.ValueType  # 3
    """Report is ready."""

class Status(_Status, metaclass=_StatusEnumTypeWrapper):
    """Report status."""

STATUS_UNSPECIFIED: Status.ValueType  # 0
"""Status is not specified."""
COLLECTING: Status.ValueType  # 1
"""Report is being collected."""
CALCULATING: Status.ValueType  # 2
"""Report is being calculated."""
READY: Status.ValueType  # 3
"""Report is ready."""
global___Status = Status
