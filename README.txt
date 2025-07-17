Projeto de Análise de Vendas - Instruções básicas.
===========================
ANÁLISE DE VENDAS - PyQt5
===========================

🔧 REQUISITOS:
--------------
- Python 3.8 ou superior
- Bibliotecas:
    pip install pyqt5 pandas matplotlib fpdf openpyxl xlsxwriter

📁 ESTRUTURA DO PROJETO:
------------------------
main.py
estilo.qss
vendas.csv
modulos/
├── graficos.py
├── funcoes_csv.py
└── exportar.py

📊 FUNCIONALIDADES:
-------------------
- Visualiza e filtra vendas a partir de arquivo CSV
- Mostra gráfico de faturamento por produto
- Permite adicionar, editar e remover vendas
- Exporta dados para Excel (.xlsx) e PDF (.pdf)

▶️ COMO EXECUTAR:
-----------------
1. Garanta que o arquivo vendas.csv esteja na pasta
2. Execute o sistema com:
    python main.py

🖥 COMO GERAR O .EXE:
---------------------
1. Instale o PyInstaller:
    pip install pyinstaller

2. Execute o comando abaixo na pasta do projeto:
    pyinstaller --onefile --windowed --icon=icon.ico main.py

3. O executável estará na pasta:
    dist/main.exe

🎯 DICA:
--------
Você pode personalizar o ícone com qualquer arquivo .ico
e alterar o estilo da interface editando o arquivo estilo.qss

