import os
import sqlite3
import tkinter as tk
import winsound
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
from PIL import ImageTk, Image
from tkcalendar import DateEntry

# ______________________________ Conexão com o Banco de Dados ______________________________ #

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Database/Return_System.db")
conn = sqlite3.connect(db_path)

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "Database/Return_System.db")


def execute_query(query, args=(), fetchall=False):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
        return cursor.fetchall() if fetchall else cursor.fetchone()


def dql(query):  # select, popular
    return execute_query(query, fetchall=True)


def dml(query):  # inserir, Delete, Update
    execute_query(query)


def lgn(query):  # login
    return execute_query(query)


# ______________________________ Classes de Login e Recuperação ______________________________ #

class LoginApp(tk.Tk):
    WINDOW_WIDTH = 960
    WINDOW_HEIGHT = 540

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('LOGIN (RETURN-SYSTEM)')
        self.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}')
        self.largura = self.winfo_screenwidth()
        self.altura = self.winfo_screenheight()
        self.pos_x = (self.largura - 960) // 2
        self.pos_y = (self.altura - 540) // 2
        self.geometry("+{}+{}".format(self.pos_x, self.pos_y))
        self.resizable(width=False, height=False)
        self.iconbitmap("Imagens/icon.ico")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Page in (Login, Cadastro, Verificacao, Atualizar_Senha, Concluido):
            page_name = Page.__name__
            frame = Page(lparent=container, lcontroller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(background="white")

        self.show_frame(Login.__name__)

    def show_frame(self, page_name, nome=None):
        frame = self.frames[page_name]
        frame.tkraise()
        if nome:
            frame.set_nome(nome)


class Login(tk.Frame):
    def __init__(self, lparent, lcontroller):
        tk.Frame.__init__(self, lparent)
        self.lcontroller = lcontroller

        self.frame = Frame(self, width=350, height=450, bg="white")
        self.frame.place(x=480, y=70)

        self.login = Button(self.frame, text="LOGIN", fg='black', border=0, bg='white', cursor='hand2',
                            font=('calibri', 14, 'bold'),
                            activebackground="white", activeforeground="black")
        self.login.place(x=60, y=5)
        Frame(self.frame, width=57, height=4, bg="#c10f43").place(x=62, y=40)

        self.cadastro = Button(self.frame, text="CADASTRO", border=0, bg='white', fg='gray', cursor='hand2',
                               font=('calibri', 14, 'bold'),
                               activebackground="white", activeforeground="black",
                               command=lambda: lcontroller.show_frame("Cadastro"))
        self.cadastro.place(x=180, y=5)

        self.img = PhotoImage(file=r'Imagens/logo_northconnect.png')
        Label(self, image=self.img, bg="white").place(x=122, y=95)

        # ______________________________ Campo para inserção de dados do usuário! ______________________________

        def on_enter(e):
            if self.usuario.get() == "Usuário":
                self.usuario.delete(0, "end")

        def on_leave(e):
            nome = self.usuario.get()
            if nome == "":
                self.usuario.insert(0, "Usuário")

        self.usuario = Entry(self.frame, width=35, fg='black', border=0, bg='white',
                             font=('Microsoft YaHei UI Light', 11))
        self.usuario.place(x=30, y=80)
        self.usuario.insert(0, 'Usuário')
        self.usuario.bind('<FocusIn>', on_enter)
        self.usuario.bind('<FocusOut>', on_leave)

        Frame(self.frame, width=295, height=2, bg="black").place(x=25, y=107)

        # ______________________________ Campo para inserção da senha do usuário! ______________________________

        def on_enter(e):
            if self.senha.get() == "Senha":
                self.senha.delete(0, "end")
                self.senha.config(show="*")

        def on_leave(e):
            senha = self.senha.get()
            if senha == "":
                self.senha.insert(0, "Senha")
                self.senha.config(show="")

        self.senha = Entry(self.frame, width=35, fg='black', border=0, bg='white', show="",
                           font=('Microsoft YaHei UI Light', 11))
        self.senha.place(x=30, y=150)
        self.senha.insert(0, 'Senha')
        self.senha.bind('<FocusIn>', on_enter)
        self.senha.bind('<FocusOut>', on_leave)
        self.senha.bind('<Return>', self.entrar)

        Frame(self.frame, width=295, height=2, bg="black").place(x=25, y=177)

        # ______________________________ Botões de Registro ______________________________

        self.botao_esqueceu_senha = Button(self.frame, width=15, text='Esqueceu a senha?', border=0, bg='white',
                                           cursor='hand2', fg='gray',
                                           command=lambda: lcontroller.show_frame("Esqueceu_Senha"),
                                           activebackground="white", activeforeground="black")
        self.botao_esqueceu_senha.place(x=215, y=190)

        self.botao_entrar = Button(self.frame, width=39, pady=7, text='Entrar', bg='#c10f43', fg='white',
                                   cursor='hand2', border=0, command=self.entrar_login,
                                   activebackground="#9d0031", activeforeground="black")
        self.botao_entrar.place(x=30, y=225)

        self.label_nao_perfil = Label(self.frame, text="Não tem um perfil?", fg='black', bg='white',
                                      font=('Microsoft YaHei UI Light', 9), activebackground="white",
                                      activeforeground="black")
        self.label_nao_perfil.place(x=75, y=280)

        self.registrar = Button(self.frame, width=9, text='Cadastrar-se', border=0, bg='white', cursor='hand2',
                                fg='#57a1f8', command=lambda: lcontroller.show_frame("Cadastro"),
                                activebackground="white", activeforeground="black")
        self.registrar.place(x=195, y=280)

    # ______________________________ Funções de Login e Senha ______________________________

    def entrar(self, event):
        name = self.usuario.get()
        password = self.senha.get()
        comando = f"SELECT * FROM usuarios WHERE (usuario = '{name}' and senha = '{password}')"

        try:
            if self.usuario.get() == "" or self.senha.get() == "":
                messagebox.showinfo(title='Credenciais Vazias', message='Por favor, preencha os campos solicitados')
                return

            dados = execute_query(comando)
            nome = dados[1]
            senha = dados[2]

            if self.usuario.get() == nome and self.senha.get() == senha:
                username = nome
                self.lcontroller.destroy()
                if __name__ == '__main__':
                    app = App(username=username)
                    app.mainloop()

        except TypeError:
            messagebox.showwarning(title='Credenciais Inválidas', message='Tente novamente ou cadastre um novo perfil')
            return

        try:
            if isinstance(self.usuario, Entry) and isinstance(self.senha, Entry):
                self.usuario.delete(0, END)
                self.senha.delete(0, END)
                self.usuario.focus()
        except TclError:
            pass

    def entrar_login(self):
        name = self.usuario.get()
        password = self.senha.get()
        comando = f"SELECT * FROM usuarios WHERE (usuario = '{name}' and senha = '{password}')"

        try:
            if self.usuario.get() == "" or self.senha.get() == "":
                messagebox.showinfo(title='Credenciais Vazias', message='Por favor, preencha os campos solicitados')
                return

            dados = execute_query(comando)
            nome = dados[1]
            senha = dados[2]

            if self.usuario.get() == nome and self.senha.get() == senha:
                username = nome
                self.lcontroller.destroy()
                if __name__ == '__main__':
                    app = App(username=username)
                    app.mainloop()

        except:
            messagebox.showwarning(title='Credenciais Inválidas', message='Tente novamente ou cadastre um novo perfil')
            return

        try:
            if isinstance(self.usuario, Entry) and isinstance(self.senha, Entry):
                self.usuario.delete(0, END)
                self.senha.delete(0, END)
                self.usuario.focus()
        except TclError:
            pass


class Cadastro(tk.Frame):
    def __init__(self, lparent, lcontroller):
        tk.Frame.__init__(self, lparent)
        self.lcontroller = lcontroller

        self.frame = Frame(self, width=350, height=450, bg="white")
        self.frame.place(x=480, y=70)

        self.login = Button(self.frame, text="LOGIN", border=0, fg='gray', bg='white', cursor='hand2',
                            command=lambda: lcontroller.show_frame("Login"),
                            font=('calibri', 14, 'bold'),
                            activebackground="white", activeforeground="black")
        self.login.place(x=60, y=5)

        self.cadastro = Button(self.frame, text="CADASTRO", border=0, fg='black', bg='white', cursor='hand2',
                               command=lambda: lcontroller.show_frame("Cadastro"),
                               font=('calibri', 14, 'bold'),
                               activebackground="white", activeforeground="black")
        self.cadastro.place(x=180, y=5)
        Frame(self.frame, width=90, height=4, bg="#c10f43").place(x=185, y=40)

        self.img = PhotoImage(file=r'Imagens/logo_northconnect.png')
        Label(self, image=self.img, bg="white").place(x=122, y=95)

        # ______________________________ Campo para inserção de dados do usuário! ______________________________

        def on_enter(e):
            if self.usuario.get() == 'Usuário':
                self.usuario.delete(0, "end")

        def on_leave(e):
            nome = self.usuario.get()
            if nome == "":
                self.usuario.insert(0, "Usuário")

        self.usuario = Entry(self.frame, width=35, fg='black', border=0, bg='white',
                             font=('Microsoft YaHei UI Light', 11))
        self.usuario.place(x=30, y=80)
        self.usuario.insert(0, 'Usuário')
        self.usuario.bind('<FocusIn>', on_enter)
        self.usuario.bind('<FocusOut>', on_leave)

        Frame(self.frame, width=295, height=2, bg="black").place(x=25, y=107)

        # ______________________________ Campo para inserção de dados da matrícula ______________________________

        def on_enter(e):
            if self.matricula.get() == "Matrícula":
                self.matricula.delete(0, "end")

        def on_leave(e):
            nome = self.matricula.get()
            if nome == "":
                self.matricula.insert(0, "Matrícula")

        self.matricula = Entry(self.frame, width=35, fg='black', border=0, bg='white',
                               font=('Microsoft YaHei UI Light', 11))
        self.matricula.place(x=30, y=150)
        self.matricula.insert(0, 'Matrícula')
        self.matricula.bind('<FocusIn>', on_enter)
        self.matricula.bind('<FocusOut>', on_leave)

        Frame(self.frame, width=295, height=2, bg="black").place(x=25, y=177)

        # ______________________________ Campo para inserção de dados de e-mail ______________________________

        def on_enter(e):
            if self.email.get() == "E-mail":
                self.email.delete(0, "end")

        def on_leave(e):
            nome = self.email.get()
            if nome == "":
                self.email.insert(0, "E-mail")

        self.email = Entry(self.frame, width=35, fg='black', border=0, bg='white',
                           font=('Microsoft YaHei UI Light', 11))
        self.email.place(x=30, y=220)
        self.email.insert(0, 'E-mail')
        self.email.bind('<FocusIn>', on_enter)
        self.email.bind('<FocusOut>', on_leave)

        Frame(self.frame, width=295, height=2, bg="black").place(x=25, y=247)

        # ______________________________ Campo para inserção da senha do usuário ______________________________

        def on_enter(e):
            if self.senha.get() == "Senha":
                self.senha.delete(0, "end")
                self.senha.config(show="*")

        def on_leave(e):
            senha = self.senha.get()
            if senha == "":
                self.senha.insert(0, "Senha")
                self.senha.config(show="")

        self.senha = Entry(self.frame, width=35, fg='black', border=0, bg='white',
                           font=('Microsoft YaHei UI Light', 11))
        self.senha.place(x=30, y=290)
        self.senha.insert(0, 'Senha')
        self.senha.bind('<FocusIn>', on_enter)
        self.senha.bind('<FocusOut>', on_leave)

        Frame(self.frame, width=295, height=2, bg="black").place(x=25, y=317)

        # ______________________________ Botões de Registro ______________________________

        Button(self.frame, width=39, pady=7, text='Registrar', bg='#c10f43', fg='white', border=0, cursor='hand2',
               command=self.registrar, activebackground="#9d0031", activeforeground="black").place(x=35, y=344)
        self.label = Label(self.frame, text="Já possui um perfil?", fg='black', bg='white',
                           font=('Microsoft YaHei UI Light', 9))
        self.label.place(x=75, y=397)

        self.registrar = Button(self.frame, width=9, text='Logar-se', border=0, bg='white', cursor='hand2',
                                fg='#57a1f8', command=lambda: lcontroller.show_frame("Login"),
                                activebackground="white", activeforeground="black")
        self.registrar.place(x=195, y=397)

    agora = datetime.now()
    agora_str = agora.strftime("%Y-%m-%d")

    # Funções

    def registrar(self):
        if self.usuario.get() == "" or self.matricula.get() == "" or self.email.get() == "":
            messagebox.showinfo(title='Erro', message='Digite todos os dados')
            return
        try:
            input_usuario = f"""INSERT INTO usuarios (usuario, senha ,matricula, email, cadastragem)
                           VALUES('{self.usuario.get()}', '{self.senha.get()}','{self.matricula.get()}',
                           '{self.email.get()}', '{self.agora_str}')"""

            dml(input_usuario)
            messagebox.showinfo(title=f'Olá, {self.usuario.get()}', message='Cadastro realizado com sucesso!')
            self.lcontroller.show_frame("Login")

        except TypeError:
            messagebox.showinfo(title='Erro', message='Erro ao Inserir')
            return

        try:
            if all(isinstance(attr, Entry) for attr in [self.usuario, self.senha, self.matricula, self.email]):
                self.usuario.delete(0, END)
                self.matricula.delete(0, END)
                self.email.delete(0, END)
                self.senha.delete(0, END)
                self.usuario.focus()
        except TclError:
            pass


class Verificacao(tk.Frame):
    def __init__(self, lparent, lcontroller):
        tk.Frame.__init__(self, lparent)
        self.lcontroller = lcontroller
        self.nome = None

        # ______________________________ Título e Texto ______________________________

        Frame(self, width=960, height=50, bg="black").place(x=0, y=0)

        self.frame = Frame(self, width=450, height=450, bg="white")
        self.frame.place(x=275, y=85)

        self.label_titulo = Label(self.frame, text="VERIFICAÇÃO", fg='black', border=0, bg='white',
                                  font=('calibri', 21, 'bold'), activebackground="white", activeforeground="black")
        self.label_titulo.place(x=136, y=20)
        Frame(self.frame, width=304, height=3, bg="#c10f43").place(x=70, y=60)

        self.label_texto = Label(self.frame,
                                 text="Insira o código que foi enviado ao seu E-mail\n no campo abaixo:",
                                 fg='black', border=0, bg='white', font=('calibri', 12),
                                 activebackground="white", activeforeground="black")
        self.label_texto.place(x=70, y=85)

        # ______________________________ Campo para inserção do Código ______________________________

        def on_enter(e):
            if self.codigo.get() == "Código":
                self.codigo.delete(0, "end")

        def on_leave(e):
            nome = self.codigo.get()
            if nome == "":
                self.codigo.insert(0, "Código")

        self.codigo = Entry(self.frame, width=35, fg='black', border=0, bg='white',
                            font=('Microsoft YaHei UI Light', 11))
        self.codigo.place(x=75, y=165)
        self.codigo.insert(0, 'Código')
        self.codigo.bind('<FocusIn>', on_enter)
        self.codigo.bind('<FocusOut>', on_leave)
        self.codigo.bind('<Return>', self.valid_token_enter)

        Frame(self.frame, width=295, height=2, bg="black").place(x=70, y=192)

        # ______________________________ Botões e Actives ______________________________

        self.botao_verificar = Button(self.frame, width=39, pady=7, text='Verificar', bg='#c10f43', fg='white',
                                      border=0, cursor='hand2', command=self.valid_token, activebackground="#9d0031",
                                      activeforeground="black")
        self.botao_verificar.place(x=77, y=265)

        self.botao_voltar = Button(self.frame, width=10, text='< Retornar', border=0, bg='white',
                                   cursor='hand2', fg='gray', command=lambda: lcontroller.show_frame("Esqueceu_Senha"),
                                   activebackground="white", activeforeground="black")
        self.botao_voltar.place(x=64, y=208)

    def set_nome(self, nome):
        self.nome = nome

    def valid_token(self):
        try:
            codigo_obtido = self.codigo.get()

            comando4 = f"SELECT reset_token FROM return_system.usuarios WHERE usuario = '{self.nome}'"
            codigo_registrado = dql(comando4)[0][0]

            if codigo_registrado == codigo_obtido:
                self.lcontroller.show_frame("Atualizar_Senha", self.nome)
            else:
                messagebox.showinfo(title='Código que você inseriu é inválido',
                                    message='Por favor, verifique se digitou '
                                            'corretamente e tente novamente.')
                return
        except IndexError:
            messagebox.showinfo(title='Erro',
                                message='Algo deu errado, tente novamente.')

    def valid_token_enter(self, event):
        try:
            codigo_obtido = self.codigo.get()

            comando4 = f"SELECT reset_token FROM return_system.usuarios WHERE usuario = '{self.nome}'"
            codigo_registrado = dql(comando4)[0][0]

            if codigo_registrado == codigo_obtido:
                self.lcontroller.show_frame("Atualizar_Senha", self.nome)
            else:
                messagebox.showinfo(title='Código que você inseriu é inválido',
                                    message='Por favor, verifique se digitou '
                                            'corretamente e tente novamente.')
                return
        except IndexError:
            messagebox.showinfo(title='Erro',
                                message='Algo deu errado, tente novamente.')


class Atualizar_Senha(tk.Frame):
    def __init__(self, lparent, lcontroller):
        tk.Frame.__init__(self, lparent)
        self.lcontroller = lcontroller
        self.nome = ''

        # ______________________________ Título e Texto ______________________________

        Frame(self, width=960, height=50, bg="black").place(x=0, y=0)

        self.frame = Frame(self, width=450, height=450, bg="white")
        self.frame.place(x=275, y=85)

        self.label_titulo = Label(self.frame, text="NOVAS CREDENCIAIS", fg='black', border=0, bg='white',
                                  font=('calibri', 21, 'bold'), activebackground="white", activeforeground="black")
        self.label_titulo.place(x=100, y=20)
        Frame(self.frame, width=304, height=3, bg="#c10f43").place(x=70, y=60)

        self.label_texto = Label(self.frame,
                                 text="O código foi verificado!\nDefina sua nova senha",
                                 fg='black', border=0, bg='white', font=('calibri', 12),
                                 activebackground="white", activeforeground="black")
        self.label_texto.place(x=140, y=85)

        # ______________________________ Campo para inserção da nova Senha ______________________________ #

        def on_enter(e):
            if self.senha1.get() == "Nova Senha":
                self.senha1.delete(0, "end")
                self.senha1.config(show="*")

        def on_leave(e):
            senha = self.senha1.get()
            if senha == "":
                self.senha1.insert(0, "Nova Senha")
                self.senha1.config(show="")

        self.senha1 = Entry(self.frame, width=24, fg='black', border=0, bg='white',
                            font=('Microsoft YaHei UI Light', 11))
        self.senha1.place(x=70, y=150)
        self.senha1.insert(0, 'Nova Senha')
        self.senha1.bind('<FocusIn>', on_enter)
        self.senha1.bind('<FocusOut>', on_leave)

        Frame(self.frame, width=295, height=2, bg="black").place(x=65, y=177)

        # ______________________________ Campo para inserção para confirmar nova Senha ______________________________ #

        def on_enter(e):
            if self.senha2.get() == "Confirmar Senha":
                self.senha2.delete(0, "end")
                self.senha2.config(show="*")

        def on_leave(e):
            senha = self.senha2.get()
            if senha == "":
                self.senha2.insert(0, "Confirmar Senha")
                self.senha2.config(show="")

        self.senha2 = Entry(self.frame, width=21, fg='black', border=0, bg='white',
                            font=('Microsoft YaHei UI Light', 11))
        self.senha2.place(x=70, y=220)
        self.senha2.insert(0, 'Confirmar Senha')
        self.senha2.bind('<FocusIn>', on_enter)
        self.senha2.bind('<FocusOut>', on_leave)
        self.senha2.bind('<Return>', self.confirmar)

        Frame(self.frame, width=295, height=2, bg="black").place(x=65, y=247)

        # ______________________________ Botões e Actives ______________________________

        self.botao_confirmar = Button(self.frame, width=39, pady=7, text='Confirmar', bg='#c10f43', fg='white',
                                      border=0, cursor='hand2', command=self.confirmar_senha,
                                      activebackground="#9d0031",
                                      activeforeground="black")
        self.botao_confirmar.place(x=77, y=280)

    def set_nome(self, nome):
        self.nome = nome

    def confirmar_senha(self):
        try:
            senha1 = self.senha1.get()
            senha2 = self.senha2.get()
            if senha1 == senha2:
                comando = f"UPDATE return_system.usuarios SET senha = '{senha2}' WHERE usuario = '{self.nome}';"
                comando2 = f"UPDATE return_system.usuarios SET reset_token = NULL WHERE usuario = '{self.nome}';"
                dml(comando)
                dml(comando2)
                self.lcontroller.show_frame('Concluido')
            else:
                messagebox.showinfo(title='Erro', message='As senhas não coincidem. Por favor, tente novamente.')
        except TypeError:
            print('Ocorreu algum erro!')

    def confirmar(self, event):
        try:
            senha1 = self.senha1.get()
            senha2 = self.senha2.get()
            if senha1 == senha2:
                comando = f"UPDATE return_system.usuarios SET senha = '{senha2}' WHERE usuario = '{self.nome}';"
                comando2 = f"UPDATE return_system.usuarios SET reset_token = NULL WHERE usuario = '{self.nome}';"
                dml(comando)
                dml(comando2)
                self.lcontroller.show_frame('Concluido')
            else:
                messagebox.showinfo(title='Erro', message='As senhas não coincidem. Por favor, tente novamente.')
        except TypeError:
            print('Ocorreu algum erro!')


class Concluido(tk.Frame):
    def __init__(self, lparent, lcontroller):
        tk.Frame.__init__(self, lparent)
        self.lcontroller = lcontroller

        # ______________________________ Título e Texto ______________________________ #

        Frame(self, width=960, height=50, bg="black").place(x=0, y=0)

        self.frame = Frame(self, width=450, height=450, bg="white")
        self.frame.place(x=275, y=85)

        self.label_titulo = Label(self.frame, text="SENHA ATUALIZADA", fg='black', border=0, bg='white',
                                  font=('calibri', 21, 'bold'), activebackground="white", activeforeground="black")
        self.label_titulo.place(x=103, y=20)
        Frame(self.frame, width=304, height=3, bg="#c10f43").place(x=70, y=60)

        self.label_texto = Label(self.frame,
                                 text="Sua senha foi alterada\ncom sucesso!", fg='black', border=0, bg='white',
                                 font=('calibri', 15), activebackground="white", activeforeground="black")
        self.label_texto.place(x=122, y=132)

        # ______________________________ Botões ______________________________ #

        self.botao_login = Button(self.frame, width=39, pady=7, text='LOGIN', bg='#c10f43', fg='white',
                                  border=0, cursor='hand2', command=lambda: lcontroller.show_frame('Login'),
                                  activebackground="#9d0031", activeforeground="black")
        self.botao_login.place(x=77, y=265)


# ______________________________ Classes do Sistema Principal ______________________________ #

class App(tk.Tk):
    WINDOW_WIDTH = 1366
    WINDOW_HEIGHT = 768

    def __init__(self, username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('RETURN-SYSTEM (ORT)')
        self.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}')
        self.largura_tela = self.winfo_screenwidth()
        self.altura_tela = self.winfo_screenheight()
        self.posicao_x = (self.largura_tela - 1366) // 2
        self.posicao_y = (self.altura_tela - 768) // 2
        self.geometry("+{}+{}".format(self.posicao_x, self.posicao_y))
        # self.resizable(width=False, height=False)
        # self.iconbitmap("Imagens/icon.ico")

        self.username = username

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Page in (MainSystem, Saida, Status, Modelos, Historico, Sobre):
            page_name = Page.__name__
            frame = Page(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(background="white")

        self.show_frame(MainSystem.__name__)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

        if page_name == "Status":
            frame.on_show_frame()

        if page_name == "MainSystem":
            frame.popular_entrada_saida()
            frame.atualizar_resultados()
            frame.auto_foco()

        if page_name == "Saida":
            frame.popular_entrada_saida()
            frame.atualizar_resultados()
            frame.auto_foco()

        if page_name == "Historico":
            frame.show_frame_historico()


class MainSystem(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.f1 = None

        # ______________________________ Cabeçalho ______________________________ #

        self.frame_cabecalho = Frame(self)
        self.frame_cabecalho.place(x=0, y=0, width=1366, height=65)
        self.frame_cabecalho.configure(relief='flat', borderwidth="2", background="black")

        self.linha = Label(self.frame_cabecalho)
        self.linha.place(x=0, y=59, width=1366, height=2)
        self.linha.configure(background="#9d0031", compound='left', disabledforeground="#a3a3a3", border=0,
                             font=('Calibri', 14, 'bold'),
                             foreground="#c10f43")

        self.separator = ttk.Separator(self, orient='vertical')
        self.separator.place(x=1165, y=6, height=50)

        self.titulo = Label(self.frame_cabecalho)
        self.titulo.place(x=100, y=15, width=335, height=30)
        self.titulo.configure(background="black", compound='left', disabledforeground="#a3a3a3",
                              font=('Calibri', 32, 'bold'),
                              foreground="#f6f6f8", text='RETURN SYSTEM /')

        self.titulo1 = Label(self.frame_cabecalho)
        self.titulo1.place(x=441, y=8, width=100, height=22)
        self.titulo1.configure(background="black", compound='left', disabledforeground="#a3a3a3",
                               font=('Calibri', 20, 'bold'), anchor=W,
                               foreground="#f6f6f8", text='QA ORT')

        self.titulo2 = Label(self.frame_cabecalho)
        self.titulo2.place(x=441, y=33, width=100, height=22)
        self.titulo2.configure(background="black", compound='left', disabledforeground="#a3a3a3",
                               font=('Calibri', 9, 'bold'), anchor=W,
                               foreground="#f6f6f8", text='[INPUT - OUTPUT]')

        self.label_text = tk.StringVar()
        self.label_text.set("" + self.controller.username)
        self.usuario = Label(self.frame_cabecalho, textvariable=self.label_text)
        self.usuario.place(x=1000, y=8, width=150, height=20)
        self.usuario.configure(background="black", compound='left', disabledforeground="#a3a3a3", anchor=W,
                               font=('Calibri', 14, 'bold'), foreground="#f6f6f8")

        self.sair = Button(self.frame_cabecalho)
        self.sair.place(x=1200, y=18, width=80, height=25)
        self.sair.configure(background="black", compound='left', disabledforeground="#a3a3a3", border=0, cursor='hand2',
                            font=('Calibri', 14, 'bold'), foreground="#b40000", text='LOG OUT',
                            command=self.sair_perfil)

        # ______________________________ Data/Hora ______________________________ #

        self.data_hora = Label(self.frame_cabecalho, font=('calibri', 12, 'bold'), background='black',
                               foreground='#f6f6f8')
        self.data_hora.place(x=1000, y=32)

        self.atualizar_data_hora()

        # ______________________________ Side-Menu ______________________________ #

        self.img1 = Button(self)
        self.img1 = ImageTk.PhotoImage(Image.open(r'Imagens/open.png'))
        self.botao_sm = Button(image=self.img1, border=0, activebackground='black', background='black',
                               borderwidth=0, command=self.side_menu)
        self.botao_sm.place(x=9, y=16)

        # ______________________________ Barra Superior ______________________________ #

        self.frame_barra_superior = Frame(self, width=1366, height=50, background="white")
        self.frame_barra_superior.place(x=0, y=65)

        self.botao_entrada = Button(self.frame_barra_superior, text="ENTRADA")
        self.botao_entrada.configure(fg='black', border=0, bg='white', foreground="black",
                                     cursor='hand2', activeforeground="#b40000", activebackground="white",
                                     font=('Calibri', 14, 'bold'), command=lambda: controller.show_frame("MainSystem"))
        self.botao_entrada.place(x=250, y=5)

        self.separator = ttk.Separator(self.frame_barra_superior, orient='vertical')
        self.separator.place(x=512, y=5, height=40)

        self.botao_status = Button(self.frame_barra_superior, text="STATUS")
        self.botao_status.configure(fg='black', border=0, bg='white', foreground="gray", cursor='hand2',
                                    activeforeground="#b40000", activebackground="white",
                                    font=('Calibri', 12, 'bold'), command=lambda: controller.show_frame("Status"))
        self.botao_status.place(x=655, y=5)

        self.separator = ttk.Separator(self.frame_barra_superior, orient='vertical')
        self.separator.place(x=853, y=5, height=40)

        self.botao_saida = Button(self.frame_barra_superior, text="SAÍDA")
        self.botao_saida.configure(fg='black', border=0, bg='white', foreground="gray", cursor='hand2',
                                   activeforeground="#b40000", activebackground="white",
                                   font=('Calibri', 12, 'bold'), command=lambda: controller.show_frame("Saida"))
        self.botao_saida.place(x=1026, y=5)

        self.linha = Label(self)
        self.linha.place(x=853, y=140, width=5, height=590)
        self.linha.configure(background="#d0cece", compound='left', disabledforeground="#a3a3a3", border=0,
                             font=('Calibri', 14, 'bold'), foreground="#d0cece")

        # ___________________________ Campo para o scanner ___________________________ #

        self.frame_scanner = Frame(self, width=853, height=653, background="white")
        self.frame_scanner.place(x=0, y=115)

        self.label_caixa = Label(self.frame_scanner, width=4, fg='#636363', border=0, bg='white', anchor=W,
                                 text="BOX:", font=('Calibri', 14, 'bold'))
        self.label_caixa.place(x=65, y=60)

        self.entry_caixa = Entry(self.frame_scanner, width=27, fg='black', border=0, bg='white',
                                 font=('Calibri', 14, 'bold'))
        self.entry_caixa.place(x=110, y=60)
        self.entry_caixa.bind("<Return>", self.proximo_entry)

        Frame(self.frame_scanner, width=320, height=2, bg="black").place(x=65, y=90)

        self.label_produto = Label(self.frame_scanner, width=10, fg='#636363', border=0, bg='white', anchor=W,
                                   text="QUALITY:", font=('Calibri', 14, 'bold'))
        self.label_produto.place(x=475, y=60)

        self.entry_produto = Entry(self.frame_scanner, width=24, fg='black', border=0, bg='white',
                                   font=('Calibri', 14, 'bold'))
        self.entry_produto.place(x=555, y=60)
        self.entry_produto.bind("<Return>", self.verificar_codigo)

        Frame(self.frame_scanner, width=320, height=2, bg="black").place(x=475, y=90)

        # ______________________________ Validação (OK, NG, Em teste) ______________________________ #

        self.label_resultado = Label(self.frame_scanner, width=10, fg='#636363', height=2, border=0, bg='white',
                                     anchor=W, text="RESULTADO", font=('Calibri', 28, 'bold'))
        self.label_resultado.place(x=230, y=165)
        # 14b6f1 (azul)
        self.label_condicao = Label(self.frame_scanner, width=10, height=2, fg='#636363', border=0, bg='white',
                                    text="--------", font=('Calibri', 28, 'bold'))
        self.label_condicao.place(x=488, y=165)

        Frame(self.frame_scanner, width=500, height=2, bg="#636363").place(x=180, y=255)

        # ______________________________ Campo das Spec ______________________________ #

        self.label_modelo = Label(self.frame_scanner, width=14, fg='#636363', height=2, border=0, bg='white', anchor=W,
                                  text="Modelo", font=('Calibri', 18))
        self.label_modelo.place(x=160, y=337)

        self.label_resultado_modelo = Label(self.frame_scanner, width=14, height=2, fg='#636363', border=0, bg='white',
                                            text="--------", font=('Calibri', 18))
        self.label_resultado_modelo.place(x=538, y=337)

        Frame(self.frame_scanner, width=730, height=2, bg="#d0cece").place(x=65, y=400)

        self.label_serialnumber = Label(self.frame_scanner, width=14, fg='#636363', height=2, border=0, bg='white',
                                        anchor=W, text="Serial Number", font=('Calibri', 18))
        self.label_serialnumber.place(x=160, y=407)

        self.label_resultado_serialnumber = Label(self.frame_scanner, width=14, height=2, fg='#636363', border=0,
                                                  bg='white', text="--------", font=('Calibri', 18))
        self.label_resultado_serialnumber.place(x=538, y=407)

        Frame(self.frame_scanner, width=730, height=2, bg="#d0cece").place(x=65, y=470)

        self.label_usuario = Label(self.frame_scanner, width=14, fg='#636363', height=2, border=0, bg='white',
                                   anchor=W, text="Inspetor", font=('Calibri', 18))
        self.label_usuario.place(x=160, y=477)

        self.label_resultado_usuario = Label(self.frame_scanner, width=14, height=2, fg='#636363', border=0, bg='white',
                                             text="--------", font=('Calibri', 18))
        self.label_resultado_usuario.place(x=538, y=477)

        Frame(self.frame_scanner, width=730, height=2, bg="#d0cece").place(x=65, y=540)

        self.label_total = Label(self.frame_scanner, width=14, fg='#636363', height=2, border=0, bg='white',
                                 anchor=W, text="Total / Diário", font=('Calibri', 18))
        self.label_total.place(x=160, y=547)

        self.label_resultado_total = Label(self.frame_scanner, width=14, height=2, fg='#636363', border=0,
                                           bg='white', text="--------", font=('Calibri', 18))
        self.label_resultado_total.place(x=538, y=547)

        # ______________________________ Processos ______________________________ #

        self.frame_processo = Frame(self, width=512, height=653, background="white")
        self.frame_processo.place(x=854, y=115)

        self.label_processo = Label(self.frame_processo, width=37, fg='#636363', height=0, border=0, bg='white',
                                    anchor=CENTER, text="PROCESSOS", font=('Calibri', 20, 'bold'))
        self.label_processo.place(x=0, y=24)

        # Treeview Scrollbar

        self.fr_tv = Frame(self.frame_processo, width=588, height=100, bg='white', relief=RAISED)
        self.fr_tv.place(x=-1, y=70)
        self.tv_scroll = ttk.Scrollbar(self.fr_tv)
        self.tv_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview

        self.tv = ttk.Treeview(self.fr_tv, columns=('modelo', 'operacao'),
                               show='headings', height=23, yscrollcommand=self.tv_scroll.set, selectmode="browse")
        self.tv.column('modelo', minwidth=0, width=260, anchor=CENTER)
        self.tv.column('operacao', minwidth=0, width=260, anchor=CENTER)
        self.tv.heading('modelo', text='MODELO')
        self.tv.heading('operacao', text='OPERAÇÃO')
        self.tv.pack()
        self.popular_entrada_saida()

        # ______________________________ Controle do Processo ______________________________ #

        self.check_controle = Frame(self.frame_processo, width=512, height=75, background="white")
        self.check_controle.place(x=0, y=542)

        self.concluido = Label(self.check_controle, width=20, fg='#636363', height=0, border=0, bg='white',
                               anchor=CENTER, relief="groove", highlightbackground="green", text="Concluído:",
                               font=('Calibri', 17))
        self.concluido.place(x=126, y=3)

        self.concluido_resultado = Label(self.check_controle, width=2, fg='#636363', height=0, border=0, bg='white',
                                         anchor=CENTER, relief="groove", highlightbackground="green",
                                         text="0", font=('Calibri', 17))
        self.concluido_resultado.place(x=300, y=3)

        self.pendentes = Label(self.check_controle, width=20, fg='#636363', height=0, border=0, bg='white',
                               anchor=CENTER, relief="groove", highlightbackground="green", text="Pendente:",
                               font=('Calibri', 17))
        self.pendentes.place(x=126, y=35)

        self.pendentes_resultado = Label(self.check_controle, width=2, fg='#636363', height=0, border=0, bg='white',
                                         anchor=CENTER, relief="groove", highlightbackground="green",
                                         text="0", font=('Calibri', 17))
        self.pendentes_resultado.place(x=300, y=35)

        # ______________________________ Funções ______________________________ #

    def side_menu(self):
        self.f1 = Frame(width=268, height=768, bg='#262626')
        self.f1.place(x=0, y=0)

        def bttn(x, y, text, bcolor, fcolor, cmd):
            def on_entera(e):
                botao_inside['background'] = bcolor
                botao_inside['foreground'] = 'white'

            def on_leavea(e):
                botao_inside['background'] = fcolor
                botao_inside['foreground'] = '#edf6f9'

            def cmd_wrapper():
                self.f1.pack_forget()
                cmd()
                self.fechar_side()

            botao_inside = Button(self.f1, text=text, width=38, height=2, fg='#edf6f9', border=0, bg='#262626',
                                  activebackground='#262626', activeforeground="white", command=cmd_wrapper)

            botao_inside.bind("<Enter>", on_entera)
            botao_inside.bind("<Leave>", on_leavea)

            botao_inside.place(x=x, y=y)

        bttn(0, 248, 'S T A T U S', '#2a2b32', '#262626', lambda: self.controller.show_frame("Status"))
        bttn(0, 285, 'E N T R A D A', '#2a2b32', '#262626', lambda: self.controller.show_frame("MainSystem"))
        bttn(0, 322, 'H I S T Ó R I C O', '#2a2b32', '#262626', lambda: self.controller.show_frame("Historico"))
        bttn(0, 357, 'M O D E L O S', '#2a2b32', '#262626', lambda: self.controller.show_frame("Modelos"))
        bttn(0, 392, 'S O B R E', '#2a2b32', '#262626', lambda: self.controller.show_frame("Sobre"))
        bttn(0, 658, 'D E S L O G A R', '#2a2b32', '#262626', self.sair_perfil)
        bttn(0, 695, 'F E C H A R', '#2a2b32', '#262626', self.fechar_app)

        global img2
        img2 = ImageTk.PhotoImage(Image.open(r'Imagens/close.png'))

        Button(self.f1, image=img2, border=0, activebackground='#262626', background='#262626',
               command=self.fechar_side).place(x=9, y=16)

    def fechar_side(self):
        try:
            if self.f1:
                self.f1.destroy()
        except TclError:
            pass

    def fechar_app(self):
        resposta = messagebox.askquestion("Fechar", "Tem certeza que deseja fechar o sistema?")
        if resposta == "yes":
            self.controller.destroy()
        else:
            pass

    def atualizar_data_hora(self):
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.data_hora:
            self.data_hora.config(text=agora)
            self.data_hora.after(1000, self.atualizar_data_hora)

    def sair_perfil(self):
        resposta = messagebox.askquestion("LOG OUT", "Tem certeza que deseja deslogar da conta?")
        if resposta == "yes":
            self.controller.destroy()
            if __name__ == '__main__':
                app = LoginApp()
                app.mainloop()
        else:
            pass

    def proximo_entry(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def verificar_codigo(self, event):
        serial_produto = self.entry_produto.get()
        serial_caixa = self.entry_caixa.get()

        part_number = (serial_caixa[15:])
        serial_number = (serial_produto[10:15])
        operacao = "ENTRADA"
        nome = self.controller.username

        agora = datetime.now()
        agora_str = agora.strftime("%Y-%m-%d %H:%M:%S")
        emissao = agora.strftime("%Y-%m-%d")

        pesquisa_modelo = f"SELECT modelo FROM Produtos WHERE part_number = '{part_number}';"
        result_modelo = dql(pesquisa_modelo)

        if result_modelo:
            modelo = result_modelo[0][0]
        else:
            modelo = "modelo não\nencontrado"

        if serial_produto == serial_caixa:
            if modelo == "modelo não\nencontrado":
                winsound.PlaySound("Sons/erro.wav", winsound.SND_ASYNC)
                self.label_condicao.config(text="MODELO NÃO\nENCONTRADO", foreground="red", width=12,
                                           font=('Calibri', 24, 'bold'))
                self.label_resultado_modelo.configure(text="--------")
                self.label_resultado_serialnumber.configure(text="--------")
                self.label_resultado_usuario.configure(text="--------")
            else:
                pesquisa_id = f"SELECT id FROM Produtos WHERE modelo = '{result_modelo[0][0]}';"
                result_id = dql(pesquisa_id)

                pesquisa_serial = f"SELECT COUNT(*) FROM status WHERE serial_number = '{serial_caixa}' AND operacao = 'ENTRADA'"
                result_serial = dql(pesquisa_serial)

                pesquisa_total_modelos = f"SELECT COUNT(*) FROM status WHERE operacao = 'ENTRADA' AND emissao = '{emissao}';"
                total_modelos_diario = dql(pesquisa_total_modelos)[0][0] + 1

                if result_serial[0][0] > 0:
                    winsound.PlaySound("Sons/erro.wav", winsound.SND_ASYNC)
                    self.label_condicao.config(text="SERIAL JÁ\nEXISTE", foreground="orange", width=12,
                                               font=('Calibri', 24, 'bold'))
                    self.label_resultado_modelo.configure(text="--------")
                    self.label_resultado_serialnumber.configure(text="--------")
                    self.label_resultado_usuario.configure(text="--------")
                    self.label_resultado_total.configure(text="--------")
                else:
                    winsound.PlaySound("Sons/ok.wav", winsound.SND_ASYNC)
                    self.label_condicao.config(text="OK", foreground="green", width=10, font=('Calibri', 28, 'bold'))
                    self.label_resultado_modelo.configure(text=f"{modelo}")
                    self.label_resultado_serialnumber.configure(text=f"{serial_number}")
                    self.label_resultado_usuario.configure(textvariable=self.label_text)
                    self.label_resultado_total.configure(text=total_modelos_diario)

                    input_status = f"""INSERT INTO status (ID, emissao, modelo, serial_number, operacao, data, usuario)
                                    VALUES('{result_id[0][0]}', '{emissao}', '{result_modelo[0][0]}', '{serial_caixa}',
                                    '{operacao}', '{agora_str}', '{nome}')"""

                    input_historico = f"""INSERT INTO historico (ID, emissao, modelo, serial_number, entrada, usuario)
                                    VALUES('{result_id[0][0]}', '{emissao}', '{result_modelo[0][0]}', '{serial_caixa}',
                                    '{agora_str}', '{nome}') """

                    dml(input_status)
                    dml(input_historico)

                    self.popular_entrada_saida()
                    self.atualizar_resultados()

        elif serial_produto != serial_caixa:
            winsound.PlaySound("Sons/erro.wav", winsound.SND_ASYNC)
            self.label_condicao.config(text="SERIAL\nDIFERENTE", foreground="#14b6f1", width=10,
                                       font=('Calibri', 28, 'bold'))
            self.label_resultado_modelo.configure(text="--------")
            self.label_resultado_serialnumber.configure(text="--------")
            self.label_resultado_usuario.configure(text="--------")
            self.label_resultado_total.configure(text="--------")
        else:
            self.label_condicao.config(text="NG", foreground="red")

        self.entry_produto.delete(0, tk.END)
        self.entry_produto.focus_set()
        self.entry_caixa.delete(0, tk.END)
        self.entry_caixa.focus_set()

        event.widget.tk_focusPrev().focus()
        return "break"

    def popular_entrada_saida(self):
        agora = datetime.now()
        emissao = agora.strftime("%Y-%m-%d")

        self.tv.delete(*self.tv.get_children())
        comando = f"SELECT modelo, operacao FROM status WHERE emissao = '{emissao}';"
        linhas = dql(comando)
        for i in linhas:
            self.tv.insert("", END, values=i)

    def atualizar_resultados(self):
        agora = datetime.now()
        emissao = agora.strftime("%Y-%m-%d")
        pesquisa = f"""SELECT serial_number, operacao FROM status WHERE emissao = '{emissao}' 
                    ORDER BY serial_number, operacao;"""
        resultado = dql(pesquisa)
        pendentes = 0
        concluidos = 0
        modelo_anterior = None
        entrada = False
        for linha in resultado:
            modelo_atual = linha[0]
            operacao_atual = linha[1]
            if modelo_atual != modelo_anterior:
                if entrada:
                    pendentes += 1
                entrada = False
            if operacao_atual == "ENTRADA":
                entrada = True
            elif operacao_atual == "SAÍDA":
                concluidos += 1
                entrada = False
            modelo_anterior = modelo_atual
        if entrada:
            pendentes += 1
        self.concluido_resultado.configure(text=str(concluidos))
        self.pendentes_resultado.configure(text=str(pendentes))

    def auto_foco(self):
        self.entry_caixa.focus_set()


class Saida(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # ______________________________ Cabeçalho ______________________________ #

        self.frame_cabecalho = Frame(self)
        self.frame_cabecalho.place(x=0, y=0, width=1366, height=65)
        self.frame_cabecalho.configure(relief='flat', borderwidth="2", background="black")

        self.linha = Label(self.frame_cabecalho)
        self.linha.place(x=0, y=59, width=1366, height=2)
        self.linha.configure(background="#9d0031", compound='left', disabledforeground="#a3a3a3", border=0,
                             font=('Calibri', 14, 'bold'),
                             foreground="#c10f43")

        self.separator = ttk.Separator(self, orient='vertical')
        self.separator.place(x=1165, y=6, height=50)

        self.titulo = Label(self.frame_cabecalho)
        self.titulo.place(x=100, y=15, width=335, height=30)
        self.titulo.configure(background="black", compound='left', disabledforeground="#a3a3a3",
                              font=('Calibri', 32, 'bold'),
                              foreground="#f6f6f8", text='RETURN SYSTEM /')

        self.titulo1 = Label(self.frame_cabecalho)
        self.titulo1.place(x=441, y=8, width=100, height=22)
        self.titulo1.configure(background="black", compound='left', disabledforeground="#a3a3a3",
                               font=('Calibri', 20, 'bold'), anchor=W,
                               foreground="#f6f6f8", text='QA ORT')

        self.titulo2 = Label(self.frame_cabecalho)
        self.titulo2.place(x=441, y=33, width=100, height=22)
        self.titulo2.configure(background="black", compound='left', disabledforeground="#a3a3a3",
                               font=('Calibri', 9, 'bold'), anchor=W,
                               foreground="#f6f6f8", text='[INPUT - OUTPUT]')

        self.label_text = tk.StringVar()
        self.label_text.set("" + self.controller.username)
        self.usuario = Label(self.frame_cabecalho, textvariable=self.label_text)
        self.usuario.place(x=1000, y=8, width=150, height=20)
        self.usuario.configure(background="black", compound='left', disabledforeground="#a3a3a3", anchor=W,
                               font=('Calibri', 14, 'bold'), foreground="#f6f6f8")

        self.sair = Button(self.frame_cabecalho)
        self.sair.place(x=1200, y=18, width=80, height=25)
        self.sair.configure(background="black", compound='left', disabledforeground="#a3a3a3", border=0, cursor='hand2',
                            font=('Calibri', 14, 'bold'), foreground="#b40000", text='LOG OUT',
                            command=self.sair_perfil)

        # ______________________________ Data/Hora ______________________________ #

        self.data_hora = Label(self.frame_cabecalho, font=('calibri', 12, 'bold'), background='black',
                               foreground='#f6f6f8')
        self.data_hora.place(x=1000, y=32)

        self.atualizar_data_hora()

        # ______________________________ Barra Superior ______________________________ #

        self.frame_barra_superior = Frame(self, width=1366, height=50, background="white")
        self.frame_barra_superior.place(x=0, y=65)

        self.botao_entrada = Button(self.frame_barra_superior, text="ENTRADA")
        self.botao_entrada.configure(fg='black', border=0, bg='white', foreground="gray",
                                     cursor='hand2', activeforeground="#b40000", activebackground="white",
                                     font=('Calibri', 12, 'bold'), command=lambda: controller.show_frame("MainSystem"))
        self.botao_entrada.place(x=250, y=5)

        self.separator = ttk.Separator(self.frame_barra_superior, orient='vertical')
        self.separator.place(x=512, y=5, height=40)

        self.botao_status = Button(self.frame_barra_superior, text="STATUS")
        self.botao_status.configure(fg='black', border=0, bg='white', foreground="gray", cursor='hand2',
                                    activeforeground="#b40000", activebackground="white",
                                    font=('Calibri', 12, 'bold'), command=lambda: controller.show_frame("Status"))
        self.botao_status.place(x=655, y=5)

        self.separator = ttk.Separator(self.frame_barra_superior, orient='vertical')
        self.separator.place(x=853, y=5, height=40)

        self.botao_saida = Button(self.frame_barra_superior, text="SAÍDA")
        self.botao_saida.configure(fg='black', border=0, bg='white', foreground="black", cursor='hand2',
                                   activeforeground="#b40000", activebackground="white",
                                   font=('Calibri', 14, 'bold'), command=lambda: controller.show_frame("Saida"))
        self.botao_saida.place(x=1026, y=5)

        self.linha = Label(self)
        self.linha.place(x=512, y=140, width=5, height=590)
        self.linha.configure(background="#d0cece", compound='left', disabledforeground="#a3a3a3", border=0,
                             font=('Calibri', 14, 'bold'), foreground="#d0cece")

        # ___________________________ Campo para o scanner ___________________________ #

        self.frame_scanner = Frame(self, width=853, height=653, background="white")
        self.frame_scanner.place(x=513, y=115)

        self.label_caixa = Label(self.frame_scanner, width=4, fg='#636363', border=0, bg='white', anchor=W,
                                 text="BOX:", font=('Calibri', 14, 'bold'))
        self.label_caixa.place(x=65, y=60)

        self.entry_caixa = Entry(self.frame_scanner, width=27, fg='black', border=0, bg='white',
                                 font=('Calibri', 14, 'bold'))
        self.entry_caixa.place(x=110, y=60)
        self.entry_caixa.bind("<Return>", self.proximo_entry)

        Frame(self.frame_scanner, width=320, height=2, bg="black").place(x=65, y=90)

        self.label_produto = Label(self.frame_scanner, width=10, fg='#636363', border=0, bg='white', anchor=W,
                                   text="QUALITY:", font=('Calibri', 14, 'bold'))
        self.label_produto.place(x=475, y=60)

        self.entry_produto = Entry(self.frame_scanner, width=24, fg='black', border=0, bg='white',
                                   font=('Calibri', 14, 'bold'))
        self.entry_produto.place(x=555, y=60)
        self.entry_produto.bind("<Return>", self.verificar_codigo)

        Frame(self.frame_scanner, width=320, height=2, bg="black").place(x=475, y=90)

        # ______________________________ Validação (OK, NG, Em teste) ______________________________ #

        self.label_resultado = Label(self.frame_scanner, width=10, fg='#636363', height=2, border=0, bg='white',
                                     anchor=W, text="RESULTADO", font=('Calibri', 28, 'bold'))
        self.label_resultado.place(x=230, y=165)
        # 14b6f1 (azul)
        self.label_condicao = Label(self.frame_scanner, width=10, height=2, fg='#636363', border=0, bg='white',
                                    text="--------", font=('Calibri', 28, 'bold'))
        self.label_condicao.place(x=488, y=165)

        Frame(self.frame_scanner, width=500, height=2, bg="#636363").place(x=180, y=255)

        # ______________________________ Campo das Spec ______________________________ #

        self.label_modelo = Label(self.frame_scanner, width=14, fg='#636363', height=2, border=0, bg='white', anchor=W,
                                  text="Modelo", font=('Calibri', 18))
        self.label_modelo.place(x=160, y=337)

        self.label_resultado_modelo = Label(self.frame_scanner, width=14, height=2, fg='#636363', border=0, bg='white',
                                            text="--------", font=('Calibri', 18))
        self.label_resultado_modelo.place(x=538, y=337)

        Frame(self.frame_scanner, width=730, height=2, bg="#d0cece").place(x=65, y=400)

        self.label_serialnumber = Label(self.frame_scanner, width=14, fg='#636363', height=2, border=0, bg='white',
                                        anchor=W, text="Serial Number", font=('Calibri', 18))
        self.label_serialnumber.place(x=160, y=407)

        self.label_resultado_serialnumber = Label(self.frame_scanner, width=14, height=2, fg='#636363', border=0,
                                                  bg='white', text="--------", font=('Calibri', 18))
        self.label_resultado_serialnumber.place(x=538, y=407)

        Frame(self.frame_scanner, width=730, height=2, bg="#d0cece").place(x=65, y=470)

        self.label_usuario = Label(self.frame_scanner, width=14, fg='#636363', height=2, border=0, bg='white',
                                   anchor=W, text="Inspetor", font=('Calibri', 18))
        self.label_usuario.place(x=160, y=477)

        self.label_resultado_usuario = Label(self.frame_scanner, width=14, height=2, fg='#636363', border=0, bg='white',
                                             text="--------", font=('Calibri', 18))
        self.label_resultado_usuario.place(x=538, y=477)

        Frame(self.frame_scanner, width=730, height=2, bg="#d0cece").place(x=65, y=540)

        self.label_total = Label(self.frame_scanner, width=14, fg='#636363', height=2, border=0, bg='white',
                                 anchor=W, text="Total / Diário", font=('Calibri', 18))
        self.label_total.place(x=160, y=547)

        self.label_resultado_total = Label(self.frame_scanner, width=14, height=2, fg='#636363', border=0,
                                           bg='white', text="--------", font=('Calibri', 18))
        self.label_resultado_total.place(x=538, y=547)

        # ______________________________ Processos ______________________________ #

        self.frame_processo = Frame(self, width=512, height=653, background="white")
        self.frame_processo.place(x=0, y=115)

        self.label_processo = Label(self.frame_processo, width=37, fg='#636363', height=0, border=0, bg='white',
                                    anchor=CENTER, text="PROCESSOS", font=('Calibri', 20, 'bold'))
        self.label_processo.place(x=0, y=24)

        # Treeview Scrollbar

        self.fr_tv = Frame(self.frame_processo, width=588, height=100, bg='white', relief=RAISED)
        self.fr_tv.place(x=-1, y=70)
        self.tv_scroll = ttk.Scrollbar(self.fr_tv)
        self.tv_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview

        self.tv = ttk.Treeview(self.fr_tv, columns=('modelo', 'operacao'),
                               show='headings', height=23, yscrollcommand=self.tv_scroll.set, selectmode="browse")
        self.tv.column('modelo', minwidth=0, width=260, anchor=CENTER)
        self.tv.column('operacao', minwidth=0, width=260, anchor=CENTER)
        self.tv.heading('modelo', text='MODELO')
        self.tv.heading('operacao', text='OPERAÇÃO')
        self.tv.pack()
        self.popular_entrada_saida()

        # ______________________________ Controle do Processo ______________________________ #

        self.check_controle = Frame(self.frame_processo, width=512, height=75, background="white")
        self.check_controle.place(x=0, y=542)

        self.concluido = Label(self.check_controle, width=20, fg='#636363', height=0, border=0, bg='white',
                               anchor=CENTER, relief="groove", highlightbackground="green", text="Concluído:",
                               font=('Calibri', 17))
        self.concluido.place(x=126, y=3)

        self.concluido_resultado = Label(self.check_controle, width=2, fg='#636363', height=0, border=0, bg='white',
                                         anchor=CENTER, relief="groove", highlightbackground="green",
                                         font=('Calibri', 17))
        self.concluido_resultado.place(x=300, y=3)

        self.pendentes = Label(self.check_controle, width=20, fg='#636363', height=0, border=0, bg='white',
                               anchor=CENTER, relief="groove", highlightbackground="green", text="Pendente:",
                               font=('Calibri', 17))
        self.pendentes.place(x=126, y=35)

        self.pendentes_resultado = Label(self.check_controle, width=2, fg='#636363', height=0, border=0, bg='white',
                                         anchor=CENTER, relief="groove", highlightbackground="green",
                                         font=('Calibri', 17))
        self.pendentes_resultado.place(x=300, y=35)

    # ______________________________ Funções ______________________________ #

    def atualizar_data_hora(self):
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.data_hora:
            self.data_hora.config(text=agora)
            self.data_hora.after(1000, self.atualizar_data_hora)

    def sair_perfil(self):
        resposta = messagebox.askquestion("LOG OUT", "Tem certeza que deseja deslogar da conta?")
        if resposta == "yes":
            self.controller.destroy()
            if __name__ == '__main__':
                app = LoginApp()
                app.mainloop()
        else:
            pass

    def proximo_entry(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def verificar_codigo(self, event):
        serial_produto = self.entry_produto.get()
        serial_caixa = self.entry_caixa.get()

        part_number = (serial_produto[15:])
        serial_number = (serial_produto[10:15])
        operacao = "SAÍDA"
        nome = self.controller.username
        agora = datetime.now()
        agora_str = agora.strftime("%Y-%m-%d %H:%M:%S")
        emissao = agora.strftime("%Y-%m-%d")

        pesquisa_modelo = f"SELECT modelo FROM Produtos WHERE part_number = '{part_number}';"
        result_modelo = dql(pesquisa_modelo)

        if result_modelo:
            modelo = result_modelo[0][0]
        else:
            modelo = "modelo não\nencontrado"

        if serial_produto == serial_caixa:
            if modelo == "modelo não\nencontrado":
                winsound.PlaySound("Sons/erro.wav", winsound.SND_ASYNC)
                self.label_condicao.config(text="MODELO NÃO\nENCONTRADO", foreground="red", width=12,
                                           font=('Calibri', 24, 'bold'))
                self.label_resultado_modelo.configure(text="--------")
                self.label_resultado_serialnumber.configure(text="--------")
                self.label_resultado_usuario.configure(text="--------")
            else:
                pesquisa_id = f"SELECT id FROM Produtos WHERE modelo = '{result_modelo[0][0]}';"
                result_id = dql(pesquisa_id)

                pesquisa_serial = f"SELECT COUNT(*) FROM status WHERE serial_number = '{serial_caixa}' AND operacao = " \
                                  f"'SAÍDA' "
                result_serial = dql(pesquisa_serial)

                pesquisa_serial2 = f"SELECT COUNT(*) FROM status WHERE serial_number = '{serial_caixa}' AND operacao " \
                                   f"= 'ENTRADA' "
                result_serial2 = dql(pesquisa_serial2)

                pesquisa_total_modelos = f"SELECT COUNT(*) FROM status WHERE operacao = 'SAÍDA' AND emissao = '{emissao}';"
                total_modelos_diario = dql(pesquisa_total_modelos)[0][0] + 1

                if result_serial[0][0] > 0:
                    winsound.PlaySound("Sons/erro.wav", winsound.SND_ASYNC)
                    self.label_condicao.config(text="SERIAL JÁ\nEXISTE", foreground="orange", width=12,
                                               font=('Calibri', 24, 'bold'))
                    self.label_resultado_modelo.configure(text=f"{modelo}")
                    self.label_resultado_serialnumber.configure(text="--------")
                    self.label_resultado_usuario.configure(text="--------")
                    self.label_resultado_total.configure(text="--------")
                elif result_serial2[0][0] == 0:
                    winsound.PlaySound("Sons/erro.wav", winsound.SND_ASYNC)
                    self.label_condicao.config(text="SERIAL SEM\n ENTRADA", foreground="red", width=12,
                                               font=('Calibri', 24, 'bold'))
                    self.label_resultado_modelo.configure(text="--------")
                    self.label_resultado_serialnumber.configure(text="--------")
                    self.label_resultado_usuario.configure(text="--------")
                    self.label_resultado_total.configure(text="--------")
                else:
                    winsound.PlaySound("Sons/ok.wav", winsound.SND_ASYNC)
                    self.label_condicao.config(text="OK", foreground="green", width=10, font=('Calibri', 28, 'bold'))
                    self.label_resultado_modelo.configure(text=f"{modelo}")
                    self.label_resultado_serialnumber.configure(text=f"{serial_number}")
                    self.label_resultado_usuario.configure(textvariable=self.label_text)
                    self.label_resultado_total.configure(text=total_modelos_diario)

                    input_status = f"""INSERT INTO status (ID, emissao, modelo, serial_number, operacao, data, usuario)
                                    VALUES('{result_id[0][0]}', '{emissao}', '{result_modelo[0][0]}', '{serial_caixa}',
                                    '{operacao}', '{agora_str}', '{nome}')"""

                    input_historico = f"""UPDATE historico
                                        SET saida = '{agora_str}'
                                        WHERE serial_number = '{serial_caixa}';"""

                    dml(input_status)
                    dml(input_historico)

                    self.popular_entrada_saida()
                    self.atualizar_resultados()

                    comando_usuario = f"SELECT usuario FROM historico WHERE serial_number = '{serial_caixa}'"
                    usuario_atual = dql(comando_usuario)[0][0]

                    if usuario_atual == nome:
                        pass
                    else:
                        nova_informacao = f" | {nome}"
                        novo_usuario = usuario_atual + nova_informacao
                        input_usuario = f"UPDATE historico SET usuario = '{novo_usuario}' WHERE serial_number = '{serial_caixa}'"
                        dml(input_usuario)

        elif serial_produto != serial_caixa:
            winsound.PlaySound("Sons/erro.wav", winsound.SND_ASYNC)
            self.label_condicao.config(text="SERIAL\nDIFERENTE", foreground="#14b6f1", width=10,
                                       font=('Calibri', 28, 'bold'))
            self.label_resultado_modelo.configure(text="--------")
            self.label_resultado_serialnumber.configure(text="--------")
            self.label_resultado_usuario.configure(text="--------")
        else:
            self.label_condicao.config(text="NG", foreground="red")

        self.entry_produto.delete(0, tk.END)
        self.entry_produto.focus_set()
        self.entry_caixa.delete(0, tk.END)
        self.entry_caixa.focus_set()

        event.widget.tk_focusPrev().focus()
        return "break"

    def popular_entrada_saida(self):
        agora = datetime.now()
        emissao = agora.strftime("%Y-%m-%d")

        self.tv.delete(*self.tv.get_children())
        comando = f"SELECT modelo, operacao FROM status WHERE emissao = '{emissao}';"
        linhas = dql(comando)
        for i in linhas:
            self.tv.insert("", END, values=i)

    def atualizar_resultados(self):
        agora = datetime.now()
        emissao = agora.strftime("%Y-%m-%d")
        pesquisa = f"""SELECT serial_number, operacao FROM status WHERE emissao = '{emissao}' 
                    ORDER BY serial_number, operacao;"""
        resultado = dql(pesquisa)
        pendentes = 0
        concluidos = 0
        modelo_anterior = None
        entrada = False
        for linha in resultado:
            modelo_atual = linha[0]
            operacao_atual = linha[1]
            if modelo_atual != modelo_anterior:
                if entrada:
                    pendentes += 1
                entrada = False
            if operacao_atual == "ENTRADA":
                entrada = True
            elif operacao_atual == "SAÍDA":
                concluidos += 1
                entrada = False
            modelo_anterior = modelo_atual
        if entrada:
            pendentes += 1
        self.concluido_resultado.configure(text=str(concluidos))
        self.pendentes_resultado.configure(text=str(pendentes))

    def auto_foco(self):
        self.entry_caixa.focus_set()


class Status(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Frames

        self.frame_cabecalho = tk.Frame(self)
        self.frame_cabecalho.place(x=0, y=0, width=1366, height=65)
        self.frame_cabecalho.configure(relief='flat', borderwidth="2", background="black")

        self.frame_superior = Frame(self, width=1366, height=85)
        self.frame_superior.place(x=0, y=65)
        self.frame_superior.configure(relief='flat')
        self.frame_superior.configure(borderwidth="2", background="white", highlightbackground="#d9d9d9",
                                      highlightcolor="black")

        self.frame_inferior = Frame(self, width=1366, height=85)
        self.frame_inferior.place(x=0, y=683)
        self.frame_inferior.configure(relief='flat', borderwidth="2", background="white",
                                      highlightbackground="#d9d9d9", highlightcolor="black")

        # ______________________________ cabecalho ______________________________ #

        self.linha = Label(self.frame_cabecalho)
        self.linha.place(x=0, y=59, width=1366, height=2)
        self.linha.configure(background="#9d0031", compound='left', disabledforeground="#a3a3a3", border=0,
                             font=('Calibri', 14, 'bold'),
                             foreground="#c10f43")

        self.separator = ttk.Separator(self, orient='vertical')
        self.separator.place(x=1165, y=6, height=50)

        self.titulo = Label(self.frame_cabecalho)
        self.titulo.place(x=100, y=15, width=335, height=30)
        self.titulo.configure(background="black", compound='left', disabledforeground="#a3a3a3",
                              font=('Calibri', 32, 'bold'),
                              foreground="#f6f6f8", text='RETURN SYSTEM /')

        self.titulo1 = Label(self.frame_cabecalho)
        self.titulo1.place(x=441, y=8, width=100, height=22)
        self.titulo1.configure(background="black", compound='left', disabledforeground="#a3a3a3",
                               font=('Calibri', 20, 'bold'), anchor=W,
                               foreground="#f6f6f8", text='QA ORT')

        self.titulo2 = Label(self.frame_cabecalho)
        self.titulo2.place(x=441, y=33, width=100, height=22)
        self.titulo2.configure(background="black", compound='left', disabledforeground="#a3a3a3",
                               font=('Calibri', 9, 'bold'), anchor=W,
                               foreground="#f6f6f8", text='[INPUT - OUTPUT]')

        self.label_text = tk.StringVar()
        self.label_text.set("" + self.controller.username)
        self.usuario = Label(self.frame_cabecalho, textvariable=self.label_text)
        self.usuario.place(x=1000, y=8, width=150, height=20)
        self.usuario.configure(background="black", compound='left', disabledforeground="#a3a3a3", anchor=W,
                               font=('Calibri', 14, 'bold'), foreground="#f6f6f8")

        self.sair = Button(self.frame_cabecalho)
        self.sair.place(x=1200, y=18, width=80, height=25)
        self.sair.configure(background="black", compound='left', disabledforeground="#a3a3a3", border=0, cursor='hand2',
                            font=('Calibri', 14, 'bold'), command=self.sairperfil,
                            foreground="#b40000", text='LOG OUT')

        # ______________________________ Data/Hora ______________________________ #

        self.data_hora = Label(self.frame_cabecalho, font=('calibri', 12, 'bold'), background='black',
                               foreground='#f6f6f8')
        self.data_hora.place(x=1000, y=32)

        self.atualizar_data_hora()

        # ______________________________ Barra Superior ______________________________ #

        self.frame_barra_superior = Frame(self, width=1366, height=50, background="white")
        self.frame_barra_superior.place(x=0, y=65)

        self.botao_entrada = Button(self.frame_barra_superior, text="ENTRADA")
        self.botao_entrada.configure(fg='black', border=0, bg='white', foreground="gray",
                                     cursor='hand2', activeforeground="#b40000", activebackground="white",
                                     font=('Calibri', 12, 'bold'), command=lambda: controller.show_frame("MainSystem"))
        self.botao_entrada.place(x=250, y=5)

        self.separator = ttk.Separator(self.frame_barra_superior, orient='vertical')
        self.separator.place(x=512, y=5, height=40)

        self.botao_status = Button(self.frame_barra_superior, text="STATUS")
        self.botao_status.configure(fg='black', border=0, bg='white', foreground="black", cursor='hand2',
                                    activeforeground="#b40000", activebackground="white",
                                    font=('Calibri', 14, 'bold'), command=lambda: controller.show_frame("Status"))
        self.botao_status.place(x=650, y=5)

        self.separator = ttk.Separator(self.frame_barra_superior, orient='vertical')
        self.separator.place(x=853, y=5, height=40)

        self.botao_saida = Button(self.frame_barra_superior, text="SAÍDA")
        self.botao_saida.configure(fg='black', border=0, bg='white', foreground="gray", cursor='hand2',
                                   activeforeground="#b40000", activebackground="white",
                                   font=('Calibri', 12, 'bold'), command=lambda: controller.show_frame("Saida"))
        self.botao_saida.place(x=1026, y=5)

        # ______________________________ Botões Superiores ______________________________ #

        self.botao_exportar = Button(self)
        self.botao_exportar.place(x=634, y=105)
        self.botao_exportar.configure(activebackground="white", activeforeground="red", background="white",
                                      borderwidth="1", compound='left', cursor="hand2", disabledforeground="#a3a3a3",
                                      foreground="#636363", highlightbackground="#d9d9d9", highlightcolor="black",
                                      pady="0", border=0, height=2, width=12, font=('calibri', 11),
                                      relief="ridge", command=self.saveExcel, text='Exportar')

        # ______________________________ Campo para Inserção do Modelo ______________________________ #

        self.label_modelo = Label(self.frame_inferior, width=6, fg='#636363', border=0, bg='white',
                                  text="Modelo:", font=('Microsoft YaHei UI Light', 11))
        self.label_modelo.place(x=153, y=20)

        self.modelo = Entry(self.frame_inferior, width=29, fg='#636363', border=0, bg='white',
                            font=('Microsoft YaHei UI Light', 11))
        self.modelo.place(x=210, y=20)
        self.modelo.bind("<KeyRelease>", self.verificar_modelo)

        Frame(self.frame_inferior, width=295, height=2, bg="#636363").place(x=150, y=43)

        # ______________________________ Campo para Inserção do Serial Number ______________________________ #

        self.label_serialnumber = Label(self.frame_inferior, width=5, fg='#636363', border=0, bg='white',
                                        text="Serial:", font=('Microsoft YaHei UI Light', 11))
        self.label_serialnumber.place(x=550, y=20)

        self.serialnumber = Entry(self.frame_inferior, width=30, fg='#636363', border=0, bg='white',
                                  font=('Microsoft YaHei UI Light', 11))
        self.serialnumber.place(x=600, y=20)
        self.serialnumber.bind("<KeyRelease>", self.verificar_serial)

        Frame(self.frame_inferior, width=295, height=2, bg="#636363").place(x=550, y=43)

        # ______________________________ CheckButton para filtrar Entrada e Saída ______________________________ #

        self.separator = ttk.Separator(self.frame_inferior, orient='vertical')
        self.separator.place(x=950, y=13, height=40)

        self.separator2 = ttk.Separator(self.frame_inferior, orient='vertical')
        self.separator2.place(x=1220, y=13, height=40)

        self.check_var_entrada = BooleanVar()
        self.check_var_entrada.set(False)
        self.check_var_saida = BooleanVar()
        self.check_var_saida.set(False)

        self.label_operacao = Label(self.frame_inferior, text="OPERAÇÃO:")
        self.label_operacao.configure(fg='#636363', border=0, bg='white', font=('calibri', 11))
        self.label_operacao.place(x=980, y=20)

        self.check_entrada = Checkbutton(self.frame_inferior, text="ENTRADA", variable=self.check_var_entrada,
                                         command=self.filtrar_operacao)
        self.check_entrada.configure(bg="white", fg='#636363', activebackground="white", activeforeground="black")
        self.check_entrada.place(x=1100, y=3)

        self.check_saida = Checkbutton(self.frame_inferior, text="SAÍDA", variable=self.check_var_saida,
                                       command=self.filtrar_operacao)
        self.check_saida.configure(bg="white", fg='#636363', activebackground="white", activeforeground="black")
        self.check_saida.place(x=1100, y=33)

        # ______________________________ Treeview Scrollbar ______________________________ #

        self.frame_scrollbar = tk.Frame(self)
        self.frame_scrollbar.place(x=-1, y=152)
        self.frame_scrollbar.configure(relief='solid', borderwidth="1", background="black", width=1366, height=530,
                                       highlightbackground="#d9d9d9", highlightcolor="#c0c0c0")

        self.fr_tv = Frame(self.frame_scrollbar, width=588, height=100, bg='white', relief=RAISED)
        self.fr_tv.place(x=0, y=0)

        self.tv_scroll = Scrollbar(self.fr_tv, orient=VERTICAL)
        self.tv_scroll.pack(side=RIGHT, fill=Y)

        self.nenhum_modelo = Label(self, text='', bg='white', foreground='gray',
                                   font=('calibri', 21, 'bold'))
        self.nenhum_modelo.place(x=520, y=350)

        # ______________________________ Treeview ______________________________ #

        self.tv = ttk.Treeview(self.fr_tv,
                               columns=('id', 'emissao', 'model', 'sn', 'operacao', 'data/hora', 'inspetor'),
                               show='headings', height=26, yscrollcommand=self.tv_scroll.set, selectmode="browse")
        self.tv.column('id', minwidth=0, width=110, anchor=CENTER)
        self.tv.column('emissao', minwidth=0, width=140, anchor=CENTER)
        self.tv.column('model', minwidth=0, width=210, anchor=CENTER)
        self.tv.column('sn', minwidth=0, width=244, anchor=CENTER)
        self.tv.column('operacao', minwidth=0, width=230, anchor=CENTER)
        self.tv.column('data/hora', minwidth=0, width=230, anchor=CENTER)
        self.tv.column('inspetor', minwidth=0, width=200, anchor=CENTER)
        self.tv.heading('id', text='ID')
        self.tv.heading('emissao', text='EMISSÃO')
        self.tv.heading('model', text='MODELO')
        self.tv.heading('sn', text='SERIAL NUMBER')
        self.tv.heading('operacao', text='OPERAÇÃO')
        self.tv.heading('data/hora', text='DATA / HORA')
        self.tv.heading('inspetor', text='INSPETOR')
        self.tv.pack()

        comando = "SELECT * FROM status"
        self.modelos = dql(comando)
        self.atualizar_treeview(self.modelos)

    def atualizar_data_hora(self):
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.data_hora:
            self.data_hora.config(text=agora)
            self.data_hora.after(1000, self.atualizar_data_hora)

    def sairperfil(self):
        resposta = messagebox.askquestion("LOG OUT", "Tem certeza que deseja deslogar da conta?")
        if resposta == "yes":
            self.controller.destroy()
            if __name__ == '__main__':
                app = LoginApp()
                app.mainloop()
        else:
            pass

    def saveExcel(self):
        colunas = ['ID', 'Emissão', 'Modelo', 'Serial Number', 'Operaração', 'Data / Hora', 'Inspetor']
        lst = []
        for row_id in self.tv.get_children():
            values = self.tv.item(row_id, 'values')
            lst.append(values)

        df = pd.DataFrame(lst, columns=colunas)
        caminho = r'C:\Users\gusta\PycharmProjects\Return-System\Arquivos excel\historico.xlsx'
        with pd.ExcelWriter(caminho, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)

            worksheet = writer.sheets['Sheet1']
            for i, col in enumerate(df.columns):
                column_len = df[col].astype(str).str.len().max()
                column_len = max(column_len, len(col))
                worksheet.set_column(i, i, column_len + 2)

        os.startfile(caminho)

    def atualizar_treeview(self, modelos_filtrados):
        for child in self.tv.get_children():
            self.tv.delete(child)

        if modelos_filtrados:
            for modelo in modelos_filtrados:
                self.tv.insert("", "end", values=modelo)
            self.nenhum_modelo.config(text='')
        else:
            self.nenhum_modelo.config(text='Nenhum modelo encontrado')

    def verificar_modelo(self, event):
        entrada = self.modelo.get().lower()
        if entrada == '':
            modelos_filtrados = self.modelos
        else:
            modelos_filtrados = []
            for modelo in self.modelos:
                if entrada in modelo[2].lower():
                    modelos_filtrados.append(modelo)
        self.atualizar_treeview(modelos_filtrados)

    def verificar_serial(self, event):
        entrada = self.serialnumber.get().lower()
        if entrada == '':
            modelos_filtrados = self.modelos
        else:
            modelos_filtrados = []
            for modelo in self.modelos:
                if entrada in modelo[3].lower():  # verificar se a entrada está no campo 'sn'
                    modelos_filtrados.append(modelo)
        self.atualizar_treeview(modelos_filtrados)

    def filtrar_operacao(self):
        entrada = self.check_var_entrada.get()
        saida = self.check_var_saida.get()

        if not entrada and not saida:
            modelos_filtrados = self.modelos
            self.check_entrada.configure(bg="white", fg='#636363', activebackground="white", activeforeground="black")
            self.check_saida.configure(bg="white", fg='#636363', activebackground="white", activeforeground="black")

        elif entrada and not saida:
            modelos_filtrados = [modelo for modelo in self.modelos if modelo[4] == 'ENTRADA']
            self.check_entrada.configure(bg="white", fg='black', activebackground="white", activeforeground="black")
        elif not entrada and saida:
            modelos_filtrados = [modelo for modelo in self.modelos if modelo[4] == 'SAÍDA']
            self.check_saida.configure(bg="white", fg='black', activebackground="white", activeforeground="black")
        else:
            modelos_filtrados = self.modelos
            self.check_entrada.configure(bg="white", fg='black', activebackground="white", activeforeground="black")
            self.check_saida.configure(bg="white", fg='black', activebackground="white", activeforeground="black")

        self.atualizar_treeview(modelos_filtrados)

    def on_show_frame(self):
        comando = "SELECT * FROM status"
        self.modelos = dql(comando)
        self.atualizar_treeview(self.modelos)


class Modelos(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Frames

        self.frame_cabecalho = tk.Frame(self)
        self.frame_cabecalho.place(x=0, y=0, width=1366, height=65)
        self.frame_cabecalho.configure(relief='flat', borderwidth="2", background="black")

        self.fr_esquerda = LabelFrame(self, width=375, height=468, bg='white', relief='flat')
        self.fr_esquerda.place(x=90, y=195)

        self.fr_direita = Frame(self, bg='white', relief=RAISED)
        self.fr_direita.place(x=500, y=125)

        self.fr_pesquisar = LabelFrame(self, width=800, height=30, bg='white', border=0)
        self.fr_pesquisar.place(x=500, y=85)

        # ______________________________ cabecalho ______________________________ #

        self.linha = Label(self.frame_cabecalho)
        self.linha.place(x=0, y=59, width=1366, height=2)
        self.linha.configure(background="#9d0031", compound='left', disabledforeground="#a3a3a3", border=0,
                             font=('Calibri', 14, 'bold'),
                             foreground="#c10f43")

        self.separator = ttk.Separator(self, orient='vertical')
        self.separator.place(x=1165, y=6, height=50)

        self.titulo = Label(self.frame_cabecalho)
        self.titulo.place(x=100, y=15, width=335, height=30)
        self.titulo.configure(background="black", compound='left', disabledforeground="#a3a3a3",
                              font=('Calibri', 32, 'bold'),
                              foreground="#f6f6f8", text='RETURN SYSTEM /')

        self.titulo1 = Label(self.frame_cabecalho)
        self.titulo1.place(x=441, y=8, width=100, height=22)
        self.titulo1.configure(background="black", compound='left', disabledforeground="#a3a3a3",
                               font=('Calibri', 20, 'bold'), anchor=W,
                               foreground="#f6f6f8", text='QA ORT')

        self.titulo2 = Label(self.frame_cabecalho)
        self.titulo2.place(x=441, y=33, width=100, height=22)
        self.titulo2.configure(background="black", compound='left', disabledforeground="#a3a3a3",
                               font=('Calibri', 9, 'bold'), anchor=W,
                               foreground="#f6f6f8", text='[INPUT - OUTPUT]')

        self.label_text = tk.StringVar()
        self.label_text.set("" + self.controller.username)
        self.usuario = Label(self.frame_cabecalho, textvariable=self.label_text)
        self.usuario.place(x=1000, y=8, width=150, height=20)
        self.usuario.configure(background="black", compound='left', disabledforeground="#a3a3a3", anchor=W,
                               font=('Calibri', 14, 'bold'), foreground="#f6f6f8")

        self.sair = Button(self.frame_cabecalho)
        self.sair.place(x=1200, y=18, width=80, height=25)
        self.sair.configure(background="black", compound='left', disabledforeground="#a3a3a3", border=0, cursor='hand2',
                            font=('Calibri', 14, 'bold'), command=self.sairperfil,
                            foreground="#b40000", text='LOG OUT')

        # ______________________________ Data/Hora ______________________________ #

        self.data_hora = Label(self.frame_cabecalho, font=('calibri', 12, 'bold'), background='black',
                               foreground='#f6f6f8')
        self.data_hora.place(x=1000, y=32)

        self.atualizar_data_hora()

        # Labels e Entradas

        self.cadastro = Label(self.fr_esquerda, text="CADASTRAR MODELO", border=0, fg='black', bg='white',
                              font=('Microsoft YaHei UI Light', 12, 'bold'))
        self.cadastro.place(x=80, y=30)
        Frame(self.fr_esquerda, width=190, height=3, bg="#c10f43").place(x=80, y=60)

        # ______________________________ Campo para inserção do modelo! ______________________________

        def on_enter(e):
            if self.modelo.get() == "Modelo":
                self.modelo.delete(0, "end")

        def on_leave(e):
            nome = self.modelo.get()
            if nome == "":
                self.modelo.insert(0, "Modelo")

        self.modelo = Entry(self.fr_esquerda, width=35, fg='black', border=0, bg='white',
                            font=('Microsoft YaHei UI Light', 11))
        self.modelo.place(x=30, y=110)
        self.modelo.insert(0, 'Modelo')
        self.modelo.bind('<FocusIn>', on_enter)
        self.modelo.bind('<FocusOut>', on_leave)

        Frame(self.fr_esquerda, width=295, height=2, bg="black").place(x=25, y=137)

        # ______________________________ Campo para inserção do Serial-Number ______________________________

        def on_enter(e):
            if self.serial_number.get() == "Serial-Number":
                self.serial_number.delete(0, "end")

        def on_leave(e):
            nome = self.serial_number.get()
            if nome == "":
                self.serial_number.insert(0, "Serial-Number")

        self.serial_number = Entry(self.fr_esquerda, width=35, fg='black', border=0, bg='white',
                                   font=('Microsoft YaHei UI Light', 11))
        self.serial_number.place(x=30, y=180)
        self.serial_number.insert(0, 'Serial-Number')
        self.serial_number.bind('<FocusIn>', on_enter)
        self.serial_number.bind('<FocusOut>', on_leave)

        Frame(self.fr_esquerda, width=295, height=2, bg="black").place(x=25, y=207)

        # Treeview Scrollbar

        self.fr_tv = Frame(self.fr_direita, width=588, height=100, bg='#f7f7f7', relief=RAISED)
        self.fr_tv.grid(column=1, row=1, rowspan=2, pady=0, padx=1, sticky=NSEW)
        self.tv_scroll = ttk.Scrollbar(self.fr_tv)
        self.tv_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview

        self.tv = ttk.Treeview(self.fr_tv, columns=('id', 'model', 'pn', 'cadastragem'),
                               show='headings', height=26, yscrollcommand=self.tv_scroll.set, selectmode="browse")
        self.tv.column('id', minwidth=0, width=120, anchor=CENTER)
        self.tv.column('model', minwidth=0, width=280, anchor=CENTER)
        self.tv.column('pn', minwidth=0, width=200, anchor=CENTER)
        self.tv.column('cadastragem', minwidth=0, width=200, anchor=CENTER)
        self.tv.heading('id', text='ID')
        self.tv.heading('model', text='MODELO')
        self.tv.heading('pn', text='PART NUMBER')
        self.tv.heading('cadastragem', text='CADASTRAGEM')
        self.tv.pack(side=tk.LEFT, fill=tk.BOTH)
        self.tv_scroll.config(command=self.tv.yview)
        self.popular()

        # Pesquisar

        def on_enter(e):
            if self.pesquisar.get() == "Busca por Modelo:":
                self.pesquisar.delete(0, "end")

        def on_leave(e):
            nome = self.pesquisar.get()
            if nome == "":
                self.pesquisar.insert(0, "Busca por Modelo:")

        self.pesquisar = Entry(self.fr_pesquisar, width=45, fg='black', border=0, bg='white',
                               font=('Microsoft YaHei UI Light', 11))
        self.pesquisar.place(x=0, y=0)
        self.pesquisar.insert(0, 'Busca por Modelo:')
        self.pesquisar.bind('<FocusIn>', on_enter)
        self.pesquisar.bind('<FocusOut>', on_leave)
        self.pesquisar.bind('<Return>', self.filtrar)

        Frame(self.fr_pesquisar, width=495, height=2, bg="black").place(x=0, y=27)

        self.botao_filtrar = Button(self.fr_pesquisar, width=11, text='Filtrar', command=self.filtrar_dados)
        self.botao_filtrar.configure(activebackground="white", activeforeground="red", background="white",
                                     borderwidth="1", compound='left', cursor="hand2", disabledforeground="#a3a3a3",
                                     foreground="black", highlightbackground="#d9d9d9", highlightcolor="black",
                                     pady="0", relief="ridge", border=0)
        self.botao_filtrar.place(x=620, y=4)

        self.botao_mostrar = Button(self.fr_pesquisar, width=11, text='Mostrar Todos', command=self.popular)
        self.botao_mostrar.configure(activebackground="white", activeforeground="red", background="white",
                                     borderwidth="1", compound='left', cursor="hand2", disabledforeground="#a3a3a3",
                                     foreground="black", highlightbackground="#d9d9d9", highlightcolor="black",
                                     pady="0", relief="ridge", border=0)
        self.botao_mostrar.place(x=720, y=4)

        # Botões

        self.botao_adicionar = Button(self.fr_esquerda, width=39, pady=7, text='Adicionar', bg='#c10f43', fg='white',
                                      activebackground="#3f3f3f", activeforeground="white", cursor='hand2',
                                      border=0, command=self.adicionar)
        self.botao_adicionar.place(x=35, y=250)

        self.botao_delete = Button(self, width=20, pady=7, text='Deletar', bg='white', fg='gray', cursor='hand2',
                                   activebackground="white", activeforeground="#c10f43", border=0,
                                   font=('Microsoft YaHei UI Light', 11), command=self.delete)
        self.botao_delete.place(x=680, y=690)

        self.botao_historico = Button(self, width=20, pady=7, text='Histórico', bg='white', fg='gray', cursor='hand2',
                                      activebackground="white", activeforeground="#c10f43", border=0,
                                      font=('Microsoft YaHei UI Light', 11),
                                      command=lambda: controller.show_frame("Historico"))
        self.botao_historico.place(x=950, y=690)

    agora = datetime.now()
    agora_str = agora.strftime("%Y-%m-%d")

    # Funções

    def popular(self):
        self.tv.delete(*self.tv.get_children())
        comando = "SELECT * FROM Produtos"
        linhas = dql(comando)
        for i in linhas:
            self.tv.insert("", END, values=i)

    def adicionar(self):
        serial = self.serial_number.get()
        part_number = serial[15:]

        if not self.modelo.get() or not self.serial_number.get():
            messagebox.showerror(title='Erro', message='Digite todos os dados')
            return

        try:
            # Inserir o produto no banco de dados
            self.inserir_produto(self.modelo.get(), part_number, self.agora_str)
        except Exception as e:
            messagebox.showerror(title='Erro', message=f'Erro ao inserir: {e}')
            return

        messagebox.showinfo(title='Sucesso', message='Produto inserido com sucesso')
        self.popular()
        self.modelo.delete(0, tk.END)
        self.serial_number.delete(0, tk.END)
        self.modelo.focus()

    def inserir_produto(self, modelo, part_number, cadastragem):
        comando = f"INSERT INTO Produtos (modelo, part_number, cadastragem) \
                    VALUES ('{modelo}', '{part_number}', '{cadastragem}')"
        dml(comando)

    def delete(self):
        item = self.tv.selection()[0]
        valores = self.tv.item(item, 'values')
        e_id = valores[0]
        try:
            comando = f'DELETE FROM Produtos WHERE id="{e_id}"'
            dml(comando)
        except:
            messagebox.showinfo(title='Erro', message='Erro ao Deletar')
            return
        self.tv.delete(item)

    def filtrar(self, event):
        self.tv.delete(*self.tv.get_children())
        comando = "SELECT * FROM Produtos  WHERE modelo LIKE '%" + self.pesquisar.get() + "%'"
        linhas = dql(comando)
        for i in linhas:
            self.tv.insert("", "end", values=i)

    def filtrar_dados(self):
        self.tv.delete(*self.tv.get_children())
        comando = "SELECT * FROM Produtos WHERE modelo LIKE '%" + self.pesquisar.get() + "%'"
        linhas = dql(comando)
        for i in linhas:
            self.tv.insert("", "end", values=i)

    def atualizar_data_hora(self):
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.data_hora:
            self.data_hora.config(text=agora)
            self.data_hora.after(1000, self.atualizar_data_hora)

    def sairperfil(self):
        resposta = messagebox.askquestion("LOG OUT", "Tem certeza que deseja deslogar da conta?")
        if resposta == "yes":
            self.controller.destroy()
            if __name__ == '__main__':
                app = LoginApp()
                app.mainloop()
        else:
            pass


class Historico(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # ______________________________ Frames ______________________________ #

        self.frame_cabecalho = Frame(self)
        self.frame_cabecalho.place(x=0, y=0, width=1366, height=65)
        self.frame_cabecalho.configure(relief='flat', borderwidth="2", background="black")

        self.frame_superior = Frame(self, width=1366, height=85)
        self.frame_superior.place(x=0, y=65)
        self.frame_superior.configure(relief='flat')
        self.frame_superior.configure(borderwidth="2", background="white", highlightbackground="#d9d9d9",
                                      highlightcolor="black")

        self.frame_inferior = Frame(self, width=1366, height=85)
        self.frame_inferior.place(x=0, y=683)
        self.frame_inferior.configure(relief='flat', borderwidth="2", background="white",
                                      highlightbackground="#d9d9d9", highlightcolor="black")

        # ______________________________ cabecalho ______________________________ #

        self.linha = Label(self.frame_cabecalho)
        self.linha.place(x=0, y=59, width=1366, height=2)
        self.linha.configure(background="#9d0031", compound='left', disabledforeground="#a3a3a3", border=0,
                             font=('Calibri', 14, 'bold'),
                             foreground="#c10f43")

        self.separator = ttk.Separator(self, orient='vertical')
        self.separator.place(x=1165, y=6, height=50)

        self.titulo = Label(self.frame_cabecalho)
        self.titulo.place(x=100, y=15, width=335, height=30)
        self.titulo.configure(background="black", compound='left', disabledforeground="#a3a3a3",
                              font=('Calibri', 32, 'bold'),
                              foreground="#f6f6f8", text='RETURN SYSTEM /')

        self.titulo1 = Label(self.frame_cabecalho)
        self.titulo1.place(x=441, y=8, width=100, height=22)
        self.titulo1.configure(background="black", compound='left', disabledforeground="#a3a3a3",
                               font=('Calibri', 20, 'bold'), anchor=W,
                               foreground="#f6f6f8", text='QA ORT')

        self.titulo2 = Label(self.frame_cabecalho)
        self.titulo2.place(x=441, y=33, width=100, height=22)
        self.titulo2.configure(background="black", compound='left', disabledforeground="#a3a3a3",
                               font=('Calibri', 9, 'bold'), anchor=W,
                               foreground="#f6f6f8", text='[INPUT - OUTPUT]')

        self.label_text = tk.StringVar()
        self.label_text.set("" + self.controller.username)
        self.usuario = Label(self.frame_cabecalho, textvariable=self.label_text)
        self.usuario.place(x=1000, y=8, width=150, height=20)
        self.usuario.configure(background="black", compound='left', disabledforeground="#a3a3a3", anchor=W,
                               font=('Calibri', 14, 'bold'), foreground="#f6f6f8")

        self.sair = Button(self.frame_cabecalho)
        self.sair.place(x=1200, y=18, width=80, height=25)
        self.sair.configure(background="black", compound='left', disabledforeground="#a3a3a3", border=0,
                            font=('Calibri', 14, 'bold'), command=self.sairperfil, cursor='hand2',
                            foreground="#b40000", text='LOG OUT')

        # ______________________________ Data/Hora ______________________________ #

        self.data_hora = Label(self.frame_cabecalho, font=('calibri', 12, 'bold'), background='black',
                               foreground='#f6f6f8')
        self.data_hora.place(x=1000, y=32)

        self.atualizar_data_hora()

        # ______________________________ Campo para Inserção do Modelo ______________________________ #

        self.label_modelo = Label(self.frame_superior, width=6, fg='black', border=0, bg='white',
                                  text="Modelo:", font=('Microsoft YaHei UI Light', 11))
        self.label_modelo.place(x=153, y=27)

        self.modelo = Entry(self.frame_superior, width=29, fg='black', border=0, bg='white',
                            font=('Microsoft YaHei UI Light', 11))
        self.modelo.place(x=210, y=27)
        self.modelo.bind('<KeyRelease>', self.verificar_modelo)

        Frame(self.frame_superior, width=295, height=2, bg="black").place(x=150, y=50)

        # ______________________________ Campo para Inserção do Serial Number ______________________________ #

        self.label_serialnumber = Label(self.frame_superior, width=5, fg='black', border=0, bg='white',
                                        text="Serial:", font=('Microsoft YaHei UI Light', 11))
        self.label_serialnumber.place(x=500, y=27)

        self.serialnumber = Entry(self.frame_superior, width=30, fg='black', border=0, bg='white',
                                  font=('Microsoft YaHei UI Light', 11))
        self.serialnumber.place(x=550, y=27)
        self.serialnumber.bind('<KeyRelease>', self.verificar_serial)

        Frame(self.frame_superior, width=295, height=2, bg="black").place(x=500, y=50)

        # ______________________________ Filtrar por Data ______________________________

        self.separator = ttk.Separator(self, orient='vertical')
        self.separator.place(x=900, y=80, height=60)

        self.separator = ttk.Separator(self, orient='vertical')
        self.separator.place(x=1200, y=80, height=60)

        self.frame_data = Frame(self.frame_superior, background="white", width=297, height=95)
        self.frame_data.place(x=900, y=0)

        self.label_entrada = Label(self.frame_data, height=0, width=0)
        self.label_entrada.place(x=25, y=15)
        self.label_entrada.configure(background="white", foreground="black", font="-family {Segoe UI} -size 10",
                                     relief="flat", anchor='w', justify='left', text='Entrada:', compound='left')

        self.label_saida = Label(self.frame_data, height=0, width=0)
        self.label_saida.place(x=28, y=45)
        self.label_saida.configure(background="white", foreground="black", font="-family {Segoe UI} -size 10",
                                   relief="flat", anchor='w', justify='left', text='Saída:', compound='left')

        self.dataI = DateEntry(self.frame_data, selectmode='DD/MM/YY')
        self.dataI.configure(width=10, font="-family {Segoe UI} -size 10")
        self.dataI.place(x=85, y=15)

        self.dataF = DateEntry(self.frame_data, selectmode='day')
        self.dataF.configure(width=10, font="-family {Segoe UI} -size 10")
        self.dataF.place(x=85, y=45)

        self.botao_data = Button(self.frame_data)
        self.botao_data.place(x=220, y=30)
        self.botao_data.configure(activebackground="white", activeforeground="red", background="white",
                                  borderwidth="1", compound='left', cursor="hand2", disabledforeground="#a3a3a3",
                                  foreground="black", font=('Microsoft YaHei UI Light', 10), border=0,
                                  pady="0", relief="ridge", command=self.pData, text='''Filtrar''')

        self.historico_date = StringVar()

        # ______________________________ Treeview Scrollbar ______________________________ #
        self.frame_scrollbar = tk.Frame(self)
        self.frame_scrollbar.place(x=-1, y=152)
        self.frame_scrollbar.configure(relief='solid', borderwidth="1", background="black", width=1366, height=530,
                                       highlightbackground="#d9d9d9", highlightcolor="#c0c0c0")

        self.fr_tv = Frame(self.frame_scrollbar, width=588, height=100, bg='white', relief=RAISED)
        self.fr_tv.place(x=0, y=0)

        self.tv_scroll = Scrollbar(self.fr_tv, orient=VERTICAL)
        self.tv_scroll.pack(side=RIGHT, fill=Y)

        self.nenhum_modelo = Label(self, text='', bg='white', foreground='gray',
                                   font=('calibri', 21, 'bold'))
        self.nenhum_modelo.place(x=520, y=350)

        # ______________________________ Treeview ______________________________ #

        self.tv = ttk.Treeview(self.fr_tv,
                               columns=('id', 'emissao', 'model', 'sn', 'entrada', 'saida', 'inspetor'),
                               show='headings', height=26, yscrollcommand=self.tv_scroll.set, selectmode="browse")
        self.tv.column('id', minwidth=0, width=100, anchor=CENTER)
        self.tv.column('emissao', minwidth=0, width=200, anchor=CENTER)
        self.tv.column('model', minwidth=0, width=200, anchor=CENTER)
        self.tv.column('sn', minwidth=0, width=244, anchor=CENTER)
        self.tv.column('entrada', minwidth=0, width=210, anchor=CENTER)
        self.tv.column('saida', minwidth=0, width=210, anchor=CENTER)
        self.tv.column('inspetor', minwidth=0, width=200, anchor=CENTER)
        self.tv.heading('id', text='ID')
        self.tv.heading('emissao', text='EMISSÃO')
        self.tv.heading('model', text='MODELO')
        self.tv.heading('sn', text='SERIAL NUMBER')
        self.tv.heading('entrada', text='ENTRADA')
        self.tv.heading('saida', text='SAÍDA')
        self.tv.heading('inspetor', text='INSPETOR')
        self.tv.pack()

        comando = "SELECT * FROM historico"
        self.modelos = dql(comando)
        self.atualizar_treeview(self.modelos)

        # ______________________________ Botões Inferiores ______________________________ #

        self.botao_exportar = Button(self.frame_inferior)
        self.botao_exportar.place(relx=0.33, rely=0.211, height=24, width=137)
        self.botao_exportar.configure(activebackground="white", activeforeground="red", background="white",
                                      borderwidth="1", compound='left', cursor="hand2", disabledforeground="#a3a3a3",
                                      foreground="gray", highlightbackground="#d9d9d9", highlightcolor="black",
                                      pady="0", border=0,
                                      relief="ridge", command=self.saveExcel, text='Exportar Histórico')

        self.botao_cadastrar = Button(self.frame_inferior)
        self.botao_cadastrar.place(relx=0.525, rely=0.211, height=24, width=137)
        self.botao_cadastrar.configure(activebackground="white", activeforeground="red",
                                       background="white", borderwidth="1", compound='left', cursor="hand2",
                                       disabledforeground="#a3a3a3", foreground="gray", border=0,
                                       highlightbackground="#000000", highlightcolor="black", pady="0", relief="ridge",
                                       command=lambda: controller.show_frame("Modelos"),
                                       text='Cadastrar Novo Modelo')

    # ______________________________ Funções/Atributos ______________________________ #

    def saveExcel(self):
        colunas = ['ID', 'Emissão', 'Modelo', 'Serial Number', 'Entrada', 'Saída', 'Inspetor']
        lst = []
        for row_id in self.tv.get_children():
            values = self.tv.item(row_id, 'values')
            lst.append(values)

        df = pd.DataFrame(lst, columns=colunas)
        caminho = r'C:\Users\gusta\PycharmProjects\Return-System\Arquivos excel\historico.xlsx'
        with pd.ExcelWriter(caminho, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)

            worksheet = writer.sheets['Sheet1']
            for i, col in enumerate(df.columns):
                column_len = df[col].astype(str).str.len().max()
                column_len = max(column_len, len(col))
                worksheet.set_column(i, i, column_len + 2)

        os.startfile(caminho)

    def pData(self):
        dt = self.dataI.get_date()
        s = dt.strftime("%Y-%m-%d")
        dt2 = self.dataF.get_date()
        f = dt2.strftime("%Y-%m-%d")
        self.tv.delete(*self.tv.get_children())
        comando = f"SELECT * FROM historico WHERE entrada BETWEEN '{s}' AND '{f}'"
        linha = dql(comando)

        for i in linha:
            self.tv.insert("", "end", values=i)

    def atualizar_data_hora(self):
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.data_hora:
            self.data_hora.config(text=agora)
            self.data_hora.after(1000, self.atualizar_data_hora)

    def sairperfil(self):
        resposta = messagebox.askquestion("LOG OUT", "Tem certeza que deseja deslogar da conta?")
        if resposta == "yes":
            self.controller.destroy()
            if __name__ == '__main__':
                app = LoginApp()
                app.mainloop()
        else:
            pass

    def atualizar_treeview(self, modelos_filtrados):
        for child in self.tv.get_children():
            self.tv.delete(child)

        if modelos_filtrados:
            for modelo in modelos_filtrados:
                self.tv.insert("", "end", values=modelo)
            self.nenhum_modelo.config(text='')
        else:
            self.nenhum_modelo.config(text='Nenhum modelo encontrado')

    def verificar_modelo(self, event):
        entrada = self.modelo.get().lower()
        if entrada == '':
            modelos_filtrados = self.modelos
        else:
            modelos_filtrados = []
            for modelo in self.modelos:
                if entrada in modelo[2].lower():
                    modelos_filtrados.append(modelo)
        self.atualizar_treeview(modelos_filtrados)

    def verificar_serial(self, event):
        entrada = self.serialnumber.get().lower()
        if entrada == '':
            modelos_filtrados = self.modelos
        else:
            modelos_filtrados = []
            for modelo in self.modelos:
                if entrada in modelo[3].lower():  # verificar se a entrada está no campo 'sn'
                    modelos_filtrados.append(modelo)
        self.atualizar_treeview(modelos_filtrados)

    def show_frame_historico(self):
        comando = "SELECT * FROM historico"
        self.modelos = dql(comando)
        self.atualizar_treeview(self.modelos)


class Sobre(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # ______________________________ Frames ______________________________ #

        self.frame_cabecalho = tk.Frame(self)
        self.frame_cabecalho.place(x=0, y=0, width=1366, height=65)
        self.frame_cabecalho.configure(relief='flat', borderwidth="2", background="black")

        # ______________________________ Labels ______________________________ #

        self.img = PhotoImage(file=r'Imagens/iconeg.png')
        Label(self, image=self.img, bg="white").place(x=452, y=85)

        self.credito_label = Label(self, text="""Direitos Autorais © 2023 North Connect. Todos os direitos 
        reservados.\n\nEste sistema foi desenvolvido por Gustavo Celso, com o objetivo de melhorar os processos de 
        entrada e saída da empresa. A cópia, reprodução ou distribuição não autorizada deste sistema é estritamente 
        proibida.""")
        self.credito_label.config(bg="white")
        self.credito_label.place(x=362, y=630)


# ______________________________ Inicialização do Sistema ______________________________ #

if __name__ == '__main__':
    root = LoginApp()
    root.mainloop()
