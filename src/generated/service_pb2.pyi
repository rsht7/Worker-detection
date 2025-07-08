from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ZoneRequest(_message.Message):
    __slots__ = ("camera_id",)
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    camera_id: int
    def __init__(self, camera_id: _Optional[int] = ...) -> None: ...

class ZoneData(_message.Message):
    __slots__ = ("camera_id", "zones")
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    ZONES_FIELD_NUMBER: _ClassVar[int]
    camera_id: int
    zones: _containers.RepeatedCompositeFieldContainer[Zone]
    def __init__(self, camera_id: _Optional[int] = ..., zones: _Optional[_Iterable[_Union[Zone, _Mapping]]] = ...) -> None: ...

class Zone(_message.Message):
    __slots__ = ("zone_id", "zone_coord", "rules")
    ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    ZONE_COORD_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    zone_id: int
    zone_coord: _containers.RepeatedScalarFieldContainer[int]
    rules: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, zone_id: _Optional[int] = ..., zone_coord: _Optional[_Iterable[int]] = ..., rules: _Optional[_Iterable[int]] = ...) -> None: ...

class AlertData(_message.Message):
    __slots__ = ("camera_id", "zone_id", "alert_type", "rules", "confidence", "timestamp", "image")
    CAMERA_ID_FIELD_NUMBER: _ClassVar[int]
    ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    ALERT_TYPE_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    camera_id: int
    zone_id: int
    alert_type: int
    rules: _containers.RepeatedScalarFieldContainer[int]
    confidence: int
    timestamp: str
    image: bytes
    def __init__(self, camera_id: _Optional[int] = ..., zone_id: _Optional[int] = ..., alert_type: _Optional[int] = ..., rules: _Optional[_Iterable[int]] = ..., confidence: _Optional[int] = ..., timestamp: _Optional[str] = ..., image: _Optional[bytes] = ...) -> None: ...

class Ack(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
