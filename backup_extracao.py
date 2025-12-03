#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ARQUIVO DE BACKUP - EXTRAÇÃO DE DADOS KE5Z
===========================================

Este arquivo é uma cópia standalone da extração de dados.
Ele NÃO depende do Streamlit e pode ser executado independentemente.

USO:
    python backup_extracao.py

IMPORTANTE:
    - Este arquivo usa caminhos relativos à raiz do projeto
    - Não interfere com o executável ou com o Streamlit
    - É apenas para backup caso o executável não funcione
    - Todos os arquivos de entrada devem estar na raiz do projeto

ESTRUTURA ESPERADA:
    Projeto/
    ├── backup_extracao.py (este arquivo)
    ├── Extracoes/
    │   ├── KE5Z/
    │   │   └── *.txt (arquivos de entrada)
    │   └── KSBB/
    │       └── *.txt (arquivos de entrada)
    ├── Dados SAPIENS.xlsx
    ├── Fornecedores.xlsx
    └── KE5Z/ (pasta de saída - será criada automaticamente)
        └── *.parquet, *.xlsx
"""

import sys
import os
from pathlib import Path
import pandas as pd

# ================== CONFIGURAÇÃO DE CAMINHOS (RAIZ DO PROJETO) ==================
# Obter diretório raiz do projeto (onde está este arquivo)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

print("="*80)
print("🔧 BACKUP DE EXTRAÇÃO - KE5Z")
print("="*80)
print(f"📁 Diretório raiz: {ROOT_DIR}")
print("="*80)

# Pastas de entrada (na raiz do projeto)
DIR_EXTRACOES = os.path.join(ROOT_DIR, "Extracoes")
DIR_KE5Z_IN = os.path.join(DIR_EXTRACOES, "KE5Z")
DIR_KSBB_IN = os.path.join(DIR_EXTRACOES, "KSBB")

# Arquivos auxiliares de entrada (na raiz do projeto)
ARQ_SAPIENS = os.path.join(ROOT_DIR, "Dados SAPIENS.xlsx")
ARQ_FORNECEDORES = os.path.join(ROOT_DIR, "Fornecedores.xlsx")

# Pastas/arquivos de saída (na raiz do projeto)
DIR_KE5Z_OUT = os.path.join(ROOT_DIR, "KE5Z")
DIR_ARQUIVOS_OUT = os.path.join(ROOT_DIR, "arquivos")
# ======================================================================

# ================== FUNÇÕES AUXILIARES ==================
def detectar_linha_cabecalho(caminho_arquivo, max_linhas=25):
    """
    Detecta automaticamente a linha do cabeçalho procurando por palavras-chave conhecidas.
    """
    palavras_chave_cabecalho = [
        'ano', 'período', 'periodo', 'nº conta', 'nºconta', 'conta',
        'centro cst', 'centrocst', 'em mcont', 'mcont', 'valor',
        'qtd', 'quantidade', 'doc.ref', 'docref', 'documento',
        'dt.lçto', 'data', 'material', 'fornec', 'fornecedor',
        'texto', 'cliente', 'usuário', 'usuario', 'tipo'
    ]
    
    try:
        with open(caminho_arquivo, 'r', encoding='latin1', errors='replace') as f:
            linhas = []
            for i, linha in enumerate(f):
                if i >= max_linhas:
                    break
                linhas.append(linha.lower().strip())
        
        melhor_linha = None
        melhor_pontuacao = 0
        
        for i, linha in enumerate(linhas):
            pontuacao = sum(1 for palavra in palavras_chave_cabecalho if palavra in linha)
            
            if '\t' in linha:
                colunas = linha.split('\t')
                if len(colunas) > 5:
                    pontuacao += 2
            
            if not any(char.isdigit() for char in linha[:50]):
                pontuacao += 1
            
            if pontuacao > melhor_pontuacao:
                melhor_pontuacao = pontuacao
                melhor_linha = i
        
        if melhor_pontuacao >= 3:
            return melhor_linha
        
        return None
    except Exception as e:
        print(f"   ⚠️  Erro ao detectar cabeçalho: {str(e)[:100]}")
        return None

def validar_cabecalho(df_temp, min_colunas=5, min_linhas=1):
    """Valida se o DataFrame lido parece ter um cabeçalho válido."""
    if df_temp is None:
        return False
    
    if len(df_temp.columns) < min_colunas or len(df_temp) < min_linhas:
        return False
    
    colunas_nomeadas = sum(1 for col in df_temp.columns if not str(col).startswith('Unnamed'))
    if colunas_nomeadas < min_colunas:
        return False
    
    colunas_nao_vazias = sum(1 for col in df_temp.columns if df_temp[col].notna().any())
    if colunas_nao_vazias < min_colunas:
        return False
    
    return True

def padronizar_colunas(df, arquivo_nome=""):
    """Padroniza nomes das colunas para garantir compatibilidade."""
    if df is None or len(df.columns) == 0:
        return df
    
    df.columns = df.columns.str.strip()
    
    mapeamento_colunas = {
        'Ano': ['ano', 'Ano', 'ANO', 'year', 'Year', 'YEAR'],
        'Período': ['período', 'Periodo', 'PERÍODO', 'PERIODO', 'period', 'Period', 
                   'PERIOD', 'mes', 'Mes', 'MES', 'mês', 'Mês'],
        'Nº conta': ['nº conta', 'Nº conta', 'Nºconta', 'nºconta', 'conta', 'Conta', 
                     'CONTA', 'Nº Conta', 'No conta', 'No. conta'],
        'Centro cst': ['centro cst', 'Centro cst', 'Centrocst', 'centrocst', 'CENTRO CST',
                      'centro', 'Centro', 'CENTRO', 'centro de custo', 'Centro de Custo'],
        'Texto': ['texto', 'Texto', 'TEXTO', 'descrição', 'Descrição', 'DESCRIÇÃO',
                 'texto breve', 'Texto breve', 'TEXTO BREVE', 'descrição material'],
        'Fornec.': ['fornec.', 'Fornec.', 'FORNEC.', 'fornecedor código', 'Fornecedor código',
                   'FORNECEDOR CÓDIGO', 'fornec', 'Fornec', 'FORNEC'],
        'Material': ['material', 'Material', 'MATERIAL', 'mat', 'Mat', 'MAT'],
        'Item': ['item', 'Item', 'ITEM'],
        'Cliente': ['cliente', 'Cliente', 'CLIENTE'],
        'doc.ref': ['doc.ref', 'doc.ref.', 'Doc.ref.', 'Doc.ref', 'DOC.REF', 'DOC.REF.',
                   'documento', 'Documento', 'DOCUMENTO', 'doc ref', 'Doc Ref'],
        'Dt.lçto.': ['dt.lçto.', 'Dt.lçto.', 'DT.LÇTO.', 'data', 'Data', 'DATA',
                    'data lançamento', 'Data Lançamento', 'data de lançamento'],
        'Em MCont.': ['em mcont.', 'Em MCont.', 'EM MCONT.', 'valor', 'Valor', 'VALOR',
                     'montante', 'Montante', 'MONTANTE', 'em mcont', 'Em MCont'],
        'Qtd.': ['qtd.', 'Qtd.', 'QTD.', 'quantidade', 'Quantidade', 'QUANTIDADE',
                'qtd', 'Qtd', 'QTD'],
        'Cen.lucro': ['cen.lucro', 'Cen.lucro', 'CEN.LUCRO', 'centro lucro', 'Centro Lucro',
                     'centro de lucro', 'Centro de Lucro'],
        'Usuário': ['usuário', 'Usuário', 'USUÁRIO', 'usuario', 'Usuario', 'USUARIO',
                   'user', 'User', 'USER'],
        'Tipo': ['tipo', 'Tipo', 'TIPO', 'type', 'Type', 'TYPE'],
        'Doc.compra': ['doc.compra', 'Doc.compra', 'DOC.COMPRA', 'documento compra',
                      'Documento Compra', 'doc compra'],
    }
    
    renomeacao = {}
    colunas_originais = df.columns.tolist()
    
    for nome_fixo, variações in mapeamento_colunas.items():
        if nome_fixo in colunas_originais:
            continue
        
        coluna_encontrada = None
        
        for col_original in colunas_originais:
            if col_original.strip().lower() in [v.lower() for v in variações]:
                coluna_encontrada = col_original
                break
        
        if not coluna_encontrada:
            for col_original in colunas_originais:
                col_lower = col_original.strip().lower()
                for variacao in variações:
                    if variacao.lower() in col_lower or col_lower in variacao.lower():
                        coluna_encontrada = col_original
                        break
                if coluna_encontrada:
                    break
        
        if coluna_encontrada and coluna_encontrada not in renomeacao.keys():
            renomeacao[coluna_encontrada] = nome_fixo
            if arquivo_nome:
                print(f"   🔄 '{coluna_encontrada}' → '{nome_fixo}'")
    
    if renomeacao:
        df.rename(columns=renomeacao, inplace=True)
        print(f"   ✅ {len(renomeacao)} coluna(s) padronizada(s)")
    
    return df
# ======================================================================

# ================== PROCESSAMENTO PRINCIPAL ==================
print("\n📂 Verificando estrutura de pastas...")

# Verificar pasta KE5Z
if not os.path.exists(DIR_KE5Z_IN):
    print(f"❌ ERRO: Pasta {DIR_KE5Z_IN} não encontrada!")
    print(f"   Crie a pasta e coloque os arquivos .txt dentro dela.")
    sys.exit(1)

print(f"✅ Pasta KE5Z encontrada: {DIR_KE5Z_IN}")

# Verificar arquivos auxiliares
if not os.path.exists(ARQ_SAPIENS):
    print(f"⚠️  AVISO: Arquivo {ARQ_SAPIENS} não encontrado!")
    print(f"   O merge com dados SAPIENS será pulado.")

if not os.path.exists(ARQ_FORNECEDORES):
    print(f"⚠️  AVISO: Arquivo {ARQ_FORNECEDORES} não encontrado!")
    print(f"   O merge com fornecedores será pulado.")

# Processar arquivos KE5Z
pasta = DIR_KE5Z_IN
dataframes = []

arquivos_txt = sorted([f for f in os.listdir(pasta) if f.endswith('.txt')])
print(f"\n📁 Arquivos .txt encontrados: {len(arquivos_txt)}")

for i, arquivo in enumerate(arquivos_txt, 1):
    caminho_arquivo = os.path.join(pasta, arquivo)
    
    print(f"\n[{i}/{len(arquivos_txt)}] Processando: {arquivo}")
    
    try:
        tamanho_mb = os.path.getsize(caminho_arquivo) / (1024 * 1024)
        print(f"   Tamanho: {tamanho_mb:.1f} MB")
        
        df = None
        
        # Detectar linha do cabeçalho
        linha_detectada = detectar_linha_cabecalho(caminho_arquivo, max_linhas=25)
        if linha_detectada is not None:
            print(f"   🔍 Cabeçalho detectado na linha {linha_detectada + 1}")
        
        # Construir lista de tentativas
        skiprows_tentativas = []
        if linha_detectada is not None:
            skiprows_tentativas.append(linha_detectada)
            for offset in [-2, -1, 1, 2]:
                valor = linha_detectada + offset
                if 0 <= valor <= 20 and valor not in skiprows_tentativas:
                    skiprows_tentativas.append(valor)
        
        valores_padrao = [9, 8, 10, 7, 11, 6, 12, 5, 13, 4, 14, 3, 15]
        for valor in valores_padrao:
            if valor not in skiprows_tentativas:
                skiprows_tentativas.append(valor)
        
        if not skiprows_tentativas:
            skiprows_tentativas = list(range(3, 16))
        
        print(f"   🔄 Tentando {len(skiprows_tentativas)} configurações...")
        
        melhor_df = None
        melhor_pontuacao = 0
        melhor_skiprows = None
        
        for skiprows_val in skiprows_tentativas:
            try:
                df_temp = pd.read_csv(
                    caminho_arquivo, 
                    sep='\t', 
                    skiprows=skiprows_val,
                    encoding='latin1', 
                    engine='c',
                    low_memory=False
                )
                
                if validar_cabecalho(df_temp, min_colunas=5, min_linhas=1):
                    pontuacao = len(df_temp.columns) * 2 + len(df_temp)
                    pontuacao += sum(1 for col in df_temp.columns if not str(col).startswith('Unnamed')) * 3
                    
                    if melhor_df is None or pontuacao > melhor_pontuacao:
                        melhor_df = df_temp
                        melhor_pontuacao = pontuacao
                        melhor_skiprows = skiprows_val
                    
                    if pontuacao > 100:
                        df = df_temp
                        if skiprows_val != 9:
                            print(f"   ✅ Arquivo lido com skiprows={skiprows_val}")
                        break
                        
            except Exception:
                try:
                    df_temp = pd.read_csv(
                        caminho_arquivo, 
                        sep='\t', 
                        skiprows=skiprows_val,
                        encoding='latin1', 
                        engine='python',
                        low_memory=False
                    )
                    
                    if validar_cabecalho(df_temp, min_colunas=5, min_linhas=1):
                        pontuacao = len(df_temp.columns) * 2 + len(df_temp)
                        pontuacao += sum(1 for col in df_temp.columns if not str(col).startswith('Unnamed')) * 3
                        
                        if melhor_df is None or pontuacao > melhor_pontuacao:
                            melhor_df = df_temp
                            melhor_pontuacao = pontuacao
                            melhor_skiprows = skiprows_val
                            
                        if pontuacao > 100:
                            df = df_temp
                            print(f"   ✅ Arquivo lido com skiprows={skiprows_val} (python)")
                            break
                except Exception:
                    continue
        
        if df is None:
            if melhor_df is not None:
                df = melhor_df
                if melhor_skiprows != 9:
                    print(f"   ✅ Melhor configuração: skiprows={melhor_skiprows}")
        
        if df is None or len(df) == 0:
            raise Exception("Arquivo não pôde ser lido após todas as tentativas")
        
        print(f"   Carregado: {len(df):,} registros, {len(df.columns)} colunas")
        
        # Padronizar colunas
        print("   🔧 Padronizando colunas...")
        df = padronizar_colunas(df, arquivo_nome=arquivo)
        
        if len(df.columns) > 9 and 'doc.ref' not in df.columns:
            df.rename(columns={df.columns[9]: 'doc.ref'}, inplace=True)
        
        # Filtrar Ano
        if 'Ano' in df.columns:
            antes_filtro = len(df)
            df = df[df['Ano'].notna() & (df['Ano'] != 0)].copy()
            depois_filtro = len(df)
            if antes_filtro != depois_filtro:
                print(f"   Removidos {antes_filtro - depois_filtro:,} registros com Ano inválido")
        
        # Processar Em MCont.
        if 'Em MCont.' not in df.columns:
            raise KeyError(f"Coluna 'Em MCont.' não encontrada")
        
        if df['Em MCont.'].dtype == 'object':
            df['Em MCont.'] = (
                df['Em MCont.']
                .astype(str)
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
            )
        df['Em MCont.'] = pd.to_numeric(df['Em MCont.'], errors='coerce')
        df['Em MCont.'] = df['Em MCont.'].fillna(0)
        
        # Processar Qtd.
        if 'Qtd.' not in df.columns:
            df['Qtd.'] = 0
        else:
            if df['Qtd.'].dtype == 'object':
                df['Qtd.'] = (
                    df['Qtd.']
                    .astype(str)
                    .str.replace('.', '', regex=False)
                    .str.replace(',', '.', regex=False)
                )
            df['Qtd.'] = pd.to_numeric(df['Qtd.'], errors='coerce')
            df['Qtd.'] = df['Qtd.'].fillna(0)
        
        dataframes.append(df)
        total_em_mcont = df['Em MCont.'].sum()
        print(f"   ✅ Processado! Total: {total_em_mcont:,.2f}")
        
    except KeyError as e:
        print(f"   ❌ ERRO DE COLUNA: {str(e)}")
        print(f"   Continuando com próximo arquivo...")
        continue
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
        print(f"   Continuando com próximo arquivo...")
        continue

# Resumo
print("\n" + "="*80)
print("📊 RESUMO DO PROCESSAMENTO")
print("="*80)
print(f"✅ Arquivos processados: {len(dataframes)}/{len(arquivos_txt)}")
print("="*80 + "\n")

# Concatenar DataFrames
if dataframes:
    print(f"🔄 Concatenando {len(dataframes)} DataFrames...")
    df_total = pd.concat(dataframes, ignore_index=True)
    print(f"✅ Concatenação concluída: {len(df_total):,} registros")
else:
    print("❌ ERRO: Nenhum arquivo foi processado com sucesso!")
    sys.exit(1)

# Remover colunas desnecessárias
colunas_para_remover = [
    'Unnamed: 0', 'Unnamed: 1', 'Unnamed: 4',
    'Nº doc.', 'Elem.PEP', 'Obj.custo', 'TD', 'SocPar',
    'EmpEm.', 'Empr', 'TMv', 'D/C', 'Imobil.',
]
df_total.drop(columns=colunas_para_remover, inplace=True, errors='ignore')

df_total['Cliente'] = df_total['Cliente'].astype(str)

# Renomear Em MCont. para Valor
df_total.rename(columns={'Em MCont.': 'Valor'}, inplace=True)

# Filtrar Nº conta
df_total = df_total[df_total['Nº conta'].notna() & (df_total['Nº conta'] != 0)]
print(f"Após filtro Nº conta: {len(df_total):,} registros")

# Processar KSBB (se disponível)
pasta_ksbb = DIR_KSBB_IN
dataframes_ksbb = []

if os.path.exists(pasta_ksbb):
    print(f"\n📁 Processando arquivos KSBB...")
    for arquivo in os.listdir(pasta_ksbb):
        caminho_arquivo = os.path.join(pasta_ksbb, arquivo)
        if os.path.isfile(caminho_arquivo) and arquivo.endswith('.txt'):
            try:
                print(f"   Lendo: {arquivo}")
                df_ksbb = pd.read_csv(
                    caminho_arquivo,
                    sep='\t',
                    encoding='latin1',
                    engine='python',
                    skiprows=3,
                    skipfooter=1,
                )
                df_ksbb.columns = df_ksbb.columns.str.strip()
                df_ksbb = df_ksbb[df_ksbb['Material'].notna() & (df_ksbb['Material'] != 0)]
                df_ksbb = df_ksbb.drop_duplicates(subset=['Material'])
                dataframes_ksbb.append(df_ksbb)
            except Exception as e:
                print(f"   ⚠️  Erro ao processar {arquivo}: {e}")
    
    if len(dataframes_ksbb) > 1:
        df_ksbb = pd.concat(dataframes_ksbb, ignore_index=True)
    elif len(dataframes_ksbb) == 1:
        df_ksbb = dataframes_ksbb[0]
    else:
        df_ksbb = pd.DataFrame()
    
    if not df_ksbb.empty:
        df_ksbb = df_ksbb.drop_duplicates(subset=['Material'])
        
        # Merge com KE5Z
        if 'Material' in df_total.columns:
            df_total = pd.merge(
                df_total,
                df_ksbb[['Material', 'Texto breve material']],
                on='Material',
                how='left',
            )
            df_total.rename(columns={'Texto breve material': 'Descrição Material'}, inplace=True)
            
            if 'Texto' in df_total.columns and 'Descrição Material' in df_total.columns:
                df_total['Texto'] = df_total.apply(
                    lambda row: (
                        row['Descrição Material']
                        if pd.notnull(row['Descrição Material'])
                        else row['Texto']
                    ),
                    axis=1,
                )
            print(f"   ✅ Merge KSBB concluído")
else:
    print(f"⚠️  Pasta KSBB não encontrada, pulando merge...")

# Merge com SAPIENS
if os.path.exists(ARQ_SAPIENS):
    print(f"\n📊 Fazendo merge com Dados SAPIENS...")
    try:
        df_sapiens = pd.read_excel(ARQ_SAPIENS, sheet_name='Conta contabil')
        df_sapiens.rename(columns={'CONTA SAPIENS': 'Nº conta'}, inplace=True)
        df_sapiens['Nº conta'] = df_sapiens['Nº conta'].astype(str)
        
        df_total = pd.merge(
            df_total,
            df_sapiens[['Nº conta', 'Type 07', 'Type 06', 'Type 05']],
            on='Nº conta',
            how='left',
        )
        
        df_CC = pd.read_excel(ARQ_SAPIENS, sheet_name='CC')
        df_CC.rename(columns={'CC SAPiens': 'Centro cst'}, inplace=True)
        
        df_total = pd.merge(
            df_total,
            df_CC[['Centro cst', 'Oficina', 'USI']],
            on='Centro cst',
            how='left',
        )
        
        df_total['USI'] = df_total['USI'].fillna('Others')
        print(f"   ✅ Merge SAPIENS concluído")
    except Exception as e:
        print(f"   ⚠️  Erro no merge SAPIENS: {e}")

# Limpar e converter tipos
print("\n🔧 Limpando e convertendo tipos de dados...")

for col in ['Ano', 'Período']:
    if col in df_total.columns:
        df_total[col] = pd.to_numeric(df_total[col], errors='coerce')

numeric_columns = ['Valor', 'Qtd.', 'doc.ref', 'Item']
for col in numeric_columns:
    if col in df_total.columns:
        df_total[col] = pd.to_numeric(df_total[col], errors='coerce')

text_columns = ['Nº conta', 'Centro cst', 'Texto', 'Fornecedor', 'Fornec.', 'Material', 
                'Descrição Material', 'Type 05', 'Type 06', 'Type 07', 'USI', 'Oficina',
                'Doc.compra', 'Usuário', 'Tipo', 'Cliente', 'Dt.lçto.', 'Imobilizado']
for col in text_columns:
    if col in df_total.columns:
        df_total[col] = df_total[col].astype(str)

for col in df_total.columns:
    if df_total[col].dtype == 'object':
        df_total[col] = df_total[col].astype(str)

df_total = df_total.where(pd.notnull(df_total), None)

if 'Dt.lçto.' in df_total.columns:
    df_total['Dt.lçto.'] = df_total['Dt.lçto.'].astype(str)
    df_total['Dt.lçto.'] = df_total['Dt.lçto.'].str.replace('.', '/', regex=False)

# Merge com Fornecedores
if os.path.exists(ARQ_FORNECEDORES):
    print(f"\n🏢 Fazendo merge com Fornecedores...")
    try:
        df_fornecedores = pd.read_excel(ARQ_FORNECEDORES, skiprows=3)
        df_fornecedores = df_fornecedores.drop_duplicates(subset=['Fornecedor'])
        df_fornecedores.rename(columns={'Fornecedor': 'Fornec.'}, inplace=True)
        df_fornecedores['Fornec.'] = df_fornecedores['Fornec.'].astype(str)
        
        df_total = pd.merge(
            df_total,
            df_fornecedores[['Fornec.', 'Nome do fornecedor']],
            on='Fornec.',
            how='left',
        )
        df_total.rename(columns={'Nome do fornecedor': 'Fornecedor'}, inplace=True)
        
        # Hist_prov
        if os.path.exists(ARQ_SAPIENS):
            try:
                df_hist_prov = pd.read_excel(ARQ_SAPIENS, sheet_name='Hist_prov', skiprows=1)
                df_hist_prov = df_hist_prov[['Nome do fornecedor', '20carac']]
                df_hist_prov['20carac'] = df_hist_prov['20carac'].str.strip()
                df_hist_prov = df_hist_prov.drop_duplicates(subset=['20carac'])
                
                df_total['20carac'] = df_total['Texto'].astype(str).str[:20]
                df_total['20carac'] = df_total['20carac'].str.strip()
                
                df_total = pd.merge(
                    df_total,
                    df_hist_prov[['20carac', 'Nome do fornecedor']],
                    on='20carac',
                    how='left',
                )
                
                if 'Nome do fornecedor' in df_total.columns and 'Fornecedor' in df_total.columns:
                    df_total['Fornecedor'] = df_total.apply(
                        lambda row: (
                            row['Nome do fornecedor']
                            if pd.notnull(row['Nome do fornecedor'])
                            else row['Fornecedor']
                        ),
                        axis=1,
                    )
            except Exception as e:
                print(f"   ⚠️  Erro no Hist_prov: {e}")
        
        print(f"   ✅ Merge Fornecedores concluído")
    except Exception as e:
        print(f"   ⚠️  Erro no merge Fornecedores: {e}")

# Preencher Types
df_total['Type 07'] = df_total['Type 07'].fillna('Others')
df_total['Type 06'] = df_total['Type 06'].fillna('Others')
df_total['Type 05'] = df_total['Type 05'].fillna('Others')

# Salvar arquivos
print("\n💾 Salvando arquivos...")
os.makedirs(DIR_KE5Z_OUT, exist_ok=True)

# Separar por USI
df_others = df_total[df_total['USI'] == 'Others'].copy()
df_main = df_total[df_total['USI'] != 'Others'].copy()

print(f"   Total: {len(df_total):,} registros")
print(f"   Principais (sem Others): {len(df_main):,}")
print(f"   Others: {len(df_others):,}")

# Salvar arquivos parquet
caminho_main = os.path.join(DIR_KE5Z_OUT, 'KE5Z_main.parquet')
df_main.to_parquet(caminho_main, index=False)
print(f"   ✅ KE5Z_main.parquet salvo")

if len(df_others) > 0:
    caminho_others = os.path.join(DIR_KE5Z_OUT, 'KE5Z_others.parquet')
    df_others.to_parquet(caminho_others, index=False)
    print(f"   ✅ KE5Z_others.parquet salvo")

caminho_completo = os.path.join(DIR_KE5Z_OUT, 'KE5Z.parquet')
df_total.to_parquet(caminho_completo, index=False)
print(f"   ✅ KE5Z.parquet salvo")

# Criar arquivo waterfall otimizado
print("\n⚡ Criando arquivo waterfall otimizado...")
colunas_waterfall = [
    'Período', 'Valor', 'USI', 'Type 05', 'Type 06', 'Type 07',
    'Fornecedor', 'Fornec.', 'Tipo', 'Nº conta'
]

colunas_existentes = [col for col in colunas_waterfall if col in df_total.columns]

if len(colunas_existentes) >= 3:
    df_waterfall = df_total[colunas_existentes].copy()
    
    # Otimizar memória
    for col in df_waterfall.columns:
        if df_waterfall[col].dtype == 'object':
            unique_ratio = df_waterfall[col].nunique(dropna=True) / max(1, len(df_waterfall))
            if unique_ratio < 0.5:
                df_waterfall[col] = df_waterfall[col].astype('category')
    
    for col in df_waterfall.select_dtypes(include=['float64']).columns:
        df_waterfall[col] = pd.to_numeric(df_waterfall[col], downcast='float')
    
    for col in df_waterfall.select_dtypes(include=['int64']).columns:
        df_waterfall[col] = pd.to_numeric(df_waterfall[col], downcast='integer')
    
    df_waterfall = df_waterfall.dropna(subset=['Período', 'Valor'])
    
    arquivo_waterfall = os.path.join(DIR_KE5Z_OUT, "KE5Z_waterfall.parquet")
    df_waterfall.to_parquet(arquivo_waterfall, index=False)
    
    try:
        tamanho_original = os.path.getsize(caminho_completo) / (1024*1024)
        tamanho_waterfall = os.path.getsize(arquivo_waterfall) / (1024*1024)
        reducao = ((tamanho_original - tamanho_waterfall) / tamanho_original) * 100
        print(f"   ✅ KE5Z_waterfall.parquet salvo")
        print(f"   📊 Tamanho original: {tamanho_original:.1f} MB")
        print(f"   📊 Tamanho otimizado: {tamanho_waterfall:.1f} MB")
        print(f"   📊 Redução: {reducao:.1f}%")
    except Exception as e:
        print(f"   ✅ KE5Z_waterfall.parquet salvo")

# Salvar Excel (amostra)
caminho_excel = os.path.join(DIR_KE5Z_OUT, 'KE5Z.xlsx')
df_total.head(10000).to_excel(caminho_excel, index=False)
print(f"   ✅ KE5Z.xlsx salvo (10k linhas)")

# Salvar arquivos Excel por USI
os.makedirs(DIR_ARQUIVOS_OUT, exist_ok=True)

# Preparar dados para Excel
df_total['Nº conta'] = df_total['Nº conta'].astype(str)
df_total = df_total[['Período', 'Nº conta', 'Centro cst', 'doc.ref', 'Dt.lçto.', 'Valor', 'Qtd.', 
                     'Type 05', 'Type 06', 'Type 07', 'USI', 'Oficina', 'Doc.compra', 'Texto', 
                     'Fornecedor', 'Material', 'Usuário', 'Fornec.', 'Tipo']]

df_total.rename(columns={
    'Texto': 'Texto breve',
    'Qtd.': 'QTD',
    'Nº conta': 'Nºconta',
    'Centro cst': 'Centrocst',
    'doc.ref': 'Nºdoc.ref.',
    'Type 07': 'Account',
    'Período': 'Mes'
}, inplace=True)

df_total['Período'] = df_total['Mes'].apply(
    lambda x: 'janeiro' if x == 1 else 'fevereiro' if x == 2 else 'março' if x == 3 
    else 'abril' if x == 4 else 'maio' if x == 5 else 'junho' if x == 6 
    else 'julho' if x == 7 else 'agosto' if x == 8 else 'setembro' if x == 9 
    else 'outubro' if x == 10 else 'novembro' if x == 11 else 'dezembro'
)

colunas = ['Mes', 'Período'] + [col for col in df_total.columns if col != 'Mes' and col != 'Período']
df_total = df_total[colunas]

# Salvar por USI
usis_disponiveis = df_total['USI'].unique() if 'USI' in df_total.columns else []

usis_veiculos = ['Veículos', 'TC Ext', 'LC']
usis_veiculos_existentes = [usi for usi in usis_veiculos if usi in usis_disponiveis]

if usis_veiculos_existentes:
    caminho_veiculos = os.path.join(DIR_ARQUIVOS_OUT, 'KE5Z_veiculos.xlsx')
    df_veiculos = df_total[df_total['USI'].isin(usis_veiculos_existentes)]
    df_veiculos.to_excel(caminho_veiculos, index=False)
    print(f"   ✅ KE5Z_veiculos.xlsx salvo ({len(df_veiculos)} registros)")

if 'PWT' in usis_disponiveis:
    caminho_pwt = os.path.join(DIR_ARQUIVOS_OUT, 'KE5Z_pwt.xlsx')
    df_pwt = df_total[df_total['USI'] == 'PWT']
    df_pwt.to_excel(caminho_pwt, index=False)
    print(f"   ✅ KE5Z_pwt.xlsx salvo ({len(df_pwt)} registros)")

# Mensagem final
print("\n" + "="*80)
print("✅ EXTRAÇÃO CONCLUÍDA COM SUCESSO!")
print("="*80)
print(f"📁 Arquivos Parquet: {os.path.abspath(DIR_KE5Z_OUT)}")
print(f"📁 Arquivos Excel: {os.path.abspath(DIR_ARQUIVOS_OUT)}")
print("="*80)

