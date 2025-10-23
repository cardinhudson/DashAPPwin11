# %%
# SOLUÇÃO DEFINITIVA PARA PROBLEMA PYVENV.CFG
import sys
import os
from pathlib import Path

# Limpar variáveis de ambiente virtual que causam problemas
vars_para_limpar = [
    'VIRTUAL_ENV', 'PYTHONHOME', 'CONDA_DEFAULT_ENV', 
    'PIPENV_ACTIVE', 'POETRY_ACTIVE', 'PYTHONPATH',
    'PYENV_VERSION', 'CONDA_PYTHON_EXE', 'CONDA_EXE'
]

for var in vars_para_limpar:
    if var in os.environ:
        del os.environ[var]

# Garantir que arquivo pyvenv.cfg existe se necessário
pyvenv_path = Path("pyvenv.cfg")
if not pyvenv_path.exists():
    python_exe = sys.executable
    python_home = str(Path(python_exe).parent)
    
    config_content = f"""home = {python_home}
executable = {python_exe}
command = {python_exe} -m venv {os.path.dirname(os.path.abspath(__file__))}
include-system-site-packages = true
version = {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}
prompt = Dash
"""
    try:
        with open(pyvenv_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print(f"Arquivo pyvenv.cfg criado automaticamente")
    except Exception as e:
        print(f"Aviso: Não foi possível criar pyvenv.cfg: {e}")

# Verificar Python ativo
print(f"Python ativo: {sys.executable}")
print(f"Diretorio: {os.getcwd()}")

# Verificação de caminhos para executável (não invasiva)
if hasattr(sys, '_MEIPASS'):
    print(f"Executando no PyInstaller - pasta _internal: {sys._MEIPASS}")
    print(f"Pasta do executável: {os.path.dirname(sys.executable)}")

# ================== CAMINHOS PADRONIZADOS (relativos à pasta principal) ==================
# Pasta raiz do projeto (para ENTRADA - dentro do _internal)
ROOT_DIR = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(os.path.abspath(__file__))

# Pasta raiz para SAÍDA (dentro do _internal para manter consistência)
if hasattr(sys, '_MEIPASS'):
    # No executável: salvar dentro do _internal para manter consistência
    OUTPUT_DIR = sys._MEIPASS
else:
    # Em desenvolvimento: mesmo diretório
    OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Pastas de entrada (dentro do _internal)
DIR_EXTRACOES = os.path.join(ROOT_DIR, "Extracoes")
DIR_KE5Z_IN = os.path.join(DIR_EXTRACOES, "KE5Z")
DIR_KSBB_IN = os.path.join(DIR_EXTRACOES, "KSBB")

# Arquivos auxiliares de entrada (dentro do _internal)
ARQ_SAPIENS = os.path.join(ROOT_DIR, "Dados SAPIENS.xlsx")
ARQ_FORNECEDORES = os.path.join(ROOT_DIR, "Fornecedores.xlsx")

# Pastas/arquivos de saída (dentro do _internal)
DIR_KE5Z_OUT = os.path.join(OUTPUT_DIR, "KE5Z")
DIR_ARQUIVOS_OUT = os.path.join(OUTPUT_DIR, "arquivos")
# ======================================================================

import pandas as pd

# Obter diretório base (onde está o executável)
if hasattr(sys, '_MEIPASS'):
    # Executando dentro do PyInstaller
    base_dir = sys._MEIPASS
    print(f"Executando dentro do PyInstaller: {base_dir}")
else:
    # Executando normalmente - usar diretório do script atual
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Executando normalmente: {base_dir}")

# Usar pasta local do projeto: Extracoes\KE5Z
pasta = DIR_KE5Z_IN

# Verificar se a pasta local existe
if not os.path.exists(pasta):
    print(f"ERRO: Pasta local {pasta} não encontrada!")
    print(f"Pasta procurada: {os.path.abspath(pasta)}")
    if hasattr(sys, '_MEIPASS'):
        print(f"Pasta _internal: {sys._MEIPASS}")
        print(f"Pasta do executável: {os.path.dirname(sys.executable)}")
    print("Criando pasta local...")
    os.makedirs(pasta, exist_ok=True)
    print(f"Pasta local criada: {os.path.abspath(pasta)}")
    print("Coloque os arquivos .txt na pasta Extracoes/KE5Z/ do projeto")
    exit(1)

print(f"Pasta encontrada: {pasta}")
# Lista para armazenar os DataFrames
dataframes = []

# Iterar sobre todos os arquivos na pasta
arquivos_txt = [f for f in os.listdir(pasta) if f.endswith('.txt')]
print(f"Arquivos .txt encontrados: {len(arquivos_txt)}")

for i, arquivo in enumerate(arquivos_txt, 1):
    caminho_arquivo = os.path.join(pasta, arquivo)
    
    print(f"\n[{i}/{len(arquivos_txt)}] Processando: {arquivo}")
    print(f"Caminho: {caminho_arquivo}")
    
    try:
        # Verificar tamanho do arquivo
        tamanho_mb = os.path.getsize(caminho_arquivo) / (1024 * 1024)
        print(f"Tamanho: {tamanho_mb:.1f} MB")
        
        # Ler o arquivo em um DataFrame com tratamento de erro
        print("Carregando dados...")
        df = pd.read_csv(
            caminho_arquivo, 
            sep='\t', 
            skiprows=9,
            encoding='latin1', 
            engine='c',  # Engine C é mais rápida para arquivos grandes
            low_memory=False  # Evitar warnings de tipos mistos
        )
        print(f"Carregado: {len(df):,} registros, {len(df.columns)} colunas")
        
        # mudar o nome da coluna Doc.ref. pelo seu índice
        if len(df.columns) > 9:
            df.rename(columns={df.columns[9]: 'doc.ref'}, inplace=True)
        
        print(f"Processando dados de {arquivo}...")
        
        # Remover espaços em branco dos nomes das colunas
        df.columns = df.columns.str.strip()
        print("Limpando dados...")
        
        # Filtrar a coluna 'Ano' com valores não nulos e diferentes de 0
        df = df[df['Ano'].notna() & (df['Ano'] != 0)]
        print(f"Após filtro Ano: {len(df):,} registros")
        
        # Substituir ',' por '.' e remover pontos de separação de milhar
        print("Convertendo coluna Em MCont...")
        df['Em MCont.'] = (
            df['Em MCont.']
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
        )
        # Converter a coluna para float, tratando erros
        df['Em MCont.'] = pd.to_numeric(df['Em MCont.'], errors='coerce')
        # Substituir valores NaN por 0 (ou outro valor padrão, se necessário)
        df['Em MCont.'] = df['Em MCont.'].fillna(0)

        # Substituir ',' por '.' e remover pontos de separação de milhar
        print("Convertendo coluna Qtd...")
        df['Qtd.'] = (
            df['Qtd.']
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
        )
        # Converter a coluna para float, tratando erros
        df['Qtd.'] = pd.to_numeric(df['Qtd.'], errors='coerce')
        # Substituir valores NaN por 0 (ou outro valor padrão, se necessário)
        df['Qtd.'] = df['Qtd.'].fillna(0)
        
        # Adicionar o DataFrame à lista
        dataframes.append(df)
        print(f"{arquivo} processado com sucesso!")
        
        # Imprimir o valor total da coluna 'Em MCont.'
        total_em_mcont = df['Em MCont.'].sum()
        print(f"Total Em MCont. em {arquivo}: {total_em_mcont:,.2f}")
        
    except Exception as e:
        print(f"Erro ao processar {arquivo}: {str(e)}")
        continue


# Concatenar todos os DataFrames em um único
if dataframes:
    df_total = pd.concat(dataframes, ignore_index=True)
else:
    print("AVISO: Nenhum arquivo .txt encontrado em KE5Z.")
    df_total = pd.DataFrame()


# Remover colunas desnecessárias
colunas_para_remover = [
    'Unnamed: 0',
    'Unnamed: 1',
    'Unnamed: 4',
    'Nº doc.',
    'Elem.PEP',
    'Obj.custo',
    'TD',
    'SocPar',
    'EmpEm.',
    'Empr',
    'TMv',
    'D/C',
    'Imobil.',
    # Colunas restauradas - removidas da lista de remoção:
    # 'Descrição Material',  # RESTAURADA
    # 'Cliente',            # RESTAURADA
    # 'Cen.',              # RESTAURADA  
    # 'Cen.lucro',         # RESTAURADA
    # 'Unnamed: 14',       # RESTAURADA
    # 'Classe objs.',      # RESTAURADA
    # 'Item',              # RESTAURADA
    # 'D',                 # RESTAURADA
]
df_total.drop(columns=colunas_para_remover, inplace=True, errors='ignore')
print(df_total.columns)

# mudar tipo da coluna 'Cliente' e 'Imobil.' para string
df_total['Cliente'] = df_total['Cliente'].astype(str)  # Cliente restaurada

# imprimir a coluna 'Em MCont.'
print(df_total['Em MCont.'])
#
#
#
#
#
# %%
# Modificar o nome da coluna 'Em MCont.' para 'Valor'
df_total.rename(columns={'Em MCont.': 'Valor'}, inplace=True)

# filtrar a coluna Nº conta não vazias e diferentes de 0
df_total = df_total[df_total['Nº conta'].notna() & (df_total['Nº conta'] != 0)]
print(len(df_total))

print(df_total.head(10))  # Exibir as primeiras linhas do DataFrame total


# Usar pasta local do projeto para KSBB: Extracoes\KSBB
pasta_ksbb = DIR_KSBB_IN

# Verificar se a pasta local existe
if not os.path.exists(pasta_ksbb):
    print(f"AVISO: Pasta local {pasta_ksbb} não encontrada!")
    print(f"Pasta procurada: {os.path.abspath(pasta_ksbb)}")
    print("Criando pasta local...")
    os.makedirs(pasta_ksbb, exist_ok=True)
    print(f"Pasta local criada: {os.path.abspath(pasta_ksbb)}")
    print("Coloque os arquivos .txt na pasta Extracoes/KSBB/ do projeto")
    # Não sair do script, apenas pular a parte do KSBB
    pasta_ksbb = None

print(f"Pasta KSBB encontrada: {pasta_ksbb}")
# Lista para armazenar os DataFrames
dataframes_ksbb = []

# Iterar sobre todos os arquivos na pasta (apenas se disponível)
if pasta_ksbb:
    for arquivo in os.listdir(pasta_ksbb):
        caminho_arquivo = os.path.join(pasta_ksbb, arquivo)

        # Verificar se é um arquivo e tem a extensão desejada (.csv)
        if os.path.isfile(caminho_arquivo) and arquivo.endswith('.txt'):
            print(f"Lendo: {arquivo}")

            # Ler o arquivo em um DataFrame
            df_ksbb = pd.read_csv(
                caminho_arquivo,
                sep='\t',
                encoding='latin1',
                engine='python',
                skiprows=3,
                skipfooter=1,
            )

            # remover espaços em branco dos nomes das colunas
            df_ksbb.columns = df_ksbb.columns.str.strip()

            # Filtrar a coluna Material com não vazias e diferentes de 0
            df_ksbb = df_ksbb[
                df_ksbb['Material'].notna() & (df_ksbb['Material'] != 0)
            ]

            # remover as linhas duplicadas pela coluna Material
            df_ksbb = df_ksbb.drop_duplicates(subset=['Material'])

            # Adicionar o DataFrame à lista
            dataframes_ksbb.append(df_ksbb)
else:
    print("Pulando processamento KSBB (pasta não disponível).")


# Concatenar todos os DataFrames em um único e ignorar caso tenha apenas 1
if len(dataframes_ksbb) > 1:
    df_ksbb = pd.concat(dataframes_ksbb, ignore_index=True)
elif len(dataframes_ksbb) == 1:
    df_ksbb = dataframes_ksbb[0]
else:
    df_ksbb = pd.DataFrame()

# remover as linhas duplicadas pela coluna Material
df_ksbb = df_ksbb.drop_duplicates(subset=['Material'])

# merge o df_total com df_ksbb_total pela coluna Material trazendo a coluna de texto breve material do df_ksbb_total
if not df_total.empty and not df_ksbb.empty and 'Material' in df_total.columns:
    df_total = pd.merge(
        df_total,
        df_ksbb[['Material', 'Texto breve material']],
        on='Material',
        how='left',
    )

# renomear a coluna Texto breve material para Descrição Material
df_total = df_total.rename(
    columns={'Texto breve material': 'Descrição Material'}
)

# exibir as 10 primeiras linhas do df_total e as colunas de Material, Descrição Material
if 'Material' in df_total.columns and 'Descrição Material' in df_total.columns:
    print(df_total[['Material', 'Descrição Material']].head(10))

# se a descrição do material nao for nula substituir o valor da coluna Texto pelo valor da Descrição Material
if 'Texto' in df_total.columns and 'Descrição Material' in df_total.columns:
    df_total['Texto'] = df_total.apply(
        lambda row: (
            row['Descrição Material']
            if pd.notnull(row['Descrição Material'])
            else row['Texto']
        ),
        axis=1,
    )

# imprimir os valores totais somarizado por periodo
print(df_total.groupby('Período')['Valor'].sum())
# mudar o tipo de coluna nº conta para string
df_total['Nº conta'] = df_total['Nº conta'].astype(str)

# %%
# Ler o arquivo Excel Dados SAPIENS.xlsx
arquivo_sapiens = ARQ_SAPIENS
df_sapiens = pd.read_excel(arquivo_sapiens, sheet_name='Conta contabil')

# mudar o nome da coluna 'CONTA SAPIENS' para Nº conta
df_sapiens.rename(columns={'CONTA SAPIENS': 'Nº conta'}, inplace=True)
print(df_sapiens.head())
# mudar o tipo da coluna Nº conta para string
df_sapiens['Nº conta'] = df_sapiens['Nº conta'].astype(str)

# Merger o arquivo df_total pela coluna Nº conta com o df_sapiens pela coluna CONTA SAPIENS
df_total = pd.merge(
    df_total,
    df_sapiens[['Nº conta', 'Type 07', 'Type 06', 'Type 05']],
    on='Nº conta',
    how='left',
)

# Ler o arquivo Excel Dados SAPIENS.xlsx e a aba CC
df_CC = pd.read_excel(arquivo_sapiens, sheet_name='CC')

# mudar o nome da coluna CC SAPiens da df_sapiens para Centro cst
df_CC.rename(columns={'CC SAPiens': 'Centro cst'}, inplace=True)

# Merge o df_total com o df_CC pela coluna Centro cst e trazer as colunas Ofincina e USI
df_total = pd.merge(
    df_total,
    df_CC[['Centro cst', 'Oficina', 'USI']],
    on='Centro cst',
    how='left',
)
# Substituir na coluna 'USI' os valores NaN por 'Others'
df_total['USI'] = df_total['USI'].fillna('Others')
# Exibir as 10 primeiras linhas do df_total e as colunas de Nº conta, Type 07, Type 06, Type 05, Centro cst, Oficina e USI
print(
    df_total[
        [
            'Nº conta', 'Type 07', 'Type 06', 'Type 05',
            'Centro cst', 'Oficina', 'USI'
        ]
    ].head(10)
)

# %%
# Limpar e converter tipos de dados antes de salvar parquet
print("Limpando e convertendo tipos de dados...")

# Converter coluna Ano e Período para numérico
for col in ['Ano', 'Período']:
    if col in df_total.columns:
        df_total[col] = pd.to_numeric(df_total[col], errors='coerce')

# Converter colunas numéricas que podem estar como string
numeric_columns = ['Valor', 'Qtd.', 'doc.ref', 'Item']
for col in numeric_columns:
    if col in df_total.columns:
        df_total[col] = pd.to_numeric(df_total[col], errors='coerce')

# Garantir que colunas de texto sejam strings
text_columns = ['Nº conta', 'Centro cst', 'Texto', 'Fornecedor', 'Fornec.', 'Material', 
                'Descrição Material', 'Type 05', 'Type 06', 'Type 07', 'USI', 'Oficina',
                'Doc.compra', 'Usuário', 'Tipo', 'Cliente', 'Dt.lçto.', 'Imobilizado']
for col in text_columns:
    if col in df_total.columns:
        df_total[col] = df_total[col].astype(str)

# Garantir que TODAS as colunas object sejam strings (fallback)
for col in df_total.columns:
    if df_total[col].dtype == 'object':
        df_total[col] = df_total[col].astype(str)

# Substituir valores NaN por None para compatibilidade com PyArrow
df_total = df_total.where(pd.notnull(df_total), None)

# Converter coluna Dt.lçto. para formato DD/MM/AAAA
if 'Dt.lçto.' in df_total.columns:
    print("Convertendo coluna Dt.lçto. para formato DD/MM/AAAA...")
    df_total['Dt.lçto.'] = df_total['Dt.lçto.'].astype(str)
    df_total['Dt.lçto.'] = df_total['Dt.lçto.'].str.replace('.', '/', regex=False)
    print(f"Coluna Dt.lçto. convertida: {df_total['Dt.lçto.'].head(3).tolist()}")

print("Tipos de dados após limpeza:")
print(df_total.dtypes)


# %% Salvar arquivo para extração PBI
# ler arquivo fornecedores e desconsiderar as 3 primeiras linhas
arquivo_fornecedores = ARQ_FORNECEDORES
df_fornecedores = pd.read_excel(arquivo_fornecedores, skiprows=3)
# remover linhas duplicadas pela coluna Fornecedor
df_fornecedores = df_fornecedores.drop_duplicates(subset=['Fornecedor'])
# mudar o nome da coluna Fornecedor para Fornec.
df_fornecedores.rename(columns={'Fornecedor': 'Fornec.'}, inplace=True)

# mudar a coluna fornec. para string
df_fornecedores['Fornec.'] = df_fornecedores['Fornec.'].astype(str)

# merge o df_total com df_fornecedores pela coluna Fornec. retornando a coluna Fornecedor
df_total = pd.merge(
    df_total,
    df_fornecedores[['Fornec.', 'Nome do fornecedor']],
    on='Fornec.',
    how='left',
)
# mudar o nome da coluna Nome do fornecedor para Fornecedor
df_total.rename(columns={'Nome do fornecedor': 'Fornecedor'}, inplace=True)



# Atualizar o nome do fornecedor com as provisoes
# Precimos ler o arquivo Dados SAPIENS.xlsx na pasta do projeto na guia Hist_prov 
# desconsiderar a primeira linha do arquivo
arquivo_hist_prov = os.path.join(base_dir, "Dados SAPIENS.xlsx")
df_hist_prov = pd.read_excel(arquivo_hist_prov, sheet_name='Hist_prov', skiprows=1)
# excluir todas as colunas menos as colunas 'Nome do fornecedor', '20carac'
df_hist_prov = df_hist_prov[['Nome do fornecedor', '20carac']]
# Remover os espaços da coluna '20carac'
df_hist_prov['20carac'] = df_hist_prov['20carac'].str.strip()

# remover linhas duplicadas pela coluna '20carac'
df_hist_prov = df_hist_prov.drop_duplicates(subset=['20carac'])

# criar uma coluna no df_total chamada '20carac' (primeiros 20 caracteres do Fornec.) 
df_total['20carac'] = df_total['Texto'].astype(str).str[:20]
# Remover os espaços da coluna '20carac'
df_total['20carac'] = df_total['20carac'].str.strip()



# merge o df_total com df_hist_prov pela coluna 20carac retornando a coluna 'Nome do fornecedor'
df_total = pd.merge(
    df_total,
    df_hist_prov[['20carac', 'Nome do fornecedor']],
    on='20carac',
    how='left',
)

# Se a coluna 'Nome do fornecedor' não for nula, substituir o valor da coluna Fornecedor pelo valor da coluna 'Nome do fornecedor'
if 'Nome do fornecedor' in df_total.columns and 'Fornecedor' in df_total.columns:
    df_total['Fornecedor'] = df_total.apply(
        lambda row: (
            row['Nome do fornecedor']
            if pd.notnull(row['Nome do fornecedor'])
            else row['Fornecedor']
        ),
        axis=1,
    )


# Colocar as colunas Type 07, Type 06, Type 05 que forem vazias ou nulas como Others
df_total['Type 07'] = df_total['Type 07'].fillna('Others')
df_total['Type 06'] = df_total['Type 06'].fillna('Others')
df_total['Type 05'] = df_total['Type 05'].fillna('Others')


# # gerar um arquivo parquet do df_total atualizado
pasta_parquet = DIR_KE5Z_OUT
os.makedirs(pasta_parquet, exist_ok=True)
print(f"Pasta parquet criada: {pasta_parquet}")

# OTIMIZAÇÃO DE MEMÓRIA: Separar dados por USI
print("\n=== SEPARANDO ARQUIVOS POR USI PARA OTIMIZAÇÃO ===")

# Separar dados Others vs resto
df_others = df_total[df_total['USI'] == 'Others'].copy()
df_main = df_total[df_total['USI'] != 'Others'].copy()

print(f"Total de registros: {len(df_total):,}")
print(f"Registros principais (sem Others): {len(df_main):,}")
print(f"Registros Others: {len(df_others):,}")

# Salvar arquivo principal (sem Others) - para uso no dashboard
caminho_main = os.path.join(pasta_parquet, 'KE5Z_main.parquet')
df_main.to_parquet(caminho_main, index=False)
print(f"Arquivo principal salvo: {caminho_main}")

# Salvar arquivo Others separadamente
if len(df_others) > 0:
    caminho_others = os.path.join(pasta_parquet, 'KE5Z_others.parquet')
    df_others.to_parquet(caminho_others, index=False)
    print(f"Arquivo Others salvo: {caminho_others}")
else:
    print("Nenhum registro Others encontrado")

# Manter arquivo completo para compatibilidade
caminho_saida_atualizado = os.path.join(pasta_parquet, 'KE5Z.parquet')
df_total.to_parquet(caminho_saida_atualizado, index=False)
print(f"Arquivo completo salvo: {caminho_saida_atualizado}")

# gerar um arquivo Excel do df_total atualizado com 10k linhas
caminho_saida_excel = os.path.join(pasta_parquet, 'KE5Z.xlsx')
df_total.head(10000).to_excel(caminho_saida_excel, index=False)
print(f"Arquivo Excel salvo: {caminho_saida_excel}")

# CRIAR ARQUIVO WATERFALL OTIMIZADO (72% menor) - ANTES DA RENOMEAÇÃO
print("\n=== CRIANDO ARQUIVO WATERFALL OTIMIZADO ===")

# Definir colunas essenciais para o waterfall (COM Type 07 ORIGINAL!)
colunas_waterfall = [
    'Período',      # OBRIGATÓRIA - Para seleção de meses
    'Valor',        # OBRIGATÓRIA - Para cálculos
    'USI',          # Filtro principal + dimensão
    'Type 05',      # Dimensão de categoria
    'Type 06',      # Dimensão de categoria
    'Type 07',      # Dimensão de categoria (ANTES da renomeação!)
    'Fornecedor',   # Dimensão de categoria + filtro
    'Fornec.',      # Filtro
    'Tipo',         # Filtro
    'Nº conta'      # NOVO: Filtro com EXCELENTE compressão (269 únicos/3M registros = 0.01%)
]

# Verificar quais colunas existem
colunas_existentes = [col for col in colunas_waterfall if col in df_total.columns]
colunas_faltantes = [col for col in colunas_waterfall if col not in df_total.columns]

print(f"Colunas encontradas ({len(colunas_existentes)}): {colunas_existentes}")
if colunas_faltantes:
    print(f"Colunas não encontradas ({len(colunas_faltantes)}): {colunas_faltantes}")

# Filtrar apenas colunas essenciais
if len(colunas_existentes) >= 3:  # Pelo menos Período, Valor, USI
    df_waterfall = df_total[colunas_existentes].copy()
    
    print(f"Dados filtrados: {len(df_waterfall):,} registros, {len(df_waterfall.columns)} colunas")
    
    # Aplicar otimizações de memória
    print("Aplicando otimizações de memória...")
    
    # Converter strings categóricas para category
    for col in df_waterfall.columns:
        if df_waterfall[col].dtype == 'object':
            unique_ratio = df_waterfall[col].nunique(dropna=True) / max(1, len(df_waterfall))
            if unique_ratio < 0.5:  # Se menos de 50% são valores únicos
                df_waterfall[col] = df_waterfall[col].astype('category')
                print(f"  {col}: convertido para category ({unique_ratio:.1%} únicos)")
    
    # Otimizar tipos numéricos
    for col in df_waterfall.select_dtypes(include=['float64']).columns:
        df_waterfall[col] = pd.to_numeric(df_waterfall[col], downcast='float')
        print(f"  {col}: otimizado para float32")
    
    for col in df_waterfall.select_dtypes(include=['int64']).columns:
        df_waterfall[col] = pd.to_numeric(df_waterfall[col], downcast='integer')
        print(f"  {col}: otimizado para int32")
    
    # Remover registros com valores nulos nas colunas críticas
    antes_limpeza = len(df_waterfall)
    df_waterfall = df_waterfall.dropna(subset=['Período', 'Valor'])
    depois_limpeza = len(df_waterfall)
    
    if antes_limpeza != depois_limpeza:
        print(f"Removidos {antes_limpeza - depois_limpeza:,} registros com valores nulos")
    
    # Salvar arquivo otimizado
    arquivo_waterfall = os.path.join(pasta_parquet, "KE5Z_waterfall.parquet")
    df_waterfall.to_parquet(arquivo_waterfall, index=False)
    
    # Calcular redução de tamanho
    try:
        tamanho_original = os.path.getsize(caminho_saida_atualizado) / (1024*1024)
        tamanho_waterfall = os.path.getsize(arquivo_waterfall) / (1024*1024)
        reducao = ((tamanho_original - tamanho_waterfall) / tamanho_original) * 100
        
        print(f"ARQUIVO WATERFALL CRIADO COM SUCESSO!")
        print(f"Arquivo: {arquivo_waterfall}")
        print(f"Registros: {len(df_waterfall):,}")
        print(f"Colunas: {list(df_waterfall.columns)}")
        print(f"Tamanho original: {tamanho_original:.1f} MB")
        print(f"Tamanho otimizado: {tamanho_waterfall:.1f} MB")
        print(f"Redução: {reducao:.1f}%")
        
        # Verificar se Type 07 está presente
        if 'Type 07' in df_waterfall.columns:
            valores_unicos = df_waterfall['Type 07'].nunique()
            print(f"Type 07 incluído com {valores_unicos:,} valores únicos!")
        
    except Exception as e:
        print(f"Erro ao calcular tamanhos: {e}")
        print(f"Arquivo waterfall salvo: {arquivo_waterfall}")
else:
    print("Colunas insuficientes para criar arquivo waterfall")

#
#
# %%
# Salvar arquivos Excel na pasta local do projeto

# organizar a ordem das colunas em Período	Nºconta	Centrocst	doc.ref.	Dt.lçto.	Cen.lucro	 Valor 	QTD	Type 05	Type 06	Account	USI	Oficina	Doc.compra	Texto breve	Fornecedor	Material	DESCRIÇÃO SAPIENS	Usuário	Cofor	Tipo
df_total = df_total[['Período', 'Nº conta', 'Centro cst', 'doc.ref', 'Dt.lçto.', 'Valor', 'Qtd.', 'Type 05', 'Type 06', 'Type 07', 'USI', 'Oficina', 'Doc.compra', 'Texto', 'Fornecedor', 'Material', 'Usuário', 'Fornec.', 'Tipo']]

# mudar os nomes das colunas para Nºconta, Centrocst, Nºdoc.ref., QTD, Texto
df_total.rename(columns={'Texto': 'Texto breve'}, inplace=True)
df_total.rename(columns={'Qtd.': 'QTD'}, inplace=True)
df_total.rename(columns={'Nº conta': 'Nºconta', 'Centro cst': 'Centrocst', 'doc.ref': 'Nºdoc.ref.'}, inplace=True)
# Mudar o nome da coluna Type 07 para Account
df_total.rename(columns={'Type 07': 'Account'}, inplace=True)
# Mudar o nome da coluna 'Periodo' para Mes
df_total.rename(columns={'Período': 'Mes'}, inplace=True)

# Criar uma coluna com os meses minusculos baseados na coluna 'Mes', sendo mes = 1 = janeiro, mes = 2 = fevereiro e assim sucessivamente
# a coluna Mes deve ser string
df_total['Período'] = df_total['Mes'].astype(str)
df_total['Período'] = df_total['Mes'].apply(lambda x: 'janeiro' if x == 1 else 'fevereiro' if x == 2 else 'março' if x == 3 else 'abril' if x == 4 else 'maio' if x == 5 else 'junho' if x == 6 else 'julho' if x == 7 else 'agosto' if x == 8 else 'setembro' if x == 9 else 'outubro' if x == 10 else 'novembro' if x == 11 else 'dezembro')

# Trazer coluna 'mes' para a primeira posição e a coluna 'Período' para a segunda posição do DataFrame
colunas = ['Mes', 'Período'] + [col for col in df_total.columns if col != 'Mes' and col != 'Período']
df_total = df_total[colunas]




# Ler filtro de meses da variável de ambiente (enviada pela página de extração)
meses_env = os.environ.get('MESES_FILTRO', '').strip()
meses_filtrados = None
if meses_env:
    try:
        meses_filtrados = {int(x) for x in meses_env.split(',') if str(x).strip().isdigit()}
        if meses_filtrados:
            print(f"Aplicando filtro de meses (MESES_FILTRO): {sorted(meses_filtrados)}")
    except Exception as e:
        print(f"Aviso: não foi possível interpretar MESES_FILTRO='{meses_env}': {e}")
        meses_filtrados = None

# Se houver filtro, aplicar sobre os DataFrames antes de salvar
if meses_filtrados and 'Mes' in df_total.columns:
    df_total_excel = df_total[df_total['Mes'].isin(meses_filtrados)].copy()
    print(f"Filtro aplicado: {len(df_total_excel):,} linhas após filtrar meses {sorted(meses_filtrados)}")
else:
    df_total_excel = df_total.copy()
    print(f"Sem filtro aplicado: {len(df_total_excel):,} linhas totais")

# Criar pasta 'arquivos' local para salvar os arquivos Excel
pasta_arquivos = DIR_ARQUIVOS_OUT
os.makedirs(pasta_arquivos, exist_ok=True)
print(f"Pasta de arquivos criada: {pasta_arquivos}")

# Salvar arquivo Excel completo primeiro (DESABILITADO - arquivo muito grande para Excel)
# caminho_completo = os.path.join(pasta_arquivos, 'KE5Z_completo.xlsx')
# df_total_excel.to_excel(caminho_completo, index=False)
print(f"Arquivo Excel completo NÃO salvo (dados muito grandes: {len(df_total_excel):,} linhas > limite Excel 1.048.576)")

# Verificar quais USIs existem nos dados
usis_disponiveis = df_total_excel['USI'].unique() if 'USI' in df_total_excel.columns else []
print(f"USIs disponíveis nos dados: {list(usis_disponiveis)}")

# Salvar arquivo Excel com filtro de USI 'Veículos', 'TC Ext' e 'LC' (se existirem)
usis_veiculos = ['Veículos', 'TC Ext', 'LC']
usis_veiculos_existentes = [usi for usi in usis_veiculos if usi in usis_disponiveis]

if usis_veiculos_existentes:
    caminho_veiculos = os.path.join(pasta_arquivos, 'KE5Z_veiculos.xlsx')
    df_veiculos = df_total_excel[df_total_excel['USI'].isin(usis_veiculos_existentes)]
    df_veiculos.to_excel(caminho_veiculos, index=False)
    print(f"Arquivo Excel Veículos salvo: {caminho_veiculos} ({len(df_veiculos)} registros)")
else:
    print("Nenhuma USI de veículos encontrada nos dados")

# Salvar arquivo Excel com filtro de USI 'PWT' (se existir)
if 'PWT' in usis_disponiveis:
    caminho_pwt = os.path.join(pasta_arquivos, 'KE5Z_pwt.xlsx')
    df_pwt = df_total_excel[df_total_excel['USI'] == 'PWT']
    df_pwt.to_excel(caminho_pwt, index=False)
    print(f"Arquivo Excel PWT salvo: {caminho_pwt} ({len(df_pwt)} registros)")
else:
    print("USI PWT não encontrada nos dados")

# Salvar arquivo Excel separado por USI (apenas USIs que NÃO foram agrupadas)
if 'USI' in df_total_excel.columns:
    usis_ja_salvas = set(usis_veiculos_existentes + (['PWT'] if 'PWT' in usis_disponiveis else []))
    for usi in usis_disponiveis:
        if pd.notna(usi) and usi != 'Others' and usi not in usis_ja_salvas:
            # Normalizar nome da USI para evitar duplicação
            nome_arquivo = usi.replace(" ", "_").replace("/", "_").replace("ç", "c").replace("ã", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
            caminho_usi = os.path.join(pasta_arquivos, f'KE5Z_{nome_arquivo}.xlsx')
            df_usi = df_total_excel[df_total_excel['USI'] == usi]
            if len(df_usi) > 0:
                df_usi.to_excel(caminho_usi, index=False)
                print(f"Arquivo Excel {usi} salvo: {caminho_usi} ({len(df_usi)} registros)")

# Mensagem final com link clicável para a pasta de arquivos Excel
pasta_arquivos_absoluta = os.path.abspath(pasta_arquivos)
print("\n" + "="*80)
print("✅ EXTRAÇÃO CONCLUÍDA COM SUCESSO!")
print("="*80)
print(f"📁 Pasta dos arquivos Excel: {pasta_arquivos_absoluta}")
print("🔗 Para abrir a pasta, copie e cole este caminho no Windows Explorer:")
print(f"   {pasta_arquivos_absoluta}")
print("")
print("📊 Arquivos gerados:")
print("   • Arquivos Parquet: pasta KE5Z/")
print("   • Arquivos Excel: pasta arquivos/")
print("")
print("💡 Dica: Pressione Win+R, cole o caminho e pressione Enter para abrir a pasta!")
print("="*80)

# Tentar abrir a pasta automaticamente no Windows
try:
    import subprocess
    if os.name == 'nt':  # Windows
        subprocess.run(['explorer', pasta_arquivos_absoluta], check=False)
        print("🚀 Pasta aberta automaticamente no Windows Explorer!")
    else:
        print("ℹ️  Sistema não-Windows detectado. Abra a pasta manualmente.")
except Exception as e:
    print(f"⚠️  Não foi possível abrir a pasta automaticamente: {e}")
    print(f"   Abra manualmente: {pasta_arquivos_absoluta}")
