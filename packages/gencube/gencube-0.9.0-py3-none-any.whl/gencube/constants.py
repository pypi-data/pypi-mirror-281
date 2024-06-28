# For Entrez.email
EMAIL = "thsrms9216@gmail.com"

# NCBI server (README.txt - https://ftp.ncbi.nlm.nih.gov/genomes/all/README.txt)
NCBI_FTP_URL = 'https://ftp.ncbi.nlm.nih.gov/genomes/all'

# ENSEMBL
ENSEMBL_FTP_HOST = 'ftp.ensembl.org'
ENSEMBL_FTP_URL = 'http://ftp.ensembl.org/pub/'
ENSEMBL_RAPID_FTP_URL = ENSEMBL_FTP_URL + 'rapid-release/'
ENSEMBL_RM_FTP_URL = 'https://ftp.ebi.ac.uk/pub/databases/ensembl/repeats/unfiltered_repeatmodeler/species/'

# UCSC GenArk server (the Earth BioGenome Project, the Vertebrate Genomes Project, the Telomere-to-Telomere Consortium, and other related projects.)
GENARK_URL = 'https://hgdownload.soe.ucsc.edu/hubs/'

# Zoonomia (200 mammals project)
ZOONOMIA_URL = 'https://genome.senckenberg.de/download/TOGA/'

# UCSC-Kent applications
BIGWIG2BEDGRAPH = 'https://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/bigWigToBedGraph'
BEDGRAPH2BIGWIG = 'https://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/bedGraphToBigWig'
BIGBED2BED = 'https://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/bigBedToBed'
BED2BIGBED = 'https://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/bedToBigBed'

## Lists
LS_NCBI_ASSEMBLY_META_KEY = [
    'Synonym_GCA',
    'Synonym_GCF',
    'LatestAccession',
    'AssemblyName',
    'UCSCName',
    'GB_BioProjects',
    'BioSampleAccn',
    'Taxid',
    'Organism',
    'AssemblyType',
    'AssemblyStatus',
    'Coverage',
    'ReleaseLevel',
    'ReleaseType',
    'AsmReleaseDate_GenBank',
    'AsmUpdateDate',
    'SubmitterOrganization',
    'ContigN50',
    'ScaffoldN50',
    'Biosource',
    'PropertyList'
    ]
LS_NCBI_ASSEMBLY_META_LABEL = [
    'Genbank',
    'RefSeq',
    'Latest accession',
    'Assembly name',
    'UCSC',
    'Bioproject',
    'Biosample',
    'Taxid',
    'Organism',
    'Assembly type',
    'Level',
    '#Coverage',
    '#ReleaseLevel',
    '#ReleaseType',
    'Release',
    'Update',
    'Organization',
    '#ContigN50',
    '#ScaffoldN50',
    '#Biosource',
    '#PropertyList'
    ]
LS_GENCUBE_GENOME_LABEL = [
    'Assembly name', 
    'Taxid',
    'Release',
    'NCBI',
    'UCSC', 
    'GenArk',
    'Ensembl',
    ]
LS_GENCUBE_GENSET_LABEL = [
    'Assembly name', 
    'Taxid',
    'Release',
    'NCBI', 
    'UCSC', 
    'GenArk',
    'Ensembl',
    'Zoonomia',
    ]
LS_GENCUBE_SEQUENCE_LABEL = [
    'Assembly name', 
    'Taxid',
    'Release',
    'NCBI', 
    'UCSC', 
    'Ensembl',
    ]
LS_GENCUBE_ANNOTATION_LABEL = [
    'Assembly name', 
    'Taxid',
    'Release',
    'NCBI', 
    'UCSC', 
    'GenArk',
    ]
LS_GENCUBE_CROSSGENOME_LABEL = [
    'Assembly name', 
    'Taxid',
    'Release',
    'NCBI', 
    'UCSC', 
    'Ensembl',
    'Zoonomia',
    ]

LS_SRA_META_STUDY_KEY = [
    'EXPERIMENT.STUDY_REF.@accession', 
    'STUDY.@alias', 
    'SAMPLE.SAMPLE_LINKS.SAMPLE_LINK.XREF_LINK.LABEL', 
    'EXPERIMENT.STUDY_REF.IDENTIFIERS.EXTERNAL_ID.#text', 
    'STUDY.DESCRIPTOR.STUDY_TITLE', 
    'STUDY.DESCRIPTOR.STUDY_ABSTRACT', 
    'EXPERIMENT.DESIGN.LIBRARY_DESCRIPTOR.LIBRARY_CONSTRUCTION_PROTOCOL', 
    'SUBMISSION.@center_name', 
    'Organization.Contact.Address.Country', 
    'RUN_SET.RUN.@published'
    ]
LS_SRA_META_SAMPLE_KEY = [
    'EXPERIMENT.@accession', 
    'SAMPLE.@accession', 
    'EXPERIMENT.DESIGN.SAMPLE_DESCRIPTOR.IDENTIFIERS.EXTERNAL_ID.#text', 
    'SAMPLE.SAMPLE_NAME.TAXON_ID', 
    'EXPERIMENT.DESIGN.LIBRARY_DESCRIPTOR.LIBRARY_STRATEGY', 
    'EXPERIMENT.DESIGN.LIBRARY_DESCRIPTOR.LIBRARY_SOURCE', 
    'EXPERIMENT.DESIGN.LIBRARY_DESCRIPTOR.LIBRARY_SELECTION', 
    'EXPERIMENT.PLATFORM.ILLUMINA.INSTRUMENT_MODEL', 
    'EXPERIMENT.TITLE', 
    'SAMPLE.TITLE', 
    'EXPERIMENT.DESIGN.LIBRARY_DESCRIPTOR.LIBRARY_NAME',
    'RUN_SET.RUN.SRAFiles.SRAFile',
    'EXPERIMENT.DESIGN.DESIGN_DESCRIPTION', 
    'SAMPLE.SAMPLE_ATTRIBUTES.SAMPLE_ATTRIBUTE', 
    'EXPERIMENT.EXPERIMENT_ATTRIBUTES.EXPERIMENT_ATTRIBUTE'
    ]
LS_SRA_META_STUDY_LABEL = [
    'SRP', 
    'GSE', 
    'BioProject', 
    'BioProject_alt', 
    'Title', 
    'Abstract', 
    'Protocol', 
    'Submission', 
    'Country', 
    'Published'
    ]
LS_SRA_META_SAMPLE_LABEL = [
    'SRX', 
    'SRS', 
    'GSM', 
    'Taxon id', 
    'Strategy', 
    'Source', 
    'Selection', 
    'Instrument model', 
    'Experiment title', 
    'Sample title', 
    'Library name',
    'File information',
    'Design description', 
    'Sample attribute', 
    'Experiment attribute'
    ]

LS_ASSEMBLY_REPORT_LABEL = [
    'Sequence-Name', 
    'Sequence-Role', 
    'Assigned-Molecule', 
    'Assigned-Molecule-Location/Type', 
    'GenBank-Accn', 
    'Relationship', 
    'RefSeq-Accn', 
    'Assembly-Unit', 
    'Sequence-Length', 
    'UCSC-style-name'
    ]

# Dictionaries
DIC_ZOONOMIA = {
    'human': 'human_hg38_reference', 
    'mouse': 'mouse_mm10_reference', 
    'chicken': 'chicken_galGal6_reference', 
    'greenSeaturtle': 'greenSeaturtle_HLcheMyd2_reference', 
    'pikePerch': 'pikePerch_HLsanLuc1_reference', 
    'purpleSeaUrchin': 'purpleSeaUrchin_HLstrPur5_reference', 
    'redEaredSlideTurtle': 'redEaredSlideTurtle_HLtraScrEle1_reference', 
    'thaleCress': 'thaleCress_HLParaTha1_reference', 
    'tobaccoHawkmoth': 'tobaccoHawkmoth_HLmanSex2_reference'
    }

DIC_STRATEGY = {
    # Genomic
    'wgs': 'Whole Genome Sequencing',
    'wga': 'Whole Genome Amplification',
    'wxs': 'Whole Exome Sequencing',
    'targeted_capture': 'Targeted Capture sequencing',
    'synthetic_long_read': 'Synthetic Long Read sequencing',
    'gbs': 'Genotyping by Sequencin',
    'rad_seq': 'Restriction Site Associated DNA Sequencing',
    'tn_seq': 'Tn sequencing, potentially referring to Transposon Sequencing',
    'clone_end': 'Clone End sequencing',
    # Genomic or Transcriptomic,
    'amplicon': 'Amplicon sequencing',
    'clone': 'Cloning sequencing',
    # Transcriptomic
    'rna_seq': 'RNA sequencing',
    'mrna_seq': 'messenger RNA sequencing',
    'ncrna_seq': 'non-coding RNA sequencing',
    'ribo_seq': 'Ribosome profiling',
    'rip_seq': 'RNA Immunoprecipitation sequencing',
    'mirna_seq': 'microRNA sequencing',
    'ssrna_seq': 'single-stranded RNA sequencing',
    'est': 'Expressed Sequence Tag sequencing',
    'fl_cdna': 'Full-Length complementary DNA sequencing',
    # Epigenomic - Chromatin Accessibility
    'atac_seq': 'Assay for Transposase-Accessible Chromatin sequencing',
    'dnase_hypersensitivity': 'DNase Hypersensitivity sequencing',
    'faire_seq': 'Formaldehyde-Assisted Isolation of Regulatory Elements sequencing',
    # Epigenomic - DNA-Protein Binding
    'chip_seq': 'Chromatin Immunoprecipitation Sequencing',
    'chip': 'Chromatin Immunoprecipitation',
    # Epigenomic - Methylome
    'mre_seq': 'Methylation-Sensitive Restriction Enzyme sequencing',
    'bisulfite_seq': 'Bisulfite sequencing',
    'mbd_seq': 'Methyl-CpG Binding Domain sequencing',
    'medip_seq': 'Methylated DNA Immunoprecipitation sequencing',
    # Epigenomic - Chromatin Interaction and Structural Analysis
    'hi_c': 'Hi-C sequencing for three-dimensional genome structure analysis',
    'chia_pet': 'Chromatin Interaction Analysis by Paired-End Tag Sequencing',
    'tethered_chromatin_conformation_capture': 'Tethered Chromatin Conformation Capture',
    }
DIC_SOURCE = {
    'genomic': '',
    'genomic_single_cell': '',
    'transcriptomic': '',
    'transcriptomic_single_cell': '',
    'metagenomic': '',
    'metatranscriptomic': '',
    'synthetic': '',
    'viral_rna': '',
    'other': '',
    }

DIC_PLATFORM = {
    'abi_solid': '',
    'bgiseq': '',
    'capillary': '',
    'complete_genomics': '',
    'dnbseq': '',
    'element': '',
    'genapsys': '',
    'genemind': '',
    'helicos': '',
    'illumina': '',
    'ion_torrent': '',
    'ls454': '',
    'oxford_nanopore': '',
    'pacbio_smrt': '',
    'tapestri': '',
    'ultima': '',
    'vela_diagnostics ': '',
    }

DIC_SELECTION = {
    '5_methylcytidine_antibody': '',
    'cage':'',
    'cdna':'',
    'cdna_oligo_dt': '',
    'cdna_randompriming': '',
    'chip':'',
    'chip_seq': '',
    'dnase':'',
    'hmpr':'',
    'hybrid_selection': '',
    'inverse_rrna': '',
    'mbd2_protein_methyl_cpg_binding_domain': '',
    'mda':'',
    'mf':'',
    'mnase':'',
    'msll':'',
    'oligo_dt': '',
    'other':'',
    'padlock_probes_capture_method': '',
    'pcr':'',
    'polya':'',
    'race':'',
    'random':'',
    'random_pcr': '',
    'reduced_representation': '',
    'repeat_fractionation': '',
    'restriction_digest': '',
    'rt_pcr': '',
    'size_fractionation': '',
    'unspecified': '',
    }

DIC_FILTER = {
    'cloud_gs': '',
    'cloud_s3': '',
    'dna_data': '',
    'filetype_bai': '',
    'filetype_bam': '',
    'filetype_crai': '',
    'filetype_cram': '',
    'filetype_fcs': '',
    'filetype_fastq': '',
    'filetype_native': '',
    'filetype_sff': '',
    'genomic': '',
    'library_layout_paired': '',
    'library_layout_single': '',
    'metagenomic': '',
    'metatranscriptomic': '',
    'other': '',
    'platform_abi_solid': '',
    'platform_bgiseq': '',
    'platform_capillary': '',
    'platform_complete_genomics': '',
    'platform_hellicos': '',
    'platform_illumina': '',
    'platform_ion_torrent': '',
    'platform_lsa454': '',
    'platform_oxford_nanopore': '',
    'platform_pacbio_smrt': '',
    'rna_data': '',
    'sra_all': '',
    'sra_assembly': '',
    'sra_bioproject': '',
    'sra_bioproject_all': '',
    'sra_biosample': '',
    'sra_biosample_all': '',
    'sra_gap': '',
    'sra_gap_all': '',
    'sra_gds': '',
    'sra_genome': '',
    'sra_gnm': '',
    'sra_nuccore': '',
    'sra_nuccore_alignment': '',
    'sra_nuccore_wgs': '',
    'sra_omni': '',
    'sra_smp': '',
    'sra_public': '',
    'sra_pubmed': '',
    'sra_taxonomy': '',
    'strategy_amplico_seq': '',
    'strategy_atac_seq': '',
    'strategy_bisulfite_seq': '',
    'strategy_chia_pet': '',
    'strategy_chip': '',
    'strategy_chip_seq': '',
    'strategy_chromosome_immunoprecipitation': '',
    'strategy_clone': '',
    'strategy_cloneend': '',
    'strategy_cts': '',
    'strategy_dnase_hypersensitivity': '',
    'strategy_epigenomic': '',
    'strategy_est': '',
    'strategy_exome': '',
    'strategy_faire_seq': '',
    'strategy_finishing': '',
    'strategy_fl_cdna': '',
    'strategy_full_length_cdna': '',
    'strategy_genome': '',
    'strategy_hi_c': '',
    'strategy_hla': '',
    'strategy_medip_seq': '',
    'strategy_mirna_seq': '',
    'strategy_mnase_seq': '',
    'strategy_mre_seq': '',
    'strategy_ncrna_seq': '',
    'strategy_other': '',
    'strategy_other': '',
    'strategy_poolclone': '',
    'strategy_rad_seq': '',
    'strategy_rip_seq': '',
    'strategy_rna_seq': '',
    'strategy_rnaseq': '',
    'strategy_selex': '',
    'strategy_synthetic_long_read': '',
    'strategy_targeted_capture': '',
    'strategy_tn_seq': '',
    'strategy_validation': '',
    'strategy_wcs': '',
    'strategy_wes': '',
    'strategy_wgseq': '',
    'strategy_wgs': '',
    'strategy_whole_exome_sequencing': '',
    'strategy_whole_genome_amplification': '',
    'strategy_whole_genome_sequencing': '',
    'strategy_wxs': '',
    'synthetic': '',
    'transcriptomic': '',
    'type_exome': '',
    'type_genome': '',
    'type_mnaseq': '',
    'viral_rna': '',
}



"""
DIC_ORGANISM = {
    'human': 'homo sapiens',
    'mouse': 'mus musculus',
    'dog': 'canis lupus familiaris',
    'dingo': 'canis lupus dingo',
    'wolf': 'canis lupus',
    # Pet animals
    'cat': 'felis catus',
    # Farm animals
    'pig': 'sus scrofa',
    'pig_domestic': 'sus scrofa domesticus',
    'cow': 'bos taurus',
    'dairy_cow': 'Bos indicus',
    'chicken': 'gallus gallus',
    'horse': 'equus caballus',
    # Farm plants
    'rice': 'oryza sativa',
    'wheat': 'triticum aestivum',
    # Peto's paradox (Long-lived & cancer-free)
    'elephant': 'loxodonta africana', # 아프리카 코끼리
    'whale': 'balaenoptera musculus', # 흰수염고래
    'naked_mole_rat': 'heterocephalus glaber',
    'blind_mole_rat': 'spalax ehrenbergi',
    # Primates
    'gorilla': 'gorilla gorilla',
    'rhesus_monkey': 'macaca mulatta', # 리서스 원숭이
    'cynomolgus_monkey': 'macaca fascicularis', # 시노몰거스 원숭이
    'baboon': 'papio', # 바부인
    'chimpanzee': 'pan troglodytes', # 침팬지
    'marmoset': 'callithrix jacchus',  # 마모셋
    'macaque': 'macaca',
    'capuchin_monkey': 'cebus capucinus',  # Used in behavioral studies and neuroscience
    'squirrel_monkey': 'saimiri sciureus',  # Used in neurobiology, behavioral biology, and pharmacology
    'bonobo': 'pan paniscus',  # Close relation to chimpanzees, used in behavioral and social studies, genetics
    # Experimental models
    'yeast': 'saccharomyces cerevisiae',
    'fruit_fly': 'drosophila melanogaster',
    'nematode': 'caenorhabditis elegans',
    'zebrafish': 'danio rerio',
    'african clawed frog': 'xenopus laevis',
    'rat': 'rattus norvegicus',
    'guinea pig': 'cavia porcellus',
    'rabbit': 'oryctolagus cuniculus',
    # Etc
    'opossum': 'didelphis virginiana'
    }   
"""