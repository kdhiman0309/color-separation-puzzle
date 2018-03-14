from connect_components import CheckConnectedComponents
from base_solver import BaseSolver


class HeuristicsSolver(BaseSolver):
    
    def __init__(self, square_graph, corner_graph, verbose=False, flag=False):
        self.square_graph = square_graph
        self.corner_graph = corner_graph
        self.path = []
        self.verbose = verbose
        self.conn_comp = CheckConnectedComponents(self.square_graph, self.corner_graph)
        self.flag = flag
    def solve(self):
        
        self.path.append(self.corner_graph.start_node)
        found = self.solve_heuristics(self.corner_graph.start_node)
        if not found:
            return []
        return self.path
    
    def get_node_on_boundary(self, node, s1, s2):
        
        #if .is_boundary_node and square.N_TL!=node:
        #    return 
        i,j = node.position
        if i==0 or i==self.corner_graph.NUM_ROWS-1:
            n1 = self.corner_graph.get_node((i,j+1))
            n2 = self.corner_graph.get_node((i,j-1))
            if n1 in s1.adj_nodes:
                return n1, n2
            else:
                return n2, n1
        else:
            n1 = self.corner_graph.get_node((i+1,j))
            n2 = self.corner_graph.get_node((i-1,j))
            
            if n1 in s1.adj_nodes:
                return n1, n2
            else:
                return n2, n1
        
        return None
    
    
        
        
    
    def solve_heuristics(self, node, S1_prev=None, S2_prev=None, prev_dir=None):
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
        
        neighbours_priority = []
        if node.is_boundary_node: 
            S1_same_color, S2_same_color = True, True
            if self.flag:
                if S1_prev and S2_prev:
                    # optimization
                    # We form a new connected component only when we reach boundary node from an internal node.
                    
                    S1_same_color = self.conn_comp.is_same_colors(S1_prev)
                    S2_same_color = self.conn_comp.is_same_colors(S2_prev)
                    if not (S1_same_color or S2_same_color):
                        #print("Not same color!")
                        node.is_visited = False
                        return False
                    else:
                        n1, n2 = self.get_node_on_boundary(node, S1_prev, S2_prev)
                        #assert(n1.is_boundary_node)
                        #assert(n1 in S1_prev.adj_nodes)
                        #assert(n2.is_boundary_node) 
                        #assert(n2 in S2_prev.adj_nodes)
                        if S1_same_color:
                            if self.corner_graph.is_edge(node,n2):
                                neighbours_priority.append(n2)
                            if self.corner_graph.is_edge(node,n1):
                                neighbours_priority.append(n1)
                                
                        else:
                            if self.corner_graph.is_edge(node,n1):
                                neighbours_priority.append(n1)
                            if self.corner_graph.is_edge(node,n2):
                                neighbours_priority.append(n2)
                            
                            
            else:
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
        '''
        # heuristics 1
        xxxxxx No Improvement xxxxxxxx
        # remove other edges from a node.
        for nei in neighbours:
            self.corner_graph.delete_edge(node, nei)
        ''' 
        if self.flag and neighbours_priority:
            neighbours = neighbours_priority
            #neighbours = set(neighbours_priority).union(set(neighbours))
            None
            
        always_taken_neighbours = self.corner_graph.always_taken_neighbours(node,neighbours)
        
        if always_taken_neighbours:
            neighbours = always_taken_neighbours
        
        for nei in neighbours:
            if not nei.is_visited:
                self.path.append(nei)
                d = self.direction(node,nei)
                S1,S2 = self.get_squares(node,d)
                print("from:",node.to_string(), "to:",nei.to_string(), end=" ")  if self.verbose else None
                print("dir:"+d+" S1",(S1.to_string() if S1 else "None"), " ", "S2:", (S2.to_string()  if S2 else "None"))  if self.verbose else None
                
                if S1 and S2:
                    self.square_graph.delete_edge(S1,S2)
                    
                if self.solve_heuristics(nei,S1,S2,d):
                    return True
                
                if S1 and S2:
                    self.square_graph.add_edge(S1,S2) 
                self.path.pop()
        '''
        # undo heuristics 1
        for nei in neighbours:
            self.corner_graph.add_edge(node, nei)
        '''
        node.is_visited = False
    
        return False
