"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import abc
import collections.abc
import grpc
import grpc.aio
import typing
import yandex.cloud.access.access_pb2
import yandex.cloud.operation.operation_pb2
import yandex.cloud.ydb.v1.database_pb2
import yandex.cloud.ydb.v1.database_service_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class DatabaseServiceStub:
    """A set of methods for managing databases."""

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    Get: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.GetDatabaseRequest,
        yandex.cloud.ydb.v1.database_pb2.Database,
    ]
    """Returns the specified database."""

    List: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.ListDatabasesRequest,
        yandex.cloud.ydb.v1.database_service_pb2.ListDatabasesResponse,
    ]
    """Retrieves a list of databases."""

    Create: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.CreateDatabaseRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Creates a new database."""

    Update: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.UpdateDatabaseRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Modifies the specified database."""

    Start: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.StartDatabaseRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Starts the specified database."""

    Stop: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.StopDatabaseRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Stops the specified database."""

    Move: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.MoveDatabaseRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]

    ListAccessBindings: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.ListAccessBindingsRequest,
        yandex.cloud.access.access_pb2.ListAccessBindingsResponse,
    ]

    SetAccessBindings: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.SetAccessBindingsRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]

    UpdateAccessBindings: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.UpdateAccessBindingsRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]

    Delete: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.DeleteDatabaseRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Deletes the specified database."""

    Restore: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.RestoreBackupRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Restores the specified backup"""

    Backup: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.BackupDatabaseRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]

class DatabaseServiceAsyncStub:
    """A set of methods for managing databases."""

    Get: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.GetDatabaseRequest,
        yandex.cloud.ydb.v1.database_pb2.Database,
    ]
    """Returns the specified database."""

    List: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.ListDatabasesRequest,
        yandex.cloud.ydb.v1.database_service_pb2.ListDatabasesResponse,
    ]
    """Retrieves a list of databases."""

    Create: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.CreateDatabaseRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Creates a new database."""

    Update: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.UpdateDatabaseRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Modifies the specified database."""

    Start: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.StartDatabaseRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Starts the specified database."""

    Stop: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.StopDatabaseRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Stops the specified database."""

    Move: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.MoveDatabaseRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]

    ListAccessBindings: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.ListAccessBindingsRequest,
        yandex.cloud.access.access_pb2.ListAccessBindingsResponse,
    ]

    SetAccessBindings: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.SetAccessBindingsRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]

    UpdateAccessBindings: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.UpdateAccessBindingsRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]

    Delete: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.DeleteDatabaseRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Deletes the specified database."""

    Restore: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.RestoreBackupRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Restores the specified backup"""

    Backup: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.ydb.v1.database_service_pb2.BackupDatabaseRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]

class DatabaseServiceServicer(metaclass=abc.ABCMeta):
    """A set of methods for managing databases."""

    @abc.abstractmethod
    def Get(
        self,
        request: yandex.cloud.ydb.v1.database_service_pb2.GetDatabaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.ydb.v1.database_pb2.Database, collections.abc.Awaitable[yandex.cloud.ydb.v1.database_pb2.Database]]:
        """Returns the specified database."""

    @abc.abstractmethod
    def List(
        self,
        request: yandex.cloud.ydb.v1.database_service_pb2.ListDatabasesRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.ydb.v1.database_service_pb2.ListDatabasesResponse, collections.abc.Awaitable[yandex.cloud.ydb.v1.database_service_pb2.ListDatabasesResponse]]:
        """Retrieves a list of databases."""

    @abc.abstractmethod
    def Create(
        self,
        request: yandex.cloud.ydb.v1.database_service_pb2.CreateDatabaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Creates a new database."""

    @abc.abstractmethod
    def Update(
        self,
        request: yandex.cloud.ydb.v1.database_service_pb2.UpdateDatabaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Modifies the specified database."""

    @abc.abstractmethod
    def Start(
        self,
        request: yandex.cloud.ydb.v1.database_service_pb2.StartDatabaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Starts the specified database."""

    @abc.abstractmethod
    def Stop(
        self,
        request: yandex.cloud.ydb.v1.database_service_pb2.StopDatabaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Stops the specified database."""

    @abc.abstractmethod
    def Move(
        self,
        request: yandex.cloud.ydb.v1.database_service_pb2.MoveDatabaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]: ...

    @abc.abstractmethod
    def ListAccessBindings(
        self,
        request: yandex.cloud.access.access_pb2.ListAccessBindingsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.access.access_pb2.ListAccessBindingsResponse, collections.abc.Awaitable[yandex.cloud.access.access_pb2.ListAccessBindingsResponse]]: ...

    @abc.abstractmethod
    def SetAccessBindings(
        self,
        request: yandex.cloud.access.access_pb2.SetAccessBindingsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]: ...

    @abc.abstractmethod
    def UpdateAccessBindings(
        self,
        request: yandex.cloud.access.access_pb2.UpdateAccessBindingsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]: ...

    @abc.abstractmethod
    def Delete(
        self,
        request: yandex.cloud.ydb.v1.database_service_pb2.DeleteDatabaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Deletes the specified database."""

    @abc.abstractmethod
    def Restore(
        self,
        request: yandex.cloud.ydb.v1.database_service_pb2.RestoreBackupRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Restores the specified backup"""

    @abc.abstractmethod
    def Backup(
        self,
        request: yandex.cloud.ydb.v1.database_service_pb2.BackupDatabaseRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]: ...

def add_DatabaseServiceServicer_to_server(servicer: DatabaseServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
