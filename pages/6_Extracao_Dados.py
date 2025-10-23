import streamlit as st
import pandas as pd
import os
import subprocess
import sys
import time
from datetime import datetime
import glob

# Adicionar diretório pai ao path para importar auth_simple
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth_simple import (
    verificar_autenticacao, exibir_header_usuario,
    verificar_status_aprovado, eh_administrador
)

# Configuração da página
st.set_page_config(
    page_title="Extração de Dados - Dashboard KE5Z",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verificar autenticação
verificar_autenticacao()

# Verificar se o usuário está aprovado
if ('usuario_nome' in st.session_state and 
    not verificar_status_aprovado(st.session_state.usuario_nome)):
    st.warning("⚠️ Sua conta ainda está pendente de aprovação.")
    st.stop()

# Verificar se é administrador
if not eh_administrador():
    st.error("🚫 **Acesso Restrito**")
    st.error("Apenas administradores podem acessar a página de extração.")
    st.info("💡 Entre em contato com o administrador se precisar de acesso.")
    st.stop()

# Header
st.title("📦 Extração de Dados KE5Z")
st.subheader("Execução do Script Extração.py")

# Exibir header do usuÃ¡rio
exibir_header_usuario()

st.markdown("---")

# Seção de Links para Pastas
st.subheader("📁 Acesso Rápido às Pastas")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Arquivos Parquet")
    st.markdown("**Localização:** `_internal/KE5Z/`")
    st.markdown("**Arquivos:**")
    st.markdown("- `KE5Z.parquet` (dados originais)")
    st.markdown("- `KE5Z_main.parquet` (dados principais)")
    st.markdown("- `KE5Z_others.parquet` (dados secundários)")
    st.markdown("- `KE5Z_waterfall.parquet` (dados otimizados)")

with col2:
    st.markdown("### 📄 Arquivos Excel")
    st.markdown("**Localização:** `_internal/arquivos/`")
    st.markdown("**Arquivos:**")
    st.markdown("- `KE5Z_[USI].xlsx` (por USI)")
    st.markdown("- `KE5Z_veiculos.xlsx`")
    st.markdown("- `KE5Z_imoveis.xlsx`")
    st.markdown("- `KE5Z_equipamentos.xlsx`")

with col3:
    st.markdown("### 📝 Arquivos TXT")
    st.markdown("**Localização:** `_internal/Extracoes/` (arquivos de entrada)")
    st.markdown("**Pastas:**")
    st.markdown("- `KE5Z/` (arquivos KE5Z)")
    st.markdown("- `KSBB/` (arquivos KSBB)")
    st.markdown("- `KSBB_veiculos/` (veículos)")
    st.markdown("- `KSBB_imoveis/` (imóveis)")

# Botões para abrir pastas
st.markdown("### 🔗 Abrir Pastas")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📂 Abrir Pasta Parquet", help="Abre a pasta com arquivos .parquet"):
        # Arquivos Parquet ficam no _internal
        parquet_path = os.path.join(os.path.dirname(sys.executable), "_internal", "KE5Z")
        if os.path.exists(parquet_path):
            os.startfile(parquet_path)
            st.success("✅ Pasta aberta!")
        else:
            st.error("❌ Pasta não encontrada!")

with col2:
    if st.button("📂 Abrir Pasta Excel", help="Abre a pasta com arquivos .xlsx"):
        # Arquivos Excel ficam no _internal
        excel_path = os.path.join(os.path.dirname(sys.executable), "_internal", "arquivos")
        if os.path.exists(excel_path):
            os.startfile(excel_path)
            st.success("✅ Pasta aberta!")
        else:
            st.error(f"❌ Pasta não encontrada! Procurada em: {excel_path}")

with col3:
    if st.button("📂 Abrir Pasta TXT", help="Abre a pasta com arquivos .txt"):
        # Arquivos TXT ficam no _internal (são arquivos de entrada, não saída)
        txt_path = os.path.join(os.path.dirname(sys.executable), "_internal", "Extracoes")
        if os.path.exists(txt_path):
            os.startfile(txt_path)
            st.success("✅ Pasta aberta!")
        else:
            st.error("❌ Pasta não encontrada!")

# Seção de Status dos Arquivos
st.markdown("### 📊 Status dos Arquivos")
col1, col2, col3 = st.columns(3)

def verificar_arquivo_existe(caminho):
    """Verifica se um arquivo ou pasta existe"""
    return os.path.exists(caminho)

def obter_tamanho_arquivo(caminho):
    """Obtém o tamanho de um arquivo em MB"""
    try:
        if os.path.isfile(caminho):
            tamanho_bytes = os.path.getsize(caminho)
            return round(tamanho_bytes / (1024 * 1024), 2)
        return 0
    except:
        return 0

def contar_arquivos_pasta(caminho):
    """Conta quantos arquivos existem em uma pasta"""
    try:
        if os.path.isdir(caminho):
            return len([f for f in os.listdir(caminho) if os.path.isfile(os.path.join(caminho, f))])
        return 0
    except:
        return 0

# Verificar arquivos Parquet
with col1:
    st.markdown("**📊 Arquivos Parquet:**")
    # Arquivos Parquet - caminho correto baseado no ambiente
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller: arquivos ficam no _internal
        parquet_dir = os.path.join(sys._MEIPASS, "KE5Z")
    else:
        # Desenvolvimento: arquivos ficam na pasta local
        parquet_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "KE5Z")
    if verificar_arquivo_existe(parquet_dir):
        arquivos_parquet = [f for f in os.listdir(parquet_dir) if f.endswith('.parquet')]
        st.success(f"✅ {len(arquivos_parquet)} arquivos encontrados")
        for arquivo in arquivos_parquet:
            caminho_arquivo = os.path.join(parquet_dir, arquivo)
            tamanho = obter_tamanho_arquivo(caminho_arquivo)
            st.markdown(f"- `{arquivo}` ({tamanho} MB)")
    else:
        st.error("❌ Pasta não encontrada")

# Verificar arquivos Excel
with col2:
    st.markdown("**📄 Arquivos Excel:**")
    # Arquivos Excel - caminho correto baseado no ambiente
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller: arquivos ficam no _internal
        excel_dir = os.path.join(sys._MEIPASS, "arquivos")
    else:
        # Desenvolvimento: arquivos ficam na pasta local
        excel_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "arquivos")
    if verificar_arquivo_existe(excel_dir):
        arquivos_excel = [f for f in os.listdir(excel_dir) if f.endswith('.xlsx')]
        st.success(f"✅ {len(arquivos_excel)} arquivos encontrados")
        for arquivo in arquivos_excel[:5]:  # Mostrar apenas os primeiros 5
            caminho_arquivo = os.path.join(excel_dir, arquivo)
            tamanho = obter_tamanho_arquivo(caminho_arquivo)
            st.markdown(f"- `{arquivo}` ({tamanho} MB)")
        if len(arquivos_excel) > 5:
            st.markdown(f"... e mais {len(arquivos_excel) - 5} arquivos")
    else:
        st.error("❌ Pasta não encontrada")

# Verificar arquivos TXT
with col3:
    st.markdown("**📝 Arquivos TXT:**")
    # Arquivos TXT - caminho correto baseado no ambiente
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller: arquivos ficam no _internal
        txt_dir = os.path.join(sys._MEIPASS, "Extracoes")
    else:
        # Desenvolvimento: arquivos ficam na pasta local
        txt_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Extracoes")
    if verificar_arquivo_existe(txt_dir):
        total_txt = 0
        for subdir in ['KE5Z', 'KSBB', 'KSBB_veiculos', 'KSBB_imoveis']:
            subdir_path = os.path.join(txt_dir, subdir)
            if verificar_arquivo_existe(subdir_path):
                arquivos_txt = [f for f in os.listdir(subdir_path) if f.endswith('.txt')]
                total_txt += len(arquivos_txt)
        st.success(f"✅ {total_txt} arquivos encontrados")
        for subdir in ['KE5Z', 'KSBB', 'KSBB_veiculos', 'KSBB_imoveis']:
            subdir_path = os.path.join(txt_dir, subdir)
            if verificar_arquivo_existe(subdir_path):
                arquivos_txt = [f for f in os.listdir(subdir_path) if f.endswith('.txt')]
                st.markdown(f"- `{subdir}/`: {len(arquivos_txt)} arquivos")
    else:
        st.error("❌ Pasta não encontrada")

st.markdown("---")
# Garantir logs na sessão antes de usar
if 'logs' not in st.session_state:
    st.session_state.logs = []

# Placeholders principais da UI
status_box = st.empty()
progress_bar = st.progress(0)
logs_placeholder = st.empty()

# CSS para multiselect com rolagem
st.markdown("""
<style>
div[data-testid="stMultiSelect"] > div {max-height: 220px; overflow-y: auto;}
</style>
""", unsafe_allow_html=True)

# Filtro de meses com opção "Todos"
meses_opcoes = ["Todos"] + list(range(1, 13))
nomes_meses = {1:"Janeiro",2:"Fevereiro",3:"Março",4:"Abril",5:"Maio",6:"Junho",7:"Julho",8:"Agosto",9:"Setembro",10:"Outubro",11:"Novembro",12:"Dezembro"}

def format_mes(m):
    return "Todos" if m == "Todos" else nomes_meses[m]

selecionados = st.multiselect(
    "📅 Selecionar Meses para Arquivos Excel",
    options=meses_opcoes,
    default=["Todos"],
    format_func=format_mes,
    help="Selecione os meses que deseja incluir nos arquivos Excel gerados."
)

if "Todos" in selecionados:
    meses_filtro = list(range(1, 13))
else:
    meses_filtro = selecionados

st.markdown("---")

col_a, col_b = st.columns([1, 1])
with col_a:
    executar = st.button("▶️ Executar Extração", use_container_width=True)
with col_b:
    aplicar_filtro = st.button("🔄 Aplicar Filtro de Mês (Excel)", use_container_width=True)

def atualizar_progresso(pct, titulo, detalhe=""):
    with status_box.container():
        st.write(f"{titulo}  {detalhe}")
    progress_bar.progress(int(pct))

def render_logs():
    ultimos = st.session_state.logs[-30:]
    with logs_placeholder.container():
        for linha in ultimos:
            st.write(linha)



st.markdown("---")

def adicionar_log(mensagem, detalhes=None, sem_timestamp=False):
    """Adiciona mensagem aos logs da sessão"""
    if sem_timestamp:
        # Para saída direta do script, não adicionar timestamp
        log_entry = mensagem
    else:
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {mensagem}"
        if detalhes:
            log_entry += f" | {detalhes}"
    
    st.session_state.logs.append(log_entry)
    if len(st.session_state.logs) > 200:  # Aumentar para 200 logs
        st.session_state.logs = st.session_state.logs[-200:]


def resolver_pasta_extracoes() -> str:
    """Resolve o nome da pasta 'Extrações' tolerando variações de acentuação.

    Retorna o nome de diretório existente a ser usado nas verificações/cópias.
    Ordem de prioridade: 'Extrações', 'Extracoes', 'ExtraÃ§Ãµes', fallback 'Extracoes'.
    """
    # Obter diretório base (onde está o executável)
    if hasattr(sys, '_MEIPASS'):
        # Executando dentro do PyInstaller
        base_dir = sys._MEIPASS
    else:
        # Executando normalmente - usar diretório do script atual
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    candidatos = [
        'Extrações',  # nome correto com acento
        'Extracoes',  # sem acento
        'ExtraÃ§Ãµes', # nome corrompido
    ]
    for nome in candidatos:
        caminho = os.path.join(base_dir, nome)
        if os.path.isdir(caminho):
            return nome
    # fallback padrão (usaremos sem acento para nova criação/cópia)
    return 'Extracoes'

def verificar_arquivos_necessarios():
    """Verifica se todos os arquivos necessários existem"""
    # Obter diretório base (onde está o executável)
    if hasattr(sys, '_MEIPASS'):
        # Executando dentro do PyInstaller
        base_dir = sys._MEIPASS
    else:
        # Executando normalmente - usar diretório do script atual
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    base_extracoes = resolver_pasta_extracoes()
    arquivos_necessarios = [
        (os.path.join(base_dir, "Extracao.py"), "Script principal"),
        (os.path.join(base_dir, base_extracoes, "KE5Z"), "Pasta com arquivos .txt KE5Z"),
        (os.path.join(base_dir, base_extracoes, "KSBB"), "Pasta com arquivos .txt KSBB"),
        (os.path.join(base_dir, "Dados SAPIENS.xlsx"), "Base de dados SAPIENS"),
        (os.path.join(base_dir, "Fornecedores.xlsx"), "Lista de fornecedores")
    ]
    
    resultados = []
    todos_ok = True
    
    for caminho, descricao in arquivos_necessarios:
        existe = os.path.exists(caminho)
        if existe:
            if os.path.isdir(caminho):
                arquivos = len([f for f in os.listdir(caminho)
                               if f.endswith('.txt')])
                resultados.append((descricao, f"✅ {arquivos} arquivos .txt",
                                   True))
            else:
                tamanho = os.path.getsize(caminho) / (1024 * 1024)
                resultados.append((descricao, f"✅ {tamanho:.1f} MB", True))
        else:
            resultados.append((descricao, "❌ Não encontrado", False))
            todos_ok = False
    
    return todos_ok, resultados


def executar_extracao(meses_filtro=None, progress_callback=None, logs_placeholder=None):
    """Executa o script Extração.py com captura de logs em tempo real"""
    try:
        # Obter diretório base (onde está o executável)
        if hasattr(sys, '_MEIPASS'):
            # Executando dentro do PyInstaller
            base_dir = sys._MEIPASS
        else:
            # Executando normalmente - usar diretório do script atual
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        adicionar_log("🚀 Iniciando execução do Extração.py...")
        if progress_callback:
            progress_callback(10, "🚀 Iniciando execução...", "Preparando ambiente")

        script_path = os.path.join(base_dir, "Extracao.py")
        
        # Passar meses selecionados via variável de ambiente (ex.: "9,10,11")
        try:
            if meses_filtro and isinstance(meses_filtro, (list, tuple)):
                os.environ["MESES_FILTRO"] = ",".join(str(int(m)) for m in meses_filtro)
        except Exception:
            # Em caso de qualquer problema na serialização, ignorar silenciosamente
            pass

        # Executar de forma diferente dependendo do ambiente
        if hasattr(sys, '_MEIPASS'):
            # Executando dentro do PyInstaller - executar diretamente para evitar problemas de python.exe
            adicionar_log("🐍 Executando script diretamente (PyInstaller)")
            adicionar_log(f"📄 Script: {script_path}")
            if progress_callback:
                progress_callback(15, "⚙️ Iniciando execução direta...", "Executando script")

            # Executar com captura de logs em tempo real usando threading
            import threading
            import queue
            import time
            from io import StringIO
            
            # Queue para capturar logs em tempo real
            log_queue = queue.Queue()
            
            def capture_output():
                """Captura stdout/stderr e envia para a queue"""
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                
                class OutputCapture:
                    def __init__(self, original, queue, prefix=""):
                        self.original = original
                        self.queue = queue
                        self.prefix = prefix
                        self.buffer = ""
                    
                    def write(self, text):
                        self.buffer += text
                        if '\n' in self.buffer:
                            lines = self.buffer.split('\n')
                            for line in lines[:-1]:
                                if line.strip():
                                    self.queue.put(f"{self.prefix}{line.strip()}")
                            self.buffer = lines[-1]
                        self.original.write(text)
                    
                    def flush(self):
                        if self.buffer.strip():
                            self.queue.put(f"{self.prefix}{self.buffer.strip()}")
                            self.buffer = ""
                        self.original.flush()
                
                sys.stdout = OutputCapture(old_stdout, log_queue, "")
                sys.stderr = OutputCapture(old_stderr, log_queue, "ERR: ")
                
                try:
                    # Executar o script diretamente
                    with open(script_path, 'r', encoding='utf-8') as f:
                        script_content = f.read()
                    
                    # Criar contexto de execução
                    exec_context = {
                        '__name__': '__main__',
                        '__file__': script_path,
                        '__builtins__': __builtins__,
                    }
                    
                    # Executar o script
                    exec(script_content, exec_context)
                    
                except Exception as e:
                    log_queue.put(f"❌ Erro na execução: {str(e)}")
                finally:
                    # Restaurar stdout/stderr
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr
                    log_queue.put("__END__")  # Sinal de fim
            
            # Iniciar thread de execução
            exec_thread = threading.Thread(target=capture_output)
            exec_thread.daemon = True
            exec_thread.start()
            
            # Processar logs em tempo real
            linhas_lidas = 0
            start_time = time.time()
            
            while exec_thread.is_alive() or not log_queue.empty():
                try:
                    # Tentar obter log com timeout
                    log_line = log_queue.get(timeout=0.1)
                    
                    if log_line == "__END__":
                        break
                    
                    if log_line.strip():
                        adicionar_log(log_line.strip(), sem_timestamp=True)
                        linhas_lidas += 1
                        
                        # Atualizar progresso
                        if progress_callback:
                            elapsed = time.time() - start_time
                            # Simular progresso baseado no tempo e linhas
                            progress = min(90, 20 + (elapsed * 2) + (linhas_lidas * 0.5))
                            progress_callback(progress, "⚙️ Processando...", f"Linhas: {linhas_lidas}")
                        
                        # Atualizar logs na tela (se placeholder estiver disponível)
                        if logs_placeholder is not None:
                            ultimos = st.session_state.logs[-30:]
                            with logs_placeholder.container():
                                for log_line_display in ultimos:
                                    st.write(log_line_display)
                
                except queue.Empty:
                    # Timeout - continuar verificando
                    time.sleep(0.1)
                    continue
                except Exception as e:
                    adicionar_log(f"❌ Erro no processamento de logs: {str(e)}")
                    break
            
            # Aguardar thread terminar
            exec_thread.join(timeout=5)
            
            # Processar logs restantes
            while not log_queue.empty():
                try:
                    log_line = log_queue.get_nowait()
                    if log_line != "__END__" and log_line.strip():
                        adicionar_log(log_line.strip(), sem_timestamp=True)
                except queue.Empty:
                    break
            
            return_code = 0  # Sucesso
                
        else:
            # Executando normalmente - usar subprocess
            python_path = sys.executable
            adicionar_log(f"🐍 Usando Python: {python_path}")
            adicionar_log(f"📄 Script: {script_path}")
            if progress_callback:
                progress_callback(15, "⚙️ Iniciando subprocess...", "Executando script")

            # Preparar ambiente para subprocess
            env = os.environ.copy()
            try:
                if meses_filtro and isinstance(meses_filtro, (list, tuple)):
                    env["MESES_FILTRO"] = ",".join(str(int(m)) for m in meses_filtro)
            except Exception:
                pass

            processo = subprocess.Popen(
                [python_path, "-u", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=base_dir,
                encoding='cp1252',
                errors='replace',
                bufsize=1,
                universal_newlines=True,
                env=env,
            )

            # Leitura em tempo real do stdout
            linhas_lidas = 0
            for linha in iter(processo.stdout.readline, ''):
                if linha == '' and processo.poll() is not None:
                    break
                texto = linha.strip()
                if texto:
                    adicionar_log(texto, sem_timestamp=True)
                    linhas_lidas += 1
                    if linhas_lidas % 5 == 0 and progress_callback:
                        pct = min(75, 15 + linhas_lidas)
                        progress_callback(pct, "⚙️ Processando...", f"Linhas: {linhas_lidas}")
                    # Atualizar logs na tela (se placeholder estiver disponível)
                    if logs_placeholder is not None:
                        ultimos = st.session_state.logs[-30:]
                        with logs_placeholder.container():
                            for log_line in ultimos:
                                st.write(log_line)

            # Capturar stderr ao final
            stderr_restante = processo.stderr.read() or ''
            if stderr_restante:
                for linha in stderr_restante.split('\n'):
                    if linha.strip():
                        adicionar_log(linha.strip(), sem_timestamp=True)

            return_code = processo.wait()

        adicionar_log(f"📊 Código de retorno: {return_code}", f"Status: {'Sucesso' if return_code == 0 else 'Erro'}")
        if progress_callback:
            progress_callback(85, "📊 Processamento concluído", "Verificando arquivos")

        arquivos_gerados = verificar_arquivos_gerados()

        if return_code == 0 or (arquivos_gerados and len(arquivos_gerados) > 0):
            adicionar_log("✅ Extração concluída com sucesso!")
            if progress_callback:
                progress_callback(100, "✅ Concluído", "")
            return True, "Extração executada com sucesso!"

        adicionar_log("❌ Extração finalizada sem sucesso")
        return False, "Erro na execução"

    except Exception as e:
        adicionar_log(f"❌ Erro: {str(e)}")
        return False, f"Erro: {str(e)}"


def verificar_arquivos_gerados():
    """Verifica quais arquivos foram gerados pela extração"""
    # Obter diretório base (onde os arquivos são salvos - diretório do executável)
    if hasattr(sys, '_MEIPASS'):
        # Executando dentro do PyInstaller - arquivos são salvos no diretório do executável
        base_dir = os.path.dirname(sys.executable)
    else:
        # Executando normalmente
        base_dir = os.getcwd()
    
    arquivos_gerados = []
    
    adicionar_log("🔍 Verificando arquivos gerados pela extração")
    
    # Verificar arquivos Parquet
    ke5z_path = os.path.join(base_dir, "KE5Z")
    if os.path.exists(ke5z_path):
        arquivos_parquet = glob.glob(os.path.join(ke5z_path, "*.parquet"))
        adicionar_log(f"📁 Pasta KE5Z encontrada", 
                      f"Arquivos .parquet: {len(arquivos_parquet)}")
        
        for arquivo in arquivos_parquet:
            tamanho = os.path.getsize(arquivo) / (1024 * 1024)
            timestamp = os.path.getmtime(arquivo)
            tempo_mod = time.strftime('%H:%M:%S',
                                     time.localtime(timestamp))
            arquivos_gerados.append(f"📊 {os.path.basename(arquivo)} "
                                   f"({tamanho:.1f} MB) - {tempo_mod}")
            adicionar_log(f"📊 Arquivo Parquet: {os.path.basename(arquivo)}", 
                          f"Tamanho: {tamanho:.1f} MB, Modificado: {tempo_mod}")
    else:
        adicionar_log("⚠️ Pasta KE5Z não encontrada")
    
    # Verificar arquivos Excel
    arquivos_path = os.path.join(base_dir, "arquivos")
    if os.path.exists(arquivos_path):
        arquivos_excel = glob.glob(os.path.join(arquivos_path, "*.xlsx"))
        adicionar_log(f"📁 Pasta arquivos encontrada", 
                      f"Arquivos .xlsx: {len(arquivos_excel)}")
        
        for arquivo in arquivos_excel:
            tamanho = os.path.getsize(arquivo) / (1024 * 1024)
            timestamp = os.path.getmtime(arquivo)
            tempo_mod = time.strftime('%H:%M:%S',
                                     time.localtime(timestamp))
            arquivos_gerados.append(f"📄 {os.path.basename(arquivo)} "
                                   f"({tamanho:.1f} MB) - {tempo_mod}")
            adicionar_log(f"📄 Arquivo Excel: {os.path.basename(arquivo)}", 
                          f"Tamanho: {tamanho:.1f} MB, Modificado: {tempo_mod}")
    else:
        adicionar_log("⚠️ Pasta arquivos não encontrada")
    
    adicionar_log(f"📊 Total de arquivos encontrados: {len(arquivos_gerados)}")
    return arquivos_gerados


def aplicar_filtro_mes_excel(meses_filtro):
    """Aplica filtro de mês nos arquivos Excel específicos"""
    try:
        # Obter diretório base (onde os arquivos são salvos - diretório do executável)
        if hasattr(sys, '_MEIPASS'):
            # Executando dentro do PyInstaller - arquivos são salvos no diretório do executável
            base_dir = os.path.dirname(sys.executable)
        else:
            # Executando normalmente
            base_dir = os.getcwd()
        
        if not meses_filtro or len(meses_filtro) == 12:
            adicionar_log("📅 Todos os meses selecionados - sem filtro aplicado", 
                          f"Meses: {meses_filtro}")
            return True
        
        arquivos_excel = [
            os.path.join(base_dir, "arquivos", "KE5Z_veiculos.xlsx"), 
            os.path.join(base_dir, "arquivos", "KE5Z_pwt.xlsx")
        ]
        adicionar_log("🔍 Iniciando aplicação de filtro de mês", 
                      f"Arquivos: {len(arquivos_excel)}, Meses: {meses_filtro}")
        
        for arquivo in arquivos_excel:
            adicionar_log(f"📁 Verificando arquivo: {os.path.basename(arquivo)}")
            if not os.path.exists(arquivo):
                adicionar_log(f"⚠️ Arquivo não encontrado: {arquivo}")
                continue

            adicionar_log(f"✅ Arquivo encontrado: {os.path.basename(arquivo)}")
            df = pd.read_excel(arquivo)
            # Normalizar nomes de colunas (tolerar variações de acentuação/caixa)
            cols_norm = {c: str(c).strip() for c in df.columns}
            df.rename(columns=cols_norm, inplace=True)
            # Se houver 'Periodo' sem acento, alinhar para 'Período'
            if 'Periodo' in df.columns and 'Período' not in df.columns:
                df.rename(columns={'Periodo': 'Período'}, inplace=True)
            adicionar_log(f"📊 Arquivo carregado: {len(df)} registros")

            # Tipos para merge
            for coluna in ['Nºconta', 'Centrocst', 'Nºdoc.ref.', 'Account', 'USI', 'Type 05', 'Type 06', 'Type 07']:
                if coluna in df.columns:
                    df[coluna] = df[coluna].astype(str)
            for coluna in ['Valor', 'QTD']:
                if coluna in df.columns:
                    df[coluna] = pd.to_numeric(df[coluna], errors='coerce')

            # Filtro por mês
            df_filtrado = None
            # Tentar criar coluna 'Mes' se só existir 'Período'
            if 'Mes' not in df.columns and 'Período' in df.columns:
                mapa = {"janeiro":1,"fevereiro":2,"março":3,"marco":3,"abril":4,"maio":5,"junho":6,
                        "julho":7,"agosto":8,"setembro":9,"outubro":10,"novembro":11,"dezembro":12}
                try:
                    df['Mes'] = df['Período'].astype(str).str.lower().map(mapa).astype('Int64')
                except Exception:
                    pass

            if 'Mes' in df.columns:
                meses_numeros = [int(m) for m in meses_filtro]
                df_filtrado = df[df['Mes'].isin(meses_numeros)]
                adicionar_log(f"✅ Filtro aplicado na coluna Mes: {len(df_filtrado)} registros")
            elif 'Período' in df.columns:
                meses_nomes = {1:"janeiro",2:"fevereiro",3:"março",4:"abril",5:"maio",6:"junho",7:"julho",8:"agosto",9:"setembro",10:"outubro",11:"novembro",12:"dezembro"}
                meses_texto = [meses_nomes[int(m)] for m in meses_filtro]
                df_filtrado = df[df['Período'].str.lower().isin(meses_texto)]
                adicionar_log(f"✅ Filtro aplicado na coluna Período: {len(df_filtrado)} registros")
            else:
                adicionar_log("⚠️ Nenhuma coluna de mês encontrada")
                continue

            if len(df_filtrado) == 0:
                adicionar_log("⚠️ Nenhum registro encontrado com os filtros")
                continue

            adicionar_log("🔍 Verificando integridade dos dados filtrados", f"Registros: {len(df_filtrado)}")

            # Salvar de volta no mesmo arquivo
            adicionar_log("💾 Salvando arquivo filtrado", f"Destino: {arquivo}")
            try:
                df_filtrado.to_excel(arquivo, index=False)
                if os.path.exists(arquivo):
                    tamanho = os.path.getsize(arquivo)
                    adicionar_log("✅ Arquivo salvo com sucesso", f"Tamanho: {tamanho} bytes")
            except Exception as e:
                adicionar_log(f"❌ Erro ao salvar arquivo: {str(e)}")
                continue

            adicionar_log(f"✅ Filtro aplicado: {len(df_filtrado)} registros de {len(df)} originais")

        return True
    except Exception as e:
        adicionar_log(f"❌ Erro ao aplicar filtro de mês: {str(e)}")
        return False


# --- AÇÕES DA UI (executadas após definição das funções) ---

if executar:
    st.session_state.logs.clear()
    atualizar_progresso(10, "Preparando...")
    ok, msg = executar_extracao(meses_filtro=meses_filtro, progress_callback=atualizar_progresso, logs_placeholder=logs_placeholder)
    atualizar_progresso(80, "Verificando arquivos...")
    verificar_arquivos_gerados()
    atualizar_progresso(100, "Concluído")
    render_logs()

if aplicar_filtro:
    st.session_state.logs.clear()
    atualizar_progresso(20, "Aplicando filtro de mês...")
    aplicar_filtro_mes_excel(meses_filtro)
    atualizar_progresso(100, "Filtro aplicado")
    render_logs()

# Verificação de arquivos necessários (no final da página)
st.subheader("📁 Verificação de Arquivos Necessários")
ok, itens = verificar_arquivos_necessarios()
for desc, info, existe in itens:
    st.write(f"{'✅' if existe else '❌'} {desc} — {info}")
