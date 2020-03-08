try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

from libs.utils import newIcon, labelValidator

BB = QDialogButtonBox


class LabelDialog(QDialog):

    def __init__(self, text="Enter object label", parent=None, listItem=None):
        super(LabelDialog, self).__init__(parent)

        self.edit = QLineEdit()
        self.edit.setText(text)
        self.edit.setValidator(labelValidator())
        self.edit.editingFinished.connect(self.postProcess)

        model = QStringListModel()
        model.setStringList(listItem)
        completer = QCompleter()
        completer.setModel(model)
        self.edit.setCompleter(completer)

        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        bottomLayout = QHBoxLayout()
        if listItem is not None and len(listItem) > 0:
            self.listWidget = QListWidget(self)
            for item in listItem:
                self.listWidget.addItem(item)
            self.listWidget.itemClicked.connect(self.listItemClick)
            self.listWidget.itemDoubleClicked.connect(self.listItemDoubleClick)
            bottomLayout.addWidget(self.listWidget)

        angleItem = ['上', '左', '右', '下', '倾斜']
        if angleItem is not None and len(angleItem) > 0:
            self.listWidgetAngle = QListWidget(self)
            for item in angleItem:
                self.listWidgetAngle.addItem(item)
            self.listWidgetAngle.itemClicked.connect(self.listItemAngleClick)
            #self.listWidgetDirection.itemDoubleClicked.connect(self.listItemDoubleClick)
            self.listWidgetAngle.setCurrentRow(0)
            bottomLayout.addWidget(self.listWidgetAngle)

        directionItem = ['正对', '侧对']
        if directionItem is not None and len(directionItem) > 0:
            self.listWidgetDirection = QListWidget(self)
            for item in directionItem:
                self.listWidgetDirection.addItem(item)
            self.listWidgetDirection.itemClicked.connect(self.listItemDirectionClick)
            #self.listWidgetDirection.itemDoubleClicked.connect(self.listItemDoubleClick)
            self.listWidgetDirection.setCurrentRow(0)
            bottomLayout.addWidget(self.listWidgetDirection)

        layout.addLayout(bottomLayout)
        self.setLayout(layout)

        self.angle = '上'
        self.direction = '正对'

    def validate(self):
        try:
            if self.edit.text().trimmed():
                self.accept()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            if self.edit.text().strip():
                self.accept()

    def postProcess(self):
        try:
            self.edit.setText(self.edit.text().trimmed())
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            self.edit.setText(self.edit.text())

    def popUp(self, text='', angle='', direction='', move=True):
        self.edit.setText(text)
        self.edit.setSelection(0, len(text))
        self.edit.setFocus(Qt.PopupFocusReason)
        for i in range(len(self.listWidget)):
            if text == self.listWidget.item(i).text():
                self.listWidget.setCurrentRow(i)
                break
        for i in range(len(self.listWidgetAngle)):
            if angle == self.listWidgetAngle.item(i).text():
                self.listWidgetAngle.setCurrentRow(i)
                break
        for i in range(len(self.listWidgetDirection)):
            if direction == self.listWidgetDirection.item(i).text():
                self.listWidgetDirection.setCurrentRow(i)
                break
        if move:
            self.move(QCursor.pos())
        return (self.edit.text(), self.angle, self.direction) if self.exec_() else (None, None, None)

    def listItemClick(self, tQListWidgetItem):
        try:
            text = tQListWidgetItem.text().trimmed()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            text = tQListWidgetItem.text().strip()
        self.edit.setText(text)

    def listItemDoubleClick(self, tQListWidgetItem):
        self.listItemClick(tQListWidgetItem)
        self.validate()

    def listItemAngleClick(self, tQListWidgetItem):
        try:
            text = tQListWidgetItem.text().trimmed()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            text = tQListWidgetItem.text().strip()
        self.angle = text

    def listItemDirectionClick(self, tQListWidgetItem):
        try:
            text = tQListWidgetItem.text().trimmed()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            text = tQListWidgetItem.text().strip()
        self.direction = text