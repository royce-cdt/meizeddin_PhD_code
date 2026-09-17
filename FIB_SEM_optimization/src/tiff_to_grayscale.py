# importing required libraries, Image library from PIL is used to read and write image files.
import tifffile
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    BASE_DIR
    / "FIB_SEM_optimization"
    / "images"
    / "cropped"
    / "Param_7"
)

input_folder = INPUT_PATH
output_folder = INPUT_PATH / "param_7_grayscale"

# Create the output folder if it doesn't exist, with any parent directories as needed.
output_folder.mkdir(parents=True, exist_ok=True)

# Loop through all .tif and .tiff files in the input folder, convert them to grayscale, and save them in the output folder.
for file in list(input_folder.glob("*.tif")) + list(input_folder.glob("*.tiff")):
    img = tifffile.imread(file)
    print("Original shape:", img.shape)

    # Convert RGB → grayscale, L means 8-bit pixels, black and white.
    gray = np.mean(img, axis=2)

    print("Grayscale shape:", gray.shape)

    output_file = output_folder / file.name
    tifffile.imwrite(output_file, gray)

    print(f"Converted: {file.name}")