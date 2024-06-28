# For accessing NCBI Entrez databases
from Bio import Entrez        
# For convertion of data format or data manipulation
import pandas as pd           # For data manipulation and analysis
import numpy as np            # For numerical operations
import xmltodict              # For converting XML data to Python dictionaries
import json                   # For parsing JSON data
# For access to or manipulation of web data
import requests               # For making HTTP requests
import urllib3                # For advanced HTTP client functionalities
import ftplib                 # For handling FTP connectionssave_metadata
from bs4 import BeautifulSoup # For parsing HTML and XML documents
from io import StringIO       # For in-memory file-like objects

import os                     # For interacting with the operating system
import subprocess             # For running and interacting with system commands and processes

import re                     # For regular expression operations
import gzip                   # For reading and writing gzip-compressed files

import hashlib                # For generating MD5 checksums
# For displayed output
from tqdm import tqdm         # For displaying progress bars
from tabulate import tabulate # For printing data in a tabular format
# For management of time information
from datetime import datetime # For manipulating date and time objects
import time                   # For handling time-related tasks
# To make input or output of test code
import pickle                 # For serializing and deserializing Python objects



# To suppress the SSL warnings when using verify=False in the requests library
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

# Constant variables
from .constants import (
    EMAIL, 
    NCBI_FTP_URL,
    ENSEMBL_FTP_HOST,
    ENSEMBL_RAPID_FTP_URL,
    ENSEMBL_RM_FTP_URL,
    GENARK_URL,
    ZOONOMIA_URL,
    BIGWIG2BEDGRAPH,
    BEDGRAPH2BIGWIG,
    BIGBED2BED,
    BED2BIGBED,
    LS_NCBI_ASSEMBLY_META_KEY, 
    LS_NCBI_ASSEMBLY_META_LABEL, 
    LS_SRA_META_STUDY_KEY, 
    LS_SRA_META_SAMPLE_KEY, 
    LS_SRA_META_STUDY_LABEL, 
    LS_SRA_META_SAMPLE_LABEL, 
    LS_ASSEMBLY_REPORT_LABEL,
    DIC_ZOONOMIA,
    )

# Always tell NCBI who you are
Entrez.email = EMAIL
#Entrez.api_key = "Your_NCBI_API_Key"

# Global variables
DOWNLOAD_FOLDER_NAME = 'gencube_raw_download'
OUT_FOLDER_NAME = 'gencube_output'
script_dir = os.path.dirname(os.path.abspath(__file__))

## -----------------------------------------------------------
## gencube genome, geneset, sequence, annotation, crossgenome
## -----------------------------------------------------------
# Search genome using users keywords
def search_assembly (keywords):
    print('# Search assemblies in NCBI database')
    print(f'  Keyword: {keywords}\n')
    
    ls_search = []
    for keyword in keywords:
        #keyword = keyword.replace('_', ' ')
        
        # Search keyword in NCBI Assembly database
        try:
            handle = Entrez.esearch(db="assembly", term=keyword, retmax="10000")
            record = Entrez.read(handle)
            handle.close()

            assembly_id = record["IdList"]
            # Check if the id list is not empty
            if assembly_id:
                # Fetch detailed information using searched ids in NCBI Assembly database
                handle = Entrez.efetch(db="assembly", id=assembly_id, rettype="docsum")
                record = Entrez.read(handle)
                handle.close()
            
                ls_search += record['DocumentSummarySet']['DocumentSummary']
            else:
                print(f"  No results found for keyword '{keyword}'. \n")
        except Exception as e:
            print(f"  !! An error occurred while searching for keyword '{keyword}': {e} \n")
            continue
        
    if ls_search:
        return ls_search
    else:
        print(f"  !! No results found for all keyword.")

# Convert the data format
def json_to_dataframe (search, level, refseq, ucsc, latest):
    # Inner function
    def get_values_from_keys(dic):
        ls_value = []
        for key in LS_NCBI_ASSEMBLY_META_KEY:
            if key == 'Synonym_GCA':
                ls_value.append(dic['Synonym']['Genbank'])
            elif key == 'Synonym_GCF':
                ls_value.append(dic['Synonym']['RefSeq'])
            elif key == 'GB_BioProjects':
                if len(dic['GB_BioProjects']) > 0:    
                    ls_value.append(dic['GB_BioProjects'][0]['BioprojectAccn'])
                else:
                    ls_value.append('')
            elif key in dic:
                    ls_value.append(dic[key])
                
        return pd.DataFrame([ls_value], columns=LS_NCBI_ASSEMBLY_META_LABEL)

    n = len(search)
    if n < 2:
        print(f'  Total {len(search)} genomes is searched.\n')
    else:
        print(f'  Total {len(search)} genomes are searched.\n')
    print('# Convert JSON to dataframe format.')
    for i in range(len(search)):
        df_tmp = get_values_from_keys(search[i])

        if i == 0:
            df_assembly = df_tmp
        else:
            df_assembly = pd.concat([df_assembly, df_tmp])

    df_assembly = df_assembly.reset_index(drop=True)
    df_assembly['Release'] = df_assembly['Release'].apply(lambda x: x.split(' ')[0])
    df_assembly['Update'] = df_assembly['Update'].apply(lambda x: x.split(' ')[0])
    df_assembly['Level'] = df_assembly['Level'].replace('Complete Genome', 'Complete')
    # Merge RefSeq and Genbank accession in a column. (Priority: RefSeq > Genbank)
    df_assembly['NCBI'] = df_assembly.apply(
        lambda x: x['RefSeq'] if x['RefSeq'] != '' else x['Genbank'], 
        axis=1)
    
    # Check Level (Assembly status)
    ls_level = level.split(',')
    ls_level = [x.capitalize() for x in ls_level] # capitalize the first letter
    df_assembly_out = df_assembly[df_assembly['Level'].isin(ls_level)]
    
    # Extract latest genomes
    if latest:
        ls_index = []
        
        for idx in df_assembly_out.index:
            latest_acc = df_assembly_out.loc[idx, 'Latest accession']
            if latest_acc == '':
                ls_index.append(idx)
            elif  latest_acc[:3] == 'GCF':
                ls_index.append(df_assembly_out[df_assembly_out['RefSeq'] == latest_acc].index[0])
            elif  latest_acc[:3] == 'GCA':
                ls_index.append(df_assembly_out[df_assembly_out['Genbank'] == latest_acc].index[0])
            else: # 지울 부분!
                print('Latest accession is other type!')

        ls_index = list(set(ls_index))
        df_assembly_out = df_assembly_out.loc[ls_index]
    
    # Extract only genoms that RefSeq accession is issued.
    if refseq:
        df_assembly_out = df_assembly_out[df_assembly_out['RefSeq'] != '']
    # Extract only genoms that UCSC name is issued.
    if ucsc:
        df_assembly_out = df_assembly_out[df_assembly_out['UCSC'] != ''] 
    # Sort by Update
    df_assembly_out = df_assembly_out.sort_values(by='Update', ascending=False).reset_index(drop=True)
    # Print searched result    
    print('  Filter options')
    print(f'  Level:   {ls_level}')
    print(f'  RefSeq:  {refseq}')
    print(f'  UCSC:    {ucsc}')
    print(f'  Latest:  {latest}\n')
    
    return df_assembly_out

# Check the available genomes in GenArk and Ensembl (Rapid Release) server
def check_access_database (df, mode):
    if mode == 'genome':
        print('# Check accessibility to GenArk, Ensembl Rapid Release')
    elif mode == 'geneset':
        print('# Check accessibility to GenArk, Ensembl Rapid Release and Zoonomia server')
    elif mode == 'sequence':
        print('# Check accessibility to Ensembl Rapid Release')
    elif mode == 'annotation':
        print('# Check accessibility to GenArk')
    elif mode == 'crossgenome':
        print('# Check accessibility to Ensembl Rapid Release and Zoonomia server')
        
    ls_genark_mode = ['genome', 'geneset', 'annotation']
    ls_ensembl_mode = ['genome', 'geneset', 'sequence', 'crossgenome']
    ls_zoonomia_mode = ['geneset', 'crossgenome']
        
    # Check GenArk
    if mode in ls_genark_mode:
        genark_meta_url = GENARK_URL + 'UCSC_GI.assemblyHubList.txt'
        genark_meta = requests.get(genark_meta_url, verify=False).text.split('\n') # need to remove 'verify=False' later for security
        
        dic_genark_meta = {}
        for line in genark_meta:
            tmp = line.split()
            if len(tmp):
                if tmp[0] != '#':
                    dic_genark_meta[line.split('\t')[0]] = line.split('\t')[2]
        
        df[['GenArk']] = ''
        print(f'  UCSC GenArk  : {len(dic_genark_meta)} genomes across {len(list(set(dic_genark_meta.values())))} species')
                
    # Check Ensembl
    if mode in ls_ensembl_mode:
        ensembl_meta_url = ENSEMBL_RAPID_FTP_URL + 'species_metadata.json'
        ensembl_meta = requests.get(ensembl_meta_url).json()
        
        dic_ensembl_meta = {}
        for acc in ensembl_meta:
            dic_ensembl_meta[acc['assembly_accession']] = acc['species']
        
        df[['Ensembl']] = ''
        print(f'  Ensembl Rapid: {len(dic_ensembl_meta)} genomes across {len(list(set(dic_ensembl_meta.values())))} species')
        
    # Check Zoonomia
    if mode in ls_zoonomia_mode:
        df_zoonomia = pd.DataFrame()
        for reference in DIC_ZOONOMIA:
            url = f'{ZOONOMIA_URL}/{DIC_ZOONOMIA[reference]}/overview.table.tsv'
            df_tmp = pd.read_csv(download_csv(url, verify=False), sep='\t')  # need to remove 'verify=False' later for security
            df_tmp['reference'] = reference
            df_zoonomia = pd.concat([df_zoonomia, df_tmp])
        
        df[['Zoonomia']] = ''
        print(f'  Zoonomia TOGA: {df_zoonomia["NCBI accession / source"].nunique()} genomes across {df_zoonomia["Species"].nunique()} species')
    
    print('')
    
    # Check availability of the searched genomes in GenArk and Ensembl
    for idx in df.index:
        refseq_id = df.loc[idx]['RefSeq']
        genbank_id = df.loc[idx]['Genbank']
        
        if mode in ls_genark_mode and (refseq_id in dic_genark_meta or genbank_id in dic_genark_meta):
            df.loc[idx, 'GenArk'] = 'v'        
        if mode in ls_ensembl_mode and (genbank_id in dic_ensembl_meta or refseq_id in dic_ensembl_meta):
            df.loc[idx, 'Ensembl'] = 'v'
        if mode in ls_zoonomia_mode and (genbank_id in df_zoonomia["NCBI accession / source"].tolist() or refseq_id in df_zoonomia["NCBI accession / source"].tolist()):
            df.loc[idx, 'Zoonomia'] = 'v'

    if mode == 'genome':
        return df, dic_genark_meta, dic_ensembl_meta
    elif mode == 'geneset':
        return df, dic_genark_meta, dic_ensembl_meta, df_zoonomia
    elif mode == 'sequence':
        return df, dic_ensembl_meta
    elif mode == 'annotation':
        return df, dic_genark_meta
    elif mode == 'crossgenome':
        return df, dic_ensembl_meta, df_zoonomia

## ---------------------------------------------
## gencube genome
## ---------------------------------------------
# Download genome data and assembly report
def download_genome (df, types, masking, dic_genark_meta, dic_ensembl_meta, recursive):
    # Make download folder
    if not os.path.exists(DOWNLOAD_FOLDER_NAME):
        os.mkdir(DOWNLOAD_FOLDER_NAME)
    if not os.path.exists(OUT_FOLDER_NAME):
        os.mkdir(OUT_FOLDER_NAME)
    
    ls_type_raw = types.split(',')
    ls_types = []
    ls_wrong = []
    dic_download = {}
    # Change the order priority (refseq -> genbank -> others)
    for type_tmp in ['refseq', 'genbank', 'genark', 'ensembl']:
        if type_tmp in ls_type_raw:
            ls_types.append(type_tmp)
            
    for type_raw in ls_type_raw:
        # Check wrong arguments
        if type_raw not in ls_types:
            ls_wrong.append(type_raw)   
    
    print(f'# Download genome data: {ls_types} \n')
    if len(ls_wrong) > 0:
        print(f'Wrong input argument(s): {ls_wrong}\n')
    
    for idx in df.index:
        assembly_id = df.loc[idx]['Assembly name']
        genbank_id = df.loc[idx]['Genbank']
        refseq_id = df.loc[idx]['RefSeq']
        check_ensembl = df.loc[idx]['Ensembl']
        check_genark = df.loc[idx]['GenArk']
        # Renaming ex. "Homo sapiens (human)" -> "Homo_sapiens"
        organism = re.sub(r'\s*\([^)]*\)', '', df.loc[idx]['Organism']).replace(' ', '_')

        ls_download = []
        # Print assembly
        if refseq_id:
            print(f'[{genbank_id} / {refseq_id} / {assembly_id}]')
        else:
            print(f'[{genbank_id} / {assembly_id}]')
        
        report = False
        for type in ls_types:
            print(f'- {type}')
            # RefSeq
            if refseq_id: 
                refseq_dir = f'{NCBI_FTP_URL}/{refseq_id[0:3]}/{refseq_id[4:7]}/{refseq_id[7:10]}/{refseq_id[10:13]}/{refseq_id}_{assembly_id}'
                refseq_fa = f'{refseq_dir}/{refseq_id}_{assembly_id}_genomic.fna.gz'
                refseq_md5sum = f'{refseq_dir}/md5checksums.txt'
                refseq_rp = f'{refseq_dir}/{refseq_id}_{assembly_id}_assembly_report.txt'
                out_fa_name = f'{organism}-{assembly_id}-refseq.sm.fa.gz'
                out_rp_name = f'{organism}-{assembly_id}_assembly_report.txt'
                # Check and download assembly report.
                
                if not report:

                    if check_url(refseq_rp):
                        download_genome_url(refseq_rp, out_rp_name, refseq_md5sum, recursive=recursive)
                        report = True
                # Check and download RefSeq genome.
                if type == 'refseq':
                    
                    if check_url(refseq_fa):
                        download_genome_url(refseq_fa, out_fa_name, refseq_md5sum, recursive=recursive)
                        ls_download.append(f'refseq.sm')
                        continue 
                    else:
                        print('  !! Refseq genome is not available. Try to download in GenBank database.')
            elif type == 'refseq':
                print('  !! There is no Refseq accession. Try to download using GenBank accession.')

            # GenBank
            if not report or type == 'genbank':
                genbank_dir = f'{NCBI_FTP_URL}/{genbank_id[0:3]}/{genbank_id[4:7]}/{genbank_id[7:10]}/{genbank_id[10:13]}/{genbank_id}_{assembly_id}'
                genbank_fa = f'{genbank_dir}/{genbank_id}_{assembly_id}_genomic.fna.gz'
                genbank_md5sum = f'{genbank_dir}/md5checksums.txt'
                genbank_rp = f'{genbank_dir}/{genbank_id}_{assembly_id}_assembly_report.txt'
                out_fa_name = f'{organism}-{assembly_id}-genbank.sm.fa.gz'
                out_rp_name = f'{organism}-{assembly_id}_assembly_report.txt'

                if check_url(genbank_rp):
                    # Check and download assembly report.
                    if not report:
                        download_genome_url(genbank_rp, out_rp_name, genbank_md5sum, recursive=recursive)
                        report = True
                    # Check and download GenBank genome. 
                    if type in ['genbank', 'refseq']:
                        if check_url(genbank_fa):
                            download_genome_url(genbank_fa, out_fa_name, genbank_md5sum, recursive=recursive)
                            ls_download.append('genbank.sm')
                            continue
                else:
                    if not report:
                        print('  !! Assembly_report is not found in RefSeq and GenBank.')

                    if type == 'refseq':
                        print('  !! GenBank genome is also not available.')
                    elif type == 'genbank':
                            print('  !! GenBank genome is not available.')
                            
            
            # GenArk
            if type == 'genark':
                if check_genark:
                    if refseq_id in dic_genark_meta:
                        genark_id = refseq_id
                    else:
                        genark_id = genbank_id

                    genark_dif = f'{GENARK_URL}/{genark_id[0:3]}/{genark_id[4:7]}/{genark_id[7:10]}/{genark_id[10:13]}/{genark_id}' 
                    genark_fa = f'{genark_dif}/{genark_id}.fa.gz'
                    out_fa_name = f'{organism}-{assembly_id}-genark.sm.fa.gz'

                    if check_url(genark_fa):
                        download_genome_url(genark_fa, out_fa_name, recursive=recursive)
                        ls_download.append('genark.sm')
                        continue
                    else:
                        continue
                    
                else:
                    print('  GenArk genome is not available.')
                    continue


            # Ensembl.
            if type in ['ensembl']:
                if check_ensembl:
                    if genbank_id in dic_ensembl_meta:
                        ensembl_acc = genbank_id
                        organism_ens = dic_ensembl_meta[genbank_id].replace(' ', '_')
                    elif refseq_id in dic_ensembl_meta:
                        ensembl_acc = refseq_id
                        organism_ens = dic_ensembl_meta[refseq_id].replace(' ', '_')
                    
                    ensembl_dir = f'/pub/rapid-release/species/{organism_ens}/{ensembl_acc}'
                    
                    ls_source = list_ftp_directory(ENSEMBL_FTP_HOST, ensembl_dir)
                    
                    source = ''
                    ls_excluded = ['rnaseq', 'brake', 'statistics']
                    if ls_source:
                        for tmp in ls_excluded:
                            if tmp in ls_source:
                                ls_source.remove(tmp)

                    for source in ls_source:
                        ensembl_dir = f'{ENSEMBL_RAPID_FTP_URL}/species/{organism_ens}/{ensembl_acc}/{source}/genome'
                        
                        #suffix = {'soft' : 'softmasked', 'hard': 'hardmasked', 'none' : 'unmasked'}
                        #suffix_new = {'soft' : 'sm', 'hard': 'hm', 'none' : 'um'}
                        #ensembl_fa = f'{ensembl_dir}/{organism}-{ensembl_acc}-{suffix[masking]}.fa.gz'
                        #ensembl_md5sum = f'{ensembl_dir}/md5sum.txt'
                        #out_fa_name = f'{organism}-{assembly_id}-ensembl_{source}.{suffix_new[masking]}.fa.gz'
                        ensembl_fa = f'{ensembl_dir}/{organism}-{ensembl_acc}-softmasked.fa.gz'
                        ensembl_md5sum = f'{ensembl_dir}/md5sum.txt'
                        out_fa_name = f'{organism}-{assembly_id}-ensembl_{source}.sm.fa.gz'
                        
                        if check_url(ensembl_fa):
                            download_genome_url(ensembl_fa, out_fa_name, ensembl_md5sum)
                            ls_download.append(f'ensembl_{source}.sm')
                        else:
                            continue
                        
                else:
                    print('  Ensembl genome is not available.')
                    continue 
        print('')
        dic_download[genbank_id] = ls_download
    return dic_download

# Change chromosome names of genome file
def convert_chr_label_genome (df, dic_download, style, masking, compresslevel):

    dic_out_mask = {'soft' : 'soft-masked', 'hard' : 'hard-masked', 'none' : 'unmasked'} 
    print(f'# Change chromosome names and masking method: {style}-style & {dic_out_mask[masking]}')
    
    for idx in df.index:
        assembly_id = df.loc[idx]['Assembly name']
        organism = re.sub(r'\s*\([^)]*\)', '', df.loc[idx]['Organism']).replace(' ', '_')
        genbank_id = df.loc[idx]['Genbank']
        refseq_id = df.loc[idx]['RefSeq']
        
        # Print assembly
        if refseq_id:
            print(f'[{genbank_id} / {refseq_id} / {assembly_id}]')
        else:
            print(f'[{genbank_id} / {assembly_id}]')
        
        if not os.path.exists(f'{DOWNLOAD_FOLDER_NAME}/{organism}-{assembly_id}_assembly_report.txt'):
            print('  !! Assembly report is not found in RefSeq and GenBank.')
            print("     Chromosome names can't be changed. \n")
            break
        
        # Make integrative dataframe of chromosome label of databases
        df_report_edit = make_chr_dataframe (organism, assembly_id)

        # Check the number of UCSC 'na'
        ucsc_na_count = df_report_edit['ucsc'].str.contains('na', na=False).sum()
        # UCSC check
        if style == 'ucsc' and ucsc_na_count > 1:
            print(f'  {ucsc_na_count} chromosome(s) have not ucsc name.')
            break
        
        # Convert the DataFrame to dictionaries for faster lookup
        genbank_to_ensembl = df_report_edit.set_index('genbank')['ensembl'].to_dict()
        refseq_to_ensembl = df_report_edit.set_index('refseq')['ensembl'].to_dict()
        genbank_to_gencode = df_report_edit.set_index('genbank')['gencode'].to_dict()
        refseq_to_gencode = df_report_edit.set_index('refseq')['gencode'].to_dict()
        genbank_to_ucsc = df_report_edit.set_index('genbank')['ucsc'].to_dict()
        refseq_to_ucsc = df_report_edit.set_index('refseq')['ucsc'].to_dict()
        ensembl_to_gencode = df_report_edit.set_index('ensembl')['gencode'].to_dict()
        ensembl_to_ucsc = df_report_edit.set_index('ensembl')['ucsc'].to_dict()

        # Check downloaded files
        ls_download = dic_download[genbank_id]
        print(f'  Downloaded genome: {ls_download}')
        for db in ls_download:
            print(f'  - {db}')
            
            dic_out_mask = {'soft' : 'sm', 'hard' : 'hm', 'none' : 'um'} 
            dic_out_suffix = {'ensembl' : 'ens-id', 'gencode' : 'gc-id', 'ucsc' : 'ucsc-id'}
            
            # Input and output name
            db_name = db.split('.')[0]
            
            in_file = f'{organism}-{assembly_id}-{db}.fa.gz'
            out_file = f'{organism}-{assembly_id}-{db_name}.{dic_out_mask[masking]}.{dic_out_suffix[style]}.fa.gz'
            
            if 'ensembl' in db_name and style == 'ensembl' and masking == 'soft':
                if not os.path.exists(f'{OUT_FOLDER_NAME}/{out_file}'):
                    print('    The downloaded file already contains Ensembl-style names and is soft-masked.')
                    print('    Just copy to output folder.')
                    subprocess.run(['cp', f'{DOWNLOAD_FOLDER_NAME}/{in_file}', f'{OUT_FOLDER_NAME}/{out_file}'], check=True)
                    continue
                else:
                    print('    The converted file already exists.')
                    continue

            # File check in working directory
            ls_download_files = os.listdir(DOWNLOAD_FOLDER_NAME)
            ls_output_folder_files = os.listdir(OUT_FOLDER_NAME)
            ls_read = []
            ls_write = []
            if in_file in ls_download_files and out_file not in ls_output_folder_files:
                
                start_time = time.time() # record start times
                
                print('    Unify chromosome names')
                try:
                    with gzip.open(f'{DOWNLOAD_FOLDER_NAME}/{in_file}', 'rt') as f_in:
                        for line in f_in:
                            ls_read.append(line)
                except gzip.BadGzipFile:
                    print('    !! The file is not a valid gzip file. \n')

                for line in ls_read:
                    if line.startswith('>'):
                        chr_name = line.strip().split()[0][1:]
                        extra = ' '.join(line.strip().split()[1:])
                        if 'ensembl' in db_name:
                            if masking == 'hard':
                                extra = extra.replace('softmasked', 'hardmasked')
                            elif masking == 'none':
                                extra = extra.replace('softmasked', 'unmasked')
                                
                        # Perform the lookup based on the db and style
                        if db_name in ['genbank', 'refseq', 'genark']:
                            if style == 'ensembl':
                                chage_chr_name = genbank_to_ensembl.get(chr_name, refseq_to_ensembl.get(chr_name, chr_name))
                            elif style == 'gencode':
                                chage_chr_name = genbank_to_gencode.get(chr_name, refseq_to_gencode.get(chr_name, chr_name))
                            elif style == 'ucsc':
                                chage_chr_name = genbank_to_ucsc.get(chr_name, refseq_to_ucsc.get(chr_name, chr_name))
                        elif 'ensembl' in db_name:
                            if style == 'gencode':
                                chage_chr_name = ensembl_to_gencode.get(chr_name, chr_name)
                            elif style == 'ucsc':
                                chage_chr_name = ensembl_to_ucsc.get(chr_name, chr_name)

                        if 'ensembl' in db_name and style == 'ensembl':
                            ls_write.append(f'>{chr_name} {extra}\n')
                        else:
                            ls_write.append(f'>{chage_chr_name} {extra}\n')
                    else:
                        # Convert masking method in sequence information
                        # - Hard-masking
                        if masking == 'hard':
                            line_edit = ''
                            for char in line:
                                if char.islower():
                                    line_edit += 'N'
                                else:
                                    line_edit += char
                                    
                            ls_write.append(line_edit)
                        # - Unmasking            
                        elif masking == 'none':
                            ls_write.append(line.upper())
                            
                        # - Soft-masking
                        elif masking == 'soft':
                            ls_write.append(line)

                
                # Write and compressed fasta file
                print(f'    Write compressed fasta file (compresslevel: {compresslevel})')
                with gzip.open(f'{OUT_FOLDER_NAME}/{out_file}', 'wt', compresslevel=int(compresslevel)) as f_out:
                    for line in ls_write:
                        f_out.write(line)
                        
                end_time = time.time() # record end time
                elapsed_time = end_time - start_time
                print(f'    Processing time: {int(elapsed_time)} seconds')

            elif out_file in ls_output_folder_files:
                print('    The converted file already exists.')
        print('\n  !! If the file appears to have any problems, please delete it and retry the process. \n')


## ---------------------------------------------
## gencube geneset
## ---------------------------------------------
# Check full accessibility
def check_access_full_geneset (df, dic_genark_meta, dic_ensembl_meta, df_zoonomia):
    # Make dataframe for gencube annotation
    df_full_annotation = df[['Assembly name']].copy()
    # Make output dataframe
    ls_geneset = ['refseq', 'genark', 'ensembl', 'zoonomia']
    
    for label in ls_geneset:
        df_full_annotation.loc[:,label] = ''
    
    print('# Check accessible data in databases.')
    
    for idx in df.index:
        # Accession or name
        assembly_id = df.loc[idx]['Assembly name']
        genbank_id = df.loc[idx]['Genbank']
        refseq_id = df.loc[idx]['RefSeq']
        check_ensembl = df.loc[idx]['Ensembl']
        check_genark = df.loc[idx]['GenArk']
        check_zoonomia = df.loc[idx]['Zoonomia']

        # Print assembly
        if refseq_id:
            print(f'[{genbank_id} / {refseq_id} / {assembly_id}]')
        else:
            print(f'[{genbank_id} / {assembly_id}]')


        # RefSeq
        if refseq_id:
            
            refseq_dir = f'{NCBI_FTP_URL}/{refseq_id[0:3]}/{refseq_id[4:7]}/{refseq_id[7:10]}/{refseq_id[10:13]}/{refseq_id}_{assembly_id}'
            
            url_md5sum = f'{refseq_dir}/md5checksums.txt'
            refseq_gtf = f'{refseq_id}_{assembly_id}_genomic.gtf.gz'
            refseq_gff = f'{refseq_id}_{assembly_id}_genomic.gff.gz'
            refseq_genomon = f'{refseq_id}_{assembly_id}_gnomon_model.gff.gz'
            refseq_cross = f'{refseq_id}_{assembly_id}_cross_species_tx_alns.gff.gz'
            refseq_same = f'{refseq_id}_{assembly_id}_same_species_tx_alns.gff.gz'
            
            if check_url(url_md5sum):
                df_md5 = get_md5 (url_md5sum) # Read md5sum information
                ls_filename = df_md5['Filename'].str.split('/').str[-1].tolist()
                
                if refseq_gtf in ls_filename:
                    df_full_annotation.loc[idx, 'refseq'] = add_string (df_full_annotation.loc[idx, 'refseq'], 'gtf')
                if refseq_gff in ls_filename:
                    df_full_annotation.loc[idx, 'refseq'] = add_string (df_full_annotation.loc[idx, 'refseq'], 'gff')
                if refseq_genomon in ls_filename:
                    df_full_annotation.loc[idx, 'refseq'] = add_string (df_full_annotation.loc[idx, 'refseq'], 'gnomon')
                if refseq_cross in ls_filename:
                    df_full_annotation.loc[idx, 'refseq'] = add_string (df_full_annotation.loc[idx, 'refseq'], 'cross')
                if refseq_same in ls_filename:
                    df_full_annotation.loc[idx, 'refseq'] = add_string (df_full_annotation.loc[idx, 'refseq'], 'same')
            else:
                print('  !! There is not md5sum file')
            
        # Genark
        if check_genark:
            
            if refseq_id in dic_genark_meta:
                genark_id = refseq_id
            else:
                genark_id = genbank_id
            genark_dif = f'{GENARK_URL}/{genark_id[0:3]}/{genark_id[4:7]}/{genark_id[7:10]}/{genark_id[10:13]}/{genark_id}' 
            
            genark_augustus = f'{genark_dif}/genes/{genark_id}_{assembly_id}.augustus.gtf.gz'
            genark_xeno = f'{genark_dif}/genes/{genark_id}_{assembly_id}.xenoRefGene.gtf.gz'
            genark_ref = f'{genark_dif}/genes/{genark_id}_{assembly_id}.ncbiRefSeq.gtf.gz'
            
            if check_url(genark_augustus, verify=False): 
                df_full_annotation.loc[idx, 'genark'] = add_string (df_full_annotation.loc[idx, 'genark'], 'agustus')
            if check_url(genark_xeno, verify=False): 
                df_full_annotation.loc[idx, 'genark'] = add_string (df_full_annotation.loc[idx, 'genark'], 'xenoref')
            if check_url(genark_ref, verify=False): 
                df_full_annotation.loc[idx, 'genark'] = add_string (df_full_annotation.loc[idx, 'genark'], 'ref')
                
        # Ensembl
        if check_ensembl:
            
            if genbank_id in dic_ensembl_meta:
                ensembl_acc = genbank_id
                organism_ens = dic_ensembl_meta[genbank_id].replace(' ', '_')
            elif refseq_id in dic_ensembl_meta:
                ensembl_acc = refseq_id
                organism_ens = dic_ensembl_meta[refseq_id].replace(' ', '_')
            
            ensembl_dir = f'/pub/rapid-release/species/{organism_ens}/{ensembl_acc}'
            
            ls_source = list_ftp_directory(ENSEMBL_FTP_HOST, ensembl_dir)
            
            source = ''
            ls_excluded = ['rnaseq', 'brake', 'statistics']
            if ls_source:
                for tmp in ls_source:
                    if tmp not in ls_excluded:
                        if not source:
                            source = tmp
                        else:
                            source += f', {tmp}'
                        
            df_full_annotation.loc[idx, 'ensembl'] = add_string (df_full_annotation.loc[idx, 'ensembl'], source)
        
        # Zoonomia
        reference = ''
        if check_zoonomia:
            ls_reference = df_zoonomia[
                (df_zoonomia["NCBI accession / source"] == genbank_id) | 
                (df_zoonomia["NCBI accession / source"] == refseq_id)
                ]['reference'].tolist()
            for tmp in list(set(ls_reference)):
                if not reference:
                    reference = tmp
                else:
                    reference += f', {tmp}'
                    
            df_full_annotation.loc[idx, 'zoonomia'] = add_string (df_full_annotation.loc[idx, 'zoonomia'], reference)
    
    # Searched result
    print(tabulate(df_full_annotation, headers='keys', tablefmt='grid'))
    print('')
    
    return df_full_annotation

# Download geneset data
def download_geneset(df, df_genome, dic_ensembl_meta, dic_genark_meta, df_zoonomia, types, styles, recursive):
    # Make download folder
    if not os.path.exists(DOWNLOAD_FOLDER_NAME):
        os.mkdir(DOWNLOAD_FOLDER_NAME)
    if not os.path.exists(OUT_FOLDER_NAME):
        os.mkdir(OUT_FOLDER_NAME)
        
    ls_types = types.split(',')
    
    print('# Download geneset data.')
    dic_download = {}
    for idx in df.index:
        # Accession or name
        assembly_id = df_genome.loc[idx]['Assembly name']
        genbank_id = df_genome.loc[idx]['Genbank']
        refseq_id = df_genome.loc[idx]['RefSeq']
        organism = re.sub(r'\s*\([^)]*\)', '', df_genome.loc[idx]['Organism']).replace(' ', '_')
        
        check_refseq = df.loc[idx]['refseq']
        check_genark = df.loc[idx]['genark']
        check_ensembl = df.loc[idx]['ensembl']
        check_zoonomia = df.loc[idx]['zoonomia']
        
        # Print assembly
        if refseq_id:
            print(f'[{genbank_id} / {refseq_id} / {assembly_id}]')
        else:
            print(f'[{genbank_id} / {assembly_id}]')
        
        ls_download = []
        # RefSeq
        if len(list(set(['refseq_gtf', 'refseq_gff', 'gnomon', 'cross_species', 'same_species']) & set(ls_types))) > 0:
            
            refseq_dir = f'{NCBI_FTP_URL}/{refseq_id[0:3]}/{refseq_id[4:7]}/{refseq_id[7:10]}/{refseq_id[10:13]}/{refseq_id}_{assembly_id}'
            
            ls_search = check_refseq.replace(' ', '').split(',')
            url_md5sum = f'{refseq_dir}/md5checksums.txt'
            refseq_gtf = f'{refseq_dir}/{refseq_id}_{assembly_id}_genomic.gtf.gz'
            refseq_gff = f'{refseq_dir}/{refseq_id}_{assembly_id}_genomic.gff.gz'
            refseq_genomon = f'{refseq_dir}/Gnomon_models/{refseq_id}_{assembly_id}_gnomon_model.gff.gz'
            refseq_cross = f'{refseq_dir}/Evidence_alignments/{refseq_id}_{assembly_id}_cross_species_tx_alns.gff.gz'
            refseq_same = f'{refseq_dir}/Evidence_alignments/{refseq_id}_{assembly_id}_same_species_tx_alns.gff.gz'
            
            if check_refseq:
                if 'refseq_gtf' in ls_types:
                    if 'gtf' in ls_search:
                        if check_url(refseq_gtf):
                            out_name = f'{organism}-{assembly_id}-refseq.gtf.gz'
                            download_url(refseq_gtf, out_name, url_md5sum=url_md5sum)
                            ls_download.append('refseq_gtf')
                        
                if 'refseq_gff' in ls_types:
                    if 'gff' in ls_search:
                        out_name = f'{organism}-{assembly_id}-refseq.gff.gz'
                        download_url(refseq_gff, out_name, url_md5sum=url_md5sum)
                        ls_download.append('refseq_gff')
                        
                if 'gnomon' in ls_types:
                    if 'gnomon' in ls_search:
                        out_name = f'{organism}-{assembly_id}-refseq_genomon.gff.gz'
                        download_url(refseq_genomon, out_name, url_md5sum=url_md5sum)
                        ls_download.append('gnomon')
                        
                if 'cross' in ls_types:
                    if 'cross' in ls_search:
                        out_name = f'{organism}-{assembly_id}-refseq_cross.gff.gz'
                        download_url(refseq_cross, out_name, url_md5sum=url_md5sum)
                        ls_download.append('cross_species')
                        
                if 'same' in ls_types:
                    if 'same' in ls_search:
                        out_name = f'{organism}-{assembly_id}-refseq_same.gff.gz'
                        download_url(refseq_same, out_name, url_md5sum=url_md5sum)
                        ls_download.append('same_species')

        # Genark
        if len(list(set(['agustus', 'xenoref', 'genark_ref']) & set(ls_types))) > 0:
            
            if refseq_id in dic_genark_meta:
                genark_id = refseq_id
            else:
                genark_id = genbank_id
            genark_dif = f'{GENARK_URL}/{genark_id[0:3]}/{genark_id[4:7]}/{genark_id[7:10]}/{genark_id[10:13]}/{genark_id}' 
            
            ls_search = check_genark.replace(' ', '').split(',')
            genark_augustus = f'{genark_dif}/genes/{genark_id}_{assembly_id}.augustus.gtf.gz'
            genark_xeno = f'{genark_dif}/genes/{genark_id}_{assembly_id}.xenoRefGene.gtf.gz'
            genark_ref = f'{genark_dif}/genes/{genark_id}_{assembly_id}.ncbiRefSeq.gtf.gz'
            
            if check_genark:
                
                if 'agustus' in ls_types:
                    if 'agustus' in ls_search:
                        out_name = f'{organism}-{assembly_id}-genark_agustus.gtf.gz'
                        download_url(genark_augustus, out_name, verify=False, recursive=recursive)
                        ls_download.append('agustus')
                        
                if 'xenoref' in ls_types:
                    if 'xenoref' in ls_search:
                        out_name = f'{organism}-{assembly_id}-genark_xenoref.gtf.gz'
                        download_url(genark_xeno, out_name, verify=False, recursive=recursive)
                        ls_download.append('xenoref')
                        
                if 'genark_ref' in ls_types:
                    if 'ref' in ls_search:
                        out_name = f'{organism}-{assembly_id}-genark_refseq.gtf.gz'
                        download_url(genark_ref, out_name, verify=False, recursive=recursive)
                        ls_download.append('genark_ref')
                
        # Ensembl
        if len(list(set(['ensembl_gtf', 'ensembl_gff']) & set(ls_types))) > 0:
            
            if genbank_id in dic_ensembl_meta:
                ensembl_acc = genbank_id
                organism_ens = dic_ensembl_meta[genbank_id].replace(' ', '_')
            elif refseq_id in dic_ensembl_meta:
                ensembl_acc = refseq_id
                organism_ens = dic_ensembl_meta[refseq_id].replace(' ', '_')
            
            if check_ensembl:
                ls_source = check_ensembl.replace(' ', '').split(',')
                
                for source in ls_source:
                    ensembl_dir = f'/pub/rapid-release/species/{organism_ens}/{ensembl_acc}/{source}/geneset'
                    # Check the geneset folder name
                    geneset = list_ftp_directory(ENSEMBL_FTP_HOST, ensembl_dir)[0]
                    
                    ensembl_file_dir = f'{ENSEMBL_RAPID_FTP_URL}/species/{organism_ens}/{ensembl_acc}/{source}/geneset/{geneset}'

                    url_md5sum = f'{ensembl_file_dir}/md5sum.txt'
                    ensembl_gtf = f'{ensembl_file_dir}/{organism_ens}-{ensembl_acc}-{geneset}-genes.gtf.gz'
                    ensembl_gff = f'{ensembl_file_dir}/{organism_ens}-{ensembl_acc}-{geneset}-genes.gff3.gz'
                    
                    if 'ensembl_gtf' in ls_types:
                        if check_url(ensembl_gtf):
                            out_name = f'{organism}-{assembly_id}-ensembl_{source}.gtf.gz'
                            download_url(ensembl_gtf, out_name, url_md5sum=url_md5sum)
                            ls_download.append(f'ensembl-{source}-gtf')

                    if 'ensembl_gff' in ls_types:
                        if check_url(ensembl_gff):
                            out_name = f'{organism}-{assembly_id}-ensembl_{source}.gff.gz'
                            download_url(ensembl_gff, out_name, url_md5sum=url_md5sum)
                            ls_download.append(f'ensembl-{source}-gff')
            
        # Zoonomia
        if len(list(set(['toga_gtf', 'toga_bed', 'toga_pseudo']) & set(ls_types))) > 0:
            
            if check_zoonomia:
                ls_reference = check_zoonomia.replace(' ', '').split(',')
                
                for reference in ls_reference:
                    
                    zoonomia_dir = f'{ZOONOMIA_URL}/{DIC_ZOONOMIA[reference]}'
                    
                    df_tmp = df_zoonomia[
                        ((df_zoonomia['NCBI accession / source'] == genbank_id) | 
                        (df_zoonomia['NCBI accession / source'] == refseq_id)) &
                        (df_zoonomia['reference'] == reference)
                    ]
                    
                    for i in range(len(df_tmp.index)):
                        taxo = df_tmp['Taxonomic Lineage'].values[i]
                        species = df_tmp['Species'].values[i].replace(' ', '_')
                        name = df_tmp['Common name'].values[i].replace(' ', '_')
                        assembly = df_tmp['Assembly name'].values[i]

                        if reference in ['human', 'mouse', 'chicken']:
                            ls_folders = list_http_folders(zoonomia_dir)
                        
                            for folder in ls_folders:
                                if folder in taxo:
                                    category = folder
                                    break
                            
                            zoonomia_file_dir = f'{zoonomia_dir}/{category}/{species}__{name}__{assembly}'
                        else:
                            zoonomia_file_dir = f'{zoonomia_dir}/{species}__{name}__{assembly}'
                        
                        zoonomia_gtf = f'{zoonomia_file_dir}/geneAnnotation.gtf.gz'
                        zoonomia_bed = f'{zoonomia_file_dir}/geneAnnotation.bed.gz'
                        zoonomia_pseudo = f'{zoonomia_file_dir}/processedPseudogeneAnnotation.bed.gz'
                        
                        if 'toga_gtf' in ls_types:
                            if check_url(zoonomia_gtf, verify=False):
                                out_gtf_name = f'{organism}-{assembly_id}-toga_{reference}.gtf.gz'
                                download_url(zoonomia_gtf, out_gtf_name, verify=False, recursive=recursive)
                                ls_download.append(f'zoonomia-{reference}-gtf')
                        
                        if 'toga_bed' in ls_types:
                            if check_url(zoonomia_bed, verify=False):
                                out_bed_name = f'{organism}-{assembly_id}-toga_{reference}.bed.gz'
                                download_url(zoonomia_bed, out_bed_name, verify=False, recursive=recursive)
                                ls_download.append(f'zoonomia-{reference}-bed')
                                
                        if 'toga_pseudo' in ls_types:
                            if check_url(zoonomia_pseudo, verify=False):
                                out_bed_name = f'{organism}-{assembly_id}-toga_{reference}_pseudo.bed.gz'
                                download_url(zoonomia_pseudo, out_bed_name, verify=False, recursive=recursive)
                                ls_download.append(f'zoonomia-{reference}-pseudobed')
                
        dic_download[genbank_id] = ls_download
        print('')
    return dic_download

# Change chromosome names of geneset file
def convert_chr_label_geneset (df, dic_download, style):
        
    print(f'# Change chromosome names: {style}-style')
    
    for idx in df.index:
        assembly_id = df.loc[idx]['Assembly name']
        organism = re.sub(r'\s*\([^)]*\)', '', df.loc[idx]['Organism']).replace(' ', '_')
        genbank_id = df.loc[idx]['Genbank']
        refseq_id = df.loc[idx]['RefSeq']
        
        # Print assembly
        if refseq_id:
            print(f'[{genbank_id} / {refseq_id} / {assembly_id}]')
        else:
            print(f'[{genbank_id} / {assembly_id}]')
            
        # Download assembly report
        print('  Download assembly report')
        report = False
        # RefSeq
        if refseq_id: 
            refseq_dir = f'{NCBI_FTP_URL}/{refseq_id[0:3]}/{refseq_id[4:7]}/{refseq_id[7:10]}/{refseq_id[10:13]}/{refseq_id}_{assembly_id}'
            refseq_md5sum = f'{refseq_dir}/md5checksums.txt'
            refseq_rp = f'{refseq_dir}/{refseq_id}_{assembly_id}_assembly_report.txt'
            out_rp_name = f'{organism}-{assembly_id}_assembly_report.txt'
            # Check and download assembly report.

            if check_url(refseq_rp):
                download_genome_url(refseq_rp, out_rp_name, refseq_md5sum)
                report = True

        # GenBank
        if not report:
            genbank_dir = f'{NCBI_FTP_URL}/{genbank_id[0:3]}/{genbank_id[4:7]}/{genbank_id[7:10]}/{genbank_id[10:13]}/{genbank_id}_{assembly_id}'
            genbank_md5sum = f'{genbank_dir}/md5checksums.txt'
            genbank_rp = f'{genbank_dir}/{genbank_id}_{assembly_id}_assembly_report.txt'
            out_rp_name = f'{organism}-{assembly_id}_assembly_report.txt'            

            if check_url(genbank_rp):
                # Check and download assembly report.
                download_genome_url(genbank_rp, out_rp_name, genbank_md5sum)

            else:
                print('  !! Assembly report is not found in RefSeq and GenBank.')
                print("     Chromosome names can't be changed. \n")
                break
                
        # Make integrative dataframe of chromosome label of databases
        df_report_edit = make_chr_dataframe (organism, assembly_id)

        # Check the number of UCSC 'na'
        ucsc_na_count = df_report_edit['ucsc'].str.contains('na', na=False).sum()
        # UCSC check
        if style == 'ucsc' and ucsc_na_count > 1:
            print(f'  {ucsc_na_count} chromosome(s) have not ucsc name.')
            break

        df_report_edit['genbank_noversion'] = df_report_edit['genbank'].apply(lambda x: x.split('.')[0])
        df_report_edit['refseq_noversion'] = df_report_edit['refseq'].apply(lambda x: x.split('.')[0])
        
        # Convert the DataFrame to dictionaries for faster lookup
        genbank_to_ensembl = df_report_edit.set_index('genbank')['ensembl'].to_dict()
        refseq_to_ensembl = df_report_edit.set_index('refseq')['ensembl'].to_dict()
        genbank_to_gencode = df_report_edit.set_index('genbank')['gencode'].to_dict()
        refseq_to_gencode = df_report_edit.set_index('refseq')['gencode'].to_dict()
        genbank_to_ucsc = df_report_edit.set_index('genbank')['ucsc'].to_dict()
        refseq_to_ucsc = df_report_edit.set_index('refseq')['ucsc'].to_dict()
        ensembl_to_gencode = df_report_edit.set_index('ensembl')['gencode'].to_dict()
        ensembl_to_ucsc = df_report_edit.set_index('ensembl')['ucsc'].to_dict()
        ucsc_to_ensembl = df_report_edit.set_index('ucsc')['ensembl'].to_dict()
        ucsc_to_gencode = df_report_edit.set_index('ucsc')['gencode'].to_dict()
        # For Zoonomia data
        genbank_noversion_to_ensembl = df_report_edit.set_index('genbank_noversion')['ensembl'].to_dict()
        refseq_noversion_to_ensembl = df_report_edit.set_index('refseq_noversion')['ensembl'].to_dict()
        genbank_noversion_to_gencode = df_report_edit.set_index('genbank_noversion')['gencode'].to_dict()
        refseq_noversion_to_gencode = df_report_edit.set_index('refseq_noversion')['gencode'].to_dict()
        genbank_noversion_to_ucsc = df_report_edit.set_index('genbank_noversion')['ucsc'].to_dict()
        refseq_noversion_to_ucsc = df_report_edit.set_index('refseq_noversion')['ucsc'].to_dict()

        # Check the number of UCSC 'na'
        ucsc_na_count = df_report_edit['ucsc'].str.contains('na', na=False).sum()
        # UCSC check
        if style == 'ucsc' and ucsc_na_count > 1:
            print(f'  {ucsc_na_count} chromosome(s) have not ucsc name.')
            break

        # Check downloaded files
        ls_download = dic_download[genbank_id]
        print(f'  Downloaded genome: {ls_download}')
        
        
        dic_db_suffix = {
            'refseq_gtf' : 'refseq.gtf.gz',
            'refseq_gff' : 'refseq.gff.gz',
            'gnomon' : 'refseq_genomon.gff.gz',
            'cross_species' : 'refseq_cross.gff.gz',
            'same_species' : 'refseq_same.gff.gz',
            'agustus' : 'genark_agustus.gtf.gz',
            'xenoref' : 'genark_xenoref.gtf.gz',
            'genark_ref' : 'genark_refseq.gtf.gz',
        }
        dic_out_suffix = {'ensembl' : 'ens-id', 'gencode' : 'gc-id', 'ucsc' : 'ucsc-id'}
        
        for db in ls_download:
            print(f'- {db}')
            
            # Input and output name
            if 'ensembl' in db:
                ls_tmp = db.split('-')
                if ls_tmp[2] == 'gtf':
                    in_file = f'{organism}-{assembly_id}-ensembl_{ls_tmp[1]}.gtf.gz'
                    out_file = f'{organism}-{assembly_id}-ensembl_{ls_tmp[1]}.{dic_out_suffix[style]}.gtf'
                elif ls_tmp[2] == 'gff':
                    in_file = f'{organism}-{assembly_id}-ensembl_{ls_tmp[1]}.gff.gz'
                    out_file = f'{organism}-{assembly_id}-ensembl_{ls_tmp[1]}.{dic_out_suffix[style]}.gff'
            elif 'zoonomia' in db:
                ls_tmp = db.split('-')
                if ls_tmp[2] == 'gtf':
                    in_file = f'{organism}-{assembly_id}-toga_{ls_tmp[1]}.gtf.gz'
                    out_file = f'{organism}-{assembly_id}-toga_{ls_tmp[1]}.{dic_out_suffix[style]}.gtf'
                elif ls_tmp[2] == 'bed':
                    in_file = f'{organism}-{assembly_id}-toga_{ls_tmp[1]}.bed.gz'
                    out_file = f'{organism}-{assembly_id}-toga_{ls_tmp[1]}.{dic_out_suffix[style]}.bed'
                elif ls_tmp[2] == 'pseudobed':
                    in_file = f'{organism}-{assembly_id}-toga_{ls_tmp[1]}_pseudo.bed.gz'
                    out_file = f'{organism}-{assembly_id}-toga_{ls_tmp[1]}_pseudo.{dic_out_suffix[style]}.bed'
            else:
                db_suffix = dic_db_suffix[db].split('.')
                
                in_file = f'{organism}-{assembly_id}-{dic_db_suffix[db]}'
                out_file = f'{organism}-{assembly_id}-{db_suffix[0]}.{dic_out_suffix[style]}.{db_suffix[1]}'
                
            if db in ['ensembl_gtf', 'ensembl_gff'] and style == 'ensembl':
                # print('  !! The file downloaded from the Ensembl database already has ensembl-style chromosome names.')
                continue
            
            # File check in working directory
            ls_download_files = os.listdir(DOWNLOAD_FOLDER_NAME)
            ls_output_folder_files = os.listdir(OUT_FOLDER_NAME)
            
            print(f'  Unify chromosome names')
            if in_file in ls_download_files and out_file not in ls_output_folder_files:
                
                ls_read = []
                ls_write = []         
                try:
                    with gzip.open(f'{DOWNLOAD_FOLDER_NAME}/{in_file}', 'rt') as f_in:
                        for line in f_in:
                            ls_read.append(line)
                            
                except gzip.BadGzipFile:
                    print('  !! The file is not a valid gzip file. \n')              
                
                count = 0
                for line in ls_read:
                    if not line.startswith('#'):
                        ls_tmp = line.strip().split('\t')
                        chr_name = ls_tmp[0]
                        
                        # Remove 'gene' block in refeq geneset data
                        category = ls_tmp[2]
                        if category == 'gene' or category == 'region':
                                continue
                        
                        # Change the chromosome name
                        if db in ['refseq_gtf', 'refseq_gff', 'gnomon', 'cross_species', 'same_species', 'agustus', 'xenoref', 'genark_ref']:
                            if style == 'ensembl':
                                ls_tmp[0] = genbank_to_ensembl.get(chr_name, refseq_to_ensembl.get(chr_name, chr_name))
                            elif style == 'gencode':
                                ls_tmp[0] = genbank_to_gencode.get(chr_name, refseq_to_gencode.get(chr_name, chr_name))
                            elif style == 'ucsc':
                                ls_tmp[0] = genbank_to_ucsc.get(chr_name, refseq_to_ucsc.get(chr_name, chr_name))
                        elif 'ensembl' in db:                         
                            if style == 'gencode':
                                ls_tmp[0] = ensembl_to_gencode.get(chr_name, chr_name)
                            elif style == 'ucsc':
                                ls_tmp[0] = ensembl_to_ucsc.get(chr_name, chr_name)
                        elif 'zoonomia' in db:
                            if style == 'ensembl':
                                ls_tmp[0] = ucsc_to_ensembl.get(chr_name, genbank_noversion_to_ensembl.get(chr_name, refseq_noversion_to_ensembl.get(chr_name, chr_name)))
                            elif style == 'gencode':
                                ls_tmp[0] = ucsc_to_gencode.get(chr_name, genbank_noversion_to_gencode.get(chr_name, refseq_noversion_to_gencode.get(chr_name, chr_name)))
                            elif style == 'ucsc':
                                ls_tmp[0] = genbank_noversion_to_ucsc.get(chr_name, refseq_noversion_to_ucsc.get(chr_name, chr_name))

                        line_edit = '\t'.join(ls_tmp) + '\n'
                        ls_write.append(line_edit)
                        
                        count += 1
                    else:
                        ls_write.append(line)

                """
                # Write and compressed gtf, gff, and bed file
                with gzip.open(f'{OUT_FOLDER_NAME}/{out_file}', 'wt', compresslevel=9) as f_out:
                    for line in ls_write:
                        f_out.write(line)
                """
                # Write gtf, gff, and bed file
                with open(f'{OUT_FOLDER_NAME}/{out_file}', 'w') as f_out:
                    for line in ls_write:
                        f_out.write(line)
                        
                
                
                # Sort file
                print('  Sort file')
                format = out_file.split('.')[-1]
                
                if format == 'bed': # bed format
                    with open(f'{OUT_FOLDER_NAME}/{out_file}', 'w') as f_out:
                        subprocess.run(['sort', '-k1,1', '-k2,2n', f'{OUT_FOLDER_NAME}/{out_file}_tmp'], stdout=f_out, check=True)
                else:               # gtf or gff format
                    with open(f'{OUT_FOLDER_NAME}/{out_file}', 'w') as f_out:
                        subprocess.run(['sort', '-k1,1', '-k4,4n', f'{OUT_FOLDER_NAME}/{out_file}_tmp'], stdout=f_out, check=True)

                # Compress file
                subprocess.run(['gzip', '--best', '--force', f'{OUT_FOLDER_NAME}/{out_file}'], check=True)
                
                """
                # Make index file
                print(f'  Make index file: {OUT_FOLDER_NAME}/{out_file}.gz')
                if format == 'bed': # bed format
                    #bed = pybedtools.BedTool(f'{OUT_FOLDER_NAME}/{out_file}.gz')
                    pysam.tabix_index(f'{OUT_FOLDER_NAME}/{out_file}.gz', force=True, preset='bed')
                elif format =='gtf':
                    #gtf = pybedtools.BedTool(f'{OUT_FOLDER_NAME}/{out_file}.gz')
                    pysam.tabix_index(f'{OUT_FOLDER_NAME}/{out_file}.gz', force=True, preset='gff')
                elif format == 'gff':
                    #gff = pybedtools.BedTool(f'{OUT_FOLDER_NAME}/{out_file}.gz')
                    pysam.tabix_index(f'{OUT_FOLDER_NAME}/{out_file}.gz', force=True, preset='gff')
                else:
                    print(f'debug point: format == {format}')
                """

                print('')
        
            else:
                print('  The output file already exists.')
                print('  !! If the file appears to have any problems, please delete it and retry the process. \n')


## ---------------------------------------------
## gencube sequence
## ---------------------------------------------
# Check full accessibility
def check_access_full_sequence (df, dic_ensembl_meta):
    # Make dataframe for gencube annotation
    df_full_annotation = df[['Assembly name']].copy()
    # Make output dataframe
    ls_sequence = ['refseq', 'ensembl', 'ensembl_repeat']
    
    for label in ls_sequence:
        df_full_annotation.loc[:,label] = ''
    
    print('# Check accessible data in databases.')
    
    for idx in df.index:
        # Accession or name
        assembly_id = df.loc[idx]['Assembly name']
        genbank_id = df.loc[idx]['Genbank']
        refseq_id = df.loc[idx]['RefSeq']
        check_ensembl = df.loc[idx]['Ensembl']
        organism = re.sub(r'\s*\([^)]*\)', '', df.loc[idx]['Organism']).replace(' ', '_')

        # Print assembly
        if refseq_id:
            print(f'[{genbank_id} / {refseq_id} / {assembly_id}]')
        else:
            print(f'[{genbank_id} / {assembly_id}]')
        
        # RefSeq
        if refseq_id:
            refseq_dir = f'{NCBI_FTP_URL}/{refseq_id[0:3]}/{refseq_id[4:7]}/{refseq_id[7:10]}/{refseq_id[10:13]}/{refseq_id}_{assembly_id}'
            
            url_md5sum = f'{refseq_dir}/md5checksums.txt'
            refseq_rna = f'{refseq_id}_{assembly_id}_rna.fna.gz'
            refseq_rna_geno = f'{refseq_id}_{assembly_id}_rna_from_genomic.fna.gz'
            refseq_cds_geno = f'{refseq_id}_{assembly_id}_cds_from_genomic.fna.gz'
            refseq_pseudo = f'{refseq_id}_{assembly_id}_pseudo_without_product.fna.gz'
            
            refseq_protein = f'{refseq_id}_{assembly_id}_protein.faa.gz'
            refseq_trans_cds = f'{refseq_id}_{assembly_id}_translated_cds.faa.gz'
            
            if check_url(url_md5sum):
                df_md5 = get_md5 (url_md5sum) # Read md5sum information
                ls_filename = df_md5['Filename'].str.split('/').str[-1].tolist()

                if refseq_rna in ls_filename:
                    df_full_annotation.loc[idx, 'refseq'] = add_string (df_full_annotation.loc[idx, 'refseq'], 'rna')
                if refseq_rna_geno in ls_filename:
                    df_full_annotation.loc[idx, 'refseq'] = add_string (df_full_annotation.loc[idx, 'refseq'], 'rna_genomic')
                if refseq_cds_geno in ls_filename:
                    df_full_annotation.loc[idx, 'refseq'] = add_string (df_full_annotation.loc[idx, 'refseq'], 'cds_genomic')
                if refseq_pseudo in ls_filename:
                    df_full_annotation.loc[idx, 'refseq'] = add_string (df_full_annotation.loc[idx, 'refseq'], 'pseudo')
                if refseq_protein in ls_filename:
                    df_full_annotation.loc[idx, 'refseq'] = add_string (df_full_annotation.loc[idx, 'refseq'], 'pep')
                if refseq_trans_cds in ls_filename:
                    df_full_annotation.loc[idx, 'refseq'] = add_string (df_full_annotation.loc[idx, 'refseq'], 'pep_cds')
            else:
                print('  !! There is not md5sum file')

        # Ensembl.
        if check_ensembl:
            if genbank_id in dic_ensembl_meta:
                ensembl_acc = genbank_id
                organism_ens = dic_ensembl_meta[genbank_id].replace(' ', '_')
            elif refseq_id in dic_ensembl_meta:
                ensembl_acc = refseq_id
                organism_ens = dic_ensembl_meta[refseq_id].replace(' ', '_')
            
            ensembl_dir = f'/pub/rapid-release/species/{organism_ens}/{ensembl_acc}'
            
            ls_source = list_ftp_directory(ENSEMBL_FTP_HOST, ensembl_dir)
            
            source = ''
            ls_excluded = ['rnaseq', 'brake', 'statistics']
            if ls_source:
                for tmp in ls_excluded:
                    if tmp in ls_source:
                        ls_source.remove(tmp)

            ls_input = []
            for source in ls_source:
                ls_tmp = [source]
                ensembl_geneset_dir = f'/pub/rapid-release/species/{organism_ens}/{ensembl_acc}/{source}/geneset'
                # Check the geneset folder name
                geneset = list_ftp_directory(ENSEMBL_FTP_HOST, ensembl_geneset_dir)[0]
                ensembl_file_dir = f'{ENSEMBL_RAPID_FTP_URL}/species/{organism_ens}/{ensembl_acc}/{source}/geneset/{geneset}'
                
                url_md5sum = f'{ensembl_file_dir}/md5sum.txt'
                ensembl_cdna = f'{organism}-{ensembl_acc}-{geneset}-cdna.fa.gz'
                ensembl_cds = f'{organism}-{ensembl_acc}-{geneset}-cds.fa.gz'
                ensembl_pep = f'{organism}-{ensembl_acc}-{geneset}-pep.fa.gz'
                
                if check_url(url_md5sum): 
                    df_md5 = get_md5 (url_md5sum) # Read md5sum information
                    ls_filename = df_md5['Filename'].str.split('/').str[-1].tolist()
                    
                    if ensembl_cdna in ls_filename:
                        ls_tmp.append('cdna')
                    if ensembl_cds in ls_filename:
                        ls_tmp.append('cds')
                    if ensembl_pep in ls_filename:
                        ls_tmp.append('pep')
                    
                    ls_input.append(ls_tmp)

                else:
                    print('There is not md5sum file')
                
            if ls_input:
                str_input = ''
                for i in range(len(ls_input)):
                    if i != 0:
                        str_input += f' / '
                    for j in range(len(ls_input[i])):
                        if j == 0:
                            str_input += f'{ls_input[i][j]}:'
                        else:
                            str_input += f' {ls_input[i][j]}'
                        if j != 0 and j != len(ls_input[i]) - 1:
                            str_input += f','
                
                df_full_annotation.loc[idx, 'ensembl'] = add_string (df_full_annotation.loc[idx, 'ensembl'], str_input)
                
        # Ensembl Repeat
        ensembl_repeat = f'{ENSEMBL_RM_FTP_URL}/{organism.lower()}/{genbank_id}.repeatmodeler.fa'
        if check_url(ensembl_repeat, show_output=False):
            df_full_annotation.loc[idx, 'ensembl_repeat'] = add_string (df_full_annotation.loc[idx, 'ensembl_repeat'], 'repeat')
    
    # Searched result
    print(tabulate(df_full_annotation, headers='keys', tablefmt='grid'))
    print('')
    
    return df_full_annotation

# Download sequence data
def download_sequence(df, df_genome, dic_ensembl_meta, types, recursive):
    # Make download folder
    if not os.path.exists(DOWNLOAD_FOLDER_NAME):
        os.mkdir(DOWNLOAD_FOLDER_NAME)
    if not os.path.exists(OUT_FOLDER_NAME):
        os.mkdir(OUT_FOLDER_NAME)
        
    ls_types = types.split(',')
    
    print('# Download sequence data.')
    for idx in df.index:
        # Accession or name
        assembly_id = df_genome.loc[idx]['Assembly name']
        genbank_id = df_genome.loc[idx]['Genbank']
        refseq_id = df_genome.loc[idx]['RefSeq']
        organism = re.sub(r'\s*\([^)]*\)', '', df_genome.loc[idx]['Organism']).replace(' ', '_')
        
        check_refseq = df.loc[idx]['refseq']
        check_ensembl = df.loc[idx]['ensembl']
        check_ensembl_repeat = df.loc[idx]['ensembl_repeat']
        
        # Print assembly
        if refseq_id:
            print(f'[{genbank_id} / {refseq_id} / {assembly_id}]')
        else:
            print(f'[{genbank_id} / {assembly_id}]')

        # RefSeq
        if len(list(set(['refseq_rna', 'refseq_rna_genomic', 'refseq_cds_genomic', 'refseq_pseudo', 'refseq_pep', 'refseq_pep_cds']) & set(ls_types))) > 0:
            
            ls_search = check_refseq.replace(' ', '').split(',')
            refseq_dir = f'{NCBI_FTP_URL}/{refseq_id[0:3]}/{refseq_id[4:7]}/{refseq_id[7:10]}/{refseq_id[10:13]}/{refseq_id}_{assembly_id}'
            url_md5sum = f'{refseq_dir}/md5checksums.txt'
            refseq_rna = f'{refseq_dir}/{refseq_id}_{assembly_id}_rna.fna.gz'
            refseq_rna_gen = f'{refseq_dir}/{refseq_id}_{assembly_id}_rna_from_genomic.fna.gz'
            refseq_cds_gen = f'{refseq_dir}/{refseq_id}_{assembly_id}_cds_from_genomic.fna.gz'
            refseq_pseudo = f'{refseq_dir}/{refseq_id}_{assembly_id}_pseudo_without_product.fna.gz'
            refseq_protein = f'{refseq_dir}/{refseq_id}_{assembly_id}_protein.faa.gz'
            refseq_trans_cds = f'{refseq_dir}/{refseq_id}_{assembly_id}_translated_cds.faa.gz'
            
            if check_refseq:
                if 'refseq_rna' in ls_types:
                    if 'rna' in ls_search:
                        if check_url(refseq_rna):
                            out_name = f'{organism}-{assembly_id}-refseq.rna.fna.gz'
                            download_url(refseq_rna, out_name, url_md5sum=url_md5sum)
                        
                if 'refseq_rna_genomic' in ls_types:
                    if 'rna_genomic' in ls_search:
                        out_name = f'{organism}-{assembly_id}-refseq.rna_from_genomic.fna.gz'
                        download_url(refseq_rna_gen, out_name, url_md5sum=url_md5sum)
                        
                if 'refseq_cds_genomic' in ls_types:
                    if 'cds_genomic' in ls_search:
                        out_name = f'{organism}-{assembly_id}-refseq.cds_from_genomic.fna.gz'
                        download_url(refseq_cds_gen, out_name, url_md5sum=url_md5sum)
                        
                if 'refseq_pseudo' in ls_types:
                    if 'pseudo' in ls_search:
                        out_name = f'{organism}-{assembly_id}-refseq.pseudo_without_product.fna.gz'
                        download_url(refseq_pseudo, out_name, url_md5sum=url_md5sum)
                        
                if 'refseq_pep' in ls_types:
                    if 'pep' in ls_search:
                        out_name = f'{organism}-{assembly_id}-refseq.protein.faa.gz'
                        download_url(refseq_protein, out_name, url_md5sum=url_md5sum)
                
                if 'refseq_pep_cds' in ls_types:
                    if 'pep_cds' in ls_search:
                        out_name = f'{organism}-{assembly_id}-refseq.translated_cds.faa.gz'
                        download_url(refseq_trans_cds, out_name, url_md5sum=url_md5sum)
                
        # Ensembl
        if len(list(set(['ensembl_cdna', 'ensembl_cds', 'ensembl_pep']) & set(ls_types))) > 0:
            
            if genbank_id in dic_ensembl_meta:
                ensembl_acc = genbank_id
                organism_ens = dic_ensembl_meta[genbank_id].replace(' ', '_')
            elif refseq_id in dic_ensembl_meta:
                ensembl_acc = refseq_id
                organism_ens = dic_ensembl_meta[refseq_id].replace(' ', '_')
            
            if check_ensembl:
                ls_source = []
                for search_in_source in check_ensembl.replace(' ', '').split('/'):
                    source = search_in_source.strip().split(':')[0]
                    ls_source.append(source)
                    ls_search = search_in_source.split(':')[1].split(',')

                for source in ls_source:
                    ensembl_dir = f'/pub/rapid-release/species/{organism_ens}/{ensembl_acc}/{source}/geneset'
                    # Check the geneset folder name
                    geneset = list_ftp_directory(ENSEMBL_FTP_HOST, ensembl_dir)[0]
                    
                    ensembl_file_dir = f'{ENSEMBL_RAPID_FTP_URL}/species/{organism_ens}/{ensembl_acc}/{source}/geneset/{geneset}'

                    url_md5sum = f'{ensembl_file_dir}/md5sum.txt'
                    ensembl_cdna = f'{ensembl_file_dir}/{organism}-{ensembl_acc}-{geneset}-cdna.fa.gz'
                    ensembl_cds = f'{ensembl_file_dir}/{organism}-{ensembl_acc}-{geneset}-cds.fa.gz'
                    ensembl_pep = f'{ensembl_file_dir}/{organism}-{ensembl_acc}-{geneset}-pep.fa.gz'

                    
                    
                    if 'ensembl_cdna' in ls_types:
                        if 'cdna' in ls_search:
                            out_name = f'{organism}-{assembly_id}-ensembl_{source}.cdna.fna.gz'
                            download_url(ensembl_cdna, out_name, url_md5sum=url_md5sum)

                    if 'ensembl_cds' in ls_types:
                        if 'cds' in ls_search:
                            out_name = f'{organism}-{assembly_id}-ensembl_{source}.cds.fna.gz'
                            download_url(ensembl_cds, out_name, url_md5sum=url_md5sum)

                    if 'ensembl_pep' in ls_types:
                        if 'pep' in ls_search:
                            out_name = f'{organism}-{assembly_id}-ensembl_{source}.pep.faa.gz'
                            download_url(ensembl_pep, out_name, url_md5sum=url_md5sum)

        # Ensembl Repeatmodeler
        if check_ensembl_repeat:
            ensembl_repeat = f'{ENSEMBL_RM_FTP_URL}/{organism.lower()}/{genbank_id}.repeatmodeler.fa'
            
            if 'ensembl_repeat' in ls_types:
                out_name = f'{organism}-{assembly_id}-ensembl.repeatmodeler.fa'
                download_url(ensembl_repeat, out_name, recursive=recursive)
  
        print('')


## ---------------------------------------------
## gencube annotation
## ---------------------------------------------
# Check full accessibility
def check_access_full_annotation (df, dic_genark_meta):
    # Make dataframe for gencube annotation
    df_full_annotation = df[['Assembly name']].copy()
    # Make output dataframe
    ls_annotation = ['genark']
    
    for label in ls_annotation:
        df_full_annotation.loc[:,label] = ''
    
    print('# Check accessible data in databases.')
    
    for idx in df.index:
        # Accession or name
        assembly_id = df.loc[idx]['Assembly name']
        genbank_id = df.loc[idx]['Genbank']
        refseq_id = df.loc[idx]['RefSeq']
        check_genark = df.loc[idx]['GenArk']

        # Print assembly
        if refseq_id:
            print(f'[{genbank_id} / {refseq_id} / {assembly_id}]')
        else:
            print(f'[{genbank_id} / {assembly_id}]')

        # GenArk
        if check_genark:
            if refseq_id in dic_genark_meta:
                genark_id = refseq_id
            else:
                genark_id = genbank_id
                        
            genark_dir = f'{GENARK_URL}/{genark_id[0:3]}/{genark_id[4:7]}/{genark_id[7:10]}/{genark_id[10:13]}/{genark_id}' 
            
            ls_bb_files = list_http_files(genark_dir + '/bbi')
            gap = False
            rmsk = False
            cpg_island = False
            for file in ls_bb_files:
                if genark_id in file:
                    type_1 = file.split('.')[-2]
                    if type_1 == 'gc5Base':
                        df_full_annotation.loc[idx, 'genark'] = add_string (df_full_annotation.loc[idx, 'genark'], 'gc')
                    if type_1 == 'simpleRepeat':
                        df_full_annotation.loc[idx, 'genark'] = add_string (df_full_annotation.loc[idx, 'genark'], 'sr')
                    if type_1 == 'tandemDups':
                        df_full_annotation.loc[idx, 'genark'] = add_string (df_full_annotation.loc[idx, 'genark'], 'td')
                    if type_1 == 'windowMasker':
                        df_full_annotation.loc[idx, 'genark'] = add_string (df_full_annotation.loc[idx, 'genark'], 'wm')


                    if ('.allGaps.bb' in file or '.gap.bb' in file) and gap == False:
                        df_full_annotation.loc[idx, 'genark'] = add_string (df_full_annotation.loc[idx, 'genark'], 'gap')
                        gap = True
                    if '.rmsk.' in file and rmsk == False:
                        df_full_annotation.loc[idx, 'genark'] = add_string (df_full_annotation.loc[idx, 'genark'], 'rm')
                        rmsk = True
                    if '.cpgIslandExt' in file and cpg_island == False:
                        df_full_annotation.loc[idx, 'genark'] = add_string (df_full_annotation.loc[idx, 'genark'], 'cpgisland')
                        cpg_island = True
                    
            

    # Searched result
    print(tabulate(df_full_annotation, headers='keys', tablefmt='grid'))
    print('')
    
    return df_full_annotation

# Download annotation data
def download_annotation(df, df_genome, dic_genark_meta, types, recursive):
    # Make download folder
    if not os.path.exists(DOWNLOAD_FOLDER_NAME):
        os.mkdir(DOWNLOAD_FOLDER_NAME)
    if not os.path.exists(OUT_FOLDER_NAME):
        os.mkdir(OUT_FOLDER_NAME)
        
    ls_types = types.split(',')
    
    print('# Download annotation data.')
    dic_download = {}
    for idx in df.index:
        # Accession or name
        assembly_id = df_genome.loc[idx]['Assembly name']
        genbank_id = df_genome.loc[idx]['Genbank']
        refseq_id = df_genome.loc[idx]['RefSeq']
        
        #check_genbank = df.loc[idx]['genbank']
        check_refseq = df.loc[idx]['refseq']
        check_genark = df.loc[idx]['genark']
        organism = re.sub(r'\s*\([^)]*\)', '', df_genome.loc[idx]['Organism']).replace(' ', '_')
        
        # Print assembly
        if refseq_id:
            print(f'[{genbank_id} / {refseq_id} / {assembly_id}]')
        else:
            print(f'[{genbank_id} / {assembly_id}]')


        ls_download = []
        # RefSeq
        if len(list(set(['ontology', 'repeatmasker']) & set(ls_types))) > 0:
            
            ls_search = check_refseq.replace(' ', '').split(',')
            refseq_dir = f'{NCBI_FTP_URL}/{refseq_id[0:3]}/{refseq_id[4:7]}/{refseq_id[7:10]}/{refseq_id[10:13]}/{refseq_id}_{assembly_id}'
            url_md5sum = f'{refseq_dir}/md5checksums.txt'
            refseq_rm = f'{refseq_dir}/{refseq_id}_{assembly_id}_rm.out.gz'                    
            
            print(refseq_dir)
                    
            if check_refseq:
                if 'repeatmasker' in ls_types:
                    if 'repeatmasker' in ls_search:
                        if check_url(refseq_rm):
                            out_name = f'{organism}-{assembly_id}-refseq.repeatMasker.out.gz'
                            download_url(refseq_rm, out_name, url_md5sum=url_md5sum)
                            ls_download.append('refseq_rm')
                        
                if 'ontology' in ls_types:
                    if 'ontology' in ls_search:
                        if check_url(url_md5sum):
                            df_md5 = get_md5 (url_md5sum) # Read md5sum information
                            ls_filename = df_md5['Filename'].str.split('/').str[-1].tolist()
                            
                            for file in ls_filename:
                                if '_gene_ontology.gaf.gz' in file:
                                    out_name = f'{organism}-{assembly_id}-refseq.gene_ontology.gaf.gz'
                                    download_url(f'{refseq_dir}/{file}' , out_name, url_md5sum=url_md5sum)
                                    ls_download.append('refseq_ontolgy')
                                    break

        # GenArk
        if len(list(set(['gc', 'sr', 'td', 'wm', 'cb', 'gap', 'rm', 'cpgisland']) & set(ls_types))) > 0:
            if refseq_id in dic_genark_meta:
                genark_id = refseq_id
            else:
                genark_id = genbank_id
                
            ls_search = check_genark.replace(' ', '').split(',')
                        
            genark_dir = f'{GENARK_URL}/{genark_id[0:3]}/{genark_id[4:7]}/{genark_id[7:10]}/{genark_id[10:13]}/{genark_id}' 
            
            print(genark_dir)
            
            #genark_rmask = f'{genark_dir}/{genark_id}.repeatMasker.out.gz'
            #genark_rmodel = f'{genark_dir}/{genark_id}.repeatModeler.out.gz'
            genark_gc = f'{genark_dir}/bbi/{genark_id}_{assembly_id}.gc5Base.bw'
            genark_sr = f'{genark_dir}/bbi/{genark_id}_{assembly_id}.simpleRepeat.bb'
            genark_td = f'{genark_dir}/bbi/{genark_id}_{assembly_id}.tandemDups.bb'
            genark_wm = f'{genark_dir}/bbi/{genark_id}_{assembly_id}.windowMasker.bb'
            genark_chrsize = f'{genark_dir}/{genark_id}.chrom.sizes.txt'
                    
            if 'gc' in ls_types:
                if 'gc' in ls_search:
                    out_name = f'{organism}-{assembly_id}-genark.gc5Base.bw'
                    download_url(genark_gc, out_name, recursive=recursive)
                    ls_download.append('genark.gc5Base')
                    
            if 'sr' in ls_types:
                if 'sr' in ls_search:
                    out_name = f'{organism}-{assembly_id}-genark.simpleRepeat.bb'
                    download_url(genark_sr, out_name, recursive=recursive)
                    ls_download.append('genark.simpleRepeat')
            if 'td' in ls_types:
                if 'td' in ls_search:
                    out_name = f'{organism}-{assembly_id}-genark.tandemDups.bb'
                    download_url(genark_td, out_name, recursive=recursive)
                    ls_download.append('genark.tandemDups')
            if 'wm' in ls_types:
                if 'wm' in ls_search:
                    out_name = f'{organism}-{assembly_id}-genark.windowMasker.bb'
                    download_url(genark_wm, out_name, recursive=recursive)
                    ls_download.append('genark.windowMasker')                    

            ls_bb_files = list_http_files(genark_dir + '/bbi')
            ls_gaps = []
            ls_rmsk = []
            ls_cpg_island = []
            for file in ls_bb_files:
                if '.gap.bb' in file or '.allGaps.bb' in file:
                    ls_gaps.append(file)
                elif '.rmsk.' in file:
                    ls_rmsk.append(file)
                elif '.cpgIslandExt' in file:
                    ls_cpg_island.append(file)
            
            # gap
            if 'gap' in ls_types:
                if 'gap' in ls_search:
                    for in_name in ls_gaps:
                        if '.gap.bb' in in_name:
                            out_name = f'{organism}-{assembly_id}-genark.gap.bb'
                            download_url(f'{genark_dir}/bbi/{in_name}', out_name, recursive=recursive)
                            ls_download.append('genark.gap')
                        elif '.allGaps.bb' in in_name:
                            out_name = f'{organism}-{assembly_id}-genark.allGaps.bb'
                            download_url(f'{genark_dir}/bbi/{in_name}', out_name, recursive=recursive)
                            ls_download.append('genark.allGaps')

            # repeatMasker
            if 'rmsk' in ls_types:
                if 'rmsk' in ls_search:
                    for in_name in ls_rmsk:
                        if '.rmsk.bb' in in_name:
                            out_name = f'{organism}-{assembly_id}-genark.rmsk.bb'
                            download_url(f'{genark_dir}/bbi/{in_name}', out_name, recursive=recursive)
                            ls_download.append('genark.rmsk')
                        else:
                            suffix = in_name.split('.')[-2]
                            out_name = f'{organism}-{assembly_id}-genark.rmsk.{suffix}.bb'
                            download_url(f'{genark_dir}/bbi/{in_name}', out_name, recursive=recursive)
                            ls_download.append(f'genark.rmsk.{suffix}')
            # CpG island        
            if 'cpgisland' in ls_types:
                if 'cpgisland' in ls_search:
                    for in_name in ls_cpg_island:
                        suffix = in_name.split('.')[-2]
                        out_name = f'{organism}-{assembly_id}-genark.{suffix}.bb'
                        download_url(f'{genark_dir}/bbi/{in_name}', out_name, recursive=recursive)
                        ls_download.append(f'genark.{suffix}')
                        
            # Chrom size
            out_chrsize_name = f'{organism}-{assembly_id}-genark.chrom.sizes.txt' # !!!!!!!!!!!!
            download_url(genark_chrsize, out_chrsize_name, recursive=recursive)
                        
        dic_download[genbank_id] = ls_download
        print('')
        
    return dic_download
                        
# Change chromosome names of annotation file
def convert_chr_label_annotation (df, dic_download, style):
        
    print(f'# Change chromosome names: {style}-style')
    
    # Download UCSC genome browser applications
    # & Change the file system permissions of files
    print('  Download UCSC genome browser applications')
    path_bw2bdg = f'{DOWNLOAD_FOLDER_NAME}/bigWigToBedGraph'
    path_bdg2bw = f'{DOWNLOAD_FOLDER_NAME}/bedGraphToBigWig'
    path_bb2bed = f'{DOWNLOAD_FOLDER_NAME}/bigBedToBed'
    path_bed2bb = f'{DOWNLOAD_FOLDER_NAME}/bedToBigBed'
    
    if os.path.exists(path_bw2bdg):
        download_url(BIGWIG2BEDGRAPH)
        subprocess.run(['chmod', '+x', path_bw2bdg], check=True)
    if os.path.exists(path_bdg2bw):    
        download_url(BEDGRAPH2BIGWIG)
        subprocess.run(['chmod', '+x', path_bdg2bw], check=True)
    if os.path.exists(path_bb2bed):
        download_url(BIGBED2BED)
        subprocess.run(['chmod', '+x', path_bb2bed], check=True)
    if os.path.exists(path_bed2bb):
        download_url(BED2BIGBED)
        subprocess.run(['chmod', '+x', path_bed2bb], check=True)
    

    for idx in df.index:
        assembly_id = df.loc[idx]['Assembly name']
        organism = re.sub(r'\s*\([^)]*\)', '', df.loc[idx]['Organism']).replace(' ', '_')
        genbank_id = df.loc[idx]['Genbank']
        refseq_id = df.loc[idx]['RefSeq']
        
        # Print assembly
        if refseq_id:
            print(f'[{genbank_id} / {refseq_id} / {assembly_id}]')
        else:
            print(f'[{genbank_id} / {assembly_id}]')
            
        # Download assembly report
        print('  Download assembly report')
        report = False
        # RefSeq
        if refseq_id: 
            refseq_dir = f'{NCBI_FTP_URL}/{refseq_id[0:3]}/{refseq_id[4:7]}/{refseq_id[7:10]}/{refseq_id[10:13]}/{refseq_id}_{assembly_id}'
            refseq_md5sum = f'{refseq_dir}/md5checksums.txt'
            refseq_rp = f'{refseq_dir}/{refseq_id}_{assembly_id}_assembly_report.txt'
            out_rp_name = f'{organism}-{assembly_id}_assembly_report.txt'
            # Check and download assembly report.

            if check_url(refseq_rp):
                download_genome_url(refseq_rp, out_rp_name, refseq_md5sum)
                report = True

        # GenBank
        if not report:
            genbank_dir = f'{NCBI_FTP_URL}/{genbank_id[0:3]}/{genbank_id[4:7]}/{genbank_id[7:10]}/{genbank_id[10:13]}/{genbank_id}_{assembly_id}'
            genbank_md5sum = f'{genbank_dir}/md5checksums.txt'
            genbank_rp = f'{genbank_dir}/{genbank_id}_{assembly_id}_assembly_report.txt'
            out_rp_name = f'{organism}-{assembly_id}_assembly_report.txt'            

            if check_url(genbank_rp):
                # Check and download assembly report.
                download_genome_url(genbank_rp, out_rp_name, genbank_md5sum)

            else:
                print('  !! Assembly report is not found in RefSeq and GenBank.')
                print("     Chromosome names can't be changed. \n")
                break
                
        # Make integrative dataframe of chromosome label of databases
        df_report_edit = make_chr_dataframe (organism, assembly_id)

        # Check the number of UCSC 'na'
        ucsc_na_count = df_report_edit['ucsc'].str.contains('na', na=False).sum()
        # UCSC check
        if style == 'ucsc' and ucsc_na_count > 1:
            print(f'  {ucsc_na_count} chromosome(s) have not ucsc name.')
            break
        
        # Convert the DataFrame to dictionaries for faster lookup
        genbank_to_ensembl = df_report_edit.set_index('genbank')['ensembl'].to_dict()
        refseq_to_ensembl = df_report_edit.set_index('refseq')['ensembl'].to_dict()
        genbank_to_gencode = df_report_edit.set_index('genbank')['gencode'].to_dict()
        refseq_to_gencode = df_report_edit.set_index('refseq')['gencode'].to_dict()
        genbank_to_ucsc = df_report_edit.set_index('genbank')['ucsc'].to_dict()
        refseq_to_ucsc = df_report_edit.set_index('refseq')['ucsc'].to_dict()

        # Check the number of UCSC 'na'
        ucsc_na_count = df_report_edit['ucsc'].str.contains('na', na=False).sum()
        # UCSC check
        if style == 'ucsc' and ucsc_na_count > 1:
            print(f'  {ucsc_na_count} chromosome(s) have not ucsc name.')
            break

        # Check downloaded files
        ls_download = dic_download[genbank_id]
        print(f'  Downloaded genome: {ls_download}')
        
        dic_out_suffix = {'ensembl' : 'ens-id', 'gencode' : 'gc-id', 'ucsc' : 'ucsc-id'}
    
        for download in ls_download:
            print(f'- {download}')
            
            # Input and output name
            if download == 'genark.gc5Base':
                in_raw_file = f'{organism}-{assembly_id}-genark.gc5Base.bw'
                in_file = f'{organism}-{assembly_id}-genark.gc5Base.bedgraph'
                out_file = f'{organism}-{assembly_id}-genark.gc5Base.{dic_out_suffix[style]}.bedgraph'
                out_file_final = f'{organism}-{assembly_id}-genark.gc5Base.{dic_out_suffix[style]}.bw'
            else:
                in_raw_file = f'{organism}-{assembly_id}-{download}.bb'
                in_file = f'{organism}-{assembly_id}-{download}.bed'
                out_file = f'{organism}-{assembly_id}-{download}.{dic_out_suffix[style]}.bed'
                out_file_final = f'{organism}-{assembly_id}-{download}.{dic_out_suffix[style]}.bb'
            
           # File check in working directory
            ls_download_files = os.listdir(DOWNLOAD_FOLDER_NAME)
            ls_output_folder_files = os.listdir(OUT_FOLDER_NAME)

            if in_raw_file in ls_download_files and out_file_final not in ls_output_folder_files: 

                # Change file format (binary to readable format)
                if download == 'genark.gc5Base':
                    # bigWig to bedGraph
                    print('  Convert bigwig to bedgraph')
                    subprocess.run([path_bw2bdg, f'{DOWNLOAD_FOLDER_NAME}/{in_raw_file}', f'{DOWNLOAD_FOLDER_NAME}/{in_file}'], check=True)
                else:
                    # bigBed to bed
                    print('  Convert bigBed to bed')
                    subprocess.run([f'{path_bb2bed}', f'{DOWNLOAD_FOLDER_NAME}/{in_raw_file}', f'{DOWNLOAD_FOLDER_NAME}/{in_file}'], check=True)                    

                print('  Unify chromosome names')
                with open(f'{DOWNLOAD_FOLDER_NAME}/{in_file}', 'r') as f_in, open(f'{OUT_FOLDER_NAME}/{out_file}', 'w') as f_out:
                    for line in f_in:
                                   
                        if not line.startswith('#'):
                            ls_tmp = line.strip().split('\t')
                            chr_name = ls_tmp[0]
                            
                            # Change the chromosome name
                            if style == 'ensembl':
                                ls_tmp[0] = genbank_to_ensembl.get(chr_name, refseq_to_ensembl.get(chr_name, chr_name))
                            elif style == 'gencode':
                                ls_tmp[0] = genbank_to_gencode.get(chr_name, refseq_to_gencode.get(chr_name, chr_name))
                            elif style == 'ucsc':
                                ls_tmp[0] = genbank_to_ucsc.get(chr_name, refseq_to_ucsc.get(chr_name, chr_name))

                            line_edit = '\t'.join(ls_tmp) + '\n'
                            f_out.write(line_edit)

                        else:
                            f_out.write(line)
                            
            else:
                print('  The output file already exists.')
                print('  !! If the file appears to have any problems, please delete it and retry the process. \n')
                continue

            # Chrom size file
            in_genark_chrsizee = f'{organism}-{assembly_id}-genark.chrom.sizes.txt'
            out_genark_chrsize = f'{organism}-{assembly_id}-genark.chrom.sizes.{dic_out_suffix[style]}.tmp.txt'
            out_genark_chrsize_sorted = f'{organism}-{assembly_id}-genark.chrom.sizes.{dic_out_suffix[style]}.txt'
            
            if in_genark_chrsizee in ls_download_files and out_genark_chrsize not in ls_output_folder_files:

                with open(f'{DOWNLOAD_FOLDER_NAME}/{in_genark_chrsizee}', 'r') as f_in, open(f'{OUT_FOLDER_NAME}/{out_genark_chrsize}', 'w') as f_out:
                    for line in f_in:
                                   
                        if not line.startswith('#'):
                            ls_tmp = line.strip().split('\t')
                            chr_name = ls_tmp[0]
                            
                            # Change the chromosome name
                            if style == 'ensembl':
                                ls_tmp[0] = genbank_to_ensembl.get(chr_name, refseq_to_ensembl.get(chr_name, chr_name))
                            elif style == 'gencode':
                                ls_tmp[0] = genbank_to_gencode.get(chr_name, refseq_to_gencode.get(chr_name, chr_name))
                            elif style == 'ucsc':
                                ls_tmp[0] = genbank_to_ucsc.get(chr_name, refseq_to_ucsc.get(chr_name, chr_name))

                            line_edit = '\t'.join(ls_tmp) + '\n'
                            f_out.write(line_edit)

                        else:
                            f_out.write(line)
                            
                # Sort chrom size file
                with open(f'{OUT_FOLDER_NAME}/{out_genark_chrsize_sorted}', 'w') as f_out:
                    subprocess.run(['sort', '-k1,1', '-k2,2n', f'{OUT_FOLDER_NAME}/{out_genark_chrsize}'], stdout=f_out, check=True)
                # Remove temporary chrom size file
                delete_file(f'{OUT_FOLDER_NAME}/{out_genark_chrsize}')


            # Change file format (binary to readable format)
            if download == 'genark.gc5Base':
                print(f'  Convert bedgraph to bigwig: {out_file_final}')
                
                # bigWig to bedGraph
                subprocess.run([f'{path_bdg2bw}', f'{OUT_FOLDER_NAME}/{out_file}', f'{OUT_FOLDER_NAME}/{out_genark_chrsize_sorted}', f'{OUT_FOLDER_NAME}/{out_file_final}'], check=True)
                
                # Remove temporary files
                delete_file(f'{DOWNLOAD_FOLDER_NAME}/{in_file}')
                delete_file(f'{OUT_FOLDER_NAME}/{out_file}')
                
            else:
                print(f'  Convert bed to bigbed: {out_file_final}')
                
                # Sort bed file
                with open(f'{OUT_FOLDER_NAME}/{out_file}_sorted', 'w') as f_out:
                    subprocess.run(['sort', '-k1,1', '-k2,2n', f'{OUT_FOLDER_NAME}/{out_file}'], stdout=f_out, check=True)
                
                # bigBed to bed
                ls_download_factor = download.split('.')
                autodql_dir = script_dir + '/autosql'
                if download == 'genark.simpleRepeat':
                    subprocess.run([path_bed2bb, '-tab', '-type=bed4+12', f'-as={autodql_dir}/simpleRepeat.as', '-verbose=0', f'{OUT_FOLDER_NAME}/{out_file}_sorted', f'{OUT_FOLDER_NAME}/{out_genark_chrsize_sorted}', f'{OUT_FOLDER_NAME}/{out_file_final}'], check=True)
                elif download == 'genark.tandemDups':
                    subprocess.run([path_bed2bb, '-type=bed12+1', '-verbose=0', f'{OUT_FOLDER_NAME}/{out_file}_sorted', f'{OUT_FOLDER_NAME}/{out_genark_chrsize_sorted}', f'{OUT_FOLDER_NAME}/{out_file_final}'], check=True)
                elif download == 'genark.windowMasker':
                    subprocess.run([path_bed2bb, '-type=bed3', '-verbose=0', f'{OUT_FOLDER_NAME}/{out_file}_sorted', f'{OUT_FOLDER_NAME}/{out_genark_chrsize_sorted}', f'{OUT_FOLDER_NAME}/{out_file_final}'], check=True)
                elif download == 'genark.allGaps':
                    subprocess.run([path_bed2bb, '-type=bed3', '-verbose=0', f'{OUT_FOLDER_NAME}/{out_file}_sorted', f'{OUT_FOLDER_NAME}/{out_genark_chrsize_sorted}', f'{OUT_FOLDER_NAME}/{out_file_final}'], check=True)
                elif download == 'genark.gap':
                    subprocess.run([path_bed2bb, '-extraIndex=name', '-verbose=0', f'{OUT_FOLDER_NAME}/{out_file}_sorted', f'{OUT_FOLDER_NAME}/{out_genark_chrsize_sorted}', f'{OUT_FOLDER_NAME}/{out_file_final}'], check=True)
                
                elif download == 'genark.rmsk':
                    subprocess.run([path_bed2bb, '-tab', '-type=bed9+5', f'-as={autodql_dir}/bigRmskBed.as', '-verbose=0', f'{OUT_FOLDER_NAME}/{out_file}_sorted', f'{OUT_FOLDER_NAME}/{out_genark_chrsize_sorted}', f'{OUT_FOLDER_NAME}/{out_file_final}'], check=True)
                elif len(ls_download_factor) == 3 and ls_download_factor[1] == 'rmsk':
                    subprocess.run([path_bed2bb, '-tab', '-type=bed6+10', f'-as={autodql_dir}/rmskBed6+10.as', '-verbose=0', f'{OUT_FOLDER_NAME}/{out_file}_sorted', f'{OUT_FOLDER_NAME}/{out_genark_chrsize_sorted}', f'{OUT_FOLDER_NAME}/{out_file_final}'], check=True)
                elif 'cpgIslandExt' in download:
                    subprocess.run([path_bed2bb, '-tab', '-type=bed4+6', f'-as={autodql_dir}/cpgIslandExt.as', '-verbose=0', f'{OUT_FOLDER_NAME}/{out_file}_sorted', f'{OUT_FOLDER_NAME}/{out_genark_chrsize_sorted}', f'{OUT_FOLDER_NAME}/{out_file_final}'], check=True)
                
                # Remove temporary files
                delete_file(f'{DOWNLOAD_FOLDER_NAME}/{in_file}')
                delete_file(f'{OUT_FOLDER_NAME}/{out_file}')
                delete_file(f'{OUT_FOLDER_NAME}/{out_file}_sorted')
                
            print('')

                  
## ---------------------------------------------
## gencube crossgenome
## ---------------------------------------------
# Check full accessibility
def check_access_full_crossgenome (df, dic_ensembl_meta, df_zoonomia):
    # Make dataframe for gencube annotation
    df_full_annotation = df[['Assembly name']].copy()
    # Make output dataframe
    ls_geneset = ['ensembl', 'zoonomia']
    
    for label in ls_geneset:
        df_full_annotation.loc[:,label] = ''
    
    print('# Check accessible data in databases.')
    
    for idx in df.index:
        # Accession or name
        assembly_id = df.loc[idx]['Assembly name']
        genbank_id = df.loc[idx]['Genbank']
        refseq_id = df.loc[idx]['RefSeq']
        check_ensembl = df.loc[idx]['Ensembl']
        check_zoonomia = df.loc[idx]['Zoonomia']

        # Print assembly
        if refseq_id:
            print(f'[{genbank_id} / {refseq_id} / {assembly_id}]')
        else:
            print(f'[{genbank_id} / {assembly_id}]')
                
        # Ensembl
        if check_ensembl:
            
            if genbank_id in dic_ensembl_meta:
                ensembl_acc = genbank_id
                organism_ens = dic_ensembl_meta[genbank_id].replace(' ', '_')
            elif refseq_id in dic_ensembl_meta:
                ensembl_acc = refseq_id
                organism_ens = dic_ensembl_meta[refseq_id].replace(' ', '_')
            
            ensembl_dir = f'/pub/rapid-release/species/{organism_ens}/{ensembl_acc}'
            
            ls_source = list_ftp_directory(ENSEMBL_FTP_HOST, ensembl_dir)
            
            source = ''
            ls_excluded = ['rnaseq', 'brake', 'statistics']
            if ls_source:
                for tmp in ls_source:
                    if tmp not in ls_excluded:
                        
                        ensembl_homology_dir = f'{ENSEMBL_RAPID_FTP_URL}/species/{organism_ens}/{ensembl_acc}/{tmp}/homology'
                        if check_url(ensembl_homology_dir, show_output=False):
                            ensembl_dir = f'/pub/rapid-release/species/{organism_ens}/{ensembl_acc}/{tmp}/homology'
                            geneset = list_ftp_directory(ENSEMBL_FTP_HOST, ensembl_dir)[0]
  
                            homology_file = f'{ensembl_homology_dir}/{geneset}/{organism_ens}-{ensembl_acc}-{geneset}-homology.tsv.gz'
                            if check_url(homology_file, show_output=False):
                                if not source:
                                    source = tmp
                                else:
                                    source += f', {tmp}'
                            else:
                                continue
                        else:
                            continue
                        
            df_full_annotation.loc[idx, 'ensembl'] = add_string (df_full_annotation.loc[idx, 'ensembl'], source)
        
        # Zoonomia
        reference = ''
        if check_zoonomia:
            ls_reference = df_zoonomia[
                (df_zoonomia["NCBI accession / source"] == genbank_id) | 
                (df_zoonomia["NCBI accession / source"] == refseq_id)
                ]['reference'].tolist()
            for tmp in list(set(ls_reference)):
                if not reference:
                    reference = tmp
                else:
                    reference += f', {tmp}'
                    
            df_full_annotation.loc[idx, 'zoonomia'] = add_string (df_full_annotation.loc[idx, 'zoonomia'], reference)
            
    # Searched result
    print(tabulate(df_full_annotation, headers='keys', tablefmt='grid'))
    print('')
    
    return df_full_annotation

# Download crossgenome data
def download_crossgenome (df, df_genome, dic_ensembl_meta, df_zoonomia, types, recursive):
    ls_types = types.split(',')
    
    print('# Download geneset data.')
    dic_download = {}
    for idx in df.index:
        # Accession or name
        assembly_id = df_genome.loc[idx]['Assembly name']
        genbank_id = df_genome.loc[idx]['Genbank']
        refseq_id = df_genome.loc[idx]['RefSeq']
        organism = re.sub(r'\s*\([^)]*\)', '', df_genome.loc[idx]['Organism']).replace(' ', '_')
        
        check_ensembl = df.loc[idx]['ensembl']
        check_zoonomia = df.loc[idx]['zoonomia']
        
        # Print assembly
        if refseq_id:
            print(f'[{genbank_id} / {refseq_id} / {assembly_id}]')
        else:
            print(f'[{genbank_id} / {assembly_id}]')
        
        ls_download = []
                
        # Ensembl
        if 'ensembl_homology' in ls_types:
            
            if genbank_id in dic_ensembl_meta:
                ensembl_acc = genbank_id
                organism_ens = dic_ensembl_meta[genbank_id].replace(' ', '_')
            elif refseq_id in dic_ensembl_meta:
                ensembl_acc = refseq_id
                organism_ens = dic_ensembl_meta[refseq_id].replace(' ', '_')
            
            if check_ensembl:
                ls_source = check_ensembl.replace(' ', '').split(',')
                
                for source in ls_source:
                    ensembl_dir = f'/pub/rapid-release/species/{organism_ens}/{ensembl_acc}/{source}/homology'
                    if ensembl_dir:
                        # Check the geneset folder name
                        geneset = list_ftp_directory(ENSEMBL_FTP_HOST, ensembl_dir)[0]
                        
                        ensembl_file_dir = f'{ENSEMBL_RAPID_FTP_URL}/species/{organism_ens}/{ensembl_acc}/{source}/homology/{geneset}'                    
                        ensembl_gtf = f'{ensembl_file_dir}/{organism_ens}-{ensembl_acc}-{geneset}-homology.tsv.gz'
                        
                        if 'ensembl_homology' in ls_types:
                            if check_url(ensembl_gtf):
                                out_name = f'{organism}-{assembly_id}-ensembl_{source}_homology.tsv.gz'
                                download_url(ensembl_gtf, out_name, recursive=recursive)

        # Zoonomia
        if len(list(set(['toga_homology', 'toga_align_codon', 'toga_align_protein', 'toga_inact_mut']) & set(ls_types))) > 0:
            
            if check_zoonomia:
                ls_reference = check_zoonomia.replace(' ', '').split(',')
                
                for reference in ls_reference:
                    
                    zoonomia_dir = f'{ZOONOMIA_URL}/{DIC_ZOONOMIA[reference]}'
                    
                    df_tmp = df_zoonomia[
                        ((df_zoonomia['NCBI accession / source'] == genbank_id) | 
                        (df_zoonomia['NCBI accession / source'] == refseq_id)) &
                        (df_zoonomia['reference'] == reference)
                    ]
                    
                    for i in range(len(df_tmp.index)):
                        taxo = df_tmp['Taxonomic Lineage'].values[i]
                        species = df_tmp['Species'].values[i].replace(' ', '_')
                        name = df_tmp['Common name'].values[i].replace(' ', '_')
                        assembly = df_tmp['Assembly name'].values[i]

                        if reference in ['human', 'mouse', 'chicken']:
                            ls_folders = list_http_folders(zoonomia_dir)
                        
                            for folder in ls_folders:
                                if folder in taxo:
                                    category = folder
                                    break
                            
                            zoonomia_file_dir = f'{zoonomia_dir}/{category}/{species}__{name}__{assembly}'
                        else:
                            zoonomia_file_dir = f'{zoonomia_dir}/{species}__{name}__{assembly}'
                        
                        zoonomia_orth = f'{zoonomia_file_dir}/orthologsClassification.tsv.gz'
                        zoonomia_align_codon = f'{zoonomia_file_dir}/codonAlignments.fa.gz'
                        zoonomia_align_codoncesar = f'{zoonomia_file_dir}/codonAlignments.allCESARexons.fa.gz'
                        zoonomia_align_protein = f'{zoonomia_file_dir}/proteinAlignment.fa.gz'
                        zoonomia_align_proteincesar = f'{zoonomia_file_dir}/proteinAlignments.allCESARexons.fa.gz'
                        zoonomia_inact_mut = f'{zoonomia_file_dir}/loss_summ_data.tsv.gz'
                        
                        if 'toga_homology' in ls_types:
                            if check_url(zoonomia_orth, verify=False):
                                out_gtf_name = f'{organism}-{assembly_id}-toga_{reference}_homology.tsv.gz'
                                download_url(zoonomia_orth, out_gtf_name, verify=False, recursive=recursive)
                        if 'toga_align_codon' in ls_types:
                            if check_url(zoonomia_align_codon, verify=False):
                                out_gtf_name = f'{organism}-{assembly_id}-toga_{reference}_align_codon.fa.gz'
                                download_url(zoonomia_align_codon, out_gtf_name, verify=False, recursive=recursive)
                            if check_url(zoonomia_align_codoncesar, verify=False):
                                out_gtf_name = f'{organism}-{assembly_id}-toga_{reference}_align_codon_cesar.fa.gz'
                                download_url(zoonomia_align_codoncesar, out_gtf_name, verify=False, recursive=recursive)
                        if 'toga_align_protein' in ls_types:
                            if check_url(zoonomia_align_protein, verify=False):
                                out_gtf_name = f'{organism}-{assembly_id}-toga_{reference}_align_protein.fa.gz'
                                download_url(zoonomia_align_protein, out_gtf_name, verify=False, recursive=recursive)
                            if check_url(zoonomia_align_proteincesar, verify=False):
                                out_gtf_name = f'{organism}-{assembly_id}-toga_{reference}_align_protein_cesar.fa.gz'
                                download_url(zoonomia_align_proteincesar, out_gtf_name, verify=False, recursive=recursive)
                        if 'toga_inact_mut' in ls_types:
                            if check_url(zoonomia_inact_mut, verify=False):
                                out_gtf_name = f'{organism}-{assembly_id}-toga_{reference}_loss_summ_data.tsv.gz'
                                download_url(zoonomia_inact_mut, out_gtf_name, verify=False, recursive=recursive)
                                
        print('')


## -----------------------------------------------------------
## gencube genome, geneset, sequence, annotation, crossgenome
## -----------------------------------------------------------
# Save variables as pickle format
def save_pickle (in_variable, out_file_name):
    out_file = f'tests/data/{out_file_name}.pkl'
    # Save the file using two different methods depending on the data type
    if isinstance(in_variable, pd.DataFrame):
        in_variable.to_pickle(out_file)
    else:
        with open(out_file, 'wb') as file:
            pickle.dump(in_variable, file)

# Load variables from pickle format file
def load_pickle (in_file_name, type=False):
    # Save the file using two different methods depending on the data type
    in_file = f'tests/data/{in_file_name}.pkl'
    if type == 'dataframe':
        return pd.read_pickle(in_file)
    else:
        with open(in_file, 'rb') as file:
            return pickle.load(file)

# Check starting time
def check_now ():
    now = datetime.now()
    formatted_now = now.strftime("%y%m%d_%H%M%S")
    return formatted_now

# Merge strings with comma
def add_string (df, string):
    if df:
        df += f', {string}'
    else:
        df = string
        
    return df

# Check url
def check_url(url, status=False, verify=True, show_output=True):
    try:
        # Use the HEAD request to fetch only the headers of the resource and allow redirects.
        response = requests.head(url, allow_redirects=True, verify=verify)  
        # Check for successful response and file accessibility.
        if status:
            return  response.status_code
        
        if response.status_code == 200:
            return True
        # Check if the response is a redirect, and the file might still be accessible.
        elif response.status_code in (301, 302, 307):
            if show_output:
                print(f"  !! Redirected to {response.headers['Location']}")
            return True
        elif response.status_code == 403:
            if show_output:
                print("  !! Access denied. File cannot be downloaded.")
            return False
        elif response.status_code == 404:
            if show_output:
                print("  !! File not found.")
            return False
        elif response.status_code == 429:
            if show_output:
                print("  !! Too many requests. Please try again later.")
            return False
        elif response.status_code >= 500:
            if show_output:
                print("  !! Server error. Please try again later.")
            return False
        else:
            # Handle any other unexpected status codes.
            if show_output:
                print(f"  !! Unexpected status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request.
        if show_output:
            print(f"  !! Error checking URL: {e}")
        return False

# Fetch information of folders located in ftp server
def list_ftp_directory(host, directory):
    ftp = ftplib.FTP(host)
    ftp.login()  # Login (anonymous access)
    ftp.cwd(directory)  # Change to the specified directory
    files = ftp.nlst()  # Retrieve directory listing
    ftp.quit()  # Close FTP connection
    return files

# Fetch information of folders located in ftp server
def list_http_folders(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Check for request errors

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links that are directories
        folders = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith('/') and not href.startswith('/'):
                folders.append(href.replace('/', ''))

        return folders
    
    except requests.exceptions.RequestException as e:
        print(f"Error accessing URL: {e}")
        return []
    
# Fetch information of files located in an HTTP server directory
def list_http_files(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Check for request errors

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links that are files
        files = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and not href.endswith('/') and not href.startswith('/'):
                files.append(href)

        return files
    
    except requests.exceptions.RequestException as e:
        print(f"Error accessing URL: {e}")
        return []

# Fetch infomration using url
def download_csv(url, verify=True):
    # Download the file with SSL verification disabled
    response = requests.get(url, verify=verify)
    response.raise_for_status()  # Check for request errors
    return StringIO(response.text)

# Save metadata
def save_metadata (df, function, keywords, level, now):
    # Remove some columns not required in metadata
    df_meta = df.drop(columns=['NCBI'])
    
    # Save the metadata
    if len(keywords) != 1:
        keyword = f'{len(keywords)}keywords'
    else:
        keyword = keywords[0]
    
    out_name = f"Meta_{function}_{keyword.replace(' ', '-')}_{level.replace(',', '-')}_{now}.txt"
    df_meta.to_csv(out_name, sep='\t', index=False)

# Calculate and return the MD5 hash of a file. 
def calculate_md5(filename):
    return hashlib.md5(open(filename,'rb').read()).hexdigest()

# Download genome file and check md5sum
def download_genome_url(url, local_filename=None, url_md5sum=None, verify=True, recursive=None):
    # File name
    raw_filename = url.split('/')[-1]
    if local_filename is None:
        local_filename = raw_filename
    path_local_file = os.path.join(DOWNLOAD_FOLDER_NAME, local_filename)

    if url_md5sum:
        response = requests.get(url_md5sum, verify=verify)
        # This will raise an error for bad responses
        response.raise_for_status()
        # Split the content by new lines and parse it
        data = response.text.split('\n')
        data = [line.split() for line in data if line]  # Split each line into parts and remove empty lines
        # Create a DataFrame
        df = pd.DataFrame(data, columns=['MD5', 'Filename'])

        # Get md5sum of file
        for idx in df.index:
            md5sum_filename = df.loc[idx, 'Filename'].split('/')[-1]
            if raw_filename == md5sum_filename:
                md5sum_original = df.loc[idx, 'MD5']

    count = 0
    recursive_download = False
    while True:
        if url_md5sum:
            if os.path.exists(path_local_file):
                # Get md5sum from download file
                md5sum_download = calculate_md5(path_local_file)
                # If md5sums are same between original and download file
                if md5sum_download == md5sum_original:
                    if count == 0:
                        if '_assembly_report.txt' in path_local_file:
                            print('  Assembly Report was already downloaded.')
                        elif 'fa.gz' in path_local_file:
                            print(f'  {local_filename} was already downloaded.')
                    break
                # If md5sums are different between original and download file
                else:
                    print(
                        '  md5sum value is not same with original file. \n'
                        f'  {md5sum_original}: original file \n'
                        f'  {md5sum_download}: download file \n'
                    )
                    if count < 1:
                        print('  Re-try downloading the file')
                        os.remove(path_local_file)
                    else:
                        print('  Try download file again.')
                        os.remove(path_local_file)
                        break
        else:
            # If there is no url_md5sum (can't be checked)
            if 'fa.gz' in local_filename and os.path.exists(path_local_file):
                if recursive == False:
                    if count == 0:
                        print(f'  {local_filename} was already downloaded.')
                    break
                else:
                    if recursive_download:
                        break
                    else:
                        os.remove(path_local_file)   

        # Check the size of the local file if it already exists.
        existing_size = os.path.getsize(path_local_file) if os.path.exists(path_local_file) else 0

        # Add the Range header to the HTTP request to download the part of the file that is not yet downloaded.
        headers = {"Range": f"bytes={existing_size}-"}
        response = requests.get(url, headers=headers, stream=True, verify=verify)
        total_size = int(response.headers.get('content-length', 0)) + existing_size

        # Open the file in append mode and proceed with the download.
        with open(path_local_file, 'ab') as f, tqdm(
            desc='  ' + local_filename,
            initial=existing_size,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                bar.update(len(chunk))
                
        count += 1
        recursive_download = True 
        
    if url_md5sum == False:
        print("  !! md5sum can't be checked - If the file appears to have any problems, please delete it and retry the process or use --recursive option.")

# Download file and check md5sum
def download_url(url, local_filename=None, url_md5sum=None, verify=True, recursive=None):
    # File name
    raw_filename = url.split('/')[-1]
    if local_filename is None:
        local_filename = raw_filename
    path_local_file = os.path.join(DOWNLOAD_FOLDER_NAME, local_filename)

    if url_md5sum:
        response = requests.get(url_md5sum, verify=verify)
        # This will raise an error for bad responses
        response.raise_for_status()
        # Split the content by new lines and parse it
        data = response.text.split('\n')
        data = [line.split() for line in data if line]  # Split each line into parts and remove empty lines
        # Create a DataFrame
        df = pd.DataFrame(data, columns=['MD5', 'Filename'])

        # Get md5sum of file
        for idx in df.index:
            md5sum_filename = df.loc[idx, 'Filename'].split('/')[-1]
            if raw_filename == md5sum_filename:
                md5sum_original = df.loc[idx, 'MD5']

    count = 0
    recursive_download = False
    while True:
        if url_md5sum:
            if os.path.exists(path_local_file):
                # Get md5sum from download file
                md5sum_download = calculate_md5(path_local_file)
                # If md5sums are same between original and download file
                if md5sum_download == md5sum_original:
                    if count == 0:
                        print(f'  {local_filename} was already downloaded.')
                    break
                # If md5sums are different between original and download file
                else:
                    print(
                        '  md5sum value is not same with original file. \n'
                        f'  {md5sum_original}: original file \n'
                        f'  {md5sum_download}: download file \n'
                    )
                    if count < 1:
                        print('  Re-try downloading the file')
                        os.remove(path_local_file)
                    else:
                        print('  Try download file again.')
                        os.remove(path_local_file)
                        break
        else:
            # If there is no url_md5sum (can't be checked)
            if os.path.exists(path_local_file):
                if recursive == False:                
                    if count == 0:
                        print(f'  {local_filename} was already downloaded.')
                    break
                else:
                    if recursive_download:
                        break
                    else:
                        os.remove(path_local_file)

        # Check the size of the local file if it already exists.
        existing_size = os.path.getsize(path_local_file) if os.path.exists(path_local_file) else 0

        # Add the Range header to the HTTP request to download the part of the file that is not yet downloaded.
        headers = {"Range": f"bytes={existing_size}-"}
        response = requests.get(url, headers=headers, stream=True, verify=verify)
        total_size = int(response.headers.get('content-length', 0)) + existing_size

        # Open the file in append mode and proceed with the download.
        with open(path_local_file, 'ab') as f, tqdm(
            desc='  ' + local_filename,
            initial=existing_size,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                bar.update(len(chunk))

        count += 1
        recursive_download = True 
    
    if url_md5sum == False:
        print("  !! md5sum can't be checked - If the file appears to have any problems, please delete it and retry the process or use --recursive option.")

# Fetch md5sum information
def get_md5 (url_md5sum, verify=True):
    response = requests.get(url_md5sum, verify=verify)
    # This will raise an error for bad responses
    response.raise_for_status() 
    # Split the content by new lines and parse it
    data = response.text.split('\n')
    data = [line.split() for line in data if line]  # Split each line into parts and remove empty lines
    # Create a DataFrame
    df = pd.DataFrame(data, columns=['MD5', 'Filename'])
    
    return df

# Remove file
def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")

# Make integrative dataframe of chromosome label of databases
def make_chr_dataframe (organism, assembly_id):
    # read report file
    ls_report = []
    in_report_name = f'{DOWNLOAD_FOLDER_NAME}/{organism}-{assembly_id}_assembly_report.txt'
    out_report_name = f'{OUT_FOLDER_NAME}/{organism}-{assembly_id}_chr_name.txt'
    
    if os.path.exists(in_report_name):
        with open (in_report_name, 'r') as file:
            for line in file:
                tmp = line.split()
                if len(tmp) > 0 and line[0] != '#':
                    if line[0] == '<':
                        break
                    ls_report.append(line.strip().split('\t'))
                    
    else:
        print(f'  {organism}-{assembly_id}_assembly_report.txt file is not found \n')
        return ''
    
    df_report_raw = pd.DataFrame(ls_report, columns=LS_ASSEMBLY_REPORT_LABEL)
    df_report = df_report_raw[['GenBank-Accn', 'RefSeq-Accn', 'Assigned-Molecule',  'UCSC-style-name']]
    df_report_edit = df_report.copy()

    # Create ensembl-style and gencode-style label
    # - Ensembl
    df_report_edit.loc[:, 'Ensembl'] = df_report.apply(
        lambda row: row['Assigned-Molecule'] if row['GenBank-Accn'].startswith('CM') or row['RefSeq-Accn'].startswith('NC') else row['GenBank-Accn'], 
        axis=1)
    # - Gencode
    df_report_edit['Gencode'] = df_report.apply(
        lambda row: 'chr' + row['Assigned-Molecule'] if row['GenBank-Accn'].startswith('CM') or row['RefSeq-Accn'].startswith('NC') else row['GenBank-Accn'], 
        axis=1)
    df_report_edit['Gencode'] = df_report_edit['Gencode'].replace('chrMT', 'chrM')
    
    df_report_edit.drop(['Assigned-Molecule'], axis=1, inplace=True)
    # Change column names
    df_report_edit.columns = ['genbank', 'refseq', 'ucsc', 'ensembl', 'gencode']
    
    # Merge rows including chrM information
    if len(df_report_edit[df_report_edit['ensembl'] == 'MT'].index) == 2:
        # Find the first valid 'genbank' value that is not 'na' among rows where 'ensembl' is 'MT'
        genbank_mt = df_report_edit.loc[(df_report_edit['ensembl'] == 'MT') & (df_report_edit['genbank'] != 'na'), 'genbank'].iloc[0]
        # Replace all 'na' values in 'genbank' for rows where 'ensembl' is 'MT'
        df_report_edit.loc[(df_report_edit['ensembl'] == 'MT') & (df_report_edit['genbank'] == 'na'), 'genbank'] = genbank_mt
        # After replacement, remove the rows that originally had a 'genbank' value (that was not 'na')
        df_report_edit = df_report_edit.drop(df_report_edit[(df_report_edit['ensembl'] == 'MT') & (df_report_edit['refseq'] == 'na')].index)
    # UCSC chrM name
    df_report_edit.loc[df_report_edit['ensembl'] == 'MT', 'ucsc'] = 'chrM'
        
    # Save dataframe
    df_report_edit_out = df_report_edit.copy()
    df_report_edit_out.columns = ['GenBank', 'RefSeq', 'UCSC', 'Ensembl', 'Gencode']
    df_report_edit_out.to_csv(out_report_name, sep='\t', index=False)
    
    # Remove report file
    #delete_file(in_report_name)

    return df_report_edit


## ---------------------------------------------
## gencube seqmeta
## ---------------------------------------------
# Make query for searching
def make_query(
    organism, strategy, source, platform, selection, 
    filter, layout, access, bioproject, biosample, accession, 
    title, aligned, author, publication, modification, 
    properties, readlength, mbases, textword, keywords, exclude):
  
    print('# Make query for searching')
    query = ''
    dic_query_pars = {}
    dic_query_kwds = {}
    dic_query_excs = {}
    # Organism
    if organism:
        query = add_query (organism, 'Organism', query, dic_query_pars)
    # Strategy
    if strategy:
        query = add_query (strategy, 'Strategy', query, dic_query_pars)
    # Source
    if source:
        query = add_query (source, 'Source', query, dic_query_pars)
    # Platform
    if platform:
        query = add_query (platform, 'Platform', query, dic_query_pars)
    # Selection
    if selection:
        query = add_query (selection, 'Selection', query, dic_query_pars)
    # Filter
    if filter:
        query = add_query (filter, 'Filter', query, dic_query_pars)
    # Layout
    if layout:
        query = add_query (layout, 'Layout', query, dic_query_pars)
    # Access
    if access:
        query = add_query (access, 'Access', query, dic_query_pars)
    # BioProject
    if bioproject:
        query = add_query (bioproject, 'BioProject', query, dic_query_pars)
    # BioSample
    if biosample:
        query = add_query (biosample, 'BioSample', query, dic_query_pars)
    # Accession
    if accession:
        query = add_query (accession, 'Accession', query, dic_query_pars)
    # Title
    if title:
        query = add_query (title, 'Title', query, dic_query_pars)
    # Aligned
    if aligned:
        query = add_query (aligned, 'Aligned', query, dic_query_pars)
    # Author
    if author:
        query = add_query (author, 'Author', query, dic_query_pars)
        
    # Publication Date
    if publication:
        query = add_query_with_date (publication, 'Publication Date', query, dic_query_pars)
    # Modification Date
    if modification:
        query = add_query_with_date (modification, 'Modification Date', query, dic_query_pars)
        
    # Properties
    if properties:
        query = add_query (properties, 'Properties', query, dic_query_pars)
    # ReadLength
    if readlength:
        query = add_query (readlength, 'ReadLength', query, dic_query_pars)
    # Mbases
    if mbases:
        query = add_query (mbases, 'Mbases', query, dic_query_pars)
    # Text Word
    if textword:
        query = add_query (textword, 'Text Word', query, dic_query_pars)
    
    # For search in steps
    if len(dic_query_pars.keys()) > 1:
        dic_query_pars['Intersection'] = query
    

    # Keywords
    tmp_show = ''
    if keywords:
        query_tmp_merge = ''
        count = 0
        print(f'  Keywords: {keywords}')
        for i in range(len(keywords)):
            
            # OR operator
            ls_keywords = keywords[i].split(',')
            
            count += len(ls_keywords)
            for j in range(len(ls_keywords)):
                
                kwd_replace = ls_keywords[j].replace('_', ' ')
                
                if j == 0:
                    query_tmp = f'"{kwd_replace}"'
                else:
                    query_tmp += f' OR "{kwd_replace}"'
                
                # For search in steps
                query_step_tmp = f'{dic_query_pars["Intersection"]} AND {kwd_replace}'
                dic_query_kwds[ls_keywords[j]] = query_step_tmp
            
            # For search in steps
            if len(ls_keywords) > 1:
                query_step_tmp = f'{dic_query_pars["Intersection"]} AND ({query_tmp})'
                tmp_key = keywords[i].replace('_', ' ').replace(',', '|')
                dic_query_kwds[tmp_key] = query_step_tmp
                if not tmp_show:
                    tmp_show = tmp_key
                else:
                    tmp_show += f' & {tmp_key}'
            if len(keywords) > 1:
                dic_query_kwds[f'space{i}'] = ' '
            
            
            # AND operator        
            if not query_tmp_merge:
                query_tmp_merge = f'({query_tmp})'
            else:
                query_tmp_merge += f' AND ({query_tmp})'
            
        query = f'({query} AND ({query_tmp_merge}))'
        
        # For search in steps
        if len(keywords) > 1:
            dic_query_kwds[f'Intersection ({tmp_show})'] = query


    # Excluded keywords (NOT operator)
    if exclude:
        ls_exclude = exclude.split(',')
        print(f'  Excluded: {ls_exclude}')
        
        for i in range(len(ls_exclude)):
            exclude_replace = ls_exclude[i].replace('_', ' ')
            query_tmp = f'"{exclude_replace}"'
            query = f'{query} NOT {query_tmp}'
            
            if i == 0:
                query_tmp_or = f'"{exclude_replace}"'
            else:
                query_tmp_or += f' OR "{exclude_replace}"'
            
            # For search in steps
            query_step_tmp = f'{dic_query_pars["Intersection"]} AND {query_tmp}'
            dic_query_excs[exclude_replace] = query_step_tmp
        # For search in steps
        query_step_tmp = f'{dic_query_pars["Intersection"]} AND ({query_tmp_or})'
        dic_query_excs[exclude.replace('_', ' ').replace(',', '|')] = query_step_tmp
            
    print('')
    
    return query, dic_query_pars, dic_query_kwds, dic_query_excs

# Make query for searching - Add query
def add_query (input, option, query, dic):
    dic[option] = ' '
    list = input.split(',')
    print(f'  {option}: {list}')
    
    for i in range(len(list)):
        tmp = list[i].replace('_', ' ')
        if i == 0:
            query_tmp = f'"{tmp}"[{option}]'
        else:
            query_tmp += f' OR "{tmp}"[{option}]'
    
        dic[tmp] = f'"{tmp}"[{option}]'
    if not query:
        return f'({query_tmp})'
    else:
        return f'({query} AND ({query_tmp}))'

# Make query for searching - Add query with date
def add_query_with_date (input, option, query, dic):
    dic[option] = ' '
    list = input.split(':')
    print(f'  {option}: {list}')
    
    for i in range(len(list)):
        tmp = list[i].replace('.', '/')
        if i == 0:
            if len(list) == 2:
                query_tmp = f'"{tmp}"[{option}]'
            elif len(list) == 1:
                query_tmp = f'"{tmp}"[{option}] : "3000"[{option}]'
        else:
            query_tmp += f' : "{tmp}"[{option}]'
        
    dic[option] = query_tmp
    return f'({query} AND ({query_tmp}))'
    

# ESearch
def search_sra(query):
    handle = Entrez.esearch(db="sra",  # Database to search
                            term=query,  # Search term
                            retmax=10000  # Number of results to return
                            )
    record = Entrez.read(handle)
    
    return record

# EFetch
def fetch_meta(ls_id):
    # check input list
    if len(ls_id) == 0:
        print("No searched id.")
    else:
        df = pd.DataFrame()
        
        print('# Fetch metadata.')
        start_time = time.time() # record start time
        
        # Using tqdm to create a progress bar
        for id in tqdm(ls_id, desc="  Fetching metadata", unit="id"):
            handle = Entrez.efetch(db="sra",
                                   id=id,
                                   rettype="gb",
                                   retmode="text"
                                  )
            # convert xml to dataframe format
            xml_data = handle.read()
            dict_data = xmltodict.parse(xml_data)
            json_data = json.dumps(dict_data)
            df_tmp = pd.json_normalize(json.loads(json_data))
            # remove complex words in column names
            df_tmp.columns = df_tmp.columns.str.replace('EXPERIMENT_PACKAGE_SET.EXPERIMENT_PACKAGE.', '', regex=True)
            df_tmp.index = [id]
            # merge dataframes
            df = pd.concat([df, df_tmp], axis=0)

        print(f'  Done!')
    
        end_time = time.time() # record end time
        elapsed_time = end_time - start_time
        print(f'  Total fetching time: {int(elapsed_time)} seconds\n')
        
    return df

# Make output dataframe format
def convert_format(df, query):
    if df.shape[0] != 0:  
        # Lists for extraction of needed information
        sr_study = pd.Series(LS_SRA_META_STUDY_KEY)
        sr_sample = pd.Series(LS_SRA_META_SAMPLE_KEY)
        sr_study_label = pd.Series(LS_SRA_META_STUDY_LABEL)
        sr_sample_label = pd.Series(LS_SRA_META_SAMPLE_LABEL)
        
        ## Table for sample ------------------------
        # check intersected values
        sr_study_ovlp = sr_study[sr_study.isin(df.columns)]
        sr_sample_ovlp = sr_sample[sr_sample.isin(df.columns)]
        sr_study_label_ovlp = sr_study_label[sr_study_ovlp.index]
        sr_sample_label_ovlp = sr_sample_label[sr_sample_ovlp.index]
        
        # Extract sample info for re-formatted sample table
        df_sample = df[pd.concat([sr_study_ovlp, sr_sample_ovlp])]
        df_sample.columns = pd.concat([sr_study_label_ovlp, sr_sample_label_ovlp])
        df_sample.reset_index(drop=True, inplace=True)
        df_sample_edit = df_sample.copy() # copy
        
        # Remove unnecessary info
        if 'GSE' in df_sample.columns:
            df_sample_edit['GSE'] = df_sample['GSE'].apply(lambda x: x if isinstance(x, str) and x.startswith('GSE') else '') # remove except of GSE ids
        if 'GSM' in df_sample.columns:
            df_sample_edit['GSE'] = df_sample['GSM'].apply(lambda x: x if isinstance(x, str) and x.startswith('GSM') else '') # remove except of GSM ids
        # Leave only YYYY-MM-DD & remove time
        if 'Published' in df_sample.columns:
            df_sample_edit['Published'] = df_sample['Published'].apply(lambda x: x if pd.isna(x) else x.split(' ')[0])
        
        # Merge two columns
        if 'BioProject' in df_sample.columns and 'BioProject_alt' in df_sample.columns:
            df_sample_edit['BioProject'] = np.where(pd.notna(df_sample['BioProject']), df_sample['BioProject'], df_sample['BioProject_alt'])
            df_sample_edit.drop('BioProject_alt', axis=1, inplace=True)
        elif 'BioProject_alt' in df_sample.columns:
            df_sample_edit.rename(columns={'BioProject_alt': 'BioProject'}, inplace=True)
        
        sr_study_label = sr_study_label[sr_study_label != 'BioProject_alt']
        sr_study_label_ovlp = sr_study_label_ovlp[sr_study_label_ovlp != 'BioProject_alt']

        ## Table for study ------------------------
        df_study = df_sample_edit[sr_study_label_ovlp]
        df_study_dropdup = df_study.drop_duplicates(subset='SRP', keep='first') # remove duplicates
        df_study_dropdup.reset_index(drop=True, inplace=True) # remove index ids
        # Count the number of samples
        df_study_edit = df_study_dropdup.copy()
        df_study_edit['# Samples'] = [df_sample_edit['SRP'].tolist().count(val) for val in df_study_dropdup['SRP']]
        
        # Make final output dataframe
        df_out_study = pd.DataFrame(columns=sr_study_label) # Make empty dataframe for final output
        df_out_sample = pd.DataFrame(columns=pd.concat([sr_sample_label, sr_study_label]))
        df_out_study = pd.concat([df_out_study, df_study_edit])
        df_out_sample = pd.concat([df_out_sample, df_sample_edit])
        # Add query info.
        df_query_info = pd.DataFrame({'SRP': ['# query'], 'GSE': [query]})
        df_out_study = pd.concat([df_out_study, df_query_info], ignore_index=True)
        df_query_info = pd.DataFrame({'SRX': ['# query'], 'SRS': [query]})
        df_out_sample = pd.concat([df_out_sample, df_query_info], ignore_index=True)
        # Refine data
        df_out_study['Submission'] = df_out_study['Submission'].replace('GEO', '')
        df_out_sample['Submission'] = df_out_sample['Submission'].replace('GEO', '')

        ## Print the number of study and sample
        print('# Confirmed total numbers')
        print(f'  Study:  {len(df_out_study.index) -1}')
        print(f'  Sample: {len(df_out_sample.index) -1}\n')
        
        return df_out_study, df_out_sample

# Save metadata
def save_seq_metadata (df_study, df_sample, out_name):
    # Make output folder
    if not os.path.exists(OUT_FOLDER_NAME):
        os.mkdir(OUT_FOLDER_NAME)
        
    ## Export the outputs
    out_name_study = f'Meta_seq_{out_name}_study_n{df_study.shape[0] - 1}.txt'
    out_name_sample = f'Meta_seq_{out_name}_sample_n{df_sample.shape[0] - 1}.txt'
    df_study.to_csv(f'{OUT_FOLDER_NAME}/{out_name_study}', sep='\t', header=True, index=False)
    df_sample.to_csv(f'{OUT_FOLDER_NAME}/{out_name_sample}'
                     , sep='\t', header=True, index=False)

    print('# Metadata are saved.')
    print(f'  {out_name_study}')
    print(f'  {out_name_sample}')
    ## Export the raw table
    df_sample.to_csv(f'Metadata_{out_name}_raw.txt', sep='\t', header=True, index=False)

# Join variables with newlines
def join_variables_with_newlines(items, max_line_length=100):
    lines = []
    current_line = ""

    for item in items:
        if current_line:  # If current_line is not empty
            if len(current_line) + len(item) + 2 <= max_line_length:  # 2 for ', '
                current_line += ", " + item
            else:
                lines.append(current_line)
                current_line = item
        else:
            current_line = item
    
    if current_line:  # Append any remaining items in current_line to lines
        lines.append(current_line)

    return '\n'.join(lines)