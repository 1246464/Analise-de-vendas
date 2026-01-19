import sys
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLabel, QFileDialog,
    QMessageBox, QScrollArea, QFrame, QComboBox, QGridLayout, QGroupBox,
    QGraphicsOpacityEffect, QTabWidget, QListWidget, QSplitter, QTextEdit
)
from PyQt5.QtCore import Qt, QPropertyAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt
from datetime import datetime

# ---- Módulos auxiliares ----
from modulos.exportar import exportar_excel, exportar_pdf
from modulos.funcoes_csv import carregar_csv, salvar_csv, adicionar_registro, editar_registro, remover_registro

class InterfaceVendas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Dashboard de Análise de Vendas")
        self.setGeometry(100, 100, 1200, 800)

        # --- Lê o último arquivo usado (se existir) ---
        import json, os
        self.config_path = "config.json"
        ultimo_arquivo = None
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    ultimo_arquivo = cfg.get("ultimo_csv")
            except:
                pass

        # --- Carrega o CSV (padrão ou último usado) ---
        if ultimo_arquivo and os.path.exists(ultimo_arquivo):
            self.df = carregar_csv(ultimo_arquivo)
            self.arquivo_atual = ultimo_arquivo
        else:
            self.df = carregar_csv("vendas.csv")
            self.arquivo_atual = "vendas.csv"

        # Lista de arquivos CSV abertos (DEVE VIR ANTES de init_ui)
        self.arquivos_abertos = {self.arquivo_atual: self.df}
        
        self.cards = []
        self.init_ui()
        if hasattr(self, "tabela"):
            self.atualizar_tabela()

    # ------------------- INTERFACE -------------------
    def init_ui(self):
        central = QWidget()
        layout_principal = QVBoxLayout(central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # ---------- Cabeçalho ----------
        header = QLabel("📊 DASHBOARD DE ANÁLISE DE VENDAS - CSV & EXCEL")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            background-color: #005f73;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 16px;
            letter-spacing: 1px;
        """)
        layout_principal.addWidget(header)

        # ---------- Sistema de Abas ----------
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: #f5f6fa;
            }
            QTabBar::tab {
                background: #ecf0f1;
                color: #2c3e50;
                padding: 12px 24px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }
            QTabBar::tab:selected {
                background: #0077b6;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background: #90e0ef;
            }
        """)
        
        # Criar abas
        self.criar_aba_dashboard()
        self.criar_aba_dados()
        self.criar_aba_banco()
        
        layout_principal.addWidget(self.tabs)
        self.setCentralWidget(central)

    # ------------------- ABA DASHBOARD -------------------
    def criar_aba_dashboard(self):
        aba = QWidget()
        layout = QVBoxLayout(aba)
        
        # Área rolável
        conteudo = QWidget()
        conteudo_layout = QVBoxLayout(conteudo)
        conteudo_layout.setContentsMargins(20, 15, 20, 15)
        conteudo_layout.setSpacing(25)

        # ---------- Botões principais ----------
        barra_botoes = QHBoxLayout()
        barra_botoes.setSpacing(10)

        btn_adicionar_grafico = QPushButton("➕ Adicionar Gráfico")
        btn_adicionar_grafico.clicked.connect(self.adicionar_grafico)

        btn_abrir_arquivo = QPushButton("📂 Abrir Arquivo")
        btn_abrir_arquivo.clicked.connect(self.adicionar_novo_arquivo)

        btn_exportar_excel = QPushButton("📤 Exportar Excel")
        btn_exportar_excel.clicked.connect(lambda: exportar_excel(self.df))

        btn_exportar_pdf = QPushButton("🖨 Exportar PDF")
        btn_exportar_pdf.clicked.connect(lambda: exportar_pdf(self.df))

        barra_botoes.addStretch(1)
        barra_botoes.addWidget(btn_abrir_arquivo)
        barra_botoes.addWidget(btn_exportar_excel)
        barra_botoes.addWidget(btn_exportar_pdf)
        barra_botoes.addWidget(btn_adicionar_grafico)

        conteudo_layout.addLayout(barra_botoes)

        # ---------- Painel de Estatísticas ----------
        self.painel_estatisticas = self.criar_painel_estatisticas()
        conteudo_layout.addWidget(self.painel_estatisticas)

        # ---------- Painel de gráficos ----------
        self.painel_graficos = QWidget()
        self.layout_graficos = QGridLayout(self.painel_graficos)
        self.layout_graficos.setHorizontalSpacing(40)
        self.layout_graficos.setVerticalSpacing(40)
        self.layout_graficos.setContentsMargins(30, 20, 30, 20)
        self.layout_graficos.setAlignment(Qt.AlignTop)

        conteudo_layout.addWidget(self.painel_graficos)
        
        # ---------- Gráfico de Tendência Temporal ----------
        grupo_tendencia = QGroupBox("📈 Análise de Tendência Temporal")
        tendencia_layout = QVBoxLayout(grupo_tendencia)
        
        # Controles
        controles_tend = QHBoxLayout()
        controles_tend.addWidget(QLabel("Coluna de Data:"))
        self.combo_data = QComboBox()
        controles_tend.addWidget(self.combo_data)
        
        controles_tend.addWidget(QLabel("Coluna de Valor:"))
        self.combo_valor = QComboBox()
        controles_tend.addWidget(self.combo_valor)
        
        btn_gerar_tendencia = QPushButton("📊 Gerar Análise")
        btn_gerar_tendencia.clicked.connect(self.gerar_grafico_tendencia)
        controles_tend.addWidget(btn_gerar_tendencia)
        controles_tend.addStretch()
        
        tendencia_layout.addLayout(controles_tend)
        
        # Canvas para gráfico
        self.fig_tendencia, self.ax_tendencia = plt.subplots(figsize=(10, 4))
        self.canvas_tendencia = FigureCanvas(self.fig_tendencia)
        tendencia_layout.addWidget(self.canvas_tendencia)
        
        conteudo_layout.addWidget(grupo_tendencia)
        
        # Atualizar combos
        self.atualizar_combos_tendencia()

        # Scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(conteudo)
        layout.addWidget(scroll)
        
        self.tabs.addTab(aba, "📊 Dashboard")

    # ------------------- ABA DADOS -------------------
    def criar_aba_dados(self):
        aba = QWidget()
        layout = QVBoxLayout(aba)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)
        
        # ---------- Gerenciador de Arquivos ----------
        gerenciador_layout = QHBoxLayout()
        
        # Lista de arquivos
        grupo_arquivos = QGroupBox("📁 Arquivos Abertos (CSV/Excel)")
        grupo_arquivos.setMaximumWidth(300)
        lista_layout = QVBoxLayout(grupo_arquivos)
        
        self.lista_arquivos = QListWidget()
        self.lista_arquivos.itemClicked.connect(self.trocar_arquivo_ativo)
        lista_layout.addWidget(self.lista_arquivos)
        
        btn_adicionar_arquivo = QPushButton("➕ Abrir Arquivo")
        btn_adicionar_arquivo.clicked.connect(self.adicionar_novo_arquivo)
        lista_layout.addWidget(btn_adicionar_arquivo)
        
        gerenciador_layout.addWidget(grupo_arquivos)
        
        # Área de dados
        area_dados = QWidget()
        dados_layout = QVBoxLayout(area_dados)
        
        label_tabela = QLabel("📋 Registros de Vendas")
        label_tabela.setStyleSheet("font-size: 16px; font-weight: bold;")
        dados_layout.addWidget(label_tabela)

        # Barra de busca
        from PyQt5.QtWidgets import QLineEdit
        busca_layout = QHBoxLayout()
        self.busca_input = QLineEdit()
        self.busca_input.setPlaceholderText("🔍 Buscar em todos os campos...")
        self.busca_input.textChanged.connect(self.filtrar_tabela)
        self.busca_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #0077b6;
                border-radius: 6px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #00b4d8;
            }
        """)
        busca_layout.addWidget(self.busca_input)
        dados_layout.addLayout(busca_layout)

        self.tabela = QTableWidget()
        self.tabela.setMinimumHeight(350)
        dados_layout.addWidget(self.tabela)

        # ---------- Botões CRUD ----------
        barra_acao = QHBoxLayout()
        barra_acao.setSpacing(10)

        btn_adicionar = QPushButton("➕ Adicionar")
        btn_adicionar.clicked.connect(self.adicionar)

        btn_editar = QPushButton("📝 Editar")
        btn_editar.clicked.connect(self.editar)

        btn_remover = QPushButton("❌ Remover")
        btn_remover.clicked.connect(self.remover)

        btn_salvar = QPushButton("💾 Salvar")
        btn_salvar.clicked.connect(self.salvar)
        
        btn_salvar_como = QPushButton("💾 Salvar Como...")
        btn_salvar_como.clicked.connect(self.salvar_como)

        barra_acao.addStretch(1)
        barra_acao.addWidget(btn_adicionar)
        barra_acao.addWidget(btn_editar)
        barra_acao.addWidget(btn_remover)
        barra_acao.addWidget(btn_salvar)
        barra_acao.addWidget(btn_salvar_como)
        dados_layout.addLayout(barra_acao)
        
        gerenciador_layout.addWidget(area_dados)
        layout.addLayout(gerenciador_layout)
        
        self.tabs.addTab(aba, "📁 Dados")
        
        # Atualizar lista
        self.atualizar_lista_arquivos()

    # ------------------- ABA BANCO DE DADOS -------------------
    def criar_aba_banco(self):
        aba = QWidget()
        layout = QVBoxLayout(aba)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)
        
        # Título
        titulo = QLabel("🗄️ Gerenciamento de Banco de Dados SQLite")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #0077b6;")
        layout.addWidget(titulo)
        
        # Botões de ação
        botoes_layout = QHBoxLayout()
        
        btn_conectar = QPushButton("🔌 Conectar/Criar BD")
        btn_conectar.clicked.connect(self.conectar_banco)
        
        btn_importar = QPushButton("📥 Importar CSV → BD")
        btn_importar.clicked.connect(self.importar_csv_para_bd)
        
        btn_exportar = QPushButton("📤 Exportar BD → CSV")
        btn_exportar.clicked.connect(self.exportar_bd_para_csv)
        
        btn_consultar = QPushButton("🔍 Consultar SQL")
        btn_consultar.clicked.connect(self.executar_consulta_sql)
        
        botoes_layout.addWidget(btn_conectar)
        botoes_layout.addWidget(btn_importar)
        botoes_layout.addWidget(btn_exportar)
        botoes_layout.addWidget(btn_consultar)
        botoes_layout.addStretch()
        
        layout.addLayout(botoes_layout)
        
        # Status da conexão
        self.label_status_bd = QLabel("⚪ Desconectado")
        self.label_status_bd.setStyleSheet("font-size: 14px; padding: 10px; background-color: #ecf0f1; border-radius: 6px;")
        layout.addWidget(self.label_status_bd)
        
        # Área de consulta SQL
        grupo_sql = QGroupBox("💻 Console SQL")
        sql_layout = QVBoxLayout(grupo_sql)
        
        self.sql_input = QTextEdit()
        self.sql_input.setPlaceholderText("Digite sua consulta SQL aqui...\n\nExemplo:\nSELECT * FROM vendas LIMIT 10;")
        self.sql_input.setMaximumHeight(150)
        sql_layout.addWidget(self.sql_input)
        
        btn_executar_sql = QPushButton("▶️ Executar SQL")
        btn_executar_sql.clicked.connect(self.executar_consulta_sql)
        sql_layout.addWidget(btn_executar_sql)
        
        layout.addWidget(grupo_sql)
        
        # Tabela de resultados
        self.tabela_bd = QTableWidget()
        layout.addWidget(self.tabela_bd)
        
        self.tabs.addTab(aba, "🗄️ Banco de Dados")
        
        # Variável para conexão
        self.conexao_bd = None
        self.caminho_bd = None

    # ------------------- PAINEL DE ESTATÍSTICAS -------------------
    def criar_painel_estatisticas(self):
        """Cria um painel com estatísticas descritivas dos dados"""
        painel = QGroupBox("📊 Estatísticas Descritivas")
        painel.setStyleSheet("""
            QGroupBox {
                background-color: #ffffff;
                border: 2px solid #0077b6;
                border-radius: 10px;
                padding: 15px;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        layout = QHBoxLayout(painel)
        
        # Criar cards de estatísticas
        self.stats_cards = []
        for i in range(4):
            card = QLabel()
            card.setAlignment(Qt.AlignCenter)
            card.setStyleSheet("""
                QLabel {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #0077b6, stop:1 #00b4d8);
                    color: white;
                    border-radius: 8px;
                    padding: 15px;
                    font-size: 13px;
                    font-weight: bold;
                }
            """)
            card.setMinimumHeight(80)
            layout.addWidget(card)
            self.stats_cards.append(card)
        
        self.atualizar_estatisticas()
        return painel

    def atualizar_estatisticas(self):
        """Atualiza os cards com estatísticas dos dados"""
        if self.df.empty:
            for card in self.stats_cards:
                card.setText("Sem dados")
            return
        
        # Total de registros
        self.stats_cards[0].setText(f"📋 Total de Registros\n{len(self.df)}")
        
        # Colunas numéricas
        colunas_numericas = self.df.select_dtypes(include=[np.number]).columns
        
        if len(colunas_numericas) > 0:
            # Soma total da primeira coluna numérica
            col = colunas_numericas[0]
            total = self.df[col].sum()
            self.stats_cards[1].setText(f"💰 Total {col}\n{total:,.2f}")
            
            # Média
            media = self.df[col].mean()
            self.stats_cards[2].setText(f"📈 Média {col}\n{media:,.2f}")
            
            # Máximo
            maximo = self.df[col].max()
            self.stats_cards[3].setText(f"🔝 Máximo {col}\n{maximo:,.2f}")
        else:
            for i in range(1, 4):
                self.stats_cards[i].setText("Sem dados\nnuméricos")

    def atualizar_combos_tendencia(self):
        """Atualiza os combos com as colunas disponíveis"""
        self.combo_data.clear()
        self.combo_valor.clear()
        
        if not self.df.empty:
            colunas = self.df.columns.tolist()
            self.combo_data.addItems(colunas)
            self.combo_valor.addItems(colunas)

    def gerar_grafico_tendencia(self):
        """Gera gráfico de tendência temporal"""
        if self.df.empty:
            QMessageBox.warning(self, "Aviso", "Não há dados para gerar o gráfico!")
            return
        
        col_data = self.combo_data.currentText()
        col_valor = self.combo_valor.currentText()
        
        if not col_data or not col_valor:
            QMessageBox.warning(self, "Aviso", "Selecione as colunas!")
            return
        
        try:
            import warnings
            self.ax_tendencia.clear()
            
            # Converter data - tentar múltiplos formatos
            df_temp = self.df.copy()
            
            # Suprimir warnings de conversão de data
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', message='Could not infer format')
                
                # Tentar converter com formato inferido (mais flexível)
                df_temp[col_data] = pd.to_datetime(df_temp[col_data], errors='coerce', dayfirst=False)
                
                # Se não conseguiu converter nenhum valor, tentar com dayfirst=True
                if df_temp[col_data].isna().all():
                    df_temp[col_data] = pd.to_datetime(self.df[col_data], errors='coerce', dayfirst=True)
                
                # Se ainda não funcionar, tentar formatos específicos comuns
                if df_temp[col_data].isna().all():
                    formatos = ['%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%Y-%m-%d', '%m/%d/%Y', '%m-%d-%Y']
                    for fmt in formatos:
                        try:
                            df_temp[col_data] = pd.to_datetime(self.df[col_data], format=fmt, errors='coerce')
                            if not df_temp[col_data].isna().all():
                                break
                        except:
                            continue
            
            df_temp[col_valor] = pd.to_numeric(df_temp[col_valor], errors='coerce')
            
            # Verificar quantos valores válidos temos
            valores_data_validos = df_temp[col_data].notna().sum()
            valores_valor_validos = df_temp[col_valor].notna().sum()
            
            # Remover valores nulos
            df_temp = df_temp.dropna(subset=[col_data, col_valor])
            
            if df_temp.empty:
                mensagem = f"Não há dados válidos para o gráfico!\n\n"
                mensagem += f"Coluna '{col_data}':\n"
                mensagem += f"  - Total de registros: {len(self.df)}\n"
                mensagem += f"  - Valores válidos como data: {valores_data_validos}\n\n"
                mensagem += f"Coluna '{col_valor}':\n"
                mensagem += f"  - Valores válidos como número: {valores_valor_validos}\n\n"
                mensagem += "Dica: Verifique se a coluna de data contém datas válidas\n"
                mensagem += "e se a coluna de valor contém números."
                QMessageBox.warning(self, "Aviso", mensagem)
                return
            
            # Ordenar por data
            df_temp = df_temp.sort_values(col_data)
            
            # Agregar por data
            df_agrupado = df_temp.groupby(col_data)[col_valor].sum().reset_index()
            
            # Plotar
            self.ax_tendencia.plot(df_agrupado[col_data], df_agrupado[col_valor], 
                                  marker='o', linewidth=2, markersize=6, color='#0077b6')
            self.ax_tendencia.fill_between(df_agrupado[col_data], df_agrupado[col_valor], 
                                          alpha=0.3, color='#90e0ef')
            
            # Linha de tendência
            x_numeric = np.arange(len(df_agrupado))
            z = np.polyfit(x_numeric, df_agrupado[col_valor], 1)
            p = np.poly1d(z)
            self.ax_tendencia.plot(df_agrupado[col_data], p(x_numeric), 
                                  "--", linewidth=2, color='#e63946', label='Tendência')
            
            self.ax_tendencia.set_title(f'Tendência de {col_valor} ao Longo do Tempo', 
                                       fontsize=14, fontweight='bold')
            self.ax_tendencia.set_xlabel(col_data, fontsize=11)
            self.ax_tendencia.set_ylabel(col_valor, fontsize=11)
            self.ax_tendencia.legend()
            self.ax_tendencia.grid(True, alpha=0.3)
            
            # Rotacionar labels de data
            plt.setp(self.ax_tendencia.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            self.fig_tendencia.tight_layout()
            self.canvas_tendencia.draw()
            
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao gerar gráfico:\n{e}")

    # ------------------- ADICIONAR GRÁFICOS -------------------
    def adicionar_grafico(self):
        if len(self.cards) >= 4:
            QMessageBox.warning(self, "Limite atingido", "Você só pode criar até 4 gráficos.")
            return

        card = self.criar_card_grafico(f"Gráfico {len(self.cards) + 1}")
        self.cards.append(card)

        row = (len(self.cards) - 1) // 2
        col = (len(self.cards) - 1) % 2
        self.layout_graficos.addWidget(card, row, col, Qt.AlignTop)
        self.layout_graficos.setHorizontalSpacing(40)
        self.layout_graficos.setVerticalSpacing(40)
        self.layout_graficos.setContentsMargins(30, 20, 30, 20)
        self.painel_graficos.adjustSize()

    # ------------------- CRIAR CARD DE GRÁFICO -------------------
    def criar_card_grafico(self, titulo):
        card = QGroupBox(titulo)
        card.setStyleSheet("""
            QGroupBox {
                background-color: #ffffff;
                border: 1px solid #dcdde1;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }
        """)
        layout = QVBoxLayout(card)

        # --- Colunas do arquivo atual ---
        colunas = self.df.columns.tolist()
        if not colunas:
            QMessageBox.warning(self, "Erro", "Nenhum dado disponível no CSV.")
            return card

        # --- Campos principais ---
        lbl_x = QLabel("Eixo X:")
        eixo_x = QComboBox(); eixo_x.addItems(colunas)
        lbl_y = QLabel("Eixo Y:")
        eixo_y = QComboBox(); eixo_y.addItems(colunas)
        lbl_t = QLabel("Tipo de Gráfico:")
        tipo = QComboBox(); tipo.addItems(["Barras", "Pizza", "Linha", "Dispersão", "3D"])

        # --- Campos adicionais ---
        lbl_z = QLabel("Eixo Z:"); eixo_z = QComboBox(); eixo_z.addItems(colunas)
        lbl_dx = QLabel("Eixo DX:"); eixo_dx = QComboBox(); eixo_dx.addItems(colunas)
        lbl_dy = QLabel("Eixo DY:"); eixo_dy = QComboBox(); eixo_dy.addItems(colunas)
        lbl_dz = QLabel("Eixo DZ:"); eixo_dz = QComboBox(); eixo_dz.addItems(colunas)

        for w in [lbl_z, eixo_z, lbl_dx, eixo_dx, lbl_dy, eixo_dy, lbl_dz, eixo_dz]:
            w.setVisible(False)

        # --- Botões e gráfico ---
        btn_gerar = QPushButton("Gerar Gráfico")
        fig, ax = plt.subplots(figsize=(5, 3))
        canvas = FigureCanvas(fig)
        btn_voltar = QPushButton("⬅ Voltar")
        btn_voltar.setVisible(False)
        btn_salvar_img = QPushButton("💾 Salvar Imagem")
        btn_salvar_img.setVisible(False)

        # --- Adiciona widgets ao layout ---
        for w in [lbl_x, eixo_x, lbl_y, eixo_y, lbl_t, tipo,
                lbl_z, eixo_z, lbl_dx, eixo_dx, lbl_dy, eixo_dy, lbl_dz, eixo_dz,
                btn_gerar, canvas, btn_voltar, btn_salvar_img]:
            layout.addWidget(w)

        controles = [lbl_x, eixo_x, lbl_y, eixo_y, lbl_t, tipo,
                    lbl_z, eixo_z, lbl_dx, eixo_dx, lbl_dy, eixo_dy, lbl_dz, eixo_dz, btn_gerar]

        # --- Exibição condicional dos campos ---
        def atualizar_campos():
            tipo_atual = tipo.currentText()
            for w in [lbl_y, eixo_y, lbl_z, eixo_z, lbl_dx, eixo_dx, lbl_dy, eixo_dy, lbl_dz, eixo_dz]:
                w.setVisible(False)

            if tipo_atual in ["Barras", "Linha"]:
                lbl_y.show(); eixo_y.show()
            elif tipo_atual == "Dispersão":
                lbl_y.show(); eixo_y.show()
                lbl_z.show(); eixo_z.show()
            elif tipo_atual == "3D":
                for w in [lbl_y, eixo_y, lbl_z, eixo_z, lbl_dx, eixo_dx, lbl_dy, eixo_dy, lbl_dz, eixo_dz]:
                    w.show()
            # Pizza usa apenas X, então não mostra Y

        tipo.currentTextChanged.connect(atualizar_campos)
        atualizar_campos()

        # --- Função para salvar gráfico como imagem ---
        def salvar_grafico_imagem():
            from PyQt5.QtWidgets import QFileDialog
            caminho, _ = QFileDialog.getSaveFileName(
                self, 
                "Salvar Gráfico", 
                "", 
                "PNG (*.png);;JPEG (*.jpg);;PDF (*.pdf)"
            )
            if caminho:
                try:
                    fig.savefig(caminho, dpi=300, bbox_inches='tight')
                    QMessageBox.information(self, "Sucesso", f"Gráfico salvo em:\n{caminho}")
                except Exception as e:
                    QMessageBox.warning(self, "Erro", f"Erro ao salvar imagem:\n{e}")

        btn_salvar_img.clicked.connect(salvar_grafico_imagem)

        # --- Animações ---
        def animar_widget(widget, aparecer=True, duracao=400):
            efeito = QGraphicsOpacityEffect()
            widget.setGraphicsEffect(efeito)
            anim = QPropertyAnimation(efeito, b"opacity")
            anim.setDuration(duracao)
            anim.setStartValue(0 if aparecer else 1)
            anim.setEndValue(1 if aparecer else 0)
            anim.start()
            if aparecer:
                widget.show()
            else:
                anim.finished.connect(widget.hide)

        def animar_grupo(grupo, aparecer=True):
            for w in grupo:
                animar_widget(w, aparecer)

        def modo_visualizacao():
            # esconde todos os controles e mostra apenas o gráfico e botão voltar
            animar_grupo(controles, aparecer=False)
            animar_widget(btn_voltar, aparecer=True)
            animar_widget(btn_salvar_img, aparecer=True)

        def modo_edicao():
            # restaura todos os controles
            animar_widget(btn_voltar, aparecer=False)
            animar_widget(btn_salvar_img, aparecer=False)
            animar_grupo(controles, aparecer=True)

        # --- Geração do gráfico ---
        def gerar():
            ax.clear()
            tipo_atual = tipo.currentText()
            x = eixo_x.currentText()
            y = eixo_y.currentText() if eixo_y.isVisible() else None
            df = self.df.copy()  # usa sempre o DataFrame mais recente

            try:
                if tipo_atual == "Barras":
                    ax.bar(df[x], df[y], color="#0077b6")
                elif tipo_atual == "Pizza":
                    ax.pie(df[x], autopct="%1.1f%%", startangle=90)
                    ax.axis("equal")
                elif tipo_atual == "Linha":
                    ax.plot(df[x], df[y], color="#0077b6", marker="o")
                elif tipo_atual == "Dispersão":
                    z = eixo_z.currentText()
                    ax.scatter(df[x], df[y], c=df[z] if z else "#00b4d8", cmap="viridis")
                elif tipo_atual == "3D":
                    from mpl_toolkits.mplot3d import Axes3D
                    fig3d = plt.figure(figsize=(5, 3))
                    ax3d = fig3d.add_subplot(111, projection="3d")
                    
                    # Converter valores para numérico quando possível
                    x_vals = np.arange(len(df[x]))
                    y_vals_data = pd.to_numeric(df[y], errors='coerce').fillna(0).values
                    
                    ax3d.bar3d(
                        x_vals,
                        np.zeros(len(x_vals)),
                        np.zeros(len(x_vals)),
                        0.5, 0.5, y_vals_data,
                        shade=True, color="#0077b6"
                    )
                    ax3d.set_xlabel(x)
                    ax3d.set_zlabel(y)
                    
                    new_canvas = FigureCanvas(fig3d)
                    layout.replaceWidget(canvas, new_canvas)
                    canvas.hide()
                    modo_visualizacao()
                    
                    # Desconectar handlers anteriores antes de conectar um novo
                    try:
                        btn_voltar.clicked.disconnect()
                    except:
                        pass
                    
                    btn_voltar.clicked.connect(lambda: [
                        layout.replaceWidget(new_canvas, canvas),
                        new_canvas.hide(),
                        canvas.show(),
                        modo_edicao()
                    ])
                    return

                ax.set_title(f"{tipo_atual} de {y or x} por {x}", fontsize=10, fontweight="bold")
                fig.tight_layout()
                canvas.draw()
                modo_visualizacao()  # ativa modo gráfico

            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao gerar gráfico:\n{e}")

        btn_gerar.clicked.connect(gerar)
        btn_voltar.clicked.connect(modo_edicao)

        return card



    # ------------------- TABELA -------------------
    def atualizar_tabela(self):
        if self.df.empty:
            self.tabela.setRowCount(0)
            self.tabela.setColumnCount(0)
            return
        
        self.tabela.setRowCount(len(self.df))
        self.tabela.setColumnCount(len(self.df.columns))
        self.tabela.setHorizontalHeaderLabels(self.df.columns)

        for i, row in self.df.iterrows():
            for j, col in enumerate(self.df.columns):
                item = QTableWidgetItem(str(row[col]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tabela.setItem(i, j, item)

        self.tabela.resizeColumnsToContents()
        self.tabela.resizeRowsToContents()

    def filtrar_tabela(self):
        """Filtra a tabela com base no texto de busca"""
        texto_busca = self.busca_input.text().lower()
        
        for i in range(self.tabela.rowCount()):
            match = False
            for j in range(self.tabela.columnCount()):
                item = self.tabela.item(i, j)
                if item and texto_busca in item.text().lower():
                    match = True
                    break
            self.tabela.setRowHidden(i, not match)

    # ------------------- CRUD -------------------
    def adicionar(self):
        self.df = adicionar_registro(self.df, self)
        self.arquivos_abertos[self.arquivo_atual] = self.df
        self.atualizar_tabela()
        self.atualizar_estatisticas()
        self.atualizar_combos_tendencia()

    def editar(self):
        linha = self.tabela.currentRow()
        if linha >= 0:
            self.df = editar_registro(self.df, linha, self)
            self.arquivos_abertos[self.arquivo_atual] = self.df
            self.atualizar_tabela()
            self.atualizar_estatisticas()
            self.atualizar_combos_tendencia()
        else:
            QMessageBox.warning(self, "Atenção", "Selecione uma linha para editar.")

    def remover(self):
        linha = self.tabela.currentRow()
        if linha >= 0:
            # Confirmação antes de remover
            resposta = QMessageBox.question(
                self, 
                "Confirmar Remoção", 
                "Tem certeza que deseja remover este registro?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if resposta == QMessageBox.Yes:
                self.df = remover_registro(self.df, linha)
                self.arquivos_abertos[self.arquivo_atual] = self.df
                self.atualizar_tabela()
                self.atualizar_estatisticas()
                self.atualizar_combos_tendencia()
                QMessageBox.information(self, "Sucesso", "Registro removido com sucesso.")
        else:
            QMessageBox.warning(self, "Atenção", "Selecione uma linha para remover.")

    def salvar(self):
        """Salva o arquivo no formato original"""
        import os
        
        # Detectar formato do arquivo atual
        if self.arquivo_atual.lower().endswith(('.xlsx', '.xls')):
            # Salvar como Excel
            try:
                self.df.to_excel(self.arquivo_atual, index=False, engine='openpyxl')
                QMessageBox.information(self, "Sucesso", "Arquivo Excel salvo com sucesso.")
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao salvar Excel:\n{e}")
        else:
            # Salvar como CSV
            salvar_csv(self.df, self.arquivo_atual)
            QMessageBox.information(self, "Sucesso", "Arquivo CSV salvo com sucesso.")

    def salvar_como(self):
        """Salva o arquivo em um novo formato (CSV ou Excel)"""
        from PyQt5.QtWidgets import QFileDialog
        import os
        
        arquivo, tipo_selecionado = QFileDialog.getSaveFileName(
            self,
            "Salvar Como",
            "",
            "Arquivo CSV (*.csv);;Arquivo Excel (*.xlsx)"
        )
        
        if not arquivo:
            return
        
        try:
            if "Excel" in tipo_selecionado or arquivo.lower().endswith('.xlsx'):
                # Garantir extensão .xlsx
                if not arquivo.lower().endswith('.xlsx'):
                    arquivo += '.xlsx'
                self.df.to_excel(arquivo, index=False, engine='openpyxl')
                QMessageBox.information(self, "Sucesso", f"Arquivo Excel salvo em:\n{arquivo}")
            else:
                # Garantir extensão .csv
                if not arquivo.lower().endswith('.csv'):
                    arquivo += '.csv'
                self.df.to_csv(arquivo, index=False)
                QMessageBox.information(self, "Sucesso", f"Arquivo CSV salvo em:\n{arquivo}")
                
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao salvar arquivo:\n{e}")

    def abrir_arquivo_csv(self):
        from PyQt5.QtWidgets import QFileDialog
        import json, os

        arquivo, _ = QFileDialog.getOpenFileName(self, "Abrir CSV", "", "Arquivos CSV (*.csv)")
        if not arquivo:
            return

        try:
            self.df = carregar_csv(arquivo)
            self.arquivo_atual = arquivo
            nome = os.path.basename(arquivo)

            # Atualiza título
            self.setWindowTitle(f"📊 Dashboard de Análise - {nome}")

            # 🔄 Limpa gráficos antigos
            for i in reversed(range(self.layout_graficos.count())):
                widget = self.layout_graficos.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            self.cards.clear()

            # 🔄 Atualiza tabela
            if hasattr(self, "tabela"):
                self.atualizar_tabela()
            
            # 🔄 Atualiza estatísticas
            if hasattr(self, "atualizar_estatisticas"):
                self.atualizar_estatisticas()

            # Salva arquivo atual
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump({"ultimo_csv": arquivo}, f, ensure_ascii=False, indent=2)

            QMessageBox.information(self, "Sucesso", f"Arquivo '{nome}' carregado com sucesso!")

        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Falha ao carregar o arquivo:\n{e}")

    # ------------------- GERENCIAMENTO DE MÚLTIPLOS ARQUIVOS -------------------
    def atualizar_lista_arquivos(self):
        """Atualiza a lista de arquivos abertos"""
        self.lista_arquivos.clear()
        for caminho in self.arquivos_abertos.keys():
            import os
            nome = os.path.basename(caminho)
            item_text = f"{'🟢' if caminho == self.arquivo_atual else '⚪'} {nome}"
            self.lista_arquivos.addItem(item_text)

    def adicionar_novo_arquivo(self):
        """Adiciona um novo arquivo CSV ou Excel à lista"""
        from PyQt5.QtWidgets import QFileDialog
        import os
        
        arquivo, _ = QFileDialog.getOpenFileName(
            self, 
            "Abrir Arquivo", 
            "", 
            "Todos os Arquivos Suportados (*.csv *.xlsx *.xls);;Arquivos CSV (*.csv);;Arquivos Excel (*.xlsx *.xls)"
        )
        if not arquivo:
            return
        
        try:
            df = carregar_csv(arquivo)
            self.arquivos_abertos[arquivo] = df
            self.arquivo_atual = arquivo
            self.df = df
            
            # Atualiza interface
            self.atualizar_lista_arquivos()
            self.atualizar_tabela()
            self.atualizar_estatisticas()
            self.atualizar_combos_tendencia()
            
            nome = os.path.basename(arquivo)
            tipo = "Excel" if arquivo.lower().endswith(('.xlsx', '.xls')) else "CSV"
            QMessageBox.information(self, "Sucesso", f"Arquivo {tipo} '{nome}' adicionado!")
            
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Falha ao carregar:\n{e}")

    def trocar_arquivo_ativo(self, item):
        """Troca o arquivo ativo ao clicar na lista"""
        index = self.lista_arquivos.row(item)
        caminho = list(self.arquivos_abertos.keys())[index]
        
        self.arquivo_atual = caminho
        self.df = self.arquivos_abertos[caminho]
        
        # Atualiza interface
        self.atualizar_lista_arquivos()
        self.atualizar_tabela()
        self.atualizar_estatisticas()
        self.atualizar_combos_tendencia()

    # ------------------- BANCO DE DADOS -------------------
    def conectar_banco(self):
        """Conecta ou cria um banco de dados SQLite"""
        import sqlite3
        from PyQt5.QtWidgets import QFileDialog
        
        arquivo, _ = QFileDialog.getSaveFileName(
            self, 
            "Conectar/Criar Banco de Dados", 
            "vendas.db",
            "SQLite Database (*.db)"
        )
        
        if not arquivo:
            return
        
        try:
            self.conexao_bd = sqlite3.connect(arquivo)
            self.caminho_bd = arquivo
            self.label_status_bd.setText(f"🟢 Conectado: {arquivo}")
            self.label_status_bd.setStyleSheet("font-size: 14px; padding: 10px; background-color: #d4edda; border-radius: 6px; color: #155724;")
            
            # Criar tabela se não existir
            cursor = self.conexao_bd.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vendas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Data TEXT,
                    Produto TEXT,
                    Quantidade REAL,
                    PrecoUnitario REAL,
                    Total REAL
                )
            """)
            self.conexao_bd.commit()
            
            QMessageBox.information(self, "Sucesso", "Banco de dados conectado com sucesso!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao conectar ao banco:\n{e}")

    def importar_csv_para_bd(self):
        """Importa dados do CSV atual para o banco de dados"""
        if not self.conexao_bd:
            QMessageBox.warning(self, "Aviso", "Conecte-se a um banco de dados primeiro!")
            return
        
        if self.df.empty:
            QMessageBox.warning(self, "Aviso", "Não há dados para importar!")
            return
        
        try:
            # Adiciona coluna Total se não existir
            df_temp = self.df.copy()
            if 'Quantidade' in df_temp.columns and 'PrecoUnitario' in df_temp.columns:
                df_temp['Total'] = pd.to_numeric(df_temp['Quantidade'], errors='coerce') * \
                                   pd.to_numeric(df_temp['PrecoUnitario'], errors='coerce')
            
            df_temp.to_sql('vendas', self.conexao_bd, if_exists='append', index=False)
            self.conexao_bd.commit()
            
            QMessageBox.information(self, "Sucesso", f"{len(df_temp)} registros importados para o banco!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao importar:\n{e}")

    def exportar_bd_para_csv(self):
        """Exporta dados do banco para o DataFrame atual"""
        if not self.conexao_bd:
            QMessageBox.warning(self, "Aviso", "Conecte-se a um banco de dados primeiro!")
            return
        
        try:
            self.df = pd.read_sql_query("SELECT * FROM vendas", self.conexao_bd)
            self.atualizar_tabela()
            self.atualizar_estatisticas()
            
            QMessageBox.information(self, "Sucesso", "Dados exportados do banco para o DataFrame!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao exportar:\n{e}")

    def executar_consulta_sql(self):
        """Executa uma consulta SQL personalizada"""
        if not self.conexao_bd:
            QMessageBox.warning(self, "Aviso", "Conecte-se a um banco de dados primeiro!")
            return
        
        consulta = self.sql_input.toPlainText().strip()
        if not consulta:
            QMessageBox.warning(self, "Aviso", "Digite uma consulta SQL!")
            return
        
        try:
            df_resultado = pd.read_sql_query(consulta, self.conexao_bd)
            
            # Exibir resultado na tabela
            self.tabela_bd.setRowCount(len(df_resultado))
            self.tabela_bd.setColumnCount(len(df_resultado.columns))
            self.tabela_bd.setHorizontalHeaderLabels(df_resultado.columns)
            
            for i, row in df_resultado.iterrows():
                for j, col in enumerate(df_resultado.columns):
                    item = QTableWidgetItem(str(row[col]))
                    self.tabela_bd.setItem(i, j, item)
            
            self.tabela_bd.resizeColumnsToContents()
            
            QMessageBox.information(self, "Sucesso", f"Consulta executada! {len(df_resultado)} registros retornados.")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro na consulta SQL:\n{e}")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open("estilo.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except:
        pass

    janela = InterfaceVendas()
    janela.show()
    sys.exit(app.exec_())
