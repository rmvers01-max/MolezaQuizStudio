import customtkinter as ctk


class AIPage(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        ctk.CTkLabel(
            self,
            text="Inteligência Artificial",
            font=("Arial",28,"bold")
        ).pack(pady=30)