from tkinter import *
from PIL import Image, ImageTk
from usuario import usuariosClass
from cardapio import cardapioClass
from estoque import estoqueClass
from novoPedido import pedidoClass
from fluxo_caixa import fluxoClass
from matGraficos import graficoClass
import sqlite3
from tkinter import messagebox
import time
import os

class TBS:
    def __init__(self, root):
        self.root = root
        self.width = 1200
        self.height = 650
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        blank_space = " "
        self.root.title(150 * blank_space + "Coffee Urach | Projeto Lab Programação")
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.root.config(bg="#d9d9d9")

        self.icon_title = PhotoImage(file="")
        title = Label(self.root, text="Coffee URACH", image=self.icon_title, compound=LEFT, font=("Times new roman", 78, "bold"), bg="#ff66c4")
        title.pack(fill=X)

        btn_logout = Button(self.root, text='Sair', font=("Times new roman", 15, "bold"), bg="white", cursor="hand2", command=self.logout).place(x=1090, y=10, width=100, height=40)

        self.lbl_clock = Label(self.root, font=("Times new roman", 12, "bold"), bg="#d9d9d9")
        self.lbl_clock.place(x=0, y=120, relwidth=1, height=30)
        self.atualizarDataHora()

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=150, width=230, height=565)

        lbl_menuLogo = Label(LeftMenu, text="")
        lbl_menuLogo.pack(side=TOP, fill=X)

        self.icon_side = PhotoImage(file="")
        lbl_menu = Label(LeftMenu, text="MENU", font=("Times new roman", 15, "bold"), bg="#ff66c4", fg="white")
        lbl_menu.pack(side=TOP, fill=X)

        btn_usuario = Button(LeftMenu, text="Lista de Usuários", image=self.icon_side, compound=LEFT, padx=20, anchor="w", font=("Times new roman", 12), command=self.usuario)
        btn_usuario.pack(fill=X)

        btn_cardapio = Button(LeftMenu, text="Cardápio", image=self.icon_side, compound=LEFT, padx=20, anchor="w", font=("Times new roman", 12), command=self.cardapio)
        btn_cardapio.pack(fill=X)

        btn_estoque = Button(LeftMenu, text="Estoque", image=self.icon_side, compound=LEFT, padx=20, anchor="w", font=("Times new roman", 12), command=self.estoque)
        btn_estoque.pack(fill=X)

        btn_caixa = Button(LeftMenu, text="Fluxo de Caixa", image=self.icon_side, compound=LEFT, padx=20, anchor="w", font=("Times new roman", 12), command=self.fluxoCaixa)
        btn_caixa.pack(fill=X)

        btn_grafico = Button(LeftMenu, text="Gráficos de Controle", image=self.icon_side, compound=LEFT, padx=20, anchor="w", font=("Times New Roman", 12), command=self.matGraficos)
        btn_grafico.pack(fill=X)

        btn_novoPedido = Button(self.root, text="Novo Pedido", font=("Times new roman", 15, "bold"), bg="#ff66c4", fg="white", cursor="hand2", command=self.novoPedido)
        btn_novoPedido.place(x=self.width - 170, y=self.height - 60, width=160, height=50)

    def atualizarDataHora(self):
        datAtual = time.strftime("%d-%m-%Y")
        horAtual = time.strftime("%H:%M:%S")

        self.lbl_clock.config(text=f"Seja bem vindo!!!\t\t Data: {datAtual} \t\t Hora: {horAtual}")
        self.root.after(1000, self.atualizarDataHora)

    def usuario(self):
        self.new_win = Toplevel(self.root)
        self.ne_obj = usuariosClass(self.new_win)

    def cardapio(self):
        self.new_win = Toplevel(self.root)
        self.ne_obj = cardapioClass(self.new_win)

    def estoque(self):
        self.new_win = Toplevel(self.root)
        self.ne_obj = estoqueClass(self.new_win)

    def fluxoCaixa(self):
        self.new_win = Toplevel(self.root)
        self.ne_obj = fluxoClass(self.new_win)

    def novoPedido(self):
        self.new_win = Toplevel(self.root)
        self.ne_obj = pedidoClass(self.new_win)
    
    def matGraficos(self):
        self.new_win = Toplevel(self.root)
        self.ne_obj = graficoClass(self.new_win)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")


if __name__ == "__main__":
    root = Tk()
    obj = TBS(root)
    root.mainloop()