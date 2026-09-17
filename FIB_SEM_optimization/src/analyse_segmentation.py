from pathlib import Path
import re

import tifffile
import pandas as pd

from segmentation_metrics import evaluate_segmentation, save_overlay


BASE_DIR = Path(__file__).resolve().parents[2]

IMAGE_DIR = (
    BASE_DIR
    / "FIB_SEM_optimization"
    / "images"
    / "cropped"
    / "Param_7"
    / "Param_7_grayscale"
)

MASK_DIR = (
    BASE_DIR
    / "FIB_SEM_optimization"
    / "images"
    / "segmented_masks"
    / "Param_7"
)

RESULT_DIR = (
    BASE_DIR
    / "FIB_SEM_optimization"
    / "results"
    / "Param_7"
)


# Create output folders
MASK_DIR.mkdir(
    parents=True,
    exist_ok=True
)

RESULT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def parse_filename(filename):
    """
    Parse filename format:

    Detector_State_Material_ImageID.tif

    Example:
    ETD_Fresh_LFP_57.tif

    Returns:
    detector
    state
    material
    image_id
    """

    name = filename.stem

    match = re.match(
        r"(.+?)_(Fresh|Cycled)_(.+?)_(\d+)$",
        name
    )

    if match is None:
        raise ValueError(
            f"Filename format not recognised: {filename}"
        )

    detector = match.group(1)

    state = match.group(2)

    material = match.group(3)

    image_id = int(
        match.group(4)
    )

    return detector, state, material, image_id



results = []


for image_path in IMAGE_DIR.glob("*.tif"):

    print(f"Processing {image_path.name}")


    # Extract metadata from filename
    detector, state, material, image_id = parse_filename(
        image_path
    )


    # Load FIB-SEM image
    image = tifffile.imread(
        image_path
    )


    # Run segmentation
    metrics, mask = evaluate_segmentation(
        image
    )


    # Add metadata
    metrics["detector"] = detector
    metrics["sample_state"] = state
    metrics["material"] = material
    metrics["image_id"] = image_id


    results.append(metrics)


    # Save segmented mask
    mask_path = (
        MASK_DIR
        / f"{image_path.stem}_mask.tif"
    )

    tifffile.imwrite(
        mask_path,
        mask.astype("uint8")
    )


    # Save overlay image
    overlay_path = (
        MASK_DIR
        / f"{image_path.stem}_overlay.png"
    )

    save_overlay(
        image,
        mask,
        overlay_path
    )



# Convert results to dataframe
seg_results = pd.DataFrame(results)


# Save CSV
output_file = (
    RESULT_DIR
    / "segmentation_quality_param_7.csv"
)

seg_results.to_csv(
    output_file,
    index=False
)


print("\nSegmentation complete")
print(f"Masks saved to: {MASK_DIR}")
print(f"Results saved to: {output_file}")


seg_results