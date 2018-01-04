#-------------------------------------------------------------------------------
# Name:        GraphSIDE
# Author:      nebula121 <nebula121.dev@gmail.com>
# Copyright:   (c) nebula121 2018
# Licence:     MIT License
#-------------------------------------------------------------------------------

import sys
from PySide.QtCore import *
from PySide.QtGui import *

class GraphFrameSetting(QDialog):
    graphFrameSettingChanged = Signal()

    def __init__(self, parent = None, graphSettingWidgetUi = None):
        super(GraphFrameSetting, self).__init__(parent)
        
        self.ui = graphSettingWidgetUi
        self.setupUi()

        self.slot1 = lambda: self.graphFrameSettingChanged.emit()

        self.connectUiChangedToSignal()
        
        
    def connectUiChangedToSignal(self):
        self.ui.titleEdit.textChanged.connect(self.slot1)
        self.ui.bgColorEdit.textChanged.connect(self.slot1)
        self.ui.axisNumSpinBox.valueChanged.connect(self.slot1)
        
        self.ui.positionSpinBox1.valueChanged.connect(self.slot1)
        self.ui.positionSpinBox2.valueChanged.connect(self.slot1)
        self.ui.spanSpinBox1.valueChanged.connect(self.slot1)
        self.ui.spanSpinBox2.valueChanged.connect(self.slot1)
        self.ui.sizeSpinBox1.valueChanged.connect(self.slot1)
        self.ui.sizeSpinBox2.valueChanged.connect(self.slot1)
        
        self.ui.xAxisTitleEdit.textChanged.connect(self.slot1)
        self.ui.xAxisTitleColorEdit.textChanged.connect(self.slot1)
        self.ui.y1AxisTitleEdit.textChanged.connect(self.slot1)
        self.ui.y1AxisTitleColorEdit.textChanged.connect(self.slot1)
        self.ui.y2AxisTitleEdit.textChanged.connect(self.slot1)
        self.ui.y2AxisTitleColorEdit.textChanged.connect(self.slot1)
        self.ui.y3AxisTitleEdit.textChanged.connect(self.slot1)
        self.ui.y3AxisTitleColorEdit.textChanged.connect(self.slot1)

        self.ui.xMaxRangeSpinBox.valueChanged.connect(self.slot1)
        self.ui.y1MaxRangeSpinBox.valueChanged.connect(self.slot1)
        self.ui.y2MaxRangeSpinBox.valueChanged.connect(self.slot1)
        self.ui.y3MaxRangeSpinBox.valueChanged.connect(self.slot1)
        self.ui.xMinRangeSpinBox.valueChanged.connect(self.slot1)
        self.ui.y1MinRangeSpinBox.valueChanged.connect(self.slot1)
        self.ui.y2MinRangeSpinBox.valueChanged.connect(self.slot1)
        self.ui.y3MinRangeSpinBox.valueChanged.connect(self.slot1)

        self.ui.xMajorTickSpinBox.valueChanged.connect(self.slot1)
        self.ui.y1MajorTickSpinBox.valueChanged.connect(self.slot1)
        self.ui.y2MajorTickSpinBox.valueChanged.connect(self.slot1)
        self.ui.y3MajorTickSpinBox.valueChanged.connect(self.slot1)
        self.ui.xMinorTickSpinBox.valueChanged.connect(self.slot1)
        self.ui.y1MinorTickSpinBox.valueChanged.connect(self.slot1)
        self.ui.y2MinorTickSpinBox.valueChanged.connect(self.slot1)
        self.ui.y3MinorTickSpinBox.valueChanged.connect(self.slot1)


    def disconnectUiChangedToSignal(self):
        self.ui.titleEdit.textChanged.disconnect(self.slot1)
        self.ui.bgColorEdit.textChanged.disconnect(self.slot1)
        self.ui.axisNumSpinBox.valueChanged.disconnect(self.slot1)
        
        self.ui.positionSpinBox1.valueChanged.disconnect(self.slot1)
        self.ui.positionSpinBox2.valueChanged.disconnect(self.slot1)
        self.ui.spanSpinBox1.valueChanged.disconnect(self.slot1)
        self.ui.spanSpinBox2.valueChanged.disconnect(self.slot1)
        self.ui.sizeSpinBox1.valueChanged.disconnect(self.slot1)
        self.ui.sizeSpinBox2.valueChanged.disconnect(self.slot1)
        
        self.ui.xAxisTitleEdit.textChanged.disconnect(self.slot1)
        self.ui.xAxisTitleColorEdit.textChanged.disconnect(self.slot1)
        self.ui.y1AxisTitleEdit.textChanged.disconnect(self.slot1)
        self.ui.y1AxisTitleColorEdit.textChanged.disconnect(self.slot1)
        self.ui.y2AxisTitleEdit.textChanged.disconnect(self.slot1)
        self.ui.y2AxisTitleColorEdit.textChanged.disconnect(self.slot1)
        self.ui.y3AxisTitleEdit.textChanged.disconnect(self.slot1)
        self.ui.y3AxisTitleColorEdit.textChanged.disconnect(self.slot1)

        self.ui.xMaxRangeSpinBox.valueChanged.disconnect(self.slot1)
        self.ui.y1MaxRangeSpinBox.valueChanged.disconnect(self.slot1)
        self.ui.y2MaxRangeSpinBox.valueChanged.disconnect(self.slot1)
        self.ui.y3MaxRangeSpinBox.valueChanged.disconnect(self.slot1)
        self.ui.xMinRangeSpinBox.valueChanged.disconnect(self.slot1)
        self.ui.y1MinRangeSpinBox.valueChanged.disconnect(self.slot1)
        self.ui.y2MinRangeSpinBox.valueChanged.disconnect(self.slot1)
        self.ui.y3MinRangeSpinBox.valueChanged.disconnect(self.slot1)

        self.ui.xMajorTickSpinBox.valueChanged.disconnect(self.slot1)
        self.ui.y1MajorTickSpinBox.valueChanged.disconnect(self.slot1)
        self.ui.y2MajorTickSpinBox.valueChanged.disconnect(self.slot1)
        self.ui.y3MajorTickSpinBox.valueChanged.disconnect(self.slot1)
        self.ui.xMinorTickSpinBox.valueChanged.disconnect(self.slot1)
        self.ui.y1MinorTickSpinBox.valueChanged.disconnect(self.slot1)
        self.ui.y2MinorTickSpinBox.valueChanged.disconnect(self.slot1)
        self.ui.y3MinorTickSpinBox.valueChanged.disconnect(self.slot1)
        

    def setupUi(self):
        self.ui.axisNumSpinBox.setRange(1, 3)

        self.ui.positionSpinBox1.setRange(0, 99)
        self.ui.positionSpinBox2.setRange(0, 99)
        self.ui.spanSpinBox1.setRange(0, 99)
        self.ui.spanSpinBox2.setRange(0, 99)
        self.ui.sizeSpinBox1.setRange(-1, 9999)
        self.ui.sizeSpinBox2.setRange(-1, 9999)

        self.ui.xMinRangeSpinBox.setRange(-999999999999., 999999999999.)
        self.ui.xMaxRangeSpinBox.setRange(-999999999999., 999999999999.)
        self.ui.y1MinRangeSpinBox.setRange(-999999999999., 999999999999.)
        self.ui.y1MaxRangeSpinBox.setRange(-999999999999., 999999999999.)
        self.ui.y2MinRangeSpinBox.setRange(-999999999999., 999999999999.)
        self.ui.y2MaxRangeSpinBox.setRange(-999999999999., 999999999999.)
        self.ui.y3MinRangeSpinBox.setRange(-999999999999., 999999999999.)
        self.ui.y3MaxRangeSpinBox.setRange(-999999999999., 999999999999.)

        self.ui.xMajorTickSpinBox.setRange(-999999999999., 999999999999.)
        self.ui.xMinorTickSpinBox.setRange(-999999999999., 999999999999.)
        self.ui.y1MajorTickSpinBox.setRange(-999999999999., 999999999999.)
        self.ui.y1MinorTickSpinBox.setRange(-999999999999., 999999999999.)
        self.ui.y2MajorTickSpinBox.setRange(-999999999999., 999999999999.)
        self.ui.y2MinorTickSpinBox.setRange(-999999999999., 999999999999.)
        self.ui.y3MajorTickSpinBox.setRange(-999999999999., 999999999999.)
        self.ui.y3MinorTickSpinBox.setRange(-999999999999., 999999999999.)


    def setupUiGraphFrameDetail(self, graphPropertyItem = None):
        self.ui.titleEdit.setText(graphPropertyItem.text(0))
        self.ui.bgColorEdit.setText(graphPropertyItem.text(1))
        self.ui.axisNumSpinBox.setValue(int(graphPropertyItem.text(16)))
        
        self.ui.positionSpinBox1.setValue(int(eval(graphPropertyItem.text(2))["c"]))
        self.ui.positionSpinBox2.setValue(int(eval(graphPropertyItem.text(2))["r"]))
        self.ui.spanSpinBox1.setValue(int(eval(graphPropertyItem.text(3))["c"]))
        self.ui.spanSpinBox2.setValue(int(eval(graphPropertyItem.text(3))["r"]))
        self.ui.sizeSpinBox1.setValue(int(eval(graphPropertyItem.text(4))["h"]))
        self.ui.sizeSpinBox2.setValue(int(eval(graphPropertyItem.text(4))["w"]))
        
        self.ui.xAxisTitleEdit.setText(graphPropertyItem.text(8))
        self.ui.xAxisTitleColorEdit.setText(graphPropertyItem.text(9))
        self.ui.y1AxisTitleEdit.setText(graphPropertyItem.text(10))
        self.ui.y1AxisTitleColorEdit.setText(graphPropertyItem.text(11))
        self.ui.y2AxisTitleEdit.setText(graphPropertyItem.text(12))
        self.ui.y2AxisTitleColorEdit.setText(graphPropertyItem.text(13))
        self.ui.y3AxisTitleEdit.setText(graphPropertyItem.text(14))
        self.ui.y3AxisTitleColorEdit.setText(graphPropertyItem.text(15))

        self.ui.xMaxRangeSpinBox.setValue(float(eval(graphPropertyItem.text(6))["xRange"]["max"]))
        self.ui.y1MaxRangeSpinBox.setValue(float(eval(graphPropertyItem.text(6))["y1Range"]["max"]))
        self.ui.y2MaxRangeSpinBox.setValue(float(eval(graphPropertyItem.text(6))["y2Range"]["max"]))
        self.ui.y3MaxRangeSpinBox.setValue(float(eval(graphPropertyItem.text(6))["y3Range"]["max"]))
        self.ui.xMinRangeSpinBox.setValue(float(eval(graphPropertyItem.text(6))["xRange"]["min"]))
        self.ui.y1MinRangeSpinBox.setValue(float(eval(graphPropertyItem.text(6))["y1Range"]["min"]))
        self.ui.y2MinRangeSpinBox.setValue(float(eval(graphPropertyItem.text(6))["y2Range"]["min"]))
        self.ui.y3MinRangeSpinBox.setValue(float(eval(graphPropertyItem.text(6))["y3Range"]["min"]))

        self.ui.xMajorTickSpinBox.setValue(float(eval(graphPropertyItem.text(7))["xTick"]["major"]))
        self.ui.y1MajorTickSpinBox.setValue(float(eval(graphPropertyItem.text(7))["y1Tick"]["major"]))
        self.ui.y2MajorTickSpinBox.setValue(float(eval(graphPropertyItem.text(7))["y2Tick"]["major"]))
        self.ui.y3MajorTickSpinBox.setValue(float(eval(graphPropertyItem.text(7))["y3Tick"]["major"]))
        self.ui.xMinorTickSpinBox.setValue(float(eval(graphPropertyItem.text(7))["xTick"]["minor"]))
        self.ui.y1MinorTickSpinBox.setValue(float(eval(graphPropertyItem.text(7))["y1Tick"]["minor"]))
        self.ui.y2MinorTickSpinBox.setValue(float(eval(graphPropertyItem.text(7))["y2Tick"]["minor"]))
        self.ui.y3MinorTickSpinBox.setValue(float(eval(graphPropertyItem.text(7))["y3Tick"]["minor"]))
