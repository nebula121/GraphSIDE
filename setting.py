#-------------------------------------------------------------------------------
# Name:        GraphSIDE
# Author:      nebula121 <nebula121.dev@gmail.com>
# Copyright:   (c) nebula121 2018
# Licence:     MIT License
#-------------------------------------------------------------------------------

import sys
import os
from PySide.QtCore import *
from PySide.QtGui import *
import json
import codecs
import copy

class Setting(QObject):

    def __init__(self, parent = None, filePath = ""):
        super(Setting, self).__init__(parent)
        
        if filePath == "":
            self.settings = self.getInitSettings()
        else:
            self.settings = self.load(filePath)
            self.checkUpdateSettingVer(self.settings["lastState"]["settingVer"])
            self.autocopmliteAllSettings(self.settings)


    def load(self, filePath = ""):
        with codecs.open(filePath, 'r','utf-8') as f:
            return json.loads(f.read(),'utf-8')


    def save(self, filePath = "", settings = {}):
        # JSONファイル書き込み
        with  codecs.open(filePath, 'w','utf-8') as f:
            json.dump(settings, f, sort_keys=True, indent=4, ensure_ascii=False)


    def autocopmliteSettings(self, targetSettings, sampleSettings):
        for key in sampleSettings:
            if key not in targetSettings:
                targetSettings[key] = sampleSettings[key]


    def autocopmliteAllSettings(self, settings):
        self.autocopmliteSettings(settings["lastState"], self.getInitSettings()["lastState"])

        self.autocopmliteSettings(settings["general"], self.getInitSettings()["general"])

        for dataSetSettingTitle in settings["dataSet"]:
            dataSetSetting = settings["dataSet"][dataSetSettingTitle]
            self.autocopmliteSettings(dataSetSetting, self.getInitSettings()["dataSet"]["dataSet1"])

            for rawDataSettingTitle in dataSetSetting["rawData"]:
                rawDataSetSetting = dataSetSetting["rawData"][rawDataSettingTitle]
                self.autocopmliteSettings(rawDataSetSetting, self.getInitSettings()["dataSet"]["dataSet1"]["rawData"]["rawData1"])

            for calcDataSettingTitle in dataSetSetting["calcData"]:
                calcDataSetSetting = dataSetSetting["calcData"][calcDataSettingTitle]
                self.autocopmliteSettings(calcDataSetSetting, self.getInitSettings()["dataSet"]["dataSet1"]["calcData"]["calcData1"])

        for graphSetSettingTitle in settings["graphSet"]:
            graphSetSetting = settings["graphSet"][graphSetSettingTitle]
            self.autocopmliteSettings(graphSetSetting, self.getInitSettings()["graphSet"]["graphSet1"])

            for graphSettingTitle in graphSetSetting["graphs"]:
                graphSetting = graphSetSetting["graphs"][graphSettingTitle]
                self.autocopmliteSettings(graphSetting, self.getInitSettings()["graphSet"]["graphSet1"]["graphs"]["graph1"])

                for plotSettingTitle in graphSetting["plots"]:
                    plotSetting = graphSetting["plots"][plotSettingTitle]
                    self.autocopmliteSettings(plotSetting, self.getInitSettings()["graphSet"]["graphSet1"]["graphs"]["graph1"]["plots"]["plot1"])


    def checkUpdateSettingVer(self, settingVer):
        if settingVer == self.getInitSettings()["lastState"]["settingVer"]:
            return
        if settingVer == "0.00":
            self.updateSetting000to01()


    def updateSetting000to01(self): ##########################################################
        ####self.settings["general"] = self.getInitSettings()["general"]############

        oldDataSetSettings = copy.deepcopy(self.settings["dataSet"])
        oldGraphSetSettings = copy.deepcopy(self.settings["graphSet"])
        oldLastStateSetting = copy.deepcopy(self.settings["lastState"])
        
        updateLastStateSetting = self.settings["lastState"]
        updatedDataSetSettings = self.settings["dataSet"]
        updatedGraphSetSettings = self.settings["graphSet"]


        #dataSet設定をアップデート
        i = 1
        for key in sorted(oldDataSetSettings.keys()):
            oldDataSetSetting = oldDataSetSettings[key]
            updatedDataSetSetting = updatedDataSetSettings[key]

            updatedDataSetSetting["title"] = key
            updatedDataSetSetting["id"] = self.getRandomStr(length = 16)
            
            j = 1
            for rawDataKey in sorted(oldDataSetSetting["rawData"]):
                updatedDataSetSetting["rawData"]["rawData" + str(j)] = copy.deepcopy(oldDataSetSetting["rawData"]["data" + str(j)])
                del  updatedDataSetSetting["rawData"]["data" + str(j)]
                j += 1

            j = 1
            for calcDataKey in sorted(oldDataSetSetting["calcData"]):
                oldCalcDataSetting = oldDataSetSetting["calcData"]["data" + str(j)]
                updatedDataSetSetting["calcData"]["calcData" + str(j)] = copy.deepcopy(oldDataSetSetting["calcData"]["data" + str(j)])
                updatedCalcDataSetting = updatedDataSetSetting["calcData"]["calcData" + str(j)]
                rDataNum = len(updatedDataSetSetting["rawData"])

                for nData in ["firstData", "secondData"]:
                    if oldCalcDataSetting[nData] == 0:
                        updatedCalcDataSetting[nData] = "d" + str(1)
                    elif oldCalcDataSetting[nData] == rDataNum + 1:
                        updatedCalcDataSetting[nData] = "d" + str(2)
                    elif oldCalcDataSetting[nData] <= rDataNum:
                        updatedCalcDataSetting[nData] = "r" + str(oldCalcDataSetting[nData])
                    elif oldCalcDataSetting[nData] > rDataNum + 1:
                        updatedCalcDataSetting[nData] = "c" + str(oldCalcDataSetting[nData] - rDataNum)

                del updatedDataSetSetting["calcData"]["data" + str(j)]
                j += 1

            updatedDataSetSettings["dataSet" + str(i)] = updatedDataSetSetting
            del updatedDataSetSettings[key]
            i += 1


        #graphSet設定をアップデート
        dataSetTitleList = list()
        for dataSetTitle in sorted(oldDataSetSettings.keys()):
            dataSetTitleList.append(dataSetTitle)

        i = 1
        for key in sorted(oldGraphSetSettings.keys()):
            #oldGraphSetSettingを用意
            oldGraphSetSetting = oldGraphSetSettings[key]
            updatedGraphSetSetting = updatedGraphSetSettings[key]

            updatedGraphSetSetting["title"] = key
            updatedGraphSetSetting["id"] = self.getRandomStr(length = 16)
            
            #使用dataSet情報を更新 findDataSetIndex
            usedDataSetTitle = oldGraphSetSetting["dataSet"]
            dataSetIndex = sorted(dataSetTitleList).index(usedDataSetTitle) + 1

            del updatedGraphSetSetting["dataSet"]
            updatedGraphSetSetting["dataSet"] = {
                "index" : dataSetIndex, 
                "id": updatedDataSetSettings["dataSet" + str(dataSetIndex)]["id"]
                }

            #graph設定をアップデート
            for graphKey in sorted(oldGraphSetSetting["graphs"]):
                #crを修正
                updatedGraphSetSetting["graphs"][graphKey]["position"]["c"] = oldGraphSetSetting["graphs"][graphKey]["position"]["r"]
                updatedGraphSetSetting["graphs"][graphKey]["position"]["r"] = oldGraphSetSetting["graphs"][graphKey]["position"]["c"]
                updatedGraphSetSetting["graphs"][graphKey]["span"]["c"] = oldGraphSetSetting["graphs"][graphKey]["span"]["r"]
                updatedGraphSetSetting["graphs"][graphKey]["span"]["r"] = oldGraphSetSetting["graphs"][graphKey]["span"]["c"]
                
                #graph設定をアップデート
                for plotKey in sorted(oldGraphSetSetting["graphs"][graphKey]["plots"].keys()):
                    oldPlotSetting = oldGraphSetSetting["graphs"][graphKey]["plots"][plotKey]
                    updatedPlotSetting = updatedGraphSetSetting["graphs"][graphKey]["plots"][plotKey]
                    usedDataSetIndex = oldGraphSetSetting["dataSet"]
                    rDataNum = len(oldDataSetSettings[usedDataSetIndex]["rawData"])
                    cDataNum = len(oldDataSetSettings[usedDataSetIndex]["calcData"])

                    for xy in ["x", "y"]:
                        if oldPlotSetting[xy] == 0:
                            updatedPlotSetting[xy] = "d1"
                        elif oldPlotSetting[xy] == rDataNum + cDataNum + 1:
                            updatedPlotSetting[xy] = "d2"
                        elif oldPlotSetting[xy] <= rDataNum:
                            updatedPlotSetting[xy] = "r" + str(oldPlotSetting[xy])
                        elif oldPlotSetting[xy] <= rDataNum + cDataNum:
                            updatedPlotSetting[xy] = "c" + str(oldPlotSetting[xy] - rDataNum)

                    if updatedPlotSetting["style"] not in ["Line (Solid)", "Line (Dash)", "Line (Dot)", "Line (DashDot)", "Line (DashDotDot)", 
                                  "Point (Circle)", "Point (Square)", "Point (Triangle)", "Point (Diamond)", "Point (Plus)"]:
                        updatedPlotSetting["style"] = "Line (Solid)"

            updatedGraphSetSettings["graphSet" + str(i)] = updatedGraphSetSetting
            del updatedGraphSetSettings[key]

            i += 1
        
        
        #lastState設定をアップデート
        del updateLastStateSetting["graphSet"]
        updateLastStateSetting["graphSet"] = {
            "index": 1, 
            "id": updatedGraphSetSettings["graphSet1"]["id"]
            }
        
        updateLastStateSetting["settingVer"] = "0.1"

        
        del oldDataSetSettings
        del oldGraphSetSettings
        del oldLastStateSetting
        
        self.settings["dataSet"] = updatedDataSetSettings
        self.settings["graphSet"] = updatedGraphSetSettings
        self.settings["lastState"] = updateLastStateSetting


    def getRandomStr(self, length, chars=None):
        import random
        import string
        if chars is None:
            chars = string.digits + string.ascii_letters
        return ''.join([random.choice(chars) for i in range(length)])


    def getInitSettings(self):
        return {
            "general": {
                "font1": "",                                        # new
                "font2": "",                                        # new
                "fontSize": 10.5                                    # new
                }, 
            "lastState": {
                "dir": "",
                "graphSet": {                                       # title -> dict(index, id)
                    "index": 1,                                     # new
                    "id": ""                                        # new
                    }, 
                "geometry": "0, 0, 0, 0",                           # new
                "settingVer": "0.1",                                # update
                },
            "shortcut": {
                "sample": ".\\sample"                               # modify
                },
            "dataSet": {
                "dataSet1": {                                       # title -> dataSetStrIndex
                    "title": "Data set",                            # modify
                    "id": self.getRandomStr(length = 16),           # new
                    "enable": True,
                    "headerNum": 0,                                 # 1 -> 0
                    "rawData": {
                        "rawData1": {                               # modify
                            "coefficient": 1.,
                            "name": "Raw data"                      # modify
                            }
                        },
                    "calcData": {
                        "calcData1": {                              # modify
                            "name": "Calc data",                    # modify
                            "firstCoefficient": 1.,
                            "firstData": "d1",                      # dataListIndex -> dataId
                            "operator": "+",
                            "secondCoefficient": 1.,
                            "secondData": "d1"                      # dataListIndex -> dataId
                            }
                        }
                    }
                },
            "graphSet": {
                "graphSet1": {                                      # title -> graphSetStrIndex
                    "title": "Graph set",                           # modify
                    "id": self.getRandomStr(length = 16),           # new
                    "enable": True,
                    "antialias": True,
                    "dataSet": {                                    # title -> dict(index, id)
                        "index": 1,                                 # new
                        "id": ""                                    # new
                        },
                    "graphs": {
                        "graph1": {
                            "title": "Graph",                       # modify
                            "id": self.getRandomStr(length = 16),   # new
                            "backgroundColor": "#FFFFFF",
                            "position": {
                                "c": 1,                             # modify
                                "r": 1                              # modify
                                },
                            "span": {
                                "c": 1,                             # modify
                                "r": 1                              # modify
                                },
                            "size": {
                                "h": 200,
                                "w": 300
                                },
                            "plots": {
                                "plot1": {
                                    "title": "Plot",                # modify
                                    "color": "k",
                                    "dataScopeMax": -1,
                                    "dataScopeMin": -1,
                                    "x": "d1",                      # dataListIndex -> dataId
                                    "y": "d1",                      # dataListIndex -> dataId
                                    "yAxis": 0,
                                    "style": "Line (Solid)"
                                    }
                                },
                            "range": {
                                "xRange": {
                                    "max": 0,
                                    "min": 100
                                    },
                                "y1Range": {
                                    "max": 0,
                                    "min": 100
                                    },
                                "y2Range": {
                                    "max": 0,
                                    "min": 100
                                    },
                                "y3Range": {
                                    "max": 0,
                                    "min": 100
                                    }
                                },
                            "tick": {
                                "xTick": {
                                    "major": -1.0,
                                    "minor": -1.0
                                    },
                                "y1Tick": {
                                    "major": -1.0,
                                    "minor": -1.0
                                    },
                                "y2Tick": {
                                    "major": -1.0,
                                    "minor": -1.0
                                    },
                                "y3Tick": {
                                    "major": -1.0,
                                    "minor": -1.0
                                    }
                                },
                            "xAxisTitle": "x",
                            "xAxisTitleColor": "#000000",
                            "y1AxisTitle": "y1",
                            "y1AxisTitleColor": "#000000",
                            "y2AxisTitle": "y2",
                            "y2AxisTitleColor": "#000000",
                            "y3AxisTitle": "y3",
                            "y3AxisTitleColor": "#000000",
                            "yAxisNum": 3
                            }
                        }       
                    }        
                }    
            }

        #return {
        #    "lastState": {
        #        "dir": "",
        #        "graphSet": "",
        #        "settingVer": "0.00"
        #        },
        #    "shortcut": {
        #        "initSample": ".\\sample"
        #        },
        #    "dataSet": {
        #        "initSample": {
        #            "title": "",
        #            "enable": True,
        #            "headerNum": 1,
        #            "rawData": {
        #                "data1": {
        #                    "coefficient": 1.,
        #                    "name": ""
        #                    }
        #                },
        #            "calcData": {
        #                "data1": {
        #                    "name": "",
        #                    "firstCoefficient": 1.,
        #                    "firstData": 0,
        #                    "operator": "+",
        #                    "secondCoefficient": 1.,
        #                    "secondData": 0
        #                    }
        #                }
        #            }
        #        },
        #    "graphSet": {
        #        "initSample": {
        #            "title": "",
        #            "enable": True,
        #            "antialias": True,
        #            "dataSet": "Sample",
        #            "graphs": {
        #                "graph1": {
        #                    "title": "Graph",
        #                    "backgroundColor": "#FFFFFF",
        #                    "position": {
        #                        "c": 1,
        #                        "r": 1
        #                        },
        #                    "span": {
        #                        "c": 1,
        #                        "r": 1
        #                        },
        #                    "size": {
        #                        "h": 200,
        #                        "w": 300
        #                        },
        #                    "plots": {
        #                        "plot1": {
        #                            "title": "",
        #                            "color": "k",
        #                            "dataScopeMax": -1,
        #                            "dataScopeMin": -1,
        #                            "x": 0,
        #                            "y": 0,
        #                            "yAxis": 0,
        #                            "style": "Line (Solid)"
        #                            }
        #                        },
        #                    "range": {
        #                        "xRange": {
        #                            "max": 0,
        #                            "min": 100
        #                            },
        #                        "y1Range": {
        #                            "max": 0,
        #                            "min": 100
        #                            },
        #                        "y2Range": {
        #                            "max": 0,
        #                            "min": 100
        #                            },
        #                        "y3Range": {
        #                            "max": 0,
        #                            "min": 100
        #                            }
        #                        },
        #                    "tick": {
        #                        "xTick": {
        #                            "major": -1.0,
        #                            "minor": -1.0
        #                            },
        #                        "y1Tick": {
        #                            "major": -1.0,
        #                            "minor": -1.0
        #                            },
        #                        "y2Tick": {
        #                            "major": -1.0,
        #                            "minor": -1.0
        #                            },
        #                        "y3Tick": {
        #                            "major": -1.0,
        #                            "minor": -1.0
        #                            }
        #                        },
        #                    "xAxisTitle": "x",
        #                    "xAxisTitleColor": "#000000",
        #                    "y1AxisTitle": "y1",
        #                    "y1AxisTitleColor": "#000000",
        #                    "y2AxisTitle": "y2",
        #                    "y2AxisTitleColor": "#000000",
        #                    "y3AxisTitle": "y3",
        #                    "y3AxisTitleColor": "#000000",
        #                    "yAxisNum": 3
        #                    }
        #                }       
        #            }        
        #        }    
        #    }
