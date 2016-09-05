# Import arcpy module
import arcpy

# Script arguments
targetWS = arcpy.GetParameterAsText(0)

AMS_Id = arcpy.GetParameterAsText(1)
if AMS_Id == '#' or not AMS_Id:
    AMS_Id = "%%" # provide a default value if unspecified

# Process: Make Table View
arcpy.MakeTableView_management("%s/AirC2_AMS_RECORD" % (targetWS), "AMS_RECORD_FILTER", "AMSID like '%AMS Id%'", "", "")

# Process: Delete Rows
arcpy.DeleteRows_management("AMS_RECORD_FILTER")

# Process: Make Table View
arcpy.MakeTableView_management("%s/AirC2_ACO_POLYGON" % (targetWS), "AMS_POLYGON_FILTER", "AMSID like '%AMS Id%'", "", "")

# Process: Delete Rows
arcpy.DeleteRows_management("AMS_POLYGON_FILTER")

# Process: Make Table View
arcpy.MakeTableView_management("%s/AirC2_ACO_PERIOD" % (targetWS), "AMS_ORDER_PERIOD_FILTER", "AMSID like '%AMS Id%'", "", "")

# Process: Delete Rows
arcpy.DeleteRows_management("AMS_ORDER_PERIOD_FILTER")

# Process: Make Table View
arcpy.MakeTableView_management("%s/AirC2_ACO_LINE" % (targetWS), "AMS_ORDER_LINE_FILTER", "AMSID like '%AMS Id%'", "", "")

# Process: Delete Rows
arcpy.DeleteRows_management("AMS_ORDER_LINE_FILTER")

# Process: Make Table View
arcpy.MakeTableView_management("%s/AirC2_ACO_POINT" % (targetWS), "ACO_POINT_FILTER", "AMSID like '%AMS Id%'", "", "")

# Process: Delete Rows
arcpy.DeleteRows_management("ACO_POINT_FILTER")

