import specs as p
import numpy as np
import matplotlib.pyplot as plt
from f7plot import responsePlotter
from data_plotter import dataPlotter
from signal_gen import SignalGenerator
from vtolAnimation import vtolAnimation
from system_dynamics import systemDynamics
from lateral_control import lateralController
from altitude_control import AltitudeController

# initial state
interim_state = [[0, p.w_b/2, 0], [0, 0, 0]]

# creating signal objects according to F8
reference_signal = SignalGenerator(amplitude=3, frequency=0.08)
reference_signal_2 = SignalGenerator(amplitude=10)
disturbance = SignalGenerator(amplitude=0.25)
disturbance_2 = SignalGenerator(amplitude=0.00)

# creating dynamics and altitude and lateral controllers for question F8
dynamics = systemDynamics(interim_state, p.t_step)
alt_control = AltitudeController(f7 = False)
lat_control = lateralController()

# drawing animation and plotting reference, input and output
plot_engine = responsePlotter()
anim_engine = vtolAnimation()

# setting start time and getting initial state
t = p.t_start
init_state = dynamics.h()
print(f"Initial coordinates: {init_state}")

while t < p.t_end:

    # setting next plotting time
    t_next_plot = t + p.t_plot

    # running dynamics between plotting times
    while t < t_next_plot:

        # defining signal functions
        r = reference_signal.square(t)
        r2 = reference_signal_2.step(t)
        d = disturbance.sin(t)
        d2 = disturbance_2.random(t)
        r += d
        r2 += d2
        
        # get vertical and horizontal coordinates
        z_state = np.array([dynamics.state[0][0], dynamics.state[1][0]])
        h_state = np.array([dynamics.state[0][1], dynamics.state[1][1]])
        
        # update both the controllers controller
        u = lat_control.update(r, z_state)
        u2 = alt_control.update(r2, h_state)

        # updating the dynamics of the system, using controller outputs
        y = dynamics.update(p.u_c(dynamics.state[0][2])*np.array([u2, u2, u])) # does u become u/d?

        # going for next time step
        t = t + p.t_step

    # update animation and data plots for lateral displacement
    anim_engine.update(dynamics.state[0][0], dynamics.state[0][1], dynamics.state[0][2])
    plot_engine.update(t, dynamics.state[0][0], r, u)
    
    # to pause in the middle for better visibility
    plt.pause(0.0005)

final_state = dynamics.h()
print(f"Final coordinates: {final_state}")

plt.pause(2)