# ismcg-examples
Simulation examples for the ISMCG \

DemoCZ case \
TestCZ case \
both cases with link. Additional and more advanced examples Adved's cases

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

On Linux use:

```
docker run -it --rm -v $PWD:/home/workdir -e LOCAL_UID=$(id -u $USER) -e LOCAL_GID=$(id -g $USER) nemocrys/opencgs:v1.0.1 bash
```

This will open a docker container in interactive mode and map your working directory into the container. All required software to execute the simulation is provided in the container. 

### Visualization

Visualization in the Docker container is not possible. Hence, a post-processing visualization engine, [ParaView](https://www.paraview.org/), is recommended 

## Configuration

dedcribe the included files 
