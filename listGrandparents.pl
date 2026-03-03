#!/usr/bin/perl

use warnings;
use strict;
use Getopt::Std;
use Data::Dumper;

# kill program and print help if no command line arguments were given
if( scalar( @ARGV ) == 0 ){
  &help;
  die "Exiting program because no command line options were used.\n\n";
}

# take command line arguments
my %opts;
getopts( '1:2:ho:', \%opts );

# if -h flag is used, or if no command line arguments were specified, kill program and print help
if( $opts{h} ){
  &help;
  die "Exiting program because help flag was used.\n\n";
}

# parse the command line
my( $f1, $f2, $out ) = &parsecom( \%opts );

my %f1parents;
my %f2parents;

my @f1Lines;
my @f2Lines;

&filetoarray( $f1, \@f1Lines );
&filetoarray( $f2, \@f2Lines );

my $f1header = shift( @f1Lines );
my $f2header = shift( @f2Lines );

foreach my $line( @f1Lines ){
	my @temp = split( /\s+/, $line );
	push( @{$f1parents{$temp[2]}}, $temp[1] );
	push( @{$f1parents{$temp[2]}}, $temp[0] );
}

foreach my $line( @f2Lines ){
	my @temp = split( /\s+/, $line );
	push( @{$f2parents{$temp[2]}}, $temp[1] );
	push( @{$f2parents{$temp[2]}}, $temp[0] );
}

open( OUT, '>', $out ) or die "Can't open $out: $!\n\n";

print OUT "offspring\tpGM\tpGF\tmGM\tmGF\n";
foreach my $ind( sort keys %f2parents ){
	print OUT $ind;
	foreach my $parent( @{$f2parents{$ind}} ){
		foreach my $gp( @{$f1parents{$parent}} ){
		print OUT "\t", $gp;
		}
	}
	print OUT "\n";
}

close OUT;

#print Dumper( \%f2parents );

exit;

#####################################################################################################
############################################ Subroutines ############################################
#####################################################################################################

# subroutine to print help
sub help{
  
  print "\nlistGrandparents.pl is a perl script developed by Steven Michael Mussmann\n\n";
  print "To report bugs send an email to mussmann\@uark.edu\n";
  print "When submitting bugs please include all input files, options used for the program, and all error messages that were printed to the screen\n\n";
  print "Program Options:\n";
  print "\t\t[ -0 | -1 | -2 | -h | -o ]\n\n";
  print "\t-h:\tDisplay this help message.\n";
  print "\t\tThe program will die after the help message is displayed.\n\n";
  print "\t-0:\tSpecify the grandparent generation file (F0) output from gtseqSim.py (required).\n\n";
  print "\t-1:\tSpecify the parent generation file (F1) output from gtseqSim.py (required).\n\n";
  print "\t-2:\tSpecify the children generation file (F2) output from gtseqSim.py (required).\n\n";
  print "\t-o:\tSpecify output file (Optional).\n\n";
  
}

#####################################################################################################
# subroutine to parse the command line options

sub parsecom{ 
  
  my( $params ) =  @_;
  my %opts = %$params;
  
  # set default values for command line arguments
  my $f1 = $opts{1} || die "No parent (F1) input file specified.\n\n"; #used to specify F1 file.
  my $f2 = $opts{2} || die "No offspring (F2) input file specified.\n\n"; #used to specify F2 file.
  my $out = $opts{o} || "output.grandparents.txt"; #used to specify output file name.

  return( $f1, $f2, $out );

}

#####################################################################################################
# subroutine to put file into an array

sub filetoarray{

  my( $infile, $array ) = @_;

  
  # open the input file
  open( FILE, $infile ) or die "Can't open $infile: $!\n\n";

  # loop through input file, pushing lines onto array
  while( my $line = <FILE> ){
    chomp( $line );
    next if($line =~ /^\s*$/);
    push( @$array, $line );
  }
  
  # close input file
  close FILE;

}

#####################################################################################################
