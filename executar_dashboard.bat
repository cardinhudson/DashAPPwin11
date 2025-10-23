@echo off
echo ========================================
echo    Dashboard KE5Z - Executando Aplicacao
echo ========================================
echo.

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo Iniciando Dashboard KE5Z...
echo.
echo A aplicacao sera aberta no seu navegador.
echo Para parar a aplicacao, pressione Ctrl+C
echo.

streamlit run app.py

pause

