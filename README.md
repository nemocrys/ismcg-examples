# The Simulation examples for ISMCG 


This repository contains two axisymmetric steady-state 2D cases of Czochralski crystal growth using [Elmer](https://www.elmerfem.org/blog/).

- [Demo-CZ](https://github.com/nemocrys/ismcg-examples/tree/main/DemoCZ) case 
- [Test-CZ](https://github.com/nemocrys/ismcg-examples/tree/main/TestCZ) case 

Additional and more advanced examples developed by the [ Model experiments group ](https://www.ikz-berlin.de/en/research/materials-science/section-fundamental-description-1) can be found here: [Opencgs examples](https://github.com/nemocrys/opencgs_examples?tab=readme-ov-file).


## Computational setup

The essential workflow for configuring and running Czochralski crystal growth simulations is encapsulated within our OpenCGS Docker container, while visualization and post-processing tasks are handled by separate software tools.

### Docker

Docker Image is a package of software that includes everything needed to run an application, in this case the required setup to run numerical simulations for crystal growth.

**For Windows:**

1) Download and install [Docker](https://docs.docker.com/get-started/get-docker/). 
2) Create a new empty folder ( ```<"docker-project"> ``` ) , where it will be used as working directory for Docker. 
3) Copy the path of the folder(e.g ```C:\Users\admin\Private\<"docker-project">```).  
4) Open Windows PowerShell. 
5) Navigate to the working directory by ```cd C:\Users\admin\Private\<"docker-project"> ```. 
6) Type ```pwd``` at the terminal to confirm you are in the correct directory .
7) Then run the following Docker command , which creates an interactive container from the [opencgs image](https://hub.docker.com/r/nemocrys/opencgs). 



```
docker run -it --rm -v ${PWD}:/home/workdir nemocrys/opencgs:v1.0.1 bash
```


**For Linux:** \
The initial steps to create a working directory remain the same, but the last Docker command is :

```
docker run -it --rm -v $PWD:/home/workdir -e LOCAL_UID=$(id -u $USER) -e LOCAL_GID=$(id -g $USER) nemocrys/opencgs:v1.0.1 bash
```



This will open a docker container in interactive mode and map your working directory into the container. 

- For mesh generation, [objectgmsh](https://github.com/nemocrys/objectgmsh), a gmsh wrapper that greatly reduces  modelling effort, is utilised. 
- To execute the simulations, [Pyelmer](https://github.com/nemocrys/pyelmer) is used, which provides an integrated workflow to compose the .sif file and set up [ElmerFEM](https://www.elmerfem.org/blog/) simulations from Python.



### Visualization


- To locally visualize the simulation mesh, [Gmsh](https://gmsh.info/) needs to be installed. 
- A post-processing visualization engine, [ParaView](https://www.paraview.org/), is also necessary.


## Acknowledgements

[This project](https://nemocrys.github.io/) has received funding from the European Research Council (ERC) under the European Union's Horizon 2020 research and innovation programme (grant agreement No 851768).

<img src="https://raw.githubusercontent.com/nemocrys/pyelmer/master/EU-ERC.png">
