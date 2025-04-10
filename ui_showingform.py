from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QTableView,
    QWidget)

class Ui_ShowingForm(object):
    def setupUi(self, ShowingForm):
        if not ShowingForm.objectName():
            ShowingForm.setObjectName(u"ShowingForm")
        ShowingForm.setWindowModality(Qt.NonModal)
        ShowingForm.resize(655, 498)
        self.tableView = QTableView(ShowingForm)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(10, 10, 641, 481))

        self.retranslateUi(ShowingForm)

        QMetaObject.connectSlotsByName(ShowingForm)
    # setupUi

    def retranslateUi(self, ShowingForm):
        ShowingForm.setWindowTitle(QCoreApplication.translate("ShowingForm", u"Form", None))
    # retranslateUi

