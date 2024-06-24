"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing
import yandex.cloud.cdn.v1.resource_pb2

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class Rule(google.protobuf.message.Message):
    """Resource rule."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    RULE_PATTERN_FIELD_NUMBER: builtins.int
    OPTIONS_FIELD_NUMBER: builtins.int
    id: builtins.int
    """Rule ID."""
    name: builtins.str
    """Rule name."""
    rule_pattern: builtins.str
    """Rule pattern.
    Must be a valid regular expression.
    """
    @property
    def options(self) -> yandex.cloud.cdn.v1.resource_pb2.ResourceOptions: ...
    def __init__(
        self,
        *,
        id: builtins.int = ...,
        name: builtins.str = ...,
        rule_pattern: builtins.str = ...,
        options: yandex.cloud.cdn.v1.resource_pb2.ResourceOptions | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["id", b"id", "name", b"name", "options", b"options", "rule_pattern", b"rule_pattern"]) -> None: ...

global___Rule = Rule
