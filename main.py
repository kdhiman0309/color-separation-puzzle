import graph
from brute_force import BruteForceSolver
from heuristics_solver import HeuristicsSolver
import time
import copy
time_HS = 0
time_BF = 0

NUM_ROWS = 5
NUM_COLS = 5

for i in range(100):
    
    g = graph.GraphBuilder()
    #g.build_graph(file_path="board_3x3_1.txt")
    g.build_random_graph(num_rows=NUM_ROWS, num_cols=NUM_COLS)
    #g.save_to_file("random.txt")
    #g.print_board()
    
    g_copy = copy.deepcopy(g)
    start=time.process_time()
    btf = BruteForceSolver(g.square_graph, g.corner_graph)
    path_BF = btf.solve()
    end=time.process_time()
    
    time_BF+=end-start
    #btf.print_path()
    
    g = g_copy
    #g.print_board()
    p = graph.PreprocessGraph(g)
    p.preprocess(g)

    start=time.process_time()
    btf = BruteForceSolver(g.square_graph, g.corner_graph)
    path_HS = btf.solve()
    end=time.process_time()
    
    time_HS+=end-start
    #btf.print_path()
    if len(path_BF)==0:
        assert(len(path_HS)==0)
    else:
        assert(len(path_HS)!=0)
    
print("BF:", time_BF, "HS", time_HS)
'''

print("################## PRE PROCESSING IN PROGRESS #######################")
g = graph.GraphBuilder()
g.build_graph(file_path="board_3x3_1.txt")

p = graph.PreprocessGraph(g)
p.preprocess(g)

print("####################### AFTER PRE PROCESSING ###############")
start=time.time()
btf = BruteForceSolver(g.square_graph, g.corner_graph)
path = btf.solve()
end=time.time()

time_PP=end-start
print("\npath:: ",end="")
for p in path:
    print(p.to_string(), end=" -> ")
print()


print("TIME BF: ", time_BF, " TIME PP: ",time_PP)

'''