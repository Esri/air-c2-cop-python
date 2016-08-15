import time, os, datetime, sys, logging, logging.handlers, shutil
import arcpy
import utils.common
import config.settings

########################## user defined functions ##############################

def getDatabaseItemCount(workspace):
     """returns the item count in provided database"""
     arcpy.env.workspace = workspace
     feature_classes = []
     utils.common.OutputMessage(logging.DEBUG, "{0} - Compiling a list of items in source Database".format(time.ctime()))
     for dirpath, dirnames, filenames in arcpy.da.Walk(workspace,datatype="Any",type="Any"):
         for filename in filenames:
             feature_classes.append(os.path.join(dirpath, filename))
     utils.common.OutputMessage(logging.DEBUG, "{0} - ".format(time.ctime()) + "There are a total of {0} items in the database".format(len(feature_classes)))
     return feature_classes, len(feature_classes)

def replicateDatabase(dbConnection, targetGDB):
    
    if arcpy.Exists(dbConnection):
        featSDE,cntSDE = getDatabaseItemCount(dbConnection)
        utils.common.OutputMessage(logging.DEBUG, "{0} - ".format(time.ctime()) + "Geodatabase being copied: %s -- Feature Count: %s" %(dbConnection, cntSDE))
     
        arcpy.env.workspace = dbConnection

        try:
            datasetList = [arcpy.Describe(a).name for a in arcpy.ListDatasets()]
        except Exception, e:
            datasetList = []
            utils.common.OutputMessage(logging.DEBUG, e)
        try:
            featureClasses = [arcpy.Describe(a).name for a in arcpy.ListFeatureClasses()]
        except Exception, e:
            featureClasses = []
            utils.common.OutputMessage(logging.DEBUG, e)
        try:
            tables = [arcpy.Describe(a).name for a in arcpy.ListTables()]
        except Exception, e:
            tables = []
            utils.common.OutputMessage(logging.DEBUG, e)

        #Compiles a list of the previous three lists to iterate over
        allDbData = datasetList + featureClasses + tables

        for sourcePath in allDbData:
            targetName = sourcePath.split('.')[-1]
            targetPath = os.path.join(targetGDB, targetName)
            if not arcpy.Exists(targetPath):
                try:
                    utils.common.OutputMessage(logging.DEBUG, "{0} - ".format(time.ctime()) + "Attempting to Copy %s to %s" %(targetName, targetPath))     
                    arcpy.Copy_management(sourcePath, targetPath)
                    utils.common.OutputMessage(logging.DEBUG, "{0} - ".format(time.ctime()) + "Finished copying %s to %s" %(targetName, targetPath))
                except Exception as e:
                    utils.common.OutputMessage(logging.DEBUG, "{0} - ".format(time.ctime()) + "Unable to copy %s to %s" %(targetName, targetPath))
                    utils.common.OutputMessage(logging.DEBUG, e)
            else:
                utils.common.OutputMessage(logging.DEBUG, "{0} - ".format(time.ctime()) + "%s already exists....skipping....." %(targetName))

        utils.common.OutputMessage(logging.DEBUG, "{0} - ".format(time.ctime()) + "Completed data copy")
        
    else:
        utils.common.OutputMessage(logging.DEBUG, "{0} - ".format(time.ctime()) + "{0} does not exist or is not supported! Please check the database path and try again.".format(dbConnection))

def repairMXDPaths(targetGDB):
     for root, dirs, files in os.walk(r"..\..\maps"):
          for f in files:
               if f.endswith(".mxd"):
                    mxd = arcpy.mapping.MapDocument(root + '\\' + f)
                    utils.common.OutputMessage(logging.DEBUG, "{0} Updating data source paths for ".format(time.ctime()) + root + '\\' + f)
                    for lyr in arcpy.mapping.ListLayers(mxd):
                         lyr.replaceDataSource(targetGDB, "SDE_WORKSPACE")
                    for table in arcpy.mapping.ListTableViews(mxd):
                         table.replaceDataSource(targetGDB, "SDE_WORKSPACE")
                    mxd.save()
                    del mxd
                
#####################################################################################



if __name__ == "__main__":

    ############################### user variables #################################
    
    databaseConnection = r"..\..\data\AirC2.gdb"
    targetGDB = arcpy.GetParameterAsText(0)
    CONST_HEADING_PAD = 50

    ############################### logging items ###################################

    # Setup logging / message output
    utils.common.setupLogging("DEBUG", config.settings.LOG_ENABLE_FILE, config.settings.LOG_PATH, 'copy_source_data', config.settings.LOG_USE_TIMESTAMP)
    try:
         ########################## function calls ######################################
         replicateDatabase(databaseConnection, targetGDB)
         repairMXDPaths(targetGDB)
         ################################################################################
    except Exception, e:
         utils.common.OutputMessage(logging.DEBUG, e)
                    

    utils.common.OutputMessage(logging.DEBUG, '-' * CONST_HEADING_PAD)
    utils.common.OutputMessage(logging.DEBUG, "{0} Script complete".format(time.ctime()))
    utils.common.OutputMessage(logging.DEBUG, '-' * CONST_HEADING_PAD)
