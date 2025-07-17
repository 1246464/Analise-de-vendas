from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

def gerar_grafico_faturamento(df):
    # Cria um QWidget com layout vertical
    widget = QWidget()
    layout = QVBoxLayout(widget)
    widget.setLayout(layout)

    # Cria o gráfico
    fig, ax = plt.subplots(figsize=(5, 3.5))
    canvas = FigureCanvas(fig)

    faturamento = df.groupby("Produto")["Faturamento"].sum().sort_values(ascending=False)
    ax.bar(faturamento.index, faturamento.values)
    ax.set_title("Faturamento por Produto")
    ax.set_ylabel("R$")

    fig.tight_layout()
    layout.addWidget(canvas)

    return widget
