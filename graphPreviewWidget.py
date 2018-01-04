#-------------------------------------------------------------------------------
# Name:        GraphSIDE
# Author:      nebula121 <nebula121.dev@gmail.com>
# Copyright:   (c) nebula121 2018
# Licence:     MIT License
#-------------------------------------------------------------------------------

import sys
from PySide.QtCore import *
from PySide.QtGui import *
import pyqtgraph as pg
import random

class GraphPreviewWidget(QWidget):

    def __init__(self, parent = None, generalSetting = {}, graphSetting = {}, dataSetSetting = {}, dataSet = [], imageScale = 1):
        
        super(GraphPreviewWidget, self).__init__(parent)
        
        self.generalSetting = generalSetting
        self.dataSetSetting = dataSetSetting
        self.imageScale = imageScale
        self.fontScale = 10.5

        self.pw = pg.PlotWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.pw)
        self.setLayout(layout)
        #self.setCentralWidget(self.lw)

        dataSet = [[], [], [], []]
            
        self.setPenFont(generalSetting = self.generalSetting)
        self.createGraphSetView(graphSetting, dataSet)
        
        # w.setStyleSheet("background-image:url(./img.png)");
        
        self.pw.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)


    def setPenFont(self, imageScale = 1, graphLineScale = None, generalSetting = {}):
        if graphLineScale == None:
            graphLineScale = imageScale
        
        # Pen
        #self.myPenR = pg.mkPen(color='#FF2800', width = graphLineScale)    #FF2800(universal赤)
        #self.myPenY = pg.mkPen(color='#faf500', width = graphLineScale)    #faf500(universal黄色)
        #self.myPenG = pg.mkPen(color='#35A16B', width = graphLineScale)    #35A16B(universal緑)
        #self.myPenB = pg.mkPen(color='#0041FF', width = graphLineScale)    #0041FF(universal青)
        #self.myPenC = pg.mkPen(color='#66CCFF', width = graphLineScale)    #66CCFF(universal空色)
        #self.myPenP00 = pg.mkPen(color='#ff99a0', width = graphLineScale)  #ff99a0(universalピンク)
        #self.myPenO = pg.mkPen(color='#FF9900', width = graphLineScale)    #FF9900(universalオレンジ)
        #self.myPenP = pg.mkPen(color='#9a0079', width = graphLineScale)    #9a0079(universal紫)
        #self.myPenM00 = pg.mkPen(color='#663300', width = graphLineScale)  #663300(universal茶色)
        #self.myPenM01 = pg.mkPen(color='#ffd1d1', width = graphLineScale)  #ffd1d1(universal明るいピンク)　#ffff99　クリーム　#cbf266　lyg　
        #self.myPenLC = pg.mkPen(color='#B4EBFA', width = graphLineScale)   #edc58f　ベージュ　
        #self.myPenLG = pg.mkPen(color='#87E7B0', width = graphLineScale)   #87E7B0(universal) #c7b2de

        #self.myPenK = pg.mkPen(color='k', width = graphLineScale)          #ffffff #c8c8cb #7f878f #000000	universal while-gray-black
        #self.myPenK1 = pg.mkPen(color='#333333', width = graphLineScale)
        #self.myPenK2 = pg.mkPen(color='#666666', width = graphLineScale)
        #self.myPenK3 = pg.mkPen(color='#999999', width = graphLineScale)
        #self.myPenK4 = pg.mkPen(color='#CCCCCC', width = graphLineScale)

        # font
        self.font = QFont(generalSetting["font1"], generalSetting["fontSize"])
        self.fontCss = {'font-family': generalSetting["font1"] + ", " + generalSetting["font2"], 'font-size': str(generalSetting["fontSize"]) + 'pt'}
        self.fontCssLegend = '<style type="text/css"> p {font-family: ' + generalSetting["font1"] + ', ' + generalSetting["font2"] + '; font-size: ' + str(imageScale * generalSetting["fontSize"]) + 'pt; color: "#000000"} </style>'


    def createGraphSetView(self, graphSetting, dataSet):
        # [6.3-2] PlotWidget
        self.pIList = list()

        i = 0

        while i < 1:
            self.pIList.append(list())
            sideAxisList = list()

            invertXTF = bool(graphSetting["range"]["xRange"]["min"] > graphSetting["range"]["xRange"]["max"])
            invertYTF = bool(graphSetting["range"]["y1Range"]["min"] > graphSetting["range"]["y1Range"]["max"])

            self.pw = pg.PlotWidget(viewBox = pg.ViewBox(border = pg.mkPen(color='#000000', width = self.imageScale),
                                                             invertX = invertXTF, invertY = invertYTF))

            # [6.3-4] 
            self.pw.setBackground(graphSetting["backgroundColor"])

            #if graphSetting["size"]["h"] != 0 and graphSetting["size"]["w"] != 0:
            #    self.setMinimumSize(graphSetting["size"]["w"], graphSetting["size"]["h"])
            #    self.setMaximumSize(graphSetting["size"]["w"], graphSetting["size"]["h"])

            if graphSetting["yAxisNum"] == 1:

                # [6.3-5] plotItem
                p1 = self.pw.plotItem
                self.pIList[i].append(p1)

                sideAxisList.append(p1.getAxis('left'))

                # [6.3-22]
                self.initializeAxisItem(p1.getAxis('bottom'), sideAxisList[0])

            elif graphSetting["yAxisNum"] == 2:
                p1 = self.pw.plotItem
                p2 = pg.ViewBox(invertX = invertXTF, invertY = invertYTF)
                self.pIList[i].append(p1)
                self.pIList[i].append(p2)
                
                sideAxisList.append(p1.getAxis('left'))
                sideAxisList.append(p1.getAxis('right'))

                # [6.3-22]
                self.initializeAxisItem(p1.getAxis('bottom'), sideAxisList[0], sideAxisList[1])
                self.setMultipleAxisPlot(p1, p2)

            elif graphSetting["yAxisNum"] == 3:
                p1 = self.pw.plotItem
                p2 = pg.ViewBox(invertX = invertXTF, invertY = invertYTF)
                p3 = pg.ViewBox(invertX = invertXTF, invertY = invertYTF)
                ax3 = pg.AxisItem(orientation = 'right')
                self.pIList[i].append(p1)
                self.pIList[i].append(p2)
                self.pIList[i].append(p3)

                sideAxisList.append(p1.getAxis('left'))
                sideAxisList.append(p1.getAxis('right'))
                sideAxisList.append(ax3)

                # [6.3-22]
                self.initializeAxisItem(p1.getAxis('bottom'), sideAxisList[0], sideAxisList[1], sideAxisList[2])
                self.setMultipleAxisPlot(p1, p2, p3, ax3)
                
            # [6.3-7] 

            # [6.3-9] 
            p1.setRange(xRange = (graphSetting["range"]["xRange"]["min"],
                                  graphSetting["range"]["xRange"]["max"]),
                                  padding = 0)
            
            if graphSetting["xAxisTitleColor"] != None:
                fontCss = self.fontCss
                fontCss['color'] = graphSetting["xAxisTitleColor"]
                # [6.3-6] 
                p1.getAxis('bottom').setLabel(graphSetting["xAxisTitle"], **fontCss)

            tick = {}
            for m in ["major", "minor"]:
                if graphSetting["tick"]["xTick"][m] == -1:
                    tick[m] = None
                else:
                    tick[m] = graphSetting["tick"]["xTick"][m]
            p1.getAxis('bottom').setTickSpacing(tick["major"], tick["minor"])

            sideAxisNum = 1
            for ax, p in zip(sideAxisList, self.pIList[i]):
                if graphSetting["y" + str(sideAxisNum) + "AxisTitleColor"] != None:
                    fontCss = self.fontCss
                    fontCss['color'] = graphSetting["y" + str(sideAxisNum) + "AxisTitleColor"]
                    ax.setLabel(graphSetting["y" + str(sideAxisNum) + "AxisTitle"], **fontCss)

                tick = {}
                for m in ["major", "minor"]:
                    if graphSetting["tick"]["y" + str(sideAxisNum) + "Tick"][m] == -1:
                        tick[m] = None
                    else:
                        tick[m] = graphSetting["tick"]["y" + str(sideAxisNum) + "Tick"][m]
                ax.setTickSpacing(tick["major"], tick["minor"])

                p.setRange(yRange = (graphSetting["range"]["y" + str(sideAxisNum) + "Range"]["min"],
                                     graphSetting["range"]["y" + str(sideAxisNum) + "Range"]["max"]),
                           padding = 0)
                sideAxisNum += 1


            # [6.3-8] 
            j = 0

            while j < len(graphSetting["plots"]):
                plotSetting = graphSetting["plots"]["plot" + str(j + 1)]

                dataSet = [[], [], [], []]
                k = 0
                while k < 5:
                    dataSet[0].append(random.uniform(graphSetting["range"]["xRange"]["min"], graphSetting["range"]["xRange"]["max"]))
                    dataSet[1].append(random.uniform(graphSetting["range"]["y" + str(plotSetting["yAxis"] + 1) +"Range"]["min"], 
                                                     graphSetting["range"]["y" + str(plotSetting["yAxis"] + 1) +"Range"]["max"]))
                    k += 1


                if plotSetting["dataScopeMin"] == -1:
                    dataScopeMin = None
                else:
                    dataScopeMin = plotSetting["dataScopeMin"]

                if plotSetting["dataScopeMax"] == -1:
                    dataScopeMax = None
                else:
                    dataScopeMax = plotSetting["dataScopeMax"]

                style = {
                        "Line (Solid)": Qt.SolidLine, 
                        "Line (Dash)": Qt.DashLine, 
                        "Line (Dot)": Qt.DotLine, 
                        "Line (DashDot)": Qt.DashDotLine, 
                        "Line (DashDotDot)": Qt.DashDotDotLine,        
                        "Point (Circle)": "o", 
                        "Point (Square)": "s", 
                        "Point (Triangle)": "t", 
                        "Point (Diamond)": "d", 
                        "Point (Plus)": "+"
                        }

                if plotSetting["style"] not in style:
                    plotSetting["style"] = "Line (Solid)"

                if plotSetting["style"].startswith("Line"):
                    self.pIList[i][plotSetting["yAxis"]].addItem(
                        pg.PlotCurveItem(dataSet[0], #self.getDataIndex(plotSetting["x"])][dataScopeMin:dataScopeMax],
                                         dataSet[1], #self.getDataIndex(plotSetting["y"])][dataScopeMin:dataScopeMax],
                                         pen = pg.mkPen(color = plotSetting["color"], width = self.imageScale, style = style[plotSetting["style"]]),
                                         name = plotSetting["title"],
                                         antialias = True)#graphSetSetting["antialias"])
                                                             )

                if plotSetting["style"].startswith("Point"):
                    self.pIList[i][plotSetting["yAxis"]].addItem(
                        pg.ScatterPlotItem(dataSet[0],
                                           dataSet[1],
                                           symbol = style[plotSetting["style"]], 
                                           pen = pg.mkPen(None), 
                                           brush = pg.mkBrush(plotSetting["color"]),
                                           size = 5,
                                           name = plotSetting["title"],
                                           antialias = True)#graphSetSetting["antialias"])
                        )

                j += 1
                
            i += 1


    def initializeAxisItem(self, bottomAx, leftAx, rightAx = None, thirdAx = None):
        bottomAx.setPen(pg.mkPen(color='#000000', width = self.imageScale))
        bottomAx.setHeight(3 * self.fontScale)
        bottomAx.tickFont = self.font

        sideAxisList = [leftAx, rightAx, thirdAx]

        for ax in sideAxisList:
            if ax != None:
                ax.setPen(pg.mkPen(color='#000000', width = self.imageScale))
                ax.setWidth(4.5*self.fontScale)
                ax.tickFont = self.font


    def setMultipleAxisPlot(self, p1, p2, p3 = None, ax3 = None):
        p1.showAxis('right')
        p1.scene().addItem(p2)
        p1.getAxis('right').linkToView(p2)
        p2.setXLink(p1)

        p2.sigRangeChanged.connect(lambda: p2.setGeometry(p1.vb.sceneBoundingRect()))
        
        if p3 != None and ax3 != None:
            spacer = QGraphicsWidget()
            spacer.setMaximumSize(15,15)
            p1.layout.addItem(spacer, 2, 3)

            p1.layout.addItem(ax3, 2, 4)
            p1.scene().addItem(p3)
            ax3.linkToView(p3)
            p3.setXLink(p1)
            
            p3.sigRangeChanged.connect(lambda: p3.setGeometry(p1.vb.sceneBoundingRect()))


    def getDataIndex(self, dataProperty):
        defaultDataNum = 2
        rawDataNum = len(self.dataSetSetting["rawData"])
        calcDataNum = len(self.dataSetSetting["calcData"])

        if dataProperty[0] == "d":
            return int(dataProperty[1:]) - 1
        elif dataProperty[0] == "r":
            return defaultDataNum + int(dataProperty[1:]) - 1
        elif dataProperty[0] == "c":
            return defaultDataNum + rawDataNum + int(dataProperty[1:]) - 1


if __name__ == '__main__':
    # Qt Applicationを作ります
    app = QApplication(sys.argv)
    # formを作成して表示します
    mainWin = GraphPreviewWidget()
    mainWin.show()
    # Qtのメインループを開始します
    sys.exit(app.exec_())
