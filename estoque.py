from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class estoqueClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Estoque")
        self.root.geometry("1100x500+200+100")
        self.root.config(bg="#d9d9d9")
        self.root.focus_force()

        self.var_id = StringVar()
        self.var_nome = StringVar()
        self.var_quantidade = IntVar()
        self.var_preco = DoubleVar()
        self.var_categoria = StringVar()

        input_frame = Frame(self.root, bg="#d9d9d9")
        input_frame.place(x=10, y=10, width=1080, height=100)

        lbl_nome = Label(input_frame, text="Nome do Item", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black")
        lbl_nome.grid(row=0, column=0, padx=5, pady=5)
        txt_nome = Entry(input_frame, textvariable=self.var_nome, font=("Times new roman", 12), bg="white")
        txt_nome.grid(row=0, column=1, padx=5, pady=5)

        lbl_quantidade = Label(input_frame, text="Quantidade", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black")
        lbl_quantidade.grid(row=1, column=0, padx=5, pady=5)
        txt_quantidade = Entry(input_frame, textvariable=self.var_quantidade, font=("Times new roman", 12), bg="white")
        txt_quantidade.grid(row=1, column=1, padx=5, pady=5)

        lbl_preco = Label(input_frame, text="Preço Unitário (R$)", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black")
        lbl_preco.grid(row=0, column=4, padx=5, pady=5)
        txt_preco = Entry(input_frame, textvariable=self.var_preco, font=("Times new roman", 12), bg="white")
        txt_preco.grid(row=0, column=5, padx=5, pady=5)

        lbl_categoria = Label(input_frame, text="Categoria", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black")
        lbl_categoria.grid(row=1, column=4, padx=5, pady=5)
        cmb_categoria = ttk.Combobox(input_frame, textvariable=self.var_categoria, values=("Bebidas", "Comidas", "Sobremesas"), state="readonly", font=("Times new roman", 12))
        cmb_categoria.grid(row=1, column=5, padx=5, pady=5)
        cmb_categoria.current(0)

        btn_adicionar = Button(input_frame, text="Adicionar", font=("Times new roman", 12, "bold"), bg="#ff66c4", fg="black", command=self.adicionar_item)
        btn_adicionar.grid(row=0, column=6, padx=5, pady=5)

        btn_atualizar = Button(input_frame, text="Atualizar", font=("Times new roman", 12, "bold"), bg="#ff66c4", fg="black", command=self.atualizar_item)
        btn_atualizar.grid(row=0, column=7, padx=5, pady=5)

        btn_excluir = Button(input_frame, text="Excluir", font=("Times new roman", 12, "bold"), bg="#ff66c4", fg="black", command=self.excluir_item)
        btn_excluir.grid(row=0, column=8, padx=5, pady=5)

        btn_limpar = Button(input_frame, text="Limpar", font=("Times new roman", 12, "bold"), bg="#ff66c4", fg="black", command=self.limpar_campos)
        btn_limpar.grid(row=0, column=9, padx=5, pady=5)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Nome", "Quantidade", "Preço Unitário", "Categoria"), show="headings")
        self.tree.place(x=10, y=120, width=1080, height=350)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Preço Unitário", text="Preço Unitário (R$)")
        self.tree.heading("Categoria", text="Categoria")

        self.tree.column("ID", width=50)
        self.tree.column("Nome", width=300)
        self.tree.column("Quantidade", width=100)
        self.tree.column("Preço Unitário", width=150)
        self.tree.column("Categoria", width=150)

        scroll_y = Scrollbar(self.tree, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.tree.config(yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.tree.yview)

        self.carregar_estoque()

        self.tree.bind("<ButtonRelease-1>", self.selecionar_item)

    def carregar_estoque(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        con = sqlite3.connect("Cafe.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM estoque")
        rows = cur.fetchall()
        con.close()

        for row in rows:
            self.tree.insert("", "end", values=row)

    def adicionar_item(self):
        nome = self.var_nome.get()
        quantidade = self.var_quantidade.get()
        preco = self.var_preco.get()
        categoria = self.var_categoria.get()

        if nome and quantidade and preco and categoria:
            try:
                con = sqlite3.connect("Cafe.db")
                cur = con.cursor()
                cur.execute("INSERT INTO estoque (nome, quantidade, preco_unitario, categoria) VALUES (?, ?, ?, ?)",
                             (nome, quantidade, preco, categoria))
                con.commit()
                con.close()
                messagebox.showinfo("Sucesso", "Item adicionado ao estoque!", parent=self.root)
                self.carregar_estoque()
                self.limpar_campos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar item: {str(e)}", parent=self.root)
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!", parent=self.root)

    def atualizar_item(self):
        id_item = self.var_id.get()
        nome = self.var_nome.get()
        quantidade = self.var_quantidade.get()
        preco = self.var_preco.get()
        categoria = self.var_categoria.get()

        if id_item and nome and quantidade and preco and categoria:
            try:
                con = sqlite3.connect("Cafe.db")
                cur = con.cursor()
                cur.execute("UPDATE estoque SET nome=?, quantidade=?, preco_unitario=?, categoria=? WHERE id=?",
                            (nome, quantidade, preco, categoria, id_item))
                con.commit()
                con.close()
                messagebox.showinfo("Sucesso", "Item atualizado com sucesso!", parent=self.root)
                self.carregar_estoque()
                self.limpar_campos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar item: {str(e)}", parent=self.root)
        else:
            messagebox.showerror("Erro", "Selecione um item para atualizar!", parent=self.root)

    def excluir_item(self):
        id_item = self.var_id.get()

        if id_item:
            try:
                con = sqlite3.connect("Cafe.db")
                cur = con.cursor()
                cur.execute("DELETE FROM estoque WHERE id=?", (id_item,))
                con.commit()
                con.close()
                messagebox.showinfo("Sucesso", "Item excluído com sucesso!", parent=self.root)
                self.carregar_estoque()
                self.limpar_campos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir item: {str(e)}", parent=self.root)
        else:
            messagebox.showerror("Erro", "Selecione um item para excluir!", parent=self.root)

    def limpar_campos(self):
        self.var_id.set("")
        self.var_nome.set("")
        self.var_quantidade.set(0)
        self.var_preco.set(0.0)
        self.var_categoria.set("Bebidas")

    def selecionar_item(self, event):
        item = self.tree.focus()
        if item:
            values = self.tree.item(item, "values")
            self.var_id.set(values[0])
            self.var_nome.set(values[1])
            self.var_quantidade.set(values[2])
            self.var_preco.set(values[3])
            self.var_categoria.set(values[4])

if __name__ == "__main__":
    root = Tk()
    obj = estoqueClass(root)
    root.mainloop()