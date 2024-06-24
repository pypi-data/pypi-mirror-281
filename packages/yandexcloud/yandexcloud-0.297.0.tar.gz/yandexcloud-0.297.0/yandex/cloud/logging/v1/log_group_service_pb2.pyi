"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.duration_pb2
import google.protobuf.field_mask_pb2
import google.protobuf.internal.containers
import google.protobuf.message
import typing
import yandex.cloud.logging.v1.log_group_pb2
import yandex.cloud.logging.v1.log_resource_pb2
import yandex.cloud.operation.operation_pb2

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class GetLogGroupRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LOG_GROUP_ID_FIELD_NUMBER: builtins.int
    log_group_id: builtins.str
    """ID of the log group to return.

    To get a log group ID make a [LogGroupService.List] request.
    """
    def __init__(
        self,
        *,
        log_group_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["log_group_id", b"log_group_id"]) -> None: ...

global___GetLogGroupRequest = GetLogGroupRequest

@typing.final
class GetLogGroupStatsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LOG_GROUP_ID_FIELD_NUMBER: builtins.int
    log_group_id: builtins.str
    """ID of the log group to return stats for.

    To get a log group ID make a [LogGroupService.List] request.
    """
    def __init__(
        self,
        *,
        log_group_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["log_group_id", b"log_group_id"]) -> None: ...

global___GetLogGroupStatsRequest = GetLogGroupStatsRequest

@typing.final
class ListLogGroupsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FOLDER_ID_FIELD_NUMBER: builtins.int
    PAGE_SIZE_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    FILTER_FIELD_NUMBER: builtins.int
    folder_id: builtins.str
    """Folder ID of the log groups to return.

    To get a folder ID make a [yandex.cloud.resourcemanager.v1.FolderService.List] request.
    """
    page_size: builtins.int
    """The maximum number of results per page to return. If the number of available
    results is larger than `page_size`, the service returns a [ListLogGroupsResponse.next_page_token]
    that can be used to get the next page of results in subsequent list requests.

    Default value: 100.
    """
    page_token: builtins.str
    """Page token. To get the next page of results, set `page_token` to the
    [ListLogGroupsResponse.next_page_token] returned by a previous list request.
    """
    filter: builtins.str
    """A filter expression that filters log groups listed in the response.

    The expression must specify:
    1. The field name. Currently filtering can only be applied to the [LogGroup.name] field.
    2. An `=` operator.
    3. The value in double quotes (`"`). Must be 3-63 characters long and match the regular expression `[a-z][-a-z0-9]{1,61}[a-z0-9]`.
    Example of a filter: `name=my-log-group`.
    """
    def __init__(
        self,
        *,
        folder_id: builtins.str = ...,
        page_size: builtins.int = ...,
        page_token: builtins.str = ...,
        filter: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["filter", b"filter", "folder_id", b"folder_id", "page_size", b"page_size", "page_token", b"page_token"]) -> None: ...

global___ListLogGroupsRequest = ListLogGroupsRequest

@typing.final
class ListLogGroupsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    GROUPS_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    next_page_token: builtins.str
    """Token for getting the next page of the list. If the number of results is greater than
    the specified [ListLogGroupsRequest.page_size], use `next_page_token` as the value
    for the [ListLogGroupsRequest.page_token] parameter in the next list request.

    Each subsequent page will have its own `next_page_token` to continue paging through the results.
    """
    @property
    def groups(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.logging.v1.log_group_pb2.LogGroup]:
        """List of log groups in the specified folder."""

    def __init__(
        self,
        *,
        groups: collections.abc.Iterable[yandex.cloud.logging.v1.log_group_pb2.LogGroup] | None = ...,
        next_page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["groups", b"groups", "next_page_token", b"next_page_token"]) -> None: ...

global___ListLogGroupsResponse = ListLogGroupsResponse

@typing.final
class CreateLogGroupRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class LabelsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.str
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    FOLDER_ID_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    RETENTION_PERIOD_FIELD_NUMBER: builtins.int
    DATA_STREAM_FIELD_NUMBER: builtins.int
    folder_id: builtins.str
    """ID of the folder to create a log group in.

    To get a folder ID make a [yandex.cloud.resourcemanager.v1.FolderService.List] request.
    """
    name: builtins.str
    """Name of the log group.
    The name must be unique within the folder.
    """
    description: builtins.str
    """Description of the log group."""
    data_stream: builtins.str
    """If specified, all log records will be written to this data stream"""
    @property
    def labels(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]:
        """Log group labels as `key:value` pairs."""

    @property
    def retention_period(self) -> google.protobuf.duration_pb2.Duration:
        """Log group entry retention period.

        Entries will be present in group during this period.
        If specified, must be non-negative.
        Empty or zero value is treated as no limit.
        Data stream name
        """

    def __init__(
        self,
        *,
        folder_id: builtins.str = ...,
        name: builtins.str = ...,
        description: builtins.str = ...,
        labels: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        retention_period: google.protobuf.duration_pb2.Duration | None = ...,
        data_stream: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["retention_period", b"retention_period"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["data_stream", b"data_stream", "description", b"description", "folder_id", b"folder_id", "labels", b"labels", "name", b"name", "retention_period", b"retention_period"]) -> None: ...

global___CreateLogGroupRequest = CreateLogGroupRequest

@typing.final
class CreateLogGroupMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LOG_GROUP_ID_FIELD_NUMBER: builtins.int
    log_group_id: builtins.str
    """ID of the log group being created."""
    def __init__(
        self,
        *,
        log_group_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["log_group_id", b"log_group_id"]) -> None: ...

global___CreateLogGroupMetadata = CreateLogGroupMetadata

@typing.final
class UpdateLogGroupRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class LabelsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.str
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    LOG_GROUP_ID_FIELD_NUMBER: builtins.int
    UPDATE_MASK_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    RETENTION_PERIOD_FIELD_NUMBER: builtins.int
    DATA_STREAM_FIELD_NUMBER: builtins.int
    log_group_id: builtins.str
    """ID of the log group to update.

    To get a log group ID make a [LogGroupService.List] request.
    """
    name: builtins.str
    """New name of the log group.
    The name must be unique within the folder.
    """
    description: builtins.str
    """New Description of the log group."""
    data_stream: builtins.str
    """Data stream name

    If specified, log records will be written to this data stream
    """
    @property
    def update_mask(self) -> google.protobuf.field_mask_pb2.FieldMask:
        """Field mask that specifies which attributes of the function should be updated."""

    @property
    def labels(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]:
        """New log group labels as `key:value` pairs."""

    @property
    def retention_period(self) -> google.protobuf.duration_pb2.Duration:
        """New log group entry retention period.

        Entries will be present in group during this period.
        If specified, must be non-negative.
        Empty or zero value is treated as no limit.
        """

    def __init__(
        self,
        *,
        log_group_id: builtins.str = ...,
        update_mask: google.protobuf.field_mask_pb2.FieldMask | None = ...,
        name: builtins.str = ...,
        description: builtins.str = ...,
        labels: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        retention_period: google.protobuf.duration_pb2.Duration | None = ...,
        data_stream: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["retention_period", b"retention_period", "update_mask", b"update_mask"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["data_stream", b"data_stream", "description", b"description", "labels", b"labels", "log_group_id", b"log_group_id", "name", b"name", "retention_period", b"retention_period", "update_mask", b"update_mask"]) -> None: ...

global___UpdateLogGroupRequest = UpdateLogGroupRequest

@typing.final
class UpdateLogGroupMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LOG_GROUP_ID_FIELD_NUMBER: builtins.int
    log_group_id: builtins.str
    """ID of the log group being updated."""
    def __init__(
        self,
        *,
        log_group_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["log_group_id", b"log_group_id"]) -> None: ...

global___UpdateLogGroupMetadata = UpdateLogGroupMetadata

@typing.final
class DeleteLogGroupRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LOG_GROUP_ID_FIELD_NUMBER: builtins.int
    log_group_id: builtins.str
    """ID of the log group to delete.

    To get a log group ID make a [LogGroupService.List] request.
    """
    def __init__(
        self,
        *,
        log_group_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["log_group_id", b"log_group_id"]) -> None: ...

global___DeleteLogGroupRequest = DeleteLogGroupRequest

@typing.final
class DeleteLogGroupMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LOG_GROUP_ID_FIELD_NUMBER: builtins.int
    log_group_id: builtins.str
    """ID of the log group being deleted."""
    def __init__(
        self,
        *,
        log_group_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["log_group_id", b"log_group_id"]) -> None: ...

global___DeleteLogGroupMetadata = DeleteLogGroupMetadata

@typing.final
class ListResourcesRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LOG_GROUP_ID_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    log_group_id: builtins.str
    """ID of the log group to list resources for.

    To get a log group ID make a [LogGroupService.List] request.
    """
    type: builtins.str
    """Resource type to return resources for.

    If not specified, [ListResourcesResponse] will contain information about all resource types.
    """
    def __init__(
        self,
        *,
        log_group_id: builtins.str = ...,
        type: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["log_group_id", b"log_group_id", "type", b"type"]) -> None: ...

global___ListResourcesRequest = ListResourcesRequest

@typing.final
class ListResourcesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCES_FIELD_NUMBER: builtins.int
    @property
    def resources(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.logging.v1.log_resource_pb2.LogGroupResource]:
        """List of resources present in log group."""

    def __init__(
        self,
        *,
        resources: collections.abc.Iterable[yandex.cloud.logging.v1.log_resource_pb2.LogGroupResource] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["resources", b"resources"]) -> None: ...

global___ListResourcesResponse = ListResourcesResponse

@typing.final
class ListOperationsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LOG_GROUP_ID_FIELD_NUMBER: builtins.int
    PAGE_SIZE_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    FILTER_FIELD_NUMBER: builtins.int
    log_group_id: builtins.str
    """ID of the log group to list operations for.

    To get a log group ID make a [LogGroupService.List] request.
    """
    page_size: builtins.int
    """The maximum number of results per page to return. If the number of available
    results is larger than `page_size`, the service returns a [ListOperationsResponse.next_page_token]
    that can be used to get the next page of results in subsequent list requests.

    Default value: 100.
    """
    page_token: builtins.str
    """Page token. To get the next page of results, set `page_token` to the
    [ListOperationsResponse.next_page_token] returned by a previous list request.
    """
    filter: builtins.str
    """A filter expression that filters resources listed in the response.

    The expression must specify:
    1. The field name. Currently filtering can be applied to the [operation.Operation.description], [operation.Operation.created_at], [operation.Operation.modified_at], [operation.Operation.created_by], [operation.Operation.done] fields.
    2. An `=` operator.
    3. The value in double quotes (`"`). Must be 3-63 characters long and match the regular expression `[a-z][-a-z0-9]{1,61}[a-z0-9]`.
    Examples of a filter: `done=false`, `created_by='John.Doe'`.
    """
    def __init__(
        self,
        *,
        log_group_id: builtins.str = ...,
        page_size: builtins.int = ...,
        page_token: builtins.str = ...,
        filter: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["filter", b"filter", "log_group_id", b"log_group_id", "page_size", b"page_size", "page_token", b"page_token"]) -> None: ...

global___ListOperationsRequest = ListOperationsRequest

@typing.final
class ListOperationsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    OPERATIONS_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    next_page_token: builtins.str
    """Token for getting the next page of the list. If the number of results is greater than
    the specified [ListOperationsRequest.page_size], use `next_page_token` as the value
    for the [ListOperationsRequest.page_token] parameter in the next list request.

    Each subsequent page will have its own `next_page_token` to continue paging through the results.
    """
    @property
    def operations(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.operation.operation_pb2.Operation]:
        """List of operations for the specified log group."""

    def __init__(
        self,
        *,
        operations: collections.abc.Iterable[yandex.cloud.operation.operation_pb2.Operation] | None = ...,
        next_page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["next_page_token", b"next_page_token", "operations", b"operations"]) -> None: ...

global___ListOperationsResponse = ListOperationsResponse

@typing.final
class GetLogGroupStatsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LOG_GROUP_ID_FIELD_NUMBER: builtins.int
    BYTES_FIELD_NUMBER: builtins.int
    RECORDS_FIELD_NUMBER: builtins.int
    log_group_id: builtins.str
    """Log group ID the stats are returned for."""
    bytes: builtins.int
    """Size of data in log group in bytes."""
    records: builtins.int
    """Amount of records in log group."""
    def __init__(
        self,
        *,
        log_group_id: builtins.str = ...,
        bytes: builtins.int = ...,
        records: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["bytes", b"bytes", "log_group_id", b"log_group_id", "records", b"records"]) -> None: ...

global___GetLogGroupStatsResponse = GetLogGroupStatsResponse
