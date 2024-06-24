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
import yandex.cloud.ai.foundation_models.v1.text_classification.text_classification_pb2

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class TextClassificationRequest(google.protobuf.message.Message):
    """Request for the service to classify text."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MODEL_URI_FIELD_NUMBER: builtins.int
    TEXT_FIELD_NUMBER: builtins.int
    model_uri: builtins.str
    """The identifier of the classification model."""
    text: builtins.str
    """Text for classification."""
    def __init__(
        self,
        *,
        model_uri: builtins.str = ...,
        text: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["model_uri", b"model_uri", "text", b"text"]) -> None: ...

global___TextClassificationRequest = TextClassificationRequest

@typing.final
class TextClassificationResponse(google.protobuf.message.Message):
    """Response containing classifier predictions."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PREDICTIONS_FIELD_NUMBER: builtins.int
    MODEL_VERSION_FIELD_NUMBER: builtins.int
    model_version: builtins.str
    """Model version (changes with model releases)."""
    @property
    def predictions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.ai.foundation_models.v1.text_classification.text_classification_pb2.ClassificationLabel]:
        """Result of classification - a list of label-confidence pairs."""

    def __init__(
        self,
        *,
        predictions: collections.abc.Iterable[yandex.cloud.ai.foundation_models.v1.text_classification.text_classification_pb2.ClassificationLabel] | None = ...,
        model_version: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["model_version", b"model_version", "predictions", b"predictions"]) -> None: ...

global___TextClassificationResponse = TextClassificationResponse

@typing.final
class FewShotTextClassificationRequest(google.protobuf.message.Message):
    """Request for the service to classify text."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MODEL_URI_FIELD_NUMBER: builtins.int
    TASK_DESCRIPTION_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    TEXT_FIELD_NUMBER: builtins.int
    SAMPLES_FIELD_NUMBER: builtins.int
    model_uri: builtins.str
    """The identifier of the classification model."""
    task_description: builtins.str
    """Text description of the classification task."""
    text: builtins.str
    """Text for classification."""
    @property
    def labels(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """List of available labels for the classification result."""

    @property
    def samples(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.ai.foundation_models.v1.text_classification.text_classification_pb2.ClassificationSample]:
        """Optional set of text samples with expected labels that may be used as an additional hint for the classifier."""

    def __init__(
        self,
        *,
        model_uri: builtins.str = ...,
        task_description: builtins.str = ...,
        labels: collections.abc.Iterable[builtins.str] | None = ...,
        text: builtins.str = ...,
        samples: collections.abc.Iterable[yandex.cloud.ai.foundation_models.v1.text_classification.text_classification_pb2.ClassificationSample] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["labels", b"labels", "model_uri", b"model_uri", "samples", b"samples", "task_description", b"task_description", "text", b"text"]) -> None: ...

global___FewShotTextClassificationRequest = FewShotTextClassificationRequest

@typing.final
class FewShotTextClassificationResponse(google.protobuf.message.Message):
    """Response containing classifier predictions."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PREDICTIONS_FIELD_NUMBER: builtins.int
    MODEL_VERSION_FIELD_NUMBER: builtins.int
    model_version: builtins.str
    """Model version (changes with model releases)."""
    @property
    def predictions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.ai.foundation_models.v1.text_classification.text_classification_pb2.ClassificationLabel]:
        """Result of classification - a list of label-confidence pairs."""

    def __init__(
        self,
        *,
        predictions: collections.abc.Iterable[yandex.cloud.ai.foundation_models.v1.text_classification.text_classification_pb2.ClassificationLabel] | None = ...,
        model_version: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["model_version", b"model_version", "predictions", b"predictions"]) -> None: ...

global___FewShotTextClassificationResponse = FewShotTextClassificationResponse
