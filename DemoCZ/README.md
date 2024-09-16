***WARNING: Work in progress!***

## Model description

In [Demo-CZ](https://github.com/nemocrys/ismcg-examples/tree/main/DemoCZ), three cases are included:
- **Case 1**:
  - Thermal simulation without magnet (blue part), include only HeatSolver
- **Case 2**:
  - Thermal and Electromagnetic calculation   
  - velocity calculation for melt and gas
  - Thermal stress in the crystal
- **Case 3**:
  - Thermal calculation with applied HTCs (heat transfer coefficients)
  - Electromagnetic calculation 

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

Run [  simulation_setup.py](https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/setup.py) using ```python3 simulation_setup.py``` to generate the mesh (using geometry.py) and the [sif](https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/simdata/01/case.sif) with pyelmer, and then execute ElmerGrid and ElmerSolver.

## Geometry

- Liquid and solid tin(crystal) : Light Blue
- Crucible : Black
- Hotplate : Red
- Magnet : Blue
- Air : Silver


<img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/whole_mesh.png" width="45%" /> <img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/mesh.png" width="45%" />




---
### Case 1 

Global (Left) and melt(right) temperature field is calculated with HeatSolve module. The required power is adjusted automatically to reach the melting point of tin (i.e 505 K) at the crystal-melt interphase

<img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/case1_T_distribution.png" width="32%" height=500/><img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/Case1_bodies_T.png" width="32%" height=500/><img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/case1_melt.png" width="32%" height=300/>

---


### Case 2 

In this case is solved the Navier-Stokes equation for gas and melt and also estimated the thermal stress in the crystal.

For this purpose the [config_mat.yml](https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/config_mat.yml) file enriched with the nessesary material properties for each solver such as  Youngs Modulus, Poisson Ratio (Stress) and viscosity (Navier-Stokes). 
Moreover the boundary conditions enriched accordingly for the new solvers, as it can be seen in the  [setup.py](https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/flows.py).

Finally, the stress calculation require second order elements which can be easily defined in [config_geometry.yml](https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/config_geometry.yml) 

```python
mesh:
  size_factor: 1  
  order: 2  
```

## Electromagnetism

Heat induction and Lorentz forces are calculated with MgDyn2DHarmonic module. The current cases acconted for an inductive cooking plate (coil with 600A current and 22 kHz frequency)


<img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/Case2_joule_heating.png " width="45%" height=300 /><img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/Case2_lorentz.png" width="45%" height=300 />

## Melt, Gas flows 

Flows in melt and gas phases are calculated with FlowSolve module. Only buoyancy forces with Boussinesq approximation are considered.

The pictures from left to right illustrate: the global temperature field, the atmospheric temperature and the vector gas velocity, the melt melt temperature field with the velocity vectors.

<img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/case2_T.png" width="32%" /><img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/case2_gas_velocity.png" width="32%"/><img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/Case2_melt_velocity.png" width="32%"/>


## Thermal Stress 

Thermal stress in the crystal is calculated with the StressSolve module assuming isotropic elastic properties (see [config_mat.yml](https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/config_mat.yml) ).

<img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/Case2_crystal_stress.png" width="32%" /><img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/Case2_crystal_stress_yy.png" width="32%" />

### Case 3 

In this case the HTCs (heat transfer coefficients) for each boundary and the inductor properties (blue part)  are regulated from the [ config_sim.yml](https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/config_sim.yml) file .

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
### Inductor (SI units)
```python
heating_induction:
  frequency: 22.0e+3 
  current: 600 
```

### Temperature field at crystal-melt 

The temperature field for the whole domain and the melt, when convection is accounted

<img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/case3_T.png" width="45%" /><img src="https://github.com/nemocrys/ismcg-examples/blob/main/DemoCZ/pics/case3_melt.png" width="45%" />

