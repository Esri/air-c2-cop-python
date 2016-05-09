# air-c2-cop
A collection of scripts and files necessary for the creation of the Defense Solutions Air C2 COP project.

The Air C2 COP is a gallery of maps and apps for an Air Operations Officer to maintain a common operating picture for command and control.These include a 3D web application built in Web AppBuilder for situational awareness and analysis, an operations dashboard for real-time awareness and decision making,and story map journals to brief pre- and post-action. These applications all reference a central web map and web scene integrated with other real-time data inputs analyzed using GeoEvent Extension.

Sections

##Requirements##

###Overview###

This template include scripts and related content for processing Air Control Orders (ACOs) and Air Tasking Orders (ATOs) from source text files (.aco and .ato) into geographic data suitable for presentation within ArcGIS.

The download includes the following content:

  *data - database schema for the processed files  
  *files - sample ACO, ATO files to be processed  
  *logs - container for log files to be created  
  *arcmap - .mxd containing styled feature classes ready for publishing to ArcGIS server  
  *output - container for output files to be created  
  *tools - processing toolbox and related scripts  
  *arcgispro - ArcGIS Pro project  

##Instructions##

###To process an ACO/ATO:###

1. Open ArcCatalog
2. Open the AirspaceManagementTools.tbx in the above tools folder
3. Double click the ProcessACO script
4. Specify parameters:

  *Source File: the source ACO file to be processed (found in files folder)  
  *Target Workspace: the target workspace containing the feature classes to write the ACO to  
  *Log Level: (Optional) - select DEBUG for extended diagnostics  

To process an ATO follow the same steps as above but select the ProcessATO tool.

###To view and share the processed ACO/ATO:###

1. Open the arcmap/AirControlOrder.mxd
2. [Share as a web map](http://server.arcgis.com/en/server/latest/get-started/windows/tutorial-publishing-a-map-service.htm "Tutorial: Publishing a map service")

###To delete an ACO/ATO:###

To delete ACOs run the DeleteACORecord. By default ALL ACOs will be deleted.  
To delete ATOs run the DeleteATORecord. By default ALL ATOs will be deleted.  

##Scripts Overview##

Each tool has a corresponding top level .py file:

ProcessACO - tools\scripts\amt_process_aco.py  
ProcessATO - tools\scripts\amt_process_ato.py  

The overall processes are split into 3 key areas:

1. Reader (tools\scripts\airspacemanagement\reader.py)

2. Parser (tools\scripts\airspacemanagement\parser.py)

3. Writer (tools\scripts\airspacemanagement\writer.py)

  *A set of readers parse the overall '//' delimeted input file into a set of 'records' (records delimited by the //)  
  *ACOReader, ATOReader and related classes control the overall file processing logic  
  *Reader classes delegate to the parser.py methods for parsing individual records into corresponding JSON data  
  *Writer classes write the JSON data into the FGDB  
  *The ACO / ATO files are processed into a JSON data structure  
  *This JSON data structure is then written into the geodatase by the writer classes  
  *The JSON data structure is also written to the output folder for convenience / diagnostics  

To prevent output to the logs folder change the setting in:

*tools\scripts\config\settings.py   LOG_ENABLE_FILE = False

Resources

Issues

Contributing

Licensing
