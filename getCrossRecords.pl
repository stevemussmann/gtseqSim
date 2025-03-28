#!/usr/bin/perl

use warnings;
use strict;
use List::MoreUtils qw(uniq);
use Getopt::Std;
#use Data::Dumper;

# kill program and print help if no command line arguments were given
if( scalar( @ARGV ) == 0 ){
  &help;
  die "Exiting program because no command line options were used.\n\n";
}

# take command line arguments
my %opts;
getopts( 'g:ho:', \%opts );

# if -h flag is used, or if no command line arguments were specified, kill program and print help
if( $opts{h} ){
  &help;
  die "Exiting program because help flag was used.\n\n";
}

# parse the command line
my( $gpars, $out ) = &parsecom( \%opts );

my @gparents;
my @gparsLines;

&filetoarray( $gpars, \@gparsLines );

my $header = shift( @gparsLines );

foreach my $line( @gparsLines ){
	my @temp = split( /\s+/, $line );
	my @temp2 = split( /_/, $temp[0] );
	my $pop = $temp2[0];

	pop( @temp );
	my $gpa = shift( @temp );
	push( @temp, $gpa );
	unshift( @temp, $pop );
	my $newline = join( "\t", @temp );
	push( @gparents, $newline );
}

my @unique = uniq( @gparents );

open( OUT, '>', $out ) or die "Can't open $out: $!\n\n";

print OUT "Pop\tgp1\tgp2\n";

foreach my $item( @unique ){
	print OUT $item, "\n";
}

close OUT;

exit;

#####################################################################################################
############################################ Subroutines ############################################
#####################################################################################################

# subroutine to print help
sub help{
  
  print "\ngetCrossRecords.pl is a perl script developed by Steven Michael Mussmann\n\n";
  print "To report bugs send an email to mussmann\@uark.edu\n";
  print "When submitting bugs please include all input files, options used for the program, and all error messages that were printed to the screen\n\n";
  print "Program Options:\n";
  print "\t\t[ -g | -h | -o ]\n\n";
  print "\t-g:\tSpecify the file of parental records from grandparent generation, output from gtseqSim.py (required).\n\n";
  print "\t-h:\tDisplay this help message and exit program.\n\n";
  print "\t-o:\tSpecify output file (Optional).\n\n";
  
}

#####################################################################################################
# subroutine to parse the command line options

sub parsecom{ 
  
  my( $params ) =  @_;
  my %opts = %$params;
  
  # set default values for command line arguments
  my $gpars = $opts{g} || die "No input file specified.\n\n"; #used to specify grandparent cross records.
  my $out = $opts{o} || "potentialCrosses.txt"; #used to specify output file name.

  return( $gpars, $out );

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
