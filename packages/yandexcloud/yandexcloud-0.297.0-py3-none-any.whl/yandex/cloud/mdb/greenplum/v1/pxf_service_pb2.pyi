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
import yandex.cloud.mdb.greenplum.v1.pxf_pb2

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class CreatePXFDatasourceMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CLUSTER_ID_FIELD_NUMBER: builtins.int
    DATASOURCE_NAME_FIELD_NUMBER: builtins.int
    cluster_id: builtins.str
    datasource_name: builtins.str
    def __init__(
        self,
        *,
        cluster_id: builtins.str = ...,
        datasource_name: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["cluster_id", b"cluster_id", "datasource_name", b"datasource_name"]) -> None: ...

global___CreatePXFDatasourceMetadata = CreatePXFDatasourceMetadata

@typing.final
class UpdatePXFDatasourceMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CLUSTER_ID_FIELD_NUMBER: builtins.int
    DATASOURCE_NAME_FIELD_NUMBER: builtins.int
    cluster_id: builtins.str
    datasource_name: builtins.str
    def __init__(
        self,
        *,
        cluster_id: builtins.str = ...,
        datasource_name: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["cluster_id", b"cluster_id", "datasource_name", b"datasource_name"]) -> None: ...

global___UpdatePXFDatasourceMetadata = UpdatePXFDatasourceMetadata

@typing.final
class DeletePXFDatasourceMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CLUSTER_ID_FIELD_NUMBER: builtins.int
    DATASOURCE_NAME_FIELD_NUMBER: builtins.int
    cluster_id: builtins.str
    datasource_name: builtins.str
    def __init__(
        self,
        *,
        cluster_id: builtins.str = ...,
        datasource_name: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["cluster_id", b"cluster_id", "datasource_name", b"datasource_name"]) -> None: ...

global___DeletePXFDatasourceMetadata = DeletePXFDatasourceMetadata

@typing.final
class ListPXFDatasourcesRequest(google.protobuf.message.Message):
    """Datasources API"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CLUSTER_ID_FIELD_NUMBER: builtins.int
    cluster_id: builtins.str
    def __init__(
        self,
        *,
        cluster_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["cluster_id", b"cluster_id"]) -> None: ...

global___ListPXFDatasourcesRequest = ListPXFDatasourcesRequest

@typing.final
class ListPXFDatasourcesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DATASOURCES_FIELD_NUMBER: builtins.int
    @property
    def datasources(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.mdb.greenplum.v1.pxf_pb2.PXFDatasource]: ...
    def __init__(
        self,
        *,
        datasources: collections.abc.Iterable[yandex.cloud.mdb.greenplum.v1.pxf_pb2.PXFDatasource] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["datasources", b"datasources"]) -> None: ...

global___ListPXFDatasourcesResponse = ListPXFDatasourcesResponse

@typing.final
class CreatePXFDatasourceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CLUSTER_ID_FIELD_NUMBER: builtins.int
    DATASOURCE_FIELD_NUMBER: builtins.int
    cluster_id: builtins.str
    @property
    def datasource(self) -> yandex.cloud.mdb.greenplum.v1.pxf_pb2.PXFDatasource: ...
    def __init__(
        self,
        *,
        cluster_id: builtins.str = ...,
        datasource: yandex.cloud.mdb.greenplum.v1.pxf_pb2.PXFDatasource | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["datasource", b"datasource"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["cluster_id", b"cluster_id", "datasource", b"datasource"]) -> None: ...

global___CreatePXFDatasourceRequest = CreatePXFDatasourceRequest

@typing.final
class UpdatePXFDatasourceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CLUSTER_ID_FIELD_NUMBER: builtins.int
    UPDATE_MASK_FIELD_NUMBER: builtins.int
    DATASOURCE_FIELD_NUMBER: builtins.int
    cluster_id: builtins.str
    @property
    def update_mask(self) -> google.protobuf.field_mask_pb2.FieldMask: ...
    @property
    def datasource(self) -> yandex.cloud.mdb.greenplum.v1.pxf_pb2.PXFDatasource: ...
    def __init__(
        self,
        *,
        cluster_id: builtins.str = ...,
        update_mask: google.protobuf.field_mask_pb2.FieldMask | None = ...,
        datasource: yandex.cloud.mdb.greenplum.v1.pxf_pb2.PXFDatasource | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["datasource", b"datasource", "update_mask", b"update_mask"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["cluster_id", b"cluster_id", "datasource", b"datasource", "update_mask", b"update_mask"]) -> None: ...

global___UpdatePXFDatasourceRequest = UpdatePXFDatasourceRequest

@typing.final
class DeletePXFDatasourceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CLUSTER_ID_FIELD_NUMBER: builtins.int
    DATASOURCE_NAME_FIELD_NUMBER: builtins.int
    cluster_id: builtins.str
    datasource_name: builtins.str
    def __init__(
        self,
        *,
        cluster_id: builtins.str = ...,
        datasource_name: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["cluster_id", b"cluster_id", "datasource_name", b"datasource_name"]) -> None: ...

global___DeletePXFDatasourceRequest = DeletePXFDatasourceRequest
