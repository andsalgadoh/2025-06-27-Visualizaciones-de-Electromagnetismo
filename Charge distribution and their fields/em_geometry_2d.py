import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import e, epsilon_0, pi
from matplotlib.colors import TwoSlopeNorm

# Atajos:
O = np.array([0, 0])
ke = 1 / (4 * pi * epsilon_0)

class Charge:
    def __init__(
            self,
            charge: float = 1,
            number_of_samples: int = 1
            ):
        self.DeltaQ = charge/number_of_samples
        self.range = range(0, number_of_samples)
        self.init_color(charge)
        self.x = None  # Definir en subclase
        self.y = None  # Definir en subclase

    def init_color(self, Q):
        if Q > 0:
            self.color = "red"
        elif Q < 0:
            self.color = "blue"
        else:
            self.color = "black"

    def potential(self, X: np.meshgrid, Y: np.meshgrid) -> np.meshgrid:
        V = np.zeros_like(X)
        for k in self.range:
            Rx = X - self.x[k]
            Ry = Y - self.y[k]
            r_squared = Rx ** 2 + Ry ** 2
            r = np.where(r_squared > 1e-4, np.sqrt(r_squared), 1e-2)
            V = V + ke * self.DeltaQ / r
        return V

class Point(Charge):
    def __init__(
            self,
            charge: float = 1,
            pos: np.array = O,
            ):
        super().__init__(charge, 1)
        self.label = "Carga puntual"
        t = np.linspace(1, 1, 1)
        self.x = pos[0] * t
        self.y = pos[1] * t

class Line2(Charge):
    def __init__(
            self,
            charge: float = 1,
            pos1: np.array = O,
            pos2: np.array = np.array([1,1]),
            number_of_samples: int = 32,
            ):
        super().__init__(charge, number_of_samples)
        self.label = "Línea de cargas"
        # Parametrización de la línea
        t = np.linspace(0, 1, number_of_samples)
        self.x = t * pos2[0] + (1 - t) * pos1[0]
        self.y = t * pos2[1] + (1 - t) * pos1[1]

class Circle(Charge):
    def __init__(
            self,
            charge: float = 1,
            radius: float = 1,
            center: np.array = O,
            number_of_samples: int = 32
            ):
        super().__init__(charge, number_of_samples)
        self.label = "Círculo de cargas"
        # Parametrización de la línea
        t = np.linspace(0, 2*pi, number_of_samples)
        self.x = radius * np.cos(t) + center[0]
        self.y = radius * np.sin(t) + center[1]

def plot_field(charge_list: Charge, x: np.ndarray, y: np.ndarray) -> None:
    [X, Y] = np.meshgrid(x, y)

    V = np.zeros_like(X)
    for Q in charge_list:
        V = V + Q.potential(X, Y)

    Ey, Ex = np.gradient(-V, y, x)

    # Figura
    fig, ax = plt.subplots(figsize=(8, 6))

    # Potencial como mapa de colores
    norm = TwoSlopeNorm(vmin=V.min(), vcenter=0, vmax=V.max())
    cf = ax.contourf(X, Y, V, levels=100, cmap='RdBu_r', norm=norm)
    cbar = plt.colorbar(cf, ax=ax, label='Potencial eléctrico (V)')

    # Equipotenciales en blanco
    ax.contour(X, Y, V, levels=20, colors='white', linewidths=0.5)

    # Líneas de campo eléctrico
    magnitude = np.sqrt(Ex**2 + Ey**2)
    ax.streamplot(X, Y, Ex, Ey, color=magnitude, linewidth=0.7, cmap='viridis', density=1.5)

    # Carga lineal dibujada sobre el gráfico
    for Q in charge_list:
        ax.plot(Q.x, Q.y, '.-', color=Q.color, linewidth=2, label=Q.label)

    # Detalles del gráfico
    ax.set_title('Potencial y campo eléctrico')
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_aspect('equal')
    ax.legend(loc="lower right")

    plt.tight_layout()
    plt.show()

# TEST ROOM:
if __name__ == "__main__":
    Q1 = Line2(charge=+1, pos1=[0, 0.1], pos2=[0, 0.9])
    Q2 = Line2(charge=-1, pos1=[0.1, 0], pos2=[0.9, 0])

    x = np.linspace(-0.2, 1, 1024)
    y = np.linspace(-0.2, 1, 1024)
    [X, Y] = np.meshgrid(x, y)

    V1 = Q1.potential(X, Y)
    V2 = Q2.potential(X, Y)
    V = V1 + V2

    Ey, Ex = np.gradient(-V, y, x)

    import matplotlib.pyplot as plt
    # Figura
    fig, ax = plt.subplots(figsize=(8, 6))

    # Potencial como mapa de colores
    cf = ax.contourf(X, Y, V, levels=100, cmap='viridis')
    cbar = plt.colorbar(cf, ax=ax, label='Potencial eléctrico (V)')

    # Equipotenciales en blanco
    ax.contour(X, Y, V, levels=20, colors='white', linewidths=0.5)

    # Líneas de campo eléctrico
    magnitude = np.sqrt(Ex**2 + Ey**2)
    ax.streamplot(X, Y, Ex, Ey, color=magnitude, linewidth=0.7, cmap='inferno', density=1.5)

    # Carga lineal dibujada sobre el gráfico
    ax.plot(Q1.x, Q1.y, color=Q1.color, linewidth=2, label='Carga lineal')
    ax.plot(Q2.x, Q2.y, color=Q2.color, linewidth=2, label='Carga lineal')

    # Detalles del gráfico
    ax.set_title('Potencial y campo eléctrico generado por una carga lineal')
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_aspect('equal')
    ax.legend()

    plt.tight_layout()
    plt.show()
