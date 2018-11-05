#Run this script in python 3.0 or above
#This script will not run in python 2.7 

#To run this scripts the sys and ete3 libraries must be installed.



import sys                                     #Imports library
from ete3 import NCBITaxa                      #Imports library

ncbi = NCBITaxa()                              #Imports taxonomic information from "taxdump.tar.gz" file. This file needs to be located in the same directory as the scripts 

taxonomic_info = []
taxonomic_lineage = []                         
unique_taxonomic_elements = {0: "Unassigned", 1: "Root", 2: "Bacteria"} 

n_contig = -1

filepath = sys.argv[1]                        #Gets the path to the .fasta file

sequence = ""
all_GC = []


#This loop calculate the GC percentage of every contig in the .fasta file and store it in a list called all_GC 
#The length of all_GC is equal to the number of contigs in the file and should be equal to the number of lines of  
#the .kraken file

with open(filepath, 'r') as b: 
    next(b)
    for line in b:
        if line.startswith('>'):
        	GC_content = float((sequence.count('G') + sequence.count('C'))) / len(sequence) * 100
        	sequence = ""
        	all_GC.append(GC_content)
        else:
        	sequence += line.rstrip()
    
    GC_content = float((sequence.count('G') + sequence.count('C'))) / len(sequence) * 100
    all_GC.append(GC_content)
b.close()





#This loop makes the dictonary of taxonomic lineages of all unique taxonomic ids (taxid) in the .kraken file
#The efficiency of this loop increases when unique taxid < all taxid in the .kraken file / 2
#This loop also eliminates the entries without taxonomic rank in each taxonomic lineage (e.g. the "Terrabacteria group" in the Actinomyces lineage)

with open('aux2.txt') as f:
  taxids = [int(i) for i in f]

for x in taxids:
	lineage = ncbi.get_lineage(x)                                                            #Gets the taxonomic lineage of a taxid 
	names = ncbi.get_taxid_translator(lineage)                                               #Gets the name of each component of the taxonomic lineage
	lineage2ranks = ncbi.get_rank(names)                                                     #Gets the taxonomic order (superkingdom, phylum, etc...) of each component of the taxonomic lineage
	no_rank=[k for k,v in lineage2ranks.items() if v== 'no rank']                            #Makes a list of the components of the lineage without a defined taxonomic order (the "no ranks")
	sub_species_taxid=lineage.pop()                                                          #Saves the sub-species taxid, as it does not have a formal taxonomic category yet 
	lineage_without_no_rank = [m for m in lineage if m not in no_rank]                       #Deletes the lineage components that do not have a defined taxonomic order
	lineage_without_no_rank.append(sub_species_taxid)                                        #Re-inserts the sub-species taxid
	taxonomic_lineage = (",".join([names[taxid] for taxid in lineage_without_no_rank]))      #Makes a string of the translated taxonomic lineage of the original taxid (without "no ranks" but including sub-species)
	unique_taxonomic_elements.update({x: taxonomic_lineage})                                 #Makes a new entry in the unique_taxonomic_elements dictionary with the original taxid as the
f.close()





#Makes a list of the GC % and taxonomic lineage of each contig 
#Since the taxonomic lineage of all taxonomic ids should be contained in the unique_taxonomic_elements dictionary, 
#no more search are necesary, and the loop just get the information from the dictionary

#Otputs the complete line in csv format for each contig in the .kraken file of the table
#Each line contains the Node (contig), its length, its coverage, its GC % and its taxonomic lineage
#The first three elements are imported from the "taba1.csv" auxiliary file and the last two were obtained in previous parts of this script
#Since this loop only does a simple join, if the NODE numbers in the .kraken file and the .fasta file are not in the same order
#the script will insert mismatches.

with open('aux1.txt') as ff, open('taba1.csv') as zz:
	all_taxids = [int(ii) for ii in ff]
	all_lines =[str(iv) for iv in zz]

for xx, line in zip(all_taxids, all_lines):
	n_contig += 1
	final_line = ""
	line_to_be_inserted = ",".join([str(all_GC[n_contig]),unique_taxonomic_elements.get(xx)])
	final_line = line.rstrip() + "," + line_to_be_inserted
	print (final_line)
ff.close()
zz.close() 