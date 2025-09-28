import tkinter as tk
from tkinter import messagebox

# --- Usuários de exemplo (em produção, buscar em banco de dados) ---
USERS = {
    "admin": "1234",
    "user": "abcd"
}

class LoginApp:
    def __init__(self, master):
        self.master = master
        master.title("Login - Conversor de Moedas")
        master.geometry("300x180")
        master.resizable(False, False)

        # Rótulos
        tk.Label(master, text="Usuário:").pack(pady=(20, 0))
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        tk.Label(master, text="Senha:").pack(pady=(10, 0))
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        # Botão de login
        tk.Button(master, text="Entrar", command=self.login).pack(pady=15)

    def login(self):
        user = self.username_entry.get().strip()
        pwd = self.password_entry.get().strip()

        if USERS.get(user) == pwd:
            messagebox.showinfo("Sucesso", f"Bem-vindo, {user}!")
            # Aqui você pode chamar a próxima janela, ex.: conversor de moedas
            self.master.destroy()
            # iniciar_conversor()  # função futura
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
