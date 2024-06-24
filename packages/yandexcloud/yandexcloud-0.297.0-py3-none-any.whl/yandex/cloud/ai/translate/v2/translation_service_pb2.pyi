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
import sys
import typing
import yandex.cloud.ai.translate.v2.translation_pb2

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class TranslateRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Format:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _FormatEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[TranslateRequest._Format.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        FORMAT_UNSPECIFIED: TranslateRequest._Format.ValueType  # 0
        PLAIN_TEXT: TranslateRequest._Format.ValueType  # 1
        """Text without markup. Default value."""
        HTML: TranslateRequest._Format.ValueType  # 2
        """Text in the HTML format."""

    class Format(_Format, metaclass=_FormatEnumTypeWrapper): ...
    FORMAT_UNSPECIFIED: TranslateRequest.Format.ValueType  # 0
    PLAIN_TEXT: TranslateRequest.Format.ValueType  # 1
    """Text without markup. Default value."""
    HTML: TranslateRequest.Format.ValueType  # 2
    """Text in the HTML format."""

    SOURCE_LANGUAGE_CODE_FIELD_NUMBER: builtins.int
    TARGET_LANGUAGE_CODE_FIELD_NUMBER: builtins.int
    FORMAT_FIELD_NUMBER: builtins.int
    TEXTS_FIELD_NUMBER: builtins.int
    FOLDER_ID_FIELD_NUMBER: builtins.int
    MODEL_FIELD_NUMBER: builtins.int
    GLOSSARY_CONFIG_FIELD_NUMBER: builtins.int
    SPELLER_FIELD_NUMBER: builtins.int
    source_language_code: builtins.str
    """The text language to translate from.
    Specified in [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639-1) format (for example, `` ru ``).

    Required for translating with glossary.
    """
    target_language_code: builtins.str
    """The target language to translate the text.
    Specified in [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639-1) format (for example, `` en ``).
    """
    format: global___TranslateRequest.Format.ValueType
    """Format of the text."""
    folder_id: builtins.str
    """ID of the folder to which you have access.
    Required for authorization with a user account (see [yandex.cloud.iam.v1.UserAccount] resource).
    Don't specify this field if you make the request on behalf of a service account.
    """
    model: builtins.str
    """Do not specify this field, custom models are not supported yet."""
    speller: builtins.bool
    """use speller"""
    @property
    def texts(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Array of the strings to translate.
        The maximum total length of all strings is 10000 characters.
        """

    @property
    def glossary_config(self) -> global___TranslateGlossaryConfig:
        """Glossary to be applied for the translation. For more information, see [Glossaries](/docs/translate/concepts/glossary)."""

    def __init__(
        self,
        *,
        source_language_code: builtins.str = ...,
        target_language_code: builtins.str = ...,
        format: global___TranslateRequest.Format.ValueType = ...,
        texts: collections.abc.Iterable[builtins.str] | None = ...,
        folder_id: builtins.str = ...,
        model: builtins.str = ...,
        glossary_config: global___TranslateGlossaryConfig | None = ...,
        speller: builtins.bool = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["glossary_config", b"glossary_config"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["folder_id", b"folder_id", "format", b"format", "glossary_config", b"glossary_config", "model", b"model", "source_language_code", b"source_language_code", "speller", b"speller", "target_language_code", b"target_language_code", "texts", b"texts"]) -> None: ...

global___TranslateRequest = TranslateRequest

@typing.final
class TranslateGlossaryConfig(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    GLOSSARY_DATA_FIELD_NUMBER: builtins.int
    @property
    def glossary_data(self) -> global___GlossaryData:
        """Pass glossary data in the request. Currently, only this way to pass glossary is supported."""

    def __init__(
        self,
        *,
        glossary_data: global___GlossaryData | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["glossary_data", b"glossary_data", "glossary_source", b"glossary_source"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["glossary_data", b"glossary_data", "glossary_source", b"glossary_source"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["glossary_source", b"glossary_source"]) -> typing.Literal["glossary_data"] | None: ...

global___TranslateGlossaryConfig = TranslateGlossaryConfig

@typing.final
class GlossaryData(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    GLOSSARY_PAIRS_FIELD_NUMBER: builtins.int
    @property
    def glossary_pairs(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___GlossaryPair]:
        """Array of text pairs.

        The maximum total length of all source texts is 10000 characters.
        The maximum total length of all translated texts is 10000 characters.
        """

    def __init__(
        self,
        *,
        glossary_pairs: collections.abc.Iterable[global___GlossaryPair] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["glossary_pairs", b"glossary_pairs"]) -> None: ...

global___GlossaryData = GlossaryData

@typing.final
class GlossaryPair(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SOURCE_TEXT_FIELD_NUMBER: builtins.int
    TRANSLATED_TEXT_FIELD_NUMBER: builtins.int
    EXACT_FIELD_NUMBER: builtins.int
    source_text: builtins.str
    """Text in the source language."""
    translated_text: builtins.str
    """Text in the target language."""
    exact: builtins.bool
    def __init__(
        self,
        *,
        source_text: builtins.str = ...,
        translated_text: builtins.str = ...,
        exact: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["exact", b"exact", "source_text", b"source_text", "translated_text", b"translated_text"]) -> None: ...

global___GlossaryPair = GlossaryPair

@typing.final
class TranslateResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TRANSLATIONS_FIELD_NUMBER: builtins.int
    @property
    def translations(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.ai.translate.v2.translation_pb2.TranslatedText]:
        """Array of the translations."""

    def __init__(
        self,
        *,
        translations: collections.abc.Iterable[yandex.cloud.ai.translate.v2.translation_pb2.TranslatedText] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["translations", b"translations"]) -> None: ...

global___TranslateResponse = TranslateResponse

@typing.final
class DetectLanguageRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TEXT_FIELD_NUMBER: builtins.int
    LANGUAGE_CODE_HINTS_FIELD_NUMBER: builtins.int
    FOLDER_ID_FIELD_NUMBER: builtins.int
    text: builtins.str
    """The text to detect the language for."""
    folder_id: builtins.str
    """ID of the folder to which you have access.
    Required for authorization with a user account (see [yandex.cloud.iam.v1.UserAccount] resource).
    Don't specify this field if you make the request on behalf of a service account.
    """
    @property
    def language_code_hints(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """List of the most likely languages. These languages will be given preference when detecting the text language.
        Specified in [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639-1) format (for example, `` ru ``).

        To get the list of supported languages, use a [TranslationService.ListLanguages] request.
        """

    def __init__(
        self,
        *,
        text: builtins.str = ...,
        language_code_hints: collections.abc.Iterable[builtins.str] | None = ...,
        folder_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["folder_id", b"folder_id", "language_code_hints", b"language_code_hints", "text", b"text"]) -> None: ...

global___DetectLanguageRequest = DetectLanguageRequest

@typing.final
class DetectLanguageResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LANGUAGE_CODE_FIELD_NUMBER: builtins.int
    language_code: builtins.str
    """The text language in [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639-1) format (for example, `` ru ``).

    To get the language name, use a [TranslationService.ListLanguages] request.
    """
    def __init__(
        self,
        *,
        language_code: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["language_code", b"language_code"]) -> None: ...

global___DetectLanguageResponse = DetectLanguageResponse

@typing.final
class ListLanguagesRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FOLDER_ID_FIELD_NUMBER: builtins.int
    folder_id: builtins.str
    """ID of the folder to which you have access.
    Required for authorization with a user account (see [yandex.cloud.iam.v1.UserAccount] resource).
    Don't specify this field if you make the request on behalf of a service account.
    """
    def __init__(
        self,
        *,
        folder_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["folder_id", b"folder_id"]) -> None: ...

global___ListLanguagesRequest = ListLanguagesRequest

@typing.final
class ListLanguagesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LANGUAGES_FIELD_NUMBER: builtins.int
    @property
    def languages(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[yandex.cloud.ai.translate.v2.translation_pb2.Language]:
        """List of supported languages."""

    def __init__(
        self,
        *,
        languages: collections.abc.Iterable[yandex.cloud.ai.translate.v2.translation_pb2.Language] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["languages", b"languages"]) -> None: ...

global___ListLanguagesResponse = ListLanguagesResponse
