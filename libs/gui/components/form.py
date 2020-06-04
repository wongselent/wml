from ... import setting

from PyQt5 import QtWidgets

class Form(QtWidgets.QFrame):
    def __init__(self, label: str = None, placeholder: str = None, parent=None, *args, **kwargs):
        super(Form, self).__init__()
        setting.load_ui(__file__, self)

        label = label + ":"
        self.form_label.setText(label)
        # self.form_edit.setPlaceHolder(placeholder)
    pass