import customtkinter as ctk
from tkinter import filedialog


class MolezaQuizStudio(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Configuração da janela
        self.title("🦥 Moleza Quiz Studio")
        self.geometry("900x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Título
        self.titulo = ctk.CTkLabel(
            self,
            text="🦥 Moleza Quiz Studio",
            font=("Arial", 28, "bold")
        )

        self.titulo.pack(pady=30)

        # Botão
        self.botao = ctk.CTkButton(
            self,
            text="Selecionar Planilha",
            command=self.selecionar_planilha
        )

        self.botao.pack(pady=20)

        # Nome do arquivo
        self.arquivo_label = ctk.CTkLabel(
            self,
            text="Nenhuma planilha selecionada"
        )

        self.arquivo_label.pack(pady=10)

        # Status
        self.status = ctk.CTkLabel(
            self,
            text="Status: Aguardando..."
        )

        self.status.pack(pady=10)

    def selecionar_planilha(self):

        caminho = filedialog.askopenfilename(

            title="Selecione uma planilha",

            filetypes=[
                ("Planilhas Excel", "*.xlsx")
            ]
        )

        if caminho:

            self.arquivo_label.configure(
                text=caminho
            )

            self.status.configure(
                text="✅ Planilha carregada!"
            )