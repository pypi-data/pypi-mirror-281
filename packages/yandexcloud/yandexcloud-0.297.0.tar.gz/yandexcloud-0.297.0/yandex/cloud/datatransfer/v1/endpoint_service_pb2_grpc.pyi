"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import abc
import collections.abc
import grpc
import grpc.aio
import typing
import yandex.cloud.datatransfer.v1.endpoint_pb2
import yandex.cloud.datatransfer.v1.endpoint_service_pb2
import yandex.cloud.operation.operation_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class EndpointServiceStub:
    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    Get: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.datatransfer.v1.endpoint_service_pb2.GetEndpointRequest,
        yandex.cloud.datatransfer.v1.endpoint_pb2.Endpoint,
    ]

    List: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.datatransfer.v1.endpoint_service_pb2.ListEndpointsRequest,
        yandex.cloud.datatransfer.v1.endpoint_service_pb2.ListEndpointsResponse,
    ]

    Create: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.datatransfer.v1.endpoint_service_pb2.CreateEndpointRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]

    Update: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.datatransfer.v1.endpoint_service_pb2.UpdateEndpointRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]

    Delete: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.datatransfer.v1.endpoint_service_pb2.DeleteEndpointRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]

class EndpointServiceAsyncStub:
    Get: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.datatransfer.v1.endpoint_service_pb2.GetEndpointRequest,
        yandex.cloud.datatransfer.v1.endpoint_pb2.Endpoint,
    ]

    List: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.datatransfer.v1.endpoint_service_pb2.ListEndpointsRequest,
        yandex.cloud.datatransfer.v1.endpoint_service_pb2.ListEndpointsResponse,
    ]

    Create: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.datatransfer.v1.endpoint_service_pb2.CreateEndpointRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]

    Update: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.datatransfer.v1.endpoint_service_pb2.UpdateEndpointRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]

    Delete: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.datatransfer.v1.endpoint_service_pb2.DeleteEndpointRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]

class EndpointServiceServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def Get(
        self,
        request: yandex.cloud.datatransfer.v1.endpoint_service_pb2.GetEndpointRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.datatransfer.v1.endpoint_pb2.Endpoint, collections.abc.Awaitable[yandex.cloud.datatransfer.v1.endpoint_pb2.Endpoint]]: ...

    @abc.abstractmethod
    def List(
        self,
        request: yandex.cloud.datatransfer.v1.endpoint_service_pb2.ListEndpointsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.datatransfer.v1.endpoint_service_pb2.ListEndpointsResponse, collections.abc.Awaitable[yandex.cloud.datatransfer.v1.endpoint_service_pb2.ListEndpointsResponse]]: ...

    @abc.abstractmethod
    def Create(
        self,
        request: yandex.cloud.datatransfer.v1.endpoint_service_pb2.CreateEndpointRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]: ...

    @abc.abstractmethod
    def Update(
        self,
        request: yandex.cloud.datatransfer.v1.endpoint_service_pb2.UpdateEndpointRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]: ...

    @abc.abstractmethod
    def Delete(
        self,
        request: yandex.cloud.datatransfer.v1.endpoint_service_pb2.DeleteEndpointRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]: ...

def add_EndpointServiceServicer_to_server(servicer: EndpointServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
