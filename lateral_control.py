import numpy as np
import specs as p

class lateralController():
    """A PD controller for controlling the lateral displacement"""
    
    def __init__(self, saturate_at_0 = True) -> None:
        """define manual kp, kd"""
        self.kp = p.kp_z
        self.kd = p.kd_z
        self.kdc = p.kdc_theta
        self.limit = p.max_torque

        # if torque cannot be less than 0
        self.saturate_at_0 = saturate_at_0

    def update(self, z_r, z_data):
        """returns the net torque required, according to reference z"""    
        z = z_data[0]
        z_1 = z_data[1]

        # equilibrium
        theta_e = 0.00
        tau_e = 0.00
        
        # PD controlled, input dc gain for inner loop
        tau_tilde = self.kp*self.kdc*(z_r-z) - self.kd*self.kdc*(z_1)
        
        # net tau
        net_tau = tau_tilde + tau_e

        # saturate
        net_tau = self.saturate(net_tau)
        
        return net_tau

    def saturate(self, u):
        """saturates to limit physics"""
        if abs(u) > self.limit:
            u = self.limit*np.sign(u)
        if self.saturate_at_0 == True and u < 0:
            u = 0.00
        return u