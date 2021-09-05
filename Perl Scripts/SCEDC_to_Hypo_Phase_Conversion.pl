#!/usr/bin/perl  -w

#PERL PROGRAM NAME: SCEDC(STP)_to_Hypo_Phase_Conversion.pl 
#AUTHOR: Justin Thornton
#DATE: August 18, 2018 
#DESCRIPTION: Rearranges configuration variables
#			  from SCEDC phase file format to 
#			  Hypoinverse phase file format.
#			  Position of each variable is denoted in the STP 
#			  to HYPOINVERSE guide.
#Version:     1.0.1

use strict;
use warnings;
use Data::Dumper qw(Dumper);

my $filename = '../STP Data/scedc_ws_phase_copy.txt'; #The phase file you want to alter
my $newfilename = '../HYPOINVERSE Data/Converted_scedc_phase_info.txt'; #The name of the new phase file 
my $main_station = '../HYPOINVERSE Data/Converted_scedc_station_info.txt'; #Station file you're looking inside
my $phase_station = '../STP Data/Event_37509232_station_file'; #Station file your creating for this event
truncate $phase_station, 0;

open(my $FH,'<',$filename)or die "Could not open file '$filename' $!";

	my @Master = <$FH>;
	chomp @Master;
	
close $FH;

open(my $fh,'>',$newfilename)or die "Could not open file '$newfilename' $!";

################ Header formating ################# 

my @Header = $Master[0];
my @Year;
my @Month;
my @Day;
my @Hour;
my @Min;
my @Sec;
my $ID;
my $Year;
my $Month;
my $Day;
my $Hour;
my $Min;
my $Sec;

for my $Header (@Header){
	@Year = split( /[:,\s\/]+/, $Header);
	$Year = $Year[4];
	printf $fh ("%4s", "$Year");
	
	@Month = split( /[:,\s\/]+/, $Header);
	$Month = $Month[5];
	printf $fh ("%2s", "$Month");
	
	@Day = split( /[:,\s\/]+/, $Header);
	$Day = $Day[6];
	printf $fh ("%2s", "$Day");
	
	@Hour = split( /[:,\s\/]+/, $Header);
	$Hour = $Hour[7];
	printf $fh ("%2s", "$Hour");
	
	@Min = split( /[:,\s\/]+/, $Header);
	$Min = $Min[8];
	printf $fh ("%2s", "$Min");
	
	@Sec = split( /[:,\s\/]+/, $Header);
	$Sec = $Sec[9]; 		#STP has 5 digits. Hypo is 4 digits.
	$Sec = $Sec * 1000; 	#This gets rid of the decimal. the header should not have any decimals.
	printf $fh ("%4.4s", "$Sec");
	
	my @LatDeg = split( /[:.,\s\/]+/, $Header);
	my $LatDeg = $LatDeg[11];
		if ( $LatDeg == abs($LatDeg) ) {
			my $LatSign = " ";
			printf $fh ("%2s", "$LatDeg");
			printf $fh ("%1s", "$LatSign");
		} else {
			$LatDeg = $LatDeg * -1;
			my $LatSign = "S";
			printf $fh ("%2s", "$LatDeg");
			printf $fh ("%1s", "$LatSign");
		}

	my $LatMin = $LatDeg[12] / 10000;
	$LatMin = $LatMin * 60; 	#This will convert Latitude decimal degrees to Latitude decimal minutes
	$LatMin = $LatMin * 1000; 	#This gets rid of the decimal. the header should not have any decimals.
	printf $fh ("%4.4s", "$LatMin");
	

	my @LongDeg =  split (/[:.,\s\/]+/, $Header);
	my $LongDeg = $LongDeg[13];
		if ($LongDeg == abs($LongDeg) ) {
			my $LongSign = "E"; 	#Hypoinverse states that west is positive while in STP West is negative
			printf $fh ("%2s", "$LongDeg");
			printf $fh ("%1s", "$LongSign");
		} else {
			$LongDeg = $LongDeg * (-1);
			my $LongSign = " ";
			printf $fh ("%2s", "$LongDeg");
			printf $fh ("%1s", "$LongSign");
		}
	
	my $LongMin = $LongDeg[14] / 10000;
	$LongMin = $LongMin * 60; 	#This will convert Longitude decimal degrees to Longitude decimal minutes
	$LongMin = $LongMin * 1000; #This gets rid of the decimal. the header should not have any decimals.
	printf $fh ("%4.4s", "$LongMin");
	
	
	my @Depth = split(/[:,\s\/]+/, $Header);
	my $Depth = $Depth[12];
	$Depth = $Depth * 100; 		#This gets rid of the decimal. the header should not have any decimals.
	printf $fh ("%5s", "$Depth");
	
	my @AmpMag = split(/[:,\s\/]+/, $Header);
	my $AmpMag = $AmpMag[13];
	$AmpMag = $AmpMag * 100; 	#This gets rid of the decimal. the header should not have any decimals.
	printf $fh ("%03d", "$AmpMag");
	
	printf $fh ("%97s", " ");	#filler space
	
	my @ID = split(/[:,\s\/]+/, $Header);
	$ID = $ID[1];
	printf $fh ("%10s\n", "$ID");
}	

################ Phase formating ################# 

shift @Master;
	
for my $Phasefile (@Master){
	my @StationCode = split(/\s+/, $Phasefile);
	printf $fh ("%-5s", "$StationCode[2]");
		open(my $Fh,'<',$main_station)or die "Could not open file '$main_station' $!";
			my @StationTempNames = <$Fh>;
			chomp @StationTempNames;	
			my @StationNames = grep(/$StationCode[2]/, @StationTempNames);
			close $Fh;
		open(my $fH,'>>',$phase_station)or die "Could not open file '$phase_station' $!";	
			print $fH join("\n", @StationNames), "\n";
			close $fH;
			
		#Hypoinverse allows a max of 11,000 stations at once.
		#The above process searches for stations used in this phase 
		#file and puts them into a seperate station file for you.
	
	my @NetworkCode = split(/\s+/, $Phasefile);
	printf $fh ("%2s", "$NetworkCode[1]");
	
	my @ComponentCode = split(/\s+/, $Phasefile);
	printf $fh ("%5s", "$NetworkCode[3]");	

	my @SignalQuality = split(/\s+/, $Phasefile);
	
	my @P_phase = split(/\s+/, $Phasefile);
			
	my @P_FirstMotion = split(/\s+/, $Phasefile); #STP uses d and c for dilational and compressional, Hypo uses U and D for up and down
		if ($P_phase[8] eq "P"){
			if ($P_FirstMotion[9] eq ".."){
				$P_FirstMotion[9] = " ";
				my $YearMonthDayHourMin = join "", $Year,$Month,$Day,$Hour,$Min;
				my $P_Arrival = $P_FirstMotion [13]; #Element 13 is time after origin (seconds)
				chop $P_Arrival;
				$P_Arrival = $P_Arrival * 100; #gets rid of decimal
				printf $fh ("%2s", uc"$SignalQuality[10]");
				printf $fh ("%1s", "$P_phase[8]");
				printf $fh ("%1s", "$P_FirstMotion[9]");
				printf $fh ("%13s", "$YearMonthDayHourMin");
				printf $fh ("%5s" , "$P_Arrival");
				
				my @EpiDistance = split(/\s+/, $Phasefile);
				my $EpiDistance = $EpiDistance[12] * 100;
				printf $fh ("%30s", "$EpiDistance");
				
				my @LocCode = split(/\s+/, $Phasefile);
				printf $fh ("%48s", "$LocCode[4]");
			
			}elsif ($P_FirstMotion[9] eq "d."){
				$P_FirstMotion[9] = "D";
				my $YearMonthDayHourMin = join "", $Year,$Month,$Day,$Hour,$Min;
				my $P_Arrival = $P_FirstMotion [13]; #Element 13 is time after origin (seconds)
				chop $P_Arrival;
				$P_Arrival = $P_Arrival * 100; #gets rid of decimal
				printf $fh ("%2s", uc"$SignalQuality[10]");
				printf $fh ("%1s", "$P_phase[8]");
				printf $fh ("%1s", "$P_FirstMotion[9]");
				printf $fh ("%13s", "$YearMonthDayHourMin");
				printf $fh ("%5s" , "$P_Arrival");
				
				my @EpiDistance = split(/\s+/, $Phasefile);
				my $EpiDistance = $EpiDistance[12] * 100;
				printf $fh ("%30s", "$EpiDistance");	
				
				my @LocCode = split(/\s+/, $Phasefile);
				printf $fh ("%48s", "$LocCode[4]");
			
			}elsif ($P_FirstMotion[9] eq "c."){
				$P_FirstMotion[9] = "U";
				my $YearMonthDayHourMin = join "", $Year,$Month,$Day,$Hour,$Min;
				my $P_Arrival = $P_FirstMotion [13]; #Element 13 is time after origin (seconds)
				chop $P_Arrival;
				$P_Arrival = $P_Arrival * 100; #gets rid of decimal
				printf $fh ("%2s", uc"$SignalQuality[10]");
				printf $fh ("%1s", "$P_phase[8]");
				printf $fh ("%1s", "$P_FirstMotion[9]");
				printf $fh ("%13s", "$YearMonthDayHourMin");
				printf $fh ("%5s" , "$P_Arrival");
				
				my @EpiDistance = split(/\s+/, $Phasefile);
				my $EpiDistance = $EpiDistance[12] * 100;
				printf $fh ("%30s", "$EpiDistance");
	
				my @LocCode = split(/\s+/, $Phasefile);
				printf $fh ("%48s", "$LocCode[4]");
			}	
		}
	my @S_Phase = split(/\s+/, $Phasefile);	
		if ($S_Phase[8] eq "S"){
			my $YearMonthDayHourMin = join "", $Year,$Month,$Day,$Hour,$Min;
			my $S_Arrival = $S_Phase [13]; #Element 13 is time after origin (seconds)
			chop $S_Arrival;
			$S_Arrival = $S_Arrival * 100; #gets rid of decimal
			printf $fh ("%17s", "$YearMonthDayHourMin");
			printf $fh ("%17s" , "$S_Arrival");
			printf $fh ("%1s", uc"$SignalQuality[10]");
			printf $fh ("%1s", "$S_Phase[8]");
			
			my @EpiDistance = split(/\s+/, $Phasefile);
			my $EpiDistance = $EpiDistance[12] * 100;
			printf $fh ("%16s", "$EpiDistance");
	
			my @LocCode = split(/\s+/, $Phasefile);
			printf $fh ("%48s", "$LocCode[4]");
		}
	
	
	printf $fh ("\n");
	
}			

################ Terminator Line #################
 
printf $fh ("%-62s", "");
printf $fh ("%10s", "$ID");

close $fh;


print "Process Complete\n";
print "Phase file for event $ID is located in '$newfilename'\n";
print "Station file for event $ID is located in '$phase_station'\n";
