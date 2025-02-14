import tkinter as tk

import pymupdf
from PIL import ImageTk, Image


class DynamicCanvas(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.image_item = None
        self.parent = parent
        self.pdf = None
        self.img = None
        self.tkimg = None
        self.scale = 1.0

        self.drag_data = {"x": self.parent.winfo_width(),
                          "y" : self.parent.winfo_height()}

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
            self.load_page()

    def change_current_page(self, event):
        self.canvas.delete("all")

        if self.pdf.current_page is None:
            return

        self.pdf.change_page(event)
        self.load_page()
        self.canvas.update_idletasks()

    def load_page(self):
        page = self.pdf.current_page

        zoom = pymupdf.Matrix(self.scale, self.scale)
        pix = page.get_pixmap(matrix=zoom)

        self.img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

        self.tkimg = ImageTk.PhotoImage(self.img)

        self.canvas.delete("all")
        self.image_item = self.canvas.create_image(int(self.parent.winfo_width()/2), int(self.parent.winfo_height()/2), anchor=tk.CENTER, image=self.tkimg)

        self.canvas.tag_bind(self.image_item, "<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.image_item, '<B1-Motion>', self.dragging)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom(self, event):
        old_scale = self.scale
        if event.delta > 0:
            self.scale *= 1.2
        else:
            self.scale *= 0.8

        # current_x = self.canvas.canvasx(0)
        # current_y = self.canvas.canvasy(0)
        #
        # canvas_x = self.canvas.canvasx(event.x)
        # canvas_y = self.canvas.canvasy(event.y)
        #
        # rel_x = (canvas_x - current_x) / (self.tkimg.width() * self.scale)
        # rel_y = (canvas_y - current_y) / (self.tkimg.height() * self.scale)

        # delta_x = (current_x - canvas_x)
        # delta_y = (current_y - canvas_y)
        #
        # self.canvas.move(self.image_item, delta_x, delta_y)
        self.canvas.xview_moveto(event.x)
        self.canvas.yview_moveto(event.y)

        self.load_page()

        # self.canvas.xview_moveto(event.x)
        # self.canvas.yview_moveto(event.y)

        # new_x = canvas_x * (self.scale / old_scale) - event.x
        # new_y = canvas_y * (self.scale / old_scale) - event.y
        #
        # self.canvas.xview_moveto(new_x / self.tkimg.width())
        # self.canvas.yview_moveto(new_y / self.tkimg.height())

    def start_drag(self, event):
        self.drag_data = {"x": event.x,
                          "y": event.y}

    def dragging(self, event):
        deltax = event.x - self.drag_data.get("x")
        deltay = event.y - self.drag_data.get("y")

        self.canvas.move(self.image_item, deltax, deltay)

        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y