import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLabel, QFileDialog,
    QMessageBox
)
from PyQt5.QtCore import Qt
from modulos.graficos import gerar_grafico_faturamento
from modulos.exportar import exportar_excel, exportar_pdf
from modulos.funcoes_csv import carregar_csv, salvar_csv, adicionar_registro, editar_registro, remover_registro

class InterfaceVendas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Análise de Vendas")
        self.setGeometry(100, 100, 1000, 700)

        self.df = carregar_csv("vendas.csv")

        self.init_ui()
        self.atualizar_interface()

    def init_ui(self):
        central = QWidget()
        self.layout = QVBoxLayout(central)

        # Botões de topo
        barra_botoes = QHBoxLayout()

        btn_carregar = QPushButton("📂 Carregar CSV")
        btn_carregar.clicked.connect(self.carregar_csv)

        btn_exportar_excel = QPushButton("📤 Exportar Excel")
        btn_exportar_excel.clicked.connect(lambda: exportar_excel(self.df))

        btn_exportar_pdf = QPushButton("🖨 Exportar PDF")
        btn_exportar_pdf.clicked.connect(lambda: exportar_pdf(self.df))

        barra_botoes.addWidget(btn_carregar)
        barra_botoes.addWidget(btn_exportar_excel)
        barra_botoes.addWidget(btn_exportar_pdf)

        self.layout.addLayout(barra_botoes)

        # Gráfico
        self.label_titulo = QLabel("Faturamento por Produto")
        self.label_titulo.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.label_titulo)

        self.grafico = gerar_grafico_faturamento(self.df)
        self.layout.addWidget(self.grafico)

        # Tabela
        self.tabela = QTableWidget()
        self.layout.addWidget(self.tabela)

        # Botões de controle de dados
        barra_acao = QHBoxLayout()

        btn_adicionar = QPushButton("➕ Adicionar")
        btn_adicionar.clicked.connect(self.adicionar)

        btn_editar = QPushButton("📝 Editar")
        btn_editar.clicked.connect(self.editar)

        btn_remover = QPushButton("❌ Remover")
        btn_remover.clicked.connect(self.remover)

        btn_salvar = QPushButton("💾 Salvar CSV")
        btn_salvar.clicked.connect(self.salvar)

        barra_acao.addWidget(btn_adicionar)
        barra_acao.addWidget(btn_editar)
        barra_acao.addWidget(btn_remover)
        barra_acao.addWidget(btn_salvar)

        self.layout.addLayout(barra_acao)
        self.setCentralWidget(central)

    def atualizar_interface(self):
        self.layout.removeWidget(self.grafico)
        self.grafico.deleteLater()
        self.grafico = gerar_grafico_faturamento(self.df)
        self.layout.insertWidget(2, self.grafico)
        self.atualizar_tabela()

    def atualizar_tabela(self):
        self.tabela.setRowCount(len(self.df))
        self.tabela.setColumnCount(len(self.df.columns))
        self.tabela.setHorizontalHeaderLabels(self.df.columns)

        for i, row in self.df.iterrows():
            for j, col in enumerate(self.df.columns):
                item = QTableWidgetItem(str(row[col]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tabela.setItem(i, j, item)

    def carregar_csv(self):
        arquivo, _ = QFileDialog.getOpenFileName(self, "Abrir CSV", "", "Arquivos CSV (*.csv)")
        if arquivo:
            self.df = carregar_csv(arquivo)
            self.atualizar_interface()

    def adicionar(self):
        self.df = adicionar_registro(self.df, self)
        self.atualizar_interface()

    def editar(self):
        linha = self.tabela.currentRow()
        if linha >= 0:
            self.df = editar_registro(self.df, linha, self)
            self.atualizar_interface()
        else:
            QMessageBox.warning(self, "Atenção", "Selecione uma linha para editar.")

    def remover(self):
        linha = self.tabela.currentRow()
        if linha >= 0:
            self.df = remover_registro(self.df, linha)
            self.atualizar_interface()
        else:
            QMessageBox.warning(self, "Atenção", "Selecione uma linha para remover.")

    def salvar(self):
        salvar_csv(self.df, "vendas.csv")
        QMessageBox.information(self, "Sucesso", "Arquivo CSV salvo com sucesso.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("estilo.qss", "r") as f:
        app.setStyleSheet(f.read())

    janela = InterfaceVendas()
    janela.show()
    sys.exit(app.exec_())
