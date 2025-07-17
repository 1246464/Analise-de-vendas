# Funções para exportar para Excel e PDF
import pandas as pd
from fpdf import FPDF
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os

def exportar_excel(df):
    caminho, _ = QFileDialog.getSaveFileName(None, "Salvar como Excel", "", "Arquivos Excel (*.xlsx)")
    if caminho:
        try:
            df.to_excel(caminho, index=False)
            QMessageBox.information(None, "Sucesso", f"Exportado para Excel:\n{caminho}")
        except Exception as e:
            QMessageBox.critical(None, "Erro", f"Erro ao exportar Excel:\n{e}")

def exportar_pdf(df):
    caminho, _ = QFileDialog.getSaveFileName(None, "Salvar como PDF", "", "Arquivos PDF (*.pdf)")
    if caminho:
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=10)
            pdf.set_title("Relatório de Vendas")

            # Cabeçalho
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(200, 10, "Relatório de Vendas", ln=True, align="C")
            pdf.ln(5)

            # Tabela
            pdf.set_font("Arial", size=9)
            colunas = df.columns.tolist()
            largura_coluna = 190 / len(colunas)
            for col in colunas:
                pdf.cell(largura_coluna, 8, col, border=1, ln=0)
            pdf.ln()

            for _, row in df.iterrows():
                for item in row:
                    texto = str(round(item, 2)) if isinstance(item, float) else str(item)
                    pdf.cell(largura_coluna, 8, texto, border=1)
                pdf.ln()

            pdf.output(caminho)
            QMessageBox.information(None, "Sucesso", f"Exportado para PDF:\n{caminho}")
        except Exception as e:
            QMessageBox.critical(None, "Erro", f"Erro ao exportar PDF:\n{e}")
