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


def cycles_to_dataframe(cycles):
    # Gather SPS cycles in a dataframe
    df_cycles = pnd.DataFrame(columns=['Length [s]', 'BPs', 'Power (MB+MQ) [MW]']) 
    for c in cycles.keys():
        df_cycles = df_cycles._append(pnd.Series(name=c,
                                                data={'Length [s]': '%1.1f'%(cycles[c].length), 
                                                      'BPs': '%1.1f'%(cycles[c].bps),
                                                      'Power (MB+MQ) [MW]': '%1.2f'%(cycles[c].power)}))
    #df_to_latextable(df_cycles, filename='latex_tables/cycles.tex', column_format='lcc')
    return df_cycles


def supercycles_scenario_to_dataframe(supercycles_scenario, 
                                     save_to_latex_file=False):

    # Get all cycles from supercycles scenario
    cycles_list = []
    for supercycle in supercycles_scenario.keys():
        cycles_list += supercycles_scenario[supercycle].cycle_names
    cycle_list = list(np.unique(cycles_list))

    df = pnd.DataFrame(columns=cycle_list+['Length [s]', 'Power [MW]']) 
    
    for supercycle in supercycles_scenario.keys():
        data = {}
        for cycle in cycle_list:
            if cycle in supercycles_scenario[supercycle].cycle_names:
                data[cycle] = '1'
            else:
                data[cycle] = '-'
        data['Length [s]'] = supercycles_scenario[supercycle].length
        data['Power [MW]'] = round(supercycles_scenario[supercycle].average_power,2)
        df = df._append(pnd.Series(name=supercycle,data=data))

    if save_to_latex_file:
        df_to_latextable(df, filename='latex_tables/shared_TCC8.tex', column_format='l|ccccccccccc|cc')

    return df


def schedule_to_dataframe(schedule,total_hours, total_hours_recalculated, fraction_no_LHC, fraction):
    df_schedule = pnd.DataFrame(columns=['Scheduled [hours]', 'Effective [hours]', 'Super-cycle percentage [%]']) 
    for c in schedule.keys():
        data = {'Scheduled [hours]': '%1.1f'%(schedule[c]/fraction_no_LHC), 
                'Effective [hours]': '%1.2f'%(schedule[c]),
                'Super-cycle percentage [%]': '%1.2f'%(schedule[c]/total_hours*100)}
        name = c
        if 'LHC' in c:
            data = {'Scheduled [hours]': '-', 
                    'Effective [hours]': '%1.2f'%(schedule[c]),
                    'Super-cycle percentage [%]': '%1.2f'%(schedule[c]/total_hours*100)}
            name = c + ' (%i%% of time)'%(fraction[c]*100)
        df_schedule = df_schedule.append(pnd.Series(name=name,data=data))
    df_schedule = df_schedule.append(pnd.Series(name='Total',data={'Scheduled [hours]': total_hours, 'Effective [hours]': total_hours_recalculated, 'Super-cycle percentage [%]': total_hours/total_hours_recalculated*100}))
    return df_schedule