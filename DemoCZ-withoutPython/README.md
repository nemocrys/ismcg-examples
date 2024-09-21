# sim-demo-cz

This case demonstrates the use of Gmsh with a GEO script and Elmer with a SIF script, i.e. without the Python interface

A detailed description of the physical and numerical model has been published here:
K. Dadzis, Czochralski growth of tin crystals as a multi-physical model experiment. [Preprint on arXiv](http://arxiv.org/abs/2305.06875)

## Geometry
Geometry is defined using a GEO script in Gmsh. It consists of the following parts/materials:

- Liquid tin melt (yellow)
- Solid tin crystal (grey)
- Crucible of aluminum (dark grey)
- Heating plate of cast iron (red)
- Induction coil (blue)
- Air (light blue)

<img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ-withoutPython/pics/pic_mesh_all.png" height="450"><img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ-withoutPython/pics/pic_mesh.png" height="400">

## Heat flow
Global temperature field is calculated with *HeatSolve* module. Automatic power adjustment is applied to reach the melting point. Fixed shape and position of crystallization interface with prescribed latent heat release is considered.

<img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ-withoutPython/pics/pic_temp.png" height="450"><img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ-withoutPython/pics/pic_temp_zoom.png" height="450">

## Electromagnetism
Heat induction and Lorentz forces are calculated with *MagnetoDynamics2D* module. A hypothetical case is considered: graphite crucible on an inductive cooking plate (coil with 600A current and 22 kHz frequency). Currently this calculation is **not** coupled to the other physical models.

<img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ-withoutPython/pics/pic_heating.png" height="200"><img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ-withoutPython/pics/pic_force.png" height="200">

## Flows
Flows in melt and gas phases are calculated with *FlowSolve* module. Only buoyancy forces with Boussinesq approximation are considered. Gas flow effect on solid temperature is included.

<img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ-withoutPython/pics/pic_flows.png" height="400">

## Thermal stresses
Thermal stress in the crystal is calculated with the *StressSolve* module assuming isotropic elastic properties. 

<img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ-withoutPython/pics/pic_stress.png" height="400">
