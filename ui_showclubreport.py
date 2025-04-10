from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHeaderView, QLabel,
    QSizePolicy, QTableView, QTextBrowser, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(516, 533)
        self.textBrowser = QTextBrowser(Dialog)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(10, 10, 501, 221))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 240, 151, 16))
        self.tableView = QTableView(Dialog)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(10, 260, 501, 261))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u041f\u043e\u0431\u0435\u0434\u0438\u0442\u0435\u043b\u0438 \u043f\u043e \u043f\u043e\u0440\u043e\u0434\u0430\u043c", None))
    # retranslateUi

