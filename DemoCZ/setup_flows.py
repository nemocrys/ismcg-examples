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

    omega = 2 * np.pi * config["heating_induction"]["frequency"]
    # Solver Setup

    sim = elmer.load_simulation("axisymmetric_steady", elmer_config_file)
    sim.settings.update({"Angular Frequency": omega})
    solver_mgdyn = elmer.load_solver("MagnetoDynamics2DHarmonic",sim,  elmer_config_file)
    solver_mgdyn.data.update({"Angular Frequency": omega})
    solver_calcfields = elmer.load_solver("MagnetoDynamicsCalcFields",sim,  elmer_config_file)
    solver_calcfields.data.update({"Angular Frequency": omega})
    solver_heat = elmer.load_solver("HeatSolver", sim, elmer_config_file)
    solver_stress = elmer.load_solver("Elasticity", sim, elmer_config_file)

    solver_Navier_Stokes = elmer.load_solver("Navier-Stokes", sim, elmer_config_file)
    solver_Navier_StokesM = elmer.load_solver("Navier-Stokes_M", sim, elmer_config_file)
    elmer.load_solver("ResultOutputSolver", sim, elmer_config_file)

    ### EQUATIONS SETUP

    eqn_heat_EM = elmer.Equation(sim, "eqn_heat_EM", [solver_mgdyn, solver_calcfields , solver_heat ])
    eqn_heat_EM_stress = elmer.Equation(sim, "eqn_heat_EM_stress", [solver_mgdyn, solver_calcfields , solver_heat, solver_stress ])
    eqn_flow_melt = elmer.Equation(sim, "eqn_flow_melt", [solver_mgdyn, solver_calcfields , solver_heat , solver_Navier_StokesM ])
    eqn_flow_gas = elmer.Equation(sim, "eqn_flow_gas", [solver_mgdyn, solver_calcfields , solver_heat , solver_Navier_Stokes ])



    # Forces Setup

    # Induction heating 22kHz, 30Ax20windings: 600A/(0.07*0.005) = 1.7e6 
    current_source = elmer.BodyForce(sim, "Current Density")
    current_source.current_density =   config["heating_induction"]["current"] / model["EM_coil"].params.area





    joule_heat = elmer.BodyForce(sim, "joule_heat")
    joule_heat.joule_heat = True


    hotplate_force = elmer.BodyForce(sim, "Hotplate")
    hotplate_force.heat_source = 0.5614 # J/kg (set to inverse mass for easy scaling)
    hotplate_force.smart_heat_control  = True
    hotplate_force.smart_heater_control_point = [
        0.005,
        0.01,
        0.0,
    ]
    hotplate_force.smart_heater_T = 505 # tin melting point


    flows = True
    if flows:
        gas_flow = elmer.BodyForce(sim, "gas_flow")
        gas_flow.data.update({"Boussinesq" : True }) 
        gas_flow.data.update({"Pressure Single Node" : "Real 0.0"  }) 

        melt_flow = elmer.BodyForce(sim, "melt_flow")
        melt_flow.data.update({"Boussinesq" : True }) 
        melt_flow.data.update({"Pressure Single Node" : "Real 0.0" }) 




    # Induction heating
    induction = elmer.Body(sim,'EM_coil', [model["EM_coil"].ph_id])
    material_name = model['EM_coil'].params.material
    mat = elmer.Material(sim, material_name, config_mat[material_name])
    ic = elmer.InitialCondition(sim, "T_" + 'EM_coil', {"Temperature": model['EM_coil'].params.T_init})

    induction.equation = eqn_heat_EM
    induction.material = mat
    induction.body_force = current_source
    induction.initial_condition = ic


    # Add crystal
    crystal = elmer.Body(sim,'crystal', [model["crystal"].ph_id])
    material_name = model["crystal"].params.material
    mat = elmer.Material(sim, material_name, config_mat[material_name])
    melting_point = mat.data["Melting Point"] # set to 505 °C
    ic = elmer.InitialCondition(sim, "T_crystal", {"Temperature": model["crystal"].params.T_init})

    crystal.equation = eqn_heat_EM_stress
    crystal.material = mat
    crystal.initial_condition = ic
    crystal.body_force = joule_heat



    # Add melt
    melt = elmer.Body(sim, "melt", [model["melt"].ph_id])
    material_name = model["melt"].params.material
    mat = elmer.Material(sim, material_name, config_mat[material_name])
    ic = elmer.InitialCondition(sim, "T_melt", {"Temperature": model["melt"].params.T_init})
    if flows:
        ic.data.update({"VelocityM 1" : "Real 1.0e-9"}) 
        ic.data.update({"VelocityM 2" : "Real 0.0"}) 

    melt.equation = eqn_flow_melt
    melt.material = mat
    melt.initial_condition = ic
    melt.body_force = melt_flow


    # Add Atmosphere
    atmosphere = elmer.Body(sim, "atmosphere", [model["atmosphere"].ph_id])
    material_name = model["atmosphere"].params.material
    mat = elmer.Material(sim, material_name, config_mat[material_name])
    ic = elmer.InitialCondition(sim, "T_atmosphere", {"Temperature": model["atmosphere"].params.T_init})
    if flows:
        ic.data.update({"Velocity 1" : 1.0e-9}) 
        ic.data.update({"Velocity 2" :  0.0}) 

    atmosphere.equation = eqn_flow_gas
    atmosphere.material = mat
    atmosphere.initial_condition = ic
    atmosphere.body_force = gas_flow




    # add other bodies

    for shape in [
        "crucible",
        "hotplate",
    ]:
        bdy = elmer.Body(sim, shape, [model[shape].ph_id])
        material_name = model[shape].params.material
        mat = elmer.Material(sim, material_name, config_mat[material_name])
        ic = elmer.InitialCondition(sim, "T_" + shape, {"Temperature": model[shape].params.T_init})

        bdy.equation = eqn_heat_EM
        bdy.material = mat    
        bdy.body_force = joule_heat
        if shape == "hotplate":
            bdy.body_force = hotplate_force
        bdy.initial_condition = ic


    if_melt_crystal = elmer.Boundary(sim,"if_melt_crystal",[model["if_melt_crystal"].ph_id])
    if_melt_crystal.fixed_heatflux = 21289
    if_melt_crystal.save_line = True
    if_melt_crystal.data.update({"VelocityM 1" :"Real 0.0" }) 
    if_melt_crystal.data.update({"VelocityM 2" :"Real 0.0" }) 


    # boundaries with convection 


    bnd = elmer.Boundary(sim, "bnd_melt", [model["bnd_melt"].ph_id])
    bnd.radiation_idealized =True
    bnd.data.update({"Radiation External Temperature" : config["T_ambient"]})
    bnd.heat_transfer_coefficient = config["boundaries"]["bnd_melt"]["htc"]
    bnd.T_ext = config["boundaries"]["bnd_melt"]["T_ext"]
    bnd.data.update({"Velocity 1" : 0.0}) 
    bnd.data.update({"Velocity 2" : 0.0}) 
    bnd.data.update({"VelocityM 1" : "Real 0.0" }) 
    bnd.data.update({"VelocityM 2" : "Real 0.0" }) 

    for bnds in [
        "bnd_crystal_side",
        "bnd_crucible",
        "bnd_hotplate",
    ]:
       bnd = elmer.Boundary(sim, bnds, [model[bnds].ph_id])
       bnd.radiation_idealized =True
       bnd.data.update({"Radiation External Temperature" : config["T_ambient"]})
       bnd.heat_transfer_coefficient = config["boundaries"][bnds]["htc"]
       bnd.T_ext = config["boundaries"][bnds]["T_ext"]




    bnd = elmer.Boundary(sim, "bnd_crystal_top", [model["bnd_crystal_top"].ph_id])
    bnd.radiation_idealized =True    
    bnd.data.update({"Radiation External Temperature" : config["T_ambient"]}) 
    #bnd.data.update({"Displacement 2":0.0})  # BC for stress solver
    bnd.T_ext = config["T_ambient"]



    bnd = elmer.Boundary(sim, "bnd_EM_coil", [model["bnd_EM_coil"].ph_id])
    bnd.radiation_idealized =True    
    bnd.data.update({"Radiation External Temperature" : config["T_ambient"]})

    # stationary interfaces
    for bnd in [
        "if_crucible_melt",
        "if_crucible_hotplate",
    ]:
        bnd = elmer.Boundary(sim, bnd, [model[bnd].ph_id])
        
    # add outside boundaries
    
    bnd = elmer.Boundary(sim, "bnd_outer", [model["bnd_outer"].ph_id])
    bnd.fixed_temperature = config["boundaries"]["bnd_outer"]["T"]
    bnd.zero_potential = True  # Potential Re=0 & Potential Im = 0


    sim.write_sif(sim_dir)


if __name__ == "__main__":
    sim_dir = "./simdata/case2_flows_2nd_order"
    #if os.path.exists(sim_dir):
    #    raise ValueError("Please remove the old simulation directory.")

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
