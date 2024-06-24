"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing
import yandex.cloud.backup.v1.resource_pb2
import yandex.cloud.operation.operation_pb2

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class ListResourcesRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FOLDER_ID_FIELD_NUMBER: builtins.int
    PAGE_SIZE_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    folder_id: builtins.str
    """Folder ID."""
    page_size: builtins.int
    """Number of results per page."""
    page_token: builtins.str
    """Token for the results page."""
    def __init__(
        self,
        *,
        folder_id: builtins.str = ...,
        page_size: builtins.int = ...,
        page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["folder_id", b"folder_id", "page_size", b"page_size", "page_token", b"page_token"]) -> None: ...

global___ListResourcesRequest = ListResourcesRequest

@typing.final
class ListResourcesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCES_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    next_page_token: builtins.str
    """Token for the next results page."""
    @property
    def resources(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.backup.v1.resource_pb2.Resource]:
        """Set of resource parameters."""

    def __init__(
        self,
        *,
        resources: collections.abc.Iterable[yandex.cloud.backup.v1.resource_pb2.Resource] | None = ...,
        next_page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["next_page_token", b"next_page_token", "resources", b"resources"]) -> None: ...

global___ListResourcesResponse = ListResourcesResponse

@typing.final
class GetResourceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COMPUTE_INSTANCE_ID_FIELD_NUMBER: builtins.int
    compute_instance_id: builtins.str
    """Compute Cloud instance ID."""
    def __init__(
        self,
        *,
        compute_instance_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["compute_instance_id", b"compute_instance_id"]) -> None: ...

global___GetResourceRequest = GetResourceRequest

@typing.final
class GetResourceResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_FIELD_NUMBER: builtins.int
    @property
    def resource(self) -> yandex.cloud.backup.v1.resource_pb2.Resource:
        """Set of resource parameters."""

    def __init__(
        self,
        *,
        resource: yandex.cloud.backup.v1.resource_pb2.Resource | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["resource", b"resource"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["resource", b"resource"]) -> None: ...

global___GetResourceResponse = GetResourceResponse

@typing.final
class DeleteResourceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COMPUTE_INSTANCE_ID_FIELD_NUMBER: builtins.int
    RESOURCE_ID_FIELD_NUMBER: builtins.int
    compute_instance_id: builtins.str
    """Compute Cloud instance ID."""
    resource_id: builtins.str
    """Resource ID is used to identify Compute Cloud instance in backup service."""
    def __init__(
        self,
        *,
        compute_instance_id: builtins.str = ...,
        resource_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["compute_instance_id", b"compute_instance_id", "resource_id", b"resource_id"]) -> None: ...

global___DeleteResourceRequest = DeleteResourceRequest

@typing.final
class DeleteResourceMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COMPUTE_INSTANCE_ID_FIELD_NUMBER: builtins.int
    compute_instance_id: builtins.str
    """Compute Cloud instance ID."""
    def __init__(
        self,
        *,
        compute_instance_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["compute_instance_id", b"compute_instance_id"]) -> None: ...

global___DeleteResourceMetadata = DeleteResourceMetadata

@typing.final
class ListTasksRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COMPUTE_INSTANCE_ID_FIELD_NUMBER: builtins.int
    PAGE_SIZE_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    compute_instance_id: builtins.str
    """Compute Cloud instance ID."""
    page_size: builtins.int
    """Number of results per page."""
    page_token: builtins.str
    """Token for the results page."""
    def __init__(
        self,
        *,
        compute_instance_id: builtins.str = ...,
        page_size: builtins.int = ...,
        page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["compute_instance_id", b"compute_instance_id", "page_size", b"page_size", "page_token", b"page_token"]) -> None: ...

global___ListTasksRequest = ListTasksRequest

@typing.final
class ListTasksResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TASKS_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    next_page_token: builtins.str
    """Token for the next results page."""
    @property
    def tasks(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.backup.v1.resource_pb2.Task]:
        """Set of tasks parameters."""

    def __init__(
        self,
        *,
        tasks: collections.abc.Iterable[yandex.cloud.backup.v1.resource_pb2.Task] | None = ...,
        next_page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["next_page_token", b"next_page_token", "tasks", b"tasks"]) -> None: ...

global___ListTasksResponse = ListTasksResponse

@typing.final
class ListDirectoryRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FOLDER_ID_FIELD_NUMBER: builtins.int
    COMPUTE_INSTANCE_ID_FIELD_NUMBER: builtins.int
    PATH_FIELD_NUMBER: builtins.int
    folder_id: builtins.str
    """Folder ID."""
    compute_instance_id: builtins.str
    """Compute Cloud instance ID."""
    path: builtins.str
    """Path to list items in."""
    def __init__(
        self,
        *,
        folder_id: builtins.str = ...,
        compute_instance_id: builtins.str = ...,
        path: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["compute_instance_id", b"compute_instance_id", "folder_id", b"folder_id", "path", b"path"]) -> None: ...

global___ListDirectoryRequest = ListDirectoryRequest

@typing.final
class ListDirectoryResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class FilesystemItem(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        class _Type:
            ValueType = typing.NewType("ValueType", builtins.int)
            V: typing_extensions.TypeAlias = ValueType

        class _TypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ListDirectoryResponse.FilesystemItem._Type.ValueType], builtins.type):
            DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
            TYPE_UNSPECIFIED: ListDirectoryResponse.FilesystemItem._Type.ValueType  # 0
            VOLUME: ListDirectoryResponse.FilesystemItem._Type.ValueType  # 1
            DIRECTORY: ListDirectoryResponse.FilesystemItem._Type.ValueType  # 2
            FILE: ListDirectoryResponse.FilesystemItem._Type.ValueType  # 3

        class Type(_Type, metaclass=_TypeEnumTypeWrapper): ...
        TYPE_UNSPECIFIED: ListDirectoryResponse.FilesystemItem.Type.ValueType  # 0
        VOLUME: ListDirectoryResponse.FilesystemItem.Type.ValueType  # 1
        DIRECTORY: ListDirectoryResponse.FilesystemItem.Type.ValueType  # 2
        FILE: ListDirectoryResponse.FilesystemItem.Type.ValueType  # 3

        NAME_FIELD_NUMBER: builtins.int
        TYPE_FIELD_NUMBER: builtins.int
        FILE_TYPE_FIELD_NUMBER: builtins.int
        SIZE_FIELD_NUMBER: builtins.int
        name: builtins.str
        """Item name."""
        type: global___ListDirectoryResponse.FilesystemItem.Type.ValueType
        """Might be Volume, Directory of File."""
        file_type: global___ListDirectoryResponse.FilesystemItem.Type.ValueType
        """Might be Directory or File."""
        size: builtins.int
        def __init__(
            self,
            *,
            name: builtins.str = ...,
            type: global___ListDirectoryResponse.FilesystemItem.Type.ValueType = ...,
            file_type: global___ListDirectoryResponse.FilesystemItem.Type.ValueType = ...,
            size: builtins.int = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["file_type", b"file_type", "name", b"name", "size", b"size", "type", b"type"]) -> None: ...

    ITEMS_FIELD_NUMBER: builtins.int
    @property
    def items(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ListDirectoryResponse.FilesystemItem]: ...
    def __init__(
        self,
        *,
        items: collections.abc.Iterable[global___ListDirectoryResponse.FilesystemItem] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["items", b"items"]) -> None: ...

global___ListDirectoryResponse = ListDirectoryResponse

@typing.final
class CreateDirectoryRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FOLDER_ID_FIELD_NUMBER: builtins.int
    COMPUTE_INSTANCE_ID_FIELD_NUMBER: builtins.int
    PATH_FIELD_NUMBER: builtins.int
    folder_id: builtins.str
    """Folder ID."""
    compute_instance_id: builtins.str
    """Compute Cloud instance ID."""
    path: builtins.str
    """Path to create directory in."""
    def __init__(
        self,
        *,
        folder_id: builtins.str = ...,
        compute_instance_id: builtins.str = ...,
        path: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["compute_instance_id", b"compute_instance_id", "folder_id", b"folder_id", "path", b"path"]) -> None: ...

global___CreateDirectoryRequest = CreateDirectoryRequest

@typing.final
class CreateDirectoryMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COMPUTE_INSTANCE_ID_FIELD_NUMBER: builtins.int
    PATH_FIELD_NUMBER: builtins.int
    compute_instance_id: builtins.str
    """Compute Cloud instance ID."""
    path: builtins.str
    """Path to create directory metadata in."""
    def __init__(
        self,
        *,
        compute_instance_id: builtins.str = ...,
        path: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["compute_instance_id", b"compute_instance_id", "path", b"path"]) -> None: ...

global___CreateDirectoryMetadata = CreateDirectoryMetadata

@typing.final
class ListResourceOperationsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COMPUTE_INSTANCE_ID_FIELD_NUMBER: builtins.int
    PAGE_SIZE_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    compute_instance_id: builtins.str
    """Compute Cloud instance ID."""
    page_size: builtins.int
    """Number of results per page."""
    page_token: builtins.str
    """Token for the results page."""
    def __init__(
        self,
        *,
        compute_instance_id: builtins.str = ...,
        page_size: builtins.int = ...,
        page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["compute_instance_id", b"compute_instance_id", "page_size", b"page_size", "page_token", b"page_token"]) -> None: ...

global___ListResourceOperationsRequest = ListResourceOperationsRequest

@typing.final
class ListResourceOperationsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    OPERATIONS_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    next_page_token: builtins.str
    """Token for the next results page."""
    @property
    def operations(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.operation.operation_pb2.Operation]:
        """List of operations for the specified instance."""

    def __init__(
        self,
        *,
        operations: collections.abc.Iterable[yandex.cloud.operation.operation_pb2.Operation] | None = ...,
        next_page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["next_page_token", b"next_page_token", "operations", b"operations"]) -> None: ...

global___ListResourceOperationsResponse = ListResourceOperationsResponse
