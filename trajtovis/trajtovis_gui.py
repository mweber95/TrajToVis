import pathlib
import os
import trajtovis

try:
    from pymol import cmd
    from pymol.Qt import QtWidgets, utils, QtCore
except ModuleNotFoundError:
    print("Pymol is not installed.")

# global reference to avoid garbage collection of our dialog
dialog = None

def __init_plugin__(app=None):
    from pymol.plugins import addmenuitemqt
    addmenuitemqt('TrajToVis', run_plugin_gui)


def run_plugin_gui():
    """
    Create the GUI Window
    """
    global dialog
    if dialog is None:
        dialog = App(_pymol_running=True)

    dialog.show()


class App(QtWidgets.QWidget):
    def __init__(self, _pymol_running=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visualisation_core: list = []
        self.pdbText = None
        self.file_name_pdb: str = ''
        module_dir: pathlib.Path = pathlib.Path(__file__).parent
        trajtovis_ui: str = str(module_dir.joinpath('trajtovis.ui'))
        pdb_show_ui: str = str(module_dir.joinpath('pdb_show.ui'))
        utils.loadUi(trajtovis_ui, self)
        self.textWindow = QtWidgets.QDialog(self)
        self.file_name_path_pdb = None
        utils.loadUi(pdb_show_ui, self.textWindow)

        # initialize form element states
        self.show_pdb.setEnabled(False)
        self.visualisation.setEnabled(False)

        # add gui elements logic
        self.load_pdb.clicked.connect(self.load_pdb_button)
        self.show_pdb.clicked.connect(self.show_pdb_file)
        self.visualisation.clicked.connect(self.visualise)
        self.core_visualisation_selection.clicked.connect(self.add_core_visualisation_selection)


    def load_pdb_button(self):
        """
        Load PDB or CIF file

        Parameters
        ----------
        file_name_path_pdb : str
        """
        self.file_name_path_pdb, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, "Load PDB / CIF", "", "PDB / CIF file (*.pdb *cif);;All Files (*)"
            )
        cmd.load(self.file_name_path_pdb)
        self.file_name_path_pdb = pathlib.Path(self.file_name_path_pdb)
        self.file_name_pdb = self.file_name_path_pdb.name
        with open(self.file_name_path_pdb, "r") as f:
            self.pdbText = f.read()
            self.show_pdb.setEnabled(True)
            self.visualisation.setEnabled(True)
        self.line_current_pdb.setText(self.file_name_pdb)

    def show_pdb_file(self):
        """
        Show the PDB file as a text file
        """
        if self.show_pdb.isEnabled():
            self.textWindow.textBrowser_pdbFile.setText(self.pdbText)
            self.textWindow.setWindowTitle(f'{self.file_name_pdb}')
            _ = self.textWindow.exec_()

    def add_resi(self):
        current = []
        start = self.start_resi.value()
        end = self.end_resi.value()
        current.append(start)
        current.append(end)
        self.visualisation_core.append(current)

    def visualise(self):
        if self.check_backbone.isChecked() or \
                self.visualisation_core or \
                self.check_cy3.isChecked() or \
                self.check_cy5.isChecked():
            self.visualisation_parameters()
        if self.visualisation_core:
            resi_selection = 'resi'
            for pair in self.visualisation_core:
                resi_selection = f'{resi_selection} {pair[0]}-{pair[1]}+'
            resi_selection = resi_selection[:-1]
            cmd.select("contact", resi_selection)
            cmd.set("cartoon_ladder_color", "hotpink", "contact")
            cmd.set("cartoon_ring_mode", "3", "contact")
            cmd.color("hotpink", "contact")
            self.visualisation_core.clear()
        if self.check_backbone.isChecked():
            cmd.set("cartoon_nucleic_acid_color", "gray")
            cmd.set("cartoon_ladder_color", "my_blue")
        if self.check_cy3.isChecked() or self.check_cy5.isChecked():
            cmd.select("dye_bases", "resn RUM+RGO")
            cmd.set("cartoon_ring_mode", "3", "dye_bases")
            cmd.show("sticks", "dye_bases")
            cmd.hide("sticks",
                     "dye_bases and name O4+H3+O2+H6+H1'+H2'1+HO'2+O2'+H4'+N3+C2+C4+C6+H6+N1+C1'+O4'+C3'+C4'+C5'+H5'+H5'2+O5'+O1P+O2P+P+H22+H8+H21+N2+N7+N9+H73")
            if self.check_cy3.isChecked():
                cmd.select("d_cy3", "resn RGO+C3W")
                cmd.color("don_cy3_green", "d_cy3")
                cmd.set("cartoon_ladder_color", "don_cy3_green", "d_cy3")
            if self.check_cy5.isChecked():
                cmd.select("d_cy5", "resn RUM+C5W")
                cmd.color("acc_cy5_red", "d_cy5")
                cmd.set("cartoon_ladder_color", "acc_cy5_red", "d_cy5")
            cmd.set("cartoon_ring_transparency", "0.7")


    @staticmethod
    def visualisation_parameters():
        cmd.bg_color("white")
        cmd.set("ray_trace_mode", "3")
        cmd.set_color("my_blue", "[103,169,207]")
        cmd.set_color("don_cy3_green", "[108,189,129]")
        cmd.set_color("acc_cy5_red", "[194,84,73]")

    def add_core_visualisation_selection(self):
        start = self.core_visualisation_start.value()
        end = self.core_visualisation_end.value()
        self.visualisation_core.append((start, end))

    def fancy_coloring(self):
        cmd.show("ribbon")
        cmd.set("ribbon_sampling", "20")
        cmd.set("ribbon_color", "gray")
        cmd.set("ribbon_transparency", "0.7")
        cmd.hide("cartoon")
        cmd.select("resn C5W and name C32")
        cmd.show("sphere", "sele")
        cmd.select("resn C3W and name C11")
        cmd.show("sphere", "sele")
        cmd.set("sphere_scale", "0.5")
        cmd.hide("sticks")
        cmd.split_states("KLTL_res_traj", "1", "100")
        cmd.select("KLTL_res_traj_0001 and resi 26-31+55-60")
        cmd.create("core", "sele")
        self.aligner("KLTL_res_traj_", "core", [1, 101])
        cmd.show("cartoon", "KLTL_res_traj_0001")

    def aligner(self, name, core, model_range):
        for i in np.arange(model_range[0], model_range[1]):
            cmd.align(f"{name}{'{:04d}'.format(i)}", core)
