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
import yandex.cloud.datatransfer.v1.endpoint.common_pb2

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class OnPremiseMongo(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HOSTS_FIELD_NUMBER: builtins.int
    PORT_FIELD_NUMBER: builtins.int
    REPLICA_SET_FIELD_NUMBER: builtins.int
    TLS_MODE_FIELD_NUMBER: builtins.int
    port: builtins.int
    replica_set: builtins.str
    @property
    def hosts(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def tls_mode(self) -> yandex.cloud.datatransfer.v1.endpoint.common_pb2.TLSMode: ...
    def __init__(
        self,
        *,
        hosts: collections.abc.Iterable[builtins.str] | None = ...,
        port: builtins.int = ...,
        replica_set: builtins.str = ...,
        tls_mode: yandex.cloud.datatransfer.v1.endpoint.common_pb2.TLSMode | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["tls_mode", b"tls_mode"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["hosts", b"hosts", "port", b"port", "replica_set", b"replica_set", "tls_mode", b"tls_mode"]) -> None: ...

global___OnPremiseMongo = OnPremiseMongo

@typing.final
class MongoConnectionOptions(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MDB_CLUSTER_ID_FIELD_NUMBER: builtins.int
    ON_PREMISE_FIELD_NUMBER: builtins.int
    USER_FIELD_NUMBER: builtins.int
    PASSWORD_FIELD_NUMBER: builtins.int
    AUTH_SOURCE_FIELD_NUMBER: builtins.int
    mdb_cluster_id: builtins.str
    user: builtins.str
    """User name"""
    auth_source: builtins.str
    """Database name associated with the credentials"""
    @property
    def on_premise(self) -> global___OnPremiseMongo: ...
    @property
    def password(self) -> yandex.cloud.datatransfer.v1.endpoint.common_pb2.Secret:
        """Password for user"""

    def __init__(
        self,
        *,
        mdb_cluster_id: builtins.str = ...,
        on_premise: global___OnPremiseMongo | None = ...,
        user: builtins.str = ...,
        password: yandex.cloud.datatransfer.v1.endpoint.common_pb2.Secret | None = ...,
        auth_source: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["address", b"address", "mdb_cluster_id", b"mdb_cluster_id", "on_premise", b"on_premise", "password", b"password"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["address", b"address", "auth_source", b"auth_source", "mdb_cluster_id", b"mdb_cluster_id", "on_premise", b"on_premise", "password", b"password", "user", b"user"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["address", b"address"]) -> typing.Literal["mdb_cluster_id", "on_premise"] | None: ...

global___MongoConnectionOptions = MongoConnectionOptions

@typing.final
class MongoConnection(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONNECTION_OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def connection_options(self) -> global___MongoConnectionOptions: ...
    def __init__(
        self,
        *,
        connection_options: global___MongoConnectionOptions | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["connection", b"connection", "connection_options", b"connection_options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["connection", b"connection", "connection_options", b"connection_options"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["connection", b"connection"]) -> typing.Literal["connection_options"] | None: ...

global___MongoConnection = MongoConnection

@typing.final
class MongoCollection(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DATABASE_NAME_FIELD_NUMBER: builtins.int
    COLLECTION_NAME_FIELD_NUMBER: builtins.int
    database_name: builtins.str
    collection_name: builtins.str
    def __init__(
        self,
        *,
        database_name: builtins.str = ...,
        collection_name: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["collection_name", b"collection_name", "database_name", b"database_name"]) -> None: ...

global___MongoCollection = MongoCollection

@typing.final
class MongoSource(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONNECTION_FIELD_NUMBER: builtins.int
    SUBNET_ID_FIELD_NUMBER: builtins.int
    COLLECTIONS_FIELD_NUMBER: builtins.int
    EXCLUDED_COLLECTIONS_FIELD_NUMBER: builtins.int
    SECONDARY_PREFERRED_MODE_FIELD_NUMBER: builtins.int
    SECURITY_GROUPS_FIELD_NUMBER: builtins.int
    subnet_id: builtins.str
    secondary_preferred_mode: builtins.bool
    """Read mode for mongo client"""
    @property
    def connection(self) -> global___MongoConnection: ...
    @property
    def collections(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___MongoCollection]:
        """List of collections for replication. Empty list implies replication of all
        tables on the deployment. Allowed to use * as collection name.
        """

    @property
    def excluded_collections(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___MongoCollection]:
        """List of forbidden collections for replication. Allowed to use * as collection
        name for forbid all collections of concrete schema.
        """

    @property
    def security_groups(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Security groups"""

    def __init__(
        self,
        *,
        connection: global___MongoConnection | None = ...,
        subnet_id: builtins.str = ...,
        collections: collections.abc.Iterable[global___MongoCollection] | None = ...,
        excluded_collections: collections.abc.Iterable[global___MongoCollection] | None = ...,
        secondary_preferred_mode: builtins.bool = ...,
        security_groups: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["connection", b"connection"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["collections", b"collections", "connection", b"connection", "excluded_collections", b"excluded_collections", "secondary_preferred_mode", b"secondary_preferred_mode", "security_groups", b"security_groups", "subnet_id", b"subnet_id"]) -> None: ...

global___MongoSource = MongoSource

@typing.final
class MongoTarget(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONNECTION_FIELD_NUMBER: builtins.int
    DATABASE_FIELD_NUMBER: builtins.int
    CLEANUP_POLICY_FIELD_NUMBER: builtins.int
    SUBNET_ID_FIELD_NUMBER: builtins.int
    SECURITY_GROUPS_FIELD_NUMBER: builtins.int
    database: builtins.str
    """Database name"""
    cleanup_policy: yandex.cloud.datatransfer.v1.endpoint.common_pb2.CleanupPolicy.ValueType
    subnet_id: builtins.str
    @property
    def connection(self) -> global___MongoConnection: ...
    @property
    def security_groups(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Security groups"""

    def __init__(
        self,
        *,
        connection: global___MongoConnection | None = ...,
        database: builtins.str = ...,
        cleanup_policy: yandex.cloud.datatransfer.v1.endpoint.common_pb2.CleanupPolicy.ValueType = ...,
        subnet_id: builtins.str = ...,
        security_groups: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["connection", b"connection"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["cleanup_policy", b"cleanup_policy", "connection", b"connection", "database", b"database", "security_groups", b"security_groups", "subnet_id", b"subnet_id"]) -> None: ...

global___MongoTarget = MongoTarget
