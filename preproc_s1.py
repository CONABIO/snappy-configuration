#!/usr/bin/env python
# -*- coding: utf-8 -*-

import snappy
import gc
import subprocess
import sys
from snappy import ProductIO
from snappy import HashMap
from snappy import GPF


GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
HashMap = snappy.jpy.get_type('java.util.HashMap')


# usage python preproc_s1.py S1A_IW_GRDH_1SDV_20150513T010448_20150513T010513_005896_007983_76F6.SAFE
# Now loop through all Sentinel-1 data sub folders that are located within a super folder (of course, make sure, that the data is already unzipped):

temp = "/home/ubuntu/tmp_s1/"

folder = sys.argv[1]
gc.enable()
timestamp = folder.split("_")[4]
date = timestamp

# Then, read in the Sentinel-1 data product:

sentinel_1 = ProductIO.readProduct("/home/ubuntu/s3_bucket/" + "Sentinel1_Mexico/" + folder + "//manifest.safe")

# If polarization bands are available, spolit up your code to process VH and VV intensity data separately. 
# The first step is the calibration procedure by transforming the DN values to Sigma Naught respectively. You can specify the parameters to output the Image in Decibels as well.

pols = ['VH','VV']
for p in pols:
  polarization = p

  ### CALIBRATION
  parameters = HashMap()
  parameters.put('outputSigmaBand', True)
  parameters.put('sourceBands', 'Intensity_' + polarization)
  parameters.put('selectedPolarisations', polarization)
  parameters.put('outputImageScaleInDb', False)
  _calibration = temp + date + "_calibrate_" + polarization
  calibration  = GPF.createProduct("Calibration", parameters, sentinel_1)
  #ProductIO.writeProduct(calibration, _calibration, 'BEAM-DIMAP')
  #calibration = ProductIO.readProduct(calib + ".dim")    

  ### SPECKLE FILTER 
  parameters = HashMap()
  parameters.put('filter','Refined Lee')
  parameters.put('filterSizeX', 3)
  parameters.put('filtersizeY', 3)
  _filtered = temp + date + "_filtered_" + polarization
  filtered  = GPF.createProduct("Speckle-Filter", parameters, calibration)
  #ProductIO.writeProduct(filtered, _filtered, 'BEAM-DIMAP')
  #filtered = ProductIO.readProduct(calib + ".dim") 

  # Apply a Range Doppler Terrain Correction to correct for layover and foreshortening effects, 
  # by using the SRTM 3 arcsecond product (90m) that is downloaded automatically. 
  # You could also specify an own DEM product with a higher spatial resolution from a local path:

  ### TERRAIN CORRECTION
  parameters = HashMap()
  parameters.put('demResamplingMethod', 'NEAREST_NEIGHBOUR')
  parameters.put('imgResamplingMethod', 'NEAREST_NEIGHBOUR')
  parameters.put('demName', 'SRTM 3Sec')
  parameters.put('pixelSpacingInMeter', 10.0)
  parameters.put('sourceBands', 'Sigma0_' + polarization)
  #parameters.put('nodataValueAtSea', True)
  _terrain = temp + date + "_dB_" + polarization
  terrain  = GPF.createProduct("Terrain-Correction", parameters, filtered)
  #ProductIO.writeProduct(terrain, _terrain, 'BEAM-DIMAP')

  # LINEAR to dB
  parameters = HashMap()
  _corrected = temp + date + "_corrected_" + polarization
  corrected  = GPF.createProduct("LinearToFromdB", parameters, terrain)
  ProductIO.writeProduct(corrected, _corrected, 'GeoTIFF-BigTIFF')
  cmd = "/home/ubuntu/.local/bin/aws s3 mv --quiet " + _corrected + ".tif" + " s3://conabio-s3-oregon/S1MEX_preprocessed/" + folder.split(".")[0] + "/"
  subprocess.call(cmd, shell=True)
