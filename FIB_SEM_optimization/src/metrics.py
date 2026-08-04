import numpy as np
import cv2

from scipy.ndimage import sobel, gaussian_filter
from skimage.measure import shannon_entropy


# -------------------------------------------------------
# Basic intensity metrics
# -------------------------------------------------------

def mean_intensity(image):
    """
    Mean pixel intensity.
    
    Useful for checking exposure consistency.
    """
    return np.mean(image)



def standard_deviation(image):
    """
    Global intensity variation.
    
    Related to contrast, but includes noise.
    """
    return np.std(image)



def rms_contrast(image):
    """
    Root Mean Square contrast.

    Higher values indicate stronger intensity differences.
    """
    image = image.astype(np.float64)

    mean = np.mean(image)

    return np.sqrt(
        np.mean((image - mean) ** 2)
    )



# -------------------------------------------------------
# Information content
# -------------------------------------------------------

def entropy(image):
    """
    Shannon entropy.

    Measures intensity distribution complexity.
    """

    return shannon_entropy(image)



# -------------------------------------------------------
# Sharpness metrics
# -------------------------------------------------------

def laplacian_variance(image):
    """
    Variance of Laplacian.

    Common microscopy sharpness metric.

    Higher = sharper edges.
    """

    lap = cv2.Laplacian(
        image.astype(np.float64),
        cv2.CV_64F
    )

    return lap.var()



def tenengrad(image):
    """
    Tenengrad focus measure.

    Based on Sobel gradient energy.

    More directly related to edge quality.
    """

    image = image.astype(np.float64)

    gx = sobel(image, axis=0)
    gy = sobel(image, axis=1)

    gradient_squared = gx**2 + gy**2

    return np.mean(gradient_squared)



# -------------------------------------------------------
# Edge strength
# -------------------------------------------------------

def mean_gradient(image):
    """
    Average Sobel gradient magnitude.

    Measures boundary strength.
    """

    image = image.astype(np.float64)

    gx = sobel(image, axis=0)
    gy = sobel(image, axis=1)

    magnitude = np.sqrt(
        gx**2 + gy**2
    )

    return np.mean(magnitude)



# -------------------------------------------------------
# Noise and SNR
# -------------------------------------------------------

def estimate_noise(image, sigma=2):
    """
    Estimate noise by subtracting
    a Gaussian-smoothed image.

    Noise = high-frequency component.
    """

    image = image.astype(np.float64)

    smooth = gaussian_filter(
        image,
        sigma=sigma
    )

    noise = image - smooth

    return np.std(noise)



def estimate_snr(image, sigma=2):
    """
    Estimated signal-to-noise ratio.

    Signal estimated from mean intensity.
    Noise estimated from high-frequency residual.
    """

    image = image.astype(np.float64)

    smooth = gaussian_filter(
        image,
        sigma=sigma
    )

    noise = image - smooth

    noise_std = np.std(noise)

    signal = np.mean(smooth)


    if noise_std == 0:
        return np.inf


    return signal / noise_std