"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.wrappers_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class PostgresqlHostConfig16_1C(google.protobuf.message.Message):
    """Options and structure of `PostgresqlConfig` reflects PostgreSQL configuration file
    parameters which detailed description is available in
    [PostgreSQL documentation](https://www.postgresql.org/docs/11/runtime-config.html).
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _BackslashQuote:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _BackslashQuoteEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[PostgresqlHostConfig16_1C._BackslashQuote.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        BACKSLASH_QUOTE_UNSPECIFIED: PostgresqlHostConfig16_1C._BackslashQuote.ValueType  # 0
        BACKSLASH_QUOTE: PostgresqlHostConfig16_1C._BackslashQuote.ValueType  # 1
        BACKSLASH_QUOTE_ON: PostgresqlHostConfig16_1C._BackslashQuote.ValueType  # 2
        BACKSLASH_QUOTE_OFF: PostgresqlHostConfig16_1C._BackslashQuote.ValueType  # 3
        BACKSLASH_QUOTE_SAFE_ENCODING: PostgresqlHostConfig16_1C._BackslashQuote.ValueType  # 4

    class BackslashQuote(_BackslashQuote, metaclass=_BackslashQuoteEnumTypeWrapper): ...
    BACKSLASH_QUOTE_UNSPECIFIED: PostgresqlHostConfig16_1C.BackslashQuote.ValueType  # 0
    BACKSLASH_QUOTE: PostgresqlHostConfig16_1C.BackslashQuote.ValueType  # 1
    BACKSLASH_QUOTE_ON: PostgresqlHostConfig16_1C.BackslashQuote.ValueType  # 2
    BACKSLASH_QUOTE_OFF: PostgresqlHostConfig16_1C.BackslashQuote.ValueType  # 3
    BACKSLASH_QUOTE_SAFE_ENCODING: PostgresqlHostConfig16_1C.BackslashQuote.ValueType  # 4

    class _ByteaOutput:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _ByteaOutputEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[PostgresqlHostConfig16_1C._ByteaOutput.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        BYTEA_OUTPUT_UNSPECIFIED: PostgresqlHostConfig16_1C._ByteaOutput.ValueType  # 0
        BYTEA_OUTPUT_HEX: PostgresqlHostConfig16_1C._ByteaOutput.ValueType  # 1
        BYTEA_OUTPUT_ESCAPED: PostgresqlHostConfig16_1C._ByteaOutput.ValueType  # 2

    class ByteaOutput(_ByteaOutput, metaclass=_ByteaOutputEnumTypeWrapper): ...
    BYTEA_OUTPUT_UNSPECIFIED: PostgresqlHostConfig16_1C.ByteaOutput.ValueType  # 0
    BYTEA_OUTPUT_HEX: PostgresqlHostConfig16_1C.ByteaOutput.ValueType  # 1
    BYTEA_OUTPUT_ESCAPED: PostgresqlHostConfig16_1C.ByteaOutput.ValueType  # 2

    class _ConstraintExclusion:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _ConstraintExclusionEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[PostgresqlHostConfig16_1C._ConstraintExclusion.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        CONSTRAINT_EXCLUSION_UNSPECIFIED: PostgresqlHostConfig16_1C._ConstraintExclusion.ValueType  # 0
        CONSTRAINT_EXCLUSION_ON: PostgresqlHostConfig16_1C._ConstraintExclusion.ValueType  # 1
        CONSTRAINT_EXCLUSION_OFF: PostgresqlHostConfig16_1C._ConstraintExclusion.ValueType  # 2
        CONSTRAINT_EXCLUSION_PARTITION: PostgresqlHostConfig16_1C._ConstraintExclusion.ValueType  # 3

    class ConstraintExclusion(_ConstraintExclusion, metaclass=_ConstraintExclusionEnumTypeWrapper): ...
    CONSTRAINT_EXCLUSION_UNSPECIFIED: PostgresqlHostConfig16_1C.ConstraintExclusion.ValueType  # 0
    CONSTRAINT_EXCLUSION_ON: PostgresqlHostConfig16_1C.ConstraintExclusion.ValueType  # 1
    CONSTRAINT_EXCLUSION_OFF: PostgresqlHostConfig16_1C.ConstraintExclusion.ValueType  # 2
    CONSTRAINT_EXCLUSION_PARTITION: PostgresqlHostConfig16_1C.ConstraintExclusion.ValueType  # 3

    class _DebugParallelQuery:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _DebugParallelQueryEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[PostgresqlHostConfig16_1C._DebugParallelQuery.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        DEBUG_PARALLEL_QUERY_UNSPECIFIED: PostgresqlHostConfig16_1C._DebugParallelQuery.ValueType  # 0
        DEBUG_PARALLEL_QUERY_ON: PostgresqlHostConfig16_1C._DebugParallelQuery.ValueType  # 1
        DEBUG_PARALLEL_QUERY_OFF: PostgresqlHostConfig16_1C._DebugParallelQuery.ValueType  # 2
        DEBUG_PARALLEL_QUERY_REGRESS: PostgresqlHostConfig16_1C._DebugParallelQuery.ValueType  # 3

    class DebugParallelQuery(_DebugParallelQuery, metaclass=_DebugParallelQueryEnumTypeWrapper): ...
    DEBUG_PARALLEL_QUERY_UNSPECIFIED: PostgresqlHostConfig16_1C.DebugParallelQuery.ValueType  # 0
    DEBUG_PARALLEL_QUERY_ON: PostgresqlHostConfig16_1C.DebugParallelQuery.ValueType  # 1
    DEBUG_PARALLEL_QUERY_OFF: PostgresqlHostConfig16_1C.DebugParallelQuery.ValueType  # 2
    DEBUG_PARALLEL_QUERY_REGRESS: PostgresqlHostConfig16_1C.DebugParallelQuery.ValueType  # 3

    class _ForceParallelMode:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _ForceParallelModeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[PostgresqlHostConfig16_1C._ForceParallelMode.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        FORCE_PARALLEL_MODE_UNSPECIFIED: PostgresqlHostConfig16_1C._ForceParallelMode.ValueType  # 0
        FORCE_PARALLEL_MODE_ON: PostgresqlHostConfig16_1C._ForceParallelMode.ValueType  # 1
        FORCE_PARALLEL_MODE_OFF: PostgresqlHostConfig16_1C._ForceParallelMode.ValueType  # 2
        FORCE_PARALLEL_MODE_REGRESS: PostgresqlHostConfig16_1C._ForceParallelMode.ValueType  # 3

    class ForceParallelMode(_ForceParallelMode, metaclass=_ForceParallelModeEnumTypeWrapper): ...
    FORCE_PARALLEL_MODE_UNSPECIFIED: PostgresqlHostConfig16_1C.ForceParallelMode.ValueType  # 0
    FORCE_PARALLEL_MODE_ON: PostgresqlHostConfig16_1C.ForceParallelMode.ValueType  # 1
    FORCE_PARALLEL_MODE_OFF: PostgresqlHostConfig16_1C.ForceParallelMode.ValueType  # 2
    FORCE_PARALLEL_MODE_REGRESS: PostgresqlHostConfig16_1C.ForceParallelMode.ValueType  # 3

    class _LogErrorVerbosity:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _LogErrorVerbosityEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[PostgresqlHostConfig16_1C._LogErrorVerbosity.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        LOG_ERROR_VERBOSITY_UNSPECIFIED: PostgresqlHostConfig16_1C._LogErrorVerbosity.ValueType  # 0
        LOG_ERROR_VERBOSITY_TERSE: PostgresqlHostConfig16_1C._LogErrorVerbosity.ValueType  # 1
        LOG_ERROR_VERBOSITY_DEFAULT: PostgresqlHostConfig16_1C._LogErrorVerbosity.ValueType  # 2
        LOG_ERROR_VERBOSITY_VERBOSE: PostgresqlHostConfig16_1C._LogErrorVerbosity.ValueType  # 3

    class LogErrorVerbosity(_LogErrorVerbosity, metaclass=_LogErrorVerbosityEnumTypeWrapper): ...
    LOG_ERROR_VERBOSITY_UNSPECIFIED: PostgresqlHostConfig16_1C.LogErrorVerbosity.ValueType  # 0
    LOG_ERROR_VERBOSITY_TERSE: PostgresqlHostConfig16_1C.LogErrorVerbosity.ValueType  # 1
    LOG_ERROR_VERBOSITY_DEFAULT: PostgresqlHostConfig16_1C.LogErrorVerbosity.ValueType  # 2
    LOG_ERROR_VERBOSITY_VERBOSE: PostgresqlHostConfig16_1C.LogErrorVerbosity.ValueType  # 3

    class _LogLevel:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _LogLevelEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[PostgresqlHostConfig16_1C._LogLevel.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        LOG_LEVEL_UNSPECIFIED: PostgresqlHostConfig16_1C._LogLevel.ValueType  # 0
        LOG_LEVEL_DEBUG5: PostgresqlHostConfig16_1C._LogLevel.ValueType  # 1
        LOG_LEVEL_DEBUG4: PostgresqlHostConfig16_1C._LogLevel.ValueType  # 2
        LOG_LEVEL_DEBUG3: PostgresqlHostConfig16_1C._LogLevel.ValueType  # 3
        LOG_LEVEL_DEBUG2: PostgresqlHostConfig16_1C._LogLevel.ValueType  # 4
        LOG_LEVEL_DEBUG1: PostgresqlHostConfig16_1C._LogLevel.ValueType  # 5
        LOG_LEVEL_INFO: PostgresqlHostConfig16_1C._LogLevel.ValueType  # 12
        LOG_LEVEL_LOG: PostgresqlHostConfig16_1C._LogLevel.ValueType  # 6
        LOG_LEVEL_NOTICE: PostgresqlHostConfig16_1C._LogLevel.ValueType  # 7
        LOG_LEVEL_WARNING: PostgresqlHostConfig16_1C._LogLevel.ValueType  # 8
        LOG_LEVEL_ERROR: PostgresqlHostConfig16_1C._LogLevel.ValueType  # 9
        LOG_LEVEL_FATAL: PostgresqlHostConfig16_1C._LogLevel.ValueType  # 10
        LOG_LEVEL_PANIC: PostgresqlHostConfig16_1C._LogLevel.ValueType  # 11

    class LogLevel(_LogLevel, metaclass=_LogLevelEnumTypeWrapper): ...
    LOG_LEVEL_UNSPECIFIED: PostgresqlHostConfig16_1C.LogLevel.ValueType  # 0
    LOG_LEVEL_DEBUG5: PostgresqlHostConfig16_1C.LogLevel.ValueType  # 1
    LOG_LEVEL_DEBUG4: PostgresqlHostConfig16_1C.LogLevel.ValueType  # 2
    LOG_LEVEL_DEBUG3: PostgresqlHostConfig16_1C.LogLevel.ValueType  # 3
    LOG_LEVEL_DEBUG2: PostgresqlHostConfig16_1C.LogLevel.ValueType  # 4
    LOG_LEVEL_DEBUG1: PostgresqlHostConfig16_1C.LogLevel.ValueType  # 5
    LOG_LEVEL_INFO: PostgresqlHostConfig16_1C.LogLevel.ValueType  # 12
    LOG_LEVEL_LOG: PostgresqlHostConfig16_1C.LogLevel.ValueType  # 6
    LOG_LEVEL_NOTICE: PostgresqlHostConfig16_1C.LogLevel.ValueType  # 7
    LOG_LEVEL_WARNING: PostgresqlHostConfig16_1C.LogLevel.ValueType  # 8
    LOG_LEVEL_ERROR: PostgresqlHostConfig16_1C.LogLevel.ValueType  # 9
    LOG_LEVEL_FATAL: PostgresqlHostConfig16_1C.LogLevel.ValueType  # 10
    LOG_LEVEL_PANIC: PostgresqlHostConfig16_1C.LogLevel.ValueType  # 11

    class _LogStatement:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _LogStatementEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[PostgresqlHostConfig16_1C._LogStatement.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        LOG_STATEMENT_UNSPECIFIED: PostgresqlHostConfig16_1C._LogStatement.ValueType  # 0
        LOG_STATEMENT_NONE: PostgresqlHostConfig16_1C._LogStatement.ValueType  # 1
        LOG_STATEMENT_DDL: PostgresqlHostConfig16_1C._LogStatement.ValueType  # 2
        LOG_STATEMENT_MOD: PostgresqlHostConfig16_1C._LogStatement.ValueType  # 3
        LOG_STATEMENT_ALL: PostgresqlHostConfig16_1C._LogStatement.ValueType  # 4

    class LogStatement(_LogStatement, metaclass=_LogStatementEnumTypeWrapper): ...
    LOG_STATEMENT_UNSPECIFIED: PostgresqlHostConfig16_1C.LogStatement.ValueType  # 0
    LOG_STATEMENT_NONE: PostgresqlHostConfig16_1C.LogStatement.ValueType  # 1
    LOG_STATEMENT_DDL: PostgresqlHostConfig16_1C.LogStatement.ValueType  # 2
    LOG_STATEMENT_MOD: PostgresqlHostConfig16_1C.LogStatement.ValueType  # 3
    LOG_STATEMENT_ALL: PostgresqlHostConfig16_1C.LogStatement.ValueType  # 4

    class _TransactionIsolation:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _TransactionIsolationEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[PostgresqlHostConfig16_1C._TransactionIsolation.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        TRANSACTION_ISOLATION_UNSPECIFIED: PostgresqlHostConfig16_1C._TransactionIsolation.ValueType  # 0
        TRANSACTION_ISOLATION_READ_UNCOMMITTED: PostgresqlHostConfig16_1C._TransactionIsolation.ValueType  # 1
        TRANSACTION_ISOLATION_READ_COMMITTED: PostgresqlHostConfig16_1C._TransactionIsolation.ValueType  # 2
        TRANSACTION_ISOLATION_REPEATABLE_READ: PostgresqlHostConfig16_1C._TransactionIsolation.ValueType  # 3
        TRANSACTION_ISOLATION_SERIALIZABLE: PostgresqlHostConfig16_1C._TransactionIsolation.ValueType  # 4

    class TransactionIsolation(_TransactionIsolation, metaclass=_TransactionIsolationEnumTypeWrapper): ...
    TRANSACTION_ISOLATION_UNSPECIFIED: PostgresqlHostConfig16_1C.TransactionIsolation.ValueType  # 0
    TRANSACTION_ISOLATION_READ_UNCOMMITTED: PostgresqlHostConfig16_1C.TransactionIsolation.ValueType  # 1
    TRANSACTION_ISOLATION_READ_COMMITTED: PostgresqlHostConfig16_1C.TransactionIsolation.ValueType  # 2
    TRANSACTION_ISOLATION_REPEATABLE_READ: PostgresqlHostConfig16_1C.TransactionIsolation.ValueType  # 3
    TRANSACTION_ISOLATION_SERIALIZABLE: PostgresqlHostConfig16_1C.TransactionIsolation.ValueType  # 4

    class _XmlBinary:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _XmlBinaryEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[PostgresqlHostConfig16_1C._XmlBinary.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        XML_BINARY_UNSPECIFIED: PostgresqlHostConfig16_1C._XmlBinary.ValueType  # 0
        XML_BINARY_BASE64: PostgresqlHostConfig16_1C._XmlBinary.ValueType  # 1
        XML_BINARY_HEX: PostgresqlHostConfig16_1C._XmlBinary.ValueType  # 2

    class XmlBinary(_XmlBinary, metaclass=_XmlBinaryEnumTypeWrapper): ...
    XML_BINARY_UNSPECIFIED: PostgresqlHostConfig16_1C.XmlBinary.ValueType  # 0
    XML_BINARY_BASE64: PostgresqlHostConfig16_1C.XmlBinary.ValueType  # 1
    XML_BINARY_HEX: PostgresqlHostConfig16_1C.XmlBinary.ValueType  # 2

    class _XmlOption:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _XmlOptionEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[PostgresqlHostConfig16_1C._XmlOption.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        XML_OPTION_UNSPECIFIED: PostgresqlHostConfig16_1C._XmlOption.ValueType  # 0
        XML_OPTION_DOCUMENT: PostgresqlHostConfig16_1C._XmlOption.ValueType  # 1
        XML_OPTION_CONTENT: PostgresqlHostConfig16_1C._XmlOption.ValueType  # 2

    class XmlOption(_XmlOption, metaclass=_XmlOptionEnumTypeWrapper): ...
    XML_OPTION_UNSPECIFIED: PostgresqlHostConfig16_1C.XmlOption.ValueType  # 0
    XML_OPTION_DOCUMENT: PostgresqlHostConfig16_1C.XmlOption.ValueType  # 1
    XML_OPTION_CONTENT: PostgresqlHostConfig16_1C.XmlOption.ValueType  # 2

    RECOVERY_MIN_APPLY_DELAY_FIELD_NUMBER: builtins.int
    SHARED_BUFFERS_FIELD_NUMBER: builtins.int
    TEMP_BUFFERS_FIELD_NUMBER: builtins.int
    WORK_MEM_FIELD_NUMBER: builtins.int
    TEMP_FILE_LIMIT_FIELD_NUMBER: builtins.int
    BACKEND_FLUSH_AFTER_FIELD_NUMBER: builtins.int
    OLD_SNAPSHOT_THRESHOLD_FIELD_NUMBER: builtins.int
    MAX_STANDBY_STREAMING_DELAY_FIELD_NUMBER: builtins.int
    CONSTRAINT_EXCLUSION_FIELD_NUMBER: builtins.int
    CURSOR_TUPLE_FRACTION_FIELD_NUMBER: builtins.int
    FROM_COLLAPSE_LIMIT_FIELD_NUMBER: builtins.int
    JOIN_COLLAPSE_LIMIT_FIELD_NUMBER: builtins.int
    DEBUG_PARALLEL_QUERY_FIELD_NUMBER: builtins.int
    CLIENT_MIN_MESSAGES_FIELD_NUMBER: builtins.int
    LOG_MIN_MESSAGES_FIELD_NUMBER: builtins.int
    LOG_MIN_ERROR_STATEMENT_FIELD_NUMBER: builtins.int
    LOG_MIN_DURATION_STATEMENT_FIELD_NUMBER: builtins.int
    LOG_CHECKPOINTS_FIELD_NUMBER: builtins.int
    LOG_CONNECTIONS_FIELD_NUMBER: builtins.int
    LOG_DISCONNECTIONS_FIELD_NUMBER: builtins.int
    LOG_DURATION_FIELD_NUMBER: builtins.int
    LOG_ERROR_VERBOSITY_FIELD_NUMBER: builtins.int
    LOG_LOCK_WAITS_FIELD_NUMBER: builtins.int
    LOG_STATEMENT_FIELD_NUMBER: builtins.int
    LOG_TEMP_FILES_FIELD_NUMBER: builtins.int
    SEARCH_PATH_FIELD_NUMBER: builtins.int
    ROW_SECURITY_FIELD_NUMBER: builtins.int
    DEFAULT_TRANSACTION_ISOLATION_FIELD_NUMBER: builtins.int
    STATEMENT_TIMEOUT_FIELD_NUMBER: builtins.int
    LOCK_TIMEOUT_FIELD_NUMBER: builtins.int
    IDLE_IN_TRANSACTION_SESSION_TIMEOUT_FIELD_NUMBER: builtins.int
    BYTEA_OUTPUT_FIELD_NUMBER: builtins.int
    XMLBINARY_FIELD_NUMBER: builtins.int
    XMLOPTION_FIELD_NUMBER: builtins.int
    GIN_PENDING_LIST_LIMIT_FIELD_NUMBER: builtins.int
    DEADLOCK_TIMEOUT_FIELD_NUMBER: builtins.int
    MAX_LOCKS_PER_TRANSACTION_FIELD_NUMBER: builtins.int
    MAX_PRED_LOCKS_PER_TRANSACTION_FIELD_NUMBER: builtins.int
    ARRAY_NULLS_FIELD_NUMBER: builtins.int
    BACKSLASH_QUOTE_FIELD_NUMBER: builtins.int
    DEFAULT_WITH_OIDS_FIELD_NUMBER: builtins.int
    ESCAPE_STRING_WARNING_FIELD_NUMBER: builtins.int
    LO_COMPAT_PRIVILEGES_FIELD_NUMBER: builtins.int
    QUOTE_ALL_IDENTIFIERS_FIELD_NUMBER: builtins.int
    STANDARD_CONFORMING_STRINGS_FIELD_NUMBER: builtins.int
    SYNCHRONIZE_SEQSCANS_FIELD_NUMBER: builtins.int
    TRANSFORM_NULL_EQUALS_FIELD_NUMBER: builtins.int
    EXIT_ON_ERROR_FIELD_NUMBER: builtins.int
    SEQ_PAGE_COST_FIELD_NUMBER: builtins.int
    RANDOM_PAGE_COST_FIELD_NUMBER: builtins.int
    ENABLE_BITMAPSCAN_FIELD_NUMBER: builtins.int
    ENABLE_HASHAGG_FIELD_NUMBER: builtins.int
    ENABLE_HASHJOIN_FIELD_NUMBER: builtins.int
    ENABLE_INDEXSCAN_FIELD_NUMBER: builtins.int
    ENABLE_INDEXONLYSCAN_FIELD_NUMBER: builtins.int
    ENABLE_MATERIAL_FIELD_NUMBER: builtins.int
    ENABLE_MERGEJOIN_FIELD_NUMBER: builtins.int
    ENABLE_NESTLOOP_FIELD_NUMBER: builtins.int
    ENABLE_SEQSCAN_FIELD_NUMBER: builtins.int
    ENABLE_SORT_FIELD_NUMBER: builtins.int
    ENABLE_TIDSCAN_FIELD_NUMBER: builtins.int
    MAX_PARALLEL_WORKERS_FIELD_NUMBER: builtins.int
    MAX_PARALLEL_WORKERS_PER_GATHER_FIELD_NUMBER: builtins.int
    TIMEZONE_FIELD_NUMBER: builtins.int
    EFFECTIVE_IO_CONCURRENCY_FIELD_NUMBER: builtins.int
    EFFECTIVE_CACHE_SIZE_FIELD_NUMBER: builtins.int
    constraint_exclusion: global___PostgresqlHostConfig16_1C.ConstraintExclusion.ValueType
    debug_parallel_query: global___PostgresqlHostConfig16_1C.DebugParallelQuery.ValueType
    client_min_messages: global___PostgresqlHostConfig16_1C.LogLevel.ValueType
    log_min_messages: global___PostgresqlHostConfig16_1C.LogLevel.ValueType
    log_min_error_statement: global___PostgresqlHostConfig16_1C.LogLevel.ValueType
    log_error_verbosity: global___PostgresqlHostConfig16_1C.LogErrorVerbosity.ValueType
    log_statement: global___PostgresqlHostConfig16_1C.LogStatement.ValueType
    search_path: builtins.str
    default_transaction_isolation: global___PostgresqlHostConfig16_1C.TransactionIsolation.ValueType
    bytea_output: global___PostgresqlHostConfig16_1C.ByteaOutput.ValueType
    xmlbinary: global___PostgresqlHostConfig16_1C.XmlBinary.ValueType
    xmloption: global___PostgresqlHostConfig16_1C.XmlOption.ValueType
    backslash_quote: global___PostgresqlHostConfig16_1C.BackslashQuote.ValueType
    timezone: builtins.str
    @property
    def recovery_min_apply_delay(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """in milliseconds."""

    @property
    def shared_buffers(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """in bytes."""

    @property
    def temp_buffers(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """in bytes."""

    @property
    def work_mem(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """in bytes."""

    @property
    def temp_file_limit(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """in bytes."""

    @property
    def backend_flush_after(self) -> google.protobuf.wrappers_pb2.Int64Value: ...
    @property
    def old_snapshot_threshold(self) -> google.protobuf.wrappers_pb2.Int64Value: ...
    @property
    def max_standby_streaming_delay(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """in milliseconds."""

    @property
    def cursor_tuple_fraction(self) -> google.protobuf.wrappers_pb2.DoubleValue: ...
    @property
    def from_collapse_limit(self) -> google.protobuf.wrappers_pb2.Int64Value: ...
    @property
    def join_collapse_limit(self) -> google.protobuf.wrappers_pb2.Int64Value: ...
    @property
    def log_min_duration_statement(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """in milliseconds."""

    @property
    def log_checkpoints(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def log_connections(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def log_disconnections(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def log_duration(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def log_lock_waits(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def log_temp_files(self) -> google.protobuf.wrappers_pb2.Int64Value: ...
    @property
    def row_security(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def statement_timeout(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """in milliseconds."""

    @property
    def lock_timeout(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """in milliseconds."""

    @property
    def idle_in_transaction_session_timeout(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """in milliseconds."""

    @property
    def gin_pending_list_limit(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """in bytes."""

    @property
    def deadlock_timeout(self) -> google.protobuf.wrappers_pb2.Int64Value:
        """in milliseconds."""

    @property
    def max_locks_per_transaction(self) -> google.protobuf.wrappers_pb2.Int64Value: ...
    @property
    def max_pred_locks_per_transaction(self) -> google.protobuf.wrappers_pb2.Int64Value: ...
    @property
    def array_nulls(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def default_with_oids(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def escape_string_warning(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def lo_compat_privileges(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def quote_all_identifiers(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def standard_conforming_strings(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def synchronize_seqscans(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def transform_null_equals(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def exit_on_error(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def seq_page_cost(self) -> google.protobuf.wrappers_pb2.DoubleValue: ...
    @property
    def random_page_cost(self) -> google.protobuf.wrappers_pb2.DoubleValue: ...
    @property
    def enable_bitmapscan(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def enable_hashagg(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def enable_hashjoin(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def enable_indexscan(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def enable_indexonlyscan(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def enable_material(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def enable_mergejoin(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def enable_nestloop(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def enable_seqscan(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def enable_sort(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def enable_tidscan(self) -> google.protobuf.wrappers_pb2.BoolValue: ...
    @property
    def max_parallel_workers(self) -> google.protobuf.wrappers_pb2.Int64Value: ...
    @property
    def max_parallel_workers_per_gather(self) -> google.protobuf.wrappers_pb2.Int64Value: ...
    @property
    def effective_io_concurrency(self) -> google.protobuf.wrappers_pb2.Int64Value: ...
    @property
    def effective_cache_size(self) -> google.protobuf.wrappers_pb2.Int64Value: ...
    def __init__(
        self,
        *,
        recovery_min_apply_delay: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        shared_buffers: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        temp_buffers: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        work_mem: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        temp_file_limit: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        backend_flush_after: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        old_snapshot_threshold: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        max_standby_streaming_delay: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        constraint_exclusion: global___PostgresqlHostConfig16_1C.ConstraintExclusion.ValueType = ...,
        cursor_tuple_fraction: google.protobuf.wrappers_pb2.DoubleValue | None = ...,
        from_collapse_limit: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        join_collapse_limit: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        debug_parallel_query: global___PostgresqlHostConfig16_1C.DebugParallelQuery.ValueType = ...,
        client_min_messages: global___PostgresqlHostConfig16_1C.LogLevel.ValueType = ...,
        log_min_messages: global___PostgresqlHostConfig16_1C.LogLevel.ValueType = ...,
        log_min_error_statement: global___PostgresqlHostConfig16_1C.LogLevel.ValueType = ...,
        log_min_duration_statement: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        log_checkpoints: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        log_connections: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        log_disconnections: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        log_duration: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        log_error_verbosity: global___PostgresqlHostConfig16_1C.LogErrorVerbosity.ValueType = ...,
        log_lock_waits: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        log_statement: global___PostgresqlHostConfig16_1C.LogStatement.ValueType = ...,
        log_temp_files: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        search_path: builtins.str = ...,
        row_security: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        default_transaction_isolation: global___PostgresqlHostConfig16_1C.TransactionIsolation.ValueType = ...,
        statement_timeout: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        lock_timeout: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        idle_in_transaction_session_timeout: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        bytea_output: global___PostgresqlHostConfig16_1C.ByteaOutput.ValueType = ...,
        xmlbinary: global___PostgresqlHostConfig16_1C.XmlBinary.ValueType = ...,
        xmloption: global___PostgresqlHostConfig16_1C.XmlOption.ValueType = ...,
        gin_pending_list_limit: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        deadlock_timeout: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        max_locks_per_transaction: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        max_pred_locks_per_transaction: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        array_nulls: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        backslash_quote: global___PostgresqlHostConfig16_1C.BackslashQuote.ValueType = ...,
        default_with_oids: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        escape_string_warning: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        lo_compat_privileges: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        quote_all_identifiers: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        standard_conforming_strings: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        synchronize_seqscans: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        transform_null_equals: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        exit_on_error: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        seq_page_cost: google.protobuf.wrappers_pb2.DoubleValue | None = ...,
        random_page_cost: google.protobuf.wrappers_pb2.DoubleValue | None = ...,
        enable_bitmapscan: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        enable_hashagg: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        enable_hashjoin: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        enable_indexscan: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        enable_indexonlyscan: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        enable_material: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        enable_mergejoin: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        enable_nestloop: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        enable_seqscan: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        enable_sort: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        enable_tidscan: google.protobuf.wrappers_pb2.BoolValue | None = ...,
        max_parallel_workers: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        max_parallel_workers_per_gather: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        timezone: builtins.str = ...,
        effective_io_concurrency: google.protobuf.wrappers_pb2.Int64Value | None = ...,
        effective_cache_size: google.protobuf.wrappers_pb2.Int64Value | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["array_nulls", b"array_nulls", "backend_flush_after", b"backend_flush_after", "cursor_tuple_fraction", b"cursor_tuple_fraction", "deadlock_timeout", b"deadlock_timeout", "default_with_oids", b"default_with_oids", "effective_cache_size", b"effective_cache_size", "effective_io_concurrency", b"effective_io_concurrency", "enable_bitmapscan", b"enable_bitmapscan", "enable_hashagg", b"enable_hashagg", "enable_hashjoin", b"enable_hashjoin", "enable_indexonlyscan", b"enable_indexonlyscan", "enable_indexscan", b"enable_indexscan", "enable_material", b"enable_material", "enable_mergejoin", b"enable_mergejoin", "enable_nestloop", b"enable_nestloop", "enable_seqscan", b"enable_seqscan", "enable_sort", b"enable_sort", "enable_tidscan", b"enable_tidscan", "escape_string_warning", b"escape_string_warning", "exit_on_error", b"exit_on_error", "from_collapse_limit", b"from_collapse_limit", "gin_pending_list_limit", b"gin_pending_list_limit", "idle_in_transaction_session_timeout", b"idle_in_transaction_session_timeout", "join_collapse_limit", b"join_collapse_limit", "lo_compat_privileges", b"lo_compat_privileges", "lock_timeout", b"lock_timeout", "log_checkpoints", b"log_checkpoints", "log_connections", b"log_connections", "log_disconnections", b"log_disconnections", "log_duration", b"log_duration", "log_lock_waits", b"log_lock_waits", "log_min_duration_statement", b"log_min_duration_statement", "log_temp_files", b"log_temp_files", "max_locks_per_transaction", b"max_locks_per_transaction", "max_parallel_workers", b"max_parallel_workers", "max_parallel_workers_per_gather", b"max_parallel_workers_per_gather", "max_pred_locks_per_transaction", b"max_pred_locks_per_transaction", "max_standby_streaming_delay", b"max_standby_streaming_delay", "old_snapshot_threshold", b"old_snapshot_threshold", "quote_all_identifiers", b"quote_all_identifiers", "random_page_cost", b"random_page_cost", "recovery_min_apply_delay", b"recovery_min_apply_delay", "row_security", b"row_security", "seq_page_cost", b"seq_page_cost", "shared_buffers", b"shared_buffers", "standard_conforming_strings", b"standard_conforming_strings", "statement_timeout", b"statement_timeout", "synchronize_seqscans", b"synchronize_seqscans", "temp_buffers", b"temp_buffers", "temp_file_limit", b"temp_file_limit", "transform_null_equals", b"transform_null_equals", "work_mem", b"work_mem"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["array_nulls", b"array_nulls", "backend_flush_after", b"backend_flush_after", "backslash_quote", b"backslash_quote", "bytea_output", b"bytea_output", "client_min_messages", b"client_min_messages", "constraint_exclusion", b"constraint_exclusion", "cursor_tuple_fraction", b"cursor_tuple_fraction", "deadlock_timeout", b"deadlock_timeout", "debug_parallel_query", b"debug_parallel_query", "default_transaction_isolation", b"default_transaction_isolation", "default_with_oids", b"default_with_oids", "effective_cache_size", b"effective_cache_size", "effective_io_concurrency", b"effective_io_concurrency", "enable_bitmapscan", b"enable_bitmapscan", "enable_hashagg", b"enable_hashagg", "enable_hashjoin", b"enable_hashjoin", "enable_indexonlyscan", b"enable_indexonlyscan", "enable_indexscan", b"enable_indexscan", "enable_material", b"enable_material", "enable_mergejoin", b"enable_mergejoin", "enable_nestloop", b"enable_nestloop", "enable_seqscan", b"enable_seqscan", "enable_sort", b"enable_sort", "enable_tidscan", b"enable_tidscan", "escape_string_warning", b"escape_string_warning", "exit_on_error", b"exit_on_error", "from_collapse_limit", b"from_collapse_limit", "gin_pending_list_limit", b"gin_pending_list_limit", "idle_in_transaction_session_timeout", b"idle_in_transaction_session_timeout", "join_collapse_limit", b"join_collapse_limit", "lo_compat_privileges", b"lo_compat_privileges", "lock_timeout", b"lock_timeout", "log_checkpoints", b"log_checkpoints", "log_connections", b"log_connections", "log_disconnections", b"log_disconnections", "log_duration", b"log_duration", "log_error_verbosity", b"log_error_verbosity", "log_lock_waits", b"log_lock_waits", "log_min_duration_statement", b"log_min_duration_statement", "log_min_error_statement", b"log_min_error_statement", "log_min_messages", b"log_min_messages", "log_statement", b"log_statement", "log_temp_files", b"log_temp_files", "max_locks_per_transaction", b"max_locks_per_transaction", "max_parallel_workers", b"max_parallel_workers", "max_parallel_workers_per_gather", b"max_parallel_workers_per_gather", "max_pred_locks_per_transaction", b"max_pred_locks_per_transaction", "max_standby_streaming_delay", b"max_standby_streaming_delay", "old_snapshot_threshold", b"old_snapshot_threshold", "quote_all_identifiers", b"quote_all_identifiers", "random_page_cost", b"random_page_cost", "recovery_min_apply_delay", b"recovery_min_apply_delay", "row_security", b"row_security", "search_path", b"search_path", "seq_page_cost", b"seq_page_cost", "shared_buffers", b"shared_buffers", "standard_conforming_strings", b"standard_conforming_strings", "statement_timeout", b"statement_timeout", "synchronize_seqscans", b"synchronize_seqscans", "temp_buffers", b"temp_buffers", "temp_file_limit", b"temp_file_limit", "timezone", b"timezone", "transform_null_equals", b"transform_null_equals", "work_mem", b"work_mem", "xmlbinary", b"xmlbinary", "xmloption", b"xmloption"]) -> None: ...

global___PostgresqlHostConfig16_1C = PostgresqlHostConfig16_1C
