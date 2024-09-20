## Model description

The main features of [Test-CZ](https://github.com/nemocrys/ismcg-examples/tree/main/TestCZ) model are:
- Heat transfer through conduction and radiation
- Induction heating of the crucible
- Phase change: the interface between crystal and melt is shifted into the isothermal of the melting point

In both cases, the total heat energy transfer across simulation bodies is evaluated. Through the *save_scalars* , it is possible to estimate integral heat fluxes (W) over surface boundary lines, defined in the  [ geometry.py](https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/geometry.py) file. The accuracy depends on mesh resolution near boundaries, hence, it is highly recommended to use 2nd order mesh elements for such calculations. This is a common computation not only to track the heat transfer within the volume but also to validate the energy balance.

## Simulation  Configuration

- [config_geometry.yml](https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/config_geometry.yml) contains the geometry parameters for the simulation mesh.
- [config_mat.yml](https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/config_mat.yml) describe the material properties (all in SI units).
- [ config_elmer.yml](https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/config_elmer.yml) enclose the employed Elmer solvers from [ ElmerManual](https://www.nic.funet.fi/pub/sci/physics/elmer/doc/ElmerSolverManual.pdf).
- [ config_sim.yml](https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/config_sim.yml) refers to pecific parameters for this simulation, e.g. induction heater properties.

The configuration of the simulation is stored in yml-files. The parameters of e.g. a material are stored in this format :
```python
tin-solid:
  Density: 7179.0
  Electric Conductivity: 4.38e+6
  Emissivity: 0.064
  Heat Capacity: 244.0
  Heat Conductivity: 60.0
  Relative Permeability: 1
  Relative Permittivity: 1
  Solid: 'Logical True'
  Melting Point: 505
  Latent Heat: 5.96e+4 
```

### Execute Simulation

Run [ geometry.py](https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/geometry.py) to generate the simulation mesh using ```python3 geometry.py```

Run [  simulation_setup.py](https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/setup.py) using ```python3 simulation_setup.py``` to generate the mesh (using geometry.py) and the [sif](https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/simdata/01/case.sif) with pyelmer, and then execute ElmerGrid and ElmerSolver.


## Geometry

- Liquid and solid tin(crystal) : Light Blue
- Crucible : Black
- Crucible adapter and bottom,top axis : Brown
- Vessel: Blue
- Air : Silver
- Inductor : Orange

2D steady-state electromagnetism and heat transfer simulation of the NEMOCRYS Test-CZ Furnace:

<img src="https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/pics/mesh.png"><img src="https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/pics/mesh_zoom.png">




## Temperature field

Global temperature field is calculated with *HeatSolve* module. The Smart Heater Control was applied for scaling of this heat source term so that the desired temperature level, usually the melting temperature of Tin (i.e 505 K) at the crystal-melt interphase.

### Global temperature distribution
<img src="https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/pics/T_distrib.png">

---
### Temperature distribution at crystal- melt

<img src="https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/pics/melt-crucible.png"><img src="https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/pics/melt.png">
