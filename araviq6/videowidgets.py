"""
Video widgets
=============

:mod:`araviq6.videowidgets` provides convenience widgets with pre-built video
pipelines.

.. autoclass:: NDArrayVideoPlayerWidget
   :members:

.. autoclass:: NDArrayCameraWidget
   :members:

"""

from .videostream import VideoFrameWorker, VideoFrameProcessor
from .util import MediaController
from araviq6.qt_compat import QtCore, QtWidgets, QtMultimedia, QtMultimediaWidgets


__all__ = [
    "NDArrayVideoPlayerWidget",
    "NDArrayCameraWidget",
]


class NDArrayVideoPlayerWidget(QtWidgets.QWidget):
    """
    Widget to play video file with array processing.

    By default this widget does not perform any array processing. User may define
    own :class:`VideoFrameWorker` instance and set by :meth:`setWorker`.

    Examples
    ========

    .. tabs::

        .. code-tab:: python
            :caption: PySide6

            from PySide6.QtCore import QUrl
            from PySide6.QtWidgets import QApplication
            import sys
            from araviq6 import get_samples_path, NDArrayVideoPlayerWidget
            def runGUI():
                app = QApplication(sys.argv)
                w = NDArrayVideoPlayerWidget()
                w.setSource(QUrl.fromLocalFile(get_samples_path('hello.mp4')))
                w.show()
                app.exec()
                app.quit()
            runGUI() # doctest: +SKIP

    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._videoPlayer = QtMultimedia.QMediaPlayer()
        self._playerVideoSink = QtMultimedia.QVideoSink()
        self._frameProcessor = VideoFrameProcessor()
        self._videoWidget = QtMultimediaWidgets.QVideoWidget()
        self._mediaController = MediaController()

        # set up the pipeline
        self._videoPlayer.setVideoSink(self._playerVideoSink)
        self._playerVideoSink.videoFrameChanged.connect(
            self._frameProcessor.processVideoFrame
        )
        self._frameProcessor.videoFrameProcessed.connect(self.displayVideoFrame)

        self._mediaController.setPlayer(self._videoPlayer)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._videoWidget)
        layout.addWidget(self._mediaController)
        self.setLayout(layout)

    def setSource(self, url: QtCore.QUrl):
        self._videoPlayer.setSource(url)

    def setWorker(self, worker: VideoFrameWorker):
        self._frameProcessor.setWorker(worker)

    @QtCore.Slot(QtMultimedia.QVideoFrame)
    def displayVideoFrame(self, frame: QtMultimedia.QVideoFrame):
        self._videoWidget.videoSink().setVideoFrame(frame)

    def closeEvent(self, event):
        self._frameProcessor.stop()
        super().closeEvent(event)


class NDArrayCameraWidget(QtWidgets.QWidget):
    """
    Widget to stream camera with array processing.

    By default this widget does not perform any array processing. User may define
    own :class:`VideoFrameWorker` instance and set by :meth:`setWorker`.

    Examples
    ========

    .. tabs::

        .. code-tab:: python
            :caption: PySide6

            from PySide6.QtWidgets import QApplication
            from PySide6.QtMultimedia import QCamera
            import sys
            from araviq6 import NDArrayCameraWidget
            def runGUI():
                app = QApplication(sys.argv)
                widget = NDArrayCameraWidget()
                camera = QCamera()
                widget.setCamera(camera)
                camera.start()
                widget.show()
                app.exec()
                app.quit()
            runGUI() # doctest: +SKIP

    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._captureSession = QtMultimedia.QMediaCaptureSession()
        self._cameraVideoSink = QtMultimedia.QVideoSink()
        self._frameProcessor = VideoFrameProcessor()
        self._videoWidget = QtMultimediaWidgets.QVideoWidget()

        # set up the pipeline
        self._captureSession.setVideoSink(self._cameraVideoSink)
        self._cameraVideoSink.videoFrameChanged.connect(
            self._frameProcessor.processVideoFrame
        )
        self._frameProcessor.videoFrameProcessed.connect(self.displayVideoFrame)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._videoWidget)
        self.setLayout(layout)

    @QtCore.Slot(QtMultimedia.QCamera)
    def setCamera(self, camera: QtMultimedia.QCamera):
        self._captureSession.setCamera(camera)

    def setWorker(self, worker: VideoFrameWorker):
        self._frameProcessor.setWorker(worker)

    @QtCore.Slot(QtMultimedia.QVideoFrame)
    def displayVideoFrame(self, frame: QtMultimedia.QVideoFrame):
        self._videoWidget.videoSink().setVideoFrame(frame)

    def closeEvent(self, event):
        self._frameProcessor.stop()
        super().closeEvent(event)
