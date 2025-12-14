import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import skimage.filters as ski
from PIL import Image
from scipy import ndimage

import imageio
def clean_binary_mask(path):
    img = Image.open(path)
    arr = np.asarray(img)
    gaussian = ski.gaussian(arr, sigma = 5)
    filtered = (gaussian > 0.7).astype(np.uint8)
    label, _ = ndimage.label(filtered)
    counts = np.bincount(label.ravel())
    keep = counts >= 1000
    keep[0] = False
    return keep[label]

def return_blurred(img):
    arr = np.asarray(img)
    gaussian = ski.gaussian(arr, sigma = 5)
    imageio.imwrite("test1.tif",gaussian)


def filter_all_scripture(scripture_folder_str, save_folder_str):
    scripture_folder = Path(scripture_folder_str)
    save_folder = Path(save_folder_str)
    for file in scripture_folder.iterdir():
        if Path(save_folder / f"{file.stem}_gaussian{file.suffix}").exists():
            pass
        else:
            filtered = clean_binary_mask(file.resolve())
            mask = (filtered * 255).astype(np.uint8)                                                                
            imageio.imwrite(save_folder / f"{file.stem}_gaussian{file.suffix}", mask)