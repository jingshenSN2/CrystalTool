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
        tabmatchresult.resize(886, 651)
        self.horizontalLayout = QtWidgets.QHBoxLayout(tabmatchresult)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.vL_result = QtWidgets.QVBoxLayout()
        self.vL_result.setObjectName("vL_result")
        self.l_result = QtWidgets.QLabel(tabmatchresult)
        self.l_result.setObjectName("l_result")
        self.vL_result.addWidget(self.l_result)
        self.hL_result_tV = QtWidgets.QHBoxLayout()
        self.hL_result_tV.setObjectName("hL_result_tV")
        self.tV_results = QtWidgets.QTableView(tabmatchresult)
        self.tV_results.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tV_results.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tV_results.setObjectName("tV_results")
        self.hL_result_tV.addWidget(self.tV_results)
        self.line = QtWidgets.QFrame(tabmatchresult)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.hL_result_tV.addWidget(self.line)
        self.tV_results_detail = QtWidgets.QTableView(tabmatchresult)
        self.tV_results_detail.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tV_results_detail.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tV_results_detail.setObjectName("tV_results_detail")
        self.hL_result_tV.addWidget(self.tV_results_detail)
        self.vL_result.addLayout(self.hL_result_tV)
        self.hL_result_pB = QtWidgets.QHBoxLayout()
        self.hL_result_pB.setObjectName("hL_result_pB")
        self.pB_result_to_res = QtWidgets.QPushButton(tabmatchresult)
        self.pB_result_to_res.setObjectName("pB_result_to_res")
        self.hL_result_pB.addWidget(self.pB_result_to_res)
        self.line_2 = QtWidgets.QFrame(tabmatchresult)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.hL_result_pB.addWidget(self.line_2)
        self.pB_result_fig = QtWidgets.QPushButton(tabmatchresult)
        self.pB_result_fig.setObjectName("pB_result_fig")
        self.hL_result_pB.addWidget(self.pB_result_fig)
        self.vL_result.addLayout(self.hL_result_pB)
        self.horizontalLayout.addLayout(self.vL_result)

        self.retranslateUi(tabmatchresult)
        QtCore.QMetaObject.connectSlotsByName(tabmatchresult)

    def retranslateUi(self, tabmatchresult):
        _translate = QtCore.QCoreApplication.translate
        tabmatchresult.setWindowTitle(_translate("tabmatchresult", "Form"))
        self.l_result.setText(_translate("tabmatchresult", "结果概览"))
        self.pB_result_to_res.setText(_translate("tabmatchresult", "另存为所选到新RES文件"))
        self.pB_result_fig.setText(_translate("tabmatchresult", "查看图片"))

