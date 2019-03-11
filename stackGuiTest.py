import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QApplication,
QLineEdit, QStackedWidget, QComboBox)


class Application(QWidget):

    def __init__(self):
        super().__init__()
        self.myCombo = QComboBox()
        self.myCombo.addItem("circle")
        self.myCombo.addItem("square")
        self.myCombo.addItem("trapezoid")
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)
        layout = QHBoxLayout(self)
        layout.addWidget(self.myCombo)
        layout.addWidget(self.stack)
        self.setLayout(layout)
        self.myCombo.currentIndexChanged.connect(self.stack.setCurrentIndex)
        self.show()

    def stack1UI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("circle"))
        layout.addWidget(QLineEdit())
        self.stack1.setLayout(layout)

    def stack2UI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("square"))
        layout.addWidget(QLineEdit())
        self.stack2.setLayout(layout)

    def stack3UI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("trapezoid"))
        layout.addWidget(QLineEdit())
        self.stack3.setLayout(layout)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())
