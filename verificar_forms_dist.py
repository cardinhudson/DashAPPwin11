"""
Script para verificar formulários no executável
"""
import re
import os

def verificar_forms_em_arquivo(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8', errors='ignore') as f:
            conteudo = f.read()
    except:
        return []
    
    forms = list(re.finditer(r'with st\.form\([^)]*\):', conteudo))
    
    problemas = []
    for form in forms:
        inicio = form.start()
        form_name = form.group()
        
        linhas = conteudo[:inicio].split('\n')
        linha_form = len(linhas)
        indentacao_form = len(linhas[-1]) - len(linhas[-1].lstrip())
        
        resto_arquivo = conteudo[inicio:]
        linhas_resto = resto_arquivo.split('\n')
        
        tem_submit = False
        for i, linha in enumerate(linhas_resto[1:], 1):
            if linha.strip():
                indentacao_atual = len(linha) - len(linha.lstrip())
                if indentacao_atual <= indentacao_form:
                    break
                if 'form_submit_button' in linha:
                    tem_submit = True
                    break
        
        if not tem_submit:
            problemas.append({
                'arquivo': caminho,
                'linha': linha_form,
                'form': form_name
            })
    
    return problemas

# Verificar na pasta dist - apenas arquivos do projeto
problemas = []
arquivos_projeto = ['app.py', 'auth_simple.py', 'Extracao.py']
pastas_projeto = ['pages']

for root, dirs, files in os.walk('dist/Dashboard_KE5Z_OFICIAL/_internal'):
    # Ignorar pycache e bibliotecas
    if '__pycache__' in root or 'streamlit' in root or 'site-packages' in root:
        continue
    
    # Verificar apenas arquivos do projeto
    for f in files:
        if f.endswith('.py'):
            # Verificar se é arquivo do projeto ou está na pasta pages
            is_projeto = f in arquivos_projeto or 'pages' in root
            if is_projeto:
                probs = verificar_forms_em_arquivo(os.path.join(root, f))
                problemas.extend(probs)

if problemas:
    print('PROBLEMAS ENCONTRADOS:')
    for p in problemas:
        print(f"  Arquivo: {p['arquivo']}")
        print(f"  Linha: {p['linha']}")
        print(f"  Form: {p['form']}")
        print()
else:
    print('OK - Todos os forms tem submit button')
