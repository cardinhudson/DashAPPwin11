# 📊 Dashboard KE5Z - Sistema Avançado de Análise Financeira

Sistema completo de análise financeira desenvolvido com Streamlit, otimizado para processamento de grandes volumes de dados.

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.11 ou superior
- Windows 10/11 (recomendado)

### Instalação Automática

1. **Execute o ambiente virtual:**
   ```bash
   # Duplo clique no arquivo:
   ativar_ambiente.bat
   ```

2. **Execute o dashboard:**
   ```bash
   # Duplo clique no arquivo:
   executar_dashboard.bat
   ```

### Instalação Manual

1. **Criar ambiente virtual:**
   ```bash
   python -m venv venv
   ```

2. **Ativar ambiente virtual:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Executar aplicação:**
   ```bash
   streamlit run app.py
   ```

## 📁 Estrutura do Projeto

```
Dash-V3/
├── 📄 app.py                    # Aplicação principal
├── 📄 auth_simple.py           # Sistema de autenticação
├── 📄 Extracao.py              # Script de extração de dados
├── 📄 requirements.txt         # Dependências do projeto
├── 📄 usuarios.json            # Base de dados de usuários
├── 📂 pages/                   # Páginas do dashboard
│   ├── 1_Dash_Mes.py          # Dashboard mensal
│   ├── 2_IUD_Assistant.py     # Assistente inteligente
│   ├── 3_Total_accounts.py    # Análise total de contas
│   ├── 4_Waterfall_Analysis.py # Análise waterfall
│   ├── 5_Admin_Usuarios.py    # Administração de usuários
│   ├── 6_Extracao_Dados.py    # Extração de dados
│   └── 7_Sobre_Projeto.py     # Informações do projeto
├── 📂 KE5Z/                   # Dados processados (Parquet)
├── 📂 Extracoes/              # Dados de entrada (TXT)
├── 📂 arquivos/               # Arquivos Excel específicos
├── 📂 venv/                   # Ambiente virtual Python
├── 🔧 ativar_ambiente.bat     # Script de ativação
└── 🚀 executar_dashboard.bat  # Script de execução
```

## 🔐 Sistema de Autenticação

### Usuário Padrão
- **Usuário:** `admin`
- **Senha:** `admin123`
- **Tipo:** Administrador

### Modos de Operação
- **☁️ Cloud:** Dados otimizados para melhor performance
- **💻 Completo:** Acesso total aos dados (modo local)

## 📊 Funcionalidades Principais

### 🏠 Dashboard Principal
- Gráficos dinâmicos por período e categorias
- Análise Type 07 com filtros específicos
- Tabelas interativas com filtros avançados
- Exportação Excel com formatação

### 📅 Dashboard Mensal
- Análise focada em um período específico
- Performance otimizada para análises detalhadas
- Download inteligente com limites de segurança

### 🌊 Análise Waterfall
- Visualização de variações mês a mês
- Identificação de trends e padrões
- 100% dados waterfall para performance máxima

### 🎯 IUD Assistant
- Assistente inteligente para análise de dados
- Interface conversacional para exploração
- Gráficos automáticos baseados em consultas

### 📊 Total Accounts
- Análise completa do centro de lucro 02S
- 100% otimizado com dados waterfall
- Gráficos e tabelas dinâmicas

## ⚡ Otimizações de Performance

### Sistema Waterfall
- **Arquivo otimizado:** `KE5Z_waterfall.parquet`
- **68% menor** que arquivo original
- **Colunas essenciais** para máxima performance

### Transformação TXT → Parquet
- **Conversão automática** de arquivos TXT grandes
- **Redução de tamanho:** Até 10x menor
- **Performance:** 5-10x mais rápido

### Gestão de Memória
- **Cache inteligente** com TTL configurável
- **Persistência em disco** para dados críticos
- **Detecção automática** de ambiente

## 🔧 Dependências

### Principais
- **Streamlit** >= 1.28.0 - Framework web
- **Pandas** >= 2.0.0 - Manipulação de dados
- **Altair** >= 5.0.0 - Visualizações
- **Plotly** >= 5.15.0 - Gráficos interativos
- **OpenPyXL** >= 3.1.0 - Exportação Excel
- **PyArrow** >= 12.0.0 - Performance Parquet

### Completas
```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
altair>=5.0.0
plotly>=5.15.0
openpyxl>=3.1.0
pyarrow>=12.0.0
python-dateutil>=2.8.0
```

## 📋 Uso do Sistema

### 1. Primeiro Acesso
1. Execute `executar_dashboard.bat`
2. Faça login com `admin` / `admin123`
3. Escolha o modo de operação (Cloud/Completo)

### 2. Extração de Dados
1. Acesse "Extração de Dados" (apenas administradores)
2. Verifique se os arquivos necessários estão presentes
3. Execute a extração para gerar dados otimizados

### 3. Análise de Dados
1. Use os filtros na barra lateral
2. Explore diferentes visualizações
3. Exporte dados em Excel quando necessário

## 🛠️ Desenvolvimento

### Estrutura de Código
- **app.py:** ~730 linhas (Dashboard principal)
- **Extracao.py:** ~610 linhas (Processamento)
- **auth_simple.py:** ~450 linhas (Autenticação)
- **Total:** ~3.500+ linhas de código

### Tecnologias
- **Python 3.11+**
- **Streamlit** (Framework web)
- **Pandas** (Análise de dados)
- **Altair/Plotly** (Visualizações)
- **PyArrow** (Performance)

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique se todos os arquivos estão presentes
2. Confirme se o ambiente virtual está ativado
3. Verifique os logs de erro no terminal

## 🎯 Características Técnicas

- **Performance:** 68% redução no uso de memória
- **Escalabilidade:** Compatível com milhões de registros
- **Portabilidade:** Funciona em qualquer PC Windows
- **Segurança:** Sistema de autenticação robusto
- **Usabilidade:** Interface intuitiva e responsiva

---

**Dashboard KE5Z** - Sistema Avançado de Análise Financeira
Desenvolvido com Streamlit e otimizado para máxima performance.

