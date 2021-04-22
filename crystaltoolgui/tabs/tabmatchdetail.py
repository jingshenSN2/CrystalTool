# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tabmatchdetail.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_tabmatchdetail(object):
    def setupUi(self, tabmatchdetail):
        tabmatchdetail.setObjectName("tabmatchdetail")
        tabmatchdetail.resize(943, 654)
        self.horizontalLayout = QtWidgets.QHBoxLayout(tabmatchdetail)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.vL_detail_2d = QtWidgets.QVBoxLayout()
        self.vL_detail_2d.setObjectName("vL_detail_2d")
        self.hL_detail_2d = QtWidgets.QHBoxLayout()
        self.hL_detail_2d.setObjectName("hL_detail_2d")
        self.l_detail_2d = QtWidgets.QLabel(tabmatchdetail)
        self.l_detail_2d.setObjectName("l_detail_2d")
        self.hL_detail_2d.addWidget(self.l_detail_2d)
        self.lE_detail_2d = QtWidgets.QLineEdit(tabmatchdetail)
        self.lE_detail_2d.setObjectName("lE_detail_2d")
        self.hL_detail_2d.addWidget(self.lE_detail_2d)
        self.pB_detail_2d = QtWidgets.QPushButton(tabmatchdetail)
        self.pB_detail_2d.setObjectName("pB_detail_2d")
        self.hL_detail_2d.addWidget(self.pB_detail_2d)
        self.vL_detail_2d.addLayout(self.hL_detail_2d)
        self.horizontalLayout.addLayout(self.vL_detail_2d)
        self.line_detail = QtWidgets.QFrame(tabmatchdetail)
        self.line_detail.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_detail.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_detail.setObjectName("line_detail")
        self.horizontalLayout.addWidget(self.line_detail)
        self.vL_detail_3d = QtWidgets.QVBoxLayout()
        self.vL_detail_3d.setObjectName("vL_detail_3d")
        self.l_detaial_3d = QtWidgets.QLabel(tabmatchdetail)
        self.l_detaial_3d.setObjectName("l_detaial_3d")
        self.vL_detail_3d.addWidget(self.l_detaial_3d)
        self.horizontalLayout.addLayout(self.vL_detail_3d)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(2, 1)

        self.retranslateUi(tabmatchdetail)
        QtCore.QMetaObject.connectSlotsByName(tabmatchdetail)

    def retranslateUi(self, tabmatchdetail):
        _translate = QtCore.QCoreApplication.translate
        tabmatchdetail.setWindowTitle(_translate("tabmatchdetail", "Form"))
        self.l_detail_2d.setText(_translate("tabmatchdetail", "二维投影图"))
        self.lE_detail_2d.setPlaceholderText(_translate("tabmatchdetail", "投影平面法向量，默认(0,0,1)"))
        self.pB_detail_2d.setText(_translate("tabmatchdetail", "重新绘制"))
        self.l_detaial_3d.setText(_translate("tabmatchdetail", "3D图（可旋转）"))

