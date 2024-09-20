## Model description

In [Demo-CZ](https://github.com/nemocrys/ismcg-examples/tree/main/DemoCZ), two cases are included:
- **Case 1**:
  - Thermal simulation, employing *HeatSolver*
- **Case 2**:
  - Thermal calculation with applied HTCs (heat transfer coefficients)
  - Thermal stress calculation *StressSolver*

In both cases, the total heat energy transfer across simulation bodies is evaluated. Through the *save_scalars* , it is possible to estimate integral heat fluxes (W) over surface boundary lines, defined in the  [ geometry.py](https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/geometry.py) file. The accuracy depends on mesh resolution near boundaries, hence, it is highly recommended to use 2nd order mesh elements for such calculations. This is a common computation not only to track the heat transfer within the volume but also to validate the energy balance.
## Simulation  Configuration

- [config_geometry.yml](https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/config_geometry.yml) contains the geometry parameters for the simulation mesh.
- [config_mat.yml](https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/config_mat.yml) describe the material properties (all in SI units).
- [ config_elmer.yml](https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/config_elmer.yml) enclose the employed Elmer solvers from [ ElmerManual](https://www.nic.funet.fi/pub/sci/physics/elmer/doc/ElmerSolverManual.pdf).
- [ config_sim.yml](https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/config_sim.yml) refers to pecific parameters for this simulation, e.g. induction heater properties.

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

Run [ geometry.py](https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/geometry.py) to generate the simulation mesh using ```python3 geometry.py```

Run [  simulation_setup.py](https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/setup.py) using ```python3 setup.py``` to generate the mesh (using geometry.py) and the [sif](https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/simdata/01/case.sif) with pyelmer, and then execute ElmerGrid and ElmerSolver.

## Geometry

- Liquid and solid tin(crystal) : Light Blue
- Crucible : Black
- Hotplate : Red
- Magnet : Blue
- Air : Silver


<img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/whole_mesh.png" width="45%" /> <img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/mesh.png" width="45%" />




---
### Case 1 

Global (Left) and melt (right) temperature field is calculated with HeatSolve module. The Smart Heater Control was applied for scaling of this heat source term so that the desired temperature level, usually the melting temperature of Tin (i.e 505 K) at the crystal-melt interphase.


<img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/case1_T_distribution.png" width="32%" height=500/><img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/Case1_bodies_T.png" width="32%" height=500/><img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/case1_melt.png" width="32%" height=300/>

---





### Case 2

In this case the HTCs (heat transfer coefficients) for each boundary are regulated from the [ config_sim.yml](https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/config_sim.yml) file .

### HTCs
```python
boundaries:
  bnd_melt:
    htc: 3.0 
    T_ext: 293.15
  bnd_crystal_side:
    htc: 6.0  
    T_ext: 293.15
  bnd_crucible:
    htc: 6.0 
    T_ext: 293.15
  bnd_hotplate:
    htc: 6.0 
    T_ext: 293.15
```

### Temperature field at crystal-melt 

The temperature field for the whole domain and the melt, when convection is accounted

<img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/Case2_T_distributionpng" width="45%" /><img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/Case2_T_melt.png" width="45%" />


## Thermal Stress 

Thermal stress in the crystal is calculated with the StressSolve module assuming isotropic elastic properties (see [config_mat.yml](https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/config_mat.yml) ).
<img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/Case2_vonmises.png" width="32%" /><img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/Case2_stress_yy.png" width="32%" />
