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
import yandex.cloud.video.v1.thumbnail_service_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class ThumbnailServiceStub:
    """Thumbnail management service."""

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    List: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.video.v1.thumbnail_service_pb2.ListThumbnailRequest,
        yandex.cloud.video.v1.thumbnail_service_pb2.ListThumbnailResponse,
    ]
    """List thumbnails for channel."""

    Create: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.video.v1.thumbnail_service_pb2.CreateThumbnailRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Create thumbnail."""

    BatchGenerateDownloadURLs: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.video.v1.thumbnail_service_pb2.BatchGenerateDownloadURLsRequest,
        yandex.cloud.video.v1.thumbnail_service_pb2.BatchGenerateDownloadURLsResponse,
    ]
    """Generate urls for download images."""

    GenerateUploadURL: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.video.v1.thumbnail_service_pb2.GenerateThumbnailUploadURLRequest,
        yandex.cloud.video.v1.thumbnail_service_pb2.GenerateThumbnailUploadURLResponse,
    ]
    """Generate url for upload image."""

class ThumbnailServiceAsyncStub:
    """Thumbnail management service."""

    List: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.video.v1.thumbnail_service_pb2.ListThumbnailRequest,
        yandex.cloud.video.v1.thumbnail_service_pb2.ListThumbnailResponse,
    ]
    """List thumbnails for channel."""

    Create: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.video.v1.thumbnail_service_pb2.CreateThumbnailRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Create thumbnail."""

    BatchGenerateDownloadURLs: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.video.v1.thumbnail_service_pb2.BatchGenerateDownloadURLsRequest,
        yandex.cloud.video.v1.thumbnail_service_pb2.BatchGenerateDownloadURLsResponse,
    ]
    """Generate urls for download images."""

    GenerateUploadURL: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.video.v1.thumbnail_service_pb2.GenerateThumbnailUploadURLRequest,
        yandex.cloud.video.v1.thumbnail_service_pb2.GenerateThumbnailUploadURLResponse,
    ]
    """Generate url for upload image."""

class ThumbnailServiceServicer(metaclass=abc.ABCMeta):
    """Thumbnail management service."""

    @abc.abstractmethod
    def List(
        self,
        request: yandex.cloud.video.v1.thumbnail_service_pb2.ListThumbnailRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.video.v1.thumbnail_service_pb2.ListThumbnailResponse, collections.abc.Awaitable[yandex.cloud.video.v1.thumbnail_service_pb2.ListThumbnailResponse]]:
        """List thumbnails for channel."""

    @abc.abstractmethod
    def Create(
        self,
        request: yandex.cloud.video.v1.thumbnail_service_pb2.CreateThumbnailRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Create thumbnail."""

    @abc.abstractmethod
    def BatchGenerateDownloadURLs(
        self,
        request: yandex.cloud.video.v1.thumbnail_service_pb2.BatchGenerateDownloadURLsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.video.v1.thumbnail_service_pb2.BatchGenerateDownloadURLsResponse, collections.abc.Awaitable[yandex.cloud.video.v1.thumbnail_service_pb2.BatchGenerateDownloadURLsResponse]]:
        """Generate urls for download images."""

    @abc.abstractmethod
    def GenerateUploadURL(
        self,
        request: yandex.cloud.video.v1.thumbnail_service_pb2.GenerateThumbnailUploadURLRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.video.v1.thumbnail_service_pb2.GenerateThumbnailUploadURLResponse, collections.abc.Awaitable[yandex.cloud.video.v1.thumbnail_service_pb2.GenerateThumbnailUploadURLResponse]]:
        """Generate url for upload image."""

def add_ThumbnailServiceServicer_to_server(servicer: ThumbnailServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
