## Model description


In [Demo-CZ](https://github.com/nemocrys/ismcg-examples/tree/main/DemoCZ), three cases are included:
- **Case 1**:
  - Thermal simulation without magnet (blue part), include only HeatSolver
- **Case 2**:
  - Thermal calculation
  - velocity calculation for melt and gas
  - Thermal stress in the crystal
- **Case 3**:
  - Thermal calculation with applied HTCs (heat transfer coefficients)




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


Run [ geometry.py](https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/geometry.py) to generate the simulation mesh.

Run [  simulation_setup.py](https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/setup.py) to generate the mesh (using geometry.py), the [sif](https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/simdata/01/case.sif) with pyelmer, run ElmerGrid and ElmerSolver.

## Geometry

- Liquid and solid tin(crystal) : Light Blue
- Crucible : Black
- Hotplate : Red
- Magnet : Blue
- Air : Silver


<img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/whole_mesh.png" width="45%" /> <img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/mesh.png" width="45%" />




---
### Case 1 ***Work in progress***

Global (Left) and melt(right) temperature field is calculated with HeatSolve module. The required power is adjusted automatically to reach the melting point of tin (i.e 505 K) at the crystal-melt interphase

<img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/case1_T_distribution.png" width="45%" /><img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/case1_melt.png" width="45%" />

---


### Case 2 ***Work in progress***

## Melt, Gas flows ***Work in progress***

## Thermal Stress ***Work in progress***

### Case 3 ***Work in progress***

## Temperature field at crystal,melt ***Work in progress***