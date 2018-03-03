from collections import defaultdict

class Color():
    WHITE="W"
    BLACK="B"
    EMPTY="E"

class Square():
    
    def __init__(self, pos, color):
        self.position = pos
        self.color = color

    def to_string(self):
        return "Square:: "+str(self.position)+" "+self.color
class SquareGraph():
    '''
        Square graph class
    '''
    
    def __init__(self):
        self.graph = defaultdict(set)
        self.map = dict()
        
    def delete_edge(self, s1, s2):
        '''
            Delete edge between s1 and s2
        '''
        if type(s1)==tuple:
            s1 = self.map[s1]
            s2 = self.map[s2]
        
        self.graph[s1].remove(s2)
        self.graph[s2].remove(s1)
        
    def add_edge(self, s1, s2):
        '''
            Add edge between s1 and s2
        '''
        if type(s1)==tuple:
            s1 = self.map[s1]
            s2 = self.map[s2]
        
        self.graph[s1].add(s2)
        self.graph[s2].add(s1)
    
    def add_square(self,s1):
        self.graph[s1]
        self.map[s1.position]=s1
    
    def get_square(self, pos):
        return self.map[pos]
    def print_me(self):
        for k,v in self.graph.items():
            print(k.to_string(), end=" -> ")
            for s in v:
                print(s.to_string(), end=", ")
            print("")
class Node():
    '''
        Corner graph node
    '''
    def __init__(self, pos,
                 SQ_TL=None, SQ_TR=None, SQ_BL=None, SQ_BR=None,  
                 is_boundary_node=False):
        self.position = pos
        self.SQ_TL = SQ_TL
        self.SQ_TR = SQ_TR
        self.SQ_BL = SQ_BL
        self.SQ_BR = SQ_BR
        self.is_boundary_node = is_boundary_node
        self.is_start_node = False
        self.is_target_node = False
        
    def to_string(self):
        return "Node:: "+str(self.position)
class CornerGraph():
    
    def __init__(self):
        self.graph = defaultdict(set)    
        self.map = dict()
    def delete_edge(self, n1, n2):
        '''
            Delete edge between n1 and n2
        '''
        if type(n1)==tuple:
            n1 = self.get_node(n1)
            n2 = self.get_node(n2)
        
        self.graph[n1].remove(n2)
        self.graph[n2].remove(n1)
        
    def add_edge(self, n1, n2):
        '''
            Add edge between n1 and n2
            n1: node n1 or position of n1, = (i,j)
            n1: node n1 or position of n2, = (i,j)
        '''
        if type(n1)==tuple:
            n1 = self.get_node(n1)
            n2 = self.get_node(n2)
        
        self.graph[n1].add(n2)
        self.graph[n2].add(n1)
    
    def add_node(self,n1):
        self.graph[n1]
        self.map[n1.position] = n1
    
    def get_node(self,pos):
        return self.map[pos]
   
    def is_edge(self, pos1, pos2):
        n1 = self.get_node(pos1)
        n2 = self.get_node(pos2)
        
        if n2 in self.get_neighbours(n1):
            return True
        else:
            return False
    
    def get_neighbours(self, n1):
        if type(n1)==tuple:
            n1 = self.get_node(n1)
        return self.graph[n1]
    
        
    def print_me(self):
        for k,v in self.graph.items():
            print(k.to_string(), end=" -> ")
            for s in v:
                print(s.to_string(), end=", ")
            print("")
            
class GraphBuilder():
    '''
        Builds square and corner graph
        
        Txt file representation 
        . = edge present
        ~ = edge broken
        B = Black square
        W = White square
        E = Empty square
        * = starting point
        # = end point
        
    '''
    def __init__(self):
        self.square_graph = SquareGraph()
        self.corner_graph = CornerGraph()
        
    def __read_file(self,file_path):
        matrix = []
        with open(file_path) as fp:
            for line in fp:
                print(line)
                matrix.append(line.rstrip().split(" "))
        
        return matrix
    
    def __is_boundary_node(self,i,j):
        if i==0 or j==0 or i == self.CR_ROWS-1 or j==self.CR_COLS-1:
            return True
        return False
    
    def __build_square_graph(self, matrix):
        # build square graph
        for i in range(1,self.CR_ROWS,2):
            for j in range(1,self.CR_COLS,2):
                sq = Square((int(i/2),int(j/2)),matrix[i][j])
                self.square_graph.add_square(sq)
                #print(sq.to_string())
        for i in range(self.SQ_ROWS):
            for j in range(self.SQ_COLS):
                if i < self.SQ_ROWS-1:
                    self.square_graph.add_edge((i,j),(i+1,j))
                if i > 0:
                    self.square_graph.add_edge((i,j),(i-1,j))
                if j < self.SQ_COLS-1:
                    self.square_graph.add_edge((i,j),(i,j+1))
                if j > 0:
                    self.square_graph.add_edge((i,j),(i,j-1))
        self.square_graph.print_me()
        
    
    def __build_corner_graph(self, matrix):
        def get_squares(_i, _j):
            r= int(_i/2)
            c = int(_j/2)
            BR,BL,TR,TL = None,None,None,None
            if r < self.SQ_ROWS:
                if c < self.SQ_COLS:
                    BR = self.square_graph.get_square((r,c))
                if c!=0:
                    BL = self.square_graph.get_square((r,c-1))
            if r!=0:
                if c < self.SQ_COLS:
                    TR = self.square_graph.get_square((r-1,c))
                if c!=0:
                    TL = self.square_graph.get_square((r-1,c-1))
            return TL,TR,BL,BR
        def my_print(x):
            if x:
                return x.position
            else:
                return x
        for i in range(0,self.CR_ROWS,2):
            for j in range(0,self.CR_COLS,2):
                TL,TR,BL,BR = get_squares(i,j)
                
                #print(i,j,my_print(TL),my_print(TR),my_print(BL),my_print(BR))
                node = Node((int(i/2),int(j/2)), SQ_TL=TL, SQ_TR=TR, SQ_BL=BL, SQ_BR=BR, is_boundary_node=self.__is_boundary_node(i,j))
                if matrix[i][j]=="*":
                    node.is_start_node=True
                elif matrix[i][j]=="#":
                    node.is_target_node=True
                self.corner_graph.add_node(node)
                
        for i in range(0,self.CR_ROWS,2):
            for j in range(0,self.CR_COLS,2):
                _i = int(i/2)
                _j = int(j/2)
                o = 1 if i%2==0 else 0
                if i !=0:
                    if matrix[i-1][j]==".":
                        self.corner_graph.add_edge((_i,_j), (_i-1,_j))
                    if i!=self.CR_ROWS-1:
                        if matrix[i+1][j]==".":
                            self.corner_graph.add_edge((_i,_j), (_i+1,_j))
                if j !=0:
                    if matrix[i][j-1]==".":
                        self.corner_graph.add_edge((_i,_j), (_i,_j-1))
                    if j!=self.CR_COLS-1:
                        if matrix[i][j+1]==".":
                            self.corner_graph.add_edge((_i,_j), (_i,_j+1))
        self.corner_graph.print_me()
    def build_graph(self,file_path):
        
        matrix = self.__read_file(file_path)
        self.CR_COLS = len(matrix[0])
        self.CR_ROWS = len(matrix)
        
        self.SQ_COLS = int(self.CR_COLS/2)
        self.SQ_ROWS = int(self.CR_ROWS/2)
        
        self.__build_square_graph(matrix)
        self.__build_corner_graph(matrix)
    
    def print_board(self):
        for i in range(self.CR_ROWS):
            for j in range(self.CR_COLS):
                e = "" if j==self.CR_COLS-1 else " "
                p1 = (int(i/2), int(j/2))
                n1 = self.corner_graph.get_node(p1)
                            
                if i%2==0:
                    if j%2== 0:
                        if n1.is_start_node:
                            print("*", end=e)
                        elif n1.is_target_node:
                            print("#", end=e)
                        else:
                            print(".", end=e)
                    else:
                        if j != self.CR_COLS-1:
                            p2 = (int(i/2), int(j/2)+1)
                            
                            if self.corner_graph.is_edge(p1,p2):
                                print(".",end=e)
                            else:
                                print("~",end=e)
                else:
                    if j%2== 1:
                        if j!=self.CR_COLS-1:
                            #print(p1)
                            print(n1.SQ_BR.color, end=e)
                    else:
                        if i!= self.CR_ROWS-1:
                            p2 = (int(i/2)+1, int(j/2))
                            
                            if self.corner_graph.is_edge(p1,p2):
                                print(".",end=e)
                            else:
                                print("~",end=e)
            
            print("")        
g = GraphBuilder()
g.build_graph("board_3x3_1.txt")
g.print_board()