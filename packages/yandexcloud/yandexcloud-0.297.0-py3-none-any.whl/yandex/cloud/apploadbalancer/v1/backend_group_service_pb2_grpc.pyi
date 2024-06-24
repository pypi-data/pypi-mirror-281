"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import abc
import collections.abc
import grpc
import grpc.aio
import typing
import yandex.cloud.apploadbalancer.v1.backend_group_pb2
import yandex.cloud.apploadbalancer.v1.backend_group_service_pb2
import yandex.cloud.operation.operation_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class BackendGroupServiceStub:
    """A set of methods for managing backend groups."""

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    Get: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.GetBackendGroupRequest,
        yandex.cloud.apploadbalancer.v1.backend_group_pb2.BackendGroup,
    ]
    """Returns the specified backend group.

    To get the list of all available backend groups, make a [List] request.
    """

    List: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.ListBackendGroupsRequest,
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.ListBackendGroupsResponse,
    ]
    """Lists backend groups in the specified folder."""

    Create: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.CreateBackendGroupRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Creates a backend group in the specified folder."""

    Update: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.UpdateBackendGroupRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Updates the specified backend group."""

    Delete: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.DeleteBackendGroupRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Deletes the specified backend group."""

    AddBackend: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.AddBackendRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Adds backends to the specified backend group."""

    RemoveBackend: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.RemoveBackendRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Removes backends from the specified backend group."""

    UpdateBackend: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.UpdateBackendRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Updates the specified backend."""

    ListOperations: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.ListBackendGroupOperationsRequest,
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.ListBackendGroupOperationsResponse,
    ]
    """Lists operations for the specified backend group."""

class BackendGroupServiceAsyncStub:
    """A set of methods for managing backend groups."""

    Get: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.GetBackendGroupRequest,
        yandex.cloud.apploadbalancer.v1.backend_group_pb2.BackendGroup,
    ]
    """Returns the specified backend group.

    To get the list of all available backend groups, make a [List] request.
    """

    List: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.ListBackendGroupsRequest,
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.ListBackendGroupsResponse,
    ]
    """Lists backend groups in the specified folder."""

    Create: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.CreateBackendGroupRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Creates a backend group in the specified folder."""

    Update: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.UpdateBackendGroupRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Updates the specified backend group."""

    Delete: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.DeleteBackendGroupRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Deletes the specified backend group."""

    AddBackend: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.AddBackendRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Adds backends to the specified backend group."""

    RemoveBackend: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.RemoveBackendRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Removes backends from the specified backend group."""

    UpdateBackend: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.UpdateBackendRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Updates the specified backend."""

    ListOperations: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.ListBackendGroupOperationsRequest,
        yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.ListBackendGroupOperationsResponse,
    ]
    """Lists operations for the specified backend group."""

class BackendGroupServiceServicer(metaclass=abc.ABCMeta):
    """A set of methods for managing backend groups."""

    @abc.abstractmethod
    def Get(
        self,
        request: yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.GetBackendGroupRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.apploadbalancer.v1.backend_group_pb2.BackendGroup, collections.abc.Awaitable[yandex.cloud.apploadbalancer.v1.backend_group_pb2.BackendGroup]]:
        """Returns the specified backend group.

        To get the list of all available backend groups, make a [List] request.
        """

    @abc.abstractmethod
    def List(
        self,
        request: yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.ListBackendGroupsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.ListBackendGroupsResponse, collections.abc.Awaitable[yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.ListBackendGroupsResponse]]:
        """Lists backend groups in the specified folder."""

    @abc.abstractmethod
    def Create(
        self,
        request: yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.CreateBackendGroupRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Creates a backend group in the specified folder."""

    @abc.abstractmethod
    def Update(
        self,
        request: yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.UpdateBackendGroupRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Updates the specified backend group."""

    @abc.abstractmethod
    def Delete(
        self,
        request: yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.DeleteBackendGroupRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Deletes the specified backend group."""

    @abc.abstractmethod
    def AddBackend(
        self,
        request: yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.AddBackendRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Adds backends to the specified backend group."""

    @abc.abstractmethod
    def RemoveBackend(
        self,
        request: yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.RemoveBackendRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Removes backends from the specified backend group."""

    @abc.abstractmethod
    def UpdateBackend(
        self,
        request: yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.UpdateBackendRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Updates the specified backend."""

    @abc.abstractmethod
    def ListOperations(
        self,
        request: yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.ListBackendGroupOperationsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.ListBackendGroupOperationsResponse, collections.abc.Awaitable[yandex.cloud.apploadbalancer.v1.backend_group_service_pb2.ListBackendGroupOperationsResponse]]:
        """Lists operations for the specified backend group."""

def add_BackendGroupServiceServicer_to_server(servicer: BackendGroupServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
