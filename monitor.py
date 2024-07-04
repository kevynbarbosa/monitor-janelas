import time
import psutil
import pygetwindow as gw
import sqlite3
import win32process
import win32gui

# Função para obter a janela ativa e o nome do aplicativo
def get_active_window():
    try:
        hwnd = win32gui.GetForegroundWindow()  # Obtém o handle da janela ativa
        _, pid = win32process.GetWindowThreadProcessId(hwnd)  # Obtém o ID do processo da janela ativa
        process = psutil.Process(pid)
        print(process)
        window = gw.getActiveWindow()
        return process.name(), window.title if window else None
    except Exception as e:
        print(f"Erro ao obter a janela ativa: {e}")
        return None, None

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('activity_monitor.db')
c = conn.cursor()

# Criação da tabela de atividades se não existir
c.execute('''CREATE TABLE IF NOT EXISTS activities
             (timestamp TEXT, application TEXT, title TEXT)''')
conn.commit()

# Monitoramento contínuo
try:
    while True:
        app, title = get_active_window()
        if app:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            c.execute("INSERT INTO activities (timestamp, application, title) VALUES (?, ?, ?)",
                      (timestamp, app, title))
            conn.commit()

            # print(app, "=> ", title)
        time.sleep(5)  # Intervalo de monitoramento
except KeyboardInterrupt:
    conn.close()
    print("Monitoramento encerrado.")
