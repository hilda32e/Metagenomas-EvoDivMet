#!/bin/bash


#This script will take the .kraken and .fasta files indicated by the user to create a .csv table that contains the 
#number of contig (NODE), its length, its coverage, its GC %, and the taxonomic lineage generated by the 
#taxonomic assignment done with kraken 2 (.kraken file)

#The output of the script is a csv table named after the .kraken file

#To run the script it is necesary that this shell script and the python script "gc_and_taxa.py" are in the same directory

#Auxiliary file "taba1.csv" contains the NODE (contig), its length, and its coverage (obtained from the .kraken file)
#Auxiliary file "aux1.txt" contains the taxonomic ids (obtained from the .kraken file)
#Auxiliary file "aux2.txt" contains the unique taxonomic ids (obtained from the .kraken file)


file_kraken=$1
file_contigs=$2

#This if statement checks if the kraken file and the fasta file correspond to the same sample. 
#The program will return an error if they do not correspond 

echo "Checking files integrity..."

var1=$(cut -f2 $file_kraken)
var2=$(cat $file_contigs | sed -n '/>/p' | sed -e 's/>//g')

if [ "$var1" != "$var2" ]; 
	then echo "Files do not correspond" 
	exit 1
fi


cut -f2 ${file_kraken} | cut -d'_' -f 2,4,6 | sed -e 's/_/,/g' > taba1.csv
cut -f3 ${file_kraken} > aux1.txt
cut -f3 ${file_kraken} | sort | uniq | awk '{if($1>3)print $1}' > aux2.txt

echo "Making taxonomic assignments and GC % calculations..."

echo "NODE,LENGTH,COVERAGE,GC,SUPERKINGDOM,PHYLUM,ORDER,FAMILY,GENUS,SPECIES,SUB-SPECIES" > ${file_kraken/%.kraken/.csv}
python gc_and_taxa.py $2 >> ${file_kraken/%.kraken/.csv}

echo "Done"

rm aux1.txt
rm aux2.txt

rm taba1.csv

