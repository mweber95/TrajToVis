class LogicForGui:
    def __init__(self):
        self.resi_list = []

    def add_logic(self, form):
        form.addButton.clicked.connect(self.add_resi)
        form.pushButton.clicked.connect(self.visualize)

    def add_resi(self):
        current = []
        start = form.start_resi.value()
        end = form.end_resi.value()
        current.append(start)
        current.append(end)
        resi_list.append(current)

    def visualize(self):
        cmd.load("/usr/local/lib/python3.8/dist-packages/trajtovis/KLTL_res_traj.pdb")
        #self.structure_coloring()
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

        self.resi_list.clear()