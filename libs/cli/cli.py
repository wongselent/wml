"""
Usage:
    wml-tool [JSON_FILE]

Arguments:



Options:
  -h --help

Examples:   

"""

from docopt import docopt


if __name__ == '__main__':
    __loot_arguments = docopt(__doc__)


# """
# Usage:
#     wml-tool [instagram SOCIAL] [--loot-profile=PROFILE_NAME | --loot-hashtag=HASHTAG_NAME] [--loot-type=LOOT_TYPE] [--loot-count=LOOT_COUNT]


# Arguments:
#   instagram     instagram


# Options:
#   -h --help
#   --loot-type=LOOT_TYPE       0: picture, 1: video
#   --loot-count=LOOT_COUNT     require interger not decimal number


# Examples:
#   wml-tool instagram --loot-profile="meme.comik.indonesia,memekamvret" --loot-type=0 --loot-count=3
#   wml-tool instagram --loot-hashtag="cat,dog" --loot-type=0 --loot-count=3

# """
# from docopt import docopt
# from addict import Dict
# from libs import instagram
# from libs.setting import SOCIAL_TYPES, DIRECTORIES

# import re


# def __get_instagram_argument():
#   pass

# def __str2List(string: str):
#   if string:
#     return re.sub(r"\s", "", string).split(",")

# if __name__ == '__main__':
#     __loot_arguments = docopt(__doc__)
#     if __loot_arguments["instagram"] or __loot_arguments["SOCIAL"] == SOCIAL_TYPES._str[SOCIAL_TYPES.IG]:
#       additional_options = Dict(
#         loot_type=int(__loot_arguments["--loot-type"]),
#         loot_count=int(__loot_arguments["--loot-count"])
#       )

#       loot_profile: str = __loot_arguments["--loot-profile"]
#       loot_hashtag: str = __loot_arguments["--loot-hashtag"]

#       if loot_profile:
#         for name in __str2List(loot_profile):
#           print(f"Looting from {name} profile:")

#           instagram.loot_profile(
#             name,
#             **additional_options
#           )
#       elif loot_hashtag:
#         for name in __str2List(loot_hashtag):
#           print(f"Looting from {name} hashtag:")

#           instagram.loot_hashtag(
#             name,
#             **additional_options
#           )

#       print("=== END ===")