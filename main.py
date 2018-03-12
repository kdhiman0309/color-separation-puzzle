import graph
import brute_force

g = graph.GraphBuilder()
g.build_graph(file_path="board_3x3_1.txt")
#g.build_random_graph(num_rows=3, num_cols=3)
g.print_board()

print("####################### BEFORE PRE PROCESSING ###############")
btf = brute_force.BruteForceSolver(g.square_graph, g.corner_graph)
path = btf.solve()
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
btf = brute_force.BruteForceSolver(g.square_graph, g.corner_graph)
path = btf.solve()
print("\npath:: ",end="")
for p in path:
    print(p.to_string(), end=" -> ")
print()