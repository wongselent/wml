from PyQt5 import QtWidgets

from libs import config
from libs.gui.components import form_widget


class SocialLooterWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(SocialLooterWidget, self).__init__(parent)
        config.load_ui(self)
        self.__parent = parent
        self.__instagram_group_form = form_widget.GroupFormWidget(
            self,
            "Instagram",
            [
                form_widget.LooterFormWidget(self, "Profile"),
                form_widget.LooterFormWidget(self, "Hashtag")
            ]
        )
        self.__9gag_group_form = form_widget.GroupFormWidget(self, "9Gag")

        self.append_widget(
            self.__instagram_group_form,
            self.__9gag_group_form
        )
        # self.loot_button.clicked.connect(self.runLoot)

    def append_widget(self, *widgets) -> None:
        for widget in widgets:
            self.social_form_layout.addWidget(widget)


class InstagramLooterWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(InstagramLooterWidget, self).__init__(parent)
        config.load_ui(self)

        self.__parent = parent


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