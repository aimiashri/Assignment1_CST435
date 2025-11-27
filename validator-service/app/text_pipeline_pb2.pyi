from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PipelineText(_message.Message):
    __slots__ = ("original_text", "processed_text", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ORIGINAL_TEXT_FIELD_NUMBER: _ClassVar[int]
    PROCESSED_TEXT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    original_text: str
    processed_text: str
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, original_text: _Optional[str] = ..., processed_text: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...
