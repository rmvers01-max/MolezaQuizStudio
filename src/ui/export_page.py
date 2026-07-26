
import customtkinter as ctk


class ExportPage(ctk.CTkFrame):

	def __init__(self, master):

		super().__init__(master)

		ctk.CTkLabel(
			self,
			text="Exportação",
			font=("Arial",28,"bold")
		).pack(pady=30)
