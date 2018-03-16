import graph
from brute_force import BruteForceSolver
from heuristics_solver import HeuristicsSolver
import time
import copy
time_HS = 0
time_BF = 0

boards = [(3,3),(3,4),(4,4),(4,5),(5,5),(5,6),(6,6)]
num_iters = [10000,1000,1000,100,100,100,50]
prob_b = 0.3
prob_w = 0.3
broken = 0.01
print("_________________________________")
print("prob_b:%f prob_w:%f prob_broken:%f"%(prob_b,prob_w,broken))
    
for i in range(len(boards)):
    NUM_ROWS,NUM_COLS = boards[i]
    #NUM_ROWS = 5
    #NUM_COLS = 5
    num_iter = int(num_iters[i]/50)
    print("board size", NUM_ROWS, NUM_COLS, "iters: ", num_iter)
    for i in range(num_iter):
        #print("_________________________________")
        g = graph.GraphBuilder()
        #g.build_graph(file_path="board_3x3_1.txt")
        g.build_random_graph(num_rows=NUM_ROWS, num_cols=NUM_COLS, prob_squares=[prob_b, prob_w], prob_broken_edges=broken)
        #g.save_to_file("random.txt")
        #g.print_board()
        
        g_copy = copy.deepcopy(g)
        start=time.process_time()
        
        p = graph.PreprocessGraph()
        p.preprocess(g)
        #p = graph.PreprocessGraph(g)
        #p.preprocess(g)
        
        btf = HeuristicsSolver(g.square_graph, g.corner_graph)
        path_BF = btf.solve()
        end=time.process_time()
        #g.print_board(path=path_BF)
        time_BF+=end-start
        #btf.print_path()
        
        g = g_copy
        #g.print_board()
        start=time.process_time()
        
        p = graph.PreprocessGraph()
        p.preprocess(g)
        #print(g.corner_graph.always_taken)
        btf = HeuristicsSolver(g.square_graph, g.corner_graph, optimzation1=True)
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
    
    print("BF:", time_BF/num_iter, "HS", time_HS/num_iter)
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