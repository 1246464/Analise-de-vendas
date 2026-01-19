# 🚀 Guia de Build - Criar Executável

## Como Gerar o Executável (.exe)

### 1. Instalar PyInstaller

```bash
pip install pyinstaller
```

### 2. Gerar o Executável

**Opção 1 - Usando o arquivo .spec (Recomendado):**

```bash
pyinstaller build_exe.spec
```

**Opção 2 - Comando direto:**

```bash
pyinstaller --name="DashboardVendas" ^
            --onefile ^
            --windowed ^
            --add-data "estilo.qss;." ^
            --add-data "vendas.csv;." ^
            --add-data "modulos;modulos" ^
            --hidden-import="PyQt5" ^
            --hidden-import="pandas" ^
            --hidden-import="matplotlib" ^
            main.py
```

### 3. Localizar o Executável

Após a compilação bem-sucedida:

- **Executável**: `dist/DashboardVendas.exe`
- **Build temporário**: `build/` (pode ser deletado)

### 4. Testar o Executável

```bash
cd dist
.\DashboardVendas.exe
```

---

## 📦 Criar Instalador (Opcional)

### Usando Inno Setup

1. **Baixe o Inno Setup**: https://jrsoftware.org/isdl.php

2. **Abra o arquivo `install.iss`** que já está no projeto

3. **Compile**:
   - No Inno Setup Compiler: Build > Compile
   - Ou via linha de comando:
   ```bash
   iscc install.iss
   ```

4. O instalador será criado em `Output/Setup_DashboardVendas.exe`

---

## ⚙️ Configurações Avançadas

### Adicionar Ícone

1. Crie ou baixe um arquivo `.ico`
2. Edite `build_exe.spec`:
   ```python
   icon='icone.ico'
   ```

### Reduzir Tamanho do Executável

Edite `build_exe.spec` e adicione:

```python
excludes=[
    'tkinter',
    'test',
    'unittest',
    'email',
    'xml',
    'pydoc',
]
```

### Múltiplos Arquivos (ao invés de --onefile)

Troque no .spec:

```python
exe = EXE(
    pyz,
    a.scripts,
    # NÃO incluir a.binaries, a.zipfiles, a.datas aqui
    ...
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='DashboardVendas'
)
```

---

## 🐛 Solução de Problemas

### Erro: "Failed to execute script"

**Solução**: Remova `console=False` temporariamente para ver o erro

```python
console=True
```

### Erro: Módulos não encontrados

**Solução**: Adicione em `hiddenimports`:

```python
hiddenimports=[
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    # outros módulos...
]
```

### Erro: Arquivos de dados não encontrados

**Solução**: Verifique `datas` no .spec:

```python
datas=[
    ('estilo.qss', '.'),
    ('vendas.csv', '.'),
],
```

### Antivírus bloqueia o .exe

**Normal**: PyInstaller executáveis são frequentemente sinalizados como falso-positivo.

**Soluções**:
1. Adicione exceção no antivírus
2. Assine digitalmente o executável (requer certificado)

---

## 📊 Tamanhos Esperados

- **Executável único**: ~80-120 MB
- **Múltiplos arquivos**: ~50-70 MB + DLLs
- **Instalador**: ~60-90 MB (compactado)

---

## ✅ Checklist de Distribuição

- [ ] Testado o executável em máquina limpa (sem Python)
- [ ] Todos os arquivos de dados incluídos
- [ ] Ícone personalizado adicionado
- [ ] README.md atualizado com instruções
- [ ] Versão documentada
- [ ] Testado em Windows 10/11
- [ ] Instalador funcionando corretamente

---

## 📝 Notas

- O primeiro build pode demorar alguns minutos
- Builds subsequentes são mais rápidos
- O executável só funciona no mesmo OS onde foi compilado
- Para Linux/Mac, compile em cada plataforma respectiva

---

## 🔗 Links Úteis

- [Documentação PyInstaller](https://pyinstaller.readthedocs.io/)
- [Inno Setup Documentation](https://jrsoftware.org/ishelp/)
- [PyQt5 Deployment](https://www.riverbankcomputing.com/static/Docs/PyQt5/deploy.html)
