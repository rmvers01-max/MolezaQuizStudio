import customtkinter as ctk


class ProjectsPage(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        ctk.CTkLabel(
            self,
            text="Projetos",
            font=("Arial",28,"bold")
        ).pack(pady=30)
