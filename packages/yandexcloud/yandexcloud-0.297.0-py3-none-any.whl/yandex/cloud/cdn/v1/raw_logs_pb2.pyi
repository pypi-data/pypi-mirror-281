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

class _RawLogsStatus:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _RawLogsStatusEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_RawLogsStatus.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    RAW_LOGS_STATUS_UNSPECIFIED: _RawLogsStatus.ValueType  # 0
    RAW_LOGS_STATUS_NOT_ACTIVATED: _RawLogsStatus.ValueType  # 1
    """Raw logs wasn't activated."""
    RAW_LOGS_STATUS_OK: _RawLogsStatus.ValueType  # 2
    """Raw logs was activated, and logs storing process works as expected."""
    RAW_LOGS_STATUS_FAILED: _RawLogsStatus.ValueType  # 3
    """Raw logs was activated, but CDN provider has been failed to store logs."""
    RAW_LOGS_STATUS_PENDING: _RawLogsStatus.ValueType  # 4
    """Raw logs was activated, but logs storing process is expected."""

class RawLogsStatus(_RawLogsStatus, metaclass=_RawLogsStatusEnumTypeWrapper):
    """Provider side statuses of Raw logs processing."""

RAW_LOGS_STATUS_UNSPECIFIED: RawLogsStatus.ValueType  # 0
RAW_LOGS_STATUS_NOT_ACTIVATED: RawLogsStatus.ValueType  # 1
"""Raw logs wasn't activated."""
RAW_LOGS_STATUS_OK: RawLogsStatus.ValueType  # 2
"""Raw logs was activated, and logs storing process works as expected."""
RAW_LOGS_STATUS_FAILED: RawLogsStatus.ValueType  # 3
"""Raw logs was activated, but CDN provider has been failed to store logs."""
RAW_LOGS_STATUS_PENDING: RawLogsStatus.ValueType  # 4
"""Raw logs was activated, but logs storing process is expected."""
global___RawLogsStatus = RawLogsStatus

@typing.final
class RawLogsSettings(google.protobuf.message.Message):
    """User settings for Raw logs."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    BUCKET_NAME_FIELD_NUMBER: builtins.int
    BUCKET_REGION_FIELD_NUMBER: builtins.int
    FILE_PREFIX_FIELD_NUMBER: builtins.int
    bucket_name: builtins.str
    """Destination S3 bucket name, note that the suer should be owner of the bucket."""
    bucket_region: builtins.str
    """Bucket region, unused for now, could be blank."""
    file_prefix: builtins.str
    """file_prefix: prefix each log object name with specified prefix.

    The prefix makes it simpler for you to locate the log objects.
    For example, if you specify the prefix value logs/, each log object that
    S3 creates begins with the logs/ prefix in its key, so pseudo S3 folders
    could be setup.
    """
    def __init__(
        self,
        *,
        bucket_name: builtins.str = ...,
        bucket_region: builtins.str = ...,
        file_prefix: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["bucket_name", b"bucket_name", "bucket_region", b"bucket_region", "file_prefix", b"file_prefix"]) -> None: ...

global___RawLogsSettings = RawLogsSettings
