"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.message
import google.protobuf.wrappers_pb2
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class SQLServerConfig2017std(google.protobuf.message.Message):
    """SQL Server 2017 Standard edition supported configuration options are listed here.

    Detailed description for each set of options is available in [SQL Server documentation](https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/server-configuration-options-sql-server?view=sql-server-2017).

    Any options that are not listed here are not supported.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MAX_DEGREE_OF_PARALLELISM_FIELD_NUMBER: builtins.int
    COST_THRESHOLD_FOR_PARALLELISM_FIELD_NUMBER: builtins.int
    AUDIT_LEVEL_FIELD_NUMBER: builtins.int
    FILL_FACTOR_PERCENT_FIELD_NUMBER: builtins.int
    OPTIMIZE_FOR_AD_HOC_WORKLOADS_FIELD_NUMBER: builtins.int
    @property
    def max_degree_of_parallelism(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """Limits the number of processors to use in parallel plan execution per task.

        See in-depth description in [SQL Server documentation](https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/configure-the-max-degree-of-parallelism-server-configuration-option?view=sql-server-2017).
        """

    @property
    def cost_threshold_for_parallelism(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """Specifies the threshold at which SQL Server creates and runs parallel plans for queries.

        SQL Server creates and runs a parallel plan for a query only when the estimated cost to run a serial plan for the same query is higher than the value of the option.

        See in-depth description in [SQL Server documentation](https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/configure-the-cost-threshold-for-parallelism-server-configuration-option?view=sql-server-2017).
        """

    @property
    def audit_level(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """Describes how to configure login auditing to monitor SQL Server Database Engine login activity.

        Possible values:
        * 0 - do not log login attempts;
        * 1 - log only failed login attempts;
        * 2 - log only successful login attempts (not recommended);
        * 3 - log all login attempts (not recommended).

        See in-depth description in [SQL Server documentation](https://docs.microsoft.com/en-us/sql/ssms/configure-login-auditing-sql-server-management-studio?view=sql-server-2017).
        """

    @property
    def fill_factor_percent(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """Manages the fill factor server configuration option.

        When an index is created or rebuilt, the fill factor determines the percentage of space on each index leaf-level page to be filled with data, reserving the rest as free space for future growth.

        Values 0 and 100 mean full page usage (no space reserved).

        See in-depth description in [SQL Server documentation](https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/configure-the-fill-factor-server-configuration-option?view=sql-server-2017).
        """

    @property
    def optimize_for_ad_hoc_workloads(self) -> google.protobuf.wrappers_pb2.BoolValue:
        """Determines whether plans should be cached only after second execution.

        Allows to avoid SQL cache bloat because of single-use plans.

        See in-depth description in [SQL Server documentation](https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/optimize-for-ad-hoc-workloads-server-configuration-option?view=sql-server-2017).
        """

    def __init__(
        self,
        *,
        max_degree_of_parallelism: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        cost_threshold_for_parallelism: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        audit_level: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        fill_factor_percent: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        optimize_for_ad_hoc_workloads: google.protobuf.wrappers_pb2.BoolValue | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["audit_level", b"audit_level", "cost_threshold_for_parallelism", b"cost_threshold_for_parallelism", "fill_factor_percent", b"fill_factor_percent", "max_degree_of_parallelism", b"max_degree_of_parallelism", "optimize_for_ad_hoc_workloads", b"optimize_for_ad_hoc_workloads"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["audit_level", b"audit_level", "cost_threshold_for_parallelism", b"cost_threshold_for_parallelism", "fill_factor_percent", b"fill_factor_percent", "max_degree_of_parallelism", b"max_degree_of_parallelism", "optimize_for_ad_hoc_workloads", b"optimize_for_ad_hoc_workloads"]) -> None: ...

global___SQLServerConfig2017std = SQLServerConfig2017std

@typing.final
class SQLServerConfigSet2017std(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EFFECTIVE_CONFIG_FIELD_NUMBER: builtins.int
    USER_CONFIG_FIELD_NUMBER: builtins.int
    DEFAULT_CONFIG_FIELD_NUMBER: builtins.int
    @property
    def effective_config(self) -> global___SQLServerConfig2017std:
        """Effective settings for an SQL Server 2017 cluster (a combination of settings defined in [user_config] and [default_config])."""

    @property
    def user_config(self) -> global___SQLServerConfig2017std:
        """User-defined settings for an SQL Server 2017 cluster."""

    @property
    def default_config(self) -> global___SQLServerConfig2017std:
        """Default configuration for an SQL Server 2017 cluster."""

    def __init__(
        self,
        *,
        effective_config: global___SQLServerConfig2017std | None = ...,
        user_config: global___SQLServerConfig2017std | None = ...,
        default_config: global___SQLServerConfig2017std | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["default_config", b"default_config", "effective_config", b"effective_config", "user_config", b"user_config"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["default_config", b"default_config", "effective_config", b"effective_config", "user_config", b"user_config"]) -> None: ...

global___SQLServerConfigSet2017std = SQLServerConfigSet2017std

@typing.final
class SQLServerConfig2017ent(google.protobuf.message.Message):
    """SQL Server 2017 Enterprise edition supported configuration options are listed here.

    Detailed description for each set of options is available in [SQL Server documentation](https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/server-configuration-options-sql-server?view=sql-server-2017).

    Any options that are not listed here are not supported.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MAX_DEGREE_OF_PARALLELISM_FIELD_NUMBER: builtins.int
    COST_THRESHOLD_FOR_PARALLELISM_FIELD_NUMBER: builtins.int
    AUDIT_LEVEL_FIELD_NUMBER: builtins.int
    FILL_FACTOR_PERCENT_FIELD_NUMBER: builtins.int
    OPTIMIZE_FOR_AD_HOC_WORKLOADS_FIELD_NUMBER: builtins.int
    @property
    def max_degree_of_parallelism(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """Limits the number of processors to use in parallel plan execution per task.

        See in-depth description in [SQL Server documentation](https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/configure-the-max-degree-of-parallelism-server-configuration-option?view=sql-server-2017).
        """

    @property
    def cost_threshold_for_parallelism(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """Specifies the threshold at which SQL Server creates and runs parallel plans for queries.

        SQL Server creates and runs a parallel plan for a query only when the estimated cost to run a serial plan for the same query is higher than the value of the option.

        See in-depth description in [SQL Server documentation](https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/configure-the-cost-threshold-for-parallelism-server-configuration-option?view=sql-server-2017).
        """

    @property
    def audit_level(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """Describes how to configure login auditing to monitor SQL Server Database Engine login activity.

        Possible values:
        * 0 - do not log login attempts;
        * 1 - log only failed login attempts;
        * 2 - log only successful login attempts (not recommended);
        * 3 - log all login attempts (not recommended).

        See in-depth description in [SQL Server documentation](https://docs.microsoft.com/en-us/sql/ssms/configure-login-auditing-sql-server-management-studio?view=sql-server-2017).
        """

    @property
    def fill_factor_percent(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """Manages the fill factor server configuration option.
        When an index is created or rebuilt, the fill factor determines the percentage of space on each index leaf-level page to be filled with data, reserving the rest as free space for future growth.

        Values 0 and 100 mean full page usage (no space reserved).

        See in-depth description in [SQL Server documentation](https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/configure-the-fill-factor-server-configuration-option?view=sql-server-2017).
        """

    @property
    def optimize_for_ad_hoc_workloads(self) -> google.protobuf.wrappers_pb2.BoolValue:
        """Determines whether plans should be cached only after second execution.

        Allows to avoid SQL cache bloat because of single-use plans.

        See in-depth description in [SQL Server documentation](https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/optimize-for-ad-hoc-workloads-server-configuration-option?view=sql-server-2017).
        """

    def __init__(
        self,
        *,
        max_degree_of_parallelism: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        cost_threshold_for_parallelism: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        audit_level: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        fill_factor_percent: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        optimize_for_ad_hoc_workloads: google.protobuf.wrappers_pb2.BoolValue | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["audit_level", b"audit_level", "cost_threshold_for_parallelism", b"cost_threshold_for_parallelism", "fill_factor_percent", b"fill_factor_percent", "max_degree_of_parallelism", b"max_degree_of_parallelism", "optimize_for_ad_hoc_workloads", b"optimize_for_ad_hoc_workloads"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["audit_level", b"audit_level", "cost_threshold_for_parallelism", b"cost_threshold_for_parallelism", "fill_factor_percent", b"fill_factor_percent", "max_degree_of_parallelism", b"max_degree_of_parallelism", "optimize_for_ad_hoc_workloads", b"optimize_for_ad_hoc_workloads"]) -> None: ...

global___SQLServerConfig2017ent = SQLServerConfig2017ent

@typing.final
class SQLServerConfigSet2017ent(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EFFECTIVE_CONFIG_FIELD_NUMBER: builtins.int
    USER_CONFIG_FIELD_NUMBER: builtins.int
    DEFAULT_CONFIG_FIELD_NUMBER: builtins.int
    @property
    def effective_config(self) -> global___SQLServerConfig2017ent:
        """Effective settings for an SQL Server 2017 cluster (a combination of settings defined in [user_config] and [default_config])."""

    @property
    def user_config(self) -> global___SQLServerConfig2017ent:
        """User-defined settings for an SQL Server 2017 cluster."""

    @property
    def default_config(self) -> global___SQLServerConfig2017ent:
        """Default configuration for an SQL Server 2017 cluster."""

    def __init__(
        self,
        *,
        effective_config: global___SQLServerConfig2017ent | None = ...,
        user_config: global___SQLServerConfig2017ent | None = ...,
        default_config: global___SQLServerConfig2017ent | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["default_config", b"default_config", "effective_config", b"effective_config", "user_config", b"user_config"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["default_config", b"default_config", "effective_config", b"effective_config", "user_config", b"user_config"]) -> None: ...

global___SQLServerConfigSet2017ent = SQLServerConfigSet2017ent
