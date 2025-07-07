def convert_zone_json_to_array(zone_json: dict) -> list[int]:
    '''
    converts a zone's data to array -> [shape_type, center_x, center_y, dimension1, dimension2]
    shape_type -> 0 in case of circle and 1 in case of rectangle
    dimension1 -> length in case of rectangle and radius in case of circle
    dimension2 -> width in case of rectangle and 0 in case of circle
    '''
    shape = zone_json["shape"]
    shape_type = shape.get("type")

    center = shape.get("centre", [0, 0])
    x, y = center[0], center[1]

    if shape_type == 0:  # circle
        radius = shape.get("radius", 0)
        return [0, x, y, radius, 0]

    elif shape_type == 1:  # rectangle
        height = shape.get("height", 0)
        width = shape.get("width", 0)
        return [1, x, y, height, width]

    else:
        raise ValueError("Unsupported shape type")