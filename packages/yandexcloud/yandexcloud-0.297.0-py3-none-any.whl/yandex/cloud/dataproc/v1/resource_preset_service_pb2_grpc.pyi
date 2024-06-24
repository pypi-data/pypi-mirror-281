"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import abc
import collections.abc
import grpc
import grpc.aio
import typing
import yandex.cloud.dataproc.v1.resource_preset_pb2
import yandex.cloud.dataproc.v1.resource_preset_service_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class ResourcePresetServiceStub:
    """A set of methods for managing ResourcePreset resources."""

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    Get: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.dataproc.v1.resource_preset_service_pb2.GetResourcePresetRequest,
        yandex.cloud.dataproc.v1.resource_preset_pb2.ResourcePreset,
    ]
    """Returns the specified ResourcePreset resource.

    To get the list of available ResourcePreset resources, make a [List] request.
    """

    List: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.dataproc.v1.resource_preset_service_pb2.ListResourcePresetsRequest,
        yandex.cloud.dataproc.v1.resource_preset_service_pb2.ListResourcePresetsResponse,
    ]
    """Retrieves the list of available ResourcePreset resources."""

class ResourcePresetServiceAsyncStub:
    """A set of methods for managing ResourcePreset resources."""

    Get: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.dataproc.v1.resource_preset_service_pb2.GetResourcePresetRequest,
        yandex.cloud.dataproc.v1.resource_preset_pb2.ResourcePreset,
    ]
    """Returns the specified ResourcePreset resource.

    To get the list of available ResourcePreset resources, make a [List] request.
    """

    List: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.dataproc.v1.resource_preset_service_pb2.ListResourcePresetsRequest,
        yandex.cloud.dataproc.v1.resource_preset_service_pb2.ListResourcePresetsResponse,
    ]
    """Retrieves the list of available ResourcePreset resources."""

class ResourcePresetServiceServicer(metaclass=abc.ABCMeta):
    """A set of methods for managing ResourcePreset resources."""

    @abc.abstractmethod
    def Get(
        self,
        request: yandex.cloud.dataproc.v1.resource_preset_service_pb2.GetResourcePresetRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.dataproc.v1.resource_preset_pb2.ResourcePreset, collections.abc.Awaitable[yandex.cloud.dataproc.v1.resource_preset_pb2.ResourcePreset]]:
        """Returns the specified ResourcePreset resource.

        To get the list of available ResourcePreset resources, make a [List] request.
        """

    @abc.abstractmethod
    def List(
        self,
        request: yandex.cloud.dataproc.v1.resource_preset_service_pb2.ListResourcePresetsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.dataproc.v1.resource_preset_service_pb2.ListResourcePresetsResponse, collections.abc.Awaitable[yandex.cloud.dataproc.v1.resource_preset_service_pb2.ListResourcePresetsResponse]]:
        """Retrieves the list of available ResourcePreset resources."""

def add_ResourcePresetServiceServicer_to_server(servicer: ResourcePresetServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
