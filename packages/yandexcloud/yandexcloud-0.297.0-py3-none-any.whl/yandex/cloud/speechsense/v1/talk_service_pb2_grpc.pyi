"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import abc
import collections.abc
import grpc
import grpc.aio
import typing
import yandex.cloud.speechsense.v1.talk_service_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class TalkServiceStub:
    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    UploadAsStream: grpc.StreamUnaryMultiCallable[
        yandex.cloud.speechsense.v1.talk_service_pb2.StreamTalkRequest,
        yandex.cloud.speechsense.v1.talk_service_pb2.UploadTalkResponse,
    ]
    """rpc for streaming talk documents. First message should contain Talk related metadata,
    second - audio metadata, others should contain audio bytes in chunks
    """

    Upload: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.speechsense.v1.talk_service_pb2.UploadTalkRequest,
        yandex.cloud.speechsense.v1.talk_service_pb2.UploadTalkResponse,
    ]
    """rpc for uploading talk document as single message"""

    UploadText: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.speechsense.v1.talk_service_pb2.UploadTextRequest,
        yandex.cloud.speechsense.v1.talk_service_pb2.UploadTextResponse,
    ]
    """rpc for uploading text talk document"""

    Search: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.speechsense.v1.talk_service_pb2.SearchTalkRequest,
        yandex.cloud.speechsense.v1.talk_service_pb2.SearchTalkResponse,
    ]
    """rpc for searching talks. will return ids only"""

    Get: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.speechsense.v1.talk_service_pb2.GetTalkRequest,
        yandex.cloud.speechsense.v1.talk_service_pb2.GetTalkResponse,
    ]
    """rpc for bulk get"""

class TalkServiceAsyncStub:
    UploadAsStream: grpc.aio.StreamUnaryMultiCallable[
        yandex.cloud.speechsense.v1.talk_service_pb2.StreamTalkRequest,
        yandex.cloud.speechsense.v1.talk_service_pb2.UploadTalkResponse,
    ]
    """rpc for streaming talk documents. First message should contain Talk related metadata,
    second - audio metadata, others should contain audio bytes in chunks
    """

    Upload: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.speechsense.v1.talk_service_pb2.UploadTalkRequest,
        yandex.cloud.speechsense.v1.talk_service_pb2.UploadTalkResponse,
    ]
    """rpc for uploading talk document as single message"""

    UploadText: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.speechsense.v1.talk_service_pb2.UploadTextRequest,
        yandex.cloud.speechsense.v1.talk_service_pb2.UploadTextResponse,
    ]
    """rpc for uploading text talk document"""

    Search: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.speechsense.v1.talk_service_pb2.SearchTalkRequest,
        yandex.cloud.speechsense.v1.talk_service_pb2.SearchTalkResponse,
    ]
    """rpc for searching talks. will return ids only"""

    Get: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.speechsense.v1.talk_service_pb2.GetTalkRequest,
        yandex.cloud.speechsense.v1.talk_service_pb2.GetTalkResponse,
    ]
    """rpc for bulk get"""

class TalkServiceServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def UploadAsStream(
        self,
        request_iterator: _MaybeAsyncIterator[yandex.cloud.speechsense.v1.talk_service_pb2.StreamTalkRequest],
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.speechsense.v1.talk_service_pb2.UploadTalkResponse, collections.abc.Awaitable[yandex.cloud.speechsense.v1.talk_service_pb2.UploadTalkResponse]]:
        """rpc for streaming talk documents. First message should contain Talk related metadata,
        second - audio metadata, others should contain audio bytes in chunks
        """

    @abc.abstractmethod
    def Upload(
        self,
        request: yandex.cloud.speechsense.v1.talk_service_pb2.UploadTalkRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.speechsense.v1.talk_service_pb2.UploadTalkResponse, collections.abc.Awaitable[yandex.cloud.speechsense.v1.talk_service_pb2.UploadTalkResponse]]:
        """rpc for uploading talk document as single message"""

    @abc.abstractmethod
    def UploadText(
        self,
        request: yandex.cloud.speechsense.v1.talk_service_pb2.UploadTextRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.speechsense.v1.talk_service_pb2.UploadTextResponse, collections.abc.Awaitable[yandex.cloud.speechsense.v1.talk_service_pb2.UploadTextResponse]]:
        """rpc for uploading text talk document"""

    @abc.abstractmethod
    def Search(
        self,
        request: yandex.cloud.speechsense.v1.talk_service_pb2.SearchTalkRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.speechsense.v1.talk_service_pb2.SearchTalkResponse, collections.abc.Awaitable[yandex.cloud.speechsense.v1.talk_service_pb2.SearchTalkResponse]]:
        """rpc for searching talks. will return ids only"""

    @abc.abstractmethod
    def Get(
        self,
        request: yandex.cloud.speechsense.v1.talk_service_pb2.GetTalkRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.speechsense.v1.talk_service_pb2.GetTalkResponse, collections.abc.Awaitable[yandex.cloud.speechsense.v1.talk_service_pb2.GetTalkResponse]]:
        """rpc for bulk get"""

def add_TalkServiceServicer_to_server(servicer: TalkServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
