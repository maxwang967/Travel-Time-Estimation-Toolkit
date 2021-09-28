def extract_cpath(cpath):
    """
    Convert link path from String to List<Int>
    """
    if (isinstance(cpath, float)):
        return []
    if (cpath == ''):
        return []
    return [int(s) for s in cpath.split(',')]


def extract_list_of_points_for_matched_edges(mgeom):
    """
    Convert geometry to list of points for matched edegs
    """
    line_str = mgeom.replace("LINESTRING (", "[(").replace(")", ")]").replace(", ", "),(").replace(" ", ",")
    points = eval(line_str)
    if len(points[0]) == 0:
        return []
    points = list(map(lambda x: [x[1], x[0]], points))
    return points


def extract_list_of_points_for_mr(mgeom):
    """
    Convert geometry to list of points for matched routes
    """
    line_str = mgeom.replace("LINESTRING(", "[(").replace(")", ")]").replace(",", "),(").replace(" ", ",")
    points = eval(line_str)
    if len(points[0]) == 0:
        return []
    points = list(map(lambda x: [x[1], x[0]], points))
    return points