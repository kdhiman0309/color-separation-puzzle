import graph
from brute_force import BruteForceSolver
from heuristics_solver import HeuristicsSolver
import time
import copy
time_HS = 0
time_BF = 0

NUM_ROWS = 5
NUM_COLS = 5

for i in range(10):
    
    g = graph.GraphBuilder()
    #g.build_graph(file_path="board_3x3_1.txt")
    g.build_random_graph(num_rows=NUM_ROWS, num_cols=NUM_COLS, prob_squares=[0.3,0.3], prob_broken_edges=0.01)
    #g.save_to_file("random.txt")
    #g.print_board()
    
    g_copy = copy.deepcopy(g)
    start=time.process_time()
    #p = graph.PreprocessGraph(g)
    #p.preprocess(g)

    btf = HeuristicsSolver(g.square_graph, g.corner_graph, flag=True)
    path_BF = btf.solve()
    end=time.process_time()
    #g.print_board(path=path_BF)
    time_BF+=end-start
    #btf.print_path()
    
    g = g_copy
    #g.print_board()
    start=time.process_time()
    
    #p = graph.PreprocessGraph(g)
    #p.preprocess(g)

    btf = HeuristicsSolver(g.square_graph, g.corner_graph, flag=True)
    path_HS = btf.solve()
    end=time.process_time()
    #g.print_board(path=path_HS)
    time_HS+=end-start
    #btf.print_path()
    if len(path_BF)==0:
        #print(len(path_BF),len(path_HS))
        assert(len(path_HS)==0)
    else:
        #print(len(path_BF),len(path_HS))
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