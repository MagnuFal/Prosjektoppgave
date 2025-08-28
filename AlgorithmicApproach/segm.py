import imagej

# initialize ImageJ
ij = imagej.init('sc.fiji:fiji:2.14.0')
print(f"ImageJ version: {ij.getVersion()}")

imp = ij.IJ.openImage("C:/Users/magfa/Documents/Prosjekt/Prosjektbilder/SEM Fe tilsetning og kjølerate/6ps/BSE_x250_m007.tif")
ij.py.show(imp, cmap='Grays_r')

#dataset = ij.io().open('C:/Users/magfa/Documents/Prosjekt/Prosjektbilder/SEM Fe tilsetning og kjølerate/6ps/BSE_x250_m007.tif')
#ij.py.show(dataset, cmap='Grays_r')

#imp.setAutoThreshold("Default dark no-reset")
#ij.Prefs.blackBackground = True
ij.IJ.run(imp, "Convert to Mask", "")
ij.py.show(imp, cmap='Grays_r')

ij.IJ.run(imp, "Subtract Background...", "")
ij.py.show(imp, cmap='Grays_r')

for i in range(100):
    ij.IJ.run(imp, "Despeckle", "")
ij.py.show(imp, cmap='Grays_r')

#Following the PyImageJ Segmentation Tutorial in the following code

import scyjava as sj

# preprocess with edge-preserving smoothing
ij.IJ.run(imp, "Kuwahara Filter", "sampling=10") # Look ma, a Fiji plugin!
ij.py.show(imp)

# threshold to binary mask
Prefs = sj.jimport('ij.Prefs')
Prefs.blackBackground = True
ij.IJ.setAutoThreshold(imp, "Otsu dark")
ImagePlus = sj.jimport("ij.ImagePlus")
mask = ImagePlus("cells-mask", imp.createThresholdMask())
ij.IJ.run(imp, "Close", "")
ij.py.show(mask)

# clean up the binary mask.
ij.IJ.run(mask, "Dilate", "")
ij.IJ.run(mask, "Fill Holes", "")
ij.IJ.run(mask, "Watershed", "")
ij.py.show(mask)

# Save the mask as a selection (a.k.a. ROI).
ij.IJ.run(mask, "Create Selection", "")
roi = mask.getRoi()
ij.IJ.run(mask, "Close", "")

# Split the ROI into cells.
# This works because cells are disconnected due to the watershed.
rois = roi.getRois()
print(len(rois), "cells detected")

# Calculate statistics.

from collections import defaultdict
from pandas import DataFrame

# Make sure to measure the same slice as segmented!
#imp.setPosition(c, z, t)

# Measure each cell, accumulating results into a dictionary.
ij.IJ.run("Set Measurements...", "area mean min centroid median skewness kurtosis redirect=None decimal=3");
results = ij.ResultsTable.getResultsTable()
stats_ij = defaultdict(list)
for cell in rois:
    imp.setRoi(cell)
    ij.IJ.run(imp, "Measure", "")
    for column in results.getHeadings():
        stats_ij[column].append(results.getColumn(column)[-1])

# Display the results.
df_ij = DataFrame(stats_ij)
# pandas thinks the keys/col names are multi-level
# see pandas docs for more info: https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html
df_ij.columns = [''.join(col) for col in df_ij.columns.values]
df_ij