import taufactor as tau
import tifffile
import torch

# load image
img = tifffile.imread("C:/Users/MTP24ME/Pictures/Cal_and_uncal_2_NREL/Labelled/nmc-2-uncal-blackisporepluscbd_inverted.tif")
# ensure 1s for conductive phase and 0s otherwise.

# create a solver object with loaded image
s = tau.Solver(img, device = torch.device('cpu'))

# call solve function
s.solve()

# view effective diffusivity and tau
print(s.D_eff, s.tau)