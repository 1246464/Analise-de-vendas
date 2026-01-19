# 📋 Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

---

## [2.1.0] - 2026-01-19

### 🎉 Suporte a Arquivos Excel

#### ✨ Adicionado
- **Leitura de Arquivos Excel**: Suporte completo para arquivos .xlsx e .xls
- **Conversão de Formatos**: 
  - Abrir Excel e salvar como CSV
  - Abrir CSV e salvar como Excel
  - Função "Salvar Como..." com seleção de formato
- **Detecção Automática**: O sistema identifica o formato e usa o método adequado
- **Botão "Abrir Arquivo"**: Substitui "Abrir CSV" com suporte para múltiplos formatos
- **Script de Exemplo**: `criar_excel_exemplo.py` para gerar arquivo de teste

#### 🎨 Melhorado
- Diálogos de abertura agora mostram filtros para CSV e Excel
- Função `carregar_csv()` renomeada conceitualmente mas mantém compatibilidade
- Mensagens de sucesso indicam o tipo de arquivo carregado
- Função de salvar detecta formato original automaticamente
- Label do gerenciador atualizado para "Arquivos Abertos (CSV/Excel)"

#### 📚 Documentação
- README.md atualizado com informações sobre Excel
- Exemplos de uso com arquivos Excel
- Instruções de conversão entre formatos

---

## [2.0.0] - 2026-01-19

### 🎉 Grandes Melhorias para Portfólio

#### ✨ Adicionado
- **Sistema de Abas**: Interface organizada em 3 abas (Dashboard, Dados, Banco de Dados)
- **Múltiplos Arquivos CSV**: Suporte para abrir e alternar entre vários arquivos simultaneamente
- **Gerenciador de Arquivos**: Lista visual com indicador de arquivo ativo
- **Banco de Dados SQLite**:
  - Conexão e criação de banco de dados
  - Importação de CSV para banco
  - Exportação de banco para CSV
  - Console SQL para consultas personalizadas
- **Análise de Tendência Temporal**:
  - Gráfico de linha com área preenchida
  - Linha de tendência (regressão linear)
  - Seleção dinâmica de colunas
- **Exportação de Gráficos**: Salvar gráficos individuais como PNG, JPEG ou PDF (300 DPI)
- **Documentação Completa**:
  - README.md profissional
  - requirements.txt
  - BUILD_GUIDE.md
  - build_exe.spec para PyInstaller

#### 🎨 Melhorado
- Design visual modernizado com gradientes
- Paleta de cores profissional (#0077b6, #00b4d8, #90e0ef)
- Estilo CSS aprimorado para todos os componentes
- Animações mais suaves
- Interface mais responsiva

#### 🐛 Corrigido
- Declaração `nonlocal` desnecessária em graficos.py
- Importações duplicadas em funcoes_csv.py
- Validação de DataFrame vazio
- Tratamento de erros melhorado
- Conversão de tipos em gráficos 3D

---

## [1.1.0] - 2026-01-19

### ✨ Adicionado
- **Painel de Estatísticas**: Cards com métricas (Total, Soma, Média, Máximo)
- **Sistema de Busca**: Filtro em tempo real na tabela
- **Confirmação de Remoção**: Diálogo antes de excluir registros
- **Validações de Dados**: Verificação de CSV vazio, arquivo não encontrado

#### 🎨 Melhorado
- Estilo visual com bordas arredondadas
- Hover effects em botões e tabela
- Mensagens de erro mais descritivas

---

## [1.0.0] - Data Inicial

### ✨ Funcionalidades Iniciais
- Interface gráfica com PyQt5
- CRUD completo (Create, Read, Update, Delete)
- Visualização de dados em tabela
- Múltiplos tipos de gráficos:
  - Barras
  - Pizza
  - Linha
  - Dispersão
  - 3D
- Até 4 gráficos personalizáveis simultaneamente
- Exportação para Excel
- Exportação para PDF
- Leitura e escrita de CSV
- Persistência do último arquivo usado
- Modularização do código (módulos separados)
- Estilo CSS customizado

---

## 🔮 Roadmap - Próximas Versões

### [2.1.0] - Planejado
- [ ] Temas claro/escuro
- [ ] Gráficos de dispersão com clusters (K-means)
- [ ] Previsão com machine learning (regressão linear)
- [ ] Comparação entre múltiplos arquivos
- [ ] Dashboard customizável (arrastar e soltar widgets)

### [2.2.0] - Planejado
- [ ] Conexão com SQL Server / MySQL
- [ ] API REST para integração externa
- [ ] Agendamento de relatórios
- [ ] Notificações por email
- [ ] Logs de auditoria

### [3.0.0] - Futuro
- [ ] Versão Web (Flask/Django)
- [ ] App mobile (Kivy)
- [ ] Autenticação de usuários
- [ ] Permissões e roles
- [ ] Backup em nuvem

---

## 📝 Formato

Este changelog segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

### Tipos de Mudanças
- **Adicionado** - Novas funcionalidades
- **Alterado** - Mudanças em funcionalidades existentes
- **Obsoleto** - Funcionalidades que serão removidas
- **Removido** - Funcionalidades removidas
- **Corrigido** - Correções de bugs
- **Segurança** - Vulnerabilidades corrigidas
