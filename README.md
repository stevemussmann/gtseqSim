# gtseqSim Introduction
This program simulates genotype data for known parent/offspring pairs based on allele frequency data, and (optionally) simulates missing data in the output files so that researchers can evaluate its impact on their analyses. This README.md file will be updated regarding program functionality as features are added.

The program is a work in progress and will have two primary functions when completed. 
1. Simulate reproduction of diploid organisms in a captive environment to evaluate the power of codominant genetic marker panels for resolving familial relationships.
2. Simulate reproduction of interspecific hybrids to evaluate the power of codominant genetic marker panels to accurately identify different hybrid categories.

If you just want to generate some known parent/offspring individuals using allele frequency data from a single genepop file, the program is fully functional at that level. However, many details pertaining to function 1 have been implemented primarily to address a specific use case in ongoing research. I plan to eventually make it more generalized so it will have a wider variety of applications.

Function 2 has not yet been implemented.

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
- This program is in a perpetual stage of development. Please make a backup copy of any files you use with this program before running it - use at your own risk.
- Currently treats all individuals in the input genepop file as belonging to the same population. I plan to implement options to allow a second population/species input through a second genepop file, but this option and related functions are currently non-functional.
- The genepop input format is somewhat flexible (i.e., either 2-digit or 3-digit format should be acceptable but not rigorously tested).
- Missing alleles must be coded in genepop 2-digit or 3-digit format (i.e., 0000 for 2-digit or 000000 for 3-digit).
- A genotyping error simulation function is planned but not yet implemented.
- Minimal error checking procedures have been implemented. I add error messages when problems are encountered, but many error messages could still be minimally helpful to the user.

## Input Requirements
### Required
The minimal input is a text file containing genotypes in genepop format.

Required Inputs:
* **-g / --genepop**: Specify an input text file in genepop format.

Optional Inputs:
* **-f / --generations**: <Integer> Enter the number of generations that you want to simulate. There is technically no limit, but I recommend keeping this number small (ideally ≤ 3).
* **-G / --genepop2**: <String> Enter the file name of a second genepop file representing a second population or species **CURRENTLY NOT IMPLEMENTED. PROGRAM WILL EXIT IF THIS OPTION IS USED.**
* **-l / --lambda**: <Float> Specify the lambda parameter value for poisson sampling of offspring. I usually set this value as the number of offspring per family group sampled per generation. 
* **-m / --miss**: <Boolean> Turn on missing data simulation (default = off).
* **-n / --inds**: <Integer> Specify the number of individual genotypes you want to simulate for the starting (F0) population (default = 50).
* **-o / --outfile**: <String> Specify an output file name prefix (default = output)
* **-p / --progeny**: <Integer> Specify the number of offspring produced per parental pair (default = 50).
* **-r / --grandma**: <Boolean> Create an input file formatted for [gRandma](https://github.com/delomast/gRandma) (NOTE: Currently only functions correctly for SNP data).
* **-s / --sequoia**: <Boolean> Create input files formatted for [sequoia](https://github.com/JiscaH/sequoia) (NOTE: Only works for biallelic data).
* **-S / --secondary**: <Integer> Specify the number of individual genotypes to simulate as part of a secondary population. This is intended to mimic a 'wild' population that exists separately from your main 'captive' population but has similar allele frequencies to the 'captive' population. None of the secondary population will be used to produce offspring.
* **-t / --prefix1**: <String> Specify the prefix to be used for naming individuals simulated from the first genepop file (-g / --genepop option) (default prefix = taxon1).
* **-T / --prefix2**: <String> Specify the prefix to be used for naming individuals simulated from the second genepop file (-G / --genepop2 option) (default prefix = taxon2. **CURRENTLY NOT IMPLEMENTED**

## Example Commands
One of the simplest use cases is to simulate some genotypes from empirically-derived allele frequency data. To generate 500 simulated genotypes from a data file (snpExample.genepop.txt) use the following command:
```
gtseqSim.py -g snpExample.genepop.txt -n 500 -f 0
```

If you want to produce offspring of those individuals to test parent/offspring relationships, you could do the following. This should produce 100 offspring from each of approximately 250 families. Sex is randomly assigned to the simulated individuals using a binomial distribution with an expected ~1:1 M:F sex ratio, and all reproduction is 1 male x 1 female. This means that it is possible you will have slightly fewer than 250 families (i.e., the limiting factor is the sex with fewer individuals. If you end up with 249 males and 251 females in your starting population, you will have 249 family groups). 
```
gtseqSim.py -g snpExample.genepop.txt -n 500 -f 1 -p 100
```

You could simulate two generations if you want to evaluate grandparentage:
```
gtseqSim.py -g snpExample.genepop.txt -n 500 -f 2 -p 100
```

If you want to simulate missing data in your output files, you can use the `-m` option to model missing data proportions from empirically-observed missing data for each locus:
```
gtseqSim.py -g snpExample.genepop.txt -n 500 -f 2 -p 100 -m
```

You can subsample the offspring of these families to obtain uneven representation of family groups, which is intended to simulate the uneven family representation that may result from randomly sampling captively-produced individuals. All parents used for reproduction will still be retained in the output:
```
gtseqSim.py -g snpExample.genepop.txt -n 500 -f 2 -p 100 -m -l 2.0
```

The `-r` and `-s` options can be used to output files in [gRandma](https://github.com/delomast/gRandma) and [sequoia](https://github.com/JiscaH/sequoia) formats, respectively. A special filter is also applied exclusively for the `gRandma` output to identify loci that are sufficiently variable (e.g., at least one individual must be heterozygous for alleles a and b, homozygous for allele a, and homozygous for allele b for a locus to be retained in the final `gRandma` output. This could result in some loci being excluded from this file which are present in others. However, the probability of this filter being triggered is reduced as the number of simulated individuals rises. The conditions used in these examples should yield enough individuals that few, if any, loci will be discarded by this filter.
```
gtseqSim.py -g snpExample.genepop.txt -n 500 -f 2 -p 100 -m -l 2.0 -r -s
```

## Outputs
### Outputs produced by every run:
This program will always output a genepop-formatted file of simulated genotypes regardless of the combination of command line options used. The default name of the file will be `output.genepop.txt`.

Parentage for each generation of offspring will always be written (unless the user requests 0 offspring generations with the option `-f 0`). These files will be named `F{x}.parentage.txt` where `{x}` represents the generation number. For example, `F1.parentage.txt` will list the parentage of the F1 offspring. An example of the output format is provided below:
```
male_parent     female_parent   offspring
taxon1_M0000207 taxon1_F0000131 F1_F0000000
taxon1_M0000207 taxon1_F0000131 F1_F0000001
taxon1_M0000207 taxon1_F0000131 F1_F0000002
taxon1_M0000207 taxon1_F0000131 F1_M0000000
taxon1_M0000207 taxon1_F0000131 F1_M0000001
taxon1_M0000207 taxon1_F0000131 F1_F0000003
taxon1_M0000207 taxon1_F0000131 F1_M0000002
taxon1_M0000207 taxon1_F0000131 F1_M0000003
taxon1_M0000207 taxon1_F0000131 F1_M0000004
```

I also wrote a perl script that will format the list of crosses used in the grandparent generation for inclusion as potential crosses in the gRandma R package. For example:
```
perl getCrossRecords.pl -g F1.parentage.txt
```

This will produce a file named `potentialCrosses.txt` with the following format. Pop = baseline population name, gp1 = female grandparent, gp2 = male grandparent.
```
Pop	gp1	gp2
taxon1	taxon1_F0000239	taxon1_M0000267
taxon1	taxon1_F0000243	taxon1_M0000160
taxon1	taxon1_F0000040	taxon1_M0000228
taxon1	taxon1_F0000299	taxon1_M0000252
taxon1	taxon1_F0000061	taxon1_M0000003
taxon1	taxon1_F0000062	taxon1_M0000092
```

I have also produced a perl script that will generate a list of grandparents for each individual in the F2 generation, given the `F{x}.parentage.txt` files from two consecutive generations. For example:
```
perl listGrandparents.pl -1 F1.parentage.txt -2 F2.parentage.txt
```

This will produce a file named `output.grandparents.txt` with the following format. In this file, pGF = paternal grandfather, pGM = paternal grandmother, mGF = maternal grandfather, mGM = maternal grandmother.
```
offspring       pGF     pGM     mGF     mGM
F2_F0000000     taxon1_M0000197 taxon1_F0000080 taxon1_M0000050 taxon1_F0000097
F2_F0000001     taxon1_M0000197 taxon1_F0000080 taxon1_M0000050 taxon1_F0000097
F2_F0000002     taxon1_M0000197 taxon1_F0000080 taxon1_M0000050 taxon1_F0000097
F2_F0000003     taxon1_M0000197 taxon1_F0000080 taxon1_M0000050 taxon1_F0000097
F2_F0000004     taxon1_M0000197 taxon1_F0000080 taxon1_M0000050 taxon1_F0000097
F2_F0000005     taxon1_M0000197 taxon1_F0000080 taxon1_M0000050 taxon1_F0000097
F2_F0000006     taxon1_M0000197 taxon1_F0000080 taxon1_M0000050 taxon1_F0000097
F2_F0000007     taxon1_M0000197 taxon1_F0000080 taxon1_M0000050 taxon1_F0000097
F2_F0000008     taxon1_M0000197 taxon1_F0000080 taxon1_M0000050 taxon1_F0000097
```

### Optional outputs
* sequoia output
    * These files will only be produced if you have provided a file of biallelic SNPs. 
    * The `-s` option produces two files. These are the sequoia-formatted genotype file (default name = `output.sequoia.txt`) and the life history data file (`sequoia.LH.txt`)
    * These can be read into the R package sequoia using the following R commands:
```
library("sequoia")
# genotypes file
geno <- as.matrix(read.csv("output.sequoia.txt", sep="\t", header=FALSE, row.names=1))

# life history file
lh <- read.csv("sequoia.LH.txt", sep="\t", header=TRUE)
```

* gRandma output
    * Currently this file will only be produced properly if the input file was a genepop file with 2-digit allele coding with the following pattern: `'00' = 'missing data', '01' = 'A', '02' = 'C', '03' = 'G', and '04' = 'T'`. Other inputs will likely result in errors.
    * The default output file name is `output.grandma.txt`.
    * If you are using known crosses as input, the default output file name from my perl script is `potentialCrosses.txt`. 
    * The files can be read into gRandma with the following R commands:
```
library("gRandma")

# genotypes file
genotypes <- read.csv("output.grandma.txt", sep="\t", header=TRUE, na.strings="")

# potential crosses file
potentialCrosses <- read.csv("potentialCrosses.txt", sep="\t", header=TRUE)
```

