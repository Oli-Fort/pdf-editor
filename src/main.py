import tkinter as tk
from ui import PDFEditorUi
import customtkinter as ctk


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    editor_ui = PDFEditorUi(root, None)

    root.bind("<Down>", editor_ui.canvas.change_current_page)
    root.bind("<Up>", editor_ui.canvas.change_current_page)
    root.bind("<Control-MouseWheel>", editor_ui.canvas.zoom)

    root.mainloop()


if __name__ == "__main__":
    main()
