import numpy as np
import matplotlib.pyplot as plt
import param as p
from signal_gen import SignalGenerator
from vtolAnimation import vtolAnimation
plt.ion()

# test animation
anim = vtolAnimation()
anim.draw_drone(p.dr_mat_i)
anim.draw_target(0)
t = p.t_start

target_signal = SignalGenerator(amplitude = 0, frequency = np.pi/4)
drone_signal = SignalGenerator(amplitude = 0, frequency = np.pi/4.5, y_offset = -1.00)
rot_signal = SignalGenerator(amplitude = 0, frequency = np.pi/4)
max_height = 2.3

plt.pause(10)

while t < p.t_end:
    
    if t < max_height and t < p.t_catch_up:
        anim.update(drone_signal.sin(t) + (t/p.t_catch_up), t + p.w_b/2, rot_signal.sin(t), target_signal.sin(t))
        target_signal.amplitude = drone_signal.amplitude = t/p.t_catch_up
        rot_signal.amplitude = target_signal.amplitude*np.pi/15

    elif t < p.t_catch_up:
        anim.update(drone_signal.sin(t) + (1.00/p.t_catch_up)*t, max_height + p.w_b/2, rot_signal.sin(t), target_signal.sin(t))
        target_signal.amplitude = drone_signal.amplitude = t/p.t_catch_up
        rot_signal.amplitude = target_signal.amplitude*np.pi/15

    else:
        anim.update(drone_signal.sin(t) + 1, max_height + p.w_b/2 , rot_signal.sin(t), target=target_signal.sin(t))
        target_signal.amplitude = 1 - (t - p.t_catch_up)/(p.t_end - p.t_catch_up)
        drone_signal.amplitude = 1 - (t - p.t_catch_up)/(p.t_end - p.t_catch_up)
        rot_signal.amplitude = np.pi/15 - (t - p.t_catch_up)/(p.t_end - p.t_catch_up)*np.pi/15
        max_height = 2.3 - (t - p.t_catch_up)/(p.t_end - p.t_catch_up)*(2.3- p.w_t)
        
    anim.fig.canvas.draw()
    anim.fig.canvas.update()
    anim.fig.canvas.flush_events()
    
    t += p.t_step

    if p.t_end == t:
        plt.pause(1.2)

