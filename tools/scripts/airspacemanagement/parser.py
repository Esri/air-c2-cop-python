# -*- coding: utf-8 -*-

###############################################################################
# Authors: Shaun Nicholson, Esri UK, May 2015
#          Anthony Giles, Helyx SIS, Feb 2016
#
# (C) Copyright ESRI (UK) Limited 2011. All rights reserved
# ESRI (UK) Ltd, Millennium House, 65 Walton Street, Aylesbury, HP21 7QG
# Tel: +44 (0) 1296 745500  Fax: +44 (0) 1296 745544
###############################################################################

import arcpy
from arcpy import env
import sys
import os
import os.path
import inspect
import time
import datetime
import logging
from datetime import datetime
import copy
import json
import re
import math

import config
import utils.common

class FileParser:

    _sourceFile = None
    _records = []

    def __init__(self, sourceFile):
        self._sourceFile = sourceFile
        pass

    def execute(self):
        utils.common.OutputMessage(logging.DEBUG, "{0} FileParser.execute() - Start".format(time.ctime()))

        with open(self._sourceFile, 'r') as file:
            recordBuffer = ''
            for line in file:
                isRecordEnd = line.endswith('//\n')
                if isRecordEnd: line = line.rstrip('\n')
                recordBuffer += line
                if isRecordEnd:
                    self._records.append(recordBuffer)
                    recordBuffer = ''
        file.closed

        self._outputRecords()

        utils.common.OutputMessage(logging.DEBUG, "{0} FileParser.execute() - Finish".format(time.ctime()))

        return self._records

    def _outputRecords(self):
        utils.common.OutputMessage(logging.DEBUG, "{0} FileParser._outputRecords() - Start".format(time.ctime()))

        utils.common.OutputMessage(logging.DEBUG, "{0} FileParser._outputRecords() - Record Count={1}".format(time.ctime(), len(self._records)))

        for record in self._records:
            utils.common.OutputMessage(logging.DEBUG, 'RECORD: ' + record)

        utils.common.OutputMessage(logging.DEBUG, "{0} FileParser._outputRecords() - Finish".format(time.ctime()))

        pass

class RecordIterator:

    _records            = []
    _currentLineIndex   = -1

    def __init__(self, records):
        self._records = records
        self._currentLineIndex = 0
        pass
    
    def isEOF(self):
        return self._currentLineIndex >= len(self._records)

    def currentLine(self):
        return self._records[self._currentLineIndex]

    def nextLine(self):
        self._currentLineIndex += 1
        return

###########################################################################
# Parse a date in string format to a real datetime.
# Assume input is in the format:
#    140845ZAPR
#    ddhhmmZmon
###########################################################################
def parseDate(dateString):
    s = dateString.upper()
    if s[-1].isdigit() == False:
        return datetime.strptime(s, '%d%H%MZ%b')
    else:
        return datetime.strptime(s, '%d%H%MZ%b%Y')

###########################################################################
# Parse a date in string format to a real datetime.
#
###########################################################################
def getDateString(timeValue):
    #return timeValue.strftime("%d-%m-%Y %H:%M")
    return timeValue.strftime("%Y/%m/%d %H:%M:00")

###########################################################################
# Convert a string to a decimal degrees value.
# Assume input is in the format:
#    LATS:500000N0113000W
#    LATS:ddmmssNdddmmssW
#    LATM:5720N00720W
#    LATM:ddmmNdddmmW
#    DMPIT:5503.0146N00233.2405W
#    DMPIT:ddmm.ssssNdddmm.ssssW
###########################################################################
def parseLatLong(llValue,height):

    v = llValue.upper()
    isS = False
    isM = False
    isD = False
    if v.startswith('LATS:') == True:
        v = v.replace('LATS:', '')
        isS = True
    if v.startswith('LATM:') == True:
        v = v.replace('LATM:', '')
        isM = True
    if v.startswith('DMPIT:') == True:
        v = v.replace('DMPIT:', '')
        isD = True
    if isS == True:
        latD = v[0:2]
        latM = v[2:4]
        latS = v[4:6]
        latC = v[6:7]
        lonD = v[7:10]
        lonM = v[10:12]
        lonS = v[12:14]
        lonC = v[14:15]
    if isM == True:
        latD = v[0:2]
        latM = v[2:4]
        latS = 0
        latC = v[4:5]
        lonD = v[5:8]
        lonM = v[8:10]
        lonS = 0
        lonC = v[10:11]
    if isD == True:
        latD = v[0:2]
        latM = v[2:4]
        latS = v[5:9]
        latC = v[9:10]
        lonD = v[10:13]
        lonM = v[13:15]
        lonS = v[16:20]
        lonC = v[20:21]

    dd = [convertDecimalDegrees(lonD, lonM, lonS, lonC), convertDecimalDegrees(latD, latM, latS, latC), height]
    
    return dd

###########################################################################
# Convert degress minutes seconds into decimal degrees.
#
###########################################################################
def convertDecimalDegrees(d, m, s, c):
    dd = float(d) + float(m)/60 + float(s)/3600
    sign = 1
    if c.upper() in 'S' or c.upper() in 'W': sign = -1
    return dd * sign

###########################################################################
# Parse a distance string.  Assumes in the form:
# 15KM
# 7.5KM
# 1KM
#
###########################################################################
def parseDistance(distanceValue):
    value = distanceValue.upper()
    
    if value.endswith('KM'):
        distanceUnit = 'Kilometers'
        value = float(value.replace('KM', ''))
    elif value.endswith('NM'):
        distanceUnit = 'NauticalMiles'
        value = float(value.replace('NM', ''))
    else:
        raise Exception('Cannot process distance value, unknown units. (%s)' % distanceValue)
    
    return (value, distanceUnit)

def parseEXER(record):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseEXER()".format(time.ctime()))
    items = record.split('/')
    return { 'id': items[1] }

def parseOPER(record):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseOPER()".format(time.ctime()))
    items = record.split('/')
    return { 'id': items[1] }

def parseMSGID(record):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseMSGID()".format(time.ctime()))
    items = record.split('/')
    return { 'id': items[1], 'source': items[2], 'type': items[5], 'version': items[6] }

def parseAMPN(record):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseAMPN()".format(time.ctime()))
    items = record.split('/')
    return { 'title': items[1], 'classification': items[2], 'text': items[3] }

def parseACOID(record):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseACOID()".format(time.ctime()))
    items = record.split('/')
    return { 'item1': items[1], 'item2': items[2] }

def parseGEODATUM(record):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseGEODATUM()".format(time.ctime()))
    items = record.split('/')
    return { 'value': items[1] }

def parsePERIOD(record):
    utils.common.OutputMessage(logging.DEBUG, "{0} parsePERIOD()".format(time.ctime()))
    items = record.split('/')
    return { 'period1': getDateString(parseDate(items[1])), 'period2': getDateString(parseDate(items[2])) }

###########################################################################
# Parse a EFFLEVEL block into JSON.
# Assume the block is in the form:
# EFFLEVEL/BRRA:GL-220AMSL//
# 
###########################################################################
def parseEFFLEVEL(record):
    items   = record.split('/')
    height  = parseHeight(items[1])
    return { 'label': items[1], 'min_height': height['min_height'], 'max_height': height['max_height'], 'ext_height': height['max_height'] - height['min_height']}

def parseHeight(value):
    json = { 'min_height': 0, 'max_height': 0 }

    v = value.split(':')
    v = v[1].split('-')
    
    if(len(v)<=1):       
        min = re.sub(r'\D', '', v[0])
        max = re.sub(r'\D', '', v[0])
    else:        
        min = re.sub(r'\D', '', v[0])
        max = re.sub(r'\D', '', v[1])

    utils.common.OutputMessage(logging.DEBUG, "{0} parseHeight() - {1}:{2}".format(time.ctime(), min, max))

    if len(min) != 0: json['min_height'] = float(min) * 100
    if len(max) != 0: json['max_height'] = float(max) * 100

    return json

###########################################################################
# Parse a ACMID block, assumes block is in the form:
# ACMID/ACM:ROZ/NAME:ATLANTIC/POLYGON/USE:RECCE//
#
###########################################################################
def parseACMID(record):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseACMID()".format(time.ctime()))
    items = record.split('/')
    return { 'id': items[1], 'name': items[2].replace('NAME:', ''), 'type': items[3], 'use': items[4].replace('USE:', '') }

###########################################################################
# Parse a POLYGON block into Esri geometry JSON.
# Assume the POLYGON block is in the form:
# POLYGON/LATS:564100N0033500W/LATS:581700N0054000W/LATS:582500N0050500W/LATS:565200N0031000W//
#
###########################################################################
def parsePOLYGON(record,height):
    utils.common.OutputMessage(logging.DEBUG, "{0} parsePOLYGON()".format(time.ctime()))
    
    json = {}
    json['hasZ'] = True
    json['spatialReference'] = {"wkid" : 4326}
    json['rings'] = [[]]

    items = record.split('/')
    
    for i in items:
        if i.startswith('LATS') == True or i.startswith('LATM') == True or i.startswith('DMPIT') == True:
            json['rings'][0].append(parseLatLong(i,height))
            pass
    # Duplicate the first point to close the polygon.
    if len(json['rings'][0]) > 0:
        json['rings'][0].append(copy.copy(json['rings'][0][0]))

    return json

###########################################################################
# Parse a CORRIDOR block into Esri geometry JSON.
# Assume the CIRCLE block is in the form:
# CORRIDOR/5NM/LATS:3611800N13055416E/LATS:3523304N12911460E/LATS:3527615N12718004E/LATS:3652752N12635564E//
# 
###########################################################################
def parseCORRIDOR(record,height):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseCORRIDOR()".format(time.ctime()))
       
    line = []
    
    items = record.split('/')
    (distance, units) = parseDistance(items[1])
        
    for i in items:
        if i.startswith('LATS') == True or i.startswith('LATM') == True or i.startswith('DMPIT') == True:
            line.append(parseLatLong(i,height))
            pass   
    
    newline = arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in line]),arcpy.SpatialReference(4326), False, False)
    
    arcpy.Buffer_analysis(arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in line]),arcpy.SpatialReference(4326), False, False), r'in_memory\tempBuffer', '%s %s' % (distance/2, units), 'FULL', 'FLAT', 'ALL')
    geometries = arcpy.CopyFeatures_management(r'in_memory\tempBuffer', arcpy.Geometry())
    
    
    objJson = json.loads(geometries[0].JSON)

    objJson['hasZ'] = True
    
    for i in range(0, len(objJson['rings'])):
        for j in range(0, len(objJson['rings'][i])):
            objJson['rings'][i][j].append(height)
    
    arcpy.Delete_management(r'in_memory\tempBuffer')
    
    del geometries
    return objJson
    
###########################################################################
# Parse an AORBIT block into Esri geometry JSON.
# Assume the AORBIT block is in the form:
# AORBIT/LATS:151000N0590900E/LATM:1610N06010E/235KM/C//
# 
###########################################################################
def parseAORBIT(record,height):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseAORBIT()".format(time.ctime()))
       
    line = []
    
    items = record.split('/')
    (distance, units) = parseDistance(items[3])
        
    for i in items:
        if i.startswith('LATS') == True or i.startswith('LATM') == True or i.startswith('DMPIT') == True:
            line.append(parseLatLong(i,height))
            pass   
    
    newline = arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in line]),arcpy.SpatialReference(4326), False, False)
    
    if items[4] == "R":
        line_side = "RIGHT"
        buffer_distance = distance
    elif items[4] == "L":
        line_side = "LEFT"
        buffer_distance = distance
    else:
        line_side = "FULL"
        buffer_distance = distance/2      
    
    arcpy.Buffer_analysis(arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in line]),arcpy.SpatialReference(4326), False, False), r'in_memory\tempBuffer', '%s %s' % (buffer_distance/2, units), line_side, 'FLAT', 'ALL')
    geometries = arcpy.CopyFeatures_management(r'in_memory\tempBuffer', arcpy.Geometry())
        
    objJson = json.loads(geometries[0].JSON)

    objJson['hasZ'] = True
    
    for i in range(0, len(objJson['rings'])):
        for j in range(0, len(objJson['rings'][i])):
            objJson['rings'][i][j].append(height)
    
    arcpy.Delete_management(r'in_memory\tempBuffer')
    
    del geometries
    return objJson
    
###########################################################################
# Parse a APOINT block into Esri geometry JSON.
# Assume the APOINT block is in the form:
# APOINT/LATS:151000N0590900E//
# 
###########################################################################
def parseAPOINT(record,height):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseAPOINT()".format(time.ctime()))
       
    json = {}
    json['hasZ'] = True
    json['spatialReference'] = {"wkid" : 4326}
    
    items = record.split('/')
    for i in items:
        if i.startswith('LATS') == True or i.startswith('LATM') == True or i.startswith('DMPIT') == True:
            pointCoords = parseLatLong(i,height)
            json['x'] = pointCoords[0]
            json['y'] = pointCoords[1]
            json['z'] = pointCoords[2]
            pass    
    return json    

###########################################################################
# Parse a CNTRLPT block into Esri geometry JSON.
# Assume the CNTRLPT block is in the form:
# CNTRLPT/CP/APPLE/4520.3500N-02126.1500E/BRRA:MSL-210AMSL/
# 
###########################################################################
def parseCNTRLPT(record):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseAPOINT()".format(time.ctime()))
       
    json = {}
    json['hasZ'] = True
    json['spatialReference'] = {"wkid" : 4326}
    
    items = record.split('/')
    for i in items:
        if i.startswith('LATS') == True or i.startswith('LATM') == True or i.startswith('DMPIT') == True:
            pointCoords = parseLatLong(i,height)
            json['x'] = pointCoords[0]
            json['y'] = pointCoords[1]
            json['z'] = pointCoords[2]
            pass    
    return json
    
###########################################################################
# Parse a GEOLINE block into Esri geometry JSON.
# Assume the GEOLINE block is in the form:
# GEOLINE/LATM:2037N05943E/LATS:204400N0594300E/LATM:2048N05982E//
# 
###########################################################################
def parseGEOLINE(record,height):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseGEOLINE()".format(time.ctime()))
    
    json = {}
    json['hasZ'] = True
    json['spatialReference'] = {"wkid" : 4326}
    json['paths'] = [[]]
    
    items = record.split('/')
            
    for i in items:
        if i.startswith('LATS') == True or i.startswith('LATM') == True or i.startswith('DMPIT') == True:
            json['paths'][0].append(parseLatLong(i,height))
            pass
    
    return json
    
##########################################################################
# Parse a APERIOD block into JSON.
# Assume the block is in the form:
# APERIOD/DISCRETE/141030ZAPR/141130ZAPR//
# APERIOD/INTERVAL/010000JAN/012359JAN/DAILY/7DAY//
# APERIOD/INTERVAL/131325ZNOV/132359ZNOV/WEEKLY/4WK//
# APERIOD/TYPE/START/STOP/FREQUENCY/DURATION//
#
###########################################################################
def parseAPERIOD(record, year):
    utils.common.OutputMessage(logging.DEBUG, "{0} ProcessGeometry.parseAPERIOD()".format(time.ctime()))
    json        = {}
    items       = record.split('/')
    type        = items[1]
    startDate   = parseDate(items[2] + str(year))
    stopDate    = parseDate(items[3] + str(year))
    start       = getDateString(startDate)
    stop        = getDateString(stopDate)
    frequency   = ''
    duration    = ''
    if type.upper() == 'INTERVAL':
        frequency   = items[4]
        duration    = items[5]
    json['APERIOD'] = { 'type': type, 'start': start, 'stop': stop, 'frequency': frequency, 'duration': duration  }
    return json

###########################################################################
# Parse a CIRCLE block into Esri geometry JSON.
# Assume the CIRCLE block is in the form:
# CIRCLE/LATS:580429N0042748W/15KM//
# Uses a buffer tool to buffer the lat long by the specified distance.
#
###########################################################################
def parseCIRCLE(record,height):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseCIRCLE()".format(time.ctime()))

    items = record.split('/')
    centreLatLong = parseLatLong(items[1],height)
    (distance, units) = parseDistance(items[2])
    circle = createBufferedPoint(centreLatLong[0], centreLatLong[1], distance, units, 4326)

    objJson = copy.copy(json.loads(circle))
    
    objJson['hasZ'] = True
    for i in range(0, len(objJson['rings'][0])):
        objJson['rings'][0][i].append(height)
        
    return objJson

###########################################################################
# Create a buffered point from a lat, long, distance and units.
#
###########################################################################
def createBufferedPoint(x, y, distance, units, sr):

    centerPoint = arcpy.Point()
    centerPoint.X = x
    centerPoint.Y = y
    centerPoint.Z = 0

    centerPointGeometry = arcpy.PointGeometry(centerPoint, arcpy.SpatialReference(sr), False, False)

    outGeomList = arcpy.Buffer_analysis(centerPointGeometry, r'in_memory\tempBuffer', '%s %s' % (distance, units), None, None, 'ALL')

    geoms = []
    rows = arcpy.SearchCursor(r'in_memory\tempBuffer')
    row = next(rows)
    while row != None:
        geom = row.shape
        geoms.append(geom)
        row = next(rows)

    del row
    del rows

    arcpy.Delete_management(r'in_memory\tempBuffer')
    
    return geoms[0].JSON

############################################################################
#
# AMSNDAT/15JW4002/-/-/-/ASW/-/-/DEPLOC:EGQS/ARRLOC:EGQS//
# AMSNDAT/MISSIONNO/AMCNO/PACKAGEID/COMMANDER/1STMISSIONTYPE/2NDMISSIONYPE/DEPARTURELOC/RECOVERYLOC//
#
###########################################################################
def parseAMSNDAT(record):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseAMSNDAT()".format(time.ctime()))
    items = record.split('/')
    return { 'title': items[1], 'missionno': items[1], 'packageId': items[3], 'commander': items[4], 'missionType': items[5], 'departureLocation': items[7], 'recoveryLocation': items[8] }

###########################################################################
# Parse a parseAMSNLOC block into Esri geometry JSON.
# Assume the POLYGON block is in the form:
# AMSNLOC/141230ZAPR/141630ZAPR/ISLAY/150/1/LATM:5720N01000W/LATM:5720N00720W/LATM:5650N00720W/LATM:5650N00500W/LATM:5540N00500W/LATM:5540N01000W//
#
###########################################################################
def parseAMSNLOC(record, year):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseAMSNLOC()".format(time.ctime()))

    items = record.split('/')

    startDate   = parseDate(items[1] + str(year))
    stopDate    = parseDate(items[2] + str(year))
    start       = getDateString(startDate)
    stop        = getDateString(stopDate)
    id          = items[3]
    height      = 0
    if len(items) > 7: height = float(items[4]) * 100

    #json['geometry'] = {}
    #json['geometry']['spatialReference'] = {"wkid" : 4326}
    #json['geometry']['paths'] = [[]]

    #for i in items:
    #    if i.startswith('LATM') == True:
    #        json['geometry']['paths'][0].append(parseLatLong(i))
    #        pass

    json = []
    for i in items:
        if i.startswith('LATM') == True:
            
            location = parseLatLong(i)
            geoJson = {}
            geoJson['type']    = 'AMSNLOC'
            geoJson['id']      = id
            geoJson['start']   = start
            geoJson['stop']    = stop
            geoJson['height']  = height
            geoJson['geometry'] = {}
            geoJson['geometry']['spatialReference'] = {"wkid" : 4326}
            geoJson['geometry']['x'] = location[0]
            geoJson['geometry']['y'] = location[1]
            geoJson['geometry']['z'] = height * 0.3048
            geoJson['SORTORDER'] = len(json) + 1

            json.append(geoJson)
            pass
            
    return json

###########################################################################
# Parse a TASKUNIT block, assumes block is in the form:
# TASKUNIT/BEN0001/ICAO:LEOP/BNS//
#
###########################################################################
def parseTASKUNIT(record):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseTASKUNIT()".format(time.ctime()))
    items = record.split('/')
    return { 'taskUnit': items[1], 'location': items[2] }

###########################################################################
# Parse a TSKCNTRY block, assumes block is in the form:
# TSKCNTRY/SP//
#
###########################################################################
def parseTSKCNTRY(record):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseTSKCNTRY()".format(time.ctime()))
    items = record.split('/')
    return { 'country': items[1] }

############################################################################
#
# MSNACFT/1/OTHAC:ALOU/BLUEBIRD01/BA/-/140/30022//
# MSNACFT/1/OTHAC:ALOU/BLUEBIRD01/BA/-/140/30022//
#
###########################################################################
def parseMSNACFT(record):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseMSNACFT()".format(time.ctime()))
    items = record.split('/')
    return { 'aircraftCount': items[1], 'aircraftType': items[2], 'callsign': items[3], 'primeConfig': items[4], 'secondConfig': items[5] }

############################################################################
# Parse a GTGTLOC block (GROUND TARGET LOCATION):
# GTGTLOC/P/TOT:141310ZAPR/NET:141300ZAPR/NLT:141345Z/DRAGONIA SAM SI/ID:0044NS0001-NS101/-/CONTROL ROOM/DMPIT:5503.0146N00233.2405W/W84/-/-/2//
#
###########################################################################
def parseGTGTLOC(record):
    utils.common.OutputMessage(logging.DEBUG, "{0} parseGTGTLOC()".format(time.ctime()))

    items = record.split('/')

    elevation = 0
    if not '-' in items[11]: elevation = float(items[11]) * 100

    json = {}
    json['type']            = 'GTGTLOC'
    json['designator']      = items[1]
    json['timeOnTarget']    = items[2]
    json['notEarlierThan']  = items[3]
    json['notLaterThan']    = items[4]
    json['targetName']      = items[5]
    json['targetId']        = items[6]
    json['targeType']       = items[7]
    json['desc']            = items[8]
    json['geodeticDatum']   = items[10]
    json['elevation']       = elevation
    json['priority']        = items[13]

    geometry                = parseLatLong(items[9])
    json['geometry'] = {}
    json['geometry']['spatialReference'] = {"wkid" : 4326}
    json['geometry']['x'] = geometry[0]
    json['geometry']['y'] = geometry[1]
    json['geometry']['z'] = elevation * 0.3048

    return json

###########################################################################
# Parse a TIMEFRAM block into JSON.
# Assume the block is in the form:
# TIMEFRAM/FROM:140600ZAPR2015/TO:150559ZAPR2015/ASOF:140920ZAPR2015//
#
###########################################################################
def _parseBlockTIMEFRAM(record):
    utils.common.OutputMessage(logging.DEBUG, "{0} ProcessGeometry.parseTIMEFRAM()".format(time.ctime()))

    items       = record.split('/')

    startDate   = parseDate(items[1].replace('FROM:', ''))
    stopDate    = parseDate(items[2].replace('TO:', ''))
    asOfDate    = parseDate(items[3].replace('ASOF:', ''))

    json        = {}
    start       = getDateString(startDate)
    stop        = getDateString(stopDate)
    asof        = getDateString(asOfDate)

    return { 'start': start, 'stop': stop, 'asof': asof }
