from PyQt5 import QtWidgets

from libs import config


class Form(QtWidgets.QFrame):
    def __init__(self, parent: QtWidgets.QWidget, label_form: str = None, placeholder: str = None) -> None:
        super(Form, self).__init__()
        config.load_ui(self)

        self.__parent = parent
        self.__label_form = label_form + ":"
        self.__placeholder = placeholder

        self.form_label.setText(self.__label_form)
        # self.form_edit.setPlaceHolder(placeholder)


class LooterFormWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, input_title: str, placeholder: str = None) -> None:
        super(LooterFormWidget, self).__init__(parent)
        config.load_ui(self)
        self.__parent = parent
        self.__input_title = input_title

        self.form_name_label.setText(self.__input_title)

        self.form_check.clicked.connect(self._setToogleInput)

    @property
    def checked(self):
        self.form_check.isChecked()

    @checked.setter
    def checked(self, value):
        self.form_check.setChecked(value)

    @property
    def input_text(self):
        return self.form_input_edit.text()

    @input_text.setter
    def input_text(self, value):
        self.form_input_edit.setText(value)

    @property
    def placeholder(self):
        self.form_input_edit.placeholderText()

    @placeholder.setter
    def placeholder(self, value):
        self.form_input_edit.setPlaceholderText(value)

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

        self.add_forms(*self.__form_objs)

    def add_forms(self, *args) -> None:
        for obj in args:
            if type(obj) == Form:
                self.group_form_layout.add_widget(obj)


class GroupFormWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, title: str = None, widgets: list = None) -> None:
        super(GroupFormWidget, self).__init__(parent)
        config.load_ui(self)
        self.__parent = parent
        self.__title = title + ":"
        self.__widgets = widgets

        self.form_group.setTitle(self.__title)

        if self.__widgets:
            config.append_widget(
                layout=self.form_group_layout,
                widgets=self.__widgets
            )
