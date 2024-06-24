"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import abc
import collections.abc
import grpc
import grpc.aio
import typing
import yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_crypto_service_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class AsymmetricEncryptionCryptoServiceStub:
    """Data plane for KMS symmetric cryptography operations

    Set of methods that perform asymmetric decryption.
    """

    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    Decrypt: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_crypto_service_pb2.AsymmetricDecryptRequest,
        yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_crypto_service_pb2.AsymmetricDecryptResponse,
    ]
    """Decrypts the given ciphertext with the specified key."""

    GetPublicKey: grpc.UnaryUnaryMultiCallable[
        yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_crypto_service_pb2.AsymmetricGetPublicKeyRequest,
        yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_crypto_service_pb2.AsymmetricGetPublicKeyResponse,
    ]
    """Gets value of public key."""

class AsymmetricEncryptionCryptoServiceAsyncStub:
    """Data plane for KMS symmetric cryptography operations

    Set of methods that perform asymmetric decryption.
    """

    Decrypt: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_crypto_service_pb2.AsymmetricDecryptRequest,
        yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_crypto_service_pb2.AsymmetricDecryptResponse,
    ]
    """Decrypts the given ciphertext with the specified key."""

    GetPublicKey: grpc.aio.UnaryUnaryMultiCallable[
        yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_crypto_service_pb2.AsymmetricGetPublicKeyRequest,
        yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_crypto_service_pb2.AsymmetricGetPublicKeyResponse,
    ]
    """Gets value of public key."""

class AsymmetricEncryptionCryptoServiceServicer(metaclass=abc.ABCMeta):
    """Data plane for KMS symmetric cryptography operations

    Set of methods that perform asymmetric decryption.
    """

    @abc.abstractmethod
    def Decrypt(
        self,
        request: yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_crypto_service_pb2.AsymmetricDecryptRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_crypto_service_pb2.AsymmetricDecryptResponse, collections.abc.Awaitable[yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_crypto_service_pb2.AsymmetricDecryptResponse]]:
        """Decrypts the given ciphertext with the specified key."""

    @abc.abstractmethod
    def GetPublicKey(
        self,
        request: yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_crypto_service_pb2.AsymmetricGetPublicKeyRequest,
        context: _ServicerContext,
    ) -> typing.Union[yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_crypto_service_pb2.AsymmetricGetPublicKeyResponse, collections.abc.Awaitable[yandex.cloud.kms.v1.asymmetricencryption.asymmetric_encryption_crypto_service_pb2.AsymmetricGetPublicKeyResponse]]:
        """Gets value of public key."""

def add_AsymmetricEncryptionCryptoServiceServicer_to_server(servicer: AsymmetricEncryptionCryptoServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
