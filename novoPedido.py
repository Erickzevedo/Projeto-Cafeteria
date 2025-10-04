from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class pedidoClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Realizar Pedido")
        self.root.geometry("1100x500+200+100")
        self.root.config(bg="#d9d9d9")
        self.root.focus_force()


        self.var_item = StringVar()
        self.var_quantidade = IntVar()
        self.var_total = DoubleVar()
        self.itens_pedido = []

        input_frame = Frame(self.root, bg="#d9d9d9")
        input_frame.place(x=10, y=10, width=1080, height=80)

        lbl_item = Label(input_frame, text="Item", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black")
        lbl_item.grid(row=0, column=0, padx=5, pady=5)
        self.cmb_item = ttk.Combobox(input_frame, textvariable=self.var_item, state="readonly", font=("Times new roman", 12))
        self.cmb_item.grid(row=0, column=1, padx=5, pady=5)
        self.carregar_cardapio()

        lbl_quantidade = Label(input_frame, text="Quantidade", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black")
        lbl_quantidade.grid(row=0, column=2, padx=5, pady=5)
        txt_quantidade = Entry(input_frame, textvariable=self.var_quantidade, font=("Times new roman", 12), bg="white")
        txt_quantidade.grid(row=0, column=3, padx=5, pady=5)

        btn_adicionar = Button(input_frame, text="Adicionar", font=("Times new roman", 12, "bold"), bg="#ff66c4", fg="black", command=self.adicionar_item)
        btn_adicionar.grid(row=0, column=4, padx=5, pady=5)

        self.tree = ttk.Treeview(self.root, columns=("Item", "Quantidade", "Preço Unitário", "Subtotal"), show="headings")
        self.tree.place(x=10, y=100, width=1080, height=300)

        self.tree.heading("Item", text="Item")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Preço Unitário", text="Preço Unitário (R$)")
        self.tree.heading("Subtotal", text="Subtotal (R$)")

        self.tree.column("Item", width=400)
        self.tree.column("Quantidade", width=150)
        self.tree.column("Preço Unitário", width=150)
        self.tree.column("Subtotal", width=150)

        scroll_y = Scrollbar(self.tree, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.tree.config(yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.tree.yview)

        self.lbl_total = Label(self.root, text="Total: R$ 0.00", font=("Times new roman", 14, "bold"), bg="#d9d9d9", fg="black")
        self.lbl_total.place(x=10, y=420, width=1080, height=30)

        btn_finalizar = Button(self.root, text="Finalizar Pedido", font=("Times new roman", 14, "bold"), bg="#ff66c4", fg="black", command=self.finalizar_pedido)
        btn_finalizar.place(x=10, y=460, width=1080, height=30)

    def carregar_cardapio(self):
        con = sqlite3.connect("Cafe.db")
        cur = con.cursor()
        cur.execute("SELECT nome, preco FROM cardapio")
        itens = cur.fetchall()
        con.close()

        self.cmb_item["values"] = [f"{item[0]} (R$ {item[1]:.2f})" for item in itens]
        if itens:
            self.cmb_item.current(0)

    def adicionar_item(self):
        item = self.var_item.get()
        quantidade = self.var_quantidade.get()

        if item and quantidade > 0:
            nome_item = item.split(" (R$ ")[0]
            preco_unitario = float(item.split(" (R$ ")[1].replace(")", ""))

            subtotal = preco_unitario * quantidade

            self.itens_pedido.append((nome_item, quantidade, preco_unitario, subtotal))

            self.tree.insert("", "end", values=(nome_item, quantidade, f"R$ {preco_unitario:.2f}", f"R$ {subtotal:.2f}"))

            self.atualizar_total()
        else:
            messagebox.showerror("Erro", "Selecione um item e insira uma quantidade válida!", parent=self.root)

    def atualizar_total(self):
        total = sum(item[3] for item in self.itens_pedido)
        self.var_total.set(total)
        self.lbl_total.config(text=f"Total: R$ {total:.2f}")

    def finalizar_pedido(self):
        if self.itens_pedido:
            itens_str = ", ".join([f"{item[0]} ({item[1]}x R$ {item[2]:.2f})" for item in self.itens_pedido])

            con = sqlite3.connect("Cafe.db")
            cur = con.cursor()
            cur.execute("INSERT INTO pedidos (itens, total, data) VALUES (?, ?, ?)",
                        (itens_str, self.var_total.get(), datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
            con.commit()
            con.close()

            messagebox.showinfo("Sucesso", "Pedido finalizado com sucesso!", parent=self.root)
            self.limpar_pedido()
        else:
            messagebox.showerror("Erro", "Adicione itens ao pedido antes de finalizar!", parent=self.root)

    def limpar_pedido(self):
        self.itens_pedido.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.var_total.set(0.0)
        self.lbl_total.config(text="Total: R$ 0.00")

if __name__ == "__main__":
    root = Tk()
    obj = pedidoClass(root)
    root.mainloop()