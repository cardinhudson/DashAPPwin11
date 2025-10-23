"""
Hook personalizado para PyInstaller + Streamlit
Resolve o erro: "No package metadata was found for streamlit"
"""
from PyInstaller.utils.hooks import copy_metadata, collect_data_files, collect_submodules

# Coletar metadados do Streamlit (ESSENCIAL para resolver o erro)
datas = copy_metadata('streamlit')

# Coletar todos os arquivos de dados do Streamlit
datas += collect_data_files('streamlit')

# Coletar todos os submódulos do Streamlit
hiddenimports = collect_submodules('streamlit')
hiddenimports += [
    'streamlit.web.cli',
    'streamlit.runtime',
    'streamlit.runtime.scriptrunner',
    'streamlit.runtime.scriptrunner.script_runner',
    'streamlit.runtime.state',
    'streamlit.runtime.legacy_caching',
    'streamlit.elements',
    'streamlit.logger',
    'altair',
    'validators',
    'watchdog',
    'tornado',
    'click',
]

