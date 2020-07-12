import os
import shutil
import tempfile
import datetime
from typing import List, Any

import numpy as np
import proglog
import qimage2ndarray as im2array
from PyQt5 import QtGui, QtWidgets
from moviepy import editor
from skimage import filters

from libs import config

tempfile.tempdir = config.TEMP_PATH


def _blur_fx(image) -> filters.gaussian:
    return filters.gaussian(image.astype(float), sigma=6)


class RenderProgressLogger(proglog.ProgressBarLogger):
    def __init__(self, progressbar_widget: QtWidgets.QProgressBar) -> None:
        super(RenderProgressLogger, self).__init__()
        self.__progressbar_widget = progressbar_widget

        self.__progressbar_widget.setMinimum(0)

    # def callback(self, **changes):
    #     for parameter, new_value in changes.items():
    #         print(">>", new_value)
    # self.__progressbar_widget.setFormat(new_value)

    def bars_callback(self, bar, attr, value, old_value=None) -> None:
        render_text: str = "Video" if bar == "t" else "Audio"

        self.__progressbar_widget.setFormat(f"Rendering {render_text}... %p%")

        if attr == "total":
            self.__progressbar_widget.setMaximum(value)
        elif attr == "index":
            self.__progressbar_widget.setValue(value)


class RenderVideo(object):
    def __init__(
            self,
            video_path: str,
            intro_file: str = None,
            outro_file: str = None,
            video_format: str = "webm",
            size: tuple = None,
            fps: int = config.VIDEO_FPS,
            bg_blur: bool = False
    ):
        if size is None:
            size = config.VIDEO_RESOLUTION.resolution(config.VIDEO_RESOLUTION.R720P)
        self.__video_path: str = video_path
        self.__intro_file: str = intro_file
        self.__outro_file: str = outro_file
        self.__video_format: str = video_format
        self.__size: tuple = size
        self.__fps: int = fps
        self.__bg_blur: bool = bg_blur

        self.__size = self.__size if self.__size else config.VIDEO_RESOLUTION.resolution(config.VIDEO_RESOLUTION.R720P)

        self.__video_name: str = os.path.basename(self.__video_path).replace(" ", "_").lower()
        self.__output_file: str = f"{config.VIDEO_PATH}/{self.__video_name}.{self.__video_format}"

    @property
    def size(self) -> tuple:
        return self.__size

    @size.setter
    def size(self, size: tuple) -> None:
        self.__size = size

    @property
    def video_format(self) -> str:
        return self.__video_format

    @property
    def video_file(self) -> str:
        return self.__output_file

    @property
    def fps(self) -> int:
        return self.__fps

    @property
    def duration(self) -> datetime.timedelta:
        duration = self.create_video_clip().duration
        return datetime.timedelta(seconds=duration)

    @property
    def frames(self) -> np.ndarray:
        fr_time: float = 1.0 / self.__fps
        return np.arange(0, self.duration - 0.001, fr_time)

    @property
    def frame_count(self) -> int:
        return len(self.frames)

    def set_size(self, width: int, height: int, reduce: int = None) -> None:
        size: List[int] = []
        for i, s in enumerate([width, height]):
            if reduce:
                s = s / reduce
            size.insert(i, int(s))

        self.__size = size

    def get_video_files(self) -> List[str]:
        video_files: List[str] = []

        for vid in os.listdir(self.__video_path):
            video_file = config.join_directory(self.__video_path, vid)
            if os.path.isfile(video_file):
                ext = os.path.splitext(video_file)[1].replace(".", "").lower()
                if ext in ["mp4", self.__video_format]:
                    video_files.append(video_file)

        if self.__intro_file:
            video_files.insert(0, self.__intro_file)

        if self.__outro_file:
            video_files.append(self.__outro_file)

        return video_files

    def create_video_clip(self, size: List[int] = None) -> editor.VideoClip:
        file_clips: List[str] = []
        width, height = size if size else self.__size

        for v in self.get_video_files():
            file_clip = (editor.VideoFileClip(v)
                         .resize(height=height))

            file_clips.append(file_clip)

        video_clip = (editor.concatenate_videoclips(
            file_clips,
            method="compose")
                      .set_position(("center", "center")))

        return video_clip

    def create_logo(self, logo_file: str = None) -> editor.VideoClip:
        logo_file: str = logo_file if logo_file else config.join_directory(config.ASSETS_PATH, "logo.png")
        logo_clip: editor.ImageClip = (editor.ImageClip(logo_file)
                                       .set_duration(self.create_video_clip().duration)
                                       .resize(height=self.__size[1] / 6)
                                       # .margin(left=15, right=15, top=15, bottom=15, opacity=0)
                                       .set_position(("left", "top")))

        return logo_clip

    def render_video(self, bitrate: int = 1000, threads: int = 4,
                     progressbar_widget: QtWidgets.QProgressBar = None) -> tuple:
        clips: List[Any] = [self.create_video_clip(), self.create_logo()]

        render_logger: Any = "bar"
        if progressbar_widget:
            render_logger = RenderProgressLogger(
                progressbar_widget=progressbar_widget
            )

        if self.__bg_blur:
            clips.insert(0, self.__create_blur_video_clip())

        composite_video_clip: editor.CompositeVideoClip = editor.CompositeVideoClip(
            clips,
            size=self.__size
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_video_file: str = f"{tmpdir}/{self.__video_name}.{self.__video_format}"
            temp_audio_file: str = f"{tmpdir}/{self.__video_name}.ogg"

            composite_video_clip.write_videofile(
                temp_video_file,
                temp_audiofile=temp_audio_file,
                fps=self.__fps,
                bitrate=f"{bitrate}k",
                threads=threads,
                preset="ultrafast",
                logger=render_logger
            )

            shutil.copyfile(temp_video_file, self.__output_file)
            composite_video_clip.close()

        return self.__output_file, composite_video_clip

    def get_frame_image(self, label_widget: QtWidgets.QLabel) -> Any:
        final_clip = self.__create_final_video()

        for fr in self.frames:
            image = im2array.array2qimage(final_clip.get_frame(fr))
            yield label_widget.setPixmap(QtGui.QPixmap.fromImage(image))

        final_clip.close()

    def get_frame_img_array(self) -> Any:
        final_clip = self.__create_final_video()

        for fr in self.frames:
            yield final_clip.get_frame(fr)

        final_clip.close()

    def __create_final_video(self) -> editor.CompositeVideoClip:
        clips: List[Any] = [self.create_video_clip(), self.create_logo()]

        if self.__bg_blur:
            clips.insert(0, self.__create_blur_video_clip())

        final_video_clip: editor.CompositeVideoClip = editor.CompositeVideoClip(
            clips,
            size=self.__size
        )

        return final_video_clip

    def __create_blur_video_clip(self) -> editor.VideoClip:
        file_clips: List[str] = []

        for v in self.get_video_files():
            video_file = (editor.VideoFileClip(
                v,
                audio=False,
                target_resolution=self.__size,
                resize_algorithm="fast_bilinear"
            )
                          .resize(self.__size))
            file_clips.append(video_file)

        blur_clip = editor.concatenate_videoclips(file_clips).fl_image(_blur_fx)

        return blur_clip

    #
    # def create_video(
    #         video_path: str,
    #         video_format: str = "webm",
    #         size: list = [config.VIDEO_WIDTH, config.VIDEO_HEIGHT],
    #         fps=config.VIDEO_FPS
    # ) -> str:
    #     video_name = os.path.basename(video_path).replace(" ", "_").lower()
    #     output_path: str = f"{config.VIDEO_UPLOAD_PATH}/{video_name}.{video_format}"
    #     video_file_clips: list = []
    #     video_file_blur_fx_clips: list = []
    #
    #     for f in os.listdir(video_path):
    #         clip: meditor.VideoFileClip = meditor.VideoFileClip(
    #             os.path.join(video_path, f),
    #             # target_resolution=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT)
    #         )
    #         # .resize(height=config.VIDEO_HEIGHT))
    #
    #         width, height = clip.size
    #
    #         if width < 1280 / 2 and width > height:
    #             height_resize = config.VIDEO_HEIGHT / 1.2
    #         else:
    #             height_resize = config.VIDEO_HEIGHT
    #
    #         clip = clip.resize(height=height_resize)
    #
    #         video_file_clips.append(clip)
    #
    #         blur_clip: meditor.VideoFileClip = (meditor.VideoFileClip(
    #             os.path.join(video_path, f),
    #             audio=False,
    #             resize_algorithm="fast_bilinear"
    #         )
    #                                             .resize(width=config.VIDEO_WIDTH))
    #
    #         video_file_blur_fx_clips.append(blur_clip)
    #
    #     video_clip: meditor.VideoClip = (meditor.concatenate_videoclips(
    #         video_file_clips,
    #         method="compose"
    #     )
    #                                      .set_pos(("center", "center")))
    #
    #     video_blur_fx_clip: meditor.VideoClip = meditor.concatenate_videoclips(video_file_blur_fx_clips).fl_image(
    #         _blur_fx)
    #
    #     watermark: meditor.ImageClip = (meditor.ImageClip(config.join_directory(config.ASSETS_PATH, "logo.png"))
    #                                     .set_duration(video_clip.duration)
    #                                     .resize(height=100)
    #                                     .margin(left=15, right=15, top=15, bottom=15, opacity=0)
    #                                     .set_position(("left", "top")))
    #
    #     final_video_clip: meditor.CompositeVideoClip = meditor.CompositeVideoClip(
    #         [video_blur_fx_clip, video_clip, watermark],
    #         size=[config.VIDEO_WIDTH, config.VIDEO_HEIGHT],
    #     )
    #
    #     final_video_clip.write_videofile(
    #         output_path,
    #         fps=config.VIDEO_FPS,
    #         bitrate="1000k",
    #         threads=4,
    #         preset="ultrafast"
    #     )
    #
    #     final_video_clip.close()
    #
    #     return output_path

# video1 = editor.VideoFileClip("/home/wongselent/Videos/WMG_PROFILE_PIC_2317623821785467907.mp4")
# video2 = editor.VideoFileClip("/home/wongselent/Videos/wml_vid_CAqmN_wA7yl.mp4")

# final_video = editor.concatenate_videoclips([video1, video2])
# final_video.write_videofile(
#     "/home/wongselent/Videos/final_render.mp4",
#     ffmpeg_params=['-lavfi', '[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma


# video1 = editor.VideoFileClip("/home/wongselent/Videos/WMG_PROFILE_PIC_2317623821785467907.mp4")
# video2 = editor.VideoFileClip("/home/wongselent/Videos/wml_vid_CAqmN_wA7yl.mp4")

# final_video = editor.concatenate_videoclips([video1, video2])
# final_video.write_videofile(
#     "/home/wongselent/Videos/final_render.mp4",
#     ffmpeg_params=['-lavfi', '[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16']
# )


# import moviepy.editor as mp

# video = mp.VideoFileClip("video.mp4")

# logo = (mp.ImageClip("logo.png")
#           .set_duration(video.duration)
#           .resize(height=50) # if you need to resize...
#           .margin(right=8, top=8, opacity=0) # (optional) logo-border padding
#           .set_pos(("right","top")))

# final = mp.CompositeVideoClip([video, logo])
# final.write_videofile("test.mp4"

# video = mp.VideoFileClip(video_file_path)

# watermark = (mp.ImageClip(watermark_file_path)
#              .set_duration(video.duration)
#              .resize(watermark_size)
#              .margin(left=8, right=8, top=8, bottom=8, opacity=0)
#              .set_pos((first_position, second_position)))

# final_video = mp.CompositeVideoClip([video, watermark])
