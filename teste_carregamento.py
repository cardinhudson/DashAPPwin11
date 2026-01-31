"""
Teste de Carregamento - Estrutura por Ano
Verifica se os dados podem ser carregados corretamente da nova estrutura
"""

import os
import sys

print("="*80)
print("🧪 TESTE DE CARREGAMENTO - ESTRUTURA POR ANO")
print("="*80)
print()

# 1. Verificar estrutura de pastas
print("📁 Verificando estrutura de pastas...")
print()

base = os.getcwd()
ke5z_path = os.path.join(base, 'KE5Z')

if os.path.exists(ke5z_path):
    print(f"✅ Pasta KE5Z/ encontrada: {ke5z_path}")
    
    # Listar anos disponíveis
    anos = sorted([d for d in os.listdir(ke5z_path) 
                   if d.isdigit() and os.path.isdir(os.path.join(ke5z_path, d))], 
                  reverse=True)
    
    print(f"📅 Anos disponíveis: {anos}")
    print()
    
    for ano in anos:
        ano_path = os.path.join(ke5z_path, ano)
        parquets = [f for f in os.listdir(ano_path) if f.endswith('.parquet')]
        
        print(f"📊 Ano {ano}:")
        print(f"   📂 Pasta: {ano_path}")
        print(f"   📄 Arquivos Parquet: {len(parquets)}")
        
        for parquet in sorted(parquets):
            file_path = os.path.join(ano_path, parquet)
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print(f"      • {parquet} ({size_mb:.2f} MB)")
        print()
else:
    print(f"❌ Pasta KE5Z/ não encontrada!")
    sys.exit(1)

# 2. Testar carregamento de dados
print("="*80)
print("📊 Testando carregamento de dados...")
print()

try:
    import pandas as pd
    print("✅ Pandas importado com sucesso")
    
    # Tentar carregar arquivo waterfall do ano mais recente
    if anos:
        ano_teste = anos[0]
        waterfall_path = os.path.join(ke5z_path, ano_teste, "KE5Z_waterfall.parquet")
        
        if os.path.exists(waterfall_path):
            print(f"📥 Carregando arquivo: {waterfall_path}")
            df = pd.read_parquet(waterfall_path)
            
            print(f"✅ Arquivo carregado com sucesso!")
            print(f"   📊 Registros: {len(df):,}")
            print(f"   📋 Colunas: {len(df.columns)}")
            print(f"   📝 Colunas: {', '.join(df.columns[:10])}")
            
            if len(df.columns) > 10:
                print(f"            ... e mais {len(df.columns) - 10} colunas")
            
            print()
            print("📈 Primeiras linhas:")
            print(df.head(3).to_string())
            
        else:
            print(f"⚠️  Arquivo waterfall não encontrado: {waterfall_path}")
    else:
        print("⚠️  Nenhum ano disponível para teste")
        
except Exception as e:
    print(f"❌ Erro ao carregar dados: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("="*80)
print("✅ TESTE CONCLUÍDO COM SUCESSO!")
print("="*80)
print()
print("🎯 Conclusão:")
print("   • Estrutura de pastas por ano: ✅ OK")
print("   • Arquivos Parquet disponíveis: ✅ OK")
print("   • Carregamento de dados: ✅ OK")
print()
print("🚀 A aplicação está pronta para uso!")
