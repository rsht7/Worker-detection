# scripts/zone_checker.py

def calculate_overlap(bbox, zone_rect):
    """
    Calculate Intersection over Area (IoA) of bbox with zone.
    bbox: [x1, y1, x2, y2]
    zone_rect: [zx1, zy1, zx2, zy2]
    Returns: float (overlap ratio 0 to 1)
    """
    x1, y1, x2, y2 = bbox
    zx1, zy1, zx2, zy2 = zone_rect

    # Intersection rectangle
    ix1 = max(x1, zx1)
    iy1 = max(y1, zy1)
    ix2 = min(x2, zx2)
    iy2 = min(y2, zy2)

    iw = max(0, ix2 - ix1)
    ih = max(0, iy2 - iy1)

    intersection_area = iw * ih
    bbox_area = (x2 - x1) * (y2 - y1)

    if bbox_area == 0:
        return 0

    return intersection_area / bbox_area  # IoA
