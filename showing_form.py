from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QTableView
from PySide6.QtSql import QSqlTableModel
from ui_showingform import Ui_ShowingForm

class ShowingForm(QDialog):
    def __init__(self, model: QSqlTableModel, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.m_model = model
        self.m_ui = Ui_ShowingForm()
        self.m_ui.setupUi(self)

        self.m_ui.tableView.setModel(model)
        self.m_ui.tableView.setEditTriggers(QTableView.NoEditTriggers)
