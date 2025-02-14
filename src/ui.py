import tkinter as tk
from tkinter import PhotoImage
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pymupdf
from PIL import ImageTk, Image
from pdf import PDF
from canvas import DynamicCanvas


class PDFEditorUi:
    def __init__(self, root, pdf):
        self.root = root
        self.pdf = pdf

        self.root.title("PDF Editor")
        self.root.geometry("1200x800")

        self.create_menu_bar()
        self.create_toolbar()

        self.canvas = DynamicCanvas(self.root)
        self.canvas.pack(expand=True, fill="both")

    def create_menu_bar(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_pdf)
        file_menu.add_command(label="Close", command=self.close_pdf)
        file_menu.add_command(label="Save", command=self.save_pdf)
        file_menu.add_command(label="Save as", command=self.saveas_pdf)

        view_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Single Page")  # TODO
        view_menu.add_command(label="Double Page")  # TODO
        view_menu.add_command(label="Continuous scroll")  # TODO

        tools_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)  # TODO

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, relief=tk.RAISED, padx=5, pady=250)

        text_box_button = tk.Button(toolbar, text="add text box", cursor="hand2", height=2, width=4)
        text_box_button.pack(side="top")

        draw_button = tk.Button(toolbar, text="draw", cursor="pencil", height=2, width=4)
        draw_button.pack(side="top")

        toolbar.pack(side="left", fill="y", anchor="center")

    def open_pdf(self):
        path = askopenfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if not path:
            return

        self.pdf = PDF(path)

        self.canvas.draw_pdf(self.pdf)

    def close_pdf(self):
        self.pdf = None
        self.canvas.draw_pdf(self.pdf)

    def save_pdf(self):
        pass

    def saveas_pdf(self):
        path = asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
