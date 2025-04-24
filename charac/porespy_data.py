import porespy as ps
import matplotlib.pyplot as plt
import tifffile


img1 = tifffile.imread('G:/My Drive/PHD/MatBox_seg/nmc_1_seg_dragon (Converted).tiff')

print(ps.metrics.phase_fraction(img1))
print(ps.metrics.pore_size_distribution(img1))

plt.imshow(img1)
plt.show() 