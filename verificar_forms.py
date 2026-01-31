"""
Script para verificar todos os formulários do projeto
e garantir que todos têm st.form_submit_button
"""
import os
import re

def verificar_forms_em_arquivo(caminho):
    """Verifica se todos os forms em um arquivo têm submit button"""
    with open(caminho, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Encontrar todos os st.form
    forms = re.finditer(r'with st\.form\([^)]*\):', conteudo)
    
    problemas = []
    for form in forms:
        inicio = form.start()
        # Pegar o nome do form
        form_name = form.group()
        
        # Encontrar o final do bloco with (próximo 'with' no mesmo nível de indentação ou fim)
        linhas = conteudo[:inicio].split('\n')
        linha_form = len(linhas)
        indentacao_form = len(linhas[-1]) - len(linhas[-1].lstrip())
        
        # Procurar por st.form_submit_button após este form
        resto_arquivo = conteudo[inicio:]
        linhas_resto = resto_arquivo.split('\n')
        
        # Procurar até encontrar próximo with no mesmo nível ou fim
        tem_submit = False
        for i, linha in enumerate(linhas_resto[1:], 1):
            # Checar indentação
            if linha.strip():
                indentacao_atual = len(linha) - len(linha.lstrip())
                
                # Se voltou ao nível do form ou menor, saiu do bloco
                if indentacao_atual <= indentacao_form:
                    break
                
                # Verificar se tem submit button
                if 'st.form_submit_button' in linha:
                    tem_submit = True
                    break
        
        if not tem_submit:
            problemas.append({
                'arquivo': caminho,
                'linha': linha_form,
                'form': form_name
            })
    
    return problemas

# Procurar em todos os arquivos .py
problemas_totais = []
for root, dirs, files in os.walk('.'):
    # Ignorar diretórios específicos
    if any(x in root for x in ['__pycache__', '.git', 'build', 'dist', 'venv', 'site-packages', '_internal']):
        continue
    
    for file in files:
        if file.endswith('.py'):
            caminho = os.path.join(root, file)
            problemas = verificar_forms_em_arquivo(caminho)
            problemas_totais.extend(problemas)

if problemas_totais:
    print("[AVISO] FORMULARIOS SEM SUBMIT BUTTON ENCONTRADOS:")
    print("=" * 60)
    for prob in problemas_totais:
        print(f"\n[Arquivo]: {prob['arquivo']}")
        print(f"[Linha]: {prob['linha']}")
        print(f"[Form]: {prob['form']}")
else:
    print("[OK] Todos os formularios tem submit button!")
    print("[OK] Nenhum problema encontrado!")
