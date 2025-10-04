from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class fluxoClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Fluxo de Caixa")
        self.root.geometry("1100x500+200+100")
        self.root.config(bg="#d9d9d9")
        self.root.focus_force()

        self.var_tipo = StringVar()
        self.var_descricao = StringVar()
        self.var_valor = StringVar()
        self.var_data = StringVar()

        input_frame = Frame(self.root, bg="#d9d9d9")
        input_frame.place(x=10, y=10, width=1080, height=80)

        lbl_tipo = Label(input_frame, text="Tipo", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black")
        lbl_tipo.grid(row=0, column=0, padx=5, pady=5)
        cmb_tipo = ttk.Combobox(input_frame, textvariable=self.var_tipo, values=("Entrada", "Saída"), state="readonly", font=("Times new roman", 12))
        cmb_tipo.grid(row=0, column=1, padx=5, pady=5)
        cmb_tipo.current(0)

        lbl_descricao = Label(input_frame, text="Descrição", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black")
        lbl_descricao.grid(row=0, column=2, padx=5, pady=5)
        txt_descricao = Entry(input_frame, textvariable=self.var_descricao, font=("Times new roman", 12), bg="white")
        txt_descricao.grid(row=0, column=3, padx=5, pady=5)

        lbl_valor = Label(input_frame, text="Valor (R$)", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black")
        lbl_valor.grid(row=0, column=4, padx=5, pady=5)
        txt_valor = Entry(input_frame, textvariable=self.var_valor, font=("Times new roman", 12), bg="white")
        txt_valor.grid(row=0, column=5, padx=5, pady=5)

        lbl_data = Label(input_frame, text="Data", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black")
        lbl_data.grid(row=0, column=6, padx=5, pady=5)
        txt_data = Entry(input_frame, textvariable=self.var_data, font=("Times new roman", 12), bg="white")
        txt_data.grid(row=0, column=7, padx=5, pady=5)
        self.var_data.set(datetime.now().strftime("%d-%m-%Y"))

        btn_adicionar = Button(input_frame, text="Adicionar", font=("Times new roman", 12, "bold"), bg="#ff66c4", fg="black", command=self.adicionar_transacao)
        btn_adicionar.grid(row=0, column=8, padx=5, pady=5)

        btn_limpar = Button(input_frame, text="Limpar", font=("Times new roman", 12, "bold"), bg="#ff66c4", fg="black", command=self.limpar_campos)
        btn_limpar.grid(row=1, column=8, padx=5, pady=5)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Tipo", "Descrição", "Valor (R$)", "Data"), show="headings")
        self.tree.place(x=10, y=100, width=1080, height=350)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Valor (R$)", text="Valor (R$)")
        self.tree.heading("Data", text="Data")

        self.tree.column("ID", width=50)
        self.tree.column("Tipo", width=100)
        self.tree.column("Descrição", width=400)
        self.tree.column("Valor (R$)", width=150)
        self.tree.column("Data", width=150)

        scroll_y = Scrollbar(self.tree, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.tree.config(yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.tree.yview)

        self.lbl_saldo = Label(self.root, text="Saldo: R$ 0.00", font=("Times new roman", 14, "bold"), bg="#d9d9d9", fg="black")
        self.lbl_saldo.place(x=10, y=460, width=1080, height=30)

        self.carregar_transacoes()

    def adicionar_transacao(self):
        tipo = self.var_tipo.get()
        descricao = self.var_descricao.get()
        valor = self.var_valor.get()
        data = self.var_data.get()

        if tipo and descricao and valor and data:
            try:
                valor = float(valor)
                con = sqlite3.connect("Cafe.db")
                cur = con.cursor()
                cur.execute("INSERT INTO fluxo_caixa (tipo, descricao, valor, data) VALUES (?, ?, ?, ?)",
                            (tipo, descricao, valor, data))
                con.commit()
                con.close()
                messagebox.showinfo("Sucesso", "Transação adicionada com sucesso!", parent=self.root)
                self.carregar_transacoes()
                self.limpar_campos()
            except ValueError:
                messagebox.showerror("Erro", "O valor deve ser um número válido!", parent=self.root)
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!", parent=self.root)

    def limpar_campos(self):
        self.var_tipo.set("Entrada")
        self.var_descricao.set("")
        self.var_valor.set("")
        self.var_data.set(datetime.now().strftime("%d-%m-%Y"))

    def carregar_transacoes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        con = sqlite3.connect("Cafe.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM fluxo_caixa")
        rows = cur.fetchall()
        con.close()

        saldo = 0.0
        for row in rows:
            self.tree.insert("", "end", values=row)
            if row[1] == "Entrada":
                saldo += row[3]
            else:
                saldo -= row[3]

        self.lbl_saldo.config(text=f"Saldo: R$ {saldo:.2f}")

if __name__ == "__main__":
    root = Tk()
    obj = fluxoClass(root)
    root.mainloop()