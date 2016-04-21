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
import json

import config
import utils.common

###########################################################################
# Class to write an ACO to a GDB.
# Process the block types:
#
###########################################################################
class ACOWriter:

    _sourceJson = None
    _targetWS   = None

    def __init__(self):
        pass

    def execute(self, sourceJson, targetWS):
        utils.common.OutputMessage(logging.DEBUG, "{0} ACOWriter.execute() - Start".format(time.ctime()))

        utils.common.OutputMessage(logging.DEBUG, "Target Workspace: " + targetWS)
        
        #Check if header has EXER block or OPER block
        if 'EXER' in sourceJson['header']:
            id      = sourceJson['header']['EXER']['id']       
        if 'OPER' in sourceJson['header']:
            id      = sourceJson['header']['OPER']['id']
        
        name    = sourceJson['header']['AMPN']['title']
        file    = sourceJson['metadata']['filename']

        self._insertHeader(targetWS, id, name, file)
        self._insertGeometry(targetWS, id, sourceJson)

        utils.common.OutputMessage(logging.DEBUG, "{0} ACOWriter.execute() - Finish".format(time.ctime()))

        pass

    def _insertHeader(self, targetWS, id, name, filename):
        utils.common.OutputMessage(logging.DEBUG, "{0} ACOWriter._insertHeader() - Start".format(time.ctime()))

        values  = [id, name, filename]

        table   = '%s/AMS_RECORD' % (targetWS)
        fields  = ['AMSID', 'NAME', 'FILENAME']

        cursor  = arcpy.da.InsertCursor(table, fields)
        row     = cursor.insertRow(values)

        del row
        del cursor

        utils.common.OutputMessage(logging.DEBUG, "{0} ACOWriter._insertHeader() - Finish".format(time.ctime()))

    def _insertGeometry(self, targetWS, amsId, sourceJson):
        utils.common.OutputMessage(logging.DEBUG, "{0} ACOWriter._insertGeometry() - Start".format(time.ctime()))

        fields          = ['AMSID', 'ID', 'NAME', 'USE', 'EFFLEVEL', 'MIN_HEIGHT', 'MAX_HEIGHT', 'EXT_HEIGHT', 'SHAPE@JSON']
        valuesPolygon   = []
        valuesLine      = []
        valuesPoint     = []

        geometryRecords = sourceJson['geometry']
        for item in geometryRecords:
            record = item['ACMID']
            if ('geometry' in record) == True:
                id      = record['id']
                name    = record['name']
                type    = record['type']
                use     = record['use']
                level   = record['efflevel']['label']
                min     = record['efflevel']['min_height']
                max     = record['efflevel']['max_height']
                extrude = record['efflevel']['ext_height']
                geom    = json.dumps(record['geometry'])
                
                utils.common.OutputMessage(logging.DEBUG, record['name'])
                
                if type.upper() == 'GEOLINE':
                    valuesLine.append((amsId, id, name, use, level, min, max, extrude, geom))
                elif type.upper() == 'LINE':
                    valuesLine.append((amsId, id, name, use, level, min, max, extrude, geom))
                elif type.upper() == 'CORRIDOR':
                    valuesPolygon.append((amsId, id, name, use, level, min, max, extrude, geom))
                elif type.upper() == 'CIRCLE':
                    valuesPolygon.append((amsId, id, name, use, level, min, max, extrude, geom))
                elif type.upper() == 'POINT':
                    valuesPoint.append((amsId, id, name, use, level, min, max, extrude, geom))
                elif type.upper() == 'POLYGON':
                    valuesPolygon.append((amsId, id, name, use, level, min, max, extrude, geom))
                else:
                    utils.common.OutputMessage(logging.DEBUG, type.upper() + " is not a valid geometry")
            if ('period' in record) == True:
                self._insertPeriods(targetWS, amsId, id, record['period'], record['name'])

        
        # Insert polygon records        
        table   = '%s/ACO_POLYGON' % (targetWS)
        cursor  = arcpy.da.InsertCursor(table, fields)
        for row in valuesPolygon:
            #utils.common.OutputMessage(logging.DEBUG, row)
            cursor.insertRow(row)            
        del cursor

        # Insert line records
        table   = '%s/ACO_LINE' % (targetWS)
        cursor  = arcpy.da.InsertCursor(table, fields)
        for row in valuesLine:
            #utils.common.OutputMessage(logging.DEBUG, row)
            cursor.insertRow(row)
        del cursor
        
        # Insert point records        
        table   = '%s/ACO_POINT' % (targetWS)
        cursor  = arcpy.da.InsertCursor(table, fields)
        for row in valuesPoint:
            cursor.insertRow(row)            
        del cursor

        utils.common.OutputMessage(logging.DEBUG, "{0} ACOWriter._insertGeometry() - Finish".format(time.ctime()))

    def _insertPeriods(self, targetWS, parentAMSID, parentId, periodsJson, periodsName):
        utils.common.OutputMessage(logging.DEBUG, "{0} ACOWriter._insertPeriods() - Start".format(time.ctime()))
        utils.common.OutputMessage(logging.DEBUG, periodsName)
        fields = ['AMSID', 'ID', 'TYPE', 'INDEX', 'PERIOD_FROM', 'PERIOD_TO', 'FREQUENCY', 'DURATION', 'Name' ]
        values = []

        for item in periodsJson:
            record = item['APERIOD']
            values.append((parentAMSID, parentId, record['type'], item['SORTORDER'], record['start'], record['stop'], record['frequency'], record['duration'], periodsName))

        table   = '%s/ACO_PERIOD' % (targetWS)
        cursor  = arcpy.da.InsertCursor(table, fields)
        for row in values:
            cursor.insertRow(row)
        del cursor

        utils.common.OutputMessage(logging.DEBUG, "{0} ACOWriter._insertPeriods() - Finish".format(time.ctime()))

###########################################################################
# Class to write an ATO to a GDB.
# Process the block types:
#
###########################################################################
class ATOWriter:

    _sourceJson = None
    _targetWS   = None

    def __init__(self):
        pass

    def execute(self, sourceJson, targetWS):
        utils.common.OutputMessage(logging.DEBUG, "{0} ATOWriter.execute() - Start".format(time.ctime()))

        utils.common.OutputMessage(logging.DEBUG, sourceJson)
        utils.common.OutputMessage(logging.DEBUG, targetWS)

        self._insertGeometry(targetWS, '', sourceJson)

        utils.common.OutputMessage(logging.DEBUG, "{0} ATOWriter.execute() - Finish".format(time.ctime()))

        pass

    def _insertGeometry(self, targetWS, amsId, sourceJson):
        utils.common.OutputMessage(logging.DEBUG, "{0} ATOWriter._insertGeometry() - Start".format(time.ctime()))

        fields = []
        fields.append('AMSID')
        fields.append('TASK_COUNTRY')
        fields.append('TASK_UNIT')
        fields.append('TASK_UNIT_LOC')
        fields.append('MSN_NO')
        fields.append('MSN_TYPE')
        fields.append('AC_TYPE')
        fields.append('AC_CALLSIGN')
        fields.append('DEP_LOC')
        fields.append('REC_LOC')

        fields.append('TYPE')

        # AMSNLOC ATTRIBUTES
        fields.append('AMSNLOC_START')
        fields.append('AMSNLOC_STOP')
        fields.append('AMSNLOC_ID')
        fields.append('HEIGHT')
        
        # GTGTLOC ATTRIBUTES
        fields.append('GTGT_NLT')
        fields.append('GTGT_TOT')
        fields.append('GTGT_NET')
        fields.append('GTGT_DESIG')
        fields.append('GTGT_TYPE')
        fields.append('GTGT_ID')
        fields.append('GTGT_NAME')
        fields.append('GTGT_DESC')
        fields.append('GTGT_PRIORITY')

        fields.append('TASK_SORT_ORDER')
        fields.append('GEOM_SORT_ORDER')
        fields.append('SHAPE@JSON')

        id = sourceJson['header']['EXER']['id']

        valuesLine = []
        for taskCountry in sourceJson['taskCountries']:
            taskUnits = taskCountry['taskUnits']
            for taskUnit in taskUnits:
                for task in taskUnit['tasks']:
                    record = task['AMSNDAT']
                    for location in record['location']:

                        values = []
                        values.append(id)
                        values.append(taskCountry['country'])
                        values.append(taskUnit['taskUnit'])
                        values.append(taskUnit['location'])
                        values.append(record['missionno'])
                        values.append(record['missionType'])
                        values.append(record['aircraft']['aircraftType'])
                        values.append(record['aircraft']['callsign'])
                        values.append(record['departureLocation'])
                        values.append(record['recoveryLocation'])

                        type = location['type']
                        values.append(type)

                        if type == 'AMSNLOC':
                            # AMSNLOC ATTRIBUTES
                            values.append(location['start'])
                            values.append(location['stop'])
                            values.append(location['id'])
                            values.append(location['height'])
                            values.append('')
                            values.append('')
                            values.append('')
                            values.append('')
                            values.append('')
                            values.append('')
                            values.append('')
                            values.append('')
                            values.append('')
                        else:
                            # GTGTLOC ATTRIBUTES
                            values.append(None)
                            values.append(None)
                            values.append(None)
                            values.append(location['elevation'])
                            values.append(location['notLaterThan'])
                            values.append(location['timeOnTarget'])
                            values.append(location['notEarlierThan'])
                            values.append(location['designator'])
                            values.append(location['targeType'])
                            values.append(location['targetId'])
                            values.append(location['targetName'])
                            values.append(location['desc'])
                            values.append(location['priority'])

                        values.append(record['SORTORDER'])
                        values.append(location['SORTORDER'])
                        values.append(json.dumps(location['geometry']))

                        valuesLine.append(values)

        #geometryRecords = sourceJson['geometry']
        #for item in geometryRecords:
        #    record = item['AMSNDAT']
        #    #utils.common.OutputMessage(logging.DEBUG, record)
        #    if record.has_key('AMSNLOC') == True and record['AMSNLOC'].has_key('geometry') == True and len(record['AMSNLOC']['geometry']['paths']) > 0:
        #        geom    = record['AMSNLOC']['geometry']
        #        id      = ''
        #        name    = ''
        #        use     = ''
        #        level   = ''
        #        valuesLine.append((amsId, id, name, use, level, json.dumps(geom)))

        #utils.common.OutputMessage(logging.DEBUG, valuesLine)

        # Insert line records
        #table   = '%s/ATO_LINE' % (targetWS)
        #cursor  = arcpy.da.InsertCursor(table, fields)
        #for row in valuesLine:
        #    cursor.insertRow(row)
        #del cursor

        # Insert points
        table   = '%s/ATO_POINT' % (targetWS)
        cursor  = arcpy.da.InsertCursor(table, fields)
        for row in valuesLine:
            cursor.insertRow(row)
        del cursor

        utils.common.OutputMessage(logging.DEBUG, "{0} ATOWriter._insertGeometry() - Finish".format(time.ctime()))

###########################################################################
# Write JSON file to target location.
#
###########################################################################
def writeJSON(jsonData, paths):
    utils.common.OutputMessage(logging.DEBUG, "{0} writeJSON() - Start".format(time.ctime()))

    currentPath     = os.path.dirname(os.path.realpath(__file__))
    utils.common.OutputMessage(logging.DEBUG, "{0} writeJSON() - {1}".format(time.ctime(), currentPath))

    targetPath      = [currentPath, '..', '..', '..']
    targetPath      = targetPath + paths
    utils.common.OutputMessage(logging.DEBUG, "{0} writeJSON() - {1}".format(time.ctime(), targetPath))

    currentFile     = os.path.join(*targetPath)

    utils.common.OutputMessage(logging.DEBUG, "{0} writeJSON() - {1}".format(time.ctime(), currentFile))

    with open(currentFile, 'w') as outfile:
        json.dump(jsonData, outfile, indent = 4, ensure_ascii=False)
