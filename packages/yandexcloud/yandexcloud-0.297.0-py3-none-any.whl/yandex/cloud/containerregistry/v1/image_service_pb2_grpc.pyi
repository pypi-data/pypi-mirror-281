"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import abc
import collections.abc
import grpc
import grpc.aio
import typing
import yandex.cloud.containerregistry.v1.image_pb2
import yandex.cloud.containerregistry.v1.image_service_pb2
import yandex.cloud.operation.operation_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class ImageServiceStub:
    """A set of methods for managing Image resources."""

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    List: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.containerregistry.v1.image_service_pb2.ListImagesRequest,
        yandex.cloud.containerregistry.v1.image_service_pb2.ListImagesResponse,
    ]
    """Retrieves the list of Image resources in the specified registry or repository."""

    Get: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.containerregistry.v1.image_service_pb2.GetImageRequest,
        yandex.cloud.containerregistry.v1.image_pb2.Image,
    ]
    """Returns the specified Image resource.

    To get the list of available Image resources, make a [List] request.
    """

    Delete: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.containerregistry.v1.image_service_pb2.DeleteImageRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Deletes the specified Docker image."""

class ImageServiceAsyncStub:
    """A set of methods for managing Image resources."""

    List: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.containerregistry.v1.image_service_pb2.ListImagesRequest,
        yandex.cloud.containerregistry.v1.image_service_pb2.ListImagesResponse,
    ]
    """Retrieves the list of Image resources in the specified registry or repository."""

    Get: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.containerregistry.v1.image_service_pb2.GetImageRequest,
        yandex.cloud.containerregistry.v1.image_pb2.Image,
    ]
    """Returns the specified Image resource.

    To get the list of available Image resources, make a [List] request.
    """

    Delete: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.containerregistry.v1.image_service_pb2.DeleteImageRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Deletes the specified Docker image."""

class ImageServiceServicer(metaclass=abc.ABCMeta):
    """A set of methods for managing Image resources."""

    @abc.abstractmethod
    def List(
        self,
        request: yandex.cloud.containerregistry.v1.image_service_pb2.ListImagesRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.containerregistry.v1.image_service_pb2.ListImagesResponse, collections.abc.Awaitable[yandex.cloud.containerregistry.v1.image_service_pb2.ListImagesResponse]]:
        """Retrieves the list of Image resources in the specified registry or repository."""

    @abc.abstractmethod
    def Get(
        self,
        request: yandex.cloud.containerregistry.v1.image_service_pb2.GetImageRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.containerregistry.v1.image_pb2.Image, collections.abc.Awaitable[yandex.cloud.containerregistry.v1.image_pb2.Image]]:
        """Returns the specified Image resource.

        To get the list of available Image resources, make a [List] request.
        """

    @abc.abstractmethod
    def Delete(
        self,
        request: yandex.cloud.containerregistry.v1.image_service_pb2.DeleteImageRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Deletes the specified Docker image."""

def add_ImageServiceServicer_to_server(servicer: ImageServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
