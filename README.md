# Metagenomas-EvoDivMet
The scripts **MetagenomeInfoTable.sh** and **gc_and_taxa.py** create a .csv table from a .kraken and a fasta files. The information contained in the table is:

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

Before running the scripts please make sure you have Python 3.0 or above (https://www.python.org) and the ETE Toolkit libraries (http://etetoolkit.org).

To run the scripts, execute the bash script **MetagenomeInfoTable.sh** with the .kraken file and .fasta file as arguments in that exact order, as shown in the following example:
  
    sh MetagenomeInfoTable.sh $KRAKEN_FILE .kraken $CONTIGS_FILE
 
The KRAKEN_FILE is the standard Kraken version 1 or 2 output and the CONTIGS_FILE  is the assembly file that was used to generate the kraken file. Since these two files are related, they should correspond to each other. If they don't (or are in an inverse order), the script will show an error message and the table will not be generated. Please make sure that you are using the corresponding input files. 

To run the script it is also necessary to have the file "taxdump.tar.gz" in the same directory as the scripts. If the file "taxdump.tar.gz" is not there (or if it is the first time that you run the script), the scripts will attempt to download the file. 

The script will generate a file named after the KRAKEN_FILE, but with the extension .csv as an output. 
