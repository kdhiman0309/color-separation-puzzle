import graph
import brute_force

g = graph.GraphBuilder()
#g.build_graph(file_path="board_3x3_1.txt")
g.build_random_graph(num_rows=5, num_cols=5)
g.save_to_file("random.txt")
g.print_board()

btf = brute_force.BruteForceSolver(g.square_graph, g.corner_graph)
path = btf.solve()
print("\npath:: ",end="")
for p in path:
    print(p.to_string(), end=" -> ")
print()