import numpy as np

class CargaElectrica:
    """Clase abstracta para todas las cargas."""
    def __init__(self):
        pass

class CargaPuntual(CargaElectrica):
    def __init__(self, pos, mag):
        self.pos = np.array(pos, dtype=float)
        self.mag = float(mag)
    
    def __str__(self):
        return f"Carga Puntual: pos={self.pos}, q={self.mag:.2e} C"

class CargaLineal(CargaElectrica):
    def __init__(self, pos1, pos2, density):
        self.pos1 = np.array(pos1, dtype=float)
        self.pos2 = np.array(pos2, dtype=float)
        self.density = float(density)
    
    def __str__(self):
        return f"Carga Lineal: inicio={self.pos1}, fin={self.pos2}, λ={self.density:.2e} C/m"

def crear_carga(Q):
    """Factory para crear instancias de cargas."""
    tipos = {
        "Puntual": CargaPuntual,
        "Lineal": CargaLineal,
        # Añadir más tipos aquí: "Rectángulo", "Esfera", etc.
    }
    
    clase = tipos.get(Q["nom"])
    if clase is None:
        raise ValueError(f"Tipo de carga desconocido: {Q['nom']}")
        print(**Q)
    return clase(**Q)