import cv2
import numpy as np
import random
import math

# Create a black canvas
image = np.zeros((500, 500, 3), dtype=np.uint8)

# Polygon center and size
center_x, center_y = 250, 250
radius = 100
num_points = 50  # Number of polygon vertices

# Generate random angles and radii for an irregular shape
points = []
for i in range(num_points):
    angle = 2 * math.pi * i / num_points
    # Add some random noise to radius for irregularity
    r = radius + random.randint(-30, 30)
    x = int(center_x + r * math.cos(angle))
    y = int(center_y + r * math.sin(angle))
    points.append([x, y])

# Convert to OpenCV format
pts = np.array(points, dtype=np.int32).reshape((-1, 1, 2))

# Draw the closed polygon
cv2.polylines(image, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

# Optionally fill the polygon
cv2.fillPoly(image, [pts], color=(0, 100, 255))  # comment this line to skip fill

# Show the result
cv2.imshow("Random Closed Polygon", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
