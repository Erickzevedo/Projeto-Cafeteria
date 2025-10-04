from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
from novoUsuario import usuarioClass
import sqlite3
import os


class login_Sistema:
    def __init__(self, root):
        self.root = root
        self.width = 1000
        self.height = 600

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        blank_space = " "
        self.root.title(110 * blank_space + "Coffee Urach | Projeto Lab Programação")
        self.root.config(bg="#d9d9d9")

        self.logo_image = ImageTk.PhotoImage(file="imagens/cafezin.png")
        self.lbl_logo_image = Label(self.root, image=self.logo_image, bd=0).place(x=60, y=50)

        self.idusuario = StringVar()
        self.password = StringVar()

        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_frame.place(x=600, width=400, height=620)

        titulo = Label(login_frame, text="SEJA\n BEM VINDO", font=("times new roman", 30, "bold"), bg="white", fg="#ff66c4").place(x=0, y=50, relwidth=1)

        lbl_idusuario = Label(login_frame, text="Usuário", font=("times new roman", 15, "bold"), bg="white", fg="#ff66c4").place(x=50, y=200)
        txt_usuario = Entry(login_frame, textvariable=self.idusuario, font=("times new roman", 15), bg="#d9d9d9").place(x=50, y=230, width=300)

        lbl_senha = Label(login_frame, text="Senha", font=("times new roman", 15, "bold"), bg="White", fg="#ff66c4").place(x=50, y=300)
        txt_senha = Entry(login_frame, textvariable=self.password, show="*", font=("times new roman", 15), bg="#d9d9d9").place(x=50, y=330, width=300)

        btn_login = Button(login_frame, command=self.login, text="Entrar", compound=LEFT, font=("times new roman", 12), bg="#ff66c4", activebackground="#ff66c4", fg="black", cursor="hand2") 
        btn_login.place(x=50, y=480, width=300, height=35)

        btn_novousuario = Button(login_frame, command=self.usuario, text="Registrar usuário", compound=LEFT, font=("times new roman", 12), bg="#ff66c4", activebackground="#ff66c4", fg="black", cursor="hand2")
        btn_novousuario.place(x=50, y=530, width=300, height=35)


    def login(self):
        con = sqlite3.connect(database=r'Cafe.db')
        cur = con.cursor()
        try:
            if self.idusuario.get() == "" or self.password.get() == "":
                messagebox.showerror("Erro", "TODOS OS CAMPOS SÃO OBRIGATÓRIOS", parent=self.root)
            else:
                cur.execute("SELECT utype FROM usuario WHERE uid=? AND senha=?", (self.idusuario.get(), self.password.get()))
                user = cur.fetchone()
                if user is None:
                    messagebox.showerror("Erro", "NOME DE USUÁRIO OU SENHA INVÁLIDOS", parent=self.root)
                else:
                    if user[0] == "Admin":
                        self.root.destroy()
                        os.system("python painel_adminstrador.py")
                    else:
                        self.root.destroy()
                        os.system("python painel_adminstrador.py")
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro devido a: {str(ex)}", parent=self.root)

    def usuario(self):
        self.new_win = Toplevel(self.root)
        self.ne_obj = usuarioClass(self.new_win)


root = Tk()
obj = login_Sistema(root)
root.mainloop()