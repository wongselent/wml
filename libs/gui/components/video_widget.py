import datetime
import os
from typing import List, Dict, Tuple

from PyQt5 import QtCore, QtWidgets

from libs import config, video_editor


class ITEM_STATE:
    start: int = 0
    render: int = 1
    finish: int = 2
    error: int = 3

    __str: Dict[int, str] = {
        start: "Ready",
        render: "Rendering...",
        finish: "Finished",
        error: "Error!"
    }

    __bg_color: Dict[int, str] = {}

    @classmethod
    def str(cls, value: int) -> str:
        return cls.__str[value]


class VideoPreviewWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(VideoPreviewWidget, self).__init__(parent)
        config.load_ui(self)

        self.__parent: QtWidgets.QWidget = parent


class VideoItemWidget(QtWidgets.QWidget):
    render_video_signal: QtCore.pyqtSignal = QtCore.pyqtSignal()

    def __init__(self, parent: QtWidgets.QListWidget, video_name: str = None, video_path: str = None,
                 video_files: List[str] = None, video_intro: str = None, video_outro: str = None,
                 threadpool_obj: QtCore.QThreadPool = None) -> None:
        super(VideoItemWidget, self).__init__(parent)
        config.load_ui(self)
        self.__parent: QtWidgets.QListWidget = parent
        self.__video_name: str = video_name
        self.__video_path: str = video_path
        self.__video_files: List[str] = video_files
        self.__video_intro: str = video_intro
        self.__video_outro: str = video_outro
        self.__render_video_obj: video_editor.RenderVideo
        self.__threadpool_obj: QtCore.QThreadPool = threadpool_obj

        self.__setup_video_item()

        self.reload_button.clicked.connect(self.__setup_video_item)
        self.render_button.clicked.connect(self.render_video)
        self.render_video_signal.connect(self.render_video)

    @QtCore.pyqtSlot()
    def render_video(self) -> None:
        self.render_button.setText("Rendering...")
        self.render_button.setDisabled(True)

        width, height = self.__parent.get_video_resolution()
        self.__render_video_obj.set_size(width=width, height=height)
        self.__render_video_obj.render_video(
            progressbar_widget=self.render_progressbar
        )

        self.__check_video_exists(self.__render_video_obj.video_file)

    def get_video_list(self) -> None:
        print(self.__video_files)

    def __set_hidden_components(self, state: bool):
        self.render_info_label.setHidden(True)
        self.render_progressbar.setHidden(state)
        self.preview_button.setHidden(state)
        self.open_button.setHidden(state)
        self.render_button.setHidden(state)
        self.reload_button.setHidden(state)

    def __check_video_exists(self, video_file: str) -> None:
        if os.path.exists(video_file):
            self.render_button.setText("Rerender")
            self.render_button.setDisabled(False)
            self.render_progressbar.setFormat("Video is Exists!")

    def __set_render_video_obj(self) -> str:
        self.__render_video_obj: video_editor.RenderVideo = video_editor.RenderVideo(
            self.__video_path,
            intro_file=self.__video_intro,
            outro_file=self.__video_outro,
            bg_blur=True
        )
        return "Render Video Object is Created!"

    def __setup_video_item(self):
        self.title_label.setText(f"{self.__video_name} [ Loading Item...")
        self.__set_hidden_components(True)

        self.__threadpool_obj.run_functions(
            self.__set_render_video_obj,
            lambda: self.title_label.setText(
                f"{self.__video_name} [ Duration: {datetime.timedelta(seconds=self.__render_video_obj.duration())} ]"),
            lambda: self.__set_hidden_components(False),
            lambda: self.__check_video_exists(self.__render_video_obj.video_file),
        )


class CreateVideoWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, threadpool_obj: QtCore.QThreadPool = None) -> None:
        super(CreateVideoWidget, self).__init__(parent)
        config.load_ui(self)
        self.__parent: QtWidgets.QWidget = parent
        self.__threadpool_obj = threadpool_obj
        self.__video_data: Dict[str, dict] = {}
        # self.__threadpool_obj: thread.ThreadPool = thread.ThreadPool(parent=self)

        self.__disable_widgets = config.set_disabled_widgets(
            self.refresh_button,
            self.render_all_button,
            state=True
        )

        resolution_types: List[int] = [
            config.VIDEO_RESOLUTION.R144P,
            config.VIDEO_RESOLUTION.R240P,
            config.VIDEO_RESOLUTION.R360P,
            config.VIDEO_RESOLUTION.R480P,
            config.VIDEO_RESOLUTION.R720P,
            config.VIDEO_RESOLUTION.R1080P
        ]

        for res in resolution_types:
            self.video_resolution_combo.addItem(
                config.VIDEO_RESOLUTION.str(res),
                config.VIDEO_RESOLUTION.resolution(res)
            )

        self.video_path_button.clicked.connect(self.get_video_path)
        self.intro_path_button.clicked.connect(self.get_intro_path)
        self.outro_path_button.clicked.connect(self.get_outro_path)
        self.refresh_button.clicked.connect(self.refresh_video_list)
        self.render_all_button.clicked.connect(self.do_render_all_video)

    def do_render_all_video(self) -> None:
        item_count: int = self.video_obj_list.count()

        for i in range(item_count):
            item: QtWidgets.QListWidgetItem = self.video_obj_list.item(i)
            item_widget: VideoItemWidget = self.video_obj_list.itemWidget(item)
            item_widget.render_video_signal.emit()

    def get_video_path(self) -> Dict[str, dict]:
        video_data: Dict[str, dict] = {}

        root_path = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption="Video Path",
            directory="/"
        )

        self.video_path_edit.setText(root_path)

        for dirpath, dirnames, filenames, in os.walk(root_path):
            for dirname in dirnames:
                video_path = config.join_directory(dirpath, dirname)
                video_data[dirname]: Dict[str, str] = {}
                video_data[dirname]["video_path"]: str = video_path
                video_data[dirname]["video_files"]: List[str] = []
                for filename in os.listdir(video_path):
                    video_file = config.join_directory(video_path, filename)
                    if os.path.isfile(video_file):
                        _, ext = os.path.splitext(video_file)
                        if ext.lower() in (".mp4", ".webm"):
                            video_data[dirname]["video_files"].append(video_file)
                            # video_data[video_path].append(video_file)

        if video_data:
            self.__video_data = video_data
            self.__create_video_item_widget(video_data)
            self.__disable_widgets(False)
            # self.refresh_button.setDisabled(False)
            # self.render_all_button.setDisabled(False)

        return video_data

    def get_intro_path(self) -> None:
        video_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Intro Path",
            directory="/",
            filter="Video Ext (*.mp4 *.webm)"
        )

        self.video_intro_edit.setText(video_file)
        self.refresh_video_list()

    def get_outro_path(self) -> None:
        video_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Outro Path",
            directory="/",
            filter="Video Ext (*.mp4 *.webm)"
        )

        self.video_outro_edit.setText(video_file)
        self.refresh_video_list()

    def get_video_resolution(self) -> Tuple[int]:
        current_index: int = self.video_resolution_combo.currentIndex()
        return tuple(self.video_resolution_combo.itemData(current_index, QtCore.Qt.UserRole))

    def refresh_video_list(self) -> None:
        if self.__video_data:
            self.__create_video_item_widget(video_data=self.__video_data)

    def __create_video_item_widget(self, video_data: Dict[str, dict]) -> None:
        self.video_obj_list.clear()
        for vid_key, vid_val in video_data.items():
            item: QtWidgets.QListWidgetItem = QtWidgets.QListWidgetItem(self.video_obj_list)

            item_data: Dict[str, str] = {
                "video_title": vid_key,
                "video_path": vid_val["video_path"],
                "video_files": vid_val["video_files"]
            }

            item_widget: VideoItemWidget = VideoItemWidget(
                self,
                video_name=vid_key,
                video_path=vid_val["video_path"],
                video_files=vid_val["video_files"],
                video_intro=self.video_intro_edit.text(),
                video_outro=self.video_outro_edit.text(),
                threadpool_obj=self.__threadpool_obj
            )

            item.setData(QtCore.Qt.UserRole, item_data)
            item.setSizeHint(item_widget.size())

            self.video_obj_list.addItem(item)
            self.video_obj_list.setItemWidget(item, item_widget)
