"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import abc
import collections.abc
import grpc
import grpc.aio
import typing
import yandex.cloud.access.access_pb2
import yandex.cloud.operation.operation_pb2
import yandex.cloud.organizationmanager.v1.group_pb2
import yandex.cloud.organizationmanager.v1.group_service_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class GroupServiceStub:
    """A set of methods for managing groups."""

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    Get: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.organizationmanager.v1.group_service_pb2.GetGroupRequest,
        yandex.cloud.organizationmanager.v1.group_pb2.Group,
    ]
    """Returns the specified Group resource.

    To get the list of available Group resources, make a [List] request.
    """

    List: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupsRequest,
        yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupsResponse,
    ]
    """Retrieves the list of group resources."""

    Create: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.organizationmanager.v1.group_service_pb2.CreateGroupRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Creates a group in the specified organization."""

    Update: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.organizationmanager.v1.group_service_pb2.UpdateGroupRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Updates the specified group."""

    Delete: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.organizationmanager.v1.group_service_pb2.DeleteGroupRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Deletes the specified group."""

    ListOperations: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupOperationsRequest,
        yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupOperationsResponse,
    ]
    """Lists operations for the specified group."""

    ListMembers: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupMembersRequest,
        yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupMembersResponse,
    ]
    """members

    List group active members.
    """

    UpdateMembers: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.organizationmanager.v1.group_service_pb2.UpdateGroupMembersRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Update group members."""

    ListAccessBindings: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.ListAccessBindingsRequest,
        yandex.cloud.access.access_pb2.ListAccessBindingsResponse,
    ]
    """access

    Lists access bindings for the specified group.
    """

    SetAccessBindings: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.SetAccessBindingsRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Sets access bindings for the specified group."""

    UpdateAccessBindings: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.UpdateAccessBindingsRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Updates access bindings for the specified group."""

class GroupServiceAsyncStub:
    """A set of methods for managing groups."""

    Get: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.organizationmanager.v1.group_service_pb2.GetGroupRequest,
        yandex.cloud.organizationmanager.v1.group_pb2.Group,
    ]
    """Returns the specified Group resource.

    To get the list of available Group resources, make a [List] request.
    """

    List: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupsRequest,
        yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupsResponse,
    ]
    """Retrieves the list of group resources."""

    Create: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.organizationmanager.v1.group_service_pb2.CreateGroupRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Creates a group in the specified organization."""

    Update: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.organizationmanager.v1.group_service_pb2.UpdateGroupRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Updates the specified group."""

    Delete: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.organizationmanager.v1.group_service_pb2.DeleteGroupRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Deletes the specified group."""

    ListOperations: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupOperationsRequest,
        yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupOperationsResponse,
    ]
    """Lists operations for the specified group."""

    ListMembers: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupMembersRequest,
        yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupMembersResponse,
    ]
    """members

    List group active members.
    """

    UpdateMembers: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.organizationmanager.v1.group_service_pb2.UpdateGroupMembersRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Update group members."""

    ListAccessBindings: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.ListAccessBindingsRequest,
        yandex.cloud.access.access_pb2.ListAccessBindingsResponse,
    ]
    """access

    Lists access bindings for the specified group.
    """

    SetAccessBindings: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.SetAccessBindingsRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Sets access bindings for the specified group."""

    UpdateAccessBindings: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.UpdateAccessBindingsRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Updates access bindings for the specified group."""

class GroupServiceServicer(metaclass=abc.ABCMeta):
    """A set of methods for managing groups."""

    @abc.abstractmethod
    def Get(
        self,
        request: yandex.cloud.organizationmanager.v1.group_service_pb2.GetGroupRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.organizationmanager.v1.group_pb2.Group, collections.abc.Awaitable[yandex.cloud.organizationmanager.v1.group_pb2.Group]]:
        """Returns the specified Group resource.

        To get the list of available Group resources, make a [List] request.
        """

    @abc.abstractmethod
    def List(
        self,
        request: yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupsResponse, collections.abc.Awaitable[yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupsResponse]]:
        """Retrieves the list of group resources."""

    @abc.abstractmethod
    def Create(
        self,
        request: yandex.cloud.organizationmanager.v1.group_service_pb2.CreateGroupRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Creates a group in the specified organization."""

    @abc.abstractmethod
    def Update(
        self,
        request: yandex.cloud.organizationmanager.v1.group_service_pb2.UpdateGroupRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Updates the specified group."""

    @abc.abstractmethod
    def Delete(
        self,
        request: yandex.cloud.organizationmanager.v1.group_service_pb2.DeleteGroupRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Deletes the specified group."""

    @abc.abstractmethod
    def ListOperations(
        self,
        request: yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupOperationsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupOperationsResponse, collections.abc.Awaitable[yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupOperationsResponse]]:
        """Lists operations for the specified group."""

    @abc.abstractmethod
    def ListMembers(
        self,
        request: yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupMembersRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupMembersResponse, collections.abc.Awaitable[yandex.cloud.organizationmanager.v1.group_service_pb2.ListGroupMembersResponse]]:
        """members

        List group active members.
        """

    @abc.abstractmethod
    def UpdateMembers(
        self,
        request: yandex.cloud.organizationmanager.v1.group_service_pb2.UpdateGroupMembersRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Update group members."""

    @abc.abstractmethod
    def ListAccessBindings(
        self,
        request: yandex.cloud.access.access_pb2.ListAccessBindingsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.access.access_pb2.ListAccessBindingsResponse, collections.abc.Awaitable[yandex.cloud.access.access_pb2.ListAccessBindingsResponse]]:
        """access

        Lists access bindings for the specified group.
        """

    @abc.abstractmethod
    def SetAccessBindings(
        self,
        request: yandex.cloud.access.access_pb2.SetAccessBindingsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Sets access bindings for the specified group."""

    @abc.abstractmethod
    def UpdateAccessBindings(
        self,
        request: yandex.cloud.access.access_pb2.UpdateAccessBindingsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Updates access bindings for the specified group."""

def add_GroupServiceServicer_to_server(servicer: GroupServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
