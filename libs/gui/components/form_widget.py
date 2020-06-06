from libs import config

from PyQt5 import QtWidgets

class Form(QtWidgets.QFrame):
    def __init__(self, parent: QtWidgets.QWidget, label_form: str = None, placeholder: str = None) -> None:
        super(Form, self).__init__()
        config.load_ui(self)

        self.__parent = parent
        self.__label_form = label_form  + ":"
        self.__placeholder = placeholder
    
        self.form_label.setText(self.__label_form)
        # self.form_edit.setPlaceHolder(placeholder)

class LooterFormWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, name: str, placeholder: str = None) -> None:
        super(LooterFormWidget, self).__init__(parent)
        config.load_ui(self)
        self.__parent = parent
        
        self.form_check: QtWidgets.QCheckBox
        self.form_input_edit: QtWidgets.QLineEdit

        self.form_check.clicked.connect(self._setToogleInput)

    @property
    def checked(self):
        self.form_check.isChecked()
    
    @checked.setter
    def checked(self, value):
        self.form_check.setChecked(value)

    def showEvent(self, event):
        self._setToogleInput()

    def _setToogleInput(self):
        self.form_input_edit.setEnabled(self.form_check.isChecked())



class GroupForm(QtWidgets.QGroupBox):
    def __init__(self, parent: QtWidgets.QWidget, title_group: str = None, form_objs: list = []) -> None:
        super(GroupForm, self).__init__(parent)
        config.load_ui(self)

        self.__parent = parent
        self.__title_group = title_group + ":"
        self.__form_objs = form_objs

        self.setTitle(self.__title_group)

        self.addForms(*self.__form_objs)


    def addForms(self, *args) -> None:
        for obj in args:
            if type(obj) == Form:
                self.group_form_layout.addWidget(obj)
        
        # spacer: QSpacerItem = QSpacerItem(0, 1000)
        
        # self.group_form_layout.addSpacerItem(spacer)
        # self.group_form_layout.add
        # v = QVBoxLayout()
        # v.

class GroupFormWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, title: str = None, widgets: list = None) -> None:
        super(GroupFormWidget, self).__init__(parent)
        config.load_ui(self)
        self.__parent = parent
        self.__title = title + ":"
        self.__widgets = widgets

        self.form_group: QtWidgets.QGroupBox
        self.form_group_layout: QtWidgets.QVBoxLayout

        self.form_group.setTitle(self.__title)
        
        if self.__widgets:
            self.addWidget(*self.__widgets)

    
    def addWidget(self, *widgets) -> None:
        for widget in widgets:
            self.form_group_layout.addWidget(widget)
    
