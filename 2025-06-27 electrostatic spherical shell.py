import numpy as np
import matplotlib.pyplot as plt

# Building blocks: Point charge and Electrostatic Field
class Charge:
    # Constant:
    epsilon0 = 8.854e-12
    k = 1/(4*np.pi*epsilon0)

    def __init__ (self,
                  magnitude: float,
                  position = np.array([0, 0, 0]),
                  ):
        self.magnitude = magnitude
        self.position = position
        
    def electric_field(self, Rx, Ry, Rz):
        R_squared = Rx**2 + Ry**2 + Rz**2
        R = np.sqrt(R_squared)
        R_cubed = np.where(R_squared != 0, R_squared * R, 1e-20)  # evitar división por cero
        coeff = Charge.k * self.magnitude / R_cubed
        Ex = coeff * Rx
        Ey = coeff * Ry
        Ez = coeff * Rz
        return [Ex, Ey, Ez]
    
    def scalar_potential(self, Rx, Ry, Rz):
        R_squared = Rx**2 + Ry**2 + Rz**2
        R = np.where(R_squared != 0, np.sqrt(R_squared), 1e-20)  # evitar división por cero
        V = Charge.k * self.magnitude / R
        return V

# Primero definamos dónde crear la carga (coordenadas esféricas)
samples_theta = 50
samples_phi = 30
shell_radius = 1.0
surface_charge_density = 1e-12

rho_samples = shell_radius
theta_samples = np.linspace(0, 2*np.pi, samples_theta)
phi_samples = np.linspace(0, np.pi, samples_phi)

delta_theta = 2*np.pi/samples_theta
delta_phi   = np.pi/samples_phi

# OVERRIDE PREVIOUS STATEMENTS: (Replaces sphere with a single RING)
# samples_phi = 1
# phi_samples = [np.pi/2]
# delta_phi = 1

# Definir lista de cargas puntuales:
charge_list = []

def surface_differential(rho, phi, delta_theta, delta_phi):
    return rho**2 * np.sin(phi) * delta_phi * delta_theta

rho = rho_samples
for theta in theta_samples:
    for phi in phi_samples:

        # Get cartesian coordinates:
        x = rho * np.sin(phi) * np.cos(theta)
        y = rho * np.sin(phi) * np.sin(theta)
        z = rho * np.cos(phi)

        position = np.array([x,y,z])

        # Get charge magnitude:
        magnitude = surface_charge_density * surface_differential(rho, phi, delta_theta, delta_phi)

        # Create a point charge:
        charge_list.append(Charge(magnitude, position))
print(f"Number of point charges = {len(charge_list)}")



# Definir Meshgrid:
grid_points = 10
grid_size = 2
x_space = np.linspace(-grid_size, grid_size, grid_points)
y_space = np.linspace(-grid_size, grid_size, grid_points)
z_space = np.linspace(-grid_size, grid_size, grid_points)
X, Y, Z = np.meshgrid(x_space, y_space, z_space)

print(f"Shape of the meshgrid: {X.shape}")

# Inicializar componentes del campo:
Ex = np.zeros_like(X)
Ey = np.zeros_like(Y)
Ez = np.zeros_like(Z)

for charge in charge_list:

    # Vector de posición desde carga hacia cada punto del espacio
    Rx = X - charge.position[0]
    Ry = Y - charge.position[1]
    Rz = Z - charge.position[2]
    # print(Rx.shape)

    E_differential = Charge.electric_field(charge, Rx, Ry, Rz)
    # Sumar componentes del campo
    Ex += E_differential[0]
    Ey += E_differential[1]
    Ez += E_differential[2]

# PLOT:
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# === Graficar el campo eléctrico ===
step = 1  # submuestreo para claridad visual
ax.quiver(X[::step,::step,::step],
          Y[::step,::step,::step],
          Z[::step,::step,::step],
          Ex[::step,::step,::step],
          Ey[::step,::step,::step],
          Ez[::step,::step,::step],
          length=2, normalize=False)

# === Graficar las cargas ===
x = np.zeros(len(charge_list))
y = np.zeros(len(charge_list))
z = np.zeros(len(charge_list))
k = 0
print(x)
for charge in charge_list:
    x[k] = charge.position[0]
    y[k] = charge.position[1]
    z[k] = charge.position[2]
    k += 1

ax.scatter(x, y, z, s=5, edgecolor='k', label='Carga')

# # === Graficar las cargas ===
# for charge in charge_list:
#     x, y, z = charge.position
#     color = 'red' if charge.magnitude > 0 else 'blue'
#     ax.scatter(x, y, z, c=color, s=10, edgecolor='k', label='Carga' if 'Carga' not in ax.get_legend_handles_labels()[1] else "")

# Etiquetas y título
ax.set_title("Campo eléctrico y distribución de cargas")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.legend(loc='upper right')

plt.show()

# AHORA PARA EL POTENCIAL:

# Inicializar componentes :
V = np.zeros_like(X)

for charge in charge_list:

    # Vector de posición desde carga hacia cada punto del espacio
    Rx = X - charge.position[0]
    Ry = Y - charge.position[1]
    Rz = Z - charge.position[2]
    print(Rx.shape)

    V_differential = Charge.scalar_potential(charge, Rx, Ry, Rz)
    # Sumar componentes del campo
    V += V_differential

# PLOT:
# Flatten the grid and potential arrays
x_flat = X.flatten()
y_flat = Y.flatten()
z_flat = Z.flatten()
V_flat = V.flatten()

# Create the plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot scalar potential using color
p = ax.scatter(x_flat, y_flat, z_flat, c=V_flat, cmap='viridis', s=5, alpha=0.8)

# Add a colorbar
cb = fig.colorbar(p, ax=ax, shrink=0.5)
cb.set_label('Potential V [V]')

# Labels
ax.set_title("Electrostatic Potential in Space")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
plt.show()