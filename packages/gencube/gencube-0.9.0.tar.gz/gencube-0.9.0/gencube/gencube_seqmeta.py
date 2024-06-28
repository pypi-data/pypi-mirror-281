# Custom functions
from .utils import (
    check_now,
    make_query, 
    search_sra, 
    fetch_meta, 
    convert_format,
    save_seq_metadata
    )

## gencube seqmeta ---------------------------------
def seqmeta(
    keywords,
    info,
    organism,
    strategy,
    source,
    platform,
    layout,
    selection,
    access,
    bioproject,
    biosample,
    accession,
    title,
    aligned,
    author,
    filter,
    mbases,
    publication,
    modification,
    properties,
    readlength,
    textword,
    exclude, 
    metadata,
    ):
    
    # Print information of organism, strategy, source
    if info:
        print('info')
        
    else:
        # Check the current time
        now = check_now()
        
        # Input query
        query, dic_query_pars, dic_query_kwds, dic_query_excs = make_query(
            organism, strategy, source, platform, selection, 
            filter, layout, access, bioproject, biosample, accession, 
            title, aligned, author, publication, modification, 
            properties, readlength, mbases, textword, keywords, exclude)

        print('# Search experimental sequencing data in NCBI SRA database')
        print(f'  Search query: {query} \n')
        
        # Check the number of searched results in each step
        print('# Check the number of searched result in each step')
        
        # Parameters
        if dic_query_pars:
            print('- Parameters')
            for key in list(dic_query_pars.keys()):
                out_count = search_sra(dic_query_pars[key])["Count"]
                if 'Intersection' not in key:
                    if dic_query_pars[key] == ' ':
                        print(f'  {key}')
                    else:
                        print(f'    {key}: {out_count}')
                else:
                    print('')
                    print(f'  Intersection (Parameters): {out_count}')
                    
                #print(dic_query_pars[key])
            print('')
        
        # Keywords
        if keywords:
            print('- Keywords with parameters')
            for key in list(dic_query_kwds.keys()):
                if 'space' in key:
                    print('')
                    continue
                out_count = search_sra(dic_query_kwds[key])["Count"]
                print(f'  {key}: {out_count}')
                
                #print(dic_query_kwds[key])
            print('')
        
        # Keywords for exclusion
        if exclude:
            print('- Keywords for exclusion with parameters')
            for key in list(dic_query_excs.keys()):
                out_count = search_sra(dic_query_excs[key])["Count"]
                print(f'  {key}: {out_count}')
                
                #print(dic_query_excs[key])
            print('')
        
        # Search query in the SRA database
        record = search_sra(query)
        search_ids = record['IdList']
        
        n = int(record["Count"])
        if n < 2:
            print(f'  Total {record["Count"]} sample-level ID is searched.\n')
        else:
            print(f'  Total {record["Count"]} sample-level IDs are searched.\n')
        
        # Fetch metadata, re-format, and save study- and sample-level tables
        if metadata:
            out_fetch = fetch_meta(search_ids)
            df_study, df_sample = convert_format(out_fetch, query)
            save_seq_metadata(df_study, df_sample)
        else:
            print('!! If you want to save the metadata of the searched datasets, please use the -m or --metadata option. \n')


