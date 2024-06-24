"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.field_mask_pb2
import google.protobuf.internal.containers
import google.protobuf.message
import typing
import yandex.cloud.compute.v1.instance_pb2
import yandex.cloud.compute.v1.placement_group_pb2
import yandex.cloud.operation.operation_pb2

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class GetPlacementGroupRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PLACEMENT_GROUP_ID_FIELD_NUMBER: builtins.int
    placement_group_id: builtins.str
    """ID of the placement group to return.

    To get a placement group ID make a [PlacementGroupService.List] request.
    """
    def __init__(
        self,
        *,
        placement_group_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["placement_group_id", b"placement_group_id"]) -> None: ...

global___GetPlacementGroupRequest = GetPlacementGroupRequest

@typing.final
class ListPlacementGroupsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FOLDER_ID_FIELD_NUMBER: builtins.int
    PAGE_SIZE_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    FILTER_FIELD_NUMBER: builtins.int
    ORDER_BY_FIELD_NUMBER: builtins.int
    folder_id: builtins.str
    """ID of the folder to list placement groups in.

    To get the folder ID make a [yandex.cloud.resourcemanager.v1.FolderService.List] request.
    """
    page_size: builtins.int
    """The maximum number of results per page to return. If the number of available
    results is larger than [page_size],
    the service returns a [ListPlacementGroupsResponse.next_page_token]
    that can be used to get the next page of results in subsequent list requests.
    """
    page_token: builtins.str
    """Page token. To get the next page of results,
    set [page_token] to the [ListPlacementGroupsResponse.next_page_token]
    returned by a previous list request.
    """
    filter: builtins.str
    """A filter expression that filters resources listed in the response.
    The expression consists of one or more conditions united by `AND` operator: `<condition1> [AND <condition2> [<...> AND <conditionN>]]`.

    Each condition has the form `<field> <operator> <value>`, where:
    1. `<field>` is the field name. Currently you can use filtering only on the limited number of fields.
    2. `<operator>` is a logical operator, one of `=`, `!=`, `IN`, `NOT IN`.
    3. `<value>` represents a value.
    String values should be written in double (`"`) or single (`'`) quotes. C-style escape sequences are supported (`\\"` turns to `"`, `\\'` to `'`, `\\\\` to backslash).
    """
    order_by: builtins.str
    """By which column the listing should be ordered and in which direction,
    format is "createdAt desc". "id asc" if omitted.
    The default sorting order is ascending
    """
    def __init__(
        self,
        *,
        folder_id: builtins.str = ...,
        page_size: builtins.int = ...,
        page_token: builtins.str = ...,
        filter: builtins.str = ...,
        order_by: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["filter", b"filter", "folder_id", b"folder_id", "order_by", b"order_by", "page_size", b"page_size", "page_token", b"page_token"]) -> None: ...

global___ListPlacementGroupsRequest = ListPlacementGroupsRequest

@typing.final
class ListPlacementGroupsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PLACEMENT_GROUPS_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    next_page_token: builtins.str
    """Token for getting the next page of the list. If the number of results is greater than
    the specified [ListPlacementGroupsRequest.page_size], use `next_page_token` as the value
    for the [ListPlacementGroupsRequest.page_token] parameter in the next list request.

    Each subsequent page will have its own `next_page_token` to continue paging through the results.
    """
    @property
    def placement_groups(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.compute.v1.placement_group_pb2.PlacementGroup]:
        """Lists placement groups in the specified folder."""

    def __init__(
        self,
        *,
        placement_groups: collections.abc.Iterable[yandex.cloud.compute.v1.placement_group_pb2.PlacementGroup] | None = ...,
        next_page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["next_page_token", b"next_page_token", "placement_groups", b"placement_groups"]) -> None: ...

global___ListPlacementGroupsResponse = ListPlacementGroupsResponse

@typing.final
class CreatePlacementGroupRequest(google.protobuf.message.Message):
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
    SPREAD_PLACEMENT_STRATEGY_FIELD_NUMBER: builtins.int
    PARTITION_PLACEMENT_STRATEGY_FIELD_NUMBER: builtins.int
    folder_id: builtins.str
    """ID of the folder to create a placement group in.

    To get a folder ID, use a [yandex.cloud.resourcemanager.v1.FolderService.List] request.
    """
    name: builtins.str
    """Name of the placement group."""
    description: builtins.str
    """Description of the placement group."""
    @property
    def labels(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]:
        """Resource labels as `key:value` pairs."""

    @property
    def spread_placement_strategy(self) -> yandex.cloud.compute.v1.placement_group_pb2.SpreadPlacementStrategy:
        """Anti-affinity placement strategy (`spread`). Instances are distributed over distinct failure domains."""

    @property
    def partition_placement_strategy(self) -> yandex.cloud.compute.v1.placement_group_pb2.PartitionPlacementStrategy: ...
    def __init__(
        self,
        *,
        folder_id: builtins.str = ...,
        name: builtins.str = ...,
        description: builtins.str = ...,
        labels: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        spread_placement_strategy: yandex.cloud.compute.v1.placement_group_pb2.SpreadPlacementStrategy | None = ...,
        partition_placement_strategy: yandex.cloud.compute.v1.placement_group_pb2.PartitionPlacementStrategy | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["partition_placement_strategy", b"partition_placement_strategy", "placement_strategy", b"placement_strategy", "spread_placement_strategy", b"spread_placement_strategy"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["description", b"description", "folder_id", b"folder_id", "labels", b"labels", "name", b"name", "partition_placement_strategy", b"partition_placement_strategy", "placement_strategy", b"placement_strategy", "spread_placement_strategy", b"spread_placement_strategy"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["placement_strategy", b"placement_strategy"]) -> typing.Literal["spread_placement_strategy", "partition_placement_strategy"] | None: ...

global___CreatePlacementGroupRequest = CreatePlacementGroupRequest

@typing.final
class CreatePlacementGroupMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PLACEMENT_GROUP_ID_FIELD_NUMBER: builtins.int
    placement_group_id: builtins.str
    """ID of the placement group that is being created."""
    def __init__(
        self,
        *,
        placement_group_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["placement_group_id", b"placement_group_id"]) -> None: ...

global___CreatePlacementGroupMetadata = CreatePlacementGroupMetadata

@typing.final
class UpdatePlacementGroupRequest(google.protobuf.message.Message):
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

    PLACEMENT_GROUP_ID_FIELD_NUMBER: builtins.int
    UPDATE_MASK_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    placement_group_id: builtins.str
    """ID of the placement group to update.

    To get the placement group ID, use an [PlacementGroupService.List] request.
    """
    name: builtins.str
    """Name of the placement group."""
    description: builtins.str
    """Description of the placement group."""
    @property
    def update_mask(self) -> google.protobuf.field_mask_pb2.FieldMask:
        """Field mask that specifies which fields of the PlacementGroup resource should be updated."""

    @property
    def labels(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]:
        """Resource labels as `key:value` pairs.

        The existing set of `labels` is completely replaced by the provided set.
        """

    def __init__(
        self,
        *,
        placement_group_id: builtins.str = ...,
        update_mask: google.protobuf.field_mask_pb2.FieldMask | None = ...,
        name: builtins.str = ...,
        description: builtins.str = ...,
        labels: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["update_mask", b"update_mask"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["description", b"description", "labels", b"labels", "name", b"name", "placement_group_id", b"placement_group_id", "update_mask", b"update_mask"]) -> None: ...

global___UpdatePlacementGroupRequest = UpdatePlacementGroupRequest

@typing.final
class UpdatePlacementGroupMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PLACEMENT_GROUP_ID_FIELD_NUMBER: builtins.int
    placement_group_id: builtins.str
    """ID of the placement group that is being updated."""
    def __init__(
        self,
        *,
        placement_group_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["placement_group_id", b"placement_group_id"]) -> None: ...

global___UpdatePlacementGroupMetadata = UpdatePlacementGroupMetadata

@typing.final
class DeletePlacementGroupRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PLACEMENT_GROUP_ID_FIELD_NUMBER: builtins.int
    placement_group_id: builtins.str
    """ID of the placement group to delete.

    To get the placement group ID, use [PlacementGroupService.List] request.
    """
    def __init__(
        self,
        *,
        placement_group_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["placement_group_id", b"placement_group_id"]) -> None: ...

global___DeletePlacementGroupRequest = DeletePlacementGroupRequest

@typing.final
class DeletePlacementGroupMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PLACEMENT_GROUP_ID_FIELD_NUMBER: builtins.int
    placement_group_id: builtins.str
    """ID of the placement group that is being deleted."""
    def __init__(
        self,
        *,
        placement_group_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["placement_group_id", b"placement_group_id"]) -> None: ...

global___DeletePlacementGroupMetadata = DeletePlacementGroupMetadata

@typing.final
class ListPlacementGroupInstancesRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PLACEMENT_GROUP_ID_FIELD_NUMBER: builtins.int
    PAGE_SIZE_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    placement_group_id: builtins.str
    """ID of the placement group to list instances for.

    To get the placement group ID, use [PlacementGroupService.List] request.
    """
    page_size: builtins.int
    """The maximum number of results per page to return. If the number of available
    results is larger than [page_size],
    the service returns a [ListPlacementGroupInstancesResponse.next_page_token]
    that can be used to get the next page of results in subsequent list requests.
    """
    page_token: builtins.str
    """Page token. To get the next page of results,
    set [page_token] to the [ListPlacementGroupInstancesResponse.next_page_token]
    returned by a previous list request.
    """
    def __init__(
        self,
        *,
        placement_group_id: builtins.str = ...,
        page_size: builtins.int = ...,
        page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["page_size", b"page_size", "page_token", b"page_token", "placement_group_id", b"placement_group_id"]) -> None: ...

global___ListPlacementGroupInstancesRequest = ListPlacementGroupInstancesRequest

@typing.final
class ListPlacementGroupInstancesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INSTANCES_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    next_page_token: builtins.str
    """This token allows you to get the next page of results for list requests. If the number of results
    is more than [ListPlacementGroupInstancesRequest.page_size], use
    [next_page_token] as the value
    for the [ListPlacementGroupInstancesRequest.page_token] query parameter
    in the next list request. Each subsequent list request will have its own
    [next_page_token] to continue paging through the results.
    """
    @property
    def instances(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.compute.v1.instance_pb2.Instance]:
        """Lists instances for the specified placement group."""

    def __init__(
        self,
        *,
        instances: collections.abc.Iterable[yandex.cloud.compute.v1.instance_pb2.Instance] | None = ...,
        next_page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["instances", b"instances", "next_page_token", b"next_page_token"]) -> None: ...

global___ListPlacementGroupInstancesResponse = ListPlacementGroupInstancesResponse

@typing.final
class ListPlacementGroupOperationsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PLACEMENT_GROUP_ID_FIELD_NUMBER: builtins.int
    PAGE_SIZE_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    placement_group_id: builtins.str
    """ID of the placement group to list operations for.

    To get the placement group ID, use [PlacementGroupService.List] request.
    """
    page_size: builtins.int
    """The maximum number of results per page to return. If the number of available
    results is larger than [page_size], the service returns a [ListPlacementGroupOperationsResponse.next_page_token]
    that can be used to get the next page of results in subsequent list requests.
    """
    page_token: builtins.str
    """Page token. To get the next page of results, set [page_token] to the
    [ListPlacementGroupOperationsResponse.next_page_token] returned by a previous list request.
    """
    def __init__(
        self,
        *,
        placement_group_id: builtins.str = ...,
        page_size: builtins.int = ...,
        page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["page_size", b"page_size", "page_token", b"page_token", "placement_group_id", b"placement_group_id"]) -> None: ...

global___ListPlacementGroupOperationsRequest = ListPlacementGroupOperationsRequest

@typing.final
class ListPlacementGroupOperationsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    OPERATIONS_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    next_page_token: builtins.str
    """This token allows you to get the next page of results for list requests. If the number of results
    is larger than [ListPlacementGroupOperationsRequest.page_size], use the [next_page_token] as the value
    for the [ListPlacementGroupOperationsRequest.page_token] query parameter in the next list request.
    Each subsequent list request will have its own [next_page_token] to continue paging through the results.
    """
    @property
    def operations(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.operation.operation_pb2.Operation]:
        """List of operations for the specified placement group."""

    def __init__(
        self,
        *,
        operations: collections.abc.Iterable[yandex.cloud.operation.operation_pb2.Operation] | None = ...,
        next_page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["next_page_token", b"next_page_token", "operations", b"operations"]) -> None: ...

global___ListPlacementGroupOperationsResponse = ListPlacementGroupOperationsResponse
