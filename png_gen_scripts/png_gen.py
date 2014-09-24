import __main__
__main__.pymol_argv = ['pymol', '-qc'] #Quite, NO GUI

import os, time, sys, re
import pymol

pymol.finish_launching()

rootdir = os.getcwd()
lst_files = os.listdir(rootdir)

# Parameters
gm = "off"
pp_col = "[blue]"
pn_col = "[red]"

# Pymol command block
def pm_run(dx_fname):
    # Loading file.dx
    pymol.cmd.load(dx_fname, "map")
    pymol.cmd.set("grid_mode", gm)
    # Generating positive surface
    pymol.cmd.isosurface("pos", "map", "3.0")
    pymol.cmd.ramp_new("ramp_pos", "map", "[3.0]", pp_col)
    pymol.cmd.set("surface_color", "ramp_pos", "pos")
    #Generating negative surface
    pymol.cmd.isosurface("neg", "map", "-3.0")
    pymol.cmd.ramp_new("ramp_neg", "map", "[-3.0]", pn_col)
    pymol.cmd.set("surface_color", "ramp_neg", "neg")
    # Ramp disable
    pymol.cmd.disable("ramp_pos")
    pymol.cmd.disable("ramp_neg")

    # Isosurface orientation definition
    #pymol.cmd.set_view ((\
    #    -0.439835846,    0.782051682,   -0.441517681,\
    #     0.835682869,    0.536445975,    0.117695667,\
    #     0.328897208,   -0.317203999,   -0.889499903,\
    #     0.000000000,    0.000000000, -177.426544189,\
    #    37.558090210,   92.955863953,   67.706909180,\
    #  -3035.355224609, 3390.208251953,  -20.000000000 ))

    pymol.cmd.set_view(( \
        -0.378446817, 0.564376295, -0.733650088, \
        0.818151116, 0.574651182, 0.020030633, \
        0.432901353, -0.592657924, -0.679225504, \
        0.000000000, 0.000000000, -152.909423828, \
        36.482994080, 89.183769226, 67.111167908, \
        111.138999939, 194.679794312, -20.000000000 ))

    out_name = dx_fname.split('.')[0]
    pymol.cmd.bg_color("white")
    pymol.cmd.ray("1000")
    pymol.cmd.png(out_name)
    pymol.cmd.delete("all")


def run():
    for f in lst_files:
        if '.dx' in f:
            print "Processing %s" % f
            pm_run(f)

    pymol.cmd.quit()


run()			
