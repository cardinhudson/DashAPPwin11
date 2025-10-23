import streamlit as st
import pandas as pd
import os
import sys

# Adicionar diretório pai ao path para importar auth_simple
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth_simple import (verificar_autenticacao, exibir_header_usuario,
                  verificar_status_aprovado, is_modo_cloud, get_modo_operacao)

# Configuração da página
st.set_page_config(
    page_title="Total Accounts - Dashboard KE5Z",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verificar autenticação - OBRIGATÓRIO no início de cada página
verificar_autenticacao()

# Verificar se o usuário está aprovado
if ('usuario_nome' in st.session_state and 
    not verificar_status_aprovado(st.session_state.usuario_nome)):
    st.warning("⏳ Sua conta ainda está pendente de aprovação. "
               "Aguarde o administrador aprovar seu acesso.")
    st.info("📧 Você receberá uma notificação quando sua conta for "
            "aprovada.")
    st.stop()

# Header com informações do usuário
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.title("📊 Total Accounts - Centro de Lucro 02S")
    st.subheader("Somatório de todas as contas do centro de lucro 02S, "
                 "exceto as contas D_B")

# Exibir header do usuário
exibir_header_usuario()

st.markdown("---")

# Conteúdo da nova página
st.write("Esta página contém o somatório de todas as contas do centro de "
         "lucro 02S, exceto as contas D_B!")

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

# Indicador de navegação no topo
st.sidebar.markdown("📋 **NAVEGAÇÃO:** Menu de páginas acima ⬆️")
st.sidebar.markdown("---")

st.sidebar.info("⚡ **DADOS WATERFALL OTIMIZADOS**\n"
                "✅ Usando KE5Z_waterfall.parquet\n"
                "📊 68% menor que arquivo original")

@st.cache_data(ttl=3600, max_entries=3, persist="disk", show_spinner=True)
def load_data_optimized(arquivo_tipo="completo"):
    """Carrega dados INTEIRAMENTE do waterfall para máxima otimização de memória"""
    
    # USAR APENAS ARQUIVO WATERFALL OTIMIZADO (68% menor + Nº conta!)
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
            
            st.sidebar.success("⚡ **TOTAL ACCOUNTS OTIMIZADO**\nUsando APENAS waterfall (68% menor + Nº conta)!")
            return df
        except Exception as e:
            st.sidebar.error(f"❌ Erro no arquivo waterfall: {str(e)}")
            st.error("❌ **Total accounts requer arquivo waterfall otimizado**")
            st.info("💡 Execute a extração de dados para gerar KE5Z_waterfall.parquet")
            st.stop()
    else:
        st.error("❌ **Arquivo waterfall não encontrado**")
        st.error("📁 Total accounts foi otimizado para usar APENAS KE5Z_waterfall.parquet")
        st.info("💡 **Solução**: Execute a extração de dados para gerar o arquivo waterfall")
        st.stop()
    
# Função otimizada - usa APENAS waterfall para máxima performance

# Carregar dados waterfall otimizados
try:
    df_principal = load_data_optimized("completo")  # Sempre usa dados completos do waterfall
    st.sidebar.success("✅ Dados waterfall carregados com sucesso")
    if not is_cloud:
        st.sidebar.info(f"📊 {len(df_principal)} registros carregados")
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {str(e)}")
    st.stop()

# Filtros principais compactos
with st.sidebar.expander("🔍 Filtros Principais", expanded=True):
    # Filtro 1: USINA
    usina_opcoes = ["Todos"] + sorted(df_principal['USI'].dropna().astype(str).unique().tolist()) if 'USI' in df_principal.columns else ["Todos"]
    default_usina = ["Veículos"] if "Veículos" in usina_opcoes else ["Todos"]
    usina_selecionada = st.multiselect("USINA:", usina_opcoes, default=default_usina)

    # Filtrar o DataFrame com base na USI
    if "Todos" in usina_selecionada or not usina_selecionada:
        df_filtrado = df_principal.copy()
    else:
        df_filtrado = df_principal[df_principal['USI'].astype(str).isin(usina_selecionada)]

    # Filtro 2: Período
    periodo_opcoes = ["Todos"] + sorted(df_filtrado['Período'].dropna().astype(str).unique().tolist()) if 'Período' in df_filtrado.columns else ["Todos"]
    periodo_selecionado = st.selectbox("Período:", periodo_opcoes)
    
    if periodo_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Período'].astype(str) == str(periodo_selecionado)]

    # Filtro 3: Centro cst
    if 'Centro cst' in df_filtrado.columns:
        centro_cst_opcoes = ["Todos"] + sorted(df_filtrado['Centro cst'].dropna().astype(str).unique().tolist())
        centro_cst_selecionado = st.selectbox("Centro cst:", centro_cst_opcoes)
        if centro_cst_selecionado != "Todos":
            df_filtrado = df_filtrado[df_filtrado['Centro cst'].astype(str) == str(centro_cst_selecionado)]

    # Filtro 4: Conta contábil
    if 'Nº conta' in df_filtrado.columns:
        conta_contabil_opcoes = sorted(df_filtrado['Nº conta'].dropna().astype(str).unique().tolist())
        conta_contabil_selecionadas = st.multiselect("Conta:", conta_contabil_opcoes)
        if conta_contabil_selecionadas:
            df_filtrado = df_filtrado[df_filtrado['Nº conta'].astype(str).isin(conta_contabil_selecionadas)]

# Cache para opções de filtros (otimização de performance)
@st.cache_data(ttl=1800, max_entries=3)
def get_filter_options(df, column_name):
    """Obtém opções de filtro com cache para melhor performance"""
    if column_name in df.columns:
        return ["Todos"] + sorted(df[column_name].dropna().astype(str).unique().tolist())
    return ["Todos"]

# Filtros secundários compactos
with st.sidebar.expander("🎯 Filtros Secundários", expanded=False):
    filtros_secundarios = [
        ("Type 05", "Type 05"),
        ("Type 06", "Type 06"), 
        ("Type 07", "Type 07"),
        ("Fornecedor", "Fornecedor"),
        ("Fornec.", "Fornec."),
        ("Tipo", "Tipo")
    ]

    for col_name, label in filtros_secundarios:
        if col_name in df_filtrado.columns:
            opcoes = get_filter_options(df_filtrado, col_name)
            selecionadas = st.multiselect(f"{label}:", opcoes, default=["Todos"])
            if selecionadas and "Todos" not in selecionadas:
                df_filtrado = df_filtrado[df_filtrado[col_name].astype(str).isin(selecionadas)]

# Filtros avançados compactos
with st.sidebar.expander("🔧 Filtros Avançados", expanded=False):
    filtros_avancados = [
        ("Oficina", "Oficina"),
        ("Usuário", "Usuário"),
        ("Denominação", "Denominação"),
        ("Dt.lçto.", "Data Lançamento")
    ]
    
    for col_name, label in filtros_avancados:
        if col_name in df_filtrado.columns:
            opcoes = get_filter_options(df_filtrado, col_name)
            if len(opcoes) > 51:
                opcoes = opcoes[:51]
                st.caption(f"⚠️ {label}: Top 50")
            
            selecionadas = st.multiselect(f"{label}:", opcoes, default=["Todos"])
            if selecionadas and "Todos" not in selecionadas:
                df_filtrado = df_filtrado[df_filtrado[col_name].astype(str).isin(selecionadas)]

##################################################################################################

# Título da nova página
st.title("Total SAP KE5Z - Todas as USINAS")

# Verificar se a coluna USI existe
if 'USI' not in df_filtrado.columns:
    st.error("❌ **Coluna 'USI' não encontrada nos dados!**")
    st.warning("⚠️ **Possíveis causas:**")
    st.write("1. Os dados não foram extraídos corretamente")
    st.write("2. O merge com dados SAPIENS não foi realizado")
    st.write("3. O arquivo KE5Z.parquet precisa ser regenerado")
    
    st.info("💡 **Soluções:**")
    st.write("- Execute a **Extração de Dados** na página correspondente")
    st.write("- Certifique-se de que o arquivo 'Dados SAPIENS.xlsx' existe")
    st.write("- Verifique se os merges estão funcionando corretamente")
    
    st.subheader("📋 Colunas disponíveis nos dados:")
    colunas_disponiveis = sorted(df_filtrado.columns.tolist())
    for i, col in enumerate(colunas_disponiveis, 1):
        st.write(f"{i}. {col}")
    
    st.stop()

# Criar uma tabela dinâmica (pivot table) para somar os valores por 'USI', incluindo campos desta coluna vazio ou NAN, a coluna por 'Período' e uma linha total
tabela_somada = df_filtrado.pivot_table(index='USI', columns='Período', values='Valor', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
# Exibir a tabela somada na página com os numeros formatados como moeda brasileira
tabela_somada = tabela_somada.style.format("R$ {:,.2f}", decimal=",",thousands=".")
st.dataframe(tabela_somada)


##################################################################################################
# Título da nova página
st.title("Total SAP KE5Z - Todas as contas")
# Criar uma tabela dinâmica (pivot table) para somar os valores por 'Nº conta' incluindo a coluna por 'Período'
tabela_somada = df_filtrado.pivot_table(index='Nº conta', columns='Período', values='Valor', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')

# Exibir a tabela somada na página com os numeros formatados como moeda brasileira
tabela_somada = tabela_somada.style.format("R$ {:,.2f}", decimal=",",thousands=".")
st.dataframe(tabela_somada)

# ============= GRÁFICOS MÊS A MÊS (MESMO PADRÃO DO DASH PRINCIPAL) =============
st.markdown("---")
st.subheader("📊 Análise Gráfica Mês a Mês")

# Gráfico principal por Período (mesmo padrão do Dash.py)
@st.cache_data(ttl=900, max_entries=2)
def create_period_chart_total_accounts(df_data):
    """Cria gráfico de período otimizado - MESMO PADRÃO DO DASH PRINCIPAL"""
    try:
        chart_data = df_data.groupby('Período')['Valor'].sum().reset_index()
        
        import altair as alt
        grafico_barras = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Período:N', title='Período'),
            y=alt.Y('Valor:Q', title='Soma do Valor'),
            color=alt.Color('Valor:Q', title='Valor', scale=alt.Scale(scheme='redyellowgreen', reverse=True)),
            tooltip=['Período:N', 'Valor:Q']
        ).properties(
            title='Total Accounts - Soma do Valor por Período',
            height=400
        )
        
        return grafico_barras
    except Exception as e:
        st.error(f"Erro ao criar gráfico de período: {e}")
        return None

# Gráfico por Type 05 (mesmo padrão do Dash.py)
@st.cache_data(ttl=900, max_entries=2)
def create_type05_chart_total_accounts(df_data):
    """Cria gráfico Type 05 otimizado - MESMO PADRÃO DO DASH PRINCIPAL"""
    try:
        
        # Verificar se as colunas existem
        if 'Type 05' not in df_data.columns:
            st.error("❌ Coluna 'Type 05' não encontrada!")
            return None
        if 'Valor' not in df_data.columns:
            st.error("❌ Coluna 'Valor' não encontrada!")
            return None
            
        type05_data = df_data.groupby('Type 05')['Valor'].sum().reset_index()
        type05_data = type05_data.sort_values('Valor', ascending=False)
        
        import altair as alt
        
        # Criar o gráfico
        chart = alt.Chart(type05_data).mark_bar().encode(
            x=alt.X('Type 05:N', title='Type 05', sort='-y'),
            y=alt.Y('Valor:Q', title='Soma do Valor'),
            color=alt.Color('Valor:Q', title='Valor', scale=alt.Scale(scheme='redyellowgreen', reverse=True))
        ).properties(
            title='Total Accounts - Soma do Valor por Type 05',
            height=400
        )
        
        return chart
    except Exception as e:
        st.error(f"Erro no gráfico Type 05: {e}")
        import traceback
        st.error(f"Traceback: {traceback.format_exc()}")
        return None

# Gráfico por Type 06 (mesmo padrão do Dash.py)
@st.cache_data(ttl=900, max_entries=2)
def create_type06_chart_total_accounts(df_data):
    """Cria gráfico Type 06 otimizado - MESMO PADRÃO DO DASH PRINCIPAL"""
    try:
        type06_data = df_data.groupby('Type 06')['Valor'].sum().reset_index()
        type06_data = type06_data.sort_values('Valor', ascending=False)
        
        import altair as alt
        
        # Criar o gráfico
        chart = alt.Chart(type06_data).mark_bar().encode(
            x=alt.X('Type 06:N', title='Type 06', sort='-y'),
            y=alt.Y('Valor:Q', title='Soma do Valor'),
            color=alt.Color('Valor:Q', title='Valor', scale=alt.Scale(scheme='redyellowgreen', reverse=True))
        ).properties(
            title='Total Accounts - Soma do Valor por Type 06',
            height=400
        )
        
        return chart
    except Exception as e:
        st.error(f"Erro no gráfico Type 06: {e}")
        return None

# Exibir gráficos em colunas
col1, col2 = st.columns(2)

with col1:
    # Gráfico principal por período
    grafico_periodo = create_period_chart_total_accounts(df_filtrado)
    if grafico_periodo:
        # Adicionar rótulos com valores nas barras
        import altair as alt
        rotulos = grafico_periodo.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black',
            fontSize=12
        ).encode(
            text=alt.Text('Valor:Q', format=',.2f')
        )
        
        grafico_completo = grafico_periodo + rotulos
        st.altair_chart(grafico_completo, use_container_width=True)

with col2:
    # Gráfico por Type 05
    if 'Type 05' in df_filtrado.columns:
        chart_type05 = create_type05_chart_total_accounts(df_filtrado)
        if chart_type05:
            st.altair_chart(chart_type05, use_container_width=True)

# Segunda linha de gráficos
col3, col4 = st.columns(2)

with col3:
    # Gráfico por Type 06
    if 'Type 06' in df_filtrado.columns:
        chart_type06 = create_type06_chart_total_accounts(df_filtrado)
        if chart_type06:
            st.altair_chart(chart_type06, use_container_width=True)

with col4:
    # Gráfico por USI (adicional)
    if 'USI' in df_filtrado.columns:
        @st.cache_data(ttl=900, max_entries=2)
        def create_usi_chart_total_accounts(df_data):
            """Cria gráfico USI otimizado"""
            try:
                usi_data = df_data.groupby('USI')['Valor'].sum().reset_index()
                usi_data = usi_data.sort_values('Valor', ascending=False)
                
                import altair as alt
                chart = alt.Chart(usi_data).mark_bar().encode(
                    x=alt.X('USI:N', title='USI', sort='-y'),
                    y=alt.Y('Valor:Q', title='Soma do Valor'),
                    color=alt.Color('Valor:Q', title='Valor', scale=alt.Scale(scheme='redyellowgreen', reverse=True)),
                    tooltip=['USI:N', 'Valor:Q']
                ).properties(
                    title='Total Accounts - Soma do Valor por USI',
                    height=400
                )
                
                return chart
            except Exception as e:
                st.error(f"Erro no gráfico USI: {e}")
                return None
        
        chart_usi = create_usi_chart_total_accounts(df_filtrado)
        if chart_usi:
            st.altair_chart(chart_usi, use_container_width=True)

st.markdown("---")

# Função para exportar uma única tabela para Excel
def exportar_excel(df, nome_arquivo):
    """Exporta DataFrame para Excel e retorna bytes para download"""
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=True, sheet_name='Dados')
    output.seek(0)
    return output.getvalue()

# Botão para download da tabela "Total SAP KE5Z - Todas as contas"
if st.button("📥 Baixar Total SAP KE5Z - Todas as contas (Excel)", use_container_width=True):
    with st.spinner("Gerando arquivo..."):
        # Criar a tabela pivot novamente para exportação (sem formatação de estilo)
        tabela_para_exportar = df_filtrado.pivot_table(index='Nº conta', columns='Período', values='Valor', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
        excel_data = exportar_excel(tabela_para_exportar, 'KE5Z_total_contas.xlsx')
        
        # Forçar download usando JavaScript
        import base64
        b64 = base64.b64encode(excel_data).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="KE5Z_total_contas.xlsx">💾 Clique aqui para baixar</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("✅ Arquivo gerado! Clique no link acima para baixar.")

# Resumo compacto
with st.sidebar.expander("📊 Resumo", expanded=False):
    st.write(f"**Registros:** {df_filtrado.shape[0]:,}")
    st.write(f"**Total:** R$ {df_filtrado['Valor'].sum():,.0f}")


# ================== NOVA TABELA: Soma por Type 05/06/07 (usa os MESMOS filtros) ==================

st.markdown("---")
st.subheader("📈 Soma dos Valores por Type 05, Type 06 e Type 07")

colunas_necessarias = {'Type 05', 'Type 06', 'Type 07', 'Valor'}
if colunas_necessarias.issubset(set(df_filtrado.columns)):
    tabela_types = (
        df_filtrado
        .groupby(['Type 05', 'Type 06', 'Type 07'], dropna=False)['Valor']
        .sum()
        .reset_index()
    )

    # Mostrar apenas linhas presentes após os filtros (evita zeros visuais)
    tabela_types = tabela_types[tabela_types['Valor'] != 0]

    # Ordenação simples para leitura
    tabela_types = tabela_types.sort_values(['Type 05', 'Type 06', 'Type 07'], na_position='last')

    # Exibição (mantém layout do app) com rolagem e zeros ocultos
    st.markdown(
        """
        <style>
        /* Habilitar rolagem vertical e horizontal para dataframes */
        div[data-testid="stDataFrame"] div[role="grid"]{max-height:420px;}
        div[data-testid="stDataFrame"] {overflow:auto !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(
        tabela_types.assign(**{'Valor': tabela_types['Valor'].round(2)}),
        use_container_width=True,
        height=420
    )

    # Download da tabela
    if st.button("📥 Baixar Soma por Types (Excel)", use_container_width=True):
        with st.spinner("Gerando arquivo..."):
            excel_data = exportar_excel(tabela_types, 'KE5Z_soma_types.xlsx')
            import base64
            b64 = base64.b64encode(excel_data).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="KE5Z_soma_types.xlsx">💾 Clique aqui para baixar</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("✅ Arquivo gerado! Clique no link acima para baixar.")
else:
    st.info("Colunas necessárias não disponíveis para esta tabela.")

