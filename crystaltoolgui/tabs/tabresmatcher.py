# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tabresmatcher.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_tabresmatcher(object):
    def setupUi(self, tabresmatcher):
        tabresmatcher.setObjectName("tabresmatcher")
        tabresmatcher.resize(697, 570)
        self.horizontalLayout = QtWidgets.QHBoxLayout(tabresmatcher)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.vL_match_1 = QtWidgets.QVBoxLayout()
        self.vL_match_1.setObjectName("vL_match_1")
        self.l_match_res = QtWidgets.QLabel(tabresmatcher)
        self.l_match_res.setObjectName("l_match_res")
        self.vL_match_1.addWidget(self.l_match_res)
        self.lV_match_res = QtWidgets.QListView(tabresmatcher)
        self.lV_match_res.setObjectName("lV_match_res")
        self.vL_match_1.addWidget(self.lV_match_res)
        self.hL_match_pB1 = QtWidgets.QHBoxLayout()
        self.hL_match_pB1.setObjectName("hL_match_pB1")
        self.pB_match_choose_res = QtWidgets.QPushButton(tabresmatcher)
        self.pB_match_choose_res.setObjectName("pB_match_choose_res")
        self.hL_match_pB1.addWidget(self.pB_match_choose_res)
        self.pB_match_delete_res = QtWidgets.QPushButton(tabresmatcher)
        self.pB_match_delete_res.setObjectName("pB_match_delete_res")
        self.hL_match_pB1.addWidget(self.pB_match_delete_res)
        self.vL_match_1.addLayout(self.hL_match_pB1)
        self.horizontalLayout.addLayout(self.vL_match_1)
        self.vL_match_2 = QtWidgets.QVBoxLayout()
        self.vL_match_2.setContentsMargins(-1, 25, -1, -1)
        self.vL_match_2.setObjectName("vL_match_2")
        self.hL_match_pdb = QtWidgets.QHBoxLayout()
        self.hL_match_pdb.setObjectName("hL_match_pdb")
        self.pB_pdb = QtWidgets.QPushButton(tabresmatcher)
        self.pB_pdb.setObjectName("pB_pdb")
        self.hL_match_pdb.addWidget(self.pB_pdb)
        self.l_pdb = QtWidgets.QLabel(tabresmatcher)
        self.l_pdb.setObjectName("l_pdb")
        self.hL_match_pdb.addWidget(self.l_pdb)
        self.vL_match_2.addLayout(self.hL_match_pdb)
        self.fL_match_1 = QtWidgets.QFormLayout()
        self.fL_match_1.setObjectName("fL_match_1")
        self.l_old_algorithm = QtWidgets.QLabel(tabresmatcher)
        self.l_old_algorithm.setObjectName("l_old_algorithm")
        self.fL_match_1.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.l_old_algorithm)
        self.l_loss_atom = QtWidgets.QLabel(tabresmatcher)
        self.l_loss_atom.setObjectName("l_loss_atom")
        self.fL_match_1.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.l_loss_atom)
        self.sB_loss_atom = QtWidgets.QSpinBox(tabresmatcher)
        self.sB_loss_atom.setObjectName("sB_loss_atom")
        self.fL_match_1.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sB_loss_atom)
        self.l_threshold = QtWidgets.QLabel(tabresmatcher)
        self.l_threshold.setObjectName("l_threshold")
        self.fL_match_1.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.l_threshold)
        self.cB_threshold = QtWidgets.QComboBox(tabresmatcher)
        self.cB_threshold.setObjectName("cB_threshold")
        self.cB_threshold.addItem("")
        self.cB_threshold.addItem("")
        self.cB_threshold.addItem("")
        self.cB_threshold.addItem("")
        self.cB_threshold.addItem("")
        self.cB_threshold.addItem("")
        self.fL_match_1.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cB_threshold)
        self.l_dBS_threshold = QtWidgets.QLabel(tabresmatcher)
        self.l_dBS_threshold.setObjectName("l_dBS_threshold")
        self.fL_match_1.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.l_dBS_threshold)
        self.dSB_threshold = QtWidgets.QDoubleSpinBox(tabresmatcher)
        self.dSB_threshold.setObjectName("dSB_threshold")
        self.fL_match_1.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.dSB_threshold)
        self.rB_old_algorithm = QtWidgets.QRadioButton(tabresmatcher)
        self.rB_old_algorithm.setText("")
        self.rB_old_algorithm.setObjectName("rB_old_algorithm")
        self.fL_match_1.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.rB_old_algorithm)
        self.vL_match_2.addLayout(self.fL_match_1)
        self.hL_match_output = QtWidgets.QHBoxLayout()
        self.hL_match_output.setObjectName("hL_match_output")
        self.l_match_output = QtWidgets.QLabel(tabresmatcher)
        self.l_match_output.setObjectName("l_match_output")
        self.hL_match_output.addWidget(self.l_match_output)
        self.cB_Nm = QtWidgets.QCheckBox(tabresmatcher)
        self.cB_Nm.setObjectName("cB_Nm")
        self.hL_match_output.addWidget(self.cB_Nm)
        self.cB_Rwm = QtWidgets.QCheckBox(tabresmatcher)
        self.cB_Rwm.setObjectName("cB_Rwm")
        self.hL_match_output.addWidget(self.cB_Rwm)
        self.cB_Rwe2 = QtWidgets.QCheckBox(tabresmatcher)
        self.cB_Rwe2.setObjectName("cB_Rwe2")
        self.hL_match_output.addWidget(self.cB_Rwe2)
        self.cB_Rc = QtWidgets.QCheckBox(tabresmatcher)
        self.cB_Rc.setObjectName("cB_Rc")
        self.hL_match_output.addWidget(self.cB_Rc)
        self.vL_match_2.addLayout(self.hL_match_output)
        self.hL_match_sort = QtWidgets.QHBoxLayout()
        self.hL_match_sort.setObjectName("hL_match_sort")
        self.l_match_sort = QtWidgets.QLabel(tabresmatcher)
        self.l_match_sort.setObjectName("l_match_sort")
        self.hL_match_sort.addWidget(self.l_match_sort)
        self.lE_match_sort = QtWidgets.QLineEdit(tabresmatcher)
        self.lE_match_sort.setInputMask("")
        self.lE_match_sort.setMaxLength(32767)
        self.lE_match_sort.setObjectName("lE_match_sort")
        self.hL_match_sort.addWidget(self.lE_match_sort)
        self.vL_match_2.addLayout(self.hL_match_sort)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vL_match_2.addItem(spacerItem)
        self.hL_match_start = QtWidgets.QHBoxLayout()
        self.hL_match_start.setObjectName("hL_match_start")
        self.pB_match_start = QtWidgets.QPushButton(tabresmatcher)
        self.pB_match_start.setObjectName("pB_match_start")
        self.hL_match_start.addWidget(self.pB_match_start)
        self.l_match_start = QtWidgets.QLabel(tabresmatcher)
        self.l_match_start.setObjectName("l_match_start")
        self.hL_match_start.addWidget(self.l_match_start)
        self.vL_match_2.addLayout(self.hL_match_start)
        self.bar_match = QtWidgets.QProgressBar(tabresmatcher)
        self.bar_match.setProperty("value", 0)
        self.bar_match.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.bar_match.setObjectName("bar_match")
        self.vL_match_2.addWidget(self.bar_match)
        self.horizontalLayout.addLayout(self.vL_match_2)

        self.retranslateUi(tabresmatcher)
        self.cB_threshold.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(tabresmatcher)

    def retranslateUi(self, tabresmatcher):
        _translate = QtCore.QCoreApplication.translate
        tabresmatcher.setWindowTitle(_translate("tabresmatcher", "Form"))
        self.l_match_res.setText(_translate("tabresmatcher", "RES文件"))
        self.pB_match_choose_res.setText(_translate("tabresmatcher", "选择RES文件"))
        self.pB_match_delete_res.setText(_translate("tabresmatcher", "删除所选"))
        self.pB_pdb.setText(_translate("tabresmatcher", "选择待搜索结构(pdb)"))
        self.l_pdb.setText(_translate("tabresmatcher", "未选择"))
        self.l_old_algorithm.setText(_translate("tabresmatcher", "使用旧算法"))
        self.l_loss_atom.setText(_translate("tabresmatcher", "可损失原子数"))
        self.l_threshold.setText(_translate("tabresmatcher", "汇报阈值基于"))
        self.cB_threshold.setCurrentText(_translate("tabresmatcher", "无"))
        self.cB_threshold.setItemText(0, _translate("tabresmatcher", "无"))
        self.cB_threshold.setItemText(1, _translate("tabresmatcher", "匹配上次数Tm"))
        self.cB_threshold.setItemText(2, _translate("tabresmatcher", "匹配比例Rm"))
        self.cB_threshold.setItemText(3, _translate("tabresmatcher", "质量加权匹配比例Rwm"))
        self.cB_threshold.setItemText(4, _translate("tabresmatcher", "电子加权匹配比例Rwe2"))
        self.cB_threshold.setItemText(5, _translate("tabresmatcher", "坐标匹配相似度Rc"))
        self.l_dBS_threshold.setText(_translate("tabresmatcher", "汇报阈值"))
        self.l_match_output.setText(_translate("tabresmatcher", "输出指标"))
        self.cB_Nm.setText(_translate("tabresmatcher", "Nm"))
        self.cB_Rwm.setText(_translate("tabresmatcher", "Rwm"))
        self.cB_Rwe2.setText(_translate("tabresmatcher", "Rwe2"))
        self.cB_Rc.setText(_translate("tabresmatcher", "Rc"))
        self.l_match_sort.setText(_translate("tabresmatcher", "排序规则"))
        self.lE_match_sort.setText(_translate("tabresmatcher", "-Rwe2,-Rwm,-Nm,-Rc"))
        self.pB_match_start.setText(_translate("tabresmatcher", "开始匹配"))
        self.l_match_start.setText(_translate("tabresmatcher", "未开始匹配"))
