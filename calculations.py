#Run this script in python 3.0 or above

#To run this scripts the sys and ete3 libraries must be installed.

	#LIBRARIES AND GLOBAL VARIABLES

import sys                                     
from ete3 import NCBITaxa                      

ncbi = NCBITaxa()                             #Imports taxonomic information from "taxdump.tar.gz" file. This file needs to be located in the same directory as the scripts 
filepath = sys.argv[1]                        #Gets the path to the .fasta file
calculate_coverage = int(sys.argv[2])         #Variable that indicates if the coverage needs to be calculated. 1 is yes and 0 is no
total_length = int(sys.argv[3])               #Gets the total length of the contigs or scaffolds. It is only used when the coverage needs to be calculated

	#FUNCTIONS	

#This function calculates the coverage of each contig or scaffold using the fasta file and its total lenght as input
#It returns an array (with length = # of contigs or scaffolds) with the coverage of each contig or scaffold
def coverage(filepath, total_length):
	all_coverage = []
	with open("read_count_per_contig.txt", 'r') as all_read_count, open("contigs_len.txt", 'r') as all_contig_len: 
		for contig_len, read_count in zip(all_contig_len, all_read_count):
			total = float(int(contig_len) * int(read_count)/total_length)
			all_coverage.append(total)
        
	all_read_count.close()
	all_contig_len.close()
	return(all_coverage)


#This function calculates the GC % percentage of each contig or scaffold using the fasta file as input
#It returns an array (with length = # of contigs or scaffolds) with the GC % of each contig or scaffold
def GC_count(filepath):
	sequence = ""
	all_GC = []
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
	return(all_GC)
	#This function calculates the GC % of each contig and returns all the values as a list


#This function first translate the NCBI taxids of each contig or scaffold, obtained by using either Kraken or Kraken2, to a genomic lineage using the .kraken file as input
#To make a consistent table, the function eliminates intermediate levels of classification that are not featured in the final table. 
#To optimize the function, a dictionary with all the previously encountered taxids and their genomic lineage is created and updated in every iteration in a way that makes it easier to deal with duplicate taxids
#This functions prints the GC % percentage (obtained from the GC_count function) and the genomic lineage of each contig or scaffold 
def Taxid_GC_print(all_GC):

	taxonomic_info = []
	taxonomic_lineage = []                         
	unique_taxonomic_elements = {0: "Unassigned", 1: "Root", 2: "Bacteria"} 

	with open("kraken_taxIDs.txt") as f, open("temporal_table.csv") as ff:     #Opens the .krakenfile given by the user and creates the "output.labels" file
		all_taxids = [int(i) for i in f]
		all_prov_lines = [str(ii) for ii in ff] 
		n_contig = -1
		
		for taxid, prov_line in zip(all_taxids, all_prov_lines):
			n_contig += 1
			final_line = ""
			if taxid in unique_taxonomic_elements:
				line_to_be_inserted = ",".join([str(all_GC[n_contig]),unique_taxonomic_elements.get(taxid)])
				final_line = prov_line.rstrip() + "," + line_to_be_inserted
				print (final_line)
			else: 
				lineage = ncbi.get_lineage(taxid)                                                            #Gets the taxonomic lineage of a taxid 
				names = ncbi.get_taxid_translator(lineage)                                               #Gets the name of each component of the taxonomic lineage
				lineage2ranks = ncbi.get_rank(names)                                                     #Gets the taxonomic order (superkingdom, phylum, etc...) of each component of the taxonomic lineage
				no_rank=[k for k,v in lineage2ranks.items() if v== 'no rank']                            #Makes a list of the components of the lineage without a defined taxonomic order (the "no ranks")
				sub_species_taxid=lineage.pop()                                                          #Saves the sub-species taxid, as it does not have a formal taxonomic category yet 
				lineage_without_no_rank = [m for m in lineage if m not in no_rank]                       #Deletes the lineage components that do not have a defined taxonomic order
				lineage_without_no_rank.append(sub_species_taxid)                                        #Re-inserts the sub-species taxid
				taxonomic_lineage = (",".join([names[taxid] for taxid in lineage_without_no_rank]))      #Makes a string of the translated taxonomic lineage of the original taxid (without "no ranks" but including sub-species)
				unique_taxonomic_elements.update({taxid: taxonomic_lineage}) 
				
				line_to_be_inserted = ",".join([str(all_GC[n_contig]),taxonomic_lineage])
				final_line = prov_line.rstrip() + "," + line_to_be_inserted
				print (final_line)
	f.close()
	ff.close() #This function makes the taxonomic assignment of each  


#This function is mostly the same as the previous one. 
#However, this function also prints the coverage of each contig or scaffold (obtained from the coverage function) before printing its GC % and genomic lineage
def Taxid_GC_cov_print(all_GC, all_coverage):

	taxonomic_info = []
	taxonomic_lineage = []                         
	unique_taxonomic_elements = {0: "Unassigned", 1: "Root", 2: "Bacteria"} 

	with open("kraken_taxIDs.txt") as f, open("temporal_table.csv") as ff:     #Opens the .krakenfile given by the user and creates the "output.labels" file
		all_taxids = [int(i) for i in f]
		all_prov_lines = [str(ii) for ii in ff] 
		n_contig = -1
		
		for taxid, prov_line in zip(all_taxids, all_prov_lines):
			n_contig += 1
			final_line = ""
			if taxid in unique_taxonomic_elements:
				line_to_be_inserted = ",".join([str(all_coverage[n_contig]),str(all_GC[n_contig]),unique_taxonomic_elements.get(taxid)])
				final_line = prov_line.rstrip() + "," + line_to_be_inserted
				print (final_line)
			else: 
				lineage = ncbi.get_lineage(taxid)                                                            #Gets the taxonomic lineage of a taxid 
				names = ncbi.get_taxid_translator(lineage)                                               #Gets the name of each component of the taxonomic lineage
				lineage2ranks = ncbi.get_rank(names)                                                     #Gets the taxonomic order (superkingdom, phylum, etc...) of each component of the taxonomic lineage
				no_rank=[k for k,v in lineage2ranks.items() if v== 'no rank']                            #Makes a list of the components of the lineage without a defined taxonomic order (the "no ranks")
				sub_species_taxid=lineage.pop()                                                          #Saves the sub-species taxid, as it does not have a formal taxonomic category yet 
				lineage_without_no_rank = [m for m in lineage if m not in no_rank]                       #Deletes the lineage components that do not have a defined taxonomic order
				lineage_without_no_rank.append(sub_species_taxid)                                        #Re-inserts the sub-species taxid
				taxonomic_lineage = (",".join([names[taxid] for taxid in lineage_without_no_rank]))      #Makes a string of the translated taxonomic lineage of the original taxid (without "no ranks" but including sub-species)
				unique_taxonomic_elements.update({taxid: taxonomic_lineage}) 
				
				line_to_be_inserted = ",".join([str(all_coverage[n_contig]),str(all_GC[n_contig]),taxonomic_lineage])
				final_line = prov_line.rstrip() + "," + line_to_be_inserted
				print (final_line)
	f.close()
	ff.close() #This function makes the taxonomic assignment of each  

	
	#BODY
	
if calculate_coverage == 1:
	all_GC=GC_count(filepath)
	all_coverage=coverage(filepath, total_length)
	Taxid_GC_cov_print(all_GC, all_coverage)
else:
	all_GC=GC_count(filepath)
	Taxid_GC_print(all_GC)



