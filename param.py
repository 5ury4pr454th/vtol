from signal_gen import SignalGenerator
import numpy as np

# mass specs
m_c = 1.53
m_r = m_l = 0.22


# inertia specs
J_c = 0.0049

# body-rotor bridge dimension
d_br = 0.38
h_br = 0.05

# body dimensions
l_b = 0.2
w_b = 0.2

# rotor dimensions
w_r = w_l = 0.25
h_r = h_l = w_b

# target dimensions
l_t = 0.2
w_t = 0.2

# initial conditions
z_i = 0
h_i = w_b/2
theta_i = 0
target_i = -l_t/2
zv_i = 0
hv_i = 0
thetav_i = 0
targetv_i = 0

# ground and sky dimension
l_g = 2
l_s = 10

dr_mat_i = np.array([[-d_br, h_br/2], [-l_b/2, h_br/2], [-l_b/2, w_b/2], [l_b/2, w_b/2], 
          [l_b/2, h_br/2], [d_br, h_br/2], [d_br, -h_br/2], [l_b/2, -h_br/2], [l_b/2, -w_b/2], [-l_b/2, -w_b/2], 
          [-l_b/2, -h_br/2], [-d_br, -h_br/2], [-d_br, h_br/2]])

#simulation conditions
t_start = 0
t_end = 10
t_step = 0.01
t_catch_up = 4
g = 9.8

# damping specs
m_u = 0.121

# coeffs of u with inputs fl,fr
# sin and cos are bound methods

def u_c(t):
    return np.array([-np.sin(t)/(m_c + m_l + m_r), np.cos(t)/(m_c + m_l + m_r), d_br/(J_c + (m_l + m_r)*(d_br**2))])

