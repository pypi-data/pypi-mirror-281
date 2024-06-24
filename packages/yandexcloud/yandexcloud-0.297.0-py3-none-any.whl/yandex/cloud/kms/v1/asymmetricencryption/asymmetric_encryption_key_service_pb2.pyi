"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.field_mask_pb2
import google.protobuf.internal.containers
import google.protobuf.message
import typing
import yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_key_pb2
import yandex.cloud.operation.operation_pb2

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class CreateAsymmetricEncryptionKeyRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class LabelsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.str
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    FOLDER_ID_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    ENCRYPTION_ALGORITHM_FIELD_NUMBER: builtins.int
    DELETION_PROTECTION_FIELD_NUMBER: builtins.int
    folder_id: builtins.str
    """ID of the folder to create a asymmetric KMS key in."""
    name: builtins.str
    """Name of the key."""
    description: builtins.str
    """Description of the key."""
    encryption_algorithm: yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_key_pb2.AsymmetricEncryptionAlgorithm.ValueType
    """Asymmetric encryption algorithm."""
    deletion_protection: builtins.bool
    """Flag that inhibits deletion of the symmetric KMS key"""
    @property
    def labels(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]:
        """Custom labels for the asymmetric KMS key as `key:value` pairs. Maximum 64 per key.
        For example, `"project": "mvp"` or `"source": "dictionary"`.
        """

    def __init__(
        self,
        *,
        folder_id: builtins.str = ...,
        name: builtins.str = ...,
        description: builtins.str = ...,
        labels: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        encryption_algorithm: yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_key_pb2.AsymmetricEncryptionAlgorithm.ValueType = ...,
        deletion_protection: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deletion_protection", b"deletion_protection", "description", b"description", "encryption_algorithm", b"encryption_algorithm", "folder_id", b"folder_id", "labels", b"labels", "name", b"name"]) -> None: ...

global___CreateAsymmetricEncryptionKeyRequest = CreateAsymmetricEncryptionKeyRequest

@typing.final
class CreateAsymmetricEncryptionKeyMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KEY_ID_FIELD_NUMBER: builtins.int
    key_id: builtins.str
    """ID of the key being created."""
    def __init__(
        self,
        *,
        key_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["key_id", b"key_id"]) -> None: ...

global___CreateAsymmetricEncryptionKeyMetadata = CreateAsymmetricEncryptionKeyMetadata

@typing.final
class GetAsymmetricEncryptionKeyRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KEY_ID_FIELD_NUMBER: builtins.int
    key_id: builtins.str
    """ID of the asymmetric KMS key to return.
    To get the ID of an asymmetric KMS key use a [AsymmetricEncryptionKeyService.List] request.
    """
    def __init__(
        self,
        *,
        key_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["key_id", b"key_id"]) -> None: ...

global___GetAsymmetricEncryptionKeyRequest = GetAsymmetricEncryptionKeyRequest

@typing.final
class ListAsymmetricEncryptionKeysRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FOLDER_ID_FIELD_NUMBER: builtins.int
    PAGE_SIZE_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    folder_id: builtins.str
    """ID of the folder to list asymmetric KMS keys in."""
    page_size: builtins.int
    """The maximum number of results per page to return. If the number of available
    results is larger than [page_size], the service returns a [ListAsymmetricEncryptionKeysResponse.next_page_token]
    that can be used to get the next page of results in subsequent list requests.
    Default value: 100.
    """
    page_token: builtins.str
    """Page token. To get the next page of results, set [page_token] to the
    [ListAsymmetricEncryptionKeysResponse.next_page_token] returned by a previous list request.
    """
    def __init__(
        self,
        *,
        folder_id: builtins.str = ...,
        page_size: builtins.int = ...,
        page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["folder_id", b"folder_id", "page_size", b"page_size", "page_token", b"page_token"]) -> None: ...

global___ListAsymmetricEncryptionKeysRequest = ListAsymmetricEncryptionKeysRequest

@typing.final
class ListAsymmetricEncryptionKeysResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KEYS_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    next_page_token: builtins.str
    """This token allows you to get the next page of results for list requests. If the number
    of results is greater than the specified [ListAsymmetricEncryptionKeysRequest.page_size], use
    the [next_page_token] as the value for the [ListAsymmetricEncryptionKeysRequest.page_token] query parameter
    in the next list request. Each subsequent list request will have its own
    [next_page_token] to continue paging through the results.
    """
    @property
    def keys(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_key_pb2.AsymmetricEncryptionKey]:
        """List of asymmetric KMS keys in the specified folder."""

    def __init__(
        self,
        *,
        keys: collections.abc.Iterable[yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_key_pb2.AsymmetricEncryptionKey] | None = ...,
        next_page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["keys", b"keys", "next_page_token", b"next_page_token"]) -> None: ...

global___ListAsymmetricEncryptionKeysResponse = ListAsymmetricEncryptionKeysResponse

@typing.final
class UpdateAsymmetricEncryptionKeyRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class LabelsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.str
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    KEY_ID_FIELD_NUMBER: builtins.int
    UPDATE_MASK_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    DELETION_PROTECTION_FIELD_NUMBER: builtins.int
    key_id: builtins.str
    """ID of the asymmetric KMS key to update.
    To get the ID of a asymmetric KMS key use a [AsymmetricEncryptionKeyService.List] request.
    """
    name: builtins.str
    """New name for the asymmetric KMS key."""
    description: builtins.str
    """New description for the asymmetric KMS key."""
    status: yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_key_pb2.AsymmetricEncryptionKey.Status.ValueType
    """New status for the asymmetric KMS key.
    Using the [AsymmetricEncryptionKeyService.Update] method you can only set ACTIVE or INACTIVE status.
    """
    deletion_protection: builtins.bool
    """Flag that inhibits deletion of the asymmetric KMS key"""
    @property
    def update_mask(self) -> google.protobuf.field_mask_pb2.FieldMask:
        """Field mask that specifies which attributes of the asymmetric KMS key are going to be updated."""

    @property
    def labels(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]:
        """Custom labels for the asymmetric KMS key as `key:value` pairs. Maximum 64 per key."""

    def __init__(
        self,
        *,
        key_id: builtins.str = ...,
        update_mask: google.protobuf.field_mask_pb2.FieldMask | None = ...,
        name: builtins.str = ...,
        description: builtins.str = ...,
        status: yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_key_pb2.AsymmetricEncryptionKey.Status.ValueType = ...,
        labels: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        deletion_protection: builtins.bool = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["update_mask", b"update_mask"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["deletion_protection", b"deletion_protection", "description", b"description", "key_id", b"key_id", "labels", b"labels", "name", b"name", "status", b"status", "update_mask", b"update_mask"]) -> None: ...

global___UpdateAsymmetricEncryptionKeyRequest = UpdateAsymmetricEncryptionKeyRequest

@typing.final
class UpdateAsymmetricEncryptionKeyMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KEY_ID_FIELD_NUMBER: builtins.int
    key_id: builtins.str
    """ID of the key being updated."""
    def __init__(
        self,
        *,
        key_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["key_id", b"key_id"]) -> None: ...

global___UpdateAsymmetricEncryptionKeyMetadata = UpdateAsymmetricEncryptionKeyMetadata

@typing.final
class DeleteAsymmetricEncryptionKeyRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KEY_ID_FIELD_NUMBER: builtins.int
    key_id: builtins.str
    """ID of the key to be deleted."""
    def __init__(
        self,
        *,
        key_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["key_id", b"key_id"]) -> None: ...

global___DeleteAsymmetricEncryptionKeyRequest = DeleteAsymmetricEncryptionKeyRequest

@typing.final
class DeleteAsymmetricEncryptionKeyMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KEY_ID_FIELD_NUMBER: builtins.int
    key_id: builtins.str
    """ID of the key being deleted."""
    def __init__(
        self,
        *,
        key_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["key_id", b"key_id"]) -> None: ...

global___DeleteAsymmetricEncryptionKeyMetadata = DeleteAsymmetricEncryptionKeyMetadata

@typing.final
class ListAsymmetricEncryptionKeyOperationsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KEY_ID_FIELD_NUMBER: builtins.int
    PAGE_SIZE_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    key_id: builtins.str
    """ID of the symmetric KMS key to get operations for.

    To get the key ID, use a [AsymmetricKeyEncryptionService.List] request.
    """
    page_size: builtins.int
    """The maximum number of results per page that should be returned. If the number of available
    results is larger than [page_size], the service returns a [ListAsymmetricEncryptionKeyOperationsResponse.next_page_token]
    that can be used to get the next page of results in subsequent list requests.
    Default value: 100.
    """
    page_token: builtins.str
    """Page token. To get the next page of results, set [page_token] to the
    [ListAsymmetricKeyOperationsResponse.next_page_token] returned by a previous list request.
    """
    def __init__(
        self,
        *,
        key_id: builtins.str = ...,
        page_size: builtins.int = ...,
        page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["key_id", b"key_id", "page_size", b"page_size", "page_token", b"page_token"]) -> None: ...

global___ListAsymmetricEncryptionKeyOperationsRequest = ListAsymmetricEncryptionKeyOperationsRequest

@typing.final
class ListAsymmetricEncryptionKeyOperationsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    OPERATIONS_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    next_page_token: builtins.str
    """This token allows you to get the next page of results for list requests. If the number of results
    is larger than [ListAsymmetricEncryptionKeyOperationsRequest.page_size], use the [next_page_token] as the value
    for the [ListAsymmetricEncryptionKeyOperationsRequest.page_token] query parameter in the next list request.
    Each subsequent list request will have its own [next_page_token] to continue paging through the results.
    """
    @property
    def operations(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.operation.operation_pb2.Operation]:
        """List of operations for the specified key."""

    def __init__(
        self,
        *,
        operations: collections.abc.Iterable[yandex.cloud.operation.operation_pb2.Operation] | None = ...,
        next_page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["next_page_token", b"next_page_token", "operations", b"operations"]) -> None: ...

global___ListAsymmetricEncryptionKeyOperationsResponse = ListAsymmetricEncryptionKeyOperationsResponse
