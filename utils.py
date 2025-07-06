import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import e, epsilon_0, pi
""" Mi objetivo es poder visualizar los campos eléctricos y potenciales
    eléctricos generados por distribuciones de cargas comunes
"""
# Atajos:
O = np.array([0, 0, 0])

# 0) Clase común para todas las cargas:
class Charge:
    pass

# 1) Carga puntual
class PointCharge(Charge):
    def __init__ (
            self,
            magnitude: float = 1.0,
            position: np.array = O,
            ):
        self.magnitude = magnitude
        self.position = position
    
    def electric_field(self, X: np.ndarray, Y: np.ndarray, Z: np.ndarray = None):
        """
        Calcula el campo eléctrico generado por una carga puntual.

        Args:
            X (np.ndarray): Meshgrid de coordenadas X.
            Y (np.ndarray): Meshgrid de coordenadas Y.
            Z (np.ndarray, opcional): Meshgrid de coordenadas Z.
                                      Si no se proporciona (o es None),
                                      se asume un cálculo en 2D.

        Returns:
            list: Una lista [Ex, Ey, Ez] con las componentes del campo eléctrico.
                  Si el cálculo es 2D, Ez será un array de ceros.
        """

        # Si es un caso 2D, se define Z de manera auxiliar
        if Z is None or len(self.position) < 3:
            is3d = False 

        # Cálculo de distancia:
        Rx = X - self.position[0]
        Ry = Y - self.position[1]
        Rz = Z - self.position[2] if is3d else np.zeros_like(Rx)

        R_squared = Rx**2 + Ry**2 + Rz**2
        R = np.sqrt(R_squared)
        R_cubed = np.where(R_squared != 0, R_squared * R, 1e-20)  # evitar división por cero

        # Cálculo del campo:
        multiplying_factor = 1/(4*pi*epsilon_0) * self.magnitude / R_cubed

        Ex = multiplying_factor * Rx
        Ey = multiplying_factor * Ry
        Ez = multiplying_factor * Rz if is3d else None

        return [Ex, Ey, Ez]
    

    def electric_potential(
            self,
            X: np.ndarray,
            Y: np.ndarray,
            Z: np.ndarray
            ):
        """
        Calcula el potencial eléctrico generado por una carga puntual (V)

        Args:
            X (np.ndarray): Meshgrid de coordenadas X.
            Y (np.ndarray): Meshgrid de coordenadas Y.
            Z (np.ndarray, opcional): Meshgrid de coordenadas Z.
                                      Si no se proporciona (o es None),
                                      se asume un cálculo en 2D.

        Returns:
            float: V
        """

        # Si es un caso 2D, se define Z de manera auxiliar
        if Z is None or len(self.position) < 3:
            is3d = False 

        # Cálculo de distancia:
        Rx = X - self.position[0]
        Ry = Y - self.position[1]
        Rz = Z - self.position[2] if is3d else np.zeros_like(Rx)

        R_squared = Rx**2 + Ry**2 + Rz**2
        R = np.where(R_squared != 0, np.sqrt(R_squared), 1e-20)  # evitar división por cero

        # Cálculo del campo:
        V = 1 / (4 * pi * epsilon_0) * self.magnitude / R
        return V

# 2) Carga de línea:
class InfiniteLineCharge(Charge):
    def __init__ (
            self,
            charge_density: float = 1.0,
            line_point: np.array = O,
            line_direction: np.array = [1,0,0],
            ):
        self.charge_density = charge_density
        self.line_point = line_point
        self.line_direction = line_direction

    def electric_field(self, X: np.ndarray, Y: np.ndarray, Z: np.ndarray = None):
        """
        Calcula el campo eléctrico generado por una carga de línea.

        Args:
            X (np.ndarray): Meshgrid de coordenadas X.
            Y (np.ndarray): Meshgrid de coordenadas Y.
            Z (np.ndarray, opcional): Meshgrid de coordenadas Z.
                                      Si no se proporciona (o es None),
                                      se asume un cálculo en 2D.

        Returns:
            list: Una lista [Ex, Ey, Ez] con las componentes del campo eléctrico.
                  Si el cálculo es 2D, Ez será un array de ceros.
        """

        # Si es un caso 2D, se define Z de manera auxiliar
        if Z is None or len(self.line_point) < 3 or len(self.line_direction) < 3:
            is3d = False

        # Vector que va desde el punto Q de la línea al punto P = (x,y,z)
        QPx = X - self.line_point[0]
        QPy = Y - self.line_point[1]
        QPz = Z - self.line_point[2] if is3d else np.zeros_like(QPx)

        # Vector guía de la línea:
        vx = self.line_direction[0]
        vy = self.line_direction[1]
        vz = self.line_direction[2] if is3d else 0

        # Vector que va desde el punto más cercano R de la línea al punto P
        QP_dot_v = (QPx * vx) + (QPy * vy) + (QPz * vz)
        magnitude_v_squared = vx**2 + vy**2 + vz**2

        if magnitude_v_squared == 0:
            raise ValueError("El vector de dirección de la línea no puede ser un vector nulo (0,0,0).")
        
        aux = QP_dot_v / magnitude_v_squared

        RPx = QPx - vx * aux
        RPy = QPy - vy * aux
        RPz = QPz - vz * aux

        R_squared = RPx**2 + RPy**2 + RPz**2
        R2 = np.where(R_squared != 0, R_squared, 1e-20)  # evitar división por cero

        # Cálculo del campo:
        multiplying_factor = self.charge_density/(2*pi*epsilon_0*R2)

        Ex = multiplying_factor * RPx
        Ey = multiplying_factor * RPy
        Ez = multiplying_factor * RPz if is3d else None

        return [Ex, Ey, Ez]
    

    def electric_potential(
            self,
            X: np.ndarray,
            Y: np.ndarray,
            Z: np.ndarray
            ):
        """
        Calcula el potencial eléctrico generado por una carga puntual (V)

        Args:
            X (np.ndarray): Meshgrid de coordenadas X.
            Y (np.ndarray): Meshgrid de coordenadas Y.
            Z (np.ndarray, opcional): Meshgrid de coordenadas Z.
                                      Si no se proporciona (o es None),
                                      se asume un cálculo en 2D.

        Returns:
            float: V
        """

        print("Esta función aun no ha sido construida")
        return 0

# Debug::
# print(f"e = {e}")
# print(f"pi = {pi}")
# print(f"epsilon_0 = {epsilon_0}")