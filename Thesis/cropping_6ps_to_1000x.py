import imagej
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import tifffile as tiff

# initialize ImageJ
ij = imagej.init('sc.fiji:fiji:2.14.0') 
print(f"ImageJ version: {ij.getVersion()}")

def crop_100x_to_1000x(tif):
    original = np.asarray(ij.py.from_java(tif))

    rows = original.shape[0]
    cutoff = int(rows * 0.934)  
    scalebar_free = original[:cutoff, :] #Crop the scalebar away

    lst = []

    new_length = int(np.shape(scalebar_free)[1] / 10)
    new_height = int(np.shape(scalebar_free)[0] / 10)

    for i in range(10):
        for j in range(10):
            lst.append(scalebar_free[i*new_height:new_height*(i+1), j*new_length:new_length*(j+1)])

    return lst

def crop_250x_to_1000x(tif):
    original = np.asarray(ij.py.from_java(tif))

    rows = original.shape[0]
    cutoff = int(rows * 0.934)  
    scalebar_free = original[:cutoff, :] #Crop the scalebar away

    lst = []

    new_length = int(np.shape(scalebar_free)[1] / 4)
    new_height = int(np.shape(scalebar_free)[0] / 4)

    for i in range(4):
        for j in range(4):
            lst.append(scalebar_free[i*new_height:new_height*(i+1), j*new_length:new_length*(j+1)])

    return lst

def crop_250x_and_save(path_lst, save_folder_path):
    for j in range(len(path_lst)):
        for i in range(16):
            file_path = Path(rf"{save_folder_path}\org_{j}nbr_{i}.tif")
            if Path(file_path).exists():
                pass
            else:
                tiff.imwrite(file_path, crop_250x_to_1000x(ij.IJ.openImage(path_lst[j]))[i])
    print("Done!")

def count_images(path):
    count = 0
    for file in path.iterdir():
        count += 1
    return count

def crop_1000x_to_1000x(tif):
    original = np.asarray(ij.py.from_java(tif))

    scalebar_free = original[0:1790, 0:2560] #Crop the scalebar away

    return scalebar_free

def crop_1000x_and_save(path_lst, save_folder_path):
    for j in range(len(path_lst)):
        file_path = Path(rf"{save_folder_path}\org_{j}.tif")
        if Path(file_path).exists():
            pass
        else:
            tiff.imwrite(file_path, crop_1000x_to_1000x(ij.IJ.openImage(paths[j])))
    print("Done!")

from PIL import Image

def upscale_images(folder_path, save_folder_path):
    folder = Path(folder_path)
    save_folder = Path(save_folder_path)

    for file in folder.iterdir():
        img = Image.open(file)

        upscaled_img = img.resize((2560, 1790), Image.Resampling.LANCZOS)

        upscaled_img.save(save_folder / f"{file.stem}_upscaled{file.suffix}")