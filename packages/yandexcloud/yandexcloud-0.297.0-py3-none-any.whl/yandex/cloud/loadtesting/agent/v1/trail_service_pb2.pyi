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
class CreateTrailRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COMPUTE_INSTANCE_ID_FIELD_NUMBER: builtins.int
    DATA_FIELD_NUMBER: builtins.int
    JOB_ID_FIELD_NUMBER: builtins.int
    AGENT_INSTANCE_ID_FIELD_NUMBER: builtins.int
    compute_instance_id: builtins.str
    job_id: builtins.str
    agent_instance_id: builtins.str
    @property
    def data(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Trail]: ...
    def __init__(
        self,
        *,
        compute_instance_id: builtins.str = ...,
        data: collections.abc.Iterable[global___Trail] | None = ...,
        job_id: builtins.str = ...,
        agent_instance_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["agent_instance_id", b"agent_instance_id", "compute_instance_id", b"compute_instance_id", "data", b"data", "job_id", b"job_id"]) -> None: ...

global___CreateTrailRequest = CreateTrailRequest

@typing.final
class Trail(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class Codes(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        CODE_FIELD_NUMBER: builtins.int
        COUNT_FIELD_NUMBER: builtins.int
        code: builtins.int
        count: builtins.int
        def __init__(
            self,
            *,
            code: builtins.int = ...,
            count: builtins.int = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["code", b"code", "count", b"count"]) -> None: ...

    @typing.final
    class Intervals(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        TO_FIELD_NUMBER: builtins.int
        COUNT_FIELD_NUMBER: builtins.int
        to: builtins.float
        count: builtins.int
        def __init__(
            self,
            *,
            to: builtins.float = ...,
            count: builtins.int = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["count", b"count", "to", b"to"]) -> None: ...

    OVERALL_FIELD_NUMBER: builtins.int
    CASE_ID_FIELD_NUMBER: builtins.int
    TIME_FIELD_NUMBER: builtins.int
    REQPS_FIELD_NUMBER: builtins.int
    RESPS_FIELD_NUMBER: builtins.int
    EXPECT_FIELD_NUMBER: builtins.int
    INPUT_FIELD_NUMBER: builtins.int
    OUTPUT_FIELD_NUMBER: builtins.int
    CONNECT_TIME_FIELD_NUMBER: builtins.int
    SEND_TIME_FIELD_NUMBER: builtins.int
    LATENCY_FIELD_NUMBER: builtins.int
    RECEIVE_TIME_FIELD_NUMBER: builtins.int
    THREADS_FIELD_NUMBER: builtins.int
    Q50_FIELD_NUMBER: builtins.int
    Q75_FIELD_NUMBER: builtins.int
    Q80_FIELD_NUMBER: builtins.int
    Q85_FIELD_NUMBER: builtins.int
    Q90_FIELD_NUMBER: builtins.int
    Q95_FIELD_NUMBER: builtins.int
    Q98_FIELD_NUMBER: builtins.int
    Q99_FIELD_NUMBER: builtins.int
    Q100_FIELD_NUMBER: builtins.int
    HTTP_CODES_FIELD_NUMBER: builtins.int
    NET_CODES_FIELD_NUMBER: builtins.int
    TIME_INTERVALS_FIELD_NUMBER: builtins.int
    overall: builtins.int
    case_id: builtins.str
    time: builtins.str
    reqps: builtins.int
    resps: builtins.int
    expect: builtins.float
    input: builtins.int
    output: builtins.int
    connect_time: builtins.float
    send_time: builtins.float
    latency: builtins.float
    receive_time: builtins.float
    threads: builtins.int
    q50: builtins.float
    q75: builtins.float
    q80: builtins.float
    q85: builtins.float
    q90: builtins.float
    q95: builtins.float
    q98: builtins.float
    q99: builtins.float
    q100: builtins.float
    @property
    def http_codes(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Trail.Codes]: ...
    @property
    def net_codes(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Trail.Codes]: ...
    @property
    def time_intervals(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Trail.Intervals]: ...
    def __init__(
        self,
        *,
        overall: builtins.int = ...,
        case_id: builtins.str = ...,
        time: builtins.str = ...,
        reqps: builtins.int = ...,
        resps: builtins.int = ...,
        expect: builtins.float = ...,
        input: builtins.int = ...,
        output: builtins.int = ...,
        connect_time: builtins.float = ...,
        send_time: builtins.float = ...,
        latency: builtins.float = ...,
        receive_time: builtins.float = ...,
        threads: builtins.int = ...,
        q50: builtins.float = ...,
        q75: builtins.float = ...,
        q80: builtins.float = ...,
        q85: builtins.float = ...,
        q90: builtins.float = ...,
        q95: builtins.float = ...,
        q98: builtins.float = ...,
        q99: builtins.float = ...,
        q100: builtins.float = ...,
        http_codes: collections.abc.Iterable[global___Trail.Codes] | None = ...,
        net_codes: collections.abc.Iterable[global___Trail.Codes] | None = ...,
        time_intervals: collections.abc.Iterable[global___Trail.Intervals] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["case_id", b"case_id", "connect_time", b"connect_time", "expect", b"expect", "http_codes", b"http_codes", "input", b"input", "latency", b"latency", "net_codes", b"net_codes", "output", b"output", "overall", b"overall", "q100", b"q100", "q50", b"q50", "q75", b"q75", "q80", b"q80", "q85", b"q85", "q90", b"q90", "q95", b"q95", "q98", b"q98", "q99", b"q99", "receive_time", b"receive_time", "reqps", b"reqps", "resps", b"resps", "send_time", b"send_time", "threads", b"threads", "time", b"time", "time_intervals", b"time_intervals"]) -> None: ...

global___Trail = Trail

@typing.final
class CreateTrailResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TRAIL_ID_FIELD_NUMBER: builtins.int
    CODE_FIELD_NUMBER: builtins.int
    trail_id: builtins.str
    code: builtins.int
    def __init__(
        self,
        *,
        trail_id: builtins.str = ...,
        code: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["code", b"code", "trail_id", b"trail_id"]) -> None: ...

global___CreateTrailResponse = CreateTrailResponse
