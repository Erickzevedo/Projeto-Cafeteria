from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class cardapioClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Novo Cardápio Digital")
        self.root.geometry("800x600")
        self.root.configure(bg="#ff66c4")

        self.categoria_var = StringVar()
        self.nome_var = StringVar()
        self.preco_var = StringVar()

        input_frame = Frame(self.root, bg="#ff66c4")
        input_frame.pack(pady=10)

        Label(input_frame, text="Categoria:", bg="#ff66c4").grid(row=0, column=0, padx=5, pady=5)
        self.categoria_combobox = ttk.Combobox(input_frame, textvariable=self.categoria_var, values=["Selecionar", "Bebidas", "Comidas", "Sobremesas"])
        self.categoria_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.categoria_combobox.set("Selecionar")

        Label(input_frame, text="Nome do Item:", bg="#ff66c4").grid(row=1, column=0, padx=5, pady=5)
        Entry(input_frame, textvariable=self.nome_var).grid(row=1, column=1, padx=5, pady=5)

        Label(input_frame, text="Preço (R$):", bg="#ff66c4").grid(row=2, column=0, padx=5, pady=5)
        Entry(input_frame, textvariable=self.preco_var).grid(row=2, column=1, padx=5, pady=5)

        Button(input_frame, text="Adicionar Item", command=self.adicionar_item, bg="green", fg="white").grid(row=3, column=0, padx=5, pady=10)
        Button(input_frame, text="Deletar Item", command=self.deletar_item, bg="red", fg="white").grid(row=3, column=1, padx=5, pady=10)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Categoria", "Nome", "Preço"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Preço", text="Preço (R$)")
        self.tree.pack(pady=10, padx=10, fill=BOTH, expand=True)

        self.carregar_itens()

    def adicionar_item(self):
        categoria = self.categoria_var.get()
        nome = self.nome_var.get()
        preco = self.preco_var.get()

        if categoria and nome and preco:
            try:
                preco = float(preco)
                con = sqlite3.connect("Cafe.db")
                cur = con.cursor()
        
                cur.execute("INSERT INTO cardapio (categoria, nome, preco) VALUES (?, ?, ?)", (categoria, nome, preco))
                con.commit()
                con.close()
                self.carregar_itens()
                self.categoria_var.set("Selecionar")
                self.nome_var.set("")
                self.preco_var.set("")
                messagebox.showinfo("Sucesso", "Item adicionado ao cardápio!")
            except ValueError:
                messagebox.showerror("Erro", "O preço deve ser um número válido.")
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

    def carregar_itens(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        con = sqlite3.connect("Cafe.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM cardapio")
        rows = cur.fetchall()
        con.close()

        for row in rows:
            self.tree.insert("", "end", values=row)

    def deletar_item(self):
        try:
            selected_item = self.tree.selection()[0]
            item_id = self.tree.item(selected_item)["values"][0]

            con = sqlite3.connect("Cafe.db")
            cur = con.cursor()
            cur.execute("DELETE FROM cardapio WHERE id=?", (item_id,))
            con.commit()
            con.close()

            self.tree.delete(selected_item)
            messagebox.showinfo("Sucesso", "Item deletado com sucesso!")
        except IndexError:
            messagebox.showerror("Erro", "Selecione um item para deletar.")

if __name__ == "__main__":
    root = Tk()
    app = cardapioClass(root)
    root.mainloop()