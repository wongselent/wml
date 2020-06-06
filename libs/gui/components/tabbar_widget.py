from PyQt5.QtWidgets import QTabBar, QTabWidget, QWidget, QSpacerItem, QVBoxLayout

class TabBar(QTabBar):
    def __init__(self, parent: QTabWidget, tab_title: str = None) -> None:
        super(TabBar, self).__init__(parent)
        self.__parent = parent
        self.__tab_title = tab_title
        self.__tabbar_layout: QVBoxLayout = QVBoxLayout()

        self.setObjectName(self.__tab_title.replace(" ", "_").lower())
        self.setLayout(self.__tabbar_layout)

        self.__parent.addTab(self, self.__tab_title)
        # self.main_tabwidget.addTab(self.__tab_page, "page 1")

    def addWidget(self, widget: QWidget) -> None:
        self.__tabbar_layout.addWidget(widget)
        
        # if not expand:
        #     vspacer: QSpacerItem = QSpacerItem(0, 1000)
        #     self.__tabbar_layout.addSpacerItem(vspacer)