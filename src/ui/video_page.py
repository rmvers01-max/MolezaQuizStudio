import customtkinter as ctk


class VideoPage(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        ctk.CTkLabel(
            self,
            text="Editor de Vídeos",
            font=("Arial", 28, "bold")
        ).pack(pady=30)
