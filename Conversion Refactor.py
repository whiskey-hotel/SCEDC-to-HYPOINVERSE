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


def deci_remove(num, multiplier):
    """The Hypo header cannot have decimals in it.
    This function gets rid of the decimal.

    Args:
        num (str or float):
        multiplier (int):
    """
    num = float(num) * multiplier
    return num


def deg_to_min(degrees):
    """This will convert (Lat,Long) decimal degrees to minutes

    Args:
        degrees (int): (Lat,Long) decimal degrees
    """
    degrees = man_string('[.]', degrees)
    minutes = float(degrees[1]) * 60
    return minutes


# The phase file you want to alter
scedc_phase = list(open('scedc_ws_phase_copy.txt', 'r'))
# The name of the new phase file
hypo_phase = open('Converted_scedc_phase_info.txt', 'w')
# Station file you're looking inside
scedc_station = 'Converted_scedc_station_info.txt'
# Station file your creating for this event
hypo_station = 'Event_37509232_station_file'


scedc_header = man_string('[:,\\/\\s]', scedc_phase[0])

year = scedc_header[6]
month = scedc_header[7]
day = scedc_header[8]
hour = scedc_header[9]
min = scedc_header[10]
sec = str(deci_remove(scedc_header[11], 1000))
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
depth = deci_remove(scedc_header[20], 100)
AmpMag = deci_remove(scedc_header[22], 100)
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
{depth:0>5.5n}\
{AmpMag:0>3.3n}\
{" ": >99}\
{ID: >}\
')


# print('{:25}'.format(x) ) #prints with 25 spaces before output
