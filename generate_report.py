import sqlite3
import matplotlib.pyplot as plt

def generate_report():
    conn = sqlite3.connect('activity_monitor.db')
    c = conn.cursor()

    c.execute("SELECT application, COUNT(*) FROM activities WHERE timestamp >= date('now', '-1 day') GROUP BY application")
    data = c.fetchall()
    
    applications = [row[0] for row in data]
    counts = [row[1] for row in data]

    plt.bar(applications, counts)
    plt.xlabel('Aplicações')
    plt.ylabel('Tempo gasto (em intervalos de 5 segundos)')
    plt.title('Relatório Diário de Atividades')
    plt.savefig('daily_report.png')
    plt.show()

    conn.close()

generate_report()
