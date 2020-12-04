# routingcalc
Routing Table Calculator for Minecraft

## rc_old.cpp

A simple implement of Floyd algorithm. A C++11 compatible compiler is required.

`g++ -std=c++11 -o rc rc_old.cpp`

## dist_mst.py

Input: node name, node position x, node position z

Output:
- distance bewteen each nodes
- MST planning and shortest total path.

Python3 is required. Sample input available at `nodes_list.txt`

## route_calc.py

Input: node1, node2, distance

Output:
- path length between each nodes
- reversed routing
- forward routing table

Python3 is required. Sample input available at `paths_list.txt`