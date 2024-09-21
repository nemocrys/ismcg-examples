import meshio


meshmsh = meshio.read(
    "case.msh",
)

#print('\n\nMSH file:\n')
#print('\npoints = \n', meshmsh.points )
#print('\ncells = \n', meshmsh.cells )
#print('\npoint_data = \n', meshmsh.point_data )
#print('\ncell_data= \n', meshmsh.cell_data )
#print('\nfield_data = \n', meshmsh.field_data )
#print('\ncell_sets = \n', meshmsh.cell_sets )
#print('\ncells_dict = \n', meshmsh.cells_dict )



meshvtu = meshio.read(
    "case/case_t0002.vtu", 
)


# Add gmsh groups from original MSH file (assuming same order of elements in VTU!!!)
for key, d in meshmsh.cell_data.items():
    if key in ["gmsh:physical", "gmsh:geometrical", "cell_tags"]:
        meshvtu.cell_data[key] = [ d[1], d[0] ] # order of cell types changed in VTU!!!
#        print('key = ', key)
#        print('d = ', len(d[0]),' ',len(d[1]),' ', d)        

#print('\n\nVTU file:\n')
#print('\npoints = \n', meshvtu.points )
#print('\ncells = \n', meshvtu.cells )
#print('\npoint_data = \n', meshvtu.point_data )
#print('\ncell_data= \n', meshvtu.cell_data )
#print('\nfield_data = \n', meshvtu.field_data )
#print('\ncell_sets = \n', meshvtu.cell_sets )
#print('\ncells_dict = \n', meshvtu.cells_dict )



meshvtu.write(
    "case/case_t0002.msh",
    file_format="gmsh22",
    binary=False
)


# With gmsh41:
#
# File "/home/pi/.local/lib/python3.7/site-packages/meshio/gmsh/_gmsh41.py", line 608, in _write_nodes
#    "Specify entity information (gmsh:dim_tags in point_data) "
#meshio._exceptions.WriteError: Specify entity information (gmsh:dim_tags in point_data) to deal with more than one cell type.


