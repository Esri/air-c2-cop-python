##Name: Download NOAA data
##
##Description: Downloads the most up to date data from the NOAA site by getting the present date.
##
##                Script works as follow;
##                    Gets the present time date in UTC
##                    Uses the OPeNDAP to NetCDF tool from Multidimension Supplimental Tool
##                    Downloads the specified variables into NetCDF format files and saves them in the relative location, based on where the script file is located.
##                    The present data is removed from the Mosaic Dataset
##                    The new data is then loaded into the Mosiac Dataset
##                    The wind data is then combined into a Multiband raster.
##
##Date Edited: 15/08/2016


#Import modules
import arcpy
import os
import datetime
from arcpy import env
from datetime import datetime, timedelta
from datetime import time

arcpy.env.overwriteOutput = True

start = str(datetime.utcnow())
print "The script started at" + " " + start

#Gets the current directory where the script is sitting so that everything else can work off relative paths.
folder = os.path.dirname(__file__)
topFolder = os.path.dirname(folder)
        
#Names of folders to be added to topFolder generated above
gdb = "Geodatabase"
NetCDFData = "NetCDFdata"
tls = "Tools"

#Declaration of variables used later
variable = "rh2m;tcdcclm;tmpsfc;hgtclb;vissfc;ugrd10m;vgrd10m;ugrdmwl;vgrdmwl;snodsfc;gustsfc;apcpsfc"
variable2 = "ugrd10m"
variable3 = "vgrd10m"
extent = "-126 30 -109 45"
dimension = "time '2016-01-01 00:00:00' '2016-12-31 00:00:00'"
env.workspace = topFolder + os.sep + gdb + "\OperationalWeather.gdb"

#_____________________________________________________________________________________________________________________________________________

def download(paramFN,paramDL):
    #Import custom toolbox required
    arcpy.ImportToolbox(topFolder + os.sep + tls + "\MultidimensionSupplementalTools\Multidimension Supplemental Tools.pyt")

    print ("Toolbox imported")

    #Get present date and time
    patternDate = '%Y%m%d'
    patternTime = '%H:%M:%S'

    utcdate = datetime.utcnow() - timedelta(hours=N)
    
##    stringDateNow = datetime.utcnow().strftime(patternDate)
##    stringTimeNow = datetime.utcnow().strftime(patternTime)

    stringDateNow = utcdate.strftime(patternDate)
    stringTimeNow = utcdate.strftime(patternTime)

    print ("datetime returned")

    #Insert present date into string for out_file
    stringToChange =  topFolder + os.sep + NetCDFData + r"\nam%s" + paramFN + ".nc"
    stringToChange2 = topFolder + os.sep + NetCDFData + r"\nam%s" + paramFN + "Wind_U.nc"
    stringToChange3 = topFolder + os.sep + NetCDFData + r"\nam%s" + paramFN + "Wind_V.nc"
    stringToChange4 = r"http://nomads.ncep.noaa.gov/dods/nam/nam%s/nam" + paramDL
     
    stringToInsert = stringDateNow
    
    stringFinal = stringToChange % stringToInsert
    stringFinal2 = stringToChange2 % stringToInsert
    stringFinal3 = stringToChange3 % stringToInsert
    stringFinal4 = stringToChange4 % stringToInsert
    filename = "nam%s1hr00z.nc" % stringToInsert

    #------------------------------------------------------------------------------------------------------------------------------------------

    #Declare variables to be added into OPeNDAP to NetCDF tool for general data
    in_url = stringFinal4
    out_file = stringFinal

    #Run OPeNDAP to NetCDF tool
    arcpy.OPeNDAPtoNetCDF_mds( in_url, variable, out_file, extent, dimension, "BY_VALUE")

    #-------------------------------------------------------------------------------------------------------------------------------------------

    #Declare variables to be added into OPeNDAP to NetCDF tool for download of wind_U data
    in_url2 = stringFinal4
    out_file2 = stringFinal2

    #Run OPeNDAP to NetCDF tool
    arcpy.OPeNDAPtoNetCDF_mds( in_url2, variable2, out_file2, extent, dimension, "BY_VALUE")

    #-------------------------------------------------------------------------------------------------------------------------------------------

    #Declare variables to be added into OPeNDAP to NetCDF tool for download of wind_V data
    in_url3 = stringFinal4
    out_file3 = stringFinal3

    #Run OPeNDAP to NetCDF tool
    arcpy.OPeNDAPtoNetCDF_mds( in_url3, variable3, out_file3, extent, dimension, "BY_VALUE")

    finishDownload = str(datetime.utcnow())
    print "OPeNDAp Tool run and data download finished at" + " " + finishDownload
    print out_file
    #____________________________________________________________________________________________________________________________________________

    #Data loading into Mosaic datasets.

    Input_Data = out_file
    Input_Data2 = out_file2
    Input_Data3 = out_file3

    i = 0
    inputs = [Input_Data,Input_Data2,Input_Data3]

    Raster_Type = "NetCDF" 

    output = topFolder + os.sep + gdb + "\OperationalWeather.gdb\\OperationalData" 
    output2 = topFolder + os.sep + gdb + "\OperationalWeather.gdb\\Ugrd10m"
    output3 = topFolder + os.sep + gdb + "\OperationalWeather.gdb\\Vgrd10m"

    outputs = [output,output2,output3]

    for ras in outputs:
        #Check if the geodatabases stated above exist
        if arcpy.Exists(ras):
            print ras + " " + "exists"
        else:
            print ras + " " + "does not exist"

        # Process: Remove Rasters From Mosaic Dataset
        arcpy.RemoveRastersFromMosaicDataset_management(ras, "OBJECTID >=0", "NO_BOUNDARY", "NO_MARK_OVERVIEW_ITEMS", "NO_DELETE_OVERVIEW_IMAGES", "NO_DELETE_ITEM_CACHE", "REMOVE_MOSAICDATASET_ITEMS", "NO_CELL_SIZES")

        # Process: Add Rasters To Mosaic Dataset
        arcpy.AddRastersToMosaicDataset_management(ras, Raster_Type, inputs[i], "UPDATE_CELL_SIZES", "UPDATE_BOUNDARY", "NO_OVERVIEWS", "", "0", "1500", "", "*.nc", "SUBFOLDERS", "ALLOW_DUPLICATES", "NO_PYRAMIDS", "NO_STATISTICS", "NO_THUMBNAILS", "", "NO_FORCE_SPATIAL_REFERENCE")

        print ("Rasters added to" + " " + ras)

        i = i+1


    finishDataLoad = str(datetime.utcnow())
    print "Data loading finished at" + " " + finishDataLoad

    #_____________________________________________________________________________________________________________________________________________

    #Sort out wind data
    #add to a multiband raster

    rasIn = env.workspace + "\Ugrd10m" + ";" + env.workspace + "\Vgrd10m"
    outcomp = env.workspace + "\OperationalWind"

    #Make composite band raster
    arcpy.CompositeBands_management(rasIn, outcomp)
    

    finishWindDataProcessing = str(datetime.utcnow())
    print "Wind data processing finished at" + " " + finishWindDataProcessing
    print " "
    print " "
    print "The script finished at" + " " + finishWindDataProcessing
#_________________________________________________________________________________________________________________________________________________

# get the present time in utc.
# set times are set around the times that the data is released by NOAA


now_time = time(int(datetime.utcnow().strftime("%H")), int(datetime.utcnow().strftime("%M")), int(datetime.utcnow().strftime("%S")))

if now_time >= time(02,50,00) and now_time < time(8,50,00):
    download("1hr00z", "1hr_00z")
    
elif now_time >= time(8,50,00) and now_time < time(14,50,00):
    download("1hr06z", "1hr_06z")
 
elif now_time >= time(14,50,00) and now_time < time(21,00,00):
    download("1hr12z", "1hr_12z")

elif ((now_time >= time(21,00,00) and now_time <= time(23,59,59)) or (now_time >= time(00,00,00) and now_time <= time(02,49,59))):
    download("1hr18z", "1hr_18z")

