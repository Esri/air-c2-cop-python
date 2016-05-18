AVDAFIF

AVDAFIF is the DAFIF Fullfile converted into datasets that are 
ready to use by the commercial software package "ArcGIS" by ESRI 
Corporation.  The software may be obtained by calling:

	Environmental Systems Research Institute (ESRI)
	1-800-447-9778
	909-793-2853
	www.esri.com


	NGA has tried to maintain a similar naming convention with 
those of the MIDAFIF Datasets.  However, due to differences in the way 
ArcView and MapInfo manage their data layers, there will be variations.
Please refer to the following descriptions of the filenames for 
assistance.

THE CURRENT LAYOUTS FOR THE FILES ARE IN EACH FOLDER,
REFERENCE DAFIF EDITION 8, FOLDER - DOCS, ED8, SPEC, APP_IV FOR MORE INFORMATION.

NOTE: THERE MAY BE A SLIGHT DIFFERENCE IN A FEW ATTRIBUTE NAMES DUE TO THE CONVERSION FROM 
THE FULLFILES TO ARCVIEW. WHILE THE DIFFERENCES ARE MINOR, PLEASE BE AWARE OF THEIR EXISTANCE.


AVDAFIF Datasets

	ARF  (Air Refueling)
ARFLN.SHP	(line features)	
ARFPAR.SHP     	(parent data collocated with the first point)
ARFPT.SHP	(point features)
ARFRMK.SHP	(remarks data collocated with the first point)
ARFSEG_A.SHP	(segment line features)
ARFSGP.SHP	(airspace polygon features)

	ARPT  (Airports)		
ACOM.SHP        (airport communications)
ACOMRM.SHP	(communications remarks)
ANAV.SHP	(airport navaids)
ARPT.SHP      	(airport reference points)

	ATS  (Airways)		
ATSH.SHP        (high altitude airways)
ATSL.SHP	(low altitude airways)

	BDRY  (Boundaries)
BDRYC.SHP	(country records)
BDRYC_E.SHP	(country ellipses)
BDRYH.SHP	(high altitude curves)
BDRYH_E.SHP	(high altitude ellipses)
BDRYHP.SHP	(high altitude parent records)
BDRYL.SHP	(low altitude curves)
BDRYL_E.SHP	(low altitude ellipses)
BDRYLP.SHP	(low altitude parent records)

	CUSTSYMB
Custom Point Symbols

	HLPT  (Heliports)
HCOM.SHP	(heliport communications)
HCOMRM.SHP	(heliport communication remarks)
HLPT.SHP	(heliport reference points)
HNAV.SHP	(heliport navaids)
PAD.SHP		(heliport landing area reference points)
PAD_P.SHP	(heliport landing area parent records)
PADSYM.SHP	(heliport landing area symbol)

	HOLD  (Holding Pattern)
HOLDH_P.SHP	(high altitude holding point features)
HOLDL_P.SHP	(low altitude holding point features)
HOLDPTNH_L.SHP	(high altitude holding pattern line features)
HOLDPTNL_L.SHP	(low altitude holding pattern line features)
HOLDPTNT_L.SHP	(terminal holding pattern line features)
HOLDT_P.SHP	(terminal holding point features)

	IR  (ICAO Regions)
IRC.SHP		(country records)
IRH.SHP		(high altitude polygons)
IRHP.SHP	(high altitude parent records)
IRL.SHP		(low altitude polygons)
IRLP.SHP	(low altitude parent records)

	MTR  (Military Training Routes)
MTRIR_L.SHP	(instrument route line features)
MTRIR_P.SHP	(instrument route point features)
MTRIRS.SHP	(instrument route symbols)
MTROV_IR_L.SHP	(instrument route overlay line features)
MTROV_IR_P.SHP	(instrument route overlay point features)
MTROV_SR_L.SHP	(slow route overlay line features)
MTROV_SR_P.SHP	(slow route overlay point features)
MTROV_VR_L.SHP	(visual route overlay line features)
MTROV_VR_P.SHP	(visual route overlay point features)
MTRPAR.SHP	(parent records)
MTRRMK.SHP	(remark records, tied to end point)
MTRSR_L.SHP	(slow route line features)
MTRSR_P.SHP	(slow route point features)
MTRSRS.SHP	(slow route symbols)
MTRVR_L.SHP	(visual route line features)
MTRVR_P.SHP	(visual route point features)
MTRVRS.SHP	(visual route symbols)

	NAV  (Navaids)
NAVH.SHP        (high altitude navaids)
NAVL.SHP     	(low altitude navaids)
NAVT.SHP	(terminal navaids)

	ORTCA  (Off Route Terrain Clearance Altitude)
ORTCA.shp  (one degree cells with an assigned altitude)


	PAPP  (RNAV Precision Approach Path Points)
(NOTE: currently there are no records for PAPP)

	PJA  (Parachute Jumping Areas)
PJA.SHP		(segment polygon features)
PJA_E.SHP	(ellipsoid features)
PJA_P.SHP	(point features)
PJAPAR.SHP	(parent records)
PJAPAR_L.SHP	(segment line records)

	RWY  (Runways)		
AGEAR.SHP    	(arresting system symbols)
ARR.SHP        	(arresting system text ONLY)
ILS.SHP		(instrument landing system symbols)
RUNWAY.SHP	(runway patterns)
RUNWAY_P.SHP	(runway pattern line features)
RWY.SHP		(runway textual data)
RWYDT.SHP	(displaced threshold patterns)
RWYDT_P.SHP	(displaced threshold line features)

	SUAS  (Special Use Airspace)
SUASC.SHP	(country records)
SUASH.SHP	(high altitude curves)
SUASH_E.SHP	(high altitude ellipses)
SUASH_P.SHP	(high altitude points)
SUASHP.SHP	(high altitude parent records)
SUASL.SHP	(low altitude curves)
SUASL_E.SHP	(low altitude ellipses)
SUASL_P.SHP	(low altitude points)
SUASLP.SHP	(low altitude parent records)

	SUPP  (Airport/Heliport supplemental data)
ADDRWY.SHP	(threshold and overrun coordinates)
ADDRWY_R.SHP	(overrun ellipses)
FUELOIL.SHP	(fuel, oil, fluids information)
GEN.SHP		(general textual information, NOTAM service, city cross reference, etc)
SVCRMK.SHP	(Service and Remarks, data from DoD enroute supplements)

(NOTE: SUPP data tied to airport/heliport reference point)
(NOTE: SUPPH data is the same directory and format as SUPP)

	TRM  (Terminals Approaches)
Subfolder name: AFR, CAN, CSA, EEA, ENM, PAA, USC, USE, USW
Followed by:
  CLB.SHP	(climb rate information)
  FDR.SHP	(feeder route information)
  MIN.SHP	(approach minimum information)
  MSA.SHP	(minimum sector altitude information)
  PAR.SHP	(parent records)
  REF.SHP	(reference data, navaids, waypoints, etc)
  REF_P.SHP	(reference date point features)
  REF_R.SHP	(reference data ellipses)
  RMK.SHP	(remarks information)
  TRM.SHP	(segment line features)
  TRM_N.SHP	(segment line features for "TF" legs where the difference 
   		  between ALT_1 and ALT_2 is null)
  TRM_P.SHP	(segment point features)

(NOTE: example: AFRMIN.TAB, CANMSA.TAB, etc)
(NOTE: TRMH data is the same directory and format as TRM)

	TZ  (Time Zones)
TZ_L.SHP	(time zone segment line features)
TZ_R.SHP	(time zone parent and ellipse features)

	VFR  (VFR Arrival/Departures Korea/Europe)
VFR.SHP		(vfr route segment line features)
VFRHLD.SHP	(vfr holding ellipse features)
VFRL.SHP	(vfr left offset segment line features)	
VFRLP.SHP	(vfr left offset point features)
VFRP.SHP	(vfr route point features)
VFRR.SHP	(vfr right offset segment line features)
VFRRMK.SHP	(vfr remarks data)
VFRRP.SHP	(vfr right offset point features)

	WPT  (Waypoints)
WPTH_P.SHP	(high altitude point features)
WPTL_P.SHP	(low altitude point features)
WPTT_P.SHP	(terminal point features)


 
