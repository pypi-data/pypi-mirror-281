"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import abc
import collections.abc
import grpc
import grpc.aio
import typing
import yandex.cloud.mdb.postgresql.v1.perf_diag_service_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class PerformanceDiagnosticsServiceStub:
    """A set of methods for PostgreSQL performance diagnostics."""

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    ListRawSessionStates: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.mdb.postgresql.v1.perf_diag_service_pb2.ListRawSessionStatesRequest,
        yandex.cloud.mdb.postgresql.v1.perf_diag_service_pb2.ListRawSessionStatesResponse,
    ]
    """Retrieves raw statistics on sessions. Corresponds to the [pg_stat_activity view](https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW)."""

    ListRawStatements: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.mdb.postgresql.v1.perf_diag_service_pb2.ListRawStatementsRequest,
        yandex.cloud.mdb.postgresql.v1.perf_diag_service_pb2.ListRawStatementsResponse,
    ]
    """Retrieves statistics on planning and execution of SQL statements (queries)."""

class PerformanceDiagnosticsServiceAsyncStub:
    """A set of methods for PostgreSQL performance diagnostics."""

    ListRawSessionStates: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.mdb.postgresql.v1.perf_diag_service_pb2.ListRawSessionStatesRequest,
        yandex.cloud.mdb.postgresql.v1.perf_diag_service_pb2.ListRawSessionStatesResponse,
    ]
    """Retrieves raw statistics on sessions. Corresponds to the [pg_stat_activity view](https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW)."""

    ListRawStatements: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.mdb.postgresql.v1.perf_diag_service_pb2.ListRawStatementsRequest,
        yandex.cloud.mdb.postgresql.v1.perf_diag_service_pb2.ListRawStatementsResponse,
    ]
    """Retrieves statistics on planning and execution of SQL statements (queries)."""

class PerformanceDiagnosticsServiceServicer(metaclass=abc.ABCMeta):
    """A set of methods for PostgreSQL performance diagnostics."""

    @abc.abstractmethod
    def ListRawSessionStates(
        self,
        request: yandex.cloud.mdb.postgresql.v1.perf_diag_service_pb2.ListRawSessionStatesRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.mdb.postgresql.v1.perf_diag_service_pb2.ListRawSessionStatesResponse, collections.abc.Awaitable[yandex.cloud.mdb.postgresql.v1.perf_diag_service_pb2.ListRawSessionStatesResponse]]:
        """Retrieves raw statistics on sessions. Corresponds to the [pg_stat_activity view](https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW)."""

    @abc.abstractmethod
    def ListRawStatements(
        self,
        request: yandex.cloud.mdb.postgresql.v1.perf_diag_service_pb2.ListRawStatementsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.mdb.postgresql.v1.perf_diag_service_pb2.ListRawStatementsResponse, collections.abc.Awaitable[yandex.cloud.mdb.postgresql.v1.perf_diag_service_pb2.ListRawStatementsResponse]]:
        """Retrieves statistics on planning and execution of SQL statements (queries)."""

def add_PerformanceDiagnosticsServiceServicer_to_server(servicer: PerformanceDiagnosticsServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
