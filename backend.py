import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class CampoElectrico:
    @staticmethod
    def calcular_campo_puntual(pos, q, punto_observacion):
        k = 8.99e9  # Constante de Coulomb
        r = punto_observacion - pos
        distancia = np.linalg.norm(r)
        if distancia == 0:
            return np.zeros(3)
        return k * q * r / distancia**3
    
    @staticmethod
    def visualizar_cargas(cargas):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        for carga in cargas:
            if isinstance(carga, CargaPuntual):
                ax.scatter(*carga.posicion, color='r', s=100, label="Puntual")
            elif isinstance(carga, CargaLineal):
                ax.plot(*zip(carga.inicio, carga.fin), color='b', label="Lineal")
        
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        plt.legend()
        plt.show()