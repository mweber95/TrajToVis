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
        self.colorful_residues: list = []
        self.pdbText = None
        self.file_name_pdb: str = ''
        module_dir: pathlib.Path = pathlib.Path(__file__).parent
        print(module_dir)
        trajtovis_ui = str(module_dir.joinpath('trajtovis.ui'))
        print(trajtovis_ui)
        pdb_show_ui = str(module_dir.joinpath('pdb_show.ui'))
        utils.loadUi(trajtovis_ui, self)
        self.textWindow = QtWidgets.QDialog(self)
        self.file_name_path_pdb = None
        utils.loadUi(pdb_show_ui, self.textWindow)

        # add gui elements logic
        self.load_pdb.clicked.connect(self.load_pdb_button)
        self.show_pdb.clicked.connect(self.open_pdb_file)


    def load_pdb_button(self, file_name_path_pdb=False):
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
        self.line_current_pdb.setText(self.file_name_pdb)

    def open_pdb_file(self):
        """
        Show the PDB file as a text file
        """
        self.textWindow.textBrowser_pdbFile.setText(self.pdbText)
        self.textWindow.setWindowTitle(f'{self.file_name_pdb}')
        is_ok = self.textWindow.exec_()

    def add_resi(self):
        current = []
        start = self.start_resi.value()
        end = self.end_resi.value()
        current.append(start)
        current.append(end)
        self.colorful_residues.append(current)

    def visualize(self):
        cmd.load("/usr/local/lib/python3.8/dist-packages/trajtovis/KLTL_res_traj.pdb")
        self.structure_coloring()
        #self.fancy_coloring()

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

    def structure_coloring(self):
        cmd.bg_color("white")
        cmd.set("cartoon_nucleic_acid_color", "gray")
        cmd.set("ray_trace_mode", "3")
        cmd.set_color("my_blue", "[103,169,207]")
        cmd.set("cartoon_ladder_color", "my_blue")
        cmd.set_color("don_green", "[108,189,129]")
        cmd.set_color("acc_red", "[194,84,73]")

        cmd.select("dye_bases", "resn RUM+RGO")
        cmd.set("cartoon_ring_mode", "3", "dye_bases")
        cmd.show("sticks", "dye_bases")
        cmd.hide("sticks",
                 "dye_bases and name O4+H3+O2+H6+H1'+H2'1+HO'2+O2'+H4'+N3+C2+C4+C6+H6+N1+C1'+O4'+C3'+C4'+C5'+H5'+H5'2+O5'+O1P+O2P+P+H22+H8+H21+N2+N7+N9+H73")

        if len(self.colorful_residues) != 0:
            hpresi = "resi "
            for group in self.colorful_residues:
                hpresi = hpresi + str(group[0]) + "-" + str(group[1]) + "+"
            hpresi = hpresi[:-1]
            print(hpresi)
            cmd.select("contact", hpresi)
            # cmd.color("hotpink", "contact")
            cmd.set("cartoon_ladder_color", "hotpink", "contact")
            cmd.set("cartoon_ring_mode", "3", "contact")
            cmd.color("hotpink", "contact")

        cmd.select("d_cy5", "resn RUM+C5W")
        cmd.select("d_cy3", "resn RGO+C3W")
        cmd.color("acc_red", "d_cy5")
        cmd.color("don_green", "d_cy3")
        cmd.set("cartoon_ladder_color", "acc_red", "d_cy5")
        cmd.set("cartoon_ladder_color", "don_green", "d_cy3")
        cmd.set("cartoon_ring_transparency", "0.7")

        self.colorful_residues.clear()