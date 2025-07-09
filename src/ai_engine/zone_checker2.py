from shapely.geometry import Polygon, box

def calculate_overlap(bbox, polygon_points):
    """
    Calculates Intersection-over-Area (IoA) between a bounding box and a polygon zone.

    Args:
        bbox (list): [x1, y1, x2, y2] bounding box coordinates
        polygon_points (list of tuples): [(x, y), (x, y), ...] polygon

    Returns:
        float: overlap ratio (0 to 1)
    """
    bbox_poly = box(*bbox)
    zone_poly = Polygon(polygon_points)

    if not zone_poly.is_valid or zone_poly.is_empty:
        return 0

    intersection_area = bbox_poly.intersection(zone_poly).area
    bbox_area = bbox_poly.area

    if bbox_area == 0:
        return 0

    return intersection_area / bbox_area
