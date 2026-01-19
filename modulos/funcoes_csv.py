# Funções para manipular o CSV
import pandas as pd
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton,
                             QHBoxLayout, QFileDialog, QMessageBox, QInputDialog)
import json

CAMPOS = ["Data", "Produto", "Quantidade", "PrecoUnitario"]


def carregar_csv(caminho):
    """Lê um arquivo CSV ou Excel e retorna um DataFrame do pandas."""
    try:
        # Detectar extensão do arquivo
        if caminho.lower().endswith(('.xlsx', '.xls')):
            df = pd.read_excel(caminho, engine='openpyxl')
        else:
            df = pd.read_csv(caminho)
        
        if df.empty:
            QMessageBox.warning(None, "Aviso", "O arquivo está vazio.")
        return df
    except FileNotFoundError:
        QMessageBox.warning(None, "Erro", f"Arquivo não encontrado: {caminho}")
        return pd.DataFrame()
    except Exception as e:
        QMessageBox.warning(None, "Erro", f"Não foi possível carregar o arquivo:\n{e}")
        return pd.DataFrame()

def salvar_csv(df, caminho):
    """Salva o DataFrame no arquivo CSV."""
    df.to_csv(caminho, index=False)

def adicionar_registro(df, parent):
    """Abre diálogo para adicionar um novo registro ao DataFrame."""
    colunas = df.columns.tolist()
    novo_registro = {}
    for col in colunas:
        valor, ok = QInputDialog.getText(parent, "Adicionar Registro", f"Valor para '{col}':")
        if not ok:
            return df
        novo_registro[col] = valor
    return pd.concat([df, pd.DataFrame([novo_registro])], ignore_index=True)

def editar_registro(df, linha, parent):
    """Permite editar uma linha existente do DataFrame."""
    colunas = df.columns.tolist()
    for col in colunas:
        valor_atual = str(df.at[linha, col])
        novo_valor, ok = QInputDialog.getText(parent, "Editar Registro", f"Novo valor para '{col}':", QLineEdit.Normal, valor_atual)
        if ok:
            df.at[linha, col] = novo_valor
    return df

def remover_registro(df, linha):
    """Remove uma linha do DataFrame."""
    df = df.drop(linha).reset_index(drop=True)
    return df

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
