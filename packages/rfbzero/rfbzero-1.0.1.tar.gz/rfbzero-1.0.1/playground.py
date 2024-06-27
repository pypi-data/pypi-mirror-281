import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from src.rfbzero.redox_flow_cell import ZeroDModel
from src.rfbzero.degradation import (ChemicalDegradationOxidized, ChemicalDegradationReduced,
                                     AutoOxidation, AutoReduction, MultiDegradationMechanism, Dimerization)
from src.rfbzero.crossover import Crossover
from src.rfbzero.experiment import ConstantCurrent, ConstantCurrentConstantVoltage, ConstantVoltage

###############################################################################
SMALL = 12
MEDIUM = 14
BIG = 16

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.serif": ['Helvetica'],
})
plt.rc('axes', linewidth=1.2, labelsize=10)   # fontsize of the x and y labels (words)
plt.rc('xtick', labelsize=9)                  # fontsize of the tick labels (numbers) #labelsize=MEDIUM
plt.rc('ytick', labelsize=9)                  # fontsize of the tick labels
plt.rc('legend', fontsize=8)                  # legend fontsize
###############################################################################

x_ticks = { "top" : True, "direction" : "in", "minor.visible" : True,
            "major.size" : 4, "major.width" :  1.2, "minor.size" : 2, "minor.width" : 0.5}
y_ticks = x_ticks.copy()
y_ticks["right"] = y_ticks.pop("top")
plt.rc('xtick', **x_ticks)
plt.rc('ytick', **y_ticks)


show_plots = False

# area = 5.0
# for crossover
mem_thick = 183 #/ 10000  # cm, nafion 117
#membrane_c = 5.0 / membrane_thickness
p_ox = 5.0e-6  # cm^2/s
p_red = 2.0e-6  # cm^2/s
##############################

"""
# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.05,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,         # V
                  resistance=1.0,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define degradation mechanisms
deg = ChemicalDegradationReduced(rate_order=1,
                          rate_constant=1e-7,  # 1/s
                          )

# define cycling protocol
protocol = ConstantCurrent(voltage_limit_charge=0.2,       # V
                           voltage_limit_discharge=-0.2,   # V
                           current=0.05,                     # A
                           )

# putting it all together
all_results = protocol.run(cell_model=cell,
                           degradation=deg,
                           duration=1000,   # cycle time to simulate (s)
                           )

print('#1 ' + str(all_results.half_cycle_capacity[:5]))

# should print out: #1 [4.6680000000001325, 9.357999999999945, 9.379999999999972, 9.379999999999972, 9.379999999999972]] # 2024-01-29

if show_plots:
    fig,ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax[0].plot(all_results.step_time, all_results.cell_v)
    ax[1].plot(all_results.step_time, all_results.current)
    ax[0].set_ylabel('Voltage (V)')
    ax[1].set_ylabel('Current (A)')
    ax[1].set_xlabel('Time')
    plt.show()


################################################################################################################
# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.05,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=1.2,         # V
                  resistance=1.0,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define degradation mechanisms
deg = ChemicalDegradationReduced(rate_order=1,
                          rate_constant=1e-6,  # 1/s
                          )

# define cycling protocol
protocol = ConstantCurrentConstantVoltage(voltage_limit_charge=1.5, voltage_limit_discharge=1.0,
                                          current_cutoff_charge=0.005, current_cutoff_discharge=-0.005,
                                          current=0.2)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           degradation=deg,
                           duration=1000,   # cycle time to simulate (s)
                           )
print('#2 ' + str(all_results.half_cycle_capacity[:5]))

# should print out: #2 [4.82247071299548, 9.634222173991992, 9.634679032932628, 9.634169387109623, 9.63418049507715]] #2024-01-29

if show_plots:
    fig,ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax[0].plot(all_results.step_time, all_results.cell_v)
    ax[1].plot(all_results.step_time, all_results.current)
    ax[0].set_ylabel('Voltage (V)')
    ax[1].set_ylabel('Current (A)')
    ax[1].set_xlabel('Time')
    plt.show()


################################################################################################################

# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.05,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,         # V
                  resistance=1.0,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define degradation mechanisms
deg = AutoReduction(rate_constant=5e-5)

protocol = ConstantCurrent(voltage_limit_charge=0.2,       # V
                           voltage_limit_discharge=-0.2,   # V
                           current=0.05,                     # A
                           )

# putting it all together
all_results = protocol.run(cell_model=cell,
                           degradation=deg,
                           duration=1000,   # cycle time to simulate (s)
                           )

print('#3 ' + str(all_results.half_cycle_capacity[:5]))

# should print out: #3 [4.657000000000139, 9.401499999999999, 9.33699999999992, 9.424000000000026, 9.33649999999992] #2024-01-29

if show_plots:
    fig,ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax[0].plot(all_results.step_time, all_results.cell_v)
    ax[1].plot(all_results.step_time, all_results.current)
    ax[0].set_ylabel('Voltage (V)')
    ax[1].set_ylabel('Current (A)')
    ax[1].set_xlabel('Time')
    plt.show()


################################################################################################################

# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.006,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=1.2,         # V
                  resistance=1.0,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define degradation mechanisms
deg = ChemicalDegradationReduced(rate_order=1,
                          rate_constant=1e-4,  # 1/s
                          )

# define cycling protocol
protocol = ConstantCurrentConstantVoltage(voltage_limit_charge=1.5, voltage_limit_discharge=1.0,
                                          current_cutoff_charge=0.005, current_cutoff_discharge=-0.005,
                                          current=0.2)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           degradation=deg,
                           duration=1000,   # cycle time to simulate (s)
                           )
print('#4 ' + str(all_results.half_cycle_capacity[:5]))

# should print out: #4 [4.818723511377226, 9.531124036814706, 9.532069809215667, 9.47981473402909, 9.479563214021956]

if show_plots:
    fig,ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax[0].plot(all_results.step_time, all_results.cell_v)
    ax[1].plot(all_results.step_time, all_results.current)
    ax[0].set_ylabel('Voltage (V)')
    ax[1].set_ylabel('Current (A)')
    ax[1].set_xlabel('Time')
    plt.show()

################################################################################################################

# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.05,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,         # V
                  resistance=1.0,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define degradation mechanisms
cross = Crossover(membrane_thickness=mem_thick, permeability_ox=p_ox, permeability_red=p_red)

protocol = ConstantCurrent(voltage_limit_charge=0.2,       # V
                           voltage_limit_discharge=-0.2,   # V
                           current=0.05,                     # A
                           )

# putting it all together
all_results = protocol.run(cell_model=cell,
                           duration=1000,   # cycle time to simulate (s)
                           crossover=cross,
                           )

print('#5 ' + str(all_results.half_cycle_capacity[:5]))

# should print out: #5 [4.733500000000096, 9.396999999999993, 9.417000000000018, 9.416000000000016, 9.414000000000014]


if show_plots:
    fig,ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax[0].plot(all_results.step_time, all_results.cell_v)
    ax[1].plot(all_results.step_time, all_results.current)
    ax[0].set_ylabel('Voltage (V)')
    ax[1].set_ylabel('Current (A)')
    ax[1].set_xlabel('Time')
    plt.show()

################################################################################################################

# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.05,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,         # V
                  resistance=1.0,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define degradation mechanisms
cross = Crossover(membrane_thickness=mem_thick, permeability_ox=p_ox, permeability_red=p_red)

# define cycling protocol
protocol = ConstantCurrentConstantVoltage(voltage_limit_charge=0.2, voltage_limit_discharge=-0.2,
                                          current_cutoff_charge=0.005, current_cutoff_discharge=-0.005,
                                          current=0.2)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           duration=1000,   # cycle time to simulate (s)
                           crossover=cross,
                           )

print('#6 ' + str(all_results.half_cycle_capacity[:5]))

# should print out: #6 [4.8494641621984576, 9.653421047565272, 9.656042252647266, 9.65565691691222, 9.655896549873965]

if show_plots:
    fig,ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax[0].plot(all_results.step_time, all_results.cell_v)
    ax[1].plot(all_results.step_time, all_results.current)
    ax[0].set_ylabel('Voltage (V)')
    ax[1].set_ylabel('Current (A)')
    ax[1].set_xlabel('Time')
    plt.show()

################################################################################################################

# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.03,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=1.0,         # V
                  resistance=1.0,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define degradation mechanisms
deg = ChemicalDegradationOxidized(rate_order=1,
                          rate_constant=1e-4,  # 1/s
                          )

# define crossover mechanisms
cross = Crossover(membrane_thickness=mem_thick, permeability_ox=p_ox, permeability_red=p_red)

# define cycling protocol
protocol = ConstantCurrentConstantVoltage(voltage_limit_charge=1.4, voltage_limit_discharge=0.9,
                                          current_cutoff_charge=0.005, current_cutoff_discharge=-0.005,
                                          current=0.2)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           duration=1000,   # cycle time to simulate (s)
                           degradation=deg,
                           crossover=cross,
                           )

print('#7 ' + str(all_results.half_cycle_capacity[:5]))

# should print out: #7 [4.837506924451878, 9.339443141765717, 9.138080393025177, 9.169079631500875, 8.97220910612655]

if show_plots:
    fig,ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax[0].plot(all_results.step_time, all_results.cell_v)
    ax[1].plot(all_results.step_time, all_results.current)
    ax[0].set_ylabel('Voltage (V)')
    ax[1].set_ylabel('Current (A)')
    ax[1].set_xlabel('Time')
    plt.show()

################################################################################################################

# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.03,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=1.1,         # V
                  resistance=0.8,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define degradation mechanisms
deg = ChemicalDegradationReduced(rate_order=2,
                          rate_constant=5e-5,  # 1/s
                          )

# define crossover mechanisms
cross = Crossover(membrane_thickness=mem_thick, permeability_ox=p_ox, permeability_red=p_red)

# define cycling protocol
protocol = ConstantCurrentConstantVoltage(voltage_limit_charge=1.45, voltage_limit_discharge=0.8,
                                          current_cutoff_charge=0.005, current_cutoff_discharge=-0.005,
                                          current=0.1)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           duration=1000,   # cycle time to simulate (s)
                           degradation=deg,
                           crossover=cross,
                           )

print('#8 ' + str(all_results.half_cycle_capacity[:5]))

# should print out: #8 [4.861585324597684, 9.66888231425943, 9.667887421644505, 9.667235100275413, 9.666099774954192]

if show_plots:
    fig,ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax[0].plot(all_results.step_time, all_results.cell_v)
    ax[1].plot(all_results.step_time, all_results.current)
    ax[0].set_ylabel('Voltage (V)')
    ax[1].set_ylabel('Current (A)')
    ax[1].set_xlabel('Time')
    plt.show()

################################################################################################################

# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.03,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=1.1,         # V
                  resistance=0.8,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define degradation mechanisms
deg1 = ChemicalDegradationReduced(rate_order=2, rate_constant=5e-5)

deg2 = AutoOxidation(rate_constant=1e-4)

# define cycling protocol
protocol = ConstantCurrentConstantVoltage(voltage_limit_charge=1.45, voltage_limit_discharge=0.8,
                                          current_cutoff_charge=0.005, current_cutoff_discharge=-0.005,
                                          current=0.1)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           duration=1000,   # cycle time to simulate (s)
                           degradation=MultiDegradationMechanism([deg1, deg2]),
                           )

#print('#9 ' + str(all_results.half_cycle_capacity[:5]))

# should print out: #9 [4.859038804309938, 9.599537139653295, 9.693121653071424, 9.599190066866509, 9.692546473602333] #2024-01-29

if show_plots:
    fig,ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax[0].plot(all_results.step_time, all_results.cell_v)
    ax[1].plot(all_results.step_time, all_results.current)
    ax[0].set_ylabel('Voltage (V)')
    ax[1].set_ylabel('Current (A)')
    ax[1].set_xlabel('Time')
    plt.show()

#####################################
# flipped multi of above
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.03,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=1.1,         # V
                  resistance=0.8,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define degradation mechanisms
deg1 = AutoOxidation(rate_constant=1e-4)
deg2 = ChemicalDegradationReduced(rate_order=2, rate_constant=5e-5)

# define cycling protocol
protocol = ConstantCurrentConstantVoltage(voltage_limit_charge=1.45, voltage_limit_discharge=0.8,
                                          current_cutoff_charge=0.005, current_cutoff_discharge=-0.005,
                                          current=0.1)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           duration=1000,   # cycle time to simulate (s)
                           degradation=MultiDegradationMechanism([deg1, deg2]),
                           )

print('#10 ' + str(all_results.half_cycle_capacity[:5]))

# should print out: #10 [4.859038804575711, 9.599537140455313, 9.693121654464113, 9.599190068807443, 9.692546476143121] #2024-01-29
####

# define degradation mechanisms
deg1 = AutoReduction(1e-4)
deg2 = ChemicalDegradationReduced(rate_order=2, rate_constant=5e-5)
deg3 = ChemicalDegradationOxidized(rate_order=2, rate_constant=3e-4)

cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.03,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=1.1,         # V
                  resistance=0.8,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )
# define cycling protocol
protocol = ConstantCurrentConstantVoltage(voltage_limit_charge=1.45, voltage_limit_discharge=0.8,
                                          current_cutoff_charge=0.005, current_cutoff_discharge=-0.005,
                                          current=0.1)
# putting it all together
all_results = protocol.run(cell_model=cell,
                           duration=1000,   # cycle time to simulate (s)
                           degradation=MultiDegradationMechanism([deg1, deg2, deg3]),
                           )
print('#tri-deg 1 ' + str(all_results.half_cycle_capacity[:5]))

#
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.03,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=1.1,         # V
                  resistance=0.8,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define cycling protocol
protocol = ConstantCurrentConstantVoltage(voltage_limit_charge=1.45, voltage_limit_discharge=0.8,
                                          current_cutoff_charge=0.005, current_cutoff_discharge=-0.005,
                                          current=0.1)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           duration=1000,   # cycle time to simulate (s)
                           degradation=MultiDegradationMechanism([deg1, deg3, deg2]),
                           )

print('tri-deg 2 ' + str(all_results.half_cycle_capacity[:5]))
#
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.03,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=1.1,         # V
                  resistance=0.8,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define cycling protocol
protocol = ConstantCurrentConstantVoltage(voltage_limit_charge=1.45, voltage_limit_discharge=0.8,
                                          current_cutoff_charge=0.005, current_cutoff_discharge=-0.005,
                                          current=0.1)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           duration=1000,   # cycle time to simulate (s)
                           degradation=MultiDegradationMechanism([deg2, deg3, deg1]),
                           )

print('tri-deg 3 ' + str(all_results.half_cycle_capacity[:5]))
#
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.03,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=1.1,         # V
                  resistance=0.8,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define cycling protocol
protocol = ConstantCurrentConstantVoltage(voltage_limit_charge=1.45, voltage_limit_discharge=0.8,
                                          current_cutoff_charge=0.005, current_cutoff_discharge=-0.005,
                                          current=0.1)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           duration=1000,   # cycle time to simulate (s)
                           degradation=MultiDegradationMechanism([deg3, deg2, deg1]),
                           )

print('tri-deg 4 ' + str(all_results.half_cycle_capacity[:5]))



## playground for crossover paper
# try perm 1e-8 to 1e-11
# for crossover
#membrane_thickness = 183 / 10000  # cm, nafion 117
#membrane_c = 5.0 / membrane_thickness
p_ox = 5.0e-8  # cm^2/s
p_red = 1.0e-8  # cm^2/s

# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.05,     # L
                  c_ox_cls=0.05,   # M
                  c_red_cls=0.05,  # M
                  c_ox_ncls=0.05,  # M
                  c_red_ncls=0.05,  # M
                  ocv_50_soc=0.0,         # V
                  resistance=0.05,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define degradation mechanisms
cross = Crossover(membrane_thickness=mem_thick, permeability_ox=p_ox, permeability_red=p_red)

# define cycling protocol
protocol = ConstantCurrentConstantVoltage(voltage_limit_charge=0.2, voltage_limit_discharge=-0.2,
                                          current_cutoff_charge=0.005, current_cutoff_discharge=-0.005,
                                          current=0.05)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           duration=30000,   # cycle time to simulate (s)
                           crossover=cross,
                           )
fig,ax = plt.subplots(nrows=3, ncols=1, sharex=True)
tt = [i/3600 for i in all_results.times]
tt_cap = [i/3600 for i in all_results.time_discharge]
ax[0].plot(tt, all_results.cell_v_profile)
ax[1].plot(tt, all_results.current_profile)
ax[2].plot(tt_cap, all_results.discharge_capacity, 'bo--')
ax[0].set_ylabel('Voltage (V)')
ax[1].set_ylabel('Current (A)')
ax[2].set_ylabel('Discharge\ncapacity (C)')
ax[2].set_xlabel('Time (h)')
plt.show()

"""
#
"""
kf = 0.5
kb = kf/80
deg = Dimerization(forward_rate_constant=kf, backward_rate_constant=kb)
deg1 = Dimerization(forward_rate_constant=kf, backward_rate_constant=kb)

#deg1 = Dimerization(forward_rate_constant=0.008, backward_rate_constant=0.0001)
degs = [(None,None), (deg,deg1)]#, deg1]
lb = ['none', 'fast Dimer']#, 'slow dimer']
ss = ['-', '--']

fig,ax = plt.subplots(nrows=5,ncols=1,sharex=True)
for idx,(d,d1) in enumerate(degs):
    cell = ZeroDModel(volume_cls=0.005,     # L
                      volume_ncls=0.01,     # L
                      c_ox_cls=0.02,   # M
                      c_red_cls=0.02,  # M
                      c_ox_ncls=0.02,  # M
                      c_red_ncls=0.02,  # M
                      ocv_50_soc=0.0,         # V
                      resistance=0.5,       # ohms
                      k_0_cls=1e-3,         # cm/s
                      k_0_ncls=1e-3,        # cm/s
                      num_electrons_cls=1,              # electrons
                      num_electrons_ncls=1,             # electrons
                      )

    # define cycling protocol
    protocol = ConstantCurrentConstantVoltage(
        voltage_limit_charge=0.2,
        voltage_limit_discharge=-0.2,
        current_cutoff_charge=0.005,
        current_cutoff_discharge=-0.005,
        current=0.05)

    # putting it all together
    all_results = protocol.run(cell_model=cell,
                               duration=2000,   # cycle time to simulate (s)
                               #degradation=d,
                               cls_degradation=d,
                               ncls_degradation=d1,
                               )
    #print(all_results.discharge_capacity[:5])

    c_red = all_results.c_red_cls_profile
    c_ox = all_results.c_ox_cls_profile
    c_dimer = [(0.04 - r - o)/2 for (r,o) in zip(c_red, c_ox)]
    if idx == 0:
        soc = [(r/0.04)*100 for r in c_red]
    else:
        soc = [((r + d)/0.04)*100 for (r,d) in zip(c_red, c_dimer)]

    ax[0].plot(all_results.times, all_results.cell_v_profile, label=lb[idx], color="b", linestyle=ss[idx])
    ax[1].plot(all_results.times, all_results.current_profile, label=lb[idx], color="k", linestyle=ss[idx])
    ax[2].plot(all_results.times, c_red, label=lb[idx] + ', red', color="r", linestyle=ss[idx])
    ax[2].plot(all_results.times, c_ox, label=lb[idx] + ', ox', color="g", linestyle=ss[idx])
    if idx == 1:
        ax[2].plot(all_results.times, c_dimer, label=lb[idx] + ', dimer', color="tab:brown", linestyle="--")

    ax[3].plot(all_results.times, soc, label=lb[idx], color="k", linestyle=ss[idx])
    ax[4].plot(all_results.time_discharge, all_results.discharge_capacity, 'o', linestyle="--", label=lb[idx])
ax[0].set_ylabel('Voltage (V)')
ax[1].set_ylabel('Current (A)')
ax[2].set_ylabel('Conc. (M)')
ax[3].set_ylabel('SOC (%)')
ax[4].set_ylabel('Discharge\ncapacity (C)')
ax[4].set_xlabel('Time (s)')
ax[0].legend()
ax[1].legend()
ax[2].legend()
ax[3].legend()
ax[4].legend()
plt.show()

#

###  JOSS paper fig 1
# 1. define symmetric cell and electrolyte parameters
cell = ZeroDModel(
    volume_cls=0.005,       # liters
    volume_ncls=0.050,      # liters
    c_ox_cls=0.01,    # molar
    c_red_cls=0.01,   # molar
    c_ox_ncls=0.01,   # molar
    c_red_ncls=0.01,  # molar
    ocv_50_soc=0.0,           # volts
    resistance=0.5,         # ohms
    k_0_cls=1e-3,           # cm/s
    k_0_ncls=1e-3,          # cm/s
)

# 2. define cycling protocol
protocol = ConstantCurrent(
    voltage_limit_charge=0.2,       # volts
    voltage_limit_discharge=-0.2,   # volts
    current=0.1,                    # amps
)

# 3. simulate the cell, via protocol, for 500 seconds
results = protocol.run(cell_model=cell, duration=500)


###  JOSS paper fig 2
# 1. define symmetric cell and electrolyte parameters
cell = ZeroDModel(
    volume_cls=0.005,       # liters
    volume_ncls=0.010,      # liters
    c_ox_cls=0.01,    # molar
    c_red_cls=0.01,   # molar
    c_ox_ncls=0.01,   # molar
    c_red_ncls=0.01,  # molar
    ocv_50_soc=0.0,           # volts
    resistance=0.5,         # ohms
    k_0_cls=1e-3,           # cm/s
    k_0_ncls=1e-3,          # cm/s
)

# 2. define cycling protocol
protocol = ConstantCurrentConstantVoltage(
    voltage_limit_charge=0.2,       # volts
    voltage_limit_discharge=-0.2,   # volts
    current_cutoff_charge=0.005,    # amps
    current_cutoff_discharge=-0.005,    # amps
    current=0.05,                    # amps
)

# 3. chemical degradation
deg = AutoReduction(rate_constant=3e-4)

# 4. simulate the cell, via protocol, for 500 seconds
results = protocol.run(
    cell_model=cell,
    degradation=deg,
    duration=4000)

theory_cap = 96485.33*0.02*0.005

norm_cap_discharge = [(i/theory_cap)*100 for i in results.discharge_cycle_capacity]
norm_cap_charge = [(i/theory_cap)*100 for i in results.charge_cycle_capacity]

soc_c = results.soc_cls
soc_n = results.soc_ncls

ox_fraction_cls = [abs((i - 100.0)/100.0) for i in soc_c]
ox_fraction_ncls = [abs((i - 100.0)/100.0) for i in soc_n]


fig,ax = plt.subplots(nrows=1, ncols=2, figsize=(6,3))
ax[0].plot(results.discharge_cycle_time, norm_cap_discharge, "bo--", label='Oxidation')
ax[0].plot(results.charge_cycle_time, norm_cap_charge, "ko--", label='Reduction')
ax[1].plot(ox_fraction_ncls, ox_fraction_cls, color='r', linewidth=1.5)
# add start point to plot
ax[1].plot(0.5, 0.5, marker='o', color="tab:purple", markersize=7, zorder=3)

ax[0].set_xlabel("Time")
ax[0].set_ylabel("Capacity (%)")
ax[0].set_xticklabels([])
ax[0].set_xticks([])
ax[0].minorticks_off()
ax[0].tick_params(axis='both', top=False, right=False, which='both')


ax[1].set_xlabel("NCLS oxidized fraction")
ax[1].set_ylabel("CLS oxidized fraction")

ax[1].axhline(0.5, linewidth=1.2, linestyle='--', color='k', alpha=0.5)
ax[1].axvline(0.5, linewidth=1.2, linestyle='--', color='k', alpha=0.5)
ax[1].set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
ax[1].set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
ax[1].set_xlim([0,1])
ax[1].set_ylim([0,1])
ax[1].minorticks_off()
ax[1].tick_params(axis='both', top=False, right=False, which='both')
ax[0].legend(frameon=False)
fig.tight_layout()

plt.show()

#save_loc #needs a \ after C = r"C:Users\erico\Desktop\manuscripts\zero_d_model_open_source"
#plt.savefig(save_loc + "\\" + 'fig2a.png', format="png", dpi=300, bbox_inches='tight')
"""

###################################################################################################################


# new testing ConstantVoltage class

"""
# CV #1
# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.05,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,         # V
                  resistance=1.0,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define degradation mechanisms
deg = ChemicalDegradationReduced(rate_order=1,
                          rate_constant=1e-5,  # 1/s
                          )

protocol = ConstantCurrentConstantVoltage(
    voltage_limit_charge=0.2,       # volts
    voltage_limit_discharge=-0.2,   # volts
    current_cutoff_charge=0.005,    # amps
    current_cutoff_discharge=-0.005,    # amps
    current=1.5,                    # amps
)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           degradation=deg,
                           duration=1000,   # cycle time to simulate (s)
                           )

print('#CV1 ' + str(all_results.half_cycle_capacity[:5]))#cycle_capacity[:5]))
"""
# should print out: #CV1 [4.809756988343156, 9.615885449472609, 9.618273796745386, 9.61179635790037, 9.61178778023123]
"""

# CV #2
# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.05,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,         # V
                  resistance=1.0,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define degradation mechanisms
deg = ChemicalDegradationOxidized(rate_order=1,
                          rate_constant=3e-5,  # 1/s
                          )

protocol = ConstantCurrentConstantVoltage(
    voltage_limit_charge=0.2,       # volts
    voltage_limit_discharge=-0.2,   # volts
    current_cutoff_charge=0.005,    # amps
    current_cutoff_discharge=-0.005,    # amps
    current=1.5,                    # amps
)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           degradation=deg,
                           duration=1000,   # cycle time to simulate (s)
                           )

print('#CV2 ' + str(all_results.half_cycle_capacity[:5]))#cycle_capacity[:5]))

# should print out: #CV2 [4.807275339287188, 9.619344783059812, 9.602266737333268, 9.602246790841223, 9.582820031260097]


# CV #3
# define the battery design parameters
cell = ZeroDModel(volume_cls=0.004,     # L
                  volume_ncls=0.05,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,         # V
                  resistance=1.0,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define degradation mechanisms
deg = AutoReduction(rate_constant=1e-4)

protocol = ConstantCurrentConstantVoltage(
    voltage_limit_charge=0.2,       # volts
    voltage_limit_discharge=-0.2,   # volts
    current_cutoff_charge=0.005,    # amps
    current_cutoff_discharge=-0.005,    # amps
    current=1.5,                    # amps
)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           degradation=deg,
                           duration=1000,   # cycle time to simulate (s)
                           )

print('#CV3 ' + str(all_results.half_cycle_capacity[:5]))#cycle_capacity[:5]))

# should print out: #CV3 [3.842876417074232, 7.723318112112475, 7.683408114412163, 7.725285883306576, 7.683453897597165]

#####################################################################################################################
# now same but with ConstantVoltage
##


# ConsV1
# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.05,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,         # V
                  resistance=1.0,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define degradation mechanisms
deg = ChemicalDegradationReduced(rate_order=1,
                          rate_constant=1e-5,  # 1/s
                          )

protocol = ConstantVoltage(
    voltage_limit_charge=0.2,       # volts
    voltage_limit_discharge=-0.2,   # volts
    current_cutoff_charge=0.005,    # amps
    current_cutoff_discharge=-0.005,    # amps
)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           degradation=deg,
                           duration=1000,   # cycle time to simulate (s)
                           )

print('#ConsV1 ' + str(all_results.half_cycle_capacity[:5]))#cycle_capacity[:5]))

# should print out: #ConsV1 [4.809756988343156, 9.615885449472609, 9.618273796745386, 9.61179635790037, 9.61178778023123]
if show_plots:
    fig,ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax[0].plot(all_results.step_time, all_results.cell_v)
    ax[1].plot(all_results.step_time, all_results.current)
    ax[0].set_ylabel('Voltage (V)')
    ax[1].set_ylabel('Current (A)')
    ax[1].set_xlabel('Time')
    plt.show()

# ConsV2
# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.05,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,         # V
                  resistance=1.0,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define degradation mechanisms
deg = ChemicalDegradationOxidized(rate_order=1,
                          rate_constant=3e-5,  # 1/s
                          )

protocol = ConstantVoltage(
    voltage_limit_charge=0.2,       # volts
    voltage_limit_discharge=-0.2,   # volts
    current_cutoff_charge=0.005,    # amps
    current_cutoff_discharge=-0.005,    # amps
)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           degradation=deg,
                           duration=1000,   # cycle time to simulate (s)
                           )

print('#ConsV2 ' + str(all_results.half_cycle_capacity[:5]))#cycle_capacity[:5]))

# should print out: #ConsV2 [4.807275339287188, 9.619344783059812, 9.602266737333268, 9.602246790841223, 9.582820031260097]
if show_plots:
    fig,ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax[0].plot(all_results.step_time, all_results.cell_v)
    ax[1].plot(all_results.step_time, all_results.current)
    ax[0].set_ylabel('Voltage (V)')
    ax[1].set_ylabel('Current (A)')
    ax[1].set_xlabel('Time')
    plt.show()

# ConsV3
# define the battery design parameters
cell = ZeroDModel(volume_cls=0.004,     # L
                  volume_ncls=0.05,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,         # V
                  resistance=1.0,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define degradation mechanisms
deg = AutoReduction(rate_constant=1e-4)

protocol = ConstantVoltage(
    voltage_limit_charge=0.2,       # volts
    voltage_limit_discharge=-0.2,   # volts
    current_cutoff_charge=0.005,    # amps
    current_cutoff_discharge=-0.005,    # amps
)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           degradation=deg,
                           duration=1000,   # cycle time to simulate (s)
                           )

print('#ConsV3 ' + str(all_results.half_cycle_capacity[:5]))#cycle_capacity[:5]))

# should print out: #ConsV3 [3.842876417074232, 7.723318112112475, 7.683408114412163, 7.725285883306576, 7.683453897597165]
if show_plots:
    fig,ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax[0].plot(all_results.step_time, all_results.cell_v)
    ax[1].plot(all_results.step_time, all_results.current)
    ax[0].set_ylabel('Voltage (V)')
    ax[1].set_ylabel('Current (A)')
    ax[1].set_xlabel('Time')
    plt.show()

########################################################################################################################
###########################


# testing assymetric currents 2024-01-10

# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.05,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,         # V
                  resistance=1.0,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define cycling protocol
protocol = ConstantCurrent(voltage_limit_charge=0.2,       # V
                           voltage_limit_discharge=-0.2,   # V
                           current_charge=0.3,                     # A
                           current_discharge=-0.03,
                           )

# putting it all together
all_results = protocol.run(cell_model=cell,
                           duration=1000,   # cycle time to simulate (s)
                           )

print('#asym i #1 ' + str(all_results.half_cycle_capacity[:5]))
# should print out:

if show_plots:
    fig,ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax[0].plot(all_results.step_time, all_results.cell_v)
    ax[1].plot(all_results.step_time, all_results.current)
    ax[0].set_ylabel('Voltage (V)')
    ax[1].set_ylabel('Current (A)')
    ax[1].set_xlabel('Time')
    plt.show()

###################################
## example 2
# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.05,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,         # V
                  resistance=1.0,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define cycling protocol
protocol = ConstantCurrentConstantVoltage(
    voltage_limit_charge=0.2,       # V
    voltage_limit_discharge=-0.2,   # V
    current_charge=0.5,                     # A
    current_discharge=-0.03,
    current_cutoff_charge=0.02,
    current_cutoff_discharge=-0.01
)

# putting it all together
all_results = protocol.run(cell_model=cell,
                           duration=1000,   # cycle time to simulate (s)
                           )

print('#asym i #1 ' + str(all_results.half_cycle_capacity[:5]))
# should print out:

if show_plots:
    fig,ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax[0].plot(all_results.step_time, all_results.cell_v)
    ax[1].plot(all_results.step_time, all_results.current)
    ax[0].set_ylabel('Voltage (V)')
    ax[1].set_ylabel('Current (A)')
    ax[1].set_xlabel('Time')
    plt.show()


##############
# example 2 CV
cell = ZeroDModel(volume_cls=0.005,     # L
                  volume_ncls=0.05,     # L
                  c_ox_cls=0.01,   # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,         # V
                  resistance=1.0,       # ohms
                  k_0_cls=1e-3,         # cm/s
                  k_0_ncls=1e-3,        # cm/s
                  num_electrons_cls=1,              # electrons
                  num_electrons_ncls=1,             # electrons
                  )

# define cycling protocol
protocol = ConstantVoltage(voltage_limit_charge=0.2,       # V
                           voltage_limit_discharge=-0.2,   # V
                           current_cutoff_charge=0.02,
                           current_cutoff_discharge=-0.05,
                           )

# putting it all together
all_results = protocol.run(cell_model=cell,
                           duration=1000,   # cycle time to simulate (s)
                           )

print('#cv ' + str(all_results.half_cycle_capacity[:5]))
# should print out:

if show_plots:
    fig,ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax[0].plot(all_results.step_time, all_results.cell_v)
    ax[1].plot(all_results.step_time, all_results.current)
    ax[0].set_ylabel('Voltage (V)')
    ax[1].set_ylabel('Current (A)')
    ax[1].set_xlabel('Time')
    plt.show()

#


deg = ChemicalDegradationReduced(rate_order=2, rate_constant=10)

cell = ZeroDModel(volume_cls=0.005,  # L
                  volume_ncls=0.03,  # L
                  c_ox_cls=0.01,  # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,  # V
                  resistance=0.8,  # ohms
                  k_0_cls=1e-3,  # cm/s
                  k_0_ncls=1e-3,  # cm/s
                  )
protocol = ConstantCurrent(voltage_limit_charge=0.2,  # V
                           voltage_limit_discharge=-0.2,  # V
                           current=0.05,  # A
                           )
all_results = protocol.run(cell_model=cell,
                           duration=1000,  # cycle time to simulate (s)
                           degradation=deg,
                           )
"""
#
"""
# testing order of degs in multideg
# time increment s
ttt = 0.05

deg_a = Dimerization(forward_rate_constant=0.01, backward_rate_constant=0.001) #AutoOxidation(rate_constant=1e-2)
deg_b = ChemicalDegradationReduced(rate_order=2, rate_constant=5e-1)

multi1 = MultiDegradationMechanism([deg_a, deg_b])

# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,  # L
                  volume_ncls=0.05,  # L
                  c_ox_cls=0.01,  # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,  # V
                  resistance=1.0,  # ohms
                  k_0_cls=1e-3,  # cm/s
                  k_0_ncls=1e-3,  # cm/s
                  num_electrons_cls=1,  # electrons
                  num_electrons_ncls=1,  # electrons
                  time_step=ttt,
                  )

# define cycling protocol
# protocol = ConstantCurrent(voltage_limit_charge=0.2,       # V
#                            voltage_limit_discharge=-0.2,   # V
#                            current_charge=0.05,                     # A
#                            current_discharge=-0.05,
#                            )
protocol = ConstantVoltage(voltage_limit_charge=0.2,       # V
                           voltage_limit_discharge=-0.2,   # V
                           current_cutoff_charge=0.02,
                           current_cutoff_discharge=-0.05,
                           )

# putting it all together
all_results = protocol.run(cell_model=cell,
                           degradation=multi1,
                           duration=1000,   # cycle time to simulate (s)
                           )

print('auto then chemdeg ' + str(all_results.half_cycle_capacity[:5]))

# 2
multi2 = MultiDegradationMechanism([deg_b, deg_a])

# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,  # L
                  volume_ncls=0.05,  # L
                  c_ox_cls=0.01,  # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,  # V
                  resistance=1.0,  # ohms
                  k_0_cls=1e-3,  # cm/s
                  k_0_ncls=1e-3,  # cm/s
                  num_electrons_cls=1,  # electrons
                  num_electrons_ncls=1,  # electrons
                  time_step=ttt,
                  )

# define cycling protocol
# protocol = ConstantCurrent(voltage_limit_charge=0.2,       # V
#                            voltage_limit_discharge=-0.2,   # V
#                            current_charge=0.05,                     # A
#                            current_discharge=-0.05,
#                            )
protocol = ConstantCurrentConstantVoltage(
    voltage_limit_charge=0.2,       # V
    voltage_limit_discharge=-0.2,   # V
    current_charge=0.5,                     # A
    current_discharge=-0.03,
    current_cutoff_charge=0.02,
    current_cutoff_discharge=-0.01
)
# protocol = ConstantVoltage(voltage_limit_charge=0.2,       # V
#                            voltage_limit_discharge=-0.2,   # V
#                            current_cutoff_charge=0.02,
#                            current_cutoff_discharge=-0.05,
#                            )

# putting it all together
all_results = protocol.run(cell_model=cell,
                           degradation=multi2,
                           duration=1000,   # cycle time to simulate (s)
                           )

print('chemdeg then auto ' + str(all_results.half_cycle_capacity[:5]))

fig,ax = plt.subplots(nrows=3, ncols=1, sharex=True)
ax[0].plot(all_results.step_time, all_results.cell_v)
ax[1].plot(all_results.step_time, all_results.current)
ax[2].plot(all_results.step_time, all_results.total_overpotential)
ax[0].set_ylabel('Voltage (V)')
ax[1].set_ylabel('Current (A)')
ax[2].set_xlabel('Time')
plt.show()
"""
#####

"""
# 2024-01-29, domain error bug ??
degradation1 = AutoOxidation(rate_constant=0.1)
degradation2 = ChemicalDegradationReduced(rate_order=1, rate_constant=0.1)
mechanism = MultiDegradationMechanism([degradation1, degradation2])

cell = ZeroDModel(volume_cls=0.005,  # L
                  volume_ncls=0.05,  # L
                  c_ox_cls=0.01,  # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,  # V
                  resistance=1.0,  # ohms
                  k_0_cls=1e-3,  # cm/s
                  k_0_ncls=1e-3,  # cm/s
                  num_electrons_cls=1,  # electrons
                  num_electrons_ncls=1,  # electrons
                  )

protocol = ConstantCurrent(voltage_limit_charge=0.2,  # V
                           voltage_limit_discharge=-0.2,  # V
                           current=0.05,  # A
                           )

all_results = protocol.run(cell_model=cell, duration=1000, degradation=mechanism)

print('test: ' + str(all_results.half_cycle_capacity[:5]))

# test c_products

deg_a = Dimerization(forward_rate_constant=0.01, backward_rate_constant=0.001)
deg_b = ChemicalDegradationReduced(rate_order=2, rate_constant=5e-2)

multi1 = MultiDegradationMechanism([deg_a, deg_b])

# define the battery design parameters
cell = ZeroDModel(volume_cls=0.005,  # L
                  volume_ncls=0.05,  # L
                  c_ox_cls=0.01,  # M
                  c_red_cls=0.01,  # M
                  c_ox_ncls=0.01,  # M
                  c_red_ncls=0.01,  # M
                  ocv_50_soc=0.0,  # V
                  resistance=1.0,  # ohms
                  k_0_cls=1e-3,  # cm/s
                  k_0_ncls=1e-3,  # cm/s
                  time_step=0.05,
                  )

protocol = ConstantVoltage(voltage_limit_charge=0.2,       # V
                           voltage_limit_discharge=-0.2,   # V
                           current_cutoff_charge=0.02,
                           current_cutoff_discharge=-0.05,
                           )

# putting it all together
all_results = protocol.run(cell_model=cell,
                           degradation=multi1,
                           duration=3000,   # cycle time to simulate (s)
                           )

print('auto then chemdeg ' + str(all_results.half_cycle_capacity[:5]))
print(all_results.c_products_cls['c_dimer'][:5])

##
fig,ax = plt.subplots(nrows=2,ncols=1,sharex=True)
ax[0].plot(all_results.step_time, all_results.cell_v)
ax[1].plot(all_results.step_time, all_results.c_products_cls['c_dimer'], 'b')
ax[1].plot(all_results.step_time, all_results.c_products_ncls['c_dimer'], 'g')
plt.show()
"""

# chap 5 fig 1
"""
fig,ax = plt.subplots(nrows=6,ncols=1,sharex=True, figsize=(5,6))

ch = 0.2
disch = -0.2
prots = [ConstantCurrent(voltage_limit_charge=ch,voltage_limit_discharge=disch,current=0.1),
         ConstantCurrentConstantVoltage(voltage_limit_charge=ch,voltage_limit_discharge=disch,current_cutoff=0.005,current=0.1),
         ConstantVoltage(voltage_limit_charge=ch,voltage_limit_discharge=disch,current_cutoff=0.005)]

for idx,pro in enumerate(prots):
    cell = ZeroDModel(
        volume_cls=0.005,  # liters
        volume_ncls=0.050,  # liters
        c_ox_cls=0.01,  # molar
        c_red_cls=0.01,  # molar
        c_ox_ncls=0.01,  # molar
        c_red_ncls=0.01,  # molar
        ocv_50_soc=0.0,  # volts
        resistance=1.0,  # ohms
        k_0_cls=1e-3,  # cm/sec
        k_0_ncls=1e-3,  # cm/sec
    )

    results = pro.run(cell_model=cell,duration=500)

    ax[idx*2].plot(results.step_time, results.cell_v, color='k')
    ax[(idx*2)+1].plot(results.step_time, results.current, color='r')
for i in [0,2,4]:
    ax[i].set_ylabel('Voltage (V)', fontsize=7)
    ax[i+1].set_ylabel('Current (A)',fontsize=7)
    ax[i].set_ylim(disch*1.2, ch*1.2)
    ax[i+1].set_ylim(-0.255, 0.255)
    ax[i].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax[i+1].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# ax[2].set_ylabel('Voltage (V)')
# ax[3].set_ylabel('Current (A)')
# ax[4].set_ylabel('Voltage (V)')
# ax[5].set_ylabel('Current (A)')
ax[5].set_xlabel('Time')# (s)')
ax[5].set_xlim(0,500)
ax[5].set_xticklabels([])
fig.tight_layout()
#plt.show()
#save_loc = # add \ after C r"C:Users\erico\Desktop\manuscripts\zero_d_model_open_source\thesis_specific_figs"
#plt.savefig(save_loc + "\\" + 'fig_protocols.png', format="png", dpi=300, bbox_inches='tight')
#plt.savefig(save_loc + "\\" + 'fig_protocols.pdf', format="pdf", dpi=300, bbox_inches='tight')

"""

# chap 5 fig 4, chem deg
# 1. setup flow cell
"""
cell = ZeroDModel(
    volume_cls=0.005,   # liters
    volume_ncls=0.010,  # liters
    c_ox_cls=0.01,      # molar
    c_red_cls=0.01,     # molar
    c_ox_ncls=0.01,     # molar
    c_red_ncls=0.01,    # molar
    ocv_50_soc=1.0,     # volts
    resistance=1.0,     # ohms
    k_0_cls=1e-3,       # cm/sec
    k_0_ncls=1e-3,      # cm/sec
)

# 2. declare cycling protocol
cccv_protocol = ConstantCurrentConstantVoltage(
    voltage_limit_charge=1.2,     # volts
    voltage_limit_discharge=0.8,  # volts
    current_cutoff=0.005,         # amps
    current=0.1,                  # amps
)

# 3. declare degradation mechanism
chem_deg = ChemicalDegradationReduced(
    rate_order=1,        # declares a first order mechanism
    rate_constant=1e-3,  # first order rate constant, 1/sec
)

# 4. put it all together
results = cccv_protocol.run(
    cell_model=cell,
    degradation=chem_deg,  # include degradation mechanism
    duration=1000
)

# plot voltage, current, and concentration profiles for duration of simulation
fig, ax = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=(6,4.5))
sim_time = results.step_time
ax[0].plot(sim_time, results.cell_v, color='k')
ax[1].plot(sim_time, results.current, color='r')
ax[2].plot(sim_time, results.c_ox_cls, color='b', label='ox')
ax[2].plot(sim_time, results.c_red_cls, color='r', label='red')
ax[3].plot(results.discharge_cycle_time, results.discharge_cycle_capacity, 'bo--', label='ox')
ax[3].plot(results.charge_cycle_time, results.charge_cycle_capacity, 'ro--', label='red')
ax[0].set_ylabel('Voltage (V)', fontsize=7)
ax[1].set_ylabel('Current (A)', fontsize=7)
ax[2].set_ylabel('Concentration (M)', fontsize=7)
ax[2].legend(frameon=False, ncols=2)
ax[3].set_ylabel('Capacity (C)', fontsize=7)
ax[3].legend(frameon=False, ncols=2)
ax[3].set_xlabel('Time (s)')
ax[3].set_ylim(4, 9.5)
ax[3].set_xlim(0,1000)
fig.tight_layout()
#plt.show()
#save_loc = # need \ after : r"C:Users\erico\Desktop\manuscripts\zero_d_model_open_source\thesis_specific_figs"
#plt.savefig(save_loc + "\\" + 'fig_chem_deg.png', format="png", dpi=300, bbox_inches='tight')
#lt.savefig(save_loc + "\\" + 'fig_chem_deg.pdf', format="pdf", dpi=300, bbox_inches='tight')
"""

# chap5 fig 5
"""
# 1. setup flow cell
cell = ZeroDModel(
    volume_cls=0.005,   # liters
    volume_ncls=0.010,  # liters
    c_ox_cls=0.01,      # molar
    c_red_cls=0.01,     # molar
    c_ox_ncls=0.01,     # molar
    c_red_ncls=0.01,    # molar
    ocv_50_soc=1.0,     # volts
    resistance=1.0,     # ohms
    k_0_cls=1e-3,       # cm/sec
    k_0_ncls=1e-3,      # cm/sec
)

# 2. declare cycling protocol
cv_protocol = ConstantVoltage(
    voltage_limit_charge=1.2,     # volts
    voltage_limit_discharge=0.8,  # volts
    current_cutoff=0.005,         # amps
)

# 3. declare CLS degradation mechanism
auto_red_cls = AutoReduction(rate_constant=2e-4)

# 4. declare NCLS degradation mechanism
chem_deg_ncls = ChemicalDegradationOxidized(
    rate_order=2,        # declares a second order mechanism
    rate_constant=2e-3,  # second order rate constant, 1/(M*sec)
)

# 5. put it all together
results = cv_protocol.run(
    cell_model=cell,
    cls_degradation=auto_red_cls,    # include CLS degradation mechanism
    ncls_degradation=chem_deg_ncls,  # include NCLS degradation mechanism
    duration=1000
)

# plot voltage, current, and concentration profiles for duration of simulation
fig, ax = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=(6,4.5))
sim_time = results.step_time
ax[0].plot(sim_time, results.cell_v, color='k')
ax[1].plot(sim_time, results.current, color='r')
ax[2].plot(sim_time, results.c_ox_cls, color='b', label='ox')
ax[2].plot(sim_time, results.c_red_cls, color='r', label='red')
ax[3].plot(sim_time, results.c_ox_ncls, color='b', label='ox')
ax[3].plot(sim_time, results.c_red_ncls, color='r', label='red')
ax[0].set_ylabel('Voltage (V)', fontsize=7)
ax[1].set_ylabel('Current (A)', fontsize=7)
ax[2].set_ylabel('CLS', fontsize=7)
ax[2].legend(frameon=False, ncols=2)
ax[2].set_ylim([0,0.026])
ax[3].set_ylabel('NCLS', fontsize=7)
fig.text(0.01, 0.29, 'Concentration (M)', va='center', rotation='vertical', fontsize=8)
#ax[3].yaxis.set_label_position("right")
ax[3].set_ylim([0,0.026])
ax[3].set_xlabel('Time (s)')
ax[3].set_xlim(0,1000)
ax[3].legend(frameon=False, ncols=2)
fig.tight_layout()
#plt.show()

#save_loc = needs \ r"C:Users\erico\Desktop\manuscripts\zero_d_model_open_source\thesis_specific_figs"
#plt.savefig(save_loc + "\\" + 'fig_chem_deg2.png', format="png", dpi=300, bbox_inches='tight')
#plt.savefig(save_loc + "\\" + 'fig_chem_deg2.pdf', format="pdf", dpi=300, bbox_inches='tight')
"""
# chap5 fig 6
"""
# 1. setup flow cell
cell = ZeroDModel(
    volume_cls=0.005,   # liters
    volume_ncls=0.010,  # liters
    c_ox_cls=0.01,      # molar
    c_red_cls=0.01,     # molar
    c_ox_ncls=0.01,     # molar
    c_red_ncls=0.01,    # molar
    ocv_50_soc=0.0,     # volts
    resistance=1.5,     # ohms
    k_0_cls=1e-3,       # cm/sec
    k_0_ncls=1e-3,      # cm/sec
)

# 2. declare cycling protocol
cccv_protocol = ConstantCurrentConstantVoltage(
    voltage_limit_charge=0.2,         # volts
    voltage_limit_discharge=-0.2,     # volts
    current_charge=0.1,               # amps
    current_discharge=-0.05,          # amps
    current_cutoff_charge=0.050,      # amps
    current_cutoff_discharge=-0.025,  # amps
)

# 3. put it all together
results = cccv_protocol.run(cell_model=cell, duration=700)

# plot voltage, current, and concentration profiles for duration of simulation
fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(6,4))
sim_time = results.step_time
ax[0].plot(sim_time, results.cell_v, color='k')
ax[1].plot(sim_time, results.current, color='r')
ax[0].set_ylabel('Voltage (V)')
ax[1].set_ylabel('Current (A)')
ax[1].set_xlabel('Time (s)')
ax[1].set_ylim(-0.11,0.11)
ax[1].set_xlim(0,700)
#plt.show()

#save_loc = needs \ r"C:Users\erico\Desktop\manuscripts\zero_d_model_open_source\thesis_specific_figs"
#plt.savefig(save_loc + "\\" + 'fig_asym_currents.png', format="png", dpi=300, bbox_inches='tight')
#plt.savefig(save_loc + "\\" + 'fig_asym_currents.pdf', format="pdf", dpi=300, bbox_inches='tight')
"""
# chap 5 fig 7
"""
# 1. setup flow cell
cell = ZeroDModel(
    volume_cls=0.005,   # liters
    volume_ncls=0.010,  # liters
    c_ox_cls=0.01,      # molar
    c_red_cls=0.01,     # molar
    c_ox_ncls=0.01,     # molar
    c_red_ncls=0.01,    # molar
    ocv_50_soc=1.0,     # volts
    resistance=1.5,     # ohms
    k_0_cls=1e-3,       # cm/sec
    k_0_ncls=1e-3,      # cm/sec
)

# 2. declare cycling protocol
cccv_protocol = ConstantCurrentConstantVoltage(
    voltage_limit_charge=1.2,         # volts
    voltage_limit_discharge=0.8,      # volts
    current_charge=0.1,               # amps
    current_discharge=-0.05,           # amps
    current_cutoff_charge=0.005,      # amps
    current_cutoff_discharge=-0.010,  # amps
)

# 3a. declare CLS degradation mechanism
chem_deg_cls = ChemicalDegradationReduced(rate_order=1, rate_constant=4e-4)

# 3b. declare another CLS degradation mechanism
auto_red_cls = AutoReduction(rate_constant=2e-4)

# 3c. combine both CLS mechanisms into a stacked MultiDegradationMechanism
cls_deg = MultiDegradationMechanism([chem_deg_cls, auto_red_cls])

# 4. declare NCLS degradation mechanism
chem_deg_ncls = ChemicalDegradationOxidized(rate_order=2, rate_constant=3e-4)

# 5. put it all together
results = cccv_protocol.run(
    cell_model=cell,
    cls_degradation=cls_deg,         # include CLS degradation mechanism
    ncls_degradation=chem_deg_ncls,  # include NCLS degradation mechanism
    duration=2000,
)

fig, ax = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=(6,5))
sim_time = results.step_time
ax[0].plot(sim_time, results.cell_v, color='k')
ax[1].plot(sim_time, results.current, color='r')
ax[2].plot(sim_time, results.c_ox_cls, color='b', label='ox')
ax[2].plot(sim_time, results.c_red_cls, color='r', label='red')
ax[3].plot(results.discharge_cycle_time, results.discharge_cycle_capacity, 'bo--', label='ox')
ax[3].plot(results.charge_cycle_time, results.charge_cycle_capacity, 'ro--', label='red')
ax[0].set_ylabel('Voltage (V)', fontsize=7)
ax[1].set_ylabel('Current (A)', fontsize=7)
ax[2].set_ylabel('CLS\nConcentration (M)', fontsize=7)
ax[2].legend(frameon=False, ncols=2)
ax[3].set_ylabel('Capacity (C)', fontsize=7)
ax[3].legend(frameon=False, ncols=2)
ax[3].set_xlabel('Time (s)')
ax[1].set_ylim(-0.11,0.11)
ax[3].set_ylim(4,10)
ax[3].set_xlim(0,2000)
#plt.show()

#save_loc = need \ r"C:Users\erico\Desktop\manuscripts\zero_d_model_open_source\thesis_specific_figs"
#plt.savefig(save_loc + "\\" + 'fig_everything_batt.png', format="png", dpi=300, bbox_inches='tight')
#plt.savefig(save_loc + "\\" + 'fig_everything_batt.pdf', format="pdf", dpi=300, bbox_inches='tight')
"""

# 1. setup flow cell
cell = ZeroDModel(
    volume_cls=0.005,   # liters
    volume_ncls=0.010,  # liters
    c_ox_cls=0.01,      # molar
    c_red_cls=0.01,     # molar
    c_ox_ncls=0.01,     # molar
    c_red_ncls=0.01,    # molar
    ocv_50_soc=0.0,     # volts
    resistance=1.0,     # ohms
    k_0_cls=1e-3,       # cm/sec
    k_0_ncls=1e-3,      # cm/sec
)

# 2. declare cycling protocol
cccv_protocol = ConstantCurrentConstantVoltage(
    voltage_limit_charge=0.2,      # volts
    voltage_limit_discharge=-0.2,  # volts
    current_cutoff=0.005,          # amps
    current=0.1,                   # amps
)

# 3. declare degradation mechanism
chem_deg = ChemicalDegradationReduced(rate_order=1, rate_constant=1e-4)

# 4. declare crossover mechanism
cross = Crossover(
    membrane_thickness=50,  # microns
    permeability_ox=1e-7,   # cm^2/sec
    permeability_red=5e-7,  # cm^2/sec
)

# 5. put it all together
results = cccv_protocol.run(
    cell_model=cell,
    degradation=chem_deg,  # include degradation mechanism
    crossover=cross,       # include crossover mechanism
    duration=1000,
)

# plot voltage, current, and concentration profiles for duration of simulation
fig, ax = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(6,4.5))
sim_time = results.step_time
ax[0].plot(sim_time, results.cell_v, color='k')
ax[1].plot(sim_time, results.current, color='r')
ax[2].plot(sim_time, [i*1e6 for i in results.crossed_ox_mols], color='b', label='ox')
ax[2].plot(sim_time, [i*1e6 for i in results.crossed_red_mols], color='r', label='red')
ax[0].set_ylabel('Voltage (V)')
ax[1].set_ylabel('Current (A)')
ax[2].set_ylabel('Species crossing at\n timestep ($\mu$mols)')
ax[2].set_xlabel('Time (s)')
ax[2].legend(frameon=False)
ax[2].set_xlim(0,1000)
plt.show()

#save_loc = need \ r"C:Users\erico\Desktop\manuscripts\zero_d_model_open_source\thesis_specific_figs"
#plt.savefig(save_loc + "\\" + 'fig_basic_cross.png', format="png", dpi=300, bbox_inches='tight')
#plt.savefig(save_loc + "\\" + 'fig_basic_cross.pdf', format="pdf", dpi=300, bbox_inches='tight')
