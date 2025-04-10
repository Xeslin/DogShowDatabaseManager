from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog
from ui_showclubreport import Ui_Dialog


class ShowClubReport(QDialog):
    def __init__(self, text, model, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.m_text = text
        self.m_model = model
        self.m_ui = Ui_Dialog()
        self.m_ui.setupUi(self)

        self.m_ui.textBrowser.append(text)
        self.m_ui.tableView.setModel(model)
