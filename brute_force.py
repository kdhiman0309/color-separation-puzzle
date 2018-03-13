from connect_components import CheckConnectedComponents
from base_solver import BaseSolver


class BruteForceSolver(BaseSolver):
    
    def __init__(self, square_graph, corner_graph, verbose=False):
        self.square_graph = square_graph
        self.corner_graph = corner_graph
        self.path = []
        self.verbose = verbose
        self.conn_comp = CheckConnectedComponents(self.square_graph, self.corner_graph)
        
    def solve(self):
        found = self.solve_brute_force(self.corner_graph.start_node)
        if not found:
            return []
        return [self.corner_graph.start_node]+self.path
    def solve_brute_force(self, node, S1_prev=None, S2_prev=None):
        if node.is_visited:
            return False
        
        node.is_visited = True
        print("At:", node.position) if self.verbose else None
        
        if node.is_target_node:
            correct_sol = self.conn_comp.check_solution()
            if not correct_sol:
                node.is_visited = False
                print("at target, conditions not met!")  if self.verbose else None
                return False
            else:
                return True
            #return True
        
        
        if node.is_boundary_node: 
            S1_same_color, S2_same_color = True, True
            if S1_prev:
                S1_same_color = self.conn_comp.is_same_colors(S1_prev)
            if S2_prev:
                S2_same_color = self.conn_comp.is_same_colors(S2_prev)
        
            if not (S1_same_color or S2_same_color):
                #print("Not same color!")
                node.is_visited = False
                return False
        
        #same_color = conn_comp.check_connect_components(S1_prev,S2_prev)
        #if (!same_color):
    			#return false
    
        neighbours = self.corner_graph.get_neighbours(node)
        print("neighbours",node.to_string(), end=" -> ")  if self.verbose else None
        if self.verbose:
            for nei in neighbours:
               print(nei.to_string(), end=" ")
            print("")
        for nei in neighbours:
            if not nei.is_visited:
                
                self.path.append(nei)
                d = self.direction(node,nei)
                S1,S2 = self.get_squares(node,d)
                print("from:",node.to_string(), "to:",nei.to_string(), end=" ")  if self.verbose else None
                print("dir:"+d+" S1",(S1.to_string() if S1 else "None"), " ", "S2:", (S2.to_string()  if S2 else "None"))  if self.verbose else None
                
                if S1 and S2:
                    self.square_graph.delete_edge(S1,S2)
                    
                if self.solve_brute_force(nei,S1,S2):
                    return True
                
                if S1 and S2:
                    self.square_graph.add_edge(S1,S2) 
                self.path.pop()
    
        node.is_visited = False
    
        return False
