#!/usr/bin/perl  -w

#PERL PROGRAM NAME: SCEDC(STP)_to_Hypo_Station_Conversion.pl 
#AUTHOR: Justin Thornton
#DATE: August 15, 2018 
#DESCRIPTION: Rearranges configuration variables
#             from SCEDC station text file format to 
#			  Hypoinverse station file format.
#			  Position of each variable is denoted in the STP 
#			  to HYPOINVERSE guide.

use strict;
use warnings;



my $filename = 'scedc_ws_station.txt'; #The file you want to alter
my $newfilename = 'Converted_scedc_station_info.txt'; #The name of the new file 

open(my $FH,'<',$filename)or die "Could not open file '$filename' $!";

	my @Master = <$FH>;
	chomp @Master;
	
close $FH;


open(my $fh,'>',$newfilename)or die "Could not open file '$newfilename' $!";
	
		for my $Mister (@Master){
			my @StationSiteCode = split(/[:,\s\/]+/, $Mister);
			my $StationSiteCode = $StationSiteCode[1];
			printf $fh ("%-6s", "$StationSiteCode");
		
			my @NetworkCode = split(/[:,\s\/]+/, $Mister);
			my $NetworkCode = $NetworkCode[0];
			printf $fh ("%-4s", "$NetworkCode");
			
			my @Component = split(/[:,\s\/]+/ , $Mister);
			my $Component = $Component[2];
			printf $fh ("%-5s", "$Component");
			
			my @LatDegTemp = split(/\s+/, $Mister);
			@LatDegTemp = reverse @LatDegTemp;
			splice (@LatDegTemp,6);
			@LatDegTemp = reverse @LatDegTemp;
			my $LatDeg = $LatDegTemp[0];
			my @LatDeg = split(/[.:,\s\/]+/ , $LatDeg);
				if ($LatDeg[0] == abs($LatDeg[0])){
					printf $fh ("%-3s", "$LatDeg[0]");
				}else{
					my $LatDeg = $LatDeg[0] * -1;
					printf $fh ("%-3s", "$LatDeg");
				}
			
			my $LatMin = $LatDeg[1];
			$LatMin =  $LatMin / 100000;		#This will convert Latitude decimal degrees to 
			$LatMin = $LatMin * 60; 			#Latitude decimal minutes
			printf $fh ("%7.4f", "$LatMin");
		
			if ($LatDeg[0] == abs($LatDeg[0])){
					my $LatSign = " ";
					printf $fh ("%1s", "$LatSign");
				}else{
					my $LatSign = "S";
					printf $fh ("%1s", "$LatSign");
				}
				
			my @LongDegTemp = split(/\s+/, $Mister);
			@LongDegTemp = reverse @LongDegTemp;
			splice (@LongDegTemp,6);
			@LongDegTemp = reverse @LongDegTemp;
			my $LongDeg = $LongDegTemp[1];
			my @LongDeg = split(/[.:,\s\/]+/ , $LongDeg);
			if ($LongDeg[0] == abs($LongDeg[0])){
					printf $fh ("%-4s", "$LongDeg[0]");
				}else{
					my $LongDeg = $LongDeg[0] * -1;
					printf $fh ("%-4s", "$LongDeg");
				}
			
			my $LongMin = $LongDeg[1];
			$LongMin =  $LongMin / 100000;		#This will convert Longitude decimal degrees
			$LongMin = $LongMin * 60; 			#to Longitude decimal minutes
			printf $fh ("%7.4f", "$LongMin");
		
			if ($LongDeg[0] == abs($LongDeg[0])){
					my $LongSign = "E"; 		#Hypoinverse states that west is positive
					printf $fh ("%1s", "$LongSign");
				}else{
					my $LongSign = " ";
					printf $fh ("%1s", "$LongSign");
				}
		
			my @ElevationTemp = split(/\s+/, $Mister);
			@ElevationTemp = reverse @ElevationTemp;
			splice (@ElevationTemp,6);
			my @Elevation = reverse @ElevationTemp;
			my $Elevation = $Elevation[2];
			printf $fh ("%4s", "$Elevation");
			
			printf $fh ("%38s", ""); 	#filler space
			
			my @LocCode = split(/\s+/, $Mister);
			my $LocCode = $LocCode[3];
			printf $fh ("%2s\n", "$LocCode");
		}
		
		
close $fh;	

my $Master = @Master;
print "Process Complete\n";
print "$Master stations are located in '$newfilename'\n";

