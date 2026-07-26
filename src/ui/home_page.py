import customtkinter as ctk

class HomePage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        titulo = ctk.CTkLabel(
            self,
            text="🏠 Dashboard",
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=20)

        texto = ctk.CTkLabel(
            self,
            text="Bem-vindo ao Moleza Quiz Studio!"
        )
        texto.pack()