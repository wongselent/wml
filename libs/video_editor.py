from . import setting
from moviepy.editor import VideoClip, VideoFileClip, CompositeVideoClip, concatenate_videoclips, ImageClip
from skimage.filters import gaussian

import os

def __blur(image):
    return gaussian(image.astype(float), sigma=8)

def create_video(video_path: str, video_format: str = "mp4") -> str:
    video_name = os.path.basename(video_path).replace(" ", "_").lower()
    output_path: str = f"{setting.VIDEO_UPLOAD_PATH}/{video_name}.{video_format}"
    video_file_clips: list = []
    video_file_blur_clips: list = []

    for f in os.listdir(video_path):
        clip: VideoFileClip = VideoFileClip(
                os.path.join(video_path, f),
            # target_resolution=(setting.VIDEO_WIDTH, setting.VIDEO_HEIGHT)
            )
            # .resize(height=setting.VIDEO_HEIGHT))

        width, height = clip.size

        if width < 1280/2 and width > height:
            height_resize = setting.VIDEO_HEIGHT/1.2
        else:
            height_resize = setting.VIDEO_HEIGHT

        clip = clip.resize(height=height_resize)
        
        video_file_clips.append(clip)

        blur_clip: VideoFileClip = (VideoFileClip(
                os.path.join(video_path, f),
                audio=False,
                resize_algorithm="fast_bilinear"
            )
            .resize(width=setting.VIDEO_WIDTH))

        video_file_blur_clips.append(blur_clip)

    video_clip: VideoClip = (concatenate_videoclips(
            video_file_clips,
            method="compose"
        )
        .set_pos(("center", "center")))

    video_blur_clip: VideoClip = concatenate_videoclips(video_file_blur_clips).fl_image(__blur)
    
    watermark: ImageClip = (ImageClip(setting.join_directory(setting.ASSETS_PATH, "logo.png"))
                 .set_duration(video_clip.duration)
                 .resize(height=100)
                 .margin(left=15, right=15, top=15, bottom=15, opacity=0)
                 .set_position(("left", "top")))

    final_video_clip: CompositeVideoClip = CompositeVideoClip(
        [video_blur_clip, video_clip, watermark],
        size=[setting.VIDEO_WIDTH, setting.VIDEO_HEIGHT]
        )

    final_video_clip.write_videofile(
        output_path,
        fps=30,
        bitrate="1000k",
        threads=4,
        preset="ultrafast"
    )

    final_video_clip.close()
    
    return 
    



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