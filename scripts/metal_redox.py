import math
import pandas as pd
import numpy as np
import os


def main():

    excel_table =  'funprof_geomosaic_kos.csv'
    working_dir = '/.samples/'
    lista = 'lsit_samples.txt'

    n,unique,raw_data = get_samples(
        working_dir=working_dir,
        sample_list=lista
    )

    acceptors, donors = match_kos(
        unique_ko_list=unique,
        spreadsheet=excel_table
    )
    
def get_samples(working_dir:str,sample_list:list):
    
    for s in sample_list:

        path_to_dir = os.path.join(working_dir,s,'funprofiler')
        if os.path.exists(path_to_dir):
            table = os.path.join(path_to_dir,'prefetch_out.csv')
            results = pd.read_csv(table, sep = ',')

            kos = results["match_name"]
            subset_ = results[["intersect_bp", "match_name"]]
            unique_kos = set(kos)
            n_kos = len(unique_kos)

    return n_kos,unique_kos,subset_


def match_kos(unique_ko_list:list,spreadsheet:str) -> tuple[A,D]:

    master_table = pd.read_csv(spreadsheet,sep = ',')
    # 1. Filter Sample KOs in our master table
    detected_mask = master_table['KO'].isin(unique_ko_list)
    print(detected_mask)

    filtered_df = master_table[detected_mask]
    # 2. Split into Donors (D) and Acceptors (A)
    donors = set(filtered_df[filtered_df['energyRole'] == 'D']['KO'])
    acceptors = set(filtered_df[filtered_df['energyRole'] == 'A']['KO'])

    return acceptors, donors



def redox_metaboli_index(donors_list:list,acceptors_list: list):

    donors_counts = np.array([donors_list])
    acceptors_counts = np.array([acceptors_list])
    # Compute the thoreatical maximum number of pairs
    index = np.log(donors_counts) + np.log(acceptors_counts)
    # or equivalently
    index2 = np.log(donors_counts * acceptors_counts)
    print("Index (sum form):", index)
    print("Index (product form):", index2)



def metal_plasticity_index():
    # metal plasticity index 
    # should be calculated by finding all the 'unique pairs' of metals, 
    # and then taking the logarithm of that

    









if __name__ == "__main__":
    main()