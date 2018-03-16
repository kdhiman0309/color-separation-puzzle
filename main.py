import graph
from brute_force import BruteForceSolver
from heuristics_solver import HeuristicsSolver
import time
import copy

#boards = [(3,3),(3,4),(4,4),(4,5),(5,5),(5,6),(6,6)]
boards = [(5,6),(6,6)]
#boards = [(2,2),(2,3)]
#num_iters = [1000,1000,1000,100,100,100,50]
num_iters = [10,10]
file = open('out4.txt','w')
prob_b = 0.8
prob_w = 0.8
broken = 0.01
_str = ""
_str+="_________________________________"+"\n"
_str+="prob_b:%f prob_w:%f prob_broken:%f"%(prob_b,prob_w,broken)+"\n"
    
def time_it(g, solver, pre_process=False):
    start=time.process_time()
    if pre_process:
        p = graph.PreprocessGraph()
        p.preprocess(g)
        
    solver.solve()
    end=time.process_time()
    return end-start
    
for i in range(len(boards)):
    _str+="_________________________________"+"\n"
    NUM_ROWS,NUM_COLS = boards[i]
    #NUM_ROWS = 5
    #NUM_COLS = 5
    num_iter = int(num_iters[i])
    _str+="board size %d %d iters:%d"%(NUM_ROWS, NUM_COLS, num_iter)+"\n"
    time_HS = 0
    time_BF = 0
    time1, time2, time3, time4, time5, time6, time7, time8 = 0,0,0,0,0,0,0,0
    for i in range(num_iter):
        #print("_________________________________")
        g = graph.GraphBuilder()
        g.build_random_graph(num_rows=NUM_ROWS, num_cols=NUM_COLS, prob_squares=[prob_b, prob_w], prob_broken_edges=broken)
        
        g_copy = copy.deepcopy(g)
        solver = BruteForceSolver(g_copy.square_graph, g_copy.corner_graph)
        time1 += time_it(g_copy, solver, pre_process=False)
        
        g_copy = copy.deepcopy(g)
        solver = BruteForceSolver(g_copy.square_graph, g_copy.corner_graph)
        time2 += time_it(g_copy, solver, pre_process=True)
        
        g_copy = copy.deepcopy(g)
        solver = BruteForceSolver(g_copy.square_graph, g_copy.corner_graph, optimization2=True)
        time3 += time_it(g_copy, solver, pre_process=True)
        
        g_copy = copy.deepcopy(g)
        solver = HeuristicsSolver(g_copy.square_graph, g_copy.corner_graph, heuristic1=True)
        time4 += time_it(g_copy, solver, pre_process=True)
        
        g_copy = copy.deepcopy(g)
        solver = HeuristicsSolver(g_copy.square_graph, g_copy.corner_graph, heuristic2=True)
        time5 += time_it(g_copy, solver, pre_process=True)
        
        g_copy = copy.deepcopy(g)
        solver = HeuristicsSolver(g_copy.square_graph, g_copy.corner_graph, heuristic2=True, optimzation1=True)
        time6 += time_it(g_copy, solver, pre_process=True)
        
        g_copy = copy.deepcopy(g)
        solver = HeuristicsSolver(g_copy.square_graph, g_copy.corner_graph, heuristic3=True)
        time7 += time_it(g_copy, solver, pre_process=True)
        
        g_copy = copy.deepcopy(g)
        solver = HeuristicsSolver(g_copy.square_graph, g_copy.corner_graph, 
                                     heuristic1=True, heuristic2=True, optimzation1=True, heuristic3=True)
        time8 += time_it(g_copy, solver, pre_process=True)
    T = [time1, time2, time3, time4, time5, time6, time7, time8]
    
    for t in range(len(T)):
        _str+="time%d, %f\n"%(t,T[t]/num_iter)
        file.write(_str)
        _str=""
file.close()
