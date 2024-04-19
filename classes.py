import pandas as pnd
import matplotlib.pyplot as plt
import numpy as np
from helpers import load_cycle_from_csv
import constants as cnst
import warnings


class Cycle():
    '''
    A simple cycle representation
    Inputs:
        - accelerator [str]: accelerator name
        - name [str]: cycle name
        - bps [int]: number of basic periods
        - user [str] (optional): LSA timing user name
        - power [float] (optional): cycle power [MW]
        - filename [str] (optional): I mains csv file name
        - coupled_cycle [Cycle]: coupled cyc
        - number_of_injections [int] (optional): number of injections
    Other class variables:
        - length [float]: cycle length [sec]
        - x [list]: I mains x values
        - y [list]: I mains y values
    '''
    def __init__(self,
                 accelerator, name, bps,
                 user='', power=0, filename=None, 
                 coupled_cycle=None, number_of_injections=1):
        
        self.accelerator = accelerator 
        self.name = name
        self.bps = bps
        self.user = user
        self.power = power 
        self.filename = filename
        self.number_of_injections = number_of_injections

        self.length = self.bps*cnst.BASIC_PERIOD # [sec]        
        self.x = None
        self.y = None
        if filename:
            self.x, self.y = load_cycle_from_csv(filename)
        self.coupled_cycle = coupled_cycle
        if self.coupled_cycle:
            self.coupled_cycle_bps = self.coupled_cycle.bps*self.number_of_injections
        else:
            self.coupled_cycle_bps = 0
    

class SuperCycle():
    '''
    A simple super cycle representation
    Inputs:
        - accelerator [str]: accelerator name
        - name [str]: supercycle name
        - cycles [list]: list of cycles in the supercycle
    Other class variables:
        - cycle_names [list]: list of cycle names in the supercycle
        - bps [int]: number of basic periods of supercycle
        - length [float]: supercycle length [sec]
        - integrated_power [float]: integrated power [MW]
        - average_power [float]: average power [MW]
    Class methods:
        calculate_supercycle_length: calculates supercycle length and bps
        calculate_supercycle_power: calculates supercycle integrated and average power
        allocate_hours: allocates hours to the supercycle assuming a machine availability
            - allocated_hours [int]: allocated hours
            - allocated_seconds [int]: allocated seconds
            - allocated_bps [int]: allocated basic periods
            - number_of_supercycles_played [int]: number of supercycles played in the allocated time
            - number_of_cycles_played [dict]: number of times each cycle is played in the allocated time
        calculate_free_bps: calculates free BPs of the injector
            - free_bps_per_supercycle [int]: free BPs per supercycle
            - free_bps_total [int]: total free BPs

    '''
    def __init__(self, accelerator, name, cycles):
        
        self.accelerator = accelerator
        self.name = name
        self.cycles = cycles

        self.cycle_names = []
        for cycle in self.cycles:
            self.cycle_names.append(cycle.name)

        self.bps, self.length = self.calculate_supercycle_length()
        self.integrated_power, self.average_power = self.calculate_supercycle_power()
        
    def calculate_supercycle_length(self):
        '''
        Calculate super cycle length and bps
        '''
        bps = 0
        length = 0
        for cycle in self.cycles:
            bps += cycle.bps
            length += cycle.length
        if length > cnst.SPS_SC_LENGTH_LIMIT:
            raise ValueError('%s SPS SC length: %1.2f seconds exceeds limit of %1.2f seconds'%(self.name,self.length,cnst.SPS_SC_LENGTH_LIMIT))
        return bps, length
    
    def calculate_supercycle_power(self):
        '''
        Calculate super cycle average power
        '''
        integrated_power = 0
        for cycle in self.cycles:
            integrated_power += cycle.length*cycle.power
        average_power = integrated_power/self.length
        if average_power > cnst.SPS_RMS_POWER_LIMIT:
            raise ValueError('%s SPS RMS power: %1.2f MW exceeds limit of %1.2f MW'%(self.name,self.average_power,cnst.SPS_RMS_POWER_LIMIT))
        return integrated_power, average_power

    def allocate_hours(self, allocated_hours, machine_availability=1):
        '''
        Allocate hours to cycles in the supercycle
        Inputs:
            allocated_hours [dict]: allocated hours
            machine_availability [float]: machine availability
        '''
        self.allocated_hours = allocated_hours*machine_availability # effective
        self.allocated_seconds = self.allocated_hours*60*60
        self.allocated_bps = self.allocated_seconds/cnst.BASIC_PERIOD
        self.number_of_supercycles_played = self.allocated_seconds/self.length
        self.number_of_cycles_played = {}
        for cycle in np.unique(self.cycle_names):
            multiplicity = self.cycle_names.count(cycle)
            self.number_of_cycles_played[cycle] = self.number_of_supercycles_played*multiplicity

    def calculate_free_bps(self):
        '''
        Calculate free BPs for each cycle in the supercycle
        '''
        self.free_bps_per_supercycle = 0
        for cycle in self.cycles:
            self.free_bps_per_supercycle += cycle.bps - cycle.coupled_cycle_bps
        try:
            self.free_bps_total = self.free_bps_per_supercycle*self.number_of_supercycles_played
        except:
            warnings.warn('Number of supercycles played not calculated yet, needs to call allocate_hours method first.')
    
    def plot_supercycle(self,
                        fontsize=15, rotation=0, basic_period_tick=0.1,fig_length_scaling=0.3,
                        show_accelerator_label=False, show_bp_label=True):
        """
        Plot the super cycle consisting of different accelerator cycles.
        """
        supercycle = self
        
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