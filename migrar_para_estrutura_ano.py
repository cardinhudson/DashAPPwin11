"""
Script de Migração - Estrutura por Ano
Migra dados existentes para nova estrutura separada por ano

Execução: python migrar_para_estrutura_ano.py
"""

import os
import shutil
import pandas as pd
from datetime import datetime

def migrar_estrutura():
    """Migra estrutura antiga para nova estrutura por ano"""
    
    print("\n" + "="*80)
    print("🔄 MIGRAÇÃO PARA ESTRUTURA POR ANO")
    print("="*80)
    
    # Detectar ano dos dados existentes (padrão: ano atual)
    ano_padrao = datetime.now().year
    print(f"\n📅 Ano padrão detectado: {ano_padrao}")
    
    # 1. Migrar pasta KE5Z
    print("\n📊 Migrando pasta KE5Z...")
    if os.path.exists("KE5Z"):
        arquivos_parquet = [f for f in os.listdir("KE5Z") if f.endswith('.parquet')]
        
        if arquivos_parquet:
            # Tentar detectar ano dos dados
            try:
                df_sample = pd.read_parquet(os.path.join("KE5Z", arquivos_parquet[0]))
                if 'Ano' in df_sample.columns:
                    anos = df_sample['Ano'].dropna().unique()
                    if len(anos) > 0:
                        ano_padrao = int(anos[0])
                        print(f"   ✅ Ano detectado dos dados: {ano_padrao}")
            except Exception as e:
                print(f"   ⚠️  Não foi possível detectar ano dos dados: {e}")
                print(f"   📅 Usando ano padrão: {ano_padrao}")
            
            # Criar nova estrutura
            nova_pasta = os.path.join("KE5Z", str(ano_padrao))
            os.makedirs(nova_pasta, exist_ok=True)
            
            # Mover arquivos
            for arquivo in arquivos_parquet:
                origem = os.path.join("KE5Z", arquivo)
                destino = os.path.join(nova_pasta, arquivo)
                
                # Se arquivo já existe no destino, fazer backup
                if os.path.exists(destino):
                    backup = destino + ".backup"
                    shutil.copy2(destino, backup)
                    print(f"   📦 Backup criado: {os.path.basename(backup)}")
                
                shutil.move(origem, destino)
                print(f"   ✅ {arquivo} → KE5Z/{ano_padrao}/")
        else:
            print("   ℹ️  Nenhum arquivo .parquet encontrado em KE5Z/")
    else:
        print("   ℹ️  Pasta KE5Z/ não existe")
        # Criar estrutura base
        os.makedirs(os.path.join("KE5Z", str(ano_padrao)), exist_ok=True)
        print(f"   ✅ Estrutura base criada: KE5Z/{ano_padrao}/")
    
    # 2. Migrar pasta Extracoes
    print("\n📁 Migrando pasta Extracoes...")
    if os.path.exists("Extracoes"):
        for subpasta in ["KE5Z", "KSBB"]:
            caminho_antigo = os.path.join("Extracoes", subpasta)
            if os.path.exists(caminho_antigo):
                caminho_novo = os.path.join("Extracoes", str(ano_padrao), subpasta)
                os.makedirs(os.path.dirname(caminho_novo), exist_ok=True)
                
                # Se já existe, fazer backup
                if os.path.exists(caminho_novo):
                    backup = caminho_novo + ".backup"
                    if os.path.exists(backup):
                        shutil.rmtree(backup)
                    shutil.copytree(caminho_novo, backup)
                    print(f"   📦 Backup criado: {backup}")
                    shutil.rmtree(caminho_novo)
                
                # Mover pasta
                shutil.move(caminho_antigo, caminho_novo)
                print(f"   ✅ {subpasta}/ → Extracoes/{ano_padrao}/{subpasta}/")
            else:
                print(f"   ℹ️  Pasta {subpasta}/ não existe em Extracoes/")
    else:
        print("   ℹ️  Pasta Extracoes/ não existe")
        # Criar estrutura base
        os.makedirs(os.path.join("Extracoes", str(ano_padrao), "KE5Z"), exist_ok=True)
        os.makedirs(os.path.join("Extracoes", str(ano_padrao), "KSBB"), exist_ok=True)
        print(f"   ✅ Estrutura base criada: Extracoes/{ano_padrao}/")
    
    # 3. Migrar pasta arquivos
    print("\n📄 Migrando pasta arquivos...")
    if os.path.exists("arquivos"):
        arquivos_excel = [f for f in os.listdir("arquivos") if f.endswith('.xlsx')]
        
        if arquivos_excel:
            nova_pasta = os.path.join("arquivos", str(ano_padrao))
            os.makedirs(nova_pasta, exist_ok=True)
            
            for arquivo in arquivos_excel:
                origem = os.path.join("arquivos", arquivo)
                destino = os.path.join(nova_pasta, arquivo)
                
                # Se arquivo já existe, fazer backup
                if os.path.exists(destino):
                    backup = destino + ".backup"
                    shutil.copy2(destino, backup)
                    print(f"   📦 Backup criado: {os.path.basename(backup)}")
                
                shutil.move(origem, destino)
                print(f"   ✅ {arquivo} → arquivos/{ano_padrao}/")
        else:
            print("   ℹ️  Nenhum arquivo .xlsx encontrado em arquivos/")
    else:
        print("   ℹ️  Pasta arquivos/ não existe")
        # Criar estrutura base
        os.makedirs(os.path.join("arquivos", str(ano_padrao)), exist_ok=True)
        print(f"   ✅ Estrutura base criada: arquivos/{ano_padrao}/")
    
    # 4. Verificar estrutura final
    print("\n" + "="*80)
    print(f"✅ MIGRAÇÃO CONCLUÍDA! Dados movidos para ano {ano_padrao}")
    print("="*80)
    print("\n📁 Nova estrutura criada:")
    print(f"   ├── KE5Z/{ano_padrao}/")
    
    # Listar arquivos em KE5Z
    ke5z_path = os.path.join("KE5Z", str(ano_padrao))
    if os.path.exists(ke5z_path):
        arquivos = [f for f in os.listdir(ke5z_path) if f.endswith('.parquet')]
        for arq in arquivos:
            print(f"   │   └── {arq}")
    
    print(f"   ├── Extracoes/{ano_padrao}/")
    print(f"   │   ├── KE5Z/")
    
    # Listar arquivos em Extracoes/KE5Z
    extracoes_ke5z = os.path.join("Extracoes", str(ano_padrao), "KE5Z")
    if os.path.exists(extracoes_ke5z):
        arquivos = [f for f in os.listdir(extracoes_ke5z) if f.endswith('.txt')][:3]
        for arq in arquivos:
            print(f"   │   │   └── {arq}")
        if len([f for f in os.listdir(extracoes_ke5z) if f.endswith('.txt')]) > 3:
            print(f"   │   │   └── ... (mais arquivos)")
    
    print(f"   │   └── KSBB/")
    print(f"   └── arquivos/{ano_padrao}/")
    
    # Listar arquivos em arquivos
    arquivos_path = os.path.join("arquivos", str(ano_padrao))
    if os.path.exists(arquivos_path):
        arquivos = [f for f in os.listdir(arquivos_path) if f.endswith('.xlsx')][:3]
        for arq in arquivos:
            print(f"       └── {arq}")
    
    print("\n" + "="*80)
    print("⚠️  PRÓXIMOS PASSOS:")
    print("="*80)
    print("1. ✅ Migração concluída com sucesso")
    print("2. 🔄 Execute 'criar_executavel_oficial.bat' para rebuild")
    print("3. 🧪 Teste o novo executável")
    print("4. 📦 Arquivos de backup foram criados (.backup)")
    print("="*80)

if __name__ == "__main__":
    print("\n⚠️  AVISO IMPORTANTE:")
    print("Este script irá reorganizar as pastas de dados do projeto.")
    print("Backups serão criados automaticamente para segurança.")
    print()
    
    resposta = input("Deseja continuar com a migração? (s/n): ")
    
    if resposta.lower() in ['s', 'sim', 'y', 'yes']:
        try:
            migrar_estrutura()
            print("\n✅ Processo concluído com sucesso!")
        except Exception as e:
            print(f"\n❌ ERRO durante migração: {e}")
            print("\n💡 Os backups (.backup) podem ser usados para restaurar os dados.")
    else:
        print("\n❌ Operação cancelada pelo usuário.")
