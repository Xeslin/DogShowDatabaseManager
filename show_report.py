from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog
from ui_show_report import Ui_Dialog

class ShowReport(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.m_text = text
        self.m_ui = Ui_Dialog()
        self.m_ui.setupUi(self)

        self.m_ui.textBrowser.append(text)
