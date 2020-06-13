import os
import shutil
import tempfile

import moviepy.editor as meditor
import numpy as np
import proglog
import qimage2ndarray as im2array
from PyQt5 import QtGui, QtWidgets
from skimage import filters

from libs import config


# tempfile.tempdir

def _blur_fx(image):
    return filters.gaussian(image.astype(float), sigma=8)


class RenderProgressLogger(proglog.ProgressBarLogger):
    def callback(self, **changes):
        for (parameter, new_value) in changes.items():
            print(parameter, new_value)


class RenderVideo():
    def __init__(
            self,
            video_path,
            intro_file: str = None,
            outro_file: str = None,
            video_format: str = "webm",
            size=None,
            fps: int = config.VIDEO_FPS,
            bg_blur: bool = False
    ):
        if size is None:
            size = [config.VIDEO_WIDTH, config.VIDEO_HEIGHT]
        self.__video_path = video_path
        self.__intro_file = intro_file
        self.__outro_file = outro_file
        self.__video_format = video_format
        self.__size = size
        self.__fps = fps
        self.__bg_blur = bg_blur

        self.__size = self.__size if self.__size else [config.VIDEO_WIDTH, config.VIDEO_HEIGHT]

        self.__video_name: str = os.path.basename(self.__video_path).replace(" ", "_").lower()
        self.__output_file: str = f"{config.VIDEO_UPLOAD_PATH}/{self.__video_name}.{self.__video_format}"

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        self.__size = value

    @property
    def video_format(self):
        return self.__video_format

    @property
    def fps(self):
        return self.__fps

    @property
    def duration(self):
        return self.__createFinalVideo().duration

    @property
    def frames(self):
        fr_time: float = 1.0 / self.__fps
        return np.arange(0, self.duration - 0.001, fr_time)

    def set_size(self, width: int, height: int, reduce: int = None):
        size: list = []
        for i, s in enumerate([width, height]):
            if reduce:
                s = s / reduce
            if s < 150:
                raise Exception(f"size {s}, under 150. Minimum size 150!")
            size.insert(i, int(s))

        self.__size = size

    def get_video_files(self) -> list:
        video_files: list = []

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

    def create_video_clip(self, size: list = None) -> meditor.VideoClip:
        file_clips: list = []
        width, height = size if size else self.__size

        for v in self.get_video_files():
            file_clip = (meditor.VideoFileClip(v)
                         .resize(height=height))

            file_clips.append(file_clip)

        video_clip = (meditor.concatenate_videoclips(
            file_clips,
            method="compose")
                      .set_position(("center", "center")))

        return video_clip

    def create_logo(self, logo_file: str = None) -> meditor.ImageClip:
        logo_file = logo_file if logo_file else config.join_directory(config.ASSETS_PATH, "logo.png")
        logo_clip = (meditor.ImageClip(logo_file)
                     .set_duration(self.create_video_clip().duration)
                     .resize(height=self.__size[1] / 6)
                     .margin(left=15, right=15, top=15, bottom=15, opacity=0)
                     .set_position(("left", "top")))

        return logo_clip

    def render_video(self, bitrate: int = 1000, threads: int = 4, logger: proglog.ProgressBarLogger = None) -> tuple:
        clips: list = [self.create_video_clip(), self.create_logo()]
        render_logger = RenderProgressLogger()

        if self.__bg_blur:
            clips.insert(0, self.__createBlurVideoClip())

        composite_video_clip = meditor.CompositeVideoClip(
            clips,
            size=self.__size
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_video_file = f"{tmpdir}/{self.__video_name}.{self.__video_format}"
            temp_audio_file = f"{tmpdir}/{self.__video_name}.ogg"

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

        results: tuple = (self.__output_file, composite_video_clip)

        return results

    def get_frame_image(self, qlabel: QtWidgets.QLabel, debug=False):
        final_clip = self.__createFinalVideo()

        for fr in self.frames:
            image = im2array.array2qimage(final_clip.get_frame(fr))
            if debug: print(fr, image)
            yield qlabel.setPixmap(QtGui.QPixmap.fromImage(image))

        final_clip.close()

    def get_frame_img_array(self, debug=False):
        final_clip = self.__createFinalVideo()

        for fr in self.frames:
            if debug:
                print(fr)
            yield final_clip.get_frame(fr)

        final_clip.close()

    def __createFinalVideo(self) -> meditor.CompositeVideoClip:
        clips: list = [self.create_video_clip(), self.create_logo()]

        if self.__bg_blur:
            clips.insert(0, self.__createBlurVideoClip())

        final_video_clip = meditor.CompositeVideoClip(
            clips,
            size=self.__size
        )

        return final_video_clip

    def __createBlurVideoClip(self) -> meditor.VideoClip:
        file_clips: list = []

        for v in self.get_video_files():
            video_file = (meditor.VideoFileClip(
                v,
                audio=False,
                target_resolution=self.__size,
                resize_algorithm="fast_bilinear"
            )
                          .resize(self.__size))
            file_clips.append(video_file)

        blur_clip = meditor.concatenate_videoclips(file_clips).fl_image(_blur_fx)

        return blur_clip


def create_video(
        video_path: str,
        video_format: str = "webm",
        size: list = [config.VIDEO_WIDTH, config.VIDEO_HEIGHT],
        fps=config.VIDEO_FPS
) -> str:
    video_name = os.path.basename(video_path).replace(" ", "_").lower()
    output_path: str = f"{config.VIDEO_UPLOAD_PATH}/{video_name}.{video_format}"
    video_file_clips: list = []
    video_file_blurFX_clips: list = []

    for f in os.listdir(video_path):
        clip: meditor.VideoFileClip = meditor.VideoFileClip(
            os.path.join(video_path, f),
            # target_resolution=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT)
        )
        # .resize(height=config.VIDEO_HEIGHT))

        width, height = clip.size

        if width < 1280 / 2 and width > height:
            height_resize = config.VIDEO_HEIGHT / 1.2
        else:
            height_resize = config.VIDEO_HEIGHT

        clip = clip.resize(height=height_resize)

        video_file_clips.append(clip)

        blur_clip: meditor.VideoFileClip = (meditor.VideoFileClip(
            os.path.join(video_path, f),
            audio=False,
            resize_algorithm="fast_bilinear"
        )
                                            .resize(width=config.VIDEO_WIDTH))

        video_file_blurFX_clips.append(blur_clip)

    video_clip: meditor.VideoClip = (meditor.concatenate_videoclips(
        video_file_clips,
        method="compose"
    )
                                     .set_pos(("center", "center")))

    video_blurFX_clip: meditor.VideoClip = meditor.concatenate_videoclips(video_file_blurFX_clips).fl_image(_blur_fx)

    watermark: meditor.ImageClip = (meditor.ImageClip(config.join_directory(config.ASSETS_PATH, "logo.png"))
                                    .set_duration(video_clip.duration)
                                    .resize(height=100)
                                    .margin(left=15, right=15, top=15, bottom=15, opacity=0)
                                    .set_position(("left", "top")))

    final_video_clip: meditor.CompositeVideoClip = meditor.CompositeVideoClip(
        [video_blurFX_clip, video_clip, watermark],
        size=[config.VIDEO_WIDTH, config.VIDEO_HEIGHT],
    )

    final_video_clip.write_videofile(
        output_path,
        fps=config.VIDEO_FPS,
        bitrate="1000k",
        threads=4,
        preset="ultrafast"
    )

    final_video_clip.close()

    return output_path

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
