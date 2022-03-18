from propeller_design_tools.funcs import delete_all_widgets_from_layout, get_all_airfoil_files
from propeller_design_tools.airfoil import Airfoil
try:
    from PyQt5 import QtWidgets, QtCore
    from propeller_design_tools.helper_ui_subclasses import PDT_Label, PDT_GroupBox, PDT_PushButton, PDT_ComboBox, \
        PDT_CheckBox
    from propeller_design_tools.helper_ui_classes import RangeLineEditWidget, SingleAxCanvas, AxesComboBoxWidget
except:
    pass


class ExistingFoilDataWidget(QtWidgets.QWidget):
    def __init__(self, main_win: 'InterfaceMainWindow'):
        super(ExistingFoilDataWidget, self).__init__()
        self.main_win = main_win

        lay = QtWidgets.QVBoxLayout()
        self.setLayout(lay)

        title_lbl = PDT_Label('Existing Data (plot controls)', font_size=14)
        lay.addWidget(title_lbl)
        btm_lay = QtWidgets.QHBoxLayout()
        lay.addLayout(btm_lay)

        # RE
        re_grp = PDT_GroupBox('RE', font_size=11)
        self.re_lay = QtWidgets.QGridLayout()
        re_grp.setLayout(self.re_lay)
        btm_lay.addWidget(re_grp)

        # mach
        mach_grp = PDT_GroupBox('Mach', font_size=11)
        self.mach_lay = QtWidgets.QVBoxLayout()
        mach_grp.setLayout(self.mach_lay)
        btm_lay.addWidget(mach_grp)

        # ncrit
        ncrit_grp = PDT_GroupBox('Ncrit', font_size=11)
        self.ncrit_lay = QtWidgets.QVBoxLayout()
        ncrit_grp.setLayout(self.ncrit_lay)
        btm_lay.addWidget(ncrit_grp)

        # gets the all checkboxes in there
        self.update_airfoil()

    def update_airfoil(self, af: Airfoil = None):
        delete_all_widgets_from_layout(layout=self.re_lay)
        delete_all_widgets_from_layout(layout=self.mach_lay)
        delete_all_widgets_from_layout(layout=self.ncrit_lay)

        row = -1
        if af is not None:
            res, machs, ncrits = af.get_polar_data_grid()
            for i, re in enumerate(res):
                chk = PDT_CheckBox('{:.1e}'.format(re), checked=True)
                if i < len(res) / 2:
                    row = i
                    col = 0
                else:
                    row = i - int(len(res) / 2)
                    col = 1
                self.re_lay.addWidget(chk, i, 0)
                self.re_lay.addWidget(chk, row, col)
            for mach in machs:
                chk = PDT_CheckBox('{:.2f}'.format(mach), checked=True)
                self.mach_lay.addWidget(chk)
            for ncrit in ncrits:
                chk = PDT_CheckBox('{}'.format(ncrit), checked=True)
                self.ncrit_lay.addWidget(chk)

        self.all_re_chk = PDT_CheckBox('(Un)check all', checked=True)
        self.re_lay.addWidget(self.all_re_chk, row + 1, 0)
        self.all_mach_chk = PDT_CheckBox('(Un)check all', checked=True)
        self.mach_lay.addWidget(self.all_mach_chk)
        self.all_ncrit_chk = PDT_CheckBox('(Un)check all', checked=True)
        self.ncrit_lay.addWidget(self.all_ncrit_chk)


class FoilDataPointWidget(QtWidgets.QWidget):
    def __init__(self, main_win: 'InterfaceMainWindow'):
        super(FoilDataPointWidget, self).__init__()
        self.main_win = main_win

        lay = QtWidgets.QFormLayout()
        self.setLayout(lay)

        overwrite_chk = PDT_CheckBox('Overwrite Existing Data?', font_size=11)
        lay.addRow(PDT_Label('Add\nDatapoints\nBy Range:', font_size=14), overwrite_chk)
        lay.setAlignment(overwrite_chk, QtCore.Qt.AlignBottom)
        self.re_rle = RangeLineEditWidget(box_range=[1e4, 1e9], default_strs=['1e6', '1e7', '3e6'],
                                          spin_double_science='science')
        self.mach_rle = RangeLineEditWidget(box_range=[0, 10], box_single_step=0.05,
                                            default_strs=['0.00', '0.00', '0.10'], spin_double_science='double')
        self.ncrit_rle = RangeLineEditWidget(box_range=[4, 14], box_single_step=1, default_strs=['9', '9', '1'],
                                             spin_double_science='spin')
        lay.addRow(PDT_Label('Re:', font_size=12), self.re_rle)
        lay.addRow(PDT_Label('Mach:', font_size=12), self.mach_rle)
        lay.addRow(PDT_Label('Ncrit:', font_size=12), self.ncrit_rle)

        self.add_btn = PDT_PushButton('Add Data', font_size=12, width=110)
        self.reset_btn = PDT_PushButton('Reset Ranges', font_size=12, width=130)
        btn_lay = QtWidgets.QHBoxLayout()
        btn_lay.addStretch()
        btn_lay.addWidget(self.add_btn)
        btn_lay.addWidget(self.reset_btn)
        btn_lay.addStretch()
        lay.addRow(btn_lay)
        lay.setAlignment(btn_lay, QtCore.Qt.AlignRight)
        lay.setLabelAlignment(QtCore.Qt.AlignRight)

    def reset_ranges(self):
        self.re_rle.reset_boxes()
        self.mach_rle.reset_boxes()
        self.ncrit_rle.reset_boxes()

    def get_re_range(self):
        return self.re_rle.get_start_stop_step()

    def get_mach_range(self):
        return self.mach_rle.get_start_stop_step()

    def get_ncrit_range(self):
        return self.ncrit_rle.get_start_stop_step()


class FoilAnalysisWidget(QtWidgets.QWidget):
    def __init__(self):
        super(FoilAnalysisWidget, self).__init__()

        # airfoil group
        af_lay = QtWidgets.QHBoxLayout()
        self.setLayout(af_lay)
        af_left_lay = QtWidgets.QVBoxLayout()
        af_lay.addLayout(af_left_lay)
        af_center_lay = QtWidgets.QVBoxLayout()
        af_lay.addLayout(af_center_lay)
        af_right_lay = QtWidgets.QVBoxLayout()
        af_lay.addLayout(af_right_lay)

        # airfoil left
        af_left_lay.addStretch()
        self.exist_data_widg = ExistingFoilDataWidget(main_win=self)
        af_left_lay.addWidget(self.exist_data_widg)
        af_left_lay.addStretch()
        self.add_foil_data_widg = FoilDataPointWidget(main_win=self)
        af_left_lay.addWidget(self.add_foil_data_widg)
        af_left_lay.addStretch()

        # airfoil center
        af_center_top_lay = QtWidgets.QFormLayout()
        af_center_lay.addLayout(af_center_top_lay)
        self.select_foil_cb = PDT_ComboBox(width=150)
        self.select_foil_cb.addItems(['None'] + get_all_airfoil_files())
        af_center_top_lay.addRow(PDT_Label('Select Foil:', font_size=14), self.select_foil_cb)
        self.foil_xy_canvas = SingleAxCanvas(self, width=4, height=4)
        af_center_lay.addWidget(self.foil_xy_canvas)

        # airfoil right
        af_right_top_lay = QtWidgets.QFormLayout()
        af_right_lay.addLayout(af_right_top_lay)
        metrics_strs = ['alpha', 'CL', 'CD', 'CDp', 'CM', 'Top_Xtr', 'Bot_Xtr', 'CL/CD']
        ax_cb_widg = AxesComboBoxWidget(x_txts=['x-axis'] + metrics_strs, y_txts=['y-axis'] + metrics_strs,
                                        init_xtxt='CD', init_ytxt='CL')
        self.af_yax_cb, self.af_xax_cb = ax_cb_widg.yax_cb, ax_cb_widg.xax_cb
        af_right_top_lay.addRow(PDT_Label('Plot Metric:', font_size=14), ax_cb_widg)
        self.foil_metric_canvas = SingleAxCanvas(self, width=8, height=5.5)
        af_right_lay.addWidget(self.foil_metric_canvas)