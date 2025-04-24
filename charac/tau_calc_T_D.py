import taufactor as tau
import tifffile
import torch

# load image
img1 = tifffile.imread('G:/My Drive/PHD/MatBox_seg/nmc_1_seg_dragon (Converted).tiff')
img2 = tifffile.imread('G:/My Drive/PHD/MatBox_seg/nmc-1-cropped-Gauss/WF1_Workflow1/S2_Global thresholding (Linear). 2 phases.tif')
img3 = tifffile.imread('G:/My Drive/PHD/MatBox_seg/nmc-1-cropped-Gauss/WF1_Workflow1/S2_Global thresholding (Fit to reach volume fractions). 2 phases.tif')
img4 = tifffile.imread('G:/My Drive/PHD/MatBox_seg/nmc-1-cropped-Gauss/WF2_Workflow2/S2_Global thresholding (Otsu). 2 phases.tif')


# ensure 1s for conductive phase and 0s otherwise.

# create a solver object with loaded image
s1 = tau.Solver(img1)
s2 = tau.Solver(img2)
s3 = tau.Solver(img3)
s4 = tau.Solver(img4)

# call solve function
s1.solve()
s2.solve()
s3.solve()
s4.solve()

# view effective diffusivity and tau
print("Dragonfly_data:")

print(s1.D_eff, s1.tau)
print("Effective diffusivity:", abs(s1.D_eff.item()))
print("Tortuosity:", s1.tau.item())

print("MATBOX_data_Linear:")

print(s2.D_eff, s2.tau)
print("Effective diffusivity:", abs(s2.D_eff.item()))
print("Tortuosity:", s2.tau.item())

print("MATBOX_data_Fit to reach volume fractions:")

print(s3.D_eff, s3.tau)
print("Effective diffusivity:", abs(s3.D_eff.item()))
print("Tortuosity:", s3.tau.item())

print("MATBOX_data_Otsu:")

print(s4.D_eff, s4.tau)
print("Effective diffusivity:", abs(s4.D_eff.item()))
print("Tortuosity:", s4.tau.item())