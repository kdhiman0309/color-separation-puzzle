

def direction(node1,node2):
	dx = node2[0] - node1[0]
	dy = node2[1] - node1[1]

	if (dx == 1):
		return 'RIGHT'
	if (dx == -1):
		return 'LEFT'
	if (dy == 1):
		return 'UP'
	if (dy == -1):
		return 'DOWN'

def get_squares(node,d):
	if(d == 'UP'):
		return node.TL, node.TR
	if(d == 'DOWN'):
		return node.BL, node.BR
	if(d == 'LEFT'):
		return node.BL, node.TL
	if(d == 'RIGHT'):
		return node.BR, node.TR

def solve_brute_force(node, path, S1_prev, S2_prev):
	if (node.is_visited == true):
		return false

	node.is_visited = true

	i,j = node.position
	BL = node.BL
	BR = node.BR
	TL = node.TL
	TR = node.TR

	if node.is_boundary_node: 
		same_color = check_connect_components(S1_prev,S2_prev)
		if (!same_color):
			return false

	neighbours = corner_graph.get_neighbours(node)
	n = nei.size
	for i in range (0,n):
		nei = neighbours[i]
		path.append(nei)
		d = direction(node,nei)
		S1,S2 = get_squares(node,d)
		square_graph.delete_edge(S1,S2)
		if solve_brute_force(nei,path,S1,S2):
			return true
		square_graph.add_edge(S1,S2) 
		path.pop()

	node.is_visited = false

	return false
