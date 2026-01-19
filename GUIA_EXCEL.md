# 📊 Guia: Trabalhando com Arquivos Excel

## 🎯 Formatos Suportados

O Dashboard agora suporta os seguintes formatos de arquivo:

- ✅ **CSV** (.csv) - Valores separados por vírgula
- ✅ **Excel 2007+** (.xlsx) - Formato moderno do Excel
- ✅ **Excel 97-2003** (.xls) - Formato legado do Excel

---

## 📂 Como Abrir Arquivos Excel

### Método 1: Aba Dashboard
1. Clique em **📂 Abrir Arquivo**
2. Selecione o filtro "Arquivos Excel (*.xlsx *.xls)" ou "Todos os Arquivos Suportados"
3. Escolha seu arquivo Excel
4. Os dados serão carregados automaticamente

### Método 2: Aba Dados
1. Vá para a aba **📁 Dados**
2. No painel "Arquivos Abertos (CSV/Excel)"
3. Clique em **➕ Abrir Arquivo**
4. Selecione seu arquivo Excel

---

## 🔄 Conversão Entre Formatos

### Excel → CSV

1. Abra seu arquivo Excel
2. Faça suas edições (opcional)
3. Clique em **💾 Salvar Como...**
4. Selecione "Arquivo CSV (*.csv)"
5. Escolha o nome e local
6. Clique em **Salvar**

### CSV → Excel

1. Abra seu arquivo CSV
2. Faça suas edições (opcional)
3. Clique em **💾 Salvar Como...**
4. Selecione "Arquivo Excel (*.xlsx)"
5. Escolha o nome e local
6. Clique em **Salvar**

---

## 💡 Dicas e Boas Práticas

### ✅ Compatibilidade
- Arquivos .xlsx são recomendados (formato mais moderno)
- Arquivos .xls (Excel 97-2003) também funcionam perfeitamente
- A estrutura de dados deve ser tabular (linhas e colunas)

### ✅ Preparação de Dados Excel
Antes de importar seu arquivo Excel, certifique-se de que:

1. **Primeira linha contém os cabeçalhos**
   ```
   Data | Produto | Quantidade | PrecoUnitario
   ```

2. **Sem células mescladas** na área de dados

3. **Sem formatações complexas** (macros, fórmulas complexas)

4. **Uma planilha por vez** (a primeira planilha será lida)

### ✅ Múltiplas Planilhas
Se seu arquivo Excel tem múltiplas planilhas:
- Apenas a **primeira planilha** será lida
- Para outras planilhas, considere:
  - Copiar para novo arquivo Excel
  - Ou exportar cada planilha como CSV separado

---

## 🔧 Funcionalidades Específicas para Excel

### Salvar no Formato Original
- Use **💾 Salvar** para manter o formato original
- Se abriu .xlsx, salvará como .xlsx
- Se abriu .csv, salvará como .csv

### Trabalhar com Múltiplos Arquivos
Você pode ter abertos simultaneamente:
- ✅ 2 arquivos CSV
- ✅ 2 arquivos Excel
- ✅ 1 CSV + 1 Excel
- ✅ Quantos arquivos precisar!

Alterne entre eles clicando na lista de arquivos.

---

## 📊 Recursos Disponíveis para Excel

Todos os recursos funcionam perfeitamente com Excel:

- ✅ Visualização em tabela
- ✅ Gráficos (todos os tipos)
- ✅ Análise de tendência temporal
- ✅ Estatísticas descritivas
- ✅ Busca e filtros
- ✅ CRUD (adicionar, editar, remover)
- ✅ Exportação para PDF
- ✅ Importação para banco de dados SQLite

---

## 🐛 Solução de Problemas

### Erro: "Não foi possível carregar o arquivo"

**Possíveis causas:**
1. Arquivo corrompido
2. Arquivo protegido por senha
3. Formato não suportado

**Soluções:**
1. Abra no Excel e salve como novo arquivo
2. Remova a proteção por senha
3. Converta para .xlsx ou .csv

### Caracteres Especiais Aparecem Errados

**Causa:** Problema de encoding

**Solução:**
1. Abra o Excel original
2. Salve como "CSV UTF-8"
3. Importe no Dashboard

### Datas não Reconhecidas

**Causa:** Formato de data não padrão

**Solução:**
No Excel, formate as datas como:
- `YYYY-MM-DD` (ex: 2024-01-15)
- `DD/MM/YYYY` (ex: 15/01/2024)

---

## 📝 Exemplo de Estrutura Ideal

### Arquivo Excel Recomendado:

| Data       | Produto  | Quantidade | PrecoUnitario |
|------------|----------|------------|---------------|
| 2024-01-15 | Notebook | 5          | 3500.00       |
| 2024-01-16 | Mouse    | 20         | 45.50         |
| 2024-01-17 | Teclado  | 15         | 120.00        |
| 2024-01-18 | Monitor  | 8          | 890.00        |
| 2024-01-19 | Webcam   | 12         | 250.00        |

### Como Criar:

Execute o script incluído:
```bash
python criar_excel_exemplo.py
```

Isso criará `vendas_exemplo.xlsx` com dados de teste!

---

## 🎓 Recursos Técnicos

### Bibliotecas Utilizadas
- **pandas**: Leitura e manipulação de dados
- **openpyxl**: Engine para arquivos .xlsx
- **xlrd**: Suporte para arquivos .xls legados (opcional)

### Limitações Conhecidas
- Arquivos Excel muito grandes (>100MB) podem demorar para carregar
- Fórmulas do Excel não são mantidas (apenas valores)
- Formatações (cores, bordas) não são preservadas
- Gráficos do Excel não são importados

---

## ✨ Novos Recursos em Desenvolvimento

- [ ] Seleção de planilha específica em arquivos multi-sheet
- [ ] Importação de fórmulas do Excel
- [ ] Exportação mantendo formatações
- [ ] Suporte para arquivos .xlsm (com macros)
- [ ] Preview antes de importar

---

## 📞 Suporte

Problemas com arquivos Excel? 
- Abra uma [Issue no GitHub](https://github.com/seu-usuario/analise-vendas/issues)
- Envie seu arquivo de exemplo (sem dados sensíveis)

---

**Aproveite o novo suporte a Excel! 🎉**
