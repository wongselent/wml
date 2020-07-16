from .. import config
from typing import List, Dict
from instaloader import Instaloader, Profile, Hashtag, Post

import itertools

__setup_looter: Instaloader = Instaloader(
    dirname_pattern=config.OUTPUT_PATH,
    download_videos=True,
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=False,
    save_metadata=False,
    compress_json=False,
    post_metadata_txt_pattern=""
)


def login(username: str, password: str) -> bool:
    try:
        __setup_looter.login(username, password)
    except Exception as ex:
        return False
    else:
        return True


def test_login() -> str:
    return __setup_looter.test_login()


def __set_pattern(loot_type: int, looter_name: str, social_dir: str) -> None:
    __setup_looter.dirname_pattern = config.join_directory(
        social_dir,
        config.MEDIA_TYPES.str(loot_type)
    )

    __setup_looter.filename_pattern = config.FILENAME_PATTERN.format(
        social=config.SOCIAL_TYPES.str(config.SOCIAL_TYPES.IG),
        looter=looter_name,
        media_type=config.MEDIA_TYPES.code(loot_type),
        username="{owner_username}",
        name="{shortcode}"
    )


def __download_from_posts(posts: Post, loot_type: int, loot_max_count: int, loot_total_count: int) -> None:
    __setup_looter.posts_download_loop(
        posts,
        config.OUTPUT_PATH,
        fast_update=True,
        max_count=loot_max_count,
        total_count=loot_total_count,    
        post_filter=lambda post: not post.is_video if loot_type == config.MEDIA_TYPES.PIC else post.is_video
    )

    # count_downloaded = 0

    # if loot_type != config.MEDIA_TYPES.PIC:
    #     __SETUP_LOOTER.download_videos = True
    
    # while count_downloaded < 20:
    #     count_downloaded += 1
        
    #     print(next(posts))


    # for post in posts:
        # if count_downloaded < loot_count:
        #     count_downloaded += 1
            # print(__SETUP_LOOTER.download_videos, post.is_video)
        # print(post.typename)            
        # if __SETUP_LOOTER.download_videos == post.is_video:
        #     print(post.typename)
        # else:
        #     print(post.typename, 0)

        #     if post.is_video:
        #         __SETUP_LOOTER.download_post(post)
    

def loot_profile(profile_name: str, loot_type: int = config.MEDIA_TYPES.PIC, loot_max_count: int = 1, loot_total_count: int = 100) -> Profile:
    __set_pattern(loot_type, "profile", config.SOCIAL_TYPES._dir[config.SOCIAL_TYPES.IG]["profile"], "{owner_username}")

    profile: Profile = Profile.from_username(__setup_looter.context, profile_name)
    posts: Post = profile.get_posts()

    __download_from_posts(posts, loot_type, loot_max_count, loot_total_count)

    return profile

def loot_hashtag(hashtag_name: str, loot_type: int = config.MEDIA_TYPES.PIC, loot_max_count: int = 1, loot_total_count: int = 100) -> Hashtag:
    __set_pattern(loot_type, "hashtag", config.OUTPUT_PATH, hashtag_name)

    hashtag: Hashtag = Hashtag.from_name(__setup_looter.context, hashtag_name)
    posts: Post = hashtag.get_top_posts()

    __download_from_posts(posts, loot_type, loot_max_count, loot_total_count)

    return hashtag

def loot_topsearch(loot_type: int = config.MEDIA_TYPES.PIC, loot_count: int = 1, loot_total_count: int = 100):
    pass
