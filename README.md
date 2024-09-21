# The Simulation examples for ISMCG 


This repository contains two axisymmetric steady-state 2D cases of Czochralski crystal growth using [Elmer](https://www.elmerfem.org/blog/).

- [Demo-CZ without Python](https://github.com/nemocrys/ismcg-examples/tree/main/DemoCZ-withoutPython) case just for reference: 
- [Demo-CZ](https://github.com/nemocrys/ismcg-examples/tree/main/DemoCZ) case 
- [Test-CZ](https://github.com/nemocrys/ismcg-examples/tree/main/TestCZ) case 

Additional and more advanced examples developed by the [ Model experiments group ](https://www.ikz-berlin.de/en/research/materials-science/section-fundamental-description-1) can be found here: [Opencgs examples](https://github.com/nemocrys/opencgs_examples?tab=readme-ov-file).


## How to install

The essential workflow for configuring and running Czochralski crystal growth simulations is encapsulated within our OpenCGS Docker container, while visualization and post-processing tasks are handled by separate software tools.

### Docker

Docker Image is a package of software that includes everything needed to run an application, in this case the required setup to run numerical simulations for crystal growth.

**For Windows:**

1) Download and install [Docker](https://docs.docker.com/get-started/get-docker/). Note than administrator rights are required.
2) Create a new empty folder ```docker-project```, where it will be used as working directory for Docker. 
3) Copy the path of the folder, e.g ```C:\Users\user\Private\docker-projects```.  
4) Open Windows PowerShell. 
5) Navigate to the working directory by ```cd C:\Users\user\Private\docker-projects```. 
6) Type ```pwd``` at the terminal to confirm you are in the correct directory .
7) Make sure that the status of Docker Desktop is "Engine running" by clicking on the taskbar icon. If it is not running, try to restart Docker.
8) Then run the following Docker command , which creates an interactive container from the [opencgs image](https://hub.docker.com/r/nemocrys/opencgs). You may also search for this image in Docker desktop and "Pull" it first, which involves about 4 GB download.

```
docker run -it --rm -v ${PWD}:/home/workdir nemocrys/opencgs:v1.0.1 bash
```

Further instructions on running the simulations are given in the Readme files of the examples. You may download all example files as ZIP from GitHub and extract in ```docker-project``` 

**For Linux:** \
The initial steps to create a working directory remain the same, but the last Docker command is :

```
docker run -it --rm -v $PWD:/home/workdir -e LOCAL_UID=$(id -u $USER) -e LOCAL_GID=$(id -g $USER) nemocrys/opencgs:v1.0.1 bash
```

This will open a docker container in interactive mode and map your working directory into the container. 

- For mesh generation, [objectgmsh](https://github.com/nemocrys/objectgmsh), a gmsh wrapper that greatly reduces  modelling effort, is utilised. 
- To execute the simulations, [Pyelmer](https://github.com/nemocrys/pyelmer) is used, which provides an integrated workflow to compose the .sif file and set up [ElmerFEM](https://www.elmerfem.org/blog/) simulations from Python.


### Code editing

Since Python is used to prepare and run the simulations, a code editor will be very useful. You may want to install one of these or similar tools:

- Notepad++ (simple): [Notepad++](https://notepad-plus-plus.org/)
- Visual Studio Code (advanced): [VSCode](https://code.visualstudio.com/)


### Visualization


- To locally visualize the simulation mesh, [Gmsh](https://gmsh.info/) needs to be installed. A ZIP file can be downloaded and extracted, without the need to run an installer.
- A post-processing visualization engine, [ParaView](https://www.paraview.org/), is also necessary. A ZIP file can be downloaded and extracted, without the need to run an installer.


## Acknowledgements

[This project](https://nemocrys.github.io/) has received funding from the European Research Council (ERC) under the European Union's Horizon 2020 research and innovation programme (grant agreement No 851768).

<img src="https://raw.githubusercontent.com/nemocrys/pyelmer/master/EU-ERC.png">
