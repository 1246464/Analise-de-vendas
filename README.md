# 📊 Dashboard de Análise de Vendas

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Sistema completo de análise e visualização de dados de vendas com interface gráfica moderna**

[Características](#-características) • [Instalação](#-instalação) • [Como Usar](#-como-usar) • [Screenshots](#-capturas-de-tela)

</div>

---

## 📸 Capturas de Tela

### Dashboard com Análise de Tendência Temporal
![Dashboard Análise](docs/images/analise_tendencia.png)
*Visualize tendências de dados ao longo do tempo com linha de tendência e área sombreada*

### Gerenciamento de Dados
![Dados e Tabelas](docs/images/dados.png)
*Gerencie múltiplos arquivos CSV/Excel com busca em tempo real e operações CRUD completas*

### Banco de Dados SQLite
![Console SQL](docs/images/banco_dados.png)
*Execute consultas SQL personalizadas e sincronize dados entre CSV e banco de dados*

---

## 🎯 Sobre o Projeto

Dashboard profissional desenvolvido em Python para análise de dados de vendas, oferecendo uma interface intuitiva e recursos avançados de visualização, gerenciamento de múltiplos arquivos CSV e integração com banco de dados SQLite.

### ✨ Características

#### 📊 **Dashboard Interativo**
- **Estatísticas em Tempo Real**: Cards visuais com métricas instantâneas (total, média, máximo)
- **Gráficos Personalizáveis**: Até 4 gráficos simultâneos (Barras, Pizza, Linha, Dispersão, 3D)
- **Análise de Tendência Temporal**: Visualização de tendências com linha de regressão
- **Exportação de Gráficos**: Salve gráficos em PNG, JPEG ou PDF (300 DPI)

#### 📁 **Gerenciamento de Dados**
- **Múltiplos Arquivos**: Abra e alterne entre vários arquivos CSV e Excel simultaneamente
- **Formatos Suportados**: CSV (.csv), Excel (.xlsx, .xls)
- **CRUD Completo**: Adicione, edite e remova registros com interface intuitiva
- **Busca em Tempo Real**: Filtro instantâneo em todas as colunas
- **Validação de Dados**: Verificação automática de tipos e valores
- **Conversão de Formatos**: Salve CSV como Excel e vice-versa

#### 🗄️ **Banco de Dados**
- **SQLite Integrado**: Conexão e gerenciamento de banco de dados
- **Importação/Exportação**: Sincronize dados entre CSV e banco
- **Console SQL**: Execute consultas SQL personalizadas
- **Backup Automático**: Persistência de dados confiável

#### 🎨 **Interface Moderna**
- **Design Profissional**: Paleta de cores harmoniosa e gradientes suaves
- **Animações Fluídas**: Transições suaves entre modos de visualização
- **Sistema de Abas**: Organização clara (Dashboard, Dados, Banco de Dados)
- **Responsivo**: Interface adaptável e intuitiva

#### 📤 **Exportação**
- **Excel**: Exportação formatada em .xlsx
- **PDF**: Relatórios profissionais com tabelas
- **Imagens**: Gráficos de alta qualidade

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone ou baixe o projeto**
```bash
git clone https://github.com/seu-usuario/analise-vendas.git
cd analise-vendas
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

Se não houver `requirements.txt`, instale manualmente:
```bash
pip install PyQt5 pandas numpy matplotlib openpyxl fpdf
```

3. **Execute o aplicativo**
```bash
python main.py
```

---

## 📖 Como Usar

### 1️⃣ Abrir Arquivos

**Aba Dados > Arquivos Abertos > ➕ Abrir Arquivo**

- Selecione um ou mais arquivos CSV (.csv) ou Excel (.xlsx, .xls)
- Alterne entre arquivos clicando na lista
- O arquivo ativo é indicado com 🟢
- Suporte para conversão automática entre formatos

### 2️⃣ Visualizar Dados

**Aba Dashboard**

- Veja estatísticas instantâneas no topo
- Clique em **➕ Adicionar Gráfico** (até 4 gráficos)
- Selecione eixos X, Y e tipo de gráfico
- Clique em **Gerar Gráfico**
- Use **💾 Salvar Imagem** para exportar

### 3️⃣ Analisar Tendências

**Aba Dashboard > Análise de Tendência Temporal**

1. Selecione a coluna de data
2. Selecione a coluna de valores
3. Clique em **📊 Gerar Análise**
4. Visualize a tendência com linha de regressão

### 4️⃣ Gerenciar Registros

**Aba Dados**

- **➕ Adicionar**: Crie novos registros
- **📝 Editar**: Modifique registros existentes
- **❌ Remover**: Exclua com confirmação
- **💾 Salvar**: Persista alterações no formato original (CSV ou Excel)
- **💾 Salvar Como**: Converta e salve em CSV ou Excel
- **🔍 Buscar**: Filtro em tempo real

### 5️⃣ Trabalhar com Banco de Dados

**Aba Banco de Dados**

1. **🔌 Conectar/Criar BD**: Escolha ou crie um arquivo .db
2. **📥 Importar CSV → BD**: Transfira dados do CSV atual
3. **📤 Exportar BD → CSV**: Carregue dados do banco
4. **🔍 Consultar SQL**: Execute queries personalizadas

**Exemplo de Consulta SQL:**
```sql
SELECT Data, SUM(Quantidade * PrecoUnitario) as Total
FROM vendas
WHERE Data >= '2024-01-01'
GROUP BY Data
ORDER BY Data DESC;
```

### 6️⃣ Exportar Dados

**Aba Dashboard**

- **📤 Exportar Excel**: Gera arquivo .xlsx
- **🖨 Exportar PDF**: Cria relatório em PDF
- **💾 Salvar Imagem**: Exporta gráficos individuais

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|------------|-----|
| **Python 3.8+** | Linguagem principal |
| **PyQt5** | Interface gráfica (GUI) |
| **Pandas** | Manipulação de dados |
| **NumPy** | Operações numéricas |
| **Matplotlib** | Visualização de gráficos |
| **SQLite3** | Banco de dados integrado |
| **OpenPyXL** | Exportação Excel |
| **FPDF** | Geração de PDF |

---

## 📁 Estrutura do Projeto

```
analise_vendas/
│
├── main.py                 # Aplicação principal
├── config.json             # Configurações (último arquivo usado)
├── estilo.qss              # Folha de estilos CSS
├── vendas.csv              # Dados de exemplo
│
├── modulos/
│   ├── exportar.py         # Funções de exportação (Excel, PDF)
│   ├── funcoes_csv.py      # CRUD e manipulação de CSV
│   └── graficos.py         # Funções auxiliares de gráficos
│
├── build/                  # Arquivos de build (PyInstaller)
└── README.md               # Documentação
```

---

## 💡 Recursos Avançados

### Tipos de Gráficos Suportados

1. **Barras**: Comparação de categorias
2. **Pizza**: Proporções e percentuais
3. **Linha**: Evolução temporal
4. **Dispersão**: Correlação entre variáveis (com eixo Z colorido)
5. **3D**: Visualização tridimensional com eixos DX, DY, DZ

### Atalhos e Dicas

- ⚡ **Busca Rápida**: Digite na caixa de busca para filtrar instantaneamente
- 🔄 **Atualização Automática**: Estatísticas atualizam ao modificar dados
- 💾 **Auto-Save**: Último arquivo usado é lembrado automaticamente
- ⚠️ **Confirmações**: Diálogos de segurança antes de ações destrutivas

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abrir um Pull Request

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👤 Autor

**Maicon**

- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [seu-perfil](https://linkedin.com/in/seu-perfil)

---

## 🎓 Aprendizados

Este projeto demonstra:

- ✅ Arquitetura MVC em Python
- ✅ Interface gráfica profissional com PyQt5
- ✅ Manipulação avançada de dados com Pandas
- ✅ Visualização interativa com Matplotlib
- ✅ Integração com banco de dados
- ✅ Boas práticas de desenvolvimento
- ✅ Modularização e organização de código

---

## 📸 Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Gerenciamento de Dados
![Dados](screenshots/dados.png)

### Banco de Dados
![Banco](screenshots/banco.png)

---

## 🆘 Suporte

Encontrou um bug ou tem uma sugestão? 

- Abra uma [Issue](https://github.com/seu-usuario/analise-vendas/issues)
- Entre em contato via email: seu-email@exemplo.com

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

Desenvolvido com ❤️ em Python

</div>
