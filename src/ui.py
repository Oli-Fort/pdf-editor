import tkinter as tk
from tkinter import PhotoImage
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pymupdf
from PIL import ImageTk, Image
from pdf import PDF
from canvas import DynamicCanvas
import webcolors
import customtkinter as ctk
from CTkMenuBar import *


class PDFEditorUi:
    def __init__(self, root, pdf):
        self.highlight_img = None
        self.textbox_img = None
        self.draw_img = None
        self.root = root
        self.mode = "normal"
        self.pdf = pdf

        self.root.title("PDF Editor")
        self.root.geometry("1200x800")

        self.create_menu_bar()
        self.create_toolbar()

        self.canvas = DynamicCanvas(self.root)
        self.canvas.pack(expand=True, fill="both")

    def create_menu_bar(self):
        menu_bar = CTkMenuBar(master=self.root)
        self.root.configure(menu=menu_bar)

        file_menu = menu_bar.add_cascade("File")
        file_menu_dropdown = CustomDropdownMenu(widget=file_menu, corner_radius=10)
        file_menu_dropdown.add_option(option="Open", command=self.open_pdf)
        file_menu_dropdown.add_option(option="Save", command=self.save_pdf)
        file_menu_dropdown.add_option(option="Save as", command=self.saveas_pdf)
        file_menu_dropdown.add_option(option="Close", command=self.close_pdf)

        view_menu = menu_bar.add_cascade("View")
        view_menu_dropdown = CustomDropdownMenu(widget=view_menu)
        view_menu_dropdown.add_option(option="Single Page", command=lambda: self.canvas.change_view_mode("single"))
        view_menu_dropdown.add_option(option="Double Page", command=lambda: self.canvas.change_view_mode("double"))
        view_menu_dropdown.add_option(option="Continuous Scroll", command=lambda: self.canvas.change_view_mode("scroll"))

        tools_menu = menu_bar.add_cascade("Tools")
        tools_menu_dropdown = CustomDropdownMenu(widget=tools_menu)
        tools_menu_dropdown.add_option(option="Appearance")
        tools_menu_dropdown.add_option(option="Draw settings", command=lambda:self.display_draw_settings())
        tools_menu_dropdown.add_option(option="Highlight settings")
        tools_menu_dropdown.add_option(option="Textbox settings")

    def create_toolbar(self):
        toolbar = ctk.CTkFrame(self.root, fg_color="gray10")

        self.textbox_img = tk.PhotoImage(file="cursors/textbox_img.png")
        self.textbox_img = self.textbox_img.subsample(4, 4)
        text_box_button = ctk.CTkButton(toolbar,
                                        text="",
                                        image=self.textbox_img,
                                        command=self.set_textbox_mode,
                                        cursor="hand2",
                                        height=30, width=30)
        text_box_button.pack(side="top", pady=2.5, padx=2.5)

        self.draw_img = tk.PhotoImage(file="cursors/pen_img.png")
        self.draw_img = self.draw_img.subsample(4, 4)
        draw_button = ctk.CTkButton(toolbar,
                                    text="",
                                    image=self.draw_img,
                                    command=self.set_draw_mode,
                                    cursor="hand2",
                                    height=30, width=30)
        draw_button.pack(side="top", pady=2.5, padx=2.5)

        self.highlight_img = tk.PhotoImage(file="cursors/highlighter_img.png")
        self.highlight_img = self.highlight_img.subsample(4, 4)
        highlight_button = ctk.CTkButton(toolbar,
                                         text="",
                                         image=self.highlight_img,
                                         command=self.set_highlight_mode,
                                         cursor="hand2",
                                         height=30, width=30)
        highlight_button.pack(side="top", pady=2.5, padx=2.5)

        toolbar.pack(side="left", anchor="w")

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
        self.pdf.save()

    def saveas_pdf(self):
        path = asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        self.pdf.save(path)

    def display_draw_settings(self):
        checkbox_frame = ctk.CTkFrame(self.root)
        checkbox_frame.pack(side="right", fill="y")

        color_frame = ctk.CTkFrame(checkbox_frame)
        color_frame.pack()

        checkbox = ctk.CTkCheckBox(color_frame)
        checkbox.grid(row=0, column=0)


    def set_textbox_mode(self):
        cursor = "" if self.root["cursor"] == "@cursors/textbox.ico" else "@cursors/textbox.ico"
        self.root.config(cursor=cursor)

        self.canvas.edit_mode = "normal" if self.root["cursor"] == "" else "textbox"
        if self.canvas.edit_mode == "normal":
            return

    def set_draw_mode(self):
        cursor = "" if self.root["cursor"] == "@cursors/pen.ico" else "@cursors/pen.ico"
        self.root.config(cursor=cursor)

        self.canvas.edit_mode = "normal" if self.root["cursor"] == "" else "draw"
        if self.canvas.edit_mode == "normal":
            return

    def set_highlight_mode(self):
        cursor = "" if self.root["cursor"] == "xterm" else "xterm"
        self.root.config(cursor=cursor)

        self.canvas.edit_mode = "normal" if self.root["cursor"] == "" else "highlight"
        if self.canvas.edit_mode == "normal":
            return

    def set_pen(self, width, color):
        self.canvas.pen_data = {
            "width": width,
            "color": color,
            "rgb_color": webcolors.name_to_rgb(color)
        }

    def set_highlighter(self, width, color):
        self.canvas.highlighter_data = {
            "width": width,
            "color": color,
            "rgb_color": webcolors.name_to_rgb(color)
        }
