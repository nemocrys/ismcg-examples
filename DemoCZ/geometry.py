import os
import numpy as np
from objectgmsh import Model, Shape, MeshControlLinear, MeshControlExponential, cut
import gmsh
import yaml
import matplotlib.pyplot as plt


occ = gmsh.model.occ
def geometry(config, sim_dir="./", name="vgf", visualize=False):
    if not os.path.exists(sim_dir):
        os.makedirs(sim_dir)

    model = Model(name)
    #--------------------------------------------- MELT --------------------------------------------- #
    # 2) Vessel ?
    # 3) material update? iron coil?
    # 4) no solver phase change, should we include it ?
    # 5) discuss body forces
    melt = Shape(model,2,"melt",[
            occ.add_rectangle(
                0,
                0,
                0,
                config["melt"]["r"],
                config["melt"]["h"],    )])
    # we use "params" to save various values we need later
    melt.mesh_size = config["melt"]["mesh_size"]
    melt.params.material = config["melt"]["material"]
    melt.params.T_init = config["melt"]["T_init"]

    #--------------------------------------------- Crucible --------------------------------------------- #
    crucible = Shape(model,2,"crucible",[
            occ.add_rectangle(
                0,
                - (config["crucible"]["h"]- config["crucible"]["hi"]) ,
                0,
                config["crucible"]["r"],
                config["crucible"]["h"],    )])
    crucible.mesh_size = config["crucible"]["mesh_size"]
    crucible.params.material = config["crucible"]["material"]
    crucible.params.T_init = config["crucible"]["T_init"]

    crucible_hole = occ.add_rectangle(
        0,
        0,
        0,
        config["melt"]["r"],
        config["crucible"]["hi"],
    )
    occ.cut(crucible.dimtags, [(2, crucible_hole)])

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

    #--------------------------------------------- Hotplate --------------------------------------------- #
    hotplate = Shape(model,2,"hotplate",
        [
            occ.add_rectangle(
                0,
                - (config["crucible"]["h"]- config["crucible"]["hi"]) -config["hotplate"]["h"],
                0,
                config["hotplate"]["r"],
                config["hotplate"]["h"],    )])
    hotplate.mesh_size = config["hotplate"]["mesh_size"]
    hotplate.params.material = config["hotplate"]["material"]
    hotplate.params.T_init = config["hotplate"]["T_init"] 

    #--------------------------------------------- EM Coil --------------------------------------------- #
    EM_coil = Shape(model,2,"EM_coil",
        [
            occ.add_rectangle(
                config["EM_coil"]["r_in"],
                -config["EM_coil"]["t"],
                0,
                config["EM_coil"]["r_out"],
                config["EM_coil"]["h"], )])
    EM_coil.mesh_size = config["EM_coil"]["mesh_size"]
    EM_coil.params.material = config["EM_coil"]["material"]
    EM_coil.params.T_init = config["EM_coil"]["T_init"] 
    EM_coil.params.area = config["EM_coil"]["r_out"] * config["EM_coil"]["h"] 

    #--------------------------------------------- Atmosphere --------------------------------------------- #
    atmosphere = occ.add_rectangle(
        0,
        -config["atmosphere"]["t"] ,
        0,
        config["atmosphere"]["r"] ,
        config["atmosphere"]["h"],
    )

    shapes = model.get_shapes(2)

    atmosphere = Shape(model, 2, "atmosphere", [atmosphere])
    atmosphere.mesh_size = config["atmosphere"]["mesh_size"]
    atmosphere.params.material = config["atmosphere"]["material"]
    atmosphere.params.T_init = config["atmosphere"]["T_init"]
    for shape in shapes:
        atmosphere.geo_ids = cut(atmosphere.dimtags, shape.dimtags, remove_tool=False)

    # set interfaces between shapes, this removes duplicate lines and ensures a consistent mesh
    occ.fragment(
        melt.dimtags
        + crucible.dimtags
        + crystal.dimtags
        + hotplate.dimtags
        + EM_coil.dimtags
        + atmosphere.dimtags,
        [],
    )
    model.synchronize()

    # extract phase interface
    if_melt_crystal = Shape(model, 1, "if_melt_crystal", melt.get_interface(crystal))

    # extract interfaces (not all are required but gives much better visualization in ParaView
    if_crucible_melt = Shape(model,1,"if_crucible_melt",crucible.get_interface(melt))
    if_crucible_hotplate = Shape(model,1,"if_crucible_hotplate",crucible.get_interface(hotplate))

    # extract boundaries for surface-to-surface radiation
    bnd_crystal_side = Shape(model, 1, "bnd_crystal_side", crystal.get_interface(atmosphere))
    bnd_crystal_top = Shape(model,1,"bnd_crystal_top",
        crystal.get_boundaries_in_box(
            [0, config["crystal"]["r"]],
            [
                config["melt"]["h"] + config["crystal"]["h"] , config["melt"]["h"] + config["crystal"]["h"] ]))
    
    bnd_crystal_side -= bnd_crystal_top

    bnd_melt = Shape(model, 1, "bnd_melt", melt.get_interface(atmosphere))
    bnd_crucible = Shape(model, 1, "bnd_crucible", crucible.get_interface(atmosphere))
    bnd_hotplate = Shape(model, 1, "bnd_hotplate", hotplate.get_interface(atmosphere))
    bnd_EM_coil = Shape(model, 1, "bnd_EM_coil", EM_coil.get_interface(atmosphere))
    bnd_outer = Shape(model,1,"bnd_outer",[atmosphere.bottom_boundary,atmosphere.top_boundary, atmosphere.right_boundary])

    # symmetry axis
    symmetry_axis = Shape(model, 1, "symmetry_axis", model.symmetry_axis)

    model.make_physical()
    #------------------------------------ mesh settings ------------------------------------ #
    model.deactivate_characteristic_length()
    model.set_const_mesh_sizes()

    # add linear mesh control to ensure smooth transition in mesh sizes
    max_meshsize = config["atmosphere"]["mesh_size"]
    for shape in model.get_shapes(2):
        MeshControlLinear(model, shape, shape.mesh_size, max_meshsize)
     # Refine mesh close to the melt crystal interphase
    MeshControlExponential(model, if_melt_crystal, melt.mesh_size / 5, exp=1.6, fact=3)
    MeshControlExponential(model, bnd_melt, melt.mesh_size / 5, exp=1.6, fact=3)
    MeshControlExponential(model, if_crucible_melt, melt.mesh_size / 5, exp=1.6, fact=3)

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