import tifffile
import numpy as np

# Load the image
img1 = tifffile.imread("C:/Users/meize/Videos/XCT_DATA/cropped/Classified image_2.tiff")

def volume_fraction(tiff_img):
    print("Unique labels in image:", np.unique(tiff_img))
    active_voxels = np.sum(tiff_img == 1)
    total_voxels = tiff_img.size

    phase_fraction = active_voxels / total_voxels
    print("Volume fraction of active material:", phase_fraction)

    labels, counts = np.unique(tiff_img, return_counts=True)
    total_voxels = tiff_img.size

    for label, count in zip(labels, counts):
        frac = count / total_voxels
        print(f"Phase {label}: {frac:.4f}")
        
volume_fraction(img1)

