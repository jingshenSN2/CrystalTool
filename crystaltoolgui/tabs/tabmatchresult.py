# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tabmatchresult.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_tabmatchresult(object):
    def setupUi(self, tabmatchresult):
        tabmatchresult.setObjectName("tabmatchresult")
        tabmatchresult.resize(400, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(tabmatchresult)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.vL_result = QtWidgets.QVBoxLayout()
        self.vL_result.setObjectName("vL_result")
        self.l_result = QtWidgets.QLabel(tabmatchresult)
        self.l_result.setObjectName("l_result")
        self.vL_result.addWidget(self.l_result)
        self.tV_result = QtWidgets.QTableView(tabmatchresult)
        self.tV_result.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tV_result.setAlternatingRowColors(False)
        self.tV_result.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tV_result.setSortingEnabled(True)
        self.tV_result.setObjectName("tV_result")
        self.vL_result.addWidget(self.tV_result)
        self.hL_result_pB = QtWidgets.QHBoxLayout()
        self.hL_result_pB.setObjectName("hL_result_pB")
        self.pB_result_select = QtWidgets.QPushButton(tabmatchresult)
        self.pB_result_select.setObjectName("pB_result_select")
        self.hL_result_pB.addWidget(self.pB_result_select)
        self.pB_result_to_res = QtWidgets.QPushButton(tabmatchresult)
        self.pB_result_to_res.setObjectName("pB_result_to_res")
        self.hL_result_pB.addWidget(self.pB_result_to_res)
        self.vL_result.addLayout(self.hL_result_pB)
        self.horizontalLayout.addLayout(self.vL_result)

        self.retranslateUi(tabmatchresult)
        QtCore.QMetaObject.connectSlotsByName(tabmatchresult)

    def retranslateUi(self, tabmatchresult):
        _translate = QtCore.QCoreApplication.translate
        tabmatchresult.setWindowTitle(_translate("tabmatchresult", "Form"))
        self.l_result.setText(_translate("tabmatchresult", "结果概览"))
        self.pB_result_select.setText(_translate("tabmatchresult", "选择所有"))
        self.pB_result_to_res.setText(_translate("tabmatchresult", "另存为所选到新RES文件"))

