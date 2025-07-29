import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QComboBox, QLineEdit, QLabel, QGroupBox,
                             QListWidget, QListWidgetItem, QSplitter,
                             QSpinBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from intermediate import CargaPuntual, CargaLineal, crear_carga

class GeoElectricApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Campo Eléctrico 2D")
        self.setGeometry(100, 100, 1000, 800)

        # Configuración del meshgrid (inicial)
        self.meshgrid_config = {
            "x_min": -5.0,
            "x_max": 5.0,
            "y_min": -5.0,
            "y_max": 5.0,
            "points": 10
        }

        self.charges = []
        self.selected_charge = None  # Para mover cargas con el mouse

        # Widget principal
        splitter = QSplitter(Qt.Horizontal)

        # --- Panel izquierdo ---
        left_panel = QWidget()
        left_layout = QVBoxLayout()

        # Lista de cargas
        self.lista_cargas = QListWidget()
        self.lista_cargas.setStyleSheet("""
            QListWidget {
                font-size: 12px;
                background-color: #f5f5f5;
            }
            QListWidget::item {
                border-bottom: 1px solid #ddd;
                padding: 5px;
            }
        """)

        # Configuración del meshgrid
        mesh_group = QGroupBox("Configuración del Meshgrid")
        mesh_layout = QVBoxLayout()

        self.x_min_spin = QDoubleSpinBox()
        self.x_min_spin.setRange(-50, 50)
        self.x_min_spin.setValue(-5.0)
        self.x_min_spin.setPrefix("x min: ")

        self.x_max_spin = QDoubleSpinBox()
        self.x_max_spin.setRange(-50, 50)
        self.x_max_spin.setValue(5.0)
        self.x_max_spin.setPrefix("x max: ")

        self.y_min_spin = QDoubleSpinBox()
        self.y_min_spin.setRange(-50, 50)
        self.y_min_spin.setValue(-5.0)
        self.y_min_spin.setPrefix("y min: ")

        self.y_max_spin = QDoubleSpinBox()
        self.y_max_spin.setRange(-50, 50)
        self.y_max_spin.setValue(5.0)
        self.y_max_spin.setPrefix("y max: ")

        self.points_spin = QSpinBox()
        self.points_spin.setRange(5, 50)
        self.points_spin.setValue(10)
        self.points_spin.setPrefix("Puntos: ")

        mesh_layout.addWidget(self.x_min_spin)
        mesh_layout.addWidget(self.x_max_spin)
        mesh_layout.addWidget(self.y_min_spin)
        mesh_layout.addWidget(self.y_max_spin)
        mesh_layout.addWidget(self.points_spin)
        mesh_group.setLayout(mesh_layout)

        # Botón para actualizar meshgrid
        self.boton_actualizar_meshgrid = QPushButton("🔄 Actualizar Meshgrid")
        self.boton_actualizar_meshgrid.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.boton_actualizar_meshgrid.clicked.connect(self.actualizar_meshgrid)

        # Botón de simulación
        self.boton_simular = QPushButton("⚡ Simular Campo Eléctrico")
        self.boton_simular.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        self.boton_simular.clicked.connect(self.simular_campo)

        left_layout.addWidget(self.lista_cargas)
        left_layout.addWidget(mesh_group)
        left_layout.addWidget(self.boton_actualizar_meshgrid)  # Nuevo botón
        left_layout.addWidget(self.boton_simular)
        left_panel.setLayout(left_layout)
        splitter.addWidget(left_panel)

        # --- Panel central ---
        formulario_widget = QWidget()
        formulario_layout = QVBoxLayout()

        grupo_carga = QGroupBox("Añadir Nueva Carga")
        layout_carga = QVBoxLayout()

        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Puntual", "Recta"])
        self.combo_tipo.currentTextChanged.connect(self.actualizar_campos)

        self.campos_posicion = QVBoxLayout()
        self.input_magnitud = QLineEdit()
        self.input_magnitud.setPlaceholderText("Ej: 1.6e-19 o -5.0e-9")

        self.boton_anadir = QPushButton("➕ Añadir Carga")
        self.boton_anadir.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.boton_anadir.clicked.connect(self.anadir_carga)

        layout_carga.addWidget(QLabel("Tipo de carga:"))
        layout_carga.addWidget(self.combo_tipo)
        layout_carga.addLayout(self.campos_posicion)
        layout_carga.addWidget(QLabel("Magnitud (C):"))
        layout_carga.addWidget(self.input_magnitud)
        layout_carga.addWidget(self.boton_anadir)
        grupo_carga.setLayout(layout_carga)

        formulario_layout.addWidget(grupo_carga)
        formulario_widget.setLayout(formulario_layout)
        splitter.addWidget(formulario_widget)

        # --- Panel derecho: Gráfico ---
        self.figura = Figure(figsize=(6, 6))
        self.canvas = FigureCanvas(self.figura)
        self.ax = self.figura.add_subplot(111)
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.set_aspect('equal')
        self.ax.set_xlabel("X (m)")
        self.ax.set_ylabel("Y (m)")
        self.ax.set_title("Visualización de Cargas y Meshgrid")
        splitter.addWidget(self.canvas)

        splitter.setSizes([300, 300, 600])
        self.setCentralWidget(splitter)

        self.actualizar_campos()
        self.actualizar_meshgrid()

        # Conectar eventos de mouse
        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
        self.canvas.mpl_connect("button_release_event", self.on_release)

    def actualizar_campos(self):
        for i in reversed(range(self.campos_posicion.count())):
            widget = self.campos_posicion.itemAt(i).widget()
            if widget: widget.deleteLater()

        tipo = self.combo_tipo.currentText()

        if tipo == "Puntual":
            self.campos_posicion.addWidget(QLabel("Posición (x, y):"))
            self.input_pos = QLineEdit("0, 0")
            self.campos_posicion.addWidget(self.input_pos)

        elif tipo == "Recta":
            self.campos_posicion.addWidget(QLabel("Inicio (x1, y1):"))
            self.input_pos1 = QLineEdit("-1, 0")
            self.campos_posicion.addWidget(self.input_pos1)
            self.campos_posicion.addWidget(QLabel("Fin (x2, y2):"))
            self.input_pos2 = QLineEdit("1, 0")
            self.campos_posicion.addWidget(self.input_pos2)

    def actualizar_meshgrid(self):
        """Actualiza la configuración del meshgrid desde los spinboxes."""
        self.meshgrid_config = {
            "x_min": self.x_min_spin.value(),
            "x_max": self.x_max_spin.value(),
            "y_min": self.y_min_spin.value(),
            "y_max": self.y_max_spin.value(),
            "points": self.points_spin.value()
        }
        self.dibujar_meshgrid()

    def dibujar_meshgrid(self):
        """Dibuja el meshgrid en el gráfico."""
        x = np.linspace(self.meshgrid_config["x_min"],
                        self.meshgrid_config["x_max"],
                        self.meshgrid_config["points"])
        y = np.linspace(self.meshgrid_config["y_min"],
                        self.meshgrid_config["y_max"],
                        self.meshgrid_config["points"])

        self.ax.clear()
        for xi in x:
            for yi in y:
                self.ax.plot(xi, yi, 'o', color='gray', markersize=3, alpha=0.5)

        self.actualizar_grafico()

    def anadir_carga(self):
        try:
            tipo = self.combo_tipo.currentText()
            magnitud = float(self.input_magnitud.text())

            if tipo == "Puntual":
                pos = [float(x.strip()) for x in self.input_pos.text().split(",")][:2]
                carga_data = {"nom": "Puntual", "pos": pos, "mag": magnitud}
                item_text = f"Puntual | Pos: {pos} | Q: {magnitud:.2e}C"

            elif tipo == "Recta":
                pos1 = [float(x.strip()) for x in self.input_pos1.text().split(",")][:2]
                pos2 = [float(x.strip()) for x in self.input_pos2.text().split(",")][:2]
                carga_data = {"nom": "Lineal", "pos1": pos1, "pos2": pos2, "density": magnitud}
                item_text = f"Recta | Inicio: {pos1} | Fin: {pos2} | λ: {magnitud:.2e}C/m"

            carga = crear_carga(carga_data)
            self.charges.append(carga)

            item = QListWidgetItem()
            widget = QWidget()
            layout = QHBoxLayout()
            widget.setLayout(layout)

            label = QLabel(item_text)
            color = "#FF6B6B" if magnitud > 0 else "#6B8CFF"
            label.setStyleSheet(f"color: {color};")
            layout.addWidget(label, stretch=1)

            btn_eliminar = QPushButton("×")
            btn_eliminar.setFont(QFont("Arial", 10, QFont.Bold))
            btn_eliminar.setFixedSize(25, 25)
            btn_eliminar.setStyleSheet("""
                QPushButton {
                    color: #ff0000;
                    border: 1px solid #ff0000;
                    border-radius: 12px;
                    background-color: rgba(255, 0, 0, 0.1);
                }
                QPushButton:hover {
                    background-color: rgba(255, 0, 0, 0.3);
                }
            """)
            btn_eliminar.clicked.connect(lambda _, i=len(self.charges)-1: self.eliminar_carga(i))
            layout.addWidget(btn_eliminar)

            item.setSizeHint(widget.sizeHint())
            self.lista_cargas.addItem(item)
            self.lista_cargas.setItemWidget(item, widget)

            self.actualizar_grafico()

        except Exception as e:
            print(f"Error al añadir carga: {e}")

    def eliminar_carga(self, index):
        if 0 <= index < len(self.charges):
            self.charges.pop(index)
            self.lista_cargas.takeItem(index)
            self.actualizar_grafico()

    def actualizar_grafico(self):
        """Dibuja las cargas sobre el meshgrid."""
        self.ax.clear()

        # Dibujar meshgrid
        x = np.linspace(self.meshgrid_config["x_min"],
                        self.meshgrid_config["x_max"],
                        self.meshgrid_config["points"])
        y = np.linspace(self.meshgrid_config["y_min"],
                        self.meshgrid_config["y_max"],
                        self.meshgrid_config["points"])

        for xi in x:
            for yi in y:
                self.ax.plot(xi, yi, 'o', color='gray', markersize=3, alpha=0.5)

        # Dibujar cargas
        for idx, carga in enumerate(self.charges):
            if isinstance(carga, CargaPuntual):
                x, y = carga.posicion[:2]
                color = "#FF6B6B" if carga.magnitud > 0 else "#6B8CFF"
                self.ax.scatter(x, y, color=color, s=200, alpha=0.7)
                self.ax.text(x, y, f"  Q={carga.magnitud:.1e}",
                             color=color, fontsize=9)

        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.set_xlabel("X (m)")
        self.ax.set_ylabel("Y (m)")
        self.ax.set_title("Visualización de Cargas y Meshgrid")
        self.canvas.draw()

    def simular_campo(self):
        """Simula el campo eléctrico."""
        self.actualizar_meshgrid()
        print("Simulando campo eléctrico con:")
        print(f"- Cargas: {self.charges}")
        print(f"- Meshgrid: {self.meshgrid_config}")

    def on_click(self, event):
        """Detecta si se hizo click sobre una carga."""
        if event.inaxes != self.ax:
            return

        for idx, carga in enumerate(self.charges):
            if isinstance(carga, CargaPuntual):
                cx, cy = carga.posicion[:2]
                dist = np.hypot(event.xdata - cx, event.ydata - cy)
                if dist < 0.3:  # margen de detección
                    print(f"Seleccionada carga {idx} en ({cx}, {cy})")
                    self.selected_charge = idx
                    break

    def on_mouse_move(self, event):
        """Mueve la carga seleccionada."""
        if self.selected_charge is not None and event.inaxes == self.ax:
            carga = self.charges[self.selected_charge]
            if isinstance(carga, CargaPuntual):
                carga.posicion[:2] = [event.xdata, event.ydata]
                self.actualizar_grafico()

    def on_release(self, event):
        """Libera la carga seleccionada."""
        if self.selected_charge is not None:
            print(f"Movida carga a ({event.xdata}, {event.ydata})")
            self.selected_charge = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GeoElectricApp()
    ventana.show()
    sys.exit(app.exec_())
