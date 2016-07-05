# Import arcpy module
import arcpy, math

####
########Draw Wedge Function##################
####

def drawWedge(cx,cy,r1,r2,start,end):
    point = arcpy.Point()
    array = arcpy.Array()
    
    #Calculate the end x,y for the wedge
    x_end = cx + r2*math.cos(start)
    y_end = cy + r2*math.sin(start)
    
    #Calculate the step value for the x,y coordiantes, use 50 points for each radius
    i = math.radians(0.1)
    
    #Calculate the outer edge of the wedge
    a = start

    #If r1 == 0 then create a wedge from the centre point
    if r1 == 0:
        #Add the start point to the array
        point.X = cx
        point.Y = cy
        array.add(point)
        #Calculate the rest of the wedge
        while a >= end:
            point.X = cx + r2*math.cos(a)
            point.Y = cy + r2*math.sin(a)
            array.add(point)
            a -= i
        #Close the polygon
        point.X = cx
        point.Y = cy
        array.add(point)
        
    else:
        while a >= end:
            point.X = cx + r2*math.cos(a)
            point.Y = cy + r2*math.sin(a)
            a -= i
            array.add(point)
            
        #Caluclate the inner edge of the wedge
        a = end
        
        while a <= start:
            a += i
            point.X = cx + r1*math.cos(a)
            point.Y = cy + r1*math.sin(a)
            array.add(point)
            
        #Close the polygon by adding the end point
        point.X = x_end
        point.Y = y_end
        array.add(point)

    #Create the polygon
    polygon = arcpy.Polygon(array)

    return polygon

####
########End of Draw Wedge Function##################
####

####
########Script Parameters##################
####
Point_Input = arcpy.GetParameterAsText(0)
Radius2_Input = arcpy.GetParameterAsText(1)
Azimuth1_Input = arcpy.GetParameterAsText(2)
Azimuth2_Input = arcpy.GetParameterAsText(3)
OffsetA_Input = arcpy.GetParameterAsText(4)
Radius1_Input = arcpy.GetParameterAsText(5)
viewshed = arcpy.GetParameterAsText(6)
wedge = arcpy.GetParameterAsText(7)
fullwedge = arcpy.GetParameterAsText(8)

elevation = r"d:\GitHub\air-c2-cop\data\Elevation\gtop30"

Output_CS = arcpy.Describe(elevation).spatialReference
arcpy.env.outputCoordinateSystem = Output_CS

polylist = []
wedges = []

####
########End of Script Parameters##################
####

arcpy.CalculateField_management(Point_Input, "RADIUS1", "0", "PYTHON", "")
arcpy.CalculateField_management(Point_Input, "OFFSETB", "0", "PYTHON", "")
arcpy.CalculateField_management(Point_Input, "RADIUS2", Radius2_Input, "PYTHON", "")
arcpy.CalculateField_management(Point_Input, "AZIMUTH1", Azimuth1_Input, "PYTHON", "")
arcpy.CalculateField_management(Point_Input, "AZIMUTH2", Azimuth2_Input, "PYTHON", "")
arcpy.CalculateField_management(Point_Input, "OFFSETA", OffsetA_Input, "PYTHON", "")
arcpy.CalculateField_management(Point_Input, "RADIUS1", Radius1_Input, "PYTHON", "")

arcpy.Buffer_analysis(Point_Input, "in_memory\OuterBuffer", "RADIUS2", "FULL", "ROUND", "NONE", "", "PLANAR")

desc = arcpy.Describe("in_memory\OuterBuffer")
xMin = desc.Extent.XMin
yMin = desc.Extent.YMin
xMax = desc.Extent.XMax
yMax = desc.Extent.YMax
Extent = str(xMin) + " " + str(yMin) + " " + str(xMax) + " " + str(yMax)
arcpy.Clip_management(elevation, Extent, "in_memory\clip")

arcpy.Viewshed_3d("in_memory\clip", Point_Input, "in_memory\intervis", "1", "FLAT_EARTH", "0.13")

arcpy.RasterToPolygon_conversion(in_raster="in_memory\intervis", out_polygon_features="in_memory\unclipped",simplify="NO_SIMPLIFY")

fields = ["SHAPE@XY","RADIUS1","RADIUS2","AZIMUTH1","AZIMUTH2"]
## get the attributes from the input point
with arcpy.da.SearchCursor(Point_Input,fields) as cursor:
    for row in cursor:
        cx = row[0][0]
        cy = row[0][1]
        r1 = row[1]
        r2 = row[2]
        start = math.radians(90 - row[3])
        if row[3] > row[4]:
            end = row[4] + 360
            end =  math.radians(90 - end)
        else: 
            end = math.radians(90 - row[4])
        
        poly = drawWedge(cx,cy,r1,r2,start,end)
        polylist.append(poly)
        fullWedge = drawWedge(cx,cy,0,r2,start,end)
        wedges.append(fullWedge)


arcpy.CopyFeatures_management(polylist,wedge)
arcpy.CopyFeatures_management(wedges,fullwedge)

arcpy.Clip_analysis("in_memory\unclipped", wedge, "in_memory\\dissolve")
arcpy.Dissolve_management("in_memory\\dissolve", viewshed, "gridcode", "", "MULTI_PART", "DISSOLVE_LINES")
