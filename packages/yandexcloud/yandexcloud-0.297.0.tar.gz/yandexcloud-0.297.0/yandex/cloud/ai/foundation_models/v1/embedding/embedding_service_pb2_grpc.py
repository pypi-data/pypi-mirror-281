# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from yandex.cloud.ai.foundation_models.v1.embedding import embedding_service_pb2 as yandex_dot_cloud_dot_ai_dot_foundation__models_dot_v1_dot_embedding_dot_embedding__service__pb2


class EmbeddingsServiceStub(object):
    """Service for obtaining embeddings from input data.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.TextEmbedding = channel.unary_unary(
                '/yandex.cloud.ai.foundation_models.v1.EmbeddingsService/TextEmbedding',
                request_serializer=yandex_dot_cloud_dot_ai_dot_foundation__models_dot_v1_dot_embedding_dot_embedding__service__pb2.TextEmbeddingRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_ai_dot_foundation__models_dot_v1_dot_embedding_dot_embedding__service__pb2.TextEmbeddingResponse.FromString,
                )


class EmbeddingsServiceServicer(object):
    """Service for obtaining embeddings from input data.
    """

    def TextEmbedding(self, request, context):
        """A method for obtaining embeddings from text data.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_EmbeddingsServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'TextEmbedding': grpc.unary_unary_rpc_method_handler(
                    servicer.TextEmbedding,
                    request_deserializer=yandex_dot_cloud_dot_ai_dot_foundation__models_dot_v1_dot_embedding_dot_embedding__service__pb2.TextEmbeddingRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_ai_dot_foundation__models_dot_v1_dot_embedding_dot_embedding__service__pb2.TextEmbeddingResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'yandex.cloud.ai.foundation_models.v1.EmbeddingsService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class EmbeddingsService(object):
    """Service for obtaining embeddings from input data.
    """

    @staticmethod
    def TextEmbedding(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.ai.foundation_models.v1.EmbeddingsService/TextEmbedding',
            yandex_dot_cloud_dot_ai_dot_foundation__models_dot_v1_dot_embedding_dot_embedding__service__pb2.TextEmbeddingRequest.SerializeToString,
            yandex_dot_cloud_dot_ai_dot_foundation__models_dot_v1_dot_embedding_dot_embedding__service__pb2.TextEmbeddingResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
