# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from yandex.cloud.marketplace.licensemanager.v1 import lock_pb2 as yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__pb2
from yandex.cloud.marketplace.licensemanager.v1 import lock_service_pb2 as yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2


class LockServiceStub(object):
    """A set of methods for managing subscription locks.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/yandex.cloud.marketplace.licensemanager.v1.LockService/Get',
                request_serializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.GetLockRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__pb2.Lock.FromString,
                )
        self.GetByInstanceAndResource = channel.unary_unary(
                '/yandex.cloud.marketplace.licensemanager.v1.LockService/GetByInstanceAndResource',
                request_serializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.GetLockByInstanceAndResourceRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__pb2.Lock.FromString,
                )
        self.List = channel.unary_unary(
                '/yandex.cloud.marketplace.licensemanager.v1.LockService/List',
                request_serializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.ListLocksRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.ListLocksResponse.FromString,
                )
        self.Create = channel.unary_unary(
                '/yandex.cloud.marketplace.licensemanager.v1.LockService/Create',
                request_serializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.CreateLockRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
                )
        self.Ensure = channel.unary_unary(
                '/yandex.cloud.marketplace.licensemanager.v1.LockService/Ensure',
                request_serializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.EnsureLockRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
                )
        self.Delete = channel.unary_unary(
                '/yandex.cloud.marketplace.licensemanager.v1.LockService/Delete',
                request_serializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.DeleteLockRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
                )


class LockServiceServicer(object):
    """A set of methods for managing subscription locks.
    """

    def Get(self, request, context):
        """Returns the specified subscription lock.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetByInstanceAndResource(self, request, context):
        """Returns the subscription lock for specified subscription instance and resource.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def List(self, request, context):
        """Returns subscriptions locks for specified resource and folder.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Create(self, request, context):
        """Locks the specified subscription instance to the resource.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Ensure(self, request, context):
        """Checks if the she specified subscription is already locked to the specified resource.
        If it is not locked, locks the subscription to the resource.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Unlocks the specified subscription lock.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LockServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.GetLockRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__pb2.Lock.SerializeToString,
            ),
            'GetByInstanceAndResource': grpc.unary_unary_rpc_method_handler(
                    servicer.GetByInstanceAndResource,
                    request_deserializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.GetLockByInstanceAndResourceRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__pb2.Lock.SerializeToString,
            ),
            'List': grpc.unary_unary_rpc_method_handler(
                    servicer.List,
                    request_deserializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.ListLocksRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.ListLocksResponse.SerializeToString,
            ),
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.CreateLockRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
            ),
            'Ensure': grpc.unary_unary_rpc_method_handler(
                    servicer.Ensure,
                    request_deserializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.EnsureLockRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.DeleteLockRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'yandex.cloud.marketplace.licensemanager.v1.LockService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LockService(object):
    """A set of methods for managing subscription locks.
    """

    @staticmethod
    def Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.marketplace.licensemanager.v1.LockService/Get',
            yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.GetLockRequest.SerializeToString,
            yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__pb2.Lock.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetByInstanceAndResource(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.marketplace.licensemanager.v1.LockService/GetByInstanceAndResource',
            yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.GetLockByInstanceAndResourceRequest.SerializeToString,
            yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__pb2.Lock.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def List(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.marketplace.licensemanager.v1.LockService/List',
            yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.ListLocksRequest.SerializeToString,
            yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.ListLocksResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.marketplace.licensemanager.v1.LockService/Create',
            yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.CreateLockRequest.SerializeToString,
            yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Ensure(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.marketplace.licensemanager.v1.LockService/Ensure',
            yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.EnsureLockRequest.SerializeToString,
            yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.marketplace.licensemanager.v1.LockService/Delete',
            yandex_dot_cloud_dot_marketplace_dot_licensemanager_dot_v1_dot_lock__service__pb2.DeleteLockRequest.SerializeToString,
            yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
