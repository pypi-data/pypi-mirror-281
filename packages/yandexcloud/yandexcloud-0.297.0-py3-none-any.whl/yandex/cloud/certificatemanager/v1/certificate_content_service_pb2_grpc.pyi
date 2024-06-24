"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import abc
import collections.abc
import grpc
import grpc.aio
import typing
import yandex.cloud.certificatemanager.v1.certificate_content_service_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class CertificateContentServiceStub:
    """A set of methods for managing certificate content."""

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    Get: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.certificatemanager.v1.certificate_content_service_pb2.GetCertificateContentRequest,
        yandex.cloud.certificatemanager.v1.certificate_content_service_pb2.GetCertificateContentResponse,
    ]
    """Returns chain and private key of the specified certificate."""

class CertificateContentServiceAsyncStub:
    """A set of methods for managing certificate content."""

    Get: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.certificatemanager.v1.certificate_content_service_pb2.GetCertificateContentRequest,
        yandex.cloud.certificatemanager.v1.certificate_content_service_pb2.GetCertificateContentResponse,
    ]
    """Returns chain and private key of the specified certificate."""

class CertificateContentServiceServicer(metaclass=abc.ABCMeta):
    """A set of methods for managing certificate content."""

    @abc.abstractmethod
    def Get(
        self,
        request: yandex.cloud.certificatemanager.v1.certificate_content_service_pb2.GetCertificateContentRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.certificatemanager.v1.certificate_content_service_pb2.GetCertificateContentResponse, collections.abc.Awaitable[yandex.cloud.certificatemanager.v1.certificate_content_service_pb2.GetCertificateContentResponse]]:
        """Returns chain and private key of the specified certificate."""

def add_CertificateContentServiceServicer_to_server(servicer: CertificateContentServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
