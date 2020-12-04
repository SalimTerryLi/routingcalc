#include <cstdio>
#include <string>
#include <algorithm>
#include <vector>

using namespace std;

struct Path{
	char src[32];
	char dest[32];
	int cost;
};

vector<Path> paths;	// stored paths
vector<string> nodes_list;	// stored nodes

template <class T>
int getIndex(vector<T> list, T item){
	for(unsigned i=0;i<list.size();++i){
		if(list[i]==item){
			return static_cast<int>(i);
		}
	}
	return -1;
}

void print_path(const unsigned &beg,const unsigned &end, const vector<vector<int> > &path)
{
	if(path[beg][end]==-1){
		printf("-X->%s",nodes_list[end].c_str());
	}
	else{
		if(beg==path[beg][end]){	// already queried the whole path
			printf("->%s",nodes_list[end].c_str());
		}else{
			print_path(beg,path[beg][end],path);
			print_path(path[beg][end],end,path);
		}
	}
}

int main(){
	printf("Input all known paths: \"source dest cost\"\n");
	printf("blank line will be treated as end of input\n");

	char input_buffer[256];	// char buffer
	Path input_path={};	// directly buffered the original path from stdin
	bool shouldExit=false;
	do{
		fgets(input_buffer,sizeof(input_buffer),stdin);
		switch (sscanf(input_buffer,"%s %s %d %s",input_path.src,input_path.dest,&input_path.cost,input_buffer)){
			case EOF:
				shouldExit=true;
				break;
			case 3:
				// update nodes
				if(find(nodes_list.begin(),nodes_list.end(),input_path.src)==nodes_list.end()){	// is a new node
					nodes_list.emplace_back(string(input_path.src));
				}
				if(find(nodes_list.begin(),nodes_list.end(),input_path.dest)==nodes_list.end()){	// is a new node
					nodes_list.emplace_back(string(input_path.dest));
				}
				// update paths
				paths.push_back(input_path);

				break;
			default:
				printf("incorrect input, try again\n");
				break;
		}
	}while(!shouldExit);

	// build the matrix
	vector<vector<int>> dist_map(nodes_list.size(),vector<int>(nodes_list.size(),-1));
	vector<vector<int>> path_map(nodes_list.size(),vector<int>(nodes_list.size(),-1));
	for(unsigned i=0;i<nodes_list.size();++i){
		dist_map[i][i]=0;	// node has dist=0 to itself
		path_map[i][i]=i;	// node routes to itself by itself
	}
	for(const auto path: paths){	// filling known paths
		int node_src_index=getIndex(nodes_list,string(path.src));
		int node_dest_index=getIndex(nodes_list,string(path.dest));
		if(path.cost<0){printf("negative cost detected! exiting...\n"); return -2;}
		if(dist_map[node_src_index][node_dest_index]!=-1){printf("duplicated path detected! exiting...\n"); return -1;}
		dist_map[node_src_index][node_dest_index]=path.cost;
		path_map[node_src_index][node_dest_index]=node_src_index;	// directly connected nodes
	}

	// Floyd
	for(unsigned k=0;k<nodes_list.size();++k)
		for(unsigned i=0;i<nodes_list.size();++i)
			for(unsigned j=0;j<nodes_list.size();++j){
				if(dist_map[i][j]==-1){	// no valid path
					if((dist_map[i][k]!=-1)&&(dist_map[k][j]!=-1)){	// new path is valid
						dist_map[i][j]=dist_map[i][k]+dist_map[k][j];
						path_map[i][j]=k;
					}
				}else{
					if((dist_map[i][k]!=-1)&&(dist_map[k][j]!=-1)){	// new path valid
						if(dist_map[i][j]>dist_map[i][k]+dist_map[k][j]) {    // new path is better
							dist_map[i][j] = dist_map[i][k] + dist_map[k][j];
							path_map[i][j]=k;
						}
					}
				}
			}

	// Echo
	printf("dist_map\nmap");
	for(const auto& i:nodes_list){printf("\t%s",i.c_str());}
	printf("\n");
	for(unsigned x=0;x<nodes_list.size();++x){
		printf("%s",nodes_list.at(x).c_str());
		for(unsigned y=0;y<nodes_list.size();++y){
			printf("\t%d",dist_map[y][x]);
		}
		printf("\n");
	}

	printf("path_map\nmap");
	for(const auto& i:nodes_list){printf("\t%s",i.c_str());}
	printf("\n");
	for(unsigned x=0;x<nodes_list.size();++x){
		printf("%s",nodes_list.at(x).c_str());
		for(unsigned y=0;y<nodes_list.size();++y){
			if(path_map[y][x]!=-1){
				printf("\t%s",nodes_list[path_map[y][x]].c_str());
			}else{
				printf("\t~");
			}
		}
		printf("\n");
	}

	printf("paths:\n");
	for(unsigned i=0;i<nodes_list.size();++i)
		for(unsigned j=0;j<nodes_list.size();++j){
			if(path_map[i][j]>=0){
				printf("%s",nodes_list[i].c_str());
				print_path(i,j,path_map);
				printf("\n");
			}
		}

	printf("exit");
	return 0;
}