import yaml
from objectgmsh import *
import numpy as np

occ = gmsh.model.occ

def inductor( 
    model,
    dim,
    d,
    d_in,
    X0,
    g=0,
    n=1,
    char_l=0,
    T_init=273.15,
    material="",
    name="inductor",
):
    """2D inductor, defined as a couple of circles
 ### https://github.com/nemocrys/test-cz-induction#overview ### 
    Args:
        model (Model): objectgmsh model
        dim (int): dimension
        d (float): diameter of windings
        d_in (flaot): inner diameter of windings (internal cooling)
        X0 (float): origin, center of bottom winding
        g (float, optional): gap between windings. Defaults to 0.
        n (int, optional): number of windings. Defaults to 1.
        char_l (int, optional): mesh size characteristic length. Defaults to 0.
        T_init (float, optional): initial temperature. Defaults to 273.15.
        material (str, optional): material name. Defaults to "".
        name (str, optional): shape name. Defaults to "inductor".

    Returns:
        Shape: objectgmsh shape
    """
    # X0: center of bottom winding
    ind = Shape(model, dim, name)
    ind.params.d = d
    ind.params.d_in = d_in
    ind.params.g = g
    ind.params.n = n
    ind.params.X0 = X0
    ind.params.T_init = T_init
    ind.params.material = material
    ind.params.area = np.pi * (d ** 2 - d_in ** 2) / 4
    if char_l == 0:
        ind.mesh_size = d / 10
    else:
        ind.mesh_size = char_l

    x = X0[0]
    y = X0[1]
    for _ in range(n):
        circle_1d = factory.addCircle(x, y, 0, d / 2)
        circle = factory.addSurfaceFilling(factory.addCurveLoop([circle_1d]))
        hole_1d = factory.addCircle(x, y, 0, d_in / 2)
        hole = factory.addSurfaceFilling(factory.addCurveLoop([hole_1d]))
        factory.synchronize()
        factory.cut([(2, circle)], [(2, hole)])
        if dim == 3:
            circle = rotate(circle)
        ind.geo_ids.append(circle)
        y += g + d

    return ind

def inductor_filling( 
    model,
    dim,
    d,
    d_in,
    X0,
    g=0,
    n=1,
    char_l=0,
    T_init=273.15,
    material="",
    name="inductor_filling",
):
    # X0: center of bottom winding
    filling = Shape(model, dim, name)
    filling.params.d = d
    filling.params.d_in = d_in
    filling.params.g = g
    filling.params.n = n
    filling.params.X0 = X0
    filling.params.T_init = T_init
    filling.params.material = material
    
    x = X0[0]
    y = X0[1]
    for _ in range(n):
        #circle_1d = factory.addCircle(x, y, 0, d / 2)
        #circle = factory.addSurfaceFilling(factory.addCurveLoop([circle_1d]))
        hole_1d = factory.addCircle(x, y, 0, d_in / 2)
        hole = factory.addSurfaceFilling(factory.addCurveLoop([hole_1d]))
        factory.synchronize()
        if dim == 3:
            circle = rotate(hole)
        filling.geo_ids.append(hole)
        y += g + d


    return filling