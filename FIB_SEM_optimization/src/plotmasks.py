from pathlib import Path
import tifffile
import matplotlib.pyplot as plt
import math


BASE_DIR = Path(__file__).resolve().parents[2]

MASK_DIR = BASE_DIR / "FIB_SEM_optimization" / "images" / "segmented_masks"


mask_files = sorted(
    MASK_DIR.glob("*_mask.tif")
)


# Number of images
n_images = len(mask_files)

# Grid size
cols = 4
rows = math.ceil(n_images / cols)


fig, axes = plt.subplots(
    rows,
    cols,
    figsize=(12, 3 * rows)
)


# Handle case of only one row
axes = axes.flatten()


for ax, mask_path in zip(axes, mask_files):

    mask = tifffile.imread(
        mask_path
    )

    ax.imshow(
        mask,
        cmap="gray"
    )

    ax.set_title(
        mask_path.stem.replace("_mask", ""),
        fontsize=8
    )

    ax.axis("off")


# Remove empty plots
for ax in axes[n_images:]:
    ax.axis("off")


plt.tight_layout()
plt.show()