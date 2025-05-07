import taufactor as tau
import tifffile
import torch
from tabulate import tabulate
from taufactor.utils import flux_direction
import numpy as np
import os


def calc_tortuosity(img_path, data_name, flux_drection = 'y'):
# load image
    img_raw = tifffile.imread(img_path)
    results = []
    print("Flux direction analysis:", flux_direction(img_raw))
    # ensure 1s for conductive phase and 0s otherwise.
    permutations = {
        'y': lambda x: x,
        'x': lambda x: torch.permute(torch.tensor(x), (1, 2, 0)).numpy(),
        'z': lambda x: torch.permute(torch.tensor(x), (2, 0, 1)).numpy()
    }
    directions = ['y', 'x' ,'z'] if flux_drection == 'all' else [flux_drection]
    for direction in directions:
        img = permutations[direction](img_raw)
        s = tau.Solver(img)
        s.solve()
        results.append([data_name, direction, f"{s.D_eff.item():.6f}", f"{s.tau.item():.6f}"])
    # prepare and print the results as a table
    headers = ["Data", "Flux Direction", "Effective Diffusivity", "Tortuosity"]
    print(tabulate(results, headers=headers, tablefmt="grid"))
    
def invert_conductive_phase(img_path):
    # Load the TIFF image
    img = tifffile.imread(img_path)

    # Check it's binary (contains only 0s and 1s)
    assert np.array_equal(np.unique(img), [0, 1]), "Image must be binary"

    # Invert the image: 0 → 1, 1 → 0
    inverted = 1 - img    
    # Create output path: same folder, modified filename
    dir_name, base_name = os.path.split(img_path)
    name, ext = os.path.splitext(base_name)
    output_name = f"{name}_inverted{ext}"
    output_path = os.path.join(dir_name, output_name)

    tifffile.imwrite(output_path, inverted.astype(np.uint8))
    print(f"Saved inverted image to: {output_path}")
    
#invert_conductive_phase("G:/Other computers/My laptop/Documents/SEG_DATA_UNCAL/Tiff/AI_2_3refslice (Converted).tiff")
#invert_conductive_phase("C:/Users/meize/Videos/XCT_DATA/New_dataset/nmc-2-uncal-blackisporepluscbd.tif")

calc_tortuosity("G:/Other computers/My laptop/Documents/SEG_DATA_UNCAL/Tiff/AI_2_3refslice (Converted)_inverted.tiff", "Ucal AI Drag", "all")
#calc_tortuosity("G:/Other computers/My laptop/Documents/SEG_DATA_UNCAL/Tiff/AI_2_3refslices_7spaces (Converted)_inverted.tiff", "Uncal AI Drag", "all")