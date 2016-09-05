# Import arcpy module
import arcpy

# Script arguments
Target_Workspace = arcpy.GetParameterAsText(0)

AMS_Id = arcpy.GetParameterAsText(1)
if AMS_Id == '#' or not AMS_Id:
    AMS_Id = "%%" # provide a default value if unspecified

# Process: Make Table View
arcpy.MakeTableView_management("%s/AirC2_ATO_MISSION"  % (targetWS, "ATO_POINT_FILTER", "AMSID like '%AMS Id%'", "", "")

# Process: Delete Rows
arcpy.DeleteRows_management("ATO_POINT_FILTER")

# Process: Make Table View
arcpy.MakeTableView_management("%s/AirC2_ATO_GENTEXT"  % (targetWS), "ATO_GENTEXT_FILTER", "AMSID like '%AMS Id%'", "", "")

# Process: Delete Rows
arcpy.DeleteRows_management("ATO_GENTEXT_FILTER")

# Process: Make Table View
arcpy.MakeTableView_management("%s/AirC2_ATO_MISSION_BRIEFING"  % (targetWS), "ATO_BRIEFING_FILTER", "AMSID like '%AMS Id%'", "", "")

# Process: Delete Rows
arcpy.DeleteRows_management("ATO_BRIEFING_FILTER")

