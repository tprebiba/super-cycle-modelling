import matplotlib.pyplot as plt
import numpy as np
import constants as cnst


def plot_actual_cycle_times(supercycle_scenario, schedule, 
                            SPScycl, colors, sps_availability,
                            startangle=0, savefigpath = None, autopct=True):
    
    actual_time = {}
    for cycle in SPScycl:
        actual_time[cycle] = 0
        for sc in supercycle_scenario:
            if cycle in supercycle_scenario[sc].get_cycle_names():
                # number of the particular super-cycle played in that year
                total_nr_of_sc = schedule[sc]*60*60/supercycle_scenario[sc].length
                actual_time[cycle] += total_nr_of_sc*supercycle_scenario[sc].cycle_dict[cycle]*SPScycl[cycle].length*sps_availability
    print(actual_time)
    
    f2, ax2 = plt.subplots(1, figsize=(8,6), facecolor='white')
    sizes = list(actual_time.values())
    labels = list(actual_time.keys())
    j = np.where(np.array(sizes)>0)
    if autopct:
        wedges = plt.pie(np.array(sizes)[j], labels=np.array(labels)[j], autopct='%1.1f%%', colors=np.array([colors[k] for k in labels])[j], textprops={'fontsize': 14}, startangle=startangle)
    else:
        wedges = plt.pie(np.array(sizes)[j], labels=np.array(labels)[j], colors=np.array([colors[k] for k in labels])[j], textprops={'fontsize': 14}, startangle=startangle)
    for w in wedges[0]:
        w.set_linewidth(1)
        w.set_edgecolor('w')
    plt.axis('equal')
    f2.tight_layout()
    plt.show()
    if savefigpath:
        f2.savefig(savefigpath, dpi=300)

        
def plot_power_consumption(supercycle_scenario, schedule, 
                            SPScycl, colors, sps_availability,
                            startangle=0, savefigpath = None):
    actual_power = {}
    for cycle in SPScycl:
        actual_power[cycle] = 0
        for sc in supercycle_scenario:
            if cycle in supercycle_scenario[sc].get_cycle_names():
                # number of the particular super-cycle played in that year
                total_nr_of_sc = schedule[sc]*60*60/supercycle_scenario[sc].length
                time = total_nr_of_sc*supercycle_scenario[sc].cycle_dict[cycle]*SPScycl[cycle].length*sps_availability
                actual_power[cycle] += time*SPScycl[cycle].power*1e-3/60/60 # in GWh

    f2, ax2 = plt.subplots(1, figsize=(8,6), facecolor='white')
    sizes = list(actual_power.values())
    labels = list(actual_power.keys())
    j = np.where(np.array(sizes)>0)
    sizes = np.array(sizes)[j]
    labels = np.array(labels)[j]
    def absolute_value(val):
        a  = np.round(val/100.*sizes.sum(), 0)
        return a
    wedges = plt.pie(sizes, labels=labels, autopct=absolute_value, colors=np.array([colors[k] for k in labels]), textprops={'fontsize': 14}, startangle=startangle)
    for w in wedges[0]:
        w.set_linewidth(1)
        w.set_edgecolor('w')
    plt.axis('equal')
    ax2.set_title('Total: %i GWh'%sizes.sum(), fontsize=17) 
    f2.tight_layout()
    plt.show()
    if savefigpath:
        f2.savefig(savefigpath, dpi=300)