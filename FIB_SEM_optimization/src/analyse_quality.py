from pathlib import Path
import pandas as pd

from preprocess import load_image, parse_filename, normalize, crop_sem_overlay
import metrics, tifffile

BASE_DIR = Path(__file__).resolve().parents[2]
IMAGE_DIR = BASE_DIR / "FIB_SEM_optimization" / "images" / "raw"
metadata = pd.read_csv(BASE_DIR / "FIB_SEM_optimization" / "FIB_SEM_Opt_datasets.csv")

cropped_dir = BASE_DIR / "FIB_SEM_optimization" / "images" / "cropped"
cropped_dir.mkdir(exist_ok=True)

# Check if previous outputs exist
existing_cropped = list(cropped_dir.glob("*.tif"))

overwrite = False

if existing_cropped:
    answer = input(
        "Existing cropped images found. Overwrite? (y/n): "
    )

    overwrite = answer.lower() == "y"

results = []


for image_file in IMAGE_DIR.glob("*.tif"):

    info = parse_filename(image_file.name)

    image = load_image(image_file)
    print(image.shape)

    image = crop_sem_overlay(image, 0, 84)

    cropped_path = cropped_dir / image_file.name

    if overwrite or not cropped_path.exists():

        tifffile.imwrite(
            cropped_path,
            image.astype("uint16")
        )

    #image = normalize(image)


    quality = {

        **info,

        "Mean":
        image.mean(),

        "RMS_Contrast":
        metrics.rms_contrast(image),

        "Entropy":
        metrics.entropy(image),

        "Sharpness":
        metrics.laplacian_variance(image),

        "Gradient":
        metrics.mean_gradient(image),

        "SNR":
        metrics.estimate_snr(image)
    }


    results.append(quality)



results = pd.DataFrame(results)


results = results.merge(
    metadata,
    on="image_id",
    how="left"
)

results = results.sort_values(by="image_id")


results.to_csv(
    BASE_DIR/ "FIB_SEM_optimization" /"results"/"image_quality_results.csv",
    index=False
)


print(results.head())