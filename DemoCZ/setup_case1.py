import os
import numpy as np
from pyelmer import elmerkw as elmer
from pyelmer.execute import run_elmer_solver, run_elmer_grid
from pyelmer.post import scan_logfile
import yaml

from geometry import geometry


def simulation_pyelmer(model, config, sim_dir="./simdata", config_mat={}, elmer_config_file="config_elmer.yml"):


    ###--- In the first part, we load the solvers from the elmer.yml file and then combine them to form different equations, which will subsequently be applied to simulation bodies. ---###

    # SOLVER SETUP
    sim = elmer.load_simulation("axisymmetric_steady", elmer_config_file)
    solver_heat = elmer.load_solver("HeatSolver", sim, elmer_config_file)
    elmer.load_solver("ResultOutputSolver", sim, elmer_config_file)
    elmer.load_solver("save_scalars", sim, elmer_config_file)


    # EQUATION SETUP
    eqn_heat = elmer.Equation(sim, "eqn_heat", [solver_heat ])  


    # FORCE SETUP
    hotplate_force = elmer.BodyForce(sim, "Hotplate")
    hotplate_force.heat_source = 0.5614 # J/kg 
    hotplate_force.smart_heat_control  = True #The Smart Heater Control was applied for scaling of this heat source term so that the desired temperature level (i.e 505K at coordinate[0.005,0.01,0]) 
    hotplate_force.smart_heater_control_point = [
        0.005,
        0.01,
        0.0]
    hotplate_force.smart_heater_T = 505 # tin melting point


    ###--- At the next section we assign : initial conditions, material, equations, forces to every body of the domain ---###


    # Add crystal
    crystal = elmer.Body(sim,'crystal', [model["crystal"].ph_id])
    material_name = model["crystal"].params.material
    mat = elmer.Material(sim, material_name, config_mat[material_name])
    ic = elmer.InitialCondition(sim, "T_crystal", {"Temperature": model["crystal"].params.T_init})
    crystal.equation = eqn_heat
    crystal.material = mat
    crystal.initial_condition = ic

    # Add melt
    melt = elmer.Body(sim, "melt", [model["melt"].ph_id])
    material_name = model["melt"].params.material
    mat = elmer.Material(sim, material_name, config_mat[material_name])
    ic = elmer.InitialCondition(sim, "T_melt", {"Temperature": model["melt"].params.T_init})
    melt.equation = eqn_heat 
    melt.material = mat
    melt.initial_condition = ic

    # Add other bodies
    for shape in [
        "crucible",
        "hotplate",
        "atmosphere",
    ]:
        bdy = elmer.Body(sim, shape, [model[shape].ph_id])
        material_name = model[shape].params.material
        mat = elmer.Material(sim, material_name, config_mat[material_name])
        ic = elmer.InitialCondition(sim, "T_" + shape, {"Temperature": model[shape].params.T_init})
        bdy.equation = eqn_heat
        bdy.material = mat    
        bdy.initial_condition = ic
        if shape == "hotplate":  # hotplace is the heat source
            bdy.body_force = hotplate_force
        

    ###--- In the final section, Boundary Conditions are defined. Each Boundary must contain variable information essential for the equations-solvers that we are solving within the simulation domain.---###

    # Boundaries

    if_melt_crystal = elmer.Boundary(sim,"if_melt_crystal",[model["if_melt_crystal"].ph_id])
    if_melt_crystal.fixed_heatflux = 21289
    if_melt_crystal.save_line = True
    if_melt_crystal.save_scalars = True

    # Melt-Surface Boundary Condition
    bnd = elmer.Boundary(sim, "bnd_melt", [model["bnd_melt"].ph_id])
    bnd.radiation_idealized =True
    bnd.data.update({"Radiation External Temperature" : config["T_ambient"]})
    bnd.save_scalars = True

    for bnds in [
        "bnd_crystal_side",
        "bnd_crucible",
        "bnd_hotplate",
    ]:
       bnd = elmer.Boundary(sim, bnds, [model[bnds].ph_id])
       bnd.radiation_idealized =True
       bnd.data.update({"Radiation External Temperature" : config["T_ambient"]})
       bnd.save_scalars = True

    # Crystal top Boundary Condition
    bnd = elmer.Boundary(sim, "bnd_crystal_top", [model["bnd_crystal_top"].ph_id])
    bnd.radiation_idealized =True    
    bnd.data.update({"Radiation External Temperature" : config["T_ambient"]}) 
    bnd.save_scalars = True


    # Stationary interfaces
    for bnd in [
        "if_crucible_melt",
        "if_crucible_hotplate",
    ]:
        bnd = elmer.Boundary(sim, bnd, [model[bnd].ph_id])
        bnd.save_scalars = True        

    # Boundary conditions at the outer part of the simulation domain
    bnd = elmer.Boundary(sim, "bnd_outer", [model["bnd_outer"].ph_id])
    bnd.fixed_temperature = config["boundaries"]["bnd_outer"]["T"]
    bnd.save_scalars = True

    sim.write_sif(sim_dir)



###--- The part below is responsible to execute the simulation run and always remain the same ---###

if __name__ == "__main__":
    sim_dir = "./simdata/Case1"
    if os.path.exists(sim_dir):
        raise ValueError("Please remove the old simulation directory.")

    with open("config_geometry.yml") as f:
        config_geo = yaml.safe_load(f)
    model = geometry(config_geo, sim_dir)

    with open("config_sim.yml") as f:
        config_sim = yaml.safe_load(f)
    with open("config_mat.yml") as f:
        config_mat = yaml.safe_load(f)

    simulation_pyelmer(model, config_sim, sim_dir, config_mat)
    run_elmer_grid(sim_dir, "case.msh")
    run_elmer_solver(sim_dir)
    err, warn, stats = scan_logfile(sim_dir)
    print("Errors:", err)
    print("Warnings:", warn)
    print("Statistics:", stats)