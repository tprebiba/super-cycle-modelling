import matplotlib.pyplot as plt
import numpy as np
import constants as cnst


def plot_supercycle(supercycle,
                    fontsize=15, rotation=0, basic_period_tick=0.1,fig_length_scaling=0.3,
                    show_accelerator_label=False, show_bp_label=True):
    """
    Plot the super cycle consisting of different accelerator cycles.
    
    Parameters:
    - accelerator_cycles: List of tuples where each tuple contains the number of basic periods
                          for each accelerator cycle.
    """
    colors = plt.cm.viridis(np.linspace(0, 1, len(supercycle.cycles)))  # Generate colors for each cycle
    
    fig, ax = plt.subplots(figsize=(supercycle.length*fig_length_scaling, 2.5))
    lw=3
    
    if show_bp_label:
        ax.set_xlabel('Basic periods', fontsize=fontsize)
    ax.tick_params(axis='x', labelsize=fontsize, bottom=False)
    ax.tick_params(axis='y', left=False, labelleft=False)
    ax.set_title(supercycle.name + ' supercycle (%1.1f s)'%supercycle.length, fontsize=fontsize)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    shift = 0.5
    x = 0
    for cycle in supercycle.cycles:
        ax.plot([x+shift, x+shift], [0,1], color='black', linewidth=lw) # left border of cycle
        ax.text(x+shift+0.15, 0.8, cycle.name, fontsize=fontsize-3, color='black', rotation=rotation) # cycle name
        for i in range(cycle.bps):
            ax.add_patch(plt.Rectangle((x+shift, 0), 1, 1, color=cnst.SPS_CYCLES_COLORS[cycle.name], alpha=0.8, linewidth=0))
            ax.plot([x+shift, x+shift], [0,basic_period_tick], color='black', linewidth=lw) # basic period "tick"
            x += 1
        ax.plot([x+shift, x+shift], [0,1], color='black', linewidth=lw) # right border of cycle
    ax.plot([x+shift, x+shift], [0,basic_period_tick], color='black', linewidth=lw) # last basic period "tick"
    ax.plot([0+shift, x+shift], [0, 0], color='black', linewidth=lw) # bottom border of supercycle
    ax.plot([0+shift, x+shift], [1, 1], color='black', linewidth=lw) # top border of supercycle
    
    ax.set_xlim(shift-0.1,x+shift+0.1)
    ax.set_xticks(np.arange(1, x+1, 1))
    if show_accelerator_label:
        ax.set_ylabel(supercycle.accelerator, fontsize=fontsize, rotation=0)
        ax.set_xlim(shift-0.8,x+shift+0.1)
    ax.set_ylim(-0.02, 1.02)
    
    fig.tight_layout()
    plt.show()


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