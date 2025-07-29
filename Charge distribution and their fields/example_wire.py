import numpy as np
import matplotlib.pyplot as plt
from em_geometry_2d import Point, plot_field

charge_list = []

k_range = range(0,512)
x_range = np.linspace(-3,3,512)
Q_range = -np.linspace(-1,1,512)
# Example wire:
for k in k_range:
    charge_list.append(Point(charge=Q_range[k], pos=[x_range[k], 1]))
    charge_list.append(Point(charge=Q_range[k], pos=[x_range[k], -1]))

xlim = 3
ylim = 3

x = np.linspace(-xlim, +xlim, 128)
y = np.linspace(-ylim, +ylim, 128)

plot_field(charge_list, x, y)