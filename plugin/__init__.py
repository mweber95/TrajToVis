# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os


def __init_plugin__(app=None):
    from pymol.plugins import addmenuitemqt
    addmenuitemqt('ABCD', run_plugin_gui)


# global reference to avoid garbage collection of our dialog
dialog = None


def run_plugin_gui():
    '''
    Open our custom dialog
    '''
    global dialog

    if dialog is None:
        dialog = make_dialog()

    dialog.show()


resi_list = []


def make_dialog():
    # entry point to PyMOL's API
    from pymol import cmd

    # pymol.Qt provides the PyQt5 interface, but may support PyQt4
    # and/or PySide as well
    from pymol.Qt import QtWidgets
    from pymol.Qt.utils import loadUi
    from pymol.Qt.utils import getSaveFileNameWithExt

    # create a new Window
    dialog = QtWidgets.QDialog()

    # populate the Window from our *.ui file which was created with the Qt Designer
    uifile = os.path.join(os.path.dirname(__file__), 'demowidget.ui')
    form = loadUi(uifile, dialog)

    def add_resi():

        current = []
        start = form.start_resi.value()
        end = form.end_resi.value()
        current.append(start)
        current.append(end)
        resi_list.append(current)
        print(current, resi_list)

    def structure_coloring():

        cmd.bg_color("white")
        cmd.set("cartoon_nucleic_acid_color", "gray")
        cmd.set("ray_trace_mode", "3")
        cmd.set_color("my_blue", "[103,169,207]")
        cmd.set("cartoon_ladder_color", "my_blue")
        cmd.set_color("don_green", "[108,189,129]")
        cmd.set_color("acc_red", "[194,84,73]")

        if form.label_check.isChecked() == True:
            cmd.select("dye_bases", "resn RUM+RGO")
            cmd.set("cartoon_ring_mode", "3", "dye_bases")
            cmd.show("sticks", "dye_bases")
            cmd.hide("sticks",
                     "dye_bases and name O4+H3+O2+H6+H1'+H2'1+HO'2+O2'+H4'+N3+C2+C4+C6+H6+N1+C1'+O4'+C3'+C4'+C5'+H5'+H5'2+O5'+O1P+O2P+P+H22+H8+H21+N2+N7+N9+H73")
            cmd.select("d_cy5", "resn RUM+C5W")
            cmd.select("d_cy3", "resn RGO+C3W")
            cmd.color("acc_red", "d_cy5")
            cmd.color("don_green", "d_cy3")
            cmd.set("cartoon_ladder_color", "acc_red", "d_cy5")
            cmd.set("cartoon_ladder_color", "don_green", "d_cy3")
            cmd.set("cartoon_ring_transparency", "0.7")

        if len(resi_list) != 0:
            hpresi = "resi "
            for set in resi_list:
                hpresi = hpresi + str(set[0]) + "-" + str(set[1]) + "+"
            hpresi = hpresi[:-1]
            print(hpresi)
            cmd.select("contact", hpresi)
            # cmd.color("hotpink", "contact")
            cmd.set("cartoon_ladder_color", "hotpink", "contact")
            cmd.set("cartoon_ring_mode", "3", "contact")
            cmd.color("hotpink", "contact")

        resi_list.clear()

    form.addButton.clicked.connect(add_resi)
    form.submit.clicked.connect(structure_coloring)

    return dialog