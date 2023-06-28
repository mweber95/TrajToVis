import os


# global reference to avoid garbage collection of our dialog
dialog = None
resi_list = []


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

    add_logic_to_form_items(form)

    return add_dialog


def add_logic_to_form_items(form):
    form.addButton.clicked.connect(add_resi)
    form.pushButton.clicked.connect(visualize)


def add_resi(form):
    current = []
    start = form.start_resi.value()
    end = form.end_resi.value()
    current.append(start)
    current.append(end)
    resi_list.append(current)


def visualize(structure_coloring, fancy_coloring):
    cmd.load("plugin/KLTL_res_traj.pdb")
    structure_coloring()
    fancy_coloring()


def fancy_coloring(aligner):
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
    aligner("KLTL_res_traj_", "core", [1, 101])
    cmd.show("cartoon", "KLTL_res_traj_0001")


def aligner(name, core, model_range):
    for i in np.arange(model_range[0], model_range[1]):
        cmd.align(f"{name}{'{:04d}'.format(i)}", core)


def structure_coloring():
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
        #cmd.color("hotpink", "contact")
        cmd.set("cartoon_ladder_color", "hotpink", "contact")
        cmd.set("cartoon_ring_mode", "3", "contact")
        cmd.color("hotpink", "contact")

    resi_list.clear()