import decimal
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QIcon
from form import Ui_Calc
from NumberEnum import Number, Operation
from decimal import Decimal
from PyQt5.QtCore import Qt

class Window(QMainWindow, Ui_Calc):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon('icon.png'))
        self.setupUi(self)
        self.setFixedWidth(211)
        self.setFixedHeight(329)
        self.initUI()
        self.result = None
        self.status = 0
        self.operationType = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

        key = event.key()
        if Qt.Key_0 <= key <= Qt.Key_9:
            self.clickNumberButton(chr(key))
        elif key == Qt.Key_Asterisk:
            self.operationClick(Operation.Multiplication.value)
        elif key == Qt.Key_Plus:
            self.operationClick(Operation.Sum.value)
        elif key == Qt.Key_Minus:
            self.operationClick(Operation.Extraction.value)
        elif key == Qt.Key_Slash:
            self.operationClick(Operation.Division.value)
        elif key == Qt.Key_Percent:
            self.operationClick(Operation.Mode.value)
        elif key == Qt.Key_Backspace:
            self.deleteClick()
        elif key == Qt.Key_Comma:
            self.fractionalClick()
        elif key == Qt.Key_Equal or key == Qt.Key_Return or key == 16777221:
            self.resultClick()

    def initUI(self):
        self.oneButton.clicked.connect(lambda: self.clickNumberButton(Number._1.value))
        self.twoButton.clicked.connect(lambda: self.clickNumberButton(Number._2.value))
        self.threeButton.clicked.connect(lambda: self.clickNumberButton(Number._3.value))
        self.fourButton.clicked.connect(lambda: self.clickNumberButton(Number._4.value))
        self.fiveButton.clicked.connect(lambda: self.clickNumberButton(Number._5.value))
        self.sixButton.clicked.connect(lambda: self.clickNumberButton(Number._6.value))
        self.sevenButton.clicked.connect(lambda: self.clickNumberButton(Number._7.value))
        self.eightButton.clicked.connect(lambda: self.clickNumberButton(Number._8.value))
        self.nineButton.clicked.connect(lambda: self.clickNumberButton(Number._9.value))
        self.zeroButton.clicked.connect(lambda: self.clickNumberButton(Number._0.value))
        self.deleteButton.clicked.connect(self.deleteClick)
        self.operationDelButton.clicked.connect(self.operationCancel)
        self.lastOperationDelButton.clicked.connect(self.currentOperationCancel)
        self.sumButton.clicked.connect(lambda: self.operationClick(Operation.Sum.value))
        self.extractionButton.clicked.connect(lambda: self.operationClick(Operation.Extraction.value))
        self.multiplicationButton.clicked.connect(lambda: self.operationClick(Operation.Multiplication.value))
        self.divisionButton.clicked.connect(lambda: self.operationClick(Operation.Division.value))
        self.modeButton.clicked.connect(lambda: self.operationClick(Operation.Mode.value))
        self.resultButton.clicked.connect(self.resultClick)
        self.fractionalButton.clicked.connect(self.fractionalClick)
        self.convertButton.clicked.connect(self.convertClick)

    def clickNumberButton(self, value):
        if self.status == 1:
            self.resultLabel.setText("")
            self.status = 0
        self.resultLabel.setText(self.resultLabel.text() + value)

    def convertClick(self):
        if len(self.resultLabel.text()) > 0:
            self.resultLabel.setText(str(Decimal(self.resultLabel.text())*Decimal(-1)))

    def fractionalClick(self):
        if self.resultLabel.text().find(Number.dot.value) == -1:
            self.resultLabel.setText(self.resultLabel.text() + Number.dot.value)

    def deleteClick(self):
        self.resultLabel.setText(self.resultLabel.text()[0:len(self.resultLabel.text())-1])

    def operationCancel(self):
        self.result = None
        self.resultLabel.setText("")
        self.operationLabel.setText("")

    def currentOperationCancel(self):
        self.resultLabel.setText("")

    # def showMessage(self):
    #     QMessageBox().about(self, "Operasyon Değişikliği Bilgisi", "Yapılacak operasyonel işlem değiştirildi")

    def operationClick(self, operation=None):
        if operation == Operation.Sum.value:
            self.operationType = Operation.Sum.value
        elif operation == Operation.Extraction.value:
            self.operationType = Operation.Extraction.value
        elif operation == Operation.Multiplication.value:
            self.operationType = Operation.Multiplication.value
        elif operation == Operation.Division.value:
            self.operationType = Operation.Division.value
        elif operation == Operation.Mode.value:
            self.operationType = Operation.Mode.value
        try:
            self.result = Decimal(self.resultLabel.text())
            self.operationLabel.setText(self.resultLabel.text() + operation)
            self.resultLabel.setText("")
        except decimal.InvalidOperation as ex:
            if self.result is not None:
                self.operationLabel.setText(str(self.result) + operation)

    def resultClick(self):
        if len(self.resultLabel.text()) > 0 and self.operationType is not None:
            if self.operationType == Operation.Sum.value:
                self.result = Decimal(self.result) + Decimal(self.resultLabel.text())
            elif self.operationType == Operation.Extraction.value:
                self.result = Decimal(self.result) - Decimal(self.resultLabel.text())
            elif self.operationType == Operation.Multiplication.value:
                self.result = Decimal(self.result) * Decimal(self.resultLabel.text())
            elif self.operationType == Operation.Division.value:
                self.result = Decimal(self.result) / Decimal(self.resultLabel.text())
            elif self.operationType == Operation.Mode.value:
                self.result = Decimal(self.result) % Decimal(self.resultLabel.text())

            if self.operationType is not None:
                self.operationLabel.setText(self.operationLabel.text() + self.resultLabel.text())
            self.resultLabel.setText(str(int(self.result) if self.result % 1 == 0 else self.result))
            self.status = 1
            self.operationType = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())