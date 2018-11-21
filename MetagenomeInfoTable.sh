#!/bin/bash

#This script takes a .fasta file and its correspondig .kraken file to create a .csv table that contains the 
#number of contig (NODE), its length, coverage, GC %, and taxonomic lineage. The output table is a csv table named after the .kraken file
#To run the script it is necesary that this shell script and the python script "calculations.py" are in the same directory

file_kraken=$1
file_contigs=$2

###########

#The following block of code checks if the kraken and fasta files correspond to each other and if they are in the correct order 

echo "Checking files integrity..."

input1=$(cut -f2 $file_kraken)
input2=$(grep '^>' $file_contigs | cut -d' ' -f1 | sed -e 's/>//g')

if [ "$input1" != "$input2" ]; 
	then echo "Files are either in an incorrect order or they are from different samples. Please check them." 
	exit 1
fi

###########

###########

#The following block of code checks if the fasta file has a supported format, creating the table if it has, or returning a warning if it hasn't
#Supported formats are IDBA-UD (">contig"), MEGAHIT (">k"), spades, velvet, metavelvet and metaSPAdes (>NODE_)
#New formats can be easly added by writing a new case condition
contigs_header=$(head -n 1 $file_contigs)

case $contigs_header in 
(*">contig"*)
	echo "$file_contigs format: IDBA-UD"

	#First step: Create the output table and a file with all the taxids from the kraken file
	echo "NODE,LENGTH,COVERAGE,GC,SUPERKINGDOM,PHYLUM,ORDER,FAMILY,GENUS,SPECIES,SUBSPECIES" > ${file_kraken/%.kraken/.csv}
	cut -f3 ${file_kraken} > kraken_taxIDs.txt

	#Second step: Create auxiliary files (most importantly, the temporal_table.csv)
	echo "Creating auxiliary files"
	grep '^>' $file_contigs | sed -e 's/ /_/g' | cut -d'_' -f2,4 | sed -e 's/_/,/g' > temporal_table.csv
	total_len=$(grep -v '^>' $file_contigs | tr -d '\n' | wc -c)
	grep '^>' $file_contigs | cut -d'_' -f5 > read_count_per_contig.txt
	grep '^>' $file_contigs | cut -d' ' -f2 | cut -d'_' -f2 > contigs_len.txt
	
	#Third step: Call the python script to make all the calculations and fill the output table 
	echo "Making GC % and coverage calculations & taxonomic assignments..."
	python calculations.py $file_contigs 1 $total_len >> ${file_kraken/%.kraken/.csv}

	#Fourth step: Delete all the auxiliary files 
	rm temporal_table.csv read_count_per_contig.txt contigs_len.txt kraken_taxIDs.txt
	echo "${file_kraken/%.kraken/.csv} created"
	echo "Done"	
;;
(">k"*)
	echo "$file_contigs format: MEGAHIT"

	#First step
	echo "NODE,LENGTH,COVERAGE,GC,SUPERKINGDOM,PHYLUM,ORDER,FAMILY,GENUS,SPECIES,SUBSPECIES" > ${file_kraken/%.kraken/.csv}
	cut -f3 ${file_kraken} > kraken_taxIDs.txt

	#Second step
	echo "Creating auxiliary files"
	grep '^>' $file_contigs | cut -d' ' -f1,4 | cut -d'_' -f2 | sed -e 's/ len=/,/g' > node_length.txt
	grep '^>' $file_contigs | cut -d' ' -f3 | cut -d'=' -f2 > coverage.txt
	paste -d',' node_length.txt coverage.txt > temporal_table.csv

	#Third step
	echo "Making GC % calculations & taxonomic assignments..."
	python calculations.py $file_contigs 0 0 >> ${file_kraken/%.kraken/.csv}

	#Fourth step
	rm kraken_taxIDs.txt temporal_table.csv node_length.txt coverage.txt
	echo "${file_kraken/%.kraken/.csv} created"
	echo "Done"	
;;
(*">NOE_"*)	
	echo "$file_contigs format: (meta)Velvet/(meta)SPAdes"

	#First step
	echo "NODE,LENGTH,COVERAGE,GC,SUPERKINGDOM,PHYLUM,ORDER,FAMILY,GENUS,SPECIES,SUBSPECIES" > ${file_kraken/%.kraken/.csv}
	cut -f3 ${file_kraken} > kraken_taxIDs.txt

	#Second step
	echo "Creating auxiliary files"
	cut -f2 ${file_kraken} | cut -d'_' -f 2,4,6 | sed -e 's/_/,/g' > temporal_table.csv 

	#Third step
	echo "Making GC % calculations & taxonomic assignments..."
	python calculations.py $file_contigs 0 0 >> ${file_kraken/%.kraken/.csv}

	#Fourth step
	rm kraken_taxIDs.txt temporal_table.csv
	echo "${file_kraken/%.kraken/.csv} created"
	echo "Done"
;;
*)
	echo "$file_contigs format: Unknown"
	echo "Please check that your contig file is a fasta of the supported formats"
	exit 1
;;esac