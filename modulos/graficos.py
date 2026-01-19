# from PyQt5.QtWidgets import (
#     QWidget, QGridLayout, QComboBox, QPushButton, QLabel, QMessageBox, QGroupBox, QVBoxLayout
# )
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd


# def gerar_grafico_faturamento(df):
#     widget = QWidget()
#     layout = QGridLayout(widget)
#     widget.setLayout(layout)

#     def criar_bloco_grafico(nome_bloco):
#         box = QGroupBox(nome_bloco)
#         box_layout = QVBoxLayout(box)

#         colunas = df.columns.tolist()

#         eixo_x = QComboBox()
#         eixo_x.addItems(colunas)
#         eixo_y = QComboBox()
#         eixo_y.addItems(colunas)

#         tipo_grafico = QComboBox()
#         tipo_grafico.addItems(["Barras", "Pizza", "Linha", "Dispersão", "3D"])

#         # --- Campos adicionais (inicialmente ocultos) ---
#         eixo_z = QComboBox()
#         eixo_z.addItems(colunas)
#         eixo_dx = QComboBox()
#         eixo_dx.addItems(colunas)
#         eixo_dy = QComboBox()
#         eixo_dy.addItems(colunas)
#         eixo_dz = QComboBox()
#         eixo_dz.addItems(colunas)

#         lbl_z = QLabel("Eixo Z:")
#         lbl_dx = QLabel("Eixo DX:")
#         lbl_dy = QLabel("Eixo DY:")
#         lbl_dz = QLabel("Eixo DZ:")

#         # --- Função que mostra/esconde campos extras ---
#         def atualizar_campos(tipo):
#             # Oculta tudo primeiro
#             for w in [lbl_z, eixo_z, lbl_dx, eixo_dx, lbl_dy, eixo_dy, lbl_dz, eixo_dz]:
#                 w.hide()

#             if tipo == "Dispersão":
#                 lbl_z.show()
#                 eixo_z.show()
#             elif tipo == "3D":
#                 for w in [lbl_z, eixo_z, lbl_dx, eixo_dx, lbl_dy, eixo_dy, lbl_dz, eixo_dz]:
#                     w.show()

#         tipo_grafico.currentTextChanged.connect(atualizar_campos)
#         atualizar_campos(tipo_grafico.currentText())

#         # Botão e figura
#         btn_gerar = QPushButton("Gerar")

#         fig, ax = plt.subplots(figsize=(4.5, 3))
#         canvas = FigureCanvas(fig)

#         # --- Função que desenha o gráfico ---
#         def atualizar_grafico():
#             for i in reversed(range(box_layout.count())):
#                 widget_remover = box_layout.itemAt(i).widget()
#                 if widget_remover is not None:
#                     widget_remover.deleteLater()

#           # --- Cria novo canvas e figura ---
#             fig, ax = plt.subplots(figsize=(5, 3))
#             canvas = FigureCanvas(fig)


#             #ax.clear()
#             x = eixo_x.currentText()
#             y = eixo_y.currentText()
#             tipo = tipo_grafico.currentText()

#             try:
#                 if tipo == "Barras":
#                     ax.bar(df[x], df[y], color="#4C72B0")
#                 elif tipo == "Pizza":
#                     ax.pie(df[y], labels=df[x], autopct="%1.1f%%", startangle=90)
#                 elif tipo == "Linha":
#                     ax.plot(df[x], df[y], color="#55A868", marker="o")
#                 elif tipo == "Dispersão":
#                     z = df[eixo_z.currentText()] if eixo_z.isVisible() else None
#                     if z is not None:
#                         ax.scatter(df[x], df[y], c=z, cmap="viridis")
#                     else:
#                         ax.scatter(df[x], df[y], color="#C44E52")
#                 elif tipo == "3D":
#                     fig3d = plt.figure(figsize=(4.5, 3))
#                     ax3d = fig3d.add_subplot(111, projection="3d")
#                     ax3d.bar3d(
#                         np.arange(len(df[x])),
#                         np.zeros_like(df[y]),
#                         np.zeros_like(df[y]),
#                         0.5, 0.5, df[y],
#                         shade=True,
#                     )
#                     canvas3d = FigureCanvas(fig3d)
#                     box_layout.replaceWidget(canvas, canvas3d)
#                     canvas.hide()
#                     box_layout.addWidget(canvas3d)
#                     return

#                 ax.set_title(f"{tipo} de {y} por {x}")
#                 fig.tight_layout()
#                 canvas.draw()
#                 box_layout.addWidget(canvas)

#             except Exception as e:
#                 QMessageBox.warning(widget, "Erro", f"Erro ao gerar gráfico: {e}")

#         btn_gerar.clicked.connect(atualizar_grafico)

#         # --- Montagem visual do bloco ---
#         box_layout.addWidget(QLabel("Eixo X:"))
#         box_layout.addWidget(eixo_x)
#         box_layout.addWidget(QLabel("Eixo Y:"))
#         box_layout.addWidget(eixo_y)
#         box_layout.addWidget(QLabel("Tipo de gráfico:"))
#         box_layout.addWidget(tipo_grafico)

#         # Campos extras (ficam escondidos até mudar o tipo)
#         box_layout.addWidget(lbl_z)
#         box_layout.addWidget(eixo_z)
#         box_layout.addWidget(lbl_dx)
#         box_layout.addWidget(eixo_dx)
#         box_layout.addWidget(lbl_dy)
#         box_layout.addWidget(eixo_dy)
#         box_layout.addWidget(lbl_dz)
#         box_layout.addWidget(eixo_dz)

#         box_layout.addWidget(btn_gerar)
#         box_layout.addWidget(canvas)

#         return box

#     # Adiciona os blocos em layout 2x2
#     layout.addWidget(criar_bloco_grafico("Gráfico 1"), 0, 0)
#     layout.addWidget(criar_bloco_grafico("Gráfico 2"), 0, 1)
#     layout.addWidget(criar_bloco_grafico("Gráfico 3"), 1, 0)
#     layout.addWidget(criar_bloco_grafico("Gráfico 4"), 1, 1)

#     return widget

# modulos/graficos.py
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QLabel, QComboBox, QPushButton, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt


def _opcoes_validas(colunas):
    # Deixa X/Y preenchidos com as primeiras colunas por padrão, se existirem
    return colunas if len(colunas) > 0 else ["(sem colunas)"]


def criar_bloco_grafico(df: pd.DataFrame, titulo: str) -> QWidget:
    """
    Retorna um QWidget contendo:
      - Combos de eixo X, Y e Tipo de gráfico
      - Campos extras automáticos para Dispersão/3D (Z, DX, DY, DZ)
      - Botão 'Gerar'
      - Canvas Matplotlib
    """
    box = QGroupBox(titulo)
    box_layout = QVBoxLayout(box)

    colunas = df.columns.tolist()
    colunas_combo = _opcoes_validas(colunas)

    # Combos principais
    box_layout.addWidget(QLabel("Eixo X:"))
    eixo_x = QComboBox()
    eixo_x.addItems(colunas_combo)
    box_layout.addWidget(eixo_x)

    box_layout.addWidget(QLabel("Eixo Y:"))
    eixo_y = QComboBox()
    eixo_y.addItems(colunas_combo)
    box_layout.addWidget(eixo_y)

    box_layout.addWidget(QLabel("Tipo de gráfico:"))
    tipo_grafico = QComboBox()
    tipo_grafico.addItems(["Barras", "Pizza", "Linha", "Dispersão", "3D"])
    box_layout.addWidget(tipo_grafico)

    # Campos extras (controlados por visibilidade)
    lbl_z = QLabel("Eixo Z:")
    eixo_z = QComboBox(); eixo_z.addItems(colunas_combo)

    lbl_dx = QLabel("Eixo DX:")
    eixo_dx = QComboBox(); eixo_dx.addItems(colunas_combo)

    lbl_dy = QLabel("Eixo DY:")
    eixo_dy = QComboBox(); eixo_dy.addItems(colunas_combo)

    lbl_dz = QLabel("Eixo DZ:")
    eixo_dz = QComboBox(); eixo_dz.addItems(colunas_combo)

    for w in [lbl_z, eixo_z, lbl_dx, eixo_dx, lbl_dy, eixo_dy, lbl_dz, eixo_dz]:
        box_layout.addWidget(w)

    def atualizar_campos_visiveis():
        tipo = tipo_grafico.currentText()
        # Esconde tudo
        for w in [lbl_z, eixo_z, lbl_dx, eixo_dx, lbl_dy, eixo_dy, lbl_dz, eixo_dz]:
            w.hide()
        # Mostra conforme o tipo
        if tipo == "Dispersão":
            lbl_z.show(); eixo_z.show()
        elif tipo == "3D":
            for w in [lbl_z, eixo_z, lbl_dx, eixo_dx, lbl_dy, eixo_dy, lbl_dz, eixo_dz]:
                w.show()

    tipo_grafico.currentTextChanged.connect(atualizar_campos_visiveis)
    atualizar_campos_visiveis()

    # Botão gerar
    btn_gerar = QPushButton("Gerar")
    box_layout.addWidget(btn_gerar)

    # Canvas fixo (não removemos os controles ao redesenhar)
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    canvas = FigureCanvas(fig)
    box_layout.addWidget(canvas)

    def _coluna_numerica(nome_col):
        # Tenta converter a série para numérico quando possível (ignora erros)
        try:
            return pd.to_numeric(df[nome_col], errors="coerce")
        except Exception:
            return df[nome_col]

    def desenhar():
        if len(colunas) < 2:
            QMessageBox.warning(box, "Atenção", "Seu CSV precisa ter pelo menos duas colunas para gerar gráficos.")
            return

        x_nome = eixo_x.currentText()
        y_nome = eixo_y.currentText()
        if x_nome not in df.columns or y_nome not in df.columns:
            QMessageBox.warning(box, "Atenção", "Selecione colunas válidas.")
            return

        tipo = tipo_grafico.currentText()
        ax.clear()

        try:
            if tipo == "Barras":
                # Em barras, se X for categórico e Y numérico, agrupa somando
                x_vals = df[x_nome]
                y_vals = _coluna_numerica(y_nome)
                if y_vals.dtype.kind in "biufc":
                    # agrega por categoria de X
                    dados = y_vals.groupby(x_vals).sum()
                    ax.bar(dados.index.astype(str), dados.values)
                    ax.set_xticklabels(dados.index.astype(str), rotation=30, ha="right")
                else:
                    ax.bar(x_vals.astype(str), df[y_nome])
                    ax.set_xticklabels(x_vals.astype(str), rotation=30, ha="right")

            elif tipo == "Pizza":
                y_vals = _coluna_numerica(y_nome)
                x_vals = df[x_nome].astype(str)
                # agrega (pizza não faz sentido com dezenas de itens únicos)
                dados = y_vals.groupby(x_vals).sum()
                ax.pie(dados.values, labels=dados.index, autopct="%1.1f%%", startangle=90)
                ax.axis("equal")

            elif tipo == "Linha":
                x_vals = df[x_nome]
                y_vals = _coluna_numerica(y_nome)
                ax.plot(x_vals, y_vals, marker="o")

            elif tipo == "Dispersão":
                x_vals = _coluna_numerica(x_nome)
                y_vals = _coluna_numerica(y_nome)
                if lbl_z.isVisible():
                    z_vals = _coluna_numerica(eixo_z.currentText())
                    sc = ax.scatter(x_vals, y_vals, c=z_vals)
                    fig.colorbar(sc, ax=ax, shrink=0.85)
                else:
                    ax.scatter(x_vals, y_vals)

            elif tipo == "3D":
                fig3d = plt.figure(figsize=(5.2, 3.4))
                ax3d = fig3d.add_subplot(111, projection="3d")

                # Usa DX/DY/DZ como dimensões auxiliares se visíveis, senão cria padrões
                x_vals = np.arange(len(df[x_nome]))
                y_vals = np.zeros_like(x_vals, dtype=float)
                z_base = np.zeros_like(x_vals, dtype=float)

                h_vals = _coluna_numerica(y_nome).fillna(0).values
                dx_vals = np.full_like(x_vals, 0.6, dtype=float)
                dy_vals = np.full_like(x_vals, 0.6, dtype=float)

                try:
                    if lbl_dx.isVisible(): dx_vals = np.clip(pd.to_numeric(df[eixo_dx.currentText()], errors='coerce').fillna(0.6).values, 0.05, None)
                    if lbl_dy.isVisible(): dy_vals = np.clip(pd.to_numeric(df[eixo_dy.currentText()], errors='coerce').fillna(0.6).values, 0.05, None)
                except Exception:
                    pass

                ax3d.bar3d(x_vals, y_vals, z_base, dx_vals, dy_vals, h_vals, shade=True)
                ax3d.set_xlabel(x_nome); ax3d.set_zlabel(y_nome)

                canvas3d = FigureCanvas(fig3d)
                # troca o canvas (remove o antigo e adiciona o novo)
                box_layout.replaceWidget(canvas, canvas3d)
                canvas.setParent(None)
                canvas = canvas3d
                return  # já renderizado


            ax.set_title(f"{tipo} de '{y_nome}' por '{x_nome}'")
            fig.tight_layout()
            canvas.draw()

        except Exception as e:
            QMessageBox.warning(box, "Erro", f"Erro ao gerar gráfico: {e}")

    btn_gerar.clicked.connect(desenhar)

    return box
