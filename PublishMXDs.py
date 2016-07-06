# Publishes a services to your portal
# A connection to ArcGIS Server must be established in the
#  Catalog window of ArcMap before running this script
import arcpy
import os
#mxd folder location
mxdloc = r c:\\...

for mxd in mxdloc:
	if mxd.endswith(".mxd"):
	
		# Define local variables
		wrkspc = 'C:/AirC2' #Location of files
		mapDoc = arcpy.mapping.MapDocument(wrkspc + '/USA/USA.mxd') #mxd to be processed.
		con = wrkspc + '/connections/arcgis on myserver_6080 (publisher).ags' #ArcGIS server connection file location
			try:


		# Provide other service details
		service = 'USA' #Name of service to be created
		sddraft = wrkspc + service + '.sddraft'
		sd = wrkspc + service + '.sd'
		summary = 'General reference map of the USA'
		tags = 'USA'

		# Create service definition draft
		arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, service, 'ARCGIS_SERVER', con, True, None, summary, tags)

		# Analyze the service definition draft
		analysis = arcpy.mapping.AnalyzeForSD(sddraft)

		# Print errors, warnings, and messages returned from the analysis
		print "The following information was returned during analysis of the MXD:"
		for key in ('messages', 'warnings', 'errors'):
		  print '----' + key.upper() + '---'
		  vars = analysis[key]
		  for ((message, code), layerlist) in vars.iteritems():
			print '    ', message, ' (CODE %i)' % code
			print '       applies to:',
			for layer in layerlist:
				print layer.name,
			print

		# Stage and upload the service if the sddraft analysis did not contain errors
		if analysis['errors'] == {}:
			# Execute StageService. This creates the service definition.
			arcpy.StageService_server(sddraft, sd)

			# Execute UploadServiceDefinition. This uploads the service definition and publishes the service.
			arcpy.UploadServiceDefinition_server(sd, con)
			print "Service successfully published"
		else: 
			print "Service could not be published because errors were found during analysis."

		print arcpy.GetMessages()