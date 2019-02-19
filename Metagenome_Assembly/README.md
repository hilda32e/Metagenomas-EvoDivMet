
# Metagenome assembly 

## To be used in a cluster

This script assembly pair-end short reads using four assemblers: MEGAHIT (v 1.1.2), IDBA-UD (v 2.0), MetaSPAdes and SPAdes (v 3.10.1). To run, the script requires that these assemblers' specific versions are installed in the cluster beforehand. 

To run the script please follow the following format:

    sh assembly.sh $READS_FORWARD.fastq $READS_REVERSE.fastq suffix

The suffix, or assembly's name, is added to the beginning of each output file.  

The outputs are organized into two folders, ASSEMBLIES, and ASSEMBLY_STATS. The first one contains the assemblies and the other one contains the scripts used to run the assemblers, as well as the error and output files generated during the run. 