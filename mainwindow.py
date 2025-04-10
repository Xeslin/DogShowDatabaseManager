import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from ui_form import Ui_MainWindow
from dogshow_db import DogShowDB
from showing_form import ShowingForm
from show_report import ShowReport
from show_club_report import ShowClubReport

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.m_db = DogShowDB()
        if not self.m_db.is_open():
            QMessageBox.critical(self, "Не удалось открыть базу данных!", self.m_db.last_error_text())
        self.m_db.errorMsg.connect(self.on_database_error)
        self.m_model = None

        self.ui.showBreeds.triggered.connect(self.on_showBreeds_triggered)
        self.ui.showDogs.triggered.connect(self.on_showDogs_triggered)
        self.ui.showClubs.triggered.connect(self.on_showClubs_triggered)
        self.ui.showParticipants.triggered.connect(self.on_showParticipants_triggered)
        self.ui.showRings.triggered.connect(self.on_showRings_triggered)
        self.ui.showExperts.triggered.connect(self.on_showExperts_triggered)
        self.ui.showJudging.triggered.connect(self.on_showJudging_triggered)
        self.ui.showMedalists.triggered.connect(self.on_showMedalists_triggered)
        self.ui.aboutRing.triggered.connect(self.on_aboutRing_triggered)
        self.ui.aboutBreeds.triggered.connect(self.on_aboutBreeds_triggered)
        self.ui.aboutExperts.triggered.connect(self.on_aboutExperts_triggered)
        self.ui.aboutDogs.triggered.connect(self.on_aboutDogs_triggered)
        self.ui.aboutMedals.triggered.connect(self.on_aboutMedals_triggered)
        self.ui.prizeReport.triggered.connect(self.on_prizeReport_triggered)
        self.ui.clubReport.triggered.connect(self.on_clubReport_triggered)

        self.ui.addRow.clicked.connect(self.on_addRow_clicked)
        self.ui.delRow.clicked.connect(self.on_deleteRow_clicked)
        self.ui.Save.clicked.connect(self.on_save_clicked)
        self.ui.Update.clicked.connect(self.on_update_clicked)


    def create_showing_form(self, model, title):
        showing_form = ShowingForm(model, self)
        showing_form.setWindowTitle(title)
        showing_form.show()

    def create_report(self, text, title):
        report = ShowReport(text, self)
        report.setWindowTitle(title)
        report.show()

    def create_club_report(self, text, model, title):
        report = ShowClubReport(text, model, self)
        report.setWindowTitle(title)
        report.show()


    def on_database_error(self, msg: str):
        QMessageBox.critical(self, "ОШИБКА!", msg)

    def on_clubReport_triggered(self):
        text, model = self.m_db.show_club_report()
        self.create_club_report(text, model, "Отчет о выступлении клуба")

    def on_prizeReport_triggered(self):
        text = self.m_db.show_prize()
        self.create_report(text, "Справка о занятии участником призового места")


    def on_aboutMedals_triggered(self):
        model = self.m_db.show_medals()
        self.create_showing_form(model, "Информация о медалях, заслуженных клубом")

    def on_aboutDogs_triggered(self):
        model = self.m_db.show_dogs()
        self.create_showing_form(model, "Информация о собаках у данного эксперта")

    def on_aboutExperts_triggered(self):
        model = self.m_db.show_experts()
        self.create_showing_form(model, "Информация об экспертах, обслуживающих породу")

    def on_aboutBreeds_triggered(self):
        model = self.m_db.show_breeds()
        self.create_showing_form(model, "Информация о породах, представляемых клубом")

    def on_aboutRing_triggered(self):
        model = self.m_db.show_ring()
        self.create_showing_form(model, "Информация о ринге выбранного участника")

    def on_showBreeds_triggered(self):
        self.m_db.bind(DogShowDB.TableType.Breeds)
        model = self.m_db.get_model(self.m_model)
        self.ui.tableView.setModel(model)

    def on_showDogs_triggered(self):
        self.m_db.bind(DogShowDB.TableType.Dogs)
        model = self.m_db.get_model(self.m_model)
        self.ui.tableView.setModel(model)

    def on_showClubs_triggered(self):
        self.m_db.bind(DogShowDB.TableType.Clubs)
        model = self.m_db.get_model(self.m_model)
        self.ui.tableView.setModel(model)

    def on_showParticipants_triggered(self):
        self.m_db.bind(DogShowDB.TableType.Participants)
        model = self.m_db.get_model(self.m_model)
        self.ui.tableView.setModel(model)

    def on_showRings_triggered(self):
        self.m_db.bind(DogShowDB.TableType.Rings)
        model = self.m_db.get_model(self.m_model)
        self.ui.tableView.setModel(model)

    def on_showExperts_triggered(self):
        self.m_db.bind(DogShowDB.TableType.Experts)
        model = self.m_db.get_model(self.m_model)
        self.ui.tableView.setModel(model)

    def on_showJudging_triggered(self):
        self.m_db.bind(DogShowDB.TableType.Judging)
        model = self.m_db.get_model(self.m_model)
        self.ui.tableView.setModel(model)

    def on_showMedalists_triggered(self):
        self.m_db.bind(DogShowDB.TableType.Medalists)
        model = self.m_db.get_model(self.m_model)
        self.ui.tableView.setModel(model)

    def on_addRow_clicked(self):
        self.m_db.add_row()
        model = self.m_db.get_model(self.m_model)
        self.ui.tableView.setModel(model)


    def on_save_clicked(self):
        model = self.m_db.get_model(self.m_model)
        if model is not None:
            if not model.submitAll():
                QMessageBox.critical(self, "Невалидные изменения!", model.lastError().text())

    def on_update_clicked(self):
        model = self.m_db.get_model(self.m_model)
        self.ui.tableView.setModel(model)

    def on_deleteRow_clicked(self):
        reply = QMessageBox.question(
            self,
            "Хотите удалить запись?",
            "Это также удалит все зависимые записи при их наличии",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.m_db.delete_row()
            model = self.m_db.get_model(self.m_model)
            self.ui.tableView.setModel(model)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
