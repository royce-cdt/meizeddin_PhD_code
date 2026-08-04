import numpy as np
from skimage.filters import threshold_otsu
from skimage.measure import label, regionprops
from skimage.morphology import remove_small_objects, closing, disk
from skimage.filters import gaussian
import matplotlib.pyplot as plt


def save_overlay(image, mask, output_path):

    plt.figure(figsize=(8,8))

    plt.imshow(
        image,
        cmap="gray"
    )

    plt.imshow(
        mask,
        cmap="jet",
        alpha=0.35
    )

    plt.axis("off")

    plt.savefig(
        output_path,
        bbox_inches="tight",
        dpi=300
    )

    plt.close()


def preprocess_image(image):
    """
    Normalize and smooth image before segmentation
    """

    # Normalize 0-1
    image = image.astype(np.float32)
    image = (image - image.min()) / (image.max() - image.min())

    # Reduce SEM noise
    image = gaussian(image, sigma=1)

    return image



def otsu_segmentation(image):
    """
    Automatic threshold segmentation
    """

    threshold = threshold_otsu(image)

    mask = image > threshold

    # Remove small noise
    mask = remove_small_objects(
        mask,
        max_size=20
    )

    # Close small gaps
    mask = closing(
        mask,
        footprint=disk(2)
    )

    return mask, threshold



def segmentation_fraction(mask):
    """
    Fraction of segmented pixels
    """

    return np.mean(mask)



def connected_components(mask):
    """
    Number of segmented regions
    """

    labelled = label(mask)

    return labelled.max()



def particle_statistics(mask):
    """
    Extract segmented feature sizes
    """

    labelled = label(mask)

    regions = regionprops(labelled)

    areas = [
        r.area
        for r in regions
    ]

    if len(areas) == 0:
        return 0, 0

    return (
        np.mean(areas),
        np.median(areas)
    )



def intensity_separability(image, mask):
    """
    Fisher discriminant ratio:
    how separated are the two intensity classes
    """

    phase1 = image[mask]
    phase2 = image[~mask]

    mu1 = np.mean(phase1)
    mu2 = np.mean(phase2)

    var1 = np.var(phase1)
    var2 = np.var(phase2)


    score = abs(mu1-mu2) / np.sqrt(
        var1 + var2
    )

    return score



def threshold_stability(image, steps=10):
    """
    Tests how sensitive segmentation is to threshold changes
    """

    otsu = threshold_otsu(image)

    fractions = []

    for factor in np.linspace(
        0.8,
        1.2,
        steps
    ):

        threshold = otsu * factor

        mask = image > threshold

        fractions.append(
            np.mean(mask)
        )


    return np.std(fractions)



def evaluate_segmentation(image):

    image = preprocess_image(image)

    mask, threshold = otsu_segmentation(image)


    results = {

        "threshold": threshold,

        "segmented_fraction":
            segmentation_fraction(mask),

        "connected_components":
            connected_components(mask),

        "mean_region_area":
            particle_statistics(mask)[0],

        "median_region_area":
            particle_statistics(mask)[1],

        "separability":
            intensity_separability(
                image,
                mask
            ),

        "threshold_instability":
            threshold_stability(image)

    }


    return results, mask