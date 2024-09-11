import os
import numpy as np
from pyelmer import elmerkw as elmer
from pyelmer.execute import run_elmer_solver, run_elmer_grid
from pyelmer.post import scan_logfile
import yaml

from geometry import geometry

def simulation_pyelmer(
    model, config, sim_dir="./simdata", config_mat={}, elmer_config_file="config_elmer.yml"
):
    ### SOLVERS SETUP
    sim = elmer.load_simulation("axisymmetric_steady", elmer_config_file)
    omega = 2 * np.pi * config["heating_induction"]["frequency"]
    sim.settings.update({"Angular Frequency": omega})

    solver_mgdyn = elmer.load_solver("MagnetoDynamics2DHarmonic",sim,  elmer_config_file)
    solver_mgdyn.data.update({"Angular Frequency": omega})
    solver_calcfields = elmer.load_solver("MagnetoDynamicsCalcFields",sim,  elmer_config_file)
    solver_calcfields.data.update({"Angular Frequency": omega})
    solver_heat = elmer.load_solver("HeatSolver", sim, elmer_config_file)
    solver_phase_change = elmer.load_solver("SteadyPhaseChange", sim, elmer_config_file)
    solver_phase_change.data["Triple Point Fixed"] = "Logical True"   
    solver_mesh = elmer.load_solver("MeshUpdate", sim, elmer_config_file)
    
    elmer.load_solver("ResultOutputSolver", sim, elmer_config_file)
    elmer.load_solver("SaveLine", sim, elmer_config_file)

    ### EQUATIONS SETUP
    eqn_main = elmer.Equation(sim, "eqn_main", [solver_mgdyn, solver_calcfields , solver_heat , solver_mesh ])
    eqn_phase_change = elmer.Equation(sim, "eqn_phase_change", [solver_phase_change])       

    # forces
    current_source = elmer.BodyForce(sim, "Current Density")

    joule_heat = elmer.BodyForce(sim, "joule_heat")
    joule_heat.joule_heat = True
    if config["general"]["heat_control"] :
        joule_heat.smart_heat_control = True
        if config["smart-heater"]["control-point"]:
            joule_heat.smart_heater_control_point = [
                config["smart_heater"]["x"],
                config["smart_heater"]["y"],
                config["smart_heater"]["z"],
            ]
            joule_heat.smart_heater_T = config["smart_heater"]["T"]

    # Induction heating
    current_source.current_density = config["heating_induction"]["current"] / model['inductor'].params.area

    induction = elmer.Body(sim,'inductor', [model["inductor"].ph_id])
    material_name = model['inductor'].params.material
    mat = elmer.Material(sim, material_name, config_mat[material_name])
    ic = elmer.InitialCondition(sim, "T_inductor", {"Temperature": model['inductor'].params.T_init})
    induction.equation = eqn_main
    induction.material = mat
    induction.body_force = current_source
    induction.initial_condition = ic

    # add crystal
    crystal = elmer.Body(sim,'crystal', [model["crystal"].ph_id])
    material_name = model["crystal"].params.material
    mat = elmer.Material(sim, material_name, config_mat[material_name])
    melting_point = mat.data["Melting Point"] # set to 505 °C
    ic = elmer.InitialCondition(sim, "T_crystal", {"Temperature": model["crystal"].params.T_init})
    crystal.equation = eqn_main
    crystal.material = mat
    crystal.initial_condition = ic
    crystal.body_force = joule_heat

    # add melt
    melt = elmer.Body(sim, "melt", [model["melt"].ph_id])
    material_name = model["melt"].params.material
    mat = elmer.Material(sim, material_name, config_mat[material_name])
    ic = elmer.InitialCondition(sim, "T_melt", {"Temperature": model["melt"].params.T_init})
    melt.equation = eqn_main
    melt.material = mat
    melt.initial_condition = ic
    melt.body_force = joule_heat

    # add other bodies
    for shape in [
        "crucible",
        "seed",
        "axis_top",
        "crucible_adapter",
        "axis_bt",
        "vessel",
        "atmosphere",
    ]:
        bdy = elmer.Body(sim, shape, [model[shape].ph_id])
        material_name = model[shape].params.material
        mat = elmer.Material(sim, material_name, config_mat[material_name])
        ic = elmer.InitialCondition(sim, "T_" + shape, {"Temperature": model[shape].params.T_init})

        bdy.equation = eqn_main
        bdy.material = mat    
        bdy.body_force = joule_heat
        bdy.initial_condition = ic

    #setup phase change, 1-D body where the smart heater applies
    melt_crystal_if = elmer.Body(sim, "melt_crystal_if", [model["if_melt_crystal"].ph_id])
    melt_crystal_if.equation = eqn_phase_change
    melt_crystal_if.material = crystal.material
    t0_phase_change = elmer.InitialCondition( sim, "t0_phase_change", {"Temperature": melting_point} )
    melt_crystal_if.initial_condition = t0_phase_change

    if_melt_crystal = elmer.Boundary(sim,"if_melt_crystal",[model["if_melt_crystal"].ph_id])
    if_melt_crystal.save_line = True
    if_melt_crystal.normal_target_body = crystal
    if_melt_crystal.smart_heater = True
    if_melt_crystal.smart_heater_T = config["smart-heater"]["T"]
    if_melt_crystal.phase_change_steady = True
    if_melt_crystal.phase_change_body = melt_crystal_if
    if_melt_crystal.material = crystal.material
    if_melt_crystal.save_scalars = True

    # boundaries with convection 
    for bnd in [
        "bnd_melt",
        "bnd_crystal",
    ]:
        bnd = elmer.Boundary(sim, bnd, [model[bnd].ph_id])
        bnd.radiation = True
        bnd.mesh_update = [0, 0]
        bnd.T_ext = config["boundaries"]["melt"]["T_ext"]
        bnd.heat_transfer_coefficient = 1.0 # or denifed in the config file

    # add boundaries with surface-to-surface radiation
    for bnd in [
        "bnd_crucible",
        "bnd_crucible_adapter" , 
        "bnd_axis_bt", 
        "bnd_seed",
        "bnd_axis_top",
        "bnd_vessel",
        "bnd_ind",
    ]:
        bnd = elmer.Boundary(sim, bnd, [model[bnd].ph_id])
        bnd.radiation = True
        bnd.mesh_update = [0, 0]        
        bnd.save_scalars = True

    # stationary interfaces
    for bnd in [
        "if_crucible__melt",
        "if_crucible__crucible_adapter",
        "if_crucible_adapter__axis_bt",
        "if_axis_bt__vessel",
        "if_crystal__seed",
        "if_seed__axis_top",
        "if_axis_top__vessel",
    ]:
        bnd = elmer.Boundary(sim, bnd, [model[bnd].ph_id])
        bnd.mesh_update = [0, 0]

    # add outside boundaries
    bnd = elmer.Boundary(sim, "if_inductor__inductor_inside", [model["if_inductor__inductor_inside"].ph_id])
    bnd.fixed_temperature = config["boundaries"]["inductor_inside"]["T"] # water cooled coil
    bnd.mesh_update = [0, 0]

    bnd = elmer.Boundary(sim, "bnd_outer_vessel", [model["bnd_outer_vessel"].ph_id])
    bnd.fixed_temperature = config["boundaries"]["container_outside"]["T"]
    bnd.zero_potential = True
    bnd.mesh_update = [0, 0]

        # symmetry axis
    bnd = elmer.Boundary(sim, "symmetry_axis", [model["symmetry_axis"].ph_id])
    bnd.mesh_update = [0, None]

    sim.write_sif(sim_dir)

if __name__ == "__main__":
    sim_dir = "./simdata/01"
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