import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import e, epsilon_0, pi
import utils

# Crear 2 cargas puntuales y visualizar su campo en 2D
point_charge_list = []
line_charge_list = []

d = 0.4
point_charge_list.append(utils.PointCharge(-1, np.array([0, 0])))
point_charge_list.append(utils.PointCharge(1, np.array([1, 0])))
point_charge_list.append(utils.PointCharge(-1, np.array([0, 1])))
point_charge_list.append(utils.PointCharge(1, np.array([1, 1])))


# Crear cargas lineales:
d2 = 0.5
# line_charge_list.append(utils.InfiniteLineCharge(1, [0 , d2], [1, 0]))
# line_charge_list.append(utils.InfiniteLineCharge(1, [0 , -d2], [1, 0]))


print(f"Number of point charges = {len(point_charge_list)}")

# Definir Meshgrid 2D:
grid_points = 71
grid_size = 2

x_space = np.linspace(-grid_size, grid_size, grid_points)
y_space = np.linspace(-grid_size, grid_size, grid_points)

X, Y = np.meshgrid(x_space, y_space)

print(f"Shape of the meshgrid: {X.shape}")

# Calcular campo eléctrico total (sumatoria)
Ex = np.zeros_like(X)
Ey = np.zeros_like(Y)

for charge in point_charge_list:
    E_differential = charge.electric_field(X, Y)
    # Sumar componentes del campo
    Ex += E_differential[0]
    Ey += E_differential[1]

for charge in line_charge_list:
    E_differential = charge.electric_field(X, Y)
    # Sumar componentes del campo
    Ex += E_differential[0]
    Ey += E_differential[1]

# PLOT:
fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot()

# === Graficar el campo eléctrico ===
E_mag = np.sqrt(Ex**2 + Ey**2)

def squash(x, p=10):
    return x / ((1 + x**p)**(1/p))

normalizing_cap = np.percentile(E_mag, 99)
squashing = squash(E_mag / normalizing_cap)

Ex_squashed = np.multiply(Ex, squashing) / E_mag
Ey_squashed = np.multiply(Ey, squashing) / E_mag
# ax.quiver(X, Y, Ex, Ey, width=0.0010, scale=7e12)
ax.quiver(X, Y, Ex_squashed, Ey_squashed, width=0.0010)

# === Graficar las cargas ===
x = np.zeros(len(point_charge_list))
y = np.zeros(len(point_charge_list))
k = 0

for charge in point_charge_list:
    if isinstance(charge, utils.PointCharge):
        x[k] = charge.position[0]
        y[k] = charge.position[1]
        k += 1

ax.scatter(x, y, s=5, edgecolor='b', label='Carga')

# Etiquetas y título
ax.set_title("Campo eléctrico y distribución de cargas")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend(loc='upper right')

plt.show()

# # AHORA PARA EL POTENCIAL:

# # Inicializar componentes :
# V = np.zeros_like(X)

# for charge in charge_list:

#     # Vector de posición desde carga hacia cada punto del espacio
#     Rx = X - charge.position[0]
#     Ry = Y - charge.position[1]
#     Rz = Z - charge.position[2]
#     print(Rx.shape)

#     V_differential = Charge.scalar_potential(charge, Rx, Ry, Rz)
#     # Sumar componentes del campo
#     V += V_differential

# # PLOT:
# # Flatten the grid and potential arrays
# x_flat = X.flatten()
# y_flat = Y.flatten()
# z_flat = Z.flatten()
# V_flat = V.flatten()

# # Create the plot
# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111, projection='3d')

# # Plot scalar potential using color
# p = ax.scatter(x_flat, y_flat, z_flat, c=V_flat, cmap='viridis', s=5, alpha=0.8)

# # Add a colorbar
# cb = fig.colorbar(p, ax=ax, shrink=0.5)
# cb.set_label('Potential V [V]')

# # Labels
# ax.set_title("Electrostatic Potential in Space")
# ax.set_xlabel("x")
# ax.set_ylabel("y")
# ax.set_zlabel("z")
# plt.show()