
class CheckConnectedComponents():

    def __init__(self, square_graph, corner_graph):
        self.square_graph = square_graph
        self.corner_graph = corner_graph
        self.visited = set()
    
    def is_same_colors(self,square):
        if True:
            return self.is_same_colors_v2(square)
        
        self.visited = set()
        return self.__same_colors(square, color=square.color)
    
    def is_same_colors_v2(self,square):
        
        squares = self.get_connected_squares(square)
        curr_color=square.color
        same_color = True
        for s in squares:
            if curr_color=='.':
                curr_color = s.color
            elif s.color!='.' and curr_color != s.color:
                same_color = False
                break
        return same_color        
    
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
    
    def get_connected_squares(self, square):
        squares = set()
        self.__get_connected_squares(square, squares)
        return squares
    
    def __get_connected_squares(self, square, squares):
        squares.add(square)
        
        for s1 in self.square_graph.get_neighbours(square):
            if not s1 in squares:
                self.__get_connected_squares(s1,squares)
        
    def check_solution(self):
        for s1 in self.square_graph.graph.keys():
            if not s1 in self.visited:
                if not self.is_same_colors(s1):
                    return False
    
        return True
    