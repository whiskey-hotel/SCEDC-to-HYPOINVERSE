# -------------------------------------------------------------------------------
# Name:       SCEDC(STP)_to_Hypo_Phase_Conversion_Refactor.py
# Purpose:    Rearranges configuration variables
#			  from SCEDC phase file format to
#			  Hypoinverse phase file format.
#			  Position of each variable is denoted in the STP
#			  to HYPOINVERSE guide.
#
# Author:      Jusin Thornton
#
# Created:     06/05/2021
#
# Version:     0.1.0
# -------------------------------------------------------------------------------

import re


def man_string(regex, line):
    """Use a regular expression to manipulate a
string into a list.

    Args:
        line (str): Original string to manipulate
        regex (str): Regular expression. Use quotations
    """
    new_list = re.split(regex, line)
    return new_list


def deci_remove(num, multiplier, type):
    """The Hypo header cannot have decimals in it.
    This function shifts the decimal of num based on 
    the multiplier. The returned float can be manipulated 
    further with string formatting methods. 

    Args:
        num (str or float):
        multiplier (int):
        type (any): The data type returned
    """
    num = round(float(num) * multiplier)
    return type(num)


def deg_to_min(degrees):
    """This will convert (Lat,Long) decimal degrees to minutes

    Args:
        degrees (int): (Lat,Long) decimal degrees
    """
    degrees = man_string('[.]', degrees)
    minutes = float(degrees[1]) * 60
    return minutes


# The SCEDC phase file you want to alter
scedc_phase_file = open('scedc_ws_phase_copy.txt', 'r')
scedc_phase = list(scedc_phase_file)
# The returned HYPOINVERSE phase file
hypo_phase = open('Converted_scedc_phase_info.txt', 'w')
# The SCEDC station file
scedc_station_file = open('Converted_scedc_station_info.txt', 'r')
scedc_station = list(scedc_station_file)
# The returned HYPOINVERSE station file for this event
hypo_station = 'Event_37509232_station_file'

################ Header formating #################

scedc_header = man_string('[:,\\/\\s]', scedc_phase[0])

year = scedc_header[6]
month = scedc_header[7]
day = scedc_header[8]
hour = scedc_header[9]
min = scedc_header[10]
sec = deci_remove(scedc_header[11], 1000, str)
LatDeg = scedc_header[14]
if float(LatDeg) == abs(float(LatDeg)):
    LatSign = " "
else:
    LatSign = "S"
    LatDeg = str(abs(float(LatDeg)))
LatMin = str(deg_to_min(scedc_header[14]))
LongDeg = scedc_header[17]
if float(LongDeg) == abs(float(LongDeg)):
    LongSign = "E"
else:
    LongSign = " "
    LongDeg = str(abs(float(LongDeg)))
LongMin = str(deg_to_min(scedc_header[17]))
depth = deci_remove(scedc_header[20], 100, float)
AmpMag = deci_remove(scedc_header[22], 100, float)
ID = scedc_header[2]

hypo_phase.write(f'\
{year: >4.4}\
{month: >2.2}\
{day: >2.2}\
{hour: >2.2}\
{min: >2.2}\
{sec: >4.4}\
{LatDeg:0>2.2}\
{LatSign: >.1}\
{LatMin: >.4}\
{LongDeg:0>3.3}\
{LongSign: >.1}\
{LongMin: >.4}\
{depth: >5.5n}\
{AmpMag:0>3.3n}\
{" ": >99}\
{ID: >}\
\n')

################ Phase formating #################
scedc_phase.pop(0)
#scedc_station = man_string('[:,\\/\\s]', scedc_station)

for count, line in enumerate(scedc_phase):
    scedc_phase_line = man_string('\s+', scedc_phase[count])
    StationCode = scedc_phase_line[2]
    NetworkCode = scedc_phase_line[1]
    ComponentCode = scedc_phase_line[3]
    SignalQuality = scedc_phase_line[10].upper()
    Phase = scedc_phase_line[8]
    if Phase == "P":
        if scedc_phase_line[9] == "..":
            P_FirstMotion = " "
        elif scedc_phase_line[9] == "d.":
            P_FirstMotion = "D"
        elif scedc_phase_line[9] == "c.":
            P_FirstMotion = "U"
    YearMonthDayHourMin = year + month + day + min
    FirstArrival = deci_remove(scedc_phase_line[13], 100, float)
    EpiDistance = deci_remove(scedc_phase_line[12], 100, float)
    LocCode = scedc_phase_line[4]
    if Phase == "P":
        hypo_phase.write(f'\
{StationCode: <5.5}\
{NetworkCode: >2.2}\
{ComponentCode: >5.3}\
{SignalQuality: >2.1}\
{Phase: >1.1}\
{P_FirstMotion: >1.1}\
{YearMonthDayHourMin: >13.12}\
{FirstArrival: >5.4n}\
{EpiDistance: >30.4n}\
{LocCode: >48.2}\
\n')
    else:
        hypo_phase.write(f'\
{StationCode: <5.5}\
{NetworkCode: >2.2}\
{ComponentCode: >5.3}\
{YearMonthDayHourMin: >17.12}\
{FirstArrival: >17.4n}\
{SignalQuality: >1.1}\
{Phase: >1.1}\
{EpiDistance: >16.4n}\
{LocCode: >48.2}\
\n')

################ Terminator Line #################
hypo_phase.write(f'{ID: >72.10}')

scedc_phase_file.close()
hypo_phase.close()
scedc_station_file.close()
