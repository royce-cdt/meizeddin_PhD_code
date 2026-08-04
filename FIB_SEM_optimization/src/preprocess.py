# File name parser
from pathlib import Path

def parse_filename(filename):
    name = Path(filename).stem
    parts = name.split("_")

    detector = parts[0]
    sample_state = parts[1]
    material = parts[2]
    image_id = int(parts[3])

    return {
        "sample_state": sample_state,
        "material": material,
        "image_id": image_id
    }

#import images
import tifffile

def load_image(path):
    image = tifffile.imread(path)

    if image is None:
        raise ValueError(f"Cannot read {path}")

    return image

#Normalising

import numpy as np

import numpy as np

def normalize(image, p_low=1.0, p_high=99.0, eps=1e-8):
    """
    Normalizes an SEM/FIB image to [0, 1] using percentile clipping.
    Prevents charging spots and detector noise floor from distorting the contrast.
    """
    # 1. Cast to float32 without modifying original array in-place
    img_float = image.astype(np.float32)
    
    # 2. Determine robust bounds ignoring extreme 1% outliers
    vmin = np.percentile(img_float, p_low)
    vmax = np.percentile(img_float, p_high)
    
    # 3. Clip extreme outliers (e.g. charging artifacts or deep shadows)
    img_clipped = np.clip(img_float, vmin, vmax)
    
    # 4. Scale to [0, 1] safely (eps prevents division by zero)
    denom = max(vmax - vmin, eps)
    normalized = (img_clipped - vmin) / denom
    
    return normalized

def crop_sem_overlay(image, top=0, bottom=0, left=0, right=0):
    """
    Crop SEM image to remove scale bars and metadata overlays.

    Works for both:
    - grayscale images: (height, width)
    - RGB images: (height, width, channels)
    """

    if image.ndim == 2:
        # grayscale
        cropped = image[
            top:image.shape[0]-bottom,
            left:image.shape[1]-right
        ]

    elif image.ndim == 3:
        # RGB / multi-channel
        cropped = image[
            top:image.shape[0]-bottom,
            left:image.shape[1]-right,
            :
        ]

    else:
        raise ValueError(
            f"Unexpected image dimensions: {image.shape}"
        )

    return cropped