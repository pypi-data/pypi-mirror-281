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
class ClassAnnotation(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PROPERTIES_FIELD_NUMBER: builtins.int
    @property
    def properties(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Property]:
        """Properties extracted by a specified model.

        For example, if you ask to evaluate the image quality,
        the service could return such properties as `good` and `bad`.
        """

    def __init__(
        self,
        *,
        properties: collections.abc.Iterable[global___Property] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["properties", b"properties"]) -> None: ...

global___ClassAnnotation = ClassAnnotation

@typing.final
class Property(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    PROBABILITY_FIELD_NUMBER: builtins.int
    name: builtins.str
    """Property name."""
    probability: builtins.float
    """Probability of the property, from 0 to 1."""
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        probability: builtins.float = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["name", b"name", "probability", b"probability"]) -> None: ...

global___Property = Property
