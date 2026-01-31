#!/usr/bin/env python3
"""
Script de teste para validar a detecção de coluna Material em arquivos KSBB
Testa sem precisar gerar o executável
"""

import pandas as pd
import os
import sys
import unicodedata

# Adicionar o diretório atual ao path para importar funções
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar a função de padronização do Extracao.py
from Extracao import padronizar_colunas

def testar_arquivo_ksbb(caminho_arquivo):
    """Testa a detecção de Material em um arquivo KSBB específico"""
    print(f"\n{'='*70}")
    print(f"TESTANDO: {os.path.basename(caminho_arquivo)}")
    print(f"{'='*70}")
    
    if not os.path.exists(caminho_arquivo):
        print(f"❌ Arquivo não encontrado: {caminho_arquivo}")
        return False
    
    # Tentar diferentes valores de skiprows
    for skip in [3, 0, 1, 2, 4, 5]:
        try:
            print(f"\n📖 Tentando ler com skiprows={skip}...")
            df = pd.read_csv(
                caminho_arquivo,
                sep='\t',
                encoding='latin1',
                engine='python',
                skiprows=skip,
                skipfooter=1,
                on_bad_lines='skip'
            )
            
            if df.empty:
                print(f"   ⚠️  DataFrame vazio com skiprows={skip}")
                continue
            
            print(f"   ✅ DataFrame carregado: {len(df)} linhas, {len(df.columns)} colunas")
            print(f"   📋 Colunas: {list(df.columns)}")
            
            # Aplicar padronização
            print(f"\n🔧 Aplicando padronização de colunas...")
            df_padronizado = padronizar_colunas(df.copy(), arquivo_nome=os.path.basename(caminho_arquivo))
            print(f"   📋 Colunas após padronização: {list(df_padronizado.columns)}")
            
            # Verificar se Material foi encontrado
            if 'Material' in df_padronizado.columns:
                print(f"\n✅ SUCESSO! Coluna 'Material' encontrada com skiprows={skip}")
                print(f"   📊 Primeiros valores de Material:")
                print(f"   {df_padronizado['Material'].head(10).tolist()}")
                return True
            else:
                print(f"\n⚠️  Coluna 'Material' não encontrada após padronização")
                print(f"   🔍 Tentando detectar coluna Material automaticamente...")
                
                # Aplicar a mesma lógica de detecção do Extracao.py
                melhor_candidata = None
                melhor_score = 0
                candidatas_info = []
                
                for col in df_padronizado.columns:
                    # Pular colunas conhecidas
                    if col in ['N° conta', 'Nº conta', 'FA00']:
                        continue
                    
                    try:
                        valores_numericos = pd.to_numeric(df_padronizado[col], errors='coerce')
                        valores_validos = valores_numericos.notna().sum()
                        valores_nao_zero = (valores_numericos != 0).sum()
                        
                        if len(df_padronizado) > 0:
                            pct_validos = valores_validos / len(df_padronizado)
                            pct_nao_zero = valores_nao_zero / len(df_padronizado) if valores_validos > 0 else 0
                            
                            score = pct_validos * 0.4 + pct_nao_zero * 0.4
                            
                            if valores_validos > 0:
                                valores_nao_zero_series = valores_numericos[valores_numericos != 0]
                                if len(valores_nao_zero_series) > 0:
                                    media_valores = valores_nao_zero_series.abs().mean()
                                    if 1000 <= media_valores <= 9999999999:
                                        score += 0.2
                                    elif 100 <= media_valores < 1000:
                                        score += 0.1
                            
                            candidatas_info.append({
                                'coluna': col,
                                'score': score,
                                'pct_validos': pct_validos,
                                'pct_nao_zero': pct_nao_zero,
                                'valores_validos': valores_validos,
                                'media': valores_numericos[valores_numericos != 0].abs().mean() if valores_validos > 0 else 0
                            })
                            
                            if score > melhor_score and pct_validos > 0.2 and pct_nao_zero > 0.2:
                                melhor_score = score
                                melhor_candidata = col
                    except Exception as e:
                        continue
                
                # Mostrar candidatas
                if candidatas_info:
                    print(f"\n   📋 Candidatas analisadas:")
                    for info in sorted(candidatas_info, key=lambda x: x['score'], reverse=True)[:5]:
                        print(f"      - '{info['coluna']}': score={info['score']:.2f}, "
                              f"válidos={info['pct_validos']:.1%}, não-zero={info['pct_nao_zero']:.1%}, "
                              f"média={info['media']:.0f}")
                
                if melhor_candidata:
                    print(f"\n   ✅ Coluna '{melhor_candidata}' identificada como Material (score: {melhor_score:.2f})")
                    df_padronizado.rename(columns={melhor_candidata: 'Material'}, inplace=True)
                    print(f"   📊 Primeiros valores de Material:")
                    print(f"   {df_padronizado['Material'].head(10).tolist()}")
                    return True
                else:
                    print(f"\n   ⚠️  Nenhuma candidata encontrada com critérios rígidos")
                    # Tentar fallback
                    melhor_candidata_fallback = None
                    melhor_score_fallback = 0
                    
                    for col in df_padronizado.columns:
                        if col in ['N° conta', 'Nº conta', 'FA00']:
                            continue
                        try:
                            valores_numericos = pd.to_numeric(df_padronizado[col], errors='coerce')
                            valores_validos = valores_numericos.notna().sum()
                            if len(df_padronizado) > 0 and valores_validos > 0:
                                pct_validos = valores_validos / len(df_padronizado)
                                if pct_validos > 0.1:
                                    score_fallback = pct_validos
                                    if score_fallback > melhor_score_fallback:
                                        melhor_score_fallback = score_fallback
                                        melhor_candidata_fallback = col
                        except:
                            continue
                    
                    if melhor_candidata_fallback:
                        print(f"\n   ✅ Fallback: Coluna '{melhor_candidata_fallback}' identificada (score: {melhor_score_fallback:.2f})")
                        return True
                    else:
                        print(f"\n   ❌ Não foi possível identificar coluna Material")
                        continue
                        
        except Exception as e:
            print(f"   ❌ Erro ao processar com skiprows={skip}: {str(e)}")
            continue
    
    return False

def main():
    """Função principal de teste"""
    print("="*70)
    print("TESTE DE DETECÇÃO DE COLUNA MATERIAL - ARQUIVOS KSBB")
    print("="*70)
    
    # Pasta de arquivos KSBB - com estrutura de ano (2025)
    pasta_ksbb = os.path.join("Extracoes", "2025", "KSBB")
    
    if not os.path.exists(pasta_ksbb):
        print(f"❌ Pasta não encontrada: {pasta_ksbb}")
        return
    
    # Listar arquivos .txt
    arquivos = [f for f in os.listdir(pasta_ksbb) if f.endswith('.txt')]
    
    if not arquivos:
        print(f"⚠️  Nenhum arquivo .txt encontrado em {pasta_ksbb}")
        return
    
    print(f"\n📁 Arquivos encontrados: {len(arquivos)}")
    for arquivo in arquivos:
        print(f"   - {arquivo}")
    
    # Testar cada arquivo
    resultados = {}
    for arquivo in arquivos:
        caminho = os.path.join(pasta_ksbb, arquivo)
        sucesso = testar_arquivo_ksbb(caminho)
        resultados[arquivo] = sucesso
    
    # Resumo
    print(f"\n{'='*70}")
    print("RESUMO DOS TESTES")
    print(f"{'='*70}")
    for arquivo, sucesso in resultados.items():
        status = "✅ SUCESSO" if sucesso else "❌ FALHOU"
        print(f"{status}: {arquivo}")
    
    sucessos = sum(1 for s in resultados.values() if s)
    print(f"\n📊 Total: {sucessos}/{len(resultados)} arquivos processados com sucesso")

if __name__ == "__main__":
    main()


