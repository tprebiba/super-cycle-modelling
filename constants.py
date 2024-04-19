from classes import Cycle, SuperCycle
import matplotlib.pyplot as plt


BASIC_PERIOD = 1.2 # [s]


#######################################################
# PSB
#######################################################
PSB_AVAILABILITY = 0.95
PSB_CYCLES = {
    'ISOLDE': Cycle(accelerator='PSB', name='ISOLDE', bps=1),
    'AD': Cycle(accelerator='PSB', name='AD', bps=1),
    'TOF': Cycle(accelerator='PSB', name='TOF', bps=1),
    'EAST': Cycle(accelerator='PSB', name='EAST', bps=1),
    'MTE': Cycle(accelerator='PSB', name='MTE', bps=1),
    'LHC': Cycle(accelerator='PSB', name='LHC', bps=1),
    'AWAKE': Cycle(accelerator='PSB', name='AWAKE', bps=1),
}


#######################################################
# PS
#######################################################
PS_AVAILABILITY = 0.9
PS_CYCLES = {
    'AD': Cycle(accelerator='PS', name='AD', bps=2,
                user='AD'),
    'TOF': Cycle(accelerator='PS', name='TOF', bps=1,
                 user='TOF'),
    'EAST': Cycle(accelerator='PS', name='EAST', bps=2,
                  user='EAST1'),
    'MTE (2 injections)': Cycle(accelerator='PS', name='MTE', bps=1*2, # two injections into the SPS
                 user='SFTPRO1'),
    'LHC (4 injections)': Cycle(accelerator='PS', name='LHC', bps=3*4, # four injections into the LHC
                 user='LHC1'),
    'AWAKE': Cycle(accelerator='PS', name='AWAKE', bps=2,
                   user='AWAKE1'),
    'LHC pilot': Cycle(accelerator='PS', name='LHC pilot', bps=2),
    'MD dedicated': Cycle(accelerator='PS', name='MD dedicated', bps=3*4),
    'MD parallel': Cycle(accelerator='PS', name='MD parallel', bps=2),
    'Scrubbing': Cycle(accelerator='PS', name='Scrubbing', bps=3*4),
    'HiRadMat': Cycle(accelerator='PS', name='HiRadMat', bps=3*4),
                       
}


#######################################################
# SPS
#######################################################
SPS_AVAILABILITY = 0.8
SPS_RMS_POWER_LIMIT = 41.1 # [MW]
SPS_SC_LENGTH_LIMIT = 90 # [s]
_source = '../01_protons_2021-2022_SPS/power_consumption_measurements/SPS_cycle_power_estimation/SPS_cycles_MBI_IMAINS/'
SPS_CYCLES = {
    #--------------------------------------------------------
    # Typical operational cycles
    'AWAKE': Cycle(accelerator='SPS', name='AWAKE', bps=6,
                   user='AWAKE1', power=31.19,filename=_source+'AWAKE1_7point2s.csv', 
                   coupled_cycle=PS_CYCLES['AWAKE']),
    'HiRadMat': Cycle(accelerator='SPS', name='HiRadMat', bps=20,
                      user='HIRADMT2', power=17.52,filename=_source+'HIRADMT2_24s.csv'),
    'SFTPRO': Cycle(accelerator='SPS', name='SFTPRO', bps=9,
                    user='SFTPRO1',power=52.83,filename=_source+'SFTPRO1_10point8.csv', 
                    coupled_cycle=PS_CYCLES['MTE (2 injections)']),
    'LHC filling': Cycle(accelerator='SPS', name='LHC filling', bps=20,
                         user='LHC25NS',power=18.03,filename=_source+'LHC25NS_LHC_filling_24s.csv', 
                         coupled_cycle=PS_CYCLES['LHC (4 injections)']),
    'LHC pilot': Cycle(accelerator='SPS', name='LHC pilot', bps=11,
                       user='LHCPILOT',power=32.5,filename=_source+'LHCPILOT_13point2s.csv'),
    'MD dedicated': Cycle(accelerator='SPS', name='MD dedicated', bps=20,
                          user='MD5',power=18.03,filename=_source+'LHC25NS_MD_dedicated_24s.csv'), # LHC25NS
    'MD parallel': Cycle(accelerator='SPS', name='MD parallel', bps=6,
                         user='MD5',power=2.81,filename=_source+'MD5_MD_parallel_7point2s.csv'),
    'Scrubbing': Cycle(accelerator='SPS', name='Scrubbing', bps=20, 
                       user='',power=18.03,filename=_source+'LHC25NS_Scrubbing_24s.csv'), # LHC25NS
    'Zero': Cycle(accelerator='SPS', name='Zero', bps=1,
                  user='ZERO',power=1.2,filename=_source+'Zero_1point2s.csv'),
    'deGauss': Cycle(accelerator='SPS', name='deGauss', bps=3,
                    user='MD1',power=4.77,filename=_source+'MD1_deGauss_3point6s.csv'),
    #--------------------------------------------------------
    # Future cycles
    'ECN3_D (1.2s)': Cycle(accelerator='SPS', name='ECN3_D (1.2s)', bps=6,#6,
                        user='',power=34.88,filename=_source+'SFTPRO1_7point2s_ESTIMATED.csv', # power estimation is correct?
                        coupled_cycle=PS_CYCLES['MTE (2 injections)']), 
    'ECN3_D (2.4s)': Cycle(accelerator='SPS', name='ECN3_D (2.4s)', bps=7,
                        user='',power=44.84,filename=_source+'SFTPRO1_8point4s_ESTIMATED.csv', # power estimation should be overestimated a bit
                        coupled_cycle=PS_CYCLES['MTE (2 injections)']), 
    'ECN3_D (4.8s)': Cycle(accelerator='SPS', name='ECN3_D (4.8s)', bps=9,
                        user='',power=52.83,filename=_source+'SFTPRO1_10point8.csv',
                        coupled_cycle=PS_CYCLES['MTE (2 injections)']), 
    'ECN3_D (9.6s)': Cycle(accelerator='SPS', name='ECN3_D (9.6s)', bps=13,
                        user='',power=63.6,filename=_source+'SFTPRO1_15point6s_ESTIMATED.csv', # power from Hannes' values
                        coupled_cycle=PS_CYCLES['MTE (2 injections)']), 
    'SFTPRO (1.2s)': Cycle(accelerator='SPS', name='SFTPRO (1.2s)', bps=6,
                        user='',power=34.88,filename=_source+'SFTPRO1_7point2s_ESTIMATED.csv', # power estimation is correct?
                        coupled_cycle=PS_CYCLES['MTE (2 injections)']), 
    'SFTPRO (9.6s)': Cycle(accelerator='SPS', name='SFTPRO (9,6s)', bps=13,
                        user='',power=63.6,filename=_source+'SFTPRO1_15point6s_ESTIMATED.csv', # power from Hannes' values
                        coupled_cycle=PS_CYCLES['MTE (2 injections)']), 
    'deGauss (3.6s)': Cycle(accelerator='SPS', name='deGauss (3.6s)', bps=3,
                            user='MD1',power=4.77,filename=_source+'MD1_deGauss_3point6s.csv'),
    'deGauss (10.8s)': Cycle(accelerator='SPS', name='deGauss (10.8s)', bps=9,
                            user='',power=2.69,filename=_source+'MD1_deGauss_10point8s_ESTIMATED.csv'), # power estimation should be correct
    #--------------------------------------------------------
    # Year specific cycles/users? Power from CCM application
    'HIRADMT1': Cycle(accelerator='SPS', name='HIRADMT1', bps=7, 
                      user='HIRADMT1', power=35.1),
    'LHC1': Cycle(accelerator='SPS', name='LHC1', bps=23,
                  user='LHC1', power=15.72),
    'LHCMD1': Cycle(accelerator='SPS', name='LHCMD1', bps=23,
                    user='LHCMD1', power=15.72),
    'LHC4': Cycle(accelerator='SPS', name='LHC4', bps=11,
                  user='LHC4', power=32.5),
    'LHCINDIV': Cycle(accelerator='SPS', name='LHCINDIV', bps=17,
                      user='LHCINDIV', power=20.4),
    'LHC3': Cycle(accelerator='SPS', name='LHC3', bps=11,
                  user='LHC3', power=32.5),
    'LHCION2': Cycle(accelerator='SPS', name='LHCION2', bps=48,
                     user='LHCION2', power=8.92),
    'LHCION1': Cycle(accelerator='SPS', name='LHCION1', bps=12,
                     user='LHCION1', power=35.25),
    'LHCION3': Cycle(accelerator='SPS', name='LHCION3', bps=11,
                     user='LHCION3', power=29.39),
    'LHCMD2': Cycle(accelerator='SPS', name='LHCMD2', bps=7,
                    user='LHCMD2', power=6.43),
    'MD3': Cycle(accelerator='SPS', name='MD3', bps=22,
                 user='MD3', power=5.07),
    'LHC2': Cycle(accelerator='SPS', name='LHC2', bps=6,
                  user='LHC2', power=2.81),
    'LHC50NS': Cycle(accelerator='SPS', name='LHC50NS', bps=6,
                     user='LHC50NS', power=2.97),
    'LHCMD4': Cycle(accelerator='SPS', name='LHCMD4', bps=24,
                    user='LHCMD4', power=14.82),
    'LHCMD3': Cycle(accelerator='SPS', name='LHCMD3', bps=24,
                    user='LHCMD3', power=20.09),
    'MD2': Cycle(accelerator='SPS', name='MD2', bps=5,
                 user='MD2', power=9.92),
    'SFTION2': Cycle(accelerator='SPS', name='SFTION2', bps=18,
                     user='SFTION2', power=0.36),
    'SFTION1': Cycle(accelerator='SPS', name='SFTION1', bps=21,
                     user='SFTION1', power=33.8),
    'MD4': Cycle(accelerator='SPS', name='MD4', bps=6,
                 user='MD4', power=4.89),
    'SFTSHIP': Cycle(accelerator='SPS', name='SFTSHIP', bps=9,
                    user='SFTSHIP', power=52.84),
    'SFTPRO2': Cycle(accelerator='SPS', name='SFTPRO2', bps=9,
                     user='SFTPRO2', power=52.7),
    'LHCION4': Cycle(accelerator='SPS', name='LHCION4', bps=11,
                     user='', power=29.39), # didn't find it, just copied LHCION3
    'SFTION4': Cycle(accelerator='SPS', name='SFTION4', bps=18,
                     user='', power=0.36)  # didn't find it, just copied SFTION2
}
_prop_cycle = plt.rcParams['axes.prop_cycle']
_colors_list = _prop_cycle.by_key()['color']
SPS_CYCLES_COLORS = {
    'SFTPRO (1.2s)': _colors_list[0], 'SFTPRO (4.8s)': _colors_list[0], 'SFTPRO': _colors_list[0], 'SFTPRO (9.6s)': _colors_list[0], 'TCC2': _colors_list[0], 'SFTPRO2': _colors_list[0],
    'LHC filling': _colors_list[1], 'LHC pilot': _colors_list[1], 'LHC': _colors_list[1], 'LHCINDIV': _colors_list[1], 'LHC1': _colors_list[1], 'LHC2': _colors_list[1], 'LHC3': _colors_list[1], 'LHC4': _colors_list[1], 'LHC50NS': _colors_list[1],
    'ECN3_D (1.2s)': _colors_list[2], 'ECN3_D (2.4s)': _colors_list[2], 'ECN3_D (4.8s)': _colors_list[2], 'ECN3_D (9.6s)': _colors_list[2], 'BDF/SHiP': _colors_list[2], 'SFTSHIP': _colors_list[2],
    'MD dedicated': _colors_list[3], 'MD parallel': _colors_list[3], 'Scrubbing': _colors_list[3], 'MD': _colors_list[3], 'MD2': _colors_list[3], 'MD3': _colors_list[3], 'MD4': _colors_list[3], 'LHCMD1': _colors_list[3], 'LHCMD2': _colors_list[3], 'LHCMD3': _colors_list[3], 'LHCMD4': _colors_list[3],
    'AWAKE': _colors_list[4], 'HiRadMat': _colors_list[4], 'HIRADMT1': _colors_list[4], 
    'Zero': _colors_list[5], 'deGauss (3.6s)': _colors_list[5], 'deGauss (10.8s)': _colors_list[5], 'deGauss': _colors_list[5],
    'SFTION1': _colors_list[6], 'SFTION2': _colors_list[6], 'LHCION1': _colors_list[6], 'LHCION2': _colors_list[6], 'LHCION3': _colors_list[6], 'Ions': _colors_list[6], 'LHCION4': _colors_list[6], 'SFTION4': _colors_list[6]
    
}


#######################################################
# Time sharing per year
#######################################################
TOTAL_DAYS = {
    'Protons only': 35*7-2*(30/24), # 35 weeks (245 days) minus 2*30 hours of technical stops 
    'With ion run': 31*7-2*(30/24), # 31 weeks (217 days) minus 2*30 hours of technical stops
}
TOTAL_HOURS = {
    'Protons only': TOTAL_DAYS['Protons only']*24,
    'With ion run': TOTAL_DAYS['With ion run']*24,
}
TOTAL_SECONDS = {
    'Protons only': TOTAL_HOURS['Protons only']*3600,
    'With ion run': TOTAL_HOURS['With ion run']*3600,
}
TOTAL_BPs = {
    'Protons only': TOTAL_HOURS['Protons only']/BASIC_PERIOD,
    'With ion run': TOTAL_HOURS['With ion run']/BASIC_PERIOD,
}
SPS_SUPERCYCLES_TIME_SHARING_HOURS = {
    'Protons only': {
        'Physics':                  2332*0.75,
        'Physics with parallel MD': 1548*0.75,
        'HiRadMat':                 240*0.75,
        'AWAKE with parallel MD':   268.1*0.75,
        'AWAKE':                    739.9*0.75,
        'Dedicated MD':             (25*10 + 5*24)*0.75,# 370*0.75=277.5
        'Scrubbing':                72*0.75, # 54 
        'Thursday MD':              (25*10)*0.75, # 250*0.75 = 187.5
        'LHC filling':              TOTAL_HOURS['Protons only']*0.15,
        'LHC setup':                TOTAL_HOURS['Protons only']*0.10,
    },
    'With ion run': {
        'Physics':                  1852*0.75,
        'Physics with parallel MD': 1356*0.75,
        'HiRadMat':                 240*0.75, # 240*0.75 = 180
        'AWAKE with parallel MD':   265.51*0.75,
        'AWAKE':                    742.49*0.75,
        'Dedicated MD':             (25*10 + 5*24)*0.75,# 370*0.75=277.5
        'Scrubbing':                72*0.75, # 54 
        'Thursday MD':              (25*10)*0.75, # 250*0.75 = 187.5
        'LHC filling':              TOTAL_HOURS['With ion run']*0.15,
        'LHC setup':                TOTAL_HOURS['With ion run']*0.10,
    }
}