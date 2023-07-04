import pathlib
import os
from trajtovis.gui_functions import LogicForGui
from pymol import cmd


# global reference to avoid garbage collection of our dialog
dialog = None

def __init_plugin__(app=None):
    from pymol.plugins import addmenuitemqt
    addmenuitemqt('TrajToVis', run_plugin_gui)


def run_plugin_gui():
    """Open our custom dialog"""
    global dialog

    if dialog is None:
        dialog = make_dialog()

    dialog.show()

def make_dialog():
    from pymol.Qt import QtWidgets
    from pymol.Qt.utils import loadUi

    add_dialog = QtWidgets.QDialog()
    ui_file = os.path.join(os.path.dirname(__file__), 'trajtovis.ui')
    form = loadUi(ui_file, add_dialog)
    form.pushButton.clicked.connect(visualize)
    #LogicForGui().add_logic(form)
    return add_dialog

def visualize():
    cmd.load("/usr/local/lib/python3.8/dist-packages/trajtovis/KLTL_res_traj.pdb")