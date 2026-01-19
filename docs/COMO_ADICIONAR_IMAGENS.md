# 📸 Como Adicionar as Imagens ao README

## Passos para adicionar suas capturas de tela:

### 1. Salve os screenshots
Você já tirou as capturas de tela. Agora salve cada uma com os seguintes nomes:

- **banco_dados.png** - Captura da aba "Banco de Dados" com o console SQL
- **dados.png** - Captura da aba "Dados" mostrando a tabela com registros
- **analise_tendencia.png** - Captura do Dashboard com o gráfico de tendência temporal

### 2. Coloque as imagens na pasta correta
Mova ou copie as imagens para:
```
analise_vendas/docs/images/
```

A estrutura deve ficar assim:
```
analise_vendas/
├── docs/
│   └── images/
│       ├── banco_dados.png
│       ├── dados.png
│       └── analise_tendencia.png
├── main.py
├── README.md
└── ...
```

### 3. Verifique se as imagens estão corretas
As imagens devem corresponder a:

- **analise_tendencia.png**: Dashboard mostrando o gráfico "Tendência de Valor ao Longo do Tempo"
- **dados.png**: Tabela com múltiplas colunas (datetime, ano, mês, dia, hora, etc)
- **banco_dados.png**: Interface do SQLite com console de queries

### 4. Faça o commit no GitHub

```bash
git add .
git commit -m "Adiciona screenshots e README atualizado"
git push origin main
```

### 5. Pronto!
As imagens aparecerão automaticamente no README do GitHub! 🎉

## Dicas:

- **Tamanho recomendado**: 1200-1920px de largura para melhor visualização
- **Formato**: PNG para melhor qualidade
- **Resolução**: Capturas em alta resolução (não amplie imagens pequenas)
- **Corte**: Remova bordas desnecessárias antes de salvar

## Se as imagens não aparecerem no GitHub:

1. Verifique se os nomes dos arquivos estão exatamente como especificado (sensível a maiúsculas/minúsculas)
2. Confirme que a pasta `docs/images/` foi incluída no commit
3. Aguarde alguns segundos para o GitHub processar as imagens
