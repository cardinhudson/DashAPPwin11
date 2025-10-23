import streamlit as st
import pandas as pd
import os
import altair as alt
# Plotly com versão compatível
import plotly.graph_objects as go
PLOTLY_AVAILABLE = True
from datetime import datetime
import re
import sys

# Adicionar diretório pai ao path para importar auth_simple
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuração da página
st.set_page_config(
    page_title="IUD Assistant - Interactive User Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verificar autenticação
from auth_simple import (verificar_autenticacao, verificar_status_aprovado, exibir_header_usuario,
                         is_modo_cloud, get_modo_operacao)
verificar_autenticacao()

# Indicador de navegação no topo
st.sidebar.markdown("📋 **NAVEGAÇÃO:** Menu de páginas acima ⬆️")
st.sidebar.markdown("---")

# Verificar se o usuário está aprovado
if 'usuario_nome' in st.session_state and not verificar_status_aprovado(st.session_state.usuario_nome):
    st.warning("⏳ Sua conta ainda está pendente de aprovação.")
    st.stop()

# Título da página com novo nome e significado
st.markdown("""
<div style="text-align: center; padding: 1.5rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 1rem;">
    <h1 style="color: white; font-size: 2.5rem; margin: 0;">🎯 IUD Assistant</h1>
    <h3 style="color: #f0f0f0; margin: 0.5rem 0;">Interactive User Dashboard</h3>
    <p style="color: #e0e0e0; font-size: 1rem; margin: 0;">
        Assistente Inteligente & Análise Waterfall Interativa
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Exibir header do usuário
exibir_header_usuario()

st.markdown("---")

# Usar modo selecionado no login (substitui detecção automática)
is_cloud = is_modo_cloud()

# Informar sobre modo selecionado
modo_atual = get_modo_operacao()
if modo_atual == 'cloud':
    st.sidebar.info("☁️ **Modo Cloud (Otimizado)**\n"
                     "Dados otimizados para melhor performance.")
else:
    st.sidebar.success("💻 **Modo Completo**\n"
                       "Acesso a todos os conjuntos de dados.")

# Interface para seleção de dados
st.sidebar.markdown("---")
st.sidebar.subheader("🗂️ Seleção de Dados")

# Verificar quais arquivos estão disponíveis
arquivos_status = {}
for tipo, nome in [("completo", "KE5Z.parquet"), ("main", "KE5Z_main.parquet"), ("others", "KE5Z_others.parquet")]:
    caminho = os.path.join("KE5Z", nome)
    arquivos_status[tipo] = os.path.exists(caminho)

# Opções disponíveis baseadas nos arquivos existentes
opcoes_dados = []
if arquivos_status.get("main", False):
    opcoes_dados.append(("📊 Dados Principais (sem Others)", "main"))

# No modo cloud, NÃO mostrar "Apenas Others" para otimizar memória
if not is_cloud and arquivos_status.get("others", False):
    opcoes_dados.append(("📋 Apenas Others", "others"))

# No Streamlit Cloud, NÃO mostrar dados completos para evitar sobrecarga
if not is_cloud and arquivos_status.get("completo", False):
    opcoes_dados.append(("📁 Dados Completos", "completo"))

# Se não há arquivos separados, usar apenas completo (modo local)
if not opcoes_dados:
    if is_cloud:
        st.error("❌ **Erro no Streamlit Cloud**: Arquivos otimizados não encontrados!")
        st.error("Execute a extração localmente para gerar `KE5Z_main.parquet` e `KE5Z_others.parquet`")
        st.stop()
    else:
        opcoes_dados = [("📁 Dados Completos", "completo")]

# Widget de seleção
opcao_selecionada = st.sidebar.selectbox(
    "Escolha o conjunto de dados:",
    options=[op[1] for op in opcoes_dados],
    format_func=lambda x: next(op[0] for op in opcoes_dados if op[1] == x),
    index=0  # Padrão: primeiro disponível
)

# Mostrar informações sobre a seleção
if opcao_selecionada == "main":
    info_msg = "🎯 **Dados Otimizados**\nCarregando apenas dados principais (USI ≠ 'Others')\nMelhor performance para análises gerais."
    if is_cloud:
        info_msg += "\n\n☁️ **Modo Cloud**: Arquivo otimizado para melhor performance."
    st.sidebar.info(info_msg)
elif opcao_selecionada == "others":
    info_msg = "🔍 **Dados Others**\nCarregando apenas registros USI = 'Others'\nPara análise específica de Others."
    if is_cloud:
        info_msg += "\n\n☁️ **Modo Cloud**: Arquivo otimizado para melhor performance."
    st.sidebar.info(info_msg)
else:
    st.sidebar.info("📊 **Dados Completos**\n"
                   "Todos os registros incluindo Others\n"
                   "💻 **Disponível apenas no modo local**")

# Mostrar aviso sobre otimização no cloud
if is_cloud:
    st.sidebar.success("⚡ **Otimização Ativa**\n"
                      "Usando arquivos separados para melhor performance no Cloud!")

# Função auxiliar para encontrar coluna de período (resolve problemas de encoding)
def encontrar_coluna_periodo(df):
    """Encontra a coluna de período mesmo com problemas de encoding"""
    for col in df.columns:
        if 'período' in col.lower() or 'periodo' in col.lower():
            return col
    return None

# Carregar dados com tratamento robusto
@st.cache_data(show_spinner=True, max_entries=3, ttl=3600, persist="disk")
def load_data(arquivo_tipo="completo"):
    """Carrega os dados do arquivo parquet com tratamento de erro - WATERFALL OTIMIZADO"""
    
    # PRIORIDADE 1: Tentar arquivo waterfall otimizado (72% menor!)
    arquivo_waterfall = os.path.join("_internal", "KE5Z", "KE5Z_waterfall.parquet")
    if os.path.exists(arquivo_waterfall):
        try:
            df = pd.read_parquet(arquivo_waterfall)
            # Aplicar filtro se necessário baseado no tipo solicitado
            if arquivo_tipo == "main" and 'USI' in df.columns:
                df = df[df['USI'] != 'Others'].copy()
            elif arquivo_tipo == "others" and 'USI' in df.columns:
                df = df[df['USI'] == 'Others'].copy()
            # arquivo_tipo "completo" usa todos os dados do waterfall
            
            # Aplicar otimizações de memória (já otimizado mas pode melhorar mais)
            try:
                for col in df.columns:
                    if df[col].dtype == 'object':
                        unique_ratio = (df[col].nunique(dropna=True) / max(1, len(df)))
                        if unique_ratio < 0.5:
                            df[col] = df[col].astype('category')
                for col in df.select_dtypes(include=['float64']).columns:
                    df[col] = pd.to_numeric(df[col], downcast='float')
                for col in df.select_dtypes(include=['int64']).columns:
                    df[col] = pd.to_numeric(df[col], downcast='integer')
            except Exception:
                pass
            
            # Validar dados básicos
            if df.empty:
                st.error("❌ Arquivo waterfall está vazio")
                return pd.DataFrame()
                
            # Incluir todos os dados válidos
            df = df[df['USI'].notna()]
            
            st.sidebar.success("⚡ **WATERFALL OTIMIZADO**\nUsando arquivo 72% menor!")
            return df
            
        except Exception as e:
            st.sidebar.warning(f"⚠️ Erro no arquivo waterfall: {str(e)}")
    
    # FALLBACK: Usar arquivos originais se waterfall não estiver disponível
    arquivos_disponiveis = {
        "completo": "KE5Z.parquet",
        "main": "KE5Z_main.parquet", 
        "others": "KE5Z_others.parquet"
    }
    
    nome_arquivo = arquivos_disponiveis.get(arquivo_tipo, "KE5Z.parquet")
    arquivo_parquet = os.path.join("KE5Z", nome_arquivo)
    
    try:
        if not os.path.exists(arquivo_parquet):
            # Se arquivo específico não existe, tentar arquivo completo
            if arquivo_tipo != "completo":
                st.warning(f"⚠️ Arquivo {nome_arquivo} não encontrado, carregando dados completos...")
                # CORREÇÃO: Evitar loop infinito - carregar diretamente o arquivo completo
                arquivo_completo = os.path.join("KE5Z", "KE5Z.parquet")
                if os.path.exists(arquivo_completo):
                    df = pd.read_parquet(arquivo_completo)
                    # Aplicar filtro baseado no tipo solicitado
                    if 'USI' in df.columns:
                        if arquivo_tipo == "main":
                            df = df[df['USI'] != 'Others'].copy()
                        elif arquivo_tipo == "others":
                            df = df[df['USI'] == 'Others'].copy()
                    return df
                else:
                    st.error(f"❌ Arquivo completo também não encontrado: {arquivo_completo}")
                    return pd.DataFrame()
            st.error(f"❌ Arquivo não encontrado: {arquivo_parquet}")
            return pd.DataFrame()
        
        df = pd.read_parquet(arquivo_parquet)
        # Compactar memória sem alterar dados
        try:
            for col in df.columns:
                if df[col].dtype == 'object':
                    unique_ratio = (df[col].nunique(dropna=True) / max(1, len(df)))
                    if unique_ratio < 0.5:
                        df[col] = df[col].astype('category')
            for col in df.select_dtypes(include=['float64']).columns:
                df[col] = pd.to_numeric(df[col], downcast='float')
            for col in df.select_dtypes(include=['int64']).columns:
                df[col] = pd.to_numeric(df[col], downcast='integer')
        except Exception:
            pass
        
        # Validar dados básicos
        if df.empty:
            st.error("❌ Arquivo parquet está vazio")
            return pd.DataFrame()
            
        # Incluir todos os dados (incluindo Others)
        df = df[df['USI'].notna()]
        
        return df
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        if is_cloud:
            st.info("☁️ Problemas de carregamento são comuns no Streamlit Cloud com arquivos grandes")
        return pd.DataFrame()

# Carregar dados
with st.spinner("🔄 Carregando dados..."):
    df_total = load_data(opcao_selecionada)

if df_total.empty:
    st.error("❌ Não foi possível carregar os dados.")
    st.info("💡 **Possíveis soluções:**")
    st.info("1. Verifique se os arquivos parquet existem na pasta KE5Z/")
    st.info("2. Tente recarregar a página")
    st.info("3. Verifique se o arquivo não está corrompido")
    
    if is_cloud:
        st.info("☁️ **No Streamlit Cloud:** Certifique-se que os arquivos foram enviados para o repositório")
    
    st.stop()

# Mostrar informações de carregamento
st.sidebar.success("✅ Dados carregados com sucesso")
if not is_cloud:
    st.sidebar.info(f"📊 {len(df_total)} registros carregados")

# Aplicar filtros padrão do projeto
st.sidebar.title("Filtros")

# Filtro 1: USINA (com tratamento de erro)
try:
    usina_opcoes = ["Todos"] + sorted(df_total['USI'].dropna().astype(str).unique().tolist()) if 'USI' in df_total.columns else ["Todos"]
    default_usina = ["Veículos"] if "Veículos" in usina_opcoes else ["Todos"]
    usina_selecionada = st.sidebar.multiselect("Selecione a USINA:", usina_opcoes, default=default_usina)
except Exception as e:
    st.sidebar.error(f"Erro nos filtros: {str(e)}")
    usina_selecionada = ["Todos"]

# Filtrar o DataFrame com base na USI
if "Todos" in usina_selecionada or not usina_selecionada:
    df_filtrado = df_total.copy()
else:
    df_filtrado = df_total[df_total['USI'].astype(str).isin(usina_selecionada)]

# Filtro 2: Período (com tratamento de erro e correção de encoding)
try:
    coluna_periodo = encontrar_coluna_periodo(df_filtrado)
    
    if coluna_periodo is not None:
        periodo_opcoes = ["Todos"] + sorted(df_filtrado[coluna_periodo].dropna().astype(str).unique().tolist())
        periodo_selecionado = st.sidebar.selectbox("Selecione o Período:", periodo_opcoes)
        if periodo_selecionado != "Todos":
            df_filtrado = df_filtrado[df_filtrado[coluna_periodo].astype(str) == str(periodo_selecionado)]
    else:
        st.sidebar.warning("⚠️ Coluna 'Período' não encontrada nos dados")
        periodo_selecionado = "Todos"
except Exception as e:
    st.sidebar.error(f"Erro no filtro Período: {str(e)}")
    periodo_selecionado = "Todos"

# Filtro 3: Centro cst (com tratamento de erro)
try:
    if 'Centro cst' in df_filtrado.columns:
        centro_cst_opcoes = ["Todos"] + sorted(df_filtrado['Centro cst'].dropna().astype(str).unique().tolist())
        centro_cst_selecionado = st.sidebar.selectbox("Selecione o Centro cst:", centro_cst_opcoes)
        if centro_cst_selecionado != "Todos":
            df_filtrado = df_filtrado[df_filtrado['Centro cst'].astype(str) == str(centro_cst_selecionado)]
except Exception as e:
    st.sidebar.error(f"Erro no filtro Centro cst: {str(e)}")

# Filtro 4: Conta contábil (com tratamento de erro)
try:
    if 'Nº conta' in df_filtrado.columns:
        conta_contabil_opcoes = sorted(df_filtrado['Nº conta'].dropna().astype(str).unique().tolist())
        # Limitar opções no cloud para evitar problemas
        if is_cloud and len(conta_contabil_opcoes) > 100:
            conta_contabil_opcoes = conta_contabil_opcoes[:100]
            st.sidebar.info("☁️ Limitando opções para melhor performance")
        
        conta_contabil_selecionadas = st.sidebar.multiselect("Selecione a Conta contábil:", conta_contabil_opcoes)
        if conta_contabil_selecionadas:
            df_filtrado = df_filtrado[df_filtrado['Nº conta'].astype(str).isin(conta_contabil_selecionadas)]
except Exception as e:
    st.sidebar.error(f"Erro no filtro Conta contábil: {str(e)}")

# Cache para opções de filtros (otimização de performance)
@st.cache_data(ttl=1800, max_entries=3)
def get_filter_options_ia(df, column_name):
    """Obtém opções de filtro com cache para melhor performance"""
    if column_name in df.columns:
        return ["Todos"] + sorted(df[column_name].dropna().astype(str).unique().tolist())
    return ["Todos"]

# Filtros principais (com cache otimizado)
filtros_principais = [
    ("Type 05", "Type 05", "multiselect"),
    ("Type 06", "Type 06", "multiselect"), 
    ("Type 07", "Type 07", "multiselect"),
    ("Fornecedor", "Fornecedor", "multiselect"),
    ("Fornec.", "Fornec.", "multiselect"),
    ("Tipo", "Tipo", "multiselect")
]

for col_name, label, widget_type in filtros_principais:
    try:
        if col_name in df_filtrado.columns:
            opcoes = get_filter_options_ia(df_filtrado, col_name)
            
            # Limitar opções no cloud para evitar problemas
            if is_cloud and len(opcoes) > 51:  # 50 + "Todos"
                opcoes = opcoes[:51]
                st.sidebar.info(f"☁️ {label}: Limitado para performance")
            
            if widget_type == "multiselect":
                selecionadas = st.sidebar.multiselect(f"Selecione o {label}:", opcoes, default=["Todos"])
                if selecionadas and "Todos" not in selecionadas:
                    df_filtrado = df_filtrado[df_filtrado[col_name].astype(str).isin(selecionadas)]
    except Exception as e:
        st.sidebar.error(f"Erro no filtro {label}: {str(e)}")

# Filtros avançados (expansível)
with st.sidebar.expander("🔍 Filtros Avançados"):
    filtros_avancados = [
        ("Oficina", "Oficina", "multiselect"),
        ("Usuário", "Usuário", "multiselect"),
        ("Denominação", "Denominação", "multiselect"),
        ("Dt.lçto.", "Data Lançamento", "multiselect")
    ]
    
    for col_name, label, widget_type in filtros_avancados:
        try:
            if col_name in df_filtrado.columns:
                opcoes = get_filter_options_ia(df_filtrado, col_name)
                # Limitar opções para melhor performance
                if len(opcoes) > 51:  # 50 + "Todos"
                    opcoes = opcoes[:51]
                    st.caption(f"⚠️ {label}: Limitado para performance")
                
                if widget_type == "multiselect":
                    selecionadas = st.multiselect(f"Selecione o {label}:", opcoes, default=["Todos"])
                    if selecionadas and "Todos" not in selecionadas:
                        df_filtrado = df_filtrado[df_filtrado[col_name].astype(str).isin(selecionadas)]
        except Exception as e:
            st.error(f"Erro no filtro {label}: {str(e)}")

# Exibir informações dos filtros (com tratamento de erro)
try:
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Resumo dos Dados")
    st.sidebar.write(f"**Linhas:** {df_filtrado.shape[0]:,}")
    st.sidebar.write(f"**Colunas:** {df_filtrado.shape[1]:,}")
    if 'Valor' in df_filtrado.columns:
        total_valor = df_filtrado['Valor'].sum()
        st.sidebar.write(f"**Total:** R$ {total_valor:,.2f}")
    
    # Informações adicionais para debug no cloud
    if is_cloud:
        st.sidebar.info(f"☁️ Modo Cloud - {len(df_filtrado)} registros")
except Exception as e:
    st.sidebar.error(f"Erro ao exibir resumo: {str(e)}")

# Usar df_filtrado em vez de df_total no restante da página

# Classe do Assistente IUD
class IUDAssistant:
    def __init__(self, df_data):
        self.df = df_data
        
    def analyze_question(self, question):
        """Analisa a pergunta usando regras locais simples"""
        question_lower = question.lower()
        
        analysis_type = "ranking"
        entities = {}
        limit = 10  # padrão
        confidence = 0.8
        
        # Detectar limite (top 10, top 20, etc.)
        top_match = re.search(r'top\s+(\d+)', question_lower)
        if top_match:
            limit = int(top_match.group(1))
            entities['limit'] = limit
        
        # Detectar "X maiores"
        maiores_match = re.search(r'(\d+)\s+maiores', question_lower)
        if maiores_match:
            limit = int(maiores_match.group(1))
            entities['limit'] = limit
        
        # Detectar análise temporal
        if any(phrase in question_lower for phrase in ['temporal', 'tempo', 'evolução', 'mensal', 'mês']):
            analysis_type = "temporal"
            entities['periodo'] = True
        
        # Detectar waterfall
        if any(word in question_lower for word in ['waterfall', 'cascata', 'variação']):
            analysis_type = "waterfall"
        
        # Detectar entidades específicas
        if any(word in question_lower for word in ['type 07', 'type07']):
            entities['type_07'] = True
        if any(word in question_lower for word in ['type 05', 'type05']):
            entities['type_05'] = True
        if any(word in question_lower for word in ['type 06', 'type06']):
            entities['type_06'] = True
        if any(word in question_lower for word in ['usi', 'usina']):
            entities['usi'] = True
        if any(word in question_lower for word in ['fornecedor', 'supplier']):
            entities['fornecedor'] = True
            
        return {
            'type': analysis_type,
            'entities': entities,
            'original_question': question,
            'limit': limit,
            'confidence': confidence
        }
    
    def execute_analysis(self, analysis):
        """Executa a análise baseada no tipo detectado"""
        try:
            if analysis['type'] == 'ranking':
                return self._ranking_analysis(analysis)
            elif analysis['type'] == 'temporal':
                return self._temporal_analysis(analysis)
            elif analysis['type'] == 'waterfall':
                return self._waterfall_analysis(analysis)
            else:
                return self._default_analysis(analysis)
        except Exception as e:
            st.error(f"Erro na análise: {str(e)}")
            return None
    
    def _ranking_analysis(self, analysis):
        """Análise de ranking"""
        entities = analysis['entities']
        limit = analysis.get('limit', 10)
        
        if entities.get('type_07'):
            data = self.df.groupby('Type 07')['Valor'].sum().reset_index()
            data = data.sort_values('Valor', ascending=False).head(limit)
            title = f"Top {limit} Type 07"
        elif entities.get('type_05'):
            data = self.df.groupby('Type 05')['Valor'].sum().reset_index()
            data = data.sort_values('Valor', ascending=False).head(limit)
            title = f"Top {limit} Type 05"
        elif entities.get('type_06'):
            data = self.df.groupby('Type 06')['Valor'].sum().reset_index()
            data = data.sort_values('Valor', ascending=False).head(limit)
            title = f"Top {limit} Type 06"
        elif entities.get('usi'):
            data = self.df.groupby('USI')['Valor'].sum().reset_index()
            data = data.sort_values('Valor', ascending=False).head(limit)
            title = f"Top {limit} USIs"
        elif entities.get('fornecedor'):
            data = self.df.groupby('Fornecedor')['Valor'].sum().reset_index()
            data = data.sort_values('Valor', ascending=False).head(limit)
            title = f"Top {limit} Fornecedores"
        else:
            # Padrão: Type 07
            data = self.df.groupby('Type 07')['Valor'].sum().reset_index()
            data = data.sort_values('Valor', ascending=False).head(limit)
            title = f"Top {limit} Type 07"
        
        # Criar gráfico
        if len(data.columns) >= 2:
            col1, col2 = data.columns[0], data.columns[1]
            chart = alt.Chart(data).mark_bar().encode(
                x=alt.X(f'{col1}:N', sort='-y', title=col1),
                y=alt.Y(f'{col2}:Q', title='Valor (R$)'),
                color=alt.Color(f'{col2}:Q', scale=alt.Scale(range=['#27ae60', '#e74c3c']))
            ).properties(title=title, width=600, height=400)
        else:
            chart = None
        
        return {
            'data': data,
            'chart': chart,
            'title': title,
            'response': f"📊 {title}\\n💰 Valor total: R$ {data[data.columns[1]].sum():,.2f}"
        }
    
    def _temporal_analysis(self, analysis):
        """Análise temporal"""
        coluna_periodo = encontrar_coluna_periodo(self.df)
        if coluna_periodo is None:
            return {'error': 'Coluna Período não encontrada'}
            
        data = self.df.groupby(coluna_periodo)['Valor'].sum().reset_index()
        data = data.sort_values(coluna_periodo)
        
        chart = alt.Chart(data).mark_line(point=True, color='#3498db').encode(
            x=alt.X(f'{coluna_periodo}:O', title='Período'),
            y=alt.Y('Valor:Q', title='Valor (R$)'),
        ).properties(title="Evolução Temporal", width=600, height=400)
        
        return {
            'data': data,
            'chart': chart,
            'title': "Evolução Temporal",
            'response': f"📈 Evolução temporal\\n📅 Períodos: {len(data)}\\n💰 Valor total: R$ {data['Valor'].sum():,.2f}"
        }
    
    def _waterfall_analysis(self, analysis):
        """Análise waterfall"""
        coluna_periodo = encontrar_coluna_periodo(self.df)
        if coluna_periodo is None:
            return {'error': 'Coluna Período não encontrada'}
            
        data = self.df.groupby(coluna_periodo)['Valor'].sum().reset_index()
        data = data.sort_values(coluna_periodo)
        
        if len(data) >= 2:
            fig = go.Figure(go.Waterfall(
                name="Waterfall",
                orientation="v",
                measure=["absolute"] + ["relative"] * (len(data) - 2) + ["absolute"],
                x=data[coluna_periodo].tolist(),
                y=data['Valor'].tolist(),
                connector={"line": {"color": "rgb(63, 63, 63)"}},
                increasing={"marker": {"color": "#e74c3c"}},  # Vermelho para aumentos
                decreasing={"marker": {"color": "#27ae60"}},  # Verde para diminuições
                totals={"marker": {"color": "#3498db"}}       # Azul para totais
            ))
            fig.update_layout(
                title="Análise Waterfall - Variações por Período",
                xaxis_title="Período",
                yaxis_title="Valor (R$)",
                height=500
            )
        else:
            fig = None
        
        return {
            'data': data,
            'chart': fig,
            'title': "Análise Waterfall",
            'response': f"🌊 Análise Waterfall\\n📅 Períodos: {len(data)}\\n💰 Variação total: R$ {data['Valor'].sum():,.2f}"
        }
    
    def _default_analysis(self, analysis):
        """Análise padrão"""
        data = self.df.groupby('Type 07')['Valor'].sum().reset_index()
        data = data.sort_values('Valor', ascending=False).head(10)
        
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X('Type 07:N', sort='-y', title='Type 07'),
            y=alt.Y('Valor:Q', title='Valor (R$)'),
            color=alt.Color('Valor:Q', scale=alt.Scale(range=['#27ae60', '#e74c3c']))
        ).properties(title="Top 10 Type 07", width=600, height=400)
        
        return {
            'data': data,
            'chart': chart,
            'title': "Top 10 Type 07",
            'response': f"📊 Top 10 Type 07\\n💰 Valor total: R$ {data['Valor'].sum():,.2f}"
        }

# Função para criar gráfico waterfall configurável
def create_waterfall_chart(data, x_col, y_col, title):
    """Cria um gráfico waterfall"""
    if len(data) < 2:
        st.warning("⚠️ Dados insuficientes para criar gráfico waterfall.")
        return None
    
    # Preparar dados para waterfall
    values = data[y_col].tolist()
    labels = data[x_col].tolist()
    
    # Criar medidas (primeiro é absoluto, intermediários são relativos, último é total)
    measures = ["absolute"]
    for i in range(1, len(values) - 1):
        measures.append("relative")
    if len(values) > 1:
        measures.append("total")
    
    fig = go.Figure(go.Waterfall(
        name="Waterfall Analysis",
        orientation="v",
        measure=measures,
        x=labels,
        y=values,
        textposition="outside",
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "#e74c3c"}},  # Vermelho para aumentos
        decreasing={"marker": {"color": "#27ae60"}},  # Verde para diminuições
        totals={"marker": {"color": "#3498db"}}       # Azul para totais
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title="Valor (R$)",
        height=500,
        showlegend=False
    )
    
    return fig

# Inicializar assistente
assistant = IUDAssistant(df_filtrado)

# Tabs para organizar as funcionalidades
tab1, tab2 = st.tabs(["🤖 IUD Assistant", "🌊 Análise Waterfall"])

# TAB 1: Assistente IUD
with tab1:
    st.subheader("💬 Chat com IUD Assistant")
    st.caption("🎯 **Interactive User Dashboard** - Assistente inteligente para análise de dados")
    
    # Histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibir mensagens do histórico
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Exibir gráfico se existir
            if "chart" in message and message["chart"] is not None:
                if hasattr(message["chart"], 'update_layout'):  # Plotly
                    st.plotly_chart(message["chart"], use_container_width=True)
                else:  # Altair
                    st.altair_chart(message["chart"], use_container_width=True)
            
            # Exibir dados se existir
            if "data" in message and message["data"] is not None:
                with st.expander("📊 Ver dados detalhados"):
                    st.dataframe(message["data"], use_container_width=True)

    # Input do usuário
    if prompt := st.chat_input("Faça uma pergunta sobre os dados..."):
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Processar pergunta
        with st.chat_message("assistant"):
            with st.spinner("Analisando..."):
                # Analisar pergunta
                analysis = assistant.analyze_question(prompt)
                
                # Executar análise
                result = assistant.execute_analysis(analysis)
                
                if result:
                    # Exibir resposta
                    st.markdown(result['response'])
                    
                    # Exibir gráfico
                    if result['chart'] is not None:
                        if hasattr(result['chart'], 'update_layout'):  # Plotly
                            st.plotly_chart(result['chart'], use_container_width=True)
                        else:  # Altair
                            st.altair_chart(result['chart'], use_container_width=True)
                    
                    # Exibir dados
                    if not result['data'].empty:
                        with st.expander("📊 Ver dados detalhados"):
                            st.dataframe(result['data'], use_container_width=True)
                    
                    # Adicionar ao histórico
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": result['response'],
                        "chart": result['chart'],
                        "data": result['data']
                    })
                else:
                    error_msg = "❌ Não foi possível processar sua pergunta. Tente reformular."
                    st.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

# TAB 2: Análise Waterfall
with tab2:
    st.subheader("🌊 Análise Waterfall Configurável")

    # Configurações (mesmo padrão do Waterfall_Analysis)
    st.markdown("### ⚙️ Configurações")

    # Detectar tema do Streamlit para aplicar no gráfico (dark/light)
    theme_base = st.get_option("theme.base") or "light"
    bg_color = st.get_option("theme.backgroundColor") or ("#0e1117" if theme_base == "dark" else "#FFFFFF")
    sec_bg_color = st.get_option("theme.secondaryBackgroundColor") or ("#262730" if theme_base == "dark" else "#F5F5F5")
    text_color = st.get_option("theme.textColor") or ("#FAFAFA" if theme_base == "dark" else "#000000")
    grid_color = "rgba(255,255,255,0.12)" if theme_base == "dark" else "rgba(0,0,0,0.12)"
    connector_color = "rgba(255,255,255,0.35)" if theme_base == "dark" else "rgba(0,0,0,0.35)"

    # Meses disponíveis a partir de 'Período'
    coluna_periodo = encontrar_coluna_periodo(df_filtrado)
    if coluna_periodo is not None:
        meses_disponiveis = sorted(df_filtrado[coluna_periodo].dropna().astype(str).unique().tolist())
    else:
        st.error("❌ Coluna 'Período' não encontrada para análise waterfall")
        st.stop()
    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_a:
        mes_inicial = st.selectbox("Mês inicial:", meses_disponiveis, index=0)
    with col_b:
        mes_final = st.selectbox("Mês final:", meses_disponiveis, index=len(meses_disponiveis) - 1)

    # Dimensão de categoria
    dims_cat = [c for c in ['Type 05', 'Type 06', 'Type 07', 'Fornecedor', 'USI'] if c in df_filtrado.columns]
    if not dims_cat:
        st.warning("Não há colunas de categoria compatíveis (Type 05/06/07, Fornecedor, USI).")
        st.stop()
    chosen_dim = st.selectbox("Dimensão da categoria:", dims_cat, index=0)

    # Categorias disponíveis e multiselect com 'Todos' (normalização por strip)
    def _norm_list(seq):
        return sorted([str(x).strip() for x in seq if str(x).strip() != ""])
    cats_all = _norm_list(df_filtrado[chosen_dim].dropna().unique().tolist())
    vol_mf = (df_filtrado[df_filtrado[coluna_periodo].astype(str) == str(mes_final)]
              .groupby(chosen_dim)['Valor'].sum().sort_values(ascending=False))
    # Slider com máximo e padrão iguais ao total de categorias
    total_cats = max(1, len(cats_all))
    with col_c:
        max_cats = st.slider(f"Top N categorias (Total: {total_cats}):", 1, total_cats, total_cats)
    vol_index = _norm_list(list(vol_mf.index))
    default_cats = vol_index[:max_cats] if len(vol_index) else cats_all[:max_cats]
    # Filtrar defaults que não estejam em options
    cats_options = ['Todos'] + cats_all
    default_cats = [c for c in default_cats if c in cats_all]
    if not default_cats:
        default_cats = cats_all[:min(10, len(cats_all))]
    cats_sel_raw = st.multiselect("Categorias (uma ou mais):", cats_options, default=default_cats)
    if (not cats_sel_raw) or ('Todos' in cats_sel_raw):
        cats_sel = cats_all
    else:
        cats_sel = cats_sel_raw

    if mes_inicial == mes_final:
        st.info("Selecione meses diferentes para comparar.")
        st.stop()

    # Totais de mês (todas as categorias)
    total_m1_all = float(df_filtrado[df_filtrado[coluna_periodo].astype(str) == str(mes_inicial)]['Valor'].sum())
    total_m2_all = float(df_filtrado[df_filtrado[coluna_periodo].astype(str) == str(mes_final)]['Valor'].sum())
    change_all = total_m2_all - total_m1_all

    # Filtrar pelas categorias escolhidas
    dff = df_filtrado[df_filtrado[chosen_dim].astype(str).isin(cats_sel)].copy()
    g1 = (dff[dff[coluna_periodo].astype(str) == str(mes_inicial)]
          .groupby(chosen_dim)['Valor'].sum())
    g2 = (dff[dff[coluna_periodo].astype(str) == str(mes_final)]
          .groupby(chosen_dim)['Valor'].sum())

    labels_cats, values_cats = [], []
    for cat in sorted(set(g1.index).union(set(g2.index))):
        delta = float(g2.get(cat, 0.0)) - float(g1.get(cat, 0.0))
        if abs(delta) > 1e-9:
            labels_cats.append(str(cat))
            values_cats.append(delta)

    # Aplicar Top N por impacto absoluto
    original_len = len(labels_cats)
    if len(labels_cats) > max_cats:
        idx = sorted(range(len(values_cats)), key=lambda i: abs(values_cats[i]), reverse=True)[:max_cats]
        labels_cats = [labels_cats[i] for i in idx]
        values_cats = [values_cats[i] for i in idx]
    cropped = len(labels_cats) < original_len

    # Remainder para fechar (com arredondamento)
    remainder = round(change_all - sum(values_cats), 2)
    all_selected = set(cats_sel) == set(cats_all)
    show_outros = (abs(remainder) >= 0.01) and (not all_selected or cropped)
    if show_outros:
        labels_cats.append('Outros')
        values_cats.append(remainder)

    labels = [f"Mês {mes_inicial}"] + labels_cats + [f"Mês {mes_final}"]
    values = [total_m1_all] + values_cats + [total_m2_all]
    measures = ['absolute'] + ['relative'] * len(values_cats) + ['total']

    # Gráfico principal com cores do tema
    fig = go.Figure(go.Waterfall(
        name='Variação',
        orientation='v',
        measure=measures,
        x=labels,
        y=values,
        text=[f"R$ {v:,.2f}" for v in values],
        textposition='outside',
        connector={'line': {'color': connector_color}},
        increasing={'marker': {'color': '#27ae60'}},
        decreasing={'marker': {'color': '#e74c3c'}},
        totals={'marker': {'color': '#4e79a7'}},
    ))
    # Rótulos de dados: branco no dark, preto no light
    fig.update_traces(textfont=dict(color=text_color))

    # Overlay "Outros" preto com base correta
    if show_outros:
        prev_sum = sum(v for lab, v in zip(labels_cats, values_cats) if lab != 'Outros')
        cum_before = total_m1_all + prev_sum
        base_val = cum_before if remainder >= 0 else cum_before + remainder
        height = abs(remainder)
        fig.add_trace(go.Bar(x=['Outros'], y=[height], base=[base_val], marker_color='#ff9800', opacity=1.0, hoverinfo='skip', showlegend=False))
        fig.update_layout(barmode='overlay')

    # Apply theme-aware template and transparent backgrounds to inherit app colors
    if theme_base == "dark":
        fig.update_layout(template="plotly_dark")
    else:
        fig.update_layout(template="plotly_white")

    fig.update_layout(
        title={'text': f"Variação Financeira - Mês {mes_inicial} para Mês {mes_final}", 'x': 0.5},
        xaxis_title='Mês / Categoria',
        yaxis_title='Valor (R$)',
        height=560,
        showlegend=False,
        # Transparente para herdar fundo da página (funciona em dark/light)
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=text_color),
        xaxis=dict(gridcolor=grid_color, zerolinecolor=grid_color, linecolor=grid_color),
        yaxis=dict(gridcolor=grid_color, zerolinecolor=grid_color, linecolor=grid_color),
    )
    fig.update_yaxes(tickformat=",.0f", tickprefix="R$ ")

    st.plotly_chart(fig, use_container_width=True)

# Sidebar com exemplos
st.sidebar.title("🎯 IUD Assistant")
st.sidebar.caption("Interactive User Dashboard")

# Exemplos de perguntas
st.sidebar.markdown("### 💡 Exemplos de Perguntas")
st.sidebar.markdown("""
**📊 Rankings:**
- Top 10 maiores Type 07
- 20 maiores fornecedores
- Top 5 USIs

**📈 Temporal:**
- Evolução temporal
- Valor por mês
- Tendência mensal

**🌊 Waterfall:**
- Gráfico waterfall
- Variações por período
- Análise de cascata
""")

# Botão para limpar histórico
if st.sidebar.button("🗑️ Limpar Histórico do Chat"):
    st.session_state.messages = []
    st.rerun()

# Informações sobre cores
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Legenda de Cores")
st.sidebar.markdown("""
- 🟢 **Verde**: Valores menores/diminuições
- 🔴 **Vermelho**: Valores maiores/aumentos
- 🔵 **Azul**: Totais e linhas temporais
""")

# Status
st.sidebar.markdown("---")
st.sidebar.write("**🎯 Status:**")
st.sidebar.success("✅ IUD Assistant Ativo")
st.sidebar.info("📊 Análise baseada em regras locais")
st.sidebar.write(f"**📈 Registros:** {len(df_filtrado):,}")
st.sidebar.write(f"**💰 Valor Total:** R$ {df_filtrado['Valor'].sum():,.2f}")
