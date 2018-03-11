from sets import Set
def check_connect_components(square_graph):
    is_visited = Set()
    for square in square_graph:
        if square not in is_visited:
            if not is_same_color(square_graph, square, square.color, is_visited):
                return False
    return True


def is_same_color(square_graph, s, color, is_visited):
    is_visited.add(s)
    if len(square_graph[s]) == 0:
        return True
    for nei in square_graph[s]:
        if nei.color is None or nei.color == color:
            if not is_same_color(square_graph, nei, color, is_visited):
                return False
        else:
            return False
    return True