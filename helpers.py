import numpy as np
import pandas as pnd
from latex_helpers import df_to_latextable


def load_cycle_from_csv(filepath,xkey='logical.MBI/IMAINS',ykey='logical.MBI/IMAINS.1'):
    df = pnd.read_csv(filepath)
    df = df.drop(df.index[0])
    convert_dict = {}
    for key in df.keys():
        convert_dict[key] = float
    df = df.astype(convert_dict)
    return df[xkey], df[ykey]


def cycles_to_dataframe(cycles, write_to_latextable=False):
    # Gather SPS cycles in a dataframe
    df_cycles = pnd.DataFrame(columns=['Length [s]', 'BPs', 'Power (MB+MQ) [MW]']) 
    for c in cycles.keys():
        df_cycles = df_cycles._append(pnd.Series(name=c,
                                                data={'Length [s]': '%1.1f'%(cycles[c].length), 
                                                      'BPs': '%1.1f'%(cycles[c].bps),
                                                      'Power (MB+MQ) [MW]': '%1.2f'%(cycles[c].power)}))
    if write_to_latextable:
        print('Writing cycles to latex table.')
        df_to_latextable(df_cycles, filename='latex_tables/cycles.tex', column_format='lcc')
    return df_cycles


def supercycles_scenario_to_dataframe(supercycles_scenario, write_to_latextable=False):

    # Get all cycles from supercycles scenario
    cycle_names = []
    for supercycle in supercycles_scenario.keys():
        cycle_names += supercycles_scenario[supercycle].cycle_names
    cycle_names = list(np.unique(cycle_names))
    df = pnd.DataFrame(columns=cycle_names+['Length [s]', 'Power [MW]']) 
    
    for supercycle in supercycles_scenario.keys():
        data = {}
        
        data['Length [s]'] = supercycles_scenario[supercycle].length
        data['Power [MW]'] = round(supercycles_scenario[supercycle].average_power,2)

        for cycle in cycle_names:
            data[cycle] = int(0)

        for cycle in supercycles_scenario[supercycle].cycle_names:
                data[cycle] += int(1)
        
        for cycle in cycle_names:
            if data[cycle] == 0:
                data[cycle] = '-'
            elif data[cycle] > 0:
                data[cycle] = str(int(data[cycle]))
        
        df = df._append(pnd.Series(name=supercycle,data=data))

    if write_to_latextable:
        df_to_latextable(df, filename='latex_tables/shared_TCC8.tex', column_format='l|ccccccccccc|cc')

    return df