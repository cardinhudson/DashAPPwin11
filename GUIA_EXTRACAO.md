# 📚 GUIA COMPLETO DE EXTRAÇÃO DE DADOS - Dashboard KE5Z

## 📋 ÍNDICE
1. [Visão Geral](#visão-geral)
2. [Estrutura de Arquivos](#estrutura-de-arquivos)
3. [Processamento KE5Z](#processamento-ke5z)
4. [Processamento KSBB](#processamento-ksbb)
5. [Relacionamentos e Merges](#relacionamentos-e-merges)
6. [Padronização de Colunas](#padronização-de-colunas)
7. [Arquivos Auxiliares](#arquivos-auxiliares)
8. [Arquivos de Saída](#arquivos-de-saída)
9. [Fluxo Completo](#fluxo-completo)
10. [Tratamento de Erros](#tratamento-de-erros)

---

## 🎯 VISÃO GERAL

O script `Extracao.py` é responsável por:
- **Carregar** dados de múltiplas fontes (KE5Z, KSBB, SAPIENS, Fornecedores)
- **Processar** e **normalizar** dados de diferentes formatos
- **Unificar** informações através de merges por chaves comuns
- **Gerar** arquivos Parquet e Excel otimizados para uso no dashboard

### Fluxo Principal:
```
KE5Z (.txt) → Processamento → Merge com KSBB → Merge com SAPIENS → Merge com Fornecedores → Arquivos de Saída
```

---

## 📁 ESTRUTURA DE ARQUIVOS

### Diretórios de Entrada
```
Extracoes/
├── KE5Z/          # Arquivos de dados KE5Z (.txt)
│   ├── KE5Z.txt
│   ├── ke5z agosto.txt
│   ├── ke5z julho.txt
│   ├── ke5z setembro.txt
│   ├── ke5z outubro.txt
│   └── ke5z novembro.txt
│
└── KSBB/          # Arquivos de dados KSBB (.txt)
    ├── KSBB.txt
    ├── ksbb agosto.txt
    ├── ksbb julho.txt
    ├── ksbb setembro.txt
    ├── ksbb outubro.txt
    └── KSBB novembro.txt
```

### Arquivos Auxiliares (Raiz do Projeto)
- `Dados SAPIENS.xlsx` - Contém informações de contas contábeis e centros de custo
- `Fornecedores.xlsx` - Mapeamento de códigos de fornecedores para nomes

### Diretórios de Saída
```
KE5Z/              # Arquivos Parquet
├── KE5Z.parquet           # Dataset completo
├── KE5Z_main.parquet       # Sem registros "Others"
├── KE5Z_others.parquet    # Apenas registros "Others"
└── KE5Z_waterfall.parquet # Versão otimizada para waterfall

arquivos/          # Arquivos Excel
├── KE5Z_veiculos.xlsx      # USIs: Veículos, TC Ext, LC
└── KE5Z_pwt.xlsx           # USI: PWT
```

---

## 🔄 PROCESSAMENTO KE5Z

### Características dos Arquivos KE5Z
- **Formato**: Arquivo de texto delimitado por TAB (`\t`)
- **Encoding**: Latin-1
- **Cabeçalho**: Geralmente na linha 10 (detectado automaticamente)
- **Tamanho**: Pode variar de 66 MB a 384 MB

### Colunas Esperadas (Após Padronização)

| Coluna Original | Coluna Padronizada | Tipo | Descrição |
|----------------|-------------------|------|-----------|
| `Ano` | `Ano` | float64 | Ano do lançamento |
| `Período` | `Período` | float64 | Mês do lançamento (7-12) |
| `Nº conta` | `Nº conta` | object | Código da conta contábil |
| `Centro cst` | `Centro cst` | object | Centro de custo |
| `doc.ref` | `doc.ref` | float64 | Número do documento de referência |
| `Em MCont.` | `Valor` (renomeado) | float64 | Valor monetário (convertido) |
| `Qtd.` | `Qtd.` | float64 | Quantidade |
| `Material` | `Material` | object | Código do material |
| `Texto` | `Texto breve material` | object | Descrição do material |
| `Fornec.` | `Fornec.` | object | Código do fornecedor |
| `Cliente` | `Cliente` | object | Código do cliente |
| `Dt.lçto.` | `Dt.lçto.` | object | Data de lançamento |
| `Usuário` | `Usuário` | object | Usuário que fez o lançamento |
| `Tipo` | `Tipo` | object | Tipo de lançamento |
| `Doc.compra` | `Doc.compra` | object | Documento de compra |
| `Cen.lucro` | `Cen.lucro` | object | Centro de lucro |
| `Item` | `Item` | float64 | Item do documento |
| `D` | `D` | object | Débito/Crédito |
| `Hora` | `Hora` | object | Hora do lançamento |
| `Imobilizado` | `Imobilizado` | object | Código do imobilizado |
| `Denominação` | `Denominação` | object | Denominação |
| `Classe objs.` | `Classe objs.` | object | Classe de objetos |

### Processamento KE5Z - Passo a Passo

#### 1. Detecção Automática de Cabeçalho
```python
# Busca palavras-chave nas primeiras 25 linhas
palavras_chave = ['ano', 'período', 'nº conta', 'centro cst', 'em mcont', 
                  'qtd', 'doc.ref', 'material', 'fornec', 'texto']
# Retorna linha do cabeçalho (0-indexed)
```

#### 2. Leitura do Arquivo
- **Tentativas múltiplas**: Testa diferentes valores de `skiprows` (3-15)
- **Validação**: Verifica se o cabeçalho tem pelo menos 5 colunas nomeadas
- **Tratamento de erros**: Pula linhas mal formatadas (`on_bad_lines='skip'`)

#### 3. Padronização de Colunas
- Remove espaços em branco dos nomes
- Aplica mapeamento de variações para nomes fixos
- **CRÍTICO**: `'Texto'` → `'Texto breve material'` (para compatibilidade com KSBB)

#### 4. Limpeza de Dados
```python
# Filtrar registros com Ano válido
df = df[df['Ano'].notna() & (df['Ano'] != 0)]

# Converter 'Em MCont.' para numérico
# Remove pontos de milhar e substitui vírgula por ponto
df['Em MCont.'] = df['Em MCont.'].str.replace('.', '', regex=False)
df['Em MCont.'] = df['Em MCont.'].str.replace(',', '.', regex=False)
df['Em MCont.'] = pd.to_numeric(df['Em MCont.'], errors='coerce').fillna(0)

# Mesmo processo para 'Qtd.'
```

#### 5. Concatenação
- Todos os arquivos KE5Z são concatenados em `df_total`
- Ordem: Alfabética (garante consistência)

#### 6. Remoção de Colunas
Colunas removidas (não utilizadas):
- `Unnamed: 0`, `Unnamed: 1`, `Unnamed: 4`
- `Nº doc.`, `Elem.PEP`, `Obj.custo`, `TD`
- `SocPar`, `EmpEm.`, `Empr`, `TMv`, `D/C`, `Imobil.`

#### 7. Renomeação Final
```python
df_total.rename(columns={'Em MCont.': 'Valor'}, inplace=True)
```

#### 8. Filtro Final
```python
# Remover registros sem Nº conta válido
df_total = df_total[df_total['Nº conta'].notna() & (df_total['Nº conta'] != 0)]
```

---

## 🔄 PROCESSAMENTO KSBB

### Características dos Arquivos KSBB
- **Formato**: Arquivo de texto delimitado por TAB (`\t`)
- **Encoding**: Latin-1
- **Cabeçalho**: Geralmente na linha 3 (`skiprows=3`)
- **Rodapé**: Última linha geralmente vazia (`skipfooter=1`)
- **Estrutura**: Pode variar entre arquivos (9 colunas vs 35 colunas)

### Colunas Esperadas (Após Padronização)

| Coluna Original | Coluna Padronizada | Tipo | Descrição | Obrigatória |
|----------------|-------------------|------|-----------|-------------|
| `Dt.lçto.` | `Dt.lçto.` | object | Data de lançamento | Não |
| `Doc.compra` | `Doc.compra` | object | Documento de compra | Não |
| `Nº doc.ref` | `doc.ref` | float64 | Número documento referência | Não |
| `Nº doc.` | `Nº doc.` | float64 | Número do documento | Não |
| `Material` | `Material` | object | **Código do material** | **SIM** |
| `Texto` | `Texto breve material` | object | **Descrição do material** | **SIM** |
| `Per` | `Período` | float64 | Período (mês) | Não |
| `Txt.cab.doc.` | `Txt.cab.doc.` | object | Texto cabeçalho documento | Não |

### Processamento KSBB - Passo a Passo

#### 1. Leitura do Arquivo
```python
df_ksbb = pd.read_csv(
    caminho_arquivo,
    sep='\t',
    encoding='latin1',
    engine='python',
    skiprows=3,
    skipfooter=1,
    on_bad_lines='skip'
)
```

#### 2. Padronização Específica KSBB
Mapeamento especial para KSBB:
```python
mapeamento_ksbb = {
    'Dt.lçto.': ['dt.lçto.', 'Dt.lçto.', 'dt.lcto.', ...],
    'Doc.compra': ['doc.compra', 'Doc.compra', ...],
    'doc.ref': ['nº doc.ref', 'Nº doc.ref', 'doc.ref', ...],
    'Nº doc.': ['nº doc.', 'Nº doc.', ...],
    'Material': ['material', 'Material', 'codigo material', ...],
    'Texto breve material': ['texto breve material', 'Texto breve material', 
                            'texto', 'Texto', ...],  # ATENÇÃO: 'Texto' vira 'Texto breve material'
    'Período': ['per', 'Per', 'periodo', ...],
    'Txt.cab.doc.': ['txt.cab.doc.', 'Txt.cab.doc.', ...]
}
```

#### 3. Detecção de Coluna Material
Se `Material` não for encontrada após padronização:
- Busca colunas candidatas (contém 'material' mas não 'texto')
- Verifica colunas numéricas/alphanuméricas com alta cardinalidade (>50% únicos)
- Se não encontrar, usa `'Texto breve material'` como fallback

#### 4. Limpeza de Dados
```python
# Filtrar registros com Material válido
df_ksbb = df_ksbb[df_ksbb['Material'].notna() & (df_ksbb['Material'] != 0)]

# Remover duplicatas por Material (mantém primeiro)
df_ksbb = df_ksbb.drop_duplicates(subset=['Material'])
```

#### 5. Concatenação
- Todos os arquivos KSBB são concatenados em `df_ksbb`
- **CRÍTICO**: Remove duplicatas novamente após concatenação

---

## 🔗 RELACIONAMENTOS E MERGES

### 1. Merge KE5Z ↔ KSBB

#### Chave de Relacionamento
- **Chave**: `Material` (coluna comum em ambos DataFrames)
- **Tipo**: `left` (mantém todos os registros de KE5Z)

#### Processo
```python
df_total = pd.merge(
    df_total,
    df_ksbb[['Material', 'Texto breve material']],
    on='Material',
    how='left'
)
```

#### Resultado
- Adiciona coluna `'Texto breve material'` ao `df_total`
- Se já existir `'Texto breve material'` no KE5Z, cria `_x` e `_y`
- **Consolidação**: Prioriza `_y` (KSBB) quando disponível

#### Consolidação de Colunas
```python
# Se existem _x e _y
df_total['Descrição Material'] = df_total.apply(
    lambda row: (
        row['Texto breve material_y'] if pd.notnull(row['Texto breve material_y'])
        else row['Texto breve material_x']
    ),
    axis=1
)
```

#### Atualização da Coluna 'Texto'
```python
# Se 'Descrição Material' existe, usar para preencher 'Texto'
if 'Descrição Material' in df_total.columns:
    df_total['Texto'] = df_total.apply(
        lambda row: (
            row['Descrição Material'] if pd.notnull(row['Descrição Material'])
            else row['Texto']
        ),
        axis=1
    )
```

### 2. Merge KE5Z ↔ SAPIENS (Conta Contábil)

#### Arquivo: `Dados SAPIENS.xlsx` - Aba `'Conta contabil'`

#### Colunas do SAPIENS
| Coluna SAPIENS | Coluna no Merge | Tipo | Descrição |
|---------------|----------------|------|-----------|
| `CONTA SAPIENS` | `Nº conta` | object | Código da conta (chave) |
| `Type 07` | `Type 07` | object | Tipo 07 (Account) |
| `Type 06` | `Type 06` | object | Tipo 06 |
| `Type 05` | `Type 05` | object | Tipo 05 |

#### Processo
```python
# Renomear coluna para compatibilidade
df_sapiens.rename(columns={'CONTA SAPIENS': 'Nº conta'}, inplace=True)
df_sapiens['Nº conta'] = df_sapiens['Nº conta'].astype(str)

# Merge
df_total = pd.merge(
    df_total,
    df_sapiens[['Nº conta', 'Type 07', 'Type 06', 'Type 05']],
    on='Nº conta',
    how='left'
)
```

#### Resultado
- Adiciona `Type 07`, `Type 06`, `Type 05` ao `df_total`
- Valores não encontrados ficam como `NaN` (preenchidos depois com 'Others')

### 3. Merge KE5Z ↔ SAPIENS (Centro de Custo)

#### Arquivo: `Dados SAPIENS.xlsx` - Aba `'CC'`

#### Colunas do SAPIENS CC
| Coluna SAPIENS | Coluna no Merge | Tipo | Descrição |
|---------------|----------------|------|-----------|
| `CC SAPiens` | `Centro cst` | object | Centro de custo (chave) |
| `Oficina` | `Oficina` | object | Nome da oficina |
| `USI` | `USI` | object | Unidade de negócio |

#### Processo
```python
# Renomear coluna
df_CC.rename(columns={'CC SAPiens': 'Centro cst'}, inplace=True)

# Merge
df_total = pd.merge(
    df_total,
    df_CC[['Centro cst', 'Oficina', 'USI']],
    on='Centro cst',
    how='left'
)

# Preencher USI vazia com 'Others'
df_total['USI'] = df_total['USI'].fillna('Others')
```

#### Resultado
- Adiciona `Oficina` e `USI` ao `df_total`
- `USI` vazia → `'Others'`

### 4. Merge KE5Z ↔ Fornecedores

#### Arquivo: `Fornecedores.xlsx`

#### Colunas do Fornecedores
| Coluna Original | Coluna no Merge | Tipo | Descrição |
|----------------|----------------|------|-----------|
| `Fornecedor` | `Fornec.` | object | Código do fornecedor (chave) |
| `Nome do fornecedor` | `Fornecedor` | object | Nome completo do fornecedor |

#### Processo
```python
# Ler arquivo (pular 3 primeiras linhas)
df_fornecedores = pd.read_excel(arquivo_fornecedores, skiprows=3)

# Remover duplicatas
df_fornecedores = df_fornecedores.drop_duplicates(subset=['Fornecedor'])

# Renomear
df_fornecedores.rename(columns={'Fornecedor': 'Fornec.'}, inplace=True)
df_fornecedores['Fornec.'] = df_fornecedores['Fornec.'].astype(str)

# Merge
df_total = pd.merge(
    df_total,
    df_fornecedores[['Fornec.', 'Nome do fornecedor']],
    on='Fornec.',
    how='left'
)

# Renomear coluna resultante
df_total.rename(columns={'Nome do fornecedor': 'Fornecedor'}, inplace=True)
```

#### Resultado
- Adiciona `Fornecedor` (nome completo) ao `df_total`

### 5. Merge KE5Z ↔ Hist_prov (Provisões)

#### Arquivo: `Dados SAPIENS.xlsx` - Aba `'Hist_prov'`

#### Colunas do Hist_prov
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `Nome do fornecedor` | object | Nome do fornecedor |
| `20carac` | object | Primeiros 20 caracteres do texto (chave) |

#### Processo
```python
# Ler arquivo (pular primeira linha)
df_hist_prov = pd.read_excel(arquivo_hist_prov, sheet_name='Hist_prov', skiprows=1)
df_hist_prov = df_hist_prov[['Nome do fornecedor', '20carac']]

# Remover espaços e duplicatas
df_hist_prov['20carac'] = df_hist_prov['20carac'].str.strip()
df_hist_prov = df_hist_prov.drop_duplicates(subset=['20carac'])

# Criar coluna '20carac' no df_total (primeiros 20 caracteres do Texto)
coluna_para_20carac = 'Texto'  # ou 'Descrição Material' se Texto não existir
df_total['20carac'] = df_total[coluna_para_20carac].astype(str).str[:20]
df_total['20carac'] = df_total['20carac'].str.strip()

# Merge
df_total = pd.merge(
    df_total,
    df_hist_prov[['20carac', 'Nome do fornecedor']],
    on='20carac',
    how='left'
)

# Atualizar Fornecedor se 'Nome do fornecedor' não for nulo
df_total['Fornecedor'] = df_total.apply(
    lambda row: (
        row['Nome do fornecedor'] if pd.notnull(row['Nome do fornecedor'])
        else row['Fornecedor']
    ),
    axis=1
)
```

#### Resultado
- Atualiza `Fornecedor` com nomes de provisões quando disponível

---

## 🔧 PADRONIZAÇÃO DE COLUNAS

### Função: `padronizar_colunas(df, arquivo_nome="")`

### Mapeamento Completo

```python
mapeamento_colunas = {
    # Temporais
    'Ano': ['ano', 'Ano', 'ANO', 'year', 'Year', 'YEAR'],
    'Período': ['período', 'Periodo', 'PERÍODO', 'PERIODO', 'period', 'Period', 
                'PERIOD', 'mes', 'Mes', 'MES', 'mês', 'Mês'],
    
    # Contábil
    'Nº conta': ['nº conta', 'Nº conta', 'Nºconta', 'nºconta', 'conta', 'Conta', 
                 'CONTA', 'Nº Conta', 'No conta', 'No. conta'],
    'Centro cst': ['centro cst', 'Centro cst', 'Centrocst', 'centrocst', 'CENTRO CST',
                  'centro', 'Centro', 'CENTRO', 'centro de custo', 'Centro de Custo'],
    'Cen.lucro': ['cen.lucro', 'Cen.lucro', 'CEN.LUCRO', 'centro lucro', 'Centro Lucro',
                 'centro de lucro', 'Centro de Lucro'],
    
    # Documentos
    'doc.ref': ['doc.ref', 'doc.ref.', 'Doc.ref.', 'Doc.ref', 'DOC.REF', 'DOC.REF.',
               'documento', 'Documento', 'DOCUMENTO', 'doc ref', 'Doc Ref'],
    'Doc.compra': ['doc.compra', 'Doc.compra', 'DOC.COMPRA', 'documento compra',
                  'Documento Compra', 'doc compra'],
    'Dt.lçto.': ['dt.lçto.', 'Dt.lçto.', 'DT.LÇTO.', 'data', 'Data', 'DATA',
                'data lançamento', 'Data Lançamento', 'data de lançamento'],
    
    # Valores
    'Em MCont.': ['em mcont.', 'Em MCont.', 'EM MCONT.', 'valor', 'Valor', 'VALOR',
                 'montante', 'Montante', 'MONTANTE', 'em mcont', 'Em MCont'],
    'Qtd.': ['qtd.', 'Qtd.', 'QTD.', 'quantidade', 'Quantidade', 'QUANTIDADE',
            'qtd', 'Qtd', 'QTD'],
    
    # Material e Descrição
    'Material': ['material', 'Material', 'MATERIAL', 'mat', 'Mat', 'MAT', 
                'Código Material', 'Código material'],
    'Texto': ['texto', 'Texto', 'TEXTO', 'descrição', 'Descrição', 'DESCRIÇÃO',
             'texto breve', 'Texto breve', 'TEXTO BREVE', 'descrição material'],
    'Texto breve material': ['texto breve material', 'Texto breve material', 
                            'TEXTO BREVE MATERIAL', 'texto breve mat', 'Texto breve mat',
                            'descrição material', 'Descrição Material', 'texto material',
                            'Texto material', 'TEXTO MATERIAL'],
    
    # Fornecedor e Cliente
    'Fornec.': ['fornec.', 'Fornec.', 'FORNEC.', 'fornecedor código', 'Fornecedor código',
               'FORNECEDOR CÓDIGO', 'fornec', 'Fornec', 'FORNEC'],
    'Cliente': ['cliente', 'Cliente', 'CLIENTE'],
    
    # Outros
    'Item': ['item', 'Item', 'ITEM'],
    'Usuário': ['usuário', 'Usuário', 'USUÁRIO', 'usuario', 'Usuario', 'USUARIO',
               'user', 'User', 'USER'],
    'Tipo': ['tipo', 'Tipo', 'TIPO', 'type', 'Type', 'TYPE'],
}
```

### Regras de Prioridade

1. **Busca Exata (Case-Insensitive)**: Primeiro tenta correspondência exata
2. **Busca Parcial**: Se não encontrar, tenta correspondência parcial
3. **Proteção Material vs Texto**: 
   - `'Material'` NUNCA deve ser mapeado para `'Texto'`
   - Se encontrar coluna com 'material' mas sem 'texto', não mapear para 'Texto'

### Ordem de Aplicação

1. Remove espaços em branco dos nomes
2. Verifica se coluna já existe com nome correto
3. Busca variações (exata primeiro, depois parcial)
4. Aplica renomeação

---

## 📊 ARQUIVOS AUXILIARES

### 1. Dados SAPIENS.xlsx

#### Aba: `'Conta contabil'`
- **Propósito**: Mapear contas contábeis para tipos (Type 07, Type 06, Type 05)
- **Chave**: `CONTA SAPIENS` → `Nº conta`
- **Colunas retornadas**: `Type 07`, `Type 06`, `Type 05`

#### Aba: `'CC'`
- **Propósito**: Mapear centros de custo para oficinas e USIs
- **Chave**: `CC SAPiens` → `Centro cst`
- **Colunas retornadas**: `Oficina`, `USI`

#### Aba: `'Hist_prov'`
- **Propósito**: Mapear primeiros 20 caracteres do texto para nomes de fornecedores (provisões)
- **Chave**: `20carac` (primeiros 20 caracteres do `Texto`)
- **Colunas retornadas**: `Nome do fornecedor`

### 2. Fornecedores.xlsx

- **Propósito**: Mapear códigos de fornecedores para nomes completos
- **Chave**: `Fornecedor` → `Fornec.`
- **Colunas retornadas**: `Nome do fornecedor` → `Fornecedor`
- **Observação**: Pula 3 primeiras linhas ao ler

---

## 💾 ARQUIVOS DE SAÍDA

### Arquivos Parquet

#### 1. KE5Z.parquet
- **Conteúdo**: Dataset completo (todos os registros)
- **Uso**: Backup completo, análises gerais
- **Tamanho**: ~70 MB (exemplo)

#### 2. KE5Z_main.parquet
- **Conteúdo**: Registros onde `USI != 'Others'`
- **Uso**: Dashboard principal (sem registros genéricos)
- **Tamanho**: Menor que completo

#### 3. KE5Z_others.parquet
- **Conteúdo**: Apenas registros onde `USI == 'Others'`
- **Uso**: Análises específicas de registros genéricos
- **Tamanho**: Maior parte dos dados

#### 4. KE5Z_waterfall.parquet
- **Conteúdo**: Versão otimizada com apenas colunas essenciais
- **Colunas**: `Período`, `Valor`, `USI`, `Type 05`, `Type 06`, `Type 07`, `Fornecedor`, `Fornec.`, `Tipo`, `Nº conta`
- **Otimizações**:
  - Strings categóricas → `category` (se <50% únicos)
  - `float64` → `float32`
  - `int64` → `int32`
- **Tamanho**: ~73% menor que completo (exemplo: 18.9 MB vs 70.5 MB)

### Arquivos Excel

#### Estrutura de Colunas (Final)
| Coluna Original | Coluna Final Excel | Tipo | Descrição |
|----------------|-------------------|------|-----------|
| `Período` | `Mes` | float64 | Mês numérico (7-12) |
| - | `Período` | object | Mês por extenso (julho, agosto, ...) |
| `Nº conta` | `Nºconta` | object | Código da conta |
| `Centro cst` | `Centrocst` | object | Centro de custo |
| `doc.ref` | `Nºdoc.ref.` | float64 | Documento referência |
| `Dt.lçto.` | `Dt.lçto.` | object | Data (DD/MM/AAAA) |
| `Valor` | `Valor` | float64 | Valor monetário |
| `Qtd.` | `QTD` | float64 | Quantidade |
| `Type 05` | `Type 05` | object | Tipo 05 |
| `Type 06` | `Type 06` | object | Tipo 06 |
| `Type 07` | `Account` | object | Tipo 07 (Account) |
| `USI` | `USI` | object | Unidade de negócio |
| `Oficina` | `Oficina` | object | Nome da oficina |
| `Doc.compra` | `Doc.compra` | object | Documento de compra |
| `Texto` | `Texto breve` | object | Descrição do material |
| `Fornecedor` | `Fornecedor` | object | Nome do fornecedor |
| `Material` | `Material` | object | Código do material |
| `Usuário` | `Usuário` | object | Usuário |
| `Fornec.` | `Fornec.` | object | Código do fornecedor |
| `Tipo` | `Tipo` | object | Tipo de lançamento |

#### Arquivos Gerados

1. **KE5Z_veiculos.xlsx**
   - **Filtro**: `USI IN ['Veículos', 'TC Ext', 'LC']`
   - **Uso**: Análises de veículos

2. **KE5Z_pwt.xlsx**
   - **Filtro**: `USI == 'PWT'`
   - **Uso**: Análises PWT

3. **KE5Z_{usi}.xlsx** (para cada USI não agrupada)
   - **Filtro**: `USI == {usi}` e `USI != 'Others'`
   - **Uso**: Análises específicas por USI

#### Limitações
- **Arquivo completo NÃO é salvo** se > 1.048.576 linhas (limite Excel)
- Arquivos são salvos separados por USI para evitar limite

---

## 🔄 FLUXO COMPLETO

### Diagrama de Fluxo

```
┌─────────────────┐
│  Arquivos KE5Z  │
│   (.txt files)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Detecção de    │
│  Cabeçalho      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Leitura e      │
│  Padronização   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Limpeza e      │
│  Normalização   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Concatenação   │
│  (df_total)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌─────────────────┐
│  Arquivos KSBB  │─────▶│  Processamento  │
│   (.txt files)  │      │      KSBB       │
└─────────────────┘      └────────┬────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  Merge por      │
                          │  Material       │
                          └────────┬────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  Merge com      │
                          │  SAPIENS        │
                          │  (Conta)        │
                          └────────┬────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  Merge com      │
                          │  SAPIENS (CC)   │
                          └────────┬────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  Merge com      │
                          │  Fornecedores   │
                          └────────┬────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  Merge com      │
                          │  Hist_prov      │
                          └────────┬────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  Preparação    │
                          │  para Saída     │
                          └────────┬────────┘
                                   │
                                   ▼
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
         ┌──────────────────┐        ┌──────────────────┐
         │  Arquivos        │        │  Arquivos        │
         │  Parquet         │        │  Excel           │
         └──────────────────┘        └──────────────────┘
```

### Sequência de Operações

1. **Carregamento KE5Z**
   - Lista arquivos `.txt` em `Extracoes/KE5Z/`
   - Para cada arquivo:
     - Detecta cabeçalho
     - Lê dados
     - Padroniza colunas
     - Limpa dados
     - Adiciona à lista

2. **Concatenação KE5Z**
   - Concatena todos os DataFrames KE5Z
   - Remove colunas desnecessárias
   - Renomeia `Em MCont.` → `Valor`
   - Filtra `Nº conta` válido

3. **Carregamento KSBB**
   - Lista arquivos `.txt` em `Extracoes/KSBB/`
   - Para cada arquivo:
     - Lê dados (`skiprows=3`, `skipfooter=1`)
     - Padroniza colunas (mapeamento KSBB)
     - Filtra `Material` válido
     - Remove duplicatas por `Material`
     - Adiciona à lista

4. **Concatenação KSBB**
   - Concatena todos os DataFrames KSBB
   - Remove duplicatas novamente

5. **Merge KE5Z ↔ KSBB**
   - Merge por `Material`
   - Consolida `Texto breve material`
   - Cria/atualiza `Descrição Material`
   - Atualiza `Texto`

6. **Merge com SAPIENS (Conta)**
   - Lê `Dados SAPIENS.xlsx` - aba `'Conta contabil'`
   - Merge por `Nº conta`
   - Adiciona `Type 07`, `Type 06`, `Type 05`

7. **Merge com SAPIENS (CC)**
   - Lê `Dados SAPIENS.xlsx` - aba `'CC'`
   - Merge por `Centro cst`
   - Adiciona `Oficina`, `USI`
   - Preenche `USI` vazia com `'Others'`

8. **Limpeza Final**
   - Converte tipos de dados
   - Converte `Dt.lçto.` para formato DD/MM/AAAA
   - Preenche `Type 07`, `Type 06`, `Type 05` vazios com `'Others'`

9. **Merge com Fornecedores**
   - Lê `Fornecedores.xlsx`
   - Merge por `Fornec.`
   - Adiciona `Fornecedor`

10. **Merge com Hist_prov**
    - Lê `Dados SAPIENS.xlsx` - aba `'Hist_prov'`
    - Cria `20carac` (primeiros 20 caracteres do `Texto`)
    - Merge por `20carac`
    - Atualiza `Fornecedor` se disponível

11. **Geração de Arquivos Parquet**
    - Separa `Others` vs resto
    - Salva `KE5Z_main.parquet`
    - Salva `KE5Z_others.parquet`
    - Salva `KE5Z.parquet` (completo)
    - Cria e salva `KE5Z_waterfall.parquet` (otimizado)

12. **Geração de Arquivos Excel**
    - Organiza colunas (ordem específica)
    - Renomeia colunas para formato final
    - Cria coluna `Período` (mês por extenso)
    - Aplica filtro de meses (se `MESES_FILTRO` definido)
    - Salva arquivos por USI

---

## ⚠️ TRATAMENTO DE ERROS

### Erros Comuns e Soluções

#### 1. Cabeçalho Não Detectado
- **Sintoma**: Arquivo lido mas colunas são `Unnamed`
- **Solução**: Tenta múltiplos valores de `skiprows` (3-15)
- **Fallback**: Lê sem `skiprows` e procura cabeçalho nas primeiras 20 linhas

#### 2. Coluna Não Encontrada
- **Sintoma**: `KeyError: 'Coluna X'`
- **Solução**: 
  - Verifica se coluna existe após padronização
  - Tenta encontrar coluna similar
  - Cria coluna vazia se necessário (ex: `Qtd.`)

#### 3. Erro de Parsing
- **Sintoma**: `ParserError: Expected X fields, saw Y`
- **Solução**: Usa `on_bad_lines='skip'` para pular linhas mal formatadas

#### 4. Material Não Encontrado no Merge
- **Sintoma**: Nenhum match no merge KE5Z ↔ KSBB
- **Solução**: 
  - Verifica normalização de `Material` (zeros à esquerda)
  - Verifica tipos de dados (deve ser `object`/`string`)
  - Remove espaços invisíveis

#### 5. Arquivo KSBB com Estrutura Diferente
- **Sintoma**: `KSBB novembro.txt` tem 35 colunas vs 9 colunas normais
- **Solução**: 
  - Detecta coluna candidata para `Material`
  - Se não encontrar, pula arquivo (não compatível)

#### 6. Valores NaN Após Merge
- **Sintoma**: Muitos valores vazios após merges
- **Solução**: 
  - Preenche com valores padrão (`'Others'` para tipos, `'Others'` para USI)
  - Mantém `NaN` apenas onde faz sentido (ex: `Fornecedor`)

### Validações Implementadas

1. **Validação de Cabeçalho**
   - Mínimo 5 colunas nomeadas
   - Mínimo 1 linha de dados
   - Não todas colunas `Unnamed`

2. **Validação de Dados**
   - `Ano` não nulo e diferente de 0
   - `Nº conta` não nulo e diferente de 0
   - `Material` (KSBB) não nulo e diferente de 0

3. **Validação de Merge**
   - Verifica se colunas de chave existem antes do merge
   - Verifica se DataFrames não estão vazios

---

## 🔑 CHAVES DE RELACIONAMENTO - RESUMO

| Relacionamento | Chave KE5Z | Chave Externa | Tipo | Resultado |
|---------------|-----------|--------------|------|-----------|
| KE5Z ↔ KSBB | `Material` | `Material` | left | `Texto breve material` |
| KE5Z ↔ SAPIENS (Conta) | `Nº conta` | `CONTA SAPIENS` | left | `Type 07`, `Type 06`, `Type 05` |
| KE5Z ↔ SAPIENS (CC) | `Centro cst` | `CC SAPiens` | left | `Oficina`, `USI` |
| KE5Z ↔ Fornecedores | `Fornec.` | `Fornecedor` | left | `Fornecedor` (nome) |
| KE5Z ↔ Hist_prov | `20carac` | `20carac` | left | `Fornecedor` (atualizado) |

---

## 📝 NOTAS IMPORTANTES

### Normalização de Material
- **CRÍTICO**: Material deve ser tratado como `string` desde o início
- Remove zeros à esquerda de strings numéricas (ex: `"0123"` → `"123"`)
- Remove espaços invisíveis e caracteres não imprimíveis
- Garante match entre KE5Z e KSBB mesmo com variações de formato

### Ordem de Colunas no Excel
A ordem final das colunas no Excel é:
1. `Mes`
2. `Período`
3. `Nºconta`
4. `Centrocst`
5. `Nºdoc.ref.`
6. `Dt.lçto.`
7. `Valor`
8. `QTD`
9. `Type 05`
10. `Type 06`
11. `Account` (Type 07)
12. `USI`
13. `Oficina`
14. `Doc.compra`
15. `Texto breve`
16. `Fornecedor`
17. `Material`
18. `Usuário`
19. `Fornec.`
20. `Tipo`

### Filtro de Meses
- Variável de ambiente: `MESES_FILTRO` (ex: `"9,10,11"`)
- Aplicado antes de salvar arquivos Excel
- Não afeta arquivos Parquet (sempre completos)

### Portabilidade
- Funções `get_base_path()` e `get_output_path()` garantem portabilidade
- No executável: busca em `_internal` primeiro, depois diretório do executável
- Em desenvolvimento: usa diretório do script

---

## ✅ CHECKLIST PARA MODIFICAÇÕES

Ao modificar o script de extração, verificar:

- [ ] Padronização de colunas está atualizada?
- [ ] Chaves de merge estão corretas?
- [ ] Tipos de dados estão consistentes?
- [ ] Validações estão implementadas?
- [ ] Tratamento de erros está completo?
- [ ] Arquivos de saída estão corretos?
- [ ] Ordem de colunas no Excel está correta?
- [ ] Normalização de Material está funcionando?
- [ ] Portabilidade está garantida?

---

**Última atualização**: Baseado em `Extracao.py` versão atual
**Autor**: Documentação gerada para suporte à IA

