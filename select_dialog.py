from PySide6.QtWidgets import QDialog, QTableView
from PySide6.QtCore import Qt, QModelIndex, Signal
from PySide6.QtSql import QSqlTableModel
from PySide6 import QtWidgets

class SelectDialog(QDialog):
    selected = Signal(int)
    def __init__(self, model: QSqlTableModel, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор записи")

        # Создаем таблицу и устанавливаем модель
        self.table_view = QTableView(self)
        self.table_view.setModel(model)
        self.table_view.setEditTriggers(QTableView.NoEditTriggers)  # Запретить редактирование

        # Подключение сигнала двойного клика к слоту
        self.table_view.doubleClicked.connect(self.on_table_view_double_clicked)

        # Установка разметки
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.table_view)
        self.setLayout(layout)

    def on_table_view_double_clicked(self, index: QModelIndex):
        # Отправляем сигнал с номером выбранной строки
        self.selected.emit(index.row())
