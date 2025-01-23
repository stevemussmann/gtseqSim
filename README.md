# gtseqSim Introduction
This program simulates genotype data for known parent/offspring pairs based on allele frequency data, and (optionally) simulates missing data in the output files so that researchers can evaluate its impact on their analyses. This README.md file will be updated regarding program functionality as features are added.

The program is a work in progress and will have two primary functions when completed. 
1. Simulate reproduction of diploid organisms in a captive environment to evaluate the power of codominant genetic marker panels for resolving familial relationships.
2. Simulate reproduction of interspecific hybrids to evaluate the power of codominant genetic marker panels to accurately identify different hybrid categories.

If you just want to generate some known parent/offspring individuals using allele frequency data from a single genepop file, the program is fully functional at that level. However, many details pertaining to function 1. have been implemented primarily to address a specific use case in ongoing research. I plan to eventually make it more generalized so it will have a wider variety of applications.

Function 2. has not yet been implemented.

Please cite this github repository if you use this software.

## Overview of capabilities

This program accepts a genepop file as input and calculates allele frequencies for a single population based upon the observed frequencies in that file. The `random.multinomial` function from numpy is then used to generate simulated genotypes for a user-defined number of individuals based upon those empirical allele frequencies. The program will function best with SNPs, but should be able to handle microsatellites in most cases. I have not yet tested the program with microhaplotype data. 

If desired, the user can simulate reproduction within the simulated population to produce one or more generations of offspring. These simulations produce distinct cohorts of offspring (i.e., generation N will be the parents of generation N+1 and the grandparents of generation N+2). All reproductive crosses are 1 male x 1 female (i.e., currently there is no option to produce half-siblings, but that may be implemented in the future). One male and one female offspring from each full-sibling family group in Generation N will become part of the parental pool in generation N+1. The program prevents inbreeding from happening within full-sibling family groups, but does not prevent reproduction among cousins. Currently there are no functions to simulate periodic gene flow into the captive population, but this capability may be added in the future. All parent/offspring relationships are recorded by the program for each generation and output to text files. 

The program also includes options to simulate missing genotype data and uneven offspring sampling per family group. The missing genotype rate is calculated separately for each locus from your input genepop file. If the `-m / --miss` option is invoked, then the program will evaluate each locus in which missing data were detected and randomly remove genotypes from these loci using the empirically-derived missing data proportion from your input genotype file. This is accomplished using the `random.binomial` function from numpy. Sampling of offspring for genetic studies often results in uneven representation of family groups. The program attempts to mimic this using the `-l / --lambda` option. This sets the lambda parameter for a poisson distribution that will determine how many offspring are sampled from each family group. Setting a relatively low value (i.e., ~2.0) should result in uneven representation of family groups in the final genotype file. In this case, few or no offspring will be sampled from many family groups, whereas a relatively large number of individuals will be sampled from a small number of family groups. This will allow the user to evaluate whether unequal family representation in a dataset may impact their ability to use a particular marker set to accurately resolve familial relationships. 

Loci are assumed to be independent. The simulated genotypes are output in up to three output formats (genepop, sequoia, and gRandma). The latter two formats will be SNP-specific. 

## Dependencies
- numpy
- pandas

## Installation
One option for installation is the setup of a conda environment. This can be accomplished by first installing [Miniconda](https://docs.conda.io/en/latest/miniconda.html), and might be the easiest option if you do not have admin privileges on your computer. Once conda is setup, configure it so that the base environment does not automatically load on startup.
```
conda config --set auto_activate_base false
```

Next, create a conda environment in which this program can be run. Use the following command, which should install a sufficiently recent version of python:
```
conda create -n gtseqSim -c conda-forge python=3 pandas numpy
```
The environment can be activated and deactivated as needed with the following commands:
```
conda activate gtseqSim
conda deactivate
```

Next, download this package to the location of your choice with the following command.
```
git clone https://github.com/stevemussmann/gtseqSim.git
```

If necessary, make the software executable:
```
chmod u+x gtseqSim.py
```

Finally, put the software in your $PATH. There are many ways of accomplishing this. For example, add the following line (replacing '/path/to/gtseqSim' with the correct path) to the end of your .bashrc file and reload your .bashrc:
```
export PATH=/path/to/gtseqSim:$PATH
```

## Development Notes
- This program is in a very early development stage - use at your own risk.
- Currently treats all individuals in the input genepop file as belonging to the same population.
- Genepop input format should be somewhat flexible (i.e., either 2-digit or 3-digit format should be acceptable but not tested).
- Missing alleles must be coded in genepop 2-digit or 3-digit format (i.e., 0000 for 2-digit or 000000 for 3-digit).
- Genotyping error simulation function not yet implemented.
- Minimal error checking procedures have been implemented. Most error messages will be minimally helpful to the user.

## Input Requirements
### Required
The minimal input is a text file containing genotypes in genepop format.

Required Inputs:
* **-g / --genepop:** Specify an input text file in genepop format.

Optional Inputs:
* **-m / --miss:** Boolean. Turn on missing data simulation (default = off).
* **-n / --inds:** Specify the number of individuals for which you want to generate simulated genotypes (default = 50).
* **-o / --outfile:** Specify an output file name (default = output.genepop.txt)

## Example Commands
To generate 500 simulated genotypes from the example data and simulate missing data, use the following command:
```
gtseqSim.py -g microsatellite_example.genepop.txt -n 500 -o msatExample.genepop.txt -m
```
This will create the output `msatExample.genepop.txt` in the folder from which the command was executed.

## Outputs
Output will be a genepop file of simulated genotypes.
