import os

import pandas as pd


GEMLISTE_FILE = os.path.join(os.path.dirname(__file__), 'gemliste_knz - 2022-01-27.csv')

def get_plz_gcode_mapping(gemliste_file=GEMLISTE_FILE, minimal=True):
    data = pd.read_csv(gemliste_file, delimiter=';', skiprows=2, skipfooter=1, engine='python')
    data.columns = ['gkz', 'gname', 'gcode', 'status', 'plz_primary', 'plz_additional']
    
    # entries where PLZ occurrs in primary column
    primary = data.copy()
    primary['plz'] = primary.plz_primary
    primary['priority'] = primary.status.map({'SR': 3, 'ST': 2, 'M': 1}).fillna(0) + 100
    primary.iloc[:50]
    
    # entries where PLZ occurrs in additional column
    additional = data.copy()
    additional = additional.loc[~additional.plz_additional.isna(), :]
    additional['plz'] = additional.plz_additional.str.split(' ')
    additional['priority'] = additional.status.map({'SR': 3, 'ST': 2, 'M': 1}).fillna(0)
    additional = additional.explode('plz')
    additional['plz'] = additional['plz'].astype(int)
    
    mapping = pd.concat([primary, additional]).reset_index(drop=True)

    # For each PLZ get max priority entry
    mapping = mapping.loc[mapping.groupby(['plz'])['priority'].idxmax().values, :].reset_index(drop=True)
    
    if minimal:
        mapping = mapping.loc[:, ['plz', 'gcode']]

    return mapping