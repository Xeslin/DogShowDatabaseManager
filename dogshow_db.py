from PySide6.QtCore import QObject, Signal
from PySide6.QtSql import  QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlRecord

from select_dialog import SelectDialog

class DogShowDB(QObject):
    class TableType:
        NoneType = 0
        Breeds = 1
        Dogs = 2
        Clubs = 3
        Participants = 4
        Rings = 5
        Experts = 6
        Judging = 7
        Medalists = 8


    errorMsg = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.m_db = QSqlDatabase.addDatabase("QSQLITE")
        self.m_db.setDatabaseName("DogShow.db")
        self.m_db.open()
        query = QSqlQuery()
        query.exec("PRAGMA foreign_keys = ON;")
        self.add_tables()
        self.m_table_type = self.TableType.NoneType
        self.m_selected_row = -1

    def is_open(self):
        return self.m_db.isOpen()

    def is_valid(self):
        return self.m_db.isValid()

    def last_error_text(self):
        return self.m_db.lastError().text()

    def add_tables(self): # создает таблицы в базе данных
        query = QSqlQuery(self.m_db)

        if not query.exec("""
        CREATE TABLE IF NOT EXISTS breeds (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL CHECK (LENGTH(name) >= 3)
        );
    """):
            self.errorMsg.emit("[addTables] Не удалось создать таблицу breeds!")


        if not query.exec("""
        CREATE TABLE IF NOT EXISTS dogs (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL CHECK (LENGTH(name) >= 3),
            breed_id INTEGER NOT NULL,
            age INTEGER CHECK (age >= 0),
            father_id INTEGER,
            mother_id INTEGER,
            registration_number VARCHAR(7) NOT NULL CHECK (registration_number NOT LIKE '%[^0-9]%' AND LENGTH(registration_number)=7),
            microchip_number VARCHAR(255) UNIQUE,
            FOREIGN KEY (breed_id) REFERENCES breeds(ID) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (father_id) REFERENCES dogs(ID) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (mother_id) REFERENCES dogs(ID) ON UPDATE CASCADE ON DELETE CASCADE
        );
    """):
            self.errorMsg.emit("[addTables] Не удалось создать таблицу dogs!")


        if not query.exec("""
        CREATE TABLE IF NOT EXISTS clubs (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL UNIQUE,
            range_start INTEGER NOT NULL,
            range_end INTEGER NOT NULL,
            CHECK (range_end > range_start)
        );
    """):
            self.errorMsg.emit("[addTables] Не удалось создать таблицу clubs!")


        if not query.exec("""
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            dog_id INTEGER NOT NULL,
            club_id INTEGER NOT NULL,
            participant_number NOT NULL UNIQUE,
            FOREIGN KEY (dog_id) REFERENCES dogs(ID) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (club_id) REFERENCES clubs(ID) ON UPDATE CASCADE ON DELETE CASCADE
        );
    """):
            self.errorMsg.emit("[addTables] Не удалось создать таблицу participants!")


        if not query.exec("""
        CREATE TABLE IF NOT EXISTS rings (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            breed_id INTEGER NOT NULL,
            FOREIGN KEY (breed_id) REFERENCES breeds(ID) ON UPDATE CASCADE ON DELETE CASCADE
        );
    """):
            self.errorMsg.emit("[addTables] Не удалось создать таблицу rings!")

        if not query.exec("""
        CREATE TABLE IF NOT EXISTS experts (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            fullname VARCHAR(255) NOT NULL CHECK (LENGTH(fullname) >= 3),
            club_id INTEGER NOT NULL,
            ring_id INTEGER NOT NULL,
            FOREIGN KEY (club_id) REFERENCES clubs(ID) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (ring_id) REFERENCES rings(ID) ON UPDATE CASCADE ON DELETE CASCADE
        );
    """):
            self.errorMsg.emit("[addTables] Не удалось создать таблицу experts!")


        if not query.exec("""
        CREATE TABLE IF NOT EXISTS judging (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            expert_id INTEGER NOT NULL,
            ring_id INTEGER NOT NULL,
            FOREIGN KEY (expert_id) REFERENCES experts(ID) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (ring_id) REFERENCES rings(ID) ON UPDATE CASCADE ON DELETE CASCADE
        );
    """):
            self.errorMsg.emit("[addTables] Не удалось создать таблицу judging!")


        if not query.exec("""
        CREATE TABLE IF NOT EXISTS medalists (
            participant_id INTEGER NOT NULL,
            type VARCHAR(255) NOT NULL,
            FOREIGN KEY (participant_id) REFERENCES participants(ID) ON UPDATE CASCADE ON DELETE CASCADE
        );
    """):
            self.errorMsg.emit("[addTables] Не удалось создать таблицу medalists!")




    def bind(self, table_type):
        self.m_table_type = table_type

    def unbind(self):
        self.m_table_type = self.TableType.NoneType


    def table_type_to_table_name(self, table_type):
        if table_type == self.TableType.NoneType:
            self.errorMsg.emit("[tableTypeToTableName] Не выбрана активная таблица!")
            return ""
        if table_type == self.TableType.Breeds:
            return "breeds"
        if table_type == self.TableType.Dogs:
            return "dogs"
        if table_type == self.TableType.Clubs:
            return "clubs"
        if table_type == self.TableType.Participants:
            return "participants"
        if table_type == self.TableType.Rings:
            return "rings"
        if table_type == self.TableType.Experts:
            return "experts"
        if table_type == self.TableType.Judging:
            return "judging"
        if table_type == self.TableType.Medalists:
            return "medalists"

        self.errorMsg.emit("[tableTypeToTableName] Неизвестный тип таблицы!")
        return ""


    def record_from_select_dialog(self, table_type, title):
        model = QSqlTableModel(None, self.m_db)
        model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        model.setTable(self.table_type_to_table_name(table_type))
        model.select()

        select_dialog = SelectDialog(model)
        if title:
            select_dialog.setWindowTitle(title)
        select_dialog.selected.connect(self.on_selected)
        select_dialog.exec()
        select_dialog.selected.disconnect(self.on_selected)

        row = self.m_selected_row
        if self.m_selected_row == -1:
            self.errorMsg.emit("[recordFromSelectDialog] Строка не выбрана!")
            return QSqlRecord()
        self.m_selected_row = -1
        res = model.record(row)
        return res

    def add_row(self):
        if self.m_table_type == self.TableType.NoneType:
            self.errorMsg.emit("[addRow] Не выбрана активная таблица!")
        elif self.m_table_type == self.TableType.Breeds:
            self.add_row_to_breeds()
        elif self.m_table_type == self.TableType.Dogs:
            self.add_row_to_dogs()
        elif self.m_table_type == self.TableType.Clubs:
            self.add_row_to_clubs()
        elif self.m_table_type == self.TableType.Participants:
            self.add_row_to_participants()
        elif self.m_table_type == self.TableType.Rings:
            self.add_row_to_rings()
        elif self.m_table_type == self.TableType.Experts:
            self.add_row_to_experts()
        elif self.m_table_type == self.TableType.Judging:
            self.add_row_to_judging()
        elif self.m_table_type == self.TableType.Medalists:
            self.add_row_to_medalists()
        else:
            self.errorMsg.emit("[addRow] Неизвестный тип таблицы!")

    def delete_row(self):
        record = self.record_from_select_dialog(self.m_table_type, "Выберите удаляемую запись")
        if record.isEmpty():
            return

        query = QSqlQuery(self.m_db)
        if self.m_table_type == self.TableType.Medalists:
            query_text = f"DELETE FROM {self.table_type_to_table_name(self.m_table_type)} WHERE participant_id = {record.value('participant_id')};"
        else:
            query_text = f"DELETE FROM {self.table_type_to_table_name(self.m_table_type)} WHERE id = {record.value('id')};"

        if not query.exec(query_text):
            self.errorMsg.emit("[deleteRow] " + query.lastError().text())


    def get_model(self, model):
        if self.m_table_type == self.TableType.NoneType:
            self.errorMsg.emit("[get_model] Не выбрана активная таблица!")
            return

        model = QSqlTableModel(None, self.m_db)
        model.beforeUpdate.connect(self.on_update)
        model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        table_name = self.table_type_to_table_name(self.m_table_type)
        if table_name:
            model.setTable(table_name)
            model.select()
        return model

    def add_row_to_breeds(self):
        query = QSqlQuery(self.m_db)
        if not query.exec("""
        INSERT INTO breeds (name)
        VALUES ('Название породы');
    """):
            self.errorMsg.emit("[addRowToBreeds] " + query.lastError().text())


    def add_row_to_dogs(self):
        query = QSqlQuery(self.m_db)
        breed_id = 0
        record = self.record_from_select_dialog(self.TableType.Breeds, "Выберите породу")
        if (record == QSqlRecord()):
            return
        else:
            breed_id = record.value("id")
        if not query.exec(f"""
        INSERT INTO dogs (name, breed_id, age, father_id, mother_id, registration_number, microchip_number)
        VALUES ('Кличка', {breed_id}, 4, NULL, NULL, '0000000', '0000');
    """):
            self.errorMsg.emit("[addRowToDogs] " + query.lastError().text())

    def add_row_to_clubs(self):
        query = QSqlQuery(self.m_db)
        if not query.exec("""
        INSERT INTO clubs (name, range_start, range_end)
        VALUES ('Название', 0, 1);
    """):
            self.errorMsg.emit("[addRowToClubs] " + query.lastError().text())

    def add_row_to_participants(self):
        query = QSqlQuery(self.m_db)
        dog_id = 0
        club_id = 0
        record_1 = self.record_from_select_dialog(self.TableType.Dogs, "Выберите собаку")
        if (record_1 == QSqlRecord()):
            return
        else:
            dog_id = record_1.value("id")
        record_2 = self.record_from_select_dialog(self.TableType.Clubs, "Выберите клуб")
        if (record_2 == QSqlRecord()):
            return
        else:
            club_id = record_2.value("id")
        if not query.exec(f"""
        INSERT INTO participants (dog_id, club_id, participant_number)
        VALUES ({dog_id}, {club_id}, 0);
    """):
            self.errorMsg.emit("[addRowToParticipants] " + query.lastError().text())


    def add_row_to_rings(self):
        query = QSqlQuery(self.m_db)
        breed_id = 0
        record = self.record_from_select_dialog(self.TableType.Breeds, "Выберите породу")
        if (record == QSqlRecord()):
            return
        else:
            breed_id = record.value("id")
        if not query.exec(f"""
        INSERT INTO rings (breed_id)
        VALUES ({breed_id});
    """):
            self.errorMsg.emit("[addRowToRings] " + query.lastError().text())


    def add_row_to_experts(self):
        query = QSqlQuery(self.m_db)
        club_id = 0
        ring_id = 0
        record_1 = self.record_from_select_dialog(self.TableType.Clubs, "Выберите клуб")
        if (record_1 == QSqlRecord()):
            return
        else:
            club_id = record_1.value("id")
        record_2 = self.record_from_select_dialog(self.TableType.Rings, "Выберите ринг")
        if (record_2 == QSqlRecord()):
            return
        else:
            ring_id = record_2.value("id")
        if not query.exec(f"""
        INSERT INTO experts (fullname, club_id, ring_id)
        VALUES ('Иванов Иван Иванович', {club_id}, {ring_id});
    """):
            self.errorMsg.emit("[addRowToExperts] " + query.lastError().text())

    def add_row_to_judging(self):
        query = QSqlQuery(self.m_db)
        expert_id = 0
        ring_id = 0
        record_1 = self.record_from_select_dialog(self.TableType.Experts, "Выберите эксперта")
        if (record_1 == QSqlRecord()):
            return
        else:
            expert_id = record_1.value("id")
        record_2 = self.record_from_select_dialog(self.TableType.Rings, "Выберите ринг")
        if (record_2 == QSqlRecord()):
            return
        else:
            ring_id = record_2.value("id")
        if not query.exec(f"""
        INSERT INTO judging (expert_id, ring_id)
        VALUES ({expert_id}, {ring_id});
    """):
            self.errorMsg.emit("[addRowToJudging] " + query.lastError().text())


    def add_row_to_medalists(self):
        query = QSqlQuery(self.m_db)
        participant_id = 0
        record = self.record_from_select_dialog(self.TableType.Participants, "Выберите участника")
        if (record == QSqlRecord()):
            return
        else:
            participant_id = record.value("id")
        if not query.exec(f"""
        INSERT INTO medalists (participant_id, type)
        VALUES ({participant_id}, 'Тип медали');
    """):
            self.errorMsg.emit("[addRowToMedalists] " + query.lastError().text())

    def show_ring(self):
        record = self.record_from_select_dialog(self.TableType.Participants, "Выберите участника")
        if (record == QSqlRecord()):
            return
        if self.m_db.transaction():
            query = QSqlQuery(self.m_db)
            if not query.exec("DROP TABLE IF EXISTS ring_info;"):
                self.errorMsg.emit("[showRing] " + query.lastError().text())
            else:
                query_text = f"""CREATE TABLE ring_info AS
                SELECT participants.id AS participant_id, rings.id AS ring_id, breeds.name AS breed_name
                FROM rings
                JOIN breeds ON rings.breed_id=breeds.id
                JOIN dogs ON dogs.breed_id=breeds.id
                JOIN participants ON dogs.id=participants.dog_id
                WHERE participants.id={record.value("id")}"""
                if not query.exec(query_text):
                    self.errorMsg.emit("[showRing] " + query.lastError().text())
                else:
                    model = QSqlTableModel(None, self.m_db)
                    model.setEditStrategy(QSqlTableModel.OnManualSubmit)
                    model.setTable("ring_info")
                    model.select()
                if self.m_db.commit():
                    return model
                else:
                    self.errorMsg.emit("[showRing] commit failed")

        else:
            self.errorMsg.emit("[showRing] transaction failed")

    def show_breeds(self):
        record = self.record_from_select_dialog(self.TableType.Clubs, "Выберите клуб")
        if (record == QSqlRecord()):
            return
        if self.m_db.transaction():
            query = QSqlQuery(self.m_db)
            if not query.exec("DROP TABLE IF EXISTS breeds_info;"):
                self.errorMsg.emit("[showBreeds] " + query.lastError().text())
            else:
                query_text = f"""CREATE TABLE breeds_info AS
                SELECT breeds.name AS breed_name
                FROM clubs
                JOIN participants ON clubs.id=participants.club_id
                JOIN dogs ON dogs.id=participants.dog_id
                JOIN breeds ON dogs.breed_id=breeds.id
                WHERE clubs.id={record.value("id")}"""
                if not query.exec(query_text):
                    self.errorMsg.emit("[showBreeds] " + query.lastError().text())
                else:
                    model = QSqlTableModel(None, self.m_db)
                    model.setEditStrategy(QSqlTableModel.OnManualSubmit)
                    model.setTable("breeds_info")
                    model.select()
                if self.m_db.commit():
                    return model
                else:
                    self.errorMsg.emit("[showBreeds] commit failed")

        else:
            self.errorMsg.emit("[showBreeds] transaction failed")


    def show_experts(self):
        record = self.record_from_select_dialog(self.TableType.Breeds, "Выберите породу")
        if (record == QSqlRecord()):
            return
        if self.m_db.transaction():
            query = QSqlQuery(self.m_db)
            if not query.exec("DROP TABLE IF EXISTS experts_info;"):
                self.errorMsg.emit("[showExperts] " + query.lastError().text())
            else:
                query_text = f"""CREATE TABLE experts_info AS
                SELECT experts.fullname AS expert_name, clubs.name AS club_name
                FROM breeds
                JOIN rings ON breeds.id=rings.breed_id
                JOIN judging ON rings.id=judging.ring_id
                JOIN experts ON judging.expert_id=experts.id
                JOIN clubs ON clubs.id=experts.club_id
                WHERE breeds.id={record.value("id")}"""
                if not query.exec(query_text):
                    self.errorMsg.emit("[showExperts] " + query.lastError().text())
                else:
                    model = QSqlTableModel(None, self.m_db)
                    model.setEditStrategy(QSqlTableModel.OnManualSubmit)
                    model.setTable("experts_info")
                    model.select()
                if self.m_db.commit():
                    return model
                else:
                    self.errorMsg.emit("[showExperts] commit failed")

        else:
            self.errorMsg.emit("[showExperts] transaction failed")

    def show_dogs(self):
        record = self.record_from_select_dialog(self.TableType.Experts, "Выберите эксперта")
        if (record == QSqlRecord()):
            return
        if self.m_db.transaction():
            query = QSqlQuery(self.m_db)
            if not query.exec("DROP TABLE IF EXISTS dogs_info;"):
                self.errorMsg.emit("[showDogs] " + query.lastError().text())
            else:
                query_text = f"""CREATE TABLE dogs_info AS
                SELECT dogs.name AS dog_name, breeds.name AS breed, dogs.age AS age, dogs.registration_number AS reg_num, dogs.microchip_number AS microchip
                FROM experts
                JOIN judging ON experts.id=judging.expert_id
                JOIN rings ON rings.id=judging.ring_id
                JOIN breeds ON rings.breed_id=breeds.id
                JOIN dogs ON dogs.breed_id=breeds.id
                WHERE experts.id={record.value("id")};"""
                if not query.exec(query_text):
                    self.errorMsg.emit("[showDogs] " + query.lastError().text())
                else:
                    model = QSqlTableModel(None, self.m_db)
                    model.setEditStrategy(QSqlTableModel.OnManualSubmit)
                    model.setTable("dogs_info")
                    model.select()
                if self.m_db.commit():
                    return model
                else:
                    self.errorMsg.emit("[showDogs] commit failed")

        else:
            self.errorMsg.emit("[showDogs] transaction failed")


    def show_medals(self):
        record = self.record_from_select_dialog(self.TableType.Clubs, "Выберите клуб")
        if (record == QSqlRecord()):
            return
        if self.m_db.transaction():
            query = QSqlQuery(self.m_db)
            if not query.exec("DROP TABLE IF EXISTS medals_info;"):
                self.errorMsg.emit("[showMedals] " + query.lastError().text())
            else:
                query_text = f"""CREATE TABLE medals_info AS
                SELECT medalists.type AS medal_type, COUNT(medalists.type) AS quantity
                FROM medalists
                JOIN participants ON participants.id=medalists.participant_id
                JOIN clubs ON clubs.id=participants.club_id
                WHERE clubs.id={record.value("id")}
                GROUP BY medalists.type;"""
                if not query.exec(query_text):
                    self.errorMsg.emit("[showMedals] " + query.lastError().text())
                else:
                    model = QSqlTableModel(None, self.m_db)
                    model.setEditStrategy(QSqlTableModel.OnManualSubmit)
                    model.setTable("medals_info")
                    model.select()
                if self.m_db.commit():
                    return model
                else:
                    self.errorMsg.emit("[showMedals] commit failed")

        else:
            self.errorMsg.emit("[showMedals] transaction failed")

    def show_prize(self):
        record = self.record_from_select_dialog(self.TableType.Participants, "Выберите участника")
        if (record == QSqlRecord()):
            return
        query = QSqlQuery(self.m_db)
        query_text = f"""SELECT participants.participant_number AS p_num, dogs.name AS name, dogs.age AS age, breeds.name AS breed, clubs.name AS club, medalists.type AS medal
        FROM participants
        LEFT JOIN medalists ON participants.id=medalists.participant_id
        JOIN dogs ON participants.dog_id=dogs.id
        JOIN clubs ON participants.club_id=clubs.id
        JOIN breeds ON dogs.breed_id=breeds.id
        WHERE participants.id={record.value("id")};"""
        if not query.exec(query_text):
            self.errorMsg.emit("[showPrize] " + query.lastError().text())
        else:
            while query.next():
                record = query.record()
            text_report = "Номер участника: " +  record.value("p_num") + "\n" + "Кличка: " + record.value("name") \
                + "\n" + "Возраст: " + str(record.value("age")) + "\n" + "Порода: " + record.value("breed") + "\n" \
                + "Клуб: " + record.value("club") + "\n"
            if record.value("medal") == "":
                text_report += "Призовое место: Нет :("
            else:
                text_report += "Призовое место: " + record.value("medal") + " медаль :)"
            return text_report

    def show_club_report(self):
        record_1 = self.record_from_select_dialog(self.TableType.Clubs, "Выберите клуб")
        if (record_1 == QSqlRecord()):
            return
        query = QSqlQuery(self.m_db)
        query_text = f"""SELECT clubs.name AS club_name, COUNT(*) AS p_count
        FROM participants
        JOIN clubs ON participants.club_id=clubs.id
        WHERE clubs.id={record_1.value("id")};"""
        if not query.exec(query_text):
            self.errorMsg.emit("[showClubReport] " + query.lastError().text())
        else:
            while query.next():
                record_2 = query.record()
            text_report = "Название клуба: " + record_2.value("club_name") + "\n" \
                + "Количество участников: " + str(record_2.value("p_count"))
        if not query.exec("DROP TABLE IF EXISTS report_info;"):
            self.errorMsg.emit("[showClubReport] " + query.lastError().text())
        else:
            query_text = f"""CREATE TABLE report_info AS
            SELECT breeds.name AS breed, COUNT(CASE WHEN medalists.type = 'Золотая' THEN 1 END) AS winners
            FROM breeds
            LEFT JOIN dogs ON dogs.breed_id=breeds.id
            LEFT JOIN participants ON participants.dog_id=dogs.id
            LEFT JOIN medalists ON medalists.participant_id=participants.id
            JOIN clubs ON participants.club_id=clubs.id
            WHERE clubs.id={record_1.value("id")}
            GROUP BY breeds.name;"""
            if not query.exec(query_text):
                self.errorMsg.emit("[showClubReport] " + query.lastError().text())
            else:
                model = QSqlTableModel(None, self.m_db)
                model.setEditStrategy(QSqlTableModel.OnManualSubmit)
                model.setTable("report_info")
                model.select()
        return text_report, model


    def on_update(self):
        pass

    def on_selected(self, row):
        self.m_selected_row = row
        select_dialog = self.sender()
        if select_dialog:
            select_dialog.close()
