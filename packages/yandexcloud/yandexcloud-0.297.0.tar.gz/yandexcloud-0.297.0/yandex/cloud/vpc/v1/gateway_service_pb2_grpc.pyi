"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import abc
import collections.abc
import grpc
import grpc.aio
import typing
import yandex.cloud.operation.operation_pb2
import yandex.cloud.vpc.v1.gateway_pb2
import yandex.cloud.vpc.v1.gateway_service_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class GatewayServiceStub:
    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    Get: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.vpc.v1.gateway_service_pb2.GetGatewayRequest,
        yandex.cloud.vpc.v1.gateway_pb2.Gateway,
    ]
    """Returns the specified Gateway resource.

    To get the list of all available Gateway resources, make a [List] request.
    """

    List: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.vpc.v1.gateway_service_pb2.ListGatewaysRequest,
        yandex.cloud.vpc.v1.gateway_service_pb2.ListGatewaysResponse,
    ]
    """Retrieves the list of Gateway resources in the specified folder."""

    Create: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.vpc.v1.gateway_service_pb2.CreateGatewayRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Creates a gateway in the specified folder."""

    Update: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.vpc.v1.gateway_service_pb2.UpdateGatewayRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Updates the specified gateway."""

    Delete: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.vpc.v1.gateway_service_pb2.DeleteGatewayRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Deletes the specified gateway."""

    ListOperations: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.vpc.v1.gateway_service_pb2.ListGatewayOperationsRequest,
        yandex.cloud.vpc.v1.gateway_service_pb2.ListGatewayOperationsResponse,
    ]
    """List operations for the specified gateway."""

    Move: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.vpc.v1.gateway_service_pb2.MoveGatewayRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Move a gateway to another folder"""

class GatewayServiceAsyncStub:
    Get: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.vpc.v1.gateway_service_pb2.GetGatewayRequest,
        yandex.cloud.vpc.v1.gateway_pb2.Gateway,
    ]
    """Returns the specified Gateway resource.

    To get the list of all available Gateway resources, make a [List] request.
    """

    List: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.vpc.v1.gateway_service_pb2.ListGatewaysRequest,
        yandex.cloud.vpc.v1.gateway_service_pb2.ListGatewaysResponse,
    ]
    """Retrieves the list of Gateway resources in the specified folder."""

    Create: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.vpc.v1.gateway_service_pb2.CreateGatewayRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Creates a gateway in the specified folder."""

    Update: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.vpc.v1.gateway_service_pb2.UpdateGatewayRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Updates the specified gateway."""

    Delete: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.vpc.v1.gateway_service_pb2.DeleteGatewayRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Deletes the specified gateway."""

    ListOperations: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.vpc.v1.gateway_service_pb2.ListGatewayOperationsRequest,
        yandex.cloud.vpc.v1.gateway_service_pb2.ListGatewayOperationsResponse,
    ]
    """List operations for the specified gateway."""

    Move: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.vpc.v1.gateway_service_pb2.MoveGatewayRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Move a gateway to another folder"""

class GatewayServiceServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def Get(
        self,
        request: yandex.cloud.vpc.v1.gateway_service_pb2.GetGatewayRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.vpc.v1.gateway_pb2.Gateway, collections.abc.Awaitable[yandex.cloud.vpc.v1.gateway_pb2.Gateway]]:
        """Returns the specified Gateway resource.

        To get the list of all available Gateway resources, make a [List] request.
        """

    @abc.abstractmethod
    def List(
        self,
        request: yandex.cloud.vpc.v1.gateway_service_pb2.ListGatewaysRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.vpc.v1.gateway_service_pb2.ListGatewaysResponse, collections.abc.Awaitable[yandex.cloud.vpc.v1.gateway_service_pb2.ListGatewaysResponse]]:
        """Retrieves the list of Gateway resources in the specified folder."""

    @abc.abstractmethod
    def Create(
        self,
        request: yandex.cloud.vpc.v1.gateway_service_pb2.CreateGatewayRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Creates a gateway in the specified folder."""

    @abc.abstractmethod
    def Update(
        self,
        request: yandex.cloud.vpc.v1.gateway_service_pb2.UpdateGatewayRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Updates the specified gateway."""

    @abc.abstractmethod
    def Delete(
        self,
        request: yandex.cloud.vpc.v1.gateway_service_pb2.DeleteGatewayRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Deletes the specified gateway."""

    @abc.abstractmethod
    def ListOperations(
        self,
        request: yandex.cloud.vpc.v1.gateway_service_pb2.ListGatewayOperationsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.vpc.v1.gateway_service_pb2.ListGatewayOperationsResponse, collections.abc.Awaitable[yandex.cloud.vpc.v1.gateway_service_pb2.ListGatewayOperationsResponse]]:
        """List operations for the specified gateway."""

    @abc.abstractmethod
    def Move(
        self,
        request: yandex.cloud.vpc.v1.gateway_service_pb2.MoveGatewayRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Move a gateway to another folder"""

def add_GatewayServiceServicer_to_server(servicer: GatewayServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
