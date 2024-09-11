# ismcg-examples

The Simulation examples for ISMCG 

This repository contains two axisymmetric steady-state 2D cases of Czochralski crystal growth using [Elmer](https://www.elmerfem.org/blog/).

- [Demo-CZ](https://github.com/nemocrys/ismcg-examples/tree/main/DemoCZ) case 
- [Test-CZ](https://github.com/nemocrys/ismcg-examples/tree/main/TestCZ) case 

Additional and more advanced examples developed by the [ Model experiments group ](https://www.ikz-berlin.de/en/research/materials-science/section-fundamental-description-1) can be found here: [Opencgs examples](https://github.com/nemocrys/opencgs_examples?tab=readme-ov-file) 


## Computational setup
The necessary software to  set up and execute crystal growth numerical simulations is included in our opencgs Docker container. \
For mesh generation, [objectgmsh](https://github.com/nemocrys/objectgmsh), a gmsh wrapper that greatly reduces  modelling effort, is utilised. \
To execute the simulations, [Pyelmer](https://github.com/nemocrys/pyelmer) is used, which provides an integrated workflow to compose the .sif file and set up [ElmerFEM](https://www.elmerfem.org/blog/) simulations from Python.

### Docker

An installation of [Docker](https://docs.docker.com/get-started/get-docker/)  is required to work with the [opencgs](https://hub.docker.com/r/nemocrys/opencgs) container.  \
Then through ```docker pull nemocrys/opencgs:v1.0.1 ```, the latest version of opencgs image is downloaded from Docker Hub.




To run the docker container on Windows execute the following command in the directory containing this repository:

```
docker run -it --rm -v ${PWD}:/home/workdir nemocrys/opencgs:v1.0.1 bash
```

On Linux, use:

```
docker run -it --rm -v $PWD:/home/workdir -e LOCAL_UID=$(id -u $USER) -e LOCAL_GID=$(id -g $USER) nemocrys/opencgs:v1.0.1 bash
```

This will open a docker container in interactive mode and map your working directory into the container. All required software to execute the simulation is provided in the container. 

### Visualization

Visualization in the Docker container is not possible. 

To locally visualize the simulation mesh, [Gmsh](https://gmsh.info/) needs to be installed. \
A post-processing visualization engine, [ParaView](https://www.paraview.org/), is also necessary.

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



## Model description

The main features of [Test-CZ](https://github.com/nemocrys/ismcg-examples/tree/main/TestCZ) model are:
- Heat transfer through conduction and radiation
- Induction heating of the crucible
- Phase change: the interface between crystal and melt is shifted into the isothermal of the melting point


2D steady-state electromagnetism and heat transfer simulation of the NEMOCRYS Test-CZ Furnace:

<img src="https://github.com/nemocrys/ismcg-examples/blob/main/TestCZ/mesh.png">

