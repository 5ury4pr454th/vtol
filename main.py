# the main script to execute while writing the code

# experiment
from system_dynam import systemDynamics
import numpy as np
import matplotlib.pyplot as plt
import param as p
from signal_gen import SignalGenerator
from vtolAnimation import vtolAnimation
plt.ion()

from time import time

# test animation
anim = vtolAnimation()
anim.draw_drone(p.dr_mat_i) # init position, h above centre

plt.pause(0.2)
t = p.t_start

fr = SignalGenerator(amplitude = 15, frequency=10).constant
fl = SignalGenerator(amplitude = 15, frequency=10).constant
interim_state = [[0, p.w_b/2, 0], [0, 0, 0]]
drone_sys = systemDynamics(interim_state, p.t_step)

while t < p.t_end:
    if drone_sys.state[0][1] - 5.04 > 0.066 :
        final_u = p.u_c(drone_sys.state[0][2])*np.array([0, 0, 0])
    else:
        final_u = p.u_c(drone_sys.state[0][2])*np.array([fl(t) + fr(t), fl(t) + fr(t), fr(t) - fl(t)])

    interim_state = drone_sys.update(final_u) 
    
    print(drone_sys.state[0][1])
    
    anim.update(interim_state[0], interim_state[1], interim_state[2])
    
    anim.fig.canvas.draw()
    anim.fig.canvas.update()
    anim.fig.canvas.flush_events()
    
    t += p.t_step

plt.pause(1)
