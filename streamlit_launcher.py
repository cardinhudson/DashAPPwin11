"""
Launcher personalizado para executar Streamlit em executável PyInstaller
Resolve problemas de metadata e inicialização
"""
import sys
import os
import subprocess
import socket
import time
import urllib.request



def is_port_open(host: str, port: int, timeout_seconds: int = 1) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout_seconds)
    try:
        sock.connect((host, port))
        return True
    except Exception:
        return False
    finally:
        try:
            sock.close()
        except Exception:
            pass


def wait_for_server(host: str, port: int, max_wait_seconds: int = 60) -> bool:
    start = time.time()
    while time.time() - start < max_wait_seconds:
        if is_port_open(host, port, timeout_seconds=1):
            return True
        time.sleep(0.5)
    return False


def main() -> None:
    try:
        if hasattr(sys, "_MEIPASS"):
            os.chdir(sys._MEIPASS)

        # Evitar abertura do navegador externo pelo Streamlit
        os.environ.setdefault("BROWSER", "none")
        os.environ.setdefault("STREAMLIT_BROWSER_GATHERUSAGESTATS", "false")

        cmd = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app.py",
            "--server.port=8501",
            "--server.headless=true",
            "--server.address=127.0.0.1",
            "--global.developmentMode=false",
        ]

        server_proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )

        if not wait_for_server("127.0.0.1", 8501, max_wait_seconds=90):
            # Mensagem sem caracteres especiais para evitar problemas de encoding
            try:
                with open("launcher_error.log", "a", encoding="utf-8") as f:
                    f.write("Servidor Streamlit nao respondeu na porta 8501.\n")
            except Exception:
                pass
            try:
                server_proc.terminate()
            except Exception:
                pass
            sys.exit(1)

        try:
            import webview

            window = webview.create_window(
                title="Dashboard KE5Z",
                url="http://127.0.0.1:8501",
                width=1280,
                height=800,
                resizable=True,
            )

            def on_closed():
                try:
                    server_proc.terminate()
                except Exception:
                    pass

            try:
                webview.start(on_closed)
            except Exception as webview_err:
                # Tentativa de instalar WebView2 automaticamente (Windows)
                try:
                    installer_url = "https://go.microsoft.com/fwlink/p/?LinkId=2124703"  # Evergreen WebView2
                    installer_path = os.path.join(os.getcwd(), "MicrosoftEdgeWebview2Setup.exe")
                    urllib.request.urlretrieve(installer_url, installer_path)
                    subprocess.run([installer_path, "/silent", "/install"], check=False)
                except Exception:
                    pass
                # Fallback: abrir no navegador padrão
                import webbrowser
                webbrowser.open("http://127.0.0.1:8501")
                server_proc.wait()

        except Exception:
            # Se pywebview não estiver disponível, abre no navegador padrão
            import webbrowser

            webbrowser.open("http://127.0.0.1:8501")
            server_proc.wait()

    except Exception as e:
        # Não usar input() em exe sem console; registrar em arquivo de log
        try:
            import traceback
            with open("launcher_error.log", "a", encoding="utf-8") as f:
                f.write(f"Erro ao iniciar aplicacao: {e}\n")
                f.write(traceback.format_exc())
        except Exception:
            pass
        # Tentar mostrar MessageBox do Windows (Unicode safe)
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(None, "Erro ao iniciar aplicacao. Veja launcher_error.log", "Dashboard KE5Z", 0)
        except Exception:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()

