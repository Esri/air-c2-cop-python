###ATO Mission Feature Class###

Field Name|Alias|Description
----------|-----|-----------
AMSID|AMSID|Specifies the Air Mission Exercise or Operation Name
TASK_COUNTRY|Tasked Country|Specifies the nationality of the tasked unit
TASK_UNIT|Tasked Unit|Specifies the identity of the tasked unit
TASK_UNIT_LOC|Tasked Unit Location|Specifies the geographic location of the tasked unit
MSN_RES_IND|Residual Mission Indicator|Indicates whether the mission is or will be a residual mission.
MSN_NO|Mission Number|Specifies the identifying number assigned to the mission
MSN_EVT_NO|Mission Event Number|Specifies the mission or event number assigned to the mission
MSN_PACKAGE_ID|Package ID|Specifies the package identifier that designates the composite force package to which the mission is assigned
MSN_TYPE_P|Primary Mission Type|Specifies the code for the primary type of air mission tasked
MSN_TYPE_P|Secondary Mission Type|Specifies the code for the secondary type of air mission tasked
AC_TYPE|Aircraft Type|Specifies the type of aircraft tasked
AC_NUMBER|Number of Aircraft|Specifies the number of aircraft tasked
AC_CALLSIGN|Aircraft Callsign|Specifies the call sign assigned to the mission aircraft
AC_PRIM_CONFIG|Primary Configuration|Specifies the primary configuration load for the tasked aircraft.
AC_SEC_CONFIG|Secondary Configuration|Specifies the secondary configuration load for the tasked aircraft.
DEP_LOC|Departure Location|Specifies the geographic location of departure of the mission
REC_LOC|Recovery Location|Specifies the geographic location of recovery for the mission
ROUTE|Route|Specifies an aerial route of flight
GTGT_ID|Ground Target Id|Specifies the identifier of the desired mean point of impact of weapons on target
GTGT_NAME|Ground Target Name|Specifies the name of the desired mean point of impact of weapons on target
GTGT_DESC|Ground Target Description|Specifies a description of the desired mean point of impact of weapons on target
GTGT_PRIORITY|Ground Target Priority|Specifies the code for the priority assigned to the target
GTGT_DESIG|Ground Target Designation|Specifies designator that classifies the target as primary or alternate
GTGT_TYPE|Ground Target Type|Specifies the target type
GTGT_NLT|Ground Target Not Later Than|Specifies the latest time off the target
GTGT_TOT|Ground Target Time On Target|Specifies the time on target
GTGT_NET|Ground Target Time Not Earlier Than|Specifies the earliest time on target

###ACO Point, Line and Polygon Feature Classes###

Field|Name|Alias	Description
----------|-----|-----------
AMSID|AMSID|Specifies the Air Mission Exercise or Operation Name
ACM|Airspace Control Means|Specifies the type of Airspace control means
NAME|Name|Specifies the type of Airspace control means identifier
USE|Use|Specifies the airspace usage
STATUS|Current Status|Flag to show if control measure is currently in use (ACTIVE or INACTIVE)
EFFLEVEL|Effective Level|Specifies the vertical dimension of the effective level
MIN_HEIGHT|Minimum Height|Specifies the minimum effective level
MIN_HEIGHT_REF|Minimum Height Reference|Specifies what the minimum effective level is relative to (eg. MSL of AGL)
MAX_HEIGHT|Maximum Height|Specifies the maximum effective level
MAX_HEIGHT_REF|Maximum Height Reference|Specifies what the maximum effective level is relative to (eg. MSL of AGL)
EXT_HEIGHT|Extrude Height|Specifies the difference between the minimum and maximum effective level


###ACO Period - Standalone Table###

Field|Name|Alias	Description
----------|-----|-----------
AMSID|AMSID|Specifies the Air Mission Exercise or Operation Name
ID|Airspace Control Means|Specifies the type of Airspace control means identifier
PERIOD|Effective From|Specifies the date and time the Airspace control means is active from
PERIOD_TO|Effective To|Specifies the date and time the Airspace control means is active to
NAME|Name|Specifies the type of Airspace control means identifier (used to link back to the geometry feature classes)

###ATO Gentext - Standalone Table###

Field|Name|Alias	Description
----------|-----|-----------
AMSID|AMSID|Specifies the Air Mission Exercise or Operation Name
TextIndicator|Text Indicator|Sets the context for the message i.e Commanders Guidance
Info|Info|Holds the message content



