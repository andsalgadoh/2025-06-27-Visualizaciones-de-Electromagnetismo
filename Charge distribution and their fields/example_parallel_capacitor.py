import numpy as np
import matplotlib.pyplot as plt
from em_geometry_2d import Line2, plot_field

charge_list = []

charge_list.append(Line2(charge=+1, pos1=[-0.1, -0.4], pos2=[-0.1, +0.4]))
charge_list.append(Line2(charge=-1, pos1=[+0.1, -0.4], pos2=[+0.1, +0.4]))

xlim = 0.5
ylim = 0.6

x = np.linspace(-xlim, +xlim, 128)
y = np.linspace(-ylim, +ylim, 128)

plot_field(charge_list, x, y)