import numpy as np
import matplotlib.pyplot as plt
from em_geometry_2d import Circle, plot_field

charge_list = []

# Example 2:
charge_list.append(Circle(charge=+1, radius=0.5, center=[-1,0], number_of_samples=128))
charge_list.append(Circle(charge=-1, radius=0.5, center=[1,0], number_of_samples=128))

xlim = 3
ylim = 3

x = np.linspace(-xlim, +xlim, 128)
y = np.linspace(-ylim, +ylim, 128)

plot_field(charge_list, x, y)


