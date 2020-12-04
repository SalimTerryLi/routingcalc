import numpy as np

f_src=open('paths_list.txt','r')

## imported info
paths=[]	# [{'src':'A', 'dest':'B', 'length':len}]
nodes=[]	# ['node_name']

while(True):
  linetmp=f_src.readline()
  if(not linetmp):
    break
  line=linetmp.split('\t')
  if(len(line)!=3):
    break
  if(nodes.count(line[0])==0):	# new node
    nodes.append(line[0])
  if(nodes.count(line[1])==0):	# new node
    nodes.append(line[1])
  path_tmp={'src':line[0], 'dest':line[1], 'length':int(line[2])}
  if(paths.count(path_tmp)!=0):
    print("Warning: duplicated path found! Ignoring...")
  else:
    paths.append(path_tmp)
len_nodes=len(nodes)
len_paths=len(paths)

f_src.close()

## -imported info

## Some magic

# force check shortest path: each transmission adds 1 length
for path in paths:
  path['length']=path['length']+1

## end magic

## prepare

# length = paths_table[index1][index2]
paths_table=np.full((len_nodes, len_nodes), -1, dtype=int)

for path in paths:
  paths_table[ nodes.index(path['src']) ][ nodes.index(path['dest']) ] = path['length']

## -prepare

print("Imported matrix:")
print("#",end ="")
for i in range(0,len_nodes):
  print("\t%s"%nodes[i],end ="")
  if(i==len_nodes-1):
    print()

for i in range(0,len_nodes):
  print(nodes[i],end ="")
  for j in range(0,len_nodes):
    print("\t%s"%paths_table[i][j],end ="")
    if(j==len_nodes-1):
      print()

print()

### Floyd

## initial matrix

dist_map=np.full((len_nodes, len_nodes), -1, dtype=int)
path_map=np.full((len_nodes, len_nodes), -1, dtype=int)
for i in range(0,len_nodes):
  dist_map[i][i]=0;	# node has dist=0 to itself
  path_map[i][i]=i;	# node routes to itself by itself
for path in paths:
  if(path['length']<=0):
    print("Error: non-positive length found. Exitting...")
    exit(-1)
  dist_map[ nodes.index(path['src']) ][ nodes.index(path['dest']) ]=path['length']
  path_map[ nodes.index(path['src']) ][ nodes.index(path['dest']) ]=nodes.index(path['src'])

## -initial matrix

## loop

for k in range(0,len_nodes):
  for i in range(0,len_nodes):
    for j in range(0,len_nodes):
      if(dist_map[i][j] == -1):	# no valid path
        if((dist_map[i][k]!=-1) and (dist_map[k][j]!=-1)):	# new path is valid
          dist_map[i][j]=dist_map[i][k]+dist_map[k][j]
          path_map[i][j]=k
      else:
        if((dist_map[i][k]!=-1) and (dist_map[k][j]!=-1)):	# new path is valid
          if(dist_map[i][j]>dist_map[i][k]+dist_map[k][j]):	# new path is better
            dist_map[i][j]=dist_map[i][k]+dist_map[k][j]
            path_map[i][j]=k

## -loop

### -Floyd

print("distance table:")
print("#",end ="")
for i in range(0,len_nodes):
  print("\t%s"%nodes[i],end ="")
  if(i==len_nodes-1):
    print()
for j in range(0,len_nodes):
  print(nodes[j],end ="")
  for i in range(0,len_nodes):
    print("\t%s"%dist_map[i][j],end ="")
    if(i==len_nodes-1):
      print()
print()

print("path table:")
print("#",end ="")
for i in range(0,len_nodes):
  print("\t%s"%nodes[i],end ="")
  if(i==len_nodes-1):
    print()
for j in range(0,len_nodes):
  print(nodes[j],end ="")
  for i in range(0,len_nodes):
    if(path_map[i][j]!=-1):
      print("\t%s"%nodes[path_map[i][j]],end ="")
    else:
      print("\t~",end ="")
    if(i==len_nodes-1):
      print()
print()

# Summary
for i in range(0,len_nodes):
  for j in range(0,len_nodes):
    if(dist_map[i][j]==-1):
      print("Warning: no path from %s to %s"%(nodes[i],nodes[j]))

def get_next_hop(src, dest, pathmap):
  if(dest==-1):	# subcall returned -1
    return -1
  if(src==dest):	# A-A type
    return src
  elif(src==pathmap[src][dest]):	# A-B type, return B
    return dest
  elif(dest==pathmap[src][dest]):
    print("ERROR!!!")
  else:	# A-B-...-M , remove M and query again
    return get_next_hop(src, pathmap[src][dest], pathmap)

print("Build instructions list:")
print("Current\tTarget\tRoute")
for i in range(0,len_nodes):
  for j in range(0,len_nodes):
    print("%s\t%s\t%s"%(nodes[i],nodes[j],nodes[get_next_hop(i,j,path_map)]))
