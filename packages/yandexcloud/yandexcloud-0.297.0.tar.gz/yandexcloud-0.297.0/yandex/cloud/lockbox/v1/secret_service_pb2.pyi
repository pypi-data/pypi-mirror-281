"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.duration_pb2
import google.protobuf.field_mask_pb2
import google.protobuf.internal.containers
import google.protobuf.message
import google.protobuf.timestamp_pb2
import typing
import yandex.cloud.lockbox.v1.secret_pb2
import yandex.cloud.operation.operation_pb2

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class PayloadEntryChange(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KEY_FIELD_NUMBER: builtins.int
    TEXT_VALUE_FIELD_NUMBER: builtins.int
    BINARY_VALUE_FIELD_NUMBER: builtins.int
    key: builtins.str
    """Non-confidential key of the entry."""
    text_value: builtins.str
    """Use the field to set a text value."""
    binary_value: builtins.bytes
    """Use the field to set a binary value."""
    def __init__(
        self,
        *,
        key: builtins.str = ...,
        text_value: builtins.str = ...,
        binary_value: builtins.bytes = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["binary_value", b"binary_value", "text_value", b"text_value", "value", b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["binary_value", b"binary_value", "key", b"key", "text_value", b"text_value", "value", b"value"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["value", b"value"]) -> typing.Literal["text_value", "binary_value"] | None: ...

global___PayloadEntryChange = PayloadEntryChange

@typing.final
class GetSecretRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ID_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret to return.

    To get a secret ID make a [List] request.
    """
    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["secret_id", b"secret_id"]) -> None: ...

global___GetSecretRequest = GetSecretRequest

@typing.final
class ListSecretsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FOLDER_ID_FIELD_NUMBER: builtins.int
    PAGE_SIZE_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    folder_id: builtins.str
    """ID of the folder to list secrets in."""
    page_size: builtins.int
    """The maximum number of results per page to return. If the number of available
    results is larger than `page_size`, the service returns a [ListSecretsRequest.next_page_token]
    that can be used to get the next page of results in subsequent list requests.
    Default value: 100.
    """
    page_token: builtins.str
    """Page token. To get the next page of results, set `page_token` to the
    [ListSecretsRequest.next_page_token] returned by a previous list request.
    """
    def __init__(
        self,
        *,
        folder_id: builtins.str = ...,
        page_size: builtins.int = ...,
        page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["folder_id", b"folder_id", "page_size", b"page_size", "page_token", b"page_token"]) -> None: ...

global___ListSecretsRequest = ListSecretsRequest

@typing.final
class ListSecretsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRETS_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    next_page_token: builtins.str
    """This token allows you to get the next page of results for list requests. If the number
    of results is greater than the specified [ListSecretsRequest.page_size], use
    the `next_page_token` as the value for the [ListSecretsRequest.page_token] query parameter
    in the next list request. Each subsequent list request will have its own
    `next_page_token` to continue paging through the results.
    """
    @property
    def secrets(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.lockbox.v1.secret_pb2.Secret]:
        """List of secrets in the specified folder."""

    def __init__(
        self,
        *,
        secrets: collections.abc.Iterable[yandex.cloud.lockbox.v1.secret_pb2.Secret] | None = ...,
        next_page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["next_page_token", b"next_page_token", "secrets", b"secrets"]) -> None: ...

global___ListSecretsResponse = ListSecretsResponse

@typing.final
class CreateSecretRequest(google.protobuf.message.Message):
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
    KMS_KEY_ID_FIELD_NUMBER: builtins.int
    VERSION_DESCRIPTION_FIELD_NUMBER: builtins.int
    VERSION_PAYLOAD_ENTRIES_FIELD_NUMBER: builtins.int
    DELETION_PROTECTION_FIELD_NUMBER: builtins.int
    folder_id: builtins.str
    """ID of the folder to create a secret in."""
    name: builtins.str
    """Name of the secret."""
    description: builtins.str
    """Description of the secret."""
    kms_key_id: builtins.str
    """Optional ID of the KMS key will be used to encrypt and decrypt the secret."""
    version_description: builtins.str
    """Description of the first version."""
    deletion_protection: builtins.bool
    """Flag that inhibits deletion of the secret."""
    @property
    def labels(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]:
        """Custom labels for the secret as `key:value` pairs. Maximum 64 per key.
        For example, `"project": "mvp"` or `"source": "dictionary"`.
        """

    @property
    def version_payload_entries(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___PayloadEntryChange]:
        """Payload entries added to the first version."""

    def __init__(
        self,
        *,
        folder_id: builtins.str = ...,
        name: builtins.str = ...,
        description: builtins.str = ...,
        labels: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        kms_key_id: builtins.str = ...,
        version_description: builtins.str = ...,
        version_payload_entries: collections.abc.Iterable[global___PayloadEntryChange] | None = ...,
        deletion_protection: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deletion_protection", b"deletion_protection", "description", b"description", "folder_id", b"folder_id", "kms_key_id", b"kms_key_id", "labels", b"labels", "name", b"name", "version_description", b"version_description", "version_payload_entries", b"version_payload_entries"]) -> None: ...

global___CreateSecretRequest = CreateSecretRequest

@typing.final
class CreateSecretMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ID_FIELD_NUMBER: builtins.int
    VERSION_ID_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret being created."""
    version_id: builtins.str
    """ID of the current version of the secret being created."""
    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
        version_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["secret_id", b"secret_id", "version_id", b"version_id"]) -> None: ...

global___CreateSecretMetadata = CreateSecretMetadata

@typing.final
class UpdateSecretRequest(google.protobuf.message.Message):
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

    SECRET_ID_FIELD_NUMBER: builtins.int
    UPDATE_MASK_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    DELETION_PROTECTION_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret to update."""
    name: builtins.str
    """New name of the secret."""
    description: builtins.str
    """New description of the secret."""
    deletion_protection: builtins.bool
    """Flag that inhibits deletion of the secret."""
    @property
    def update_mask(self) -> google.protobuf.field_mask_pb2.FieldMask:
        """Field mask that specifies which attributes of the secret are going to be updated."""

    @property
    def labels(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]:
        """Custom labels for the secret as `key:value` pairs. Maximum 64 per key."""

    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
        update_mask: google.protobuf.field_mask_pb2.FieldMask | None = ...,
        name: builtins.str = ...,
        description: builtins.str = ...,
        labels: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        deletion_protection: builtins.bool = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["update_mask", b"update_mask"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["deletion_protection", b"deletion_protection", "description", b"description", "labels", b"labels", "name", b"name", "secret_id", b"secret_id", "update_mask", b"update_mask"]) -> None: ...

global___UpdateSecretRequest = UpdateSecretRequest

@typing.final
class UpdateSecretMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ID_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret being updated."""
    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["secret_id", b"secret_id"]) -> None: ...

global___UpdateSecretMetadata = UpdateSecretMetadata

@typing.final
class DeleteSecretRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ID_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret to be deleted."""
    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["secret_id", b"secret_id"]) -> None: ...

global___DeleteSecretRequest = DeleteSecretRequest

@typing.final
class DeleteSecretMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ID_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret being deleted."""
    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["secret_id", b"secret_id"]) -> None: ...

global___DeleteSecretMetadata = DeleteSecretMetadata

@typing.final
class ActivateSecretRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ID_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret to be activated."""
    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["secret_id", b"secret_id"]) -> None: ...

global___ActivateSecretRequest = ActivateSecretRequest

@typing.final
class ActivateSecretMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ID_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret being activated."""
    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["secret_id", b"secret_id"]) -> None: ...

global___ActivateSecretMetadata = ActivateSecretMetadata

@typing.final
class DeactivateSecretRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ID_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret to be deactivated."""
    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["secret_id", b"secret_id"]) -> None: ...

global___DeactivateSecretRequest = DeactivateSecretRequest

@typing.final
class DeactivateSecretMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ID_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret being deactivated."""
    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["secret_id", b"secret_id"]) -> None: ...

global___DeactivateSecretMetadata = DeactivateSecretMetadata

@typing.final
class AddVersionRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ID_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    PAYLOAD_ENTRIES_FIELD_NUMBER: builtins.int
    BASE_VERSION_ID_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret."""
    description: builtins.str
    """Description of the version."""
    base_version_id: builtins.str
    """Optional base version id. Defaults to the current version if not specified"""
    @property
    def payload_entries(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___PayloadEntryChange]:
        """Describe how payload entries of the base version change in the added version."""

    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
        description: builtins.str = ...,
        payload_entries: collections.abc.Iterable[global___PayloadEntryChange] | None = ...,
        base_version_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["base_version_id", b"base_version_id", "description", b"description", "payload_entries", b"payload_entries", "secret_id", b"secret_id"]) -> None: ...

global___AddVersionRequest = AddVersionRequest

@typing.final
class AddVersionMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ID_FIELD_NUMBER: builtins.int
    VERSION_ID_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret."""
    version_id: builtins.str
    """ID of the added version."""
    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
        version_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["secret_id", b"secret_id", "version_id", b"version_id"]) -> None: ...

global___AddVersionMetadata = AddVersionMetadata

@typing.final
class ListVersionsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ID_FIELD_NUMBER: builtins.int
    PAGE_SIZE_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret to list versions for."""
    page_size: builtins.int
    """The maximum number of results per page to return. If the number of available
    results is larger than `page_size`, the service returns a [ListVersionsRequest.next_page_token]
    that can be used to get the next page of results in subsequent list requests.
    Default value: 100.
    """
    page_token: builtins.str
    """Page token. To get the next page of results, set `page_token` to the
    [ListVersionsRequest.next_page_token] returned by a previous list request.
    """
    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
        page_size: builtins.int = ...,
        page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["page_size", b"page_size", "page_token", b"page_token", "secret_id", b"secret_id"]) -> None: ...

global___ListVersionsRequest = ListVersionsRequest

@typing.final
class ListVersionsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VERSIONS_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    next_page_token: builtins.str
    """This token allows you to get the next page of results for list requests. If the number
    of results is greater than the specified [ListVersionsRequest.page_size], use
    the `next_page_token` as the value for the [ListVersionsRequest.page_token] query parameter
    in the next list request. Each subsequent list request will have its own
    `next_page_token` to continue paging through the results.
    """
    @property
    def versions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.lockbox.v1.secret_pb2.Version]:
        """List of versions for the specified secret."""

    def __init__(
        self,
        *,
        versions: collections.abc.Iterable[yandex.cloud.lockbox.v1.secret_pb2.Version] | None = ...,
        next_page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["next_page_token", b"next_page_token", "versions", b"versions"]) -> None: ...

global___ListVersionsResponse = ListVersionsResponse

@typing.final
class ScheduleVersionDestructionRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ID_FIELD_NUMBER: builtins.int
    VERSION_ID_FIELD_NUMBER: builtins.int
    PENDING_PERIOD_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret whose version should be scheduled for destruction."""
    version_id: builtins.str
    """ID of the version to be destroyed."""
    @property
    def pending_period(self) -> google.protobuf.duration_pb2.Duration:
        """Time interval between the version destruction request and actual destruction.
        Default value: 7 days.
        """

    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
        version_id: builtins.str = ...,
        pending_period: google.protobuf.duration_pb2.Duration | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["pending_period", b"pending_period"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["pending_period", b"pending_period", "secret_id", b"secret_id", "version_id", b"version_id"]) -> None: ...

global___ScheduleVersionDestructionRequest = ScheduleVersionDestructionRequest

@typing.final
class ScheduleVersionDestructionMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ID_FIELD_NUMBER: builtins.int
    VERSION_ID_FIELD_NUMBER: builtins.int
    DESTROY_AT_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret whose version is being scheduled for destruction."""
    version_id: builtins.str
    """ID of the version that is being scheduled for destruction."""
    @property
    def destroy_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Destruction timestamp."""

    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
        version_id: builtins.str = ...,
        destroy_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["destroy_at", b"destroy_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["destroy_at", b"destroy_at", "secret_id", b"secret_id", "version_id", b"version_id"]) -> None: ...

global___ScheduleVersionDestructionMetadata = ScheduleVersionDestructionMetadata

@typing.final
class CancelVersionDestructionRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ID_FIELD_NUMBER: builtins.int
    VERSION_ID_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret to cancel a version's destruction for."""
    version_id: builtins.str
    """ID of the secret whose scheduled destruction should be cancelled."""
    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
        version_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["secret_id", b"secret_id", "version_id", b"version_id"]) -> None: ...

global___CancelVersionDestructionRequest = CancelVersionDestructionRequest

@typing.final
class CancelVersionDestructionMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ID_FIELD_NUMBER: builtins.int
    VERSION_ID_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret whose version's destruction is being cancelled."""
    version_id: builtins.str
    """ID of the version whose scheduled destruction is being cancelled."""
    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
        version_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["secret_id", b"secret_id", "version_id", b"version_id"]) -> None: ...

global___CancelVersionDestructionMetadata = CancelVersionDestructionMetadata

@typing.final
class ListSecretOperationsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECRET_ID_FIELD_NUMBER: builtins.int
    PAGE_SIZE_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    secret_id: builtins.str
    """ID of the secret to get operations for."""
    page_size: builtins.int
    """The maximum number of results per page that should be returned. If the number of available
    results is larger than `page_size`, the service returns a [ListSecretOperationsRequest.next_page_token]
    that can be used to get the next page of results in subsequent list requests.
    Default value: 100.
    """
    page_token: builtins.str
    """Page token. To get the next page of results, set `page_token` to the
    [ListSecretOperationsRequest.next_page_token] returned by a previous list request.
    """
    def __init__(
        self,
        *,
        secret_id: builtins.str = ...,
        page_size: builtins.int = ...,
        page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["page_size", b"page_size", "page_token", b"page_token", "secret_id", b"secret_id"]) -> None: ...

global___ListSecretOperationsRequest = ListSecretOperationsRequest

@typing.final
class ListSecretOperationsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    OPERATIONS_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    next_page_token: builtins.str
    """This token allows you to get the next page of results for list requests. If the number of results
    is larger than [ListSecretOperationsResponse.page_size], use the `next_page_token` as the value
    for the [ListSecretOperationsResponse.page_token] query parameter in the next list request.
    Each subsequent list request will have its own `next_page_token` to continue paging through the results.
    """
    @property
    def operations(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.operation.operation_pb2.Operation]:
        """List of operations for the specified secret."""

    def __init__(
        self,
        *,
        operations: collections.abc.Iterable[yandex.cloud.operation.operation_pb2.Operation] | None = ...,
        next_page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["next_page_token", b"next_page_token", "operations", b"operations"]) -> None: ...

global___ListSecretOperationsResponse = ListSecretOperationsResponse
