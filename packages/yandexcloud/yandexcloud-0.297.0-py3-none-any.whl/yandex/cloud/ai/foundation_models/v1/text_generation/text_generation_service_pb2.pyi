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
import yandex.cloud.ai.foundation_models.v1.text_common_pb2

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class CompletionRequest(google.protobuf.message.Message):
    """Request for the service to generate text completion."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MODEL_URI_FIELD_NUMBER: builtins.int
    COMPLETION_OPTIONS_FIELD_NUMBER: builtins.int
    MESSAGES_FIELD_NUMBER: builtins.int
    model_uri: builtins.str
    """The [ID of the model](/docs/foundation-models/concepts/yandexgpt/models) to be used for completion generation."""
    @property
    def completion_options(self) -> yandex.cloud.ai.foundation_models.v1.text_common_pb2.CompletionOptions:
        """Configuration options for completion generation."""

    @property
    def messages(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.ai.foundation_models.v1.text_common_pb2.Message]:
        """A list of messages representing the context for the completion model."""

    def __init__(
        self,
        *,
        model_uri: builtins.str = ...,
        completion_options: yandex.cloud.ai.foundation_models.v1.text_common_pb2.CompletionOptions | None = ...,
        messages: collections.abc.Iterable[yandex.cloud.ai.foundation_models.v1.text_common_pb2.Message] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["completion_options", b"completion_options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["completion_options", b"completion_options", "messages", b"messages", "model_uri", b"model_uri"]) -> None: ...

global___CompletionRequest = CompletionRequest

@typing.final
class CompletionResponse(google.protobuf.message.Message):
    """Response containing generated text completions."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ALTERNATIVES_FIELD_NUMBER: builtins.int
    USAGE_FIELD_NUMBER: builtins.int
    MODEL_VERSION_FIELD_NUMBER: builtins.int
    model_version: builtins.str
    """The model version changes with each new releases."""
    @property
    def alternatives(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.ai.foundation_models.v1.text_common_pb2.Alternative]:
        """A list of generated completion alternatives."""

    @property
    def usage(self) -> yandex.cloud.ai.foundation_models.v1.text_common_pb2.ContentUsage:
        """A set of statistics describing the number of content tokens used by the completion model."""

    def __init__(
        self,
        *,
        alternatives: collections.abc.Iterable[yandex.cloud.ai.foundation_models.v1.text_common_pb2.Alternative] | None = ...,
        usage: yandex.cloud.ai.foundation_models.v1.text_common_pb2.ContentUsage | None = ...,
        model_version: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["usage", b"usage"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["alternatives", b"alternatives", "model_version", b"model_version", "usage", b"usage"]) -> None: ...

global___CompletionResponse = CompletionResponse

@typing.final
class TokenizeRequest(google.protobuf.message.Message):
    """Request for the service to tokenize input text."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MODEL_URI_FIELD_NUMBER: builtins.int
    TEXT_FIELD_NUMBER: builtins.int
    model_uri: builtins.str
    """The identifier of the model to be used for tokenization."""
    text: builtins.str
    """Text to be tokenized."""
    def __init__(
        self,
        *,
        model_uri: builtins.str = ...,
        text: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["model_uri", b"model_uri", "text", b"text"]) -> None: ...

global___TokenizeRequest = TokenizeRequest

@typing.final
class TokenizeResponse(google.protobuf.message.Message):
    """Response containing tokenized content from request."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TOKENS_FIELD_NUMBER: builtins.int
    MODEL_VERSION_FIELD_NUMBER: builtins.int
    model_version: builtins.str
    """Model version (changes with model releases)."""
    @property
    def tokens(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.ai.foundation_models.v1.text_common_pb2.Token]:
        """A list of tokens obtained from tokenization."""

    def __init__(
        self,
        *,
        tokens: collections.abc.Iterable[yandex.cloud.ai.foundation_models.v1.text_common_pb2.Token] | None = ...,
        model_version: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["model_version", b"model_version", "tokens", b"tokens"]) -> None: ...

global___TokenizeResponse = TokenizeResponse
