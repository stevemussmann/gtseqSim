# gtseqSim
Simulate genotype data based on allele frequencies.

This program is a work in progress. This README.md file will be updated regarding program functionality as features are added.

This program calculates allele frequencies for a single population based upon the observed frequencies in the input genepop file. The `random.multinomial` function from numpy is then used to generate simulated genotypes for a user-defined number of individuals based upon those empirical allele frequencies. Loci are assumed to be independent. The simulated genotypes are then output in genepop format.

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
- Does not currently handle missing data properly. Missing data might cause the program to crash or produce weird/unexpected output unless missing alleles also coded in 2-digit or 3-digit format (i.e., 0000 for 2-digit or 000000 for 3-digit).
- Genotyping error and missing data simulation functions not yet implemented.
- Minimal error checking procedures have been implemented. Error messages will be minimally helpful to the user.

## Input Requirements
### Required
The minimal input is a text file containing genotypes in genepop format.

Required Inputs:
* **-g / --genepop:** Specify an input text file in genepop format.

Optional Inputs:
* **-n / --inds:** Specify the number of individuals for which you want to generate simulated genotypes.
* **-o / --outfile:** Specify an output file name (default = output.genepop.txt)

## Example Commands
To generate 500 simulated genotypes from the example data, use the following command:
```
gtseqSim.py -g microsatellite_example.genepop.txt -n 500 -o msatExample.genepop.txt
```
This will create the output `msatExample.genepop.txt` in the folder from which the command was executed.

## Outputs
Output will be a genepop file of simulated genotypes.
