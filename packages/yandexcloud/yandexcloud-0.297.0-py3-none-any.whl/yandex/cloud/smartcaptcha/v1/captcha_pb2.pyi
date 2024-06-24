"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _CaptchaComplexity:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _CaptchaComplexityEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_CaptchaComplexity.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    CAPTCHA_COMPLEXITY_UNSPECIFIED: _CaptchaComplexity.ValueType  # 0
    EASY: _CaptchaComplexity.ValueType  # 1
    """High chance to pass pre-check and easy advanced challenge."""
    MEDIUM: _CaptchaComplexity.ValueType  # 2
    """Medium chance to pass pre-check and normal advanced challenge."""
    HARD: _CaptchaComplexity.ValueType  # 3
    """Little chance to pass pre-check and hard advanced challenge."""
    FORCE_HARD: _CaptchaComplexity.ValueType  # 4
    """Impossible to pass pre-check and hard advanced challenge."""

class CaptchaComplexity(_CaptchaComplexity, metaclass=_CaptchaComplexityEnumTypeWrapper):
    """Captcha's complexity."""

CAPTCHA_COMPLEXITY_UNSPECIFIED: CaptchaComplexity.ValueType  # 0
EASY: CaptchaComplexity.ValueType  # 1
"""High chance to pass pre-check and easy advanced challenge."""
MEDIUM: CaptchaComplexity.ValueType  # 2
"""Medium chance to pass pre-check and normal advanced challenge."""
HARD: CaptchaComplexity.ValueType  # 3
"""Little chance to pass pre-check and hard advanced challenge."""
FORCE_HARD: CaptchaComplexity.ValueType  # 4
"""Impossible to pass pre-check and hard advanced challenge."""
global___CaptchaComplexity = CaptchaComplexity

class _CaptchaPreCheckType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _CaptchaPreCheckTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_CaptchaPreCheckType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    CAPTCHA_PRE_CHECK_TYPE_UNSPECIFIED: _CaptchaPreCheckType.ValueType  # 0
    CHECKBOX: _CaptchaPreCheckType.ValueType  # 1
    """User must click the "I am not a robot" button."""
    SLIDER: _CaptchaPreCheckType.ValueType  # 2
    """User must move the slider from left to right."""

class CaptchaPreCheckType(_CaptchaPreCheckType, metaclass=_CaptchaPreCheckTypeEnumTypeWrapper):
    """Captcha's basic check type, see [Task types / Main task](/docs/smartcaptcha/concepts/tasks#main-task)."""

CAPTCHA_PRE_CHECK_TYPE_UNSPECIFIED: CaptchaPreCheckType.ValueType  # 0
CHECKBOX: CaptchaPreCheckType.ValueType  # 1
"""User must click the "I am not a robot" button."""
SLIDER: CaptchaPreCheckType.ValueType  # 2
"""User must move the slider from left to right."""
global___CaptchaPreCheckType = CaptchaPreCheckType

class _CaptchaChallengeType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _CaptchaChallengeTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_CaptchaChallengeType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    CAPTCHA_CHALLENGE_TYPE_UNSPECIFIED: _CaptchaChallengeType.ValueType  # 0
    IMAGE_TEXT: _CaptchaChallengeType.ValueType  # 1
    """Text recognition: The user has to type a distorted text from the picture into a special field."""
    SILHOUETTES: _CaptchaChallengeType.ValueType  # 2
    """Silhouettes: The user has to mark several icons from the picture in a particular order."""
    KALEIDOSCOPE: _CaptchaChallengeType.ValueType  # 3
    """Kaleidoscope: The user has to build a picture from individual parts by shuffling them using a slider."""

class CaptchaChallengeType(_CaptchaChallengeType, metaclass=_CaptchaChallengeTypeEnumTypeWrapper):
    """Additional task, see [Task types / Additional task](/docs/smartcaptcha/concepts/tasks#additional-task)."""

CAPTCHA_CHALLENGE_TYPE_UNSPECIFIED: CaptchaChallengeType.ValueType  # 0
IMAGE_TEXT: CaptchaChallengeType.ValueType  # 1
"""Text recognition: The user has to type a distorted text from the picture into a special field."""
SILHOUETTES: CaptchaChallengeType.ValueType  # 2
"""Silhouettes: The user has to mark several icons from the picture in a particular order."""
KALEIDOSCOPE: CaptchaChallengeType.ValueType  # 3
"""Kaleidoscope: The user has to build a picture from individual parts by shuffling them using a slider."""
global___CaptchaChallengeType = CaptchaChallengeType

@typing.final
class Captcha(google.protobuf.message.Message):
    """A Captcha resource."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    FOLDER_ID_FIELD_NUMBER: builtins.int
    CLOUD_ID_FIELD_NUMBER: builtins.int
    CLIENT_KEY_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    ALLOWED_SITES_FIELD_NUMBER: builtins.int
    COMPLEXITY_FIELD_NUMBER: builtins.int
    STYLE_JSON_FIELD_NUMBER: builtins.int
    SUSPEND_FIELD_NUMBER: builtins.int
    TURN_OFF_HOSTNAME_CHECK_FIELD_NUMBER: builtins.int
    PRE_CHECK_TYPE_FIELD_NUMBER: builtins.int
    CHALLENGE_TYPE_FIELD_NUMBER: builtins.int
    SECURITY_RULES_FIELD_NUMBER: builtins.int
    DELETION_PROTECTION_FIELD_NUMBER: builtins.int
    OVERRIDE_VARIANTS_FIELD_NUMBER: builtins.int
    id: builtins.str
    """ID of the captcha."""
    folder_id: builtins.str
    """ID of the folder that the captcha belongs to."""
    cloud_id: builtins.str
    """ID of the cloud that the captcha belongs to."""
    client_key: builtins.str
    """Client key of the captcha, see [CAPTCHA keys](/docs/smartcaptcha/concepts/keys)."""
    name: builtins.str
    """Name of the captcha. The name is unique within the folder. 3-63 characters long."""
    complexity: global___CaptchaComplexity.ValueType
    """Complexity of the captcha."""
    style_json: builtins.str
    """JSON with variables to define the captcha appearance. For more details see generated JSON in cloud console."""
    suspend: builtins.bool
    """Determines that the captcha is currently in restricted mode, see [SmartCaptcha restricted mode](/docs/smartcaptcha/concepts/restricted-mode)."""
    turn_off_hostname_check: builtins.bool
    """Turn off host name check, see [Domain validation](/docs/smartcaptcha/concepts/domain-validation)."""
    pre_check_type: global___CaptchaPreCheckType.ValueType
    """Basic check type of the captcha."""
    challenge_type: global___CaptchaChallengeType.ValueType
    """Additional task type of the captcha."""
    deletion_protection: builtins.bool
    """Determines whether captcha is protected from being deleted."""
    @property
    def created_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Creation timestamp in [RFC3339](https://www.ietf.org/rfc/rfc3339.txt) text format."""

    @property
    def allowed_sites(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """List of allowed host names, see [Domain validation](/docs/smartcaptcha/concepts/domain-validation)."""

    @property
    def security_rules(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___SecurityRule]:
        """List of security rules."""

    @property
    def override_variants(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___OverrideVariant]:
        """List of variants to use in security_rules"""

    def __init__(
        self,
        *,
        id: builtins.str = ...,
        folder_id: builtins.str = ...,
        cloud_id: builtins.str = ...,
        client_key: builtins.str = ...,
        created_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        name: builtins.str = ...,
        allowed_sites: collections.abc.Iterable[builtins.str] | None = ...,
        complexity: global___CaptchaComplexity.ValueType = ...,
        style_json: builtins.str = ...,
        suspend: builtins.bool = ...,
        turn_off_hostname_check: builtins.bool = ...,
        pre_check_type: global___CaptchaPreCheckType.ValueType = ...,
        challenge_type: global___CaptchaChallengeType.ValueType = ...,
        security_rules: collections.abc.Iterable[global___SecurityRule] | None = ...,
        deletion_protection: builtins.bool = ...,
        override_variants: collections.abc.Iterable[global___OverrideVariant] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["created_at", b"created_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["allowed_sites", b"allowed_sites", "challenge_type", b"challenge_type", "client_key", b"client_key", "cloud_id", b"cloud_id", "complexity", b"complexity", "created_at", b"created_at", "deletion_protection", b"deletion_protection", "folder_id", b"folder_id", "id", b"id", "name", b"name", "override_variants", b"override_variants", "pre_check_type", b"pre_check_type", "security_rules", b"security_rules", "style_json", b"style_json", "suspend", b"suspend", "turn_off_hostname_check", b"turn_off_hostname_check"]) -> None: ...

global___Captcha = Captcha

@typing.final
class OverrideVariant(google.protobuf.message.Message):
    """OverrideVariant object. Contains the settings to override."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UUID_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    COMPLEXITY_FIELD_NUMBER: builtins.int
    PRE_CHECK_TYPE_FIELD_NUMBER: builtins.int
    CHALLENGE_TYPE_FIELD_NUMBER: builtins.int
    uuid: builtins.str
    """Unique identifier of the variant."""
    description: builtins.str
    """Optional description of the rule. 0-512 characters long."""
    complexity: global___CaptchaComplexity.ValueType
    """Complexity of the captcha."""
    pre_check_type: global___CaptchaPreCheckType.ValueType
    """Basic check type of the captcha."""
    challenge_type: global___CaptchaChallengeType.ValueType
    """Additional task type of the captcha."""
    def __init__(
        self,
        *,
        uuid: builtins.str = ...,
        description: builtins.str = ...,
        complexity: global___CaptchaComplexity.ValueType = ...,
        pre_check_type: global___CaptchaPreCheckType.ValueType = ...,
        challenge_type: global___CaptchaChallengeType.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["challenge_type", b"challenge_type", "complexity", b"complexity", "description", b"description", "pre_check_type", b"pre_check_type", "uuid", b"uuid"]) -> None: ...

global___OverrideVariant = OverrideVariant

@typing.final
class CaptchaSecretKey(google.protobuf.message.Message):
    """CaptchaSecretKey object. Contains captcha data that need to keep in secret."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SERVER_KEY_FIELD_NUMBER: builtins.int
    server_key: builtins.str
    """Server key of the captcha, see [CAPTCHA keys](/docs/smartcaptcha/concepts/keys)."""
    def __init__(
        self,
        *,
        server_key: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["server_key", b"server_key"]) -> None: ...

global___CaptchaSecretKey = CaptchaSecretKey

@typing.final
class SecurityRule(google.protobuf.message.Message):
    """SecurityRule object. Defines the condition and action: when and which variant to show."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    PRIORITY_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    CONDITION_FIELD_NUMBER: builtins.int
    OVERRIDE_VARIANT_UUID_FIELD_NUMBER: builtins.int
    name: builtins.str
    """Name of the rule. The name is unique within the captcha. 1-50 characters long."""
    priority: builtins.int
    """Priority of the rule. Lower value means higher priority."""
    description: builtins.str
    """Optional description of the rule. 0-512 characters long."""
    override_variant_uuid: builtins.str
    """Variant UUID to show in case of match the rule. Keep empty to use defaults."""
    @property
    def condition(self) -> global___Condition:
        """The condition for matching the rule."""

    def __init__(
        self,
        *,
        name: builtins.str = ...,
        priority: builtins.int = ...,
        description: builtins.str = ...,
        condition: global___Condition | None = ...,
        override_variant_uuid: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["condition", b"condition"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["condition", b"condition", "description", b"description", "name", b"name", "override_variant_uuid", b"override_variant_uuid", "priority", b"priority"]) -> None: ...

global___SecurityRule = SecurityRule

@typing.final
class Condition(google.protobuf.message.Message):
    """Condition object. AND semantics implied."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class StringMatcher(google.protobuf.message.Message):
        """StringMatcher object."""

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        EXACT_MATCH_FIELD_NUMBER: builtins.int
        EXACT_NOT_MATCH_FIELD_NUMBER: builtins.int
        PREFIX_MATCH_FIELD_NUMBER: builtins.int
        PREFIX_NOT_MATCH_FIELD_NUMBER: builtins.int
        PIRE_REGEX_MATCH_FIELD_NUMBER: builtins.int
        PIRE_REGEX_NOT_MATCH_FIELD_NUMBER: builtins.int
        exact_match: builtins.str
        exact_not_match: builtins.str
        prefix_match: builtins.str
        prefix_not_match: builtins.str
        pire_regex_match: builtins.str
        pire_regex_not_match: builtins.str
        def __init__(
            self,
            *,
            exact_match: builtins.str = ...,
            exact_not_match: builtins.str = ...,
            prefix_match: builtins.str = ...,
            prefix_not_match: builtins.str = ...,
            pire_regex_match: builtins.str = ...,
            pire_regex_not_match: builtins.str = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["exact_match", b"exact_match", "exact_not_match", b"exact_not_match", "match", b"match", "pire_regex_match", b"pire_regex_match", "pire_regex_not_match", b"pire_regex_not_match", "prefix_match", b"prefix_match", "prefix_not_match", b"prefix_not_match"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["exact_match", b"exact_match", "exact_not_match", b"exact_not_match", "match", b"match", "pire_regex_match", b"pire_regex_match", "pire_regex_not_match", b"pire_regex_not_match", "prefix_match", b"prefix_match", "prefix_not_match", b"prefix_not_match"]) -> None: ...
        def WhichOneof(self, oneof_group: typing.Literal["match", b"match"]) -> typing.Literal["exact_match", "exact_not_match", "prefix_match", "prefix_not_match", "pire_regex_match", "pire_regex_not_match"] | None: ...

    @typing.final
    class HostMatcher(google.protobuf.message.Message):
        """HostMatcher object."""

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        HOSTS_FIELD_NUMBER: builtins.int
        @property
        def hosts(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Condition.StringMatcher]:
            """List of hosts. OR semantics implied."""

        def __init__(
            self,
            *,
            hosts: collections.abc.Iterable[global___Condition.StringMatcher] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["hosts", b"hosts"]) -> None: ...

    @typing.final
    class UriMatcher(google.protobuf.message.Message):
        """UriMatcher object. AND semantics implied."""

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        PATH_FIELD_NUMBER: builtins.int
        QUERIES_FIELD_NUMBER: builtins.int
        @property
        def path(self) -> global___Condition.StringMatcher:
            """Path of the URI [RFC3986](https://datatracker.ietf.org/doc/html/rfc3986#section-3.3)."""

        @property
        def queries(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Condition.QueryMatcher]:
            """List of query matchers. AND semantics implied."""

        def __init__(
            self,
            *,
            path: global___Condition.StringMatcher | None = ...,
            queries: collections.abc.Iterable[global___Condition.QueryMatcher] | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["path", b"path"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["path", b"path", "queries", b"queries"]) -> None: ...

    @typing.final
    class QueryMatcher(google.protobuf.message.Message):
        """QueryMatcher object."""

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        """Key of the query parameter."""
        @property
        def value(self) -> global___Condition.StringMatcher:
            """Value of the query parameter."""

        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___Condition.StringMatcher | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    @typing.final
    class HeaderMatcher(google.protobuf.message.Message):
        """HeaderMatcher object."""

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        NAME_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        name: builtins.str
        """Name of header (case insensitive)."""
        @property
        def value(self) -> global___Condition.StringMatcher:
            """Value of the header."""

        def __init__(
            self,
            *,
            name: builtins.str = ...,
            value: global___Condition.StringMatcher | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["name", b"name", "value", b"value"]) -> None: ...

    @typing.final
    class IpMatcher(google.protobuf.message.Message):
        """IpMatcher object. AND semantics implied."""

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        IP_RANGES_MATCH_FIELD_NUMBER: builtins.int
        IP_RANGES_NOT_MATCH_FIELD_NUMBER: builtins.int
        GEO_IP_MATCH_FIELD_NUMBER: builtins.int
        GEO_IP_NOT_MATCH_FIELD_NUMBER: builtins.int
        @property
        def ip_ranges_match(self) -> global___Condition.IpRangesMatcher: ...
        @property
        def ip_ranges_not_match(self) -> global___Condition.IpRangesMatcher: ...
        @property
        def geo_ip_match(self) -> global___Condition.GeoIpMatcher: ...
        @property
        def geo_ip_not_match(self) -> global___Condition.GeoIpMatcher: ...
        def __init__(
            self,
            *,
            ip_ranges_match: global___Condition.IpRangesMatcher | None = ...,
            ip_ranges_not_match: global___Condition.IpRangesMatcher | None = ...,
            geo_ip_match: global___Condition.GeoIpMatcher | None = ...,
            geo_ip_not_match: global___Condition.GeoIpMatcher | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["geo_ip_match", b"geo_ip_match", "geo_ip_not_match", b"geo_ip_not_match", "ip_ranges_match", b"ip_ranges_match", "ip_ranges_not_match", b"ip_ranges_not_match"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["geo_ip_match", b"geo_ip_match", "geo_ip_not_match", b"geo_ip_not_match", "ip_ranges_match", b"ip_ranges_match", "ip_ranges_not_match", b"ip_ranges_not_match"]) -> None: ...

    @typing.final
    class IpRangesMatcher(google.protobuf.message.Message):
        """IpRangesMatcher object."""

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        IP_RANGES_FIELD_NUMBER: builtins.int
        @property
        def ip_ranges(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
            """List of IP ranges. OR semantics implied."""

        def __init__(
            self,
            *,
            ip_ranges: collections.abc.Iterable[builtins.str] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["ip_ranges", b"ip_ranges"]) -> None: ...

    @typing.final
    class GeoIpMatcher(google.protobuf.message.Message):
        """GeoIpMatcher object."""

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        LOCATIONS_FIELD_NUMBER: builtins.int
        @property
        def locations(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
            """ISO 3166-1 alpha 2. OR semantics implied."""

        def __init__(
            self,
            *,
            locations: collections.abc.Iterable[builtins.str] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["locations", b"locations"]) -> None: ...

    HOST_FIELD_NUMBER: builtins.int
    URI_FIELD_NUMBER: builtins.int
    HEADERS_FIELD_NUMBER: builtins.int
    SOURCE_IP_FIELD_NUMBER: builtins.int
    @property
    def host(self) -> global___Condition.HostMatcher:
        """Host where captcha placed."""

    @property
    def uri(self) -> global___Condition.UriMatcher:
        """URI where captcha placed."""

    @property
    def headers(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Condition.HeaderMatcher]:
        """Captcha request headers."""

    @property
    def source_ip(self) -> global___Condition.IpMatcher:
        """The IP address of the requester."""

    def __init__(
        self,
        *,
        host: global___Condition.HostMatcher | None = ...,
        uri: global___Condition.UriMatcher | None = ...,
        headers: collections.abc.Iterable[global___Condition.HeaderMatcher] | None = ...,
        source_ip: global___Condition.IpMatcher | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["host", b"host", "source_ip", b"source_ip", "uri", b"uri"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["headers", b"headers", "host", b"host", "source_ip", b"source_ip", "uri", b"uri"]) -> None: ...

global___Condition = Condition
