import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3

class graficoClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Gráficos de Fluxo de Caixa")
        self.root.geometry("1100x600")
        self.root.config(bg="#d9d9d9")
        self.root.focus_force()

        # Frame para o gráfico
        self.graph_frame = tk.Frame(self.root, bg="#d9d9d9")
        self.graph_frame.place(x=10, y=10, width=1080, height=580)

        # Gerar o gráfico diretamente ao inicializar
        self.gerar_grafico()

    def gerar_grafico(self):
        # Conectar ao banco de dados
        con = sqlite3.connect("Cafe.db")
        cur = con.cursor()

        # Buscar entradas e saídas agrupadas por data
        cur.execute("SELECT data, SUM(valor) FROM fluxo_caixa WHERE tipo='Entrada' GROUP BY data")
        entradas = cur.fetchall()

        cur.execute("SELECT data, SUM(valor) FROM fluxo_caixa WHERE tipo='Saída' GROUP BY data")
        saidas = cur.fetchall()

        con.close()

        # Extrair datas e valores
        datas_entradas = [row[0] for row in entradas]
        valores_entradas = [row[1] for row in entradas]

        datas_saidas = [row[0] for row in saidas]
        valores_saidas = [row[1] for row in saidas]

        # Criar o gráfico
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(datas_entradas, valores_entradas, label="Entradas", marker='o')
        ax.plot(datas_saidas, valores_saidas, label="Saídas", marker='o')

        ax.set_title("Fluxo de Caixa - Entradas e Saídas")
        ax.set_xlabel("Data")
        ax.set_ylabel("Valor (R$)")
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Exibir o gráfico no frame
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    obj = graficoClass(root)
    root.mainloop()