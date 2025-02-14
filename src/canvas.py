import tkinter as tk

import pymupdf
from PIL import ImageTk, Image


class DynamicCanvas(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pdf = None
        self.img = None
        self.tkimg = None
        self.scale = 1.0

        self.canvas = tk.Canvas(self)
        self.v_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.canvas.pack(expand=True, fill="both", side="left")
        self.v_scrollbar.pack(side="right", fill="y")

    def on_resize(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def draw_pdf(self, pdf):
        self.pdf = pdf

        if self.pdf is None:
            self.canvas.delete("all")
        else:
            self.draw_current_page()

    def draw_current_page(self):
        page = self.pdf.current_page
        pix = page.get_pixmap()
        self.img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(int(self.parent.winfo_width()/2), int(self.parent.winfo_height()/2), anchor=tk.CENTER, image=self.tkimg, state="normal")

    def change_current_page(self, event):
        self.canvas.delete("all")

        if self.pdf.current_page is None:
            return

        self.pdf.change_page(event)
        self.draw_current_page()
        self.canvas.update_idletasks()

    def load_page(self):
        page = self.pdf.current_page

        zoom = pymupdf.Matrix(self.scale, self.scale)
        pix = page.get_pixmap(matrix=zoom)

        self.img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

        self.tkimg = ImageTk.PhotoImage(self.img)

        self.canvas.delete("all")
        self.canvas.create_image(int(self.parent.winfo_width()/2), int(self.parent.winfo_height()/2), anchor=tk.CENTER, image=self.tkimg)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom(self, event):
        old_scale = self.scale
        if event.delta > 0:
            self.scale *= 1.2
        else:
            self.scale *= 0.8

        # current_x = self.canvas.canvasx(0)
        # current_y = self.canvas.canvasy(0)#int(self.parent.winfo_height()/2))
        #
        # canvas_x = self.canvas.canvasx(event.x)
        # canvas_y = self.canvas.canvasy(event.y)
        #
        # rel_x = (canvas_x - current_x) / (self.tkimg.width() * self.scale)
        # rel_y = (canvas_y - current_y) / (self.tkimg.height() * self.scale)

        self.load_page()

        # new_x = canvas_x * (self.scale / old_scale) - event.x
        # new_y = canvas_y * (self.scale / old_scale) - event.y
        #
        # self.canvas.xview_moveto(new_x / self.tkimg.width())
        # self.canvas.yview_moveto(new_y / self.tkimg.height())

    def drag(self, event):
        self.canvas.delete("all")
        self.canvas.create_image(event.x, event.y, anchor=tk.CENTER, image=self.tkimg)
