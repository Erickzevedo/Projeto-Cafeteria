from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class usuariosClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+200+100")
        self.root.title("Lista de Usuários Cadastrados")
        self.root.config(bg="#d9d9d9")
        self.root.focus_force()

        frame_tabela = Frame(self.root, bg="#d9d9d9")
        frame_tabela.place(x=10, y=10, width=1080, height=480)

        scroll_x = Scrollbar(frame_tabela, orient=HORIZONTAL)
        scroll_y = Scrollbar(frame_tabela, orient=VERTICAL)

        self.tabela_usuarios = ttk.Treeview(
            frame_tabela,
            columns=("ID", "Nome", "Email", "Gênero", "Contato", "Nascimento", "Contratação", "Senha", "Tipo", "Endereço"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.tabela_usuarios.xview)
        scroll_y.config(command=self.tabela_usuarios.yview)

        self.tabela_usuarios.column("#0", width=0, stretch=NO)

        self.tabela_usuarios.heading("ID", text="ID")
        self.tabela_usuarios.heading("Nome", text="Nome")
        self.tabela_usuarios.heading("Email", text="Email")
        self.tabela_usuarios.heading("Gênero", text="Gênero")
        self.tabela_usuarios.heading("Contato", text="Contato")
        self.tabela_usuarios.heading("Nascimento", text="Data Nasc.")
        self.tabela_usuarios.heading("Contratação", text="Contratação")
        self.tabela_usuarios.heading("Senha", text="Senha")
        self.tabela_usuarios.heading("Tipo", text="Tipo")
        self.tabela_usuarios.heading("Endereço", text="Endereço")

        self.tabela_usuarios.column("ID", width=50)
        self.tabela_usuarios.column("Nome", width=150)
        self.tabela_usuarios.column("Email", width=150)
        self.tabela_usuarios.column("Gênero", width=80)
        self.tabela_usuarios.column("Contato", width=100)
        self.tabela_usuarios.column("Nascimento", width=100)
        self.tabela_usuarios.column("Contratação", width=100)
        self.tabela_usuarios.column("Senha", width=100)
        self.tabela_usuarios.column("Tipo", width=100)
        self.tabela_usuarios.column("Endereço", width=200)

        self.tabela_usuarios.pack(fill=BOTH, expand=1)

        self.carregar_dados()

    def carregar_dados(self):
        con = sqlite3.connect(database="Cafe.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT * FROM usuario")
            rows = cur.fetchall()
            for item in self.tabela_usuarios.get_children():
                self.tabela_usuarios.delete(item)
            for row in rows:
                self.tabela_usuarios.insert("", "end", values=row)
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {str(ex)}")
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = usuariosClass(root)
    root.mainloop()