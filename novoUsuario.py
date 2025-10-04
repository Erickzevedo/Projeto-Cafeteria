from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class usuarioClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1080x300+220+130")
        blank_space = " "
        self.root.title(110 * blank_space + "Coffee Urach | Projeto Lab Programação")
        self.root.config(bg="#d9d9d9")
        self.root.focus_force()

        self.var_usu_id = StringVar()
        self.var_genero = StringVar()
        self.var_contato = StringVar()
        self.var_nome = StringVar()
        self.var_nasc = StringVar()
        self.var_contr = StringVar()
        self.var_email = StringVar()
        self.var_senha = StringVar()
        self.var_utype = StringVar()

        title = Label(self.root, text="Dados do Usuário", font=("Times new roman", 15, "bold"), bg="#ff66c4", fg="black", bd=3).place(x=50, y=10, width=1000)

        lbl_empid = Label(self.root, text="ID Usuário", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black").place(x=50, y=60)
        lbl_genero = Label(self.root, text="Gênero", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black").place(x=370, y=60)
        lbl_contato = Label(self.root, text="Contato", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black").place(x=750, y=60)

        txt_empid = Entry(self.root, textvariable=self.var_usu_id, font=("Times new roman", 14)).place(x=150, y=60, width=180)
        txt_gender = Entry(self.root, textvariable=self.var_genero, font=("Times new roman", 14), bg="white").place(x=450, y=60, width=180)
        txt_contact = Entry(self.root, textvariable=self.var_contato, font=("Times new roman", 14), bg="white").place(x=850, y=60, width=180)

        lbl_name = Label(self.root, text="Nome", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black").place(x=50, y=100)
        lbl_nasc = Label(self.root, text="Data Nasc", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black").place(x=370, y=100)
        lbl_contrato = Label(self.root, text="Inic Contrato", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black").place(x=750, y=100)

        txt_name = Entry(self.root, textvariable=self.var_nome, font=("Times new roman", 14), bg="white").place(x=150, y=100, width=180)
        txt_nasc = Entry(self.root, textvariable=self.var_nasc, font=("Times new roman", 14), bg="white").place(x=450, y=100, width=180)
        txt_contrato = Entry(self.root, textvariable=self.var_contr, font=("Times new roman", 14), bg="white").place(x=850, y=100, width=180)

        lbl_email = Label(self.root, text="Email", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black").place(x=50, y=140)
        lbl_senha = Label(self.root, text="Senha", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black").place(x=370, y=140)
        lbl_utype = Label(self.root, text="Usuário", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black").place(x=750, y=140)

        txt_email = Entry(self.root, textvariable=self.var_email, font=("Times new roman", 14), bg="white").place(x=150, y=140, width=180)
        txt_senha = Entry(self.root, textvariable=self.var_senha, font=("Times new roman", 14), bg="white").place(x=450, y=140, width=180)

        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=("Administrador", "Funcionário"), state="readonly", justify=CENTER, font=("Times new roman", 12, "bold"))
        cmb_utype.place(x=850, y=140, width=180)
        cmb_utype.current(0)

        lbl_endereço = Label(self.root, text="Endereço", font=("Times new roman", 12, "bold"), bg="#d9d9d9", fg="black").place(x=50, y=180)

        self.txt_endereço = Text(self.root, font=("Times new roman", 12, "bold"), bg="white")
        self.txt_endereço.place(x=150, y=180, width=300, height=60)

        btn_add = Button(self.root, text="Salvar", command=self.add, font=("Times new roman", 15), bg="#ff66c4", fg="black", bd=0, cursor="hand2").place(x=930, y=250, width=110, height=28)

    def add(self):
        con = sqlite3.connect(database=r"Cafe.db")
        cur = con.cursor()
        try:
            if self.var_usu_id.get() == "":
                messagebox.showerror("Erro", "ID do funcionário necessária", parent=self.root)
            else:
                cur.execute("SELECT * FROM usuario WHERE uid=?", (self.var_usu_id.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Erro", "Esta ID de funcionário já foi atribuída, tente uma ID diferente", parent=self.root)
                else:
                    cur.execute("""
                        INSERT INTO usuario 
                        (uid, nome, email, genero, contato, datanascimento, datacontrataçao, senha, utype, endereço) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        self.var_usu_id.get(),
                        self.var_nome.get(),
                        self.var_email.get(),
                        self.var_genero.get(),
                        self.var_contato.get(),
                        self.var_nasc.get(),
                        self.var_contr.get(),
                        self.var_senha.get(),
                        self.var_utype.get(),
                        self.txt_endereço.get('1.0', END).strip(),
                    ))
                    con.commit()
                    messagebox.showinfo("Sucesso", "Funcionário adicionado com sucesso", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro devido a : {str(ex)} ", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect("Cafe.db")
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM usuario WHERE uid=?", (self.var_usu_id.get(),))
            con.commit()
            if cur.rowcount > 0:
                messagebox.showinfo("Sucesso", "Registro deletado com sucesso!")
            else:
                messagebox.showwarning("Aviso", "Nenhum registro encontrado para deletar.")
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao deletar: {str(ex)}")
        finally:
            con.close()

    def get_data(self, ev):
        f = self.UsuarioTabela.focus()
        content = (self.UsuarioTabela.item(f))
        row = content['values']
        self.var_usu_id.set(row[0])
        self.var_nome.set(row[1])
        self.var_email.set(row[2])
        self.var_genero.set(row[3])
        self.var_contato.set(row[4])
        self.var_nasc.set(row[5])
        self.var_contr.set(row[6])
        self.var_senha.set(row[7])
        self.var_utype.set(row[8])
        self.txt_endereço.delete("1.0", END)
        self.txt_endereço.insert(END, row[9])


if __name__ == "__main__":
    root = Tk()
    obj = usuarioClass(root)
    root.mainloop()