import os
import sys
from typing import List, Dict, Iterator, Callable, Optional

from instaloader import Instaloader, Hashtag, Post, exceptions

from .. import config

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
        media_name="{shortcode}",
        date="{date}"
    )


def __download_from_posts(posts: Iterator[Post], loot_type: int, max_count: int, search_count: int = 10,
                          callback: Optional[Callable[[Post], bool]] = None) -> None:
    # current_date: datetime.date = datetime.datetime.now().date()
    downloaded_count: int = 0

    for num, post in enumerate(posts):
        history_pattern: str = config.HISTORY_DOWNLOADED_PATTERN.format(
            social=config.SOCIAL_TYPES.str(config.SOCIAL_TYPES.IG),
            date=post.date.date()
        )

        history_file: str = config.join_directory(config.HISTORY_DOWNLOADED_PATH, history_pattern)

        if not os.path.exists(history_file):
            config.write_json_file(history_file, config.MEDIA_TYPES.history_pattern)

        downloaded_data: Dict[str, List[str]] = config.read_json_file(history_file)

        if downloaded_count == max_count:
            break

        post_is_video: bool = not post.is_video if loot_type == config.MEDIA_TYPES.PIC else post.is_video

        if post_is_video:
            media_url: str = post.url
            while True:
                try:
                    if media_url not in downloaded_data[
                        config.MEDIA_TYPES.str(config.MEDIA_TYPES.VID)
                    ]:
                        __setup_looter.download_post(post, config.OUTPUT_PATH)
                        downloaded_count += 1
                        downloaded_data[config.MEDIA_TYPES.str(config.MEDIA_TYPES.VID)].append(media_url)
                        from tqdm import tqdm
                        callback(post)
                        print(f"[ {downloaded_count}/{max_count} | {num}/{search_count} ]:"
                              f" {post.mediaid} - {post.date.date()} | Downloading..")
                    else:
                        print(f"{post.mediaid} - {post.date.date()} | Media is Downloaded!!!")
                    break
                except Exception as ex:
                    print("Error", sys.exc_info())
                    continue

            config.write_json_file(history_file, downloaded_data)

            if num >= search_count:
                print("max searching count")
                break


# def loot_profile(profile_name: str, loot_type: int = config.MEDIA_TYPES.PIC, loot_max_count: int = 1, loot_total_count: int = 100) -> Profile:
#     __set_pattern(loot_type, "profile", config.SOCIAL_TYPES._dir[config.SOCIAL_TYPES.IG]["profile"], "{owner_username}")
#
#     profile: Profile = Profile.from_username(__setup_looter.context, profile_name)
#     posts: Iterator[Post] = profile.get_posts()
#
#     __download_from_posts(posts, loot_type, loot_max_count, loot_total_count)
#
#     return profile


def loot_hashtag(hashtag_name: str, loot_type: int = config.MEDIA_TYPES.PIC, max_count: int = 1,
                 search_count: int = 10, callback: Optional[Callable[[Post], bool]] = None) -> None:
    __set_pattern(loot_type, "hashtag", config.OUTPUT_PATH)

    try:
        hashtag: Hashtag = Hashtag.from_name(__setup_looter.context, hashtag_name)
        posts: Iterator[Post] = hashtag.get_all_posts()
        __download_from_posts(posts, loot_type, max_count, search_count, callback)
    except exceptions.QueryReturnedNotFoundException:
        print(f"Hashtag: \"{hashtag_name}\" Not Found!!!")
        return


def loot_topsearch(loot_type: int = config.MEDIA_TYPES.PIC, loot_count: int = 1, loot_total_count: int = 100):
    pass
