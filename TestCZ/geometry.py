import os
import numpy as np
from objectgmsh import Model, Shape, MeshControlLinear, MeshControlExponential, cut
import gmsh
import yaml
import matplotlib.pyplot as plt
from my_tools import inductor
from my_tools import inductor_filling
from objectgmsh import *

occ = gmsh.model.occ
def geometry(config, sim_dir="./", name="vgf", visualize=False):
    if not os.path.exists(sim_dir):
        os.makedirs(sim_dir)

    model = Model(name)
    #--------------------------------------------- MELT --------------------------------------------- #
    melt = Shape(model,2,"melt",[
            occ.add_rectangle(
                0,
                0,
                0,
                config["melt"]["r"],
                config["melt"]["h"],    )])
    melt.mesh_size = config["melt"]["mesh_size"] # we use "params" to save various values we need later
    melt.params.material = config["melt"]["material"]
    melt.params.T_init = config["melt"]["T_init"]
    #--------------------------------------------- Crucible --------------------------------------------- #
    crucible = Shape(model,2,"crucible",[
            occ.add_rectangle(
                0,
                - config["crucible"]["t_bt"],
                0,
                config["crucible"]["r_out"],
                config["crucible"]["h"],    )])
    
    crucible_hole = occ.add_rectangle(0,0,0,config["crucible"]["r_in"],config["crucible"]["h_in"])
    occ.cut(crucible.dimtags, [(2, crucible_hole)])

    crucible.mesh_size = config["crucible"]["mesh_size"]
    crucible.params.material = config["crucible"]["material"]
    crucible.params.T_init = config["crucible"]["T_init"]
    #--------------------------------------------- Crystal --------------------------------------------- #
    crystal = Shape(model,2,"crystal",[
            occ.add_rectangle(
                0,
                config["melt"]["h"],
                0,
                config["crystal"]["r"],
                config["crystal"]["h"], )])
    crystal.mesh_size = config["crystal"]["mesh_size"]
    crystal.params.material = config["crystal"]["material"]
    crystal.params.T_init = config["crystal"]["T_init"]   

    crystal_top = config["melt"]["h"] + config["crystal"]["h"]
    #--------------------------------------------- Seed --------------------------------------------- #
    seed = Shape(model,2,"seed",[
            occ.add_rectangle(
                0,
                crystal_top,
                0,
                config["seed"]["r"],
                config["seed"]["h"],    )])
    seed.mesh_size = config["seed"]["mesh_size"]
    seed.params.material = config["seed"]["material"]
    seed.params.T_init = config["seed"]["T_init"]  
    #--------------------------------------------- Axis Top --------------------------------------------- #
    axis_top = Shape(model,2,"axis_top",[
            occ.add_rectangle(
                0,
                config["axis_top"]["t"],
                0,
                config["axis_top"]["r"],
                config["axis_top"]["h"],    )])
    axis_top.mesh_size = config["axis_top"]["mesh_size"]
    axis_top.params.material = config["axis_top"]["material"]
    axis_top.params.T_init = config["axis_top"]["T_init"]  
    #--------------------------------------------- Inductors --------------------------------------------- #
    
    ind = inductor(model,2, **config["inductor"],name="inductor")
    ind_cut = inductor_filling(model,2, **config["inductor"],name="inductor_cut")

    
    # x = config["inductor"]["X0"][0]
    # y = config["inductor"]["X0"][1]
    # d = config["inductor"]["d"]
    # d_in = config["inductor"]["d_in"]
    # n = config["inductor"]["n"]
    # g =  config["inductor"]["g"]
    # geo_ids = []
    # for _ in range(n):
    #     circle_1d = occ.addCircle(x, y, 0, d / 2)
    #     circle = occ.addSurfaceFilling(occ.addCurveLoop([circle_1d]))
    #     hole_1d = occ.addCircle(x, y, 0, d_in / 2)
    #     hole = occ.addSurfaceFilling(occ.addCurveLoop([hole_1d]))
    #     occ.synchronize()
    #     occ.cut([(2, circle)], [(2, hole)])
    #     y += g + d
        

    # ind = Shape(model,2, "inductor", [circle])
    # ind.geo_ids.append(circle)


    # x = config["inductor"]["X0"][0]
    # y = config["inductor"]["X0"][1]
    # d = config["inductor"]["d"]
    # d_in = config["inductor"]["d_in"]
    # n = config["inductor"]["n"]
    # g =  config["inductor"]["g"]

    # # ind_cut = Shape(model,2, "inductor_cut")
    # geo_ids = []
    # for _ in range(n):
    #     #circle_1d = factory.addCircle(x, y, 0, d / 2)
    #     #circle = factory.addSurfaceFilling(factory.addCurveLoop([circle_1d]))
    #     hole_1d = factory.addCircle(x, y, 0, d_in / 2)
    #     hole = factory.addSurfaceFilling(factory.addCurveLoop([hole_1d]))
    #     occ.synchronize()
    #     y += g + d
        
    # ind_cut = Shape(model,2, "inductor_cut",[hole])
    # geo_ids.append(hole)


    #--------------------------------------------- crucible_adapter --------------------------------------------- #
    crucible_adapter = Shape(model,2,"crucible_adapter",[
            occ.add_rectangle(
                config["crucible_adapter"]["r_in"],
                - config["crucible_adapter"]["t_bt"],
                0,
                config["crucible_adapter"]["r_out"] -  config["crucible_adapter"]["r_in"],
                config["crucible_adapter"]["h"],    )])
    crucible_adapter.mesh_size = config["crucible_adapter"]["mesh_size"]
    crucible_adapter.params.material = config["crucible_adapter"]["material"]
    crucible_adapter.params.T_init = config["crucible_adapter"]["T_init"]
    #--------------------------------------------- Axis bottom --------------------------------------------- #
    axis_bt = Shape(model,2,"axis_bt",[
            occ.add_rectangle(
                config["axis_bt"]["r_in"],
                - config["axis_bt"]["t_bt"],
                0,
                config["axis_bt"]["r_out"] -  config["axis_bt"]["r_in"],
                config["axis_bt"]["h"], )])
    axis_bt.mesh_size = config["axis_bt"]["mesh_size"]
    axis_bt.params.material = config["axis_bt"]["material"]
    axis_bt.params.T_init = config["axis_bt"]["T_init"]
    # remove shapes overlap
    crucible_adapter.geo_ids = cut(crucible_adapter.dimtags, axis_bt.dimtags, remove_tool=False)
    #--------------------------------------------- Vessel --------------------------------------------- #
    vessel = Shape(model,2,"vessel",[
            occ.add_rectangle(
                0,
                - config["vessel"]["t"] - config["vessel"]["w"],
                0,
                config["vessel"]["r_in"] +  config["vessel"]["w"],
                config["vessel"]["h_in"] + 2*config["vessel"]["w"], )])
    
    vessel_hole = occ.add_rectangle(0,- config["vessel"]["t"] ,0,config["vessel"]["r_in"],config["vessel"]["h_in"])
    # keep only the boundaries
    occ.cut(vessel.dimtags, [(2, vessel_hole)])

    vessel.mesh_size = config["vessel"]["mesh_size"]
    vessel.params.material = config["vessel"]["material"]
    vessel.params.T_init = config["vessel"]["T_init"]
    #--------------------------------------------- Atmosphere --------------------------------------------- #
    atmosphere = occ.add_rectangle(
        0,
        -config["vessel"]["t"] ,
        0,
        config["vessel"]["r_in"],
        config["vessel"]["h_in"],   )

    shapes = model.get_shapes(2) # Integrate atmosphere as the rest volume all bodies
    atmosphere = Shape(model, 2, "atmosphere", [atmosphere])
    atmosphere.mesh_size = config["atmosphere"]["mesh_size"]
    atmosphere.params.material = config["atmosphere"]["material"]
    atmosphere.params.T_init = config["atmosphere"]["T_init"]
    for shape in shapes:
        atmosphere.geo_ids = cut(atmosphere.dimtags, shape.dimtags, remove_tool=False)
    #set interfaces between shapes, this removes duplicate lines and ensures a consistent mesh
    occ.fragment(
        melt.dimtags
        + crucible.dimtags
        + crystal.dimtags
        + crucible_adapter.dimtags
        + axis_bt.dimtags
        + seed.dimtags
        + axis_top.dimtags
        + ind.dimtags
        + ind_cut.dimtags
        + vessel.dimtags
        + atmosphere.dimtags,
        [], )
    model.synchronize()
    #extract phase interface
    if_melt_crystal = Shape(model, 1, "if_melt_crystal", melt.get_interface(crystal))
    # extract interfaces as 1-D shapes
    if_crucible__melt = Shape(model,1,"if_crucible__melt",crucible.get_interface(melt))
    if_crucible__crucible_adapter = Shape(model,1,"if_crucible__crucible_adapter",crucible.get_interface(crucible_adapter))
    if_crucible_adapter__axis_bt = Shape(model,1,"if_crucible_adapter__axis_bt",crucible_adapter.get_interface(axis_bt))
    if_axis_bt__vessel = Shape(model,1,"if_axis_bt__vessel",axis_bt.get_interface(vessel))
    if_crystal__seed= Shape(model,1,"if_crystal__seed",crystal.get_interface(seed))
    if_seed__axis_top= Shape(model,1,"if_seed__axis_top",seed.get_interface(axis_top))
    if_axis_top__vessel= Shape(model,1,"if_axis_top__vessel",axis_top.get_interface(vessel))
    if_inductor__inductor_inside= Shape(model,1,"if_inductor__inductor_inside",ind.get_interface(ind_cut))


    # extract boundaries for surface-to-surface radiation
    bnd_crystal = Shape(model, 1, "bnd_crystal", crystal.get_interface(atmosphere))
    bnd_melt = Shape(model, 1, "bnd_melt", melt.get_interface(atmosphere))
    bnd_crucible = Shape(model, 1, "bnd_crucible", crucible.get_interface(atmosphere))
    bnd_crucible_adapter = Shape(model, 1, "bnd_crucible_adapter", crucible_adapter.get_interface(atmosphere))
    bnd_axis_bt = Shape(model, 1, "bnd_axis_bt", axis_bt.get_interface(atmosphere))
    bnd_seed = Shape(model, 1, "bnd_seed", seed.get_interface(atmosphere))
    bnd_axis_top = Shape(model, 1, "bnd_axis_top", axis_top.get_interface(atmosphere))
    bnd_vessel = Shape(model, 1, "bnd_vessel", vessel.get_interface(atmosphere))
    bnd_ind = Shape(model, 1, "bnd_ind", ind.get_interface(atmosphere))
    bnd_outer_vessel = Shape(model,1,"bnd_outer_vessel",[vessel.bottom_boundary,vessel.top_boundary, vessel.right_boundary])
    # symmetry axis
    symmetry_axis = Shape(model, 1, "symmetry_axis", model.symmetry_axis)

    model.remove_shape(ind_cut)
    model.make_physical()
    #------------------------------------ mesh settings ------------------------------------ #
    model.deactivate_characteristic_length()
    model.set_const_mesh_sizes()

    # add linear mesh control to ensure smooth transition in mesh sizes
    max_meshsize = config["atmosphere"]["mesh_size"]
    for shape in model.get_shapes(2):
        MeshControlLinear(model, shape, shape.mesh_size, max_meshsize)
    #refine mesh close to the melt crystal interphase
    MeshControlExponential(model, if_melt_crystal, melt.mesh_size / 5, exp=1.6, fact=3)
    MeshControlExponential(model, bnd_melt, melt.mesh_size / 5, exp=1.6, fact=3)
    MeshControlExponential(model, if_crucible__melt, melt.mesh_size / 5, exp=1.6, fact=3)
    MeshControlExponential(model, bnd_ind, melt.mesh_size / 5, exp=1.6, fact=3)

    gmsh.model.setColor(melt.dimtags, 173, 216, 230)  
    gmsh.model.setColor(crystal.dimtags, 173, 216, 230) 
    gmsh.model.setColor(atmosphere.dimtags, 192,192,192)  
    gmsh.model.setColor(crucible.dimtags,0,20,50)  
    gmsh.model.setColor(vessel.dimtags, 0,0,255)
    gmsh.model.setColor(ind.dimtags, 255, 165, 0)
    gmsh.model.setColor(seed.dimtags, 165, 42, 42)
    for body in [ axis_bt,axis_top,crucible_adapter]: 
         gmsh.model.setColor(body.dimtags, 88, 57, 39)  


    model.generate_mesh(**config["mesh"])
    #------------------------------------------------------------------------ #
    if visualize:
        model.show()
    print(model)
    model.write_msh(sim_dir + "/case.msh")
    model.close_gmsh()
    return model

if __name__ == "__main__":
    sim_dir = "./"

    with open("config_geometry.yml") as f:
        config_geo = yaml.safe_load(f)
    model = geometry(config_geo, sim_dir, visualize=True)