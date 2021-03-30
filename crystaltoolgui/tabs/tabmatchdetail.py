# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tabmatchdetail.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_tabmatchdetail(object):
    def setupUi(self, tabmatchdetail):
        tabmatchdetail.setObjectName("tabmatchdetail")
        self.horizontalLayout = QtWidgets.QHBoxLayout(tabmatchdetail)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.vL_detail_3d = QtWidgets.QVBoxLayout()
        self.vL_detail_3d.setObjectName("vL_detail_3d")
        self.l_detaial_3d = QtWidgets.QLabel(tabmatchdetail)
        self.l_detaial_3d.setObjectName("l_detaial_3d")
        self.vL_detail_3d.addWidget(self.l_detaial_3d)
        self.gV_3d = QtWidgets.QGraphicsView(tabmatchdetail)
        self.gV_3d.setObjectName("gV_3d")
        self.vL_detail_3d.addWidget(self.gV_3d)
        self.horizontalLayout.addLayout(self.vL_detail_3d)
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
        self.gV_2d = QtWidgets.QGraphicsView(tabmatchdetail)
        self.gV_2d.setObjectName("gV_2d")
        self.vL_detail_2d.addWidget(self.gV_2d)
        self.horizontalLayout.addLayout(self.vL_detail_2d)

        self.retranslateUi(tabmatchdetail)
        QtCore.QMetaObject.connectSlotsByName(tabmatchdetail)

    def retranslateUi(self, tabmatchdetail):
        _translate = QtCore.QCoreApplication.translate
        tabmatchdetail.setWindowTitle(_translate("tabmatchdetail", "Form"))
        self.l_detaial_3d.setText(_translate("tabmatchdetail", "3D图（可旋转）"))
        self.l_detail_2d.setText(_translate("tabmatchdetail", "二维投影图"))
        self.lE_detail_2d.setPlaceholderText(_translate("tabmatchdetail", "投影平面法向量，默认(0,0,1)"))
        self.pB_detail_2d.setText(_translate("tabmatchdetail", "重新绘制"))

