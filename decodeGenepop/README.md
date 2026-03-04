# decodeGenepop Introduction
This is a file converter that will convert the genepop files written by gtseqSim back into a nucleotide format, if given a nested python dict (in JSON format) containing the allelic conversions. Key1 = locus name; Key2 = allele (nucleotides); Value = allele (genepop encoding).

I initially wrote this file converter to accomplish a specific file conversion for a certain project, so it is not yet generalized to accept genepop files from other sources, or even all output possibilities from gtseqSim. It can currently only handle outputs containing one parental generation, one offspring generation, and a seconary (unrelated) population.

## Installation
If you followed the instructions for downloading/installing the gtseqSim package and creating its conda environment then you should be able to run that conda environment if you link `decodeGenepop.py` somewhere in your `$PATH`


## Usage
See example below to provide genepop file and json dictionary
```
decodeGenepop.py -g input.genepop -j locusDict.json
```

The input locus dictionary should look something like this:
```
{
        "NC_037099.1:62937268-62937373": {
                "T": "101",
                "C": "102"
        },
        "NC_037104.1:55923357-55923657": {
                "A": "101",
                "C": "102"
        }
}
```
