"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import abc
import collections.abc
import grpc
import grpc.aio
import typing
import yandex.cloud.serverless.apigateway.websocket.v1.connection_pb2
import yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class ConnectionServiceStub:
    """A set of methods for managing API Gateway WebSocket connections."""

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    Get: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2.GetConnectionRequest,
        yandex.cloud.serverless.apigateway.websocket.v1.connection_pb2.Connection,
    ]
    """Returns the specified connection info."""

    Send: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2.SendToConnectionRequest,
        yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2.SendToConnectionResponse,
    ]
    """Sends data to the specified connection."""

    Disconnect: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2.DisconnectRequest,
        yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2.DisconnectResponse,
    ]
    """Disconnects the specified connection."""

class ConnectionServiceAsyncStub:
    """A set of methods for managing API Gateway WebSocket connections."""

    Get: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2.GetConnectionRequest,
        yandex.cloud.serverless.apigateway.websocket.v1.connection_pb2.Connection,
    ]
    """Returns the specified connection info."""

    Send: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2.SendToConnectionRequest,
        yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2.SendToConnectionResponse,
    ]
    """Sends data to the specified connection."""

    Disconnect: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2.DisconnectRequest,
        yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2.DisconnectResponse,
    ]
    """Disconnects the specified connection."""

class ConnectionServiceServicer(metaclass=abc.ABCMeta):
    """A set of methods for managing API Gateway WebSocket connections."""

    @abc.abstractmethod
    def Get(
        self,
        request: yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2.GetConnectionRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.serverless.apigateway.websocket.v1.connection_pb2.Connection, collections.abc.Awaitable[yandex.cloud.serverless.apigateway.websocket.v1.connection_pb2.Connection]]:
        """Returns the specified connection info."""

    @abc.abstractmethod
    def Send(
        self,
        request: yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2.SendToConnectionRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2.SendToConnectionResponse, collections.abc.Awaitable[yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2.SendToConnectionResponse]]:
        """Sends data to the specified connection."""

    @abc.abstractmethod
    def Disconnect(
        self,
        request: yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2.DisconnectRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2.DisconnectResponse, collections.abc.Awaitable[yandex.cloud.serverless.apigateway.websocket.v1.connection_service_pb2.DisconnectResponse]]:
        """Disconnects the specified connection."""

def add_ConnectionServiceServicer_to_server(servicer: ConnectionServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
