import numpy as np

f_src=open('nodes_list.txt','r')

# imported node information
nodes=[]	# info: [{'node':'x', 'x':pos_x, 'z':pos_z}]
len_nodes=0	# amount

while(True):
  linetmp=f_src.readline()
  if(not linetmp):
    break
  line=linetmp.split('\t')
  if(len(line)!=3):
    break
  nodes.append({'node':line[0],'x':int(line[1]),'z':int(line[2])})
len_nodes=len(nodes)

f_src.close()

print("Distance table:")
# n*n distance table: length=dist_table_full[index1][index2]
dist_table_full=np.full((len_nodes, len_nodes), -1, dtype=int)
# n*(n-1)/2 E dict: {'node1':index1, 'node2':index2, 'length':len}
dist_table_dict=[]

print("#\t",end ="")
for i in range(0,len_nodes):
  if(i==len_nodes-1):
    print(nodes[i]['node'],end ="\n")
  else:
    print(nodes[i]['node'],end ="\t")

for i in range(0,len_nodes):
  print(nodes[i]['node'],end ="\t")
  for j in range(0,len_nodes):
    dist_table_full[i][j]=int(pow(pow(nodes[i]['x']-nodes[j]['x'],2)+pow(nodes[i]['z']-nodes[j]['z'],2),1/2))
    if(i < j):
      dist_table_dict.append({'node1':i, 'node2':j, 'length':dist_table_full[i][j]})
    if(j==len_nodes-1):
      print(dist_table_full[i][j],end ="\n")
    else:
      print(dist_table_full[i][j],end ="\t")

print()

## MST: Prim
# G = (V=nodes, E=dist_table_full)
prim_V_a=[]	# target nodes collection
prim_V_b=[]	# source nodes collection
prim_path=[]	# generated path: {'node1':index, 'node2':index}
sum_length=0

for i in range(0,len_nodes):
  prim_V_b.append({'index':i})

prim_V_a.append(prim_V_b.pop())	# init node

while(prim_V_b):
  node_b=prim_V_b.pop()

  connectedto_a_index=-1	# which a should b connected to
  min_length=-1	# total minimum length
  for node_a in prim_V_a:
    target_len=dist_table_full[node_a['index']][node_b['index']]
    if(target_len == -1):
      continue	# skip
    if(min_length==-1):
      min_length=target_len
      connectedto_a_index=node_a['index']
    else:
      if(min_length > target_len):
        min_length = target_len
        connectedto_a_index=node_a['index']
  if(connectedto_a_index == -1):
    print("MST failed for node %d %s : no path valid"%(node_b['index'],nodes[node_b['index']]['node']))
  else:
    sum_length=sum_length+dist_table_full[connectedto_a_index][node_b['index']]
    prim_V_a.append(node_b)
    prim_path.append({'node1':min(connectedto_a_index,node_b['index']), 'node2':max(connectedto_a_index,node_b['index'])})
# MST length table
conn_table_mst=np.full((len(prim_V_a), len(prim_V_a)), 0, dtype=int)
for gen_path in prim_path:
  conn_table_mst[gen_path['node1']][gen_path['node2']]=dist_table_full[gen_path['node1']][gen_path['node2']]
  conn_table_mst[gen_path['node2']][gen_path['node1']]=dist_table_full[gen_path['node2']][gen_path['node1']]
# print table
print("MST table:")
print("#\t",end ="")
for i in range(0,len(prim_V_a)):
  if(i==len(prim_V_a)-1):
    print(nodes[prim_V_a[i]['index']]['node'],end ="\n")
  else:
    print(nodes[prim_V_a[i]['index']]['node'],end ="\t")

for i in range(0,len(prim_V_a)):
  print(nodes[prim_V_a[i]['index']]['node'],end ="\t")
  for j in range(0,len(prim_V_a)):
    if(j==len(prim_V_a)-1):
      print(conn_table_mst[prim_V_a[i]['index']][prim_V_a[j]['index']],end ="\n")
    else:
      print(conn_table_mst[prim_V_a[i]['index']][prim_V_a[j]['index']],end ="\t")
print("Total length: %d"%sum_length)
## MST: Prim
    
print()

print("MST paths:")

print("From\tTo\tLength")
for path in prim_path:
  print("%s\t%s\t%d"%(nodes[path['node1']]['node'],nodes[path['node2']]['node'],conn_table_mst[path['node1']][path['node2']]))
  print("%s\t%s\t%d"%(nodes[path['node2']]['node'],nodes[path['node1']]['node'],conn_table_mst[path['node2']][path['node1']]))
