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

# CORREÇÃO: Não criar pyvenv.cfg em executáveis PyInstaller
# O pyvenv.cfg com caminhos absolutos causa problemas de portabilidade
# Executáveis PyInstaller são standalone e não precisam deste arquivo
if hasattr(sys, '_MEIPASS'):
    # No executável: NÃO criar pyvenv.cfg (causa problemas de portabilidade)
    pass
else:
    # Em desenvolvimento: criar apenas se necessário e usar caminhos relativos
    pyvenv_path = Path("pyvenv.cfg")
    if not pyvenv_path.exists():
        # Usar caminhos relativos para evitar problemas de portabilidade
        config_content = f"""home = .
executable = .
include-system-site-packages = true
version = {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}
prompt = Dash
"""
        try:
            with open(pyvenv_path, 'w', encoding='utf-8') as f:
                f.write(config_content)
            print(f"Arquivo pyvenv.cfg criado automaticamente (desenvolvimento)")
        except Exception as e:
            print(f"Aviso: Não foi possível criar pyvenv.cfg: {e}")

# Verificar Python ativo
print(f"Python ativo: {sys.executable}")
print(f"Diretorio: {os.getcwd()}")

# ================== FUNÇÃO PORTÁVEL PARA CAMINHOS ==================
def get_base_path():
    """Retorna o caminho base correto para LEITURA de dados (PORTÁVEL)
    
    Estratégia de busca para portabilidade:
    1. No executável: primeiro tenta _internal (onde dados são copiados)
    2. Se não encontrar, tenta diretório do executável (para quando pasta é movida)
    3. Em desenvolvimento: usa diretório do script
    """
    if hasattr(sys, '_MEIPASS'):
        # Rodando no executável PyInstaller
        # CORREÇÃO CRÍTICA: Tentar múltiplos locais para portabilidade
        
        # 1. Primeiro tentar _internal (onde dados são copiados no build)
        try:
            meipass_path = os.path.abspath(sys._MEIPASS)
            if os.path.exists(meipass_path):
                # Verificar se existe pasta Extracoes em _internal
                extracoes_path = os.path.join(meipass_path, "Extracoes")
                if os.path.exists(extracoes_path):
                    return meipass_path
        except Exception:
            pass
        
        # 2. Fallback: tentar diretório do executável (para quando pasta é movida)
        try:
            exe_path = os.path.abspath(sys.executable)
            exe_dir = os.path.dirname(exe_path)
            if os.path.exists(exe_dir):
                # Verificar se existe pasta Extracoes ou _internal/Extracoes no diretório do executável
                extracoes_path_exe = os.path.join(exe_dir, "Extracoes")
                extracoes_path_internal = os.path.join(exe_dir, "_internal", "Extracoes")
                if os.path.exists(extracoes_path_exe):
                    return exe_dir
                elif os.path.exists(extracoes_path_internal):
                    return os.path.join(exe_dir, "_internal")
        except Exception:
            pass
        
        # 3. Último fallback: usar _MEIPASS mesmo que não exista (pode ser temporário)
        try:
            return os.path.abspath(sys._MEIPASS)
        except Exception:
            return sys._MEIPASS
    else:
        # Rodando em desenvolvimento
        return os.path.dirname(os.path.abspath(__file__))

def get_output_path():
    """Retorna o caminho correto para ESCRITA de dados (PORTÁVEL)
    
    No executável: salvar dentro do _internal (onde dados são lidos)
    Em desenvolvimento: mesmo diretório do script
    """
    if hasattr(sys, '_MEIPASS'):
        # No executável: salvar dentro do _internal (mesmo local onde dados são lidos)
        try:
            meipass_path = os.path.abspath(sys._MEIPASS)
            if os.path.exists(meipass_path):
                return meipass_path
            else:
                # Fallback: usar _MEIPASS mesmo que não exista
                return sys._MEIPASS
        except Exception:
            # Fallback: usar _MEIPASS
            return sys._MEIPASS
    else:
        # Em desenvolvimento: mesmo diretório
        return os.path.dirname(os.path.abspath(__file__))

# Verificação de caminhos para executável (não invasiva)
if hasattr(sys, '_MEIPASS'):
    print(f"Executando no PyInstaller - pasta _internal: {sys._MEIPASS}")
    print(f"Pasta do executável: {os.path.dirname(sys.executable)}")

# ================== CAMINHOS PADRONIZADOS (PORTÁVEIS) ==================
# Pasta raiz do projeto (para ENTRADA - dentro do _internal)
ROOT_DIR = get_base_path()

# Pasta raiz para SAÍDA (no diretório do executável para portabilidade)
OUTPUT_DIR = get_output_path()

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

# Obter diretório base (onde está o executável) - PORTÁVEL
base_dir = get_base_path()
print(f"Diretório base (portável): {base_dir}")

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

# ================== FUNÇÃO DE DETECÇÃO AUTOMÁTICA DE CABEÇALHO ==================
def detectar_linha_cabecalho(caminho_arquivo, max_linhas=20):
    """
    Detecta automaticamente a linha do cabeçalho procurando por palavras-chave conhecidas.
    
    Args:
        caminho_arquivo: Caminho do arquivo a ser analisado
        max_linhas: Número máximo de linhas para verificar
    
    Returns:
        Número da linha do cabeçalho (0-indexed) ou None se não encontrar
    """
    # Palavras-chave que indicam que encontramos o cabeçalho
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
        
        # Procurar linha que contenha múltiplas palavras-chave
        melhor_linha = None
        melhor_pontuacao = 0
        
        for i, linha in enumerate(linhas):
            # Contar quantas palavras-chave aparecem nesta linha
            pontuacao = sum(1 for palavra in palavras_chave_cabecalho if palavra in linha)
            
            # Bônus se a linha parece ser um cabeçalho (tem múltiplas colunas separadas por tab)
            if '\t' in linha:
                colunas = linha.split('\t')
                if len(colunas) > 5:  # Cabeçalho geralmente tem muitas colunas
                    pontuacao += 2
            
            # Bônus se não parece ser uma linha de dados numéricos
            if not any(char.isdigit() for char in linha[:50]):
                pontuacao += 1
            
            if pontuacao > melhor_pontuacao:
                melhor_pontuacao = pontuacao
                melhor_linha = i
        
        # Retornar apenas se encontrou uma linha com pelo menos 3 palavras-chave
        if melhor_pontuacao >= 3:
            return melhor_linha
        
        return None
    except Exception as e:
        print(f"   ⚠️  Erro ao detectar cabeçalho automaticamente: {str(e)[:100]}")
        return None

def validar_cabecalho(df_temp, min_colunas=5, min_linhas=1):
    """
    Valida se o DataFrame lido parece ter um cabeçalho válido.
    
    Args:
        df_temp: DataFrame a ser validado
        min_colunas: Número mínimo de colunas esperadas
        min_linhas: Número mínimo de linhas esperadas
    
    Returns:
        True se o cabeçalho parece válido, False caso contrário
    """
    if df_temp is None:
        return False
    
    # Verificar número mínimo de colunas e linhas
    if len(df_temp.columns) < min_colunas or len(df_temp) < min_linhas:
        return False
    
    # Verificar se as colunas não são todas "Unnamed" (indica que não leu cabeçalho corretamente)
    colunas_nomeadas = sum(1 for col in df_temp.columns if not str(col).startswith('Unnamed'))
    if colunas_nomeadas < min_colunas:
        return False
    
    # Verificar se não tem muitas colunas vazias (indica problema na leitura)
    colunas_nao_vazias = sum(1 for col in df_temp.columns if df_temp[col].notna().any())
    if colunas_nao_vazias < min_colunas:
        return False
    
    return True

# ================== FUNÇÃO DE ANÁLISE DE CONSISTÊNCIA DE ARQUIVOS ==================
def analisar_consistencia_arquivos(pasta_arquivos, tipo="KE5Z", max_arquivos=5):
    """
    Analisa a consistência entre arquivos verificando:
    - Quantidade de colunas
    - Nomes das colunas
    - Tipos de dados das colunas
    
    Args:
        pasta_arquivos: Caminho da pasta com os arquivos
        tipo: Tipo de arquivo ("KE5Z" ou "KSBB")
        max_arquivos: Número máximo de arquivos para analisar (padrão: 5)
    
    Returns:
        Dicionário com resultados da análise
    """
    if not os.path.exists(pasta_arquivos):
        return {"erro": f"Pasta não encontrada: {pasta_arquivos}"}
    
    arquivos_txt = sorted([f for f in os.listdir(pasta_arquivos) if f.endswith('.txt')])
    
    if not arquivos_txt:
        return {"erro": "Nenhum arquivo .txt encontrado"}
    
    # Limitar número de arquivos para análise
    arquivos_analise = arquivos_txt[:max_arquivos]
    
    print(f"\n{'='*80}")
    print(f"🔍 ANÁLISE DE CONSISTÊNCIA - {tipo}")
    print(f"{'='*80}")
    print(f"📁 Arquivos encontrados: {len(arquivos_txt)}")
    print(f"🔬 Analisando: {len(arquivos_analise)} arquivo(s)")
    print(f"{'='*80}\n")
    
    resultados = {
        "tipo": tipo,
        "total_arquivos": len(arquivos_txt),
        "arquivos_analisados": len(arquivos_analise),
        "arquivos": [],
        "consistencia": {
            "quantidade_colunas": True,
            "nomes_colunas": True,
            "tipos_colunas": True,
            "problemas": []
        }
    }
    
    estruturas = []
    skiprows_padrao = 9 if tipo == "KE5Z" else 3
    
    for arquivo in arquivos_analise:
        caminho_arquivo = os.path.join(pasta_arquivos, arquivo)
        
        try:
            # Tentar detectar linha do cabeçalho automaticamente
            linha_detectada = detectar_linha_cabecalho(caminho_arquivo, max_linhas=25)
            skiprows_usar = linha_detectada if linha_detectada is not None else skiprows_padrao
            
            # Ler apenas primeiras linhas para análise (mais rápido)
            df_temp = pd.read_csv(
                caminho_arquivo,
                sep='\t',
                encoding='latin1',
                engine='python',
                skiprows=skiprows_usar,
                nrows=100,  # Ler apenas 100 linhas para análise
                on_bad_lines='skip'
            )
            
            # Remover espaços das colunas
            df_temp.columns = df_temp.columns.str.strip()
            
            # Aplicar padronização
            df_temp = padronizar_colunas(df_temp, arquivo_nome="")
            
            estrutura = {
                "arquivo": arquivo,
                "quantidade_colunas": len(df_temp.columns),
                "nomes_colunas": list(df_temp.columns),
                "tipos_colunas": {col: str(df_temp[col].dtype) for col in df_temp.columns},
                "sucesso": True
            }
            
            estruturas.append(estrutura)
            resultados["arquivos"].append(estrutura)
            
            print(f"✅ {arquivo}")
            print(f"   Colunas: {estrutura['quantidade_colunas']}")
            print(f"   Primeiras 5 colunas: {estrutura['nomes_colunas'][:5]}")
            
        except Exception as e:
            erro_info = {
                "arquivo": arquivo,
                "erro": str(e),
                "sucesso": False
            }
            estruturas.append(erro_info)
            resultados["arquivos"].append(erro_info)
            resultados["consistencia"]["problemas"].append(f"{arquivo}: {str(e)}")
            print(f"❌ {arquivo}: Erro - {str(e)}")
            continue
    
    # Verificar consistência
    if len(estruturas) == 0:
        resultados["consistencia"]["problemas"].append("Nenhum arquivo foi lido com sucesso")
        return resultados
    
    # Filtrar apenas estruturas válidas
    estruturas_validas = [e for e in estruturas if e.get("sucesso", False)]
    
    if len(estruturas_validas) == 0:
        resultados["consistencia"]["problemas"].append("Nenhum arquivo válido para comparação")
        return resultados
    
    # 1. Verificar quantidade de colunas
    quantidades = [e["quantidade_colunas"] for e in estruturas_validas]
    quantidade_unica = len(set(quantidades)) == 1
    
    if not quantidade_unica:
        resultados["consistencia"]["quantidade_colunas"] = False
        problemas = {}
        for qtd in set(quantidades):
            arquivos_com_qtd = [e["arquivo"] for e in estruturas_validas if e["quantidade_colunas"] == qtd]
            problemas[qtd] = arquivos_com_qtd
        resultados["consistencia"]["problemas"].append(
            f"Quantidade de colunas diferente: {problemas}"
        )
        print(f"\n⚠️  QUANTIDADE DE COLUNAS DIFERENTE:")
        for qtd, arquivos in problemas.items():
            print(f"   {qtd} colunas: {arquivos}")
    else:
        print(f"\n✅ QUANTIDADE DE COLUNAS: Consistente ({quantidades[0]} colunas)")
    
    # 2. Verificar nomes das colunas
    primeira_estrutura = estruturas_validas[0]
    nomes_referencia = set(primeira_estrutura["nomes_colunas"])
    
    nomes_consistentes = True
    diferencas_nomes = {}
    
    for estrutura in estruturas_validas[1:]:
        nomes_atual = set(estrutura["nomes_colunas"])
        
        # Verificar diferenças
        faltando = nomes_referencia - nomes_atual
        extras = nomes_atual - nomes_referencia
        
        if faltando or extras:
            nomes_consistentes = False
            diferencas_nomes[estrutura["arquivo"]] = {
                "faltando": list(faltando),
                "extras": list(extras)
            }
    
    if not nomes_consistentes:
        resultados["consistencia"]["nomes_colunas"] = False
        resultados["consistencia"]["problemas"].append(
            f"Diferenças nos nomes das colunas: {diferencas_nomes}"
        )
        print(f"\n⚠️  NOMES DE COLUNAS DIFERENTES:")
        for arquivo, difs in diferencas_nomes.items():
            if difs["faltando"]:
                print(f"   {arquivo} - Faltando: {difs['faltando'][:5]}")
            if difs["extras"]:
                print(f"   {arquivo} - Extras: {difs['extras'][:5]}")
    else:
        print(f"\n✅ NOMES DE COLUNAS: Consistente")
        print(f"   Colunas: {sorted(list(nomes_referencia))[:10]}...")
    
    # 3. Verificar tipos de dados
    tipos_referencia = primeira_estrutura["tipos_colunas"]
    tipos_consistentes = True
    diferencas_tipos = {}
    
    for estrutura in estruturas_validas[1:]:
        tipos_atual = estrutura["tipos_colunas"]
        
        # Comparar tipos das colunas comuns
        colunas_comuns = set(tipos_referencia.keys()) & set(tipos_atual.keys())
        diferencas = {}
        
        for col in colunas_comuns:
            if tipos_referencia[col] != tipos_atual[col]:
                diferencas[col] = {
                    "referencia": tipos_referencia[col],
                    "atual": tipos_atual[col]
                }
        
        if diferencas:
            tipos_consistentes = False
            diferencas_tipos[estrutura["arquivo"]] = diferencas
    
    if not tipos_consistentes:
        resultados["consistencia"]["tipos_colunas"] = False
        resultados["consistencia"]["problemas"].append(
            f"Diferenças nos tipos de dados: {diferencas_tipos}"
        )
        print(f"\n⚠️  TIPOS DE DADOS DIFERENTES:")
        for arquivo, difs in list(diferencas_tipos.items())[:3]:  # Mostrar apenas 3 primeiros
            print(f"   {arquivo}:")
            for col, tipos in list(difs.items())[:5]:  # Mostrar apenas 5 primeiras diferenças
                print(f"      {col}: {tipos['referencia']} → {tipos['atual']}")
    else:
        print(f"\n✅ TIPOS DE DADOS: Consistente")
    
    # Resumo final
    print(f"\n{'='*80}")
    if (resultados["consistencia"]["quantidade_colunas"] and 
        resultados["consistencia"]["nomes_colunas"] and 
        resultados["consistencia"]["tipos_colunas"]):
        print("✅ TODOS OS ARQUIVOS SÃO CONSISTENTES!")
        print("   Pronto para merge sem problemas")
    else:
        print("⚠️  INCONSISTÊNCIAS DETECTADAS:")
        for problema in resultados["consistencia"]["problemas"][:5]:
            print(f"   - {problema[:100]}...")
        print("\n   ⚠️  A padronização de colunas será aplicada para resolver diferenças")
    print(f"{'='*80}\n")
    
    return resultados

# ================== FUNÇÃO DE PADRONIZAÇÃO DE COLUNAS ==================
def padronizar_colunas(df, arquivo_nome=""):
    """
    Padroniza nomes das colunas para garantir compatibilidade.
    Mapeia variações de nomes para os nomes fixos usados no código.
    """
    if df is None or len(df.columns) == 0:
        return df
    
    # Remover espaços em branco dos nomes das colunas primeiro
    df.columns = df.columns.str.strip()
    
    # Mapeamento de nomes possíveis para nomes fixos (mantendo os nomes atuais do código)
    mapeamento_colunas = {
        # Coluna 'Ano'
        'Ano': ['ano', 'Ano', 'ANO', 'year', 'Year', 'YEAR'],
        
        # Coluna 'Período'
        'Período': ['período', 'Periodo', 'PERÍODO', 'PERIODO', 'period', 'Period', 
                   'PERIOD', 'mes', 'Mes', 'MES', 'mês', 'Mês'],
        
        # Coluna 'Nº conta'
        'Nº conta': ['nº conta', 'Nº conta', 'Nºconta', 'nºconta', 'conta', 'Conta', 
                     'CONTA', 'Nº Conta', 'No conta', 'No. conta'],
        
        # Coluna 'Centro cst'
        'Centro cst': ['centro cst', 'Centro cst', 'Centrocst', 'centrocst', 'CENTRO CST',
                      'centro', 'Centro', 'CENTRO', 'centro de custo', 'Centro de Custo'],
        
        # Coluna 'Texto'
        'Texto': ['texto', 'Texto', 'TEXTO', 'descrição', 'Descrição', 'DESCRIÇÃO',
                 'texto breve', 'Texto breve', 'TEXTO BREVE', 'descrição material'],
        
        # Coluna 'Texto breve material' (específica para arquivos KSBB)
        'Texto breve material': ['texto breve material', 'Texto breve material', 'TEXTO BREVE MATERIAL',
                               'texto breve mat', 'Texto breve mat', 'descrição material', 'Descrição Material',
                               'texto material', 'Texto material', 'TEXTO MATERIAL'],
        
        # Coluna 'Fornec.'
        'Fornec.': ['fornec.', 'Fornec.', 'FORNEC.', 'fornecedor código', 'Fornecedor código',
                   'FORNECEDOR CÓDIGO', 'fornec', 'Fornec', 'FORNEC'],
        
        # Coluna 'Material' (DEVE VIR ANTES DE 'Texto' para evitar conflitos)
        'Material': ['material', 'Material', 'MATERIAL', 'mat', 'Mat', 'MAT', 'Código Material', 'Código material'],
        
        # Coluna 'Item'
        'Item': ['item', 'Item', 'ITEM'],
        
        # Coluna 'Cliente'
        'Cliente': ['cliente', 'Cliente', 'CLIENTE'],
        
        # Coluna 'doc.ref'
        'doc.ref': ['doc.ref', 'doc.ref.', 'Doc.ref.', 'Doc.ref', 'DOC.REF', 'DOC.REF.',
                   'documento', 'Documento', 'DOCUMENTO', 'doc ref', 'Doc Ref'],
        
        # Coluna 'Dt.lçto.'
        'Dt.lçto.': ['dt.lçto.', 'Dt.lçto.', 'DT.LÇTO.', 'data', 'Data', 'DATA',
                    'data lançamento', 'Data Lançamento', 'data de lançamento'],
        
        # Coluna 'Em MCont.'
        'Em MCont.': ['em mcont.', 'Em MCont.', 'EM MCONT.', 'valor', 'Valor', 'VALOR',
                     'montante', 'Montante', 'MONTANTE', 'em mcont', 'Em MCont'],
        
        # Coluna 'Qtd.'
        'Qtd.': ['qtd.', 'Qtd.', 'QTD.', 'quantidade', 'Quantidade', 'QUANTIDADE',
                'qtd', 'Qtd', 'QTD'],
        
        # Coluna 'Cen.lucro'
        'Cen.lucro': ['cen.lucro', 'Cen.lucro', 'CEN.LUCRO', 'centro lucro', 'Centro Lucro',
                     'centro de lucro', 'Centro de Lucro'],
        
        # Coluna 'Usuário'
        'Usuário': ['usuário', 'Usuário', 'USUÁRIO', 'usuario', 'Usuario', 'USUARIO',
                   'user', 'User', 'USER'],
        
        # Coluna 'Tipo'
        'Tipo': ['tipo', 'Tipo', 'TIPO', 'type', 'Type', 'TYPE'],
        
        # Coluna 'Doc.compra'
        'Doc.compra': ['doc.compra', 'Doc.compra', 'DOC.COMPRA', 'documento compra',
                      'Documento Compra', 'doc compra'],
    }
    
    # Criar dicionário de renomeação
    renomeacao = {}
    colunas_originais = df.columns.tolist()
    
    # Para cada nome fixo esperado, procurar nas colunas originais
    for nome_fixo, variações in mapeamento_colunas.items():
        # Se a coluna já existe com o nome correto, não precisa renomear
        if nome_fixo in colunas_originais:
            continue
        
        # Procurar por variações
        coluna_encontrada = None
        
        # 1. Busca exata (case-insensitive)
        for col_original in colunas_originais:
            if col_original.strip().lower() in [v.lower() for v in variações]:
                coluna_encontrada = col_original
                break
        
        # 2. Busca parcial (se não encontrou exato)
        # CORREÇÃO: Evitar mapear 'Material' para 'Texto' - verificar correspondência exata primeiro
        if not coluna_encontrada:
            for col_original in colunas_originais:
                col_lower = col_original.strip().lower()
                for variacao in variações:
                    variacao_lower = variacao.lower()
                    # Verificar correspondência exata primeiro (mais restritiva)
                    if col_lower == variacao_lower:
                        coluna_encontrada = col_original
                        break
                    # Depois verificar correspondência parcial (menos restritiva)
                    elif variacao_lower in col_lower or col_lower in variacao_lower:
                        # CORREÇÃO CRÍTICA: Evitar mapear 'Material' para 'Texto'
                        # Se estamos procurando 'Texto' e encontramos 'Material', não mapear
                        if nome_fixo == 'Texto' and 'material' in col_lower and 'texto' not in col_lower:
                            continue  # Pular este match - Material não deve virar Texto
                        coluna_encontrada = col_original
                        break
                if coluna_encontrada:
                    break
        
        # 3. Se encontrou, adicionar ao mapeamento de renomeação
        # Verificar se a coluna já não foi mapeada anteriormente
        if coluna_encontrada and coluna_encontrada not in renomeacao.keys():
            renomeacao[coluna_encontrada] = nome_fixo
            if arquivo_nome:
                print(f"   🔄 '{coluna_encontrada}' → '{nome_fixo}'")
    
    # Aplicar renomeação
    if renomeacao:
        df.rename(columns=renomeacao, inplace=True)
        print(f"   ✅ {len(renomeacao)} coluna(s) padronizada(s)")
    
    return df
# ======================================================================

# ================== ANÁLISE DE CONSISTÊNCIA ANTES DO PROCESSAMENTO ==================
# Executar análise de consistência dos arquivos KE5Z
print("\n" + "="*80)
print("🔍 INICIANDO ANÁLISE DE CONSISTÊNCIA DOS ARQUIVOS")
print("="*80)
resultado_analise_ke5z = analisar_consistencia_arquivos(pasta, tipo="KE5Z", max_arquivos=5)

# Lista para armazenar os DataFrames
dataframes = []

# Iterar sobre todos os arquivos na pasta (sem limite de quantidade)
arquivos_txt = [f for f in os.listdir(pasta) if f.endswith('.txt')]
# Ordenar arquivos por nome para garantir ordem consistente
arquivos_txt = sorted(arquivos_txt)
print(f"📁 Arquivos .txt encontrados: {len(arquivos_txt)}")
print(f"   Arquivos serão processados em ordem alfabética")

for i, arquivo in enumerate(arquivos_txt, 1):
    caminho_arquivo = os.path.join(pasta, arquivo)
    
    print(f"\n[{i}/{len(arquivos_txt)}] Processando: {arquivo}")
    print(f"Caminho: {caminho_arquivo}")
    
    try:
        # Verificar tamanho do arquivo
        tamanho_mb = os.path.getsize(caminho_arquivo) / (1024 * 1024)
        print(f"Tamanho: {tamanho_mb:.1f} MB")
        
        # Ler o arquivo em um DataFrame com tratamento de erro múltiplo
        print("Carregando dados...")
        df = None
        
        # ETAPA 1: Tentar detectar automaticamente a linha do cabeçalho
        linha_detectada = detectar_linha_cabecalho(caminho_arquivo, max_linhas=25)
        if linha_detectada is not None:
            print(f"   🔍 Cabeçalho detectado automaticamente na linha {linha_detectada + 1}")
        
        # ETAPA 2: Construir lista de tentativas de skiprows (priorizar detecção automática)
        skiprows_tentativas = []
        
        # Adicionar linha detectada automaticamente no início (se encontrada)
        if linha_detectada is not None:
            skiprows_tentativas.append(linha_detectada)
            # Adicionar variações próximas da linha detectada
            for offset in [-2, -1, 1, 2]:
                valor = linha_detectada + offset
                if 0 <= valor <= 20 and valor not in skiprows_tentativas:
                    skiprows_tentativas.append(valor)
        
        # Adicionar valores padrão conhecidos (se ainda não foram adicionados)
        valores_padrao = [9, 8, 10, 7, 11, 6, 12, 5, 13, 4, 14, 3, 15]
        for valor in valores_padrao:
            if valor not in skiprows_tentativas:
                skiprows_tentativas.append(valor)
        
        # Garantir que temos pelo menos alguns valores para tentar
        if not skiprows_tentativas:
            skiprows_tentativas = list(range(3, 16))  # Tentar linhas 3 a 15
        
        print(f"   🔄 Tentando {len(skiprows_tentativas)} configurações diferentes de cabeçalho...")
        
        # ETAPA 3: Tentar ler com diferentes skiprows
        melhor_df = None
        melhor_pontuacao = 0
        melhor_skiprows = None
        
        for skiprows_val in skiprows_tentativas:
            try:
                # Tentar com engine C (mais rápido)
                # CORREÇÃO: Adicionar tratamento de erros de parsing
                # Nota: engine='c' pode não suportar on_bad_lines, então vamos tentar primeiro sem
                try:
                    df_temp = pd.read_csv(
                        caminho_arquivo, 
                        sep='\t', 
                        skiprows=skiprows_val,
                        encoding='latin1', 
                        engine='c',
                        low_memory=False,
                        on_bad_lines='skip'  # Pular linhas com erro de parsing
                    )
                except TypeError:
                    # Se engine C não suporta on_bad_lines, tentar sem (pode falhar mas vamos tratar)
                    df_temp = pd.read_csv(
                        caminho_arquivo, 
                        sep='\t', 
                        skiprows=skiprows_val,
                        encoding='latin1', 
                        engine='c',
                        low_memory=False
                    )
                
                # Validar qualidade do cabeçalho
                if validar_cabecalho(df_temp, min_colunas=5, min_linhas=1):
                    # Calcular pontuação de qualidade
                    pontuacao = len(df_temp.columns) * 2  # Mais colunas = melhor
                    pontuacao += len(df_temp)  # Mais linhas = melhor
                    pontuacao += sum(1 for col in df_temp.columns if not str(col).startswith('Unnamed')) * 3
                    
                    # Se for a primeira leitura válida ou melhor que a anterior
                    if melhor_df is None or pontuacao > melhor_pontuacao:
                        melhor_df = df_temp
                        melhor_pontuacao = pontuacao
                        melhor_skiprows = skiprows_val
                    
                    # Se a pontuação for muito boa, usar imediatamente
                    if pontuacao > 100:
                        df = df_temp
                        if skiprows_val != 9:
                            print(f"   ✅ Arquivo lido com skiprows={skiprows_val} (detectado automaticamente)")
                        break
                        
            except Exception as e:
                # Se engine C falhou, tentar engine Python para este skiprows
                # CORREÇÃO: Adicionar tratamento de erros de parsing
                try:
                    df_temp = pd.read_csv(
                        caminho_arquivo, 
                        sep='\t', 
                        skiprows=skiprows_val,
                        encoding='latin1', 
                        engine='python',
                        low_memory=False,
                        on_bad_lines='skip'  # Pular linhas com erro de parsing
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
                            print(f"   ✅ Arquivo lido com skiprows={skiprows_val} (engine python)")
                            break
                except Exception as e2:
                    # Continuar para próxima tentativa
                    continue
        
        # ETAPA 4: Usar melhor DataFrame encontrado (se não foi definido ainda)
        if df is None:
            if melhor_df is not None:
                df = melhor_df
                if melhor_skiprows != 9:
                    print(f"   ✅ Melhor configuração encontrada: skiprows={melhor_skiprows}")
            else:
                # Última tentativa desesperada: tentar sem skiprows e procurar cabeçalho
                try:
                    print(f"   ⚠️  Tentando leitura sem skiprows (última tentativa)...")
                    # CORREÇÃO: Adicionar tratamento de erros de parsing
                    df_temp = pd.read_csv(
                        caminho_arquivo, 
                        sep='\t', 
                        encoding='latin1', 
                        engine='python',
                        low_memory=False,
                        nrows=100,  # Ler apenas primeiras 100 linhas para testar
                        on_bad_lines='skip'  # Pular linhas com erro de parsing
                    )
                    
                    # Procurar linha que parece ser cabeçalho
                    for i in range(min(20, len(df_temp))):
                        linha_teste = df_temp.iloc[i:i+1]
                        if validar_cabecalho(linha_teste, min_colunas=5, min_linhas=0):
                            # Reler arquivo completo com este skiprows
                            # CORREÇÃO: Adicionar tratamento de erros de parsing
                            df = pd.read_csv(
                                caminho_arquivo, 
                                sep='\t', 
                                skiprows=i,
                                encoding='latin1', 
                                engine='python',
                                low_memory=False,
                                on_bad_lines='skip'  # Pular linhas com erro de parsing
                            )
                            print(f"   ✅ Arquivo lido com skiprows={i} (descoberto na última tentativa)")
                            break
                except Exception as e3:
                    pass
        
        # ETAPA 5: Verificação final
        if df is None or len(df) == 0:
            raise Exception("Arquivo lido mas está vazio ou sem colunas válidas após todas as tentativas")
        
        # Validar qualidade final
        if not validar_cabecalho(df, min_colunas=5, min_linhas=1):
            print(f"   ⚠️  AVISO: Cabeçalho pode não estar correto. Colunas: {list(df.columns)[:10]}")
        
        print(f"Carregado: {len(df):,} registros, {len(df.columns)} colunas")
        
        # APLICAR PADRONIZAÇÃO DE COLUNAS (antes de processar)
        print("🔧 Padronizando nomes das colunas...")
        df = padronizar_colunas(df, arquivo_nome=arquivo)
        
        # mudar o nome da coluna Doc.ref. pelo seu índice (backup caso não tenha sido padronizada)
        if len(df.columns) > 9 and 'doc.ref' not in df.columns:
            df.rename(columns={df.columns[9]: 'doc.ref'}, inplace=True)
        
        print(f"Processando dados de {arquivo}...")
        print("Limpando dados...")
        
        # Verificar se coluna 'Ano' existe antes de filtrar
        if 'Ano' not in df.columns:
            print(f"⚠️  AVISO: Coluna 'Ano' não encontrada em {arquivo} após padronização!")
            print(f"   Colunas disponíveis: {list(df.columns)[:10]}...")
            print(f"   Continuando sem filtro de Ano...")
        else:
            # Filtrar a coluna 'Ano' com valores não nulos e diferentes de 0
            # Usar .copy() para evitar SettingWithCopyWarning
            antes_filtro = len(df)
            df = df[df['Ano'].notna() & (df['Ano'] != 0)].copy()
            depois_filtro = len(df)
            if antes_filtro != depois_filtro:
                print(f"   Removidos {antes_filtro - depois_filtro:,} registros com Ano inválido")
        print(f"Após filtro Ano: {len(df):,} registros")
        
        # Verificar e processar coluna 'Em MCont.'
        if 'Em MCont.' not in df.columns:
            print(f"❌ ERRO: Coluna 'Em MCont.' não encontrada em {arquivo} após padronização!")
            print(f"   Colunas disponíveis: {list(df.columns)}")
            raise KeyError(f"Coluna 'Em MCont.' não encontrada. Colunas disponíveis: {list(df.columns)}")
        
        # Substituir ',' por '.' e remover pontos de separação de milhar
        print("Convertendo coluna Em MCont...")
        # Verificar se a coluna é string antes de fazer replace
        if df['Em MCont.'].dtype == 'object':
            df['Em MCont.'] = (
                df['Em MCont.']
                .astype(str)
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
            )
        # Converter a coluna para float, tratando erros
        df['Em MCont.'] = pd.to_numeric(df['Em MCont.'], errors='coerce')
        # Substituir valores NaN por 0 (ou outro valor padrão, se necessário)
        df['Em MCont.'] = df['Em MCont.'].fillna(0)

        # Verificar e processar coluna 'Qtd.'
        if 'Qtd.' not in df.columns:
            print(f"⚠️  AVISO: Coluna 'Qtd.' não encontrada em {arquivo} após padronização!")
            print(f"   Criando coluna 'Qtd.' com valores zero...")
            df['Qtd.'] = 0
        else:
            # Substituir ',' por '.' e remover pontos de separação de milhar
            print("Convertendo coluna Qtd...")
            # Verificar se a coluna é string antes de fazer replace
            if df['Qtd.'].dtype == 'object':
                df['Qtd.'] = (
                    df['Qtd.']
                    .astype(str)
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
        
    except KeyError as e:
        print(f"❌ ERRO DE COLUNA ao processar {arquivo}: {str(e)}")
        print(f"   Este arquivo tem uma estrutura diferente dos demais.")
        print(f"   Verifique se o arquivo está no formato correto.")
        print(f"   Continuando com os próximos arquivos...")
        continue
    except pd.errors.ParserError as e:
        # CORREÇÃO: Tratamento específico para erros de parsing (Expected X field, saw Y)
        print(f"❌ ERRO DE PARSING ao processar {arquivo}: {str(e)}")
        print(f"   Este erro geralmente ocorre quando há linhas mal formatadas no arquivo.")
        print(f"   Tentando processar com tratamento de erros mais robusto...")
        
        # Tentar novamente com engine Python e tratamento de erros
        try:
            # Tentar detectar linha do cabeçalho novamente
            linha_detectada = detectar_linha_cabecalho(caminho_arquivo, max_linhas=30)
            skiprows_inicial = linha_detectada if linha_detectada is not None else 9
            
            # Tentar ler com engine Python e pular linhas problemáticas
            df = pd.read_csv(
                caminho_arquivo,
                sep='\t',
                skiprows=skiprows_inicial,
                encoding='latin1',
                engine='python',
                low_memory=False,
                on_bad_lines='skip'  # Pular linhas com erro
            )
            
            if validar_cabecalho(df, min_colunas=5, min_linhas=1):
                print(f"   ✅ Arquivo processado com sucesso após tratamento de erros!")
                # Continuar processamento normal (padronizar colunas, etc.)
                df = padronizar_colunas(df, arquivo_nome=arquivo)
                # Processar colunas numéricas
                if 'Ano' in df.columns:
                    df = df[df['Ano'].notna() & (df['Ano'] != 0)].copy()
                if 'Em MCont.' in df.columns:
                    if df['Em MCont.'].dtype == 'object':
                        df['Em MCont.'] = df['Em MCont.'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
                    df['Em MCont.'] = pd.to_numeric(df['Em MCont.'], errors='coerce').fillna(0)
                if 'Qtd.' not in df.columns:
                    df['Qtd.'] = 0
                else:
                    if df['Qtd.'].dtype == 'object':
                        df['Qtd.'] = df['Qtd.'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
                    df['Qtd.'] = pd.to_numeric(df['Qtd.'], errors='coerce').fillna(0)
                
                dataframes.append(df)
                print(f"{arquivo} processado com sucesso (com tratamento de erros)!")
                total_em_mcont = df['Em MCont.'].sum() if 'Em MCont.' in df.columns else 0
                print(f"Total Em MCont. em {arquivo}: {total_em_mcont:,.2f}")
                continue
            else:
                print(f"   ⚠️  Arquivo processado mas estrutura pode estar incorreta.")
                print(f"   Continuando com os próximos arquivos...")
                continue
        except Exception as e2:
            print(f"   ❌ Não foi possível processar mesmo com tratamento de erros: {str(e2)}")
            print(f"   Continuando com os próximos arquivos...")
            continue
    except Exception as e:
        print(f"❌ Erro ao processar {arquivo}: {str(e)}")
        print(f"   Tipo de erro: {type(e).__name__}")
        import traceback
        print(f"   Detalhes completos do erro:")
        traceback.print_exc()
        print(f"   Continuando com os próximos arquivos...")
        continue

# Resumo do processamento
total_arquivos = len(arquivos_txt)
arquivos_processados = len(dataframes)
arquivos_falhados = total_arquivos - arquivos_processados

print("\n" + "="*80)
print("📊 RESUMO DO PROCESSAMENTO")
print("="*80)
print(f"✅ Arquivos processados com sucesso: {arquivos_processados}/{total_arquivos}")
if arquivos_falhados > 0:
    print(f"❌ Arquivos com erro: {arquivos_falhados}/{total_arquivos}")
print(f"📁 Total de arquivos encontrados: {total_arquivos}")
print("="*80 + "\n")

# Concatenar todos os DataFrames em um único
if dataframes:
    print(f"🔄 Concatenando {len(dataframes)} DataFrames...")
    df_total = pd.concat(dataframes, ignore_index=True)
    print(f"✅ Concatenação concluída: {len(df_total):,} registros totais")
else:
    print("⚠️  AVISO: Nenhum arquivo .txt encontrado ou processado em KE5Z.")
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

# ================== ANÁLISE DE CONSISTÊNCIA DOS ARQUIVOS KSBB ==================
# Executar análise de consistência dos arquivos KSBB (se disponível)
if pasta_ksbb and os.path.exists(pasta_ksbb):
    resultado_analise_ksbb = analisar_consistencia_arquivos(pasta_ksbb, tipo="KSBB", max_arquivos=5)
else:
    resultado_analise_ksbb = None

# Lista para armazenar os DataFrames
dataframes_ksbb = []
# Lista para armazenar informações detalhadas de cada arquivo
info_arquivos_ksbb = []

# Iterar sobre todos os arquivos na pasta (apenas se disponível)
if pasta_ksbb:
    for arquivo in os.listdir(pasta_ksbb):
        caminho_arquivo = os.path.join(pasta_ksbb, arquivo)

        # Verificar se é um arquivo e tem a extensão desejada (.txt)
        if os.path.isfile(caminho_arquivo) and arquivo.endswith('.txt'):
            print(f"Lendo: {arquivo}")

            try:
                # Ler o arquivo em um DataFrame
                # CORREÇÃO: Adicionar tratamento de erros de parsing
                df_ksbb = pd.read_csv(
                    caminho_arquivo,
                    sep='\t',
                    encoding='latin1',
                    engine='python',
                    skiprows=3,
                    skipfooter=1,
                    on_bad_lines='skip'  # Pular linhas com erro de parsing
                )

                # remover espaços em branco dos nomes das colunas
                df_ksbb.columns = df_ksbb.columns.str.strip()
                
                # Remover coluna 'Unnamed: 0' se existir (tab extra no início do arquivo)
                if 'Unnamed: 0' in df_ksbb.columns:
                    df_ksbb = df_ksbb.drop(columns=['Unnamed: 0'])
                
                # PADRONIZAÇÃO ESPECÍFICA PARA KSBB
                # Criar mapeamento robusto que aceita variações nos nomes
                print(f"   🔧 Padronizando nomes das colunas KSBB...")
                
                mapeamento_ksbb = {
                    # Data de lançamento
                    'Dt.lçto.': ['dt.lçto.', 'Dt.lçto.', 'dt.lcto.', 'Dt.lcto.', 'DT.LÇTO.', 'data lancamento', 'Data lançamento'],
                    
                    # Documento de compra
                    'Doc.compra': ['doc.compra', 'Doc.compra', 'DOC.COMPRA', 'documento compra', 'Documento compra'],
                    
                    # Número documento referência
                    'doc.ref': ['nº doc.ref', 'Nº doc.ref', 'N° doc.ref', 'doc.ref', 'Doc.ref', 'nº doc ref', 'doc ref', 'numero doc ref'],
                    
                    # Número documento
                    'Nº doc.': ['nº doc.', 'Nº doc.', 'N° doc.', 'numero doc', 'Numero doc', 'NÚM DOC'],
                    
                    # Material (código do material)
                    'Material': ['material', 'Material', 'MATERIAL', 'mat', 'Mat', 'codigo material', 'Código material'],
                    
                    # Texto breve material (descrição)
                    'Texto breve material': ['texto breve material', 'Texto breve material', 'TEXTO BREVE MATERIAL',
                                           'texto breve mat', 'Texto breve mat', 'descricao material', 'Descrição material',
                                           'texto material', 'Texto material'],
                    
                    # Período
                    'Período': ['per', 'Per', 'PER', 'periodo', 'Periodo', 'PERÍODO', 'PERIODO'],
                    
                    # Texto cabeçalho documento
                    'Txt.cab.doc.': ['txt.cab.doc.', 'Txt.cab.doc.', 'TXT.CAB.DOC.', 'texto cab doc', 'Texto cabeçalho']
                }
                
                # Aplicar mapeamento
                renomeacoes_ksbb = {}
                colunas_originais = df_ksbb.columns.tolist()
                
                for nome_padrao, variacoes in mapeamento_ksbb.items():
                    # Se já existe com nome correto, pular
                    if nome_padrao in colunas_originais:
                        continue
                    
                    # Procurar variações
                    for col_original in colunas_originais:
                        col_lower = col_original.strip().lower()
                        
                        # Verificar se corresponde a alguma variação
                        for variacao in variacoes:
                            if col_lower == variacao.lower():
                                if col_original not in renomeacoes_ksbb:
                                    renomeacoes_ksbb[col_original] = nome_padrao
                                    print(f"   🔄 '{col_original}' → '{nome_padrao}'")
                                break
                
                # Aplicar renomeações
                if renomeacoes_ksbb:
                    df_ksbb.rename(columns=renomeacoes_ksbb, inplace=True)
                    print(f"   ✅ {len(renomeacoes_ksbb)} coluna(s) padronizada(s)")
                else:
                    print(f"   ✅ Nomes já estão padronizados")
                
                print(f"   📋 Colunas finais: {list(df_ksbb.columns)}")

                # CORREÇÃO: Verificar se coluna 'Material' existe após padronização
                # A padronização pode ter renomeado incorretamente 'Material' para 'Texto'
                # Precisamos verificar e corrigir isso
                if 'Material' not in df_ksbb.columns:
                    print(f"   ⚠️  AVISO: Coluna 'Material' não encontrada em {arquivo} após padronização!")
                    print(f"   Colunas disponíveis: {list(df_ksbb.columns)[:10]}...")
                    
                    # Verificar se 'Material' foi renomeado incorretamente para 'Texto'
                    # Se 'Texto' existe mas não 'Material', pode ser que a padronização tenha errado
                    # Neste caso, precisamos verificar se há uma coluna que deveria ser 'Material'
                    # Olhando a estrutura dos arquivos KSBB, eles têm 'Material' e 'Texto' como colunas separadas
                    
                    # Tentar encontrar coluna que seja o código do material (geralmente numérica ou alfanumérica)
                    # Primeiro, verificar se há uma coluna que parece ser Material (não é 'Texto')
                    colunas_candidatas = []
                    for col in df_ksbb.columns:
                        col_lower = str(col).lower()
                        # Se a coluna contém 'material' mas não é 'Texto breve material', pode ser Material
                        if 'material' in col_lower and 'texto' not in col_lower and 'breve' not in col_lower:
                            colunas_candidatas.append(col)
                        # Ou se é uma coluna numérica/alphanumérica que não é 'Texto'
                        elif col != 'Texto' and col != 'Texto breve material' and df_ksbb[col].dtype in ['object', 'int64', 'float64']:
                            # Verificar se parece ser código de material (valores únicos altos)
                            if df_ksbb[col].nunique() > len(df_ksbb) * 0.5:  # Mais de 50% são únicos
                                colunas_candidatas.append(col)
                    
                    if colunas_candidatas:
                        # Usar a primeira candidata como Material
                        col_material = colunas_candidatas[0]
                        print(f"   🔄 Encontrada coluna candidata para Material: '{col_material}'")
                        df_ksbb.rename(columns={col_material: 'Material'}, inplace=True)
                    else:
                        # Se não encontrar, verificar se 'Texto breve material' pode ser usado como Material
                        # (caso especial onde Material e Texto breve material são a mesma coisa)
                        if 'Texto breve material' in df_ksbb.columns:
                            print(f"   ⚠️  Usando 'Texto breve material' como Material (estrutura especial)")
                            # Criar coluna Material a partir de Texto breve material (primeiros caracteres)
                            df_ksbb['Material'] = df_ksbb['Texto breve material'].astype(str).str[:20]
                        else:
                            print(f"   ⚠️  Este arquivo KSBB não tem coluna Material identificável.")
                            print(f"   Estrutura do arquivo: {len(df_ksbb.columns)} colunas")
                            print(f"   Pulando este arquivo (não é compatível com merge por Material)...")
                            continue

                # Filtrar a coluna Material com não vazias e diferentes de 0
                antes_filtro = len(df_ksbb)
                df_ksbb = df_ksbb[
                    df_ksbb['Material'].notna() & (df_ksbb['Material'] != 0)
                ]
                depois_filtro = len(df_ksbb)
                if antes_filtro != depois_filtro:
                    print(f"   Removidos {antes_filtro - depois_filtro:,} registros com Material inválido")

                # remover as linhas duplicadas pela coluna Material
                antes_dedup = len(df_ksbb)
                df_ksbb = df_ksbb.drop_duplicates(subset=['Material'])
                depois_dedup = len(df_ksbb)
                if antes_dedup != depois_dedup:
                    print(f"   Removidas {antes_dedup - depois_dedup:,} linhas duplicadas")

                # Adicionar informações detalhadas sobre o arquivo processado
                info_arquivo = {
                    'arquivo': arquivo,
                    'registros': len(df_ksbb),
                    'colunas': len(df_ksbb.columns),
                    'nomes_colunas': list(df_ksbb.columns),
                    'tipos_colunas': {col: str(df_ksbb[col].dtype) for col in df_ksbb.columns}
                }
                info_arquivos_ksbb.append(info_arquivo)
                
                # Adicionar o DataFrame à lista
                dataframes_ksbb.append(df_ksbb)
                print(f"   ✅ {arquivo} processado com sucesso: {len(df_ksbb)} registros, {len(df_ksbb.columns)} colunas")
                print(f"      Colunas: {', '.join(df_ksbb.columns[:5].tolist())}...")
                
            except KeyError as e:
                print(f"   ❌ ERRO DE COLUNA ao processar {arquivo}: {str(e)}")
                print(f"   Este arquivo tem uma estrutura diferente dos demais.")
                if 'df_ksbb' in locals():
                    print(f"   Colunas disponíveis: {list(df_ksbb.columns)[:10]}...")
                print(f"   Continuando com os próximos arquivos...")
                continue
            except Exception as e:
                print(f"   ❌ Erro ao processar {arquivo}: {str(e)}")
                print(f"   Tipo de erro: {type(e).__name__}")
                import traceback
                print(f"   Detalhes: {traceback.format_exc()[:200]}...")
                print(f"   Continuando com os próximos arquivos...")
                continue
else:
    print("Pulando processamento KSBB (pasta não disponível).")


# Concatenar todos os DataFrames em um único e ignorar caso tenha apenas 1
if len(dataframes_ksbb) > 1:
    df_ksbb = pd.concat(dataframes_ksbb, ignore_index=True)
elif len(dataframes_ksbb) == 1:
    df_ksbb = dataframes_ksbb[0]
else:
    df_ksbb = pd.DataFrame()

# ================== RELATÓRIO COMPARATIVO DOS ARQUIVOS KSBB INDIVIDUAIS ==================
if len(info_arquivos_ksbb) > 0:
    print("\n" + "="*80)
    print("📊 COMPARAÇÃO DETALHADA - ARQUIVOS KSBB INDIVIDUAIS")
    print("="*80)
    
    # Comparar quantidade de colunas
    quantidades = [info['colunas'] for info in info_arquivos_ksbb]
    if len(set(quantidades)) == 1:
        print(f"✅ QUANTIDADE DE COLUNAS: Consistente ({quantidades[0]} colunas em todos os arquivos)")
    else:
        print(f"⚠️  QUANTIDADE DE COLUNAS: Diferente entre arquivos")
        for info in info_arquivos_ksbb:
            print(f"   - {info['arquivo']}: {info['colunas']} colunas")
    
    # Comparar nomes das colunas
    if len(info_arquivos_ksbb) > 1:
        primeira_estrutura = info_arquivos_ksbb[0]
        nomes_referencia = set(primeira_estrutura['nomes_colunas'])
        nomes_consistentes = True
        
        print(f"\n📋 NOMES DAS COLUNAS (após padronização):")
        print(f"   Arquivo de referência: {primeira_estrutura['arquivo']}")
        print(f"   Colunas: {sorted(list(nomes_referencia))}")
        
        for info in info_arquivos_ksbb[1:]:
            nomes_atual = set(info['nomes_colunas'])
            faltando = nomes_referencia - nomes_atual
            extras = nomes_atual - nomes_referencia
            
            if faltando or extras:
                nomes_consistentes = False
                print(f"\n   ⚠️  {info['arquivo']}:")
                if faltando:
                    print(f"      Colunas faltantes: {list(faltando)}")
                if extras:
                    print(f"      Colunas extras: {list(extras)}")
            else:
                print(f"   ✅ {info['arquivo']}: Colunas idênticas")
        
        if nomes_consistentes:
            print(f"\n✅ TODOS OS ARQUIVOS KSBB TÊM OS MESMOS NOMES DE COLUNAS!")
        
        # Comparar tipos de dados
        print(f"\n🔬 TIPOS DE DADOS DAS COLUNAS:")
        tipos_referencia = primeira_estrutura['tipos_colunas']
        tipos_consistentes = True
        
        for info in info_arquivos_ksbb[1:]:
            tipos_atual = info['tipos_colunas']
            diferencas = {}
            
            colunas_comuns = set(tipos_referencia.keys()) & set(tipos_atual.keys())
            for col in colunas_comuns:
                if tipos_referencia[col] != tipos_atual[col]:
                    diferencas[col] = {
                        'referencia': tipos_referencia[col],
                        'atual': tipos_atual[col]
                    }
            
            if diferencas:
                tipos_consistentes = False
                print(f"   ⚠️  {info['arquivo']}: Diferenças nos tipos")
                for col, tipos in list(diferencas.items())[:5]:
                    print(f"      {col}: {tipos['referencia']} → {tipos['atual']}")
        
        if tipos_consistentes:
            print(f"   ✅ TODOS OS ARQUIVOS KSBB TÊM OS MESMOS TIPOS DE DADOS!")
    
    print("="*80 + "\n")

# remover as linhas duplicadas pela coluna Material (se existir)
if not df_ksbb.empty and 'Material' in df_ksbb.columns:
    antes_dedup = len(df_ksbb)
    df_ksbb = df_ksbb.drop_duplicates(subset=['Material'])
    depois_dedup = len(df_ksbb)
    if antes_dedup != depois_dedup:
        print(f"Removidas {antes_dedup - depois_dedup:,} linhas duplicadas no total KSBB")

# ================== RELATÓRIO DETALHADO DO DATAFRAME KSBB FINAL ==================
if not df_ksbb.empty:
    print("\n" + "="*80)
    print("📊 RELATÓRIO DETALHADO - ARQUIVOS KSBB PROCESSADOS")
    print("="*80)
    print(f"✅ Total de arquivos KSBB processados: {len(dataframes_ksbb)}")
    print(f"📈 Total de registros únicos (após deduplicação): {len(df_ksbb):,}")
    print(f"📋 Quantidade de colunas: {len(df_ksbb.columns)}")
    print(f"\n📝 COLUNAS APÓS PADRONIZAÇÃO:")
    for i, col in enumerate(df_ksbb.columns, 1):
        tipo = df_ksbb[col].dtype
        valores_unicos = df_ksbb[col].nunique()
        print(f"   {i:2d}. {col:30s} | Tipo: {str(tipo):15s} | Valores únicos: {valores_unicos:,}")
    
    # Verificar colunas críticas para merge
    print(f"\n🔍 VERIFICAÇÃO DE COLUNAS CRÍTICAS PARA MERGE:")
    colunas_criticas = ['Material', 'Texto breve material']
    for col_critica in colunas_criticas:
        if col_critica in df_ksbb.columns:
            nao_nulos = df_ksbb[col_critica].notna().sum()
            nulos = df_ksbb[col_critica].isna().sum()
            print(f"   ✅ {col_critica}:")
            print(f"      - Valores não nulos: {nao_nulos:,} ({nao_nulos/len(df_ksbb)*100:.1f}%)")
            print(f"      - Valores nulos: {nulos:,} ({nulos/len(df_ksbb)*100:.1f}%)")
        else:
            print(f"   ❌ {col_critica}: COLUNA NÃO ENCONTRADA!")
            # Tentar encontrar coluna similar
            colunas_similares = [col for col in df_ksbb.columns 
                               if any(palavra in str(col).lower() for palavra in col_critica.lower().split())]
            if colunas_similares:
                print(f"      Colunas similares encontradas: {colunas_similares}")
    
    # Comparar com estrutura esperada
    print(f"\n📊 COMPARAÇÃO COM ESTRUTURA ESPERADA:")
    colunas_esperadas_ksbb = ['Material', 'Texto breve material']
    colunas_faltantes = [col for col in colunas_esperadas_ksbb if col not in df_ksbb.columns]
    if colunas_faltantes:
        print(f"   ⚠️  Colunas faltantes: {colunas_faltantes}")
    else:
        print(f"   ✅ Todas as colunas esperadas estão presentes")
    
    print("="*80 + "\n")
else:
    print("\n⚠️  AVISO: Nenhum arquivo KSBB foi processado ou DataFrame está vazio")

# merge o df_total com df_ksbb pela coluna Material trazendo a coluna de texto breve material do df_ksbb
# LÓGICA RESTAURADA DO ARQUIVO OFICIAL (igual ao que funciona)
if not df_total.empty and not df_ksbb.empty and 'Material' in df_total.columns and 'Material' in df_ksbb.columns:
    # Verificar se a coluna 'Texto breve material' existe no KSBB
    if 'Texto breve material' in df_ksbb.columns:
        print(f"   ✅ Coluna 'Texto breve material' encontrada no KSBB")
        print(f"   🔗 Fazendo merge: df_total['Material'] ← df_ksbb[['Material', 'Texto breve material']]")
        
        # Fazer o merge DIRETO sem renomear (como no arquivo oficial)
        df_total = pd.merge(
            df_total,
            df_ksbb[['Material', 'Texto breve material']],
            on='Material',
            how='left',
        )
        
        print(f"✅ Merge com KSBB concluído: {len(df_total):,} registros totais")
    else:
        print("⚠️  AVISO: Coluna 'Texto breve material' não encontrada no df_ksbb")
        print(f"   Colunas disponíveis no df_ksbb: {list(df_ksbb.columns)}")
        print(f"   Pulando merge de descrição de material...")
elif not df_total.empty:
    if df_ksbb.empty:
        print("⚠️  AVISO: DataFrame KSBB está vazio. Pulando merge...")
    elif 'Material' not in df_total.columns:
        print("⚠️  AVISO: Coluna 'Material' não encontrada no df_total. Pulando merge...")
    elif 'Material' not in df_ksbb.columns:
        print("⚠️  AVISO: Coluna 'Material' não encontrada no df_ksbb. Pulando merge...")

# renomear a coluna Texto breve material para Descrição Material (como no arquivo oficial)
# CORREÇÃO: O merge criou colunas _x e _y porque havia duplicação
print("\n🔧 Consolidando colunas 'Texto breve material'...")
print(f"   Colunas relacionadas: {[col for col in df_total.columns if 'texto' in col.lower() or ('material' in col.lower() and 'descrição' not in col.lower())]}")

# Se existem colunas _x e _y, consolidar
if 'Texto breve material_x' in df_total.columns and 'Texto breve material_y' in df_total.columns:
    print("   🔄 Detectadas colunas duplicadas (_x e _y) - consolidando...")
    # _x é do KE5Z, _y é do KSBB (merge)
    # Priorizar _y (KSBB) quando não for nulo
    df_total['Descrição Material'] = df_total.apply(
        lambda row: (
            row['Texto breve material_y'] if pd.notnull(row['Texto breve material_y']) and str(row['Texto breve material_y']).strip() != ''
            else row['Texto breve material_x']
        ),
        axis=1
    )
    
    # Remover colunas temporárias
    df_total.drop(columns=['Texto breve material_x', 'Texto breve material_y'], inplace=True)
    
    de_ksbb = df_total['Descrição Material'].notna().sum()
    print(f"   ✅ Colunas consolidadas em 'Descrição Material': {de_ksbb:,} registros preenchidos")
    
elif 'Texto breve material' in df_total.columns:
    df_total = df_total.rename(columns={'Texto breve material': 'Descrição Material'})
    print(f"   ✅ Coluna renomeada: 'Texto breve material' → 'Descrição Material'")
else:
    print(f"   ⚠️  Nenhuma coluna 'Texto breve material' encontrada!")

# exibir as 10 primeiras linhas do df_total e as colunas de Material, Descrição Material
if 'Material' in df_total.columns and 'Descrição Material' in df_total.columns:
    print("\nAmostra (Material, Descrição Material):")
    print(df_total[['Material', 'Descrição Material']].head(10))

# se a descrição do material nao for nula substituir o valor da coluna Texto pelo valor da Descrição Material (como no arquivo oficial)
if 'Descrição Material' in df_total.columns:
    if 'Texto' in df_total.columns:
        # Atualizar coluna Texto existente com dados de Descrição Material
        print("\n🔧 Atualizando coluna 'Texto' com dados de 'Descrição Material'...")
        antes = (df_total['Texto'].notna() & (df_total['Texto'] != '')).sum()
        
        df_total['Texto'] = df_total.apply(
            lambda row: (
                row['Descrição Material']
                if pd.notnull(row['Descrição Material'])
                else row['Texto']
            ),
            axis=1,
        )
        
        depois = (df_total['Texto'].notna() & (df_total['Texto'] != '')).sum()
        print(f"   ✅ Coluna 'Texto' atualizada: {antes:,} → {depois:,} registros preenchidos")
    else:
        # Criar coluna Texto a partir de Descrição Material
        print("\n🔧 Criando coluna 'Texto' a partir de 'Descrição Material'...")
        df_total['Texto'] = df_total['Descrição Material']
        preenchidos = (df_total['Texto'].notna() & (df_total['Texto'] != '')).sum()
        print(f"   ✅ Coluna 'Texto' criada: {preenchidos:,} registros preenchidos")
else:
    print("\n⚠️  AVISO: Coluna 'Descrição Material' não encontrada - coluna 'Texto' não será atualizada")

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
# CORREÇÃO PORTABILIDADE: Usar get_base_path() para encontrar arquivo
arquivo_sapiens = os.path.join(get_base_path(), "Dados SAPIENS.xlsx")
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
print("\n🔧 Convertendo colunas de texto para string...")
text_columns = ['Nº conta', 'Centro cst', 'Fornec.', 'Type 05', 'Type 06', 'Type 07', 'USI', 'Oficina',
                'Doc.compra', 'Usuário', 'Tipo', 'Cliente', 'Dt.lçto.', 'Imobilizado']

for col in text_columns:
    if col in df_total.columns:
        df_total[col] = df_total[col].astype(str)
        valores_preenchidos = (df_total[col] != '').sum()
        if valores_preenchidos > 0:
            print(f"   ✅ {col}: {valores_preenchidos:,} valores preenchidos")

# NÃO converter 'Texto', 'Fornecedor', 'Material', 'Descrição Material' para evitar perda de dados
# Essas colunas já foram processadas corretamente antes

# Substituir valores vazios por None para compatibilidade com PyArrow (apenas para Parquet)
df_total_parquet = df_total.copy()
df_total_parquet = df_total_parquet.where(pd.notnull(df_total_parquet), None)

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
print("\n🔧 Processando dados de fornecedores...")
arquivo_fornecedores = ARQ_FORNECEDORES
df_fornecedores = pd.read_excel(arquivo_fornecedores, skiprows=3)
print(f"   📊 Fornecedores carregados: {len(df_fornecedores)} registros")

# remover linhas duplicadas pela coluna Fornecedor
df_fornecedores = df_fornecedores.drop_duplicates(subset=['Fornecedor'])
print(f"   📊 Fornecedores únicos: {len(df_fornecedores)} registros")

# mudar o nome da coluna Fornecedor para Fornec.
df_fornecedores.rename(columns={'Fornecedor': 'Fornec.'}, inplace=True)

# mudar a coluna fornec. para string
df_fornecedores['Fornec.'] = df_fornecedores['Fornec.'].astype(str)

# Verificar se coluna 'Fornec.' existe no df_total
if 'Fornec.' not in df_total.columns:
    print("   ⚠️  AVISO: Coluna 'Fornec.' não encontrada no df_total!")
    print(f"   Colunas disponíveis: {[col for col in df_total.columns if 'fornec' in col.lower()]}")
    # Tentar encontrar coluna similar
    for col in df_total.columns:
        if 'fornec' in col.lower():
            print(f"   🔄 Usando coluna '{col}' como 'Fornec.'")
            df_total.rename(columns={col: 'Fornec.'}, inplace=True)
            break

# merge o df_total com df_fornecedores pela coluna Fornec. retornando a coluna Fornecedor
if 'Fornec.' in df_total.columns:
    print(f"   🔗 Fazendo merge: df_total['Fornec.'] ← df_fornecedores[['Fornec.', 'Nome do fornecedor']]")
    
    # Converter Fornec. para string antes do merge
    df_total['Fornec.'] = df_total['Fornec.'].astype(str)
    
    df_total = pd.merge(
        df_total,
        df_fornecedores[['Fornec.', 'Nome do fornecedor']],
        on='Fornec.',
        how='left',
    )
    # mudar o nome da coluna Nome do fornecedor para Fornecedor
    df_total.rename(columns={'Nome do fornecedor': 'Fornecedor'}, inplace=True)
    
    # Verificar resultado do merge
    fornecedores_encontrados = df_total['Fornecedor'].notna().sum()
    print(f"   ✅ Merge de fornecedores concluído: {fornecedores_encontrados:,} registros com fornecedor identificado")
else:
    print("   ❌ Não foi possível fazer merge de fornecedores (coluna 'Fornec.' não encontrada)")
    # Criar coluna vazia
    df_total['Fornecedor'] = ''



# Atualizar o nome do fornecedor com as provisoes
# Precimos ler o arquivo Dados SAPIENS.xlsx na pasta do projeto na guia Hist_prov 
# desconsiderar a primeira linha do arquivo
# CORREÇÃO PORTABILIDADE: Usar get_base_path() para encontrar arquivo
arquivo_hist_prov = os.path.join(get_base_path(), "Dados SAPIENS.xlsx")
df_hist_prov = pd.read_excel(arquivo_hist_prov, sheet_name='Hist_prov', skiprows=1)
# excluir todas as colunas menos as colunas 'Nome do fornecedor', '20carac'
df_hist_prov = df_hist_prov[['Nome do fornecedor', '20carac']]
# Remover os espaços da coluna '20carac'
df_hist_prov['20carac'] = df_hist_prov['20carac'].str.strip()

# remover linhas duplicadas pela coluna '20carac'
df_hist_prov = df_hist_prov.drop_duplicates(subset=['20carac'])

# criar uma coluna no df_total chamada '20carac' (primeiros 20 caracteres do Texto) 
# CORREÇÃO: Verificar qual coluna usar (Texto, Descrição Material, ou Texto breve material)
coluna_para_20carac = None
if 'Texto' in df_total.columns:
    coluna_para_20carac = 'Texto'
elif 'Descrição Material' in df_total.columns:
    coluna_para_20carac = 'Descrição Material'
elif 'Texto breve material' in df_total.columns:
    coluna_para_20carac = 'Texto breve material'
else:
    # Fallback: usar primeira coluna de texto disponível
    colunas_texto = [col for col in df_total.columns if df_total[col].dtype == 'object']
    if colunas_texto:
        coluna_para_20carac = colunas_texto[0]
        print(f"⚠️  AVISO: Usando coluna '{coluna_para_20carac}' para criar '20carac'")

if coluna_para_20carac:
    df_total['20carac'] = df_total[coluna_para_20carac].astype(str).str[:20]
else:
    print("⚠️  ERRO: Nenhuma coluna de texto encontrada para criar '20carac'")
    df_total['20carac'] = ''
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

# Separar dados Others vs resto (usar df_total com strings vazias para Excel)
df_others = df_total[df_total['USI'] == 'Others'].copy()
df_main = df_total[df_total['USI'] != 'Others'].copy()

print(f"Total de registros: {len(df_total):,}")
print(f"Registros principais (sem Others): {len(df_main):,}")
print(f"Registros Others: {len(df_others):,}")

# Criar versão para Parquet (com None ao invés de strings vazias)
df_total_parquet = df_total.copy()
df_total_parquet = df_total_parquet.replace('', None)

# Separar dados Others vs resto para Parquet
df_main_parquet = df_total_parquet[df_total_parquet['USI'] != 'Others'].copy()
df_others_parquet = df_total_parquet[df_total_parquet['USI'] == 'Others'].copy()

# Salvar arquivo principal (sem Others) - para uso no dashboard
caminho_main = os.path.join(pasta_parquet, 'KE5Z_main.parquet')
df_main_parquet.to_parquet(caminho_main, index=False)
print(f"Arquivo principal salvo: {caminho_main}")

# Salvar arquivo Others separadamente
if len(df_others_parquet) > 0:
    caminho_others = os.path.join(pasta_parquet, 'KE5Z_others.parquet')
    df_others_parquet.to_parquet(caminho_others, index=False)
    print(f"Arquivo Others salvo: {caminho_others}")
else:
    print("Nenhum registro Others encontrado")

# Manter arquivo completo para compatibilidade
caminho_saida_atualizado = os.path.join(pasta_parquet, 'KE5Z.parquet')
df_total_parquet.to_parquet(caminho_saida_atualizado, index=False)
print(f"Arquivo completo salvo: {caminho_saida_atualizado}")

# gerar um arquivo Excel do df_total atualizado com 10k linhas (usar df_total, não df_total_parquet)
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

# organizar a ordem das colunas (CONFIGURAÇÃO ORIGINAL RESTAURADA)
print("\n🔧 Preparando colunas para Excel...")

# PASSO 1: Consolidar coluna 'Texto' ANTES de filtrar colunas
# Se 'Descrição Material' existe (do merge KSBB), usar ela para criar/atualizar 'Texto'
if 'Descrição Material' in df_total.columns:
    if 'Texto' in df_total.columns:
        # Se ambas existem, priorizar 'Descrição Material' quando não for vazia
        df_total['Texto'] = df_total.apply(
            lambda row: row['Descrição Material'] if pd.notnull(row['Descrição Material']) and str(row['Descrição Material']).strip() != ''
            else row['Texto'],
            axis=1
        )
        print("   ✅ Coluna 'Texto' atualizada com dados de 'Descrição Material' (do KSBB)")
    else:
        # Se só 'Descrição Material' existe, criar 'Texto' a partir dela
        df_total['Texto'] = df_total['Descrição Material']
        print("   ✅ Coluna 'Texto' criada a partir de 'Descrição Material' (do KSBB)")
elif 'Texto breve material' in df_total.columns and 'Texto' not in df_total.columns:
    df_total['Texto'] = df_total['Texto breve material']
    print("   ✅ Coluna 'Texto' criada a partir de 'Texto breve material'")
elif 'Texto' not in df_total.columns:
    df_total['Texto'] = ''
    print("   ⚠️  Coluna 'Texto' criada vazia (nenhuma fonte disponível)")

# Garantir que 'Fornecedor' existe
if 'Fornecedor' not in df_total.columns:
    df_total['Fornecedor'] = ''
    print("   ⚠️  Coluna 'Fornecedor' criada vazia")

# Verificar dados antes de filtrar
texto_preenchido = (df_total['Texto'].notna() & (df_total['Texto'] != '')).sum()
fornecedor_preenchido = (df_total['Fornecedor'].notna() & (df_total['Fornecedor'] != '')).sum()
material_preenchido = (df_total['Material'].notna() & (df_total['Material'] != '')).sum() if 'Material' in df_total.columns else 0

print(f"   📊 Texto preenchido: {texto_preenchido:,} / {len(df_total):,} ({texto_preenchido/len(df_total)*100:.1f}%)")
print(f"   📊 Fornecedor preenchido: {fornecedor_preenchido:,} / {len(df_total):,} ({fornecedor_preenchido/len(df_total)*100:.1f}%)")
print(f"   📊 Material preenchido: {material_preenchido:,} / {len(df_total):,} ({material_preenchido/len(df_total)*100:.1f}%)")

# PASSO 2: FILTRAR E ORGANIZAR COLUNAS (ORDEM ORIGINAL)
df_total = df_total[['Período', 'Nº conta', 'Centro cst', 'doc.ref', 'Dt.lçto.', 'Valor', 'Qtd.', 'Type 05', 'Type 06', 'Type 07', 'USI', 'Oficina', 'Doc.compra', 'Texto', 'Fornecedor', 'Material', 'Usuário', 'Fornec.', 'Tipo']]

# mudar os nomes das colunas para Nºconta, Centrocst, Nºdoc.ref., QTD, Texto breve
df_total.rename(columns={'Texto': 'Texto breve'}, inplace=True)
df_total.rename(columns={'Qtd.': 'QTD'}, inplace=True)
df_total.rename(columns={'Nº conta': 'Nºconta', 'Centro cst': 'Centrocst', 'doc.ref': 'Nºdoc.ref.'}, inplace=True)
# Mudar o nome da coluna Type 07 para Account
df_total.rename(columns={'Type 07': 'Account'}, inplace=True)
# Mudar o nome da coluna 'Periodo' para Mes
df_total.rename(columns={'Período': 'Mes'}, inplace=True)

# Criar uma coluna com os meses por extenso baseados na coluna 'Mes'
# a coluna Mes deve ser string
df_total['Período'] = df_total['Mes'].astype(str)
df_total['Período'] = df_total['Mes'].apply(lambda x: 'janeiro' if x == 1 else 'fevereiro' if x == 2 else 'março' if x == 3 else 'abril' if x == 4 else 'maio' if x == 5 else 'junho' if x == 6 else 'julho' if x == 7 else 'agosto' if x == 8 else 'setembro' if x == 9 else 'outubro' if x == 10 else 'novembro' if x == 11 else 'dezembro')

# Trazer coluna 'mes' para a primeira posição e a coluna 'Período' para a segunda posição do DataFrame
colunas = ['Mes', 'Período'] + [col for col in df_total.columns if col != 'Mes' and col != 'Período']
df_total = df_total[colunas]

print(f"   ✅ Colunas organizadas: {len(df_total.columns)} colunas")
print(f"   📊 Ordem: {list(df_total.columns)}")




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
    df_veiculos = df_total_excel[df_total_excel['USI'].isin(usis_veiculos_existentes)].copy()
    
    # Salvar diretamente sem conversões adicionais (já foram feitas antes)
    df_veiculos.to_excel(caminho_veiculos, index=False)
    print(f"Arquivo Excel Veículos salvo: {caminho_veiculos} ({len(df_veiculos)} registros)")
else:
    print("Nenhuma USI de veículos encontrada nos dados")

# Salvar arquivo Excel com filtro de USI 'PWT' (se existir)
if 'PWT' in usis_disponiveis:
    caminho_pwt = os.path.join(pasta_arquivos, 'KE5Z_pwt.xlsx')
    df_pwt = df_total_excel[df_total_excel['USI'] == 'PWT'].copy()
    
    # Salvar diretamente sem conversões adicionais
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
            df_usi = df_total_excel[df_total_excel['USI'] == usi].copy()
            
            if len(df_usi) > 0:
                # Salvar diretamente sem conversões adicionais
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
