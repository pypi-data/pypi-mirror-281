from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Capture(_message.Message):
    __slots__ = ("start",)
    class Codec(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CODEC_UNKNOWN: _ClassVar[Capture.Codec]
        CODEC_AUTOMATIC: _ClassVar[Capture.Codec]
        CODEC_H264: _ClassVar[Capture.Codec]
        CODEC_H264_SOFTWARE: _ClassVar[Capture.Codec]
        CODEC_H265: _ClassVar[Capture.Codec]
        CODEC_H265_SOFTWARE: _ClassVar[Capture.Codec]
        CODEC_PRORES_422_PROXY: _ClassVar[Capture.Codec]
        CODEC_PRORES_422_LT: _ClassVar[Capture.Codec]
        CODEC_PRORES_422: _ClassVar[Capture.Codec]
        CODEC_PRORES_422_HQ: _ClassVar[Capture.Codec]
        CODEC_PRORES_4444: _ClassVar[Capture.Codec]
        CODEC_PRORES_4444_XQ: _ClassVar[Capture.Codec]
        CODEC_HAP: _ClassVar[Capture.Codec]
        CODEC_HAP_ALPHA: _ClassVar[Capture.Codec]
        CODEC_HAP_Q: _ClassVar[Capture.Codec]
        CODEC_HAP_Q_ALPHA: _ClassVar[Capture.Codec]
        CODEC_NOTCH: _ClassVar[Capture.Codec]
    CODEC_UNKNOWN: Capture.Codec
    CODEC_AUTOMATIC: Capture.Codec
    CODEC_H264: Capture.Codec
    CODEC_H264_SOFTWARE: Capture.Codec
    CODEC_H265: Capture.Codec
    CODEC_H265_SOFTWARE: Capture.Codec
    CODEC_PRORES_422_PROXY: Capture.Codec
    CODEC_PRORES_422_LT: Capture.Codec
    CODEC_PRORES_422: Capture.Codec
    CODEC_PRORES_422_HQ: Capture.Codec
    CODEC_PRORES_4444: Capture.Codec
    CODEC_PRORES_4444_XQ: Capture.Codec
    CODEC_HAP: Capture.Codec
    CODEC_HAP_ALPHA: Capture.Codec
    CODEC_HAP_Q: Capture.Codec
    CODEC_HAP_Q_ALPHA: Capture.Codec
    CODEC_NOTCH: Capture.Codec
    class FrameRate(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FRAME_RATE_UNKNOWN: _ClassVar[Capture.FrameRate]
        FRAME_RATE_24: _ClassVar[Capture.FrameRate]
        FRAME_RATE_25: _ClassVar[Capture.FrameRate]
        FRAME_RATE_29_97: _ClassVar[Capture.FrameRate]
        FRAME_RATE_30: _ClassVar[Capture.FrameRate]
        FRAME_RATE_50: _ClassVar[Capture.FrameRate]
        FRAME_RATE_59_94: _ClassVar[Capture.FrameRate]
        FRAME_RATE_60: _ClassVar[Capture.FrameRate]
    FRAME_RATE_UNKNOWN: Capture.FrameRate
    FRAME_RATE_24: Capture.FrameRate
    FRAME_RATE_25: Capture.FrameRate
    FRAME_RATE_29_97: Capture.FrameRate
    FRAME_RATE_30: Capture.FrameRate
    FRAME_RATE_50: Capture.FrameRate
    FRAME_RATE_59_94: Capture.FrameRate
    FRAME_RATE_60: Capture.FrameRate
    class Resolution(_message.Message):
        __slots__ = ("width", "height")
        WIDTH_FIELD_NUMBER: _ClassVar[int]
        HEIGHT_FIELD_NUMBER: _ClassVar[int]
        width: int
        height: int
        def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...
    class Start(_message.Message):
        __slots__ = ("rtmp", "disk", "resi")
        class RTMP(_message.Message):
            __slots__ = ("codec", "frame_rate", "host", "resolution", "stream_started", "video_bitrate")
            CODEC_FIELD_NUMBER: _ClassVar[int]
            FRAME_RATE_FIELD_NUMBER: _ClassVar[int]
            HOST_FIELD_NUMBER: _ClassVar[int]
            RESOLUTION_FIELD_NUMBER: _ClassVar[int]
            STREAM_STARTED_FIELD_NUMBER: _ClassVar[int]
            VIDEO_BITRATE_FIELD_NUMBER: _ClassVar[int]
            codec: Capture.Codec
            frame_rate: Capture.FrameRate
            host: str
            resolution: Capture.Resolution
            stream_started: bool
            video_bitrate: int
            def __init__(self, codec: _Optional[_Union[Capture.Codec, str]] = ..., frame_rate: _Optional[_Union[Capture.FrameRate, str]] = ..., host: _Optional[str] = ..., resolution: _Optional[_Union[Capture.Resolution, _Mapping]] = ..., stream_started: bool = ..., video_bitrate: _Optional[int] = ...) -> None: ...
        class Disk(_message.Message):
            __slots__ = ("codec", "frame_rate", "resolution", "stream_started", "video_bitrate")
            CODEC_FIELD_NUMBER: _ClassVar[int]
            FRAME_RATE_FIELD_NUMBER: _ClassVar[int]
            RESOLUTION_FIELD_NUMBER: _ClassVar[int]
            STREAM_STARTED_FIELD_NUMBER: _ClassVar[int]
            VIDEO_BITRATE_FIELD_NUMBER: _ClassVar[int]
            codec: Capture.Codec
            frame_rate: Capture.FrameRate
            resolution: Capture.Resolution
            stream_started: bool
            video_bitrate: int
            def __init__(self, codec: _Optional[_Union[Capture.Codec, str]] = ..., frame_rate: _Optional[_Union[Capture.FrameRate, str]] = ..., resolution: _Optional[_Union[Capture.Resolution, _Mapping]] = ..., stream_started: bool = ..., video_bitrate: _Optional[int] = ...) -> None: ...
        class Resi(_message.Message):
            __slots__ = ("codec", "frame_rate", "resolution", "stream_started", "video_bitrate")
            CODEC_FIELD_NUMBER: _ClassVar[int]
            FRAME_RATE_FIELD_NUMBER: _ClassVar[int]
            RESOLUTION_FIELD_NUMBER: _ClassVar[int]
            STREAM_STARTED_FIELD_NUMBER: _ClassVar[int]
            VIDEO_BITRATE_FIELD_NUMBER: _ClassVar[int]
            codec: Capture.Codec
            frame_rate: Capture.FrameRate
            resolution: Capture.Resolution
            stream_started: bool
            video_bitrate: int
            def __init__(self, codec: _Optional[_Union[Capture.Codec, str]] = ..., frame_rate: _Optional[_Union[Capture.FrameRate, str]] = ..., resolution: _Optional[_Union[Capture.Resolution, _Mapping]] = ..., stream_started: bool = ..., video_bitrate: _Optional[int] = ...) -> None: ...
        RTMP_FIELD_NUMBER: _ClassVar[int]
        DISK_FIELD_NUMBER: _ClassVar[int]
        RESI_FIELD_NUMBER: _ClassVar[int]
        rtmp: Capture.Start.RTMP
        disk: Capture.Start.Disk
        resi: Capture.Start.Resi
        def __init__(self, rtmp: _Optional[_Union[Capture.Start.RTMP, _Mapping]] = ..., disk: _Optional[_Union[Capture.Start.Disk, _Mapping]] = ..., resi: _Optional[_Union[Capture.Start.Resi, _Mapping]] = ...) -> None: ...
    START_FIELD_NUMBER: _ClassVar[int]
    start: Capture.Start
    def __init__(self, start: _Optional[_Union[Capture.Start, _Mapping]] = ...) -> None: ...
