"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import abc
import collections.abc
import grpc
import grpc.aio
import typing
import yandex.cloud.ai.vision.v1.vision_service_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class VisionServiceStub:
    """A set of methods for the Vision service."""

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    BatchAnalyze: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.ai.vision.v1.vision_service_pb2.BatchAnalyzeRequest,
        yandex.cloud.ai.vision.v1.vision_service_pb2.BatchAnalyzeResponse,
    ]
    """Analyzes a batch of images and returns results with annotations."""

class VisionServiceAsyncStub:
    """A set of methods for the Vision service."""

    BatchAnalyze: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.ai.vision.v1.vision_service_pb2.BatchAnalyzeRequest,
        yandex.cloud.ai.vision.v1.vision_service_pb2.BatchAnalyzeResponse,
    ]
    """Analyzes a batch of images and returns results with annotations."""

class VisionServiceServicer(metaclass=abc.ABCMeta):
    """A set of methods for the Vision service."""

    @abc.abstractmethod
    def BatchAnalyze(
        self,
        request: yandex.cloud.ai.vision.v1.vision_service_pb2.BatchAnalyzeRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.ai.vision.v1.vision_service_pb2.BatchAnalyzeResponse, collections.abc.Awaitable[yandex.cloud.ai.vision.v1.vision_service_pb2.BatchAnalyzeResponse]]:
        """Analyzes a batch of images and returns results with annotations."""

def add_VisionServiceServicer_to_server(servicer: VisionServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
