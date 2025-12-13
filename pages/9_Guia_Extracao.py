import streamlit as st
import sys
import os

# Adicionar diretório pai ao path para importar auth_simple
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth_simple import (verificar_autenticacao, exibir_header_usuario,
                         exibir_info_ultima_extracao, exibir_rodape_versao)

# Configuração da página
st.set_page_config(
    page_title="Guia de Extração - Dashboard KE5Z",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verificar autenticação
verificar_autenticacao()

# Navegação simples
st.sidebar.markdown("📋 **NAVEGAÇÃO:** Use abas do navegador")
st.sidebar.markdown("🏠 Dashboard: Aplicação Desktop")
st.sidebar.markdown("---")

# Exibir informação da última extração no topo
exibir_info_ultima_extracao()

# Header
exibir_header_usuario()

# Título principal
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 2rem;">
    <h1 style="color: white; font-size: 3rem; margin: 0;">📚 Guia Completo de Extração de Dados</h1>
    <h3 style="color: #f0f0f0; margin: 0;">Dashboard KE5Z - Processamento de Dados</h3>
    <p style="color: #e0e0e0; font-size: 1.2rem; margin-top: 1rem;">
        Documentação Completa para IA - Todos os Relacionamentos e Processos
    </p>
</div>
""", unsafe_allow_html=True)

# Índice
st.markdown("## 📋 **ÍNDICE**")
st.markdown("""
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
""")

st.markdown("---")

# Seção 1: Visão Geral
st.markdown("## 🎯 VISÃO GERAL")

st.markdown("### Objetivo do Script")
st.markdown("""
O script `Extracao.py` é responsável por:
- **Carregar** dados de múltiplas fontes (KE5Z, KSBB, SAPIENS, Fornecedores)
- **Processar** e **normalizar** dados de diferentes formatos
- **Unificar** informações através de merges por chaves comuns
- **Gerar** arquivos Parquet e Excel otimizados para uso no dashboard
""")

st.markdown("### Fluxo Principal")
st.code("""
KE5Z (.txt) → Processamento → Merge com KSBB → Merge com SAPIENS → Merge com Fornecedores → Arquivos de Saída
""", language="text")

st.markdown("---")

# Seção 2: Estrutura de Arquivos
st.markdown("## 📁 ESTRUTURA DE ARQUIVOS")

st.markdown("### Diretórios de Entrada")
st.code("""
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
""", language="text")

st.markdown("### Arquivos Auxiliares (Raiz do Projeto)")
st.markdown("""
- `Dados SAPIENS.xlsx` - Contém informações de contas contábeis e centros de custo
- `Fornecedores.xlsx` - Mapeamento de códigos de fornecedores para nomes
""")

st.markdown("### Diretórios de Saída")
st.code("""
KE5Z/              # Arquivos Parquet
├── KE5Z.parquet           # Dataset completo
├── KE5Z_main.parquet       # Sem registros "Others"
├── KE5Z_others.parquet    # Apenas registros "Others"
└── KE5Z_waterfall.parquet # Versão otimizada para waterfall

arquivos/          # Arquivos Excel
├── KE5Z_veiculos.xlsx      # USIs: Veículos, TC Ext, LC
└── KE5Z_pwt.xlsx           # USI: PWT
""", language="text")

st.markdown("---")

# Seção 3: Processamento KE5Z
st.markdown("## 🔄 PROCESSAMENTO KE5Z")

st.markdown("### Características dos Arquivos KE5Z")
st.markdown("""
- **Formato**: Arquivo de texto delimitado por TAB (`\t`)
- **Encoding**: Latin-1
- **Cabeçalho**: Geralmente na linha 10 (detectado automaticamente)
- **Tamanho**: Pode variar de 66 MB a 384 MB
""")

st.markdown("### Colunas Principais (Após Padronização)")

colunas_ke5z = {
    "Coluna": ["Ano", "Período", "Nº conta", "Centro cst", "doc.ref", "Em MCont.", "Qtd.", "Material", "Texto", "Fornec.", "Cliente", "Dt.lçto.", "Usuário", "Tipo", "Doc.compra"],
    "Tipo": ["float64", "float64", "object", "object", "float64", "float64", "float64", "object", "object", "object", "object", "object", "object", "object", "object"],
    "Descrição": [
        "Ano do lançamento",
        "Mês do lançamento (7-12)",
        "Código da conta contábil",
        "Centro de custo",
        "Número do documento de referência",
        "Valor monetário (renomeado para 'Valor')",
        "Quantidade",
        "Código do material",
        "Descrição do material (padronizado para 'Texto breve material')",
        "Código do fornecedor",
        "Código do cliente",
        "Data de lançamento",
        "Usuário que fez o lançamento",
        "Tipo de lançamento",
        "Documento de compra"
    ]
}

st.dataframe(colunas_ke5z, use_container_width=True, hide_index=True)

st.markdown("### Processamento KE5Z - Passo a Passo")

with st.expander("1. Detecção Automática de Cabeçalho"):
    st.code("""
# Busca palavras-chave nas primeiras 25 linhas
palavras_chave = ['ano', 'período', 'nº conta', 'centro cst', 'em mcont', 
                  'qtd', 'doc.ref', 'material', 'fornec', 'texto']
# Retorna linha do cabeçalho (0-indexed)
    """, language="python")

with st.expander("2. Leitura do Arquivo"):
    st.markdown("""
    - **Tentativas múltiplas**: Testa diferentes valores de `skiprows` (3-15)
    - **Validação**: Verifica se o cabeçalho tem pelo menos 5 colunas nomeadas
    - **Tratamento de erros**: Pula linhas mal formatadas (`on_bad_lines='skip'`)
    """)

with st.expander("3. Padronização de Colunas"):
    st.markdown("""
    - Remove espaços em branco dos nomes
    - Aplica mapeamento de variações para nomes fixos
    - **CRÍTICO**: `'Texto'` → `'Texto breve material'` (para compatibilidade com KSBB)
    """)

with st.expander("4. Limpeza de Dados"):
    st.code("""
# Filtrar registros com Ano válido
df = df[df['Ano'].notna() & (df['Ano'] != 0)]

# Converter 'Em MCont.' para numérico
# Remove pontos de milhar e substitui vírgula por ponto
df['Em MCont.'] = df['Em MCont.'].str.replace('.', '', regex=False)
df['Em MCont.'] = df['Em MCont.'].str.replace(',', '.', regex=False)
df['Em MCont.'] = pd.to_numeric(df['Em MCont.'], errors='coerce').fillna(0)

# Mesmo processo para 'Qtd.'
    """, language="python")

with st.expander("5. Concatenação e Renomeação"):
    st.code("""
# Todos os arquivos KE5Z são concatenados em df_total
df_total = pd.concat(dataframes, ignore_index=True)

# Renomear coluna principal
df_total.rename(columns={'Em MCont.': 'Valor'}, inplace=True)

# Filtrar registros sem Nº conta válido
df_total = df_total[df_total['Nº conta'].notna() & (df_total['Nº conta'] != 0)]
    """, language="python")

st.markdown("---")

# Seção 4: Processamento KSBB
st.markdown("## 🔄 PROCESSAMENTO KSBB")

st.markdown("### Características dos Arquivos KSBB")
st.markdown("""
- **Formato**: Arquivo de texto delimitado por TAB (`\t`)
- **Encoding**: Latin-1
- **Cabeçalho**: Geralmente na linha 3 (`skiprows=3`)
- **Rodapé**: Última linha geralmente vazia (`skipfooter=1`)
- **Estrutura**: Pode variar entre arquivos (9 colunas vs 35 colunas)
""")

st.markdown("### Colunas Principais (Após Padronização)")

colunas_ksbb = {
    "Coluna": ["Material", "Texto breve material", "Dt.lçto.", "Doc.compra", "doc.ref", "Nº doc.", "Período", "Txt.cab.doc."],
    "Tipo": ["object", "object", "object", "object", "float64", "float64", "float64", "object"],
    "Obrigatória": ["✅ SIM", "✅ SIM", "❌ Não", "❌ Não", "❌ Não", "❌ Não", "❌ Não", "❌ Não"],
    "Descrição": [
        "Código do material (CHAVE para merge)",
        "Descrição do material (CHAVE para merge)",
        "Data de lançamento",
        "Documento de compra",
        "Número documento referência",
        "Número do documento",
        "Período (mês)",
        "Texto cabeçalho documento"
    ]
}

st.dataframe(colunas_ksbb, use_container_width=True, hide_index=True)

st.markdown("### Processamento KSBB - Passo a Passo")

with st.expander("1. Leitura do Arquivo"):
    st.code("""
df_ksbb = pd.read_csv(
    caminho_arquivo,
    sep='\t',
    encoding='latin1',
    engine='python',
    skiprows=3,
    skipfooter=1,
    on_bad_lines='skip'
)
    """, language="python")

with st.expander("2. Padronização Específica KSBB"):
    st.markdown("""
    Mapeamento especial para KSBB:
    - `'Nº doc.ref'` → `'doc.ref'`
    - `'Per'` → `'Período'`
    - `'Texto'` → `'Texto breve material'` (se não existir)
    """)

with st.expander("3. Detecção de Coluna Material"):
    st.markdown("""
    Se `Material` não for encontrada após padronização:
    - Busca colunas candidatas (contém 'material' mas não 'texto')
    - Verifica colunas numéricas/alphanuméricas com alta cardinalidade (>50% únicos)
    - Se não encontrar, usa `'Texto breve material'` como fallback
    """)

with st.expander("4. Limpeza de Dados"):
    st.code("""
# Filtrar registros com Material válido
df_ksbb = df_ksbb[df_ksbb['Material'].notna() & (df_ksbb['Material'] != 0)]

# Remover duplicatas por Material (mantém primeiro)
df_ksbb = df_ksbb.drop_duplicates(subset=['Material'])
    """, language="python")

st.markdown("---")

# Seção 5: Relacionamentos e Merges
st.markdown("## 🔗 RELACIONAMENTOS E MERGES")

st.markdown("### 1. Merge KE5Z ↔ KSBB")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Chave de Relacionamento")
    st.info("""
    **Chave**: `Material` (coluna comum em ambos DataFrames)
    
    **Tipo**: `left` (mantém todos os registros de KE5Z)
    """)

with col2:
    st.markdown("#### Resultado")
    st.success("""
    - Adiciona coluna `'Texto breve material'` ao `df_total`
    - Consolida descrições de material
    - Prioriza dados do KSBB quando disponível
    """)

st.code("""
df_total = pd.merge(
    df_total,
    df_ksbb[['Material', 'Texto breve material']],
    on='Material',
    how='left'
)

# Consolidação de colunas
df_total['Descrição Material'] = df_total.apply(
    lambda row: (
        row['Texto breve material_y'] if pd.notnull(row['Texto breve material_y'])
        else row['Texto breve material_x']
    ),
    axis=1
)
""", language="python")

st.markdown("### 2. Merge KE5Z ↔ SAPIENS (Conta Contábil)")

st.markdown("#### Arquivo: `Dados SAPIENS.xlsx` - Aba `'Conta contabil'`")

merge_sapiens = {
    "Coluna SAPIENS": ["CONTA SAPIENS", "Type 07", "Type 06", "Type 05"],
    "Coluna no Merge": ["Nº conta", "Type 07", "Type 06", "Type 05"],
    "Chave": ["✅ SIM", "❌ Não", "❌ Não", "❌ Não"],
    "Descrição": [
        "Código da conta (chave de merge)",
        "Tipo 07 (Account)",
        "Tipo 06",
        "Tipo 05"
    ]
}

st.dataframe(merge_sapiens, use_container_width=True, hide_index=True)

st.code("""
df_sapiens.rename(columns={'CONTA SAPIENS': 'Nº conta'}, inplace=True)
df_sapiens['Nº conta'] = df_sapiens['Nº conta'].astype(str)

df_total = pd.merge(
    df_total,
    df_sapiens[['Nº conta', 'Type 07', 'Type 06', 'Type 05']],
    on='Nº conta',
    how='left'
)
""", language="python")

st.markdown("### 3. Merge KE5Z ↔ SAPIENS (Centro de Custo)")

st.markdown("#### Arquivo: `Dados SAPIENS.xlsx` - Aba `'CC'`")

merge_cc = {
    "Coluna SAPIENS": ["CC SAPiens", "Oficina", "USI"],
    "Coluna no Merge": ["Centro cst", "Oficina", "USI"],
    "Chave": ["✅ SIM", "❌ Não", "❌ Não"],
    "Descrição": [
        "Centro de custo (chave de merge)",
        "Nome da oficina",
        "Unidade de negócio (preenchido com 'Others' se vazio)"
    ]
}

st.dataframe(merge_cc, use_container_width=True, hide_index=True)

st.code("""
df_CC.rename(columns={'CC SAPiens': 'Centro cst'}, inplace=True)

df_total = pd.merge(
    df_total,
    df_CC[['Centro cst', 'Oficina', 'USI']],
    on='Centro cst',
    how='left'
)

# Preencher USI vazia com 'Others'
df_total['USI'] = df_total['USI'].fillna('Others')
""", language="python")

st.markdown("### 4. Merge KE5Z ↔ Fornecedores")

st.markdown("#### Arquivo: `Fornecedores.xlsx`")

merge_fornecedores = {
    "Coluna Original": ["Fornecedor", "Nome do fornecedor"],
    "Coluna no Merge": ["Fornec.", "Fornecedor"],
    "Chave": ["✅ SIM", "❌ Não"],
    "Descrição": [
        "Código do fornecedor (chave de merge)",
        "Nome completo do fornecedor (resultado do merge)"
    ]
}

st.dataframe(merge_fornecedores, use_container_width=True, hide_index=True)

st.code("""
df_fornecedores = pd.read_excel(arquivo_fornecedores, skiprows=3)
df_fornecedores = df_fornecedores.drop_duplicates(subset=['Fornecedor'])
df_fornecedores.rename(columns={'Fornecedor': 'Fornec.'}, inplace=True)

df_total = pd.merge(
    df_total,
    df_fornecedores[['Fornec.', 'Nome do fornecedor']],
    on='Fornec.',
    how='left'
)

df_total.rename(columns={'Nome do fornecedor': 'Fornecedor'}, inplace=True)
""", language="python")

st.markdown("### 5. Merge KE5Z ↔ Hist_prov (Provisões)")

st.markdown("#### Arquivo: `Dados SAPIENS.xlsx` - Aba `'Hist_prov'`")

st.info("""
**Chave Especial**: `20carac` (primeiros 20 caracteres do `Texto`)

Este merge atualiza nomes de fornecedores com informações de provisões.
""")

st.code("""
# Criar coluna '20carac' no df_total
df_total['20carac'] = df_total['Texto'].astype(str).str[:20]
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
""", language="python")

st.markdown("### 📊 Resumo de Todas as Chaves de Relacionamento")

resumo_merges = {
    "Relacionamento": [
        "KE5Z ↔ KSBB",
        "KE5Z ↔ SAPIENS (Conta)",
        "KE5Z ↔ SAPIENS (CC)",
        "KE5Z ↔ Fornecedores",
        "KE5Z ↔ Hist_prov"
    ],
    "Chave KE5Z": [
        "Material",
        "Nº conta",
        "Centro cst",
        "Fornec.",
        "20carac"
    ],
    "Chave Externa": [
        "Material",
        "CONTA SAPIENS",
        "CC SAPiens",
        "Fornecedor",
        "20carac"
    ],
    "Tipo": [
        "left",
        "left",
        "left",
        "left",
        "left"
    ],
    "Resultado": [
        "Texto breve material",
        "Type 07, Type 06, Type 05",
        "Oficina, USI",
        "Fornecedor (nome)",
        "Fornecedor (atualizado)"
    ]
}

st.dataframe(resumo_merges, use_container_width=True, hide_index=True)

st.markdown("---")

# Seção 6: Padronização de Colunas
st.markdown("## 🔧 PADRONIZAÇÃO DE COLUNAS")

st.markdown("### Função: `padronizar_colunas(df, arquivo_nome='')`")

st.markdown("### Mapeamento Completo de Colunas")

mapeamento_colunas = {
    "Nome Padrão": [
        "Ano", "Período", "Nº conta", "Centro cst", "Cen.lucro",
        "doc.ref", "Doc.compra", "Dt.lçto.", "Em MCont.", "Qtd.",
        "Material", "Texto", "Texto breve material",
        "Fornec.", "Cliente", "Item", "Usuário", "Tipo"
    ],
    "Variações Aceitas": [
        "ano, Ano, ANO, year, Year, YEAR",
        "período, Periodo, PERÍODO, period, mes, Mês",
        "nº conta, Nºconta, conta, Conta, CONTA",
        "centro cst, Centrocst, centro, Centro",
        "cen.lucro, Cen.lucro, centro lucro",
        "doc.ref, Doc.ref, documento, Documento",
        "doc.compra, Doc.compra, documento compra",
        "dt.lçto., Dt.lçto., data, Data",
        "em mcont., Em MCont., valor, Val or",
        "qtd., Qtd., quantidade, Quantidade",
        "material, Material, mat, Mat",
        "texto, Texto, descrição, Descrição",
        "texto breve material, Texto breve material, descrição material",
        "fornec., Fornec., fornecedor código",
        "cliente, Cliente, CLIENTE",
        "item, Item, ITEM",
        "usuário, Usuário, usuario, Usuario",
        "tipo, Tipo, type, Type"
    ]
}

st.dataframe(mapeamento_colunas, use_container_width=True, hide_index=True)

st.markdown("### Regras de Prioridade")
st.markdown("""
1. **Busca Exata (Case-Insensitive)**: Primeiro tenta correspondência exata
2. **Busca Parcial**: Se não encontrar, tenta correspondência parcial
3. **Proteção Material vs Texto**: 
   - `'Material'` NUNCA deve ser mapeado para `'Texto'`
   - Se encontrar coluna com 'material' mas sem 'texto', não mapear para 'Texto'
""")

st.markdown("### Ordem de Aplicação")
st.markdown("""
1. Remove espaços em branco dos nomes
2. Verifica se coluna já existe com nome correto
3. Busca variações (exata primeiro, depois parcial)
4. Aplica renomeação
""")

st.markdown("---")

# Seção 7: Arquivos Auxiliares
st.markdown("## 📊 ARQUIVOS AUXILIARES")

st.markdown("### 1. Dados SAPIENS.xlsx")

with st.expander("Aba: 'Conta contabil'"):
    st.markdown("""
    - **Propósito**: Mapear contas contábeis para tipos (Type 07, Type 06, Type 05)
    - **Chave**: `CONTA SAPIENS` → `Nº conta`
    - **Colunas retornadas**: `Type 07`, `Type 06`, `Type 05`
    """)

with st.expander("Aba: 'CC'"):
    st.markdown("""
    - **Propósito**: Mapear centros de custo para oficinas e USIs
    - **Chave**: `CC SAPiens` → `Centro cst`
    - **Colunas retornadas**: `Oficina`, `USI`
    """)

with st.expander("Aba: 'Hist_prov'"):
    st.markdown("""
    - **Propósito**: Mapear primeiros 20 caracteres do texto para nomes de fornecedores (provisões)
    - **Chave**: `20carac` (primeiros 20 caracteres do `Texto`)
    - **Colunas retornadas**: `Nome do fornecedor`
    """)

st.markdown("### 2. Fornecedores.xlsx")
st.markdown("""
- **Propósito**: Mapear códigos de fornecedores para nomes completos
- **Chave**: `Fornecedor` → `Fornec.`
- **Colunas retornadas**: `Nome do fornecedor` → `Fornecedor`
- **Observação**: Pula 3 primeiras linhas ao ler
""")

st.markdown("---")

# Seção 8: Arquivos de Saída
st.markdown("## 💾 ARQUIVOS DE SAÍDA")

st.markdown("### Arquivos Parquet")

with st.expander("KE5Z.parquet"):
    st.markdown("""
    - **Conteúdo**: Dataset completo (todos os registros)
    - **Uso**: Backup completo, análises gerais
    - **Tamanho**: ~70 MB (exemplo)
    """)

with st.expander("KE5Z_main.parquet"):
    st.markdown("""
    - **Conteúdo**: Registros onde `USI != 'Others'`
    - **Uso**: Dashboard principal (sem registros genéricos)
    - **Tamanho**: Menor que completo
    """)

with st.expander("KE5Z_others.parquet"):
    st.markdown("""
    - **Conteúdo**: Apenas registros onde `USI == 'Others'`
    - **Uso**: Análises específicas de registros genéricos
    - **Tamanho**: Maior parte dos dados
    """)

with st.expander("KE5Z_waterfall.parquet"):
    st.markdown("""
    - **Conteúdo**: Versão otimizada com apenas colunas essenciais
    - **Colunas**: `Período`, `Valor`, `USI`, `Type 05`, `Type 06`, `Type 07`, `Fornecedor`, `Fornec.`, `Tipo`, `Nº conta`
    - **Otimizações**:
      - Strings categóricas → `category` (se <50% únicos)
      - `float64` → `float32`
      - `int64` → `int32`
    - **Tamanho**: ~73% menor que completo (exemplo: 18.9 MB vs 70.5 MB)
    """)

st.markdown("### Arquivos Excel")

st.markdown("#### Estrutura de Colunas (Final)")

colunas_excel = {
    "Coluna Original": ["Período", "Nº conta", "Centro cst", "doc.ref", "Dt.lçto.", "Valor", "Qtd.", "Type 05", "Type 06", "Type 07", "USI", "Oficina", "Doc.compra", "Texto", "Fornecedor", "Material", "Usuário", "Fornec.", "Tipo"],
    "Coluna Final Excel": ["Mes", "Nºconta", "Centrocst", "Nºdoc.ref.", "Dt.lçto.", "Valor", "QTD", "Type 05", "Type 06", "Account", "USI", "Oficina", "Doc.compra", "Texto breve", "Fornecedor", "Material", "Usuário", "Fornec.", "Tipo"],
    "Tipo": ["float64", "object", "object", "float64", "object", "float64", "float64", "object", "object", "object", "object", "object", "object", "object", "object", "object", "object", "object", "object"]
}

st.dataframe(colunas_excel, use_container_width=True, hide_index=True)

st.markdown("#### Arquivos Gerados")
st.markdown("""
1. **KE5Z_veiculos.xlsx**
   - **Filtro**: `USI IN ['Veículos', 'TC Ext', 'LC']`
   - **Uso**: Análises de veículos

2. **KE5Z_pwt.xlsx**
   - **Filtro**: `USI == 'PWT'`
   - **Uso**: Análises PWT

3. **KE5Z_{usi}.xlsx** (para cada USI não agrupada)
   - **Filtro**: `USI == {usi}` e `USI != 'Others'`
   - **Uso**: Análises específicas por USI
""")

st.warning("""
**Limitações**:
- **Arquivo completo NÃO é salvo** se > 1.048.576 linhas (limite Excel)
- Arquivos são salvos separados por USI para evitar limite
""")

st.markdown("---")

# Seção 9: Fluxo Completo
st.markdown("## 🔄 FLUXO COMPLETO")

st.markdown("### Diagrama de Fluxo")

st.code("""
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
                          └────────┬────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  Merge com      │
                          │  Fornecedores   │
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
""", language="text")

st.markdown("### Sequência de Operações")

operacoes = [
    "1. Carregamento KE5Z - Lista arquivos .txt, detecta cabeçalho, lê dados, padroniza colunas, limpa dados",
    "2. Concatenação KE5Z - Concatena todos os DataFrames, remove colunas desnecessárias, renomeia Em MCont. → Valor",
    "3. Carregamento KSBB - Lista arquivos .txt, lê dados, padroniza colunas, filtra Material válido, remove duplicatas",
    "4. Concatenação KSBB - Concatena todos os DataFrames, remove duplicatas novamente",
    "5. Merge KE5Z ↔ KSBB - Merge por Material, consolida Texto breve material, cria Descrição Material, atualiza Texto",
    "6. Merge com SAPIENS (Conta) - Lê Dados SAPIENS.xlsx aba 'Conta contabil', merge por Nº conta, adiciona Type 07, Type 06, Type 05",
    "7. Merge com SAPIENS (CC) - Lê Dados SAPIENS.xlsx aba 'CC', merge por Centro cst, adiciona Oficina, USI, preenche USI vazia com 'Others'",
    "8. Limpeza Final - Converte tipos de dados, converte Dt.lçto. para DD/MM/AAAA, preenche Type 07/06/05 vazios com 'Others'",
    "9. Merge com Fornecedores - Lê Fornecedores.xlsx, merge por Fornec., adiciona Fornecedor",
    "10. Merge com Hist_prov - Lê Dados SAPIENS.xlsx aba 'Hist_prov', cria 20carac, merge por 20carac, atualiza Fornecedor",
    "11. Geração de Arquivos Parquet - Separa Others vs resto, salva KE5Z_main.parquet, KE5Z_others.parquet, KE5Z.parquet, KE5Z_waterfall.parquet",
    "12. Geração de Arquivos Excel - Organiza colunas, renomeia colunas, cria Período (mês por extenso), aplica filtro de meses, salva arquivos por USI"
]

for op in operacoes:
    st.markdown(f"- {op}")

st.markdown("---")

# Seção 10: Tratamento de Erros
st.markdown("## ⚠️ TRATAMENTO DE ERROS")

st.markdown("### Erros Comuns e Soluções")

with st.expander("1. Cabeçalho Não Detectado"):
    st.markdown("""
    - **Sintoma**: Arquivo lido mas colunas são `Unnamed`
    - **Solução**: Tenta múltiplos valores de `skiprows` (3-15)
    - **Fallback**: Lê sem `skiprows` e procura cabeçalho nas primeiras 20 linhas
    """)

with st.expander("2. Coluna Não Encontrada"):
    st.markdown("""
    - **Sintoma**: `KeyError: 'Coluna X'`
    - **Solução**: 
      - Verifica se coluna existe após padronização
      - Tenta encontrar coluna similar
      - Cria coluna vazia se necessário (ex: `Qtd.`)
    """)

with st.expander("3. Erro de Parsing"):
    st.markdown("""
    - **Sintoma**: `ParserError: Expected X fields, saw Y`
    - **Solução**: Usa `on_bad_lines='skip'` para pular linhas mal formatadas
    """)

with st.expander("4. Material Não Encontrado no Merge"):
    st.markdown("""
    - **Sintoma**: Nenhum match no merge KE5Z ↔ KSBB
    - **Solução**: 
      - Verifica normalização de `Material` (zeros à esquerda)
      - Verifica tipos de dados (deve ser `object`/`string`)
      - Remove espaços invisíveis
    """)

with st.expander("5. Arquivo KSBB com Estrutura Diferente"):
    st.markdown("""
    - **Sintoma**: `KSBB novembro.txt` tem 35 colunas vs 9 colunas normais
    - **Solução**: 
      - Detecta coluna candidata para `Material`
      - Se não encontrar, pula arquivo (não compatível)
    """)

with st.expander("6. Valores NaN Após Merge"):
    st.markdown("""
    - **Sintoma**: Muitos valores vazios após merges
    - **Solução**: 
      - Preenche com valores padrão (`'Others'` para tipos, `'Others'` para USI)
      - Mantém `NaN` apenas onde faz sentido (ex: `Fornecedor`)
    """)

st.markdown("### Validações Implementadas")
st.markdown("""
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
""")

st.markdown("---")

# Seção Final: Notas Importantes
st.markdown("## 📝 NOTAS IMPORTANTES")

st.markdown("### Normalização de Material")
st.warning("""
**CRÍTICO**: Material deve ser tratado como `string` desde o início
- Remove zeros à esquerda de strings numéricas (ex: `"0123"` → `"123"`)
- Remove espaços invisíveis e caracteres não imprimíveis
- Garante match entre KE5Z e KSBB mesmo com variações de formato
""")

st.markdown("### Ordem de Colunas no Excel")
st.info("""
A ordem final das colunas no Excel é:
1. `Mes`, 2. `Período`, 3. `Nºconta`, 4. `Centrocst`, 5. `Nºdoc.ref.`,
6. `Dt.lçto.`, 7. `Valor`, 8. `QTD`, 9. `Type 05`, 10. `Type 06`,
11. `Account` (Type 07), 12. `USI`, 13. `Oficina`, 14. `Doc.compra`,
15. `Texto breve`, 16. `Fornecedor`, 17. `Material`, 18. `Usuário`,
19. `Fornec.`, 20. `Tipo`
""")

st.markdown("### Filtro de Meses")
st.info("""
- Variável de ambiente: `MESES_FILTRO` (ex: `"9,10,11"`)
- Aplicado antes de salvar arquivos Excel
- Não afeta arquivos Parquet (sempre completos)
""")

st.markdown("### Portabilidade")
st.info("""
- Funções `get_base_path()` e `get_output_path()` garantem portabilidade
- No executável: busca em `_internal` primeiro, depois diretório do executável
- Em desenvolvimento: usa diretório do script
""")

st.markdown("---")

# Checklist Final
st.markdown("## ✅ CHECKLIST PARA MODIFICAÇÕES")

checklist = [
    "Padronização de colunas está atualizada?",
    "Chaves de merge estão corretas?",
    "Tipos de dados estão consistentes?",
    "Validações estão implementadas?",
    "Tratamento de erros está completo?",
    "Arquivos de saída estão corretos?",
    "Ordem de colunas no Excel está correta?",
    "Normalização de Material está funcionando?",
    "Portabilidade está garantida?"
]

for item in checklist:
    st.markdown(f"- [ ] {item}")

st.markdown("---")

# Rodapé com versão
exibir_rodape_versao()

