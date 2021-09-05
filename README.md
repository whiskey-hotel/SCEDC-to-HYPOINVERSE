# STP to HYPOINVERSE

## Background

I first tackled this project at the request of my former research advisor in college. We were using earthquake data from the **Southern California Earthquake Data Center (SCEDEC) Seismogram Transfer Program (STP)**. STP provided earthquake phase files which could be used for a number projects.

My advisor also utilized the Fortran program **HYPOINVERSE2000** by Fred Klein which could be used for identifying additional properties of an earthquake, including location and magnitude.

The goal of this project was to utilize earthquake phase data from STP with the HYPOINVERSE program. This required me to convert the phase data from STP format to the HYPOINVERSE format.

## Solution

I utilized Perl in my first attempt at this project. In the code you'll find two perl scripts:

-   SCEDC_to_Hypo_Phase_Conversion.pl
-   SCEDC_to_Hypo_Station_Conversion.pl

While they are both functioning, you'll notice that they are a little hard to follow and mostly just "spaghetti code". This is one of my earliest attempts at programming and my only focus was making sure that it worked.

Knowing what I know now, I decided to refactor the code in python. The refactored version is called:

-   Conversion Refactor.py

In this script I try to make the code more readable and maintainable for future features.

## How it works

The PDF filed named _STP to HYPOINVERSE GUIDE_ provides a more in-depth explanation of how to use STP, HYPOINVERSE, and the Perl scripts. Much of this functionality hasn’t changed since refactoring it to python.

Essentially, the script reads the STP phase file into an array, manipulates the array with regular expressions and f-string formatting, then saves the array into a new file with HYPOINVERSE formatting.

The Perl version of this code used a separate station file script since the phase file script was getting lengthy. In the python version, I created a separate function in the file for converting station information.

The current version assumes that you have two saved text files with all STP station data and all STP phase data.

## Upcoming updates

I want to make this script a one stop shop for converting STP data to HYPOINVERSE data and outputting the pertinent HYPOINVERSE results.

-   Use a web scraper to identify STP station information without needing to save a separate text file with all STP station information
-   Make a user prompt with all of the STP request information (i.e. date, time, lat, long, etc)
-   Make a user prompt for all HYPOINVERSE settings
