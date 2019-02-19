
# Repository of scripts used in the analysis of metagenomic data 

## Evodivmet


This repository contains scripts used to assemble and analyze metagenomic data. While many of the scripts can be run locally, in GNU or OS X, some (the ones with an * in their name) only work in a cluster with a PBS job scheduler such as Langebio's mazorka. If you want to use those scripts, please check that they are compatible with the job scheduler in your cluster. 

### Summary of the scripts 

#### Assembly 

1. assembly.sh*: This script is used to submit assembly jobs using 4 assemblers: [MEGAHIT](https://github.com/voutcn/megahit), [IDBA-UD](https://github.com/loneknightpy/idba), [MetaSPAdes and spades](http://cab.spbu.ru/software/spades/)

#### Analysis 
    
1. MetagenomeInfoTable.sh: This script generates a CSV table with taxonomic data (previously generated with Kraken) and intrinsic data (such as length or GC %) of each contig or scaffold in an assembly. 

2. KrakenLabels.py: This script generates the labels file that was deprecated in Kraken 2.0 