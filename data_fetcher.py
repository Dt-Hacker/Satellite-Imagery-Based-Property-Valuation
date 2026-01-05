# =====================================================
# DATA_FETCHER.py
# =====================================================
import os
import math
import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm

# =====================================================
# OUTPUT DIRECTORIES (I am working on kaggle)
# =====================================================
TRAIN_IMG_DIR = "/kaggle/working/images/train"
TEST_IMG_DIR  = "/kaggle/working/images/test"

os.makedirs(TRAIN_IMG_DIR, exist_ok=True)
os.makedirs(TEST_IMG_DIR, exist_ok=True)

# ======================================================
# ESRI WORLD IMAGERY ENDPOINT
# ======================================================
ESRI_URL = "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export"

# ======================================================
# IMAGE PARAMETERS
# ======================================================
IMG_SIZE = 256          # Output image size: 256x256
AREA_METERS = 200       # Area around property (200m x 200m)

# ======================================================
# BASIC GEO HELPERS
# ======================================================
def meters_to_lat(meters):
    return meters / 111320

def meters_to_lon(meters, lat):
    return meters / (111320 * math.cos(math.radians(lat)))

def get_bbox(lat, lon, meters):
    dlat = meters_to_lat(meters)
    dlon = meters_to_lon(meters, lat)
    return (
        lon - dlon / 2,
        lat - dlat / 2,
        lon + dlon / 2,
        lat + dlat / 2
    )

# ======================================================
# IMAGE FETCH FUNCTION (Without keeping any delay)
# ======================================================
def fetch_esri_image(lat, lon, save_path, retries=3):
    bbox = get_bbox(lat, lon, AREA_METERS)

    params = {
        "bbox": ",".join(map(str, bbox)),
        "bboxSR": 4326,
        "imageSR": 4326,
        "size": f"{IMG_SIZE},{IMG_SIZE}",
        "format": "png",
        "f": "image"
    }

    for _ in range(retries):
        try:
            response = requests.get(
                ESRI_URL,
                params=params,
                timeout=20
            )

            if response.status_code == 200:
                img = Image.open(BytesIO(response.content)).convert("RGB")
                img.save(save_path)
                return True

        except requests.exceptions.ReadTimeout:
            continue
        except Exception:
            continue

    return False

# ======================================================
# DOWNLOAD TRAIN IMAGES
# ======================================================
print("Downloading TRAIN satellite images...")

train_success = 0
train_fail = 0

for idx, row in tqdm(train_df.iterrows(), total=len(train_df)):
    img_path = f"{TRAIN_IMG_DIR}/{idx}.png"

    if os.path.exists(img_path):
        continue

    if fetch_esri_image(row["lat"], row["long"], img_path):
        train_success += 1
    else:
        train_fail += 1

print(f"TRAIN images downloaded: {train_success}")
print(f"TRAIN images failed    : {train_fail}")

# ======================================================
# DOWNLOAD TEST IMAGES
# ======================================================
print("Downloading TEST satellite images...")

test_success = 0
test_fail = 0

for idx, row in tqdm(test_df.iterrows(), total=len(test_df)):
    img_path = f"{TEST_IMG_DIR}/{idx}.png"

    if os.path.exists(img_path):
        continue

    if fetch_esri_image(row["lat"], row["long"], img_path):
        test_success += 1
    else:
        test_fail += 1

print(f"TEST images downloaded: {test_success}")
print(f"TEST images failed    : {test_fail}")

print("Satellite image acquisition completed.")
