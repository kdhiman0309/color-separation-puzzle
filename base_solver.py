class BaseSolver():
    
    def direction(self,node1,node2):
        # node1 -> node2
        # 1,1  -> 0,1
        dr = node2.position[0] - node1.position[0]    
        dc = node2.position[1] - node1.position[1]

        if (dr == 1):
            return 'DOWN'
        if (dr == -1):
            return 'UP'
        if (dc == 1):
            return 'RIGHT'
        if (dc == -1):
            return 'LEFT'

    def get_squares(self,node,d):
        if(d == 'UP'):
            return node.SQ_TL, node.SQ_TR
        if(d == 'DOWN'):
            return node.SQ_BL, node.SQ_BR
        if(d == 'LEFT'):
            return node.SQ_BL, node.SQ_TL
        if(d == 'RIGHT'):
            return node.SQ_BR, node.SQ_TR