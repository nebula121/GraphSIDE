#-------------------------------------------------------------------------------
# Name:        GraphSIDE
# Author:      nebula121 <nebula121.dev@gmail.com>
# Copyright:   (c) nebula121 2018
# Licence:     MIT License
#-------------------------------------------------------------------------------

import sys
import gc
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import QUiLoader
from graphPreviewWidget import GraphPreviewWidget
from graphFrameSetting import GraphFrameSetting
from plotSetting import PlotSetting
from setting import Setting

class GraphSettingWidget(QDialog):
    
    def __init__(self, parent = None, generalSetting = {}, graphSetSetting = {}, dataSetSetting = {}):
        super(GraphSettingWidget, self).__init__(parent)
        
        self.tempGeneralSetting = generalSetting
        self.tempGraphSetSetting = graphSetSetting
        self.tempDataSetSetting = dataSetSetting

        self.ui = QUiLoader().load("./graphSetting.ui")
        self.setupUi()

        self.gf = GraphFrameSetting(graphSettingWidgetUi = self.ui)
        self.p = PlotSetting(plotSettingWidgetUi = self.ui, dataSetSetting = self.tempDataSetSetting)

        self.ui.graphTreeWidget.currentItemChanged.connect(lambda: self.setupUiGraphDetail(self.ui.graphTreeWidget.currentItem()))

        self.ui.graphNewButton.clicked.connect(lambda: self.insertTreeWidgetItem(treeWidget = self.ui.graphTreeWidget, 
                                                                                 index = self.ui.graphTreeWidget.indexOfTopLevelItem(self.ui.graphTreeWidget.currentItem())))
        self.ui.graphCopyButton.clicked.connect(lambda: self.insertTreeWidgetItem(treeWidget = self.ui.graphTreeWidget, 
                                                                                 index = self.ui.graphTreeWidget.indexOfTopLevelItem(self.ui.graphTreeWidget.currentItem()), 
                                                                                 item = self.ui.graphTreeWidget.currentItem().clone()))
        self.ui.graphUpButton.clicked.connect(lambda: self.moveTreeWidgetItem(treeWidget = self.ui.graphTreeWidget, 
                                                                                index = self.ui.graphTreeWidget.indexOfTopLevelItem(self.ui.graphTreeWidget.currentItem()), 
                                                                                direction = -1))
        self.ui.graphDownButton.clicked.connect(lambda: self.moveTreeWidgetItem(treeWidget = self.ui.graphTreeWidget, 
                                                                                index = self.ui.graphTreeWidget.indexOfTopLevelItem(self.ui.graphTreeWidget.currentItem()), 
                                                                                direction = +1))
        self.ui.graphDeleteButton.clicked.connect(lambda: self.deleteTreeWidgetItem(treeWidget = self.ui.graphTreeWidget, 
                                                                                   index = self.ui.graphTreeWidget.indexOfTopLevelItem(self.ui.graphTreeWidget.currentItem())))

        self.gf.graphFrameSettingChanged.connect(lambda: self.updateGraphPropertyItem1())
        self.p.plotSettingChanged.connect(lambda: self.updateGraphPropertyItem2())


    def setupUi(self):
        self.ui.graphEnableButton.setEnabled(False)
        self.ui.plotEnableButton.setEnabled(False)
        
        self.ui.graphTreeWidget.setHeaderLabels(["Title", "backgroundColor", 
                                                 "position", "span", "size", 
                                                 "plots", "range", "tick", 
                                                 "xAxisTitle", "xAxisTitleColor", 
                                                 "y1AxisTitle", "y1AxisTitleColor", 
                                                 "y2AxisTitle", "y2AxisTitleColor", 
                                                 "y3AxisTitle", "y3AxisTitleColor", 
                                                 "Num of axis", 
                                                 "Position (Span)", "Size", "Num of plots",])
        
        i = 1
        while i < 16:
            self.ui.graphTreeWidget.setColumnHidden(i, True)
            i += 1

        header = self.ui.graphTreeWidget.header()
        #header.moveSection(0, 0) # "Title" -> 0
        header.moveSection(16, 1) # "Axis" -> 3
        header.moveSection(17, 1) # "Position (Span)" -> 1
        header.moveSection(18, 2) # "Size" -> 2
        header.moveSection(19, 4) # "The number of plot" -> 4

        for key in sorted(self.tempGraphSetSetting["graphs"].keys()):
            graphSetting = self.tempGraphSetSetting["graphs"][key]
            graphPropertyItem = self.getTreeWidgetItemFromGraphSetting(graphSetting)

            self.ui.graphTreeWidget.addTopLevelItem(graphPropertyItem)

        self.ui.tabWidget.setCurrentIndex(0)


    def setupUiGraphDetail(self, graphPropertyItem = None):
        self.gf.disconnectUiChangedToSignal()

        self.gf.setupUiGraphFrameDetail(graphPropertyItem)
        self.p.setupUiGraphFrameDetail(graphPropertyItem)
        
        preview = GraphPreviewWidget(generalSetting = self.tempGeneralSetting, 
                                     graphSetting = self.getGraphSettingFromTreeWidgetItem(self.ui.graphTreeWidget.currentItem()), 
                                     dataSetSetting = self.tempDataSetSetting)
        pageNum = self.ui.stackedWidget.addWidget(preview.pw)

        self.ui.stackedWidget.currentWidget().deleteLater()
        self.ui.stackedWidget.setCurrentIndex(pageNum)

        self.gf.connectUiChangedToSignal()


    def updateGraphPropertyItem1(self):
        if self.ui.graphTreeWidget.currentItem():
            graphPropertyItem = self.ui.graphTreeWidget.currentItem()
            
            graphPropertyItem.setText(0, self.ui.titleEdit.text())
            graphPropertyItem.setText(1, self.ui.bgColorEdit.text())
            
            position = {"c": self.ui.positionSpinBox1.value(), 
                        "r": self.ui.positionSpinBox2.value()}
            span = {"c": self.ui.spanSpinBox1.value(), 
                    "r": self.ui.spanSpinBox2.value()}
            size = {"h": self.ui.sizeSpinBox1.value(), 
                    "w": self.ui.sizeSpinBox2.value()}
            graphPropertyItem.setText(2, str(position))
            graphPropertyItem.setText(3, str(span))
            graphPropertyItem.setText(4, str(size))

            range = {"xRange": {"max": self.ui.xMaxRangeSpinBox.value(), 
                                "min": self.ui.xMinRangeSpinBox.value()}, 
                     "y1Range": {"max": self.ui.y1MaxRangeSpinBox.value(), 
                                 "min": self.ui.y1MinRangeSpinBox.value()}, 
                     "y2Range": {"max": self.ui.y2MaxRangeSpinBox.value(), 
                                 "min": self.ui.y2MinRangeSpinBox.value()}, 
                     "y3Range": {"max": self.ui.y3MaxRangeSpinBox.value(), 
                                 "min": self.ui.y3MinRangeSpinBox.value()}}
            graphPropertyItem.setText(6, str(range))
            
            tick = {"xTick": {"major": self.ui.xMajorTickSpinBox.value(), 
                              "minor": self.ui.xMinorTickSpinBox.value()}, 
                    "y1Tick": {"major": self.ui.y1MajorTickSpinBox.value(), 
                               "minor": self.ui.y1MinorTickSpinBox.value()}, 
                    "y2Tick": {"major": self.ui.y2MajorTickSpinBox.value(), 
                               "minor": self.ui.y2MinorTickSpinBox.value()}, 
                    "y3Tick": {"major": self.ui.y3MajorTickSpinBox.value(), 
                               "minor": self.ui.y3MinorTickSpinBox.value()}}
            graphPropertyItem.setText(7, str(tick))

            graphPropertyItem.setText(8, self.ui.xAxisTitleEdit.text())
            graphPropertyItem.setText(9, self.ui.xAxisTitleColorEdit.text())
            graphPropertyItem.setText(10, self.ui.y1AxisTitleEdit.text())
            graphPropertyItem.setText(11, self.ui.y1AxisTitleColorEdit.text())
            graphPropertyItem.setText(12, self.ui.y2AxisTitleEdit.text())
            graphPropertyItem.setText(13, self.ui.y2AxisTitleColorEdit.text())
            graphPropertyItem.setText(14, self.ui.y3AxisTitleEdit.text())
            graphPropertyItem.setText(15, self.ui.y3AxisTitleColorEdit.text())
            
            graphPropertyItem.setText(16, str(self.ui.axisNumSpinBox.value()))
            
            graphPropertyItem.setText(17, str(eval(graphPropertyItem.text(2))["c"]) + "-" + str(eval(graphPropertyItem.text(2))["r"]) + 
                                  " (" + str(eval(graphPropertyItem.text(3))["c"]) + "-" + str(eval(graphPropertyItem.text(3))["r"]) + ")")
            graphPropertyItem.setText(18, str(eval(graphPropertyItem.text(4))["h"]) + "*" + str(eval(graphPropertyItem.text(4))["w"]))


    def updateGraphPropertyItem2(self):
        if self.ui.graphTreeWidget.currentItem():
            graphPropertyItem = self.ui.graphTreeWidget.currentItem()
            graphPropertyItem.setText(5, str(self.p.getPlotSettings()))
            graphPropertyItem.setText(19, str(len(self.p.getPlotSettings().keys())))


    def getTreeWidgetItemFromGraphSetting(self, graphSetting = Setting().getInitSettings()["graphSet"]["graphSet1"]["graphs"]["graph1"]):
        item = QTreeWidgetItem([""])
        item.setText(0, graphSetting["title"])    
        item.setText(1, graphSetting["backgroundColor"])

        item.setText(2, str(graphSetting["position"]))
        item.setText(3, str(graphSetting["span"]))
        item.setText(4, str(graphSetting["size"]))
        item.setText(5, str(graphSetting["plots"]))
        item.setText(6, str(graphSetting["range"]))
        item.setText(7, str(graphSetting["tick"]))
        item.setText(8, graphSetting["xAxisTitle"])
        item.setText(9, graphSetting["xAxisTitleColor"])
        item.setText(10, graphSetting["y1AxisTitle"])
        item.setText(11, graphSetting["y1AxisTitleColor"])
        item.setText(12, graphSetting["y2AxisTitle"])
        item.setText(13, graphSetting["y2AxisTitleColor"])
        item.setText(14, graphSetting["y3AxisTitle"])
        item.setText(15, graphSetting["y3AxisTitleColor"])
        item.setText(16, str(graphSetting["yAxisNum"]))

        item.setText(17, str(graphSetting["position"]["c"]) + "-" + str(graphSetting["position"]["r"]) + 
                         " (" + str(graphSetting["span"]["c"]) + "-" + str(graphSetting["span"]["r"]) + ")")
        item.setText(18, str(graphSetting["size"]["h"]) + "*" + str(graphSetting["size"]["w"]))
        item.setText(19, str(len(graphSetting["plots"].keys())))

        return item


    def insertTreeWidgetItem(self, treeWidget = None, index = -1, item = None):
        if treeWidget is None:
            return

        if item is None:
            item = self.getTreeWidgetItemFromGraphSetting()

        if index != -1:
            treeWidget.insertTopLevelItem(index + 1, item)
        else:
            treeWidget.addTopLevelItem(item)


    def moveTreeWidgetItem(self, treeWidget = None, index = 0, direction = 0):
        if treeWidget is None:
            return
        if index == 0 and direction == -1:
            return
        if index == treeWidget.topLevelItemCount() - 1 and direction == +1:
            return

        item = treeWidget.takeTopLevelItem(index)
        treeWidget.insertTopLevelItem(index + direction, item)
        treeWidget.setCurrentItem(item)


    def deleteTreeWidgetItem(self, treeWidget = None, index = -1):
        item = treeWidget.takeTopLevelItem(index)
        del item


    def getCurrentGraphSettings(self):
        graphSettings = dict()

        i = 0
        while i < self.ui.graphTreeWidget.topLevelItemCount():
            graphSettings["graph" + str(i + 1)] = self.getGraphSettingFromTreeWidgetItem(item = self.ui.graphTreeWidget.topLevelItem(i))

            i += 1

        return graphSettings


    def getGraphSettingFromTreeWidgetItem(self, item = None):
        graphSetting = dict()

        graphSetting["title"] = item.text(0)
        graphSetting["backgroundColor"] = item.text(1)
        graphSetting["position"] = eval(item.text(2))
        graphSetting["span"] = eval(item.text(3))
        graphSetting["size"] = eval(item.text(4))
        graphSetting["plots"] = eval(item.text(5))
        graphSetting["range"] = eval(item.text(6))
        graphSetting["tick"] = eval(item.text(7))
        graphSetting["xAxisTitle"] = item.text(8)
        graphSetting["xAxisTitleColor"] = item.text(9)
        graphSetting["y1AxisTitle"] = item.text(10)
        graphSetting["y1AxisTitleColor"] = item.text(11)
        graphSetting["y2AxisTitle"] = item.text(12)
        graphSetting["y2AxisTitleColor"] = item.text(13)
        graphSetting["y3AxisTitle"] = item.text(14)
        graphSetting["y3AxisTitleColor"] = item.text(15)
        graphSetting["yAxisNum"] = int(item.text(16))

        return graphSetting
