import os

from PyQt5 import QtCore, QtWidgets

from libs import config, video_editor


class ITEM_STATE:
    start = 0
    render = 1
    finish = 2
    error = 3

    __str = {
        start: "Ready",
        render: "Rendering...",
        finish: "Finished",
        error: "Error!"
    }

    __bg_color = {}

    @classmethod
    def str(cls, state):
        if state in cls.__str.keys():
            return cls.__str[state]
        else:
            raise Exception(f"{state} not in ITEM_STATE")


class VideoPreviewWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(VideoPreviewWidget, self).__init__(parent)
        config.load_ui(self)

        self.__parent = parent


class VideoItemWidget(QtWidgets.QWidget):
    state_item_signal = QtCore.pyqtSignal(int)
    render_video_signal = QtCore.pyqtSignal()

    def __init__(self, parent: QtWidgets.QListWidget, video_name: str = None, video_path: str = None,
                 video_files: list = None, video_intro: str = None, video_outro: str = None) -> None:
        super(VideoItemWidget, self).__init__(parent)
        config.load_ui(self)
        self.__parent = parent
        self.__video_name = video_name
        self.__video_path = video_path
        self.__video_files = video_files
        self.__video_intro = video_intro
        self.__video_outro = video_outro

        self.__render_video_obj: video_editor.RenderVideo = video_editor.RenderVideo(
            self.__video_path,
            intro_file=self.__video_intro,
            outro_file=self.__video_outro,
            bg_blur=True
        )

        self.render_progressbar.setHidden(True)
        # self.render_info_label.setHidden(True)
        self.preview_button.setHidden(True)
        self.open_button.setHidden(True)
        self.title_label.setText(self.__video_name)

        self.render_button.clicked.connect(self.render_video)
        self.render_video_signal.connect(self.render_video)
        self.state_item_signal.connect(self.set_state_item)

    QtCore.pyqtSlot()

    def render_video(self) -> None:
        try:
            self.set_state_item(ITEM_STATE.render)
            self.__render_video_obj.set_size(width=config.VIDEO_WIDTH, height=config.VIDEO_HEIGHT, reduce=3)
            self.__render_video_obj.render_video()
        except Exception as ex:
            print(ex)
            self.set_state_item(ITEM_STATE.error)
            return
        else:
            self.set_state_item(ITEM_STATE.render)
        finally:
            self.set_state_item(ITEM_STATE.finish)

    QtCore.pyqtSlot(int)

    def set_state_item(self, state) -> None:
        self.render_info_label.setText(ITEM_STATE.str(state))

    def get_video_list(self) -> None:
        print(self.__video_files)


class CreateVideoWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(CreateVideoWidget, self).__init__(parent)
        config.load_ui(self)
        self.__parent = parent

        self.video_path_button.clicked.connect(self.get_video_path)
        self.intro_path_button.clicked.connect(self.get_intro_path)
        self.outro_path_button.clicked.connect(self.get_outro_path)
        self.render_all_button.clicked.connect(self.do_render_all_video)

    def do_render_all_video(self) -> None:
        item_count: int = self.video_obj_list.count()

        for i in range(item_count):
            item: QtWidgets.QListWidgetItem = self.video_obj_list.item(i)
            item_widget: VideoItemWidget = self.video_obj_list.itemWidget(item)

            item_widget.render_video_signal.emit()
            # try:
            #     item_widget.state_item_signal.emit(ITEM_STATE.render)
            #
            # except Exception as ex:
            #     print(ex)
            #     item_widget.state_item_signal.emit(ITEM_STATE.error)
            #     return
            # else:
            #     item_widget.state_item_signal.emit(ITEM_STATE.render)
            # finally:
            #     item_widget.state_item_signal.emit(ITEM_STATE.finish)

    def get_video_path(self) -> dict:
        video_data: dict = {}

        root_path = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption="Video Path",
            directory="/"
        )

        self.video_path_edit.setText(root_path)

        for dirpath, dirnames, filenames, in os.walk(root_path):
            for dirname in dirnames:
                video_path = config.join_directory(dirpath, dirname)
                video_data[dirname] = {}
                video_data[dirname]["video_path"] = video_path
                video_data[dirname]["video_files"] = []
                for filename in os.listdir(video_path):
                    video_file = config.join_directory(video_path, filename)
                    if os.path.isfile(video_file):
                        _, ext = os.path.splitext(video_file)
                        if ext.lower() in (".mp4", ".webm"):
                            video_data[dirname]["video_files"].append(video_file)
                            # video_data[video_path].append(video_file)

        if video_data:
            self.__create_video_item_widget(video_data)

        return video_data

    def get_intro_path(self) -> None:
        root_path = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Intro Path",
            directory="/",
            filter="Video Ext (*.mp4 *.webm)"
        )

        self.video_intro_edit.setText(root_path)

    def get_outro_path(self) -> None:
        root_path = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Intro Path",
            directory="/",
            filter="Video Ext (*.mp4 *.webm)"
        )

        self.video_outro_edit.setText(root_path)

    def __create_video_item_widget(self, video_data: dict) -> None:
        self.video_obj_list.clear()
        for vid_key, vid_val in video_data.items():
            item: QtWidgets.QListWidgetItem = QtWidgets.QListWidgetItem(self.video_obj_list)
            item_data: dict = {
                "video_title": vid_key,
                "video_path": vid_val["video_path"],
                "video_files": vid_val["video_files"]
            }
            item_widget: VideoItemWidget = VideoItemWidget(
                self.video_obj_list,
                video_name=vid_key,
                video_path=vid_val["video_path"],
                video_files=vid_val["video_files"],
                video_intro=self.video_intro_edit.text(),
                video_outro=self.video_outro_edit.text()
            )

            item.setData(QtCore.Qt.UserRole, item_data)
            item.setSizeHint(item_widget.sizeHint())
            item_widget.state_item_signal.emit(ITEM_STATE.start)
            item_widget.set_state_item(ITEM_STATE.start)

            self.video_obj_list.addItem(item)
            self.video_obj_list.setItemWidget(item, item_widget)
