
class CheckConnectedComponents():

    def __init__(self, square_graph, corner_graph):
        self.square_graph = square_graph
        self.corner_graph = corner_graph
        self.visited = set()
    
    def is_same_colors(self,square):
        self.visited = set()
        return self.__same_colors(square, color=square.color)
    
    def __same_colors(self, square, color=None):
        if not color or color=='.':
            color = square.color
        
        if color!='.' and square.color!='.' and square.color != color:
            # exit if current 'color' and square color are opposite 
            return False
        
        self.visited.add(square)
        
        for s1 in self.square_graph.get_neighbours(square):
            if not s1 in self.visited:
                if not self.__same_colors(s1, color):
                    return False
            
        
        return True
    
    
    def check_solution(self):
        for s1 in self.square_graph.graph.keys():
            if not s1 in self.visited:
                if not self.is_same_colors(s1):
                    return False
    
        return True
    