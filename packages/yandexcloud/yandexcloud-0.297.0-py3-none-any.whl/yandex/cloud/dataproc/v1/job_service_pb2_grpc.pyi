"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import abc
import collections.abc
import grpc
import grpc.aio
import typing
import yandex.cloud.dataproc.v1.job_pb2
import yandex.cloud.dataproc.v1.job_service_pb2
import yandex.cloud.operation.operation_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class JobServiceStub:
    """A set of methods for managing Data Proc jobs."""

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    List: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.dataproc.v1.job_service_pb2.ListJobsRequest,
        yandex.cloud.dataproc.v1.job_service_pb2.ListJobsResponse,
    ]
    """Retrieves a list of jobs for a cluster."""

    Create: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.dataproc.v1.job_service_pb2.CreateJobRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Creates a job for a cluster."""

    Get: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.dataproc.v1.job_service_pb2.GetJobRequest,
        yandex.cloud.dataproc.v1.job_pb2.Job,
    ]
    """Returns the specified job."""

    ListLog: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.dataproc.v1.job_service_pb2.ListJobLogRequest,
        yandex.cloud.dataproc.v1.job_service_pb2.ListJobLogResponse,
    ]
    """Returns a log for specified job."""

    Cancel: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.dataproc.v1.job_service_pb2.CancelJobRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Cancels the specified Dataproc job."""

class JobServiceAsyncStub:
    """A set of methods for managing Data Proc jobs."""

    List: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.dataproc.v1.job_service_pb2.ListJobsRequest,
        yandex.cloud.dataproc.v1.job_service_pb2.ListJobsResponse,
    ]
    """Retrieves a list of jobs for a cluster."""

    Create: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.dataproc.v1.job_service_pb2.CreateJobRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Creates a job for a cluster."""

    Get: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.dataproc.v1.job_service_pb2.GetJobRequest,
        yandex.cloud.dataproc.v1.job_pb2.Job,
    ]
    """Returns the specified job."""

    ListLog: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.dataproc.v1.job_service_pb2.ListJobLogRequest,
        yandex.cloud.dataproc.v1.job_service_pb2.ListJobLogResponse,
    ]
    """Returns a log for specified job."""

    Cancel: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.dataproc.v1.job_service_pb2.CancelJobRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Cancels the specified Dataproc job."""

class JobServiceServicer(metaclass=abc.ABCMeta):
    """A set of methods for managing Data Proc jobs."""

    @abc.abstractmethod
    def List(
        self,
        request: yandex.cloud.dataproc.v1.job_service_pb2.ListJobsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.dataproc.v1.job_service_pb2.ListJobsResponse, collections.abc.Awaitable[yandex.cloud.dataproc.v1.job_service_pb2.ListJobsResponse]]:
        """Retrieves a list of jobs for a cluster."""

    @abc.abstractmethod
    def Create(
        self,
        request: yandex.cloud.dataproc.v1.job_service_pb2.CreateJobRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Creates a job for a cluster."""

    @abc.abstractmethod
    def Get(
        self,
        request: yandex.cloud.dataproc.v1.job_service_pb2.GetJobRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.dataproc.v1.job_pb2.Job, collections.abc.Awaitable[yandex.cloud.dataproc.v1.job_pb2.Job]]:
        """Returns the specified job."""

    @abc.abstractmethod
    def ListLog(
        self,
        request: yandex.cloud.dataproc.v1.job_service_pb2.ListJobLogRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.dataproc.v1.job_service_pb2.ListJobLogResponse, collections.abc.Awaitable[yandex.cloud.dataproc.v1.job_service_pb2.ListJobLogResponse]]:
        """Returns a log for specified job."""

    @abc.abstractmethod
    def Cancel(
        self,
        request: yandex.cloud.dataproc.v1.job_service_pb2.CancelJobRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Cancels the specified Dataproc job."""

def add_JobServiceServicer_to_server(servicer: JobServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
