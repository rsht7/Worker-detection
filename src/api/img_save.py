import os
import random
import string

STATIC_IMAGE_DIR = os.path.join(os.path.dirname(__file__), "./static/images")


def generate_random_suffix(length: int = 6) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def save_alert_image(camera_id: int, ts: str, image_bytes: bytes) -> str:
    timestamp = ts
    rand_suffix = generate_random_suffix()
    filename = f"camera_{camera_id}_{timestamp}_{rand_suffix}.jpg"
    path = os.path.join(STATIC_IMAGE_DIR, filename)

    with open(path, "wb") as f:
        f.write(image_bytes)

    # Return relative URL path for frontend use
    return f"/images/{filename}"
