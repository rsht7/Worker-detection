from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ZoneRequest(_message.Message):
    __slots__ = ("camera_id",)
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    def __init__(self, camera_id: _Optional[str] = ...) -> None: ...

class ZoneData(_message.Message):
    __slots__ = ("camera_id", "zones")
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    ZONES_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    zones: _containers.RepeatedCompositeFieldContainer[Zone]
    def __init__(self, camera_id: _Optional[str] = ..., zones: _Optional[_Iterable[_Union[Zone, _Mapping]]] = ...) -> None: ...

class Zone(_message.Message):
    __slots__ = ("zone_id", "numpy_mask", "rules")
    ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    NUMPY_MASK_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    zone_id: str
    numpy_mask: bytes
    rules: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, zone_id: _Optional[str] = ..., numpy_mask: _Optional[bytes] = ..., rules: _Optional[_Iterable[str]] = ...) -> None: ...

class AlertData(_message.Message):
    __slots__ = ("camera_id", "zone_id", "alert_type", "confidence", "timestamp", "image")
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    ALERT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    camera_id: str
    zone_id: str
    alert_type: str
    confidence: int
    timestamp: str
    image: bytes
    def __init__(self, camera_id: _Optional[str] = ..., zone_id: _Optional[str] = ..., alert_type: _Optional[str] = ..., confidence: _Optional[int] = ..., timestamp: _Optional[str] = ..., image: _Optional[bytes] = ...) -> None: ...

class Ack(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...
