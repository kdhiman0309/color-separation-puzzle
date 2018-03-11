from collections import defaultdict
import random
class Color():
    WHITE="W"
    BLACK="B"
    EMPTY="."

class Square():
    
    def __init__(self, pos, color, N_TL=None, N_TR=None, N_BL=None, N_BR=None):
        self.position = pos
        self.color = color
        self.N_TL = N_TL
        self.N_TR = N_TR
        self.N_BL = N_BL
        self.N_BR = N_BR
        

    def to_string(self):
        return "Square:: "+str(self.position)+" "+self.color \
                + " ;TL "+ (str(self.N_TL.position) if self.N_TL else "")\
                + " ;TR "+ (str(self.N_TR.position) if self.N_TR else "")\
                + " ;BL "+ (str(self.N_BL.position) if self.N_BL else "")\
                + " ;BR "+ (str(self.N_BR.position) if self.N_BR else "")
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
        return "Node:: "+str(self.position)\
                + " ;TL "+ (str(self.SQ_TL.position) if self.SQ_TL else "")\
                + " ;TR "+ (str(self.SQ_TR.position) if self.SQ_TR else "")\
                + " ;BL "+ (str(self.SQ_BL.position) if self.SQ_BL else "")\
                + " ;BR "+ (str(self.SQ_BR.position) if self.SQ_BR else "")
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
        #self.square_graph.print_me()
        
    
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
        def set_node(node, TL,TR,BL,BR):
            if TL:
                TL.N_BR = node
            if TR: 
                TR.N_BL = node
            if BL:
                BL.N_TR = node
            if BR:
                BR.N_TL = node
            
        for i in range(0,self.CR_ROWS,2):
            for j in range(0,self.CR_COLS,2):
                TL,TR,BL,BR = get_squares(i,j)
                #print(i,j,my_print(TL),my_print(TR),my_print(BL),my_print(BR))
                node = Node((int(i/2),int(j/2)), SQ_TL=TL, SQ_TR=TR, SQ_BL=BL, SQ_BR=BR, is_boundary_node=self.__is_boundary_node(i,j))
                set_node(node,TL,TR,BL,BR)
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
        #self.corner_graph.print_me()
    
    def build_graph(self,file_path=None, matrix=None):
        
        if not matrix:
            matrix = self.__read_file(file_path)
        
        self.CR_COLS = len(matrix[0])
        self.CR_ROWS = len(matrix)
        
        self.SQ_COLS = int(self.CR_COLS/2)
        self.SQ_ROWS = int(self.CR_ROWS/2)
        
        self.__build_square_graph(matrix)
        self.__build_corner_graph(matrix)
        
        self.square_graph.print_me()
        self.corner_graph.print_me()
    
    def build_random_graph(self, num_rows=5, num_cols=5, prob_broken_edges=0.001, prob_squares = [0.2, 0.2]):
        # prob_squares [Black, White]
        self.SQ_ROWS = num_rows
        self.SQ_COLS = num_cols
        
        self.CR_COLS = int(num_rows*2+1)
        self.CR_ROWS = int(num_cols*2+1)
        
        matrix = [['.']* self.CR_COLS for _ in range(self.CR_ROWS)]
        
        # start point
        
        def get_random_boundary_point():
            r=1
            
            while(r%2!=0):
                r = random.randint(0,self.CR_ROWS-1)
            c = 1
            while(c%2!=0):
                c = random.randint(0,self.CR_COLS-1)
            return r,c
        
        def set_start():
            r,c = get_random_boundary_point()
            first_row = random.randint(0,1)
            if first_row==1:
                r=0
            else:
                c=0
            matrix[r][c] = '*'
        
        def set_end():
            r,c = get_random_boundary_point()
            first_row = random.randint(0,1)
            if first_row==1:
                r=self.CR_ROWS-1
            else:
                c=self.CR_COLS-1
            matrix[r][c] = '#'
        
        
        set_start()
        set_end()
        
        # set broken edges
        
        for i in range(0,self.CR_ROWS,1):
            for j in range(0,self.CR_COLS,2):
                o = 1 if i%2==0 else 0
                
                prob = random.random()
                if prob <= prob_broken_edges:
                    if j+o < self.CR_COLS:
                        matrix[i][j+o]='~'
                
        # set squares color
        for i in range(1,self.CR_ROWS,2):
            for j in range(1,self.CR_COLS,2):
                prob = random.random()
                if prob<=prob_squares[0]:
                    matrix[i][j] = 'B'
                elif prob<=prob_squares[0]+prob_squares[1]:
                    matrix[i][j] = 'W'
                else:
                    matrix[i][j] = '.'
        
        for x in matrix:
            for y in x:
                print(y,end=" ")
            print("")
        self.build_graph(matrix=matrix)
        
    def save_to_file(self,file_name):
        self.print_board(file_name)
        
    
    def print_board(self, file_name=None):
        _str = ""
        for i in range(self.CR_ROWS):
            for j in range(self.CR_COLS):
                e = "" if j==self.CR_COLS-1 else " "
                p1 = (int(i/2), int(j/2))
                n1 = self.corner_graph.get_node(p1)
                            
                if i%2==0:
                    if j%2== 0:
                        if n1.is_start_node:
                            _str += "*"+e
                            
                        elif n1.is_target_node:
                            _str += "#"+e
                            
                        else:
                            _str += "."+e
                            
                    else:
                        if j != self.CR_COLS-1:
                            p2 = (int(i/2), int(j/2)+1)
                            
                            if self.corner_graph.is_edge(p1,p2):
                                _str += "."+e
                            else:
                                _str += "~"+e
                                
                else:
                    if j%2== 1:
                        if j!=self.CR_COLS-1:
                            #print(p1)
                            _str += n1.SQ_BR.color+e
                            
                    else:
                        if i!= self.CR_ROWS-1:
                            p2 = (int(i/2)+1, int(j/2))
                            
                            if self.corner_graph.is_edge(p1,p2):
                                _str += "."+e
                                
                            else:
                                _str += "~"+e
                                
            
            _str += "\n"
        if file_name:
            file = open(file_name,'w')
            file.write(_str)
        else:
            print(_str)

class PreprocessGraph(GraphBuilder):
    
    def __case_corner(g,i,j,ty):
        corner_sq=g.square_graph.get_square((i,j))
        corner_color=corner_sq.color
        print (corner_sq.to_string())
        
        if ty=='BL':
            adj_square1 = g.square_graph.get_square((i-1,j))
            adj_square2 = g.square_graph.get_square((i,j+1))
            color1 = adj_square1.color
            color2 = adj_square2.color
            if color1!='E' and color1!=corner_color and color1==color2:
                sq1 = g.square_graph.get_square((i-1,j+1))   
            
        if ty=='BR':
            adj_square1 = g.square_graph.get_square((i-1,j))
            adj_square2 = g.square_graph.get_square((i,j-1))
            color1 = adj_square1.color
            color2 = adj_square2.color
            if color1!='E' and color1!=corner_color and color1==color2:
                sq1 = g.square_graph.get_square((i-1,j-1))   
            
        if ty=='TL':
            adj_square1 = g.square_graph.get_square((i+1,j))
            adj_square2 = g.square_graph.get_square((i,j+1))
            color1 = adj_square1.color
            color2 = adj_square2.color
            if color1!='E' and color1!=corner_color and color1==color2:
                sq1 = g.square_graph.get_square((i+1,j+1))   
                
        if ty=='TR':
            adj_square1 = g.square_graph.get_square((i+1,j))
            adj_square2 = g.square_graph.get_square((i,j-1))
            color1 = adj_square1.color
            color2 = adj_square2.color
            if color1!='E' and color1!=corner_color and color1==color2:
                sq1 = g.square_graph.get_square((i+1,j-1))   
                
        g.square_graph.delete_edge(adj_square1,sq1)
        g.square_graph.delete_edge(adj_square2,sq1)
            
            
    def __vertical_same_color(g,i,j):
        prev_sq=g.square_graph.get_square((i,j))
        prev_color=prev_sq.color
    
        if prev_color!='E':
            for k in range(i+1,g.SQ_ROWS):
                curr_sq = g.square_graph.get_square((k,j))
                curr_color = curr_sq.color
                if curr_color==color and color!='E':
                    #delete_edge(curr_sq.top_edge)
                    g.square_graph.delete_edge(curr_sq,prev_sq)
                prev_color=curr_color
                
    def __horizontal_same_color(g,i,j):
        prev_sq=g.square_graph.get_square((i,j))
        prev_color=prev_sq.color
    
        if prev_color!='E':
            for k in range(j+1,g.SQ_COLS):
                curr_sq = g.square_graph.get_square((i,k))
                curr_color = curr_sq.color
                if curr_color==color and color!='E':
                    #delete_edge(curr_sq.left_edge)
                    g.square_graph.delete_edge(curr_sq,prev_sq)
                prev_color=curr_color
                
    def __middle_case(g,i,j):
        mid_sq=g.square_graph.get_square((i,j))
        mid_color=mid_sq.color
        sq_tp= g.square_graph.get_square((i-1,j))
        sq_lf= g.square_graph.get_square((i,j-1))
        sq_rt= g.square_graph.get_square((i,j+1))
        sq_bt= g.square_graph.get_square((i-1,j))
        
        #case-->   b
        #        b w b
        
        if mid_color!='E' and mid_color!=sq_lf.color and sq_lf.color==sq_rt.color and sq_lf.color==sq_tp.color:
            sq1=g.square_graph.get_square((i-1,j-1))
            sq2=g.square_graph.get_square((i-1,j+1))
            sq3=g.square_graph.get_square((i+1,j))
            #delete_edge(sq_lf.top_edge)
            g.square_graph.delete_edge(sq_lf,sq1)
            
            #delete_edge(sq_rt.top_edge)
            g.square_graph.delete_edge(sq_rt,sq2)
            
            #delete_edge(sq_tp.left_edge)
            g.square_graph.delete_edge(sq_tp,sq1)
            
            #delete_edge(sq_tp.right_edge)
            g.square_graph.delete_edge(sq_tp,sq2)
            
            #delete_edge(mid_sq.bottom_edge)
            g.square_graph.delete_edge(mid_sq,sq3)
        
        #case--> b w b
        #          b
        
        if mid_color!='E' and mid_color!=sq_lf.color and sq_lf.color==sq_rt.color and sq_lf.color==sq_bt.color:
            sq1=g.square_graph.get_square((i+1,j-1))
            sq2=g.square_graph.get_square((i+1,j+1))
            sq3=g.square_graph.get_square((i-1,j))
            
            #delete_edge(sq_lf.bottom_edge)
            g.square_graph.delete_edge(sq_lf,sq1)
            
            #delete_edge(sq_rt.bottom_edge)
            g.square_graph.delete_edge(sq_rt,sq2)
            
            #delete_edge(sq_bt.left_edge)
            g.square_graph.delete_edge(sq_bt,sq1)
            
            #delete_edge(sq_bt.right_edge)
            g.square_graph.delete_edge(sq_bt,sq2)
            
            #delete_edge(mid_sq.top_edge)
            g.square_graph.delete_edge(mid_sq,sq3)
        
    def preprocess(self,g):
        print(g.square_graph.map)
        #case: BL SQ
        i=g.SQ_ROWS-1
        j=0
        ty='BL'
        corner_color=g.square_graph.get_square((i,j)).color
        if corner_color!='E':
            self.__case_corner(i,j,ty)
        
        #case: BR SQ
        i=g.SQ_ROWS-1
        j=g.SQ_COLS-1
        ty='BR'
        corner_color=g.square_graph.get_square((i,j)).color
        if corner_color!='E':
            self-__case_corner(g,i,j,ty)
            
        #case: TL SQ
        i=0
        j=0
        ty='TL'
        corner_color=g.square_graph.get_square((i,j)).color
        if corner_color!='E':
            self.__case_corner(g,i,j,ty)
        
        #case: TR SQ
        i=0
        j=g.SQ_COLS-1
        ty='TR'
        corner_color=g.square_graph.get_square((i,j)).color
        if corner_color!='E':
            self.__case_corner(g,i,j,ty)
            
        for col in range(0,g.SQ_COLS):
            self.__vertical_same_color(g,0,col)
            
        for row in range(0,g.SQ_ROWS):
            self.__horizontal_same_color(g,row,0)
            
        for i in range(1,g.SQ_ROWS-1):
            for j in range(1,g.SQ_COLS-1):
                self.__middle_case(g,i,j)

g = GraphBuilder()
g.build_graph(file_path="board_3x3_1.txt")
#g.print_board()
#g.build_random_graph(prob_broken_edges=0.01)
#g.save_to_file("board_5x5_random.txt")
