# Funções para manipular o CSV
import pandas as pd
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout

CAMPOS = ["Data", "Produto", "Quantidade", "PrecoUnitario"]

def carregar_csv(caminho):
    df = pd.read_csv(caminho)
    if "Faturamento" not in df.columns:
        df["Faturamento"] = df["Quantidade"] * df["PrecoUnitario"]
    return df

def salvar_csv(df, caminho):
    df.to_csv(caminho, index=False)

def adicionar_registro(df, parent):
    dialog = RegistroDialog(parent, "Adicionar Registro")
    if dialog.exec_():
        novo = dialog.obter_dados()
        novo["Faturamento"] = float(novo["Quantidade"]) * float(novo["PrecoUnitario"])
        df = df.append(novo, ignore_index=True)
    return df

def editar_registro(df, linha, parent):
    dados_atuais = df.loc[linha].to_dict()
    dialog = RegistroDialog(parent, "Editar Registro", dados_atuais)
    if dialog.exec_():
        editado = dialog.obter_dados()
        editado["Faturamento"] = float(editado["Quantidade"]) * float(editado["PrecoUnitario"])
        for campo in CAMPOS + ["Faturamento"]:
            df.at[linha, campo] = editado[campo]
    return df

def remover_registro(df, linha):
    return df.drop(index=linha).reset_index(drop=True)

class RegistroDialog(QDialog):
    def __init__(self, parent=None, titulo="Registro", dados=None):
        super().__init__(parent)
        self.setWindowTitle(titulo)
        self.inputs = {}
        layout = QVBoxLayout()

        for campo in CAMPOS:
            layout.addWidget(QLabel(campo))
            entrada = QLineEdit()
            if dados and campo in dados:
                entrada.setText(str(dados[campo]))
            layout.addWidget(entrada)
            self.inputs[campo] = entrada

        botoes = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_cancelar = QPushButton("Cancelar")
        btn_ok.clicked.connect(self.accept)
        btn_cancelar.clicked.connect(self.reject)
        botoes.addWidget(btn_ok)
        botoes.addWidget(btn_cancelar)

        layout.addLayout(botoes)
        self.setLayout(layout)

    def obter_dados(self):
        return {campo: self.inputs[campo].text() for campo in CAMPOS}
