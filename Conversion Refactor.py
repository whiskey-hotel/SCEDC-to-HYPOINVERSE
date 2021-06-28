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


def ManString(regex, line):
    """Use a regular expression to manipulate a
string into a list.

    Args:
        line (str): Original string
        regex (str): Regular expression. Use quotations
    """
    new_list = re.split(regex, line)
    return new_list


def DeciRemove(num, multiplier, type):
    """The Hypo header cannot have decimals in it.
    This function shifts the decimal of num based on 
    the multiplier. The returned data type can be manipulated 
    further with string formatting methods. 

    Args:
        num (str or float):
        multiplier (int): 
        type (any): The data type to return
    """
    num = round(float(num) * multiplier)
    return type(num)


def DegToMin(degrees):
    """This will convert (Lat,Long) decimal degrees to minutes

    Args:
        degrees (int): (Lat,Long) decimal degrees
    """
    degrees = ManString('[.]', degrees)
    minutes = float(degrees[1]) * 60
    return minutes


def station_formatting(station_info):
    station_site_code = station_info[1]
    network_code_station = station_info[0]
    component_code_station = station_info[2]

    lat_deg_station = station_info[-7]
    if float(lat_deg_station) == abs(float(lat_deg_station)):
        lat_sign_station = " "
    else:
        lat_sign_station = "S"
        lat_deg_station = str(abs(float(lat_deg_station)))
    lat_min_station = str(DegToMin(station_info[-7]))

    long_deg_station = station_info[-6]
    if float(long_deg_station) == abs(float(long_deg_station)):
        long_sign_station = "E"
    else:
        long_sign_station = " "
        long_deg_station = str(abs(float(long_deg_station)))
    long_min_station = str(DegToMin(station_info[-6]))
    elevation = station_info[-5]
    loc_code_station = station_info[3]

    hypo_station.write(f'\n\
{station_site_code: <5.5}\
{network_code_station: >2.2}\
{component_code_station: >5.3}\
{lat_deg_station: >4.2}\
{lat_min_station: >8.7}\
{lat_sign_station: >1.1}\
{long_deg_station: >3.3}\
{long_min_station: >8.7}\
{long_sign_station: >1.1}\
{elevation: >4.4}\
{loc_code_station: >40.2}\n')
    return


# The SCEDC phase file you want to alter
scedc_phase_file = open('scedc_ws_phase_copy.txt', 'r')
scedc_phase = list(scedc_phase_file)
# The returned HYPOINVERSE phase file
hypo_phase = open('Converted_scedc_phase_info.txt', 'w')
# The SCEDC station file
scedc_station_file = open('scedc_ws_station.txt', 'r')
scedc_station = list(scedc_station_file)
#
# The returned HYPOINVERSE station file for this event
hypo_station = open('Converted_scedc_station_info.txt', 'w')

################ Header formating #################

scedc_header = ManString('[:,\\/\\s]', scedc_phase[0])

year = scedc_header[6]
month = scedc_header[7]
day = scedc_header[8]
hour = scedc_header[9]
min = scedc_header[10]
sec = DeciRemove(scedc_header[11], 1000, str)
lat_deg = scedc_header[14]
if float(lat_deg) == abs(float(lat_deg)):
    lat_sign = " "
else:
    lat_sign = "S"
    lat_deg = str(abs(float(lat_deg)))
lat_min = str(DegToMin(scedc_header[14]))
long_deg = scedc_header[17]
if float(long_deg) == abs(float(long_deg)):
    long_sign = "E"
else:
    long_sign = " "
    long_deg = str(abs(float(long_deg)))
long_min = str(DegToMin(scedc_header[17]))
depth = DeciRemove(scedc_header[20], 100, float)
amp_mag = DeciRemove(scedc_header[22], 100, float)
id = scedc_header[2]

hypo_phase.write(f'\
{year: >4.4}\
{month: >2.2}\
{day: >2.2}\
{hour: >2.2}\
{min: >2.2}\
{sec: >4.4}\
{lat_deg:0>2.2}\
{lat_sign: >.1}\
{lat_min: >.4}\
{long_deg:0>3.3}\
{long_sign: >.1}\
{long_min: >.4}\
{depth: >5.5n}\
{amp_mag:0>3.3n}\
{" ": >99}\
{id: >}\
\n')

################ Phase formating #################

# Remove header information from the list
scedc_phase.pop(0)
# Split the station file
station_list = [re.split('\\s+', scedc_station[count]) for count, line in enumerate(scedc_station)]
# make new list of all station code names
station_names = [station[1] for station in station_list]
used_station_names = []
# compare station code to the station names
# write the station into a file with station func.
# add the station to a list.
# if the station is in the list, skip the
# the station formatting function

for count, line in enumerate(scedc_phase):
    scedc_phase_line = ManString('\\s+', scedc_phase[count])
    station_code = scedc_phase_line[2]
    if station_code not in used_station_names:
        index = station_names.index(station_code)
        station_formatting(station_list[index])  # station function
        used_station_names.append(station_code)
    network_code = scedc_phase_line[1]
    component_code = scedc_phase_line[3]
    signal_quality = scedc_phase_line[10].upper()
    phase = scedc_phase_line[8]
    if phase == "P":
        if scedc_phase_line[9] == "..":
            P_FirstMotion = " "
        elif scedc_phase_line[9] == "d.":
            P_FirstMotion = "D"
        elif scedc_phase_line[9] == "c.":
            P_FirstMotion = "U"
    YearMonthDayHourMin = year + month + day + min
    first_arrival = DeciRemove(scedc_phase_line[13], 100, float)
    epi_distance = DeciRemove(scedc_phase_line[12], 100, float)
    loc_code = scedc_phase_line[4]

    if phase == "P":
        hypo_phase.write(f'\
{station_code: <5.5}\
{network_code: >2.2}\
{component_code: >5.3}\
{signal_quality: >2.1}\
{phase: >1.1}\
{P_FirstMotion: >1.1}\
{YearMonthDayHourMin: >13.12}\
{first_arrival: >5.4n}\
{epi_distance: >30.4n}\
{loc_code: >48.2}\
\n')
    else:
        hypo_phase.write(f'\
{station_code: <5.5}\
{network_code: >2.2}\
{component_code: >5.3}\
{YearMonthDayHourMin: >17.12}\
{first_arrival: >17.4n}\
{signal_quality: >1.1}\
{phase: >1.1}\
{epi_distance: >16.4n}\
{loc_code: >48.2}\
\n')

################ Terminator Line #################
hypo_phase.write(f'{id: >72.10}')


scedc_phase_file.close()
hypo_phase.close()
scedc_station_file.close()
hypo_station.close()
