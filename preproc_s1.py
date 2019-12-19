import snappy
import time

from snappy import ProductIO
from snappy import HashMap
from snappy import GPF

import os, gc   


GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()

HashMap = snappy.jpy.get_type('java.util.HashMap')

# Now loop through all Sentinel-1 data sub folders that are located within a super folder (of course, make sure, that the data is already unzipped):

path = "./downloaded/"   # Path with unzipped scenes

for folder in os.listdir(path):

   gc.enable()
   
   output = path + folder + "//"  
   timestamp = folder.split("_")[4] 
   date = timestamp[:8]

   print(output)

   print(date)
   # Then, read in the Sentinel-1 data product:

   sentinel_1 = ProductIO.readProduct(output + "//manifest.safe")    
   print sentinel_1
   
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

      calib = output + date + "_calibrate_" + polarization 
      calibration = GPF.createProduct("Calibration", parameters, sentinel_1) 
      ProductIO.writeProduct(calibration, calib, 'BEAM-DIMAP')
      
      #calibration = ProductIO.readProduct(calib + ".dim")    

      ### speckle filter
      parameters = HashMap()
      parameters.put('filter','Refined Lee')
      #parameters.put('windowSize','7')

      filtered = GPF.createProduct("Speckle-Filter", parameters, calibration)   

      #ProductIO.writeProduct(filtered_, calib, 'BEAM-DIMAP')

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
 
      db = output + date + "_corrected_" + polarization 
      target_2 = GPF.createProduct("Terrain-Correction", parameters, filtered) 
      
      #ProductIO.writeProduct(target_2, terrain, 'GeoTIFF-BigTIFF')

      # linear to dB
      parameters = HashMap()
      targetDB = GPF.createProduct("LinearToFromdB", parameters, target_2)

      ProductIO.writeProduct(targetDB, db, 'GeoTIFF-BigTIFF')
      time.sleep( 10 )  # Sleep time while java garbage collector ends. (May be not required)
