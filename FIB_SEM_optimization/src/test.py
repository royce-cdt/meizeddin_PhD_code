import metrics
import tifffile
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parents[2]
IMAGE_DIR = BASE_DIR / "FIB_SEM_optimization" / "images"
image_path = IMAGE_DIR / "CBS_Fresh_LFP_33.tif"


image = tifffile.imread(image_path)

# convert to float 0-1

image = image.astype(float)

image = (
    image - image.min()
) / (
    image.max() - image.min()
)


print("Mean:", metrics.mean_intensity(image))

print("Contrast:",
      metrics.rms_contrast(image))

print("Entropy:",
      metrics.entropy(image))

print("Sharpness:",
      metrics.laplacian_variance(image))

print("Tenengrad:",
      metrics.tenengrad(image))

print("Gradient:",
      metrics.mean_gradient(image))

print("SNR:",
      metrics.estimate_snr(image))