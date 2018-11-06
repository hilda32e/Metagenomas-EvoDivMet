# Metagenomas-EvoDivMet
The scripts MetagenomeInfoTable.sh and gc_and_taxa.py create a .csv table from a .kraken and a fasta files. The information contained in the table is:

  1. NODE (contig number)
  2. Length 
  3. Coverage
  4. GC %
  5. Superkingdom
  6. Phylum
  7. Order
  8. Family
  9. Genus
  10. Species
  11. Sub-species

To run the script download the MetagenomeInfoTable.sh file and the gc_and_taxa.py to the same directory. Then run the MetagenomeInfoTable.sh file with the .kraken file and .fasta file as arguments in that exact order, as shown in the following example:
  
    sh MetagenomeInfoTable.sh KRAKEN_OUTPUT_FILE.kraken CONTIGS.fasta
 
The KRAKEN_OUTPUT_FILE is the standard kraken version 1 or 2 output and the CONTIGS.fasta file is the assembly file that was used to generate the kraken file. Being related, these two files should correspond to each other, if they are not, the script will show an error message and the table will not be generated. Please make sure that you are using the corresponding input files. 

Please also bear in mind that the input files must be in the order shown (.kraken file first and .fasta file last). If they are not in that order, the python script will show and error and the table will not the generated correctly.

To run the script it is necessary to have Python 3.0 or above, and the sys and ete3 libraries. Please install them beforehand. 

To run the script it is also necessary to have the file "taxdump.tar.gz" in the same directory as the scripts. If the file "taxdump.tar.gz" is not there (or if it is the first time that you run the script), the scripts will attempt to download the file, for which is necesary to have an active internet connexion. 
