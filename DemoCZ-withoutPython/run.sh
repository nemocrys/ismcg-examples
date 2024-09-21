#!/bin/bash

#ElmerGrid 14 2 case.msh 2>&1 | tee loggrid.txt
#ElmerSolver 2>&1 | tee logsolve.txt
python3 vtu2msh.py 2>&1 | tee logpost.txt

