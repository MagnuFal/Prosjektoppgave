import imagej
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# initialize ImageJ
ij = imagej.init('sc.fiji:fiji:2.14.0') 
print(f"ImageJ version: {ij.getVersion()}")

def scripture_mask(n): 
    
    original = np.asarray(ij.py.from_java(n))
    ij.IJ.setThreshold(n, 190, 255)
    ij.IJ.run(n, "Convert to Mask", '')

    for i in range(1):
        ij.IJ.run(n, "Despeckle", "")

    noisy = np.asarray(ij.py.from_java(n))

    for i in range(1):
        ij.IJ.run(n, "Subtract Background...", "rolling=2")

    noise = np.asarray(ij.py.from_java(n))

    cleaned_up = noisy - noise

    binary_mask = cleaned_up / 255 

    return (binary_mask > 0.5).astype(int) 