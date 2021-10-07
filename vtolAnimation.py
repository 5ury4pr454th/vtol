import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import param as p

# plt.ion()

class vtolAnimation:

    def __init__(self) -> None:
        
        self.first = self.first_t = True
        # self.fig, self.ax = plt.subplots(figsize = (10,10))
        self.fig, self.ax = plt.subplots()
        self.handle = dict()

        self.ax.plot([-p.l_g, p.l_g], [0.00,0.00], color = 'black')      
        self.ax.set_xlim(-p.l_g, p.l_g)
        self.ax.set_ylim(-0.5, p.l_s)

    
    def update(self, z, h, theta, target = 0) -> None:

        # updating the drone:

        # under rotation of angle q:
        # (a,b) -> (acosq - bsinq, asinq + bcosq)
        
        # the rotation matrix involved
        # [[cosq, -sinq]
        #  [sinq, cosq]]

        rot_mat = np.array([[np.cos(theta), -np.sin(theta)],
                 [np.sin(theta), np.cos(theta)]])
        stats = np.matmul(rot_mat, p.dr_mat_i.T).T

        # translation by z and h
        stats = np.add(stats, np.array([z, h])) 

        # update animation
        self.draw_drone(stats)
        if target != 0:
            self.draw_target(target)


    def draw_drone(self, stats) -> None:
        
        if self.first == True:
            drone = mpatches.Polygon(np.add(p.dr_mat_i, [p.z_i, p.h_i]), closed = True)
            self.handle['drone_body'] = drone
            self.ax.add_patch(drone)
            self.first = False
        else:
            self.handle['drone_body'].set_xy(stats)

    def draw_target(self, x) -> None:
       
        if self.first_t == True:
            target_body = mpatches.Rectangle([p.target_i, 0], p.l_t, p.w_t, color = 'red', alpha = 0.9)
            self.handle['target'] = target_body
            self.ax.add_patch(self.handle['target'])
            self.first_t = False
        else:
            self.handle['target'].set_x(x - p.l_t/2)