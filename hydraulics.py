import sys
import channel
from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QApplication,
                               QComboBox, QStackedWidget, QHBoxLayout, QLineEdit,
                             QPushButton, QTextEdit, QRadioButton)
from PySide6.QtCore import *


class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.pipeShape = QComboBox()
        self.pipeShape.addItem("circular")
        self.pipeShape.addItem("rectangular")
        self.pipeShape.addItem("trapezoidal")
        self.circleDiameter = QLineEdit()
        self.rectWidth = QLineEdit()
        self.rectDepth = QLineEdit()
        self.rectOpen = QRadioButton("Open")
        self.rectClosed = QRadioButton("Closed")
        self.rectOpen.setChecked(True)
        self.trapWidth = QLineEdit()
        self.trapDepth = QLineEdit()
        self.trapSide = QLineEdit()
        self.trapOpen = QRadioButton("Open")
        self.trapClosed = QRadioButton("Closed")
        self.trapOpen.setChecked(True)
        self.lengthEdit = QLineEdit()
        self.lengthEdit.setFixedWidth(125)
        self.usInvert = QLineEdit()
        self.usInvert.setFixedWidth(125)
        self.dsInvert = QLineEdit()
        self.dsInvert.setFixedWidth(125)
        self.Ks = QLineEdit()
        self.Ks.setFixedWidth(125)
        self.Ks.setText("3.0")
        self.kinvisc = QLineEdit()
        self.kinvisc.setFixedWidth(125)
        self.kinvisc.setText("1.141e-06")
        self.dsK = QLineEdit()
        self.dsK.setFixedWidth(125)
        self.dsK.setText("0.0")
        self.usK = QLineEdit()
        self.usK.setFixedWidth(125)
        self.usK.setText("0.0")
        self.flow = QLineEdit()
        self.myFunc = QPushButton("Calculate", self)
        self.myFunc.clicked.connect(self.calculate)
        self.result = QTextEdit()

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

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select Pipe Shape:"))
        layout.addWidget(self.pipeShape)

        layout.addWidget(self.stack)
        layoutFlow = QHBoxLayout()
        layoutFlow.addWidget(QLabel("Flow Rate:"))
        layoutFlow.addWidget(QLabel("m3/s"))
        layoutFlow.addWidget(self.flow)
        layout.addLayout(layoutFlow)
        layout.addWidget(self.myFunc)
        layout.addWidget(self.result)

        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout2.addWidget(QLabel("Length"))
        layout2.addWidget(self.lengthEdit)
        layout2.addWidget(QLabel("m"))
        layout2.addStretch()
        layout3 = QHBoxLayout()
        layout3.addWidget(QLabel("Upstream IL"))
        layout3.addWidget(self.usInvert)
        layout3.addWidget(QLabel("m"))
        layout4 = QHBoxLayout()
        layout4.addWidget(QLabel("Downstream IL"))
        layout4.addWidget(self.dsInvert)
        layout4.addWidget(QLabel("m"))
        layout5 = QHBoxLayout()
        layout5.addWidget(QLabel("Ks"))
        layout5.addWidget(self.Ks)
        layout5.addWidget(QLabel("mm"))
        layout6 = QHBoxLayout()
        layout6.addWidget(QLabel("kinematic visc"))
        layout6.addWidget(self.kinvisc)
        layout6.addWidget(QLabel("m2/s"))
        layout7 = QHBoxLayout()
        layout7.addWidget(QLabel("Upstream K"))
        layout7.addWidget(self.usK)
        layout7.addWidget(QLabel("no."))
        layout8 = QHBoxLayout()
        layout8.addWidget(QLabel("Downstream K"))
        layout8.addWidget(self.dsK)
        layout8.addWidget(QLabel("no."))
        layout1.addLayout(layout2)
        layout1.addLayout(layout3)
        layout1.addLayout(layout4)
        layout1.addLayout(layout5)
        layout1.addLayout(layout6)
        layout1.addLayout(layout7)
        layout1.addLayout(layout8)
        layout1.setAlignment(Qt.AlignTop)

        topLayout = QHBoxLayout(self)
        topLayout.addLayout(layout)
        topLayout.addLayout(layout1)

        self.setLayout(topLayout)
        self.pipeShape.currentIndexChanged.connect(self.stack.setCurrentIndex)
        self.setGeometry(100, 100, 670, 500)
        self.show()

    def stack1UI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Diameter"))
        layout.addWidget(self.circleDiameter)
        layout.addWidget(QLabel("m"))
        layout.setAlignment(Qt.AlignTop)
        self.stack1.setLayout(layout)

    def stack2UI(self):
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout1.addWidget(QLabel("Width"))
        layout1.addWidget(self.rectWidth)
        layout1.addWidget(QLabel("m"))
        layout2.addWidget(QLabel("Depth"))
        layout2.addWidget(self.rectDepth)
        layout2.addWidget(QLabel("m"))
        layout3.addWidget(self.rectOpen)
        layout3.addWidget(self.rectClosed)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.setAlignment(Qt.AlignTop)
        self.stack2.setLayout(layout)

    def stack3UI(self):
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()
        layout1.addWidget(QLabel("Width"))
        layout1.addWidget(self.trapWidth)
        layout1.addWidget(QLabel("m"))
        layout2.addWidget(QLabel("Depth"))
        layout2.addWidget(self.trapDepth)
        layout2.addWidget(QLabel("m"))
        layout3.addWidget(QLabel("Side Slope"))
        layout3.addWidget(self.trapSide)
        layout3.addWidget(QLabel("unit"))
        layout4.addWidget(self.trapOpen)
        layout4.addWidget(self.trapClosed)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(layout4)
        layout.setAlignment(Qt.AlignTop)
        self.stack3.setLayout(layout)

    def calculate(self):
        try:
            flow = float(self.flow.text())
            kinvisc = float(self.kinvisc.text())
            length = float(self.lengthEdit.text())
            usIL = float(self.usInvert.text())
            dsIL = float(self.dsInvert.text())
            Ks = float(self.Ks.text()) / 1000.0
            usK = float(self.usK.text())
            dsK = float(self.dsK.text())
            conduit = channel.Channel()
            conduit.setValues(flow, 0.8, 2, 100.0, 1.0, 0.9, 0.003, kinvisc)
            conduit.calculate()
            resultText = "critical depth:\t %0.3f" % conduit.crit_depth
            resultText += "\nnormal depth:\t %0.3f" % conduit.norm_depth
            resultText += "\nds water depth:\t %0.3f" % conduit.water[0]
            resultText += "\nus water depth:\t %0.3f" % conduit.water[-1]
            resultText += "\nds water level:\t %0.3f" % conduit.head[0]
            resultText += "\nus water level:\t %0.3f" % conduit.head[-1]
            resultText += "\nds energy level:\t %0.3f" % conduit.energy[0]
            resultText += "\nus energy level:\t %0.3f" % conduit.energy[-1]
            self.result.setText(str(resultText))
        except ValueError:
            pass
        except:
            print("error")
            pass

        # if self.pipeShape.currentIndex() == 0:
        #   self.result.setText(self.circleDiameter.text())
        # elif self.pipeShape.currentIndex() == 1:
        #   self.result.setText(self.rectWidth.text())
        # else:
        #   self.result.setText(self.trapWidth.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec())
