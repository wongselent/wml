from .. import setting, tool

from instaloader import Instaloader, Profile, Hashtag, Post

import itertools

# class DIRNAME_PATTERNS:
#     PROFILE:str = lambda loot_type: join_directory(SOCIAL_TYPES._dir[SOCIAL_TYPES.IG].PROFILE, "{owner_username}", loot_type)

# class FILENAME_PATTERNS:
#     PROFILE:str = lambda media_code: f"{PPREFIX}_PROFILE_{media_code}_{{shortcode}}"

__SETUP_LOOTER: Instaloader = Instaloader(
    dirname_pattern = setting.OUTPUT_PATH,
    download_videos = False,
    download_video_thumbnails = False,
    download_geotags = False,
    download_comments = False,
    save_metadata = False,
    compress_json = False,
    post_metadata_txt_pattern = ""
)

def login(username: str, password: str) -> bool:
    try:
        __SETUP_LOOTER.login(username, password)
    except Exception as ex:
        return False
    else:
        return True

def test_login() -> str:
    return __SETUP_LOOTER.test_login()

def __set_pattern(loot_type:int, social_dir:str, *args) -> None:
    __SETUP_LOOTER.dirname_pattern: str = tool.join_directory(social_dir, *args, setting.MEDIA_TYPES._str[loot_type])
    __SETUP_LOOTER.filename_pattern: str = f"{setting.PPREFIX}--{setting.MEDIA_TYPES._code[loot_type]}--{{owner_username}}--{{shortcode}}"

def __download_from_posts(posts: Post, loot_type: int, loot_max_count: int, loot_total_count: int) -> None:
    __SETUP_LOOTER.posts_download_loop(
        posts,
        setting.OUTPUT_PATH,
        fast_update=True,
        max_count=loot_max_count,
        total_count=loot_total_count
        post_filter=lambda post: not post.is_video if loot_type == setting.MEDIA_TYPES.PIC else post.is_video
    )
    # count_downloaded = 0

    # if loot_type != setting.MEDIA_TYPES.PIC:
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
    

def loot_profile(profile_name: str, loot_type: int = setting.MEDIA_TYPES.PIC, loot_count: int = 1, loot_total_count: int = 100) -> Profile:
    __set_pattern(loot_type, setting.SOCIAL_TYPES._dir[setting.SOCIAL_TYPES.IG]["profile"], "{owner_username}")

    profile: Profile = Profile.from_username(__SETUP_LOOTER.context, profile_name)
    posts: Post = profile.get_posts()

    __download_from_posts(posts, loot_type, loot_count, loot_total_count)

    return profile

def loot_hashtag(hashtag_name: str, loot_type: int = setting.MEDIA_TYPES.PIC, loot_count: int = 1, loot_total_count: int = 100) -> Hashtag:
    __set_pattern(loot_type, setting.SOCIAL_TYPES._dir[setting.SOCIAL_TYPES.IG]["hashtag"], hashtag_name)

    hashtag: Hashtag = Hashtag.from_name(__SETUP_LOOTER.context, hashtag_name)
    posts: Post = hashtag.get_top_posts()

    __download_from_posts(posts, loot_type, loot_count, loot_total_count)

    return hashtag

def loot_topsearch(loot_type: int = setting.MEDIA_TYPES.PIC, loot_count: int = 1, loot_total_count: int = 100):
    pass
