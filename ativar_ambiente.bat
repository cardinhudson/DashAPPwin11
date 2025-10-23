@echo off
echo ========================================
echo    Dashboard KE5Z - Ativacao do Ambiente
echo ========================================
echo.

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo Ambiente virtual ativado com sucesso!
echo.
echo Para executar o dashboard, use:
echo   streamlit run app.py
echo.
echo Para sair do ambiente virtual, use:
echo   deactivate
echo.

cmd /k

