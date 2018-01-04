#-------------------------------------------------------------------------------
# Name:        GraphSIDE
# Author:      nebula121 <nebula121.dev@gmail.com>
# Copyright:   (c) nebula121 2018
# Licence:     MIT License
#-------------------------------------------------------------------------------

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import QUiLoader
from setting import Setting

class GeneralSettingWidget(QDialog):
    
    def __init__(self, parent = None, generalSetting = {}, shortcutSetting = {}):
        super(GeneralSettingWidget, self).__init__(parent)
        
        self.tempGeneralSetting = generalSetting
        self.tempShortcutSetting = shortcutSetting

        self.ui = QUiLoader().load("./generalSetting.ui")
        self.setupUi()
        
        self.ui.shortcutTreeWidget.currentItemChanged.connect(lambda:  self.setupUiShortcutDetail(self.ui.shortcutTreeWidget.currentItem()))
        self.slot1 = lambda: self.updateShortcutPropertyItem(key = self.ui.shortcutEdit.text(), folderPath = self.ui.folderPathEdit.text())
        self.ui.shortcutEdit.textChanged.connect(self.slot1)
        self.ui.folderPathEdit.textChanged.connect(self.slot1)
       
        self.ui.shortcutNewButton.clicked.connect(lambda: self.insertShortcutSetting(index = self.ui.shortcutTreeWidget.indexOfTopLevelItem(self.ui.shortcutTreeWidget.currentItem())))
        self.ui.shortcutCopyButton.clicked.connect(lambda: self.insertShortcutSetting(index = self.ui.shortcutTreeWidget.indexOfTopLevelItem(self.ui.shortcutTreeWidget.currentItem()), 
                                                                                      shortcutProperty = self.ui.shortcutTreeWidget.currentItem().clone()))
        self.ui.shortcutUpButton.clicked.connect(lambda: self.moveTreeWidgetItem(index = self.ui.shortcutTreeWidget.indexOfTopLevelItem(self.ui.shortcutTreeWidget.currentItem()), 
                                                                                 direction = -1))
        self.ui.shortcutDownButton.clicked.connect(lambda: self.moveTreeWidgetItem(index = self.ui.shortcutTreeWidget.indexOfTopLevelItem(self.ui.shortcutTreeWidget.currentItem()), 
                                                                                 direction = +1))
        self.ui.shortcutSortButton.clicked.connect(lambda: self.ui.shortcutTreeWidget.sortItems(0, Qt.AscendingOrder))
        self.ui.shortcutDeleteButton.clicked.connect(lambda: self.deleteShortcutSetting(index = self.ui.shortcutTreeWidget.indexOfTopLevelItem(self.ui.shortcutTreeWidget.currentItem())))
        self.ui.folderSelectDialogButton.clicked.connect(lambda: self.openFolderSelectDialog(self.ui.folderPathEdit.text()))


    def setupUi(self):
        self.ui.font1ComboBox.setCurrentFont(QFont(self.tempGeneralSetting["font1"]))
        self.ui.font2ComboBox.setCurrentFont(QFont(self.tempGeneralSetting["font2"]))
        
        self.ui.fontSizeSpinBox.setDecimals(1)
        self.ui.fontSizeSpinBox.setValue(self.tempGeneralSetting["fontSize"])

        self.ui.shortcutTreeWidget.setHeaderLabels(["Shortcut", "Folder path"])

        for key in sorted(self.tempShortcutSetting):
            self.ui.shortcutTreeWidget.addTopLevelItem(self.getShortcutPropertyItem(key))


    def setupUiShortcutDetail(self, shortcutProperty):
        if shortcutProperty:
            self.ui.shortcutEdit.textChanged.disconnect(self.slot1)
            self.ui.folderPathEdit.textChanged.disconnect(self.slot1)
        
            self.ui.shortcutEdit.setText(shortcutProperty.text(0))
            self.ui.folderPathEdit.setText(shortcutProperty.text(1))

            self.ui.shortcutEdit.textChanged.connect(self.slot1)
            self.ui.folderPathEdit.textChanged.connect(self.slot1)


    def getShortcutPropertyItem(self, key = None):
        shortcutPropertyItem = QTreeWidgetItem()

        if key is not None:
            shortcutPropertyItem.setText(0, key)
            shortcutPropertyItem.setText(1, self.tempShortcutSetting[key])
        elif key is None:
            key = "sample"
            shortcutPropertyItem.setText(0, key)
            shortcutPropertyItem.setText(1, Setting().getInitSettings()["shortcut"][key])

        return shortcutPropertyItem


    def updateShortcutPropertyItem(self, key = "", folderPath = 0):
        if self.ui.shortcutTreeWidget.currentItem():
            shortcutProperty = self.ui.shortcutTreeWidget.currentItem()
            shortcutProperty.setText(0, key)
            shortcutProperty.setText(1, folderPath)


    def checkDuplicationShortcutKey(self):
        index = 0
        shortcutList = list()
        duplicateItemIndexList = list()

        while index < self.ui.shortcutTreeWidget.topLevelItemCount():
            if self.ui.shortcutTreeWidget.topLevelItem(index).text(0) in shortcutList:
                duplicateItemIndexList.append(index)
                if shortcutList.index(self.ui.shortcutTreeWidget.topLevelItem(index).text(0)) not in duplicateItemIndexList:
                    duplicateItemIndexList.append(shortcutList.index(self.ui.shortcutTreeWidget.topLevelItem(index).text(0)))

            shortcutList.append(self.ui.shortcutTreeWidget.topLevelItem(index).text(0))

            self.ui.shortcutTreeWidget.topLevelItem(index).setBackground(0, QBrush(Qt.transparent))

            index += 1

        for i in duplicateItemIndexList:
            self.ui.shortcutTreeWidget.topLevelItem(i).setBackground(0, QBrush(Qt.red))


    def openFolderSelectDialog(self, dir):
        self.ui.shortcutEdit.textChanged.disconnect(self.slot1)
        self.ui.folderPathEdit.textChanged.disconnect(self.slot1)

        dialog = QFileDialog(directory = dir)
        dialog.setFileMode(QFileDialog.Directory);
        dialog.setOption(QFileDialog.ShowDirsOnly, True);
        if dialog.exec():
            folderPath = dialog.selectedFiles()[0]
            folderPath = folderPath.replace('/', '\\')
            self.ui.folderPathEdit.setText(folderPath)
            
            self.updateShortcutPropertyItem(key = self.ui.shortcutEdit.text(), folderPath = self.ui.folderPathEdit.text())
        
        self.ui.shortcutEdit.textChanged.connect(self.slot1)
        self.ui.folderPathEdit.textChanged.connect(self.slot1)


    def getCurrentGeneralSetting(self):
        generalSetting = dict()
        generalSetting["font1"] = self.ui.font1ComboBox.currentFont().family()
        generalSetting["font2"] = self.ui.font2ComboBox.currentFont().family()
        generalSetting["fontSize"] = self.ui.fontSizeSpinBox.value()

        return generalSetting


    def getCurrentShortcutSettings(self):
        shortcutSettings  = dict()

        i = 0
        while i < self.ui.shortcutTreeWidget.topLevelItemCount():
            key = self.ui.shortcutTreeWidget.topLevelItem(i).text(0)
            shortcutSettings[key] = self.ui.shortcutTreeWidget.topLevelItem(i).text(1)

            i += 1

        return shortcutSettings


    def insertShortcutSetting(self, index = -1, shortcutProperty = None):
        if shortcutProperty is None:
            shortcutProperty = self.getShortcutPropertyItem()

        if index != -1:
            self.ui.shortcutTreeWidget.insertTopLevelItem(index + 1, shortcutProperty)
        else:
            self.ui.shortcutTreeWidget.addTopLevelItem(shortcutProperty)

        self.checkDuplicationShortcutKey()


    def moveTreeWidgetItem(self, index = 0, direction = 0):
        if index == 0 and direction == -1:
            return
        if index == self.ui.shortcutTreeWidget.topLevelItemCount() - 1 and direction == +1:
            return

        item = self.ui.shortcutTreeWidget.takeTopLevelItem(index)
        self.ui.shortcutTreeWidget.insertTopLevelItem(index + direction, item)
        self.ui.shortcutTreeWidget.setCurrentItem(item)


    def deleteShortcutSetting(self, index = -1):
        item = self.ui.shortcutTreeWidget.takeTopLevelItem(index)
        del item
        self.checkDuplicationShortcutKey()
