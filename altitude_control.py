import numpy as np
import specs as p

class AltitudeController():
    
    """A PD controller for controlling the altitude"""
    
    def __init__(self, f7 = True, saturate_at_0 = True) -> None:
        """define manual kp, kd"""

        # different kp, kd for Question F7
        if f7:
            self.kp = p.f7kp_h
            self.kd = p.f7kd_h

        else:
            self.kp = p.kp_h
            self.kd = p.kd_h

        self.limit = p.max_force
        self.saturate_at_0 = saturate_at_0

    def update(self, h_r, h_data):
        """returns the net force required, according to reference h"""    
        h = h_data[0]
        h_1 = h_data[1]

        # equilibrium
        theta_e = 0.00
        F_e = (p.m_c + p.m_r + p.m_l)*p.g*np.cos(theta_e)
        
        # PD controlled
        F_tilde = self.kp*(h_r-h) - self.kd*(h_1)
        
        # net force
        net_F = F_tilde + F_e

        # saturate
        net_F = self.saturate(net_F)
        
        return net_F

    def saturate(self, u):
        """saturates to limit physics"""
        if abs(u) > self.limit:
            u = self.limit*np.sign(u)
        if self.saturate_at_0 == True and u < 0:
            u = 0.00
        return u