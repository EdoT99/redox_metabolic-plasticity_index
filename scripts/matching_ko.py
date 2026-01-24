#!/usr/bin/env python3

import argparse
import pandas as pd
import os
import gdown
from datetime import datetime

def main():


    args = parse_args()

    if args.download:
        print("Dowloading...")
        dowloads,date = download()
        match_table = match(dowloads,date)
    else:
        print("Using provided tables...")
        downloads = [args.table_ori, args.table_ref]
        date = dowloads[0].split("_")[-1]
        match_table = match(downloads,date)
    
    geo_ko_table = susbet(
        table_1=match_table,
        date=date
        )



def download():

    file_id = "15UoOvEQWEAQcsT9YdbUh3V66qc4hVk9Q16Y8kg6v2Nw"
    date = datetime.today().strftime("%Y%m%d")

    keys = {
        "Data_genes_biogeochemistry-Biogeochemical_genes":"2398433",
        "Data_genes_biogeochemistry-Genes_KO_funprofiler_processing":"1674537050"
        }
    
    downloads = []
    for name,gid in keys.items(): #ori,reference

        url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv&gid={gid}"
        output = f"download/{name}_{date}.csv"
        downloads.append(output)

        gdown.download(url, output, quiet=False)
    
    return downloads, date
    

def match(tables:list,date:str):

    table_1 = tables[1]
    table_2 = tables[0]

    original = pd.read_csv(table_1,sep=",")
    reference = pd.read_csv(table_2,sep=",")

    for i,line in enumerate(original.itertuples()):
        KO = line.KO

        for ref_row in reference.itertuples():
            ko_codes = str(ref_row.KO).split('+')

            if KO in ko_codes:
                value = ref_row.Catalyst_metal

                if value == "" or value == None:
                    match_value = "no_match"
                    original.loc[i, "Metal"] = match_value
                else:
                    match_value = value
                    original.loc[i, "Metal"] = match_value
                break

    
    path_to_table = os.path.join("tables",f"table_matched_{date}.csv")
    original.to_csv(path_to_table,sep=",",index = False)

    return path_to_table


def susbet(
        table_1:str,
        date:str
           ):
    original = pd.read_csv(table_1,sep=",")

    original["energyRole"] = (original["energyRole"].astype(str).str.strip().str.replace(r"\s+", "", regex=True))
    table_energy_roles = original[original["energyRole"].str.contains(r"^(A|D)(,?(A|D))*$",regex = True, na = False)]

    print(f"Total entries: {len(table_energy_roles['energyRole'])}")
    counts = table_energy_roles["energyRole"].value_counts()
    
    #print(f"A count: {counts.get('A', 0)}")
    #print(f"D count: {counts.get('D', 0)}")
    print(counts)

    path_to_table = os.path.join("tables",f"table_ko_energy_roles_{date}.csv")
    table_energy_roles.to_csv(path_to_table,sep=",",index = False)

    return path_to_table


def parse_args():
    parser = argparse.ArgumentParser("TEXT HERE")
    parser.add_argument("-a", "--table_ori",
        help="Downlaod tables from Drive"
    )
    parser.add_argument("-b", "--table_ref",
        help="Downlaod tables from Drive"
    )
    parser.add_argument("-d", "--download",
        help="Downlaod tables from Drive",
        action="store_true"
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
 