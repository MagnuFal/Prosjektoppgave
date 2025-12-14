import imagej
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# initialize ImageJ
ij = imagej.init('sc.fiji:fiji:2.14.0') 
print(f"ImageJ version: {ij.getVersion()}")

def area_fraction(arr):

    return np.sum(arr > 0) / arr.size

import pandas as pd
def area_fractions_from_folder(folder_path, csv):
    results = []
    folder = Path(folder_path)

    for file in folder.iterdir():
        imp = ij.IJ.openImage(str(file.resolve()))
        arr = np.asarray(ij.py.from_java(imp))
        imp.close()
        results.append({"Filename:" : {file.stem}, "Area fraction" : area_fraction(arr)})

    df = pd.DataFrame(results)
    df.to_csv(csv, index=False)
    avg = df["Area fraction"].mean()
    std = df["Area fraction"].std()
    print(f"Average area fraction: {avg} +- {std}")