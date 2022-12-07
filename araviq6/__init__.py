"""
AraViQ6: NDArray from QVideoFrame with Qt6
==========================================

AraViQ6 is a package to build video pipeline with :class:`numpy.ndarray` from
Qt6's ``QVideoFrame``.

"""

from .version import __version__  # noqa

from .array2qvideoframe import (
    array2qvideoframe,
)
from .videostream import (
    VideoFrameWorker,
    VideoFrameProcessor,
    FrameToArrayConverter,
    ArrayToFrameConverter,
    ArrayWorker,
    ArrayProcessor,
    NDArrayVideoPlayer,
    NDArrayMediaCaptureSession,
)
from .labels import ScalableQLabel, NDArrayLabel
from .videowidgets import (
    PlayerProcessWidget,
    NDArrayCameraWidget,
)
from .util import (
    ClickableSlider,
    MediaController,
    get_samples_path,
)


__all__ = [
    "array2qvideoframe",
    "VideoFrameWorker",
    "VideoFrameProcessor",
    "FrameToArrayConverter",
    "ArrayToFrameConverter",
    "ArrayWorker",
    "ArrayProcessor",
    "NDArrayVideoPlayer",
    "NDArrayMediaCaptureSession",
    "ScalableQLabel",
    "NDArrayLabel",
    "PlayerProcessWidget",
    "NDArrayCameraWidget",
    "ClickableSlider",
    "MediaController",
    "get_samples_path",
]
