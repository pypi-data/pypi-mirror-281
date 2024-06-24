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
import yandex.cloud.serverless.functions.v1.function_pb2
import yandex.cloud.serverless.functions.v1.function_service_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class FunctionServiceStub:
    """A set of methods for managing serverless functions."""

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    Get: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.GetFunctionRequest,
        yandex.cloud.serverless.functions.v1.function_pb2.Function,
    ]
    """Returns the specified function.

    To get the list of all available functions, make a [List] request.
    """

    List: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionsRequest,
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionsResponse,
    ]
    """Retrieves the list of functions in the specified folder."""

    Create: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.CreateFunctionRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Creates a function in the specified folder."""

    Update: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.UpdateFunctionRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Updates the specified function."""

    Delete: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.DeleteFunctionRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Deletes the specified function."""

    GetVersion: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.GetFunctionVersionRequest,
        yandex.cloud.serverless.functions.v1.function_pb2.Version,
    ]
    """Returns the specified version of a function.

    To get the list of available version, make a [ListVersions] request.
    """

    GetVersionByTag: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.GetFunctionVersionByTagRequest,
        yandex.cloud.serverless.functions.v1.function_pb2.Version,
    ]
    """Returns all versions with the specified tag.

    To get the list of all available versions, make a [ListVersions] request.
    """

    ListVersions: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionsVersionsRequest,
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionsVersionsResponse,
    ]
    """Retrieves the list of versions for the specified function, or of all function versions
    in the specified folder.
    """

    DeleteVersion: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.DeleteFunctionVersionRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Deletes the specified version of a function.

    NOTE: old untagged function versions are deleted automatically.
    """

    SetTag: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.SetFunctionTagRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Set a tag for the specified version of a function."""

    RemoveTag: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.RemoveFunctionTagRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Remove a tag from the specified version of a function."""

    ListTagHistory: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionTagHistoryRequest,
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionTagHistoryResponse,
    ]
    """Returns the log of tags assigned to versions of the specified function."""

    CreateVersion: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.CreateFunctionVersionRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Creates a version for the specified function."""

    ListRuntimes: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListRuntimesRequest,
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListRuntimesResponse,
    ]
    """Lists available runtime environments for the specified function."""

    ListOperations: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionOperationsRequest,
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionOperationsResponse,
    ]
    """Lists operations for the specified function."""

    ListAccessBindings: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.ListAccessBindingsRequest,
        yandex.cloud.access.access_pb2.ListAccessBindingsResponse,
    ]
    """Lists existing access bindings for the specified function."""

    SetAccessBindings: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.SetAccessBindingsRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Sets access bindings for the function."""

    UpdateAccessBindings: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.UpdateAccessBindingsRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Updates access bindings for the specified function."""

    ListScalingPolicies: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListScalingPoliciesRequest,
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListScalingPoliciesResponse,
    ]
    """Lists existing scaling policies for specified function"""

    SetScalingPolicy: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.SetScalingPolicyRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Set scaling policy for specified function and tag"""

    RemoveScalingPolicy: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.RemoveScalingPolicyRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Remove scaling policy for specified function and tag"""

class FunctionServiceAsyncStub:
    """A set of methods for managing serverless functions."""

    Get: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.GetFunctionRequest,
        yandex.cloud.serverless.functions.v1.function_pb2.Function,
    ]
    """Returns the specified function.

    To get the list of all available functions, make a [List] request.
    """

    List: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionsRequest,
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionsResponse,
    ]
    """Retrieves the list of functions in the specified folder."""

    Create: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.CreateFunctionRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Creates a function in the specified folder."""

    Update: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.UpdateFunctionRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Updates the specified function."""

    Delete: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.DeleteFunctionRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Deletes the specified function."""

    GetVersion: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.GetFunctionVersionRequest,
        yandex.cloud.serverless.functions.v1.function_pb2.Version,
    ]
    """Returns the specified version of a function.

    To get the list of available version, make a [ListVersions] request.
    """

    GetVersionByTag: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.GetFunctionVersionByTagRequest,
        yandex.cloud.serverless.functions.v1.function_pb2.Version,
    ]
    """Returns all versions with the specified tag.

    To get the list of all available versions, make a [ListVersions] request.
    """

    ListVersions: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionsVersionsRequest,
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionsVersionsResponse,
    ]
    """Retrieves the list of versions for the specified function, or of all function versions
    in the specified folder.
    """

    DeleteVersion: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.DeleteFunctionVersionRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Deletes the specified version of a function.

    NOTE: old untagged function versions are deleted automatically.
    """

    SetTag: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.SetFunctionTagRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Set a tag for the specified version of a function."""

    RemoveTag: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.RemoveFunctionTagRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Remove a tag from the specified version of a function."""

    ListTagHistory: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionTagHistoryRequest,
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionTagHistoryResponse,
    ]
    """Returns the log of tags assigned to versions of the specified function."""

    CreateVersion: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.CreateFunctionVersionRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Creates a version for the specified function."""

    ListRuntimes: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListRuntimesRequest,
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListRuntimesResponse,
    ]
    """Lists available runtime environments for the specified function."""

    ListOperations: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionOperationsRequest,
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionOperationsResponse,
    ]
    """Lists operations for the specified function."""

    ListAccessBindings: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.ListAccessBindingsRequest,
        yandex.cloud.access.access_pb2.ListAccessBindingsResponse,
    ]
    """Lists existing access bindings for the specified function."""

    SetAccessBindings: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.SetAccessBindingsRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Sets access bindings for the function."""

    UpdateAccessBindings: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.access.access_pb2.UpdateAccessBindingsRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Updates access bindings for the specified function."""

    ListScalingPolicies: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListScalingPoliciesRequest,
        yandex.cloud.serverless.functions.v1.function_service_pb2.ListScalingPoliciesResponse,
    ]
    """Lists existing scaling policies for specified function"""

    SetScalingPolicy: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.SetScalingPolicyRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Set scaling policy for specified function and tag"""

    RemoveScalingPolicy: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.serverless.functions.v1.function_service_pb2.RemoveScalingPolicyRequest,
        yandex.cloud.operation.operation_pb2.Operation,
    ]
    """Remove scaling policy for specified function and tag"""

class FunctionServiceServicer(metaclass=abc.ABCMeta):
    """A set of methods for managing serverless functions."""

    @abc.abstractmethod
    def Get(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.GetFunctionRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.serverless.functions.v1.function_pb2.Function, collections.abc.Awaitable[yandex.cloud.serverless.functions.v1.function_pb2.Function]]:
        """Returns the specified function.

        To get the list of all available functions, make a [List] request.
        """

    @abc.abstractmethod
    def List(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionsResponse, collections.abc.Awaitable[yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionsResponse]]:
        """Retrieves the list of functions in the specified folder."""

    @abc.abstractmethod
    def Create(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.CreateFunctionRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Creates a function in the specified folder."""

    @abc.abstractmethod
    def Update(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.UpdateFunctionRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Updates the specified function."""

    @abc.abstractmethod
    def Delete(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.DeleteFunctionRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Deletes the specified function."""

    @abc.abstractmethod
    def GetVersion(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.GetFunctionVersionRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.serverless.functions.v1.function_pb2.Version, collections.abc.Awaitable[yandex.cloud.serverless.functions.v1.function_pb2.Version]]:
        """Returns the specified version of a function.

        To get the list of available version, make a [ListVersions] request.
        """

    @abc.abstractmethod
    def GetVersionByTag(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.GetFunctionVersionByTagRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.serverless.functions.v1.function_pb2.Version, collections.abc.Awaitable[yandex.cloud.serverless.functions.v1.function_pb2.Version]]:
        """Returns all versions with the specified tag.

        To get the list of all available versions, make a [ListVersions] request.
        """

    @abc.abstractmethod
    def ListVersions(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionsVersionsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionsVersionsResponse, collections.abc.Awaitable[yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionsVersionsResponse]]:
        """Retrieves the list of versions for the specified function, or of all function versions
        in the specified folder.
        """

    @abc.abstractmethod
    def DeleteVersion(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.DeleteFunctionVersionRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Deletes the specified version of a function.

        NOTE: old untagged function versions are deleted automatically.
        """

    @abc.abstractmethod
    def SetTag(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.SetFunctionTagRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Set a tag for the specified version of a function."""

    @abc.abstractmethod
    def RemoveTag(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.RemoveFunctionTagRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Remove a tag from the specified version of a function."""

    @abc.abstractmethod
    def ListTagHistory(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionTagHistoryRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionTagHistoryResponse, collections.abc.Awaitable[yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionTagHistoryResponse]]:
        """Returns the log of tags assigned to versions of the specified function."""

    @abc.abstractmethod
    def CreateVersion(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.CreateFunctionVersionRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Creates a version for the specified function."""

    @abc.abstractmethod
    def ListRuntimes(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.ListRuntimesRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.serverless.functions.v1.function_service_pb2.ListRuntimesResponse, collections.abc.Awaitable[yandex.cloud.serverless.functions.v1.function_service_pb2.ListRuntimesResponse]]:
        """Lists available runtime environments for the specified function."""

    @abc.abstractmethod
    def ListOperations(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionOperationsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionOperationsResponse, collections.abc.Awaitable[yandex.cloud.serverless.functions.v1.function_service_pb2.ListFunctionOperationsResponse]]:
        """Lists operations for the specified function."""

    @abc.abstractmethod
    def ListAccessBindings(
        self,
        request: yandex.cloud.access.access_pb2.ListAccessBindingsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.access.access_pb2.ListAccessBindingsResponse, collections.abc.Awaitable[yandex.cloud.access.access_pb2.ListAccessBindingsResponse]]:
        """Lists existing access bindings for the specified function."""

    @abc.abstractmethod
    def SetAccessBindings(
        self,
        request: yandex.cloud.access.access_pb2.SetAccessBindingsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Sets access bindings for the function."""

    @abc.abstractmethod
    def UpdateAccessBindings(
        self,
        request: yandex.cloud.access.access_pb2.UpdateAccessBindingsRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Updates access bindings for the specified function."""

    @abc.abstractmethod
    def ListScalingPolicies(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.ListScalingPoliciesRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.serverless.functions.v1.function_service_pb2.ListScalingPoliciesResponse, collections.abc.Awaitable[yandex.cloud.serverless.functions.v1.function_service_pb2.ListScalingPoliciesResponse]]:
        """Lists existing scaling policies for specified function"""

    @abc.abstractmethod
    def SetScalingPolicy(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.SetScalingPolicyRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Set scaling policy for specified function and tag"""

    @abc.abstractmethod
    def RemoveScalingPolicy(
        self,
        request: yandex.cloud.serverless.functions.v1.function_service_pb2.RemoveScalingPolicyRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.operation.operation_pb2.Operation, collections.abc.Awaitable[yandex.cloud.operation.operation_pb2.Operation]]:
        """Remove scaling policy for specified function and tag"""

def add_FunctionServiceServicer_to_server(servicer: FunctionServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
