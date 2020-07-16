from typing import List

from PyQt5 import QtWidgets

from libs import config
from libs.socials import  instagram


class InstagramLooterWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(InstagramLooterWidget, self).__init__(parent)
        config.load_ui(self)

        self.__parent = parent

        self.loot_button.clicked.connect(self.start_looting)

    def start_looting(self) -> None:
        profile_list: List[str] = config.set_plaintext_to_list(self.profile_text)
        print(profile_list)

        hashtag_list: List[str] = config.set_plaintext_to_list(self.hashtag_text)
        print(hashtag_list)

        if hashtag_list:
            for hashtag in hashtag_list:
                instagram.loot_hashtag(hashtag, config.MEDIA_TYPES.VID, 50)

    # @property
    # def social_values(self) -> dict:
    #     data = {
    #         config.SOCIAL_TYPES.IG: {
    #             "profiles": config.setStringToList(self.ig_profile_edit.text()),
    #             "hashtag": config.setStringToList(self.ig_hashtag_edit.text())
    #         }
    #     }

    #     return data

    # def runLoot(self) -> None:
    #     self.setEnabled(False)

    #     self.instagramLooter(
    #         self.social_values[config.SOCIAL_TYPES.IG]["profiles"],
    #         self.social_values[config.SOCIAL_TYPES.IG]["hashtag"]
    #     )

    #     self.setEnabled(True)

    # def instagramLooter(self, profiles: list, hashtags: list) -> None:
    #     print("== Start Instagram Looting == ")

    #     if self.ig_groupbox.isChecked():
    #         if self.ig_profile_check.isChecked() and profiles:
    #             for profile in profiles:
    #                 try:
    #                     instagram.loot_profile(profile)
    #                 except Exception as ex:
    #                     print(ex)
    #                     return

    #         if self.ig_hashtag_check.isChecked() and hashtags:
    #             for hashtag in hashtags:
    #                 try:
    #                     instagram.loot_hashtag(hashtag)
    #                 except Exception as ex:
    #                     print(ex)
    #                     return

    #     print("== Instagram Looting End. == ")
