"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class TextEmbeddingRequest(google.protobuf.message.Message):
    """Request for the service to obtain text embeddings."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MODEL_URI_FIELD_NUMBER: builtins.int
    TEXT_FIELD_NUMBER: builtins.int
    model_uri: builtins.str
    """The [ID of the model](/docs/foundation-models/concepts/embeddings) to be used for obtaining text embeddings."""
    text: builtins.str
    """The input text for which the embedding is requested."""
    def __init__(
        self,
        *,
        model_uri: builtins.str = ...,
        text: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["model_uri", b"model_uri", "text", b"text"]) -> None: ...

global___TextEmbeddingRequest = TextEmbeddingRequest

@typing.final
class TextEmbeddingResponse(google.protobuf.message.Message):
    """Response containing generated text embedding."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EMBEDDING_FIELD_NUMBER: builtins.int
    NUM_TOKENS_FIELD_NUMBER: builtins.int
    MODEL_VERSION_FIELD_NUMBER: builtins.int
    num_tokens: builtins.int
    """The number of tokens in the input text."""
    model_version: builtins.str
    """The model version changes with each new releases."""
    @property
    def embedding(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """A repeated list of double values representing the embedding."""

    def __init__(
        self,
        *,
        embedding: collections.abc.Iterable[builtins.float] | None = ...,
        num_tokens: builtins.int = ...,
        model_version: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["embedding", b"embedding", "model_version", b"model_version", "num_tokens", b"num_tokens"]) -> None: ...

global___TextEmbeddingResponse = TextEmbeddingResponse
