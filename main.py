import graph
import brute_force
import time

g = graph.GraphBuilder()
#g.build_graph(file_path="board_3x3_1.txt")
g.build_random_graph(num_rows=5, num_cols=5)
g.save_to_file("random.txt")
g.print_board()

print("####################### BEFORE PRE PROCESSING ###############")
start=time.time()
btf = brute_force.BruteForceSolver(g.square_graph, g.corner_graph)
path = btf.solve()
end=time.time()

time_BF=end-start
print("\npath:: ",end="")
for p in path:
    print(p.to_string(), end=" -> ")
print()


print("################## PRE PROCESSING IN PROGRESS #######################")
g = graph.GraphBuilder()
g.build_graph(file_path="board_3x3_1.txt")

p = graph.PreprocessGraph(g)
p.preprocess(g)

print("####################### AFTER PRE PROCESSING ###############")
start=time.time()
btf = brute_force.BruteForceSolver(g.square_graph, g.corner_graph)
path = btf.solve()
end=time.time()

time_PP=end-start
print("\npath:: ",end="")
for p in path:
    print(p.to_string(), end=" -> ")
print()


print("TIME BF: ", time_BF, " TIME PP: ",time_PP)